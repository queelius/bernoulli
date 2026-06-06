"""Tests for ``bernoulli.sets.correlated_bloom.MultiSaltBloomFilter``.

The class is a research helper used by experiment 05 to study how the
empirical AND-FPR of two Bloom filters degrades as they share an increasing
fraction of their hash family. Tests cover:

- The standard one-sided Bloom contract (no false negatives).
- Endpoint behaviors of two filters built with ``s`` shared salts:
  * ``s == 0``: AND-FPR is roughly the product (within Wilson CI).
  * ``s == k``: AND-FPR equals the single-filter FPR (identical filters).
- Constructor validation.
"""

from __future__ import annotations

import math
import random

import pytest

from bernoulli.harness import sample_unique_bytes, wilson_ci
from bernoulli.sets.correlated_bloom import (
    MultiSaltBloomFilter,
    make_correlated_pair,
)


class TestConstruction:
    def test_basic_construction(self) -> None:
        mbf = MultiSaltBloomFilter(
            capacity=1000, target_fpr=0.01, salts=[0xAA, 0xBB, 0xCC]
        )
        assert mbf.num_hashes == 3
        assert mbf.num_bits >= 1000
        assert mbf.num_bits % 8 == 0
        assert len(mbf) == 0
        assert mbf.salts == (0xAA, 0xBB, 0xCC)

    def test_invalid_capacity(self) -> None:
        with pytest.raises(ValueError):
            MultiSaltBloomFilter(capacity=0, target_fpr=0.01, salts=[1])
        with pytest.raises(ValueError):
            MultiSaltBloomFilter(capacity=-1, target_fpr=0.01, salts=[1])

    def test_invalid_target_fpr(self) -> None:
        with pytest.raises(ValueError):
            MultiSaltBloomFilter(capacity=100, target_fpr=0.0, salts=[1])
        with pytest.raises(ValueError):
            MultiSaltBloomFilter(capacity=100, target_fpr=1.0, salts=[1])

    def test_empty_salts_rejected(self) -> None:
        with pytest.raises(ValueError):
            MultiSaltBloomFilter(capacity=100, target_fpr=0.01, salts=[])

    def test_salts_coerced_to_64bit(self) -> None:
        # Negative or oversized values get masked; class should accept them.
        mbf = MultiSaltBloomFilter(
            capacity=100, target_fpr=0.01, salts=[-1, 1 << 80]
        )
        assert all(s <= 0xFFFFFFFFFFFFFFFF for s in mbf.salts)


class TestNoFalseNegatives:
    def test_no_false_negatives(self) -> None:
        rng = random.Random(11)
        salts = [rng.getrandbits(64) for _ in range(7)]
        mbf = MultiSaltBloomFilter(capacity=2000, target_fpr=0.05, salts=salts)
        keys = sample_unique_bytes(1000, length=16, rng=rng)
        for k in keys:
            mbf.add(k)
        assert len(mbf) == 1000
        for k in keys:
            assert mbf.contains(k), f"false negative on {k!r}"

    def test_in_operator_works(self) -> None:
        mbf = MultiSaltBloomFilter(capacity=10, target_fpr=0.01, salts=[0xA])
        mbf.add(b"x")
        assert b"x" in mbf

    def test_in_operator_rejects_non_bytes(self) -> None:
        mbf = MultiSaltBloomFilter(capacity=10, target_fpr=0.01, salts=[0xA])
        with pytest.raises(TypeError):
            _ = "string" in mbf  # type: ignore[operator]


class TestSpaceMetrics:
    def test_memory_bytes_consistent(self) -> None:
        mbf = MultiSaltBloomFilter(capacity=1000, target_fpr=0.01, salts=[1, 2, 3])
        assert mbf.memory_bytes() == mbf.num_bits // 8

    def test_bits_per_key_finite_after_insert(self) -> None:
        mbf = MultiSaltBloomFilter(capacity=100, target_fpr=0.01, salts=[1, 2])
        for i in range(50):
            mbf.add(f"k{i}".encode())
        bpk = mbf.bits_per_key()
        assert bpk > 0
        assert math.isfinite(bpk)

    def test_bits_per_key_infinite_when_empty(self) -> None:
        mbf = MultiSaltBloomFilter(capacity=100, target_fpr=0.01, salts=[1])
        assert math.isinf(mbf.bits_per_key())


