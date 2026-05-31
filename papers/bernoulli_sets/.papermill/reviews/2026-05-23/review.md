# Multi-Agent Review Report

**Date**: 2026-05-23
**Paper**: Bernoulli sets: a model for random approximate sets
**Recommendation**: minor-revision

## Summary

**Overall Assessment**: The paper is in good shape. The 18-page post-extraction manuscript is a clean foundational paper with two axioms, eight theorems, and an ADT formulation that downstream papers (cipher-maps, maximizing-confidentiality, the bernoulli companion series) can rely on. All proofs are correct, all numerical data reproducible, the build is clean, and the bibliography is fully consistent. One substantive technical issue remains: a notation conflict in the rate-argument order on line 157 of bernoulli_model.tex that also has a semantic mismatch in its accompanying prose (P1 = L1). The four other findings from the prior review (2026-03-19) that were flagged as minor are still present and should be addressed before submission.

**Strengths**:
1. Two axioms entail the full distributional theory; the dependency-tracking remarks (3.1 axiom economy, 3.5 notational convention) explicitly map which axiom drives which result (source: logic-checker, methodology-auditor).
2. The k-fold composition figure data is reproducible: all 42 numerical values match independent recomputation to 8 decimal places (source: logic-checker).
3. The ADT formulation provides a clean specification that downstream papers in the trapdoor-computing program consume faithfully (source: methodology-auditor, novelty-assessor).
4. Notation matches conventions in the broader program (cipher-maps uses identical Greek-letter rates) (source: prose-auditor, literature-context).
5. Honest novelty framing: Remark 3.1 explicitly identifies the per-element binary channel model as classical (Shannon, Warner) and limits the novelty claim to the set-level axiomatic framework and composition theorem (source: novelty-assessor).
6. Clean build, all citations resolve, no unused bib entries (source: format-validator, citation-verifier).

**Weaknesses**:
1. Line 157 has a rate-argument order swap and a semantic prose error (source: logic-checker, prose-auditor; cross-verified).
2. The opening sentence of Section 3 (line 7 of bernoulli_model.tex) has a subject-verb agreement error and was already flagged in the 2026-03-19 review; it remains unchanged (source: prose-auditor).
3. Companion-paper paragraph repeated almost verbatim across introduction and conclusion (source: prose-auditor; carried from prior review).

**Finding Counts**: Critical: 0 | Major: 1 | Minor: 9 | Suggestions: 8

## Critical Issues

None.

## Major Issues

### M1: Rate-argument order swap and semantic mismatch in line 157 (source: logic-checker L1, prose-auditor P1)
- **Location**: `sections/bernoulli_model.tex` line 157.
- **Quoted text**: `$\Set{A} \, \AT{\SetUnion}[\fprate][\tprate] \, \Set{B} \sim \AT{(\SetUnion[\Set{A}][\Set{B}])}[\tprate][\fprate]$ where $\AT{\SetUnion}[\fprate][\tprate]$ maps negatives to positives with probability $\fprate$ and maps positives to negatives with probability $\tprate$.`
- **Problem**: Two issues. (a) The right-hand-side subscript order `[\tprate][\fprate]` is reversed from the consistent convention `[\fprate][\tprate]` used throughout the paper (line 103: `\tilde{X}[\fprate][\tprate]`, line 134: `\ctor{\fprate}{\tprate}`, line 163: `\APFun{id}[\fprate][\tprate]`, line 169: same). (b) The prose says `\tprate` is the rate at which positives go to negatives. The rate at which a positive becomes a negative is the false negative rate (`\fnrate = 1 - \tprate`), not the true positive rate. A careful reader will notice the inconsistency and either be confused or assume an error.
- **Suggestion**: Standardize the subscript to `[\fprate][\tprate]` on both sides. Rewrite the prose: "where $\AT{\SetUnion}[\fprate][\tprate]$ retains positives with probability $\tprate$ and admits negatives with probability $\fprate$ (equivalently, maps positives to negatives with probability $\fnrate$ and negatives to positives with probability $\fprate$)."
- **Cross-verified**: Yes. Both logic-checker (L1) and prose-auditor (P1) independently flagged this. Methodology-auditor did not flag it but reviewed the surrounding ADT formulation and found no deeper conceptual issue: the rest of the framework is consistent, so line 157 is a localized typo, not a systematic confusion.

