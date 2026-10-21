from fractions import Fraction
from itertools import product

import pytest

from contracts import Budget, FunctionalSchema, IntersectionQuery, error_bound, plan_rate
from value_store import FrozenValues, ValueMode


def exact_probability(k, a, b, p):
    result = Fraction(0)
    sources = [(r, v) for r in (0, 1) for v in range(k) if v != (a, b)[r]]
    for outcomes in product((False, True), repeat=len(sources)):
        values = dict(zip(sources, outcomes, strict=True))
        weight = p ** sum(outcomes) * (1 - p) ** (len(outcomes) - sum(outcomes))
        answer = any((a == v or values[0, v]) and (b == v or values[1, v]) for v in range(k))
        result += weight * answer
    return result


@pytest.mark.parametrize('k', [2, 3, 4])
@pytest.mark.parametrize('p', [Fraction(0), Fraction(1, 7), Fraction(1, 2), Fraction(1)])
def test_constrained_contract_is_exact_worst_profile(k, p):
    observed = max(exact_probability(k, a, b, p) for a in range(-1, k) for b in range(-1, k) if a != b or a == -1)
    assert error_bound(Budget.CONSTRAINED_PRODUCT, k, p) == observed
    assert observed <= error_bound(Budget.CONSTRAINED_UNION, k, p)


def test_single_candidate_and_invalid_domains():
    p = Fraction(1, 3)
    for budget in Budget:
        assert error_bound(budget, 1, p) == p
        assert error_bound(budget, 0, p) == 0
        with pytest.raises(ValueError):
            error_bound(budget, -1, p)
        with pytest.raises(ValueError):
            error_bound(budget, 2, Fraction(2))


@pytest.mark.parametrize('budget', list(Budget))
def test_planning_rate_has_exact_safe_rounding(budget):
    target = Fraction(1, 20)
    for k in (1, 3, 64, 1024):
        rate = plan_rate(budget, k, target)
        assert error_bound(budget, k, rate) <= target
        assert error_bound(budget, k, rate + Fraction(1, 2**40)) >= target


def test_source_identity_and_constraint_extraction():
    schema = FunctionalSchema(8, total=True)
    query = IntersectionQuery(3, 5, repeats=4)
    lineage = query.lineage(schema)
    assert len(lineage) == 8
    assert sum(map(len, lineage)) == 16
    repeated = IntersectionQuery(3, 3, repeats=4)
    assert sum(map(len, repeated.lineage(schema))) == 8
    assert repeated.exact_from_schema(schema) is True
    assert repeated.exact_from_schema(FunctionalSchema(8, total=False)) is None


@pytest.mark.parametrize('mode', list(ValueMode))
def test_value_payload_roundtrip_and_no_false_negatives(mode):
    values = [0, 3, 1, 3, 7]
    store = FrozenValues.build(values, 8, mode, 3, seed=19)
    restored = FrozenValues.deserialize(store.serialize())
    assert restored.payload_bytes == len(store.serialize())
    assert restored.equal(1, 3)
    assert all(restored.equal(i, i) for i in range(len(values)))
    assert [store.value(i) for i in range(len(values))] == [restored.value(i) for i in range(len(values))]
    if mode is ValueMode.EXACT:
        assert not restored.equal(1, 2)
    with pytest.raises(IndexError):
        restored.value(-1)
    with pytest.raises(IndexError):
        restored.value(len(values))
    for payload in (b'', store.serialize()[:-1], b'xxxxxxxx' + store.serialize()[8:]):
        with pytest.raises(ValueError):
            FrozenValues.deserialize(payload)


def test_finite_linear_family_exhaustive_pair_guarantee():
    # Enumerating every 2x3 matrix is an exact finite-family calculation.
    values = list(range(8))
    for a in values:
        for b in values:
            if a >= b:
                continue
            collisions = 0
            for masks in product(range(8), repeat=2):
                store = FrozenValues.from_masks(values, 8, masks)
                collisions += store.equal(a, b)
            assert collisions == 16


def test_linear_collision_dependence_counterexample():
    # Differences 1,2,3 have rank2, so their three collision events are not iid.
    collisions = 0
    for mask in range(4):
        store = FrozenValues.from_masks([0, 1, 2, 3], 4, (mask,))
        collisions += any(store.equal(0, i) for i in (1, 2, 3))
    assert collisions == 4  # independent estimate would be 7/8
