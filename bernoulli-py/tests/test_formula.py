"""Tests for ``bernoulli.formula``: exact error rates through Boolean formulas.

The reference for every exact claim is brute-force enumeration over observed
words, which follows the model's definition directly. Property tests compare
the evaluator against it on random formulas, including ones that reuse a
variable; worked tests pin the README counterexample and tie the module to the
single-gate formulas in ``BernoulliBool`` and ``bernoulli.sets.composition``.
"""

from __future__ import annotations

import itertools
import math
import random
from collections.abc import Sequence

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from bernoulli import BernoulliBool
from bernoulli.formula import (
    MAX_ENUMERATION_VARIABLES,
    And,
    Formula,
    Not,
    Or,
    RatePair,
    Var,
    error_probability,
    error_profile,
    marginal_rates,
    output_probability,
    variables,
    worst_case_rates,
)
from bernoulli.harness import wilson_ci
from bernoulli.sets.composition import Partition, SetRates, intersection, union

EPS, OMEGA = 0.02, 0.10
CHANNELS = [SetRates(fpr=EPS, fnr=OMEGA)] * 3
X = variables(3)
COUNTEREXAMPLE = (X[0] & X[1]) | X[2]
WORD_010 = (False, True, False)
EXACT_010 = 1.0 - (1.0 - EPS * (1.0 - OMEGA)) * (1.0 - EPS)  # 0.03764
PAIR_REUSE = 1.0 - (1.0 - EPS * EPS) * (1.0 - EPS)  # 0.020392


def brute_force_output_probability(
    formula: Formula, channels: Sequence[RatePair], word: Sequence[bool]
) -> float:
    """The model's definition: sum over observed words of P(o | w) [f(o)]."""
    total = 0.0
    for observed in itertools.product((False, True), repeat=len(channels)):
        weight = 1.0
        for o, w, ch in zip(observed, word, channels, strict=True):
            p_true = 1.0 - ch.fnr if w else ch.fpr
            weight *= p_true if o else 1.0 - p_true
        if formula.evaluate(observed):
            total += weight
    return total


# ---------------------------------------------------------------------------
# strategies
# ---------------------------------------------------------------------------

rate_st = st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)
channel_st = st.builds(SetRates, fpr=rate_st, fnr=rate_st)


def formulas(n_vars: int, max_leaves: int = 6) -> st.SearchStrategy[Formula]:
    """Random formulas over ``n_vars`` variables; variables may repeat."""
    leaf = st.integers(min_value=0, max_value=n_vars - 1).map(Var)
    return st.recursive(
        leaf,
        lambda sub: st.one_of(
            sub.map(Not),
            st.tuples(sub, sub).map(lambda lr: And(*lr)),
            st.tuples(sub, sub).map(lambda lr: Or(*lr)),
        ),
        max_leaves=max_leaves,
    )


@st.composite
def monotone_read_once(draw: st.DrawFn, n_vars: int) -> Formula:
    """A random AND/OR tree using each of ``x0 .. x{n-1}`` exactly once."""
    order = draw(st.permutations(range(n_vars)))
    nodes: list[Formula] = [Var(i) for i in order]
    while len(nodes) > 1:
        i = draw(st.integers(min_value=0, max_value=len(nodes) - 2))
        left, right = nodes[i], nodes[i + 1]
        node: Formula = And(left, right) if draw(st.booleans()) else Or(left, right)
        nodes[i : i + 2] = [node]
    return nodes[0]


@st.composite
def formula_case(
    draw: st.DrawFn,
) -> tuple[Formula, list[SetRates], tuple[bool, ...]]:
    n = draw(st.integers(min_value=1, max_value=4))
    f = draw(formulas(n))
    channels = draw(st.lists(channel_st, min_size=n, max_size=n))
    word = tuple(draw(st.lists(st.booleans(), min_size=n, max_size=n)))
    return f, channels, word


