# Multi-Agent Review Report

**Date**: 2026-06-09
**Paper**: *The abstract data type of the approximate relation* (Alexander Towell, SIUE; ORCID 0000-0001-6443-9897)
**Target venue (assessed against)**: database-theory venue (ICDT / PODS), or a DB journal (Information Systems)
**Recommendation**: **minor-revision** (as a Zenodo preprint / IS-journal submission) / **major-revision** (if ICDT/PODS is the hard target)

> **Process note.** This environment provides no recursive subagents (the Task tool is unavailable inside this context) and no live web search. The "specialists" and "literature scouts" are therefore single-context analyses performed by the orchestrating reviewer, written to the per-role files in this directory. The **math, build, and reproducibility findings are first-hand and trustworthy** (I ran the build and the Monte Carlo harness and independently re-derived every closed form). The **citation/novelty findings that depend on external prior art are tagged `[needs external verification]`** and must be checked by the area chair, who has web access. This matches the standing memory note on this reviewer's limits.

## Summary

**Overall Assessment**: The salvage succeeded. This is a coherent, internally consistent, honestly scoped paper whose every closed-form rate I independently re-derived and cross-checked against the shipped Monte Carlo harness (23 fit rows pass, worst absolute error 0.000686) and against the sibling composition paper. The build is production-clean (21 pp, zero undefined refs/cites, zero warnings). All five 2026-05-29 criticals and all 2026-06-07 minors are fixed. The paper is submittable **today as a Zenodo preprint** and is close to an Information-Systems-journal bar. For a **database-theory venue specifically**, the differentiated contribution (the join independence-failure correlation and the invariant-preservation/closure analysis) is real but modest, and its venue-defining novelty rests on two external prior-art questions the area chair must verify, plus it lacks the complexity/lower-bound/dichotomy result that ICDT/PODS reviewers typically expect.

**Strengths**:
1. **The join independence-failure result (`thm:join_dependence`) is a genuine, sharp, correctly-proved contribution** that the probabilistic-database framing does not subsume, backed by a Monte Carlo confirmation of the exact `1/a` factor. This is the paper's spine and it holds. (logic-checker; methodology-auditor; novelty-assessor)
2. **The invariant-preservation analysis is the cleanest novelty** (reflexive/symmetric/functional/transitive preservation probabilities, with the symmetry-admits-cheap-closure / transitivity-cascades contrast). The reviewer is unaware of prior work on representation-induced invariant survival. (novelty-assessor)
3. **Honest scoping throughout.** Every sibling-owned result (set-level intersection/union, subset/equality predicates, map composition, entropy bound, optimal construction) is deferred by an accurate citation, not re-derived or over-claimed. The join-FPR three-region deferral carries exactly the right caveat. (logic-checker; novelty-assessor)
4. **The validation harness is real and faithful**, includes a *negative control* (the independent model the paper predicts FAILS), and reproduces every formula to 3-4 digits. (methodology-auditor)
5. **Production-clean build and uniform notation**: the prior rate-argument-order critical is fully resolved; `[\fprate][\tprate]` is applied uniformly. (format-validator; prose-auditor)

**Weaknesses**:
1. The **marginal** operator rates (join FNR, projection FPR) appear recoverable as tuple-independent-PDB extensional evaluation, so they do not differentiate from probabilistic databases; the related-work paragraph leaves this opening unaddressed. (novelty-assessor, `[needs external verification]`)
2. The **projection `1-(1-ε)^k` amplification is a standard OR-of-filters identity** presented without conceding it is known; novelty there is by-framing only. (novelty-assessor, `[needs external verification]`)
3. The **load-bearing assumption `asm:ber_trial` is garbled** in wording ("an related test"; opaque operator names), and a referee re-deriving from it will stumble. (prose-auditor; methodology-auditor; logic-checker)
4. **Two structural mis-labels**: Section 2 is mis-titled "Relational algebra" (it is preliminaries), and the approximate-partial-function ADT is mis-nested under "Preservation of relational invariants." (prose-auditor)
5. **Missing external prior-art** (Bloomjoin/semijoin, sketch AQP, searchable encryption) that a DB-theory referee will expect cited and distinguished; one duplicate bibliography entry (`aset` = `bernoulliSets`). (citation-verifier, `[needs external verification]`)
6. For ICDT/PODS, **no complexity/lower-bound/dichotomy result**; the symmetry-vs-transitivity closure contrast is gestured at but not formalized as a theorem. (novelty-assessor; literature context)

