"""Count-Min sketch: a Bernoulli<int> frequency estimator with one-sided error.

A Count-Min sketch estimates the frequency of each key in a stream using a
``depth x width`` table of counters and one hash function per row. ``add(key)``
increments one counter per row; ``estimate(key)`` is the *minimum* of those
counters. Collisions only ever add to a counter, so the estimate is never below
the true count: the error is one-sided (overestimate only), the integer-valued
analogue of a Bloom filter's one-sided false positives.

Framework view
--------------
Count-Min is a ``Bernoulli<int>`` estimator with ``fnr = 0`` on the count axis
(it never undercounts) and a bounded overcount. With ``width = e / epsilon`` and
``depth = ln(1 / delta)``, the estimate exceeds the truth by at most
``epsilon * N`` (``N`` = total mass added) with probability at least
``1 - delta``. The minimum across rows is the debiasing step: each row is an
independent overestimate, and the smallest is the tightest.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from bernoulli.sets.bloom import _fnv1a_64
from bernoulli.sketches.hyperloglog import _splitmix64

_ROW_STRIDE = 0x9E3779B97F4A7C15
_MASK64 = 0xFFFFFFFFFFFFFFFF


@dataclass(slots=True)
class CountMinSketch:
    """A Count-Min frequency sketch as a one-sided ``Bernoulli<int>`` estimator.

    Parameters
    ----------
    width : int
        Counters per row. Controls the additive error ``epsilon = e / width``.
    depth : int
        Number of rows (independent hashes). Controls the failure probability
        ``delta = e ** -depth``.
    salt : int
        Optional salt for independent sketches over the same stream.

    Examples
    --------
    >>> cms = CountMinSketch(width=2000, depth=5)
    >>> for _ in range(100):
    ...     cms.add(b"apple")
    >>> cms.add(b"pear")
    >>> cms.estimate(b"apple") >= 100      # never an undercount
    True
    >>> cms.estimate(b"never-added") >= 0
    True
    """

    width: int
    depth: int
    salt: int = 0
    _table: list[list[int]] = field(default_factory=list)
    _total: int = 0

    def __post_init__(self) -> None:
        if self.width < 1:
            raise ValueError(f"width must be >= 1, got {self.width!r}")
        if self.depth < 1:
            raise ValueError(f"depth must be >= 1, got {self.depth!r}")
        if not self._table:
            self._table = [[0] * self.width for _ in range(self.depth)]
        elif len(self._table) != self.depth or any(
            len(row) != self.width for row in self._table
        ):
            raise ValueError("provided table does not match (depth, width)")

    @classmethod
    def from_error(
        cls, epsilon: float, delta: float, salt: int = 0
    ) -> CountMinSketch:
        """Size the sketch for additive error ``epsilon * N`` at confidence ``1 - delta``.

        ``width = ceil(e / epsilon)`` and ``depth = ceil(ln(1 / delta))``.
        """
        if not 0.0 < epsilon < 1.0:
            raise ValueError(f"epsilon must be in (0, 1), got {epsilon!r}")
        if not 0.0 < delta < 1.0:
            raise ValueError(f"delta must be in (0, 1), got {delta!r}")
        width = math.ceil(math.e / epsilon)
        depth = math.ceil(math.log(1.0 / delta))
        return cls(width=width, depth=max(1, depth), salt=salt)

    def _positions(self, key: bytes) -> list[int]:
        base = _fnv1a_64(key) ^ self.salt
        return [
            _splitmix64(base ^ ((row * _ROW_STRIDE) & _MASK64)) % self.width
            for row in range(self.depth)
        ]

    def add(self, key: bytes, count: int = 1) -> None:
        """Add ``count`` occurrences of ``key`` (default 1)."""
        if count < 0:
            raise ValueError(f"count must be non-negative, got {count!r}")
        for row, pos in enumerate(self._positions(key)):
            self._table[row][pos] += count
        self._total += count

    def estimate(self, key: bytes) -> int:
        """Estimate the count of ``key`` (the row minimum; never an undercount)."""
        return min(
            self._table[row][pos] for row, pos in enumerate(self._positions(key))
        )

    def total(self) -> int:
        """Total mass added so far (``N``)."""
        return self._total

    def error_bound(self) -> float:
        """Additive overestimate bound ``epsilon * N`` with ``epsilon = e / width``."""
        return (math.e / self.width) * self._total

    def memory_bytes(self) -> int:
        """Footprint at 32-bit counters: ``width * depth * 4`` bytes."""
        return self.width * self.depth * 4

    def __getitem__(self, key: bytes) -> int:
        return self.estimate(key)
