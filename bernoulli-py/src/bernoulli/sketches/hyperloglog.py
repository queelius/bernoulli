"""HyperLogLog cardinality estimator as a Bernoulli<int> estimator.

HyperLogLog estimates the cardinality of a multiset using ``m = 2**precision``
registers, each storing the maximum leading-zero count seen for hashes routed
to that bucket. Standard error of the relative estimate is approximately
``sigma_rel ~ 1.04 / sqrt(m)``.

Framework view
--------------
HLL outputs a Bernoulli<int> estimator: ``HLL(S)`` returns an estimate of
``|S|`` that is approximately Normal with mean ``|S|`` and standard deviation
``sigma_rel * |S|``. Two HLLs may be merged via register-wise max, yielding
an estimate for ``|A union B|``. Inclusion-exclusion gives::

    |A intersect B| = |A| + |B| - |A union B|

The variance of the intersection estimate is the sum of the three component
variances (each pair has nontrivial covariance, but at small overlap the
fact that ``|A| + |B| ~ 2 * |A union B|`` makes the variance of the
intersection estimate dominated by the union term, which is roughly
``sigma_rel * |A union B|``). When ``|A intersect B| << min(|A|, |B|)``,
the relative error of the intersection estimate explodes.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import ClassVar

from bernoulli.sets.bloom import _fnv1a_64

_MIN_PRECISION = 4
_MAX_PRECISION = 18

_MASK64 = 0xFFFFFFFFFFFFFFFF


def _splitmix64(x: int) -> int:
    """Strong 64-bit avalanche mixer (Stafford's variant of splitmix64).

    FNV-1a alone has weak high-bit avalanche; pairing it with splitmix gives
    the uniform distribution HLL needs over both bucket selection bits and
    leading-zero suffix bits.
    """
    x = (x + 0x9E3779B97F4A7C15) & _MASK64
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & _MASK64
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & _MASK64
    return x ^ (x >> 31)


def _alpha_m(m: int) -> float:
    """The HLL bias-correction constant alpha_m from the HLL paper."""
    if m == 16:
        return 0.673
    if m == 32:
        return 0.697
    if m == 64:
        return 0.709
    return 0.7213 / (1.0 + 1.079 / m)


def _leading_zeros_plus_one(value: int, max_bits: int) -> int:
    """Return position of the most-significant 1-bit (1-indexed) in
    ``max_bits`` bits. If ``value == 0``, returns ``max_bits + 1``.

    Uses ``int.bit_length`` so the cost is O(1) rather than O(max_bits).
    """
    if value == 0:
        return max_bits + 1
    return max_bits - value.bit_length() + 1


@dataclass(slots=True)
class HyperLogLog:
    """HyperLogLog cardinality sketch as a Bernoulli<int> estimator.

    Parameters
    ----------
    precision : int
        Log2 of the number of registers (``m = 2**precision``). Larger values
        give lower relative error but use more memory. Typical values: 10
        (1024 registers, ~3.25% sigma) to 14 (16384 registers, ~0.81% sigma).
    salt : int
        Optional salt mixed into the hash, for building independent HLLs
        over the same key population.

    Examples
    --------
    >>> hll = HyperLogLog(precision=12)
    >>> for i in range(10000):
    ...     hll.add(str(i).encode())
    >>> est = hll.count()
    >>> abs(est - 10000) / 10000 < 0.05
    True
    """

    precision: int = 14
    salt: int = 0
    _registers: list[int] = field(default_factory=list)

    HASH_BITS: ClassVar[int] = 64

    def __post_init__(self) -> None:
        if not _MIN_PRECISION <= self.precision <= _MAX_PRECISION:
            raise ValueError(
                f"precision must be in [{_MIN_PRECISION}, {_MAX_PRECISION}], "
                f"got {self.precision!r}"
            )
        m = 1 << self.precision
        if not self._registers:
            self._registers = [0] * m
        elif len(self._registers) != m:
            raise ValueError(
                f"register length {len(self._registers)} != m={m}"
            )

    @property
    def m(self) -> int:
        """Number of registers."""
        return 1 << self.precision

    def bits_per_register(self) -> int:
        """6 bits is enough to encode leading-zero counts up to 64."""
        return 6

    def memory_bytes(self) -> int:
        """Compact (packed) memory footprint, 6 bits per register."""
        return (self.m * 6 + 7) // 8

    def expected_relative_error(self) -> float:
        """Asymptotic relative standard deviation: ``1.04 / sqrt(m)``."""
        return 1.04 / math.sqrt(self.m)

    def _hash(self, item: bytes) -> int:
        return _splitmix64(_fnv1a_64(item) ^ self.salt)

    def add(self, item: bytes) -> None:
        """Add an item to the sketch by updating the relevant register."""
        h = self._hash(item)
        # Top ``precision`` bits select the register.
        idx = h >> (self.HASH_BITS - self.precision)
        # Lower (HASH_BITS - precision) bits are the leading-zero suffix.
        remaining = self.HASH_BITS - self.precision
        suffix = h & ((1 << remaining) - 1)
        rho = _leading_zeros_plus_one(suffix, remaining)
        if rho > self._registers[idx]:
            self._registers[idx] = rho

    def count(self) -> float:
        """Estimate cardinality with HLL bias correction (no HLL++ tweaks).

        Returns
        -------
        float
            The cardinality estimate. Standard relative error is approximately
            ``1.04 / sqrt(m)``.
        """
        m = self.m
        alpha = _alpha_m(m)
        # E_raw = alpha * m^2 / sum(2^(-M_i))
        denom = 0.0
        zeros = 0
        for r in self._registers:
            denom += 2.0 ** (-r)
            if r == 0:
                zeros += 1
        if denom == 0.0:
            return float("inf")
        e_raw = alpha * m * m / denom

        # Small-range correction: linear counting when many empty registers.
        if e_raw <= 2.5 * m and zeros > 0:
            return m * math.log(m / zeros)

        # Large-range correction (only matters near 2^32 with 32-bit hashes;
        # with 64-bit hashes it almost never triggers, but keep it for safety).
        two_pow_32 = float(1 << 32)
        if e_raw > two_pow_32 / 30.0:
            # If we used 32-bit hashes this would correct, but we use 64-bit.
            # Skip the correction.
            return e_raw
        return e_raw

    def merge(self, other: HyperLogLog) -> HyperLogLog:
        """Register-wise max merge: returns a new HLL representing A union B.

        Both inputs must have the same precision. Salt must match too, since
        registers are only compatible if items were hashed identically.
        """
        if self.precision != other.precision:
            raise ValueError(
                f"precision mismatch: {self.precision} vs {other.precision}"
            )
        if self.salt != other.salt:
            raise ValueError(
                f"salt mismatch: {self.salt} vs {other.salt}; "
                f"register comparisons require the same hash channel"
            )
        merged = HyperLogLog(precision=self.precision, salt=self.salt)
        merged._registers = [
            max(a, b)
            for a, b in zip(self._registers, other._registers, strict=True)
        ]
        return merged

    def __len__(self) -> int:
        """Cardinality estimate as an integer (rounded)."""
        return int(round(self.count()))
