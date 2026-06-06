"""Static GF(2) retrieval and codec-controlled non-member output (book ch. 9).

A *retrieval* structure stores a function ``f : keys -> r-bit values`` for a
known key set in about ``r`` bits per key, storing **no keys at all**. It cannot
answer membership (every input gets some value), but on the build set it returns
the stored value exactly, and on non-members it returns an approximately uniform
``r``-bit pattern.

:class:`GF2Retrieval` is the peeling (XOR-filter) construction: each key maps to
three slots (one per segment), and a solution vector ``Z`` is found so that
``Z[h0] xor Z[h1] xor Z[h2] == value`` for every build key. The key trick for a
*uniform* non-member output (so a codec, not the storage statistics, controls
it) is to seed every slot with a random value first, then back-substitute the
pivots: members still retrieve exactly, non-members XOR three random-looking
slots and come out uniform.

:class:`EncodedRetrieval` composes a retrieval with a
:mod:`bernoulli.maps.codec`: the codec's codespace allocation then **controls
the non-member value distribution**. This is the maph CODESPACE_NONMEMBERS
result (`~/github/repos/maph/docs/CODESPACE_NONMEMBERS.md`): for a query not in
the build set, ``P(query returns v) == codec.codespace_fraction(v)``, regardless
of how often ``v`` was stored.

The ribbon construction of Dietzfelbinger and Walzer is the cache- and
load-optimized variant of the same GF(2) retrieval (a banded coefficient matrix
solved by on-line Gaussian elimination instead of peeling). The peeling form
here is the simplest correct reference; the band is a performance concern,
deferred with the rest of the C-accelerated hot paths.
"""

from __future__ import annotations

import math
from collections import deque
from collections.abc import Mapping
from typing import Generic, Protocol, TypeVar

from bernoulli.maps.perfect_hash import _fnv1a_64, _level_hash, _splitmix64

V = TypeVar("V")

_SEG1_SEED = 0x1111111111111111
_SEG2_SEED = 0x2222222222222222
_FREE_SEED = 0x6E5D4C3B2A190817


class GF2Retrieval:
    """A static ``keys -> value_bits`` retrieval built by GF(2) peeling.

    Parameters
    ----------
    items : Mapping[bytes, int]
        The build map; each value is reduced modulo ``2 ** value_bits``.
    value_bits : int
        Width ``r`` of the stored values.
    overhead : float
        Slot count is ``ceil(overhead * n / 3) * 3``. Must exceed 1; the
        3-segment peeling threshold is near 1.12 asymptotically, so the
        default 1.23 leaves room for finite-``n`` retries.
    max_tries : int
        Number of reseed attempts before giving up (peeling can fail; a fresh
        seed almost always succeeds).
    seed : int
        Base hash seed.

    Examples
    --------
    >>> items = {f"k{i}".encode(): i % 16 for i in range(500)}
    >>> ret = GF2Retrieval(items, value_bits=4)
    >>> all(ret.query(k) == v for k, v in items.items())   # exact on the build set
    True
    """

    def __init__(
        self,
        items: Mapping[bytes, int],
        value_bits: int,
        *,
        overhead: float = 1.23,
        max_tries: int = 64,
        seed: int = 1,
    ) -> None:
        if value_bits < 1:
            raise ValueError(f"value_bits must be >= 1, got {value_bits!r}")
        if overhead <= 1.0:
            raise ValueError(f"overhead must be > 1, got {overhead!r}")

        self._r = value_bits
        self._mask = (1 << value_bits) - 1
        keys = list(items)
        self._n = len(keys)
        self._seg = 0
        self._m = 0
        self._seed_used = seed
        self._z: list[int] = []
        if self._n == 0:
            return

        vals = [items[k] & self._mask for k in keys]
        # Additive slack (the standard XOR-filter +32) keeps the segments roomy
        # for small n, where a bare overhead*n would collapse seg toward 1 and
        # make every key collide on the same three slots; it vanishes as n grows.
        seg = max(1, math.ceil((overhead * self._n + 32) / 3))
        m = 3 * seg

        for trial in range(max_tries):
            trial_seed = (seed + trial * 0x9E3779B1) & 0xFFFFFFFFFFFFFFFF
            edges = [self._positions(k, seg, trial_seed) for k in keys]
            order = self._peel(edges, m)
            if order is not None:
                self._seg = seg
                self._m = m
                self._seed_used = trial_seed
                self._z = self._back_substitute(edges, vals, order, m, trial_seed)
                return

        raise RuntimeError(
            f"GF(2) peeling failed in {max_tries} tries for n={self._n}; "
            "raise overhead"
        )

    def _positions(self, key: bytes, seg: int, seed: int) -> tuple[int, int, int]:
        """Three distinct slots, one per segment (always peelable-shaped)."""
        base = _fnv1a_64(key)
        return (
            _level_hash(base, seed) % seg,
            seg + _level_hash(base, seed ^ _SEG1_SEED) % seg,
            2 * seg + _level_hash(base, seed ^ _SEG2_SEED) % seg,
        )

    @staticmethod
    def _peel(edges: list[tuple[int, int, int]], m: int) -> list[tuple[int, int]] | None:
        """Peel the 3-hypergraph; return (key, pivot-slot) pairs in peel order.

        Uses the XOR trick: each slot tracks the count and the XOR of incident
        live key indices, so a degree-1 slot reveals its single key directly.
        Returns ``None`` if not fully peelable.
        """
        count = [0] * m
        xor_id = [0] * m
        for i, (a, b, c) in enumerate(edges):
            for s in (a, b, c):
                count[s] += 1
                xor_id[s] ^= i

        order: list[tuple[int, int]] = []
        peeled = [False] * len(edges)
        queue = deque(s for s in range(m) if count[s] == 1)
        while queue:
            s = queue.popleft()
            if count[s] != 1:
                continue
            i = xor_id[s]
            if peeled[i]:
                continue
            peeled[i] = True
            order.append((i, s))
            for s2 in edges[i]:
                count[s2] -= 1
                xor_id[s2] ^= i
                if count[s2] == 1:
                    queue.append(s2)

        return order if len(order) == len(edges) else None

    def _back_substitute(
        self,
        edges: list[tuple[int, int, int]],
        vals: list[int],
        order: list[tuple[int, int]],
        m: int,
        seed: int,
    ) -> list[int]:
        """Seed every slot random, then fix pivots in reverse peel order."""
        z = [_splitmix64(seed ^ (slot * 0x9E3779B97F4A7C15)) & self._mask for slot in range(m)]
        for i, pivot in reversed(order):
            a, b, c = edges[i]
            others = [p for p in (a, b, c) if p != pivot]
            z[pivot] = vals[i] ^ z[others[0]] ^ z[others[1]]
        return z

    def query(self, key: bytes) -> int:
        """Retrieve the ``r``-bit value for ``key`` (exact for build keys)."""
        if self._n == 0:
            return 0
        a, b, c = self._positions(key, self._seg, self._seed_used)
        return self._z[a] ^ self._z[b] ^ self._z[c]

    def value_bits(self) -> int:
        return self._r

    def num_keys(self) -> int:
        return self._n

    def bits_per_key(self) -> float:
        """Stored bits per key: ``m * r / n`` (overhead times ``r``)."""
        return (self._m * self._r) / self._n if self._n else 0.0

    def memory_bytes(self) -> int:
        return (self._m * self._r + 7) // 8 if self._n else 0


