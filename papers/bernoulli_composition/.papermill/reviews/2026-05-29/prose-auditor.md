# Prose Audit Report

## Summary

The writing is generally clear, well-structured, and appropriately terse for a
companion paper. The set-theoretic section (Section 3) is the strongest:
operation, theorem, proof, corollaries, then a summary table and remarks, in a
clean rhythm. The two weak spots are Section 4 (Relational probabilities), where
the notation abruptly shifts and three of the theorem and corollary blocks are
unnamed, and Section 5 (Interval arithmetic), which reads like a less-finished
draft with several loose sentences and a redundant re-introduction of confidence
intervals. No meaning is lost anywhere; the issues are confusion and roughness,
not communication failure.

## Critical Issues

None.

## Major Issues

### M1. Section 4 silently switches notation from subscript-pair to superscript-subscript and from `Ã` to `X̃, Ỹ`, with inconsistent rate naming
- **Location**: Section 4 (Relational probabilities), throughout; contrast with Section 3.
- **Quoted text**: Section 4 opens "given $x \in A$, $x \in \tilde{A}^\fprate_\tprate$ with probability $\tprate$" and the subset theorem uses "$\tilde{X}$ has a false positive rate $\fprate_1$ and a true positive rate $\tprate_1$"; Section 3 consistently writes "$\tilde{A}_1$ ... false positive rate $\fprate_1$ and false negative rate $\fnrate_1$".
- **Problem**: Three shifts happen at once at the section boundary: (1) the operand names change from `Ã_1, Ã_2` to `X̃, Ỹ`; (2) the rate parameterization changes from the (FPR, FNR) pairing used in Section 3 to a (FPR, TPR) pairing written as a super and subscript `\tilde{X}^{\fprate}_{\tprate}`; (3) the subset theorem then mixes both, naming `e1, τ1` for `X̃` but using `ω2 = 1-τ2` (FNR) inside the formula. A reader carrying Section 3's conventions forward has to re-derive which symbol is which. Nothing is wrong, but the cognitive tax is real and avoidable.
- **Suggested fix**: Standardize on one operand naming (`Ã_1, Ã_2`) and one rate display across Sections 3 to 5. If the superscript-subscript form is wanted for `X̃`, introduce it once in Preliminaries and use it everywhere; otherwise keep the inline "(FPR `e1`, TPR `τ1`)" phrasing consistently. Add a single sentence at the top of Section 4 mapping the relational notation to Section 3's.
- **Severity**: major
- **Confidence**: high

### M2. Three of the four relational results are unnamed (bare "Theorem" / "Corollary"), and two carry near-identical statements, making them hard to reference and easy to confuse
- **Location**: Section 4; the subset theorem and the four corollaries.
- **Quoted text**: The block headers read only "\begin{theorem}" and "\begin{corollary}" with no title, e.g., the equality result is "Corollary [unnamed]" and the two infinite-universe results are both unnamed corollaries beginning "Over an infinite universal set...".
- **Problem**: Section 3's results all have descriptive titles ("Union false positive rate", "Closure of positive Bernoulli sets under intersection"), which makes them quotable and cross-referenceable. Section 4 drops titles entirely. Worse, two consecutive corollaries both begin "Over an infinite universal set, the probability that..." and differ only in equality vs subset; without titles a reader skims past the distinction. The label `cor:equality_prob` exists but is never referenced (confirmed: it is among the unreferenced labels), so the equality result cannot currently be cited from elsewhere by name.
- **Suggested fix**: Title every result in Section 4: "Subset probability", "Equality probability", "Equality probability (equal parameters)", "Subset probability (positive sets)", "Zero-probability of exact equality (infinite universe)", "Zero-probability of containment (infinite universe)". Ensure each has a referenced label.
- **Severity**: major
- **Confidence**: high

## Minor Issues

### m1. Section 5 redundantly re-introduces confidence intervals already given in Preliminaries, and the two passages risk reader confusion about which "interval" is meant
- **Location**: Section 5, paragraphs beginning "We may not be interested in the expected value..." and "Intervals represent an uncertainty and they manifest themselves in two independent ways."
- **Quoted text**: "the realized true positive rate $\tprateob$, which is normally centered around the expected true positive rate $\tprate$ ... A set sampled from $\tilde{A}[\fprate][\tprate]$ is an approximate set such that the $\gamma\cdot 100\%$ asymptotic confidence intervals for the realized false negative and false positive rates are respectively given by ..." (then restates the CLT confidence intervals already in `eq:conf_fpr`, `eq:conf_tpr`).
- **Problem**: The confidence-interval formulas appear in Preliminaries (`eq:conf_fpr`, `eq:conf_tpr`) and are restated here almost verbatim. The section does usefully distinguish two notions (statistical confidence interval vs interval-arithmetic uncertainty), which is a good point, but the restatement of the formulas is padding and the prose around it is the roughest in the paper ("they manifest themselves in two independent ways" is vague). The distinction deserves two crisp sentences, not a re-derivation.
- **Suggested fix**: Replace the restated formulas with a cross-reference ("see `eq:conf_fpr`, `eq:conf_tpr`") and keep one tight paragraph contrasting (a) sampling uncertainty in the realized rate (a confidence interval) from (b) epistemic uncertainty in the expected rate parameter (an interval-arithmetic input). This is the conceptual payoff; foreground it.
- **Severity**: minor
- **Confidence**: high

