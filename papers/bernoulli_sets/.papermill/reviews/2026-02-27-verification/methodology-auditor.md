# Methodology Auditor Report

## Summary
The paper is primarily theoretical, with one empirical validation (Monte Carlo for PPV). The theoretical methodology is sound: axioms are cleanly stated, proofs follow from them, and derived results are consistent. The main methodological gap remains the lack of empirical validation for the set operation formulas, which are the paper's primary contribution.

## Theoretical Methodology

### Axiom Design
The two-axiom design is clean and minimal. Element-wise independence (Axiom 1) is the standard assumption for Bloom filters and similar structures. Conditional independence of block rates (Axiom 2) is needed only for the entropy decomposition. The axiom economy remark correctly characterizes which results depend on which axioms.

### Proof Strategy
Proofs are primarily combinatorial (counting arguments, law of total probability) and use standard tools (CLT, Hoeffding's inequality, Borel-Cantelli). The methodology is appropriate for the results claimed.

### Statistical Rigor
- Confidence intervals (Theorem 4.4): Correctly derived as asymptotic normal intervals. The caveat "asymptotic" is stated.
- PPV approximation (Theorem 4.5): Second-order Taylor expansion with stated error bound O(1/min(p,n)^2). Valid when p*tau and n*epsilon are both large.
- Method of moments estimator for p (equation in Section 4): Noted as undefined when U is infinite. Bias is not quantified -- this is acknowledged in the conclusion as future work.

## Empirical Validation

### Present: PPV Monte Carlo (Figure 4.3)
- 50,000 trials per point
- Prevalence lambda = 1%, p = 100, n = 9900
- Theory and simulation points are reported as "indistinguishable"
- This validates the Taylor approximation for PPV under these specific parameters

### Absent: Set Operation Formulas
The union FPR, union FNR, intersection FPR/FNR, and set difference formulas (Section 5) lack empirical validation. These are the paper's primary contribution. The paper has Monte Carlo infrastructure (code/ppv.cpp, code/bin_class_measures_sim.cpp) that could be extended.

### Absent: k-fold Composition
The k-fold composition data in Figure 3.2 appears to be computed analytically from the recurrence, not verified by simulation. Simulation would strengthen confidence.

## Reproducibility
- All formulas are closed-form and reproducible
- Monte Carlo code exists in code/ directory
- Data files for plots are in data/ directory (17 CSV files)
- Build instructions are clear (pdflatex + bibtex)

## Remaining Issues

1. **No Monte Carlo validation for set operations** (Section 5). This is the paper's main contribution and should be validated empirically. (Severity: minor -- the proofs are correct, but validation strengthens the contribution)

2. **k-fold composition figure not empirically verified**. The data points appear analytically computed. (Severity: suggestion)

3. **Cross-set independence (Assumption 5.1) not discussed for practical violations**. When two Bloom filters share hash functions, errors at the same element may be correlated, violating this assumption. A remark on robustness would be useful. (Severity: suggestion)

4. **Method of moments estimator bias not quantified**. The estimator p-hat = (|B| - u*epsilon)/(tau - epsilon) is biased because E[|B|] depends on p through a nonlinear function. (Severity: suggestion)
