"""Space-accuracy analyses for FNR-zero approximate sets (book chapter 8).

For an approximate set with false-positive rate ``fpr`` and zero false-negative
rate, the information-theoretic floor on space is::

    floor = -log2(fpr)   bits per key

(book chapter 8, the counting / pigeonhole argument). A classical Bloom filter
at its optimal hash count pays a *constant multiplicative* overhead of
``log2(e) = 1 / ln(2) ~= 1.4427`` above the floor, independent of ``fpr``. The
perfect hash filter (PHF; Dietzfelbinger and Pagh 2008, Sec. 1; book chapter
14) instead pays an *additive* overhead: ``ceil(-log2 fpr)`` bits for an integer
fingerprint width plus the minimal perfect hash's own cost ``c`` bits per key.
That cost does not vanish: any minimal perfect hash needs at least
``log2(e) ~= 1.4427`` bits per key (Fredman and Komlos 1984), and practical ones
use about 2 to 3.5. The PHF therefore beats a Bloom filter only when
``(log2(e) - 1) * log2(1/fpr) > c`` (see :func:`phf_beats_bloom`).

This module is the executable form of those comparisons. It builds on the
primitives in :mod:`bernoulli.algebra` and adds the PHF model, efficiency, and
the Bloom-versus-PHF savings. The ``bhf_*`` names are deprecated aliases from
0.3.0, which mislabeled the PHF as the Bernoulli hash function and defaulted its
perfect-hash cost to zero, below the lower bound.
"""

from __future__ import annotations

import math
import warnings
from dataclasses import dataclass

from bernoulli.algebra import (
    bits_per_key_for_fpr,
    bloom_bits_per_key_for_fpr,
)

#: The constant multiplicative overhead a classical Bloom filter pays over the
#: entropy floor at optimal k: ``log2(e) = 1 / ln(2)``.
BLOOM_OVERHEAD_FACTOR: float = 1.0 / math.log(2.0)

#: Lower bound on the bits per key of any minimal perfect hash function,
#: ``log2(e)`` (Fredman and Komlos 1984). A PHF pays at least this over its
#: fingerprints.
MPHF_LOWER_BOUND_BITS: float = math.log2(math.e)


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


def phf_bits_per_key(fpr: float, mphf_bits_per_key: float = MPHF_LOWER_BOUND_BITS) -> float:
    """Bits per key for the perfect hash filter (book chapter 14).

    The fingerprint width is the integer ``r = ceil(-log2 fpr)`` (the smallest
    ``r`` with ``2**-r <= fpr``) and ``mphf_bits_per_key`` is the minimal perfect
    hash's cost ``c``. The default is the lower bound ``log2(e)``; pass the
    measured cost of a real construction (BBHash, RecSplit, ...) for a
    realistic figure.

    Examples
    --------
    >>> round(phf_bits_per_key(0.01), 4)            # 7 + log2(e)
    8.4427
    >>> phf_bits_per_key(0.01, mphf_bits_per_key=2.5)
    9.5
    """
    if mphf_bits_per_key < 0.0:
        raise ValueError(f"mphf_bits_per_key must be non-negative, got {mphf_bits_per_key!r}")
    return float(fingerprint_width(fpr)) + mphf_bits_per_key


def phf_beats_bloom(fpr: float, mphf_bits_per_key: float = MPHF_LOWER_BOUND_BITS) -> bool:
    """Whether a PHF uses fewer bits per key than an optimal Bloom filter at ``fpr``.

    Compares the two space models exactly, including the fingerprint
    ceiling. With continuous fingerprint widths this is the book's rule
    ``(log2(e) - 1) * log2(1/fpr) > c``.

    Examples
    --------
    >>> phf_beats_bloom(2.0 ** -7, mphf_bits_per_key=3.23)    # 10.23 vs 10.10
    False
    >>> phf_beats_bloom(2.0 ** -10, mphf_bits_per_key=3.23)   # 13.23 vs 14.43
    True
    """
    return phf_bits_per_key(fpr, mphf_bits_per_key) < bloom_bits_per_key(fpr)


