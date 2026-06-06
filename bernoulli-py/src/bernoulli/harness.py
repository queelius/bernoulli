"""Empirical measurement harness for Bernoulli structures.

Functions in this module take a callable ``query: X -> BernoulliBool`` (or
just ``X -> bool``) plus labeled ground-truth samples, and return measured
rates with confidence intervals.

The harness is the bridge between the framework's predictions (closed-form
rates from the algebra) and the actual behavior of an implementation. The
two should agree; when they don't, the harness exposes the discrepancy.

Design notes
------------
- All measurements use the Wilson score confidence interval at 95% confidence
  by default. The Wilson interval is more reliable than the normal
  approximation for low-rate proportions where ``np`` and ``n(1-p)`` may be
  small.
- The harness intentionally does not assume independence between samples.
  If your query distribution is correlated, the CI will be optimistic.
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import TypeVar

from bernoulli.atom import BernoulliBool

X = TypeVar("X")


@dataclass(frozen=True)
class RateEstimate:
    """A point estimate plus a Wilson 95% confidence interval."""

    estimate: float
    n: int
    ci_low: float
    ci_high: float
    confidence: float = 0.95

    @property
    def ci_width(self) -> float:
        return self.ci_high - self.ci_low

    def __str__(self) -> str:
        return (
            f"{self.estimate:.4g}  ({self.ci_low:.4g}, {self.ci_high:.4g}) "
            f"[n={self.n}, CI={int(self.confidence * 100)}%]"
        )


def wilson_ci(successes: int, n: int, confidence: float = 0.95) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion.

    Returns ``(low, high)`` such that the true rate is in ``[low, high]``
    with the configured confidence (default 95%).
    """
    if n <= 0:
        return (0.0, 1.0)
    if not 0.0 < confidence < 1.0:
        raise ValueError(f"confidence must be in (0, 1), got {confidence!r}")

    p = successes / n
    # z-score for the desired two-sided confidence level.
    # 95% -> 1.959963984540054; we approximate via an inverse-CDF call below.
    # Using a simple table for the common cases keeps this dependency-free.
    if math.isclose(confidence, 0.95):
        z = 1.959963984540054
    elif math.isclose(confidence, 0.99):
        z = 2.5758293035489004
    elif math.isclose(confidence, 0.90):
        z = 1.6448536269514722
    else:
        # Approximate via the rational approximation of the standard normal
        # quantile (Abramowitz & Stegun 26.2.23).
        z = _normal_quantile((1.0 + confidence) / 2.0)

    z2 = z * z
    denom = 1.0 + z2 / n
    centre = (p + z2 / (2.0 * n)) / denom
    half_width = z * math.sqrt(p * (1.0 - p) / n + z2 / (4.0 * n * n)) / denom
    return (max(0.0, centre - half_width), min(1.0, centre + half_width))


