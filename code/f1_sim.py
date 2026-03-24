"""
Monte Carlo simulation of the F1-score for the Bernoulli set model.

Generates two CSV files:
  - data/f1_theory.csv:        theoretical E[F1] via second-order delta method
  - data/f1_sim_vs_theory.csv: Monte Carlo sample means for validation

Parameters match the PPV validation figure: p=100, n=9900, fnrate=0.
"""

import numpy as np
import csv
import os

# Fixed parameters
P = 100        # positives
N = 9900       # negatives
FNRATE = 0.0   # false negative rate (positive Bernoulli set)
TPRATE = 1.0 - FNRATE
N_SIM = 50_000 # Monte Carlo trials per fprate value

# FPR grid: matches prec_vs_fprate2.csv (0 to 0.05, step 0.001)
fprates = np.arange(0.0, 0.051, 0.001)


def f1_theory(fprate, tprate, p, n):
    """Second-order delta method approximation of E[F1].

    F1 = 2*TP / (2*TP + FP + FN) = 2*TP / (TP + FP + p)
         (using FN = p - TP)

    Let h(t, f) = 2t / (t + f + p).  Then F1 = h(TP_p, FP_n).

    Gradient at means (t_bar, f_bar):
        dh/dt = 2(f + p) / (t + f + p)^2
        dh/df = -2t / (t + f + p)^2

    Hessian:
        d2h/dt2 = -2*2*(f+p) / (t+f+p)^3
        d2h/df2 =  2*2*t / (t+f+p)^3
        d2h/dtdf = 2*(t - f - p) / (t+f+p)^3

    E[h] ≈ h(t_bar, f_bar) + (1/2) * tr(H * Sigma)
    where Sigma = diag(sigma_t^2, sigma_f^2).
    """
    t_bar = p * tprate
    f_bar = n * fprate
    s = t_bar + f_bar + p  # denominator

    if s == 0:
        return 0.0

    # Zeroth-order term
    h0 = 2 * t_bar / s

    # Variances of TP_p ~ Bin(p, tprate) and FP_n ~ Bin(n, fprate)
    var_t = p * tprate * (1 - tprate)
    var_f = n * fprate * (1 - fprate)

    # Second-order correction: (1/2) * (H_tt * var_t + H_ff * var_f)
    h_tt = -4 * (f_bar + p) / s**3
    h_ff = 4 * t_bar / s**3

    correction = 0.5 * (h_tt * var_t + h_ff * var_f)
    return h0 + correction


def f1_variance(fprate, tprate, p, n):
    """First-order delta method variance of F1.

    Var[F1] ≈ (∇h)^T Σ (∇h)
    """
    t_bar = p * tprate
    f_bar = n * fprate
    s = t_bar + f_bar + p

    if s == 0:
        return 0.0

    var_t = p * tprate * (1 - tprate)
    var_f = n * fprate * (1 - fprate)

    dh_dt = 2 * (f_bar + p) / s**2
    dh_df = -2 * t_bar / s**2

    return dh_dt**2 * var_t + dh_df**2 * var_f


def f1_simulate(fprate, tprate, p, n, n_sim, rng):
    """Monte Carlo estimate of E[F1]."""
    tp = rng.binomial(p, tprate, size=n_sim)
    fp = rng.binomial(n, fprate, size=n_sim)

    denom = tp + fp + p  # = 2*tp + fp + fn since fn = p - tp
    # Avoid division by zero (only possible if p=0 and fprate=0)
    with np.errstate(invalid='ignore'):
        f1 = np.where(denom > 0, 2.0 * tp / denom, 0.0)
    return float(np.mean(f1))


def main():
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

    rng = np.random.default_rng(seed=42)

    # Theory curve
    theory_path = os.path.join(out_dir, 'f1_theory.csv')
    with open(theory_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for fpr in fprates:
            ef1 = f1_theory(fpr, TPRATE, P, N)
            writer.writerow([round(fpr, 6), ef1])

    # Simulation vs theory
    sim_path = os.path.join(out_dir, 'f1_sim_vs_theory.csv')
    with open(sim_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for fpr in fprates:
            mean_f1 = f1_simulate(fpr, TPRATE, P, N, N_SIM, rng)
            writer.writerow([round(fpr, 6), mean_f1])

    print(f"Wrote {theory_path}")
    print(f"Wrote {sim_path}")

    # Quick validation: compare at fpr=0.01
    fpr_check = 0.01
    theo = f1_theory(fpr_check, TPRATE, P, N)
    sim = f1_simulate(fpr_check, TPRATE, P, N, 200_000, rng)
    print(f"\nValidation at fprate={fpr_check}:")
    print(f"  Theory:     {theo:.6f}")
    print(f"  Simulation: {sim:.6f}")
    print(f"  Difference: {abs(theo - sim):.6f}")


if __name__ == '__main__':
    main()
