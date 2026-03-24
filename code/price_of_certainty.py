#!/usr/bin/env python3
"""
Monte Carlo simulations validating the Price of FPR Certainty theorem.

Three simulations:
  1. FPR distribution validation: KS test of adaptive FPR against Beta(p, m-p+1)
  2. Space comparison: theoretical curves for fixed vs adaptive BHF
  3. Salt length validation: empirical vs theoretical E[L] for fixed-threshold BHF

Usage:
    python3 code/price_of_certainty.py --seed 42 --outdir data/
"""

import argparse
import csv
import hashlib
import math
import os
import struct
from pathlib import Path

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def hash_to_int(x_bytes: bytes, salt: bytes, N: int) -> int:
    """SHA-256 hash of (x || salt) mod N."""
    digest = hashlib.sha256(x_bytes + salt).digest()
    # Use first 8 bytes as uint64, mod N
    val = struct.unpack(">Q", digest[:8])[0]
    return val % N


def int_to_bytes(i: int) -> bytes:
    """Encode integer as big-endian bytes (variable length)."""
    if i == 0:
        return b"\x00"
    length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, "big")


# ---------------------------------------------------------------------------
# Simulation 1: FPR distribution validation
# ---------------------------------------------------------------------------

def sim1_fpr_distribution(rng: np.random.Generator, outpath: Path):
    """Validate that adaptive FPR ~ Beta(p, m - p + 1)."""
    configs = [
        (50, 1),
        (50, 5),
        (100, 10),
        (200, 20),
    ]
    N = 10_000
    n_trials = 10_000

    rows = []
    for m, p in configs:
        fprs = []
        for trial in range(n_trials):
            # Draw m uniform hash values in [0, N-1]
            hashes = rng.integers(0, N, size=m)
            # Adaptive threshold: p-th order statistic (accepts p elements,
            # allows m-p false negatives)
            sorted_hashes = np.sort(hashes)
            t = int(sorted_hashes[p - 1])  # p-th smallest (0-indexed: p-1)
            # FPR = (t + 1) / N
            fpr = (t + 1) / N
            fprs.append(fpr)

        fprs = np.array(fprs)

        # Theoretical distribution: the p-th order statistic of m Uniform(0,1)
        # values follows Beta(p, m - p + 1).
        alpha_param = p
        beta_param = m - p + 1

        # KS test
        ks_stat, ks_pval = stats.kstest(fprs, "beta", args=(alpha_param, beta_param))

        # Theoretical moments
        theo_mean = alpha_param / (alpha_param + beta_param)
        theo_var = (alpha_param * beta_param) / (
            (alpha_param + beta_param) ** 2 * (alpha_param + beta_param + 1)
        )
        emp_mean = float(np.mean(fprs))
        emp_var = float(np.var(fprs, ddof=1))

        rows.append({
            "m": m,
            "p": p,
            "N": N,
            "n_trials": n_trials,
            "alpha": alpha_param,
            "beta": beta_param,
            "emp_mean": f"{emp_mean:.6f}",
            "theo_mean": f"{theo_mean:.6f}",
            "emp_var": f"{emp_var:.8f}",
            "theo_var": f"{theo_var:.8f}",
            "ks_stat": f"{ks_stat:.6f}",
            "ks_pval": f"{ks_pval:.6f}",
        })
        print(
            f"  Sim1 m={m}, p={p}: KS stat={ks_stat:.4f}, "
            f"p-val={ks_pval:.4f}, "
            f"mean={emp_mean:.4f} (theo {theo_mean:.4f})"
        )

    fieldnames = list(rows[0].keys())
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {outpath}")
    return rows


# ---------------------------------------------------------------------------
# Simulation 2: Space comparison (theoretical curves)
# ---------------------------------------------------------------------------

def sim2_space_comparison(outpath: Path):
    """Compute theoretical space curves for fixed vs adaptive BHF."""
    epsilons = [0.01, 0.05, 0.1]
    N = 100
    m_values = list(range(1, 201))

    rows = []
    for eps in epsilons:
        log2_inv_eps = -math.log2(eps)
        log2_N_bits = math.ceil(math.log2(N))
        overhead = 2 * log2_N_bits  # bits for (N, t)

        for m in m_values:
            # Fixed threshold: E[L] = m * log2(1/eps), total = E[L] + overhead
            fixed_salt = m * log2_inv_eps
            fixed_total = fixed_salt + overhead
            fixed_per_elem = fixed_total / m

            # Adaptive: just (N, t), no salt
            adaptive_total = overhead
            adaptive_per_elem = adaptive_total / m

            # Gap
            gap = fixed_total - adaptive_total  # = m * log2(1/eps)
            gap_per_elem = gap / m  # -> log2(1/eps) as m -> inf

            # Lower bound
            lower_bound = log2_inv_eps

            rows.append({
                "epsilon": eps,
                "m": m,
                "N": N,
                "log2_inv_eps": f"{log2_inv_eps:.4f}",
                "fixed_total_bits": f"{fixed_total:.2f}",
                "fixed_per_elem": f"{fixed_per_elem:.4f}",
                "adaptive_total_bits": f"{adaptive_total:.2f}",
                "adaptive_per_elem": f"{adaptive_per_elem:.4f}",
                "gap_bits": f"{gap:.2f}",
                "gap_per_elem": f"{gap_per_elem:.4f}",
                "lower_bound": f"{lower_bound:.4f}",
            })

    fieldnames = list(rows[0].keys())
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {outpath}")


