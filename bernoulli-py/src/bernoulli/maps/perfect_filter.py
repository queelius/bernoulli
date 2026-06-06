"""The perfect-hash filter: the Bernoulli hash function of book chapter 14.

A :class:`PerfectFilter` is a static approximate set built from a known key set.
It pairs a minimal perfect hash (slot assignment) with an ``r``-bit fingerprint
per slot:

- **Build:** assign each key a unique slot via the perfect hash, and store the
  key's ``r``-bit fingerprint in that slot.
- **Query ``x``:** read the fingerprint at ``slot_for(x)`` and compare it to
  ``x``'s fingerprint. Match means "present".

Because every build key owns its slot and its own fingerprint is stored there,
a member always matches: ``fnr = 0`` exactly. A non-member lands on some slot
holding an unrelated fingerprint, which matches its own with probability
``2^-r``: ``fpr = 2^-r``.

Space is ``mu + r`` bits per key, where ``mu`` is the perfect hash's overhead
(a few bits, see :class:`bernoulli.maps.MinimalPerfectHash`) and ``r`` is the
fingerprint width. With ``r = ceil(-log2 epsilon)`` this is
``-log2 epsilon + mu``, the chapter 14 / chapter 8 bound, below the Bloom
filter's ``1.44 * (-log2 epsilon)`` whenever ``mu`` is smaller than Bloom's
``0.44 * (-log2 epsilon)`` slack. The price is that the set must be known up
front: unlike a Bloom filter, a PerfectFilter is not incrementally insertable.

See :mod:`bernoulli.sets.entropy_bound` for the matching space model
(``bhf_bits_per_key(epsilon, perfect_hash_overhead=mu)``).
"""

from __future__ import annotations

import math
from collections.abc import Iterable

from bernoulli.atom import BernoulliBool
from bernoulli.maps.perfect_hash import (
    MinimalPerfectHash,
    _fnv1a_64,
    _level_hash,
)

# A dedicated seed, far from the PHF level seeds, so the fingerprint hash is
# independent of the slot-assignment hash.
_FINGERPRINT_SEED = 0xA5A5A5A5A5A5A5A5


class PerfectFilter:
    """A static perfect-hash filter (BHF): ``fnr = 0``, ``fpr = 2^-r``.

    Parameters
    ----------
    keys : Iterable[bytes]
        The build set. Duplicates are ignored.
    target_fpr : float, optional
        Desired false-positive rate; the fingerprint width is
        ``ceil(-log2 target_fpr)`` and the achieved FPR is ``2^-r <= target_fpr``.
    fingerprint_bits : int, optional
        Set the fingerprint width ``r`` directly (overrides ``target_fpr``).
    gamma, seed : passed to :class:`MinimalPerfectHash`.

    Examples
    --------
    >>> keys = [f"key-{i}".encode() for i in range(2000)]
    >>> pf = PerfectFilter(keys, target_fpr=0.01)
    >>> all(pf.contains(k) for k in keys)        # no false negatives, ever
    True
    >>> pf.fpr() <= 0.01
    True
    """

    def __init__(
        self,
        keys: Iterable[bytes],
        *,
        target_fpr: float | None = None,
        fingerprint_bits: int | None = None,
        gamma: float = 2.0,
        seed: int = 1,
    ) -> None:
        if fingerprint_bits is not None:
            if fingerprint_bits < 1:
                raise ValueError(
                    f"fingerprint_bits must be >= 1, got {fingerprint_bits!r}"
                )
            r = fingerprint_bits
        elif target_fpr is not None:
            if not 0.0 < target_fpr < 1.0:
                raise ValueError(f"target_fpr must be in (0, 1), got {target_fpr!r}")
            r = max(1, math.ceil(-math.log2(target_fpr)))
        else:
            raise ValueError("provide either target_fpr or fingerprint_bits")

        unique = list(dict.fromkeys(keys))
        self._n = len(unique)
        self._r = r
        self._mask = (1 << r) - 1
        self._phf: MinimalPerfectHash | None = (
            MinimalPerfectHash(unique, gamma=gamma, seed=seed) if unique else None
        )
        self._fingerprints = [0] * self._n
        if self._phf is not None:
            for key in unique:
                self._fingerprints[self._phf.slot_for(key)] = self._fingerprint(key)

    def _fingerprint(self, key: bytes) -> int:
        """The ``r``-bit fingerprint of a key (independent of the slot hash)."""
        return _level_hash(_fnv1a_64(key), _FINGERPRINT_SEED) & self._mask

    def contains(self, key: bytes) -> bool:
        if self._phf is None:
            return False
        slot = self._phf.slot_for(key)
        return self._fingerprints[slot] == self._fingerprint(key)

    def slot_for(self, key: bytes) -> int | None:
        """The slot of ``key`` if present (fingerprint matches), else ``None``."""
        if self._phf is None:
            return None
        slot = self._phf.slot_for(key)
        return slot if self._fingerprints[slot] == self._fingerprint(key) else None

    def query(self, key: bytes) -> BernoulliBool:
        """Lift membership into a one-sided ``BernoulliBool`` (``fnr = 0``)."""
        return BernoulliBool.one_sided_fpr(value=self.contains(key), fpr=self.fpr())

    def fpr(self) -> float:
        """Configured false-positive rate ``2^-r``."""
        return 2.0 ** (-self._r)

    def fnr(self) -> float:
        """Structurally zero: a member always matches its own fingerprint."""
        return 0.0

    def fingerprint_bits(self) -> int:
        return self._r

    def num_keys(self) -> int:
        return self._n

    def range_size(self) -> int:
        return self._n

    def bits_per_key(self) -> float:
        """Perfect-hash overhead plus fingerprint width, in bits per key."""
        if self._phf is None:
            return 0.0
        return self._phf.bits_per_key() + self._r

    def memory_bytes(self) -> int:
        if self._phf is None:
            return 0
        return self._phf.memory_bytes() + (self._n * self._r + 7) // 8

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError(f"key must be bytes-like, got {type(key).__name__}")
        return self.contains(bytes(key))

    def __len__(self) -> int:
        return self._n
