"""Tests for ``bernoulli.algorithms.miller_rabin``."""

from __future__ import annotations

import math
import random

import pytest

from bernoulli.algorithms import miller_rabin
from bernoulli.atom import BernoulliBool

SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
]
SMALL_COMPOSITES = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 27]


class TestWitnessPasses:
    @pytest.mark.parametrize("p", SMALL_PRIMES[2:])  # skip 2, 3
    @pytest.mark.parametrize("a", [2, 3, 5, 7])
    def test_primes_always_pass(self, p: int, a: int) -> None:
        if a >= p - 1:
            pytest.skip("a out of range for this small prime")
        assert miller_rabin.witness_passes(p, a)

    def test_composite_witnessed_by_at_least_one_small_base(self) -> None:
        # 25 is composite. At least one of bases 2, 3, ..., 23 should witness.
        n = 25
        any_witnesses = any(
            not miller_rabin.witness_passes(n, a) for a in range(2, n - 1)
        )
        assert any_witnesses

    def test_n_lt_2(self) -> None:
        assert miller_rabin.witness_passes(0, 2) is False
        assert miller_rabin.witness_passes(1, 2) is False

    def test_small_primes_special_case(self) -> None:
        assert miller_rabin.witness_passes(2, 0) is True
        assert miller_rabin.witness_passes(3, 0) is True

    def test_even_composite(self) -> None:
        assert miller_rabin.witness_passes(4, 2) is False
        assert miller_rabin.witness_passes(100, 7) is False

    def test_invalid_base(self) -> None:
        with pytest.raises(ValueError):
            miller_rabin.witness_passes(11, 1)
        with pytest.raises(ValueError):
            miller_rabin.witness_passes(11, 11)


class TestWitnessQuery:
    def test_returns_bernoulli_bool(self) -> None:
        b = miller_rabin.witness_query(7, a=2)
        assert isinstance(b, BernoulliBool)

    def test_prime_returns_one_sided_fpr_25_pct(self) -> None:
        b = miller_rabin.witness_query(101, a=2)
        assert b.value is True
        assert b.fnr == 0.0
        assert b.fpr == 0.25

    def test_definite_composite_has_zero_fpr(self) -> None:
        # Even number > 2: witnessed immediately, no further uncertainty.
        b = miller_rabin.witness_query(100)
        assert b.value is False
        assert b.fpr == 0.0

    def test_random_base_chosen_when_a_is_none(self) -> None:
        rng = random.Random(0)
        b = miller_rabin.witness_query(101, rng=rng)
        assert isinstance(b, BernoulliBool)


class TestIsProbablyPrime:
    @pytest.mark.parametrize("p", SMALL_PRIMES)
    def test_primes_always_pass(self, p: int) -> None:
        b = miller_rabin.is_probably_prime(p, rounds=10, rng=random.Random(0))
        assert b.value is True
        assert b.fnr == 0.0

    @pytest.mark.parametrize("c", SMALL_COMPOSITES)
    def test_composites_caught_with_high_probability(self, c: int) -> None:
        # 20 rounds drives FPR to (1/4)^20, so essentially every composite
        # is caught. (Worst-case Carmichael-like would still take many bases.)
        b = miller_rabin.is_probably_prime(c, rounds=20, rng=random.Random(0))
        assert b.value is False

    def test_fpr_decays_geometrically(self) -> None:
        # If we ran 10 rounds and the value was still True, fpr = (1/4)^10.
        b = miller_rabin.is_probably_prime(101, rounds=10, rng=random.Random(0))
        assert b.value is True
        assert math.isclose(b.fpr, 0.25 ** 10, abs_tol=1e-20)

    def test_zero_rounds(self) -> None:
        # No information: trivially "passes" with FPR = 1.
        b = miller_rabin.is_probably_prime(101, rounds=0)
        assert b.fpr == 1.0

    def test_invalid_rounds(self) -> None:
        with pytest.raises(ValueError):
            miller_rabin.is_probably_prime(101, rounds=-1)


class TestComposeViaAtom:
    """Two independent witness checks AND'd should match (1/4)^2."""

    def test_two_round_and_via_atom(self) -> None:
        b1 = miller_rabin.witness_query(101, a=2)
        b2 = miller_rabin.witness_query(101, a=3)
        combined = b1 & b2
        # Both inputs are one-sided FPR with fpr=0.25, fnr=0:
        # AND collapses to fpr = 0.25 * 0.25 = 0.0625, fnr = 0.
        assert math.isclose(combined.fpr, 0.0625)
        assert combined.fnr == 0.0
