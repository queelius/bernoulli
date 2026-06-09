#!/usr/bin/env python3
"""Monte Carlo validation of the Phase-C results in bernoulli_relations.

This script empirically checks the closed-form error-propagation and
invariant-preservation formulas of the paper by direct simulation. Each
approximate relation is realized as an independent per-tuple Bernoulli trial
over a small product universe: a true member (positive) is reported with
probability tau = 1 - omega (true-positive rate) and a true non-member
(negative) is reported with probability eps (false-positive rate).

We validate, against their analytical formulas:

  PROJECTION  (thm:project)
    - false-positive rate at fan-in k:           1 - (1-eps)^k
    - true-positive rate, j members of k tuples: 1 - (1-tau)^j (1-eps)^(k-j)

  JOIN        (thm:join, thm:join_dependence)
    - per-tuple false-negative rate:             omega_R + omega_S - omega_R omega_S
    - shared-component correlation:              P(both accepted) = a P(B1) P(B2),
      i.e. a factor 1/a ABOVE the independent model a^2 P(B1) P(B2)
      -- the demonstration that element-wise independence FAILS.

  SYMMETRIC CLOSURE (thm:symmetric_closure)
    - closure false-positive rate:               1 - (1-eps)^2
    - closure true-positive rate:                1 - (1-tau)^2

  REFLEXIVE   (thm:reflexive)
    - P(approximation reflexive):                tau^|A|

  FUNCTIONAL  (thm:functional)
    - P(no spurious value at a key):             (1-eps)^(|Y|-1)

Each result prints analytical vs empirical with absolute error. No paper
dependency: pure-Python + numpy. Reproducible via a fixed seed.

Usage:  python3 validate.py [--trials N] [--seed S]
"""

from __future__ import annotations

import argparse

import numpy as np

# ---------------------------------------------------------------------------
# Base rates used throughout (the paper's illustrative symmetric rates).
# ---------------------------------------------------------------------------
EPS = 0.05   # false-positive rate  (varepsilon)
OMEGA = 0.10  # false-negative rate  (omega)
TAU = 1.0 - OMEGA  # true-positive rate  (tau)


def draw_membership(rng: np.random.Generator, is_member: np.ndarray,
                    eps: float, tau: float) -> np.ndarray:
    """One independent Bernoulli trial per tuple.

    is_member[i] True  -> reported with probability tau (true positive kept).
    is_member[i] False -> reported with probability eps (false positive).
    Returns a boolean array of reported memberships.
    """
    u = rng.random(is_member.shape)
    p = np.where(is_member, tau, eps)
    return u < p


# ---------------------------------------------------------------------------
# PROJECTION
# ---------------------------------------------------------------------------
def validate_projection(rng, trials, results):
    """Projection is a logical OR over the fiber of an output tuple.

    For each fan-in k we build a fiber of k DISTINCT underlying tuples and
    accept the projected tuple iff at least one fiber tuple is reported.
    """
    # (i) false-positive amplification: every fiber tuple is a true negative.
    for k in (1, 2, 3, 4, 5, 8):
        is_member = np.zeros((trials, k), dtype=bool)        # all negatives
        reported = draw_membership(rng, is_member, EPS, TAU)  # (trials, k)
        accepted = reported.any(axis=1)                       # OR over fiber
        emp = accepted.mean()
        ana = 1.0 - (1.0 - EPS) ** k
        results.append((f"Projection FPR, fan-in k={k}", ana, emp))

    # (ii) true-positive boost: j genuine members among k fiber tuples.
    for k, j in ((1, 1), (3, 1), (3, 2), (5, 2)):
        is_member = np.zeros((trials, k), dtype=bool)
        is_member[:, :j] = True                               # first j members
        reported = draw_membership(rng, is_member, EPS, TAU)
        accepted = reported.any(axis=1)
        emp = accepted.mean()
        ana = 1.0 - (1.0 - TAU) ** j * (1.0 - EPS) ** (k - j)
        results.append((f"Projection TPR, k={k}, j={j}", ana, emp))


