# Novelty Assessor Report, bernoulli_entropy

**Reviewer role**: Contribution clarity, differentiation, significance
**Date**: 2026-05-29
**Calibration**: Assessed RELATIVE to the paper's declared role as a companion in the 9-paper Bernoulli-sets family. Shared foundations (the two axioms, binomial error-count distributions, composition theorem) are imported from `bernoulli_sets` by design and are NOT counted against novelty.

## Declared contributions (from intro)
1. Joint entropy of FP/FN counts with closed-form asymptotic expansion (Thm 3.1), extended to random positive count (Sec 3.1).
2. Restatement and proof of the Carter et al. 1978 space lower bound in Bernoulli notation (Prop 4.1), with the Bloom 69%-efficiency corollary and an explicit open problem for the general case.

## Assessment

The paper is honest about what is new versus borrowed, which is its main virtue. It does not inflate. The contributions are real but modest, and that modesty is appropriately signaled ("restate and prove ... for completeness"). My concern is not over-claiming; it is whether the *new* content (Result 1) is substantial enough to anchor a standalone paper, and whether the paper sufficiently differentiates its lower-bound contribution from the prior art it restates.

### Finding MAJOR-1: Result 1's novelty is real but thin, and the paper does not argue its significance
- **Location**: `sections/entropy.tex` (whole), and `sections/intro.tex` "Contribution" paragraph.
- **Problem**: The joint entropy is obtained by (a) additivity from independence and (b) substituting the textbook binomial-entropy asymptotic. Both ingredients are standard; the novelty is purely in *applying* them to the Bernoulli error counts. That is a legitimate but small delta. The paper never says *why this entropy is useful*: the intro asserts "any lossless representation of the error pattern requires at least this many bits on average," but the body never connects the entropy back to a coding scheme, to the space bound of Section 4, or to anything downstream. The entropy result and the space-complexity result sit side by side without interacting. For a reader asking "so what?", the paper has no answer beyond "it is a natural quantity."
- **Suggestion**: Add one paragraph linking Result 1 to a consequence. Candidates: (i) relate H(FP,FN) to the number of bits needed to *transmit which elements erred* (a source-coding statement), (ii) connect it to the mutual information `I(tilde A; A)` that the conclusion lists as future work (why defer it? a few lines would land it), or (iii) use the entropy to bound the *redundancy* of the data structure relative to the Section 4 lower bound. Any of these would convert "a natural quantity we computed" into "a quantity that does work."

### Finding MAJOR-2: The lower-bound contribution is a restatement; the differentiating value (Bernoulli notation + completeness) is asserted, not demonstrated
- **Location**: `sections/space_complexity.tex` lines 14-15.
- **Quoted text**: "We restate it here in the notation of the present paper and include a proof for completeness."
- **Problem**: Restating a 1978 result in new notation is only a contribution if (a) the new notation makes something clearer or composable that the original did not, or (b) the proof is cleaner/more self-contained than the original. The paper claims (a) implicitly by existing inside the Bernoulli family, but never shows what the Bernoulli framing *adds* to the bound (e.g., does it compose with the union/intersection error rates of `bernoulli_composition`? does it specialize cleanly to the family's map/relation types?). And the proof, while clean, is the standard pigeonhole argument, not a new one. As written, Section 4 reads as "a careful re-proof," which is fine for a companion paper but should be framed as such rather than as a contribution.
- **Suggestion**: Either (i) explicitly state the value-add of the Bernoulli framing in one sentence (e.g., "stated this way, the bound plugs into the composition theorem of [bernoulliComposition] as ..."), or (ii) soften the contribution framing in the intro from "we restate and prove" to acknowledge it is primarily expository, with the *novel* piece being the open-problem analysis in Rem 4.2.

### Finding MINOR-1: The most novel idea (the general-case open problem) is under-developed relative to its prominence
- **Location**: `sections/space_complexity.tex` Rem 4.2; echoed in conclusion as "the most pressing open question."
- **Problem**: The remark correctly explains why the pigeonhole argument fails for `0 < tau < 1` and offers the heuristic `-tau*log2(eps)`, then disclaims it. This is genuinely the most original thinking in the paper, yet it is a single remark. Calling it "the most pressing open question" in the conclusion while giving it three sentences undersells it.
- **Suggestion**: Promote it. Even a partial result (a weaker but valid lower bound for the general case, or a precise statement of *why* the encoding problem "changes qualitatively") would materially raise the paper's contribution. If a full bound is out of reach, state a conjecture formally and give the strongest partial argument available.

### Finding MINOR-2: Self-overlap risk with the family is low but should be pre-empted
- **Location**: relationship to `bernoulli_sets`, `bernoulli-hash-function`, `phf`, `shs`.
- **Problem**: The space bound here is "the target achieved by the BHF" (per state file). A referee unfamiliar with the family might wonder whether the bound and its achievability belong in one paper. The split is defensible (lower bound here, construction there), but the paper does not say so.
- **Suggestion**: One sentence in the intro or conclusion: "The matching construction that achieves this bound is developed in [bernoulli-hash-function]; here we establish only the bound." This pre-empts the salami-slicing concern and clarifies scope.

## Differentiation from prior art (with literature context)
- vs. **Carter et al. 1978**: explicitly a restatement; correctly attributed. Not claimed novel. Good.
- vs. **Pagh-Pagh-Rao 2005** (uncited): PPR gives the tight `(1+o(1))` bound *and* a matching structure. The paper's lower bound is the same order; PPR is strictly more complete on this exact question. Not citing it leaves the paper's "this is the optimum" framing weaker than it should be. (See citation-verifier and literature context.) This is a differentiation gap: the paper should position relative to the modern tight result, not only the 1978 origin.
- vs. **Result 1 prior art**: no direct pre-emption found; the joint FP/FN entropy appears to be unpublished elsewhere. Novelty confirmed, significance unestablished (MAJOR-1).

## Significance verdict
As a standalone artifact: **low-to-moderate**. Result 2 is expository; Result 1 is novel but elementary and unmotivated; the open problem is the freshest part but underdeveloped. As a **companion within the family**: **appropriate and useful**, it fills the "information-theoretic properties" slot and supplies the bound the BHF paper targets. The recommendation should weigh the companion role, but the author should still strengthen the motivation of Result 1 and the framing of Result 2.

## Confidence
Medium-high. The novelty calibration is clear; the main judgment call is how much credit a restatement-plus-elementary-new-result deserves, which I have tied to concrete, addressable framing fixes rather than a verdict that the work is unpublishable.
