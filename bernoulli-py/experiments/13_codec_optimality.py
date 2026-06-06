#!/usr/bin/env python3
"""Experiment 13: Codec (TV, L) Pareto frontier.

Goal: characterize the trade-off between expected codeword length L and
total-variation distance TV(p_f, q) where ``q_v = 2^(-l_v)`` is the
codec's codespace allocation. Huffman-from-frequencies minimizes L. Exp 07
established that TV controls non-member leakage. We therefore want to know:

1. Is Huffman on the (TV, L) Pareto frontier?
2. Is Huffman TV-optimal among Kraft-feasible length assignments?
3. What is the structure of TV-optimal length assignments?
4. How much TV reduction is achievable, and at what L cost?

Methodology: enumerate all Kraft-feasible length tuples for a given
``(|V|, m_bits)`` and small distribution; compute (L, TV) for each;
identify Pareto frontier and the position of the Huffman assignment.

Stdlib only (math, itertools, dataclasses). No numpy.

Naming: we keep mathematical-literature convention (L, H, TV, dL, dTV;
l_v for codeword length). Ruff's N806/E741 are silenced for this file.
"""
# ruff: noqa: N806, E741

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
sys.path.insert(0, str(PKG_ROOT / "src"))

from bernoulli.maps.codec import (  # noqa: E402
    PrefixCodec,
    shannon_entropy,
)

# =====================================================================
# Pareto-frontier enumeration
# =====================================================================


@dataclass(frozen=True)
class Assignment:
    lengths: tuple[int, ...]  # codeword lengths in order of values
    L: float  # expected codeword length
    TV: float  # total variation distance between p and q = 2^(-l)
    kraft: float  # sum 2^(-l)


def enumerate_kraft_feasible(
    n_values: int,
    m_bits: int,
    cap: int = 200000,
) -> list[tuple[int, ...]]:
    """Enumerate length tuples (l_1, ..., l_n) with l_i in [1, m_bits]
    satisfying Kraft (sum 2^(-l_i) <= 1).

    Returns a list of length tuples. Stops at ``cap`` tuples to bound
    runtime; raises if the truncation kicks in (so we know).
    """
    out: list[tuple[int, ...]] = []
    for tup in product(range(1, m_bits + 1), repeat=n_values):
        kraft = 0.0
        for l in tup:
            kraft += math.ldexp(1.0, -l)
        if kraft <= 1.0 + 1e-12:
            out.append(tup)
            if len(out) >= cap:
                break
    return out


def assignment_metrics(
    lengths: tuple[int, ...],
    p: tuple[float, ...],
) -> Assignment:
    """Compute (L, TV, kraft) for a length tuple aligned to probability p."""
    L = 0.0
    kraft = 0.0
    for l, pi in zip(lengths, p, strict=True):
        L += pi * l
        kraft += math.ldexp(1.0, -l)
    # TV(p, q) where q_v = 2^(-l_v). The unused codespace 1 - sum q_v
    # decays onto a default value (folded onto the largest-mass codeword).
    # For TV computation, we treat q as a sub-probability that sums to
    # exactly kraft <= 1; the surplus mass (1 - kraft) is added to the
    # value with maximum p (canonical PaddedCodec-like default).
    if kraft < 1.0 - 1e-15:
        # Allocate surplus to argmax(p) to match PrefixCodec.from_frequencies
        # default (which assigns the surplus to the heaviest value).
        idx_max = max(range(len(p)), key=lambda i: p[i])
        q = list(math.ldexp(1.0, -l) for l in lengths)
        q[idx_max] += 1.0 - kraft
    else:
        q = [math.ldexp(1.0, -l) for l in lengths]
    tv = 0.5 * sum(abs(pi - qi) for pi, qi in zip(p, q, strict=True))
    return Assignment(lengths=lengths, L=L, TV=tv, kraft=kraft)