**Finding Counts**: Critical: 0 | Major: 5 | Minor: 9 | Suggestions: 4

## Critical Issues
**None.** The build is clean, the math is verified, and the prior criticals are all resolved.

## Major Issues

### MAJOR-1. Marginal operator rates do not differentiate from tuple-independent probabilistic databases (source: novelty-assessor) `[needs external verification]`
- **Location**: intro.tex:62-78 (related work); rel_algebra.tex `thm:join`, `thm:project`.
- **Quoted text** (intro.tex:73-76): "A probabilistic database does not ask whether an approximated symmetric relation stays symmetric, or how a projection's fan-in amplifies a structural false-positive rate, because in that setting the relation has no underlying exact truth to be faithful to and no representation-induced error to propagate."
- **Problem**: A tuple-independent probabilistic database with per-tuple probability `p` is formally close to a Bernoulli relation with `τ=p`. The *marginal* results (join FNR `1-τ_Rτ_S`, projection FPR `1-(1-ε)^k`) look recoverable as extensional query evaluation over independent tuples, which the PDB literature very likely already does. The related-work paragraph distinguishes the *object* correctly but does not pre-empt the marginal-equivalence objection, leaving a referee an opening to call the operator marginals a special case of independent-tuple PDB evaluation.
- **Suggestion**: Concede explicitly that the marginal rates coincide with tuple-independent-PDB extensional evaluation, and pin the contribution on (a) the *joint* law / correlation (`thm:join_dependence`) and (b) invariant preservation, which possible-worlds marginals do not give.
- **Cross-verified**: Routed to prose-auditor (is it framing, not novelty?). Prose-auditor concurs it is a framing gap, fixable in one paragraph; the underlying join-joint-law and invariant results survive the concession. The area chair must `[VERIFY]` whether independent-tuple PDB evaluation already yields the marginal join/project rates.

### MAJOR-2. Projection FPR amplification is a known OR-of-filters identity, presented as new (source: novelty-assessor) `[needs external verification]`
- **Location**: intro.tex:36-44 (contributions); rel_algebra.tex:96-153 (`thm:project`).
- **Quoted text** (intro.tex:37-39): "Projection amplifies the false-positive rate to `1 - (1-ε)^{k}` in the fan-in `k` and raises the model order while preserving element-wise independence."
- **Problem**: `1-(1-ε)^k` is the standard FPR of an OR over `k` independent AMQ trials (equivalently, a union of `k` Bloom filters). The proof is correct, but the formula is not new; only the relational-projection/fan-in framing and the model-order reading are. The contributions list does not concede this.
- **Suggestion**: Add one sentence acknowledging the identity and claim only the relational-operator framing and the model-order observation.
- **Cross-verified**: logic-checker confirms the formula and proof are correct (it is the OR-over-fiber composition); the dispute is purely about novelty attribution, not correctness. Area chair to `[VERIFY]` no prior relational-projection framing exists.

### MAJOR-3. The load-bearing assumption `asm:ber_trial` is garbled (source: prose-auditor; cross-verified by logic-checker and methodology-auditor)
- **Location**: approx_rel_model.tex:60-61.
- **Quoted text**: "The outcome of an *related* test on any tuple in the complementary set is an independent and identically distributed Bernoulli trial with a mean `ε`. The outcome of an *is-not-relation* test on any tuple in the relation is an independent and identically distributed Bernoulli trial with a mean `ω`."
- **Problem**: This is the single most-cited assumption in the paper (every proof invokes it). It has three defects: "an related" is ungrammatical; the operator names "*related* test" / "*is-not-relation* test" are opaque; and the test-name is conflated with the population it is applied to. The *logic* is correct (non-member false-positives at mean `ε`; member missed at mean `ω`), but a referee re-deriving from it will stumble.
- **Suggestion**: Restate plainly in FPR/FNR vocabulary: "For a tuple not in `R`, the test reports it (false positive) as an i.i.d. Bernoulli trial with mean `ε`. For a tuple in `R`, the test fails to report it (false negative) as an i.i.d. Bernoulli trial with mean `ω`."
- **Cross-verified**: logic-checker (LC-SUGGESTION-2) and methodology-auditor both independently flagged the same sentence as load-bearing and confusingly worded. Three-way agreement. Severity is MAJOR not minor *because* every proof depends on it.

