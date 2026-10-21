"""Tests for ``bernoulli.atom.BernoulliBool``."""

from __future__ import annotations

import math
import random

import pytest

from bernoulli import BernoulliBool


class TestConstruction:
    def test_default_rates_are_zero(self) -> None:
        b = BernoulliBool(value=True)
        assert b.fpr == 0.0
        assert b.fnr == 0.0

    def test_rates_validated(self) -> None:
        with pytest.raises(ValueError):
            BernoulliBool(value=True, fpr=-0.1)
        with pytest.raises(ValueError):
            BernoulliBool(value=True, fpr=1.5)
        with pytest.raises(ValueError):
            BernoulliBool(value=True, fnr=-0.01)
        with pytest.raises(ValueError):
            BernoulliBool(value=True, fnr=2.0)

    def test_frozen(self) -> None:
        b = BernoulliBool(value=True, fpr=0.1, fnr=0.05)
        with pytest.raises((AttributeError, Exception)):
            b.value = False  # type: ignore[misc]

    def test_rates_property(self) -> None:
        b = BernoulliBool(value=True, fpr=0.3, fnr=0.4)
        assert b.rates == (0.3, 0.4)

    def test_certain_constructor(self) -> None:
        b = BernoulliBool.certain(True)
        assert b.value is True and b.fpr == 0.0 and b.fnr == 0.0
        assert b.is_certain

    def test_from_bsc(self) -> None:
        b = BernoulliBool.from_bsc(value=False, crossover=0.05)
        assert b.fpr == 0.05 and b.fnr == 0.05

    def test_one_sided_fpr_constructor(self) -> None:
        b = BernoulliBool.one_sided_fpr(value=True, fpr=0.25)
        assert b.fnr == 0.0 and b.fpr == 0.25
        assert b.is_one_sided_fpr

    def test_one_sided_fnr_constructor(self) -> None:
        b = BernoulliBool.one_sided_fnr(value=False, fnr=0.1)
        assert b.fpr == 0.0 and b.fnr == 0.1
        assert b.is_one_sided_fnr


class TestNot:
    def test_swaps_rates(self) -> None:
        b = BernoulliBool(value=True, fpr=0.1, fnr=0.2)
        nb = ~b
        assert nb.value is False
        assert nb.fpr == 0.2
        assert nb.fnr == 0.1

    def test_involutive(self) -> None:
        b = BernoulliBool(value=True, fpr=0.13, fnr=0.27)
        assert ~~b == b

    def test_NOT_alias(self) -> None:
        b = BernoulliBool(value=True, fpr=0.1, fnr=0.2)
        assert b.NOT() == ~b


class TestAnd:
    def test_distribution_free_fnr(self) -> None:
        b1 = BernoulliBool(value=True, fpr=0.1, fnr=0.05)
        b2 = BernoulliBool(value=True, fpr=0.08, fnr=0.12)
        result = b1 & b2
        # fnr = 0.05 + 0.12 - 0.05*0.12 = 0.164
        assert math.isclose(result.fnr, 0.164, abs_tol=1e-12)

    def test_value_is_logical_and(self) -> None:
        a = BernoulliBool(value=True)
        b = BernoulliBool(value=False)
        c = BernoulliBool(value=True)
        assert (a & b).value is False
        assert (a & c).value is True
        assert (b & b).value is False

    def test_one_sided_fpr_and_is_exact_product(self) -> None:
        # Miller-Rabin pattern: both inputs have fnr=0; AND has fpr = a1*a2.
        b1 = BernoulliBool.one_sided_fpr(True, fpr=0.25)
        b2 = BernoulliBool.one_sided_fpr(True, fpr=0.25)
        result = b1 & b2
        assert result.fnr == 0.0
        assert math.isclose(result.fpr, 0.0625, abs_tol=1e-12)

    def test_general_and_is_shared_truth_product(self) -> None:
        # Shared-truth semantics: FPR = alpha_1 * alpha_2 always.
        b1 = BernoulliBool(value=True, fpr=0.10, fnr=0.05)
        b2 = BernoulliBool(value=True, fpr=0.08, fnr=0.12)
        result = b1 & b2
        assert math.isclose(result.fpr, 0.10 * 0.08)

    def test_AND_alias(self) -> None:
        b1 = BernoulliBool(value=True, fpr=0.1, fnr=0.05)
        b2 = BernoulliBool(value=True, fpr=0.2, fnr=0.1)
        assert b1.AND(b2) == (b1 & b2)