def _normal_quantile(p: float) -> float:
    """Inverse of the standard normal CDF at probability ``p``.

    Uses the Beasley-Springer-Moro approximation; accurate to ~1e-7 for
    the central region. Sufficient for confidence-interval z-scores.
    """
    if not 0.0 < p < 1.0:
        raise ValueError(f"p must be in (0, 1), got {p!r}")
    # Coefficients for the rational approximation.
    a = [
        -3.969683028665376e+01,
        2.209460984245205e+02,
        -2.759285104469687e+02,
        1.383577518672690e+02,
        -3.066479806614716e+01,
        2.506628277459239e+00,
    ]
    b = [
        -5.447609879822406e+01,
        1.615858368580409e+02,
        -1.556989798598866e+02,
        6.680131188771972e+01,
        -1.328068155288572e+01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e+00,
        -2.549732539343734e+00,
        4.374664141464968e+00,
        2.938163982698783e+00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e+00,
        3.754408661907416e+00,
    ]
    p_low = 0.02425
    p_high = 1.0 - p_low
    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (
            ((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]
        ) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
    if p <= p_high:
        q = p - 0.5
        r = q * q
        return (
            ((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]
        ) * q / (
            ((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0
        )
    q = math.sqrt(-2.0 * math.log(1.0 - p))
    return -(
        ((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]
    ) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)


def estimate_rate(
    successes: int, n: int, confidence: float = 0.95
) -> RateEstimate:
    """Build a ``RateEstimate`` from raw counts."""
    point = successes / n if n > 0 else 0.0
    low, high = wilson_ci(successes, n, confidence)
    return RateEstimate(estimate=point, n=n, ci_low=low, ci_high=high, confidence=confidence)


@dataclass(frozen=True)
class EmpiricalRates:
    """Empirically measured ``(fpr, fnr)`` of a query function with CIs."""

    fpr: RateEstimate
    fnr: RateEstimate

    def __str__(self) -> str:
        return f"empirical_fpr={self.fpr}\nempirical_fnr={self.fnr}"


def _coerce_to_bool(result: bool | BernoulliBool) -> bool:
    """Normalize either a raw bool or a BernoulliBool to a bool."""
    if isinstance(result, BernoulliBool):
        return result.value
    return bool(result)


def empirical_rates(
    query: Callable[[X], bool | BernoulliBool],
    positive_samples: Iterable[X],
    negative_samples: Iterable[X],
    confidence: float = 0.95,
) -> EmpiricalRates:
    """Measure the empirical FPR and FNR of ``query`` on labeled samples.

    Parameters
    ----------
    query : Callable[[X], bool | BernoulliBool]
        The function under test. May return a raw bool or a BernoulliBool;
        the latter's ``.value`` is used.
    positive_samples : Iterable[X]
        Inputs for which the truth is True. FNR = fraction the query
        misclassifies as False.
    negative_samples : Iterable[X]
        Inputs for which the truth is False. FPR = fraction the query
        misclassifies as True.
    confidence : float
        Confidence level for the Wilson CI.
    """
    pos = list(positive_samples)
    neg = list(negative_samples)
    fn = sum(1 for x in pos if not _coerce_to_bool(query(x)))
    fp = sum(1 for x in neg if _coerce_to_bool(query(x)))
    return EmpiricalRates(
        fpr=estimate_rate(fp, len(neg), confidence),
        fnr=estimate_rate(fn, len(pos), confidence),
    )


@dataclass(frozen=True)
class CompositionCheck:
    """Empirical vs. predicted rates for a composed Bernoulli query."""

    predicted_fpr: float
    predicted_fnr: float
    empirical: EmpiricalRates
    composition: str = ""  # human-readable description

    @property
    def fpr_within_ci(self) -> bool:
        return self.empirical.fpr.ci_low <= self.predicted_fpr <= self.empirical.fpr.ci_high

    @property
    def fnr_within_ci(self) -> bool:
        return self.empirical.fnr.ci_low <= self.predicted_fnr <= self.empirical.fnr.ci_high

    def __str__(self) -> str:
        ok_fpr = "OK" if self.fpr_within_ci else "MISS"
        ok_fnr = "OK" if self.fnr_within_ci else "MISS"
        return (
            f"composition: {self.composition}\n"
            f"  fpr: predicted={self.predicted_fpr:.4g}  "
            f"empirical={self.empirical.fpr}  [{ok_fpr}]\n"
            f"  fnr: predicted={self.predicted_fnr:.4g}  "
            f"empirical={self.empirical.fnr}  [{ok_fnr}]"
        )


def sample_unique_bytes(
    n: int, length: int = 16, rng: random.Random | None = None
) -> list[bytes]:
    """Generate ``n`` distinct random byte strings of ``length`` bytes.

    Convenience for harness scripts that need disjoint key sets.
    """
    rng = rng or random.Random()
    seen: set[bytes] = set()
    while len(seen) < n:
        seen.add(rng.randbytes(length))
    return list(seen)