### MAJOR-4. Section 2 is mis-titled "Relational algebra" (source: prose-auditor)
- **Location**: relations.tex:4 (`\section{Relational algebra}`); contrast intro.tex:96 ("`\Cref{sec:relations}` reviews relations and the relational operators") and rel_algebra.tex:4 ("Error propagation through relational operators").
- **Problem**: Section 2 is *preliminaries* (sets, tuples, Cartesian products, operator definitions, a classical worked example), not the paper's algebra. Section 4 is the algebra. The title mislabels Section 2 and competes with Section 4; the TOC reads as if the algebra were developed in Section 2.
- **Suggestion**: Retitle Section 2 "Relations and relational operators" (or "Relational preliminaries"), matching the intro's own phrasing. One-line change.
- **Cross-verified**: Confirmed against the TOC (`main.toc`: "2 Relational algebra" above "4 Error propagation through relational operators") and the intro's self-description. Unambiguous.

### MAJOR-5. The approximate-partial-function ADT is mis-nested under "Preservation of relational invariants" (source: prose-auditor; supported by novelty-assessor)
- **Location**: properties.tex:215 (`\subsection{The approximate partial function}` as 5.5 of Section 5); TOC confirms 5.5 / 5.5.1.
- **Problem**: A partial-function ADT is a *model* contribution, not an invariant-preservation result. Single-valuedness (5.3, `thm:functional`) belongs in Section 5; the full ADT exposition (classical recap, `(|Y|+1)^{|X|}` counting, Dom/Image/Range, a table example, `def:approx_pfun`, a claimed contribution) does not. It buries intro contribution 3 at depth 5.5 and is structurally jarring.
- **Suggestion**: Promote the approximate partial function to its own top-level section (between invariants and the application) or fold `def:approx_pfun` into the model section (Section 3), keeping only the single-valuedness *preservation* result in Section 5. Trim the classical scaffolding (also addresses novelty-assessor NA-MINOR-2).
- **Cross-verified**: novelty-assessor independently flagged the same exposition as heavy/classical/sibling-overlapping (NA-MINOR-2). Structure and novelty findings agree.

## Minor Issues

### MINOR-1. Duplicate bibliography entry: `aset` and `bernoulliSets` are the same paper (source: citation-verifier)
- **Location**: references.bib:14-19 (`aset`) and references.bib:39-45 (`bernoulliSets`); identical title "Bernoulli Sets: A Model for Random Approximate Sets". Both are cited, producing two reference-list entries for one work.
- **Suggestion**: Merge to one key (keep `bernoulliSets`), redirect all `\cite{aset}`, delete the redundant entry.

### MINOR-2. `def:approx_rel` condition (i) uses opaque complement notation `\AT{R^∁}[\fnrate][\fprate]` while (ii) uses clean `\ARelation` (source: prose-auditor; format-validator)
- **Location**: approx_rel_model.tex:42. Resolves at build (transitive macro) but reads in a different notation than the adjacent condition (ii).
- **Suggestion**: Restate (i) as `P(X ∉ R̃ | X ∈ R) = ω`, symmetric with (ii). Also hardens the transitive `\AT` dependency (FV-MINOR-1).

### MINOR-3. Fragile transitive macro dependency (source: format-validator)
- **Location**: `\AT`/`\SetComplement` in approx_rel_model.tex arrive only via `approxsetnotation → approx_data_type_notation`; main.tex does not load that package directly. Clean today; would silently break if the `\usepackage` list is trimmed. Resolve by MINOR-2 (drop `\AT`) or load the package explicitly.

### MINOR-4. validate.py does not cover `thm:symmetric_preservation` (source: methodology-auditor)
- The harness validates 8 closed forms but omits the `(τ²+ω²)^P((1-ε)²+ε²)^N` symmetry-*preservation* rate (only the *closure* rows are in `tbl:validation`). I confirmed it by independent re-derivation + a one-off MC (0.8199 vs 0.8200), but the shipped script leaves it uncovered. Add a `validate_symmetric_preservation` case so every theorem has a harness row.

