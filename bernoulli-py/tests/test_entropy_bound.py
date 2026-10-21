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

    def test_phf_at_one_percent(self) -> None:
        assert math.isclose(eb.phf_bits_per_key(0.01), 7.0 + math.log2(math.e))
        assert eb.fingerprint_width(0.01) == 7

    def test_micro_fpr_row(self) -> None:
        # Book chapter 14 comparison table at fpr = 1e-6: floor ~19.93, bloom ~28.76.
        assert math.isclose(eb.entropy_floor_bits_per_key(1e-6), -math.log2(1e-6))
        assert math.isclose(
            eb.bloom_bits_per_key(1e-6), -math.log2(1e-6) / math.log(2.0)
        )
        assert math.isclose(eb.bloom_bits_per_key(1e-6), 28.76, abs_tol=1e-2)
        assert eb.phf_bits_per_key(1e-6, mphf_bits_per_key=0.0) == 20.0

    def test_bloom_overhead_bits(self) -> None:
        assert math.isclose(
            eb.bloom_overhead_bits_per_key(0.01),
            eb.bloom_bits_per_key(0.01) - eb.entropy_floor_bits_per_key(0.01),
        )

    def test_savings(self) -> None:
        assert math.isclose(
            eb.bloom_vs_phf_savings_bits(0.01),
            eb.bloom_bits_per_key(0.01) - 7.0 - math.log2(math.e),
        )

    def test_phf_with_measured_perfect_hash_cost(self) -> None:
        assert eb.phf_bits_per_key(0.01, mphf_bits_per_key=2.5) == 9.5

    def test_negative_perfect_hash_cost_raises(self) -> None:
        with pytest.raises(ValueError):
            eb.phf_bits_per_key(0.01, mphf_bits_per_key=-1.0)

    def test_mphf_lower_bound_is_log2_e(self) -> None:
        assert math.isclose(eb.MPHF_LOWER_BOUND_BITS, 1.0 / math.log(2.0))

    def test_book_crossover_example(self) -> None:
        # Book chapter 14: c = 3.23 bits per key; Bloom wins at 2^-7, the PHF at 2^-10.
        assert not eb.phf_beats_bloom(2.0 ** -7, mphf_bits_per_key=3.23)
        assert eb.phf_beats_bloom(2.0 ** -10, mphf_bits_per_key=3.23)


class TestDeprecatedAliases:
    def test_bhf_bits_per_key_warns_and_keeps_0_3_0_behavior(self) -> None:
        with pytest.warns(DeprecationWarning):
            assert eb.bhf_bits_per_key(0.01) == 7.0
        with pytest.warns(DeprecationWarning):
            assert eb.bhf_bits_per_key(0.01, perfect_hash_overhead=2.5) == 9.5
        with pytest.warns(DeprecationWarning), pytest.raises(ValueError):
            eb.bhf_bits_per_key(0.01, perfect_hash_overhead=-1.0)

    def test_bloom_vs_bhf_savings_warns_and_keeps_0_3_0_behavior(self) -> None:
        with pytest.warns(DeprecationWarning):
            assert math.isclose(
                eb.bloom_vs_bhf_savings_bits(0.01), eb.bloom_bits_per_key(0.01) - 7.0
            )

    def test_compare_accepts_the_0_3_0_keyword_with_a_warning(self) -> None:
        with pytest.warns(DeprecationWarning):
            c = eb.compare(0.01, perfect_hash_overhead=2.5)
        assert c.phf_bits_per_key == 9.5

    def test_comparison_bhf_properties_alias_phf_fields(self) -> None:
        c = eb.compare(0.01, mphf_bits_per_key=2.0)
        assert c.bhf_bits_per_key == c.phf_bits_per_key == 9.0
        assert c.bhf_efficiency == c.phf_efficiency


class TestCompare:
    def test_compare_at_one_percent(self) -> None:
        c = eb.compare(0.01)
        assert math.isclose(c.floor_bits_per_key, -math.log2(0.01))
        assert math.isclose(c.bloom_bits_per_key, -math.log2(0.01) / math.log(2.0))
        assert math.isclose(c.phf_bits_per_key, 7.0 + math.log2(math.e))
        assert math.isclose(c.bloom_efficiency, math.log(2.0), abs_tol=1e-9)
        # At 1% a PHF at the perfect-hash lower bound still beats Bloom (8.44 vs 9.59).
        assert c.phf_efficiency > c.bloom_efficiency


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
    def test_phf_at_least_floor_plus_perfect_hash_bound(self, fpr: float) -> None:
        floor = eb.entropy_floor_bits_per_key(fpr)
        assert eb.phf_bits_per_key(fpr) >= floor + eb.MPHF_LOWER_BOUND_BITS - 1e-12

    @given(fpr_st, fpr_st)
    def test_floor_monotone_decreasing(self, f1: float, f2: float) -> None:
        lo, hi = min(f1, f2), max(f1, f2)
        # Higher FPR costs no more bits than a lower FPR.
        assert (
            eb.entropy_floor_bits_per_key(hi)
            <= eb.entropy_floor_bits_per_key(lo) + 1e-12
        )

    @given(
        st.floats(min_value=1e-12, max_value=0.5),
        st.floats(min_value=0.0, max_value=6.0, allow_nan=False),
    )
    def test_phf_beats_bloom_is_the_exact_space_comparison(self, fpr: float, c: float) -> None:
        expected = eb.phf_bits_per_key(fpr, c) < eb.bloom_bits_per_key(fpr)
        assert eb.phf_beats_bloom(fpr, c) is expected

    @given(st.integers(min_value=1, max_value=40), st.floats(min_value=0.0, max_value=6.0))
    def test_crossover_rule_at_integer_widths(self, r: int, c: float) -> None:
        # At fpr = 2^-r the fingerprint ceiling is exact, so the book's rule
        # (log2(e) - 1) * log2(1/fpr) > c decides the winner (ties excluded).
        slack = (eb.MPHF_LOWER_BOUND_BITS - 1.0) * r
        if abs(slack - c) > 1e-9:
            assert eb.phf_beats_bloom(2.0 ** -r, c) is (slack > c)