def bhf_bits_per_key(fpr: float, perfect_hash_overhead: float = 0.0) -> float:
    """Deprecated alias for :func:`phf_bits_per_key` with the 0.3.0 default.

    0.3.0 called the perfect hash filter "the Bernoulli hash function" and
    defaulted the perfect-hash cost to 0, below the ``log2(e)`` lower bound.
    This alias keeps that exact behavior; use :func:`phf_bits_per_key`.
    """
    warnings.warn(
        "bhf_bits_per_key is deprecated: it models the perfect hash filter; "
        "use phf_bits_per_key (whose default perfect-hash cost is log2(e))",
        DeprecationWarning,
        stacklevel=2,
    )
    if perfect_hash_overhead < 0.0:
        raise ValueError(
            f"perfect_hash_overhead must be non-negative, got {perfect_hash_overhead!r}"
        )
    return float(fingerprint_width(fpr)) + perfect_hash_overhead


def fingerprint_width(fpr: float) -> int:
    """The integer fingerprint width ``r = ceil(-log2 fpr)`` for a PHF.

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


def bloom_vs_phf_savings_bits(
    fpr: float, mphf_bits_per_key: float = MPHF_LOWER_BOUND_BITS
) -> float:
    """Bits per key the PHF saves over a classical Bloom filter (negative: Bloom wins)."""
    return bloom_bits_per_key(fpr) - phf_bits_per_key(fpr, mphf_bits_per_key)


def bloom_vs_bhf_savings_bits(fpr: float, perfect_hash_overhead: float = 0.0) -> float:
    """Deprecated alias for :func:`bloom_vs_phf_savings_bits` with the 0.3.0 default."""
    warnings.warn(
        "bloom_vs_bhf_savings_bits is deprecated; use bloom_vs_phf_savings_bits",
        DeprecationWarning,
        stacklevel=2,
    )
    return bloom_bits_per_key(fpr) - (float(fingerprint_width(fpr)) + perfect_hash_overhead)


@dataclass(frozen=True, slots=True)
class SpaceComparison:
    """A side-by-side space comparison at one target FPR (book chapters 8 and 14)."""

    fpr: float
    floor_bits_per_key: float
    bloom_bits_per_key: float
    phf_bits_per_key: float
    bloom_efficiency: float
    phf_efficiency: float

    @property
    def bhf_bits_per_key(self) -> float:
        """Deprecated alias for :attr:`phf_bits_per_key`."""
        return self.phf_bits_per_key

    @property
    def bhf_efficiency(self) -> float:
        """Deprecated alias for :attr:`phf_efficiency`."""
        return self.phf_efficiency


def compare(
    fpr: float,
    mphf_bits_per_key: float = MPHF_LOWER_BOUND_BITS,
    *,
    perfect_hash_overhead: float | None = None,
) -> SpaceComparison:
    """Build a :class:`SpaceComparison` of floor, Bloom, and PHF at ``fpr``.

    ``perfect_hash_overhead`` is the deprecated 0.3.0 name for
    ``mphf_bits_per_key``; passing it warns and overrides the default.

    Examples
    --------
    >>> c = compare(0.01)
    >>> round(c.floor_bits_per_key, 2), round(c.bloom_bits_per_key, 2), round(c.phf_bits_per_key, 2)
    (6.64, 9.59, 8.44)
    """
    if perfect_hash_overhead is not None:
        warnings.warn(
            "compare(perfect_hash_overhead=...) is deprecated; use mphf_bits_per_key",
            DeprecationWarning,
            stacklevel=2,
        )
        mphf_bits_per_key = perfect_hash_overhead
    floor = entropy_floor_bits_per_key(fpr)
    bloom = bloom_bits_per_key(fpr)
    phf = phf_bits_per_key(fpr, mphf_bits_per_key)
    return SpaceComparison(
        fpr=fpr,
        floor_bits_per_key=floor,
        bloom_bits_per_key=bloom,
        phf_bits_per_key=phf,
        bloom_efficiency=floor / bloom,
        phf_efficiency=floor / phf,
    )