# ---------------------------------------------------------------------------
# formula construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_operators_build_nodes(self) -> None:
        x0, x1 = variables(2)
        assert (x0 & x1) == And(Var(0), Var(1))
        assert (x0 | x1) == Or(Var(0), Var(1))
        assert ~x0 == Not(Var(0))

    def test_str(self) -> None:
        assert str(COUNTEREXAMPLE) == "(x0 & x1) | x2"
        assert str(~(X[0] | ~X[1])) == "~(x0 | ~x1)"

    def test_evaluate_matches_python_boolean(self) -> None:
        for word in itertools.product((False, True), repeat=3):
            assert COUNTEREXAMPLE.evaluate(word) == ((word[0] and word[1]) or word[2])

    def test_occurrences_and_read_once(self) -> None:
        assert COUNTEREXAMPLE.is_read_once()
        reused = (X[0] & X[1]) | (X[0] & X[2])
        assert not reused.is_read_once()
        assert reused.occurrences()[0] == 2

    def test_negative_index_rejected(self) -> None:
        with pytest.raises(ValueError):
            Var(-1)

    def test_variables(self) -> None:
        assert variables(0) == ()
        assert variables(2) == (Var(0), Var(1))
        with pytest.raises(ValueError):
            variables(-1)

    def test_nodes_are_hashable_and_frozen(self) -> None:
        assert len({X[0] & X[1], And(Var(0), Var(1))}) == 1
        with pytest.raises((AttributeError, TypeError)):
            X[0].index = 5  # type: ignore[misc]


# ---------------------------------------------------------------------------
# the counterexample: pair reuse is not exact
# ---------------------------------------------------------------------------


class TestCounterexample:
    def test_exact_error_at_word_010(self) -> None:
        assert math.isclose(error_probability(COUNTEREXAMPLE, CHANNELS, WORD_010), EXACT_010)
        assert math.isclose(EXACT_010, 0.03764)

    def test_chained_operators_reuse_the_pair(self) -> None:
        b = BernoulliBool(value=False, fpr=EPS, fnr=OMEGA)
        chained = (b & b) | b
        assert math.isclose(chained.fpr, PAIR_REUSE)
        assert math.isclose(PAIR_REUSE, 0.020392)
        # The reused pair understates the true error by almost half.
        assert chained.fpr < 0.55 * EXACT_010

    def test_pair_reuse_is_exact_only_at_all_negative_word(self) -> None:
        profile = error_profile(COUNTEREXAMPLE, CHANNELS)
        negatives = [w for w in profile if not COUNTEREXAMPLE.evaluate(w)]
        matches = [w for w in negatives if math.isclose(profile[w], PAIR_REUSE)]
        assert matches == [(False, False, False)]

    def test_worst_case_pair_bounds_every_word(self) -> None:
        worst = worst_case_rates(COUNTEREXAMPLE, CHANNELS)
        assert math.isclose(worst.fpr, EXACT_010)
        for word, err in error_profile(COUNTEREXAMPLE, CHANNELS).items():
            bound = worst.fnr if COUNTEREXAMPLE.evaluate(word) else worst.fpr
            assert err <= bound + 1e-12

    def test_monte_carlo_agrees_with_exact_not_pair(self) -> None:
        """A seeded simulation through BernoulliBool.observe sides with exact."""
        rng = random.Random(20261021)
        n = 20_000
        hits = 0
        for _ in range(n):
            o = [BernoulliBool.observe(w, fpr=EPS, fnr=OMEGA, rng=rng).value for w in WORD_010]
            hits += (o[0] and o[1]) or o[2]
        low, high = wilson_ci(hits, n)
        assert low <= EXACT_010 <= high
        assert not low <= PAIR_REUSE <= high

    def test_set_composition_point_mass_is_exact_sparse_is_not(self) -> None:
        """Nesting ch6 composition: exact with point-mass partitions only."""
        a = b = c = SetRates(fpr=EPS, fnr=OMEGA)
        # The query is in B only: cell b_only for (A, B), then neither for (A&B, C).
        inner = intersection(a, b, Partition(both=0.0, a_only=0.0, b_only=1.0, neither=0.0))
        outer = union(inner, c, Partition.sparse())
        assert math.isclose(outer.fpr, EXACT_010)
        inner_sparse = intersection(a, b, Partition.sparse())
        assert math.isclose(union(inner_sparse, c, Partition.sparse()).fpr, PAIR_REUSE)


# ---------------------------------------------------------------------------
# exactness against brute force
# ---------------------------------------------------------------------------


