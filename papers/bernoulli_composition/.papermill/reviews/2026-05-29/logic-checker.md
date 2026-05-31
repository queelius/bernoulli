# Logic Check Report

## Summary

The mathematical content is sound. Every closed-form error rate, relational
probability, and corollary I checked is correct: I verified the union FPR and
FNR, intersection FPR and FNR, set-difference rates, the subset probability, the
equality probability, the positive- and negative-set corollaries, the asymptotic
TNR distribution, and the parametric-parsimony parameter counts by independent
Monte Carlo simulation and brute-force enumeration, and all matched to numerical
precision. The issues below are gaps in proof rigor and stated hypotheses, not
incorrect results. No critical (result-breaking) errors were found.

## Critical Issues

None. All theorems verified correct on the merits.

## Major Issues

### M1. The subset probability theorem omits the cross-set independence and identical-distribution hypotheses it relies on, and silently uses Axiom 1 across distinct sets
- **Location**: Section 4 (Relational probabilities), unnamed theorem on `P(X̃ ⊆ Ỹ)` and its proof.
- **Quoted text**: "By element-wise independence and cross-set independence (\cref{asm:cross_set_indep}), the probability is $\gamma = \prod_{j=1}^{u} \left(1 - \Prob{j \in \tilde{X}} \Prob{j \notin \tilde{Y}}\right)$".
- **Problem**: The factorization over `j` requires that the *pair* of events `(j ∈ X̃, j ∉ Ỹ)` be independent across distinct `j`, and within a block that the per-element probabilities be identical. The proof cites `asm:cross_set_indep`, which is stated only in Section 3 (set-theoretic operations) and is scoped there to two sets `Ã_1, Ã_2`. The relational section uses `X̃, Ỹ` and never re-invokes Axiom 1 (element-wise independence) explicitly for the *joint* `(X̃, Ỹ)` process. The step from `P(∀j: j∈X̃ ⇒ j∈Ỹ)` to `∏_j (1 - P(j∈X̃ ∧ j∉Ỹ))` is correct only because the joint indicators across `j` are mutually independent (Axiom 1 applied to the product channel). This is true under the model but is asserted, not derived. A careful reader cannot reconstruct which axiom licenses the product over `j` for a *two-set* event.
- **Fix**: In Section 4, state explicitly that `X̃` and `Ỹ` are independent Bernoulli sets (reuse `asm:cross_set_indep`, and either restate it generically for two named sets or forward-reference it from Section 3 with a sentence noting it applies verbatim). Then add one sentence: "By element-wise independence (Axiom 1) applied to the product process `(1_{X̃}(j), 1_{Ỹ}(j))_{j∈U}`, these joint indicators are mutually independent across `j`, so the probability factors as a product over `j`."
- **Severity**: major
- **Confidence**: high

### M2. The "interval propagation: Union" theorem asserts mixed-monotonicity endpoint selection for the weighted union FNR without proving monotonicity in each variable, and treats the weights `w_i` as constants
- **Location**: Section 5 (Interval arithmetic), `thm:uncertain_rates_union`, second half.
- **Quoted text**: "Since the union FNR (\cref{eq:union_fnr}) increases in $\fnrate_1, \fnrate_2$ and decreases in $\fprate_1, \fprate_2$, the upper bound is attained at $(\overline{\fnrate}_1, \overline{\fnrate}_2, \underline{\fprate}_1, \underline{\fprate}_2)$ and the lower bound at $(\underline{\fnrate}_1, \underline{\fnrate}_2, \overline{\fprate}_1, \overline{\fprate}_2)$."
- **Problem**: Two gaps. (a) The monotonicity claims are stated, not shown. The union FNR is `w1 ω1(1-e2) + w2 ω2(1-e1) + w3 ω1 ω2`. The partial derivative with respect to `ω1` is `w1(1-e2) + w3 ω2 ≥ 0` and with respect to `e2` is `-w1 ω1 ≤ 0`, so the claim is true, but the reader must verify it. (b) More importantly, the weights `w1, w2, w3` are themselves functions of the unknown cardinalities and, per Remark on unknown partitions, may *also* be uncertain. The interval theorem treats them as fixed constants. If the `w_i` are uncertain, the endpoint analysis is incomplete because the output also varies with the simplex point `(w1, w2, w3)`. The theorem should either assume the weights are known exactly (state this) or extend the endpoint optimization over the weight simplex.
- **Fix**: Add the one-line sign computation for each partial derivative (it is short). State explicitly that `thm:uncertain_rates_union` assumes the partition weights are known constants, and cross-reference approach (b) in the unknown-partitions remark (optimize over the simplex) for the case where they are not.
- **Severity**: major
- **Confidence**: high

