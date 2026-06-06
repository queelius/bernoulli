"""A minimal perfect hash function (BBHash) over a static key set.

A perfect hash maps each key of a build set ``S`` to a distinct slot, and is
*minimal* when the slots are exactly ``{0, ..., n-1}``. This is the slot-
assignment layer of the Bernoulli hash function (book chapter 14): a perfect
hash plus a per-slot fingerprint gives a space-near-optimal approximate set
(see :class:`bernoulli.maps.PerfectFilter`).

Construction (BBHash, Limasset et al. 2017)
-------------------------------------------
Hash all remaining keys into a bit array of ``gamma * n`` cells. Keys that land
alone in a cell (no collision) are *assigned* that cell and removed; colliding
keys recurse to the next level on a fresh, smaller array. A handful of levels
assigns everyone. The minimal slot of a key is then ``(keys assigned in earlier
levels) + (rank of its cell within its level)``.

This is a pure-Python reference. The per-level prefix-popcount used for ranking
is stored as an integer list for clarity; a production structure replaces it
with a succinct rank index costing about ``0.25`` bits per cell. ``bits_per_key``
reports the *logical* BBHash size (the level bit arrays), not the Python
objects.
"""

from __future__ import annotations

import math

_MASK64 = 0xFFFFFFFFFFFFFFFF
_GOLDEN = 0x9E3779B97F4A7C15


def _fnv1a_64(data: bytes) -> int:
    """64-bit FNV-1a base hash of a key."""
    h = 0xCBF29CE484222325
    for byte in data:
        h ^= byte
        h = (h * 0x100000001B3) & _MASK64
    return h


def _splitmix64(x: int) -> int:
    """One round of the splitmix64 mixer (a good 64-bit avalanche)."""
    x = (x + _GOLDEN) & _MASK64
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & _MASK64
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & _MASK64
    return x ^ (x >> 31)


def _level_hash(base: int, level_seed: int) -> int:
    """A per-level hash derived from a key's base hash and the level seed.

    Mixing the base hash with a well-spread level seed gives effectively
    independent placements across levels from a single FNV pass per key.
    """
    return _splitmix64(base ^ _splitmix64(level_seed)) & _MASK64


class _Level:
    """One BBHash level: a cell bit array plus its rank metadata."""

    __slots__ = ("bits", "m", "seed", "base_rank", "prefix")

    def __init__(self, bits: bytearray, m: int, seed: int, base_rank: int) -> None:
        self.bits = bits
        self.m = m
        self.seed = seed
        self.base_rank = base_rank
        # prefix[i] = number of set bits in positions [0, i); prefix[m] = popcount.
        prefix = [0] * (m + 1)
        run = 0
        for i in range(m):
            prefix[i] = run
            run += (bits[i >> 3] >> (i & 7)) & 1
        prefix[m] = run
        self.prefix = prefix


class MinimalPerfectHash:
    """A minimal perfect hash over ``keys`` (satisfies ``PerfectHashFunction``).

    Parameters
    ----------
    keys : list[bytes]
        The build set. Duplicates are ignored (the first occurrence wins).
    gamma : float
        Load factor for each level's bit array (cells = ``gamma * remaining``).
        Larger ``gamma`` assigns more keys per level (fewer levels, faster build)
        at a higher bits-per-key cost; ``gamma = 2.0`` is a robust default.
    seed : int
        Base seed for the level hash family.

    Examples
    --------
    >>> keys = [f"key-{i}".encode() for i in range(1000)]
    >>> mph = MinimalPerfectHash(keys)
    >>> slots = sorted(mph.slot_for(k) for k in keys)
    >>> slots == list(range(1000))      # a bijection onto {0, ..., n-1}
    True
    """

    def __init__(
        self, keys: list[bytes], gamma: float = 2.0, seed: int = 1, max_levels: int = 32
    ) -> None:
        if gamma <= 1.0:
            raise ValueError(f"gamma must be > 1, got {gamma!r}")

        # Deduplicate while preserving order; work on (key, base-hash) pairs.
        unique = list(dict.fromkeys(keys))
        remaining = [(_fnv1a_64(k)) for k in unique]

        self._levels: list[_Level] = []
        base_rank = 0
        level = 0
        while remaining:
            if level >= max_levels:
                raise RuntimeError(
                    f"BBHash did not converge in {max_levels} levels; "
                    "try a larger gamma or check for hash pathologies"
                )
            m = max(1, math.ceil(gamma * len(remaining)))
            level_seed = seed + level
            positions = [_level_hash(base, level_seed) % m for base in remaining]

            counts = [0] * m
            for p in positions:
                counts[p] += 1

            bits = bytearray((m + 7) // 8)
            assigned = 0
            for i in range(m):
                if counts[i] == 1:
                    bits[i >> 3] |= 1 << (i & 7)
                    assigned += 1

            self._levels.append(_Level(bits, m, level_seed, base_rank))
            base_rank += assigned
            remaining = [
                base
                for base, p in zip(remaining, positions, strict=True)
                if counts[p] != 1
            ]
            level += 1

        self._n = base_rank  # == number of unique keys

    def slot_for(self, key: bytes) -> int:
        """The minimal slot for ``key``.

        For a build-set key this is its unique index in ``[0, n)``. For a
        non-member it is an arbitrary valid index (the fingerprint layer, not
        the PHF, decides membership).
        """
        base = _fnv1a_64(key)
        for level in self._levels:
            p = _level_hash(base, level.seed) % level.m
            if (level.bits[p >> 3] >> (p & 7)) & 1:
                return level.base_rank + level.prefix[p]
        return 0

    def num_keys(self) -> int:
        return self._n

    def range_size(self) -> int:
        # Minimal: the slot range equals the key count.
        return self._n

    def structure_bits(self) -> int:
        """Total logical size of the BBHash level bit arrays, in bits."""
        return sum(level.m for level in self._levels)

    def bits_per_key(self) -> float:
        """Logical BBHash bits per key (the level bit arrays only)."""
        return self.structure_bits() / self._n if self._n else 0.0

    def memory_bytes(self) -> int:
        """Logical size of the level bit arrays, in bytes."""
        return sum((level.m + 7) // 8 for level in self._levels)
