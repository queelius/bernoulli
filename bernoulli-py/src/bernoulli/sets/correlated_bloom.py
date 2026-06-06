"""Multi-salt Bloom filter for studying correlated hash channels.

A research-only variant of :class:`bernoulli.sets.bloom.BloomFilter` whose
``k`` hash functions are derived as ``_fnv1a_64(key) XOR salts[i]`` for an
explicit list of per-hash salts. This sidesteps the Kirsch-Mitzenmacher
double-hashing trick used by ``BloomFilter`` so each hash function is
controlled by exactly one salt; two filters can then be made to share an
arbitrary subset of their hash families by sharing the corresponding salts.

Motivation
----------
Experiment 01 sweeps the two endpoints of hash-family overlap:

- Section A: two filters built with totally independent salts. The empirical
  AND-FPR matches the framework's product prediction
  ``alpha_1 * alpha_2`` to within ~15%.
- Section C: two filters built with the *same* salt. The AND collapses to
  the single-filter FPR (~19x the naive product).

Experiment 05 fills in the spectrum: build two filters with ``s`` shared
salts and ``k - s`` salts that are unique to each filter, vary ``s`` from
``0`` to ``k``, and measure how the empirical AND-FPR / (alpha_1 * alpha_2)
ratio degrades.

The class deliberately exposes one bit per salt; ``add`` sets ``len(salts)``
bits and ``contains`` requires every per-salt position to be set. With this
construction the predicted AND-FPR with ``s`` shared salts and ``k`` total
hashes per filter is::

    p = 1 - exp(-k * n / m)        # bit-set probability (standard formula)
    P(non-member passes filter)    = p^k             (single filter)
    P(non-member passes both)      = p^s * p^(k-s) * p^(k-s) = p^(2k - s)

which exceeds the naive prediction ``(p^k)^2 = p^(2k)`` by a factor of
``p^(-s) > 1`` (since ``p < 1``). At ``s = 0``, the factor is ``1``; at
``s = k``, it collapses to ``p^(-k) = 1 / alpha`` and the AND-FPR equals
the single-filter FPR.

This is a research helper, not a production data structure. The `BloomFilter`
class in :mod:`bernoulli.sets.bloom` remains the standard implementation.
"""

from __future__ import annotations

import math

from bernoulli.sets.bloom import _fnv1a_64


