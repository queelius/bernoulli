"""Pure-Python Bloom filter as a Bernoulli<set>.

A small, dependency-free reference implementation. A C-accelerated variant
with the same public surface is planned (``c/bloom.c``); none exists yet.

Design notes
------------
- Hash mixing uses a single 64-bit base hash (FNV-1a inlined) plus the
  Kirsch-Mitzenmacher double-hashing trick: ``h_i(x) = h1(x) + i * h2(x)``,
  using the upper and lower halves of the 64-bit base hash.
- Bit storage is a Python ``bytearray`` (8 bits per byte). Ample for the
  scales relevant to teaching and unit testing.
- The class implements the :class:`bernoulli.sets.MembershipOracle` protocol.
- ``query(x)`` returns a :class:`bernoulli.atom.BernoulliBool` lifted with
  the configured FPR and ``fnr=0`` (the structural property of Bloom).
"""

from __future__ import annotations

import math

from bernoulli.algebra import (
    bloom_filter_fpr,
    bloom_filter_optimal_k,
)
from bernoulli.atom import BernoulliBool


def _fnv1a_64(data: bytes) -> int:
    """64-bit FNV-1a hash."""
    h = 0xCBF29CE484222325
    for byte in data:
        h ^= byte
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def _split64(h: int) -> tuple[int, int]:
    """Split a 64-bit hash into two 32-bit halves for double-hashing."""
    return (h & 0xFFFFFFFF, (h >> 32) & 0xFFFFFFFF)


class BloomFilter:
    """Classical k-hash Bloom filter.

    Parameters
    ----------
    capacity : int
        Expected number of distinct keys to insert (n).
    target_fpr : float
        Desired false-positive rate (alpha). Used to size the bit array
        and select k.
    salt : int
        Optional salt added to the hash; lets you build several
        statistically independent Bloom filters from the same key set.

    Examples
    --------
    >>> bf = BloomFilter(capacity=1000, target_fpr=0.01)
    >>> bf.add(b"hello")
    >>> bf.contains(b"hello")
    True
    >>> isinstance(bf.query(b"hello"), BernoulliBool)
    True
    """

    def __init__(
        self,
        capacity: int,
        target_fpr: float,
        salt: int = 0,
    ) -> None:
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity!r}")
        if not 0.0 < target_fpr < 1.0:
            raise ValueError(f"target_fpr must be in (0, 1), got {target_fpr!r}")

        # m = -n * ln(alpha) / ln(2)^2
        bits_real = -capacity * math.log(target_fpr) / (math.log(2.0) ** 2)
        self._num_bits = max(8, int(math.ceil(bits_real)))
        # Round up to a multiple of 8 for byte alignment.
        self._num_bits = ((self._num_bits + 7) // 8) * 8

        k_real = bloom_filter_optimal_k(num_keys=capacity, num_bits=self._num_bits)
        self._num_hashes = max(1, int(round(k_real)))

        self._capacity = capacity
        self._target_fpr = target_fpr
        self._salt = salt & 0xFFFFFFFFFFFFFFFF
        self._bits = bytearray(self._num_bits // 8)
        self._num_inserted = 0

    @property
    def num_bits(self) -> int:
        return self._num_bits

    @property
    def num_hashes(self) -> int:
        return self._num_hashes

    @property
    def num_inserted(self) -> int:
        return self._num_inserted

    def num_keys(self) -> int:
        return self._num_inserted

    def memory_bytes(self) -> int:
        return self._num_bits // 8

    def bits_per_key(self) -> float:
        if self._num_inserted == 0:
            return float("inf") if self._num_bits > 0 else 0.0
        return self._num_bits / self._num_inserted

    def fpr(self) -> float:
        """Asymptotic FPR at current load (matches the formula, not measured)."""
        n_eff = max(self._num_inserted, 1)
        return bloom_filter_fpr(
            num_keys=n_eff,
            num_bits=self._num_bits,
            num_hashes=self._num_hashes,
        )

    def _positions(self, key: bytes) -> list[int]:
        """k position indices for a key, derived by Kirsch-Mitzenmacher."""
        h = _fnv1a_64(key) ^ self._salt
        h1, h2 = _split64(h)
        # Ensure h2 is odd to avoid degenerate cycles in the AP.
        if h2 == 0:
            h2 = 1
        positions = []
        for i in range(self._num_hashes):
            pos = (h1 + i * h2) % self._num_bits
            positions.append(pos)
        return positions

    def add(self, key: bytes) -> None:
        for pos in self._positions(key):
            self._bits[pos >> 3] |= 1 << (pos & 7)
        self._num_inserted += 1

    def contains(self, key: bytes) -> bool:
        return all(
            self._bits[pos >> 3] & (1 << (pos & 7))
            for pos in self._positions(key)
        )

    def query(self, key: bytes) -> BernoulliBool:
        """Lift ``contains`` into a one-sided ``BernoulliBool`` with current FPR."""
        return BernoulliBool.one_sided_fpr(value=self.contains(key), fpr=self.fpr())

    def __len__(self) -> int:
        return self._num_inserted

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError(f"key must be bytes-like, got {type(key).__name__}")
        return self.contains(bytes(key))
