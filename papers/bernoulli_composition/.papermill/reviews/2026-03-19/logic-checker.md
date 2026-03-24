# Logic Checker Report

**Paper**: Composition of Bernoulli sets
**Date**: 2026-03-19

## Summary

All proofs are logically sound. The derivations for complement, union, intersection, and set difference error rates are correct. The relational predicate proofs (subset, equality) are correct. The parametric parsimony remark's claims are verified. No critical or major logic errors found.

## Detailed Findings

### Theorem 3.1 (Complement error rates) -- CORRECT
The proof correctly identifies that positives of A^c are negatives of A and vice versa. The FPR/FNR swap follows directly. No issues.

### Theorem 3.2 (Union FPR) -- CORRECT
The inclusion-exclusion argument via complement probability is standard and correctly applied. The use of cross-set independence (Assumption 3.1) is appropriate since x is a negative of both A_1 and A_2, so the two error events are independent.

### Theorem 3.3 (Union FNR) -- CORRECT
The three-region partition of A_1 U A_2 is exhaustive and disjoint. Each region's probability is correctly computed:
- Region (i): x in A_1, x notin A_2 => fnr_1 * (1-fpr_2). Correct.
- Region (ii): x notin A_1, x in A_2 => (1-fpr_1) * fnr_2. Correct.
- Region (iii): x in A_1, x in A_2 => fnr_1 * fnr_2. Correct.
The law of total probability application with partition weights is correct.

### Corollaries 3.1, 3.2 (Union of positive/negative sets) -- CORRECT
Setting fnr_1 = fnr_2 = 0 and fpr_1 = fpr_2 = 0 respectively in the union formulas yields the stated results.

### Theorem 3.4 (Intersection FNR) -- CORRECT
Dual to union FPR. The complement probability argument correctly gives 1 - (1-fnr_1)(1-fnr_2).

### Theorem 3.5 (Intersection FPR) -- CORRECT
The three-region partition of the negatives of A_1 cap A_2 is exhaustive and disjoint. Each region's probability is correctly computed. Weights sum to 1.

### Corollaries 3.3, 3.4 (Intersection of positive/negative sets) -- CORRECT

### Theorem 3.6 (Set difference error rates) -- CORRECT
Correctly reduces to intersection with complement. The FNR substitution (fnr -> fpr_2 for the complement) is correct. The FPR partition weights are correctly identified for the negatives of A_1 \ A_2.

### De Morgan duality observation -- CORRECT
The functional form symmetry between union FPR and intersection FNR is correctly attributed to De Morgan's laws and the complement rate-swap theorem.

### Remark on parametric parsimony -- CORRECT
- "A general fourth-order channel on 4 observed symbols has 4 x 3 = 12 free parameters": Verified. A 4x4 stochastic matrix with 4 rows each summing to 1 has 4*(4-1) = 12 free parameters.
- "union of two second-order Bernoulli sets requires only 4 parameters": Verified. Two sets, each with (fpr, tpr), give 4 parameters.
- "composing m independent second-order Bernoulli sets yields a model of order up to 2^m... but the parameter count grows linearly as 2m rather than as 2^m(2^m - 1)": Verified. The Kronecker product factorization under independence is standard.

### Remark on monoidal structure -- CORRECT
Associativity and commutativity are inherited from the powerset. The identity elements (empty set for union, universal set for intersection) require the degenerate-case axiom, which is correctly referenced.

### Grammar (Equations 3.19-3.20) -- CORRECT
The grammar correctly characterizes the closure properties. Positive sets are closed under union (Cor 3.1) and intersection (Thm 3.6), and complement of a negative set is positive (Thm 3.1).

### Subset probability theorem (Section 4) -- CORRECT
The three-block partition under the assumption X subset Y is correct. The per-block probabilities are verified.

### Equality probability corollary -- CORRECT
The two-block partition under X = Y is correct. The agreement probabilities (tpr_1*tpr_2 + fnr_1*fnr_2 for positives, fpr_1*fpr_2 + tnr_1*tnr_2 for negatives) correctly account for both ways two independent Bernoulli indicators can agree.

### Infinite universe corollaries -- CORRECT with minor caveat
The equality corollary is correct. The subset corollary requires |U| - |Y| -> infinity, which is implicit in "over an infinite universal set" but could be stated more precisely.

### Interval arithmetic (Section 5) -- CORRECT
Monotonicity claims for the union FPR and FNR formulas are verified by partial derivatives. The endpoint evaluation for guaranteed bounds is sound.

## Confidence: HIGH
All proofs follow standard probability arguments (independence, law of total probability, inclusion-exclusion). No gaps or errors detected.