### MINOR-5. No asymmetric-operand join case in the harness (source: methodology-auditor)
- All validation runs symmetric operands (`ε_R=ε_S`, `ω_R=ω_S`). The manuscript states the asymmetric three-region FPR; add an `ε_R≠ε_S` join row so the asymmetric claim is reproducible from shipped code. (I verified asymmetric FNR `ω_R=.1, ω_S=.2 → 0.28` independently.)

### MINOR-6. Monte Carlo standard error not reported (source: methodology-auditor)
- `tbl:validation` gives point estimates and absolute error but no SE/CI. At 2e6 trials the SE (~0.0002 near rate 0.1) is below the observed errors, so the agreement is sound; stating the SE quantifies the "3-4 decimal places" claim.

### MINOR-7. Missing external prior-art anchors for a DB-theory venue (source: citation-verifier) `[needs external verification]`
- Bloomjoin/semijoin-filtering, sketch-based AQP (AGMS/Count-Min), and searchable-encryption (Goh Z-IDX / Bloom SSE) are uncited. Cite and distinguish each before a DB-venue submission. Each `[VERIFY]` by the area chair.

### MINOR-8. `thm:join_dependence` proof asserts `B_i` independence without re-deriving (source: logic-checker)
- rel_algebra.tex:336: add a half-clause citing the cross-approximation independence (rel_algebra.tex:24) and `asm:ber_trial` so the proof is self-contained. Cosmetic; result is correct.

### MINOR-9. No target-venue document class (source: format-validator)
- The manuscript uses generic `article`. A DB-venue submission needs `acmart` (PODS/SIGMOD-adjacent) or LIPIcs (ICDT). Expected pre-submission step, not a current defect; flagged for completeness.

## Suggestions
1. **State the covariance** `Cov = a(1-a)P(B₁)P(B₂)` alongside the `1/a` ratio in `thm:join_dependence`. It is a clean positive closed form (I verified it) and quantifies "positively correlated." (logic-checker)
2. **Lead the contributions list with the invariant fragility + closure dichotomy**, which is the strongest and most differentiated novelty, currently under-weighted relative to the operator section. (novelty-assessor)
3. **Formalize the symmetry-vs-transitivity closure contrast as a dichotomy theorem** (which invariants admit a constant-cost deterministic closure and which cascade). This is the kind of result that would lift the paper toward an actual ICDT/PODS contribution. (novelty-assessor; literature context)
4. **If minted carries no rendered listing in the final body**, drop it (and `-shell-escape`) as the sibling `bernoulli_maps` did, to simplify the build and satisfy venue submission systems that disallow shell-escape. (format-validator)

## Detailed Notes by Domain

### Logic and Proofs
Zero critical, zero major logic findings. I independently re-derived all 11 load-bearing closed forms by exact algebra (including the covariance form and the asymmetric join FNR), and re-confirmed `thm:symmetric_preservation` (the row the harness skips). Every proof is correct and adequately rigorous: selection, projection (incl. the subtle j≥2 TPR), projection model-order, join FNR/FPR three-region, the join independence failure (`1/a`), and all four invariants. The transitivity section is honestly hedged with the now-explicit independence caveat. Only one minor self-containment gap (MINOR-8) and two optional strengthenings.

### Novelty and Contribution
Split verdict. The differentiated core is (1) `thm:join_dependence` (the join joint-law correlation) and (2) the invariant-preservation/closure analysis; both survive the prob-DB contrast. The projection formula is a known identity (MAJOR-2) and the marginal operator rates may be PDB-recoverable (MAJOR-1); both need framing concessions and external verification. The partial-function ADT and the encrypted-search application are novelty-by-framing, honestly scoped. The invariant results are under-sold relative to their novelty.

### Methodology
Strong reproducibility. The harness is faithful (correct per-tuple law), reproducible (fixed seed), and includes a proper negative control for the independence-failure claim. Gaps are completeness-only: one theorem uncovered (MINOR-4), symmetric/asymmetric variants under-exercised (MINOR-5), and no reported MC standard error (MINOR-6). None undermines a result.