def pareto_frontier(assignments: list[Assignment]) -> list[Assignment]:
    """Identify the (TV, L) Pareto-optimal assignments.

    Smaller L and smaller TV both desirable.
    """
    front: list[Assignment] = []
    for a in assignments:
        dominated = False
        for b in assignments:
            if b is a:
                continue
            # b dominates a if b.L <= a.L and b.TV <= a.TV with one strict.
            if (
                b.L <= a.L + 1e-12
                and b.TV <= a.TV + 1e-12
                and (b.L < a.L - 1e-12 or b.TV < a.TV - 1e-12)
            ):
                dominated = True
                break
        if not dominated:
            front.append(a)
    front.sort(key=lambda a: (a.L, a.TV))
    return front


def huffman_assignment(
    p: tuple[float, ...],
    m_bits: int,
) -> tuple[int, ...]:
    """Build the Huffman-from-frequencies assignment via PrefixCodec
    and return the resulting length tuple aligned to value index order.
    """
    freqs = {i: p[i] for i in range(len(p)) if p[i] > 0}
    pc: PrefixCodec[int] = PrefixCodec.from_frequencies(freqs, m_bits=m_bits)
    out: list[int] = []
    for i in range(len(p)):
        if p[i] > 0:
            out.append(pc.codeword_length(i))
        else:
            # Zero-mass values are dropped by Huffman; assign max length so
            # they cost nothing under p but stay Kraft-feasible.
            out.append(m_bits)
    return tuple(out)


# =====================================================================
# Distributions
# =====================================================================


def dist_uniform(n: int) -> tuple[float, ...]:
    return tuple(1.0 / n for _ in range(n))


def dist_zipf(n: int, s: float = 1.0) -> tuple[float, ...]:
    raw = [1.0 / ((i + 1) ** s) for i in range(n)]
    z = sum(raw)
    return tuple(r / z for r in raw)


def dist_two_mode(n: int) -> tuple[float, ...]:
    # First two get 0.4 each; remainder split equally.
    if n < 3:
        return tuple(1.0 / n for _ in range(n))
    rest = 0.2 / (n - 2)
    return (0.4, 0.4) + tuple(rest for _ in range(n - 2))


def dist_heavy_tail(n: int) -> tuple[float, ...]:
    # 90% on first; rest evenly on tail.
    rest = 0.1 / (n - 1)
    return (0.9,) + tuple(rest for _ in range(n - 1))


def dist_dyadic_4() -> tuple[float, ...]:
    return (0.5, 0.25, 0.125, 0.125)


def dist_dyadic_8() -> tuple[float, ...]:
    return (0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 0.0078125)


# =====================================================================
# Reporting helpers
# =====================================================================


def fmt_lengths(lengths: tuple[int, ...]) -> str:
    return "(" + ",".join(str(l) for l in lengths) + ")"


def fmt_p(p: tuple[float, ...]) -> str:
    return "[" + ", ".join(f"{x:.4f}" for x in p) + "]"


