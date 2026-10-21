"""Exact semantics and exact worst-case error for small instances.

Independent of the closed-form rules in ``tworate.py``.  For an expression e
(after desugaring Let/Pair/Tag/Case into the Boolean core) we compute

    eps*(e) = sup_v  sup_M  P_M(obs(e) = 1 | v)   over v with exact(e)(v) = 0
    omg*(e) = sup_v  sup_M  P_M(obs(e) = 0 | v)   over v with exact(e)(v) = 1

where M ranges over ALL admissible joint laws of the primitives' error
indicators at v: arbitrary within a source, a product across sources, and
with marginals P(I_i = 1) <= b_i(v)  (b_i = eps_i if the primitive's exact
value is 0, omg_i if it is 1).

The objective is linear in each source block's law, so the supremum over the
product of block polytopes is attained at a product of block vertices.  Block
vertices are enumerated exactly (basic feasible solutions, Fraction
arithmetic).  Everything is exact; nothing is sampled.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache

from tworate import (
    And, Case, Const, Expr, Fst, If, Let, Not, Or, Pair, Prim, Snd, Tag, Var, Xor,
)

Q = Fraction


# ---------------------------------------------------------------------------
# Desugaring to the Boolean core
# ---------------------------------------------------------------------------


def desugar(e: Expr, env: dict[str, Expr] | None = None) -> Expr:
    """Inline Let (sharing is preserved: the same Prim objects are reused),
    reduce projections, and turn Case-of-Tag into If."""
    env = {} if env is None else env
    if isinstance(e, (Prim, Const)):
        return e
    if isinstance(e, Var):
        return env[e.name]
    if isinstance(e, Let):
        return desugar(e.body, {**env, e.name: desugar(e.bound, env)})
    if isinstance(e, Pair):
        return Pair(desugar(e.l, env), desugar(e.r, env))
    if isinstance(e, Fst):
        p = desugar(e.e, env)
        assert isinstance(p, Pair)
        return p.l
    if isinstance(e, Snd):
        p = desugar(e.e, env)
        assert isinstance(p, Pair)
        return p.r
    if isinstance(e, Tag):
        return Tag(desugar(e.c, env), desugar(e.l, env), desugar(e.r, env))
    if isinstance(e, Case):
        s = desugar(e.scrut, env)
        assert isinstance(s, Tag)
        b1 = desugar(e.lbody, {**env, e.lname: s.l})
        b2 = desugar(e.rbody, {**env, e.rname: s.r})
        return If(s.c, b1, b2)
    if isinstance(e, Not):
        return Not(desugar(e.e, env))
    if isinstance(e, (And, Or, Xor)):
        return type(e)(desugar(e.l, env), desugar(e.r, env))
    if isinstance(e, If):
        return If(desugar(e.c, env), desugar(e.t, env), desugar(e.f, env))
    raise TypeError(f"unknown expression {e!r}")


def prims(e: Expr) -> list[Prim]:
    """Distinct primitive bits of a core expression, in first-occurrence order."""
    seen: dict[Prim, None] = {}

    def go(e: Expr) -> None:
        if isinstance(e, Prim):
            seen.setdefault(e, None)
        elif isinstance(e, Const):
            pass
        elif isinstance(e, Not):
            go(e.e)
        elif isinstance(e, (And, Or, Xor)):
            go(e.l)
            go(e.r)
        elif isinstance(e, If):
            go(e.c)
            go(e.t)
            go(e.f)
        else:
            raise TypeError(f"core expression expected, got {e!r}")

    go(e)
    names: dict[str, Prim] = {}
    for p in seen:
        if p.name in names and names[p.name] != p:
            raise ValueError(f"inconsistent declarations for primitive {p.name}")
        names[p.name] = p
    return list(seen)


def evaluate(e: Expr, val: dict[Prim, bool]) -> bool:
    """Evaluate a core expression given a value for every primitive."""
    if isinstance(e, Prim):
        return val[e]
    if isinstance(e, Const):
        return e.value
    if isinstance(e, Not):
        return not evaluate(e.e, val)
    if isinstance(e, And):
        return evaluate(e.l, val) and evaluate(e.r, val)
    if isinstance(e, Or):
        return evaluate(e.l, val) or evaluate(e.r, val)
    if isinstance(e, Xor):
        return evaluate(e.l, val) != evaluate(e.r, val)
    if isinstance(e, If):
        return evaluate(e.t, val) if evaluate(e.c, val) else evaluate(e.f, val)
    raise TypeError(f"core expression expected, got {e!r}")


# ---------------------------------------------------------------------------
# Admissible block polytopes
# ---------------------------------------------------------------------------


def _solve(rows: list[list[Q]], rhs: list[Q]) -> list[Q] | None:
    """Exact Gaussian elimination for a square system; None if singular."""
    n = len(rows)
    a = [row[:] + [r] for row, r in zip(rows, rhs)]
    for col in range(n):
        piv = next((i for i in range(col, n) if a[i][col] != 0), None)
        if piv is None:
            return None
        a[col], a[piv] = a[piv], a[col]
        p = a[col][col]
        a[col] = [x / p for x in a[col]]
        for i in range(n):
            if i != col and a[i][col] != 0:
                f = a[i][col]
                a[i] = [x - f * y for x, y in zip(a[i], a[col])]
    return [a[i][n] for i in range(n)]


@lru_cache(maxsize=None)
def block_vertices(budgets: tuple[Q, ...]) -> tuple[tuple[Q, ...], ...]:
    """Vertices of {p in Simplex({0,1}^m) : P(I_i = 1) <= budgets[i]}.

    A point p is indexed by error patterns x in {0,1}^m (x_i = 1 means
    primitive i of the block is wrong).  Vertices are basic feasible
    solutions: a support S and |S|-1 tight budget rows plus the sum row.
    """
    m = len(budgets)
    patterns = list(itertools.product((0, 1), repeat=m))
    verts: set[tuple[Q, ...]] = set()
    for k in range(1, m + 2):
        for support in itertools.combinations(range(len(patterns)), k):
            for tight in itertools.combinations(range(m), k - 1):
                rows = [[Q(1)] * k]
                rhs = [Q(1)]
                for i in tight:
                    rows.append([Q(patterns[s][i]) for s in support])
                    rhs.append(budgets[i])
                sol = _solve(rows, rhs)
                if sol is None or any(x < 0 for x in sol):
                    continue
                p = [Q(0)] * len(patterns)
                for s, x in zip(support, sol):
                    p[s] = x
                ok = all(
                    sum(p[j] for j, pat in enumerate(patterns) if pat[i] == 1) <= budgets[i]
                    for i in range(m)
                )
                if ok:
                    verts.add(tuple(p))
    return tuple(sorted(verts))


# ---------------------------------------------------------------------------
# Exact worst-case error
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Witness:
    """A maximizing latent valuation and joint law of the error indicators."""

    error: Q
    exact_value: bool
    atoms: tuple[tuple[str, bool], ...]
    law: tuple[tuple[tuple[int, ...], Q], ...]  # (error pattern over prims, prob)
    prim_names: tuple[str, ...]


def _blocks(ps: list[Prim]) -> list[list[int]]:
    by_src: dict[str, list[int]] = {}
    for i, p in enumerate(ps):
        by_src.setdefault(p.source, []).append(i)
    return list(by_src.values())


def worst_case(e: Expr, exact_rates: bool = False) -> tuple[Q, Q, Witness | None, Witness | None]:
    """(eps*, omg*, witness_eps, witness_omg) for expression e.

    ``exact_rates=True`` fixes every primitive's error rate at its declared
    value and makes all primitives mutually independent (the setting of the
    textbook all-negative-corner example); otherwise rates are upper bounds
    and the joint law is any admissible one.
    """
    core = desugar(e)
    ps = prims(core)
    atoms = sorted({p.atom for p in ps})
    blocks = _blocks(ps)
    n = len(ps)
    best = {False: (Q(0), None), True: (Q(0), None)}
    for bits in itertools.product((False, True), repeat=len(atoms)):
        v = dict(zip(atoms, bits))
        truth = {p: v[p.atom] for p in ps}
        exact = evaluate(core, truth)
        budgets = [p.omg if truth[p] else p.eps for p in ps]
        # err[x] = 1 iff flipping the primitives marked by x changes the answer
        err = {}
        for x in itertools.product((0, 1), repeat=n):
            obs = {p: (truth[p] != bool(xi)) for p, xi in zip(ps, x)}
            err[x] = evaluate(core, obs) != exact
        if exact_rates:
            laws_per_block = [
                [tuple(_product_law([budgets[i] for i in blk]))] for blk in blocks
            ]
        else:
            laws_per_block = [
                list(block_vertices(tuple(budgets[i] for i in blk))) for blk in blocks
            ]
        for choice in itertools.product(*laws_per_block):
            total = Q(0)
            law = []
            for x in itertools.product((0, 1), repeat=n):
                pr = Q(1)
                for blk, p_blk in zip(blocks, choice):
                    sub = tuple(x[i] for i in blk)
                    idx = int("".join(map(str, sub)), 2) if sub else 0
                    pr *= p_blk[idx]
                    if pr == 0:
                        break
                if pr:
                    law.append((x, pr))
                    if err[x]:
                        total += pr
            if total > best[exact][0] or (best[exact][1] is None and total == best[exact][0]):
                best[exact] = (
                    total,
                    Witness(total, exact, tuple(v.items()), tuple(law),
                            tuple(p.name for p in ps)),
                )
    (eps, w0), (omg, w1) = best[False], best[True]
    return eps, omg, w0, w1


def _product_law(rates: list[Q]) -> list[Q]:
    out = []
    for x in itertools.product((0, 1), repeat=len(rates)):
        pr = Q(1)
        for xi, r in zip(x, rates):
            pr *= r if xi else 1 - r
        out.append(pr)
    return out


def check_witness(e: Expr, w: Witness) -> Q:
    """Independently re-verify a witness: admissibility and its error."""
    core = desugar(e)
    ps = {p.name: p for p in prims(core)}
    v = dict(w.atoms)
    truth = {p: v[p.atom] for p in ps.values()}
    order = [ps[n] for n in w.prim_names]
    total_mass = sum(pr for _, pr in w.law)
    assert total_mass == 1, total_mass
    for i, p in enumerate(order):
        b = p.omg if truth[p] else p.eps
        marg = sum(pr for x, pr in w.law if x[i] == 1)
        assert marg <= b, (p, marg, b)
    # independence across sources: the law must equal the product of its
    # source-block marginals
    by_src: dict[str, list[int]] = {}
    for i, p in enumerate(order):
        by_src.setdefault(p.source, []).append(i)
    blocks = list(by_src.values())
    marg_blk = []
    for blk in blocks:
        mb: dict[tuple[int, ...], Q] = {}
        for x, pr in w.law:
            key = tuple(x[i] for i in blk)
            mb[key] = mb.get(key, Q(0)) + pr
        marg_blk.append(mb)
    law = dict(w.law)
    for x in itertools.product((0, 1), repeat=len(order)):
        prod = Q(1)
        for blk, mb in zip(blocks, marg_blk):
            prod *= mb.get(tuple(x[i] for i in blk), Q(0))
        assert law.get(x, Q(0)) == prod, "law is not a product across sources"
    exact = evaluate(core, truth)
    assert exact == w.exact_value
    err = Q(0)
    for x, pr in w.law:
        obs = {p: (truth[p] != bool(xi)) for p, xi in zip(order, x)}
        if evaluate(core, obs) != exact:
            err += pr
    return err


def error_at(e: Expr, atoms: dict[str, bool]) -> Q:
    """Error probability at one latent valuation when every primitive errs
    independently at exactly its declared rate."""
    core = desugar(e)
    ps = prims(core)
    truth = {p: atoms[p.atom] for p in ps}
    exact = evaluate(core, truth)
    rates = [p.omg if truth[p] else p.eps for p in ps]
    total = Q(0)
    for x, pr in zip(itertools.product((0, 1), repeat=len(ps)), _product_law(rates)):
        obs = {p: (truth[p] != bool(xi)) for p, xi in zip(ps, x)}
        if evaluate(core, obs) != exact:
            total += pr
    return total
