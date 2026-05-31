# Prose Auditor Report, bernoulli_relations

**Agent**: prose-auditor (writing quality, narrative arc, notation consistency); also serving as cross-verifier for novelty-assessor's "framing vs. novelty" question
**Date**: 2026-05-29
**Verdict**: The prose is at an early-draft stage with visible editing scaffolding (literal TODO/NOTE/integrate markers, placeholder `?` references, duplicated paragraphs, unfinished sentences). Notation is mostly consistent at the macro level but has one substantive ambiguity. The narrative arc promised by the abstract does not match the section order or the delivered content.

## Narrative and structure

### PR-1 (MAJOR). The abstract describes a paper that the sections do not assemble into
The abstract lays out a clear arc: relation -> approximate relation -> bits-per-relation bound -> join/project propagation -> partial-function composition -> approximate-set implementation -> perfect-hash-map -> oblivious-database application. The actual built sections are: relations (exact algebra), the approximate-relation model, "properties" (which is mostly approximate *maps*, not relational properties), and predicates (subset/equality). The promised entropy bound, perfect-hash-map, and oblivious-database sections are either orphaned or absent from the build (see format-validator). A reader following the abstract will be lost by Section 3. **Fix**: align the abstract with the deliverable content (lead with join/project propagation per novelty N-3) and reorder sections so the relational story is continuous: relations -> approximate relation -> *operators with error propagation* -> invariants -> predicates -> application.

### PR-2 (MAJOR). "Properties" section is misnamed and mis-scoped
`sections/properties.tex` opens as "Approximate relations with invariants" (good, relational), then halfway through pivots into a long "Random approximate maps" subsection (function domains, augmented codomains, map composition, currying) that is about maps, not relations, and duplicates `bernoulli_maps` (novelty N-1). The section thus has two unrelated halves and ends on three stub subsubsections ("Composition...from relational stuff.", "Currying...") that are single-sentence placeholders. **Fix**: split. Keep invariants here; move/cite the maps material to `bernoulli_maps`.

### PR-3 (MAJOR). Pervasive editing scaffolding left in the source
Concrete instances a reader/referee will see (or that block the build):
- relations.tex line 6: literal `integrate:::` ... `:::` block wrapping an unfinished sentence ending "where the projection $\Proj$".
- predicates.tex: `\cref{?}`, `\cref{??}`, `\cref{dummyrefs}`, "Proof of theorem~\ref{thm:subset}", a proof body that is the single character `?`, the comment `%%% THIS IS NOT FINISHED`, and a verbatim-duplicated display equation.
- properties.tex: stub subsubsections "Composition...from relational stuff." and "Currying...".
- oblivious_rel_model.tex: at least seven `TODO:`/`NOTE:` blocks, a stray literal "[4]" citation marker pasted from another source, and two paragraphs duplicated verbatim (the "relational model manages data..." paragraph appears at lines 5 and 64).
- constrained_ras.tex: `\sections{...}` typo (also a build error) and theorem bodies with `?` for the rates.
This is normal mid-draft state, but it must be cleared before the paper is reviewable. **None of these should survive to a submission.**

### PR-4 (MINOR). Repetition of boilerplate definitions
The ADT boilerplate ("A *type* is a set ... An *abstract data type* is a type and a set of operations ... A *data structure* is a particular way of organizing data ...") appears twice nearly verbatim: in approx_rel_model.tex and again in properties.tex (subsubsection "Abstract data type"). Consolidate to one statement and reference it.

## Notation

### PR-5 (MAJOR, shared with logic-checker CL-2). Rate-argument order is inconsistent
`\ARelation{R}[\fnrate][\fprate]` (FNR-first) in approx_rel_model.tex vs. `(\tprate,\fprate)` (TPR-first) in properties.tex and the symmetric theorem. Because the macro encodes no meaning in the slots, the reader cannot disambiguate. This is simultaneously a clarity defect (this report) and a correctness defect (logic-checker), and both stand. **Fix**: adopt the family-standard ordering and apply it everywhere; consider a notation macro that names the rates (for example a comment or a `\ARelation*` variant) so the slots are self-documenting.

### PR-6 (MINOR). `\SetUnion` used for logical OR inside probabilities
In the symmetric-relation proof, the event "(x,y) in R or (y,x) in R" is typeset with `\SetUnion` between two membership propositions. Use `\lor`. (Also flagged by logic-checker ML-1 as obscuring the argument.)

### PR-7 (MINOR). Minor typos and slips
- relations.tex: "multipicity" -> "multiplicity".
- properties.tex: "similiar" -> "similar"; "one-to-one over the domain of definition,," (double comma); "umambiguously" -> "unambiguously".
- approx_rel_model.tex: "an \emph{related} test" and "an \emph{is-not-relation} test" in Assumption 1 read awkwardly; rephrase to "a membership test on a negative tuple" / "on a positive tuple".
- oblivious_rel_model.tex: "let the implementation ake care" -> "take care"; "no such such participates" (constrained_ras.tex) -> "no such element participates".

## Cross-verification of novelty-assessor's routed question

**Question routed**: is the duplication/over-claim (novelty N-1, N-3) a genuine novelty deficit, or a framing problem?

**My finding: it is a framing problem, confirmed.** Reading the sections as prose, the *novel* relational material (relation-as-approximate-set-of-tuples; join/project example; the invariants question) is present and coherent; it is simply (a) interleaved with borrowed maps/predicate material and (b) under-weighted relative to the abstract's promises. When I mentally excise the map-composition subsection and the subset/equality derivations (the sibling-owned parts), what remains is a thin but genuine and non-duplicative paper. So the unclear/overloaded writing is indeed **hiding a real but underdeveloped contribution**, not masking an empty one. This agrees with novelty-assessor's position. The corrective is editorial and structural (re-fence, re-cite, re-weight, finish the join/project section), not "find a new idea." I record **no disagreement** with the novelty-assessor.

One caveat for the area chair: because the genuinely novel parts (invariants, join/project propagation) are also the *least finished* (placeholder proofs, orphaned files), the framing fix and the mathematical-completion work are coupled. You cannot foreground the novel core by editing alone; the proofs in properties.tex/constrained_ras.tex must actually be written.

## Summary for synthesis
- Major: 4 (PR-1 abstract/structure mismatch; PR-2 misnamed/mis-scoped "properties"; PR-3 editing scaffolding throughout; PR-5 rate-order ambiguity, shared with CL-2)
- Minor: 4 (PR-4 repeated boilerplate; PR-6 OR-as-union; PR-7 typos; and the duplicated paragraphs noted in PR-3)
- Cross-verification: confirmed novelty-assessor's "framing not deficit" read; no disagreement.
The writing is salvageable and the bones are sound, but the draft is visibly mid-edit and the abstract oversells. Clear the scaffolding, fix the one real notation ambiguity, realign the abstract, and split the maps material out.
