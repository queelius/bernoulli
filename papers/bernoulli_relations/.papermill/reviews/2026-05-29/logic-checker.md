# Logic Checker Report, bernoulli_relations

**Agent**: logic-checker (proof correctness, logical chain integrity, claim support)
**Date**: 2026-05-29
**Verdict**: The foundational restatements are sound. Beyond those, the new contributions rest on unfinished or incorrect proofs. Several theorems have placeholder proof bodies; at least two definitions contain genuine logical errors.

## Theorems and proofs that are SOUND (with caveats)

### OK-1. Theorem `thm:fpbinom` (false-positive count is binomial)
Statement: given `\n` negatives with FPR `\fprate`, `\FP_\n ~ binom(\n, \fprate)`. Proof: i.i.d. Bernoulli trials per Assumption `asm:ber_trial`, summed. **Correct.** This is a verbatim restatement of the foundation result applied to the product universe `X_1 x ... x X_n`. Legitimate for an extension paper, but it should be cited to `bernoulli_sets` (key `aset`) rather than presented as a fresh proof. (Novelty note, not a logic defect.)

### OK-2. Theorem `thm:fpr` (FPR is a random variable; mean, variance, CLT)
Statement: `\FPR_\n = \FP_\n / \n` has support `{j/n}`, mean `\fprate`, variance `\fprate(1-\fprate)/\n`, and is asymptotically normal. Proof computes `E[FPR]` and `Var[FPR]` correctly from the binomial. **Correct.** Same provenance caveat as OK-1. Minor: the variance line writes `\Var{\FP}` without the subscript `\n` that appears everywhere else (cosmetic).

## CRITICAL logical errors

### CL-1. Definition `def:approx_pfun`, condition (ii): conditions on the event itself
Quoted text (properties.tex):
> "If $\Tuple{\RV{X}}$ is *not* in the domain of $\PFun{f}$, it is in the domain of $\APFun{f}$ with a probability $\fprate$,
> $$\Prob{\Tuple{\RV{X}} \in \Dom(\APFun{f}) \Given \Tuple{\RV{X}} \notin \Dom(\APFun{f})} = \fprate.$$"

The conditioning event is written `\notin \Dom(\APFun{f})` (the *approximate* function), but the prose says "not in the domain of `f`" (the *objective* function). As written, the conditional probability conditions the event `X in Dom(approx f)` on its own negation `X notin Dom(approx f)`, which is identically `0`, not `\fprate`. **The conditioning set must be `\Dom(\PFun{f})`, the objective function.** Compare condition (i) just above, which correctly conditions on `\Dom(\PFun{f})`. This is a one-character error (`\APFun` should be `\PFun`) but it makes the definition state something false. Fix: change the conditioning event to `\Tuple{\RV{X}} \notin \Dom(\PFun{f})`.

### CL-2. Argument-order inconsistency for `\ARelation` makes the central definition ambiguous
The notation macro `\ARelation{R}[#2][#3]` places the first optional argument in the *subscript* slot and the second in the *superscript* slot, with no inherent meaning. The manuscript then uses two incompatible conventions:
- Definition `def:approx_rel` (approx_rel_model.tex) writes `\ARelation{R}[\fnrate][\fprate]` (false-negative first, false-positive second).
- The symmetric-relation theorem (properties.tex) and `\APFun{f}[\tprate][\fprate]` throughout write the **true**-positive rate first, then FPR.

So `\ARelation{R}[a][b]` means (FNR, FPR) in one section and (TPR, FPR) in another. Because TPR `= 1 - FNR`, a reader cannot tell whether the first slot is a "rate of error" or a "rate of success" without re-deriving from context. This is not merely stylistic: in def:approx_rel the two displayed conditional probabilities are *both* labeled with the pair `[\fnrate][\fprate]`, yet condition (i) is a false-negative statement and condition (ii) a false-positive statement, so the same subscript/superscript pair is asked to denote both. **Pick one convention (the family standard appears to be `(\tprate,\fprate)` or `(\fprate,\fnrate)`, per `bernoulli_sets`) and apply it uniformly.** Until fixed, every rate-bearing statement in the paper is ambiguous.

## MAJOR: theorems stated without proof (placeholder proof bodies)

