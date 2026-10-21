"""Independent fixtures catch lost source identity, unsound bounds, and DP errors."""

import math
import random
from itertools import combinations, product

import pytest

from contracts import (
    DNF,
    Channel,
    Relation,
    acceptance_to_error,
    condition_bounds,
    degree_two_exact,
    dissociation_bounds,
    exact_probability,
    frechet_bounds,
    packing_bounds,
)


def test_aliasing_and_absorption():
    q = DNF.from_terms([{0, 1}, {0}]).quotient({0: 5, 1: 5})
    assert exact_probability(q, {5: 0.2}) == pytest.approx(0.2)
    assert exact_probability(DNF.from_terms([[0, 0]]), {0: 0.2}) == pytest.approx(0.2)


def test_direct_dnf_construction_enforces_absorption():
    q = DNF(frozenset({frozenset({0}), frozenset({0, 1})}))
    assert degree_two_exact(q, {0: 0.5, 1: 0.5}) == pytest.approx(0.5)


def test_package_independence_assumption_boundary():
    from bernoulli import BernoulliBool

    b = BernoulliBool(True, fpr=0.2, fnr=0.1)
    # Existing API explicitly models two independent shared-truth observations.
    assert (b & b).fpr == pytest.approx(0.04)
    # The research representation instead retains the identity of one frozen bit.
    assert exact_probability(DNF.atom(0) & DNF.atom(0), {0: b.fpr}) == pytest.approx(0.2)


def test_shared_join_projection():
    r = Relation(("a", "b"), {(1, 10): DNF.atom(0), (1, 11): DNF.atom(1)})
    s = Relation(("b", "c"), {(10, 7): DNF.atom(2), (11, 7): DNF.atom(2)})
    q = r.join(s).select(lambda row: row["a"] == 1).project(("a", "c")).rows[(1, 7)]
    assert exact_probability(q, {0: 0.3, 1: 0.4, 2: 0.2}) == pytest.approx(0.116)
    assert dissociation_bounds(q, {0: 0.3, 1: 0.4, 2: 0.2})[1] == pytest.approx(0.1352)
    assert condition_bounds(q, {0: 0.3, 1: 0.4, 2: 0.2}, [2]) == pytest.approx((0.116, 0.116))


def test_symmetry_induces_projection_dependence():
    r = Relation(("a", "b"), {(0, 1): DNF.atom(0), (1, 0): DNF.atom(0)})
    projected = r.project(("a",))
    both = projected.rows[(0,)] & projected.rows[(1,)]
    assert exact_probability(both, {0: 0.2}) == pytest.approx(0.2)


def test_literal_cycle_probabilities():
    for edges, expected in [
        ([{0, 1}, {1, 2}], 3 / 8),
        ([{0, 1}, {1, 2}, {2, 3}, {3, 0}], 9 / 16),
        ([{0, 1}, {1, 2}, {0, 2}], 1 / 2),
    ]:
        q = DNF.from_terms(edges)
        assert degree_two_exact(q, dict.fromkeys(q.support, 0.5)) == pytest.approx(expected)


def test_symmetric_cubic_query_literal_edge_cover_count():
    # K4 has 41 edge covers out of 64 edge subsets. Query detects a full star.
    edges = list(combinations(range(4), 2))
    q = DNF.from_terms([{i for i, e in enumerate(edges) if v in e} for v in range(4)])
    assert exact_probability(q, dict.fromkeys(range(6), 0.5)) == pytest.approx(23 / 64)
    lo, hi = dissociation_bounds(q, dict.fromkeys(range(6), 0.5))
    assert lo <= 23 / 64 <= hi
    assert hi == pytest.approx(1 - (7 / 8) ** 4)


