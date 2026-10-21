"""bernoulli: a two-rate error model for approximate data structures.

Every structure in this package reports how it can be wrong as a pair of
rates, the false-positive rate ``fpr`` and the false-negative rate ``fnr``,
and the package propagates those rates through composition. It is the
reference implementation of the Bernoulli model developed in the monograph
*Bernoulli Types* (https://metafunctor.com/latex/bernoulli-monograph/book.html).

What is implemented (pure Python, no runtime dependencies):

- **Phase 1, the atom.** :class:`BernoulliBool` (a noisy bit with ``~``, ``&``
  and ``|``), :mod:`bernoulli.algebra` (the composition theorem, k-fold chains,
  Bloom sizing) and :mod:`bernoulli.measures` (PPV, NPV, Youden's J, F1, MCC).
  :mod:`bernoulli.formula` gives exact error rates through whole Boolean
  formulas, where a single rate pair does not compose.
- **Phase 2, sets.** :class:`MembershipOracle`, :class:`BloomFilter`, rate
  propagation for union, intersection, complement and difference
  (:class:`SetRates`, :class:`Partition`, :mod:`bernoulli.sets.composition`)
  and the space bounds of :mod:`bernoulli.sets.entropy_bound`.
- **Phase 3, maps.** :class:`MinimalPerfectHash` (BBHash),
  :class:`PerfectFilter` (perfect hash plus fingerprints), the codecs
  :class:`DenseCodec`, :class:`PaddedCodec` and :class:`PrefixCodec`, and the
  retrieval structures :class:`GF2Retrieval` and :class:`EncodedRetrieval`.
- **Phase 4, relations.** :class:`BernoulliRelation`: exact tuples that carry
  membership rates through select, project and join.
- **Phase 5, sketches.** :class:`CountMinSketch`, :class:`HyperLogLog` and
  :class:`MinHash`; Miller-Rabin lives in :mod:`bernoulli.algorithms`.

Not implemented: the planned C acceleration (``c/`` holds only a design note),
serialization, and any cryptographic hashing. The hashes are FNV-1a and
splitmix64, which support no security claim. See ``PHASING.md`` for the
roadmap.

Research utilities stay in their submodules and are not re-exported here:
:mod:`bernoulli.harness` (rate measurement with confidence intervals),
:mod:`bernoulli.bench` (timing), :mod:`bernoulli.sets.cascade` and
:mod:`bernoulli.sets.correlated_bloom`.
"""

from bernoulli import algebra, formula, measures
from bernoulli._version import __version__
from bernoulli.atom import BernoulliBool
from bernoulli.maps import (
    ApproximateMap,
    DenseCodec,
    EncodedRetrieval,
    GF2Retrieval,
    MinimalPerfectHash,
    PaddedCodec,
    PerfectFilter,
    PerfectHashFunction,
    PrefixCodec,
)
from bernoulli.relations import BernoulliRelation
from bernoulli.sets import BloomFilter, MembershipOracle, Partition, SetRates
from bernoulli.sketches import CountMinSketch, HyperLogLog, MinHash

__all__ = [
    "__version__",
    # Phase 1: the atom
    "BernoulliBool",
    "algebra",
    "formula",
    "measures",
    # Phase 2: sets
    "BloomFilter",
    "MembershipOracle",
    "Partition",
    "SetRates",
    # Phase 3: maps
    "ApproximateMap",
    "DenseCodec",
    "EncodedRetrieval",
    "GF2Retrieval",
    "MinimalPerfectHash",
    "PaddedCodec",
    "PerfectFilter",
    "PerfectHashFunction",
    "PrefixCodec",
    # Phase 4: relations
    "BernoulliRelation",
    # Phase 5: sketches
    "CountMinSketch",
    "HyperLogLog",
    "MinHash",
]
