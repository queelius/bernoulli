#!/usr/bin/env python3
"""Validate the correlated-parity proposition (sec:crosstalk) and its first-order
reading, and generate the numbers for the crosstalk table (sec:worked-crosstalk).

The proposition: for flip indicators F_i with means r_i, pairwise covariances
c_ij, and biases mu_i = 1 - 2 r_i, the parity-flip probability is

    P = 1/2 (1 - E prod S_i),   S_i = 1 - 2 F_i,
    E prod S_i = prod mu_i + 4 sum_{i<j} c_ij prod_{k not in {i,j}} mu_k + R,

where R collects central cross-moments of order >= 3. Dropping R gives the
first-order rate; for n = 2 the remainder is empty and the formula is exact.

Two contrasting dependence structures, both with exact closed/enumerable truth:

1. CHAIN crosstalk (pairwise-dominated): shared flip-causes C_e ~ Bern(lambda)
   on edges e = (i, i+1); F_i = B_i OR (any incident C_e), B_i ~ Bern(eps_i).
   Adjacent covariances are O(lambda), all higher central cross-moments are
   O(lambda^2), so the first-order formula should track the exact value with
   O(lambda^2) error. This is the physically typical regime: readout crosstalk
   between neighboring resonators is dominantly pairwise.

2. GLOBAL common cause (all-order): one C ~ Bern(lambda) ORs into every bit.
   Every central cross-moment is O(lambda) (|m_T| ~ lambda 2^|T|), so the
   first-order formula fails at every lambda, while the exact expansion (all
   terms) and the direct closed form agree. This shows the first-order regime
   is about the dependence STRUCTURE, not just the correlation strength.

Exact truths are computed by conditioning on the cause configuration (2^(n-1)
configs for the chain, 2 for the global model): given the causes, bits are
independent and the parity formula of Theorem (Parity) applies per config.

Run: python3 crosstalk_validation.py   (numpy only; ~20 s for the MC confirm)
"""
import itertools
import numpy as np

# ibm_hanoi 2025-02-26 cold-word rates (eps_i) for the first 8 qubits; see
# readout_figure.py for the full snapshot and provenance. Invariant: EPS8 must
# equal the eps column of the first 8 entries of readout_figure.RATES (manual
# copies of the same snapshot; keep them in sync).
EPS8 = np.array([0.0086, 0.0072, 0.0064, 0.0096, 0.0054, 0.0040, 0.0160, 0.0092])


def parity_flip_indep(rates):
    """Theorem (Parity): 1/2 (1 - prod (1 - 2 r_i))."""
    return 0.5 * (1.0 - np.prod(1.0 - 2.0 * np.asarray(rates)))


def first_order(r, C):
    """First-order correlated parity: independent value minus
    2 sum_{i<j} c_ij prod_{k not in {i,j}} mu_k  (proposition, R dropped)."""
    r = np.asarray(r)
    mu = 1.0 - 2.0 * r
    n = len(r)
    corr = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            others = [k for k in range(n) if k not in (i, j)]
            corr += C[i, j] * np.prod(mu[others])
    return parity_flip_indep(r) - 2.0 * corr


# ----------------------------------------------------------------------
# exact two-bit identity: P = 1/2 (1 - mu1 mu2) - 2 c, checked by enumeration
# over a grid of (r1, r2, c) including the Frechet covariance bounds.
# ----------------------------------------------------------------------
def check_two_bit():
    worst = 0.0
    for r1 in (0.01, 0.1, 0.3, 0.5, 0.8):
        for r2 in (0.02, 0.25, 0.6):
            lo = max(0.0, r1 + r2 - 1.0) - r1 * r2   # Frechet lower bound on c
            hi = min(r1, r2) - r1 * r2               # Frechet upper bound on c
            for c in (lo, 0.5 * lo, 0.0, 0.5 * hi, hi):
                p11 = r1 * r2 + c
                p10, p01 = r1 - p11, r2 - p11
                exact = p10 + p01                     # P(F1 xor F2 = 1)
                formula = 0.5 * (1 - (1 - 2 * r1) * (1 - 2 * r2)) - 2 * c
                worst = max(worst, abs(exact - formula))
    print(f"two-bit identity, worst |enumeration - formula| over grid: {worst:.2e}")
    assert worst < 1e-12


