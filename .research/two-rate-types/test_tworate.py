"""Executable evidence for the two-rate type rules.

Every comparison is exact (Fraction arithmetic).  The oracle computes the
true worst case over ALL latent valuations and ALL admissible joint error
laws (arbitrary within a source, product across sources), so "sound" means
rule >= oracle and "tight" means rule == oracle.
"""

from __future__ import annotations

import itertools
import sys
from fractions import Fraction as Q
from pathlib import Path

import pytest
from hypothesis import HealthCheck, assume, event, given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).parent))

from oracle import block_vertices, check_witness, desugar, error_at, worst_case  # noqa: E402
from tworate import (  # noqa: E402
    And, BoolT, Case, Const, Fst, If, Let, Not, Options, Or, Pair, Prim, Snd, Tag,
    TypeError_, Var, Xor, check, infer, no_false_negatives_syntactic, rule_and,
    single_prob,
)

RATES = [Q(0), Q(1, 100), Q(1, 20), Q(1, 10), Q(1, 4), Q(1, 3), Q(1, 2), Q(3, 5), Q(9, 10), Q(1)]
SMALL_RATES = [Q(0), Q(1, 100), Q(1, 20), Q(1, 10), Q(1, 4), Q(1, 3)]
SETTINGS = settings(max_examples=150, deadline=None,
                    suppress_health_check=[HealthCheck.too_slow])

rates = st.sampled_from(RATES)


def prim(i: int, eps: Q, omg: Q, source: str | None = None, atom: str | None = None) -> Prim:
    return Prim(f"p{i}", atom or f"x{i}", source or f"s{i}", eps, omg)


def sound(e, opt: Options = Options()) -> tuple[BoolT, Q, Q]:
    t = check(e, opt)
    eps, omg, _, _ = worst_case(e)
    assert t.eps >= eps, (e, t, eps)
    assert t.omg >= omg, (e, t, omg)
    return t, eps, omg


# ---------------------------------------------------------------------------
# 1. The pitfall from the brief: (b0 & b1) | b2 at latent word 010
# ---------------------------------------------------------------------------


def test_pitfall_example_exact_numbers():
    eps, omg = Q(2, 100), Q(10, 100)
    b = [prim(i, eps, omg) for i in range(3)]
    e = Or(And(b[0], b[1]), b[2])
    exact_010 = error_at(e, {"x0": False, "x1": True, "x2": False})
    assert exact_010 == Q(3764, 100000)  # 0.03764
    # naive: reuse the all-negative AND corner eps0*eps1 as the AND's FPR
    naive_and = eps * eps
    naive = naive_and + eps - naive_and * eps
    assert naive == Q(20392, 1000000)  # 0.020392
    assert naive < exact_010  # the naive summary is UNSOUND
    # the latent-supremum rule
    t = check(e)
    assert t.eps == Q(396, 10000)  # 0.0396 = 1 - (1 - 0.02)^2
    assert t.eps >= exact_010
    # with rates as upper bounds, 0.0396 is attained (b1 with actual FNR 0)
    eps_star, omg_star, w0, w1 = worst_case(e)
    assert eps_star == t.eps and omg_star == t.omg
    assert check_witness(e, w0) == t.eps
    # with rates fixed exactly, the worst case over latent words is 0.03764
    eps_exact_rates, _, _, _ = worst_case(e, exact_rates=True)
    assert eps_exact_rates == exact_010


def test_package_atom_and_is_the_unsound_corner():
    """bernoulli.atom.BernoulliBool.__and__ multiplies FPRs (shared-truth
    semantics).  Used on operands with different truths it under-reports."""
    atom = pytest.importorskip("bernoulli.atom")
    a = atom.BernoulliBool(value=False, fpr=0.02, fnr=0.10)
    b = atom.BernoulliBool(value=True, fpr=0.02, fnr=0.10)
    reported = (a & b).fpr
    p0, p1 = prim(0, Q(2, 100), Q(10, 100)), prim(1, Q(2, 100), Q(10, 100))
    true_err = error_at(And(p0, p1), {"x0": False, "x1": True})
    assert true_err == Q(18, 1000)
    assert reported == pytest.approx(0.0004)
    assert reported < float(true_err)
    # The two-rate rule is sound for this use.
    assert check(And(p0, p1)).eps == Q(2, 100)


# ---------------------------------------------------------------------------
# 2. Each rule is the best transformer (tight on fresh, distinct operands)
# ---------------------------------------------------------------------------


