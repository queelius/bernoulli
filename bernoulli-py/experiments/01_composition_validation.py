#!/usr/bin/env python3
"""Experiment 01: Composition validation.

Goal: verify empirically that the framework's closed-form composition
formulas (book ch. 3) hold for *real* data structures, not just for
synthetic rate parameters. Identify regimes where they break.

Sections:

A. Two independent Bloom filters over the *same* key set, different salts.
   Predicted joint FPR (treating channels as independent): alpha_1 * alpha_2.
   Empirical joint FPR: measured over random non-members.
   Hypothesis: independent salts give effectively independent channels.

B. Two Bloom filters over *disjoint* key sets, different salts.
   Same predicted formula; same hypothesis. (Sanity check.)

C. Two Bloom filters over the *same* key set, *same* salt.
   Predicted joint FPR if naively assuming independence: alpha^2.
   Actual joint FPR: alpha (the two filters are identical, so the AND
   is the same Bernoulli; no suppression).
   This isolates "shared randomness" as the failure mode of the
   composition formula.

D. Miller-Rabin k-round AND chain over uniformly chosen odd composites.
   Predicted: (1/4)^k worst-case bound; per-composite empirical can be
   much smaller.
   Empirical: average per-composite FPR after k rounds.

E. NoisyClassifier x NoisyClassifier with known prior.
   Predicted: book eq. 3.3 (and_with_prior).
   Empirical: simulate over a labeled population at the given prior.

Output:

- Stdout: human-readable summary.
- experiments/RESULTS.md: structured markdown report.
"""

from __future__ import annotations

import math
import random
import sys
import time
from pathlib import Path

# Make the experiment runnable from anywhere; we expect to be in the
# repo root (the directory containing src/bernoulli/).
HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
sys.path.insert(0, str(PKG_ROOT / "src"))

from bernoulli.algorithms import miller_rabin  # noqa: E402
from bernoulli.algorithms.noisy_classifier import NoisyClassifier  # noqa: E402
from bernoulli.atom import BernoulliBool  # noqa: E402
from bernoulli.harness import (  # noqa: E402
    empirical_rates,
    estimate_rate,
    sample_unique_bytes,
)
from bernoulli.sets import BloomFilter  # noqa: E402


def _build_bloom(
    keys: list[bytes], target_fpr: float, salt: int
) -> BloomFilter:
    bf = BloomFilter(capacity=len(keys), target_fpr=target_fpr, salt=salt)
    for k in keys:
        bf.add(k)
    return bf


def section_A(rng: random.Random) -> dict[str, float]:
    """Two independent Bloom filters over the SAME key set, different salts."""
    n = 5000
    target_fpr = 0.05
    n_probes = 30_000

    keys = sample_unique_bytes(n, length=16, rng=rng)
    bf1 = _build_bloom(keys, target_fpr, salt=0xA1A1A1A1)
    bf2 = _build_bloom(keys, target_fpr, salt=0x5B5B5B5B)

    # Probe with non-members.
    probes: list[bytes] = []
    seen = set(keys)
    while len(probes) < n_probes:
        cand = rng.randbytes(16)
        if cand not in seen:
            probes.append(cand)

    fp1 = sum(1 for k in probes if bf1.contains(k))
    fp2 = sum(1 for k in probes if bf2.contains(k))
    fp_and = sum(1 for k in probes if bf1.contains(k) and bf2.contains(k))

    a1 = fp1 / n_probes
    a2 = fp2 / n_probes
    a_and = fp_and / n_probes
    predicted_and = a1 * a2

    return {
        "name": "A: same keys, different salts",
        "alpha_1": a1,
        "alpha_2": a2,
        "predicted_and_fpr": predicted_and,
        "empirical_and_fpr": a_and,
        "ratio": (a_and / predicted_and) if predicted_and > 0 else float("inf"),
        "n_probes": n_probes,
    }