### Writing and Presentation
Publication-quality after the salvage; all prior prose warts fixed. The abstract and intro front-load the join result and the prob-DB distinction effectively (answering the area chair's GOAL 5: yes). Residue is one garbled load-bearing assumption (MAJOR-3) and two structural mis-labels (MAJOR-4, MAJOR-5), each a localized fix. Notation is now uniform (`[\fprate][\tprate]`), resolving the prior rate-order critical.

### Citations and References
Mechanically clean (full cite/bib closure, 0 bibtex warnings). One duplicate entry (MINOR-1, `aset`=`bernoulliSets`). All present citations are appropriately used; the prob-DB and relational-model citations are correct in role. Missing external prior-art anchors (MINOR-7) matter for the DB-theory venue. External bibliographic facts flagged `[needs external verification]`.

### Formatting and Production
Production-clean: 21 pp, 0 undefined refs/cites, 0 warnings, 0 overfull boxes, 0 bibtex warnings, 0 duplicate-destination warnings. The prior 3.31pt overfull box is gone. Findings are a fragile transitive macro dependency (MINOR-3) and the absence of a target-venue class (MINOR-9).

## Literature Context Summary
The framing "approximate relation = AMQ over the tuple universe, propagate the FPR through operators" is **plausibly incremental** relative to the Bloomjoin / runtime-filter / AQP literature **until the join-independence-failure result lands**. The projection amplification is a standard OR-of-filters identity. The two results that genuinely differentiate the paper are `thm:join_dependence` (the join joint-law correlation) and the invariant-preservation analysis; the latter is the cleanest novelty (the reviewer is unaware of prior representation-induced-invariant-survival work). The prob-DB distinction is real *in object* but has a soft seam at tuple-independent PDBs (the marginal rates). For ICDT/PODS the paper lacks the venue's usual complexity/lower-bound/dichotomy currency and is better positioned at an Information Systems journal or as a Zenodo preprint unless a sharper theoretical hook (a closure-dichotomy theorem, or the deferred entropy lower bound) is added. **The full literature packet's `[VERIFY]` list is the area chair's action list; the venue decision turns chiefly on the Bloomjoin-dependence and independent-tuple-PDB checks.**

## Database-theory-venue readiness verdict
- **As a Zenodo preprint (the family's stated default)**: **READY** after the minor fixes. The math is verified, the build is clean, the scoping is honest.
- **As an Information Systems / DB-systems journal submission**: **MINOR-REVISION.** Fix MAJOR-1 through MAJOR-5 (two framing concessions, the assumption wording, two structural relabels) and add the missing prior-art citations; the differentiated core (join correlation + invariant fragility) is a legitimate, validated, useful contribution for such a venue.
- **As an ICDT / PODS submission**: **MAJOR-REVISION, and a stretch even then.** These theory venues expect a complexity/lower-bound/dichotomy result; the paper currently offers closed-form rate-propagation and preservation probabilities, which is atypical for the program. To be competitive it would need (i) the framing concessions of MAJOR-1/2 so the novelty is unmistakably the joint law + invariants, and (ii) a genuine theorem in the venue's currency, the most natural being a **dichotomy on which invariants admit a constant-cost closure** (symmetry yes, transitivity no) or the **information-theoretic lower bound** on bits-per-relation to preserve an invariant at a target rate (currently deferred to `bernoulliEntropy`). Without (ii), recommend redirecting to an IS journal or the preprint track.

## Review Metadata
- Agents used (run as single-context analyses by the orchestrator; no recursive subagents available): literature-scout-broad, literature-scout-targeted (merged into the literature packet), logic-checker, novelty-assessor, methodology-auditor, prose-auditor, citation-verifier, format-validator.
- First-hand verifications performed by the orchestrator: full LaTeX build (clean, 21 pp); `code/validate.py` run (23/23 fit rows pass, worst err 6.86e-4); independent re-derivation of all 11 closed forms incl. covariance, asymmetric join FNR, and the harness-skipped `thm:symmetric_preservation`; full label/ref/cite closure check; bib duplicate detection.
- Cross-verifications performed: 4 (MAJOR-1 novelty→prose framing; MAJOR-3 prose→logic+methodology three-way; MAJOR-5 prose→novelty; join-dependence logic→methodology structural reproduction).
- Disagreements noted: 0 (specialists concur; correctness vs. novelty-attribution distinctions on the projection formula are complementary, not contradictory).
- Findings tagged `[needs external verification]`: MAJOR-1, MAJOR-2, MINOR-7 (and the consolidated literature-packet `[VERIFY]` list).