# ---------------------------------------------------------------------------
# JOIN
# ---------------------------------------------------------------------------
def validate_join(rng, trials, results):
    """Join is a logical AND of two independent operand tests.

    A join tuple (r, s) is reported iff both r is reported in R and s in S.
    We use the paper's symmetric rates on both operands.
    """
    eps_r = eps_s = EPS
    omega_r = omega_s = OMEGA
    tau_r = tau_s = TAU

    # (i) per-tuple false-negative rate for a genuine join member
    #     (r in R and s in S): missed iff either operand misses.
    r_member = np.ones(trials, dtype=bool)
    s_member = np.ones(trials, dtype=bool)
    r_rep = draw_membership(rng, r_member, eps_r, tau_r)
    s_rep = draw_membership(rng, s_member, eps_s, tau_s)
    out_rep = r_rep & s_rep
    emp_fnr = 1.0 - out_rep.mean()                # P(missed)
    ana_fnr = omega_r + omega_s - omega_r * omega_s
    results.append(("Join FNR (both members)", ana_fnr, emp_fnr))

    # (ii) both-absent false-positive corner: r not in R, s not in S; the join
    #      fires only if both operands false-positive -> eps_r * eps_s.
    r_neg = np.zeros(trials, dtype=bool)
    s_neg = np.zeros(trials, dtype=bool)
    r_rep_n = draw_membership(rng, r_neg, eps_r, tau_r)
    s_rep_n = draw_membership(rng, s_neg, eps_s, tau_s)
    emp_fpr_corner = (r_rep_n & s_rep_n).mean()
    ana_fpr_corner = eps_r * eps_s
    results.append(("Join FPR (both-absent corner)", ana_fpr_corner,
                    emp_fpr_corner))

    # (iii) THE INDEPENDENCE-FAILURE CORRELATION.
    #   Two output tuples (r, s1) and (r, s2) share the SAME left trial on r.
    #   Draw ONE trial for r, two independent trials for s1, s2 (all genuine
    #   members here, so a = P(r reported) = tau_r, P(Bi) = tau_s).
    #   P(both accepted) = a * P(B1) * P(B2);  independent model = a^2 P(B1)P(B2).
    a = tau_r                       # P(r reported)
    pB = tau_s                      # P(s_i reported)
    r_shared = draw_membership(rng, np.ones(trials, dtype=bool), eps_r, tau_r)
    s1 = draw_membership(rng, np.ones(trials, dtype=bool), eps_s, tau_s)
    s2 = draw_membership(rng, np.ones(trials, dtype=bool), eps_s, tau_s)
    out1 = r_shared & s1
    out2 = r_shared & s2
    emp_both = (out1 & out2).mean()
    ana_both = a * pB * pB                       # correlated (shared trial)
    ana_indep = (a * pB) * (a * pB)              # WRONG independent model
    results.append(("Join shared-r P(both), correlated model",
                    ana_both, emp_both))
    # The independent model is what the paper predicts FAILS: the empirical
    # P(both) should match the correlated value above, NOT this product of
    # marginals. Flagged as an expected mismatch (demonstration, not a fit).
    results.append(("Join shared-r P(both) vs independent model "
                    "[expect mismatch: independence FAILS]",
                    ana_indep, emp_both, "demo"))
    # Report the empirical correlation factor vs the predicted 1/a.
    factor_emp = emp_both / (ana_indep)
    factor_ana = 1.0 / a
    results.append(("Join correlation factor P(both)/[indep], pred = 1/a",
                    factor_ana, factor_emp))


# ---------------------------------------------------------------------------
# SYMMETRIC CLOSURE
# ---------------------------------------------------------------------------
def validate_symmetric_closure(rng, trials, results):
    """Symmetric closure: admit an unordered pair if EITHER ordered trial fires.

    Each unordered pair has two independent ordered trials. For a positive pair
    both ordered tuples are members; for a negative pair both are non-members.
    """
    # negative pair: both ordered trials are false-positive draws.
    neg = np.zeros((trials, 2), dtype=bool)
    neg_rep = draw_membership(rng, neg, EPS, TAU)
    closure_neg = neg_rep.any(axis=1)            # OR of the two ordered trials
    emp_fpr = closure_neg.mean()
    ana_fpr = 1.0 - (1.0 - EPS) ** 2
    results.append(("Symmetric closure FPR", ana_fpr, emp_fpr))

    # positive pair: both ordered trials are true-positive draws.
    pos = np.ones((trials, 2), dtype=bool)
    pos_rep = draw_membership(rng, pos, EPS, TAU)
    closure_pos = pos_rep.any(axis=1)
    emp_tpr = closure_pos.mean()
    ana_tpr = 1.0 - (1.0 - TAU) ** 2
    results.append(("Symmetric closure TPR", ana_tpr, emp_tpr))


