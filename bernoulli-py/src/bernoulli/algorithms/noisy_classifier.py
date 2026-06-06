"""A configurable two-sided noisy classifier.

A teaching / harness-validation construct. Given a ground-truth predicate
``f: X -> bool`` and target rates ``(fpr, fnr)``, simulates a Bernoulli<bool>
classifier whose output flips relative to ``f`` with the configured rates.

Useful for:

- Validating the harness: empirical rates should match the configured rates.
- Validating composition formulas: AND / OR of two independent classifiers
  must obey the closed-form bounds and the prior-dependent forms.
- Studying calibration: how confidence intervals on (fpr, fnr) tighten with
  sample size.
"""

from __future__ import annotations

import random
from collections.abc import Callable
from typing import Generic, TypeVar

from bernoulli.atom import BernoulliBool

X = TypeVar("X")


class NoisyClassifier(Generic[X]):
    """Wraps a ground-truth predicate and adds independent ``(fpr, fnr)`` noise.

    Parameters
    ----------
    truth : Callable[[X], bool]
        The ground-truth predicate.
    fpr : float
    fnr : float
        Configured channel rates.
    rng : random.Random | None
        Random source. Defaults to a fresh ``random.Random()``.

    Examples
    --------
    >>> import random
    >>> truth = lambda n: n % 2 == 0
    >>> clf = NoisyClassifier(truth, fpr=0.1, fnr=0.05, rng=random.Random(0))
    >>> b = clf.query(4)
    >>> isinstance(b, BernoulliBool)
    True
    """

    def __init__(
        self,
        truth: Callable[[X], bool],
        fpr: float = 0.0,
        fnr: float = 0.0,
        rng: random.Random | None = None,
    ) -> None:
        if not 0.0 <= fpr <= 1.0:
            raise ValueError(f"fpr must be in [0, 1], got {fpr!r}")
        if not 0.0 <= fnr <= 1.0:
            raise ValueError(f"fnr must be in [0, 1], got {fnr!r}")
        self._truth = truth
        self._fpr = fpr
        self._fnr = fnr
        self._rng = rng or random.Random()

    @property
    def fpr_param(self) -> float:
        return self._fpr

    @property
    def fnr_param(self) -> float:
        return self._fnr

    def predict(self, x: X) -> bool:
        """Sample a noisy prediction for ``x``."""
        truth_value = self._truth(x)
        if truth_value:
            return self._rng.random() >= self._fnr
        return self._rng.random() < self._fpr

    def query(self, x: X) -> BernoulliBool:
        """Predict and lift to a ``BernoulliBool`` with the configured rates."""
        return BernoulliBool(value=self.predict(x), fpr=self._fpr, fnr=self._fnr)
