"""Approximate maps in the Bernoulli framework.

The general ``BernoulliMap[X, Y]`` is a function ``X -> Bernoulli<Y>``: it
maps an input ``x`` to a value of ``Y``, with the value being correct
on the build set and (with bounded error) controlled on non-members.

The architectural insight underlying Phase 3 is that a wide class of natural
randomized algorithms produce Bernoulli maps with structurally zero false-
negative rate and a controllable false-positive rate. Examples include:

- Single-round Miller-Rabin over the integers (X = N, Y = {prime, composite}).
- The membership predicate of a Bloom or perfect-hash filter
  (X = U, Y = {member, nonmember}).
- The cipher-map evaluation of a key into a published codebook
  (X = key universe, Y = published value type).

A general construction subsuming all of these is also straightforward: given
a function ``f: X -> Y`` and a build set ``S subset X`` of size ``n``,

1. Construct a perfect hash function ``phf: X -> {0, ..., n-1}`` over ``S``.
2. Allocate an indexable container ``store: array[n]`` with cells of width
   ``M`` bits, ideally ``M`` close to the Shannon entropy ``H(Y)`` of the
   value distribution.
3. For each ``x in S``, encode ``f(x)`` into ``store[phf(x)]`` using a codec
   (Huffman / arithmetic / dense, depending on the entropy structure).

The resulting object is a Bernoulli map ``f_tilde: X -> Y`` with:

- ``fnr = 0`` on the build set: ``f_tilde(x) == f(x)`` for all ``x in S``.
- For ``x not in S``: ``f_tilde(x)`` returns a value distributed by the codec's
  codespace allocation (the recent maph empirical finding;
  see ``~/github/repos/maph/docs/CODESPACE_NONMEMBERS.md``).

Optionally, a fingerprint layer can be added to give ``contains`` a controllable
false-positive rate, yielding the "perfect filter" composition.

Phase 3 components:

- :class:`PerfectHashFunction`, :class:`ApproximateMap`: protocols mirroring
  maph's ``concepts/perfect_hash_function.hpp`` and ``concepts/approximate_map.hpp``.
- :class:`MinimalPerfectHash`: a BBHash minimal perfect hash (slot assignment).
- :class:`PerfectFilter`: perfect hash plus per-slot fingerprint, the chapter 14
  Bernoulli hash function (``fnr = 0``, ``fpr = 2^-r``, ``mu + r`` bits per key).
- :class:`DenseCodec`, :class:`PaddedCodec`, :class:`PrefixCodec`,
  :func:`shannon_entropy`: value-to-bit-pattern codecs (Huffman-style and dense).
- :class:`GF2Retrieval`: a static ``keys -> r-bit values`` retrieval by GF(2)
  peeling (the pure-Python core that the ribbon band optimizes for cache).
- :class:`EncodedRetrieval`: retrieval composed with a codec, so the codec's
  codespace allocation controls the non-member value distribution.
"""

from bernoulli.maps.codec import (
    DenseCodec,
    PaddedCodec,
    PrefixCodec,
    shannon_entropy,
)
from bernoulli.maps.perfect_filter import PerfectFilter
from bernoulli.maps.perfect_hash import MinimalPerfectHash
from bernoulli.maps.protocol import ApproximateMap, PerfectHashFunction
from bernoulli.maps.retrieval import EncodedRetrieval, GF2Retrieval

__all__ = [
    "ApproximateMap",
    "DenseCodec",
    "EncodedRetrieval",
    "GF2Retrieval",
    "MinimalPerfectHash",
    "PaddedCodec",
    "PerfectFilter",
    "PerfectHashFunction",
    "PrefixCodec",
    "shannon_entropy",
]