class _Codec(Protocol[V]):
    """The codec surface :class:`EncodedRetrieval` needs."""

    m_bits: int

    def encode(self, value: V) -> int: ...

    def decode(self, pattern: int) -> V: ...

    def non_member_distribution(self) -> dict[V, float]: ...


class EncodedRetrieval(Generic[V]):
    """Retrieval composed with a codec: the codec controls non-member output.

    For a build key, returns the stored value exactly. For a non-member, returns
    ``codec.decode(uniform pattern)``, so the non-member value distribution is
    the codec's codespace allocation, ``non_member_distribution()``, independent
    of how often each value was stored.

    Parameters
    ----------
    mapping : Mapping[bytes, V]
        Build map from keys to values in the codec's vocabulary.
    codec : codec with ``m_bits``, ``encode``, ``decode``, ``non_member_distribution``.
    overhead, seed : passed to :class:`GF2Retrieval`.

    Examples
    --------
    >>> from bernoulli.maps.codec import DenseCodec
    >>> codec = DenseCodec(["a", "b", "c", "d"], m_bits=2)
    >>> data = {f"k{i}".encode(): "abcd"[i % 4] for i in range(400)}
    >>> er = EncodedRetrieval(data, codec)
    >>> all(er.query(k) == v for k, v in data.items())   # exact on the build set
    True
    """

    def __init__(
        self,
        mapping: Mapping[bytes, V],
        codec: _Codec[V],
        *,
        overhead: float = 1.23,
        seed: int = 1,
    ) -> None:
        self._codec = codec
        encoded = {key: codec.encode(value) for key, value in mapping.items()}
        self._retrieval = GF2Retrieval(
            encoded, value_bits=codec.m_bits, overhead=overhead, seed=seed
        )

    def query(self, key: bytes) -> V:
        return self._codec.decode(self._retrieval.query(key))

    def num_keys(self) -> int:
        return self._retrieval.num_keys()

    def bits_per_key(self) -> float:
        return self._retrieval.bits_per_key()

    def memory_bytes(self) -> int:
        return self._retrieval.memory_bytes()

    def non_member_distribution(self) -> dict[V, float]:
        """The predicted non-member value distribution (the codec's allocation)."""
        return self._codec.non_member_distribution()