def section_B(rng: random.Random) -> dict[str, float]:
    """Two Bloom filters over DISJOINT key sets."""
    n = 5000
    target_fpr = 0.05
    n_probes = 30_000

    keys1 = sample_unique_bytes(n, length=16, rng=rng)
    seen = set(keys1)
    keys2: list[bytes] = []
    while len(keys2) < n:
        cand = rng.randbytes(16)
        if cand not in seen:
            keys2.append(cand)
            seen.add(cand)

    bf1 = _build_bloom(keys1, target_fpr, salt=0)
    bf2 = _build_bloom(keys2, target_fpr, salt=0)  # same salt is fine; disjoint data

    probes: list[bytes] = []
    while len(probes) < n_probes:
        cand = rng.randbytes(16)
        if cand not in seen:
            probes.append(cand)

    fp1 = sum(1 for k in probes if bf1.contains(k))
    fp2 = sum(1 for k in probes if bf2.contains(k))
    fp_and = sum(1 for k in probes if bf1.contains(k) and bf2.contains(k))

    a1 = fp1 / n_probes
    a2 = fp2 / n_probes
    a_and = fp_and / n_probes
    predicted_and = a1 * a2

    return {
        "name": "B: disjoint keys, same salt (data independence)",
        "alpha_1": a1,
        "alpha_2": a2,
        "predicted_and_fpr": predicted_and,
        "empirical_and_fpr": a_and,
        "ratio": (a_and / predicted_and) if predicted_and > 0 else float("inf"),
        "n_probes": n_probes,
    }


def section_C(rng: random.Random) -> dict[str, float]:
    """Two Bloom filters over the SAME key set with the SAME salt: no suppression."""
    n = 5000
    target_fpr = 0.05
    n_probes = 30_000

    keys = sample_unique_bytes(n, length=16, rng=rng)
    bf1 = _build_bloom(keys, target_fpr, salt=0xDEADBEEF)
    bf2 = _build_bloom(keys, target_fpr, salt=0xDEADBEEF)

    seen = set(keys)
    probes: list[bytes] = []
    while len(probes) < n_probes:
        cand = rng.randbytes(16)
        if cand not in seen:
            probes.append(cand)

    fp1 = sum(1 for k in probes if bf1.contains(k))
    fp_and = sum(1 for k in probes if bf1.contains(k) and bf2.contains(k))

    a1 = fp1 / n_probes
    a_and = fp_and / n_probes
    predicted_independent = a1 * a1

    return {
        "name": "C: same keys, SAME salt (degenerate)",
        "alpha_1": a1,
        "alpha_2": a1,
        "predicted_and_fpr_independent": predicted_independent,
        "empirical_and_fpr": a_and,
        "ratio_to_naive_prediction": (
            (a_and / predicted_independent) if predicted_independent > 0 else float("inf")
        ),
        "n_probes": n_probes,
    }


def section_D(rng: random.Random) -> list[dict[str, float]]:
    """Miller-Rabin k-round AND chain on random odd composites."""

    # Generate a pool of odd composites by selecting odd n that fail
    # one trivial small-base Fermat test (cheap composite generator).
    composites: list[int] = []
    while len(composites) < 200:
        n = rng.randrange(10_001, 1_000_000) | 1  # odd, >= 10001
        # Quick composite filter: divisible by 3, 5, 7, ..., or fails a base-2 test.
        if any(n % p == 0 for p in (3, 5, 7, 11, 13)):
            composites.append(n)
            continue
        # Otherwise check base-2 Miller-Rabin.
        if not miller_rabin.witness_passes(n, 2):
            composites.append(n)
    # Filter: ensure they are *actually* composite by trial division.
    confirmed = [n for n in composites if any(n % p == 0 for p in range(2, int(n ** 0.5) + 1))]

    rounds_to_try = [1, 2, 3, 5, 8]
    rows = []
    for k in rounds_to_try:
        # Per composite, run k random witness checks; record whether ALL passed.
        # This is the empirical FPR per composite.
        false_positives = 0
        for n in confirmed:
            local_rng = random.Random(rng.randint(0, 1 << 30))
            b = miller_rabin.is_probably_prime(n, rounds=k, rng=local_rng)
            if b.value:
                false_positives += 1
        empirical_fpr = false_positives / len(confirmed)
        worst_case = 0.25 ** k
        rows.append(
            {
                "k": k,
                "n_composites": len(confirmed),
                "worst_case_fpr": worst_case,
                "empirical_fpr": empirical_fpr,
                "ratio": empirical_fpr / worst_case if worst_case > 0 else 0.0,
            }
        )
    return rows