class TestExactness:
    @given(formula_case())
    @settings(max_examples=300, deadline=None)
    def test_output_probability_matches_brute_force(
        self, case: tuple[Formula, list[SetRates], tuple[bool, ...]]
    ) -> None:
        f, channels, word = case
        expected = brute_force_output_probability(f, channels, word)
        assert math.isclose(output_probability(f, channels, word), expected, abs_tol=1e-12)

    @given(formula_case())
    @settings(max_examples=100, deadline=None)
    def test_error_is_complement_on_positive_words(
        self, case: tuple[Formula, list[SetRates], tuple[bool, ...]]
    ) -> None:
        f, channels, word = case
        p = output_probability(f, channels, word)
        err = error_probability(f, channels, word)
        assert math.isclose(err, 1.0 - p if f.evaluate(word) else p, abs_tol=1e-15)
        assert 0.0 <= err <= 1.0

    def test_reused_variable_is_one_observation(self) -> None:
        """``x0 & x0`` is ``x0``; the BernoulliBool operator would square fpr."""
        ch = [SetRates(fpr=0.3, fnr=0.2)]
        x0 = Var(0)
        assert error_profile(x0 & x0, ch) == pytest.approx(error_profile(x0, ch))
        assert error_profile(x0 | x0, ch) == pytest.approx(error_profile(x0, ch))
        # A contradiction and a tautology are never observed wrongly.
        assert all(e == 0.0 for e in error_profile(x0 & ~x0, ch).values())
        assert all(e == 0.0 for e in error_profile(x0 | ~x0, ch).values())

    def test_shared_variable_across_subtrees(self) -> None:
        f = (X[0] & X[1]) | (X[0] & X[2])
        for word in itertools.product((False, True), repeat=3):
            assert math.isclose(
                output_probability(f, CHANNELS, word),
                brute_force_output_probability(f, CHANNELS, word),
            )

    @given(st.data(), st.integers(min_value=1, max_value=5), st.booleans())
    @settings(max_examples=200, deadline=None)
    def test_shared_truth_operators_exact_for_read_once_trees(
        self, data: st.DataObject, n: int, truth: bool
    ) -> None:
        """``&`` and ``|`` are exact when every leaf observes the same bit."""
        f = data.draw(monotone_read_once(n))
        channels = data.draw(st.lists(channel_st, min_size=n, max_size=n))
        leaves = [BernoulliBool(value=truth, fpr=c.fpr, fnr=c.fnr) for c in channels]

        def fold(node: Formula) -> BernoulliBool:
            if isinstance(node, Var):
                return leaves[node.index]
            if isinstance(node, And):
                return fold(node.left) & fold(node.right)
            assert isinstance(node, Or)
            return fold(node.left) | fold(node.right)

        composed = fold(f)
        err = error_probability(f, channels, (truth,) * n)
        assert math.isclose(err, composed.fnr if truth else composed.fpr, abs_tol=1e-12)


# ---------------------------------------------------------------------------
# algebraic laws
# ---------------------------------------------------------------------------


class TestLaws:
    @given(st.lists(channel_st, min_size=2, max_size=2))
    def test_de_morgan(self, channels: list[SetRates]) -> None:
        a, b = variables(2)
        left = error_profile(~(a & b), channels)
        right = error_profile(~a | ~b, channels)
        assert left == pytest.approx(right, abs=1e-12)

    @given(st.lists(channel_st, min_size=2, max_size=2))
    def test_not_preserves_error_profile(self, channels: list[SetRates]) -> None:
        """Negating the output flips correct and observed values together."""
        a, b = variables(2)
        assert error_profile(~(a & b), channels) == pytest.approx(
            error_profile(a & b, channels), abs=1e-12
        )

    @given(channel_st)
    def test_single_variable_profile_is_the_channel(self, ch: SetRates) -> None:
        profile = error_profile(Var(0), [ch])
        assert profile[(False,)] == pytest.approx(ch.fpr)
        assert profile[(True,)] == pytest.approx(ch.fnr)

    def test_noiseless_channels_never_err(self) -> None:
        f = (X[0] & ~X[1]) | (X[1] & X[2])
        profile = error_profile(f, [SetRates()] * 3)
        assert all(e == 0.0 for e in profile.values())

    def test_inverting_channels_always_err_on_a_variable(self) -> None:
        profile = error_profile(Var(0), [SetRates(fpr=1.0, fnr=1.0)])
        assert all(e == 1.0 for e in profile.values())


# ---------------------------------------------------------------------------
# summaries: worst case and marginal
# ---------------------------------------------------------------------------


