# Methodology Auditor Report

**Date**: 2026-03-19
**Paper**: Bernoulli sets: a model for random approximate sets

## Summary

The methodology is sound. The axiomatic approach is well-structured: axioms are clearly stated, results follow logically, and the scope is well-bounded. No critical methodological issues. Two minor observations and one suggestion.

## Methodology Assessment

### Axiomatic Framework Design
- **Axiom 1** (Element-wise independence): Clearly stated, practically motivated (hash-based data structures), and used as the primary workhorse for all distributional results. The axiom includes both mutual independence of error events and identical distribution within partition blocks.
- **Axiom 2** (Conditional independence of block rates): Clearly stated with explicit characterization of when it is needed (Remark 3.2). The economy of this axiom system is a strength.
- **Assessment**: Well-designed. The axioms are minimal and sufficient.

### Proof Methodology
- All proofs follow standard probabilistic arguments (linearity of expectation, CLT, Hoeffding, Borel-Cantelli).
- The "proof by analogy" approach for Theorems 4.3, 4.4, and Corollaries (stating "the proof follows the same logic as...") is appropriate for symmetric results but could be slightly more explicit for a foundational paper.
- The appendix proof of Corollary 4.2.2 is the most technically substantial and is correctly executed.

### Model Validation
- The paper establishes that Bloom filters and perfect hash filters satisfy the axioms (Section 3.1, line 123).
- The Boolean universe example (Example 3.1) serves as a minimal worked example.
- The k-fold composition figure (Figure 2) provides numerical illustration of the composition theorem.

### Reproducibility
- All mathematical results are fully specified and derivable from the axioms.
- The figure data is reproducible from the composition recurrence.
- No experimental data or simulations are presented in the main paper (the code/ directory contains C++ simulations, but these are not referenced in the active sections).

## Findings

### Minor Issues

**m1: "Proof by analogy" for symmetric results** (severity: minor)
- Theorems 4.3, 4.4, and Corollary 4.4.1 defer their proofs to analogous earlier results. While this is standard practice, a foundational paper might benefit from at least stating the key substitutions explicitly (e.g., "replacing eps with omega, n with p, and negatives with positives").
- **Location**: sections/distributions.tex, lines 132, 142, 156
- **Suggestion**: Add one-line explicit substitution mappings, e.g., "The proof is identical to that of Theorem 4.2, with $\omega$ in place of $\varepsilon$ and $p$ in place of $n$."

**m2: Unused simulation code** (severity: minor)
- The code/ directory contains C++ Monte Carlo simulations (ppv.cpp, bin_class_measures_sim.cpp) that are not referenced in the paper. These appear to belong to the companion paper on classification measures.
- **Suggestion**: Either reference the simulations as validation, move them to the companion paper directory, or note their existence in a remark about empirical validation.

### Suggestion

**s1: Empirical validation paragraph**
- The paper is purely theoretical. A brief paragraph or remark noting that the distributional predictions have been validated by Monte Carlo simulation (even if the simulation details are in a companion paper) would strengthen the methodology section.
- **Location**: End of Section 4 or beginning of conclusion

## Overall Assessment

The methodology is clean, well-structured, and appropriate for a foundational mathematical paper. The axiomatic approach is the right choice for this type of contribution.
