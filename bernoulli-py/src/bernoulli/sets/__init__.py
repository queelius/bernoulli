"""Approximate sets in the Bernoulli framework.

A ``BernoulliSet[X]`` is a function ``X -> Bernoulli<bool>`` that answers
"is ``x`` a member?" with bounded error rates ``(fpr, fnr)``.

Phase 2 components:

- :class:`MembershipOracle`: protocol for any approximate-set implementation.
  Mirrors maph's ``concepts/membership_oracle.hpp``.
- :class:`BloomFilter`: the canonical k-hash Bloom filter (pure Python; a C
  accelerator lands with the cffi core).
- :class:`SetRates`, :class:`Partition`, and :mod:`bernoulli.sets.composition`:
  union, intersection, complement, and difference rate propagation (book
  chapter 6), including the three-region intersection FPR and its sparse limit.
- :mod:`bernoulli.sets.entropy_bound`: the ``-log2(fpr)`` floor, the Bloom
  ``1.44x`` overhead, and the BHF model (book chapters 8 and 14).
- ``SpaceOptimalBloomFilter`` (forthcoming): the explicit BHF construction
  reaching the entropy floor.

Many natural objects are Bernoulli sets with structurally zero FNR:

- The set of primes, queried via a single round of Miller-Rabin: ``fnr = 0``,
  ``fpr <= 1/4``.
- The membership predicate of a Bloom filter: ``fnr = 0``, ``fpr`` controlled
  by sizing.
- A perfect filter's positive predicate: ``fnr = 0``, ``fpr = 2^-fp_bits``.

These are :func:`bernoulli.atom.BernoulliBool.one_sided_fpr` instances; AND
chains of them stay one-sided and drive FPR multiplicatively to zero.
"""

from bernoulli.sets import composition, entropy_bound
from bernoulli.sets.bloom import BloomFilter
from bernoulli.sets.composition import Partition, SetRates
from bernoulli.sets.protocol import MembershipOracle

__all__ = [
    "BloomFilter",
    "MembershipOracle",
    "Partition",
    "SetRates",
    "composition",
    "entropy_bound",
]
