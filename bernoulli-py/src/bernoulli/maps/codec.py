"""Codecs: value-to-bit-pattern maps for Bernoulli<map> retrieval.

A *codec* assigns to each logical value ``v`` in a finite alphabet a class
of ``M``-bit patterns. The size of that class divided by ``2^M`` is the
codespace fraction allocated to ``v``.

Three concrete codecs are provided:

- :class:`DenseCodec`: ``|V| = 2^M`` (or smaller), every value gets exactly
  one M-bit pattern. Codespace fractions are uniform at ``1 / 2^M``. Special
  case of :class:`PrefixCodec` with all codeword lengths equal to ``M``.

- :class:`PaddedCodec`: one designated default value absorbs the surplus.
  Each non-default value gets exactly one M-bit pattern; the default
  collects the rest. Useful when one outcome dominates (sparse maps).

- :class:`PrefixCodec`: prefix-free (Huffman-style). Each value ``v`` gets a
  codeword of length ``l_v <= M``; the codespace fraction is ``2^(-l_v)``.
  Built either from explicit ``(value, length)`` pairs (subject to Kraft)
  or from frequencies via :meth:`PrefixCodec.from_frequencies` (which runs
  a Huffman procedure).

Why codecs matter for non-member output
---------------------------------------
The maph project verified empirically that for ribbon-based retrieval, the
non-member output distribution is determined by the codec's codespace
allocation, not by the storage frequency of values. The mechanism: ribbon
back-substitution produces approximately uniform M-bit patterns for keys
not in the build set; decoding through the codec maps those uniform
patterns to values according to the per-value codespace fractions.

In Bernoulli framework terms, the codec is the lever that controls the
non-member ``Bernoulli<Y>`` distribution. The storage distribution is a
*build-set* property; the codec controls the *non-member* property.
See ``~/github/repos/maph/docs/CODESPACE_NONMEMBERS.md`` for the C++
prior art and the contrastive empirical test.

Mirrors maph's ``include/maph/codecs/prefix_codec.hpp`` (Python port; not
a binding).
"""

from __future__ import annotations

import math
from collections.abc import Hashable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Generic, TypeVar

V = TypeVar("V", bound=Hashable)


def shannon_entropy(freqs: Mapping[V, float]) -> float:
    """Shannon entropy ``H(Y) = -sum p_v log2 p_v`` of a frequency map.

    Frequencies that do not already sum to 1 are normalized; zero-mass
    values contribute zero (by the convention ``0 log 0 = 0``). The result
    is in bits.

    Parameters
    ----------
    freqs : Mapping[V, float]
        Non-negative weight per value; need not be normalized.

    Returns
    -------
    float
        Entropy in bits, ``>= 0``.
    """
    total = 0.0
    for w in freqs.values():
        if w < 0:
            raise ValueError(f"shannon_entropy: negative weight {w!r}")
        total += w
    if total <= 0.0:
        raise ValueError("shannon_entropy: total weight must be positive")
    h = 0.0
    for w in freqs.values():
        if w <= 0.0:
            continue
        p = w / total
        h -= p * math.log2(p)
    return h