### ML-1. Symmetric-relation theorem (properties.tex): proof is a single dangling expression
Statement: a random approximate relation `\ARelation{R}(\tprate,\fprate)` of a symmetric relation induces a symmetric `\ARelation{R}[s](\tprate, 1-(1-\fprate)^2)` under the OR-symmetrization `(x_1,x_2) in R_s iff (x_1,x_2) in R or (x_2,x_1) in R`.
Proof, in full:
> $$\Prob{\Pair{x}{y} \in \ARelation{R} \SetUnion \Pair{y}{x} \in \ARelation{R} \Given \Pair{x}{y} \notin \Relation{R}}$$

That is the entire proof: one probability expression, no derivation, no conclusion. The claimed result `1-(1-\fprate)^2` is plausible (probability that *at least one* of two independent FPR-`\fprate` trials fires, `= 1-(1-\fprate)^2`), but:
1. The TPR is claimed unchanged at `\tprate`, which is **not obviously correct**: under OR-symmetrization a true positive `(x,y)` now also fires if `(y,x)` tests positive, so the induced true-positive rate on the symmetric relation should also change (it should *increase*, by the same OR logic), unless `R` is already symmetric so that `(y,x)` is also a true positive. The statement does not specify whether the input `R` is symmetric; the prose says "of a symmetric relation," in which case both `(x,y)` and `(y,x)` are positives and the TPR transformation needs its own line. As written the theorem asserts an asymmetric transformation (FPR changes, TPR does not) without justifying the asymmetry.
2. `\SetUnion` (set union) is used where logical OR (`\lor`) is meant inside `\Prob{...}`; the event is "membership of (x,y) OR membership of (y,x)," not a union of sets. Notation error that obscures the argument.
Fix: complete the proof for both rates, state the symmetry assumption on `R` explicitly, and use `\lor` for the disjunction of events.

### ML-2. Map-composition theorem (properties.tex): proof trails off mid-sentence
Statement: for `\APFun{f}(\tprate_1,\fprate_1)` and `\APFun{g}(\tprate_2,\fprate_2)`, the composition is a random approximate map with TPR `\tprate_1 \tprate_2` and FPR in the interval `IntervalSpan(\fprate_1 \tprate_2 ∪ \tprate_1 \fprate_2 ∪ \fprate_1 \fprate_2)`.
Proof ends literally with:
> "Given that $a \in \Dom(\PFun{f} \circ \PFun{g})$, the probability $a \notin \Dom(\APFun{f} \circ \APFun{g})$ is just the probability that ..."

The proof stops at "...is just the probability that ...". No derivation of either the TPR product or the FPR interval is given. Two further concerns:
- The TPR `\tprate_1 \tprate_2` is the standard composition result and matches `bernoulli_maps` (`fnrate_{g∘f}=1-(1-fnrate_1)(1-fnrate_2)`, equivalently `\tprate_1\tprate_2` for the survival form). This is correct but, again, **belongs to and should be cited from `bernoulli_maps`** rather than re-proved here (novelty/attribution overlap, see N-1).
- The FPR "interval" notation `IntervalSpan(a ∪ b ∪ c)` is undefined: it mixes set-union of three scalar products inside an interval-span operator. The intended meaning is presumably `[min, max]` of the three products `{\fprate_1\tprate_2, \tprate_1\fprate_2, \fprate_1\fprate_2}`, but this must be stated and the bounds justified (why those three terms, why an interval rather than a point value).

### ML-3. True-subset-rate theorem (predicates.tex): proof is the single character "?"
Statement (Theorem "True subset rate"): for non-random `\Set{A} ⊆ \Set{B}`, `\Set{A}` is a subset of `\ASet{B}(\tprate,·)` with probability `\tprate^k`, `k=|A|`.
Proof, in full: `?`.
The claim itself is correct and easy (each of the `k` elements of `A`, all true members of `B`, must test positive in `\ASet{B}`, independently, giving `\tprate^k`), so this is a one-line proof that was never written. Fill it in.

