# Multi-Agent Review Report

**Date**: 2026-05-29
**Paper**: The Perfect Hash Filter: An efficient implementation of the positive Bernoulli set and Bernoulli map abstract data types (Alexander Towell, SIUE)
**Recommendation**: not-ready

## Summary

**Overall Assessment**: This is an early-stage (~25%) implementation/application paper in the Bernoulli-set family, and it reads like one: a clear conceptual skeleton with a genuinely well-written ADT section, wrapped around a core derivation that is unfinished and currently does not compile. Calibrated to its draft stage, the paper is on a sound trajectory but is blocked by a small number of concrete, fixable problems: the PDF does not build (a referenced figure file does not exist), the central data structure is presented as novel when it is the well-known "minimal-perfect-hash + fingerprint" approximate-membership structure (with no related work and no comparison to xor/cuckoo/Bloomier filters), the headline space-optimality claim is overstated and rests on an unpublished companion manuscript, and there are zero experiments despite a substantial benchmarkable C++ library sitting unused in the same repository. None of these is fatal to the underlying idea; together they place the paper well short of submittable.

**Strengths**:
1. The ADT section (`adt.tex`) is mature, careful writing: the type/abstract-data-type exposition, the reconciliation of a deterministic implementation with the probabilistic model, and the observation that positive/negative approximate sets are semirings (not Boolean algebras, since they are not closed under complement) are correct and well-presented. (prose-auditor, logic-checker)
2. The core FPR result (Theorem `thm:fp_rate`: FPR `= 2^-M` for an `M`-bit fingerprint, zero false negatives) is correct in its mathematics, and the typed-PHF and fuzzy-set/hedge expositions are clean and pedagogically effective. (logic-checker, prose-auditor)
3. The bibliography already contains the right 16 real references for the subfield (Bloom, CFGMW, FKS, Mehlhorn, CHD, cuckoo, xor, ribbon, Bloomier, Pagh-Pagh-Rao, etc.), most with DOIs, so the related-work gap is a deployment problem, not a research problem. (citation-verifier, literature)
4. A real, substantial C++20 library (`maph`, ~12.8k LOC, with tests and benchmark harnesses) exists in the repository, so the missing experiments are largely a matter of connecting existing code to the paper's predictions. (methodology-auditor)

**Weaknesses**:
1. The manuscript does not compile: a fatal error (`img/phfilter.tex` not found; the `img/` directory is absent) aborts the build before any PDF is produced. (format-validator)
2. The central construction is established prior art (the MPHF+fingerprint AMQ behind xor/fuse/cuckoo/Bloomier filters), but is presented as a new derivation with no related-work section and no differentiation. (novelty-assessor, literature)
3. The "asymptotically achieves the `-log2 eps` lower bound" claim is overstated (correct only as `eps -> 0`; beaten by xor/fuse filters at practical FPR) and is internally contradicted by two different Bloom crossover thresholds (`2^-3` vs `2^-4`). (novelty-assessor, logic-checker, literature)
4. Load-bearing results depend on an unpublished companion manuscript (`oph`, "Theorem 3"), and the headline space theorem cannot currently be checked. (logic-checker, citation-verifier)
5. A multi-step proof carries a sign error (union induced FPR written `eps_1+eps_2+eps_1 eps_2` in the proof body vs the correct `eps_1+eps_2-eps_1 eps_2` in the theorem statement), a theorem is duplicated verbatim, and both estimator statements have a spurious leading minus sign. (logic-checker)
6. Zero experiments, while the abstract promises "a C++ implementation and compare it to the theoretical analysis," and the paper's C++ section points at a stale, non-existent codebase rather than the real `maph` library. (methodology-auditor)

**Finding Counts**: Critical: 4 | Major: 17 | Minor: 19 | Suggestions: 6

(Per-domain critical/major tallies: logic 1C/4M, novelty 1C/2M, methodology 1C/3M, format 1C/2M, prose 0C/3M, citations 0C/3M. The four distinct Critical issues are F1, C1-novelty, C1-methodology, and C1-logic; the prose and citation domains raised no criticals.)

---

## Critical Issues

