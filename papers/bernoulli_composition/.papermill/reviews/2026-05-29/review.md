# Multi-Agent Review Report

**Date**: 2026-05-29
**Paper**: Composition of Bernoulli sets (Alexander Towell)
**Recommendation**: major-revision

## Summary

**Overall Assessment**: The mathematics is correct. Every closed-form error
rate, relational probability, and corollary was independently verified
(analytically and by Monte Carlo / brute-force enumeration) and all hold. The
paper does not require a major-revision because anything is wrong; it requires one
because the proofs of the strongest results have stated-but-unproven steps and
unstated hypotheses, the headline formulas are not yet operational (they depend on
unknown set cardinalities and on a cross-set independence precondition that is
never examined), and the paper omits the standard approximate-set prior art
(Bloom 1970, the Broder and Mitzenmacher survey) that it both motivates itself
with and generalizes. These are all addressable without new theory.

**Strengths**:
1. The cardinality-weighted false-negative rate of the union and false-positive
   rate of the intersection are genuine contributions with no located precedent;
   they compute overlap-dependent behavior that the standard same-set Bloom-filter
   analyses do not (novelty-assessor; confirmed correct by logic-checker via
   simulation).
2. The closed-form subset and equality probabilities, with their infinite-universe
   corollaries, appear genuinely new and are the cleanest results in the paper
   (novelty-assessor; verified exact by logic-checker).
3. Section 3 is model theorem-paper exposition: operation, theorem, complete
   proof, corollaries, consolidated table, and an explicit De Morgan duality
   (prose-auditor).
4. The paper builds clean: 15 pages, three passes, zero unresolved references,
   no phantom or orphan citations, all assets present (format-validator).
5. Scope discipline is good; it stays in its companion lane and does not duplicate
   the foundation paper (novelty-assessor, citation-verifier).

**Weaknesses**:
1. The strongest proofs (subset probability; interval propagation; infinite-universe
   corollaries) state key steps and hypotheses without proving or naming them
   (logic-checker M1, M2, M3).
2. The weighted formulas, which are the novel ones, are not usable in practice as
   written: they need the unknown cardinality `|A1 ∩ A2|`, and the one always-available
   remedy (optimize over the weight simplex) is mentioned in a clause and never
   carried out (methodology-auditor M1).
3. Cross-set independence underlies every result but its common failure mode
   (filters sharing a hash seed have correlated, not independent, errors) is never
   flagged (methodology-auditor M2).
4. Bloom filters and the AMQ survey are invoked rhetorically but never cited, so the
   union result looks like a fresh derivation of folklore and the reader cannot see
   the genuine delta (citation-verifier M1, M2; novelty-assessor positioning).
5. Section 4 changes notation mid-paper and leaves three of four results unnamed,
   two of them near-duplicates (prose-auditor M1, M2).

**Finding Counts**: Critical: 0 | Major: 8 | Minor: 12 | Suggestions: 6

---

## Critical Issues

None. No result is incorrect and the paper compiles.

---

## Major Issues

### 1. Subset-probability proof uses Axiom 1 across two distinct sets without stating it (source: logic-checker M1)
- **Location**: Section 4, subset-probability theorem and proof.
- **Quoted text**: "By element-wise independence and cross-set independence (\cref{asm:cross_set_indep}), the probability is $\gamma = \prod_{j=1}^{u} \left(1 - \Prob{j \in \tilde{X}} \Prob{j \notin \tilde{Y}}\right)$".
- **Problem**: The product over `j` requires the joint indicators `(1_{X̃}(j), 1_{Ỹ}(j))` to be mutually independent across `j`. This is true under the model (Axiom 1 applied to the product process) but is asserted, not derived, and `asm:cross_set_indep` is stated in Section 3 for `Ã_1, Ã_2`, not re-invoked here for `X̃, Ỹ`. The reader cannot reconstruct which axiom licenses the factorization for a two-set event.
- **Suggestion**: State that `X̃, Ỹ` are independent Bernoulli sets and add one sentence invoking Axiom 1 on the product process to justify the product over `j`.
- **Cross-verified**: Yes, by the orchestrator and methodology-auditor. The result itself is correct (brute-force enumeration: 0.4492121879 vs formula 0.4492121879). The finding is an exposition gap, not an error, so it is correctly logged as major (significant gap) rather than critical.

