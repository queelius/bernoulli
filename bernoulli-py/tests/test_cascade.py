"""Tests for ``bernoulli.sets.cascade.BloomCascade``."""

from __future__ import annotations

import random

import pytest

from bernoulli.sets.bloom import BloomFilter
from bernoulli.sets.cascade import BloomCascade, _layer_salt


class TestConstruction:
    def test_basic_construction(self) -> None:
        cascade = BloomCascade([(100, 0.1), (100, 0.05)])
        assert cascade.num_layers == 2
        assert cascade.num_keys() == 0

    def test_empty_layers_rejected(self) -> None:
        with pytest.raises(ValueError):
            BloomCascade([])

    def test_invalid_layer_spec_propagates(self) -> None:
        # BloomFilter validates each (capacity, target_fpr); construction
        # must not silently accept nonsense.
        with pytest.raises(ValueError):
            BloomCascade([(0, 0.1)])
        with pytest.raises(ValueError):
            BloomCascade([(100, 0.0)])

    def test_layers_use_different_salts(self) -> None:
        """Layers must be statistically independent: different salts."""
        cascade = BloomCascade([(100, 0.1), (100, 0.1), (100, 0.1)])
        salts = {bf._salt for bf in cascade.filters}
        assert len(salts) == 3, "every layer should have a distinct salt"

    def test_layer_salt_helper_is_deterministic(self) -> None:
        # Same index -> same salt; different index -> different salt.
        assert _layer_salt(0) == _layer_salt(0)
        assert _layer_salt(0) != _layer_salt(1)


class TestAddContains:
    def test_no_false_negatives(self) -> None:
        """Every inserted key must pass ``contains`` (exact set is the truth)."""
        cascade = BloomCascade([(1000, 0.1), (1000, 0.05)])
        keys = [f"key_{i}".encode() for i in range(500)]
        for k in keys:
            cascade.add(k)
        for k in keys:
            assert cascade.contains(k), f"missed inserted key {k!r}"

    def test_no_false_negatives_via_in_operator(self) -> None:
        cascade = BloomCascade([(100, 0.1), (100, 0.05)])
        cascade.add(b"hello")
        assert b"hello" in cascade

    def test_in_operator_rejects_non_bytes(self) -> None:
        cascade = BloomCascade([(10, 0.1)])
        with pytest.raises(TypeError):
            _ = "string" in cascade  # type: ignore[operator]

    def test_contains_is_zero_fp(self) -> None:
        """Backed by an exact set; ``contains`` must NEVER report a false positive."""
        rng = random.Random(0)
        cascade = BloomCascade([(500, 0.2), (500, 0.2)])
        inserted = {rng.randbytes(8) for _ in range(500)}
        while len(inserted) < 500:
            inserted.add(rng.randbytes(8))
        for k in inserted:
            cascade.add(k)
        # Probe with non-members: contains() must say False every time.
        for _ in range(2000):
            cand = rng.randbytes(8)
            if cand in inserted:
                continue
            assert cascade.contains(cand) is False

    def test_add_all_bulk(self) -> None:
        cascade = BloomCascade([(100, 0.1), (100, 0.05)])
        cascade.add_all([b"a", b"b", b"c"])
        assert cascade.num_keys() == 3
        assert b"a" in cascade


class TestProbablyPresent:
    def test_inserted_keys_are_probably_present(self) -> None:
        cascade = BloomCascade([(200, 0.1), (200, 0.05)])
        for i in range(100):
            cascade.add(f"k{i}".encode())
        for i in range(100):
            assert cascade.probably_present(f"k{i}".encode())

    def test_probably_present_rate_matches_product(self) -> None:
        """For non-members, P(all layers say True) ~= prod of per-layer FPRs.

        This is the framework's prediction (book ch.3 AND chain) and the
        whole point of the cascade construction.
        """
        rng = random.Random(42)
        n = 5000
        target_1 = 0.10
        target_2 = 0.05
        cascade = BloomCascade([(n, target_1), (n, target_2)])

        inserted = set()
        while len(inserted) < n:
            inserted.add(rng.randbytes(16))
        for k in inserted:
            cascade.add(k)

        n_probes = 30_000
        layer1_hits = 0
        layer2_hits = 0
        all_hits = 0
        probes_done = 0
        while probes_done < n_probes:
            cand = rng.randbytes(16)
            if cand in inserted:
                continue
            l1 = cascade.filters[0].contains(cand)
            l2 = cascade.filters[1].contains(cand)
            if l1:
                layer1_hits += 1
            if l2:
                layer2_hits += 1
            if cascade.probably_present(cand):
                all_hits += 1
            probes_done += 1

        a1 = layer1_hits / probes_done
        a2 = layer2_hits / probes_done
        a_all = all_hits / probes_done
        predicted = a1 * a2

        # Allow generous tolerance: 30k probes against ~1% predicted rate
        # gives ~17 events; CI is wide. We assert ratio in a wide band.
        # The independent-channels assumption (validated in experiment 01)
        # gives ratio ~1; values 0.5-2 are well within Wilson CI for these n.
        ratio = a_all / predicted if predicted > 0 else 0.0
        assert 0.5 < ratio < 2.0, (
            f"empirical/predicted = {ratio:.3f}, a1={a1:.4g}, "
            f"a2={a2:.4g}, predicted={predicted:.4g}, empirical={a_all:.4g}"
        )

    def test_probably_present_eq_contains_for_members(self) -> None:
        """For inserted keys, both must agree (and both True)."""
        cascade = BloomCascade([(50, 0.1), (50, 0.1)])
        for i in range(20):
            cascade.add(f"x{i}".encode())
        for i in range(20):
            k = f"x{i}".encode()
            assert cascade.probably_present(k) == cascade.contains(k) is True


