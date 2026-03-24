# Methodology Auditor Report

## Summary
The paper is primarily theoretical, deriving results from two axioms. The methodology is appropriate for the claims made. The axiomatic approach is clean and the logical chain from axioms to results is well-structured. The one Monte Carlo validation (Figure 4.3, PPV) confirms the Taylor approximation. The main methodological gap is the absence of empirical validation for the core set operation formulas (Section 5), which are the paper's primary contribution.

## Methodology Assessment

### Axiomatic Framework (SOUND)
The two axioms (element-wise independence, conditional independence of block rates) are clearly stated and well-motivated. The connection to practical data structures (Bloom filters, perfect hash filters) is established through the ADT formulation (Section 3.1). The axioms are realistic for the intended applications.

### Proof Methodology (SOUND)
Proofs are direct and use standard techniques: law of total probability, partition decomposition, linearity of expectation, central limit theorem, Hoeffding's inequality, Borel-Cantelli lemma. The approach is correct and reproducible.

### Empirical Validation (PARTIAL)
- Figure 4.3 compares theoretical expected PPV with Monte Carlo simulation (N=50,000 trials). The agreement is excellent, validating the Taylor approximation.
- The set operation formulas (Section 5) -- the paper's main contribution -- lack any empirical validation. A simulation confirming the union or intersection FPR/FNR formulas would significantly strengthen the paper.

### Assumptions
1. **Element-wise independence (Axiom 1)**: Clearly stated. The paper notes that Bloom filters and perfect hash filters satisfy this. In practice, some data structures have weak correlations (e.g., cache-line-aligned filters), but this is acknowledged as an open problem in the conclusion.
2. **Cross-set independence (Assumption 5.1)**: Stated at the beginning of Section 5. The paper does not discuss when this holds in practice or what happens when it is violated (e.g., two Bloom filters sharing hash functions). This is a gap.
3. **Conditional independence of block rates (Axiom 2)**: Needed only for uncertain-$R$ results. Clearly scoped.

### Reproducibility
The paper includes:
- C++ simulation code (code/ppv.cpp, code/bin_class_measures_sim.cpp)
- CSV data files for all plots
- Mathematica/Maxima scripts for symbolic verification

This is good for reproducibility.

## Remaining Issues

### Minor

**m1. Cross-set independence (Assumption 5.1) needs practical discussion**
When does this hold? When two Bloom filters share a hash family, the cross-set independence assumption is violated. A brief remark discussing robustness would be useful.

**m2. No empirical validation of set operation formulas**
The core formulas of Section 5 should be validated by at least one Monte Carlo simulation. Given that the paper already has simulation infrastructure (code/), this is achievable.

### Suggestions

1. Add a Monte Carlo experiment validating the union FPR formula from Theorem 5.1 against simulated Bloom filter unions.
2. Add a brief discussion of the practical robustness of the cross-set independence assumption.
3. Consider providing error bounds for the Taylor approximation of expected PPV, not just the approximation quality claim.
