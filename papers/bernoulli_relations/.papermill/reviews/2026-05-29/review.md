# Multi-Agent Review Report

**Date**: 2026-05-29
**Paper**: The abstract data type of the *approximate relation* (Alexander Towell, SIUE; ORCID 0000-0001-6443-9897)
**Role in family**: Extension paper of the 9-paper Bernoulli / random-approximate-set collection (foundation: `bernoulli_sets`). Reviewed relative to that declared role.
**Recommendation**: not-ready

## Summary

**Overall Assessment**: This is an early-stage draft of a genuinely worthwhile idea (a relational-algebra layer over the Bernoulli set model) that is not yet in reviewable condition. It does not compile (multiple independent build-blockers, including the known missing `references.bib` and, more severely, five missing subfiled section files), several of its new theorems have placeholder or unfinished proofs, two definitions contain outright logical errors, and the genuinely novel material is both under-developed and entangled with re-derivations of sibling-paper results. The bones are sound and the contribution is real; the execution is roughly one to two solid drafting passes away from review-ready.

**Strengths**:
1. The core idea (a relation as an approximate set of tuples over a Cartesian-product universe, with join/project/select error propagation) is a natural, useful, and non-duplicative capstone for the family. (novelty-assessor N+1, N+2)
2. The invariant-preservation angle (can a random approximation remain reflexive/symmetric/transitive/functional, and at what rate?) is original relative to both the family and the probabilistic-database literature. (novelty-assessor N+3)
3. The exact relational-algebra preliminaries (join, projection, composition definitions, and a concrete worked join-then-project example) are clear and correct. (logic-checker, prose-auditor)
4. The two inherited foundational theorems that are fully proved (`thm:fpbinom`, `thm:fpr`) are correct restatements of the foundation results. (logic-checker OK-1, OK-2)

**Weaknesses**:
1. The paper does not build. Five of ten subfiled section files are missing, and there is no `references.bib`. (format-validator C-F1, C-F2)
2. Most new claims are unproven: four theorems have placeholder/unfinished proofs (one proof body is the single character `?`; another trails off at "is just the probability that ..."). (logic-checker ML-1..ML-4)
3. Two definitions are logically wrong as typeset: a conditional probability conditions an event on its own negation, and the rate-argument order is inconsistent (FNR-first vs TPR-first) across sections. (logic-checker CL-1, CL-2; confirmed by methodology-auditor)
4. The equality-predicate formula is incorrect (an inapplicable inclusion-exclusion term). (methodology-auditor cross-check of ML-5)
5. Two sections re-derive sibling-owned results (map composition belongs to `bernoulli_maps`; subset/equality rates to `bernoulli_composition`), and the abstract over-claims scope (promising entropy bounds and perfect-hash-map constructions owned by other papers) while under-weighting the join/project material that is actually this paper's. (novelty-assessor N-1, N-3; prose-auditor PR-1, PR-2)
6. The nearest external prior art, probabilistic/uncertain databases, is never mentioned. (novelty-assessor N-2; citation-verifier CV-3)

**Finding Counts**: Critical: 5 | Major: 14 | Minor: 13 | Suggestions: 6

## Critical Issues

### C1. Paper does not compile: five missing subfiled section files (source: format-validator)
- **Location**: `main.tex` lines 110-119 (`\subfile{}` calls)
- **Quoted text**: `\subfile{sections/intro}` ... `\subfile{sections/rel_algebra}` ... `\subfile{sections/test}` ... `\subfile{sections/unused/optimality}` ... `\subfile{sections/unused/oblivious_rel_model}`
- **Problem**: `sections/intro.tex`, `sections/rel_algebra.tex`, `sections/test.tex`, `sections/unused/optimality.tex`, and `sections/unused/oblivious_rel_model.tex` do not exist on disk (the `sections/unused/` directory does not exist; `oblivious_rel_model.tex` exists one level up). With `-shell-escape`, the build dies fatally at the first missing file (`intro`): `! LaTeX Error: File 'sections/intro.tex' not found. ==> Emergency stop.` This is more severe than the state file recorded (which noted only the bibliography).
- **Suggestion**: Create the five files (one-line stubs suffice to restore a clean build), or comment out the four not-ready `\subfile{}` lines and redirect the fifth to the existing `sections/oblivious_rel_model.tex`. Make `main.tex`'s subfile list correspond 1:1 to files on disk.
- **Cross-verified**: Reproduced directly by the area chair via two `pdflatex` runs (with and without `-shell-escape`). Confirmed.