@pytest.mark.parametrize("n", range(2, 10))
def test_weighted_degree_two_matches_enumeration(n):
    rng = random.Random(n)
    for cycle in [False, True]:
        terms = [{i, i + 1} for i in range(n - 1)]
        if cycle:
            terms.append({n - 1, 0})
        q = DNF.from_terms(terms)
        p = {i: rng.choice([0.0, 0.01, 0.2, 0.5, 0.9, 1.0]) for i in range(n)}
        assert degree_two_exact(q, p) == pytest.approx(exact_probability(q, p), abs=1e-13)


def test_disconnected_components_and_singletons():
    q = DNF.from_terms([{0}, {1, 2}, {3, 4}, {4, 5}, {3, 5}])
    p = dict.fromkeys(range(6), 0.5)
    assert degree_two_exact(q, p) == pytest.approx(13 / 16)


def test_all_small_dnfs_and_endpoint_rates_are_bounded():
    terms = [frozenset(i for i in range(3) if mask & (1 << i)) for mask in range(8)]
    for mask in range(256):
        q = DNF.from_terms([terms[i] for i in range(8) if mask & (1 << i)])
        for ps in product([0.0, 0.2, 1.0], repeat=3):
            p = dict(enumerate(ps))
            exact = exact_probability(q, p)
            for method in [frechet_bounds, dissociation_bounds, packing_bounds]:
                lo, hi = method(q, p)
                assert lo - 1e-12 <= exact <= hi + 1e-12


def test_conditioning_monotonicity_and_exact_completion():
    rng = random.Random(73)
    for _ in range(40):
        q = DNF.from_terms([rng.sample(range(6), rng.randint(1, 3)) for _ in range(8)])
        p = {i: rng.random() for i in range(6)}
        exact = exact_probability(q, p)
        old = (0.0, 1.0)
        for k in range(7):
            bounds = condition_bounds(q, p, list(range(k)))
            assert bounds[0] >= old[0] - 1e-12
            assert bounds[1] <= old[1] + 1e-12
            assert bounds[0] - 1e-12 <= exact <= bounds[1] + 1e-12
            old = bounds
        assert old == pytest.approx((exact, exact))


def test_irrelevant_conditioning_sources_do_not_exhaust_stack():
    q = DNF.from_terms([{0, 1}, {1, 2}, {0, 2}])
    p = dict.fromkeys(range(3), 0.5)
    assert condition_bounds(q, p, range(1000, 3000)) == condition_bounds(q, p, [])


def test_sources_eliminated_by_conditioning_do_not_exhaust_stack():
    q = DNF.from_terms(
        [{0, i} for i in range(1, 1101)] + [{2000, 2001}, {2001, 2002}, {2000, 2002}]
    )
    p = dict.fromkeys(q.support, 0.5)
    assert condition_bounds(q, p, range(1101)) == condition_bounds(q, p, [0])


def test_truth_uniform_one_sided_cycle_contract():
    from contracts import degree_two_contract

    q = DNF.from_terms([{0, 1}, {1, 2}, {2, 3}, {3, 0}])
    contract = degree_two_contract(q, 0.1, 0.2)
    assert contract.zero_sensitivity == 2
    assert contract.one_sensitivity == 2
    assert contract.fpr_max == pytest.approx(0.19)
    assert contract.fnr_max == pytest.approx(0.36)
    fps, fns = [], []
    for bits in product([False, True], repeat=4):
        truth = dict(enumerate(bits))
        if q.evaluate(truth):
            p = {i: 0.8 if b else 0.0 for i, b in truth.items()}
            fns.append(1 - exact_probability(q, p))
        else:
            p = {i: 1.0 if b else 0.1 for i, b in truth.items()}
            fps.append(exact_probability(q, p))
    assert contract.fpr_max == pytest.approx(max(fps))
    assert contract.fnr_max == pytest.approx(max(fns))