class TestOr:
    def test_distribution_free_fpr(self) -> None:
        b1 = BernoulliBool(value=True, fpr=0.10, fnr=0.05)
        b2 = BernoulliBool(value=True, fpr=0.08, fnr=0.12)
        result = b1 | b2
        # fpr = 0.10 + 0.08 - 0.10*0.08 = 0.172
        assert math.isclose(result.fpr, 0.172, abs_tol=1e-12)

    def test_value_is_logical_or(self) -> None:
        a = BernoulliBool(value=True)
        b = BernoulliBool(value=False)
        c = BernoulliBool(value=False)
        assert (a | b).value is True
        assert (b | c).value is False

    def test_one_sided_fnr_or_is_exact_product(self) -> None:
        b1 = BernoulliBool.one_sided_fnr(True, fnr=0.3)
        b2 = BernoulliBool.one_sided_fnr(True, fnr=0.4)
        result = b1 | b2
        assert result.fpr == 0.0
        assert math.isclose(result.fnr, 0.12, abs_tol=1e-12)

    def test_general_or_is_shared_truth_product(self) -> None:
        # Shared-truth semantics: FNR = beta_1 * beta_2 always.
        b1 = BernoulliBool(value=True, fpr=0.10, fnr=0.05)
        b2 = BernoulliBool(value=True, fpr=0.08, fnr=0.12)
        result = b1 | b2
        assert math.isclose(result.fnr, 0.05 * 0.12, abs_tol=1e-12)


class TestBookExample:
    """Worked example from book chapter 3, AND-under-noise section."""

    @pytest.fixture
    def observers(self) -> tuple[BernoulliBool, BernoulliBool]:
        b1 = BernoulliBool(value=True, fpr=0.10, fnr=0.05)
        b2 = BernoulliBool(value=True, fpr=0.08, fnr=0.12)
        return b1, b2

    def test_and_fnr_matches_book(
        self, observers: tuple[BernoulliBool, BernoulliBool]
    ) -> None:
        b1, b2 = observers
        result = b1 & b2
        assert math.isclose(result.fnr, 0.164, abs_tol=1e-12)

    def test_and_fpr_with_prior_matches_book(
        self, observers: tuple[BernoulliBool, BernoulliBool]
    ) -> None:
        b1, b2 = observers
        result = b1.and_with_prior(b2, prior=0.5)
        # Book says approximately 0.057; exact value is 0.043 / 0.75.
        assert math.isclose(result.fpr, 0.043 / 0.75, abs_tol=1e-12)


class TestDeMorgan:
    """OR via De Morgan must agree with direct OR (book section 3.2)."""

    def test_or_matches_de_morgan_distribution_free(self) -> None:
        b1 = BernoulliBool(value=True, fpr=0.1, fnr=0.05)
        b2 = BernoulliBool(value=False, fpr=0.08, fnr=0.12)
        direct = b1 | b2
        de_morgan = ~(~b1 & ~b2)
        # FPR is distribution-free in OR, so the two paths must agree.
        assert math.isclose(direct.fpr, de_morgan.fpr, abs_tol=1e-12)
        # Values must agree.
        assert direct.value == de_morgan.value