### C2. No `references.bib`; every citation unresolved (source: format-validator, citation-verifier) [HEADLINE, known pre-existing]
- **Location**: `main.tex` line 121
- **Quoted text**: `\bibliography{references}`
- **Problem**: No `references.bib` exists anywhere in the tree. `bibtex main` fails and all `\cite` render as `[?]`. Distinct keys used: `aset`, `bf`, `phf`, `approxrel`. This is a known, pre-existing gap (recorded in `state.md`), reported here as the top formatting issue per the review brief. It is currently *masked* by C1: the build dies before bibtex runs, so creating the bibliography alone will not yield a PDF; C1 and C2 must both be fixed.
- **Suggestion**: Create `references.bib`. Seed it from `bernoulli_sets/references.bib` (which already defines `bf` and `phf` verbatim), add an `aset` entry (the foundation paper), an `approxrel` self/companion reference, and the external anchors below (Codd, probabilistic databases). A `references.bib` must be created before the paper compiles cleanly.
- **Cross-verified**: `find ... -name '*.bib'` returns nothing; confirmed by both format-validator and citation-verifier.

### C3. Definition `def:approx_pfun` condition (ii) conditions an event on its own negation (source: logic-checker; cross-verified by methodology-auditor)
- **Location**: `sections/properties.tex` line 233 (Definition `def:approx_pfun`)
- **Quoted text**: `\Prob{\Tuple{\RV{X}} \in \Dom(\APFun{f}) \Given \Tuple{\RV{X}} \notin \Dom(\APFun{f})} = \fprate`
- **Problem**: The conditioning event is `\notin \Dom(\APFun{f})` (the approximate function), so the display conditions `X ∈ Dom(approx f)` on its own complement; that probability is identically 0, not `\fprate`. The prose ("not in the domain of `f`") shows the intended conditioning set is the *objective* function's domain.
- **Suggestion**: Change the conditioning event to `\Tuple{\RV{X}} \notin \Dom(\PFun{f})` (matching condition (i) directly above, which is correct).
- **Cross-verified**: Yes, by methodology-auditor, independently reproduced. CONFIRMED critical. Quote verified verbatim against the manuscript.

### C4. Rate-argument order is inconsistent across the paper, making every rate-bearing statement ambiguous (source: logic-checker, prose-auditor; cross-verified by methodology-auditor)
- **Location**: `sections/approx_rel_model.tex` (Definition `def:approx_rel`) vs. `sections/properties.tex` (symmetric theorem; map notation)
- **Quoted text**: `\ARelation{R}[\fnrate][\fprate]` (FNR-first, in def:approx_rel) vs. `\ARelation{R}(\tprate,\fprate)` (TPR-first, in the symmetric-relation theorem)
- **Problem**: The `\ARelation` macro assigns no intrinsic meaning to its two optional slots (subscript/superscript only). One section uses (FNR, FPR), another uses (TPR, FPR). Since `TPR = 1 − FNR`, the reader cannot tell whether slot 1 is an error rate or a success rate without re-deriving from context, and any downstream formula that plugs a rate into slot 1 is off by a complement. In `def:approx_rel` the *same* pair `[\fnrate][\fprate]` labels both a false-negative display and a false-positive display.
- **Suggestion**: Adopt one family-standard ordering (e.g., `(\tprate,\fprate)` or `(\fprate,\fnrate)`) and apply it uniformly; consider self-documenting notation.
- **Cross-verified**: Yes, by methodology-auditor (confirmed it propagates into the math, not merely cosmetic). CONFIRMED critical.

