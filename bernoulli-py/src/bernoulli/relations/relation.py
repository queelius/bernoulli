"""Approximate relations: a Bernoulli set of tuples with a relational algebra.

A :class:`BernoulliRelation` is a relation (a set of tuples over a named schema)
viewed as a Bernoulli set over the tuple space: membership of a tuple is answered
with a false-positive rate and a false-negative rate. The relational operators
are the Bernoulli set algebra of book chapter 6 lifted to tuples:

- **select** (sigma): a noiseless restriction by an exact predicate; the
  per-tuple membership rates are unchanged.
- **join** (the natural join): a tuple of the combined schema is a member iff its
  left part is in one relation *and* its right part is in the other, the
  conjunction of two independent lifted memberships. Rates propagate by the ch6
  *intersection* composition (so the bare product ``fpr_R * fpr_S`` is only the
  ``Partition.sparse()`` limit; a tuple whose left part is a genuine member
  false-positives at ``fpr_S`` alone).
- **project** (pi): a projected tuple is a member iff *any* tuple in its fiber is
  a member, a disjunction over the fiber. Folding several source tuples onto one
  projected tuple drives the false-negative rate down multiplicatively
  (``fnr ** fiber_size``); the false-positive amplification is domain-dependent
  and left as the chapter's open question (join/projection error under correlated
  approximations).

Tuples are tracked exactly, so the operators produce the correct result relation;
the rate fields propagate the membership approximation alongside.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass

from bernoulli.sets.composition import Partition, SetRates, intersection

Row = dict[str, object]
Tuple = tuple[object, ...]


@dataclass(frozen=True, slots=True)
class BernoulliRelation:
    """A relation over a named schema, as a Bernoulli set of tuples.

    Parameters
    ----------
    schema : Iterable[str]
        Attribute names, in tuple-position order. Must be distinct.
    tuples : Iterable[tuple]
        The rows; each must have one value per schema attribute.
    rates : SetRates, optional
        The membership ``(fpr, fnr)`` of the relation. Defaults to exact.

    Examples
    --------
    >>> r = BernoulliRelation(("id", "city"), [(1, "NYC"), (2, "LA")],
    ...                       SetRates(fpr=0.01, fnr=0.0))
    >>> r.arity, len(r)
    (2, 2)
    >>> r.contains((1, "NYC"))
    True
    """

    schema: tuple[str, ...]
    tuples: frozenset[Tuple]
    rates: SetRates

    def __init__(
        self,
        schema: Iterable[str],
        tuples: Iterable[Tuple],
        rates: SetRates | None = None,
    ) -> None:
        schema_t = tuple(schema)
        if len(set(schema_t)) != len(schema_t):
            raise ValueError(f"schema attributes must be distinct, got {schema_t!r}")
        rows = frozenset(tuples)
        for t in rows:
            if len(t) != len(schema_t):
                raise ValueError(
                    f"tuple {t!r} has arity {len(t)}, expected {len(schema_t)}"
                )
        object.__setattr__(self, "schema", schema_t)
        object.__setattr__(self, "tuples", rows)
        object.__setattr__(self, "rates", rates if rates is not None else SetRates())

    @property
    def arity(self) -> int:
        return len(self.schema)

    def __len__(self) -> int:
        return len(self.tuples)

    def __iter__(self) -> Iterator[Tuple]:
        return iter(self.tuples)

    def contains(self, row: Tuple) -> bool:
        """Exact membership of a tuple in the relation's content."""
        return tuple(row) in self.tuples

    def _row_dict(self, t: Tuple) -> Row:
        return dict(zip(self.schema, t, strict=True))

    def select(self, predicate: Callable[[Row], bool]) -> BernoulliRelation:
        """sigma: keep tuples satisfying ``predicate`` (a noiseless restriction).

        The predicate receives each row as a ``{attribute: value}`` dict and is
        evaluated exactly, so the membership rates are unchanged.

        Examples
        --------
        >>> r = BernoulliRelation(("id", "age"), [(1, 30), (2, 17), (3, 41)],
        ...                       SetRates(fpr=0.02))
        >>> adults = r.select(lambda row: row["age"] >= 18)
        >>> sorted(t[0] for t in adults), adults.rates.rates
        ([1, 3], (0.02, 0.0))
        """
        kept = frozenset(t for t in self.tuples if predicate(self._row_dict(t)))
        return BernoulliRelation(self.schema, kept, self.rates)

    def project(self, attrs: Iterable[str]) -> BernoulliRelation:
        """pi: project onto ``attrs``; folding fibers drives FNR down.

        A projected tuple is missed only if every source tuple in its fiber is
        missed, so its FNR is ``fnr ** fiber_size``; the relation's reported FNR
        is the mean over projected tuples. The FPR amplification on projection is
        domain-dependent and is left at the input FPR (the chapter's open
        question), so this is a lower bound on the projected FPR.

        Examples
        --------
        >>> r = BernoulliRelation(("city", "id"),
        ...                       [("NYC", 1), ("NYC", 2), ("LA", 3)],
        ...                       SetRates(fpr=0.01, fnr=0.2))
        >>> cities = r.project(["city"])
        >>> sorted(t[0] for t in cities)
        ['LA', 'NYC']
        >>> round(cities.rates.fnr, 4)   # mean of 0.2**2 (NYC) and 0.2**1 (LA)
        0.12
        """
        attrs_t = tuple(attrs)
        missing = [a for a in attrs_t if a not in self.schema]
        if missing:
            raise ValueError(f"attributes {missing!r} not in schema {self.schema!r}")
        idx = [self.schema.index(a) for a in attrs_t]
        fibers: Counter[Tuple] = Counter()
        for t in self.tuples:
            fibers[tuple(t[i] for i in idx)] += 1

        w = self.rates.fnr
        fnr_proj = (
            sum(w**f for f in fibers.values()) / len(fibers) if fibers else 0.0
        )
        return BernoulliRelation(
            attrs_t, frozenset(fibers), SetRates(fpr=self.rates.fpr, fnr=fnr_proj)
        )

    def join(
        self, other: BernoulliRelation, *, partition: Partition | None = None
    ) -> BernoulliRelation:
        """Natural join on shared attributes; rates by ch6 intersection.

        A joined tuple is a member iff its left part is in ``self`` and its right
        part is in ``other``: the conjunction of two independent lifted
        memberships, whose rates are the chapter 6 intersection composition. The
        ``partition`` over the four membership cells defaults to
        ``Partition.sparse()`` (the bare-product limit ``fpr_R * fpr_S``).

        Examples
        --------
        >>> r = BernoulliRelation(("id", "city"), [(1, "NYC"), (2, "LA")],
        ...                       SetRates.one_sided_fpr(0.10))
        >>> s = BernoulliRelation(("id", "age"), [(1, 30), (2, 17), (3, 41)],
        ...                       SetRates.one_sided_fpr(0.20))
        >>> j = r.join(s)
        >>> sorted((t[0], t[1], t[2]) for t in j)
        [(1, 'NYC', 30), (2, 'LA', 17)]
        >>> round(j.rates.fpr, 4), j.rates.fnr      # sparse: 0.10 * 0.20
        (0.02, 0.0)
        """
        shared = [a for a in self.schema if a in other.schema]
        right_extra = [a for a in other.schema if a not in shared]
        result_schema = self.schema + tuple(right_extra)

        self_key = [self.schema.index(a) for a in shared]
        other_key = [other.schema.index(a) for a in shared]
        other_extra_idx = [other.schema.index(a) for a in right_extra]

        index: dict[Tuple, list[Tuple]] = defaultdict(list)
        for t2 in other.tuples:
            index[tuple(t2[i] for i in other_key)].append(t2)

        result: set[Tuple] = set()
        for t1 in self.tuples:
            key = tuple(t1[i] for i in self_key)
            for t2 in index.get(key, ()):
                result.add(t1 + tuple(t2[i] for i in other_extra_idx))

        part = partition if partition is not None else Partition.sparse()
        rates = intersection(self.rates, other.rates, part)
        return BernoulliRelation(result_schema, frozenset(result), rates)
