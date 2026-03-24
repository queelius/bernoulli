# Literature Context

**Paper**: Composition of Bernoulli sets
**Date**: 2026-03-19

## Broad Context

This paper bridges probabilistic data structures and set-theoretic algebra, formalizing how error rates propagate through set operations. The key related areas are:

### Bloom Filter Composition
- Bloom filters are the canonical positive Bernoulli set (FNR = 0). Union of Bloom filters is well-studied: the bitwise-OR of two Bloom filter bit arrays yields a Bloom filter for the union, with FPR approximately additive for small rates. This paper formalizes and generalizes this observation to arbitrary Bernoulli sets (both error types, all four set operations).
- Intersection of Bloom filters has no direct bitwise analog (bitwise-AND does not give a Bloom filter for the intersection), making the algebraic treatment here valuable.

### Interval Arithmetic
- Moore (1966) and Hickey, Ju, & Van Emden (2001) are cited for foundational interval arithmetic. The application to error rate propagation is novel in this context.
- The dependency problem in interval arithmetic is acknowledged but argued to be manageable due to the simplicity of the formulas.

### Channel Composition
- The parametric parsimony remark connects to the theory of product channels in information theory (Cover & Thomas). The Kronecker product factorization of joint transition matrices under independence is standard.

## Targeted Comparisons

### Direct Predecessors
- The companion paper (bernoulliSets) provides all axioms and distributions assumed here. This paper is a clean separation of the compositional algebra.
- No competing formalization of set-operation error rates at this generality level was found. Prior work on Bloom filter unions is the closest, but is restricted to the positive (FNR = 0) case.

### Missing References
- The `coverThomas` entry in `references.bib` is defined but never cited in this paper. It is cited in the companion paper `bernoulli_sets/` for the channel matrix product theorem. Either cite it in the parametric parsimony remark (where the Kronecker product connection is relevant) or remove it from this paper's bibliography.
- No references to related work on approximate set composition in database query planning (e.g., Bloom filter join optimization) are included. This could strengthen the motivation but is not strictly required for a mathematical companion paper.