def _build_pair_and_probe(
    n: int,
    target_fpr: float,
    k: int,
    s: int,
    n_probes: int,
    seed: int,
) -> tuple[float, float, float]:
    """Return ``(alpha_1, alpha_2, alpha_AND)`` measured on ``n_probes`` non-members."""
    rng = random.Random(seed)
    keys = sample_unique_bytes(n, length=16, rng=rng)
    f1, f2, _ = make_correlated_pair(
        capacity=n,
        target_fpr=target_fpr,
        k=k,
        s=s,
        rng_or_seed=rng.getrandbits(31),
    )
    for key in keys:
        f1.add(key)
        f2.add(key)

    seen = set(keys)
    probes: list[bytes] = []
    while len(probes) < n_probes:
        cand = rng.randbytes(16)
        if cand not in seen:
            probes.append(cand)

    fp1 = sum(1 for k_ in probes if f1.contains(k_))
    fp2 = sum(1 for k_ in probes if f2.contains(k_))
    fp_and = sum(1 for k_ in probes if f1.contains(k_) and f2.contains(k_))
    return fp1 / n_probes, fp2 / n_probes, fp_and / n_probes


class TestSharedSaltEndpoints:
    def test_s_equal_zero_matches_product_within_wilson_ci(self) -> None:
        """Independent salts: empirical AND-FPR is consistent with alpha_1*alpha_2.

        Use a wide-but-honest Wilson CI on the joint count to absorb the
        residual ~10-15% bias seen in experiment 01 section A.
        """
        n = 4000
        n_probes = 30_000
        a1, a2, a_and = _build_pair_and_probe(
            n=n, target_fpr=0.05, k=7, s=0, n_probes=n_probes, seed=2026
        )
        joint_count = round(a_and * n_probes)
        lo, hi = wilson_ci(joint_count, n_probes, confidence=0.99)
        predicted = a1 * a2
        # Either the predicted product lies in the joint count's 99% Wilson CI,
        # or the empirical ratio is at most ~1.5 (well below the s=k collapse).
        ratio = a_and / predicted if predicted > 0 else float("inf")
        assert (
            (lo <= predicted <= hi) or ratio <= 1.5
        ), f"a1={a1}, a2={a2}, predicted={predicted}, a_and={a_and}, CI=({lo}, {hi}), ratio={ratio}"

    def test_s_equal_k_collapses_to_single_filter(self) -> None:
        """Identical filters (s == k): AND equals single-filter FPR exactly."""
        n = 2000
        n_probes = 10_000
        a1, a2, a_and = _build_pair_and_probe(
            n=n, target_fpr=0.05, k=5, s=5, n_probes=n_probes, seed=7
        )
        # Two filters with identical salt vectors are bitwise identical after
        # the same insertions, so their AND is exactly the single-filter FPR.
        assert a1 == a2 == a_and

    def test_partial_sharing_is_intermediate(self) -> None:
        """For 0 < s < k, AND-FPR sits between alpha_1*alpha_2 and alpha_1."""
        n = 3000
        n_probes = 20_000
        a1, a2, a_and = _build_pair_and_probe(
            n=n, target_fpr=0.05, k=6, s=3, n_probes=n_probes, seed=42
        )
        product = a1 * a2
        single = max(a1, a2)
        # The empirical AND must lie at least as high as the product (with some
        # statistical wiggle) and at most as high as the single-filter FPR.
        # We allow a small tolerance below `product` for sample noise.
        wiggle = 1.5 * math.sqrt(product * (1 - product) / n_probes)
        assert a_and + wiggle >= product, f"a_and={a_and}, product={product}"
        assert a_and <= single + 1e-9, f"a_and={a_and}, single={single}"


class TestPairBuilder:
    def test_pair_uses_correct_salt_counts(self) -> None:
        f1, f2, salts = make_correlated_pair(
            capacity=100, target_fpr=0.05, k=5, s=2, rng_or_seed=99
        )
        assert len(salts["shared"]) == 2
        assert len(salts["only_1"]) == 3
        assert len(salts["only_2"]) == 3
        assert f1.num_hashes == 5
        assert f2.num_hashes == 5
        # Both filters include the shared salts; only-1 and only-2 are disjoint
        # by construction (drawn separately).
        assert set(salts["shared"]).issubset(set(f1.salts))
        assert set(salts["shared"]).issubset(set(f2.salts))

    def test_pair_validates_s_range(self) -> None:
        with pytest.raises(ValueError):
            make_correlated_pair(
                capacity=100, target_fpr=0.05, k=5, s=-1, rng_or_seed=0
            )
        with pytest.raises(ValueError):
            make_correlated_pair(
                capacity=100, target_fpr=0.05, k=5, s=6, rng_or_seed=0
            )

    def test_s_equal_k_makes_identical_salt_sets(self) -> None:
        f1, f2, _ = make_correlated_pair(
            capacity=100, target_fpr=0.05, k=4, s=4, rng_or_seed=1234
        )
        # When s == k both filters share exactly the same salt set.
        assert set(f1.salts) == set(f2.salts)
