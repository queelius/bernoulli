# Prose Auditor Report

**Paper**: Composition of Bernoulli sets
**Date**: 2026-03-19

## Summary

The writing is clear, well-organized, and professional. The paper follows a logical progression from preliminaries through the four set operations to relational predicates and interval arithmetic. Proofs are detailed and readable. A few minor issues are noted below.

## Findings

### Minor Issues

1. **Section 4, line 6: Missing codomain in member-of predicate type signature**
   - Written: "$\in : U \times 2^U$"
   - Should be: "$\in : U \times 2^U \to \{0,1\}$"
   - The other predicates on line 10 correctly include the codomain.

2. **Section 4, positive subset corollary proof: "vanish" is misleading**
   - "the second and third factors of the subset theorem vanish (each equals $1^n$)"
   - "Vanish" typically means "go to zero." The factors become 1 (multiplicative identity), not 0. Better: "reduce to 1" or "become trivial."

3. **Section 3, convergence remark: Variable name collision**
   - The remark uses $n$ as the sequence index ($\PASet{A}[\fprate_1],\ldots,\PASet{A}[\fprate_n]$), but the same letter $n$ is used elsewhere in the paper for the number of negatives and for model order. This could confuse a careful reader. Consider using $k$ or $N$ for the sequence length.

4. **Section 5: Informal use of $\tprateob$ without definition**
   - Line 42 uses $\tprateob$ (the realized TPR) without defining it in this paper. It is defined in the companion paper. A brief inline definition ("the realized true positive rate $\tprateob$") would help readers of this paper alone.

5. **Section 4, subset theorem: No theorem name or number**
   - The subset probability theorem (beginning "Given $X \subseteq Y$") has no descriptive name, unlike all theorems in Section 3. Adding "[Subset probability]" would improve navigability.

6. **Section 4: Corollaries lack descriptive names**
   - The corollaries after the equality probability are unnamed. Adding brief names (e.g., "[Equal-rate equality probability]", "[Positive subset probability]", "[Equality over infinite universe]", "[Subset over infinite universe]") would improve scannability.

7. **Section 4, line 14: Subset definition uses product over A, not U**
   - The definition $A \subseteq B = \prod_{x \in A} [x \in B]$ iterates over $x \in A$, which is mathematically correct but unconventional. The standard formulation is $\forall x \in U: x \in A \Rightarrow x \in B$. The product form is equivalent but may confuse readers expecting the universal-quantifier form.

### Suggestions

1. The table caption (Table 1) says "The partition weights $w_1$, $w_2$, $w_3$ are operation-dependent" and references the equations. A footnote or inline note clarifying that the weights require knowledge of objective set cardinalities would preempt a common reader question (this is addressed later in Remark 3.4, but the table is where most readers will look first).

2. The conclusion's "Open problems" paragraph mentions estimating cardinalities from approximate sets. This could note that this estimation problem is non-trivial because the estimator $|\tilde{A}_1 \cap \tilde{A}_2|$ has computable but rate-dependent bias.

## Narrative Arc

The paper's narrative is well-constructed:
- Introduction motivates the compositional question.
- Preliminaries restate exactly what is needed from the companion paper.
- Section 3 systematically treats all four operations with consistent proof structure.
- Section 4 derives relational predicates as a natural extension.
- Section 5 addresses the practical concern of uncertain parameters.
- Conclusion is concise and identifies open problems.

## Overall Quality: HIGH
The writing is among the clearest in the paper family. The consistent proof structure and systematic progression make the paper easy to follow.
