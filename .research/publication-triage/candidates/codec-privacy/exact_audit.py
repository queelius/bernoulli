"""Finite probability oracles for the bounded publication audit."""

from collections.abc import Mapping, Sequence
from fractions import Fraction
from itertools import product
from math import prod

Law = Mapping[tuple[int, ...], Fraction]


def release_laws(
    p: Sequence[Fraction], q: Sequence[Fraction], releases: int
) -> tuple[dict[tuple[int, ...], Fraction], dict[tuple[int, ...], Fraction]]:
    member = {(value,) * releases: mass for value, mass in enumerate(p)}
    nonmember = {
        observation: prod((q[value] for value in observation), start=Fraction(1))
        for observation in product(range(len(q)), repeat=releases)
    }
    return member, nonmember


def bayes_accuracy(member: Law, nonmember: Law, prior: Fraction) -> Fraction:
    return sum(
        (
            max(prior * member.get(y, Fraction(0)), (1 - prior) * nonmember.get(y, Fraction(0)))
            for y in member.keys() | nonmember.keys()
        ),
        start=Fraction(0),
    )


def diagonal_bayes_accuracy(
    p: Sequence[Fraction], q: Sequence[Fraction], releases: int, prior: Fraction
) -> Fraction:
    return 1 - sum(
        (
            min(prior * member_mass, (1 - prior) * nonmember_mass**releases)
            for member_mass, nonmember_mass in zip(p, q, strict=True)
        ),
        start=Fraction(0),
    )


def coincidence_accuracy(q: Sequence[Fraction], releases: int, prior: Fraction) -> Fraction:
    return 1 - (1 - prior) * sum((mass**releases for mass in q), start=Fraction(0))


def binary_span(generators: Sequence[int]) -> frozenset[int]:
    space = {0}
    for generator in generators:
        space |= {vector ^ generator for vector in space}
    return frozenset(space)
