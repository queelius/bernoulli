"""Case studies: two-rate types versus single-probability (Decaf-style) bounds.

Run:  python casestudies.py            (prints a Markdown table, writes JSON)

Columns
-------
two-rate          (eps, omg) derived by the rules (tworate.check)
Decaf (derived)   delta from Decaf's product rule applied unconditionally
                  (p = p_a * p_b, primitives annotated with p = 1 - max(eps, omg))
single (sound)    delta from the like-for-like sound single-probability system:
                  product only when provenance is disjoint, union bound otherwise
exact             (eps*, omg*) from the exact oracle, when the instance is small
                  enough to enumerate (else "-": rule values are proved tight or
                  sound, not enumerated)
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from oracle import worst_case  # noqa: E402
from tworate import And, Expr, Not, Options, Or, Prim, Xor, check, single_prob  # noqa: E402


@dataclass
class Case:
    key: str
    title: str
    program: str
    expr: Expr
    enumerate_exact: bool
    note: str
    decaf_annotated: Q | None = None  # Decaf with a hand-written annotation, if relevant


def chain(op, xs):
    e = xs[0]
    for x in xs[1:]:
        e = op(e, x)
    return e


def cases() -> list[Case]:
    out: list[Case] = []
    pct = Q(1, 100)

    # 1. Bloom pre-filter guarding an exact check of the SAME fact (LSM-tree read path)
    bloom = Prim("bloom_x", "x_in_S", "seedB", pct, Q(0))
    disk = Prim("disk_x", "x_in_S", "exact", Q(0), Q(0))
    out.append(Case("prefilter-same", "Bloom pre-filter + exact check (same fact)",
                    "bloom(S,x) && disk_lookup(S,x)", And(bloom, disk), True,
                    "equal erasures: the composite is exact"))

    # 1b. pre-filter on a DIFFERENT fact
    pol = Prim("policy_x", "x_ok", "exact", Q(0), Q(0))
    out.append(Case("prefilter-diff", "Bloom answer AND exact predicate (different facts)",
                    "bloom(S,x) && policy(x)", And(bloom, pol), True,
                    "FPR equal to Decaf; only the one-sidedness is new"))

    # 2a. AND of two Bloom answers about different facts (intersection query)
    a = Prim("bloomA_x", "x_in_A", "seedA", pct, Q(0))
    b = Prim("bloomB_x", "x_in_B", "seedB2", pct, Q(0))
    out.append(Case("and-two-blooms", "AND of two Bloom answers (different sets)",
                    "bloom(A,x) && bloom(B,x)", And(a, b), True,
                    "eps = max, not the sum"))

    # 2b. cascade of k independent filters over the SAME set
    reps = [Prim(f"rep{i}", "x_in_S", f"seedR{i}", pct, Q(0)) for i in range(3)]
    out.append(Case("cascade-same", "Cascade of 3 independent filters on one set",
                    "bloom1(S,x) && bloom2(S,x) && bloom3(S,x)", chain(And, reps), True,
                    "equal erasures + disjoint seeds: product"))

    # 2c. the same cascade when the filters share hashing randomness
    reps_dep = [Prim(f"repd{i}", "x_in_S", "seedShared", pct, Q(0)) for i in range(3)]
    out.append(Case("cascade-shared-seed", "Same cascade, shared hash seed",
                    "bloom1..3 sharing one seed", chain(And, reps_dep), True,
                    "no independence certificate: min"))

    # 3. Miller-Rabin (k rounds, same n) composed with a set query
    k = 10
    mr = [Prim(f"mr{i}", "n_prime", f"witness{i}", Q(1, 4), Q(0)) for i in range(k)]
    mrk = chain(And, mr)
    out.append(Case("mr-alone", f"Miller-Rabin alone ({k} rounds, same n)",
                    "mr(n,a1) && ... && mr(n,a10)", mrk, False,
                    "amplification derived from equal erasures + disjoint witnesses",
                    decaf_annotated=Q(1, 4) ** k))
    out.append(Case("mr4-alone", "Miller-Rabin alone (4 rounds, same n)",
                    "mr(n,a1) && ... && mr(n,a4)", chain(And, mr[:4]), True,
                    "small instance, enumerated", decaf_annotated=Q(1, 4) ** 4))
    bn = Prim("bloom_n", "n_in_S", "seedBn", pct, Q(0))
    out.append(Case("mr-and-set", f"Miller-Rabin ({k} rounds) AND set query",
                    "mr_k(n) && bloom(S,n)", And(mrk, bn), False,
                    "two-rate derives amplification; Decaf needs a hand annotation",
                    decaf_annotated=1 - (1 - Q(1, 4) ** k) * (1 - pct)))
    mr4 = chain(And, mr[:4])
    out.append(Case("mr4-and-set", "Miller-Rabin (4 rounds) AND set query",
                    "mr_4(n) && bloom(S,n)", And(mr4, bn), True,
                    "small instance, enumerated",
                    decaf_annotated=1 - (1 - Q(1, 4) ** 4) * (1 - pct)))

    # 4. OR over shards (disjoint partition, independent per-shard filters)
    shards = [Prim(f"shard{i}", f"x_in_S{i}", f"seedS{i}", Q(1, 1000), Q(0)) for i in range(8)]
    out.append(Case("or-shards", "OR over 8 sharded filters",
                    "bloom(S1,x) || ... || bloom(S8,x)", chain(Or, shards), False,
                    "same FPR as Decaf; adds omg = 0"))
    out.append(Case("or-shards-3", "OR over 3 sharded filters",
                    "bloom(S1,x) || bloom(S2,x) || bloom(S3,x)", chain(Or, shards[:3]), True,
                    "small instance, enumerated"))

    # 5. Negated membership: blocklist gate
    blk = Prim("block_x", "x_blocked", "seedBL", pct, Q(0))
    auth = Prim("auth_x", "x_authorized", "exact", Q(0), Q(0))
    out.append(Case("blocklist", "Blocklist gate !bloom(Block,x) && auth(x)",
                    "!bloom(Block,x) && auth(x)", And(Not(blk), auth), True,
                    "static 'never admits a blocked item' (eps = 0)"))
    auth_ml = Prim("authml_x", "x_authorized", "model", Q(2, 100), Q(5, 100))
    out.append(Case("blocklist-approx-auth", "Blocklist gate with approximate auth",
                    "!bloom(Block,x) && auth~(x)", And(Not(blk), auth_ml), True,
                    "eps comes only from auth~"))

    # 6. Where two-rate adds nothing: symmetric noise
    s1 = Prim("sym1", "y1", "hw1", Q(1, 100), Q(1, 100))
    s2 = Prim("sym2", "y2", "hw2", Q(1, 100), Q(1, 100))
    out.append(Case("symmetric-and", "AND of symmetric-noise bits",
                    "cmp1 && cmp2 (bit-flip hardware)", And(s1, s2), True,
                    "max(eps,omg) equals Decaf"))
    out.append(Case("xor-blooms", "XOR (symmetric difference) of two Bloom answers",
                    "bloom(A,x) != bloom(B,x)", Xor(a, b), True,
                    "XOR destroys one-sidedness"))
    return out


def fmt(x: Q) -> str:
    f = float(x)
    if f == 0:
        return "0"
    if f < 1e-3:
        return f"{f:.2e}"
    return f"{f:.4g}"


def run() -> list[dict]:
    rows = []
    for c in cases():
        t = check(c.expr)
        t_nosame = check(c.expr, Options(use_same_truth=False))
        decaf, _ = single_prob(c.expr, provenance=False)
        single, _ = single_prob(c.expr, provenance=True)
        union, _ = single_prob(c.expr, independent_product=False)
        ex = worst_case(c.expr)[:2] if c.enumerate_exact else None
        rows.append({
            "key": c.key, "title": c.title, "program": c.program, "note": c.note,
            "two_rate": [str(t.eps), str(t.omg)],
            "two_rate_without_same_truth": [str(t_nosame.eps), str(t_nosame.omg)],
            "decaf_derived": str(decaf),
            "decaf_annotated": None if c.decaf_annotated is None else str(c.decaf_annotated),
            "single_sound": str(single), "single_union": str(union),
            "exact": None if ex is None else [str(ex[0]), str(ex[1])],
            "_t": (t.eps, t.omg), "_decaf": decaf, "_single": single, "_ex": ex,
            "_ann": c.decaf_annotated,
        })
    return rows


def table(rows: list[dict]) -> str:
    head = ("| case | two-rate (eps, omg) | exact (eps*, omg*) | Decaf derived delta"
            " | Decaf annotated | single-prob sound delta |\n|---|---|---|---|---|---|")
    lines = [head]
    for r in rows:
        te, to = r["_t"]
        ex = r["_ex"]
        exs = "-" if ex is None else f"({fmt(ex[0])}, {fmt(ex[1])})"
        ann = "-" if r["_ann"] is None else fmt(r["_ann"])
        lines.append(f"| {r['title']} | ({fmt(te)}, {fmt(to)}) | {exs} | {fmt(r['_decaf'])}"
                     f" | {ann} | {fmt(r['_single'])} |")
    return "\n".join(lines)


if __name__ == "__main__":
    rows = run()
    print(table(rows))
    clean = [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]
    (Path(__file__).parent / "casestudies.json").write_text(json.dumps(clean, indent=2) + "\n")
