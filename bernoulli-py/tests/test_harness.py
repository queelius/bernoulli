"""Tests for ``bernoulli.harness``."""

from __future__ import annotations

import math
import random

import pytest

from bernoulli.algorithms.noisy_classifier import NoisyClassifier
from bernoulli.harness import (
    EmpiricalRates,
    empirical_rates,
    estimate_rate,
    sample_unique_bytes,
    wilson_ci,
)


class TestWilsonCI:
    def test_zero_n(self) -> None:
        low, high = wilson_ci(0, 0)
        assert (low, high) == (0.0, 1.0)

    def test_balanced_proportion(self) -> None:
        # 50/100 with 95% CI: should bracket 0.5 reasonably tight.
        low, high = wilson_ci(50, 100)
        assert low < 0.5 < high
        assert high - low < 0.25

    def test_extreme_proportion(self) -> None:
        # 0/1000: should give a small upper bound (and a near-zero lower).
        low, high = wilson_ci(0, 1000)
        assert low < 1e-10  # essentially zero (FP noise is fine)
        assert 0.0 < high < 0.01

    def test_invalid_confidence(self) -> None:
        with pytest.raises(ValueError):
            wilson_ci(50, 100, confidence=0.0)
        with pytest.raises(ValueError):
            wilson_ci(50, 100, confidence=1.0)


class TestEstimateRate:
    def test_basic(self) -> None:
        est = estimate_rate(successes=10, n=100)
        assert math.isclose(est.estimate, 0.1)
        assert est.ci_low <= 0.1 <= est.ci_high
        assert est.n == 100


class TestEmpiricalRates:
    def test_perfect_classifier(self) -> None:
        clf = NoisyClassifier(lambda n: n % 2 == 0, fpr=0.0, fnr=0.0)
        positives = list(range(0, 200, 2))  # even
        negatives = list(range(1, 200, 2))  # odd
        rates = empirical_rates(clf.predict, positives, negatives)
        assert rates.fpr.estimate == 0.0
        assert rates.fnr.estimate == 0.0

    def test_noisy_classifier_recovered(self) -> None:
        rng = random.Random(0)
        clf = NoisyClassifier(lambda n: n % 2 == 0, fpr=0.1, fnr=0.05, rng=rng)
        positives = list(range(0, 20_000, 2))
        negatives = list(range(1, 20_000, 2))
        rates = empirical_rates(clf.predict, positives, negatives)
        assert rates.fpr.ci_low <= 0.1 <= rates.fpr.ci_high
        assert rates.fnr.ci_low <= 0.05 <= rates.fnr.ci_high

    def test_accepts_bernoulli_bool_returns(self) -> None:
        clf = NoisyClassifier(lambda n: n % 2 == 0, fpr=0.1, fnr=0.05, rng=random.Random(0))
        positives = list(range(0, 1000, 2))
        negatives = list(range(1, 1000, 2))
        rates = empirical_rates(clf.query, positives, negatives)  # query returns BernoulliBool
        assert isinstance(rates, EmpiricalRates)


class TestSampleUniqueBytes:
    def test_unique_count(self) -> None:
        samples = sample_unique_bytes(100, length=8, rng=random.Random(0))
        assert len(samples) == 100
        assert len(set(samples)) == 100

    def test_length(self) -> None:
        samples = sample_unique_bytes(10, length=16, rng=random.Random(0))
        for s in samples:
            assert len(s) == 16


class TestNormalQuantile:
    """The inverse-normal approximation behind non-tabulated confidence levels."""

    @pytest.mark.parametrize(
        ("p", "z"),
        [
            (0.5, 0.0),
            (0.975, 1.959963984540054),
            (0.995, 2.5758293035489004),
            (0.9, 1.2815515655446004),
            (0.001, -3.090232306167813),  # lower tail branch
            (0.999, 3.090232306167813),  # upper tail branch
        ],
    )
    def test_known_values(self, p: float, z: float) -> None:
        from bernoulli.harness import _normal_quantile

        assert math.isclose(_normal_quantile(p), z, abs_tol=1e-6)

    def test_symmetry(self) -> None:
        from bernoulli.harness import _normal_quantile

        for p in (0.01, 0.2, 0.4):
            assert math.isclose(_normal_quantile(p), -_normal_quantile(1.0 - p), abs_tol=1e-9)

    @pytest.mark.parametrize("p", [0.0, 1.0, -0.1])
    def test_out_of_range(self, p: float) -> None:
        from bernoulli.harness import _normal_quantile

        with pytest.raises(ValueError):
            _normal_quantile(p)

    def test_untabulated_confidence_uses_quantile(self) -> None:
        # 80% two-sided: z = 1.2815515655446004.
        z = 1.2815515655446004
        n, k = 400, 100
        p = k / n
        denom = 1.0 + z * z / n
        centre = (p + z * z / (2.0 * n)) / denom
        half = z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / denom
        low, high = wilson_ci(k, n, confidence=0.80)
        assert math.isclose(low, centre - half, abs_tol=1e-6)
        assert math.isclose(high, centre + half, abs_tol=1e-6)

    @pytest.mark.parametrize("confidence", [0.90, 0.99])
    def test_tabulated_levels_widen_with_confidence(self, confidence: float) -> None:
        low, high = wilson_ci(30, 100, confidence=confidence)
        base_low, base_high = wilson_ci(30, 100)
        if confidence > 0.95:
            assert low < base_low and high > base_high
        else:
            assert low > base_low and high < base_high


class TestRateEstimateAndCompositionCheck:
    def test_ci_width_and_str(self) -> None:
        r = estimate_rate(10, 100)
        assert math.isclose(r.ci_width, r.ci_high - r.ci_low)
        assert "n=100" in str(r) and "CI=95%" in str(r)

    def test_composition_check_flags(self) -> None:
        from bernoulli.harness import CompositionCheck

        emp = EmpiricalRates(fpr=estimate_rate(10, 1000), fnr=estimate_rate(50, 1000))
        hit = CompositionCheck(predicted_fpr=0.01, predicted_fnr=0.05, empirical=emp)
        miss = CompositionCheck(predicted_fpr=0.5, predicted_fnr=0.5, empirical=emp)
        assert hit.fpr_within_ci and hit.fnr_within_ci
        assert not miss.fpr_within_ci and not miss.fnr_within_ci
        assert "[OK]" in str(hit) and "[MISS]" in str(miss)
