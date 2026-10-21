"""Two-rate (FPR, FNR) types for approximate Boolean programs: the checker.

A judgment ``e : Bool[eps, omg] ! R`` means: for EVERY latent valuation v of
the exact facts, if the exact program's value at v is 0 then
P(observed = 1 | v) <= eps, and if it is 1 then P(observed = 0 | v) <= omg.
``R`` is the provenance: the set of random sources the observed value can
depend on.  The joint law of the observations is arbitrary within a source
and a product across distinct sources (sources are independent seeds).

The rules below are closed forms.  ``oracle.py`` recomputes the same
quantities from first principles (truth tables, vertex enumeration of the
admissible error polytopes); the test-suite compares the two.

Arithmetic is exact (``fractions.Fraction``) throughout.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Union

Q = Fraction
ZERO = Q(0)
ONE = Q(1)


# ---------------------------------------------------------------------------
# Syntax
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Prim:
    """An approximate primitive occurrence: one frozen random bit.

    ``atom`` names its exact meaning (the latent fact it estimates);
    ``source`` names the random seed it draws on; ``eps``/``omg`` are its
    declared conditional rates.  Two ``Prim`` values that compare equal are
    the same bit (re-reading a frozen answer); distinct names are distinct
    bits that may still share a source (and hence be dependent).
    """

    name: str
    atom: str
    source: str
    eps: Q
    omg: Q

    def __post_init__(self) -> None:
        for r in (self.eps, self.omg):
            if not (ZERO <= r <= ONE):
                raise ValueError(f"rate out of [0,1]: {r}")


@dataclass(frozen=True)
class Const:
    value: bool


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Not:
    e: "Expr"


@dataclass(frozen=True)
class And:
    l: "Expr"
    r: "Expr"


@dataclass(frozen=True)
class Or:
    l: "Expr"
    r: "Expr"


@dataclass(frozen=True)
class Xor:
    l: "Expr"
    r: "Expr"


@dataclass(frozen=True)
class If:
    c: "Expr"
    t: "Expr"
    f: "Expr"


@dataclass(frozen=True)
class Let:
    name: str
    bound: "Expr"
    body: "Expr"


@dataclass(frozen=True)
class Pair:
    l: "Expr"
    r: "Expr"


@dataclass(frozen=True)
class Fst:
    e: "Expr"


@dataclass(frozen=True)
class Snd:
    e: "Expr"


@dataclass(frozen=True)
class Tag:
    """``Tag(c, l, r)`` is ``inl l`` when ``c`` reads 1, else ``inr r``.

    The tag is approximate exactly when ``c`` is.  An exact injection is
    ``Tag(Const(True), l, r)`` (``r`` irrelevant).  Both payload slots are
    always present, which is what makes ``Case`` a total multiplexer.
    """

    c: "Expr"
    l: "Expr"
    r: "Expr"


@dataclass(frozen=True)
class Case:
    scrut: "Expr"
    lname: str
    lbody: "Expr"
    rname: str
    rbody: "Expr"


Expr = Union[Prim, Const, Var, Not, And, Or, Xor, If, Let, Pair, Fst, Snd, Tag, Case]


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


# Erasures (exact meanings) are hashable nested tuples.
Erasure = tuple


@dataclass(frozen=True)
class BoolT:
    eps: Q
    omg: Q
    prov: frozenset[str] = field(default_factory=frozenset)
    erasure: Erasure = ("?",)

    @property
    def delta(self) -> Q:
        """Symmetric collapse: the single error probability this type implies."""
        return max(self.eps, self.omg)


@dataclass(frozen=True)
class ProdT:
    l: "Type"
    r: "Type"


@dataclass(frozen=True)
class SumT:
    tag: BoolT
    l: "Type"
    r: "Type"


Type = Union[BoolT, ProdT, SumT]


class TypeError_(Exception):
    pass


# ---------------------------------------------------------------------------
# Rate combinators (the only arithmetic the rules use)
# ---------------------------------------------------------------------------


def union_dep(a: Q, b: Q) -> Q:
    """Union bound, valid under arbitrary dependence (capped at 1)."""
    return min(ONE, a + b)


def union_ind(a: Q, b: Q) -> Q:
    """P(A or B) for independent A, B at their maximal rates."""
    return a + b - a * b


def meet_dep(a: Q, b: Q) -> Q:
    """Upper Frechet bound on P(A and B) under arbitrary dependence."""
    return min(a, b)


def meet_ind(a: Q, b: Q) -> Q:
    return a * b


def xor_dep(a: Q, b: Q) -> Q:
    """sup P(I1 != I2) over couplings with P(I1)<=a, P(I2)<=b."""
    return min(ONE, a + b)


def xor_ind(a: Q, b: Q) -> Q:
    """sup over the rate box of r1 + r2 - 2 r1 r2 (bilinear: max at corners)."""
    return max(a, b, a + b - 2 * a * b)


def _indep(t1: BoolT, t2: BoolT) -> bool:
    """Independence is certified exactly when provenances are disjoint."""
    return not (t1.prov & t2.prov)


# ---------------------------------------------------------------------------
# The rules
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Options:
    """Switches used by the tests to ablate refinements.

    ``use_independence``: apply product tightenings when provenance is disjoint.
    ``use_same_truth``: apply the equal-erasure refinement at AND/OR/XOR.
    ``force_independence``: UNSOUND ablation, treats every pair as independent
    (used only to exhibit why provenance tracking is needed).
    """

    use_independence: bool = True
    use_same_truth: bool = True
    force_independence: bool = False


DEFAULT = Options()


def _is_ind(t1: BoolT, t2: BoolT, opt: Options) -> bool:
    if opt.force_independence:
        return True
    return opt.use_independence and _indep(t1, t2)


def _neg(er: Erasure) -> Erasure:
    """Exact meaning of NOT, normalized by double negation and constants."""
    if er[0] == "not":
        return er[1]
    if er[0] == "const":
        return ("const", not er[1])
    return ("not", er)


def rule_not(t: BoolT) -> BoolT:
    return BoolT(t.omg, t.eps, t.prov, _neg(t.erasure))


def rule_and(t1: BoolT, t2: BoolT, opt: Options = DEFAULT) -> BoolT:
    ind = _is_ind(t1, t2, opt)
    union = union_ind if ind else union_dep
    meet = meet_ind if ind else meet_dep
    same = opt.use_same_truth and t1.erasure == t2.erasure
    # Feasible exact pairs: {00,01,10,11}, or {00,11} when meanings coincide.
    eps = meet(t1.eps, t2.eps) if same else max(t1.eps, t2.eps)
    omg = union(t1.omg, t2.omg)
    # Idempotence of the exact meaning keeps chains of equal meanings
    # recognizable: exact(a & a') = exact(a) when exact(a) = exact(a').
    er = t1.erasure if same else ("and", t1.erasure, t2.erasure)
    return BoolT(eps, omg, t1.prov | t2.prov, er)


def rule_or(t1: BoolT, t2: BoolT, opt: Options = DEFAULT) -> BoolT:
    # De Morgan: OR = NOT(AND(NOT, NOT)); the erasure is kept as "or".
    dual = rule_and(rule_not(t1), rule_not(t2), opt)
    same = opt.use_same_truth and t1.erasure == t2.erasure
    er = t1.erasure if same else ("or", t1.erasure, t2.erasure)
    return BoolT(dual.omg, dual.eps, dual.prov, er)


def rule_xor(t1: BoolT, t2: BoolT, opt: Options = DEFAULT) -> BoolT:
    ind = _is_ind(t1, t2, opt)
    x = xor_ind if ind else xor_dep
    same = opt.use_same_truth and t1.erasure == t2.erasure
    # Output 0 at exact pairs 00 and 11; output 1 at 01 and 10.
    eps = max(x(t1.eps, t2.eps), x(t1.omg, t2.omg))
    omg = ZERO if same else max(x(t1.eps, t2.omg), x(t1.omg, t2.eps))
    er = ("const", False) if same else ("xor", t1.erasure, t2.erasure)
    return BoolT(eps, omg, t1.prov | t2.prov, er)


def rule_if(tc: BoolT, t1: BoolT, t2: BoolT, opt: Options = DEFAULT) -> BoolT:
    """Multiplexer.  Worst cases: the taken branch errs, or the condition
    flips and the other branch disagrees.  Only c must be independent of the
    branch it is combined with; the branches may share provenance."""
    u1 = union_ind if _is_ind(tc, t1, opt) else union_dep
    u2 = union_ind if _is_ind(tc, t2, opt) else union_dep
    eps = max(u1(t1.eps, tc.omg), u2(t2.eps, tc.eps))
    omg = max(u1(t1.omg, tc.omg), u2(t2.omg, tc.eps))
    same = opt.use_same_truth and t1.erasure == t2.erasure
    if same:
        # IF-equal: both branches estimate the same fact, so the exact value
        # ignores c.  With exact condition value 1 the error event is
        # (c reads 1 & branch-1 errs) or (c flips & branch-2 errs).
        both_ind = _is_ind(tc, t1, opt) and _is_ind(tc, t2, opt)
        eps = min(eps, _if_equal(t1.eps, t2.eps, tc, both_ind))
        omg = min(omg, _if_equal(t1.omg, t2.omg, tc, both_ind))
    er = t1.erasure if same else ("if", tc.erasure, t1.erasure, t2.erasure)
    return BoolT(eps, omg, tc.prov | t1.prov | t2.prov, er)


def _if_equal(r1: Q, r2: Q, tc: BoolT, both_ind: bool) -> Q:
    """Worst error of `if c then e1 else e2` when e1, e2 have equal meaning,
    for one output class with branch rates r1, r2.  Exact c = 1 flips to the
    else-branch with rate omg_c; exact c = 0 flips to the then-branch with
    rate eps_c."""
    if both_ind:
        # (1 - rc) r1 + rc r2, maximized over the rate box
        return max(r1 + tc.omg * max(ZERO, r2 - r1), r2 + tc.eps * max(ZERO, r1 - r2))
    # union bound with the flip mass charged only up to the other branch's error
    return max(union_dep(r1, min(tc.omg, r2)), union_dep(r2, min(tc.eps, r1)))


def prim_type(p: Prim) -> BoolT:
    exact = p.eps == 0 and p.omg == 0
    prov = frozenset() if exact else frozenset({p.source})
    return BoolT(p.eps, p.omg, prov, ("atom", p.atom))


def infer(e: Expr, env: dict[str, Type] | None = None, opt: Options = DEFAULT) -> Type:
    env = {} if env is None else env
    if isinstance(e, Prim):
        return prim_type(e)
    if isinstance(e, Const):
        return BoolT(ZERO, ZERO, frozenset(), ("const", e.value))
    if isinstance(e, Var):
        if e.name not in env:
            raise TypeError_(f"unbound variable {e.name}")
        return env[e.name]
    if isinstance(e, Let):
        tb = infer(e.bound, env, opt)
        return infer(e.body, {**env, e.name: tb}, opt)
    if isinstance(e, Pair):
        return ProdT(infer(e.l, env, opt), infer(e.r, env, opt))
    if isinstance(e, (Fst, Snd)):
        t = infer(e.e, env, opt)
        if not isinstance(t, ProdT):
            raise TypeError_("projection of a non-pair")
        return t.l if isinstance(e, Fst) else t.r
    if isinstance(e, Tag):
        return SumT(_bool(infer(e.c, env, opt)), infer(e.l, env, opt), infer(e.r, env, opt))
    if isinstance(e, Case):
        ts = infer(e.scrut, env, opt)
        if not isinstance(ts, SumT):
            raise TypeError_("case of a non-sum")
        t1 = _bool(infer(e.lbody, {**env, e.lname: ts.l}, opt))
        t2 = _bool(infer(e.rbody, {**env, e.rname: ts.r}, opt))
        return rule_if(ts.tag, t1, t2, opt)
    if isinstance(e, Not):
        return rule_not(_bool(infer(e.e, env, opt)))
    if isinstance(e, (And, Or, Xor)):
        t1 = _bool(infer(e.l, env, opt))
        t2 = _bool(infer(e.r, env, opt))
        rule = {And: rule_and, Or: rule_or, Xor: rule_xor}[type(e)]
        return rule(t1, t2, opt)
    if isinstance(e, If):
        return rule_if(
            _bool(infer(e.c, env, opt)),
            _bool(infer(e.t, env, opt)),
            _bool(infer(e.f, env, opt)),
            opt,
        )
    raise TypeError_(f"unknown expression {e!r}")


def _bool(t: Type) -> BoolT:
    if not isinstance(t, BoolT):
        raise TypeError_(f"expected Bool, got {t!r}")
    return t


def check(e: Expr, opt: Options = DEFAULT) -> BoolT:
    return _bool(infer(e, None, opt))


# ---------------------------------------------------------------------------
# Single-probability baseline (Decaf-style)
# ---------------------------------------------------------------------------


def single_prob(e: Expr, env: dict[str, object] | None = None, independent_product: bool = True,
                provenance: bool = True) -> tuple[Q, frozenset[str]]:
    """Single error probability delta with P(observed != exact | v) <= delta.

    ``independent_product=True`` mirrors Decaf's multiplicative rule
    p = p_a * p_b (i.e. delta = 1-(1-d1)(1-d2)); with ``provenance=True`` that
    product is applied only when provenance is disjoint (otherwise the union
    bound), which is the like-for-like sound baseline.  With
    ``provenance=False`` the product is applied unconditionally, as Decaf does.
    Returns (delta, provenance).
    """
    env = {} if env is None else env

    def comb(a: Q, ra: frozenset[str], b: Q, rb: frozenset[str]) -> Q:
        ind = independent_product and (not provenance or not (ra & rb))
        return union_ind(a, b) if ind else union_dep(a, b)

    def go(e: Expr, env: dict) -> tuple[object, ...]:
        if isinstance(e, Prim):
            t = prim_type(e)
            return ("b", t.delta, t.prov)
        if isinstance(e, Const):
            return ("b", ZERO, frozenset())
        if isinstance(e, Var):
            return env[e.name]
        if isinstance(e, Let):
            return go(e.body, {**env, e.name: go(e.bound, env)})
        if isinstance(e, Pair):
            return ("p", go(e.l, env), go(e.r, env))
        if isinstance(e, Fst):
            return go(e.e, env)[1]
        if isinstance(e, Snd):
            return go(e.e, env)[2]
        if isinstance(e, Tag):
            return ("s", go(e.c, env), go(e.l, env), go(e.r, env))
        if isinstance(e, Case):
            s = go(e.scrut, env)
            _, c, l, r = s
            b1 = go(e.lbody, {**env, e.lname: l})
            b2 = go(e.rbody, {**env, e.rname: r})
            return _if(c, b1, b2)
        if isinstance(e, Not):
            return go(e.e, env)
        if isinstance(e, (And, Or, Xor)):
            _, a, ra = go(e.l, env)
            _, b, rb = go(e.r, env)
            return ("b", comb(a, ra, b, rb), ra | rb)
        if isinstance(e, If):
            return _if(go(e.c, env), go(e.t, env), go(e.f, env))
        raise TypeError_(f"unknown expression {e!r}")

    def _if(c: tuple, b1: tuple, b2: tuple) -> tuple:
        _, dc, rc = c
        _, d1, r1 = b1
        _, d2, r2 = b2
        # error <= P(c wrong) combined with P(taken branch wrong)
        v = max(comb(dc, rc, d1, r1), comb(dc, rc, d2, r2))
        return ("b", v, rc | r1 | r2)

    out = go(e, env)
    if out[0] != "b":
        raise TypeError_("single_prob expects a Boolean expression")
    return out[1], out[2]


# ---------------------------------------------------------------------------
# One-sidedness (polarity) predicate, stated syntactically
# ---------------------------------------------------------------------------


def no_false_negatives_syntactic(e: Expr, positive: bool = True) -> bool:
    """Polarity condition for a Boolean core expression (no Let/Var/sums).

    True iff every primitive under an even number of negations has omg = 0,
    every primitive under an odd number has eps = 0, and every primitive
    under a XOR or inside an if-condition is exact; if-branches inherit the
    polarity of the if.  Used to test the polarity theorem (with the
    equal-meaning rules disabled).
    """

    def ok(e: Expr, pos: bool) -> bool:
        # returns True iff the derived rate for the class 'pos' is zero:
        # pos=True  -> derived omg == 0 ; pos=False -> derived eps == 0
        if isinstance(e, Prim):
            return (e.omg == 0) if pos else (e.eps == 0)
        if isinstance(e, Const):
            return True
        if isinstance(e, Not):
            return ok(e.e, not pos)
        if isinstance(e, (And, Or)):
            return ok(e.l, pos) and ok(e.r, pos)
        if isinstance(e, Xor):
            return all(ok(x, p) for x in (e.l, e.r) for p in (True, False))
        if isinstance(e, If):
            return (ok(e.c, True) and ok(e.c, False) and ok(e.t, pos) and ok(e.f, pos))
        raise TypeError_(f"core expression expected, got {e!r}")

    return ok(e, positive)
