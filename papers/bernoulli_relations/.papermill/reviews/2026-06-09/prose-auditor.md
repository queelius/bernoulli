# Prose Auditor Report

**Paper**: *The abstract data type of the approximate relation*
**Date**: 2026-06-09
**Scope**: Writing quality, narrative arc, notation consistency, section structure. The salvage cycle resolved the gross prose defects of the 2026-05-29 review and the minor terminology warts of the 2026-06-07-postsalvage review (verified below). Findings here are the residue plus three structural items a DB-theory referee will notice.

## Status of prior-review prose findings (all verified FIXED)
- "correlation / complementary correlation" coinage and "false relation rate" synonym (prior MINOR-1): **gone.** approx_rel_model.tex:13 now uses "correspondence" consistently; no "false relation rate."
- `\ExactMap` and `\ARelationType` dead macros (prior MINOR-2): **gone** (grep-confirmed, neither defined nor used).
- Empty numbered equation in sec:map (prior SUGGESTION-2): **gone.**
- "immutable approximate set" copy-paste heading (prior SUGGESTION-1): **fixed**; properties.tex:281 now reads "The abstract data type of the *approximate partial function*."
- Transitivity heuristic-independence caveat (prior MINOR-4): **added**; properties.tex:191 now flags "as a first-order heuristic, ignoring the cross-triple coupling."
- "oblivious" in prose (terminology sweep): **clean**; the word survives only in the filename and a build comment, never in body text.

The prose is in genuinely good shape. The narrative arc (gap, contributions, preliminaries, model, operator propagation, invariants, application) is coherent and the abstract front-loads the join result and the prob-DB distinction effectively, which directly answers the area chair's GOAL 5: **yes, the abstract and intro front-load the join result and the prob-DB contrast well.** The abstract names the join independence failure as the pivot ("A join, by contrast, does *not* preserve element-wise independence") and the intro calls it "the paper's sharpest finding."

## Residual findings

### PA-MAJOR-1 (notation/assumption clarity, load-bearing): `asm:ber_trial` wording is garbled
- **Location**: approx_rel_model.tex:60-61.
- **Quoted text**: "The outcome of an *related* test on any tuple in the complementary set is an independent and identically distributed Bernoulli trial with a mean `ε`. The outcome of an *is-not-relation* test on any tuple in the relation is an independent and identically distributed Bernoulli trial with a mean `ω`."
- **Problem**: Three defects in the single most load-bearing sentence of the paper. (1) "an related" is ungrammatical (should be "a relatedness"). (2) The operator names "*related* test" and "*is-not-relation* test" are opaque and assigned in a way that reads backwards: the "related test" (does this tuple test as related?) is described as applying "on any tuple in the complementary set," which conflates the test with the population it is applied to. (3) The two sentences pair a test-name with a population-and-rate in a way that obscures the clean statement. The *logic* is correct (a non-member false-positives at mean `ε`; a member is missed at mean `ω`), but every proof in the paper cites this assumption, and a referee re-deriving from it will stumble.
- **Suggestion**: Restate plainly, matching the body's FPR/FNR vocabulary: "For a tuple not in `R`, the membership test reports it (a false positive) as an i.i.d. Bernoulli trial with mean `ε`. For a tuple in `R`, the test fails to report it (a false negative) as an i.i.d. Bernoulli trial with mean `ω`." Drop the "related test"/"is-not-relation test" coinage.

### PA-MAJOR-2 (structure): Section 2 is mis-titled "Relational algebra"
- **Location**: relations.tex:4 (`\section{Relational algebra}`), versus the intro's own description (intro.tex:96: "`\Cref{sec:relations}` reviews relations and the relational operators") and the actual algebra section (rel_algebra.tex:4, "Error propagation through relational operators").
- **Problem**: Section 2 is *preliminaries*: it defines sets, tuples, Cartesian products, relations, and the operator *definitions* (join/project/compose) plus a worked classical example. It is **not** the paper's relational algebra; Section 4 is. Titling the preliminaries "Relational algebra" mislabels it and competes with Section 4 for the algebra identity. The TOC shows "2 Relational algebra" sitting above "4 Error propagation through relational operators," which reads as if the algebra were developed in Section 2 and merely re-applied in Section 4.
- **Suggestion**: Retitle Section 2 to "Relations and relational operators" (or "Relational preliminaries"), matching the intro's own phrasing. One-line change; removes a real source of referee confusion.