### 2. Interval-propagation (Union) asserts mixed monotonicity without proof and treats uncertain weights as constants (source: logic-checker M2; reinforced by methodology-auditor M1)
- **Location**: Section 5, `thm:uncertain_rates_union`.
- **Quoted text**: "Since the union FNR (\cref{eq:union_fnr}) increases in $\fnrate_1, \fnrate_2$ and decreases in $\fprate_1, \fprate_2$, the upper bound is attained at $(\overline{\fnrate}_1, \overline{\fnrate}_2, \underline{\fprate}_1, \underline{\fprate}_2)$ and the lower bound at $(\underline{\fnrate}_1, \underline{\fnrate}_2, \overline{\fprate}_1, \overline{\fprate}_2)$."
- **Problem**: (a) The monotonicity is stated, not shown (the sign of each partial derivative is a one-liner and should be given). (b) The weights `w1, w2, w3` are themselves uncertain in general (they depend on unknown cardinalities), yet the theorem treats them as fixed; if they vary, the endpoint analysis is incomplete.
- **Suggestion**: Add the partial-derivative signs; state that the theorem assumes known weights, and cross-reference the simplex-optimization remedy for the uncertain-weight case.
- **Cross-verified**: Yes. Monotonicity claims are correct (`∂FNR/∂ω1 = w1(1-e2)+w3 ω2 ≥ 0`, `∂FNR/∂e2 = -w1 ω1 ≤ 0`); the gap is that the paper does not show this.

### 3. Infinite-universe corollaries omit their conditioning hypotheses (source: logic-checker M3; reinforced by prose-auditor M2)
- **Location**: Section 4, the two corollaries beginning "Over an infinite universal set...".
- **Quoted text**: "Over an infinite universal set, the probability that two second-order random approximate sets realize the same value is $0$."
- **Problem**: As stated these read as claims about two arbitrary Bernoulli sets, but the proofs require `X = Y` (equality) and `X ⊆ Y` (subset). Without naming the premise the statements are ambiguous.
- **Suggestion**: Restate with the premise ("Given `X = Y` with both objective sets fixed...") and add the one-line lemma that each block factor is strictly below 1 on the open parameter square.
- **Cross-verified**: Yes. Results correct given the premise; I confirmed the negative-block factor `e1 e2 + (1-e1)(1-e2)` stays strictly below 1 on `(0,1)^2` (max approached at 0.998, never 1).

### 4. The weighted formulas are not operational: unknown cardinalities, no remedy carried through (source: methodology-auditor M1)
- **Location**: Section 3, `rem:unknown_partitions`; Conclusion, "Open problems".
- **Quoted text**: "The partition weights $w_1, w_2, w_3$ require knowledge of the objective set cardinalities ... which are typically unknown in practice. Three approaches handle this: (a) ... interval-valued rates; (b) worst-case bounds ... optimizing the weights over the feasible region; (c) the cardinalities may be estimated from the approximate sets themselves ...".
- **Problem**: The paper's practical claim (Conclusion: "closed-form error rates and confidence intervals for any set-theoretic expression") is undercut: the novel weighted rates cannot be evaluated without `|A1 ∩ A2|`. Remedy (b) is always available (each weighted rate is linear in the weights, so the worst case is a simplex vertex), but it is a single clause and never worked out; (c) is deferred to future work.
- **Suggestion**: Carry through (b): maximize/minimize each weighted rate over the simplex `w1+w2+w3=1, w_i ≥ 0` to get the closed-form guaranteed bounds. A few lines turns three "needs oracle cardinalities" formulas into usable bounds.
- **Cross-verified**: Consistent with logic-checker M2 (same uncertain-weights gap, complementary framing).

