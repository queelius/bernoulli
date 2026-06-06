"""Approximate sets in the Bernoulli framework.

A ``BernoulliSet[X]`` is a function ``X -> Bernoulli<bool>`` that answers
"is ``x`` a member?" with bounded error rates ``(fpr, fnr)``.

Phase 2 deliverables (scaffolded here):

- :class:`MembershipOracle`: protocol for any approximate-set implementation.
  Mirrors maph's ``concepts/membership_oracle.hpp``.
- :class:`BernoulliSet`: combines a membership oracle with a Bernoulli rate
  pair, lifting an X -> bool function into X -> Bernoulli<bool>.
- ``BloomFilter`` (forthcoming): the canonical k-hash Bloom filter, with an
  optional C accelerator.
- ``SpaceOptimalBloomFilter`` (forthcoming): the BHF construction reaching
  the entropy bound.

Many natural objects are Bernoulli sets with structurally zero FNR:

- The set of primes, queried via a single round of Miller-Rabin: ``fnr = 0``,
  ``fpr <= 1/4``.
- The membership predicate of a Bloom filter: ``fnr = 0``, ``fpr`` controlled
  by sizing.
- A perfect filter's positive predicate: ``fnr = 0``, ``fpr = 2^-fp_bits``.

These are :func:`bernoulli.atom.BernoulliBool.one_sided_fpr` instances; AND
chains of them stay one-sided and drive FPR multiplicatively to zero.
"""

from bernoulli.sets.bloom import BloomFilter
from bernoulli.sets.protocol import MembershipOracle

__all__ = ["BloomFilter", "MembershipOracle"]