## Minor Issues

### m1: Theorem 4.2 PMF subscript inconsistency (source: logic-checker L2)
- **Location**: `sections/distributions.tex` lines 58 vs 77.
- **Quoted text**: Theorem statement (line 58): `$p_{\alpha_n}(\fprateob | \fprate) = p_{\FP_n}(\fprateob n | \fprate)$`. Proof (line 77): `$p_{\alpha_n}(\fprateob_n | \fprate) = p_{\FP_n}(n \fprateob)$`.
- **Problem**: Proof uses `\fprateob_n` subscript and drops `| \fprate` conditioning from the RHS; theorem statement omits subscript and keeps conditioning. Pick one form.
- **Suggestion**: Standardize on `$p_{\alpha_n}(\fprateob | \fprate) = p_{\FP_n}(n \fprateob | \fprate)$` (no subscript, conditioning preserved on both sides; argument order `n \fprateob` reads more naturally).
- **Cross-verified**: No; single-source finding but high confidence.

### m2: Implicit conditioning on R in joint density factorization (source: logic-checker L3)
- **Location**: `sections/bernoulli_model.tex` lines 122-127.
- **Quoted text**: `$f(\tilde{X}, \alpha, \beta) = f(\tilde{X} | \alpha, \beta) f(\alpha | R) f(\beta | R)$`.
- **Problem**: LHS has no explicit conditioning on R but RHS does. This is correct (because `\tilde{X}` absorbs the conditioning) but visually opaque.
- **Suggestion**: Add a brief parenthetical "(where $\tilde{X}$ denotes $\tilde{R}$ conditioned on $R = X$, as above)" after the equation.

### m3: Opening sentence of Section 3 (source: prose-auditor P2; carried from 2026-03-19)
- **Location**: `sections/bernoulli_model.tex` line 7.
- **Quoted text**: "In the \emph{Bernoulli} set model, we describe the statistical properties of processes that \emph{generate} approximations of a certain kind that model many existing processes and generalizes to higher-order approximations under algebraic composition."
- **Problem**: Convoluted nested clauses, vague phrase "of a certain kind that model many existing processes", and a subject-verb agreement error ("processes ... generalizes").
- **Suggestion**: Rewrite, e.g., "The Bernoulli set model describes a class of random set-generating processes: those whose element-wise errors are independent and identically distributed within partition blocks. This class subsumes many practical implementations and is closed under algebraic composition."

### m4: Repetitive companion-papers paragraph (source: prose-auditor P3; carried from 2026-03-19)
- **Location**: `sections/conclusion.tex` lines 20-23 vs `sections/intro.tex` lines 36-38.
- **Problem**: The conclusion repeats the introduction's companion-papers paragraph almost verbatim.
- **Suggestion**: Condense the conclusion to a single sentence: "The compositional algebra, classification measures, entropy, approximate maps, and algebraic data types are developed in companion papers [bernoulliComposition, bernoulliMeasures, bernoulliEntropy, bernoulliMaps]."

### m5: Complement notation mismatch in notation reference (source: prose-auditor P4; carried from 2026-03-19)
- **Location**: `sections/appendix.tex` line 42 vs `sections/algebra_of_sets.tex` line 26.
- **Quoted text**: Notation reference: `$\Set{A}^C$`; body: `$A^c$`.
- **Problem**: Uppercase C in notation reference vs lowercase c in body.
- **Suggestion**: Change appendix line 42 to `$\Set{A}^c$`.

### m6: Generative model vs random variable ambiguity (source: prose-auditor P5)
- **Location**: `sections/bernoulli_model.tex` lines 97-98.
- **Quoted text**: "We denote the second-order random approximate set generative model by $\tilde{R}$..."
- **Problem**: The shift between "generative model", "approximate set" and "random variable" interpretations of `\tilde{R}` is ambiguous. Later uses parameterize `\tilde{X}[\fprate][\tprate]` as if it were a parameterized distribution.
- **Suggestion**: State once that `\tilde{R}` refers to a random subset of U drawn from the parameterized Bernoulli model and stick with that interpretation.