### C5. Equality-predicate formula is incorrect (source: methodology-auditor, upgrading logic-checker ML-5)
- **Location**: `sections/predicates.tex` lines 50-53
- **Quoted text**: `(\tprate_1 \tprate_2 + \fnrate_1 \fnrate_2 - \tprate_1 \tprate_2 \fnrate_1 \fnrate_2)^{\Card{\Set{A}}} (\fprate_1 \fprate_2 + \tnrate_1 \tnrate_2 - \fprate_1 \fprate_2 \tnrate_1 \tnrate_2)^{\Card{\Set{U}} - \Card{\Set{A}}}`
- **Problem**: For two independent approximate observations to *agree* on a true member, the per-element probability is `P(both in) + P(both out) = \tprate_1\tprate_2 + (1-\tprate_1)(1-\tprate_2) = \tprate_1\tprate_2 + \fnrate_1\fnrate_2`. "Both in" and "both out" are mutually exclusive, so there is no inclusion-exclusion correction. The subtracted term `-\tprate_1\tprate_2\fnrate_1\fnrate_2` (and its off-`A` analog) is the `P(A∪B)=P(A)+P(B)−P(A)P(B)` structure for independent *overlapping* events, which does not apply here. The term should be deleted.
- **Suggestion**: Correct to `(\tprate_1\tprate_2 + \fnrate_1\fnrate_2)^{|A|}(\fprate_1\fprate_2 + \tnrate_1\tnrate_2)^{|U|-|A|}`, supply the derivation (the formula is currently offered "without proof"), and check whether this belongs in `bernoulli_composition` instead.
- **Cross-verified**: Yes; the logic-checker flagged it as disputed/unproven, the methodology-auditor independently recomputed and upgraded it to incorrect. Recorded as a noted strengthening (not a disagreement).

## Major Issues

### M1. Four new theorems have placeholder or unfinished proofs (source: logic-checker)
- **Locations / quoted text**:
  - Symmetric-relation theorem, `properties.tex`: proof body is the lone expression `\Prob{\Pair{x}{y} \in \ARelation{R} \SetUnion \Pair{y}{x} \in \ARelation{R} \Given \Pair{x}{y} \notin \Relation{R}}` with no derivation or conclusion (ML-1).
  - Map-composition theorem, `properties.tex` line 143: proof ends "...the probability $a \notin \Dom(\APFun{f} \circ \APFun{g})$ is just the probability that  ..." (ML-2).
  - True-subset-rate theorem, `predicates.tex` line 63: proof body is `?` (ML-3).
  - Extended subset-rate derivation, `predicates.tex`: contains `%%% THIS IS NOT FINISHED` (line 213), a duplicated display equation, and dependence on undefined lemmas `\cref{?}`, `\cref{dummyrefs}`, `thm:subset` (ML-4).
- **Problem**: The paper states its new results but proves almost none of them. Several destinations are plausible/correct in form, but the arguments are absent.
- **Suggestion**: Complete each proof. For the symmetric theorem, also justify why TPR is unchanged while FPR becomes `1−(1−\fprate)^2`, and state whether the input relation is assumed symmetric. For map composition, define the `IntervalSpan(... ∪ ... ∪ ...)` notation or replace it with explicit `[min, max]` bounds.
- **Cross-verified**: Quotes verified verbatim by the area chair.

### M2. Two sections re-derive sibling-owned results (source: novelty-assessor, prose-auditor; cross-verified)
- **Location**: `properties.tex` "Random approximate maps" subsection; `predicates.tex` subset/equality derivations
- **Problem**: Map composition (TPR `\tprate_1\tprate_2`, FPR interval) is the central result of `bernoulli_maps`; subset/equality predicate rates belong to `bernoulli_composition` per the family's topic table. Re-hosting them here duplicates the siblings and dilutes this paper's identity.
- **Suggestion**: Cite the siblings at these passages; retain only what is genuinely relational (e.g., composition expressed as join+project). Add the `bernoulliMaps`, `bernoulliComposition` keys (present in the foundation bib) once `references.bib` exists.
- **Cross-verified**: novelty-assessor routed the "deficit vs. framing" question to prose-auditor, who confirmed it is a framing problem (the novel core survives excision of the borrowed parts). No disagreement.

### M3. No differentiation from probabilistic databases (source: novelty-assessor, citation-verifier)
- **Problem**: Probabilistic/uncertain databases (Suciu et al.; Trio; MayBMS) are the nearest external prior art and are never mentioned. A DB/theory referee will ask how an approximate relation differs from a tuple-independent probabilistic database.
- **Suggestion**: Add a paragraph stating the distinction (probabilistic DBs model uncertain *data*; the Bernoulli model has an objective base relation with uncertainty injected by a space-saving *representation*). Cite the literature.