@dataclass(frozen=True, slots=True)
class DenseCodec(Generic[V]):
    """Every value gets a unique M-bit pattern; codespace fractions uniform.

    Parameters
    ----------
    values : Sequence[V]
        The vocabulary; ``len(values) <= 2 ** m_bits`` is required. Each
        value gets a distinct M-bit code, assigned in iteration order.
    m_bits : int
        Codeword width in bits. ``1 <= m_bits <= 32``.

    Notes
    -----
    Surplus patterns (``2^M - len(values)`` of them) decode to the *first*
    indexed value, which is harmless for round-trip and matches the
    ``decode(encode(v)) == v`` contract on the indexed alphabet but means
    the first value's codespace fraction is greater than ``1/2^M`` in the
    presence of surplus. To make the codespace fraction reporting honest,
    the implementation reports per-pattern share (``1/2^M``) for each
    indexed value but folds surplus mass into the first value (or into a
    user-supplied default; see :meth:`with_default`).

    The most common useful case is ``len(values) == 2 ** m_bits`` (no
    surplus), in which case the codec is a true bijection.
    """

    _values: tuple[V, ...]
    m_bits: int
    _index: dict[V, int] = field(repr=False, compare=False)

    def __init__(self, values: Sequence[V], m_bits: int) -> None:
        if not 1 <= m_bits <= 32:
            raise ValueError(f"m_bits must be in [1, 32], got {m_bits!r}")
        if len(values) == 0:
            raise ValueError("DenseCodec: at least one value required")
        if len(values) > (1 << m_bits):
            raise ValueError(
                f"DenseCodec: too many values ({len(values)}) for "
                f"m_bits={m_bits} (capacity {1 << m_bits})"
            )
        # Deduplicate while preserving order; reject duplicates.
        seen: set[V] = set()
        for v in values:
            if v in seen:
                raise ValueError(f"DenseCodec: duplicate value {v!r}")
            seen.add(v)
        object.__setattr__(self, "_values", tuple(values))
        object.__setattr__(self, "m_bits", int(m_bits))
        object.__setattr__(self, "_index", {v: i for i, v in enumerate(self._values)})

    @property
    def values(self) -> tuple[V, ...]:
        """The vocabulary, in code-assignment order."""
        return self._values

    @property
    def codespace_size(self) -> int:
        """``2 ** m_bits``: total number of M-bit patterns."""
        return 1 << self.m_bits

    def encode(self, value: V) -> int:
        """Return the M-bit pattern for ``value``.

        Raises
        ------
        KeyError
            If ``value`` is not in the codec's vocabulary.
        """
        if value not in self._index:
            raise KeyError(f"DenseCodec: value {value!r} not in vocabulary")
        return self._index[value]

    def decode(self, pattern: int) -> V:
        """Return the value associated with the M-bit ``pattern``.

        Patterns greater than or equal to ``len(values)`` decode to the
        first indexed value (surplus folding).
        """
        if not 0 <= pattern < self.codespace_size:
            raise ValueError(
                f"DenseCodec: pattern {pattern!r} not in [0, {self.codespace_size})"
            )
        if pattern < len(self._values):
            return self._values[pattern]
        return self._values[0]

    def codespace_fraction(self, value: V) -> float:
        """Fraction of the codespace assigned to ``value``.

        For non-surplus indexed values, this is ``1 / 2^M``. The first
        indexed value also collects the surplus when ``len(values) <
        2 ** m_bits``.
        """
        if value not in self._index:
            return 0.0
        per_pattern = 1.0 / self.codespace_size
        if value == self._values[0]:
            surplus = self.codespace_size - len(self._values)
            return per_pattern * (1 + surplus)
        return per_pattern

    def bits_per_value(self) -> float:
        """Codeword width in bits (constant ``m_bits`` for dense codecs)."""
        return float(self.m_bits)

    def expected_codeword_length(self, freqs: Mapping[V, float]) -> float:
        """Expected codeword length under ``freqs``: trivially ``m_bits``."""
        # Validate that values are in vocabulary.
        for v in freqs:
            if v not in self._index:
                raise KeyError(f"DenseCodec: value {v!r} not in vocabulary")
        return float(self.m_bits)

    def non_member_distribution(self) -> dict[V, float]:
        """Predicted ``P(decode(uniform M-bit pattern) == v)`` per value."""
        return {v: self.codespace_fraction(v) for v in self._values}


