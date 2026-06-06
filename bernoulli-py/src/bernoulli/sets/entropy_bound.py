"""Space-accuracy analyses for FNR-zero approximate sets (book chapter 8).

For an approximate set with false-positive rate ``fpr`` and zero false-negative
rate, the information-theoretic floor on space is::

    floor = -log2(fpr)   bits per key

(book chapter 8, the counting / pigeonhole argument). A classical Bloom filter
at its optimal hash count pays a *constant multiplicative* overhead of
``log2(e) = 1 / ln(2) ~= 1.4427`` above the floor, independent of ``fpr``. The
Bernoulli hash function (BHF, book chapter 14) instead pays an *additive*
overhead: ``ceil(-log2 fpr)`` bits for an integer fingerprint width plus a
sublinear perfect-hash term ``mu`` that vanishes as the key count grows.

This module is the executable form of those comparisons. It builds on the
primitives in :mod:`bernoulli.algebra` and adds the BHF model, efficiency, and
the Bloom-versus-BHF savings.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from bernoulli.algebra import (
    bits_per_key_for_fpr,
    bloom_bits_per_key_for_fpr,
)

#: The constant multiplicative overhead a classical Bloom filter pays over the
#: entropy floor at optimal k: ``log2(e) = 1 / ln(2)``.
BLOOM_OVERHEAD_FACTOR: float = 1.0 / math.log(2.0)


def entropy_floor_bits_per_key(fpr: float) -> float:
    """The floor ``-log2(fpr)`` bits per key (book chapter 8).

    No FNR-zero representation can undercut this asymptotically.

    Examples
    --------
    >>> round(entropy_floor_bits_per_key(0.01), 4)
    6.6439
    """
    return bits_per_key_for_fpr(fpr)


def bloom_bits_per_key(fpr: float) -> float:
    """Bits per key a classical Bloom filter spends at optimal k for ``fpr``.

    Equals ``BLOOM_OVERHEAD_FACTOR * entropy_floor_bits_per_key(fpr)``.

    Examples
    --------
    >>> round(bloom_bits_per_key(0.01), 4)
    9.5851
    """
    return bloom_bits_per_key_for_fpr(fpr)


def bloom_overhead_bits_per_key(fpr: float) -> float:
    """The Bloom filter's wasted bits per key over the floor, ``(1.44 - 1) * floor``."""
    return bloom_bits_per_key(fpr) - entropy_floor_bits_per_key(fpr)


def bhf_bits_per_key(fpr: float, perfect_hash_overhead: float = 0.0) -> float:
    """Bits per key for the Bernoulli hash function (book chapter 14).

    The fingerprint width is the integer ``r = ceil(-log2 fpr)`` (the smallest
    ``r`` with ``2**-r <= fpr``); the ``perfect_hash_overhead`` (``mu``) is the
    sublinear per-key cost of the perfect-hash representation, a small constant
    at finite key counts that vanishes asymptotically.

    Examples
    --------
    >>> bhf_bits_per_key(0.01)            # ceil(6.6439) = 7
    7.0
    >>> bhf_bits_per_key(0.01, perfect_hash_overhead=2.5)
    9.5
    """
    if perfect_hash_overhead < 0.0:
        raise ValueError(
            f"perfect_hash_overhead must be non-negative, got {perfect_hash_overhead!r}"
        )
    fingerprint_width = math.ceil(bits_per_key_for_fpr(fpr))
    return float(fingerprint_width) + perfect_hash_overhead


def fingerprint_width(fpr: float) -> int:
    """The integer fingerprint width ``r = ceil(-log2 fpr)`` for a BHF.

    The achieved FPR is ``2**-r <= fpr``, generally strictly below the target by
    the ceiling-rounding slack.

    Examples
    --------
    >>> fingerprint_width(0.01)
    7
    >>> 2 ** -fingerprint_width(0.01) <= 0.01
    True
    """
    return math.ceil(bits_per_key_for_fpr(fpr))


def efficiency(bits_per_key: float, fpr: float) -> float:
    """Floor divided by actual bits per key: 1.0 is optimal, lower is wasteful.

    A classical Bloom filter has efficiency ``ln(2) ~= 0.693`` at every ``fpr``.

    Examples
    --------
    >>> round(efficiency(bloom_bits_per_key(0.01), 0.01), 4)
    0.6931
    """
    if bits_per_key <= 0.0:
        raise ValueError(f"bits_per_key must be positive, got {bits_per_key!r}")
    return entropy_floor_bits_per_key(fpr) / bits_per_key


def bloom_vs_bhf_savings_bits(fpr: float, perfect_hash_overhead: float = 0.0) -> float:
    """Bits per key the BHF saves over a classical Bloom filter at ``fpr``."""
    return bloom_bits_per_key(fpr) - bhf_bits_per_key(fpr, perfect_hash_overhead)


@dataclass(frozen=True, slots=True)
class SpaceComparison:
    """A side-by-side space comparison at one target FPR (book chapter 8 / 14)."""

    fpr: float
    floor_bits_per_key: float
    bloom_bits_per_key: float
    bhf_bits_per_key: float
    bloom_efficiency: float
    bhf_efficiency: float


def compare(fpr: float, perfect_hash_overhead: float = 0.0) -> SpaceComparison:
    """Build a :class:`SpaceComparison` of floor, Bloom, and BHF at ``fpr``.

    Examples
    --------
    >>> c = compare(0.01)
    >>> round(c.floor_bits_per_key, 2), round(c.bloom_bits_per_key, 2), c.bhf_bits_per_key
    (6.64, 9.59, 7.0)
    """
    floor = entropy_floor_bits_per_key(fpr)
    bloom = bloom_bits_per_key(fpr)
    bhf = bhf_bits_per_key(fpr, perfect_hash_overhead)
    return SpaceComparison(
        fpr=fpr,
        floor_bits_per_key=floor,
        bloom_bits_per_key=bloom,
        bhf_bits_per_key=bhf,
        bloom_efficiency=floor / bloom,
        bhf_efficiency=floor / bhf,
    )