class TestObserve:
    def test_observe_returns_correct_when_no_noise(self) -> None:
        b = BernoulliBool.observe(True, fpr=0.0, fnr=0.0)
        assert b.value is True
        b = BernoulliBool.observe(False, fpr=0.0, fnr=0.0)
        assert b.value is False

    def test_observe_distribution(self) -> None:
        rng = random.Random(42)
        n = 50_000
        # truth = True, fnr=0.1: expect ~10% of observations to flip to False.
        flips = sum(
            1
            for _ in range(n)
            if BernoulliBool.observe(True, fpr=0.0, fnr=0.1, rng=rng).value is False
        )
        observed_rate = flips / n
        assert math.isclose(observed_rate, 0.1, abs_tol=0.01)


class TestPriorEdgeCases:
    def test_prior_zero(self) -> None:
        b1 = BernoulliBool(value=False, fpr=0.1, fnr=0.05)
        b2 = BernoulliBool(value=False, fpr=0.2, fnr=0.05)
        # prior=0 means truth is always False; all output-True events are FPs.
        result = b1.and_with_prior(b2, prior=0.0)
        # The denominator is 1 - 0 = 1; numerator is just (1-pi)^2 * a1*a2 = 0.02.
        assert math.isclose(result.fpr, 0.1 * 0.2, abs_tol=1e-12)

    def test_prior_one(self) -> None:
        b1 = BernoulliBool(value=True, fpr=0.1, fnr=0.05)
        b2 = BernoulliBool(value=True, fpr=0.2, fnr=0.07)
        # prior=1: truth always True, no false-positive events possible.
        result = b1.and_with_prior(b2, prior=1.0)
        assert result.fpr == 0.0

    def test_or_fnr_at_tiny_prior_does_not_cancel(self) -> None:
        """Regression: ``1 - (1 - pi)**2`` used to round to 0 for tiny pi.

        As pi -> 0 the positive class is dominated by the two one-true words,
        so the FNR tends to the average of ``fnr_1 (1 - fpr_2)`` and
        ``(1 - fpr_1) fnr_2``.
        """
        b1 = BernoulliBool(value=False, fpr=0.0, fnr=0.0)
        b2 = BernoulliBool(value=False, fpr=0.0, fnr=1.0)
        for prior in (1e-50, 5e-324):  # the second is the smallest subnormal
            result = b1.or_with_prior(b2, prior=prior)
            assert math.isclose(result.fnr, 0.5, rel_tol=1e-12)

    def test_and_fpr_near_prior_one_stays_accurate(self) -> None:
        """Precision check at pi within an ulp of 1 (the cancelled form)."""
        b1 = BernoulliBool(value=True, fpr=0.0, fnr=0.0)
        b2 = BernoulliBool(value=True, fpr=1.0, fnr=0.0)
        prior = math.nextafter(1.0, 0.0)
        result = b1.and_with_prior(b2, prior=prior)
        # Negative words are dominated by (True, False) and (False, True).
        assert math.isclose(result.fpr, 0.5, rel_tol=1e-9)

    def test_invalid_prior_raises(self) -> None:
        b1 = BernoulliBool(value=True, fpr=0.1, fnr=0.05)
        b2 = BernoulliBool(value=True, fpr=0.2, fnr=0.07)
        with pytest.raises(ValueError):
            b1.and_with_prior(b2, prior=-0.1)
        with pytest.raises(ValueError):
            b1.and_with_prior(b2, prior=1.1)


class TestOrWithPriorValidationAndStr:
    def test_or_invalid_prior_raises(self) -> None:
        b = BernoulliBool(value=True, fpr=0.1, fnr=0.05)
        with pytest.raises(ValueError):
            b.or_with_prior(b, prior=1.5)

    def test_or_prior_zero_has_empty_positive_class(self) -> None:
        b = BernoulliBool(value=False, fpr=0.1, fnr=0.05)
        assert b.or_with_prior(b, prior=0.0).fnr == 0.0

    def test_str(self) -> None:
        assert str(BernoulliBool(value=True, fpr=0.1, fnr=0.05)) == (
            "Bernoulli<bool>(True, fpr=0.1, fnr=0.05)"
        )
