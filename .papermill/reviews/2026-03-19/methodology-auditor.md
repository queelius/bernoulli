# Methodology Auditor Report

**Paper**: Composition of Bernoulli sets
**Date**: 2026-03-19

## Summary

This is a purely theoretical paper with no experiments. The methodology consists of probability-theoretic derivations under clearly stated axioms. The methodology is sound.

## Findings

### Axiom Foundation
The paper correctly restates the two axioms from the companion paper (element-wise independence and conditional independence of block error rates) and adds a third assumption (cross-set independence, Assumption 3.1) specific to this paper. This assumption is clearly stated and well-motivated.

### Derivation Pattern
All derivations follow a consistent methodology:
1. Identify the event of interest (false positive or false negative of the composed set).
2. Partition the relevant elements into disjoint regions based on membership in the operand sets.
3. Compute the per-element error probability in each region using independence.
4. Apply the law of total probability with partition weights.

This pattern is applied uniformly across all four operations, providing structural consistency.

### Numerical Example (Example 3.1)
**Finding (Minor)**: The numerical example shows intermediate values rounded to 5 decimal places (0.02288, 0.00990, 0.00030) that sum to 0.03308, but the exact computation gives 62/1875 = 0.033067. The discrepancy (0.03308 vs 0.03307) arises from the paper using approximate weights (w1 = 0.467 rather than 70/150 = 0.46667). This is inconsequential for an illustration but could be noted or avoided by using exact fractions.

### Reproducibility
All results are fully reproducible: the formulas are closed-form and depend only on the error rates and set cardinalities. No numerical methods, approximations, or implementation-dependent steps are involved.

### Missing Methodology
- No Monte Carlo validation of the derived formulas is provided. For a theoretical paper this is acceptable, but a simulation confirming the formulas (especially for set difference and intersection with mixed rates) would strengthen confidence.
- The interval arithmetic section does not provide explicit formulas for intersection and set difference intervals, deferring them to a brief remark. This leaves the reader to work out the endpoint assignments.