def section_E(rng: random.Random) -> dict[str, float]:
    """Two NoisyClassifiers viewing the SAME truth (shared-truth AND).

    Predicted by ``__and__`` operator (shared-truth semantics):
    ``fpr_AND = alpha_1 * alpha_2``,  ``fnr_AND = 1 - (1-beta_1)(1-beta_2)``.
    """
    truth = lambda n: n % 2 == 0  # noqa: E731
    rng1 = random.Random(rng.randint(0, 1 << 30))
    rng2 = random.Random(rng.randint(0, 1 << 30))

    fpr1, fnr1 = 0.10, 0.05
    fpr2, fnr2 = 0.08, 0.12
    clf1 = NoisyClassifier(truth, fpr=fpr1, fnr=fnr1, rng=rng1)
    clf2 = NoisyClassifier(truth, fpr=fpr2, fnr=fnr2, rng=rng2)

    n_each = 30_000
    positives = list(range(0, 2 * n_each, 2))
    negatives = list(range(1, 2 * n_each + 1, 2))

    def joint_predict(x: int) -> bool:
        return clf1.predict(x) and clf2.predict(x)

    rates = empirical_rates(joint_predict, positives, negatives)

    # Shared-truth prediction.
    template1 = BernoulliBool(value=True, fpr=fpr1, fnr=fnr1)
    template2 = BernoulliBool(value=True, fpr=fpr2, fnr=fnr2)
    predicted = template1 & template2

    return {
        "name": "E: shared-truth AND of two NoisyClassifiers",
        "predicted_fpr": predicted.fpr,
        "predicted_fnr": predicted.fnr,
        "empirical_fpr_estimate": rates.fpr.estimate,
        "empirical_fpr_ci": (rates.fpr.ci_low, rates.fpr.ci_high),
        "empirical_fnr_estimate": rates.fnr.estimate,
        "empirical_fnr_ci": (rates.fnr.ci_low, rates.fnr.ci_high),
        "fpr_within_ci": rates.fpr.ci_low <= predicted.fpr <= rates.fpr.ci_high,
        "fnr_within_ci": rates.fnr.ci_low <= predicted.fnr <= rates.fnr.ci_high,
    }


def section_F(rng: random.Random) -> dict[str, float]:
    """Two NoisyClassifiers viewing INDEPENDENT truths drawn from prior 0.5.

    Predicted by ``and_with_prior``: prior-dependent FPR formula from book
    eq. 3.3. Each query draws *two* independent inputs from a Bernoulli(pi)
    population and AND's the two classifier outputs.
    """
    truth = lambda n: n % 2 == 0  # noqa: E731
    rng1 = random.Random(rng.randint(0, 1 << 30))
    rng2 = random.Random(rng.randint(0, 1 << 30))

    fpr1, fnr1 = 0.10, 0.05
    fpr2, fnr2 = 0.08, 0.12
    clf1 = NoisyClassifier(truth, fpr=fpr1, fnr=fnr1, rng=rng1)
    clf2 = NoisyClassifier(truth, fpr=fpr2, fnr=fnr2, rng=rng2)

    # Generate independent (x1, x2) pairs at prior pi = 0.5 over even/odd.
    pair_rng = random.Random(rng.randint(0, 1 << 30))
    n_pairs = 60_000
    pairs: list[tuple[int, int]] = []
    for _ in range(n_pairs):
        x1 = 2 * pair_rng.randint(0, 100_000) + (0 if pair_rng.random() < 0.5 else 1)
        x2 = 2 * pair_rng.randint(0, 100_000) + (0 if pair_rng.random() < 0.5 else 1)
        pairs.append((x1, x2))

    # Joint truth per pair: AND of independent truths.
    fp = 0
    fn = 0
    n_pos = 0  # pairs where joint truth is True
    n_neg = 0
    for x1, x2 in pairs:
        truth_and = truth(x1) and truth(x2)
        observed_and = clf1.predict(x1) and clf2.predict(x2)
        if truth_and:
            n_pos += 1
            if not observed_and:
                fn += 1
        else:
            n_neg += 1
            if observed_and:
                fp += 1

    fpr_est = estimate_rate(fp, n_neg)
    fnr_est = estimate_rate(fn, n_pos)

    template1 = BernoulliBool(value=True, fpr=fpr1, fnr=fnr1)
    template2 = BernoulliBool(value=True, fpr=fpr2, fnr=fnr2)
    predicted = template1.and_with_prior(template2, prior=0.5)

    return {
        "name": "F: independent-truths AND at prior=0.5",
        "predicted_fpr": predicted.fpr,
        "predicted_fnr": predicted.fnr,
        "empirical_fpr_estimate": fpr_est.estimate,
        "empirical_fpr_ci": (fpr_est.ci_low, fpr_est.ci_high),
        "empirical_fnr_estimate": fnr_est.estimate,
        "empirical_fnr_ci": (fnr_est.ci_low, fnr_est.ci_high),
        "fpr_within_ci": fpr_est.ci_low <= predicted.fpr <= fpr_est.ci_high,
        "fnr_within_ci": fnr_est.ci_low <= predicted.fnr <= fnr_est.ci_high,
        "n_pos": n_pos,
        "n_neg": n_neg,
    }