# ---------------------------------------------------------------------------
# Simulation 3: Salt length validation
# ---------------------------------------------------------------------------

def sim3_salt_length(rng: np.random.Generator, outpath: Path):
    """Validate empirical salt lengths against theoretical E[L]."""
    configs = [
        (0.1, 1),
        (0.1, 2),
        (0.1, 3),
        (0.1, 4),
        (0.1, 5),
        (0.2, 1),
        (0.2, 2),
        (0.2, 3),
        (0.2, 4),
        (0.2, 5),
    ]
    N = 100
    n_reps = 500

    rows = []
    for eps, m in configs:
        t = max(0, round(eps * N) - 1)  # threshold: floor(eps * N) - 1
        actual_eps = (t + 1) / N
        p_success = actual_eps ** m  # probability a random salt works (mu=0)

        # Theoretical E[L] from geometric: E[Q] = 1/p, L = floor(log2(Q))
        # E[L] approx -log2(p) for small p
        theo_EQ = 1.0 / p_success
        theo_EL = -math.log2(p_success)  # leading-order approximation

        # Exact E[L] = sum_{n=1}^{inf} q^{2^n - 1} where q = 1 - p
        q = 1.0 - p_success
        exact_EL = 0.0
        for n in range(1, 200):
            exp = 2**n - 1
            term = q ** exp
            if term < 1e-15:
                break
            exact_EL += term

        # --- Hash-based BHF construction ---
        hash_salt_lengths = []
        for rep in range(n_reps):
            # Generate m random "elements" (unique per rep)
            elements = [f"elem_{rep}_{i}".encode() for i in range(m)]
            # Search for salt
            for salt_int in range(1, 10_000_000):
                salt = int_to_bytes(salt_int)
                # Check all elements pass threshold
                all_pass = True
                for elem in elements:
                    h = hash_to_int(elem, salt, N)
                    if h > t:
                        all_pass = False
                        break
                if all_pass:
                    salt_len = max(0, salt_int.bit_length() - 1)  # floor(log2(salt_int))
                    hash_salt_lengths.append(salt_len)
                    break

        hash_mean = float(np.mean(hash_salt_lengths)) if hash_salt_lengths else float("nan")
        hash_std = float(np.std(hash_salt_lengths, ddof=1)) if len(hash_salt_lengths) > 1 else float("nan")

        # --- Geometric mode ---
        geo_salt_lengths = []
        for _ in range(n_reps):
            # Draw Q ~ Geom(p_success)
            q_val = rng.geometric(p_success)
            L = max(0, int(math.floor(math.log2(q_val)))) if q_val >= 1 else 0
            geo_salt_lengths.append(L)

        geo_mean = float(np.mean(geo_salt_lengths))
        geo_std = float(np.std(geo_salt_lengths, ddof=1))

        rows.append({
            "epsilon": eps,
            "m": m,
            "N": N,
            "t": t,
            "actual_eps": f"{actual_eps:.4f}",
            "p_success": f"{p_success:.8f}",
            "n_reps": n_reps,
            "theo_EL_approx": f"{theo_EL:.4f}",
            "exact_EL": f"{exact_EL:.4f}",
            "hash_mean_L": f"{hash_mean:.4f}",
            "hash_std_L": f"{hash_std:.4f}",
            "geo_mean_L": f"{geo_mean:.4f}",
            "geo_std_L": f"{geo_std:.4f}",
            "hash_n_found": len(hash_salt_lengths),
        })
        print(
            f"  Sim3 eps={eps}, m={m}: "
            f"p={p_success:.6f}, "
            f"exact_EL={exact_EL:.2f}, "
            f"hash_mean={hash_mean:.2f}, "
            f"geo_mean={geo_mean:.2f}"
        )

    fieldnames = list(rows[0].keys())
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"  -> {outpath}")
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Price of FPR Certainty simulations"
    )
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    parser.add_argument(
        "--outdir", type=str, default="data/", help="Output directory for CSVs"
    )
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("=== Simulation 1: FPR distribution validation ===")
    sim1_rows = sim1_fpr_distribution(rng, outdir / "sim1_fpr_distribution.csv")

    # Check KS p-values
    for row in sim1_rows:
        pval = float(row["ks_pval"])
        if pval < 0.05:
            print(f"  WARNING: KS p-value {pval:.4f} < 0.05 for m={row['m']}, p={row['p']}")

    print("\n=== Simulation 2: Space comparison (theoretical) ===")
    sim2_space_comparison(outdir / "sim2_space_comparison.csv")

    print("\n=== Simulation 3: Salt length validation ===")
    sim3_salt_length(rng, outdir / "sim3_salt_length.csv")

    print("\nAll simulations complete.")


if __name__ == "__main__":
    main()
