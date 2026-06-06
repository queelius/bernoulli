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