### 5. Cross-set independence is strong and its practical failure mode is never examined (source: methodology-auditor M2)
- **Location**: Section 3, `asm:cross_set_indep`.
- **Quoted text**: "The Bernoulli sets $\tilde{A}_1$ and $\tilde{A}_2$ are constructed using independent randomness".
- **Problem**: Every set-operation result depends on this. In practice two Bloom filters built with the same hash family and seed have perfectly correlated errors, not independent ones; for identical filters the union FPR is `e1`, not `1-(1-e1)^2`. A practitioner could misapply the formulas to correlated filters and get systematically wrong estimates.
- **Suggestion**: Add a short paragraph giving the canonical violation (shared seed yields correlated errors), state that the formulas require independent construction, and scope out correlated composition.
- **Cross-verified**: Logic-checker m1 independently flags that this is an added assumption not derivable from the foundation axioms, supporting the methodology concern.

### 6. Section 4 switches notation mid-paper and uses three display forms for one parameterization (source: prose-auditor M1)
- **Location**: Section 4 vs Section 3.
- **Quoted text**: Section 4 line 7: "$x \in \tilde{A}^\fprate_\tprate$"; line 63: "$\tilde{X}[\fprate_1][\tprate_1] = \tilde{Y}[\fprate_2][\tprate_2]$"; line 83: "$\tilde{X}^\fprate_\tprate = \tilde{Y}^\fprate_\tprate$"; vs Section 3's consistent "$\tilde{A}_1$ ... false positive rate $\fprate_1$ and false negative rate $\fnrate_1$".
- **Problem**: Operand names switch (`Ã_1,Ã_2` to `X̃,Ỹ`), rate pairing switches (FPR/FNR to FPR/TPR), and the display alternates between superscript-subscript and the bracket macro, three forms for the same object, within one section. Verified directly: `relational.tex` uses `\tilde{A}^\fprate_\tprate`, `\tilde{X}[..][..]`, and `\tilde{X}^\fprate_\tprate`. Nothing is wrong but the cognitive tax is real.
- **Suggestion**: Standardize operand naming and one rate display across Sections 3 to 5; map the relational notation to Section 3's in one opening sentence.
- **Cross-verified**: Yes (orchestrator re-grepped the section and confirmed all three forms present).

### 7. Three of four relational results are unnamed and two are near-duplicates (source: prose-auditor M2)
- **Location**: Section 4.
- **Quoted text**: bare "\begin{theorem}" / "\begin{corollary}"; two consecutive corollaries both begin "Over an infinite universal set, the probability that...".
- **Problem**: Section 3 titles every result; Section 4 titles none, and the two infinite-universe corollaries differ only in equality vs subset. The equality label `cor:equality_prob` exists but is never referenced, so the result cannot be cited by number.
- **Suggestion**: Title every Section 4 result and ensure each has a referenced label.
- **Cross-verified**: Format-validator independently lists `cor:equality_prob` among unreferenced labels.

### 8. Standard AMQ prior art (Bloom 1970, Broder and Mitzenmacher 2004) is invoked but uncited (source: citation-verifier M1, M2; novelty-assessor positioning)
- **Location**: Introduction and Conclusion (motivation); Section 3 (intersection result).
- **Quoted text**: Conclusion: "A practitioner building a system on Bloom filters need not re-derive the error analysis for each new combination of filters"; Introduction: "database query planners ... routinely compose approximate sets through union, intersection, complement, and difference."
- **Problem**: The paper names Bloom filters as its motivating application, and its union FPR `1-(1-e1)(1-e2)` is the standard independent-filter OR behavior documented in the Broder and Mitzenmacher survey, yet neither work is cited. The reader cannot distinguish the genuine contribution (cardinality-weighted FNR/FPR for distinct sets) from folklore (union FPR for same-array filters). Both entries already exist in the foundation paper's bibliography (`bf`, `broderMitzenmacher`), so importing them is trivial.
- **Suggestion**: Cite Bloom (1970) and Broder and Mitzenmacher (2004) at the motivation and at the union/intersection results; add one sentence stating which behavior is known and which is new.
- **Cross-verified**: Yes. Novelty-assessor flags the same gap as the paper's top positioning risk; methodology-auditor notes the missing folklore baseline.

---

## Minor Issues