### CR1. The manuscript does not compile (missing figure file) (source: format-validator)
- **Location**: `sections/rd_ph_filter.tex` line 169 (`\input{img/phfilter.tex}`), reached via `main.tex` line 156.
- **Quoted text**: build output: "`! LaTeX Error: File 'img/phfilter.tex' not found.` ... `! Emergency stop.` ... `!  ==> Fatal error occurred, no output PDF file produced!`"
- **Problem**: The committed `main.tex` now includes the core section `rd_ph_filter.tex` (so the long-standing "core section excluded" item is partly resolved), but that section `\input`s a TikZ figure file that does not exist; the entire `img/` directory is absent (and so is `data/`). No PDF is produced. The `state.md` "compiles to 10 pages" note is stale. This is the top blocker: nothing can be evaluated on a rendered PDF until it is fixed.
- **Suggestion**: Author `paper/img/phfilter.tex` (the 3-element PHF figure described in its caption). As an immediate stopgap, stub or comment the `\input` to restore the build, then create the real figure. Also create `paper/data/` (or convert the `adt.tex` CSV plots to closed form).
- **Cross-verified**: Build was actually run (not inferred); fatal error and absent directories confirmed by direct `ls` and `pdflatex` invocation.

### CR2. Core data structure presented as novel but is established prior art, with no related work (source: novelty-assessor; corroborated by literature)
- **Location**: Abstract (`main.tex` lines 147 to 149); Introduction (`sections/intro.tex`); construction + FPR theorem (`rd_ph_filter.tex` lines 52 to 206). No related-work section exists in `main.tex`.
- **Quoted text**: Abstract: "We derive the \gls*{gls-phf}, an immutable data structure that implements the static \emph{positive Bernoulli set}---a set with a quantifiable false positive rate and zero false negatives ... asymptotically achieves the information-theoretic lower bound of `-\log_2 \varepsilon` bits per element."
- **Problem**: "Perfect hash to a slot, store a `b`-bit fingerprint, test by fingerprint equality" is the textbook static-AMQ construction underlying xor filters (Graf and Lemire 2020, ~1.23x the lower bound), fuse filters (~1.075x), cuckoo filters (Fan et al. 2014), and, for the key-value case, the Bloomier filter (Chazelle et al. 2004). All are in the paper's own `.bib` (`graf2020`, `fan2014`, `bloomier`, `pagh2005`, `dietzfelbinger2008`) yet none is cited in prose, and there is no related-work section. The FPR theorem is, to an AMQ reader, a re-derivation of folklore.
- **Suggestion**: Add a related-work section naming xor/fuse/cuckoo/Bloomier and Pagh-Pagh-Rao; reframe the contribution from "we derive a new structure" to "we show the MPHF+fingerprint structure is a faithful realization of the positive Bernoulli set ADT, analyze its two error rates in the Bernoulli model, and extend it to maps and fuzzy retrieval." State the realistic novelty (the Bernoulli-ADT framing, the k-perfect FNR analysis, the fuzzy-IR application) explicitly.
- **Cross-verified**: Yes, by prose-auditor: the fix is structural content (a related-work section, a qualified claim), not rewording, so the novelty and prose lenses agree this is a real gap rather than a framing artifact.

### CR3. Abstract promises an empirical comparison that does not exist; zero experiments (source: methodology-auditor)
- **Location**: Abstract (`main.tex` line 148); the C++ section (`cpp_imp.tex`).
- **Quoted text**: "Finally, we provide a C++ implementation and compare it to the theoretical analysis."
- **Problem**: There is no experiments section. No measured FPR vs predicted `2^-M`, no measured bits/key vs the predicted formula, no throughput/construction-time numbers, no comparison plot. The figures in `rd_ph_filter.tex` are closed-form curve evaluations presented as results. The C++ section's listing paths point to a non-existent `random_approximate_sets_adt/` tree, while the repository's actual ~12.8k-LOC `maph` library is never mentioned.
- **Suggestion**: Add an experiments section driven by the existing `maph` benchmarks (measured FPR vs `2^-b`, measured bits/key vs prediction, throughput vs a real Bloom filter), or remove the empirical-comparison promise from the abstract until one exists. Decide which codebase the paper documents and rewrite `cpp_imp.tex` around it.
- **Cross-verified**: Yes, by logic-checker: the analytic claims the experiments would validate are themselves currently defective (CR4, sign errors), so experiments must be co-developed with the proof fixes.

