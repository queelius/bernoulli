"""Independent finite oracles, plus integration checks on the stored retrieval."""

from fractions import Fraction as F  # noqa: N817 - conventional exact-arithmetic notation
from itertools import product

import pytest
from bernoulli.maps.codec import PrefixCodec
from bernoulli.maps.retrieval import GF2Retrieval
from exact_audit import (
    bayes_accuracy,
    binary_span,
    coincidence_accuracy,
    diagonal_bayes_accuracy,
    release_laws,
)


def test_rare_diagonal_counterexample_against_all_classifiers():
    p, q = (F(99, 100), F(1, 100)), (F(1, 2), F(1, 2))
    member, nonmember = release_laws(p, q, 2)
    observations = list(product(range(2), repeat=2))
    scores = []
    for decisions in product((False, True), repeat=4):
        scores.append(
            sum(
                F(1, 2) * (member.get(y, F(0)) if decision else nonmember[y])
                for y, decision in zip(observations, decisions, strict=True)
            )
        )
    assert max(scores) == F(87, 100)
    assert bayes_accuracy(member, nonmember, F(1, 2)) == max(scores)
    assert diagonal_bayes_accuracy(p, q, 2, F(1, 2)) == max(scores)
    assert coincidence_accuracy(q, 2, F(1, 2)) == F(3, 4)


@pytest.mark.parametrize("alphabet", [2, 3])
def test_closed_form_against_complete_observation_enumeration(alphabet):
    distributions = [
        tuple(F(x, 4) for x in counts)
        for counts in product(range(5), repeat=alphabet)
        if sum(counts) == 4
    ]
    for p, q, releases, prior in product(
        distributions, distributions, range(1, 5), (F(1, 4), F(1, 2), F(3, 4))
    ):
        member, nonmember = release_laws(p, q, releases)
        assert sum(member.values()) == sum(nonmember.values()) == 1
        assert diagonal_bayes_accuracy(p, q, releases, prior) == bayes_accuracy(
            member, nonmember, prior
        )
        equality_score = sum(
            prior * member.get(y, F(0)) if len(set(y)) == 1 else (1 - prior) * nonmember[y]
            for y in nonmember
        )
        assert equality_score == coincidence_accuracy(q, releases, prior)


def test_equal_marginals_disjoint_frozen_transcripts():
    same = {(0, 0): F(1, 2), (1, 1): F(1, 2)}
    opposite = {(0, 1): F(1, 2), (1, 0): F(1, 2)}
    for coordinate in (0, 1):
        assert sum(mass for y, mass in same.items() if y[coordinate] == 0) == F(1, 2)
        assert sum(mass for y, mass in opposite.items() if y[coordinate] == 0) == F(1, 2)
    assert bayes_accuracy(same, opposite, F(1, 2)) == 1


def test_span_against_all_linear_combinations():
    for generators in product(range(8), repeat=3):
        expected = set()
        for coefficients in product((0, 1), repeat=3):
            result = 0
            for coefficient, vector in zip(coefficients, generators, strict=True):
                if coefficient:
                    result ^= vector
            expected.add(result)
        assert binary_span(generators) == expected
    assert binary_span(()) == {0}


def test_existing_prefix_default_randomization_excludes_surplus():
    codec = PrefixCodec([("a", 1), ("b", 3)], default_value="a", m_bits=3)
    full_fiber = {pattern for pattern in range(8) if codec.decode(pattern) == "a"}
    reachable = {codec.encode_random("a", suffix) for suffix in range(4)}
    assert len(full_fiber) == 7
    assert len(reachable) == 4
    assert reachable < full_fiber


def test_existing_retrieval_is_frozen_and_member_exact():
    items = {f"member-{i}".encode(): i % 8 for i in range(30)}
    for seed in (1, 7, 2026):
        retrieval = GF2Retrieval(items, value_bits=3, seed=seed)
        assert all(retrieval.query(key) == value for key, value in items.items())
        assert len({retrieval.query(b"absent") for _ in range(20)}) == 1
