"""Finite-enumeration checks for the manuscript's corrected mathematical scope.

These verify independent-source laws, including boundary rates. They do not
establish that a physical filter has an independent source distribution.
"""

from itertools import product
from math import expm1, isclose, log1p, log2, prod
import sys

import pytest

from validate import main, single_valued_row_probability


def weighted_assignments(probabilities):
    for bits in product((0, 1), repeat=len(probabilities)):
        weight = prod(
            probability if bit else 1 - probability
            for bit, probability in zip(bits, probabilities, strict=True)
        )
        yield bits, weight


def probability_of(probabilities, predicate):
    return sum(
        weight for bits, weight in weighted_assignments(probabilities)
        if predicate(bits)
    )


@pytest.mark.parametrize("value_count", range(1, 7))
@pytest.mark.parametrize("eps", (0.0, 0.05, 0.5, 1.0))
@pytest.mark.parametrize("tau", (0.0, 0.5, 0.9, 1.0))
def test_defined_row_against_full_enumeration(value_count, eps, tau):
    exact = probability_of(
        (tau,) + (eps,) * (value_count - 1), lambda bits: sum(bits) <= 1
    )
    assert single_valued_row_probability(value_count, eps, tau) == pytest.approx(exact)


@pytest.mark.parametrize("value_count", range(7))
@pytest.mark.parametrize("eps", (0.0, 0.05, 0.5, 1.0))
def test_undefined_row_against_full_enumeration(value_count, eps):
    exact = probability_of((eps,) * value_count, lambda bits: sum(bits) <= 1)
    assert single_valued_row_probability(value_count, eps, None) == pytest.approx(exact)


@pytest.mark.parametrize(
    ("value_count", "eps", "tau"),
    ((-1, 0.1, None), (1, -0.1, None), (1, 1.1, None),
     (0, 0.1, 0.9), (1, 0.1, -0.1), (1, 0.1, 1.1)),
)
def test_invalid_row_parameters(value_count, eps, tau):
    with pytest.raises(ValueError):
        single_valued_row_probability(value_count, eps, tau)


def test_global_single_valuedness_includes_undefined_rows():
    eps, tau = 0.3, 0.6
    probabilities = (tau, eps, tau, eps, eps, eps)
    exact = probability_of(
        probabilities, lambda bits: all(sum(bits[start:start + 2]) <= 1
                                        for start in (0, 2, 4))
    )
    q_defined = single_valued_row_probability(2, eps, tau)
    q_undefined = single_valued_row_probability(2, eps, None)
    assert exact == pytest.approx(q_defined**2 * q_undefined)
    assert q_defined > 1 - eps  # A lone spurious value can still be single-valued.


@pytest.mark.parametrize("orbit_truth", tuple(product((0, 1), repeat=3)))
def test_mixed_orbit_sizes_and_canonical_rates(orbit_truth):
    orbits = ((0,), (1, 2), (3,))  # Diagonal, off-diagonal pair, diagonal.
    eps, tau = 0.2, 0.8
    probabilities = tuple(
        tau if truth else eps
        for truth, orbit in zip(orbit_truth, orbits, strict=True)
        for _ in orbit
    )
    for orbit, truth in zip(orbits, orbit_truth, strict=True):
        rate = tau if truth else eps
        or_rate = probability_of(probabilities, lambda bits: any(bits[i] for i in orbit))
        canonical = probability_of(probabilities, lambda bits: bits[orbit[0]])
        assert or_rate == pytest.approx(1 - (1 - rate) ** len(orbit))
        assert canonical == pytest.approx(rate)
    for bits, _ in weighted_assignments(probabilities):
        repaired = [0] * 4
        for orbit in orbits:
            for index in orbit:
                repaired[index] = int(any(bits[i] for i in orbit))
        assert repaired[1] == repaired[2]
        assert repaired[0] == bits[0] and repaired[3] == bits[3]


SOURCE_SUPPORTS = tuple(
    frozenset(i for i, selected in enumerate(mask) if selected)
    for mask in product((0, 1), repeat=3)
)