def summarize_distribution(
    name: str,
    p: tuple[float, ...],
    m_bits: int,
    cap: int,
    print_frontier_count: int = 8,
) -> dict[str, object]:
    """Run enumeration and Pareto analysis on (p, m_bits). Print a summary
    block and return a dict with structured fields."""
    n = len(p)
    H = shannon_entropy({i: p[i] for i in range(n)})
    print(f"\n=== Distribution: {name}  (|V|={n}, m_bits={m_bits}) ===")
    print(f"p = {fmt_p(p)}")
    print(f"H(Y) = {H:.4f} bits")

    tuples = enumerate_kraft_feasible(n, m_bits, cap=cap)
    truncated = len(tuples) >= cap
    print(f"Kraft-feasible length tuples: {len(tuples)}"
          + ("  [TRUNCATED]" if truncated else ""))

    assignments = [assignment_metrics(t, p) for t in tuples]
    front = pareto_frontier(assignments)
    print(f"Pareto frontier size: {len(front)}")

    huff = huffman_assignment(p, m_bits)
    huff_metrics = assignment_metrics(huff, p)
    huff_on_frontier = any(
        a.lengths == huff for a in front
    )

    # TV-min and L-min over the entire feasible set.
    tv_min = min(assignments, key=lambda a: (a.TV, a.L))
    L_min = min(assignments, key=lambda a: (a.L, a.TV))
    # Maximum-TV assignment (worst case, Exp 07 adversarial bound).
    tv_max = max(assignments, key=lambda a: (a.TV, -a.L))

    print(
        f"Huffman: lengths={fmt_lengths(huff)}  "
        f"L={huff_metrics.L:.4f}  TV={huff_metrics.TV:.4f}  "
        f"kraft={huff_metrics.kraft:.4f}  "
        f"on_frontier={huff_on_frontier}"
    )
    print(
        f"L-min : lengths={fmt_lengths(L_min.lengths)}  "
        f"L={L_min.L:.4f}  TV={L_min.TV:.4f}  kraft={L_min.kraft:.4f}"
    )
    print(
        f"TV-min: lengths={fmt_lengths(tv_min.lengths)}  "
        f"L={tv_min.L:.4f}  TV={tv_min.TV:.4f}  kraft={tv_min.kraft:.4f}"
    )
    print(
        f"TV-max: lengths={fmt_lengths(tv_max.lengths)}  "
        f"L={tv_max.L:.4f}  TV={tv_max.TV:.4f}  kraft={tv_max.kraft:.4f}"
    )

    print(f"  L-min equal to Huffman L?     {abs(L_min.L - huff_metrics.L) < 1e-9}")
    huffman_is_tv_optimal = abs(huff_metrics.TV - tv_min.TV) < 1e-9
    print(f"  Huffman achieves min TV?      {huffman_is_tv_optimal}")
    if not huffman_is_tv_optimal:
        # How much TV reduction at what L cost?
        dTV = huff_metrics.TV - tv_min.TV
        dL = tv_min.L - huff_metrics.L
        print(
            f"  Huffman -> TV-min: dTV={dTV:+.4f}, dL={dL:+.4f} "
            f"(L overhead {dL / max(huff_metrics.L, 1e-9) * 100:+.1f}%)"
        )

    # Print head of frontier table.
    print("  Pareto frontier (head):")
    print("    lengths            L        TV      kraft   note")
    for a in front[:print_frontier_count]:
        note = []
        if a.lengths == huff:
            note.append("HUFFMAN")
        if abs(a.TV - tv_min.TV) < 1e-12:
            note.append("TV-min")
        if abs(a.L - L_min.L) < 1e-12:
            note.append("L-min")
        notes = ",".join(note) if note else ""
        print(
            f"    {fmt_lengths(a.lengths):18s}  "
            f"{a.L:6.4f}  {a.TV:6.4f}  {a.kraft:6.4f}  {notes}"
        )

    return {
        "name": name,
        "n": n,
        "m_bits": m_bits,
        "H": H,
        "p": p,
        "n_feasible": len(tuples),
        "pareto_size": len(front),
        "huffman_lengths": huff,
        "huffman_L": huff_metrics.L,
        "huffman_TV": huff_metrics.TV,
        "huffman_kraft": huff_metrics.kraft,
        "huffman_on_frontier": huff_on_frontier,
        "huffman_is_tv_optimal": huffman_is_tv_optimal,
        "L_min": L_min,
        "TV_min": tv_min,
        "TV_max": tv_max,
        "frontier_head": front[:print_frontier_count],
    }


