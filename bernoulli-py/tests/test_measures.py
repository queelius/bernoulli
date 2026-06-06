"""Tests for ``bernoulli.measures``."""

from __future__ import annotations

import math

import pytest

from bernoulli import measures


class TestPpvNpv:
    def test_perfect_predictor(self) -> None:
        # fpr=0, fnr=0, prevalence=0.1: PPV must be 1, NPV must be 1.
        assert math.isclose(measures.ppv(fpr=0.0, fnr=0.0, prevalence=0.1), 1.0)
        assert math.isclose(measures.npv(fpr=0.0, fnr=0.0, prevalence=0.1), 1.0)

    def test_low_prevalence_high_fpr_low_ppv(self) -> None:
        # Classic "rare disease" example: PPV is low at low prevalence.
        # 99% accurate test, 0.1% prevalence -> PPV around 9%.
        ppv_val = measures.ppv(fpr=0.01, fnr=0.01, prevalence=0.001)
        assert ppv_val < 0.15  # not 99% as naive intuition would suggest

    def test_ppv_at_unit_prevalence(self) -> None:
        # If prevalence = 1, PPV = 1 (every prediction is correct).
        assert measures.ppv(fpr=0.5, fnr=0.5, prevalence=1.0) == 1.0

    def test_npv_at_zero_prevalence(self) -> None:
        # If prevalence = 0, NPV = 1 (every negative is correct).
        assert measures.npv(fpr=0.5, fnr=0.5, prevalence=0.0) == 1.0


class TestYoudenJ:
    def test_perfect(self) -> None:
        assert measures.youden_j(fpr=0.0, fnr=0.0) == 1.0

    def test_chance(self) -> None:
        # fpr + fnr = 1 -> chance level.
        assert measures.youden_j(fpr=0.5, fnr=0.5) == 0.0

    def test_worst(self) -> None:
        # Always wrong -> J = -1.
        assert measures.youden_j(fpr=1.0, fnr=1.0) == -1.0

    def test_informedness_alias(self) -> None:
        assert measures.informedness(fpr=0.1, fnr=0.05) == measures.youden_j(0.1, 0.05)


class TestF1:
    def test_perfect(self) -> None:
        assert measures.f1_score(fpr=0.0, fnr=0.0, prevalence=0.5) == 1.0

    def test_zero_when_no_true_positives(self) -> None:
        # fnr=1 means every positive is missed; F1 reduces to 0.
        f1_val = measures.f1_score(fpr=0.1, fnr=1.0, prevalence=0.5)
        assert f1_val == 0.0


class TestBaseRateError:
    def test_balanced(self) -> None:
        # prevalence 0.5: error = 0.5*beta + 0.5*alpha = avg(alpha, beta).
        assert math.isclose(
            measures.base_rate_error(fpr=0.1, fnr=0.2, prevalence=0.5),
            0.15,
        )

    def test_extreme_prevalence(self) -> None:
        # prevalence 1: error = fnr only.
        assert measures.base_rate_error(fpr=0.5, fnr=0.1, prevalence=1.0) == 0.1
        # prevalence 0: error = fpr only.
        assert measures.base_rate_error(fpr=0.05, fnr=0.5, prevalence=0.0) == 0.05


class TestBalancedAccuracy:
    def test_perfect(self) -> None:
        assert measures.balanced_accuracy(fpr=0.0, fnr=0.0) == 1.0

    def test_chance(self) -> None:
        assert math.isclose(
            measures.balanced_accuracy(fpr=0.5, fnr=0.5),
            0.5,
        )


class TestMatthewsCC:
    def test_perfect(self) -> None:
        # Perfect predictor at any non-degenerate prevalence -> MCC = 1.
        assert math.isclose(
            measures.matthews_cc(fpr=0.0, fnr=0.0, prevalence=0.5),
            1.0,
            abs_tol=1e-12,
        )

    def test_always_wrong(self) -> None:
        # Always wrong -> MCC = -1.
        assert math.isclose(
            measures.matthews_cc(fpr=1.0, fnr=1.0, prevalence=0.5),
            -1.0,
            abs_tol=1e-12,
        )

    def test_chance(self) -> None:
        # alpha = 1 - beta and prevalence chosen so denominator is symmetric:
        # at fpr=0.5, fnr=0.5, prevalence=0.5, the predictor is independent
        # of truth, MCC = 0.
        assert math.isclose(
            measures.matthews_cc(fpr=0.5, fnr=0.5, prevalence=0.5),
            0.0,
            abs_tol=1e-12,
        )

    def test_degenerate_zero_prevalence(self) -> None:
        # No positives -> MCC undefined; we return 0 by convention.
        assert measures.matthews_cc(fpr=0.1, fnr=0.0, prevalence=0.0) == 0.0


class TestRateValidation:
    @pytest.mark.parametrize(
        "fn",
        [
            measures.ppv,
            measures.npv,
            measures.f1_score,
            measures.matthews_cc,
            measures.base_rate_error,
        ],
    )
    def test_rates_in_range(self, fn) -> None:  # type: ignore[no-untyped-def]
        with pytest.raises(ValueError):
            fn(fpr=-0.1, fnr=0.1, prevalence=0.5)
        with pytest.raises(ValueError):
            fn(fpr=0.1, fnr=1.1, prevalence=0.5)
        with pytest.raises(ValueError):
            fn(fpr=0.1, fnr=0.1, prevalence=2.0)