class TestSummaries:
    @given(st.lists(channel_st, min_size=2, max_size=2), st.floats(0.0, 1.0))
    def test_single_gate_marginal_matches_with_prior_methods(
        self, channels: list[SetRates], prior: float
    ) -> None:
        a, b = variables(2)
        b1 = BernoulliBool(value=False, fpr=channels[0].fpr, fnr=channels[0].fnr)
        b2 = BernoulliBool(value=False, fpr=channels[1].fpr, fnr=channels[1].fnr)
        m_and = marginal_rates(a & b, channels, priors=prior)
        ref_and = b1.and_with_prior(b2, prior)
        if prior < 1.0:
            assert m_and.fpr == pytest.approx(ref_and.fpr, abs=1e-12)
        if prior > 0.0:
            assert m_and.fnr == pytest.approx(ref_and.fnr, abs=1e-12)
        m_or = marginal_rates(a | b, channels, priors=prior)
        ref_or = b1.or_with_prior(b2, prior)
        if prior < 1.0:
            assert m_or.fpr == pytest.approx(ref_or.fpr, abs=1e-12)
        if prior > 0.0:
            assert m_or.fnr == pytest.approx(ref_or.fnr, abs=1e-12)

    def test_book_worked_example(self) -> None:
        """Book section 3.1: (0.10, 0.05) AND (0.08, 0.12) at pi = 0.5."""
        a, b = variables(2)
        ch = [SetRates(fpr=0.10, fnr=0.05), SetRates(fpr=0.08, fnr=0.12)]
        r = marginal_rates(a & b, ch, priors=0.5)
        assert r.fnr == pytest.approx(0.164)
        assert r.fpr == pytest.approx(0.043 / 0.75)

    @given(
        st.lists(channel_st, min_size=3, max_size=3),
        st.lists(st.floats(0.0, 1.0), min_size=3, max_size=3),
    )
    @settings(deadline=None)
    def test_marginal_lies_within_profile_range(
        self, channels: list[SetRates], priors: list[float]
    ) -> None:
        m = marginal_rates(COUNTEREXAMPLE, channels, priors)
        worst = worst_case_rates(COUNTEREXAMPLE, channels)
        assert m.fpr <= worst.fpr + 1e-12
        assert m.fnr <= worst.fnr + 1e-12

    def test_marginal_point_mass_prior_is_word_error(self) -> None:
        m = marginal_rates(COUNTEREXAMPLE, CHANNELS, priors=[0.0, 1.0, 0.0])
        assert m.fpr == pytest.approx(EXACT_010)
        assert m.fnr == 0.0  # the positive class has probability zero

    def test_empty_class_gives_zero_rate(self) -> None:
        x0 = Var(0)
        tautology = x0 | ~x0
        worst = worst_case_rates(tautology, [SetRates(fpr=0.3, fnr=0.2)])
        assert worst.fpr == 0.0


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_word_length_mismatch(self) -> None:
        with pytest.raises(ValueError, match="length"):
            error_probability(COUNTEREXAMPLE, CHANNELS, (False, True))

    def test_too_few_channels(self) -> None:
        with pytest.raises(ValueError, match="x2"):
            error_profile(COUNTEREXAMPLE, CHANNELS[:2])

    def test_channel_rates_out_of_range(self) -> None:
        class BadChannel:
            fpr = 1.5
            fnr = 0.0

        with pytest.raises(ValueError, match="channel 0"):
            output_probability(Var(0), [BadChannel()], (True,))

    def test_priors_validated(self) -> None:
        with pytest.raises(ValueError, match="priors"):
            marginal_rates(COUNTEREXAMPLE, CHANNELS, priors=[0.5, 0.5])
        with pytest.raises(ValueError, match="prior 1"):
            marginal_rates(COUNTEREXAMPLE, CHANNELS, priors=[0.5, 1.5, 0.5])

    def test_enumeration_limit(self) -> None:
        n = MAX_ENUMERATION_VARIABLES + 1
        channels = [SetRates()] * n
        with pytest.raises(ValueError, match="latent words"):
            error_profile(Var(0), channels)
        # A single latent word stays cheap at any size.
        assert error_probability(Var(0), channels, (False,) * n) == 0.0

    def test_repeated_variables_count_against_the_budget(self) -> None:
        def all_repeated(k: int) -> Formula:
            f: Formula = Var(0) & Var(0)
            for i in range(1, k):
                f = f & (Var(i) & Var(i))
            return f

        k = MAX_ENUMERATION_VARIABLES + 1
        with pytest.raises(ValueError, match="repeated variables"):
            error_probability(all_repeated(k), [SetRates()] * k, (True,) * k)
        # The profile functions spend n + r: 11 variables, all repeated, is 22.
        with pytest.raises(ValueError, match="latent words"):
            error_profile(all_repeated(11), [SetRates()] * 11)
        # Within budget, the same construction evaluates exactly.
        assert error_probability(all_repeated(4), [SetRates()] * 4, (True,) * 4) == 0.0

    def test_bernoulli_bool_is_a_rate_pair(self) -> None:
        b = BernoulliBool(value=True, fpr=0.1, fnr=0.2)
        assert error_profile(Var(0), [b]) == pytest.approx(
            {(False,): 0.1, (True,): 0.2}
        )