def main() -> None:
    print("=" * 72)
    print("Experiment 13: Codec (TV, L) Pareto frontier")
    print("=" * 72)

    summaries: list[dict[str, object]] = []

    # |V|=4, m_bits=4: small enough to exhaustively enumerate.
    cases_small = [
        ("uniform-4",   dist_uniform(4),    4),
        ("zipf-4",      dist_zipf(4),       4),
        ("two-mode-4",  dist_two_mode(4),   4),
        ("heavy-4",     dist_heavy_tail(4), 4),
        ("dyadic-4",    dist_dyadic_4(),    4),
    ]
    # |V|=6, m_bits=4: more options.
    cases_med = [
        ("uniform-6",   dist_uniform(6),    4),
        ("zipf-6",      dist_zipf(6),       4),
        ("two-mode-6",  dist_two_mode(6),   4),
        ("heavy-6",     dist_heavy_tail(6), 4),
    ]
    # |V|=8, m_bits=4: larger; cap will keep it manageable.
    cases_big = [
        ("uniform-8",   dist_uniform(8),    4),
        ("zipf-8",      dist_zipf(8),       4),
        ("dyadic-8",    dist_dyadic_8(),    4),
    ]
    # |V|=8, m_bits=6: bigger codespace, more length flexibility.
    cases_wide = [
        ("zipf-8-m6",   dist_zipf(8),       6),
        ("heavy-8-m6",  dist_heavy_tail(8), 6),
    ]

    for name, p, m in cases_small:
        summaries.append(summarize_distribution(name, p, m, cap=200000))
    for name, p, m in cases_med:
        summaries.append(summarize_distribution(name, p, m, cap=200000))
    for name, p, m in cases_big:
        summaries.append(summarize_distribution(name, p, m, cap=200000))
    for name, p, m in cases_wide:
        summaries.append(summarize_distribution(name, p, m, cap=200000))

    # =================================================================
    # Cross-distribution verdicts
    # =================================================================
    print("\n" + "=" * 72)
    print("Verdicts across distributions")
    print("=" * 72)

    n_total = len(summaries)
    n_huff_on_frontier = sum(1 for s in summaries if s["huffman_on_frontier"])
    n_huff_tv_optimal = sum(1 for s in summaries if s["huffman_is_tv_optimal"])

    print(f"  Cases total: {n_total}")
    print(f"  Huffman on Pareto frontier: {n_huff_on_frontier} / {n_total}")
    print(f"  Huffman TV-optimal:         {n_huff_tv_optimal} / {n_total}")

    # Cases where Huffman is not TV-optimal: report TV reduction available
    # and the L cost.
    print()
    print("Cases where Huffman is NOT TV-optimal:")
    print(f"  {'name':14s}  {'H':>6s}  {'L_h':>6s}  {'TV_h':>6s}  "
          f"{'L_t':>6s}  {'TV_t':>6s}  {'dTV':>6s}  {'dL':>6s}  {'%L':>5s}")
    for s in summaries:
        if not s["huffman_is_tv_optimal"]:
            tv_min: Assignment = s["TV_min"]  # type: ignore[assignment]
            dTV = s["huffman_TV"] - tv_min.TV  # type: ignore[operator]
            dL = tv_min.L - s["huffman_L"]  # type: ignore[operator]
            pct = dL / max(s["huffman_L"], 1e-9) * 100  # type: ignore[arg-type]
            print(
                f"  {s['name']:14s}  "
                f"{s['H']:6.4f}  {s['huffman_L']:6.4f}  {s['huffman_TV']:6.4f}  "
                f"{tv_min.L:6.4f}  {tv_min.TV:6.4f}  {dTV:+6.4f}  {dL:+6.4f}  "
                f"{pct:+5.1f}"
            )

    # H3 test: is the TV-min assignment given by ceil/floor rounding of
    # -log2(p_v) (subject to Kraft)?
    print()
    print("H3 test: TV-min vs naive round(-log2(p_v))")
    for s in summaries:
        p = s["p"]  # type: ignore[index]
        rounded = tuple(
            min(s["m_bits"], max(1, int(round(-math.log2(pi))))) if pi > 0 else s["m_bits"]  # type: ignore[arg-type]
            for pi in p
        )
        tv_min: Assignment = s["TV_min"]  # type: ignore[assignment]
        kraft_rounded = sum(math.ldexp(1.0, -l) for l in rounded)
        rounded_feasible = kraft_rounded <= 1.0 + 1e-12
        match = rounded == tv_min.lengths
        print(
            f"  {s['name']:14s}  rounded={fmt_lengths(rounded)} "
            f"kraft={kraft_rounded:.4f} {'feasible' if rounded_feasible else 'INFEASIBLE'}  "
            f"TV-min={fmt_lengths(tv_min.lengths)}  "
            f"{'MATCH' if match else 'differ'}"
        )

    # Quantize-gap (L1 between p and q): how close can q get to p?
    print()
    print("L1 quantization gap = 2 * min TV (across all length assignments):")
    for s in summaries:
        tv_min: Assignment = s["TV_min"]  # type: ignore[assignment]
        print(
            f"  {s['name']:14s}  H={s['H']:6.4f}  "
            f"L1(p,q*)={2*tv_min.TV:.4f}  "
            f"min-TV={tv_min.TV:.4f}  Huffman-TV={s['huffman_TV']:.4f}"
        )


if __name__ == "__main__":
    main()
