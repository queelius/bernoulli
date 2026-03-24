# Methodology Auditor Report (Post-Revision)

**Date**: 2026-02-26
**Paper**: Bernoulli sets

## Axiomatic Framework

### Axiom 1 (Element-wise independence) -- IMPROVED
Now explicitly includes the i.i.d. clause: "the error indicators $\{\mathbf{1}_{\tilde{A}}(x) : x \in B_i\}$ are identically distributed." This was MJ1 from the previous review and is correctly fixed.

### Axiom 2 (Conditional independence of block error rates) -- UNCHANGED
Correctly states conditional independence of block error rates given the objective set.

### Assumption 5.1 (Cross-set independence) -- NEW
A formal assumption added at the start of Section 5 stating that error indicators across distinct Bernoulli sets are independent. This was MJ2 from the previous review and is correctly fixed. The assumption is correctly cited in the union, intersection, and set difference proofs.

**Gap**: The relational section (Section 6) uses cross-set independence implicitly but does not cite Assumption 5.1.

## Experimental Validation

### Theory-vs-Simulation Figure (Fig. 4) -- NEW
The paper now includes a comparison of theoretical expected PPV (Equation 4.8) with Monte Carlo simulation ($N = 50,000$ trials per point) for a positive Bernoulli set with prevalence $\lambda = 1\%$. The caption states "the theoretical curve and simulation points are indistinguishable, validating the second-order Taylor approximation."

Spot-check of data point at $\fprate = 0.001$:
- Theory: PPV $\approx p/(p + n\fprate) = 100/109.9 \approx 0.910$
- Data: 0.9107
- Match: YES

This validates the theoretical framework for at least one key result. Ideally, similar validation would be shown for the set-operation error rates, but one validation figure is sufficient for a theory paper.

## Practical Applicability

### Unknown Partition Sizes (Remark 5.4) -- NEW
The paper now explicitly addresses the practical limitation that partition weights require knowledge of objective set cardinalities. Three approaches are outlined:
1. Interval bounds when only upper bounds on cardinalities are available
2. Worst-case analysis by optimizing over feasible weight region
3. Estimation from approximate sets with computable bias

This is adequate. A full development of approach (c) (bias-corrected estimation) would strengthen the paper but is reasonably left as future work.

## Reproducibility

- **Build**: Clean, fully reproducible with `pdflatex + bibtex`
- **Simulations**: C++ code in `code/` directory; CSV data in `data/` directory
- **Notation**: Fully specified in alex.sty and Appendix notation reference
- **Proofs**: Complete or with explicit "follows the same logic" references

## Overall: The methodology is sound. All previous methodological concerns have been addressed.
