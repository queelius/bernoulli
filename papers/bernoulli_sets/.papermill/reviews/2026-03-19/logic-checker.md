# Logic Checker Report

**Date**: 2026-03-19
**Paper**: Bernoulli sets: a model for random approximate sets

## Summary

All proofs are logically correct. The logical chain from axioms to theorems is sound. No critical issues found. Two minor observations noted.

## Findings

### Theorems and Proofs Verified

1. **Proposition 3.1** (Element rates): Correct. Linearity of expectation applied to iid Bernoulli indicators under Axiom 1.

2. **Theorem 3.1** (Composition rates): Correct. The law of total probability correctly yields the composed TPR = tau' * tau + omega' * eps and composed FPR = eps' * tau + eta' * eps. This matches the standard binary channel matrix product (Cover & Thomas). Numerically verified.

3. **Theorem 3.2** (Two-fold composition): Correct. Follows by direct application of Theorem 3.1 with inner/outer rates. Inductive step is valid.

4. **Theorem 4.1** (FP binomial): Correct. n iid Bernoulli(eps) trials yield Bin(n, eps).

5. **Theorem 4.2** (FPR distribution): Correct. Scaled binomial. Expectation and variance correctly derived.

6. **Corollary 4.2.1** (TN binomial): Correct. TN = n - FP, so Bin(n, 1-eps).

7. **Corollary 4.2.2** (FPR convergence): Correct. Proof in appendix uses Hoeffding + Borel-Cantelli correctly.

8. **Theorem 4.3** (FN binomial): Correct. Symmetric to Theorem 4.1.

9. **Theorem 4.4** (FNR distribution): Correct. Symmetric to Theorem 4.2.

10. **Theorem 4.5** (CLT for rates): Correct. Standard CLT applied to mean of iid Bernoulli trials.

11. **Theorem 4.6** (Confidence intervals): Correct. Standard Wald interval construction.

12. **Appendix A** (Proof of Corollary 4.2.2): Correct. Hoeffding bound, geometric series convergence, Borel-Cantelli lemma all applied correctly.

### Definitions Verified

- **Definition 3.8** (Positive approximate set): fnrate = 0, tprate = 1. Every realization is a superset of A. Correct.
- **Definition 3.9** (Negative approximate set): fprate = 0, tnrate = 1. Every realization is a subset of A. Correct.
- **Complement duality** (line 113): Complement of positive is negative and vice versa. Verified by direct computation of error rates under complementation.

### Remarks Verified

- **Remark 3.1** (BSC): Correct identification of per-element model as binary channel.
- **Remark 3.2** (Axiom economy): Correct characterization of when each axiom is needed.
- **Remark 3.4** (Parametric parsimony): Kronecker factorization claim verified. Parameter counts (12 general vs 4 Kronecker) are correct for the union example.
- **Remark 3.5** (Latent and observed sets): Correct duality description.
- **Remark 3.6** (Bernoulli Booleans): Correct projection from set-level to Boolean universe. Miller-Rabin example is accurate.

### Minor Observations

**m1: Notation inconsistency in Theorem 4.2 proof** (severity: minor)
- The theorem statement uses $p_{\alpha_n}(\hat{\varepsilon} | \varepsilon)$ but the proof uses $p_{\alpha_n}(\hat{\varepsilon}_n | \varepsilon)$. The subscript $n$ on $\hat{\varepsilon}$ appears only in the proof, not the theorem statement.
- **Location**: sections/distributions.tex, lines 58 vs 77

**m2: Implicit conditioning in density decomposition** (severity: minor)
- The equation $f(\tilde{X}, \alpha, \beta) = f(\tilde{X} | \alpha, \beta) f(\alpha | R) f(\beta | R)$ is correct but the left side lacks explicit conditioning on $R$. The notation $\tilde{X}$ implicitly means "$\tilde{R}$ given $R = X$" (established on line 91), so the conditioning is absorbed into the notation. A reader encountering this equation might be confused about the absent $R$ conditioning.
- **Location**: sections/bernoulli_model.tex, lines 117-119

## Figure Data Verification

- **Figure 2** (k-fold composition): All 21 data points for TPR_k and FPR_k verified numerically against the composition recurrence. Stationary point eps/(eps + fnr) = 1/3 verified.

## Boolean Universe Example Verification

- **Example 3.1**: All four probability mass values verified. Positive approximate set reachability claim verified.