@pytest.mark.parametrize("left,right", product(SOURCE_SUPPORTS, repeat=2))
@pytest.mark.parametrize(
    "probabilities", ((0.2, 0.5, 0.8), (0.0, 0.5, 0.8),
                      (1.0, 0.5, 0.8), (0.0, 1.0, 1.0))
)
def test_projection_source_covariance(left, right, probabilities):
    def q(support):
        return prod(1 - probabilities[i] for i in support)

    marginal_left = probability_of(probabilities, lambda bits: any(bits[i] for i in left))
    marginal_right = probability_of(probabilities, lambda bits: any(bits[i] for i in right))
    joint = probability_of(
        probabilities,
        lambda bits: any(bits[i] for i in left) and any(bits[i] for i in right),
    )
    covariance = joint - marginal_left * marginal_right
    expected = q(left - right) * q(right - left) * q(left & right) * (1 - q(left & right))
    assert marginal_left == pytest.approx(1 - q(left))
    assert covariance == pytest.approx(expected, abs=1e-14)
    if all(0 < p < 1 for p in probabilities):
        assert (expected > 0) == bool(left & right)


def test_uniform_fanin_does_not_imply_uniform_true_positive_rate():
    one_member = probability_of((0.9, 0.05, 0.05), any)
    two_members = probability_of((0.9, 0.9, 0.05), any)
    assert one_member == pytest.approx(0.90975)
    assert two_members == pytest.approx(0.9905)
    assert one_member != two_members


@pytest.mark.parametrize("a,b1,b2", product((0.0, 0.25, 1.0), repeat=3))
def test_join_covariance_including_degenerate_sources(a, b1, b2):
    probabilities = (a, b1, b2)
    first = probability_of(probabilities, lambda bits: bits[0] and bits[1])
    second = probability_of(probabilities, lambda bits: bits[0] and bits[2])
    joint = probability_of(probabilities, all)
    assert joint - first * second == pytest.approx(a * (1 - a) * b1 * b2)


def is_transitive(relation):
    return all(
        (left, right) in relation
        for left, middle in relation
        for middle2, right in relation
        if middle == middle2
    )


THREE_VERTEX_UNIVERSE = tuple(product(range(3), repeat=2))


@pytest.mark.parametrize("eps,tau", ((0.05, 0.9), (0.7, 0.2)))
@pytest.mark.parametrize(
    "exact",
    (
        frozenset(),
        frozenset((a, b) for a, b in THREE_VERTEX_UNIVERSE if a == b),
        frozenset((a, b) for a, b in THREE_VERTEX_UNIVERSE if a < b),
        frozenset(THREE_VERTEX_UNIVERSE),
    ),
)
def test_transitivity_bound_against_finite_law(eps, tau, exact):
    universe = THREE_VERTEX_UNIVERSE
    # The four fixtures vary density; the probability calculation enumerates
    # every reported relation, including relations with false premise edges.
    probabilities = tuple(tau if pair in exact else eps for pair in universe)
    preservation = probability_of(
        probabilities,
        lambda bits: is_transitive(
            {pair for pair, bit in zip(universe, bits, strict=True) if bit}
        ),
    )
    upper_bound = 1 - min(eps, tau) ** 2 * (1 - max(eps, tau))
    assert preservation <= upper_bound + 1e-14


@pytest.mark.parametrize("value_count", range(1, 6))
@pytest.mark.parametrize("eps", (0.0, 0.05, 1.0))
@pytest.mark.parametrize("tau", (0.0, 0.9, 1.0))
def test_deletion_retained_true_value(value_count, eps, tau):
    exact = sum(
        weight / sum(bits)
        for bits, weight in weighted_assignments((tau,) + (eps,) * (value_count - 1))
        if bits[0]
    )
    formula = tau if eps == 0 else tau * (1 - (1 - eps) ** value_count) / (eps * value_count)
    assert exact == pytest.approx(formula)


@pytest.mark.parametrize("maximum_size", (1, 2, 5))
@pytest.mark.parametrize("target", (1e-6, 0.05, 0.9))
def test_orbit_rate_budget_uses_size_bound(maximum_size, target):
    raw_rate = -expm1(log1p(-target) / maximum_size)
    for actual_size in range(1, maximum_size + 1):
        repaired_rate = 1 - (1 - raw_rate) ** actual_size
        assert repaired_rate <= target + 1e-14
        if actual_size == maximum_size:
            assert repaired_rate == pytest.approx(target)
    if target == 1e-6:
        assert isclose(log2(target / raw_rate), log2(maximum_size), abs_tol=1e-6)


def test_validation_driver_smoke(monkeypatch, capsys):
    monkeypatch.setattr(
        sys, "argv", ["validate.py", "--trials", "25000", "--tol", "0.04"]
    )
    assert main() == 0
    report = capsys.readouterr().out
    assert "ALL PASS" in report
    assert "MISMATCH (expected)" in report
    assert "P(single-valued undefined key)" in report