### CR4. Sign error propagates through the union space-complexity proof (source: logic-checker)
- **Location**: `sections/adt.tex`, Theorem `thm:union_space_complexity` (lines 367 to 467).
- **Quoted text**: theorem statement uses "`\fprateob_1 + \fprateob_2 - \fprateob_1 \fprateob_2`" (lines 363, 373, 380); the proof body switches to "`\fprateob_1 + \fprateob_2 + \fprateob_1 \fprateob_2`" (lines 413, 421, 431), then reverts to `-` in the "(... revisited)" line 440.
- **Problem**: The induced FPR of the union of two independent positive Bernoulli sets is `eps_1 + eps_2 - eps_1 eps_2` (inclusion-exclusion / the family's own composition theorem). The `+` form in the proof is wrong, so the derivation does not actually reach the stated efficiency expression. The corollary (lines 462 to 467) compounds the error by dividing by `log2(eps_1 eps_2)`, dropping the `alpha` weights the theorem carries. A "???" is also left mid-proof at line 428.
- **Suggestion**: Use `eps_1 + eps_2 - eps_1 eps_2` throughout; re-derive `eq:proof_union_ae`; reconcile the corollary's `alpha` specialization; complete the "???" step.
- **Cross-verified**: Yes, by methodology-auditor: the sign is inconsistent with the paper's own composition framework (intro's `eta_total = 1 - prod(1-eta_i)`), not merely with convention, so it is a genuine internal contradiction.

---

## Major Issues

