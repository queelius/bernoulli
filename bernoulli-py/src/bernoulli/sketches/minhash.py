"""MinHash: a Bernoulli<float> Jaccard-similarity estimator.

A MinHash signature is, for each of ``k`` independent hash functions, the minimum
hash value over the set's elements. For two sets, the fraction of signature
positions where the two minima agree is an unbiased estimate of the Jaccard
similarity ``J(A, B) = |A intersect B| / |A union B|``: each position agrees
exactly when the global-minimum element under that hash lies in the intersection,
which happens with probability ``J``.

Framework view
--------------
MinHash outputs a ``Bernoulli<float>`` similarity estimator: ``jaccard`` returns
a value that is approximately Normal with mean ``J`` and standard deviation
``sqrt(J (1 - J) / k)``, at most ``0.5 / sqrt(k)``. Two signatures merge by
element-wise minimum, giving the signature of the union, so MinHash composes the
way a Bernoulli set does.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass, field

from bernoulli.sets.bloom import _fnv1a_64
from bernoulli.sketches.hyperloglog import _splitmix64

_MASK64 = 0xFFFFFFFFFFFFFFFF
_HASH_STRIDE = 0x2545F4914F6CDD1D


@dataclass(slots=True)
class MinHash:
    """A MinHash signature as a ``Bernoulli<float>`` Jaccard estimator.

    Parameters
    ----------
    num_hashes : int
        Signature length ``k``. The relative error of the Jaccard estimate
        scales as ``1 / sqrt(k)``.
    salt : int
        Optional salt; two signatures must share ``num_hashes`` and ``salt`` to
        be comparable (same hash channel).

    Examples
    --------
    >>> a = MinHash.from_items([str(i).encode() for i in range(1000)], num_hashes=256)
    >>> b = MinHash.from_items([str(i).encode() for i in range(500, 1500)], num_hashes=256)
    >>> # true Jaccard of [0,1000) and [500,1500) is 500 / 1500 = 1/3
    >>> abs(a.jaccard(b) - 1 / 3) < 0.06
    True
    """

    num_hashes: int = 128
    salt: int = 0
    _signature: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.num_hashes < 1:
            raise ValueError(f"num_hashes must be >= 1, got {self.num_hashes!r}")
        if not self._signature:
            self._signature = [_MASK64] * self.num_hashes
        elif len(self._signature) != self.num_hashes:
            raise ValueError(
                f"signature length {len(self._signature)} != num_hashes={self.num_hashes}"
            )

    @classmethod
    def from_items(
        cls, items: Iterable[bytes], num_hashes: int = 128, salt: int = 0
    ) -> MinHash:
        """Build a signature from an iterable of byte-string elements."""
        mh = cls(num_hashes=num_hashes, salt=salt)
        for item in items:
            mh.add(item)
        return mh

    def _hashes(self, item: bytes) -> list[int]:
        base = _fnv1a_64(item) ^ self.salt
        return [
            _splitmix64(base ^ ((j * _HASH_STRIDE) & _MASK64))
            for j in range(self.num_hashes)
        ]

    def add(self, item: bytes) -> None:
        """Fold an element into the signature (per-position running minimum)."""
        for j, h in enumerate(self._hashes(item)):
            if h < self._signature[j]:
                self._signature[j] = h

    def signature(self) -> list[int]:
        """A copy of the ``k`` per-hash minima."""
        return list(self._signature)

    def jaccard(self, other: MinHash) -> float:
        """Estimate Jaccard similarity as the fraction of agreeing positions."""
        if self.num_hashes != other.num_hashes:
            raise ValueError(
                f"num_hashes mismatch: {self.num_hashes} vs {other.num_hashes}"
            )
        if self.salt != other.salt:
            raise ValueError(
                f"salt mismatch: {self.salt} vs {other.salt}; signatures must "
                "share a hash channel to be comparable"
            )
        agree = sum(
            1
            for a, b in zip(self._signature, other._signature, strict=True)
            if a == b
        )
        return agree / self.num_hashes

    def merge(self, other: MinHash) -> MinHash:
        """Element-wise minimum: the signature of the union of the two sets."""
        if self.num_hashes != other.num_hashes:
            raise ValueError(
                f"num_hashes mismatch: {self.num_hashes} vs {other.num_hashes}"
            )
        if self.salt != other.salt:
            raise ValueError(f"salt mismatch: {self.salt} vs {other.salt}")
        merged = MinHash(num_hashes=self.num_hashes, salt=self.salt)
        merged._signature = [
            min(a, b)
            for a, b in zip(self._signature, other._signature, strict=True)
        ]
        return merged

    def expected_error(self, jaccard: float | None = None) -> float:
        """Standard deviation of the estimate: ``sqrt(J (1 - J) / k)``.

        With ``jaccard`` unknown, returns the worst case ``0.5 / sqrt(k)`` (at
        ``J = 0.5``).
        """
        if jaccard is None:
            return 0.5 / math.sqrt(self.num_hashes)
        if not 0.0 <= jaccard <= 1.0:
            raise ValueError(f"jaccard must be in [0, 1], got {jaccard!r}")
        return math.sqrt(jaccard * (1.0 - jaccard) / self.num_hashes)

    def memory_bytes(self) -> int:
        """Footprint at 64-bit minima: ``num_hashes * 8`` bytes."""
        return self.num_hashes * 8
