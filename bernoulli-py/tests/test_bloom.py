"""Tests for ``bernoulli.sets.bloom.BloomFilter``."""

from __future__ import annotations

import random

import pytest

from bernoulli.atom import BernoulliBool
from bernoulli.sets import BloomFilter


class TestConstruction:
    def test_basic_construction(self) -> None:
        bf = BloomFilter(capacity=1000, target_fpr=0.01)
        assert bf.num_bits >= 1000  # at least n bits for any reasonable FPR
        assert bf.num_hashes >= 1
        assert len(bf) == 0

    def test_invalid_capacity(self) -> None:
        with pytest.raises(ValueError):
            BloomFilter(capacity=0, target_fpr=0.01)
        with pytest.raises(ValueError):
            BloomFilter(capacity=-5, target_fpr=0.01)

    def test_invalid_fpr(self) -> None:
        with pytest.raises(ValueError):
            BloomFilter(capacity=100, target_fpr=0.0)
        with pytest.raises(ValueError):
            BloomFilter(capacity=100, target_fpr=1.0)
        with pytest.raises(ValueError):
            BloomFilter(capacity=100, target_fpr=-0.1)

    def test_independent_salts_differ(self) -> None:
        bf1 = BloomFilter(capacity=100, target_fpr=0.01, salt=0)
        bf2 = BloomFilter(capacity=100, target_fpr=0.01, salt=1)
        for k in (b"a", b"b", b"c", b"long-key"):
            bf1.add(k)
            bf2.add(k)
        # Different salts should give different bit patterns (with high prob).
        assert bf1._bits != bf2._bits


class TestAddContains:
    def test_no_false_negatives(self) -> None:
        bf = BloomFilter(capacity=1000, target_fpr=0.01)
        keys = [f"key_{i}".encode() for i in range(500)]
        for k in keys:
            bf.add(k)
        for k in keys:
            assert bf.contains(k), f"missed key {k!r} (false negative!)"

    def test_membership_via_in_operator(self) -> None:
        bf = BloomFilter(capacity=10, target_fpr=0.01)
        bf.add(b"hello")
        assert b"hello" in bf
        # b"world" may or may not be a false positive; we only assert no FN.

    def test_in_operator_rejects_non_bytes(self) -> None:
        bf = BloomFilter(capacity=10, target_fpr=0.01)
        with pytest.raises(TypeError):
            _ = "string" in bf  # type: ignore[operator]


class TestQueryReturnsBernoulli:
    def test_query_returns_bernoulli_bool(self) -> None:
        bf = BloomFilter(capacity=100, target_fpr=0.01)
        bf.add(b"x")
        b = bf.query(b"x")
        assert isinstance(b, BernoulliBool)
        assert b.value is True
        assert b.fnr == 0.0  # one-sided

    def test_query_for_unknown_key(self) -> None:
        bf = BloomFilter(capacity=100, target_fpr=0.01)
        bf.add(b"present")
        b = bf.query(b"absent_with_high_probability_xyz")
        assert isinstance(b, BernoulliBool)
        assert b.fnr == 0.0


class TestEmpiricalFpr:
    def test_empirical_fpr_close_to_target(self) -> None:
        """At design load, empirical FPR should be near the target rate."""
        rng = random.Random(0)
        target = 0.05
        n = 5000
        bf = BloomFilter(capacity=n, target_fpr=target)
        # Insert exactly n distinct keys (random bytes).
        inserted = {rng.randbytes(16) for _ in range(n)}
        while len(inserted) < n:
            inserted.add(rng.randbytes(16))
        for k in inserted:
            bf.add(k)
        # Probe a large set of unrelated keys.
        probes = []
        while len(probes) < 20_000:
            cand = rng.randbytes(16)
            if cand not in inserted:
                probes.append(cand)
        false_positives = sum(1 for k in probes if bf.contains(k))
        empirical_fpr = false_positives / len(probes)
        # Allow generous tolerance: BloomFilter formula gives an asymptotic value.
        # At n_eff = n, the formula prediction is the bound.
        assert abs(empirical_fpr - target) < 0.02


class TestProtocolSatisfaction:
    def test_satisfies_membership_oracle(self) -> None:
        from bernoulli.sets import MembershipOracle

        bf = BloomFilter(capacity=10, target_fpr=0.01)
        assert isinstance(bf, MembershipOracle)


class TestSpaceMetrics:
    def test_bits_per_key_after_insertion(self) -> None:
        bf = BloomFilter(capacity=100, target_fpr=0.01)
        for i in range(50):
            bf.add(f"k{i}".encode())
        bpk = bf.bits_per_key()
        # For target FPR 0.01, optimal Bloom uses ~9.6 bits/key (1.44 * log2(100)).
        # With actual_inserted < capacity, bpk is higher.
        assert bpk > 0
        # Sanity bounds: not absurd.
        assert 5 < bpk < 100

    def test_memory_bytes_consistent(self) -> None:
        bf = BloomFilter(capacity=1000, target_fpr=0.01)
        assert bf.memory_bytes() == bf.num_bits // 8
