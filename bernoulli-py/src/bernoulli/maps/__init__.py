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

Phase 3 deliverables (scaffolded here):

- :class:`PerfectHashFunction`: protocol mirroring maph's
  ``concepts/perfect_hash_function.hpp``.
- :class:`ApproximateMap`: protocol mirroring maph's
  ``concepts/approximate_map.hpp``.
- ``PrefixCodec``: Huffman-style codec (port from maph's
  ``codecs/prefix_codec.hpp``).
- ``RibbonRetrieval``: GF(2) ribbon retrieval (port from maph's
  ``retrieval/ribbon_retrieval.hpp``).
- ``EncodedRetrieval``: codec-controlled retrieval composition.
- ``PerfectFilter``: PHF + fingerprint, the canonical approximate map.
"""

from bernoulli.maps.protocol import ApproximateMap, PerfectHashFunction

__all__ = ["ApproximateMap", "PerfectHashFunction"]
