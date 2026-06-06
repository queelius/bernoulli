"""Tests for bernoulli.relations.relation (approximate relational algebra)."""

from __future__ import annotations

import math

import pytest

from bernoulli.relations import BernoulliRelation
from bernoulli.sets.composition import Partition, SetRates, intersection


def rel(
    schema: tuple[str, ...],
    tuples: list[tuple[object, ...]],
    fpr: float = 0.0,
    fnr: float = 0.0,
) -> BernoulliRelation:
    return BernoulliRelation(schema, tuples, SetRates(fpr, fnr))


class TestConstruction:
    def test_basics(self) -> None:
        r = rel(("id", "city"), [(1, "NYC"), (2, "LA")], fpr=0.01)
        assert r.arity == 2
        assert len(r) == 2
        assert r.contains((1, "NYC"))
        assert not r.contains((9, "X"))
        assert set(r) == {(1, "NYC"), (2, "LA")}

    def test_dedup(self) -> None:
        assert len(rel(("a",), [(1,), (1,), (2,)])) == 2

    def test_arity_mismatch(self) -> None:
        with pytest.raises(ValueError):
            BernoulliRelation(("a", "b"), [(1,)])

    def test_duplicate_schema(self) -> None:
        with pytest.raises(ValueError):
            BernoulliRelation(("a", "a"), [])

    def test_default_rates_exact(self) -> None:
        assert BernoulliRelation(("a",), [(1,)]).rates.rates == (0.0, 0.0)


class TestSelect:
    def test_filters_and_keeps_rates(self) -> None:
        r = rel(("id", "age"), [(1, 30), (2, 17), (3, 41)], fpr=0.02, fnr=0.05)
        adults = r.select(lambda row: row["age"] >= 18)  # type: ignore[operator]
        assert {t[0] for t in adults} == {1, 3}
        assert adults.rates.rates == (0.02, 0.05)  # restriction leaves rates alone
        assert adults.schema == ("id", "age")


class TestProject:
    def test_exact_projection(self) -> None:
        r = rel(("city", "id"), [("NYC", 1), ("NYC", 2), ("LA", 3)])
        cities = r.project(["city"])
        assert {t[0] for t in cities} == {"NYC", "LA"}
        assert cities.schema == ("city",)

    def test_fnr_drops_with_fiber(self) -> None:
        r = rel(("city", "id"), [("NYC", 1), ("NYC", 2), ("LA", 3)], fnr=0.2)
        cities = r.project(["city"])
        # mean of 0.2**2 (NYC fiber 2) and 0.2**1 (LA fiber 1) = (0.04 + 0.2) / 2
        assert math.isclose(cities.rates.fnr, 0.12)
        assert cities.rates.fpr == 0.0

    def test_unknown_attr_raises(self) -> None:
        with pytest.raises(ValueError):
            rel(("a",), [(1,)]).project(["b"])


class TestJoin:
    def test_natural_join_tuples(self) -> None:
        r = rel(("id", "city"), [(1, "NYC"), (2, "LA")])
        s = rel(("id", "age"), [(1, 30), (2, 17), (3, 41)])
        j = r.join(s)
        assert j.schema == ("id", "city", "age")
        assert set(j) == {(1, "NYC", 30), (2, "LA", 17)}

    def test_rates_via_intersection_sparse(self) -> None:
        r = rel(("id", "x"), [(1, "a")], fpr=0.10)
        s = rel(("id", "y"), [(1, "b")], fpr=0.20)
        j = r.join(s)
        assert math.isclose(j.rates.fpr, 0.10 * 0.20)  # sparse-limit product
        assert j.rates.fnr == 0.0

    def test_rates_are_set_intersection(self) -> None:
        rr, sr = SetRates(0.1, 0.05), SetRates(0.2, 0.07)
        r = BernoulliRelation(("id", "x"), [(1, "a"), (2, "b")], rr)
        s = BernoulliRelation(("id", "y"), [(1, "c"), (2, "d")], sr)
        part = Partition.from_masses(1, 1, 1, 1)
        j = r.join(s, partition=part)
        assert j.rates == intersection(rr, sr, part)  # join IS intersection on rates

    def test_no_shared_attrs_is_cross_product(self) -> None:
        r = rel(("a",), [(1,), (2,)])
        s = rel(("b",), [(9,), (8,)])
        j = r.join(s)
        assert j.schema == ("a", "b")
        assert len(j) == 4
