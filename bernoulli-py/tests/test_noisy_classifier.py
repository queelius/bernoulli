"""Tests for ``bernoulli.algorithms.noisy_classifier``."""

from __future__ import annotations

import math
import random

import pytest

from bernoulli.algorithms.noisy_classifier import NoisyClassifier
from bernoulli.atom import BernoulliBool


def _is_even(n: int) -> bool:
    return n % 2 == 0


class TestConstruction:
    def test_default_rates_zero(self) -> None:
        clf = NoisyClassifier(_is_even)
        assert clf.fpr_param == 0.0
        assert clf.fnr_param == 0.0

    def test_invalid_rates(self) -> None:
        with pytest.raises(ValueError):
            NoisyClassifier(_is_even, fpr=-0.1)
        with pytest.raises(ValueError):
            NoisyClassifier(_is_even, fnr=1.5)


class TestPerfectClassifier:
    def test_zero_noise_returns_truth(self) -> None:
        clf = NoisyClassifier(_is_even, fpr=0.0, fnr=0.0)
        for n in range(100):
            assert clf.predict(n) == _is_even(n)


class TestEmpiricalRatesMatchConfig:
    def test_fpr_matches_at_scale(self) -> None:
        rng = random.Random(0)
        target_fpr = 0.1
        clf = NoisyClassifier(_is_even, fpr=target_fpr, fnr=0.0, rng=rng)
        # Negative samples: odd numbers (truth = False).
        n = 50_000
        flips = sum(1 for i in range(1, 2 * n + 1, 2) if clf.predict(i))
        empirical = flips / n
        assert math.isclose(empirical, target_fpr, abs_tol=0.01)

    def test_fnr_matches_at_scale(self) -> None:
        rng = random.Random(1)
        target_fnr = 0.2
        clf = NoisyClassifier(_is_even, fpr=0.0, fnr=target_fnr, rng=rng)
        n = 50_000
        # Positive samples: even numbers.
        misses = sum(1 for i in range(0, 2 * n, 2) if not clf.predict(i))
        empirical = misses / n
        assert math.isclose(empirical, target_fnr, abs_tol=0.01)


class TestQueryReturnsBernoulli:
    def test_query_returns_bernoulli_bool(self) -> None:
        clf = NoisyClassifier(_is_even, fpr=0.1, fnr=0.05)
        b = clf.query(4)
        assert isinstance(b, BernoulliBool)
        assert b.fpr == 0.1
        assert b.fnr == 0.05