### m2. The abstract and contribution list under-sell the genuinely new results and lead with the most standard one
- **Location**: Abstract; Introduction contribution list item 1.
- **Quoted text**: "We derive closed-form error rates for complement, union, intersection, and set difference, showing that every such operation ... yields a (possibly higher-order) Bernoulli set".
- **Problem**: The union FPR and complement are the least novel pieces (folklore; see novelty report), yet they lead. The cardinality-weighted FNR-of-union and FPR-of-intersection, and the subset and equality probabilities, are the actual advances and are described generically ("closed-form error rates ... and ... relational predicates"). A reader skimming the abstract cannot tell that the overlap-dependent rates and the predicate probabilities are where the new content lives.
- **Suggested fix**: In the abstract, name the distinctive results: "...including overlap-dependent (cardinality-weighted) rates for the union's false negatives and the intersection's false positives, and closed-form subset and equality probabilities that vanish as the universe grows." One added clause changes the reader's sense of the contribution.
- **Severity**: minor
- **Confidence**: high

### m3. "Relational probabilities" section title and opening sentence are slightly mislabeled relative to content
- **Location**: Section 4 title and first sentence.
- **Quoted text**: "\section{Relational probabilities}" then "The relational \emph{member-of} predicate $\in : U \times 2^U \to \{0,1\}$ is the set-indicator function".
- **Problem**: The section computes probabilities of *relational predicates between two approximate sets* (subset, equality), but opens with a paragraph on the membership predicate that mostly restates Preliminaries. The genuinely new material (subset and equality probabilities) starts a third of the way in. The lead-in feels like throat-clearing.
- **Suggested fix**: Open with the question the section answers ("Given two Bernoulli sets, what is the probability that one is a subset of the other, or that they are equal?"), then introduce the predicates, then the theorems. Move or compress the membership-predicate recap.
- **Severity**: minor
- **Confidence**: medium

### m4. Minor wording and typographic roughness in Section 5
- **Location**: Section 5.
- **Quoted text**: "In our case, the formulae are simple enough to ensure dependencies are satisfied."; "The more certain---the smaller the width of the intervals---the more certain the output rate."
- **Problem**: "ensure dependencies are satisfied" is imprecise (the dependency problem is about avoiding overestimation when a variable appears more than once; "satisfied" is the wrong verb). The second sentence is awkward and repeats "certain" three times. These are local polish items.
- **Suggested fix**: "In our case the formulas are simple enough (each rate appears with consistent monotonicity) that endpoint evaluation gives tight bounds, avoiding the dependency problem." And: "Narrower input intervals yield a narrower output interval."
- **Severity**: minor
- **Confidence**: high

### m5. Several results and the figure are stated but never cross-referenced in prose
- **Location**: Throughout (see format report for the full list).
- **Quoted text**: e.g., `thm:setdiff_rates`, `cor:equality_prob`, `fig:union_fpr`, `rem:monoid`, `rem:parametric_parsimony` are defined but not `\ref`-ed.
- **Problem**: A figure that no sentence points to ("as Figure X shows") reads as decorative; a theorem never referenced later looks orphaned. The set-difference theorem in particular is a headline result yet nothing downstream cites it by number.
- **Suggested fix**: Add at least one in-text reference to the figure and to each major theorem from the summary or conclusion ("the four operations are collected in Table 1; see Theorems ... ").
- **Severity**: minor
- **Confidence**: high

## Structural Assessment

- **Abstract**: adequate. Accurate and self-contained, but leads with the least
  novel result; see m2.
- **Introduction**: strong. Clear problem statement (compositional question),
  explicit three-item contribution list, clean organization paragraph.
- **Narrative flow**: adequate. Sections 1 to 3 flow well; the Section 3 to 4
  boundary has a notation discontinuity (M1); Section 5 reads less finished.
- **Notation consistency**: needs work. The Section 4 shift (M1) is the main
  defect; within Sections 3 and 5 notation is consistent.
- **Figures/tables**: adequate. Table 1 is well-built and genuinely useful. The
  single figure is correct but illustrates only the simplest formula and is not
  referenced in prose (m5; see also methodology m3).
- **Length/balance**: adequate to strong. At ~15 pages the paper is appropriately
  sized for its contribution. Section 5 is the one slightly padded part (m1).

## Strengths

- **Section 3 is a model of clean theorem-paper exposition**: each operation gets
  a stated rate, a complete proof, special-case corollaries, and the four
  operations are consolidated in a single readable table with the De Morgan
  duality drawn out explicitly. The duality remark ("the false positive rate of
  the union has the same functional form as the false negative rate of the
  intersection") is a genuinely illuminating sentence.
- **The worked numerical example** is concrete, correct, and placed exactly where
  a reader wants it (right after the table).
- **The production grammar** for positive and negative expressions is presented
  compactly and its justification paragraph is well-argued.
- **The introduction's framing** ("Without a compositional algebra, each new
  combination requires a bespoke error analysis") states the motivation in one
  memorable sentence.
