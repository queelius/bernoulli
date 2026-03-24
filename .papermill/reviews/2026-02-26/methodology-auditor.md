# Methodology Auditor Report

**Date**: 2026-02-26
**Paper**: Bernoulli sets: a model for sets with random errors

## Summary

This is a theoretical mathematics/CS paper. Methodology assessment focuses on the axiomatic framework design, the proof techniques, the assumptions' realism, and the computational/empirical validation.

## Axiomatic Framework

### Axiom Adequacy
The two axioms (element-wise independence, conditional independence of block rates) are reasonable and well-motivated. They capture the essential behavior of Bloom filters and related structures.

**Strength**: The axiom economy remark (Remark 3.2) is excellent -- clearly delineating which results depend on which axioms.

**Weakness**: As noted by the logic checker, the axioms as stated are *necessary but not sufficient* for the model. The paper implicitly assumes identical distribution within each partition block (not just independence). This should be an explicit axiom or stated assumption.

### Assumption Realism
The paper acknowledges limitations in the conclusion: element-wise independence excludes locality-sensitive hashing, and the finite universal set assumption excludes continuous sample spaces. These are appropriate caveats.

However, two assumptions deserve more discussion:

1. **Independence across Bernoulli sets**: The union/intersection theorems assume that the errors of $\tilde{A}_1$ and $\tilde{A}_2$ are independent. This is stated in the proofs ("by the independence of errors across the two Bernoulli sets") but never as a formal assumption. In practice, two Bloom filters built from the same hash family may have correlated errors. This assumption should be explicitly stated and discussed.

2. **Known cardinalities**: The error-rate formulas for union, intersection, and set difference require knowledge of the partition sizes (e.g., $|A_1 \cap A_2|$, $|A_1 \setminus A_2|$). In practice, these are often unknown. The paper should discuss this limitation more prominently -- the formulas are exact given the partition sizes, but in applications one may need to estimate or bound these quantities.

## Proof Techniques

The proofs use standard techniques: law of total probability, binomial distribution properties, Taylor expansion, central limit theorem, Hoeffding's inequality. These are all appropriate.

The Taylor expansion approach for PPV (Theorem 4.7) is reasonable but should state when the approximation is valid. For small $p$ or large $\varepsilon$, the binomial distributions may not be well-approximated near their means.

## Computational Validation

The paper includes:
- Monte Carlo simulations (code/ppv.cpp, bin_class_measures_sim.cpp) that generated the CSV data files
- Numerical examples (Example 5.1 with concrete calculations)
- Plots (6 figures)

This is good practice. However:

### Issue M1: No systematic comparison of theoretical predictions to simulation
**Severity**: Major
**Problem**: The paper has simulation code and derived theoretical formulas, but never explicitly compares them. For instance, Figure 1 shows a histogram of simulated PPV values, but does not overlay the theoretical distribution. Figure 3 (PPV vs FPR) uses computed data but doesn't state whether these are theoretical or simulated values. A rigorous validation paper would show that the theoretical predictions match simulation within statistical tolerance.
**Suggestion**: Add at least one figure or table showing: (1) simulated error rates for union/intersection operations, (2) the theoretical predictions from the formulas, (3) the deviation. This would significantly strengthen confidence in the results.

### Issue M2: Figure data provenance unclear
**Severity**: Minor
**Problem**: The 17 CSV files in data/ are used by the plots but there is no documentation of how they were generated. Were they from simulation or analytical computation? What parameters were used?
**Suggestion**: Add a brief note in the paper or a README in the data directory explaining how each dataset was generated.

## Statistical Rigor

### Confidence Intervals
The confidence interval formulas (eqs 4.7, 4.8) use the normal approximation. This is standard but has known issues for rates near 0 or 1 and for small sample sizes. The Wilson interval or Clopper-Pearson interval would be more appropriate in edge cases. This is a minor point since the paper presents these as asymptotic results.

### Maximum Entropy Claim
The paper states: "The Bernoulli set model is the maximum entropy distribution over $\{0,1\}^u$ subject to the constraint that each element has a fixed marginal error probability." This is a true statement about the binomial distribution but should cite the specific result or provide a brief justification beyond the parenthetical reference to Cover & Thomas.

## Reproducibility

**Strengths**:
- The paper is self-contained: all definitions, axioms, and proofs are provided
- Supporting code exists (C++ simulations, R scripts, Mathematica notebooks)
- CSV data is included for all plots

**Weaknesses**:
- No instructions for running the simulations
- No specification of random seeds or number of trials
- The research/ directory contains computational artifacts but no documentation

## Summary of Findings

| Finding | Severity |
|---------|----------|
| Independence across Bernoulli sets unstated | Major |
| Known cardinalities assumption underdiscussed | Major |
| No theory-vs-simulation comparison | Major |
| Data provenance unclear | Minor |
| i.i.d. assumption implicit | Major (shared with logic-checker) |
| Confidence interval approximation limitations | Minor |