### ML-4. The long subset-rate derivation (predicates.tex) is internally incomplete and self-citing to undefined results
The extended derivation of the "true subset rate" `\tsr` (the multi-page product expansion over index sets I, J, K) has structural problems:
- It invokes `\cref{?}` ("By [?], `\RV{B_1},...,\RV{B_u}` are statistically independent") and `\cref{dummyrefs}` and "Proof of theorem~\ref{thm:subset}" where no theorem `thm:subset` is defined. The independence step, which is load-bearing for turning the joint probability into a product, is asserted by reference to a non-existent result.
- Two consecutive identical display equations appear (the `\tsr = \prod_I (1-\tprate_1(1-\tprate_2)) \prod_J ... \prod_K ...` block is duplicated verbatim), suggesting a copy-paste left mid-edit.
- A comment `%%% THIS IS NOT FINISHED` is present in the source immediately above one of the key display equations. The author has self-flagged this derivation as incomplete.
The final factored form `(1-\tprate_1(1-\tprate_2))^{|V_1|} (1-\fprate_1(1-\tprate_2))^{|V_2|} (1-\fprate_1(1-\fprate_2))^{|V_3|}` is consistent with the partition into (members of both), (members of B not A), (members of neither), so the *destination* is right; the *path* is unfinished and depends on undefined lemmas. This material also overlaps `bernoulli_composition` (relational predicates), see N-1.

### ML-5. Equality-rate formula (predicates.tex) is stated "without proof" and uses a symmetry that needs checking
Quoted: "we claim without proof that ... two independent observations ... hold the equality relation with a probability given by
`(\tprate_1 \tprate_2 + \fnrate_1 \fnrate_2 - \tprate_1 \tprate_2 \fnrate_1 \fnrate_2)^{|A|} (\fprate_1 \fprate_2 + \tnrate_1 \tnrate_2 - \fprate_1 \fprate_2 \tnrate_1 \tnrate_2)^{|U|-|A|}`".
Per-element this is `P(both test positive) + P(both test negative)` for an element of `A` (and analogously off `A`). But `P(both positive) + P(both negative)` for two independent Bernoulli(`\tprate_1`), Bernoulli(`\tprate_2`) trials is `\tprate_1\tprate_2 + (1-\tprate_1)(1-\tprate_2)`. Expanding `(1-\tprate_1)(1-\tprate_2) = 1 - \tprate_1 - \tprate_2 + \tprate_1\tprate_2`, which is **not** equal to the stated `\fnrate_1\fnrate_2 - \tprate_1\tprate_2\fnrate_1\fnrate_2` form unless a different agreement event is intended. The stated expression has the structure of an inclusion-exclusion for "at least one agreement of a certain type," not "both agree." Either the formula is wrong or the agreement event is non-standard; since it is offered "without proof," a derivation is required to adjudicate. **Flagged for the author to derive, and cross-routed to methodology for an independent recomputation (see cross-verification).**

## MINOR logical / exposition gaps

- **MNL-1**. `constrained_ras.tex` (orphaned, not built): the Cartesian-product theorem states TPR/FPR as `?`/`?` (literal question marks) with proof "Prove true positive and false positive rates." Pure placeholder.
- **MNL-2**. `constrained_ras.tex` power-set theorem: the derivation of the false-positive count `2^{TP}(2^{FP}-1)` is actually fairly complete and correct in structure (counts subsets containing at least one false positive). But the closing expectation step `E[2^{TP}](2^{E[FP]}-1)/(2^p(2^n-1))` silently swaps `E[2^{FP}]` for `2^{E[FP]}` (Jensen gap), which is the very approximation the `c = (1/2)ln^2 2` correction term elsewhere tries to capture. The relationship between the exact `E[2^{FP}]` and the approximation should be made explicit. (Belongs partly to `bernoulli_entropy`/`bernoulli_composition`.)
- **MNL-3**. `relations.tex` line 6 contains the literal editing marker `integrate:::` ... `:::` wrapping a paragraph about partial functions and projection, with a sentence that ends "where the projection $\Proj$" and simply stops. Unfinished sentence inside a marked-for-integration block.
- **MNL-4**. The is-relation operator in def:approx_rel maps to `{0,1}` and is called both an operator and a member of `\PS{X_1 x ... x X_n}`; the dual "a relation IS a subset" vs "a relation HAS an is-relation operator" framing is fine but the definition conflates the set and its indicator without a word of transition.

## Cross-verification handoff
CL-1, CL-2 (critical) and ML-5 (a "without proof" formula whose correctness I dispute) are routed to the methodology-auditor for independent re-derivation. See that report's MA-X items and the unified review's cross-verification section.

## Summary for synthesis
- Critical: 2 (CL-1 self-conditioning probability; CL-2 rate-argument-order ambiguity)
- Major: 5 (ML-1..ML-5: four placeholder/unfinished proofs plus one disputed unproven formula)
- Minor: 4
The arithmetic *destinations* are mostly plausible and consistent with the family, but the paper currently proves almost none of its new claims. This is an early draft whose mathematical content is a scaffold of correct-looking statements with the proofs not yet written.