1. **Cross-set independence labeled an "assumption" without noting it is an added axiom** not derivable from the foundation axioms (logic-checker m1).
2. **"Model order of composed sets" remark asserts the order without doing the block count** (1 negative + 3 positive blocks = 4); reconcile with the "fourth-order" parsimony remark (logic-checker m2).
3. **Almost-sure-convergence remark uses `∏ e_i → 0` without a bounded-away-from-1 condition** on the rates (logic-checker m3).
4. **Set-difference theorem reuses `w1, w2, w3` with a third region-to-weight permutation**; correct but a transcription hazard (logic-checker m4).
5. **Single numerical example covers only the union**; the more error-prone intersection and difference formulas get no worked numeric anchor (methodology-auditor m1).
6. **Remedy (c) claims "computable bias" but gives no expression**; either provide `E|Ã1 ∩ Ã2|` or drop "computable" from the inline remark (methodology-auditor m2).
7. **Figure illustrates only the simplest formula** (union FPR) and its additive-reference line applies to one curve; consider a panel for a weighted rate (methodology-auditor m3, prose-auditor m5).
8. **Section 5 redundantly restates the CLT confidence intervals** already in Preliminaries; replace with a cross-reference and keep the useful two-notions distinction crisp (prose-auditor m1).
9. **Abstract and contribution list lead with the least novel result**; name the overlap-dependent rates and the predicate probabilities (prose-auditor m2, novelty-assessor).
10. **Section 4 title and lead-in over-recap membership**; open with the question the section answers (prose-auditor m3).
11. **Loose wording in Section 5**: "ensure dependencies are satisfied" (wrong verb for the dependency problem) and "the more certain ... the more certain" (prose-auditor m4).
12. **Bibliography author-name formatting inconsistent** (initials vs full names) and `coverThomas` cited without a section pin (citation-verifier m2, format-validator m2).

---

## Suggestions

1. Promote the subset/equality probabilities and the overlap-dependent rates to
   the abstract as co-headline contributions; they are the paper's most defensible
   novelty (novelty-assessor).
2. Add a worked intersection example reusing the union example's cardinalities so
   all three weighted formulas have a checked numeric template (methodology-auditor).
3. Add in-text references to the figure and to the set-difference and equality
   results; several headline labels are currently never `\ref`-ed (format-validator,
   prose-auditor).
4. When the open problem on estimating `|A1 ∩ A2|` is discussed, cite the
   cardinality-estimation-from-filters literature (HyperLogLog inclusion-exclusion,
   filter count estimators) (citation-verifier, novelty-assessor).
5. If targeting PODS or VLDB, connect the monoidal-fold observation to mergeable
   sketches and probabilistic-database set semantics (novelty-assessor, literature
   context).
6. Add stable identifiers (arXiv) to the three unpublished companion citations
   before submission, since the paper's correctness rests on inherited results a
   reviewer must be able to check (citation-verifier m1).

---

## Detailed Notes by Domain

### Logic and Proofs
All results verified correct. The orchestrator and logic-checker independently
reproduced every formula: union FPR/FNR, intersection FPR/FNR, set-difference
rates (Monte Carlo within 0.02% of analytic), subset probability and equality
probability (exact to 10 digits by enumeration), the positive/negative corollaries,
the asymptotic TNR mean and variance, and the `2m` vs `2^m(2^m-1)` parsimony counts.
The three major findings are all exposition/rigor gaps in otherwise-correct proofs:
a missing independence justification in the subset proof (1), unproven monotonicity
and constant-weight assumption in the interval theorem (2), and unstated conditioning
in the infinite-universe corollaries (3). Four minor rigor items round out the
section. No circular reasoning, no non-sequiturs, no overclaim relative to what is
proven.

### Novelty and Contribution
Real but uneven, assessed against the paper's declared companion role (shared
foundations not penalized). Genuine advances: cardinality-weighted union FNR and
intersection FPR (no located precedent), and closed-form subset/equality
probabilities (cleanest novelty, under-advertised). Over-claimed relative to
folklore: union FPR (standard independent-filter OR), complement swap, and the
monoid/semigroup framing (classical skeleton; novelty is the rate propagation).
The "interval arithmetic extension" is a clean application of textbook tools and
should be framed as such. Top positioning risk: without a stated Bloom-filter
baseline a reviewer will ask "isn't the union just OR of filters?"