### M4. Abstract over-claims scope and mis-weights content (source: novelty-assessor N-3, prose-auditor PR-1)
- **Location**: `main.tex` abstract (lines 93-95)
- **Problem**: Promises a bits-per-relation entropy bound (owned by `bernoulli_entropy`/`bernoulli-hash-function`), a perfect-hash-map construction (owned by `bernoulli-phf`/`bernoulli-hash-function`), partial-function composition (owned by `bernoulli_maps`), and an oblivious-database / rank-ordered Encrypted Search application (orphaned from the build). The join/project propagation that this paper *should* deliver is the least developed part of the body.
- **Suggestion**: Rewrite the abstract to claim only this paper's territory (relation-as-approximate-set ADT; join/project/select error propagation; invariant preservation; oblivious application), deferring sibling-owned results with citations, and lead with join/project.

### M5. "Properties" section is misnamed and mis-scoped (source: prose-auditor PR-2)
- **Location**: `sections/properties.tex`
- **Problem**: Opens as "Approximate relations with invariants" (relational), then pivots into a long "Random approximate maps" subsection (maps, not relations) and ends on stub subsubsections "Composition...from relational stuff." and "Currying...".
- **Suggestion**: Split. Keep invariants; move/cite the maps material to `bernoulli_maps`.

### M6. Independence assumption not examined under joins/projections (source: methodology-auditor MA-1)
- **Problem**: Assumption `asm:ber_trial` posits i.i.d. membership tests, but join/project produce tuples sharing components, tested through the same underlying cells, so their errors are not independent. The paper's signature question (does element-wise independence survive a join?) is never addressed.
- **Suggestion**: Add an explicit treatment of when relational operators preserve vs. break the independence axiom (the Kronecker-factorization argument the family uses elsewhere). This is also the paper's clearest novelty.

### M7. No validation strategy for the propagation formulas (source: methodology-auditor MA-3)
- **Problem**: The foundation paper validates its claims by Monte Carlo (`bernoulli_sets/code/`); here the new propagation results (several of them unproven or, per C5, wrong) have no empirical check.
- **Suggestion**: Add a per-theorem Monte Carlo harness (sample base relation, apply approximation at known rates, apply operator, compare empirical to formula). This would have caught C5 immediately.

### M8. Large-universe regime tension unresolved (source: methodology-auditor MA-2)
- **Problem**: Subset/equality predicate-preservation probabilities carry `|U|` exponents and go to 0 as `|U| → ∞`, exactly the regime where the model is meant to apply (the manuscript itself notes this), yet the tension is never reconciled.
- **Suggestion**: Discuss the deployment regime explicitly; clarify whether predicate preservation is useful at scale or only for small universes.

### M9. Orphaned section files, including the abstract's headline application (source: format-validator M-F1)
- **Location**: `sections/constrained_ras.tex` (never subfiled); `sections/oblivious_rel_model.tex` (path mismatch vs. `sections/unused/oblivious_rel_model`)
- **Problem**: Substantive content (the power-set false-positive theorem; the entire oblivious-database application) is on disk but absent from the build.
- **Suggestion**: Decide what is in scope; wire in or archive deliberately. Fix the path so the oblivious application either builds or is explicitly deferred.

### M10. Unresolved cross-references with placeholder keys (source: format-validator M-F2)
- **Quoted text**: `\cref{?}`, `\cref{dummyrefs}`, `\cref{sec:bool_search}`, `\cref{sec:powerset}`, `\cref{thm:true_subset_rate}`, `\ref{thm:subset}`, and `\cref{table:mathrel_vsrelmodel}` vs. defined label `tab:mathrel_vsrelmodel`
- **Problem**: None of these targets resolve; several sit inside otherwise-complete derivations. The `table:`/`tab:` mismatch breaks even the one table reference.
- **Suggestion**: Define the missing labels or remove the references; fix the `tab:` spelling.

### M11. Empty `\cite{}` calls (source: citation-verifier CV-2)
- **Location**: `sections/oblivious_rel_model.tex` lines 5, 64
- **Quoted text**: `...consistent with first-order predicate logic\cite{} where data is represented...`
- **Problem**: Literal `\cite{}` with no key (intended referent: Codd 1970). The same file also has a stray literal "[4]" pasted from another source.
- **Suggestion**: Add `codd1970` and fill both keys; delete the stray "[4]".