### PA-MAJOR-3 (structure): the partial-function ADT is mis-nested under "Preservation of relational invariants"
- **Location**: properties.tex:215 (`\subsection{The approximate partial function}` as subsection 5.5 of Section 5 "Preservation of relational invariants"); TOC confirms 5.5 and 5.5.1.
- **Problem**: A partial function is not an invariant-preservation result. *Single-valuedness* (5.3, `thm:functional`) correctly belongs in the invariants section. But subsection 5.5 is a full ADT exposition (classical partial-function recap, counting formula, Dom/Image/Range, a table example, `def:approx_pfun`), which is a *model* contribution, not an invariant. Nesting it as the last subsection of the invariants section is structurally jarring and buries `def:approx_pfun` (a claimed contribution, intro item 3) at depth 5.5.
- **Suggestion**: Promote the approximate partial function to its own top-level section (between invariants and the application), or fold its `def:approx_pfun` into the model section (Section 3) as the single-valued specialization, keeping only the single-valuedness *preservation* result in Section 5. This also addresses the novelty-assessor's NA-MINOR-2 (the exposition is heavy/classical and should be trimmed).

### PA-MINOR-1 (notation asymmetry): `def:approx_rel` condition (i) uses opaque complement notation
- **Location**: approx_rel_model.tex:42 (condition (i)).
- **Quoted text**: `\Prob{\AT{\SetComplement[\Relation{R}]}[\fnrate][\fprate](\RV{X_1}, \cdots) \Given \Relation{R}(\RV{X_1}, \cdots)} = \fnrate`
- **Problem**: Condition (i) is expressed via the complement-approximation macro `\AT{R^∁}[\fnrate][\fprate]` (with swapped rate slots), while condition (ii) directly below uses the clean `\ARelation{R}[\fprate][\tprate]`. The two conditions thus read in two different notations for the same definition; condition (i) forces the reader to parse a complement-of-relation with reversed rates to recover the plain statement "a member is missed with probability `ω`." The macro resolves at build (it is pulled in transitively via `approxsetnotation → approx_data_type_notation`), so this is not a build error, only a clarity asymmetry.
- **Suggestion**: Restate condition (i) in the same `\ARelation` notation as (ii): `P(X ∉ R̃ | X ∈ R) = ω`. Symmetric with (ii), no complement gymnastics.

### PA-MINOR-2 (micro): "an" before consonant and a stray article
- **Location**: approx_rel_model.tex:60 ("an *related* test"), already covered by PA-MAJOR-1; also check approx_rel_model.tex:6 ("A random approximate relation `R̃` is a *random approximate set*\cite{aset} of a relation") reads slightly oddly ("a random approximate set *of* a relation"); minor.

## Notation consistency (positive)
The `\ARelation{R}[\fprate][\tprate]` convention (subscript FPR, superscript TPR) is now applied **uniformly** across properties.tex, rel_algebra.tex, oblivious_rel_model.tex, and approx_rel_model.tex (grep-confirmed: every `\ARelation{R}[...]` uses `[\fprate][\tprate]`). The prior review's "rate-argument order inconsistent" critical (C4, 2026-05-29) is fully resolved. The only residual is the `\AT` complement form in def:approx_rel condition (i) (PA-MINOR-1).

## Verdict
Prose is publication-quality after the salvage. Zero critical, zero gross-clarity issues. The three MAJOR findings are all *structural/clarity* (a garbled load-bearing assumption sentence, a mis-titled preliminaries section, a mis-nested ADT subsection); each is a localized, low-effort fix that a DB-theory referee would otherwise flag. The abstract/intro front-loading of the join result and prob-DB distinction is effective as-is.