### m7: Notation reference includes unused symbols (source: prose-auditor P6; carried from 2026-03-19)
- **Location**: `sections/appendix.tex` lines 35-36, 82.
- **Problem**: Cartesian products, n-fold products, CDF notation, and set difference appear in the notation reference but not in the active paper body.
- **Suggestion**: Trim the notation reference to symbols used in the active 18-page paper.

### m8: Ribbon filter citation is the arXiv preprint (source: citation-verifier C1; carried from 2026-03-19)
- **Location**: `references.bib` lines 99-104.
- **Problem**: The Ribbon filter paper has a published venue (ICDE 2022 workshop / ALENEX 2023); the bib entry retains the arXiv preprint form.
- **Suggestion**: Update to the published venue or add `note={Preprint}` for transparency.

### m9: Frequentist interchangeability phrasing (source: methodology-auditor M3)
- **Location**: `sections/bernoulli_model.tex` line 142.
- **Quoted text**: "Two data types that model Bernoulli sets with the same expected error rates are interchangeable in the frequentist sense: at the limit of repeated independent runs, they produce the same distribution over outcomes."
- **Problem**: "The same distribution over outcomes" is ambiguous; a tighter statement is more useful.
- **Suggestion**: Replace with "they induce the same joint distribution on $\{0,1\}^U$ (the indicator vector of the approximate set)".

## Suggestions

1. **"Follows the same logic" proofs should spell out substitutions** (source: methodology-auditor M1). For Theorems 4.3, 4.4 and Corollaries 4.1, 4.3, add explicit substitution mappings rather than stopping at "follows the same logic".

