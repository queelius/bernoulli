"""Tests for ``bernoulli.sketches.hyperloglog.HyperLogLog``."""

from __future__ import annotations

import math

import pytest

from bernoulli.sketches import HyperLogLog


class TestConstruction:
    def test_basic_construction(self) -> None:
        hll = HyperLogLog(precision=10)
        assert hll.m == 1024
        assert hll.bits_per_register() == 6
        assert all(r == 0 for r in hll._registers)

    def test_invalid_precision(self) -> None:
        with pytest.raises(ValueError):
            HyperLogLog(precision=3)
        with pytest.raises(ValueError):
            HyperLogLog(precision=20)

    def test_expected_relative_error(self) -> None:
        for p in (10, 12, 14, 16):
            hll = HyperLogLog(precision=p)
            m = 1 << p
            expected = 1.04 / math.sqrt(m)
            assert hll.expected_relative_error() == pytest.approx(expected)


class TestAccuracy:
    def test_small_set_accuracy(self) -> None:
        """100 items: well inside the small-range (linear counting) regime."""
        hll = HyperLogLog(precision=12)
        for i in range(100):
            hll.add(f"item_{i}".encode())
        est = hll.count()
        rel_err = abs(est - 100) / 100
        assert rel_err < 0.05, f"relative error {rel_err:.4f} exceeds 5%"

    def test_medium_set_accuracy(self) -> None:
        """10k items at precision 12 (sigma_rel ~ 1.6%): within 5%."""
        hll = HyperLogLog(precision=12)
        for i in range(10_000):
            hll.add(f"item_{i}".encode())
        est = hll.count()
        rel_err = abs(est - 10_000) / 10_000
        assert rel_err < 0.05, f"relative error {rel_err:.4f} exceeds 5%"

    def test_large_set_accuracy_p14(self) -> None:
        """100k items at precision 14 (sigma_rel ~ 0.81%): within 2%."""
        hll = HyperLogLog(precision=14)
        for i in range(100_000):
            hll.add(f"v={i}".encode())
        est = hll.count()
        rel_err = abs(est - 100_000) / 100_000
        assert rel_err < 0.02, f"relative error {rel_err:.4f} exceeds 2%"


class TestMerge:
    def test_merge_disjoint(self) -> None:
        hll_a = HyperLogLog(precision=12)
        hll_b = HyperLogLog(precision=12)
        for i in range(5_000):
            hll_a.add(f"a_{i}".encode())
        for i in range(5_000):
            hll_b.add(f"b_{i}".encode())
        merged = hll_a.merge(hll_b)
        est = merged.count()
        true_union = 10_000
        rel_err = abs(est - true_union) / true_union
        assert rel_err < 0.05, f"merge relative error {rel_err:.4f} exceeds 5%"

    def test_merge_idempotent(self) -> None:
        """Merging an HLL with itself should give roughly the same count."""
        hll = HyperLogLog(precision=12)
        for i in range(5_000):
            hll.add(f"x_{i}".encode())
        merged = hll.merge(hll)
        assert merged.count() == pytest.approx(hll.count())

    def test_merge_precision_mismatch(self) -> None:
        a = HyperLogLog(precision=10)
        b = HyperLogLog(precision=12)
        with pytest.raises(ValueError):
            a.merge(b)

    def test_merge_salt_mismatch(self) -> None:
        a = HyperLogLog(precision=10, salt=1)
        b = HyperLogLog(precision=10, salt=2)
        with pytest.raises(ValueError):
            a.merge(b)


class TestEmptyAndDuplicates:
    def test_empty_count(self) -> None:
        hll = HyperLogLog(precision=10)
        # Empty: small-range correction with zeros == m gives log(m/m) = 0.
        assert hll.count() == 0.0

    def test_duplicates_dont_inflate(self) -> None:
        hll = HyperLogLog(precision=12)
        for _ in range(1000):
            hll.add(b"same_key")
        est = hll.count()
        # Should estimate ~1, well within the small-range regime.
        assert est < 5.0