# ----------------------------------------------------------------------
# chain crosstalk model
# ----------------------------------------------------------------------
def chain_exact(eps, lam):
    """Exact parity-flip probability by conditioning on the 2^(n-1) edge-cause
    configurations: given the causes, a bit with an active incident edge is
    forced to flip; the rest flip independently at eps_i."""
    n = len(eps)
    total = 0.0
    for cfg in itertools.product((0, 1), repeat=n - 1):
        w = np.prod([lam if c else 1 - lam for c in cfg])
        forced = [i for i in range(n)
                  if (i > 0 and cfg[i - 1]) or (i < n - 1 and (i < len(cfg) and cfg[i]))]
        free = [i for i in range(n) if i not in forced]
        # parity of forced ones XOR parity of free flips
        p_free = parity_flip_indep(eps[free]) if free else 0.0
        if len(forced) % 2 == 0:
            total += w * p_free
        else:
            total += w * (1.0 - p_free)
    return total


def chain_marginals_cov(eps, lam):
    """Closed-form marginals and pairwise covariances of the chain model."""
    n = len(eps)
    deg = np.array([1 if i in (0, n - 1) else 2 for i in range(n)])
    r = 1.0 - (1.0 - eps) * (1.0 - lam) ** deg
    C = np.zeros((n, n))
    for i in range(n - 1):
        j = i + 1
        p00 = (1 - eps[i]) * (1 - eps[j]) * (1 - lam) ** (deg[i] + deg[j] - 1)
        C[i, j] = C[j, i] = p00 - (1 - r[i]) * (1 - r[j])
    return r, C


def chain_mc(eps, lam, N, rng):
    n = len(eps)
    causes = rng.random((N, n - 1)) < lam
    flips = rng.random((N, n)) < eps
    forced = np.zeros((N, n), dtype=bool)
    forced[:, 1:] |= causes
    forced[:, :-1] |= causes
    F = flips | forced
    return (F.sum(axis=1) % 2).mean()


# ----------------------------------------------------------------------
# global common-cause model
# ----------------------------------------------------------------------
def global_exact(eps, lam):
    n = len(eps)
    return (1 - lam) * parity_flip_indep(eps) + lam * (n % 2)


def global_marginals_cov(eps, lam):
    n = len(eps)
    r = 1.0 - (1.0 - eps) * (1.0 - lam)
    C = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            p00 = (1 - eps[i]) * (1 - eps[j]) * (1 - lam)
            C[i, j] = C[j, i] = p00 - (1 - r[i]) * (1 - r[j])
    return r, C


def main():
    check_two_bit()
    rng = np.random.default_rng(11)
    N = 2_000_000

    print("\nCHAIN crosstalk (pairwise-dominated), n=8, ibm_hanoi cold rates")
    print(f"{'lambda':>8} {'P_indep':>9} {'P_first':>9} {'P_exact':>9} "
          f"{'fo_err':>9} {'P_MC':>9}")
    for lam in (0.001, 0.005, 0.01, 0.02, 0.05):
        r, C = chain_marginals_cov(EPS8, lam)
        pi = parity_flip_indep(r)
        pf = first_order(r, C)
        pe = chain_exact(EPS8, lam)
        pm = chain_mc(EPS8, lam, N, rng)
        assert abs(pm - pe) < 5 * np.sqrt(pe * (1 - pe) / N) + 1e-9, "MC vs exact"
        print(f"{lam:8.3f} {pi:9.5f} {pf:9.5f} {pe:9.5f} {abs(pf-pe):9.2e} {pm:9.5f}")

    print("\nGLOBAL common cause (all-order dependence), n=8, same rates")
    print(f"{'lambda':>8} {'P_indep':>9} {'P_first':>9} {'P_exact':>9} {'fo_err':>9}")
    for lam in (0.001, 0.005, 0.01, 0.02, 0.05):
        r, C = global_marginals_cov(EPS8, lam)
        pi = parity_flip_indep(r)
        pf = first_order(r, C)
        pe = global_exact(EPS8, lam)
        print(f"{lam:8.3f} {pi:9.5f} {pf:9.5f} {pe:9.5f} {abs(pf-pe):9.2e}")

    print("\nSign check (chain, lambda=0.01): exact below independent anchor:",
          chain_exact(EPS8, 0.01) < parity_flip_indep(chain_marginals_cov(EPS8, 0.01)[0]))

    # odd-n strong-correlation sign reversal of the GLOBAL model: positive
    # covariance RAISES the parity error once higher cumulants dominate.
    eps9 = np.append(EPS8, 0.0092)
    for lam in (0.1, 0.5):
        r, _ = global_marginals_cov(eps9, lam)
        print(f"global n=9 lambda={lam}: exact={global_exact(eps9, lam):.4f} "
              f"indep={parity_flip_indep(r):.4f}")


if __name__ == "__main__":
    main()