### M3. The two infinite-universe corollaries inherit conditioning hypotheses (`X = Y`, `X ⊆ Y`) that are not restated, making the statements ambiguous
- **Location**: Section 4, the two corollaries beginning "Over an infinite universal set, the probability that two second-order random approximate sets realize the same value is 0" and "...realizes a value that is a subset of another...".
- **Quoted text**: "Over an infinite universal set, the probability that two second-order random approximate sets realize the same value is $0$."
- **Problem**: As stated, the corollary reads as a statement about two arbitrary Bernoulli sets. Its proof, and the parent corollary it specializes, requires `X = Y` (same objective set) for the equality-probability formula to apply; for the subset corollary it requires `X ⊆ Y`. Without the conditioning, "two second-order random approximate sets realize the same value" is underspecified: same objective set? Different? The proof ("Each factor in the equality probability is strictly less than 1...") only makes sense given the parent formula's `X = Y` premise. The result is correct under that premise (I verified the negative-block factor `e1 e2 + (1-e1)(1-e2) < 1` strictly on `(0,1)^2`, max approached but never reaching 1), but the statement must name the premise.
- **Fix**: Restate as "Given `X = Y` with both objective sets fixed, over an infinite universe `P(X̃ = Ỹ) = 0`," and similarly "Given `X ⊆ Y`... `P(X̃ ⊆ Ỹ) = 0`." Add the one-line lemma that each block factor is strictly below 1 on the open parameter square.
- **Severity**: major
- **Confidence**: high

## Minor Issues

### m1. Cross-set independence is introduced as an "assumption" but is really the two-set instance of Axiom 1; relationship to the foundation axioms should be stated
- **Location**: Section 3, `asm:cross_set_indep`.
- **Quoted text**: "The Bernoulli sets $\tilde{A}_1$ and $\tilde{A}_2$ are constructed using independent randomness".
- **Problem**: The paper inherits Axiom 1 (element-wise independence *within* one set) from the foundation paper, then adds cross-set independence as a fresh assumption. This is reasonable (two independently constructed filters), but the logical status is unclear: is this an additional modeling axiom or a derivable consequence? It is an additional assumption (two arbitrary Bernoulli sets need not be independent), so the paper is correct to assume it, but it should say "We additionally assume" and note this does not follow from the foundation axioms.
- **Severity**: minor
- **Confidence**: high

### m2. The "model order of composed sets" remark equates order with "number of distinct partition blocks" but the union FNR uses three positive blocks while the FPR uses one negative block; the resulting order is asserted, not computed
- **Location**: Section 3, `rem:composed_order`.
- **Quoted text**: "The result is therefore a higher-order Bernoulli set (\cref{def:model_order}) whose order equals the number of distinct partition blocks."
- **Problem**: For the union, negatives form a single block (uniform FPR `1-(1-e1)(1-e2)`) while positives split into three blocks. By the foundation paper's definition (order = total number of partition blocks of `U`), the union is order 4 (three positive blocks plus one negative block), consistent with the parsimony remark's "fourth-order." The remark says order equals "number of distinct partition blocks" without doing the count, so the reader must reconcile it with the "fourth-order" claim two remarks later. Stating the count (1 negative block + 3 positive blocks = 4) closes the gap.
- **Severity**: minor
- **Confidence**: high

### m3. The almost-sure convergence remark uses `∏ e_i → 0` without a condition preventing `e_i → 1`
- **Location**: Section 3, "Convergence of intersections of positive approximate sets" remark.
- **Quoted text**: "each negative element survives with probability $\prod_{i=1}^{k} \fprate_i \to 0$."
- **Problem**: `∏ e_i → 0` requires, for instance, `sup_i e_i ≤ c < 1` or `∑(1-e_i) = ∞`. If the `e_i` approach 1 fast enough the product need not vanish. For the intended reading (identically distributed or bounded-away-from-1 rates) the claim is fine, but the hypothesis should be named. The "almost surely" also deserves a word: with independent rounds, survival of a fixed negative element across all `k` is a decreasing event whose probability is the product, and Borel-Cantelli gives a.s. eventual exclusion under `∑ e_i^{(per round)}`-type conditions.
- **Fix**: Add "assuming the rates are bounded away from 1 (e.g., `e_i ≤ c < 1`)".
- **Severity**: minor
- **Confidence**: medium

