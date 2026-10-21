"""Research reference: frozen independent-source lineage, not a new inference method.

All probability methods except frechet_bounds ASSUME mutually independent distinct
source IDs. Reusing an ID reuses one frozen bit. Real-arithmetic bounds are sound;
this float implementation is checked to numerical tolerance, not interval-certified.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from itertools import product

Bounds = tuple[float, float]


def _probability(p: float) -> None:
    if not 0.0 <= p <= 1.0:
        raise ValueError("probabilities must be finite and in [0, 1]")


@dataclass(frozen=True)
class Channel:
    truth: bool
    fpr: float
    fnr: float

    def __post_init__(self) -> None:
        _probability(self.fpr)
        _probability(self.fnr)

    @property
    def acceptance(self) -> float:
        return 1.0 - self.fnr if self.truth else self.fpr


@dataclass(frozen=True)
class DNF:
    terms: frozenset[frozenset[int]]

    def __post_init__(self) -> None:
        unique = frozenset(frozenset(t) for t in self.terms)
        # Absorption only compares strictly smaller terms; equal-arity graph
        # lineages avoid quadratic comparisons. General absorption can be costly.
        buckets: dict[int, list[frozenset[int]]] = {}
        for term in unique:
            buckets.setdefault(len(term), []).append(term)
        retained: list[frozenset[int]] = []
        for size in sorted(buckets):
            smaller = tuple(retained)
            retained.extend(t for t in buckets[size] if not any(s < t for s in smaller))
        object.__setattr__(self, "terms", frozenset(retained))

    @classmethod
    def from_terms(cls, terms: Iterable[Iterable[int]]) -> DNF:
        return cls(frozenset(frozenset(t) for t in terms))

    @classmethod
    def atom(cls, source: int) -> DNF:
        return cls.from_terms([{source}])

    @property
    def support(self) -> frozenset[int]:
        return frozenset(i for term in self.terms for i in term)

    def evaluate(self, values: Mapping[int, bool]) -> bool:
        return any(all(values[i] for i in term) for term in self.terms)

    def __or__(self, other: DNF) -> DNF:
        return DNF.from_terms(self.terms | other.terms)

    def __and__(self, other: DNF) -> DNF:
        return DNF.from_terms(a | b for a in self.terms for b in other.terms)

    def quotient(self, aliases: Mapping[int, int]) -> DNF:
        return DNF.from_terms({aliases.get(i, i) for i in term} for term in self.terms)

    def condition(self, source: int, value: bool) -> DNF:
        return DNF.from_terms(t - {source} for t in self.terms if value or source not in t)


@dataclass
class Relation:
    """Explicit finite candidate tuples; missing rows denote exact absence.

    False positives outside these candidate rows are excluded by assumption.
    Attribute names describe a schema, not an encoded expression to be parsed.
    """

    attributes: tuple[str, ...]
    rows: dict[tuple[int, ...], DNF]

    def __post_init__(self) -> None:
        if len(set(self.attributes)) != len(self.attributes):
            raise ValueError("duplicate attributes")
        if any(len(row) != len(self.attributes) for row in self.rows):
            raise ValueError("tuple arity does not match schema")

    def select(self, predicate: Callable[[Mapping[str, int]], bool]) -> Relation:
        return Relation(
            self.attributes,
            {
                row: q
                for row, q in self.rows.items()
                if predicate(dict(zip(self.attributes, row, strict=True)))
            },
        )

    def project(self, attributes: tuple[str, ...]) -> Relation:
        if not set(attributes) <= set(self.attributes):
            raise ValueError("projection references unknown attributes")
        indexes = [self.attributes.index(a) for a in attributes]
        rows: dict[tuple[int, ...], DNF] = {}
        for row, q in self.rows.items():
            key = tuple(row[i] for i in indexes)
            rows[key] = rows.get(key, DNF.from_terms([])) | q
        return Relation(attributes, rows)

    def join(self, other: Relation) -> Relation:
        common = [
            (self.attributes.index(a), other.attributes.index(a))
            for a in self.attributes
            if a in other.attributes
        ]
        extra = [i for i, a in enumerate(other.attributes) if a not in self.attributes]
        attributes = self.attributes + tuple(other.attributes[i] for i in extra)
        rows: dict[tuple[int, ...], DNF] = {}
        for a, qa in self.rows.items():
            for b, qb in other.rows.items():
                if all(a[i] == b[j] for i, j in common):
                    key = a + tuple(b[i] for i in extra)
                    rows[key] = rows.get(key, DNF.from_terms([])) | (qa & qb)
        return Relation(attributes, rows)


def _validate(q: DNF, probabilities: Mapping[int, float]) -> None:
    for i in q.support:
        _probability(probabilities[i])


def exact_probability(q: DNF, probabilities: Mapping[int, float]) -> float:
    """Exhaustive weighted enumeration; exponential, deliberately an oracle."""
    _validate(q, probabilities)
    ids = sorted(q.support)

    def weights() -> Iterable[float]:
        for bits in product([False, True], repeat=len(ids)):
            if q.evaluate(dict(zip(ids, bits, strict=True))):
                yield math.prod(
                    probabilities[i] if bit else 1 - probabilities[i]
                    for i, bit in zip(ids, bits, strict=True)
                )

    return math.fsum(weights())


def frechet_bounds(q: DNF, probabilities: Mapping[int, float]) -> Bounds:
    """Sound even with arbitrary dependence; not necessarily globally sharp."""
    _validate(q, probabilities)
    lowers = [max(0.0, 1 - sum(1 - probabilities[i] for i in t)) for t in q.terms]
    uppers = [min((probabilities[i] for i in t), default=1.0) for t in q.terms]
    return max(lowers, default=0.0), min(1.0, sum(uppers))


def dissociation_bounds(q: DNF, probabilities: Mapping[int, float]) -> Bounds:
    """Gatterbauer--Suciu disjunctive dissociation, symmetric lower allocation.

    Each variable occurs once per conjunction. Independent occurrence copies
    get p for the upper bound and 1-(1-p)^(1/d) for the lower bound.
    """
    _validate(q, probabilities)
    occurrences = Counter(i for t in q.terms for i in t)
    lower_rates = {
        i: 1.0 if probabilities[i] == 1.0 else -math.expm1(math.log1p(-probabilities[i]) / d)
        for i, d in occurrences.items()
    }
    lo = 1 - math.prod(1 - math.prod(lower_rates[i] for i in t) for t in q.terms)
    hi = 1 - math.prod(1 - math.prod(probabilities[i] for i in t) for t in q.terms)
    return lo, hi


def packing_bounds(q: DNF, probabilities: Mapping[int, float]) -> Bounds:
    """Independent disjoint-witness packing lower; FKG/dissociation upper."""
    _validate(q, probabilities)
    weighted = [(math.prod(probabilities[i] for i in t), t) for t in q.terms]
    used: set[int] = set()
    no_witness = 1.0
    for weight, term in sorted(weighted, key=lambda pair: (-pair[0], tuple(sorted(pair[1])))):
        if used.isdisjoint(term):
            no_witness *= 1 - weight
            used.update(term)
    return 1 - no_witness, dissociation_bounds(q, probabilities)[1]


def condition_bounds(q: DNF, probabilities: Mapping[int, float], sources: Iterable[int]) -> Bounds:
    """Shannon conditioning with nested intersection ensures prefix refinement.

    Cost exponential in number of selected sources; no new inference algorithm.
    Bounds nest when extending a fixed source-order prefix, not on reordering.
    """
    _validate(q, probabilities)
    support = q.support
    selected = tuple(i for i in dict.fromkeys(sources) if i in support)

    def visit(query: DNF, index: int) -> Bounds:
        remaining_support = query.support
        while index < len(selected) and selected[index] not in remaining_support:
            index += 1
        raw = dissociation_bounds(query, probabilities)
        lo = max(raw[0], packing_bounds(query, probabilities)[0])
        hi = raw[1]
        if index == len(selected) or lo == hi:
            return lo, hi
        source = selected[index]
        p = probabilities[source]
        a = visit(query.condition(source, False), index + 1)
        b = visit(query.condition(source, True), index + 1)
        return max(lo, (1 - p) * a[0] + p * b[0]), min(hi, (1 - p) * a[1] + p * b[1])

    return visit(q, 0)


def _degree_two_components(q: DNF) -> list[tuple[list[int], bool]]:
    graph: dict[int, set[int]] = {}
    for t in q.terms:
        if len(t) == 2:
            a, b = t
            graph.setdefault(a, set()).add(b)
            graph.setdefault(b, set()).add(a)
        elif len(t) > 2:
            raise ValueError("requires at most binary witnesses")
    if any(len(neighbors) > 2 for neighbors in graph.values()):
        raise ValueError("requires source occurrence degree at most two")
    remaining = set(graph)
    components = []
    while remaining:
        root = remaining.pop()
        stack = [root]
        component = {root}
        while stack:
            for neighbor in graph[stack.pop()]:
                if neighbor not in component:
                    component.add(neighbor)
                    remaining.remove(neighbor)
                    stack.append(neighbor)
        endpoints = [i for i in component if len(graph[i]) == 1]
        start = min(endpoints or component)
        cycle = not endpoints
        order = [start]
        previous = None
        while True:
            next_ids = graph[order[-1]] - {previous, start}
            if not next_ids:
                break
            nxt = min(next_ids)
            previous = order[-1]
            order.append(nxt)
        components.append((order, cycle))
    return components


def degree_two_exact(q: DNF, probabilities: Mapping[int, float]) -> float:
    """Exact weighted independent-set DP for binary witnesses, max degree two.

    Linear arithmetic work on the normalized lineage. Standard path/cycle DP;
    input lineage construction and exact rational bit complexity are separate.
    """
    _validate(q, probabilities)
    if frozenset() in q.terms:
        return 1.0
    no_event = math.prod(1 - probabilities[next(iter(t))] for t in q.terms if len(t) == 1)
    for order, cycle in _degree_two_components(q):
        mass = 0.0
        for first in [False, True]:
            p = probabilities[order[0]]
            zero, one = (1 - p, 0.0) if not first else (0.0, p)
            for i in order[1:]:
                p = probabilities[i]
                zero, one = (zero + one) * (1 - p), zero * p
            mass += zero if cycle and first else zero + one
        no_event *= mass
    return 1 - no_event


@dataclass(frozen=True)
class OneSidedContract:
    """Separate sharp pure-FP and pure-FN maxima over unconstrained truth vectors.

    For two-sided noise the same numbers are upper bounds, generally not sharp.
    None means the exact conditioning class is empty (a constant query).
    """

    zero_sensitivity: int | None
    one_sensitivity: int | None
    fpr_max: float | None
    fnr_max: float | None


def degree_two_contract(q: DNF, fpr: float, fnr: float) -> OneSidedContract:
    """Truth-uniform contracts for normalized binary/degree-two lineages.

    Source truth may be any assignment consistent with aliases, with no extra
    integrity constraints. Each side is exact in its corresponding one-sided
    noise model. See theory.md section 8 for the maximal-boundary proof.
    """
    _probability(fpr)
    _probability(fnr)
    if not q.terms:
        return OneSidedContract(0, None, 0.0, None)
    if frozenset() in q.terms:
        return OneSidedContract(None, 0, None, 0.0)
    zero = sum(len(order) - (len(order) + 2) // 3 for order, _ in _degree_two_components(q))
    zero += sum(len(t) == 1 for t in q.terms)
    one = max(map(len, q.terms))
    fp = 1.0 if fpr == 1.0 else -math.expm1(zero * math.log1p(-fpr))
    fn = 1.0 if fnr == 1.0 else -math.expm1(one * math.log1p(-fnr))
    return OneSidedContract(zero, one, fp, fn)


def acceptance_to_error(truth: bool, bounds: Bounds) -> Bounds:
    """For a fixed exact answer: FPR if false, FNR if true; no truth prior."""
    lo, hi = bounds
    return (1 - hi, 1 - lo) if truth else bounds