### M12. Editing scaffolding throughout the source (source: prose-auditor PR-3)
- **Quoted text**: `integrate:::` (relations.tex line 6); `%%% THIS IS NOT FINISHED` (predicates.tex line 213); `TODO:`/`NOTE:` blocks and a verbatim-duplicated paragraph (oblivious_rel_model.tex, "The relational model manages data..." appears at lines 5 and 64); stub subsubsections "Composition...from relational stuff." / "Currying...".
- **Problem**: Normal mid-draft state, but not reviewable.
- **Suggestion**: Clear all scaffolding before submission.

### M13. `\sections{}` typo in orphaned file (source: format-validator C-F3)
- **Location**: `sections/constrained_ras.tex` line 4
- **Quoted text**: `\sections{Random approximate sets with invariants}`
- **Problem**: `\sections` is undefined; would throw "Undefined control sequence" if the file were wired into the build.
- **Suggestion**: Fix to `\section{...}`.

### M14. Empty glossary machinery (source: format-validator M-F3)
- **Problem**: `glossaries` is loaded with `[xindy,...]` and `\printglossary` is called, but no entries are defined (`\loadglsentries`/`\include{defs}` commented out). Adds a `makeglossaries` step and yields an empty glossary.
- **Suggestion**: Populate the glossary or drop the package and `\printglossary`.

## Minor Issues

1. **MNL-1** (logic-checker): `constrained_ras.tex` Cartesian-product theorem states rates as literal `?`/`?` with proof "Prove true positive and false positive rates." Placeholder.
2. **MNL-2** (logic-checker): `constrained_ras.tex` power-set expectation step swaps `E[2^{FP}]` for `2^{E[FP]}` (Jensen gap) without comment; relate to the `c=(1/2)ln^2 2` correction. (Partly belongs to `bernoulli_entropy`.)
3. **MNL-3** (logic-checker/prose): unfinished sentence inside the `integrate:::` block (relations.tex line 9, "...where the projection $\Proj$").
4. **PR-4** (prose-auditor): ADT boilerplate ("A *type* is a set ...") duplicated nearly verbatim in approx_rel_model.tex and properties.tex; consolidate.
5. **PR-6** (prose-auditor, shared with ML-1): `\SetUnion` used for logical OR inside a probability; use `\lor`.
6. **PR-7** typos: "multipicity"→"multiplicity"; "similiar"→"similar"; "umambiguously"→"unambiguously"; double comma "definition,,"; "let the implementation ake care"→"take care"; "no such such participates".
7. **MIN-F1** (format-validator): `\graphicspath{img}` should be `\graphicspath{{img/}}`.
8. **MIN-F2** (format-validator): documented build command omits `-shell-escape` and `makeglossaries`; update CLAUDE.md and state.md to the `bernoulli-phf` pattern.
9. **MIN-F3** (format-validator): no target venue selected; relational-algebra angle suits a database/theory venue.
10. **MIN-F4** (format-validator): stale build artifacts (`main.log`, `main.mtc`, `main.mtc0`) in the tree; confirm gitignored, not staged.
11. **CV-4** (citation-verifier): sibling papers re-derived in prose but never cited; add `bernoulliMaps`/`bernoulliComposition` once bib exists.
12. (logic-checker OK-2): variance line in `thm:fpr` writes `\Var{\FP}` without the `\n` subscript used elsewhere.
13. (logic-checker MNL-4): def:approx_rel conflates the relation-as-set with its indicator operator without a transitional sentence.

## Suggestions

1. Reorder the paper around its actual contribution: relations → approximate relation model → operators with error propagation (join/project/select) → invariants → predicates → oblivious application.
2. Make the join/project error-propagation section the center of gravity; it is the unique, defensible core (novelty-assessor N+2) and is currently the thinnest.
3. Develop the invariant-preservation material (novelty-assessor N+3) into a full section; it is the most original and least finished.
4. Add the probabilistic-database contrast paragraph early (it frames the whole contribution).
5. Add a Monte Carlo validation harness mirroring `bernoulli_sets/code/`; it both validates and catches errors like C5.
6. For the oblivious application, state a threat/leakage model or downgrade it to an explicitly-labeled sketch and cite the trapdoor-computing line.

## Detailed Notes by Domain

### Logic and Proofs
Two inherited theorems (`thm:fpbinom`, `thm:fpr`) are correct restatements of foundation results (cite `aset`). Beyond those, the paper proves almost none of its new claims: four placeholder/unfinished proofs (ML-1..ML-4) and one definition that is vacuously false as typeset (CL-1/C3). The rate-argument-order ambiguity (CL-2/C4) undermines every rate-bearing statement. The arithmetic *destinations* are generally plausible and family-consistent, but the *paths* are unwritten. See `logic-checker.md`.

