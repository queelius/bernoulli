"""Tests for ``bernoulli.sets.entropy_bound`` (book chapters 8 and 14)."""

from __future__ import annotations

import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from bernoulli.sets import entropy_bound as eb

fpr_st = st.floats(
    min_value=1e-9, max_value=1.0, allow_nan=False, allow_infinity=False
)


class TestWorkedExamples:
    def test_floor_at_one_percent(self) -> None:
        assert math.isclose(eb.entropy_floor_bits_per_key(0.01), -math.log2(0.01))
        assert math.isclose(eb.entropy_floor_bits_per_key(0.01), 6.643856, abs_tol=1e-5)

    def test_bloom_at_one_percent(self) -> None:
        assert math.isclose(
            eb.bloom_bits_per_key(0.01), -math.log2(0.01) / math.log(2.0)
        )
        assert math.isclose(eb.bloom_bits_per_key(0.01), 9.585, abs_tol=2e-3)

    def test_bhf_at_one_percent(self) -> None:
        assert eb.bhf_bits_per_key(0.01) == 7.0
        assert eb.fingerprint_width(0.01) == 7

    def test_micro_fpr_row(self) -> None:
        # Book chapter 14 comparison table at fpr = 1e-6: floor ~19.93, bloom ~28.76.
        assert math.isclose(eb.entropy_floor_bits_per_key(1e-6), -math.log2(1e-6))
        assert math.isclose(
            eb.bloom_bits_per_key(1e-6), -math.log2(1e-6) / math.log(2.0)
        )
        assert math.isclose(eb.bloom_bits_per_key(1e-6), 28.76, abs_tol=1e-2)
        assert eb.bhf_bits_per_key(1e-6) == 20.0

    def test_bloom_overhead_bits(self) -> None:
        assert math.isclose(
            eb.bloom_overhead_bits_per_key(0.01),
            eb.bloom_bits_per_key(0.01) - eb.entropy_floor_bits_per_key(0.01),
        )

    def test_savings(self) -> None:
        assert math.isclose(
            eb.bloom_vs_bhf_savings_bits(0.01),
            eb.bloom_bits_per_key(0.01) - 7.0,
        )

    def test_bhf_with_perfect_hash_overhead(self) -> None:
        assert eb.bhf_bits_per_key(0.01, perfect_hash_overhead=2.5) == 9.5

    def test_negative_overhead_raises(self) -> None:
        with pytest.raises(ValueError):
            eb.bhf_bits_per_key(0.01, perfect_hash_overhead=-1.0)


class TestCompare:
    def test_compare_at_one_percent(self) -> None:
        c = eb.compare(0.01)
        assert math.isclose(c.floor_bits_per_key, -math.log2(0.01))
        assert math.isclose(c.bloom_bits_per_key, -math.log2(0.01) / math.log(2.0))
        assert c.bhf_bits_per_key == 7.0
        assert math.isclose(c.bloom_efficiency, math.log(2.0), abs_tol=1e-9)
        assert c.bhf_efficiency > c.bloom_efficiency


class TestProperties:
    @given(st.floats(min_value=1e-9, max_value=0.999, allow_nan=False, allow_infinity=False))
    def test_bloom_efficiency_is_ln2(self, fpr: float) -> None:
        # Excludes fpr == 1, where the floor is 0 and efficiency is undefined.
        eff = eb.efficiency(eb.bloom_bits_per_key(fpr), fpr)
        assert math.isclose(eff, math.log(2.0), rel_tol=1e-9)

    @given(st.floats(min_value=1e-9, max_value=0.499))
    def test_bloom_exceeds_floor(self, fpr: float) -> None:
        assert eb.bloom_bits_per_key(fpr) > eb.entropy_floor_bits_per_key(fpr)

    @given(fpr_st)
    def test_fingerprint_width_meets_target(self, fpr: float) -> None:
        r = eb.fingerprint_width(fpr)
        assert 2.0 ** (-r) <= fpr + 1e-15

    @given(fpr_st)
    def test_bhf_at_least_floor(self, fpr: float) -> None:
        assert eb.bhf_bits_per_key(fpr) >= eb.entropy_floor_bits_per_key(fpr) - 1e-12

    @given(fpr_st, fpr_st)
    def test_floor_monotone_decreasing(self, f1: float, f2: float) -> None:
        lo, hi = min(f1, f2), max(f1, f2)
        # Higher FPR costs no more bits than a lower FPR.
        assert (
            eb.entropy_floor_bits_per_key(hi)
            <= eb.entropy_floor_bits_per_key(lo) + 1e-12
        )

    @given(st.floats(min_value=1e-9, max_value=0.1))
    def test_bhf_more_efficient_than_bloom(self, fpr: float) -> None:
        # The BHF beats Bloom only for strict enough targets: near integer
        # bit-widths its ceiling rounding can cost a full bit and lose to
        # Bloom's 1.44x. Holds comfortably for fpr <= 0.1 (floor >= 3.32 bits).
        floor = eb.entropy_floor_bits_per_key(fpr)
        bhf_eff = floor / eb.bhf_bits_per_key(fpr)
        bloom_eff = floor / eb.bloom_bits_per_key(fpr)
        assert bhf_eff >= bloom_eff - 1e-12
