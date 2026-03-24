# Novelty Assessor Report

**Paper**: Composition of Bernoulli sets
**Date**: 2026-03-19

## Summary

The paper provides a clean, complete algebraic treatment of set-operation error rates for Bernoulli sets. The individual results (union FPR, intersection of Bloom filters, etc.) are not surprising to specialists in probabilistic data structures, but the unified treatment -- covering all four operations, both error types, monoidal structure, relational predicates, and interval arithmetic in a single coherent framework -- is the contribution. This is a well-scoped companion paper.

## Contribution Assessment

### Contribution 1: Closed-form error rates for all four set operations
**Significance**: MODERATE. The complement and union FPR formulas are folklore for Bloom filters. The full second-order treatment (both FPR and FNR, all four operations, weighted partition formulas) is more complete than what appears in the existing literature.

**Differentiation**: The key advance over prior work is handling the general case (nonzero FPR and FNR simultaneously) and making the partition weight structure explicit.

### Contribution 2: Relational predicates (subset, equality probabilities)
**Significance**: MODERATE. These are natural consequences of the element-wise independence axiom, but having exact closed-form expressions for subset and equality probabilities is useful and appears to be new in this formulation.

### Contribution 3: Interval arithmetic extension
**Significance**: LOW-MODERATE. The interval propagation is a direct application of standard interval arithmetic (Moore, 1966) to the error rate formulas. The monotonicity analysis enabling endpoint evaluation is straightforward. The value is in demonstrating the approach rather than in technical novelty.

## Strengths
1. The paper is well-scoped: it does one thing (compositional algebra) and does it completely.
2. The De Morgan duality observation provides structural insight.
3. The parametric parsimony remark (new) adds valuable conceptual clarity about why the closed-form formulas exist despite the higher-order structure.
4. The closure grammar (Equations 3.19-3.20) is a nice formalism for characterizing which expressions preserve the positive/negative property.

## Weaknesses
1. No experimental validation or comparison with Monte Carlo simulation to confirm the derived formulas numerically (beyond one worked example).
2. The interval arithmetic section is thin (2 pages). The intersection and set difference interval formulas are deferred to a remark rather than stated explicitly.

## Overall
For a companion paper providing the algebraic infrastructure assumed by sibling papers, the contribution is appropriate. The paper would not stand alone as a strong independent contribution, but it is not intended to.