### m4. Set-difference theorem reuses the symbol `w1, w2, w3` with a third permutation of region-to-weight assignment; correct but a notational hazard
- **Location**: Section 3, `thm:setdiff_rates`, `eq:setdiff_weights`.
- **Problem**: Union weights map `(w1,w2,w3)` to `(A1\A2, A2\A1, A1∩A2)`; intersection weights to `(A1\A2, A2\A1, U\(A1∪A2))`; set-difference weights to `(A1∩A2, U\(A1∪A2), A2\A1)`. Each is internally correct (I verified the set-difference rates by simulation: FNR 0.154 analytic vs 0.1538 sim; FPR 0.043 analytic vs 0.0432 sim), but three different region orderings under the same names invite transcription error by anyone reusing the table. This is a clarity/robustness issue rather than a logic error.
- **Severity**: minor
- **Confidence**: high

## Verified Sound

The following were checked and confirmed correct. Where feasible I used both an
analytic re-derivation and an independent simulation or enumeration.

- **Theorem (Complement error rates)**: FPR and FNR swap. Trivially correct; proof is complete and clean.
- **Theorem (Union FPR)** `1-(1-e1)(1-e2)`: correct. Proof via complementary event and cross-set independence is complete.
- **Theorem (Union FNR)** weighted three-region formula: verified by Monte Carlo (analytic 0.06626 vs sim 0.06625). Proof via law of total probability over the three positive regions is complete and correct.
- **Corollaries (Union of positive / negative sets)**: the positive-set FPR `e1+e2-e1e2` equals `1-(1-e1)(1-e2)` (verified algebraically); both corollaries follow correctly.
- **Theorem (Intersection FNR)** `1-(1-ω1)(1-ω2)`: correct, dual to union FPR; proof complete.
- **Theorem (Intersection FPR)** weighted three-region formula: verified by Monte Carlo (analytic 0.02690 vs sim 0.02691). Proof complete.
- **Corollaries (Intersection of positive / negative sets)**: follow correctly from the general formulas.
- **Theorem (Set difference rates)**: verified by Monte Carlo (FNR 0.154 vs 0.1538; FPR 0.043 vs 0.0432). The reduction `A1\A2 = A1 ∩ A2^c` and substitution of complemented rates is valid; proof complete.
- **De Morgan duality remark**: the claim that union FPR and intersection FNR share functional form, justified by complementation swapping FPR and FNR, is correct.
- **Closure theorems (positive under intersection; negative under union)**: correct; proofs follow from the corollaries with the nonnegativity observations, which hold.
- **Production grammar for positive/negative expressions**: the justification via De Morgan plus the closure theorems is logically valid. The grammar correctly characterizes a sufficient (not claimed necessary) class.
- **Subset probability theorem** `(1-τ1ω2)^|X| (1-e1ω2)^{|Y|-|X|} (1-e1η2)^{|U|-|Y|}`: verified by brute-force enumeration (0.4492121879 vs 0.4492121879). Block-2 uses `e1` correctly (since `j ∉ X`). Result correct; see M1 on the missing independence justification.
- **Equality probability corollary** `(τ1τ2+ω1ω2)^|X| (e1e2+η1η2)^{|U|-|X|}`: verified by enumeration (0.2049977748 vs 0.2049977748). Correct.
- **Equal-parameter equality corollary** `(τ^2+ω^2)^|X| (e^2+η^2)^{|U|-|X|}`: correct specialization.
- **Positive-set subset corollary** `(1-τ1ω2)^|X|`: correct (factors 2 and 3 collapse to 1 when `e1=0`).
- **Infinite-universe corollaries**: correct results given the inherited conditioning; see M3 on restating the premise. The strict-inequality-per-factor argument is valid (I confirmed each block factor stays strictly below 1 on the open parameter square).
- **Asymptotic TNR of union** `Normal(η1η2, η1η2(1-η1η2)/n)`: mean and variance both correct (per-element Bernoulli(`η1η2`); verified mean 0.85484 vs 0.85500 and variance 0.000621 vs 0.000620).
- **Parametric parsimony counts**: "fourth-order channel on 4 symbols has 4×3=12 parameters, Kronecker factorization reduces to 4," and the general `2m` vs `2^m(2^m-1)` claim, are arithmetically correct (verified for m=1,2,3).
- **Monoid structure remark**: associativity and commutativity inherited from `2^U`, identities `∅` and `U` under the degenerate-case axiom. Correct as stated.