class MultiSaltBloomFilter:
    """Bloom filter parameterized by an explicit list of per-hash salts.

    Each of the ``k = len(salts)`` hash functions is computed as
    ``(_fnv1a_64(key) XOR salts[i]) mod num_bits``. Sharing a salt between
    two filters causes them to query the same bit on every key, which
    correlates their false-positive events.

    Parameters
    ----------
    capacity : int
        Expected number of distinct keys to insert (n). Used to size the bit
        array via the standard Bloom formula
        ``m = -n * ln(target_fpr) / ln(2)^2``.
    target_fpr : float
        Target false-positive rate (alpha). Used only for sizing. The actual
        FPR depends on ``len(salts)`` and the achieved load.
    salts : list[int]
        One 64-bit salt per hash function. ``len(salts)`` is the effective
        ``k`` of the filter; it does not have to match the optimal ``k`` for
        ``(capacity, target_fpr)``. Salts are coerced to 64-bit unsigned ints.

    Notes
    -----
    Bit array sizing (``m``) is identical to :class:`BloomFilter`. The number
    of hash functions, however, is dictated by ``len(salts)`` rather than by
    the optimal-k formula; that is the whole point of the class.

    Examples
    --------
    >>> mbf = MultiSaltBloomFilter(capacity=1000, target_fpr=0.05,
    ...                            salts=[0xA, 0xB, 0xC])
    >>> mbf.num_hashes
    3
    >>> mbf.add(b"hello")
    >>> mbf.contains(b"hello")
    True
    """

    def __init__(
        self,
        capacity: int,
        target_fpr: float,
        salts: list[int],
    ) -> None:
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity!r}")
        if not 0.0 < target_fpr < 1.0:
            raise ValueError(f"target_fpr must be in (0, 1), got {target_fpr!r}")
        if not salts:
            raise ValueError("salts must contain at least one entry")

        # Same sizing as BloomFilter: m = -n * ln(alpha) / ln(2)^2, byte-aligned.
        bits_real = -capacity * math.log(target_fpr) / (math.log(2.0) ** 2)
        self._num_bits = max(8, int(math.ceil(bits_real)))
        self._num_bits = ((self._num_bits + 7) // 8) * 8

        self._capacity = capacity
        self._target_fpr = target_fpr
        self._salts: tuple[int, ...] = tuple(s & 0xFFFFFFFFFFFFFFFF for s in salts)
        self._bits = bytearray(self._num_bits // 8)
        self._num_inserted = 0

    @property
    def num_bits(self) -> int:
        return self._num_bits

    @property
    def num_hashes(self) -> int:
        return len(self._salts)

    @property
    def salts(self) -> tuple[int, ...]:
        return self._salts

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
        """Asymptotic FPR using the standard Bloom formula with k = len(salts).

        Note that ``len(salts)`` is *not* necessarily optimal for the
        configured ``(capacity, target_fpr)``; the value reported here is the
        formula prediction at the actual load and the actual k.
        """
        n = max(self._num_inserted, 1)
        m = self._num_bits
        k = len(self._salts)
        if m == 0 or k == 0:
            return 0.0
        p_bit_set = 1.0 - math.exp(-k * n / m)
        return p_bit_set ** k

    def _positions(self, key: bytes) -> list[int]:
        """k position indices for a key, one per salt, no double-hashing."""
        h = _fnv1a_64(key)
        m = self._num_bits
        return [(h ^ s) % m for s in self._salts]

    def add(self, key: bytes) -> None:
        for pos in self._positions(key):
            self._bits[pos >> 3] |= 1 << (pos & 7)
        self._num_inserted += 1

    def contains(self, key: bytes) -> bool:
        return all(
            self._bits[pos >> 3] & (1 << (pos & 7))
            for pos in self._positions(key)
        )

    def __len__(self) -> int:
        return self._num_inserted

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError(f"key must be bytes-like, got {type(key).__name__}")
        return self.contains(bytes(key))


def make_correlated_pair(
    capacity: int,
    target_fpr: float,
    k: int,
    s: int,
    rng_or_seed: int,
) -> tuple[MultiSaltBloomFilter, MultiSaltBloomFilter, dict[str, list[int]]]:
    """Build two ``MultiSaltBloomFilter`` instances sharing ``s`` of ``k`` hashes.

    Returns the pair of (filter_1, filter_2, salt_assignment_dict).

    Parameters
    ----------
    capacity : int
        Sizing capacity passed to each filter.
    target_fpr : float
        Sizing target FPR passed to each filter.
    k : int
        Number of hash functions per filter.
    s : int
        Number of hash functions shared between the two filters.
        ``0 <= s <= k``. ``s == 0`` gives independent salts; ``s == k`` gives
        identical filters.
    rng_or_seed : int
        Seed for an internal :class:`random.Random` used to draw all salts.
        Passing the same seed for repeated calls reproduces the salts; the
        same seed across two ``s`` values does NOT reuse salts (each call
        draws a fresh salt vector of length ``2*k - s``).

    Returns
    -------
    (filter_1, filter_2, salts)
        ``salts`` is a dict with keys ``"shared"``, ``"only_1"``, ``"only_2"``
        listing the salt values used.
    """
    if not 0 <= s <= k:
        raise ValueError(f"need 0 <= s <= k, got s={s!r}, k={k!r}")
    import random as _random

    rng = _random.Random(rng_or_seed)

    def _draw_salts(n: int) -> list[int]:
        return [rng.getrandbits(64) for _ in range(n)]

    shared = _draw_salts(s)
    only_1 = _draw_salts(k - s)
    only_2 = _draw_salts(k - s)

    salts_1 = only_1 + shared
    salts_2 = only_2 + shared
    f1 = MultiSaltBloomFilter(capacity=capacity, target_fpr=target_fpr, salts=salts_1)
    f2 = MultiSaltBloomFilter(capacity=capacity, target_fpr=target_fpr, salts=salts_2)
    return f1, f2, {"shared": shared, "only_1": only_1, "only_2": only_2}


__all__ = ["MultiSaltBloomFilter", "make_correlated_pair"]
