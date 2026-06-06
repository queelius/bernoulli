"""Classification measures derived from ``(fpr, fnr, prevalence)``.

Given the channel parameters ``(alpha, beta) = (fpr, fnr)`` of a Bernoulli<bool>
predictor and the prevalence ``pi = P(true value == True)``, the standard
classification measures are deterministic functions of those three numbers.
This module provides them.

Coverage:

- :func:`ppv`, :func:`npv`: positive and negative predictive values.
- :func:`tpr`, :func:`tnr`: sensitivity and specificity.
- :func:`youden_j`: Youden's J statistic (informedness).
- :func:`f1_score`: harmonic mean of PPV and recall.
- :func:`matthews_cc`: Matthews correlation coefficient.
- :func:`base_rate_error`: total error rate at population prevalence.
- :func:`balanced_accuracy`: average of TPR and TNR.

These are derived from the joint distribution of ``(true value, prediction)``
implied by the channel matrix and prevalence. None of them depend on the
specific predictor; they are functions of its rates.
"""

from __future__ import annotations

import math


def _validate_rate(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be in [0, 1], got {value!r}")


def tpr(fnr: float) -> float:
    """True positive rate (sensitivity, recall): ``1 - fnr``."""
    _validate_rate("fnr", fnr)
    return 1.0 - fnr


def tnr(fpr: float) -> float:
    """True negative rate (specificity): ``1 - fpr``."""
    _validate_rate("fpr", fpr)
    return 1.0 - fpr


def youden_j(fpr: float, fnr: float) -> float:
    """Youden's J = TPR + TNR - 1 = ``1 - fpr - fnr``.

    Also called the "informedness" of the predictor. Ranges over ``[-1, 1]``;
    a value of 0 corresponds to chance, 1 to a perfect predictor.
    """
    _validate_rate("fpr", fpr)
    _validate_rate("fnr", fnr)
    return 1.0 - fpr - fnr


def informedness(fpr: float, fnr: float) -> float:
    """Synonym for :func:`youden_j`."""
    return youden_j(fpr, fnr)


def ppv(fpr: float, fnr: float, prevalence: float) -> float:
    """Positive predictive value: ``P(true == True | predict == True)``.

    Bayes:  ``ppv = pi * (1 - beta) / (pi * (1 - beta) + (1 - pi) * alpha)``.

    PPV is the measure that explains why a 99%-accurate test for a 1-in-10000
    disease will mostly produce false positives: at low prevalence the
    denominator is dominated by ``(1 - pi) * alpha``.
    """
    _validate_rate("fpr", fpr)
    _validate_rate("fnr", fnr)
    _validate_rate("prevalence", prevalence)
    pi = prevalence
    num = pi * (1.0 - fnr)
    denom = pi * (1.0 - fnr) + (1.0 - pi) * fpr
    return num / denom if denom > 0.0 else 0.0


def npv(fpr: float, fnr: float, prevalence: float) -> float:
    """Negative predictive value: ``P(true == False | predict == False)``."""
    _validate_rate("fpr", fpr)
    _validate_rate("fnr", fnr)
    _validate_rate("prevalence", prevalence)
    pi = prevalence
    num = (1.0 - pi) * (1.0 - fpr)
    denom = (1.0 - pi) * (1.0 - fpr) + pi * fnr
    return num / denom if denom > 0.0 else 0.0


def f1_score(fpr: float, fnr: float, prevalence: float) -> float:
    """F1 score: harmonic mean of PPV and recall.

    ``F1 = 2 * P * R / (P + R)`` where ``P = ppv`` and ``R = tpr = 1 - fnr``.
    """
    p = ppv(fpr, fnr, prevalence)
    r = 1.0 - fnr
    if p + r <= 0.0:
        return 0.0
    return 2.0 * p * r / (p + r)


def base_rate_error(fpr: float, fnr: float, prevalence: float) -> float:
    """Total error rate at population scale: ``pi * fnr + (1 - pi) * fpr``.

    The probability that a uniformly drawn instance is misclassified.
    """
    _validate_rate("fpr", fpr)
    _validate_rate("fnr", fnr)
    _validate_rate("prevalence", prevalence)
    return prevalence * fnr + (1.0 - prevalence) * fpr


def balanced_accuracy(fpr: float, fnr: float) -> float:
    """Mean of TPR and TNR: ``(1 - fnr + 1 - fpr) / 2 = 1 - (fpr + fnr) / 2``.

    Insensitive to prevalence. Equals ``(youden_j + 1) / 2``.
    """
    _validate_rate("fpr", fpr)
    _validate_rate("fnr", fnr)
    return 1.0 - 0.5 * (fpr + fnr)


def matthews_cc(fpr: float, fnr: float, prevalence: float) -> float:
    """Matthews correlation coefficient (MCC), parameterized by rates.

    Computed from the joint cell probabilities ``(TP, FN, FP, TN)`` derived
    from ``(prevalence, fpr, fnr)``::

        TP = pi * (1 - fnr)
        FN = pi * fnr
        FP = (1 - pi) * fpr
        TN = (1 - pi) * (1 - fpr)

    MCC ranges over ``[-1, 1]``; a value of 0 corresponds to chance.

    Returns 0 when any marginal is zero (the denominator vanishes; the MCC
    is conventionally taken as 0 in that degenerate case).
    """
    _validate_rate("fpr", fpr)
    _validate_rate("fnr", fnr)
    _validate_rate("prevalence", prevalence)

    pi = prevalence
    tp = pi * (1.0 - fnr)
    fn = pi * fnr
    fp_ = (1.0 - pi) * fpr
    tn = (1.0 - pi) * (1.0 - fpr)

    num = tp * tn - fp_ * fn
    denom_sq = (tp + fp_) * (tp + fn) * (tn + fp_) * (tn + fn)
    if denom_sq <= 0.0:
        return 0.0
    return num / math.sqrt(denom_sq)