@dataclass(frozen=True, slots=True)
class PaddedCodec(Generic[V]):
    """One designated default value absorbs the surplus codespace.

    Parameters
    ----------
    values : Sequence[V]
        Full vocabulary including the default. Each non-default value gets
        exactly one M-bit pattern; the default gets the rest.
    default_value : V
        Member of ``values`` that absorbs the surplus codespace.
    m_bits : int
        Codeword width.

    Notes
    -----
    Codespace shares::

        codespace_fraction(default)     = (2^M - (|V| - 1)) / 2^M
        codespace_fraction(non-default) = 1 / 2^M

    Useful when one outcome dominates (sparse retrieval, "missing" sentinel).
    """

    _values: tuple[V, ...]
    default_value: V
    m_bits: int
    _index: dict[V, int] = field(repr=False, compare=False)

    def __init__(
        self, values: Sequence[V], default_value: V, m_bits: int
    ) -> None:
        if not 1 <= m_bits <= 32:
            raise ValueError(f"m_bits must be in [1, 32], got {m_bits!r}")
        if len(values) == 0:
            raise ValueError("PaddedCodec: at least one value required")
        if len(values) > (1 << m_bits):
            raise ValueError(
                f"PaddedCodec: too many values ({len(values)}) for "
                f"m_bits={m_bits} (capacity {1 << m_bits})"
            )
        if default_value not in values:
            raise ValueError(
                f"PaddedCodec: default_value {default_value!r} not in values"
            )
        seen: set[V] = set()
        for v in values:
            if v in seen:
                raise ValueError(f"PaddedCodec: duplicate value {v!r}")
            seen.add(v)

        # Default occupies index 0; remaining values follow in input order.
        ordered: list[V] = [default_value]
        for v in values:
            if v != default_value:
                ordered.append(v)

        object.__setattr__(self, "_values", tuple(ordered))
        object.__setattr__(self, "default_value", default_value)
        object.__setattr__(self, "m_bits", int(m_bits))
        object.__setattr__(self, "_index", {v: i for i, v in enumerate(ordered)})

    @property
    def values(self) -> tuple[V, ...]:
        """The vocabulary, default first."""
        return self._values

    @property
    def codespace_size(self) -> int:
        return 1 << self.m_bits

    def encode(self, value: V) -> int:
        if value not in self._index:
            raise KeyError(f"PaddedCodec: value {value!r} not in vocabulary")
        return self._index[value]

    def decode(self, pattern: int) -> V:
        if not 0 <= pattern < self.codespace_size:
            raise ValueError(
                f"PaddedCodec: pattern {pattern!r} not in [0, {self.codespace_size})"
            )
        if pattern < len(self._values):
            return self._values[pattern]
        return self.default_value

    def codespace_fraction(self, value: V) -> float:
        if value not in self._index:
            return 0.0
        per_pattern = 1.0 / self.codespace_size
        if value == self.default_value:
            surplus = self.codespace_size - len(self._values)
            return per_pattern * (1 + surplus)
        return per_pattern

    def bits_per_value(self) -> float:
        return float(self.m_bits)

    def expected_codeword_length(self, freqs: Mapping[V, float]) -> float:
        for v in freqs:
            if v not in self._index:
                raise KeyError(f"PaddedCodec: value {v!r} not in vocabulary")
        return float(self.m_bits)

    def non_member_distribution(self) -> dict[V, float]:
        return {v: self.codespace_fraction(v) for v in self._values}