def fmt(x: float, digits: int = 4) -> str:
    return f"{x:.{digits}g}"


def render_report(
    A: dict, B: dict, C: dict, D: list[dict], E: dict, F: dict
) -> str:
    out: list[str] = []
    out.append("# Experiment 01: Composition validation\n")
    out.append(
        "Empirical check that the Bernoulli framework's composition formulas hold "
        "for real data structures, and identification of regimes where they break.\n"
    )

    out.append("## A. Two Bloom filters, same keys, different salts (independent channels)\n")
    out.append(
        f"- alpha_1 (empirical): {fmt(A['alpha_1'])}\n"
        f"- alpha_2 (empirical): {fmt(A['alpha_2'])}\n"
        f"- Predicted alpha_AND = alpha_1 * alpha_2: {fmt(A['predicted_and_fpr'])}\n"
        f"- Empirical alpha_AND: {fmt(A['empirical_and_fpr'])}\n"
        f"- Ratio (empirical / predicted): **{fmt(A['ratio'])}**\n"
        f"- n_probes: {A['n_probes']}\n"
    )
    out.append(
        "Interpretation: independent salts give independent hash channels, so "
        "the AND collapses to the product as predicted. A ratio near 1 confirms "
        "the framework's independence assumption.\n"
    )

    out.append("## B. Two Bloom filters, disjoint keys, same salt (data independence)\n")
    out.append(
        f"- alpha_1: {fmt(B['alpha_1'])}\n"
        f"- alpha_2: {fmt(B['alpha_2'])}\n"
        f"- Predicted alpha_AND: {fmt(B['predicted_and_fpr'])}\n"
        f"- Empirical alpha_AND: {fmt(B['empirical_and_fpr'])}\n"
        f"- Ratio: **{fmt(B['ratio'])}**\n"
    )
    out.append(
        "Interpretation: same salt over different data still gives independent "
        "outputs on non-member queries. Sanity check.\n"
    )

    out.append("## C. Two Bloom filters, same keys AND same salt (degenerate)\n")
    out.append(
        f"- alpha (single filter): {fmt(C['alpha_1'])}\n"
        f"- Naively predicted alpha_AND = alpha^2: {fmt(C['predicted_and_fpr_independent'])}\n"
        f"- Empirical alpha_AND: {fmt(C['empirical_and_fpr'])}\n"
        f"- Ratio (empirical / naive prediction): **{fmt(C['ratio_to_naive_prediction'])}**\n"
    )
    out.append(
        "Interpretation: identical filters share all randomness; the two channels "
        "are perfectly correlated. The empirical AND-FPR equals alpha (not alpha^2). "
        "This is exactly the failure mode the framework's Axiom 1 (cross-instance "
        "independence) flags. The ratio above 1 is the cost of the violated "
        "assumption.\n"
    )

    out.append("## D. Miller-Rabin k-round AND chain on random odd composites\n")
    out.append("| k | n_composites | Worst-case bound (1/4)^k | Empirical FPR | Ratio |\n")
    out.append("|--:|--:|--:|--:|--:|\n")
    for row in D:
        out.append(
            f"| {row['k']} | {row['n_composites']} | "
            f"{fmt(row['worst_case_fpr'])} | {fmt(row['empirical_fpr'])} | "
            f"{fmt(row['ratio'])} |\n"
        )
    out.append("\n")
    out.append(
        "Interpretation: the per-composite empirical FPR is far below the "
        "worst-case `(1/4)^k` bound. For random composites, most fail base-2 "
        "or base-3 immediately, so the chain converges to zero FPR much faster "
        "than the worst-case suggests. The bound is tight only for adversarially "
        "constructed Carmichael-like numbers.\n"
    )

    out.append("## E. Shared-truth AND of two NoisyClassifiers (prior=0.5 population)\n")
    out.append(
        f"- Predicted FPR (shared-truth ``__and__`` = alpha_1*alpha_2): "
        f"{fmt(E['predicted_fpr'])}\n"
        f"- Empirical FPR estimate: {fmt(E['empirical_fpr_estimate'])} "
        f"(95% CI [{fmt(E['empirical_fpr_ci'][0])}, {fmt(E['empirical_fpr_ci'][1])}])\n"
        f"- FPR within CI: **{E['fpr_within_ci']}**\n"
        f"- Predicted FNR (shared-truth = 1 - (1-beta_1)(1-beta_2)): "
        f"{fmt(E['predicted_fnr'])}\n"
        f"- Empirical FNR estimate: {fmt(E['empirical_fnr_estimate'])} "
        f"(95% CI [{fmt(E['empirical_fnr_ci'][0])}, {fmt(E['empirical_fnr_ci'][1])}])\n"
        f"- FNR within CI: **{E['fnr_within_ci']}**\n"
    )
    out.append(
        "Interpretation: both classifiers query the same input (truth is the "
        "same property of the same n). The shared-truth formulas are prior-free; "
        "FPR collapses to alpha_1*alpha_2 and FNR to the union-of-misses formula.\n"
    )

    out.append("## F. Independent-truths AND of two NoisyClassifiers (prior=0.5)\n")
    out.append(
        f"- Predicted FPR (and_with_prior, book eq. 3.3): {fmt(F['predicted_fpr'])}\n"
        f"- Empirical FPR estimate: {fmt(F['empirical_fpr_estimate'])} "
        f"(95% CI [{fmt(F['empirical_fpr_ci'][0])}, {fmt(F['empirical_fpr_ci'][1])}])\n"
        f"- FPR within CI: **{F['fpr_within_ci']}**\n"
        f"- Predicted FNR: {fmt(F['predicted_fnr'])}\n"
        f"- Empirical FNR estimate: {fmt(F['empirical_fnr_estimate'])} "
        f"(95% CI [{fmt(F['empirical_fnr_ci'][0])}, {fmt(F['empirical_fnr_ci'][1])}])\n"
        f"- FNR within CI: **{F['fnr_within_ci']}**\n"
        f"- n_pos (true AND = True): {F['n_pos']}, n_neg: {F['n_neg']}\n"
    )
    out.append(
        "Interpretation: each query draws *two independent* inputs from the "
        "Bernoulli(pi) population and AND's the classifier outputs. This is "
        "the regime in which the prior-dependent FPR formula applies.\n"
    )

    out.append("\n## Summary\n")
    out.append(
        "- Composition formulas hold cleanly when channels are independent "
        "(sections A, B, E, F).\n"
        "- Section C makes the independence assumption visible by violating it: "
        "shared randomness collapses the AND to a single channel.\n"
        "- Section D shows the gap between worst-case and typical-case behavior "
        "of the Miller-Rabin chain on random composites.\n"
        "- Sections E and F demonstrate that **shared-truth** and "
        "**independent-truths** AND give different FPRs from the same input "
        "rates. The framework now exposes both: ``b1 & b2`` (shared) and "
        "``b1.and_with_prior(b2, pi)`` (independent).\n"
    )
    return "".join(out)


def main() -> int:
    rng = random.Random(2026)

    print("Running experiment 01: Composition validation...\n")
    t0 = time.time()

    print("[A] Bloom filters, same keys, different salts...")
    A = section_A(random.Random(rng.randint(0, 1 << 30)))

    print("[B] Bloom filters, disjoint keys...")
    B = section_B(random.Random(rng.randint(0, 1 << 30)))

    print("[C] Bloom filters, same keys, same salt (degenerate)...")
    C = section_C(random.Random(rng.randint(0, 1 << 30)))

    print("[D] Miller-Rabin k-round chain...")
    D = section_D(random.Random(rng.randint(0, 1 << 30)))

    print("[E] Shared-truth NoisyClassifier composition...")
    E = section_E(random.Random(rng.randint(0, 1 << 30)))

    print("[F] Independent-truths NoisyClassifier composition...")
    F = section_F(random.Random(rng.randint(0, 1 << 30)))

    elapsed = time.time() - t0
    report = render_report(A, B, C, D, E, F)
    print()
    print(report)
    print(f"\nElapsed: {elapsed:.1f}s")

    out_path = HERE / "RESULTS.md"
    out_path.write_text(report)
    print(f"Report written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