OPS = {
    "not": lambda a, b, c: Not(a),
    "and": lambda a, b, c: And(a, b),
    "or": lambda a, b, c: Or(a, b),
    "xor": lambda a, b, c: Xor(a, b),
    "if": lambda a, b, c: If(a, b, c),
}


@pytest.mark.parametrize("dependent", [False, True], ids=["I", "D"])
@pytest.mark.parametrize("op", sorted(OPS))
@settings(max_examples=60, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(rs=st.lists(rates, min_size=6, max_size=6))
def test_each_rule_is_best_transformer(op, dependent, rs):
    leaves = [prim(i, rs[2 * i], rs[2 * i + 1], source="s" if dependent else None)
              for i in range(3)]
    e = OPS[op](*leaves)
    t = check(e)
    eps, omg, w0, w1 = worst_case(e)
    assert (t.eps, t.omg) == (eps, omg), (op, rs, dependent, t, eps, omg)
    for w, target in ((w0, eps), (w1, omg)):
        if w is not None:
            assert check_witness(e, w) == target


# ---------------------------------------------------------------------------
# 3. Read-once exactness (Moore-style single-use theorem)
# ---------------------------------------------------------------------------


@st.composite
def read_once(draw, max_leaves: int, dependent: bool, allow_if: bool = True):
    """A random read-once, constant-free core expression."""
    counter = itertools.count()
    budget = [draw(st.integers(min(2, max_leaves), max_leaves))]

    def leaf():
        i = next(counter)
        return prim(i, draw(rates), draw(rates), source="s" if dependent else None)

    def build(n: int):
        if n == 1:
            e = leaf()
        else:
            ops = ["and", "or", "xor"] + (["if"] if allow_if and n >= 3 else [])
            op = draw(st.sampled_from(ops))
            if op == "if":
                k1 = draw(st.integers(1, n - 2))
                k2 = draw(st.integers(1, n - 1 - k1))
                k3 = n - k1 - k2
                e = If(build(k1), build(k2), build(k3))
            else:
                k = draw(st.integers(1, n - 1))
                e = {"and": And, "or": Or, "xor": Xor}[op](build(k), build(n - k))
        if draw(st.integers(0, 3)) == 0:
            e = Not(e)
        return e

    return build(budget[0])


@SETTINGS
@given(e=read_once(max_leaves=5, dependent=False))
def test_read_once_tight_independent(e):
    t = check(e)
    eps, omg, w0, w1 = worst_case(e)
    assert (t.eps, t.omg) == (eps, omg)
    for w, target in ((w0, eps), (w1, omg)):
        if w is not None:
            assert check_witness(e, w) == target


@SETTINGS
@given(e=read_once(max_leaves=3, dependent=True))
def test_read_once_tight_dependent(e):
    t = check(e)
    eps, omg, w0, w1 = worst_case(e)
    assert (t.eps, t.omg) == (eps, omg)
    for w, target in ((w0, eps), (w1, omg)):
        if w is not None:
            assert check_witness(e, w) == target


@settings(max_examples=60, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(e=read_once(max_leaves=4, dependent=True))
def test_read_once_tight_dependent_up_to_four_leaves(e):
    t = check(e)
    eps, omg, _, _ = worst_case(e)
    assert (t.eps, t.omg) == (eps, omg)


def test_read_once_tight_dependent_four_leaves():
    """Fixed four-leaf shapes in the single-source regime (slow oracle)."""
    r = [(Q(1, 10), Q(1, 20)), (Q(1, 4), Q(0)), (Q(1, 3), Q(1, 2)), (Q(1, 100), Q(9, 10))]
    p = [prim(i, *r[i], source="s") for i in range(4)]
    shapes = [
        Or(And(p[0], p[1]), And(p[2], p[3])),
        Xor(And(p[0], Not(p[1])), Or(p[2], p[3])),
        If(p[0], And(p[1], p[2]), Not(p[3])),
        And(And(p[0], p[1]), Or(p[2], p[3])),
    ]
    for e in shapes:
        t = check(e)
        eps, omg, _, _ = worst_case(e)
        assert (t.eps, t.omg) == (eps, omg), e


# ---------------------------------------------------------------------------
# 4. Soundness on arbitrary programs: sharing, constants, aliases, mixed sources
# ---------------------------------------------------------------------------


@st.composite
def general(draw, n_prims: int = 4, n_atoms: int = 3, n_sources: int = 2, depth: int = 3):
    pool = []
    for i in range(draw(st.integers(min(2, n_prims), n_prims))):
        atom = f"x{draw(st.integers(0, n_atoms - 1))}"
        src = f"s{draw(st.integers(0, n_sources - 1))}"
        pool.append(Prim(f"p{i}", atom, src, draw(rates), draw(rates)))

    def build(d: int):
        if d == 0 or (d < depth and draw(st.integers(0, 4)) == 0):
            if draw(st.integers(0, 9)) == 0:
                return Const(draw(st.booleans()))
            return draw(st.sampled_from(pool))
        op = draw(st.sampled_from(["not", "and", "or", "xor", "if"]))
        if op == "not":
            return Not(build(d - 1))
        if op == "if":
            return If(build(d - 1), build(d - 1), build(d - 1))
        return {"and": And, "or": Or, "xor": Xor}[op](build(d - 1), build(d - 1))

    return build(depth)


def _max_block(e) -> int:
    from oracle import prims as _prims
    counts: dict[str, int] = {}
    for p in _prims(desugar(e)):
        counts[p.source] = counts.get(p.source, 0) + 1
    return max(counts.values(), default=0)


def _record(e) -> None:
    from oracle import prims as _prims
    ps = _prims(desugar(e))
    assume(len(ps) >= 2)
    event(f"primitives={len(ps)}")
    event(f"shared-source={'yes' if len({p.source for p in ps}) < len(ps) else 'no'}")
    event(f"shared-atom={'yes' if len({p.atom for p in ps}) < len(ps) else 'no'}")


@settings(max_examples=1000, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(e=general(depth=4))
def test_soundness_general(e):
    assume(_max_block(e) <= 3)
    _record(e)
    sound(e)


@settings(max_examples=400, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(e=general(n_prims=5, n_atoms=3, n_sources=5, depth=4))
def test_soundness_general_mostly_independent(e):
    assume(_max_block(e) <= 2)
    _record(e)
    sound(e)


@SETTINGS
@given(e=general(), use_ind=st.booleans(), use_same=st.booleans())
def test_soundness_of_ablations(e, use_ind, use_same):
    """Dropping a refinement must keep the rules sound (and only looser)."""
    assume(_max_block(e) <= 3)
    opt = Options(use_independence=use_ind, use_same_truth=use_same)
    t_full = check(e)
    t_abl = check(e, opt)
    assert t_abl.eps >= t_full.eps and t_abl.omg >= t_full.omg
    sound(e, opt)


# ---------------------------------------------------------------------------
# 5. Provenance is necessary: forcing independence is unsound
# ---------------------------------------------------------------------------


def test_forced_independence_is_unsound_for_shared_source():
    # Two distinct answers from ONE source (e.g. two keys against one filter),
    # both truly positive.  Disjoint error events realize omg1 + omg2.
    a = Prim("a", "x", "s", Q(1, 10), Q(1, 5))
    b = Prim("b", "y", "s", Q(1, 10), Q(1, 5))
    e = And(a, b)
    eps, omg, _, w1 = worst_case(e)
    assert omg == Q(2, 5)
    assert check(e).omg == Q(2, 5)                     # provenance-aware: sound and tight
    forced = check(e, Options(force_independence=True))
    assert forced.omg == Q(9, 25) < omg                # 1-(4/5)^2 < 2/5: unsound
    assert check_witness(e, w1) == omg


def test_forced_independence_same_truth_is_unsound():
    # Two hash probes of one filter estimating the same fact: perfectly
    # correlated errors are admissible, so eps1*eps2 is unsound.
    a = Prim("a", "x", "s", Q(1, 10), Q(0))
    b = Prim("b", "x", "s", Q(1, 10), Q(0))
    e = And(a, b)
    eps, _, _, _ = worst_case(e)
    assert eps == Q(1, 10) == check(e).eps
    assert check(e, Options(force_independence=True)).eps == Q(1, 100) < eps


# ---------------------------------------------------------------------------
# 6. Equal-meaning refinement: amplification (Miller-Rabin, replicated filters)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("k", [1, 2, 3, 4])
def test_miller_rabin_amplification(k):
    rounds = [Prim(f"mr{i}", "prime_n", f"w{i}", Q(1, 4), Q(0)) for i in range(k)]
    e = rounds[0]
    for r in rounds[1:]:
        e = And(e, r)
    t = check(e)
    assert (t.eps, t.omg) == (Q(1, 4) ** k, Q(0))
    eps, omg, _, _ = worst_case(e)
    assert (eps, omg) == (t.eps, t.omg)                 # tight
    # without the equal-meaning refinement the rule cannot amplify
    assert check(e, Options(use_same_truth=False)).eps == Q(1, 4)
    # a single-probability system cannot amplify either: delta grows with k
    delta, _ = single_prob(e)
    assert delta == 1 - Q(3, 4) ** k


def test_same_truth_dependent_is_min():
    a = Prim("a", "x", "s", Q(1, 10), Q(1, 20))
    b = Prim("b", "x", "s", Q(1, 4), Q(1, 50))
    e = And(a, b)
    t = check(e)
    eps, omg, _, _ = worst_case(e)
    assert (t.eps, t.omg) == (eps, omg) == (Q(1, 10), Q(1, 20) + Q(1, 50))


# ---------------------------------------------------------------------------
# 7. Where sharing costs precision (sound but not tight)
# ---------------------------------------------------------------------------


def test_sharing_not_tight_but_sound():
    b = prim(0, Q(1, 10), Q(1, 5))
    t, eps, omg = sound(And(b, b))
    assert (eps, omg) == (Q(1, 10), Q(1, 5))
    assert (t.eps, t.omg) == (Q(1, 10), Q(2, 5))           # omega doubled
    t, eps, omg = sound(And(b, Not(b)))
    assert (eps, omg) == (0, 0)                             # constant exact value
    assert t.eps == Q(1, 5)


def test_if_rule_beats_its_boolean_encoding():
    c = prim(0, Q(1, 100), Q(1, 100))
    a = prim(1, Q(1, 10), Q(1, 20))
    b = prim(2, Q(1, 10), Q(1, 20))
    direct = check(If(c, a, b))
    encoded_expr = Or(And(c, a), And(Not(c), b))
    encoded = check(encoded_expr)
    eps, omg, _, _ = worst_case(If(c, a, b))
    assert (direct.eps, direct.omg) == (eps, omg)
    assert encoded.eps > direct.eps
    eps2, omg2, _, _ = worst_case(encoded_expr)
    assert (eps2, omg2) == (eps, omg)                       # same function...
    assert encoded.eps > eps2                               # ...looser bound


# ---------------------------------------------------------------------------
# 8. Strict refinement of the single-probability baseline
# ---------------------------------------------------------------------------


@settings(max_examples=400, deadline=None)
@given(e=general(n_prims=5, n_atoms=4, n_sources=3, depth=4))
def test_two_rate_refines_single_probability(e):
    t = check(e)
    delta, _ = single_prob(e)
    assert max(t.eps, t.omg) <= delta


def test_refinement_is_strict_for_one_sided_operands():
    a = prim(0, Q(1, 100), Q(0))
    b = prim(1, Q(1, 100), Q(0))
    t = check(And(a, b))
    delta, _ = single_prob(And(a, b))
    assert (t.eps, t.omg) == (Q(1, 100), Q(0))
    assert delta == Q(199, 10000)                           # about twice


# ---------------------------------------------------------------------------
# 9. One-sidedness: syntactic polarity <=> derived omega = 0 (and complete
#    for read-once programs)
# ---------------------------------------------------------------------------


one_sided_rates = st.sampled_from([Q(0), Q(0), Q(1, 10), Q(1, 4)])


@st.composite
def read_once_mixed(draw, max_leaves=4, dependent=False):
    counter = itertools.count()

    def leaf():
        i = next(counter)
        return prim(i, draw(one_sided_rates), draw(one_sided_rates),
                    source="s" if dependent else None)

    def build(n):
        if n == 1:
            e = leaf()
        else:
            op = draw(st.sampled_from(["and", "or", "xor"] + (["if"] if n >= 3 else [])))
            if op == "if":
                k1 = draw(st.integers(1, n - 2))
                k2 = draw(st.integers(1, n - 1 - k1))
                e = If(build(k1), build(k2), build(n - k1 - k2))
            else:
                k = draw(st.integers(1, n - 1))
                e = {"and": And, "or": Or, "xor": Xor}[op](build(k), build(n - k))
        return Not(e) if draw(st.integers(0, 3)) == 0 else e

    return build(draw(st.integers(1, max_leaves)))


@settings(max_examples=300, deadline=None)
@given(e=st.booleans().flatmap(lambda dep: read_once_mixed(max_leaves=4 if not dep else 3,
                                                           dependent=dep)))
def test_polarity_theorem(e):
    opt = Options(use_same_truth=False)
    t = check(e, opt)
    assert (t.omg == 0) == no_false_negatives_syntactic(e, True)
    assert (t.eps == 0) == no_false_negatives_syntactic(e, False)
    eps, omg, _, _ = worst_case(e)
    assert (omg == 0) == (t.omg == 0)                       # complete on read-once
    assert (eps == 0) == (t.eps == 0)


# ---------------------------------------------------------------------------
# 10. Let, products and sums
# ---------------------------------------------------------------------------


def test_let_sharing_matches_oracle():
    a = prim(0, Q(1, 10), Q(0))
    b = prim(1, Q(1, 20), Q(1, 50))
    e = Let("x", And(a, b), Or(Var("x"), Not(Var("x"))))
    t, eps, omg = sound(e)
    assert (eps, omg) == (0, 0)                              # tautology


def test_pairs_project_componentwise():
    a = prim(0, Q(1, 10), Q(0))
    b = prim(1, Q(1, 20), Q(1, 50))
    e = Let("p", Pair(a, b), And(Fst(Var("p")), Snd(Var("p"))))
    assert check(e) == check(And(a, b))
    sound(e)


def test_case_of_approximate_tag_is_the_if_rule():
    c = prim(0, Q(1, 100), Q(1, 50))
    l = prim(1, Q(1, 10), Q(0))
    r = prim(2, Q(0), Q(1, 10))
    s = Tag(c, Pair(l, Const(True)), r)
    e = Case(s, "u", And(Fst(Var("u")), Snd(Var("u"))), "w", Not(Var("w")))
    t = check(e)
    ref = check(If(c, And(l, Const(True)), Not(r)))
    assert (t.eps, t.omg) == (ref.eps, ref.omg)
    # branches: l = (1/10, 0); not r = (1/10, 0); all sources independent
    u = lambda a, b: a + b - a * b  # noqa: E731
    assert (t.eps, t.omg) == (max(u(Q(1, 10), Q(1, 50)), u(Q(1, 10), Q(1, 100))),
                              max(u(Q(0), Q(1, 50)), u(Q(0), Q(1, 100))))
    t2, eps, omg = sound(e)
    assert (t2.eps, t2.omg) == (eps, omg)                    # read-once: tight


def test_type_errors():
    with pytest.raises(TypeError_):
        check(Fst(prim(0, Q(0), Q(0))))
    with pytest.raises(TypeError_):
        check(Var("nope"))
    with pytest.raises(TypeError_):
        check(And(Pair(Const(True), Const(True)), Const(True)))
    with pytest.raises(TypeError_):
        check(Case(prim(0, Q(0), Q(0)), "a", Var("a"), "b", Var("b")))
    with pytest.raises(ValueError):
        Prim("p", "x", "s", Q(2), Q(0))


# ---------------------------------------------------------------------------
# 11. Hardness illustration: tight eps* = 0 iff the program is constant
# ---------------------------------------------------------------------------


def test_tight_zero_iff_constant():
    d = Q(1, 10)
    x = [prim(i, d, d) for i in range(3)]
    unsat = And(And(Or(x[0], x[1]), Not(x[0])), Not(x[1]))   # (x0|x1)&!x0&!x1
    sat = And(Or(x[0], x[1]), Not(x[0]))
    eps_u, omg_u, _, _ = worst_case(unsat)
    eps_s, omg_s, _, _ = worst_case(sat)
    assert eps_u == 0 and omg_u == 0
    assert eps_s > 0
    assert check(unsat).eps > 0                              # rules cannot see UNSAT


# ---------------------------------------------------------------------------
# 12. Oracle self-checks
# ---------------------------------------------------------------------------


def test_block_vertices_single_and_pair():
    assert set(block_vertices((Q(1, 4),))) == {(Q(1), Q(0)), (Q(3, 4), Q(1, 4))}
    vs = block_vertices((Q(1, 4), Q(1, 3)))
    for v in vs:
        assert sum(v) == 1 and min(v) >= 0
        assert v[2] + v[3] <= Q(1, 4) and v[1] + v[3] <= Q(1, 3)
    # the disjoint-errors vertex and the nested-errors vertex are both present
    assert (Q(5, 12), Q(1, 3), Q(1, 4), Q(0)) in vs
    assert (Q(2, 3), Q(1, 12), Q(0), Q(1, 4)) in vs


def test_infer_with_environment():
    env = {"z": BoolT(Q(1, 10), Q(0), frozenset({"s"}), ("atom", "z"))}
    t = infer(And(Var("z"), Var("z")), env)
    assert isinstance(t, BoolT) and t.eps == Q(1, 10)
    assert rule_and(env["z"], env["z"]).eps == Q(1, 10)


# ---------------------------------------------------------------------------
# 13. Case studies: rules match the exact oracle and refine the baseline
# ---------------------------------------------------------------------------


def test_case_studies():
    import casestudies

    rows = casestudies.run()
    assert len(rows) >= 10
    for r in rows:
        te, to = r["_t"]
        assert max(te, to) <= r["_single"], r["key"]
        if r["_ex"] is not None:
            assert (te, to) == tuple(r["_ex"]), r["key"]
    by = {r["key"]: r for r in rows}
    assert by["prefilter-same"]["_t"] == (0, 0)
    assert by["cascade-same"]["_t"] == (Q(1, 100) ** 3, 0)
    assert by["mr-alone"]["_t"] == (Q(1, 4) ** 10, 0)
    assert by["blocklist"]["_t"] == (0, Q(1, 100))
    assert by["xor-blooms"]["_t"][1] > 0
    assert "|" in casestudies.table(rows)


def test_single_prob_structural_forms_and_errors():
    a = prim(0, Q(1, 10), Q(0))
    b = prim(1, Q(1, 20), Q(1, 50))
    c = prim(2, Q(1, 100), Q(1, 100))
    e = Let("p", Pair(a, b),
            Case(Tag(c, Fst(Var("p")), Snd(Var("p"))), "u", Var("u"), "w", Not(Var("w"))))
    d, prov = single_prob(e)
    t = check(e)
    assert max(t.eps, t.omg) <= d and prov == frozenset({"s0", "s1", "s2"})
    assert d == single_prob(If(c, a, Not(b)))[0]
    with pytest.raises(TypeError_):
        single_prob(Pair(a, b))
    with pytest.raises(TypeError_):
        single_prob(object())  # type: ignore[arg-type]
    with pytest.raises(TypeError_):
        check(object())  # type: ignore[arg-type]
    with pytest.raises(TypeError_):
        no_false_negatives_syntactic(Let("x", a, Var("x")))
    with pytest.raises(TypeError):
        desugar(object())  # type: ignore[arg-type]
    from oracle import evaluate, prims as _prims
    with pytest.raises(TypeError):
        _prims(Pair(a, b))
    with pytest.raises(TypeError):
        evaluate(Pair(a, b), {})
    with pytest.raises(ValueError):
        _prims(And(a, Prim("p0", "x0", "s0", Q(1, 2), Q(0))))


@SETTINGS
@given(op=st.sampled_from(["and", "or", "xor"]), rs=st.lists(rates, min_size=4, max_size=4),
       dependent=st.booleans())
def test_same_meaning_rules_are_best_transformers(op, rs, dependent):
    """Two answers estimating the SAME latent fact (equal erasures)."""
    a = Prim("a", "x", "s" if dependent else "sa", rs[0], rs[1])
    b = Prim("b", "x", "s" if dependent else "sb", rs[2], rs[3])
    e = {"and": And, "or": Or, "xor": Xor}[op](a, b)
    t = check(e)
    eps, omg, _, _ = worst_case(e)
    assert (t.eps, t.omg) == (eps, omg), (op, rs, dependent)


def test_xor_keeps_some_asymmetry_but_not_one_sidedness():
    """Refines the brief's parity claim: the tight XOR pair is per-class,
    tighter than the symmetric 1/2(1 - prod(1 - 2 q_i)) collapse."""
    a = prim(0, Q(1, 100), Q(1, 10))
    b = prim(1, Q(1, 100), Q(1, 10))
    t = check(Xor(a, b))
    q = Q(1, 10)
    collapse = (1 - (1 - 2 * q) * (1 - 2 * q)) / 2
    assert t.eps == collapse == Q(18, 100)          # FPR driven by the two FNRs
    assert t.omg == Q(1, 100) + Q(1, 10) - 2 * Q(1, 1000) < collapse
    assert worst_case(Xor(a, b))[:2] == (t.eps, t.omg)
    one_sided = check(Xor(prim(0, Q(1, 100), Q(0)), prim(1, Q(1, 100), Q(0))))
    assert one_sided.omg == Q(1, 100) > 0           # one-sidedness destroyed


def test_independence_never_helps_and_fpr_across_different_facts():
    a, b = prim(0, Q(1, 10), Q(1, 5)), prim(1, Q(1, 4), Q(1, 3))
    ind = check(And(a, b))
    dep = check(And(a, b), Options(use_independence=False))
    assert ind.eps == dep.eps == Q(1, 4)
    assert ind.omg < dep.omg


def test_mixed_source_structure_is_sound_but_not_tight():
    """Open problem: read-once, but sources only partially shared.  The
    top AND sees overlapping provenance and must use the union bound, yet b
    (own source) cannot be anti-correlated with c, so the bound is loose."""
    a = Prim("a", "xa", "s1", Q(1, 10), Q(1, 5))
    b = Prim("b", "xb", "s2", Q(1, 10), Q(1, 5))
    c = Prim("c", "xc", "s1", Q(1, 10), Q(1, 5))
    e = And(And(a, b), c)
    t, eps, omg = sound(e)
    assert t.omg == Q(9, 25) + Q(1, 5)              # (1-(4/5)^2) + 1/5 = 0.56
    assert omg < t.omg
    assert omg == Q(13, 25)                          # 0.52: exact worst case


# ---------------------------------------------------------------------------
# 14. Review-driven additions: IF-equal rule, provenance plumbing, structured
#     programs with an independent evaluator
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("dependent", [False, True], ids=["I", "D"])
@settings(max_examples=100, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(rs=st.lists(rates, min_size=6, max_size=6))
def test_if_equal_rule_is_best_transformer(dependent, rs):
    c = Prim("c", "xc", "s" if dependent else "sc", rs[0], rs[1])
    a = Prim("a", "x", "s" if dependent else "sa", rs[2], rs[3])
    b = Prim("b", "x", "s" if dependent else "sb", rs[4], rs[5])
    e = If(c, a, b)
    t = check(e)
    eps, omg, _, _ = worst_case(e)
    assert (t.eps, t.omg) == (eps, omg), (rs, dependent)
    # and it refines the default IF rule
    t0 = check(e, Options(use_same_truth=False))
    assert t.eps <= t0.eps and t.omg <= t0.omg


def test_if_equal_review_example():
    c = prim(0, Q(1, 2), Q(1, 2))
    a = Prim("a", "x", "sa", Q(1, 10), Q(1, 10))
    b = Prim("b", "x", "sb", Q(1, 10), Q(1, 10))
    assert check(If(c, a, b)).eps == Q(1, 10) == worst_case(If(c, a, b))[0]
    assert check(If(c, a, b), Options(use_same_truth=False)).eps == Q(11, 20)


GRID = [Q(0), Q(1, 10), Q(1, 5), Q(1, 2), Q(9, 10)]


def test_if_output_carries_condition_provenance():
    """Kills the 'drop c from IF provenance' mutant: c and d share a source."""
    for r in GRID:
        c = Prim("c", "xc", "s", r, r)
        d = Prim("d", "xd", "s", r, r)
        sound(And(If(c, Const(True), Const(False)), d))
        sound(Or(If(c, d, Const(False)), Prim("f", "xf", "s", r, r)))


def test_if_equal_erasure_is_the_branch_erasure():
    """Kills the 'equal-branch IF takes the condition's erasure' mutant."""
    for rc, ra in itertools.product(GRID, repeat=2):
        c = Prim("c", "xc", "sc", rc, rc)
        a = Prim("a", "xa", "sa", ra, ra)
        c2 = Prim("c2", "xc", "sc2", rc, rc)
        sound(And(If(c, a, a), c2))
        sound(Or(If(c, a, a), c2))


def test_exact_primitives_carry_no_provenance():
    """An exact primitive sharing a source name must not block independence."""
    x = Prim("xe", "xx", "s", Q(0), Q(0))
    a = Prim("a", "xa", "s2", Q(1, 10), Q(1, 5))
    b = Prim("b", "xb", "s", Q(1, 10), Q(1, 5))
    e = And(Or(x, a), b)
    t = check(e)
    assert (t.eps, t.omg) == worst_case(e)[:2]


def eval_direct(e, env, val):
    """Independent big-step evaluator over the FULL syntax (no desugaring)."""
    if isinstance(e, Prim):
        return val[e.name]
    if isinstance(e, Const):
        return e.value
    if isinstance(e, Var):
        return env[e.name]
    if isinstance(e, Let):
        return eval_direct(e.body, {**env, e.name: eval_direct(e.bound, env, val)}, val)
    if isinstance(e, Pair):
        return (eval_direct(e.l, env, val), eval_direct(e.r, env, val))
    if isinstance(e, Fst):
        return eval_direct(e.e, env, val)[0]
    if isinstance(e, Snd):
        return eval_direct(e.e, env, val)[1]
    if isinstance(e, Tag):
        return ("tag", eval_direct(e.c, env, val), eval_direct(e.l, env, val),
                eval_direct(e.r, env, val))
    if isinstance(e, Case):
        _, tag, lv, rv = eval_direct(e.scrut, env, val)
        if tag:
            return eval_direct(e.lbody, {**env, e.lname: lv}, val)
        return eval_direct(e.rbody, {**env, e.rname: rv}, val)
    if isinstance(e, Not):
        return not eval_direct(e.e, env, val)
    if isinstance(e, And):
        return eval_direct(e.l, env, val) and eval_direct(e.r, env, val)
    if isinstance(e, Or):
        return eval_direct(e.l, env, val) or eval_direct(e.r, env, val)
    if isinstance(e, Xor):
        return eval_direct(e.l, env, val) != eval_direct(e.r, env, val)
    if isinstance(e, If):
        return eval_direct(e.t if eval_direct(e.c, env, val) else e.f, env, val)
    raise TypeError(e)


@st.composite
def structured(draw, n_prims=4, n_atoms=3, n_sources=2, depth=3):
    """Random programs using Let (with reuse), Pair/Fst/Snd and Tag/Case."""
    pool = [Prim(f"p{i}", f"x{draw(st.integers(0, n_atoms - 1))}",
                 f"s{draw(st.integers(0, n_sources - 1))}", draw(rates), draw(rates))
            for i in range(draw(st.integers(2, n_prims)))]
    names = itertools.count()
    binop = st.sampled_from([And, Or, Xor])

    def build(d):
        if d == 0:
            return draw(st.sampled_from(pool)) if draw(st.integers(0, 9)) else Const(draw(st.booleans()))
        k = draw(st.sampled_from(["op", "not", "if", "let", "pair", "case", "leaf"]))
        if k == "leaf":
            return draw(st.sampled_from(pool))
        if k == "not":
            return Not(build(d - 1))
        if k == "op":
            return draw(binop)(build(d - 1), build(d - 1))
        if k == "if":
            return If(build(d - 1), build(d - 1), build(d - 1))
        n = f"v{next(names)}"
        if k == "let":
            body = draw(binop)(Var(n), draw(st.sampled_from([Var(n), build(d - 1)])))
            return Let(n, build(d - 1), body)
        if k == "pair":
            return Let(n, Pair(build(d - 1), build(d - 1)),
                       draw(binop)(Fst(Var(n)), Snd(Var(n))))
        m = f"w{next(names)}"
        scrut = Tag(build(d - 1), Pair(build(d - 1), build(d - 1)), build(d - 1))
        return Case(scrut, n, draw(binop)(Fst(Var(n)), Snd(Var(n))),
                    m, Not(Var(m)) if draw(st.booleans()) else draw(binop)(Var(m), build(d - 1)))

    return build(depth)


@settings(max_examples=300, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(e=structured(), seed=st.integers(0, 2 ** 16))
def test_desugaring_matches_independent_evaluator(e, seed):
    from oracle import evaluate as core_eval, prims as _prims
    core = desugar(e)
    ps = _prims(core)
    import random
    rng = random.Random(seed)
    for _ in range(4):
        val = {p.name: rng.random() < 0.5 for p in ps}
        assert core_eval(core, {p: val[p.name] for p in ps}) == eval_direct(e, {}, val)


@settings(max_examples=400, deadline=None, suppress_health_check=[HealthCheck.too_slow])
@given(e=structured())
def test_soundness_structured_programs(e):
    assume(_max_block(e) <= 3)
    _record(e)
    sound(e)
    delta, _ = single_prob(e)
    t = check(e)
    assert max(t.eps, t.omg) <= delta
