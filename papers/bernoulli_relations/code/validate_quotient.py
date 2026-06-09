#!/usr/bin/env python3
"""Validate the canonical-representative (quotient) construction against the
OR-closure for symmetric relations (sec:closure_dichotomy).

Claims under test:

1. CANONICAL TEST: answer the query on (x, y) by a single Bernoulli trial on the
   canonical representative (min, max) of its unordered orbit. Symmetry then
   holds DETERMINISTICALLY (query(x,y) == query(y,x) in every realization), the
   false-positive and true-positive rates stay at the base (eps, tau), and a
   construction-time build stores one element per member orbit (|R|/2 for a
   symmetric R with no diagonal), i.e. the invariant is free.

2. OR-CLOSURE: admit the orbit if either ordered trial fires. Symmetry also
   deterministic, but rates move to (1-(1-eps)^2, 1-(1-tau)^2): the log2(m)
   surcharge of the corollary buys the true-positive boost, not the invariant.

3. The naive (per-ordered-pair) approximation is symmetric only with the
   vanishing probability of the symmetry-preservation theorem.

Run: python3 validate_quotient.py   (numpy only)
"""
import numpy as np

EPS, TAU = 0.05, 0.90
A = 40            # ground set size
TRIALS = 200_000  # Monte Carlo runs (per-pair trials vectorized inside)


def main():
    rng = np.random.default_rng(3)

    # a symmetric R on A x A without diagonal: random unordered pairs
    n_orbits = A * (A - 1) // 2
    orbit_member = rng.random(n_orbits) < 0.15     # which unordered pairs are in R
    P = int(orbit_member.sum())                    # member orbits
    N = n_orbits - P                               # non-member orbits

    # --- canonical test: ONE trial per orbit -----------------------------
    fires_m = rng.random((TRIALS, P)) < TAU        # member orbits fire (TP)
    fires_n = rng.random((TRIALS, N)) < EPS        # non-member orbits fire (FP)
    # symmetry is structural: both orders read the same trial, so it holds in
    # every realization by construction; rates are the per-orbit rates.
    can_tpr = fires_m.mean()
    can_fpr = fires_n.mean()

    # --- OR-closure: TWO independent ordered trials per orbit, OR'd ------
    or_m = ((rng.random((TRIALS, P)) < TAU) | (rng.random((TRIALS, P)) < TAU)).mean()
    or_n = ((rng.random((TRIALS, N)) < EPS) | (rng.random((TRIALS, N)) < EPS)).mean()

    # --- naive per-ordered-pair approximation: P(symmetric) --------------
    # per orbit the two ordered trials agree w.p. tau^2 + (1-tau)^2 (members)
    # or (1-eps)^2 + eps^2 (non-members); whole-relation probability is the
    # product (thm:symmetric_preservation). At A=40 that probability is ~1e-10,
    # unobservable by Monte Carlo, which is the theorem's point; estimate it on
    # a small instance where the event still occurs.
    runs, Ps, Ns = 200_000, 4, 11                  # |A|=6 scale: 15 orbits
    agree_m = (rng.random((runs, Ps)) < TAU) == (rng.random((runs, Ps)) < TAU)
    agree_n = (rng.random((runs, Ns)) < EPS) == (rng.random((runs, Ns)) < EPS)
    p_sym_emp = (agree_m.all(axis=1) & agree_n.all(axis=1)).mean()
    p_sym_ana = (TAU**2 + (1 - TAU)**2) ** Ps * ((1 - EPS)**2 + EPS**2) ** Ns

    print(f"symmetric R over |A|={A}: {P} member orbits, {N} non-member orbits\n")
    print(f"{'construction':<22} {'FPR':>10} {'TPR':>10} {'stored':>8} {'symmetric?':>11}")
    print(f"{'canonical (quotient)':<22} {can_fpr:10.5f} {can_tpr:10.5f} "
          f"{P:8d} {'always':>11}")
    print(f"{'  analytical':<22} {EPS:10.5f} {TAU:10.5f}")
    print(f"{'OR-closure':<22} {or_n:10.5f} {or_m:10.5f} {2*P:8d} {'always':>11}")
    print(f"{'  analytical':<22} {1-(1-EPS)**2:10.5f} {1-(1-TAU)**2:10.5f}")
    print(f"\nnaive P(symmetric) at |A|=40 (analytical): "
          f"{(TAU**2 + (1-TAU)**2) ** P * ((1-EPS)**2 + EPS**2) ** N:.3e}  (vanishing)")
    print(f"naive P(symmetric), small instance ({Ps}+{Ns} orbits): "
          f"empirical {p_sym_emp:.4f}, analytical {p_sym_ana:.4f}")

    assert abs(can_fpr - EPS) < 0.001 and abs(can_tpr - TAU) < 0.002
    assert abs(or_n - (1 - (1 - EPS)**2)) < 0.001
    assert abs(or_m - (1 - (1 - TAU)**2)) < 0.001
    print("\nall canonical/OR-closure rate checks PASS")


if __name__ == "__main__":
    main()