# ---------------------------------------------------------------------------
# CLOSURE DICHOTOMY (thm:local_closure, thm:transitivity_cascade)
# ---------------------------------------------------------------------------
def validate_closure_dichotomy(rng, trials, results):
    """Generalize the symmetric closure and separate it from transitivity.

    thm:local_closure: a monotone local invariant with orbits of m ordered pairs
    has OR-closure FPR 1-(1-eps)^m and TPR 1-(1-tau)^m (m=1 reflexive, m=2 the
    symmetric closure). Checked by Monte Carlo for m in {1,3,4}.

    thm:transitivity_cascade: the transitive closure of a path of length k needs
    ceil(log2 k) passes and C(k+1,2) pairs -- a DETERMINISTIC, structural check
    (no rate) that no bounded one-pass closure of the local form exists.
    """
    # Generalized OR-closure over an orbit of m ordered trials.
    for m in (1, 3, 4):
        neg = np.zeros((trials, m), dtype=bool)
        emp_fpr = draw_membership(rng, neg, EPS, TAU).any(axis=1).mean()
        results.append((f"Local-closure FPR, orbit m={m}", 1.0 - (1.0 - EPS) ** m, emp_fpr))
        pos = np.ones((trials, m), dtype=bool)
        emp_tpr = draw_membership(rng, pos, EPS, TAU).any(axis=1).mean()
        results.append((f"Local-closure TPR, orbit m={m}", 1.0 - (1.0 - TAU) ** m, emp_tpr))

    # Transitivity cascade: path 1->2->...->(k+1); iterate the one-pass rule to
    # the fixed point and count passes and manufactured pairs (exact integers).
    for k in (4, 8, 16):
        R = {(i, i + 1) for i in range(1, k + 1)}
        passes = 0
        while True:
            new = {(x, z) for (x, y) in R for (y2, z) in R if y == y2 and (x, z) not in R}
            if not new:
                break
            R |= new
            passes += 1
        results.append((f"Transitivity cascade passes, path k={k}",
                        float(int(np.ceil(np.log2(k)))), float(passes)))
        results.append((f"Transitivity cascade |closure|, path k={k}",
                        float((k + 1) * k // 2), float(len(R))))


# ---------------------------------------------------------------------------
# REFLEXIVE
# ---------------------------------------------------------------------------
def validate_reflexive(rng, trials, results):
    """Reflexivity survives iff every diagonal pair is a true positive.

    |A| independent diagonal trials, each a true positive with probability tau.
    """
    for card_A in (3, 5, 8):
        diag = np.ones((trials, card_A), dtype=bool)   # |A| diagonal members
        rep = draw_membership(rng, diag, EPS, TAU)
        reflexive = rep.all(axis=1)                    # AND over diagonal
        emp = reflexive.mean()
        ana = TAU ** card_A
        results.append((f"P(reflexive), |A|={card_A}", ana, emp))


# ---------------------------------------------------------------------------
# FUNCTIONAL (single-valued)
# ---------------------------------------------------------------------------
def validate_functional(rng, trials, results):
    """A key stays single-valued iff none of the |Y|-1 non-true values is a
    false positive. Each is an independent false-positive trial with prob eps.
    """
    for card_Y in (2, 4, 8):
        spurious = card_Y - 1                          # candidate spurious values
        # all of these are TRUE NEGATIVES for this key.
        neg = np.zeros((trials, spurious), dtype=bool)
        rep = draw_membership(rng, neg, EPS, TAU)
        no_spurious = ~rep.any(axis=1)                 # none fired
        emp = no_spurious.mean()
        ana = (1.0 - EPS) ** spurious
        results.append((f"P(no spurious value), |Y|={card_Y}", ana, emp))


# ---------------------------------------------------------------------------
# Driver / reporting
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=2_000_000,
                        help="Monte Carlo trials per estimate (default 2e6).")
    parser.add_argument("--seed", type=int, default=20260608,
                        help="PRNG seed for reproducibility.")
    parser.add_argument("--tol", type=float, default=5e-3,
                        help="Abs-error tolerance for the PASS/FAIL flag.")
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    # Each entry: (name, analytical, empirical). The optional 4th field marks a
    # row as a DELIBERATE expected-mismatch demonstration (the independent model
    # the paper predicts is wrong): it is shown but excluded from the pass tally.
    results: list[tuple] = []

    print(f"Monte Carlo validation of bernoulli_relations Phase-C results")
    print(f"trials per estimate = {args.trials:,}   seed = {args.seed}")
    print(f"base rates: eps (FPR) = {EPS}, omega (FNR) = {OMEGA}, "
          f"tau (TPR) = {TAU}")
    print()

    validate_projection(rng, args.trials, results)
    validate_join(rng, args.trials, results)
    validate_symmetric_closure(rng, args.trials, results)
    validate_closure_dichotomy(rng, args.trials, results)
    validate_reflexive(rng, args.trials, results)
    validate_functional(rng, args.trials, results)

    # Pretty table.
    name_w = max(len(row[0]) for row in results)
    header = (f"{'result'.ljust(name_w)} | {'analytical':>12} | "
              f"{'empirical':>12} | {'abs error':>11} | flag")
    print(header)
    print("-" * len(header))
    worst = 0.0
    all_pass = True
    for row in results:
        name, ana, emp = row[0], row[1], row[2]
        is_demo = len(row) > 3 and row[3] == "demo"
        err = abs(ana - emp)
        if is_demo:
            # A predicted mismatch: large abs error is the POINT, not a failure.
            flag = "MISMATCH (expected)"
        else:
            worst = max(worst, err)
            ok = err <= args.tol
            all_pass = all_pass and ok
            flag = "PASS" if ok else "FAIL"
        print(f"{name.ljust(name_w)} | {ana:12.6f} | {emp:12.6f} | "
              f"{err:11.6f} | {flag}")
    print("-" * len(header))
    print(f"worst absolute error (fit rows only) = {worst:.6f}   "
          f"(tolerance {args.tol})   overall: "
          f"{'ALL PASS' if all_pass else 'SOME FAILED'}")
    print("note: the one MISMATCH row is the join independence-failure "
          "demonstration --")
    print("      the empirical P(both) matches the CORRELATED model, not the "
          "independent one.")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