class TestSpaceMetrics:
    def test_memory_bytes_is_sum_of_layer_bytes(self) -> None:
        cascade = BloomCascade([(100, 0.1), (100, 0.05), (100, 0.01)])
        expected = sum(bf.memory_bytes() for bf in cascade.filters)
        assert cascade.memory_bytes() == expected

    def test_bits_per_key_is_filter_bytes_only(self) -> None:
        cascade = BloomCascade([(100, 0.1), (100, 0.05)])
        for i in range(50):
            cascade.add(f"k{i}".encode())
        expected = (cascade.memory_bytes() * 8) / 50
        assert cascade.bits_per_key() == pytest.approx(expected)

    def test_bits_per_key_empty(self) -> None:
        cascade = BloomCascade([(100, 0.1)])
        assert cascade.bits_per_key() == float("inf")

    def test_predicted_filter_fpr_is_product(self) -> None:
        """The closed-form predictor returns the product of layer FPRs."""
        cascade = BloomCascade([(100, 0.1), (100, 0.1), (100, 0.1)])
        for i in range(100):
            cascade.add(f"k{i}".encode())
        predicted = cascade.predicted_filter_fpr()
        manual = 1.0
        for bf in cascade.filters:
            manual *= bf.fpr()
        assert predicted == pytest.approx(manual)


class TestRepr:
    def test_repr_includes_layer_specs_and_count(self) -> None:
        cascade = BloomCascade([(100, 0.1), (50, 0.05)])
        cascade.add(b"k")
        text = repr(cascade)
        assert "BloomCascade" in text
        assert "n=1" in text
        assert "100" in text
        assert "50" in text


class TestThreeLayer:
    def test_three_layer_no_false_negatives(self) -> None:
        cascade = BloomCascade([(500, 0.2), (500, 0.1), (500, 0.05)])
        keys = [f"k{i}".encode() for i in range(300)]
        for k in keys:
            cascade.add(k)
        for k in keys:
            assert cascade.contains(k)

    def test_three_layer_filter_fpr_decreases_with_depth(self) -> None:
        """Adding a layer should never make the cumulative filter FPR worse."""
        cascade = BloomCascade([(200, 0.3), (200, 0.3), (200, 0.3)])
        for i in range(150):
            cascade.add(f"k{i}".encode())
        # Cumulative product over a prefix is monotonically non-increasing.
        product = 1.0
        prev = 1.0
        for bf in cascade.filters:
            product *= bf.fpr()
            assert product <= prev
            prev = product


class TestSingleLayerEquivalence:
    def test_single_layer_cascade_matches_bloom(self) -> None:
        """A 1-layer cascade should behave like a Bloom + exact set."""
        rng = random.Random(7)
        n = 200
        keys = {rng.randbytes(12) for _ in range(n)}
        while len(keys) < n:
            keys.add(rng.randbytes(12))
        cascade = BloomCascade([(n, 0.05)])
        bloom = BloomFilter(capacity=n, target_fpr=0.05, salt=_layer_salt(0))
        for k in keys:
            cascade.add(k)
            bloom.add(k)
        # On member queries: both True.
        for k in keys:
            assert cascade.probably_present(k) is True
            assert bloom.contains(k) is True
        # On non-member queries: cascade.probably_present == bloom.contains.
        agree = 0
        total = 0
        for _ in range(2000):
            cand = rng.randbytes(12)
            if cand in keys:
                continue
            total += 1
            if cascade.probably_present(cand) == bloom.contains(cand):
                agree += 1
        assert agree == total, "single-layer cascade must mirror its Bloom layer"
