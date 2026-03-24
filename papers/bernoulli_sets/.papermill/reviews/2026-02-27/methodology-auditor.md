# Methodology Auditor Report

**Paper**: Bernoulli sets: a model for sets with random errors
**Date**: 2026-02-27

## Summary
The paper is primarily theoretical, with methodology consisting of axiomatic development, mathematical proof, and Monte Carlo validation. The methodology is generally sound. The Monte Carlo simulation (Figure 4.3) validates the theoretical PPV formula, which is good practice. The paper does not include experimental benchmarks against real data structures, which limits empirical validation.

## Findings

### Critical Issues
None.

### Major Issues

**M1. The independence axiom may not hold exactly for real data structures**
- **Location**: Axiom 1 (bernoulli_model.tex lines 12-21)
- **Problem**: The element-wise independence axiom is presented as holding for Bloom filters and perfect hash filters. For standard Bloom filters with random hash functions, the independence is approximate (hash collisions introduce weak correlations). Bose et al. (2008), which is cited, explicitly discuss the gap between the idealized independence model and the actual (slightly dependent) Bloom filter behavior.
- **Suggestion**: Add a discussion of how robust the results are to slight violations of the independence axiom. Even a brief note like "The results are first-order accurate when correlations are $o(1/n)$" would strengthen the methodology.

**M2. The Taylor approximation for expected PPV lacks explicit error bounds (Theorem 4.5)**
- **Location**: distributions.tex lines 285-301
- **Problem**: The theorem states the error is $\mathcal{O}(1/\min(p,n)^2)$ but does not provide the constant. For practitioners, knowing that the approximation is "good for large sets" is insufficient without quantifying "large."
- **Suggestion**: Either provide explicit remainder bounds or add a table showing the approximation error for representative values of $p$ and $n$.

### Minor Issues

**m1. Monte Carlo validation is incomplete (Figure 4.3)**
- The Monte Carlo simulation validates only the PPV formula for positive Bernoulli sets. No validation is provided for the set operation formulas (Section 5), which are the core contribution.
- **Suggestion**: Add a simulation validating at least one set operation formula (e.g., union FPR or union FNR).

**m2. The interval arithmetic section lacks worked numerical examples**
- **Location**: Section 7
- **Problem**: The interval propagation is described abstractly but no numerical example demonstrates the output interval widths for a realistic scenario.
- **Suggestion**: Add a numerical example showing interval propagation through a union of two Bloom filters with confidence-interval-based input rates.

**m3. Cross-set independence assumption may be too strong (Assumption 5.1)**
- **Location**: set_theory.tex lines 18-21
- **Problem**: Assumption 5.1 requires that the two Bernoulli sets $\tilde{A}_1$ and $\tilde{A}_2$ use independent randomness. In practice, if two Bloom filters share the same hash functions (as is common for space efficiency), this assumption is violated.
- **Suggestion**: Discuss the practical implications of this assumption and what happens when it is violated.

**m4. No discussion of finite-sample behavior of the asymptotic normal approximation**
- **Location**: Section 4.1 (distributions.tex lines 174-200)
- **Problem**: The CLT-based normal approximation is used throughout, but no guidance is given on how large $n$ or $p$ must be for the approximation to be adequate (e.g., the standard rule of thumb $np > 5$ and $n(1-p) > 5$ for binomial-to-normal).
- **Suggestion**: Add a brief note on when the normal approximation is adequate vs. when the exact binomial should be used.

### Suggestions
1. Consider adding a section or appendix demonstrating the framework on a concrete application (e.g., cascaded Bloom filters in a distributed system, or Boolean query over encrypted search indexes).
2. The paper would benefit from a comparison table: "For these specific scenarios, our closed-form predictions match Monte Carlo within X%."
