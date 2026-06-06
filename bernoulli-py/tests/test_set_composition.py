"""Tests for ``bernoulli.sets.composition`` (book chapter 6).

Worked examples match the book; property tests use hypothesis to check the
structural invariants of the three-region rate formulas.
"""

from __future__ import annotations

import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from bernoulli.sets.composition import (
    Partition,
    SetRates,
    complement,
    difference,
    intersection,
    union,
)

# ---------------------------------------------------------------------------
# strategies
# ---------------------------------------------------------------------------

rate_st = st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)
set_rates_st = st.builds(SetRates, fpr=rate_st, fnr=rate_st)


@st.composite
def partitions(draw: st.DrawFn) -> Partition:
    masses = [draw(st.floats(min_value=0.0, max_value=1.0)) for _ in range(4)]
    if sum(masses) <= 0.0:
        masses[0] = 1.0
    return Partition.from_masses(*masses)


# ---------------------------------------------------------------------------
# SetRates / Partition validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_set_rates_rejects_out_of_range(self) -> None:
        with pytest.raises(ValueError):
            SetRates(fpr=1.5)
        with pytest.raises(ValueError):
            SetRates(fnr=-0.1)

    def test_partition_rejects_bad_sum(self) -> None:
        with pytest.raises(ValueError):
            Partition(both=0.5, a_only=0.5, b_only=0.5, neither=0.5)

    def test_from_masses_normalizes(self) -> None:
        p = Partition.from_masses(1, 1, 1, 1)
        assert math.isclose(p.both, 0.25)
        assert math.isclose(p.both + p.a_only + p.b_only + p.neither, 1.0)

    def test_from_masses_all_zero_raises(self) -> None:
        with pytest.raises(ValueError):
            Partition.from_masses(0, 0, 0, 0)


# ---------------------------------------------------------------------------
# complement
# ---------------------------------------------------------------------------


class TestComplement:
    def test_swaps_axes(self) -> None:
        assert complement(SetRates(fpr=0.01, fnr=0.05)).rates == (0.05, 0.01)

    @given(set_rates_st)
    def test_involutive(self, a: SetRates) -> None:
        assert complement(complement(a)) == a


# ---------------------------------------------------------------------------
# union
# ---------------------------------------------------------------------------


class TestUnion:
    def test_fpr_is_single_region_product_form(self) -> None:
        a = SetRates.one_sided_fpr(0.01)
        b = SetRates.one_sided_fpr(0.02)
        u = union(a, b, Partition.sparse())
        assert math.isclose(u.fpr, 1.0 - 0.99 * 0.98)
        assert u.fnr == 0.0

    def test_fnr_three_region(self) -> None:
        # Two-sided operands; members split equally across the three cells.
        a = SetRates(fpr=0.01, fnr=0.10)
        b = SetRates(fpr=0.02, fnr=0.20)
        p = Partition(both=1 / 3, a_only=1 / 3, b_only=1 / 3, neither=0.0)
        u = union(a, b, p)
        expected = (
            (1 / 3) * 0.10 * (1 - 0.02)
            + (1 / 3) * 0.20 * (1 - 0.01)
            + (1 / 3) * 0.10 * 0.20
        )
        assert math.isclose(u.fnr, expected)

    @given(set_rates_st, set_rates_st, partitions())
    def test_fpr_at_least_each_operand(self, a: SetRates, b: SetRates, p: Partition) -> None:
        u = union(a, b, p)
        assert u.fpr >= a.fpr - 1e-12
        assert u.fpr >= b.fpr - 1e-12

    @given(rate_st, rate_st, partitions())
    def test_fnr_zero_operands_stay_fnr_zero(
        self, fa: float, fb: float, p: Partition
    ) -> None:
        u = union(SetRates.one_sided_fpr(fa), SetRates.one_sided_fpr(fb), p)
        assert u.fnr == 0.0


# ---------------------------------------------------------------------------
# intersection
# ---------------------------------------------------------------------------


class TestIntersection:
    def test_sparse_limit_is_bare_product(self) -> None:
        a = SetRates.one_sided_fpr(0.01)
        b = SetRates.one_sided_fpr(0.01)
        assert math.isclose(intersection(a, b, Partition.sparse()).fpr, 1e-4)

    def test_single_missing_keyword_region_is_single_rate(self) -> None:
        # A query in A only (not in B) is a false positive at rate fpr_B alone,
        # not fpr_A * fpr_B.
        a = SetRates.one_sided_fpr(0.01)
        b = SetRates.one_sided_fpr(0.05)
        p = Partition(both=0.0, a_only=1.0, b_only=0.0, neither=0.0)
        assert math.isclose(intersection(a, b, p).fpr, 0.05)

    def test_fnr_is_single_region_product_form(self) -> None:
        a = SetRates(fpr=0.01, fnr=0.10)
        b = SetRates(fpr=0.02, fnr=0.20)
        i = intersection(a, b, Partition.from_masses(1, 1, 1, 1))
        assert math.isclose(i.fnr, 1.0 - 0.90 * 0.80)

    @given(rate_st, rate_st, partitions())
    def test_fpr_bounded_by_worst_operand(
        self, fa: float, fb: float, p: Partition
    ) -> None:
        # For FNR-zero operands the three-region FPR is a convex combination of
        # fpr_B, fpr_A, fpr_A*fpr_B, hence at most max(fpr_A, fpr_B).
        i = intersection(SetRates.one_sided_fpr(fa), SetRates.one_sided_fpr(fb), p)
        assert i.fpr <= max(fa, fb) + 1e-12

    @given(rate_st, rate_st, partitions())
    def test_fnr_zero_operands_stay_fnr_zero(
        self, fa: float, fb: float, p: Partition
    ) -> None:
        i = intersection(SetRates.one_sided_fpr(fa), SetRates.one_sided_fpr(fb), p)
        assert i.fnr == 0.0


# ---------------------------------------------------------------------------
# difference
# ---------------------------------------------------------------------------


class TestDifference:
    def test_difference_of_fnr_zero_sets_is_two_sided(self) -> None:
        # Book section 6.2: A minus B of two Bloom-style sets is two-sided.
        a = SetRates.one_sided_fpr(0.01)
        b = SetRates.one_sided_fpr(0.02)
        d = difference(a, b, Partition.from_masses(1, 1, 1, 1))
        assert d.fnr > 0.0

    def test_difference_fnr_matches_closed_form(self) -> None:
        # FNR of A minus B = 1 - (1 - fnr_A)(1 - fpr_B).
        a = SetRates(fpr=0.01, fnr=0.10)
        b = SetRates(fpr=0.05, fnr=0.20)
        d = difference(a, b, Partition.from_masses(1, 1, 1, 1))
        assert math.isclose(d.fnr, 1.0 - (1 - 0.10) * (1 - 0.05))


# ---------------------------------------------------------------------------
# cross-cutting property: composition never produces invalid rates
# ---------------------------------------------------------------------------


@given(set_rates_st, set_rates_st, partitions())
def test_all_ops_produce_valid_rates(a: SetRates, b: SetRates, p: Partition) -> None:
    for op in (union, intersection, difference):
        r = op(a, b, p)  # SetRates.__post_init__ raises if out of [0, 1]
        assert 0.0 <= r.fpr <= 1.0
        assert 0.0 <= r.fnr <= 1.0