def test_uniform_contract_constants_components_and_boundaries():
    from contracts import degree_two_contract

    false = degree_two_contract(DNF.from_terms([]), 0.1, 0.2)
    assert (false.fpr_max, false.fnr_max) == (0.0, None)
    true = degree_two_contract(DNF.from_terms([[]]), 0.1, 0.2)
    assert (true.fpr_max, true.fnr_max) == (None, 0.0)
    assert degree_two_contract(DNF.atom(0), 0.0, 1.0).fpr_max == 0.0
    assert degree_two_contract(DNF.atom(0), 0.0, 1.0).fnr_max == 1.0
    assert degree_two_contract(DNF.atom(0), 1.0, 0.0).fpr_max == 1.0
    q = DNF.from_terms([{0}, {1, 2}, {3, 4}, {4, 5}, {3, 5}])
    contract = degree_two_contract(q, 0.1, 0.2)
    assert contract.zero_sensitivity == 4
    assert contract.fpr_max == pytest.approx(1 - 0.9**4)
    assert contract.fnr_max == pytest.approx(0.36)
    with pytest.raises(ValueError):
        degree_two_contract(q, -1.0, 0.1)


def test_two_sided_errors_bounded_by_one_sided_maxima():
    from contracts import degree_two_contract

    q = DNF.from_terms([{0, 1}, {1, 2}, {2, 3}, {3, 0}])
    contract = degree_two_contract(q, 0.1, 0.2)
    for bits in product([False, True], repeat=4):
        truth = dict(enumerate(bits))
        p = {i: 0.8 if b else 0.1 for i, b in truth.items()}
        acceptance = exact_probability(q, p)
        if q.evaluate(truth):
            assert 1 - acceptance <= contract.fnr_max + 1e-12
        else:
            assert acceptance <= contract.fpr_max + 1e-12


def test_error_orientation_and_channel_semantics():
    assert Channel(False, 0.1, 0.2).acceptance == 0.1
    assert Channel(True, 0.1, 0.2).acceptance == 0.8
    assert acceptance_to_error(False, (0.2, 0.3)) == (0.2, 0.3)
    assert acceptance_to_error(True, (0.2, 0.3)) == pytest.approx((0.7, 0.8))
    q = DNF.from_terms([{0, 1}])
    p = {0: Channel(False, 0.1, 0.2).acceptance, 1: Channel(True, 0.4, 0.2).acceptance}
    assert exact_probability(q, p) == pytest.approx(0.08)


def test_arbitrary_dependence_bounds_cover_nonproduct_laws():
    q = DNF.from_terms([{0, 1}])
    assert frechet_bounds(q, {0: 0.5, 1: 0.5}) == (0.0, 0.5)


@pytest.mark.parametrize("q", [DNF.from_terms([]), DNF.from_terms([[]])])
def test_constants(q):
    expected = float(q.evaluate({}))
    for method in [frechet_bounds, dissociation_bounds, packing_bounds]:
        assert method(q, {}) == (expected, expected)
    assert exact_probability(q, {}) == expected
    assert degree_two_exact(q, {}) == expected


def test_invalid_inputs_rejected():
    for p in [-0.1, 1.1, math.nan, math.inf]:
        with pytest.raises(ValueError):
            exact_probability(DNF.atom(0), {0: p})
        with pytest.raises(ValueError):
            Channel(True, p, 0.1)
    with pytest.raises(ValueError):
        Channel(False, 0.1, -1)
    with pytest.raises(ValueError):
        degree_two_exact(DNF.from_terms([{0, 1, 2}]), {0: 0.1, 1: 0.2, 2: 0.3})
    with pytest.raises(ValueError):
        degree_two_exact(
            DNF.from_terms([{0, i} for i in range(1, 4)]), dict.fromkeys(range(4), 0.5)
        )
    with pytest.raises(ValueError):
        Relation(("x", "x"), {})
    with pytest.raises(ValueError):
        Relation(("x",), {(1, 2): DNF.atom(0)})
    with pytest.raises(ValueError):
        Relation(("x",), {}).project(("y",))
    with pytest.raises(KeyError):
        exact_probability(DNF.atom(0), {})