### Methodology
Pure theory; judged accordingly. Derivations fully reproducible (confirmed). Two
major gaps both about applicability: the novel weighted rates need unknown
cardinalities and no remedy is carried to closure (the linear-in-weights structure
makes the simplex-vertex worst case a few lines away), and the cross-set
independence precondition, on which everything rests, is never examined despite a
common failure mode (shared hash seeds). Minor items: only the union has a worked
example; the "computable bias" claim is unsupported; the figure covers only the
easy formula.

### Writing and Presentation
Section 3 is strong and the introduction frames the problem well. The two major
issues are localized in Section 4 (a three-way notation discontinuity at the
section boundary, and three unnamed/near-duplicate results) and Section 5 (rougher
prose, a redundant CLT restatement). The abstract under-sells the genuinely new
results. None of this loses meaning; it raises reader effort and obscures the
contribution.

### Citations and References
Hygiene is clean: 6 keys, 6 entries, no phantoms, no orphans, all external entries
correctly attributed. The substantive gap is omission of the standard AMQ prior
art the paper motivates itself with (Bloom 1970; Broder and Mitzenmacher 2004),
both already in the family's bibliography. Three unpublished companion self-cites
need stable identifiers before submission; self-citation ratio (3/6) is high but
structurally justified by the companion design.

### Formatting and Production
Production-clean. Builds in three passes with zero errors, zero substantive
warnings, zero unresolved references, no "??" in the PDF, all `\input` files and
`alex.sty` present, the single figure inline (no missing image assets). 15 pages.
Minor: 27 defined-but-unreferenced labels (headline theorem, figure, and equality
corollary among them, signaling missing in-text references) and inconsistent
bibliography name formatting. No venue selected, so a document-class and
citation-style switch will be needed at submission.

---

## Literature Context Summary

With live web search unavailable this pass, the scouts were grounded in the
paper's and the foundation paper's bibliographies plus standard domain knowledge.
High-confidence takeaways: the union FPR is folklore; the Broder and Mitzenmacher
survey discusses union and intersection of Bloom filters and is missing here;
interval-arithmetic and channel-Kronecker tools are used correctly. Medium-confidence
takeaways (flagged for a live-search pass before camera-ready): the
cardinality-weighted intersection FPR and the subset/equality probabilities have no
direct precedent and are the paper's strongest novelty; mergeable-sketch and
probabilistic-database set semantics are the adjacent literatures to engage if
targeting PODS or VLDB. A targeted forward-citation search of the Broder and
Mitzenmacher survey and recent filter papers (2018 to 2025) on terms like "filter
algebra," "mergeable sketches," and "approximate set containment probability" is
recommended to confirm priority.

---

## Review Metadata

- **Agents used**: literature-scout-broad, literature-scout-targeted (merged into
  one context packet), logic-checker, novelty-assessor, methodology-auditor,
  prose-auditor, citation-verifier, format-validator. Orchestrated and
  cross-checked by the area-chair process.
- **Tooling note**: The Task subagent-spawning tool and WebSearch were not
  available in this environment. The orchestrator executed each specialist's
  methodology directly per its agent definition, and performed independent
  numerical verification (Monte Carlo and brute-force enumeration) of every
  quantitative claim. Literature and citation findings about specific competing
  papers are therefore at medium confidence and flagged for a live-search pass;
  build, label, formula, and quote findings are at high confidence.
- **Cross-verifications performed**: 4 (subset-proof reproduction; interval
  monotonicity sign-check; infinite-universe factor bound; uncertain-weights gap
  corroborated across logic and methodology).
- **Hallucination check**: every major-finding quote was re-grepped against the
  manuscript and confirmed verbatim, including the three-way notation forms in
  `relational.tex`. No discarded findings.
- **Disagreements noted**: 0. Where specialists touched the same issue (notation
  vs missing-hypothesis; unknown weights across logic and methodology; missing
  Bloom citations across citation and novelty), the views were complementary, not
  contradictory, and were merged.