@dataclass(frozen=True, slots=True)
class PrefixCodec(Generic[V]):
    """Prefix-free (Huffman-style) codec packed into M-bit slots.

    Each value ``v`` is assigned a codeword of length ``l_v <= M``; the
    codeword is left-aligned in the M-bit slot, and the trailing
    ``M - l_v`` bits form a free suffix. The set of M-bit patterns that
    begin with a given codeword is the value's *class*, of size
    ``2^(M - l_v)``.

    Codespace fraction::

        codespace_fraction(v) = 2^(-l_v)

    Decoding scans codewords longest-first and returns the value whose
    codeword is a prefix of the given pattern. If the supplied codeword
    lengths satisfy Kraft's inequality strictly (``sum 2^(-l_v) < 1``),
    the surplus patterns are folded onto a designated default value.

    Parameters
    ----------
    codes : Sequence[tuple[V, int]]
        ``(value, codeword_length)`` pairs. Lengths must satisfy Kraft's
        inequality and lie in ``[1, M]``.
    default_value : V
        Receives leftover codespace when Kraft's sum is strictly below 1.
        Must be a member of the codec's value set.
    m_bits : int
        Slot width.
    """

    _codewords: tuple[tuple[V, int, int], ...]
    """Sorted by descending length: ``(value, prefix_left_aligned, length)``."""

    _index: dict[V, tuple[int, int]] = field(repr=False, compare=False)
    """``value -> (prefix_left_aligned, length)``."""

    default_value: V
    m_bits: int
    _surplus_count: int = field(repr=False, compare=False)

    def __init__(
        self,
        codes: Sequence[tuple[V, int]],
        default_value: V,
        m_bits: int,
    ) -> None:
        if not 1 <= m_bits <= 32:
            raise ValueError(f"m_bits must be in [1, 32], got {m_bits!r}")
        if len(codes) == 0:
            raise ValueError("PrefixCodec: at least one code required")

        # Validate lengths and Kraft inequality.
        seen_values: set[V] = set()
        kraft = 0.0
        for v, length in codes:
            if v in seen_values:
                raise ValueError(f"PrefixCodec: duplicate value {v!r}")
            seen_values.add(v)
            if not 1 <= length <= m_bits:
                raise ValueError(
                    f"PrefixCodec: code length {length} for {v!r} not in [1, {m_bits}]"
                )
            kraft += math.ldexp(1.0, -length)
        if kraft > 1.0 + 1e-9:
            raise ValueError(
                f"PrefixCodec: Kraft inequality violated (sum 2^(-l_v) = {kraft})"
            )
        if default_value not in seen_values:
            raise ValueError(
                f"PrefixCodec: default_value {default_value!r} not among codes"
            )

        # Canonical codeword assignment: sort by (length, value-stable-key)
        # and walk forward with the canonical-Huffman algorithm.
        sortable = sorted(
            codes,
            key=lambda p: (p[1], _stable_key(p[0])),
        )
        entries: list[tuple[V, int, int]] = []
        next_code = 0
        last_length = 0
        for v, length in sortable:
            if last_length != 0 and length > last_length:
                next_code <<= length - last_length
            code = next_code
            aligned = code << (m_bits - length)
            entries.append((v, aligned, length))
            next_code = code + 1
            last_length = length

        # Surplus tracking.
        if last_length < m_bits:
            next_code <<= m_bits - last_length
        codespace_size = 1 << m_bits
        surplus_count = (
            codespace_size - next_code if next_code <= codespace_size else 0
        )

        # Sort entries descending by length (longest codewords first) for
        # decode scan: a longer codeword's prefix is a strict superset of
        # any shorter codeword's prefix when they share the same first bits.
        entries_by_length = sorted(entries, key=lambda e: -e[2])

        index: dict[V, tuple[int, int]] = {
            v: (aligned, length) for (v, aligned, length) in entries
        }

        object.__setattr__(self, "_codewords", tuple(entries_by_length))
        object.__setattr__(self, "_index", index)
        object.__setattr__(self, "default_value", default_value)
        object.__setattr__(self, "m_bits", int(m_bits))
        object.__setattr__(self, "_surplus_count", int(surplus_count))

    @classmethod
    def from_frequencies(
        cls,
        freqs: Mapping[V, float],
        m_bits: int,
        default_value: V | None = None,
    ) -> PrefixCodec[V]:
        """Build a Huffman code from ``freqs``, packed into M-bit slots.

        Parameters
        ----------
        freqs : Mapping[V, float]
            Non-negative weights per value. Zero-weight values are dropped.
        m_bits : int
            Slot width. Codeword lengths are clipped to ``m_bits`` (which
            may violate Kraft for very skewed inputs at small M; the
            constructor will raise if so).
        default_value : V, optional
            Surplus collector. Defaults to the highest-frequency value.

        Returns
        -------
        PrefixCodec[V]
        """
        nonzero = [(v, w) for v, w in freqs.items() if w > 0]
        if not nonzero:
            raise ValueError("from_frequencies: no positive-weight values")
        if default_value is None:
            default_value = max(nonzero, key=lambda p: p[1])[0]

        if len(nonzero) == 1:
            (only,) = [v for v, _ in nonzero]
            return cls(codes=[(only, 1)], default_value=only, m_bits=m_bits)

        lengths = _huffman_lengths(nonzero, m_bits)
        return cls(codes=lengths, default_value=default_value, m_bits=m_bits)

    @property
    def values(self) -> tuple[V, ...]:
        """The vocabulary, in decode-scan order (longest codewords first)."""
        return tuple(v for (v, _, _) in self._codewords)

    @property
    def codespace_size(self) -> int:
        return 1 << self.m_bits

    def encode(self, value: V) -> int:
        """Return the canonical M-bit pattern for ``value``.

        The canonical pattern is the codeword left-aligned in the M-bit
        slot with the suffix bits zero. To get a uniformly random pattern
        within the value's class, use :meth:`encode_random`.
        """
        if value not in self._index:
            raise KeyError(f"PrefixCodec: value {value!r} not in vocabulary")
        aligned, _length = self._index[value]
        return aligned

    def encode_random(
        self,
        value: V,
        rng_uniform: int | None = None,
    ) -> int:
        """Return a pattern uniformly drawn from ``value``'s class.

        ``rng_uniform`` is an integer in ``[0, 2^(M - l_v))`` chosen by the
        caller (so the function is deterministic / pure). If ``None``,
        returns the canonical (suffix-zero) encoding.
        """
        if value not in self._index:
            raise KeyError(f"PrefixCodec: value {value!r} not in vocabulary")
        aligned, length = self._index[value]
        if rng_uniform is None:
            return aligned
        suffix_bits = self.m_bits - length
        if not 0 <= rng_uniform < (1 << suffix_bits):
            raise ValueError(
                f"PrefixCodec.encode_random: rng_uniform out of range [0, "
                f"{1 << suffix_bits})"
            )
        return aligned | rng_uniform

    def decode(self, pattern: int) -> V:
        """Return the value whose codeword is a prefix of ``pattern``.

        Falls back to ``default_value`` for surplus patterns.
        """
        if not 0 <= pattern < self.codespace_size:
            raise ValueError(
                f"PrefixCodec: pattern {pattern!r} not in [0, {self.codespace_size})"
            )
        for v, aligned, length in self._codewords:
            mask = _mask_for_length(length, self.m_bits)
            if (pattern & mask) == (aligned & mask):
                return v
        return self.default_value

    def codespace_fraction(self, value: V) -> float:
        """``|class(v)| / 2^M = 2^(-l_v)``; default also collects surplus."""
        if value not in self._index:
            if value == self.default_value:
                return self._surplus_share()
            return 0.0
        _aligned, length = self._index[value]
        share = math.ldexp(1.0, -length)
        if value == self.default_value:
            share += self._surplus_share()
        return share

    def codeword_length(self, value: V) -> int:
        """Codeword length ``l_v`` in bits."""
        if value not in self._index:
            raise KeyError(f"PrefixCodec: value {value!r} not in vocabulary")
        return self._index[value][1]

    def bits_per_value(self) -> float:
        """Slot width: ``m_bits``. The *information* per value is the
        expected codeword length, exposed as :meth:`expected_codeword_length`.
        """
        return float(self.m_bits)

    def expected_codeword_length(self, freqs: Mapping[V, float]) -> float:
        """Expected codeword length ``L = sum p_v * l_v`` under ``freqs``.

        Frequencies are normalized internally. Values absent from the codec
        are treated as decoded to the default and contribute its codeword
        length (the user has presumably verified vocabulary coverage).
        """
        total = 0.0
        for w in freqs.values():
            if w < 0:
                raise ValueError(f"expected_codeword_length: negative weight {w!r}")
            total += w
        if total <= 0.0:
            raise ValueError("expected_codeword_length: total weight must be positive")

        out = 0.0
        for v, w in freqs.items():
            if w <= 0.0:
                continue
            p = w / total
            if v in self._index:
                _, length = self._index[v]
            else:
                # Treat as decoded to default.
                _, length = self._index[self.default_value]
            out += p * length
        return out

    def kraft_sum(self) -> float:
        """``sum 2^(-l_v)`` over the indexed vocabulary."""
        return sum(math.ldexp(1.0, -length) for (_v, _a, length) in self._codewords)

    def non_member_distribution(self) -> dict[V, float]:
        """Predicted ``P(decode(uniform M-bit pattern) == v)`` per value."""
        out: dict[V, float] = {v: self.codespace_fraction(v) for v, _, _ in self._codewords}
        # Default may also need an entry if it lives outside the codeword set
        # (it doesn't here, since the constructor requires default in codes;
        # the surplus is folded into its existing entry).
        return out

    def _surplus_share(self) -> float:
        return self._surplus_count / float(self.codespace_size)


