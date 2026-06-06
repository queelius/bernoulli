"""Approximate relations in the Bernoulli framework (book chapter 12).

A :class:`BernoulliRelation` is a relation (a set of tuples over a named schema)
viewed as a Bernoulli set of tuples. Its relational algebra is the chapter 6 set
algebra lifted to tuples: ``select`` is a noiseless restriction, ``join`` is the
intersection composition over the combined membership, and ``project`` is the
union composition over each fiber. See :mod:`bernoulli.relations.relation`.
"""

from bernoulli.relations.relation import BernoulliRelation

__all__ = ["BernoulliRelation"]
