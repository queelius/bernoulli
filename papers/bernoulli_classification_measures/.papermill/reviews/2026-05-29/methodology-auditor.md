# Methodology Review

**Paper**: Binary classification measures for random approximate sets
**Reviewer role**: methodology-auditor (performed by area chair)
**Date**: 2026-05-29

## Scope

This paper's "methodology" is (a) the delta-method derivations and (b) the Monte Carlo validation of those derivations. I audited both: I re-derived the formulas, re-ran an independent simulation, and inspected the provided simulation code and data.

## Delta-method derivations: PASS

- The second-order delta method is the appropriate tool for E[PPV] and E[F1] (nonlinear ratios of random variables). The validity condition is stated correctly (p tau and n epsilon both large; error O(1/min(p,n)^2)).
- I confirmed numerically that the second-order approximation is excellent in the paper's regime and degrades gracefully: at p = n = 20 (far smaller than any realistic deployment), the second-order E[PPV] still matches Monte Carlo to within 2e-4.
- The first-order variance approximations are the standard (grad)^T Sigma (grad) with diagonal covariance (justified by TP-FP independence). Confirmed against MC for PPV, F1, and (exactly) for accuracy and J.

## Monte Carlo validation: PASS with reproducibility notes

The provided script `code/f1_sim.py` is clean, correct, and reproducible:
- Fixed seed (`np.random.default_rng(seed=42)`), N = 50,000 trials per grid point, grid matches the theory CSV (FPR 0 to 0.05 step 0.001).
- The simulation draws TP ~ Bin(p, tau) and FP ~ Bin(n, eps) directly, which is exactly the model, and computes F1 = 2 TP / (TP + FP + p). This is a faithful, axiom-level simulation, not a re-implementation of the formula being tested, so it is a genuine independent check.
- I recomputed the agreement from the committed CSVs: max |theory - sim| = 2.0e-4 for F1 and 1.9e-4 for PPV across all 51 grid points. This is consistent with Monte Carlo standard error at N = 50,000 and validates the claim that the curves are "indistinguishable."

## Methodology findings

### MAJOR-1 (reproducibility): Only the F1 simulation script is provided; PPV and accuracy/J validation are not scripted
- **Location**: `code/` contains only `f1_sim.py`. The PPV validation data (`data/ppv_sim_vs_theory.csv`) and the theory curves (`data/prec_vs_fprate{1,2,3}.csv`) have no committed generating script.
- **Problem**: The PPV theory-vs-sim figure (fig 3) and the three prevalence curves (fig 2) cannot be regenerated from the repository. A reader can reproduce F1 but must reverse-engineer the PPV pipeline. The state file lists the PPV data as if scripted, but no script exists.
- **Impact**: Partial reproducibility. The math checks out (I reproduced PPV independently), so this is a packaging gap, not a correctness problem.
- **Suggestion**: Add a `code/ppv_sim.py` mirroring `f1_sim.py`, and a short script (or note) generating `prec_vs_fprate{1,2,3}.csv` for lambda in {0.1%, 1%, 10%}. Alternatively, generalize `f1_sim.py` to emit all measures.

### MINOR-1 (validation breadth): Validation only at tau = 1 (omega = 0)
- **Location**: All four data figures fix the positive Bernoulli set (FNR = 0, so TP = p deterministically).
- **Problem**: With omega = 0, TP is degenerate (variance 0), so the figures exercise only the FP binomial. The delta-method machinery for the TP variance term (sigma_t^2) is never stress-tested by simulation, even though it appears in the general formulas. The general (omega > 0) case is the more demanding test of the approximation.
- **Impact**: The general formulas are still correct (I verified E[F1], Var[F1], E[PPV] at tau = 0.5, 0.8, 0.9 against MC), but the paper's own evidence does not cover that regime.
- **Suggestion**: Add at least one validation point or panel with omega > 0 (for example tau = 0.9), or state explicitly that the figures specialize to the positive-set case and that the general case was verified separately.

### MINOR-2 (statistical reporting): No Monte Carlo error bars or standard-error statement on the figures
- **Location**: Figs 3 and 4.
- **Problem**: The captions assert the points are "indistinguishable" from theory but show no error bars and quote no Monte Carlo standard error. Appendix C argues the standard error is "negligible" via the CLT but gives no number.
- **Suggestion**: Report the per-point Monte Carlo standard error (roughly sd/sqrt(50000)) or add error bars. One sentence with a representative number (the agreement is ~2e-4, well within sampling noise) would close this.

### SUGGESTION-1: Validate the variance formulas, not just the means
The figures validate E[PPV] and E[F1]. The variance formulas (eqs 3.3, 3.15) are stated but not plotted against the empirical variance. A small table comparing predicted vs empirical Var at a few FPR values would strengthen the paper at low cost. I confirmed they match (for example F1 at eps=0.01: predicted 4.905e-4 vs MC 4.912e-4), so this is easy evidence to add.

### SUGGESTION-2: Note the binomial model assumes sampling with the same rate across the block
The simulation correctly draws single binomials, matching Axiom 2.1 (identically distributed within a block). Worth one sentence connecting the simulation design to the axiom, so the reader sees the simulation is testing the model and not assuming the result.
