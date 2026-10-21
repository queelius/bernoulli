"""Independent finite checks, not a simulation-based privacy proof."""

from fractions import Fraction
from itertools import product

import pytest

from joint_probe import System, image_dimension, rank, transcript_law


def test_uniform_marginals_do_not_determine_three_query_transcript() -> None:
    # One slot per segment in a 2+2+2 incidence space.
    queries = (41, 38, 26)
    constrained = System(6, (21,), (1,), queries)
    unconstrained = System(6, (42,), (1,), queries)
    left = transcript_law(constrained)
    right = transcript_law(unconstrained)
    assert len(left) == 4
    assert len(right) == 8
    assert all(sum(word) % 2 == 1 for word in left)
    for index in range(3):
        assert sum(p for word, p in left.items() if word[index]) == Fraction(1, 2)
        assert sum(p for word, p in right.items() if word[index]) == Fraction(1, 2)
    assert image_dimension(constrained) == 2
    assert image_dimension(unconstrained) == 3
    assert rank(queries) == 3


def test_rank_formula_against_complete_slot_enumeration() -> None:
    # All one/two-row constraints and two queries in dimensions 1..3.
    for columns in range(1, 4):
        for rows in product(range(1 << columns), repeat=2):
            for queries in product(range(1 << columns), repeat=2):
                for witness in (0, (1 << columns) - 1):
                    targets = tuple((row & witness).bit_count() % 2 for row in rows)
                    system = System(columns, rows, targets, queries)
                    law = transcript_law(system)
                    size = 1 << image_dimension(system)
                    assert len(law) == size
                    assert set(law.values()) == {Fraction(1, size)}


def test_repeated_query_is_one_frozen_observation() -> None:
    system = System(2, (), (), (1, 1))
    assert transcript_law(system) == {(0, 0): Fraction(1, 2), (1, 1): Fraction(1, 2)}
    # The public query dependence exists with no stored constraints.
    assert rank(system.queries) - image_dimension(system) == 0


def test_two_bit_words_and_empty_query() -> None:
    assert transcript_law(System(0, (), (), ())) == {(): Fraction(1)}
    law = transcript_law(System(3, (7,), (2,), (1, 2, 4), bits=2))
    assert len(law) == 16
    assert all(x ^ y ^ z == 2 for x, y, z in law)


def test_inconsistent_system_and_exhaustion_limits() -> None:
    with pytest.raises(ValueError, match="inconsistent"):
        transcript_law(System(1, (1, 1), (0, 1), (1,)))
    with pytest.raises(ValueError, match="65536"):
        transcript_law(System(17, (), (), ()))
    for args in [(-1, (), (), (), 1), (1, (2,), (0,), (), 1),
                 (1, (1,), (), (), 1), (1, (1,), (2,), (), 1),
                 (1, (), (), (), 0)]:
        with pytest.raises(ValueError):
            System(*args)
    with pytest.raises(ValueError):
        rank((-1,))