### MJ1. Optimality claim not differentiated from structures that beat it at practical FPR (logic-checker, novelty-assessor, literature)
- **Location**: Abstract; `intro.tex` lines 16 to 21.
- **Quoted text**: "achieves an expected space complexity approaching the information-theoretic lower bound of `-\log_2 \varepsilon` ... For false positive rates `\varepsilon < 2^{-3}`, the \gls{gls-phf} is the more space-efficient structure."
- **Problem**: The comparison is only against the 1970 Bloom filter; xor/fuse filters reach the same `-> 1` asymptote with less overhead than a full MPHF, so the flat "more space-efficient structure" claim does not hold against the state of the art. The optimality is correct only in the `eps -> 0` limit (the body's own `rd_ph_filter.tex` says as much), which the abstract omits.
- **Suggestion**: Qualify to the `eps -> 0` regime; compare against xor/cuckoo/fuse, not just Bloom; restrict "more efficient" to where it actually holds.

### MJ2. Load-bearing space theorem rests on unpublished `oph` (logic-checker, citation-verifier)
- **Location**: `rd_ph_filter.tex` Theorem `thm:mPHF_size` proof, line 230.
- **Quoted text**: "according to Theorem~3 in \cite{oph}, the \emph{expected} lower-bound for a perfect hash function with a load factor `r` is given by `\log_2 \mathrm{e} - (\frac{1}{r}-1)\log_2(\frac{1}{1-r})`".
- **Problem**: `oph` is `@unpublished{... Manuscript in preparation}`. The headline space result and everything derived from it (corollary, entropy, estimators) is therefore unverifiable as written.
- **Suggestion**: Prove the perfect-hash load-factor bound inline (a standard occupancy/entropy computation) or mark the result explicitly conditional on forthcoming work and weaken the abstract.

### MJ3. Verbatim-duplicated theorem with identical proof (logic-checker, prose-auditor)
- **Location**: `rd_ph_filter.tex` lines 426 to 447 and 451 to 472.
- **Quoted text**: line 427 "An estimator of the cardinality ..."; line 452 "A \emph{maximum likelihood estimator} of the cardinality ..." (identical statement and proof).
- **Problem**: The same estimator result is stated and proved twice; the second merely relabels it "MLE" (the proof is actually a method-of-moments plug-in, not an MLE argument).
- **Suggestion**: Delete one; justify or correct the "maximum likelihood" label.

### MJ4. Sign error in both cardinality-estimator statements (logic-checker)
- **Location**: `rd_ph_filter.tex` lines 429 and 454 vs proofs at 445 and 469.
- **Quoted text**: statements give "`\hat{m} = -\frac{\BL(\PASet{S})}{-\log_2 \fprate + 1.44}`"; proofs conclude without the leading minus.
- **Problem**: A leading minus makes the estimated cardinality negative; the proofs' unsigned form is correct.
- **Suggestion**: Remove the leading minus from both statements.

### MJ5. Distributional claim cites nothing (empty `\cite{}`) (logic-checker, citation-verifier)
- **Location**: `rd_ph_filter.tex` line 387; empty `\ref{}` tags lines 437, 462.
- **Quoted text**: "According to \cite{}, the probability mass of the perfect hash function is given by `\RV{N} \sim ... = q^{2^n-1}(1 - q^{2^n})`".
- **Problem**: A specific pmf is asserted on an empty citation; two equation cross-tags reference an empty `\ref{}`. These render as `[?]`/`(??)`.
- **Suggestion**: Supply the source (likely `oph`) or derive it; fill the `\ref{}` tags.

### MJ6. The C++ section is disconnected from the repository's actual implementation (methodology-auditor)
- **Location**: `cpp_imp.tex` (whole).
- **Quoted text**: listing paths to `code/random_approximate_sets_adt/include/approximate_set/dynamic/aset.hpp` (lines 21, 33, 265); live block has `template PerfectHashFn` (line 99) and mismatched braces (lines 110, 118).
- **Problem**: The referenced codebase does not exist; the real `maph` library (~12.8k LOC) is undocumented by the paper; the one live listing does not compile.
- **Suggestion**: Choose the documented artifact, rewrite around its real API, delete stale pseudo-listings.

### MJ7. Analytic "results" lack provenance and reference missing data files (methodology-auditor, format-validator)
- **Location**: `rd_ph_filter.tex` `fig:abs_eff` (lines 273 to 296); `adt.tex` figure lines 540 to 546 (`data/data1.csv` and three more CSVs; `data/` is absent).
- **Problem**: The 6-digit optimal-load-factor table has no stated computation; the union-efficiency figure reads CSVs that do not exist (currently shielded in a `\COMMENT{}` block but intended content).
- **Suggestion**: State/ship the computation; add the CSVs or use closed-form plots (a sibling figure already does).

### MJ8. Key assumptions asserted, never validated; reconciliation hand-waved at the crucial number (methodology-auditor)
- **Location**: `rd_ph_filter.tex` lines 172 to 179; `adt.tex` lines 154 to 229.
- **Quoted text**: `adt.tex` line 206 "at `\Card{U} = 2`, the probability of this outcome is `$?$`."
- **Problem**: The independence axiom is assumed (not argued) to follow from "cryptographic hash function" and never checked empirically; the deterministic-vs-probabilistic reconciliation lands on a blank exactly where a number is needed.
- **Suggestion**: Add a small empirical independence check; fill in the `\Card{U}=2` probability.

### MJ9. Genuinely novel-to-this-paper elements are under-developed (novelty-assessor)
- **Location**: `k_perfect_hashing.tex`; `pmf.tex` (TODO subsections lines 79 to 83); `apps_postings_list.tex`.
- **Quoted text**: `pmf.tex` "% TODO: Derive the information-theoretic lower bound ... % TODO: Derive the upper bound on the entropy of the PMF encoding."
- **Problem**: The parts that would carry the real contribution (k-perfect FNR analysis, the map's space/entropy bounds, the fuzzy-IR application with numbers) are the least finished.
- **Suggestion**: Prioritize these; cite Bloomier for the map; give the fuzzy-IR app one end-to-end numeric example.

### MJ10. The introduction does not function as an introduction (prose-auditor)
- **Location**: `intro.tex` (whole).
- **Problem**: No motivation, no contributions list, no related-work pointer; the "organized as follows" roadmap forward-references sections, several of which only resolve once the build is fixed.
- **Suggestion**: Add motivation, a numbered contributions list, and a related-work pointer; verify roadmap cross-refs resolve.

### MJ11. Core derivation section has broken sentences and stray symbols at critical points (prose-auditor)
- **Location**: `rd_ph_filter.tex` lines 52 to 95 and line 199.
- **Quoted text**: line 199 "no other member of `\Set{S}` hashes ?, and ..."; lines 58 to 65 contain an unbalanced `\SetContains` signature and an orphaned duplicated sentence (line 65).
- **Problem**: The most important section reads as a working draft at the moment the construction's type is introduced; the membership-test algorithm `alg:PHF_has` is entirely inside a `\COMMENT{}` block (lines 134 to 160).
- **Suggestion**: Rewrite lines 52 to 95 as one clean typed definition; fix the "?"; uncomment and finish the membership algorithm.

### MJ12. The C++ section is not presentable prose (prose-auditor)
- **Location**: `cpp_imp.tex` lines 12, 15, 152.
- **Quoted text**: line 12 "TODO: break up each function/class/maybe method into separate listings"; line 152 "`... ; ???`".
- **Problem**: TODO notes to self, orphan phrases, large commented blocks, a non-compiling listing, almost no connecting prose.
- **Suggestion**: Write the section around a few clean, compiling listings once the codebase question is resolved.

### MJ13. All nine self-citations are unpublished placeholders; several load-bearing (citation-verifier)
- **Location**: `references.bib` lines 5 to 57.
- **Problem**: `oph` (space theorem), `shs` (claimed "optimally implements the Bernoulli set and oblivious set", `adt.tex` line 340) rest on non-existent manuscripts; `bsets`/`bmaps` exist as real family drafts and can be upgraded now.
- **Suggestion**: Upgrade `bsets`/`bmaps`/`phf`; prove or defer the `oph`/`shs`-dependent claims.

### MJ14. Real prior-art references present but never cited; lower bound mislabeled a "postulate" (citation-verifier, literature)
- **Location**: prose vs `.bib`; `rd_ph_filter.tex` line 210 and `adt.tex` line 280 (`\begin{postulate}` for the `-log2 eps` bound).
- **Problem**: `graf2020`, `fan2014`, `dillinger2021`, `pagh2005`, `dietzfelbinger2008`, `bloomier`, `carter1978` are in the `.bib` but uncited in prose; the `-log2 eps` lower bound is stated as a postulate when it is the published CFGMW (1978, `carter1978`) result.
- **Suggestion**: Cite `carter1978` at both postulate sites and reclassify as a theorem; deploy the filter references in a related-work section; cite `bloomier` in `pmf.tex`.

### MJ15. `k`-perfect placement probability has an indexing/off-by-one concern (logic-checker, methodology-auditor)
- **Location**: `k_perfect_hashing.tex` lines 13 to 27.
- **Quoted text**: "`\RV{K}_j \sim \geodist((N - j + 1)/N)`" and "`p(k) = \prod_{j=1}^{m-1}(1 - (j/N)^{k+1})`".
- **Problem**: The geometric (occupied-from-top) and the product (`(j/N)` from the bottom) index conventions do not visibly correspond, and the `j=1` terms disagree; "coupon collector" is a loose label for what is a bounded-probe occupancy model.
- **Suggestion**: State the placement model precisely, align indices, validate by a short Monte Carlo.

### MJ16. Duplicate figure label and dangling/placeholder cross-references (format-validator, prose-auditor)
- **Location**: `adt.tex` lines 514 and 579 (both `\label{fig:cor_union_same_fprate}`); `\cref{dummyref}` at `adt.tex` lines 99, 362, 411, 456; `\cref{thm:fpr,thm:fnr}` at line 25 vs the actual `thm:fp_rate` (defined line 184); `lst:asetunion`/`lst:asetcomp` reference commented-out listings.
- **Problem**: Duplicate label; `dummyref` is a literal placeholder cited 4 times (will render `??`); `thm:fpr`/`thm:fnr` do not match the defined label and will mis-resolve; the listing labels point at commented-out content.
- **Suggestion**: Unique-label the live figure; replace `dummyref` with the real composition-theorem citation; fix the `thm:fp_rate` name mismatch; restore or de-reference the listings.

### MJ17. Empirical independence / FPR distribution not validated against the family's binomial prediction (methodology-auditor)
- **Location**: n/a (absent); ties to `rd_ph_filter.tex` line 179.
- **Problem**: The whole point of being a "Bernoulli set" is the binomial error-count behavior from `bsets`; the implementation's measured FPR distribution across seeds is never compared to that prediction.
- **Suggestion**: Add a seed-sweep experiment comparing measured FP counts to the binomial.

---

## Minor Issues

1. "???"/"$?$" placeholders in displayed math/prose: `adt.tex` 206, 428; `rd_ph_filter.tex` 199; `cpp_imp.tex` 152. (prose, logic)
2. Typos: "mutalbe" (`rd_ph_filter.tex` 366), "memmbership"/"probality" (418), "maximumn" (439, 464); mis-typed `h{$x$}` macro (199, 201); `\BL{X}` missing parens (`adt.tex` 298). (prose)
3. Two competing Bloom crossover thresholds stated as fact: `2^-3` (`intro.tex` 20) vs `2^-4` (`rd_ph_filter.tex` 531), without flagging the theoretical-vs-CHD distinction. (prose, novelty)
4. Abstract over-promises (the C++ comparison) relative to current content. (prose, methodology)
5. `emaps` cited decoratively (`k_perfect_hashing.tex` 10) but is an uncitable placeholder. (citation)
6. `bloom1970` (the original Bloom paper) unused while the survey `bf` carries all Bloom citations; cite the primary source for the structure and `1.44` bound. (citation)
7. Bib hygiene: `graf2020` typed `@inproceedings` but has journal fields (it is `@article` in ACM JEA); `dillinger2021` key-year vs `year={2022}`. (citation)
8. Definition of sigma-algebra left unfinished ("closed under...", `adt.tex` 51 to 53) though surrounding reasoning is correct. (logic)
9. Max-entropy-coder theorem proof trails off without a conclusion (`rd_ph_filter.tex` 404 to 416). (logic, prose)
10. Contribution list absent; novelty hard to locate. (novelty)
11. Relationship to sibling `bernoulli-hash-function` (the "optimal construction") unstated. (novelty)
12. `\COMMENT{}` gobble macro disables a whole algorithm and figures fragilely; prefer real comments/VCS. (format)
13. `state.md` build claim ("compiles to 10 pages") is stale. (format)
14. The `k`-perfect placement model lacks simulation support. (methodology)
15. No experimental protocol/hardware described (because no experiments yet). (methodology)
16. `fig:efficiency_vs_fprate_union_paset` defined inside a `\COMMENT{}` block, never produced. (format, prose)
17. `simple`, `fks`, `mehlhorn1982` (MPHF references) uncited though directly relevant to the `1.44`/`2.07` numbers. (citation)
18. Orphan sentence "Open set of data types, closed set of operations." (`cpp_imp.tex` 15). (prose)
19. Document class generic `article` with venue undetermined; defer formatting to venue selection. (format)

## Suggestions

1. Restore the build first (stub `img/phfilter.tex`, fix `dummyref` and the `thm:fp_rate` name mismatch), then iterate; a building PDF is the precondition for all other review.
2. Write a related-work section by deploying the references already in the `.bib`; this is the single cheapest high-value improvement and directly addresses CR2/MJ14.
3. Wire the existing `maph` benchmarks into an experiments section: measured FPR vs `2^-b`, measured bits/key vs the predicted formula, throughput vs Bloom; this addresses CR3 and grounds the optimality discussion.
4. Add RecSplit and the BBHash/fuse references to strengthen the "MPHF overhead is small" argument and to compare honestly with the best current filters.
5. Add a numbered contributions paragraph and one paragraph situating the PHF relative to `bernoulli-hash-function` and the (theoretical) singular hash set.
6. Run a one-page Monte Carlo validating both the FPR (`2^-M`) and the `k`-perfect placement probability `p(k)` before relying on the latter.

---

## Detailed Notes by Domain

### Logic and Proofs
The core FPR theorem is correct; the central problems are mechanical and concentrated in the unfinished `rd_ph_filter.tex` and the union-efficiency proof in `adt.tex`. The most serious is the propagating union-FPR sign error (CR4), which prevents that proof from reaching its stated result and is internally inconsistent with the family's own composition theorem. A theorem is duplicated verbatim (MJ3), both estimator statements carry a spurious sign (MJ4), a distributional claim cites nothing (MJ5), and the headline space theorem is conditional on an unpublished manuscript (MJ2). The sigma-algebra/semiring discussion is a genuine correct contribution. Full detail: `logic-checker.md`.

### Novelty and Contribution
Calibrated to an implementation paper, the realistic novelty is the Bernoulli-ADT framing, the k-perfect two-rate analysis, and the fuzzy-IR application, not the data structure (which is the known MPHF+fingerprint AMQ). The paper currently claims the structure itself and omits related work entirely (CR2), and the parts that would carry the real contribution are the least finished (MJ9). The optimality claim is under-differentiated (MJ1). Full detail: `novelty-assessor.md`.

### Methodology
Zero experiments against an abstract that promises a comparison (CR3), a C++ section pointing at a non-existent codebase while the real `maph` library goes undocumented (MJ6), results tables without provenance and figures reading absent CSVs (MJ7), and unvalidated independence assumptions (MJ8, MJ17). The good news: the analytic framework is the right one, and a benchmarkable library already exists in-repo. Full detail: `methodology-auditor.md`.

### Writing and Presentation
Bimodal: `adt.tex`, the typed-PHF section, and the fuzzy-set exposition are mature; the intro (MJ10), the core derivation's introduction-of-type passage (MJ11), and the C++ section (MJ12) are unfinished, with visible authoring scars (TODO notes, "???", orphan sentences, a duplicated theorem and figure label). Notation discipline is good. The skeleton matches the abstract's promised arc, so this is finishing work, not restructuring. Full detail: `prose-auditor.md`.

### Citations and References
Better than the state file suggested: 16 real references already present, most with DOIs, no fabricated citations. The problems are (a) nine unpublished self-citation placeholders, some load-bearing (MJ13); (b) the real references are not deployed in prose, and the published lower bound is mislabeled a "postulate" (MJ14); (c) an empty `\cite{}` in the core section (MJ5). The cheapest win in the whole review is deploying references the paper already owns. Full detail: `citation-verifier.md`.

### Formatting and Production
The paper does not build (CR1): a fatal missing-figure error, with `img/` and `data/` directories absent. Duplicate figure label, placeholder `dummyref` cited four times, and a `thm:fpr`/`thm:fnr` vs `thm:fp_rate` name mismatch will cause wrong cross-refs even after the build is restored (MJ16). A minimal path to a building PDF is documented in `format-validator.md`.

## Literature Context Summary

The paper's central structure is the well-known MPHF+fingerprint approximate-membership query, the baseline behind xor filters (Graf and Lemire 2020, ~1.23x the `n log2(1/eps)` lower bound), fuse filters (~1.075x), cuckoo filters (Fan et al. 2014, deletion-capable), and the Bloomier filter (Chazelle et al. 2004, the key-value case the Perfect Map Filter re-derives). The `-log2 eps` lower bound the paper states as a "postulate" is the published CFGMW (1978) theorem. The `1.44` MPHF figure is the `log2(e)` information-theoretic minimum; practical MPHFs (CHD 2009; RecSplit 2020) sit at ~1.5 to 3 bits/key, so the PHF's space claim is correct only as `eps -> 0` and is beaten by xor/fuse at practical FPR. All of these references except RecSplit/BBHash are already in the paper's `.bib`. The defensible contribution, given the declared role, is the Bernoulli-ADT framing plus the k-perfect FNR analysis and the fuzzy-IR application; the data structure is not new. Full detail: `literature-context.md`.

## Review Metadata
- Agents used (lenses applied): literature-scout (broad + targeted, compiled directly; see method note in `literature-context.md`), logic-checker, novelty-assessor, methodology-auditor, prose-auditor, citation-verifier, format-validator.
- Cross-verifications performed: 4 (CR2 novelty x prose; CR3 methodology x logic; CR4 logic x methodology; MJ1 logic x novelty x literature). All four confirmed; no reversals.
- Disagreements noted: 0 substantive. The only apparent conflict (the `state.md` "compiles" claim vs the format-validator's fatal-error finding) was resolved against the state file by an actual build run: `main.tex` now includes `rd_ph_filter.tex`, which broke the build after the state note was written.
- Note on execution: the dedicated literature-scout subagents could not be spawned in this run (the `Task` tool was unavailable inside the sandbox); the area chair applied all specialist lenses directly, reading every section, the bibliography, the glossary, and the C++ tree, and running the build. Every Critical and Major finding's quoted text was verified against the manuscript by direct read/grep.