2. **Decide the fate of code/ and data/** (source: methodology-auditor M2). 17 CSVs and 2 C++ simulations remain in the repo but are unused by the compiled paper. Either move to companion papers or document them.

3. **Promote parametric parsimony in the contribution list** (source: novelty-assessor N2). The Kronecker factorization observation in Remark 3.4 is a novel angle; consider promoting it to the introduction's enumerated contribution list.

4. **One-sentence program-context signal** (source: novelty-assessor N1). A one-sentence note that this framework has been used as the error layer in encrypted-search / oblivious-computation contexts would help reviewers calibrate the foundational role.

5. **Equation labels** under definitions should use `eq:` prefix not `def:` (source: format-validator F1). Rename `def:sample_fprate`, `def:sample_tprate` to `eq:sample_fprate`, `eq:sample_tprate`. (Carried from prior review.)

6. **Section label typo** (source: format-validator F2). Rename `sec:asymtotic` to `sec:asymptotic` and update references. (Carried from prior review.)

7. **Link colors for print** (source: format-validator F3). Switch to `colorlinks=false` for print venues; keep colored for web. (Carried from prior review.)

8. **Bibliography naming coordination** (source: citation-verifier C3). When this paper goes to arXiv, update the cipher-maps `bernoulli-types` citation to point to the specific arXiv ID for `bernoulli_sets`. This is a downstream coordination item, not a fault of this paper.

## Detailed Notes by Domain

### Logic and Proofs (logic-checker)

All eight theorems, one proposition, four corollaries, and the appendix Hoeffding-plus-Borel-Cantelli proof verified correct. The chain from axioms to distributional results is sound. The composition figure data (42 numerical values) matches independent computation exactly. One major notation issue (M1) and two minor notation issues (m1, m2).

### Novelty and Contribution (novelty-assessor)

Two axioms, binomial error counts, channel-matrix composition, confidence intervals, ADT formulation, and parametric parsimony. The per-element binary channel model is acknowledged as classical (Shannon, Warner) and the novelty claim is properly limited to the set-level framework. The contribution is real but small in absolute terms; its significance is amplified by its foundational role in the bernoulli and trapdoor-computing programs. Promoting the parametric-parsimony observation could strengthen the standalone contribution signal.

### Methodology (methodology-auditor)

The axiomatic methodology is appropriate. Axiom-economy tracking (Remark 3.2) is exemplary. Proofs use standard probability tools correctly. The "follows the same logic" pattern for symmetric results should be tightened with explicit substitution mappings. The ADT abstraction is faithful to how downstream papers (cipher-maps) consume it.

### Writing and Presentation (prose-auditor)

The prose is competent and the narrative arc is intuitive. The new Remark 3.5 (Notational convention for alpha and beta) is a model response to a prior reviewer concern. Five carried-over minor issues from the 2026-03-19 review remain (opening sentence of Section 3, repetitive companion-paper paragraph, complement notation mismatch, generative model ambiguity, unused notation reference symbols) plus one major issue (line 157).

### Citations and References (citation-verifier)

All 22 bibliography entries are cited; no orphans. Classical references (Shannon, Feller, Cover-Thomas, Hoeffding, Mitzenmacher-Upfal) are accurate. Probabilistic data structure references accurate except for the Ribbon filter citation (arXiv preprint instead of published venue). Four `@Unpublished` companion-paper entries plus phf require publication-strategy planning before submission.

### Formatting and Production (format-validator)

Clean three-pass build to 18 pages with no errors. The only build warning is a benign microtype font message. All cross-references resolve. Two label-naming nits (`def:` prefix on equation labels; `sec:asymtotic` typo) are zero-cost to fix.

## Self-containedness Assessment

The paper is **self-contained for its stated scope**. None of its eight theorems, one proposition, four corollaries, or the appendix proof depends on a result from an unpublished companion paper. The forward references to bernoulliComposition, bernoulliMeasures, bernoulliEntropy, and bernoulliMaps are scoping signals, not load-bearing citations.

That said, two pragmatic concerns:

1. **Five `@Unpublished` entries** (phf, bernoulliComposition, bernoulliMeasures, bernoulliEntropy, bernoulliMaps) all describe work that is either in preparation or not publicly available. A reviewer asking "where is the perfect hash filter result that you use as a running example?" cannot follow the citation. Strategy: arXiv-publish at least the four companion papers and phf before submission.

2. **The user's prior expectation** (per the request) was that this paper contains the information-theoretic lower bound `-log2(fprate)` and the Bloom filter absolute efficiency `ln 2 ≈ 0.69`. Those results are no longer in the compiled paper. They were extracted to `sections/entropy.tex` (not compiled here) and will reside in the companion `bernoulliEntropy` paper. This is a deliberate scope decision that should be communicated to anyone (including downstream paper authors) who has been relying on the prior content.

## Consistency with Cipher-Maps and Maximizing-Confidentiality

Cross-checked notation:
- `\fprate`, `\fnrate`, `\tprate`, `\tnrate` all match.
- The composition formula in cipher-maps Section 6 (Relationship to the Bernoulli Model) is `\eta_{g \circ f} \leq 1 - (1 - \eta_f)(1 - \eta_g)`, which is the inequality form of this paper's Theorem 3.2 equality (cipher-maps uses inequality because seeds are fixed deterministically; this paper assumes the rates are exact).
- Cipher-maps describes the Bernoulli framework as having a "layered type hierarchy: Bool → Set → Map → Relation → Type" (line 2065). This paper supplies the Set layer and treats the Boolean universe as an example (Example 3.1, Remark 3.7 / "Membership tests as Bernoulli Booleans"). This is consistent.
- Cipher-maps cites this framework under `bernoulli-types` and titles it "Bernoulli Sets and Maps: A Probabilistic Framework for Approximate Data Structures". When this paper goes to arXiv, the cipher-maps bib entry should be updated to cite the specific arXiv ID.

Maximizing-confidentiality (in trapdoor-computing/papers/) does not currently cite the Bernoulli framework directly. If it should, a new citation will need to be added.

## Literature Context Summary

The bernoulli_sets paper bridges probabilistic data structures and abstract data type theory. The field has many well-analyzed individual structures (Bloom 1970, cuckoo 2014, xor 2020, ribbon 2021) and surveys (Broder-Mitzenmacher 2004; Tarkoma et al. 2012) but lacks a unified axiomatic framework. The claimed gap is valid. The per-element binary channel model is classical (Shannon 1948, Warner 1965), but the set-level axiomatization with composition theorem and ADT formulation is not present in prior work. The paper's citation coverage is appropriate for its scope.

## Review Metadata

- Specialists run: logic-checker, novelty-assessor, methodology-auditor, prose-auditor, citation-verifier, format-validator.
- Literature scouts: broad + targeted, merged into literature-context.md.
- Cross-verifications performed: 1 (line 157 issue verified by both logic-checker and prose-auditor; methodology-auditor consulted on whether this reflects a deeper ADT confusion and concluded it does not).
- Disagreements noted: 0.
- All quoted text verified against the manuscript by the area chair before inclusion.