# =====================================================================
# Internal helpers
# =====================================================================


def _stable_key(v: V) -> tuple[int, str]:
    """Sort key that works across heterogeneous hashable types."""
    return (0 if isinstance(v, int) else 1, str(v))


def _mask_for_length(length: int, m_bits: int) -> int:
    """Bitmask selecting the top ``length`` bits of an ``m_bits``-bit pattern."""
    if length >= m_bits:
        return (1 << m_bits) - 1
    return (((1 << m_bits) - 1) >> (m_bits - length)) << (m_bits - length)


def _huffman_lengths(
    nonzero_freqs: Sequence[tuple[V, float]],
    max_len: int,
) -> list[tuple[V, int]]:
    """Compute length-limited Huffman codeword lengths from positive frequencies.

    Uses the Larmore-Hirschberg "package-merge" algorithm to enforce
    ``length <= max_len`` for every value while minimizing the expected
    codeword length under the input frequencies. The result always
    satisfies Kraft's inequality (``sum 2^(-l_v) <= 1``) provided
    ``2^max_len >= len(nonzero_freqs)``.

    For ``max_len`` large enough that the unconstrained Huffman algorithm
    naturally produces depths ``<= max_len``, this returns the same
    lengths as the unconstrained Huffman.

    References
    ----------
    Larmore and Hirschberg, "A fast algorithm for optimal length-limited
    Huffman codes," J. ACM 37(3), 1990.
    """
    n = len(nonzero_freqs)
    if n == 0:
        return []
    if n == 1:
        # Single value: depth 1 (Huffman convention for a unary alphabet).
        v, _ = nonzero_freqs[0]
        return [(v, 1)]
    if (1 << max_len) < n:
        raise ValueError(
            f"_huffman_lengths: cannot encode {n} values in max_len={max_len} bits "
            f"(need at least ceil(log2({n})) = {(n - 1).bit_length()} bits)"
        )

    # Package-merge.
    #
    # Each "coin" is a multiset of value indices (here represented as a
    # frozenset of indices it covers). We start with `max_len` rows; row r
    # has one coin per value, denomination 2^-(r+1), value = freq[v].
    #
    # Process rows from smallest denomination (largest r) toward the
    # smallest. Merge pairs of cheapest coins in row r into "packages"
    # in row r-1. Coins in row r-1 then comprise (a) packages from row
    # r and (b) the original row r-1 coins.
    #
    # After processing, select the cheapest 2n-2 coins from the top row
    # (denomination 2^-1). The number of times value v appears among the
    # selected coins (across all original rows it contributed to) equals
    # its codeword length l_v.

    weights: list[float] = [float(w) for _, w in nonzero_freqs]

    # Each coin: (cost, members_indices_as_tuple).
    # Start with the lowest-denomination row.
    def make_initial_row() -> list[tuple[float, tuple[int, ...]]]:
        return [(weights[i], (i,)) for i in range(n)]

    # Top row (denomination 2^-1) initially has just the original coins.
    # We process from depth `max_len` down to depth 1; at each step,
    # pair adjacent items in the sorted list and merge them as packages
    # for the next-shallower depth.
    current_row = sorted(make_initial_row(), key=lambda c: c[0])
    for _depth in range(max_len, 1, -1):
        # Pair up the current row into packages for the next-shallower row.
        packages: list[tuple[float, tuple[int, ...]]] = []
        i = 0
        while i + 1 < len(current_row):
            cost = current_row[i][0] + current_row[i + 1][0]
            members = current_row[i][1] + current_row[i + 1][1]
            packages.append((cost, members))
            i += 2
        # Drop any unpaired tail coin (cannot contribute to a package).
        # Combine packages with the next-shallower original row, then sort.
        next_row = packages + make_initial_row()
        next_row.sort(key=lambda c: c[0])
        current_row = next_row

    # Select the cheapest 2n-2 coins from the top row.
    selected = current_row[: 2 * n - 2]

    # Count appearances of each value index across selected coins.
    counts = [0] * n
    for _cost, members in selected:
        for idx in members:
            counts[idx] += 1

    # Codeword length = appearance count; clip to [1, max_len] for safety.
    out: list[tuple[V, int]] = []
    for i, (v, _w) in enumerate(nonzero_freqs):
        length = max(1, min(counts[i], max_len))
        out.append((v, length))
    return out


__all__ = [
    "DenseCodec",
    "PaddedCodec",
    "PrefixCodec",
    "shannon_entropy",
]