### Novelty and Contribution
Real, moderate novelty in the *declared extension role*: relation-as-approximate-set ADT (N+1), join/project/select error propagation (N+2, the strongest and least developed), invariant preservation (N+3, most original), oblivious application (N+4). Undercut by re-derivation of sibling-owned results (N-1), an over-claiming abstract (N-3), and zero engagement with probabilistic databases (N-2). The deficits are framing/attribution, not an empty contribution. See `novelty-assessor.md`.

### Methodology
A theory paper with no experiments. The modeling methodology has three gaps: independence is not examined under joins (MA-1, the key unasked question), the large-universe regime tension is unresolved (MA-2), and there is no validation harness (MA-3). The oblivious application lacks a threat model (MA-4). Cross-verification confirmed C3 and C4 and upgraded the equality formula to incorrect (C5). See `methodology-auditor.md`.

### Writing and Presentation
Early-draft prose with visible scaffolding (TODO/NOTE/`integrate:::`/`%%% THIS IS NOT FINISHED`, placeholder `?` refs, duplicated paragraphs and equations, stub subsubsections). The abstract does not match the section order or content (PR-1); "properties" is misnamed and mis-scoped (PR-2). Notation is mostly consistent except the rate-order ambiguity (PR-5 = C4). Salvageable with one structural pass. See `prose-auditor.md`.

### Citations and References
No `references.bib` at all (C2): four named keys dangle (`aset`, `bf`, `phf`, `approxrel`), two `\cite{}` are empty (M11), and the nearest external prior art (probabilistic DBs, Codd) is uncited (M3, CV-3). Mechanical to seed from `bernoulli_sets/references.bib` plus a few additions. See `citation-verifier.md`.

### Formatting and Production
Does not build, for two independent reasons: five missing subfiled files (C1, fatal first) and the missing bibliography (C2, masked behind C1). Plus a `\sections` typo (M13), orphaned files including the headline application (M9), dangling cross-refs (M10), an empty glossary (M14), and an incorrect documented build command (MIN-F2). See `format-validator.md`.

## Literature Context Summary
The paper sits adjacent to probabilistic/uncertain databases (Suciu et al.; Trio; MayBMS), approximate-membership structures (Bloom, cuckoo/xor/ribbon filters), AQP sketches (Count-Min, HyperLogLog), and oblivious/encrypted data structures (SSE, ORAM, CryptDB). Its defensible niche relative to all of these is: an *objective* base relation approximated by a *space-saving representation* with FPR/FNR, error propagated through *relational-algebra operators*, with *invariant-preservation* questions that the probabilistic-DB literature does not ask. Within the family, map composition belongs to `bernoulli_maps` and subset/equality predicates to `bernoulli_composition`; the relations paper must cite rather than re-derive these. Full details in `literature-context.md`.

## Review Metadata
- Agents used: literature-scout (broad + targeted, merged), logic-checker, novelty-assessor, methodology-auditor, prose-auditor, citation-verifier, format-validator. (Specialist analyses conducted by the area chair under each lens; this environment did not expose separate Task-tool subagents or live web access. External literature is from model knowledge and must be verified against primary sources before citation.)
- Cross-verifications performed: 3 (CL-1 → methodology: confirmed critical; CL-2 → methodology: confirmed critical and shown to propagate into the math; ML-5 → methodology: confirmed and upgraded to "incorrect", now C5). Plus the novelty "framing vs. deficit" question → prose-auditor: confirmed framing, no disagreement.
- Disagreements noted: 0 (one strengthening: methodology upgraded ML-5 from "disputed" to "incorrect").
- Hallucination check: all five critical and the load-bearing major quotes re-verified verbatim against the manuscript by the area chair (def:approx_pfun line 233; the `?` proof body line 63; the trailing map-composition proof line 143; the duplicated oblivious paragraph; the `%%% THIS IS NOT FINISHED` and `integrate:::` markers). No discarded findings.
- Recommendation rationale: five critical issues (two build-blockers, two logical errors in definitions, one incorrect formula) plus fourteen major issues spanning all six domains place this firmly at **not-ready**. The contribution is genuine and the path forward is clear, but the volume of unfinished proofs, the non-building manuscript, and the missing bibliography require substantial rework before a re-review.
