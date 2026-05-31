# Multi-Agent Review Report

**Date**: 2026-05-29
**Paper**: The algebra of the random approximate map model (Alexander Towell)
**Recommendation**: major-revision

## Summary

**Overall Assessment**: This is a structurally important extension paper in the Bernoulli family, and its central contribution, the compositional algebra of approximate maps in section 5, is original, correct, and well-written (verified symbolically and against the foundation paper). The recommendation is major-revision rather than minor because the space-complexity machinery in sections 6 and 7 contains one incorrect stated formula that contradicts the paper's own later derivation, several unproven or mis-directed proof steps, and an over-claim that the singular hash map is a "concrete algorithm," together with a build that fails under its own documented command. None of these touches the core result; all are repairable, and the headline space bound is reproducible once the broken intermediate is replaced.

**Strengths**:
1. The composition theorem (false negative rate `1-(1-fn1)(1-fn2)` and the `rho`-parametrized false positive rate) is genuinely novel and correct; it is the correct Maybe-type specialization of the foundation's full-channel composition theorem, with the `rho` overlap parameter being a new contribution with no analog in the foundation (logic-checker, confirmed by methodology-auditor and by independent symbolic check).
2. The function-space and Kronecker-factorization viewpoint unifies Bernoulli Booleans, sets, maps, and relations cleanly and gives the family a single conceptual spine (novelty-assessor).
3. Sections 1 to 5 are well-staged, with a strong "Boolean thread" and worked examples whose arithmetic checks exactly (prose-auditor, logic-checker).
4. Bibliography integrity is high: all 15 entries are used and accurate, with no undefined citations or references (citation-verifier).
5. The paper is honest about scope: it flags Monte Carlo validation and the `rho` dependence as future work (methodology-auditor).

**Weaknesses**:
1. The section 6.6 "probability of success" formula is incorrect and contradicts the section 7 result for the same object (logic-checker C1; methodology-auditor confirms).
2. The singular hash map proof (section 7) is notationally inconsistent (`mod t` vs `mod BL` vs `trunc`, a backwards `N < max BL` hypothesis) and does not rigorously establish its otherwise-likely-correct formula (logic-checker M1).
3. The section 7 space theorem proves only an upper bound via Jensen but states a two-sided bound; the lower-bound half is asserted, not derived (logic-checker M3; methodology-auditor concurs).
4. The singular hash map is presented as a "concrete algorithm" but is an exponential-expected-time existence construction; abstract and intro over-promise it (methodology-auditor M6, prose-auditor M8, novelty-assessor Contribution 4).
5. No empirical validation of the two most novel quantitative claims (`rho` composition FPR and the SHM bound), which the paper itself notes (methodology-auditor M5).
6. The documented build command omits the required `-shell-escape` and fails to produce a PDF; `minted`/`multicol` are loaded but unused (format-validator M10).
7. Two companion papers (data_type, composition) are referenced in prose but absent from the bibliography, leaving the novelty boundary with data_type uncitable (citation-verifier M9, novelty-assessor).

**Finding Counts**: Critical: 1 | Major: 9 | Minor: 22 | Suggestions: 6

## Critical Issues

### C1. The section 6.6 "probability of success" formula is incorrect and contradicts section 7 (source: logic-checker; cross-verified: methodology-auditor)
- **Location**: `sections/entropy_maps.tex`, subsection "Probability of success" (`sec:prob-success`), line 151.
- **Quoted text**: "The probability of success given a rate-distortion $\fnrate$ on positives and $\fprate$ on negatives is given by $p(\fprate,\fnrate) = \binom{m}{(1-\fnrate)m} \fprate^{m(1-\fnrate)} (1-\fprate)^{m \fnrate}$."
- **Problem**: Three independent defects. (1) Wrong base: the per-trial success probability is a product of per-key collision probabilities of order `eps` and `2^{-BL(v)}` (as section 7 correctly derives, `p = eps^{m-1}/2^{m mu}`), not `eps^{m(1-fnr)}(1-eps)^{m fnr}`; the factor `(1-eps)^{m fnr}` has no derivation and contradicts section 7, where false-negative keys are dropped, not "succeed with probability `1-eps`." (2) The binomial coefficient `binom{m}{(1-fnr)m}` counts subsets of stored keys, which does not belong in a single bit string's success probability for a fixed stored set; if a marginalization were intended, the `fnr` Bernoulli weights are missing. (3) `(1-fnr)m` and `m fnr` are treated as exact integers with no floor/ceiling caveat.
- **Suggestion**: Delete this expression and route section 6.6 through the section 7 result restricted to the `(1-fnr)m` stored keys (`p = eps^{(1-fnr)m - 1}/2^{(1-fnr)m mu}`). Reconcile sections 6.6 and 7 so they state the same `p`.
- **Cross-verified**: Yes, by methodology-auditor. The methodology-auditor independently reproduced the headline bound `-log2 eps + mu` from section 7's correct `p` (not from this formula), confirming both that the headline result survives and that this intermediate is the broken link. Severity agreed: critical (it is a stated theorem-grade result that downstream steps depend on, and it is internally contradicted).

## Major Issues

### M1. The singular hash map success-probability proof is notationally inconsistent and not rigorous (source: logic-checker; cross-verified: methodology-auditor)
- **Location**: `sections/shm.tex`, proof of `thm:shm-success`, lines 78 to 99.
- **Quoted text**: "$k_1$ hashes to $y = \hash(k_1) \mod t$, where $\hash \colon \BitSet^* \to \BitSet^N$ ... and $N < \max{\BL(v_1),\ldots,\BL(v_m)}$" and "The probability that $\hash(1 \cat k_1) \mod \BL(v_1) = v_1$ is given by $\frac{1}{2^{\BL(v_1)}}$."
- **Problem**: Three reduction operations (`mod t`, `mod BL(v_1)`, `trunc(.,k)` from Algorithm 1) appear for one mechanism; `hash(...) mod BL(v_1)` reduces modulo a small bit-length integer and cannot equal a value `v_1` (type-incorrect; the intended event is "the first `BL(v_1)` bits equal the codeword for `v_1`"). The hypothesis `N < max BL` is backwards (there must be enough hash bits: `N >= max BL`, or use the random oracle `B^infty`). The leading `1 cat` tag and the independence of the membership and value events are asserted without the random-oracle justification.
- **Suggestion**: Rewrite against the random oracle and the actual `trunc(.,k)` operation, stating events as bit-prefix matches: membership prefix agreement (`eps^{m-1}` given one key fixes the bucket) and value-prefix matches (`2^{-m mu}`). The final formula is likely correct; the derivation must be made so.
- **Cross-verified**: Yes. Methodology-auditor reproduced the resulting `p = eps^{m-1}/2^{m mu}` cleanly under a random-oracle model, so the conclusion is trustworthy even though the written proof is not.

### M2. The `E[log2 T]` space estimate in section 6.6 is asserted and self-contradictory about what it computes (source: logic-checker)
- **Location**: `sections/entropy_maps.tex`, `sec:prob-success`, lines 156 to 164.
- **Quoted text**: "The expected code size is $\Expect{\log_2 \RV{T}}$, which is non-linear and problematic but may be approximated with [...] This result is not the result of computing $\Expect{\log_2 \RV{T}}$, nor the expectation of its Taylor approximation. It is simply $\log_2 \Expect{\RV{T}}$."
- **Problem**: The text calls the displayed expression an "approximation" of `E[log2 T]`, then says it is actually `log2 E[T]`. By Jensen, `log2 E[T] >= E[log2 T]`, so it is an upper bound, not an approximation, and the displayed binary-entropy expression is given without the intermediate derivation that would let a reader verify it (especially against the broken C1 `p`).
- **Suggestion**: State plainly that expected code size is bounded by `log2 E[T]` (a Jensen upper bound), derive the expression from `E[T]=1/p` with the corrected `p`, and import the `O(1/m)` gap that section 7 already states.

### M3. The section 7 space theorem proves only an upper bound but states a two-sided bound (source: logic-checker; cross-verified: methodology-auditor)
- **Location**: `sections/shm.tex`, `thm:shm-space` and proof, lines 113 to 161.
- **Quoted text**: "By Jensen's inequality (since $\log_2$ is concave), $\Expect{\log_2 \RV{Q}} \leq \log_2 \Expect{\RV{Q}}$" supporting a theorem that states both a "lower-bound given by $-(1 - \fnrate) \log_2 \fprate + (1 - \fnrate) \mu$" and an "upper-bound given by $-(1 - \fnrate) \log_2 \fprate + \mu$."
- **Problem**: The Jensen step yields only an upper bound on `E[log2 Q]`. The lower-bound half is argued informally ("the value bits scale proportionally ... contributing `(1-fnr)mu`") without an inequality, so it is unproven. The proof also slides between the realized length `floor(log2 n)` and the expectation `E[log2 Q]`.
- **Suggestion**: State the `fnr=0` case as a clean asymptotic equality `-log2 eps + mu` (which the proof supports), and present the lower/upper pair as the uniform-bit-length vs degenerate-bit-length *cases* with a proper two-sided argument; make explicit that the stored cost is `log2 Q` for the successful trial index.
- **Cross-verified**: Yes. Methodology-auditor concurs the `fnr=0` equality and the upper bound reproduce, the lower-bound half is asserted.

### M4. The Kronecker theorem's parameter-count comparison uses an incorrect baseline and an undefined order `N` (source: logic-checker)
- **Location**: `sections/special_cases.tex`, `thm:kronecker`, line 116.
- **Quoted text**: "the number of free parameters is $n \cdot (|\Set{Y}| - 1)$, compared to $N(|\Set{Y}|^{|\Set{X}|} - 1)$ for a general $N$-th order channel on $\Set{Y}^{\Set{X}}$."
- **Problem**: The honest baseline for a general channel on the function space is a `|Y|^|X| x |Y|^|X|` stochastic matrix with `|Y|^|X|(|Y|^|X| - 1)` free parameters, not `N(|Y|^|X| - 1)` for an unspecified `N`. The comparison is not apples-to-apples, and the per-block count `|Y|-1` silently assumes row-homogeneous per-input channels (all latent values share one response row), an assumption beyond "i.i.d. across inputs." The qualitative claim (independence collapses exponential to linear parameter count) is correct and is the point.
- **Suggestion**: Fix the baseline to `|Y|^{|X|}(|Y|^{|X|}-1)`, drop or define `N`, and state the within-block row-homogeneity assumption precisely so it agrees with the body's `4x4 -> 12 -> 4` example.

### M5. No empirical validation of the two most novel quantitative claims (source: methodology-auditor)
- **Location**: whole paper; `sections/conclusion.tex` line 23.
- **Quoted text**: "Monte Carlo validation of the composition error bounds, particularly the dependence on the parameter $\rho$ governing false-positive overlap, remains to be developed."
- **Problem**: The `rho`-parametrized composition FPR and the SHM asymptotic bound are exactly the claims that benefit from a sanity simulation (the `rho` value "depends on the implementation" and only the uniform case is worked; the SHM bound is asymptotic with an asserted `O(1/m)` gap). The `research/` artifacts are not referenced or reported.
- **Suggestion**: Add a short Monte Carlo validating `thm:comp-fpr` across `rho in {0, 0.1, 0.5, 1}` and `thm:comp-fnr` for `k`-fold composition (a few dozen lines), and a random-oracle simulation of the SHM bound at `m = 10, 100, 1000`. This is the cheapest way to raise confidence in the headline results.

### M6. The singular hash map is over-claimed as a "concrete algorithm"; it is an exponential-time existence construction (source: methodology-auditor and prose-auditor; related: novelty-assessor Contribution 4)
- **Location**: abstract (`main.tex` line 98); `sections/intro_new.tex` line 30 (Contribution 4); `sections/shm.tex` Algorithm 1 and `eq:exp_trials`.
- **Quoted text** (abstract): "the \emph{singular hash map}, a concrete algorithm achieving the information-theoretic lower bound of $-\log_2 \fprate + \mu$ bits per element."
- **Problem**: `E[Q] = 2^{m mu}/eps^{m-1}` grows exponentially in `m` (for `m=30, mu=8, eps=2^{-8}` this is about `2^{472}` expected trials), so Algorithm 1 is infeasible beyond toy sizes. "Concrete algorithm achieving" sets an expectation of a runnable method; the body delivers a theoretical achievability argument (a random-coding-style existence result). This is the strongest external contributor of "overclaim" and dovetails with the absence of a comparison to practical retrieval structures that hit the same floor in linear time.
- **Suggestion**: Reframe as "a hash-based construction that asymptotically attains the lower bound," add the exponential-expected-trials caveat in the body, and situate it against the practical retrieval line. Foreground the composition theorem in the abstract instead.
- **Cross-verified**: prose-auditor (M8) and methodology-auditor (M6) independently flagged the same overclaim from writing and feasibility angles respectively; novelty-assessor independently ranked this the weakest contribution. Three-way agreement.

### M7. Sections 6 to 7 are a register break from sections 1 to 5 (source: prose-auditor; cross-verified: novelty-assessor)
- **Location**: `sections/entropy_maps.tex` and `sections/shm.tex` versus sections 1 to 5.
- **Quoted text**: "This result is not the result of computing $\Expect{\log_2 \RV{T}}$, nor the expectation of its Taylor approximation. It is simply $\log_2 \Expect{\RV{T}}$."
- **Problem**: The first five sections use precise, well-staged prose; section 6.6 and the section 7 proof degrade into terse, self-referential fragments with a notational dialect that does not match the earlier sections. Prose roughness co-occurs with the actual mathematical errors (C1, M1, M2).
- **Suggestion**: Rewrite sections 6.4 to 7.2 to the standard of sections 1 to 5: stage each definition, narrate each proof step, use one reduction operation (`trunc(.,k)`) throughout, and cut the asides.
- **Cross-verified**: Yes, by novelty-assessor: the rough prose coincides with the weakest novelty axis (entropy map / SHM), so unclear writing is not hiding a strong contribution; clarity and novelty are aligned. This is a framing-and-polish problem, not a hidden-strength problem.

### M8. Two companion papers are referenced in prose but missing from the bibliography (source: citation-verifier; cross-verified: novelty-assessor)
- **Location**: `sections/intro_new.tex` lines 35 to 36; `sections/special_cases.tex` line 105; `sections/conclusion.tex` line 17; `sections/composition_new.tex` line 445.
- **Quoted text**: "A companion paper on random approximate algebraic types develops the constructive counterpart ..." (the data_type paper) and "the companion paper on composition of Bernoulli sets" (the composition paper), both referenced by description only, with no bib key or `\cite`.
- **Problem**: Both are real family papers; the foundation cites them as `bernoulliComposition`/`bernoulliEntropy`. Referencing by description leaves them uncitable. The data_type omission matters most because the novelty boundary (the maps-vs-data_type ownership of the Kronecker-factorization headline) depends on it, and the "two perspectives, one theorem" conclusion points at a paper the reader cannot consult. By contrast `aset` and `arelation` are in the bib, so the omission is an inconsistency.
- **Suggestion**: Add `@Unpublished` entries for the data_type and composition papers mirroring the `aset`/`arelation` format, and `\cite` them at the prose locations. State explicitly which paper owns the Kronecker-factorization theorem so maps and data_type do not appear to independently claim the same result.
- **Cross-verified**: Yes, by novelty-assessor, who flagged the same missing data_type citation as the one place where novelty attribution between two family papers is fuzzy.

### M9. The documented build command omits the required `-shell-escape` and fails (source: format-validator)
- **Location**: `bernoulli_maps/CLAUDE.md` and `.papermill/state.md` build commands; `main.tex` line 39 (`\usepackage{minted}`).
- **Quoted text** (recorded command): "`pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`".
- **Problem**: `minted` requires shell escape; the documented command fails on pass 1 with "You must invoke LaTeX with the -shell-escape flag. ... Fatal error occurred, no output PDF file produced!" The working command is `pdflatex -shell-escape main.tex && bibtex main && makeglossaries main && pdflatex -shell-escape main.tex && pdflatex -shell-escape main.tex` (verified: 24-page PDF, zero undefined refs/cites). Confirmed that `minted` and `multicol` are **not used** anywhere in the active sections (only in `sections/unused/`).
- **Suggestion**: Best fix: remove `\usepackage{minted}` and `\usepackage{multicol}` from `main.tex` (both unused), which eliminates the shell-escape requirement and lets the documented plain command work. Otherwise, update the documented command in `CLAUDE.md`, `state.md`, and the collection note to include `-shell-escape` and `makeglossaries`.

## Minor Issues

(Attributions in parentheses; full detail in the per-specialist reports.)

1. The composition FNR theorem is the correct Maybe-type specialization of the foundation's `thm:composition_rates`, but the paper never states this; one sentence ("a dropped positive cannot be re-promoted, so the foundation's cross term vanishes") would close the family loop. This is a verification-pass positive, not a defect. (logic m1)
2. "Composition raises the model order" is stated as "in general second-order" but the crucial qualifier (only when `f`'s false-positive distribution depends on `x`) is relegated to an unnumbered remark that partly contradicts the headline. Fold the condition into the lemma hypothesis. (logic m2, prose m14)
3. "Closure under composition" proves only positivity (`P[correct]>0`), not the defining approximate-map property; rename or add the one line citing element-wise independence per stage. (logic m3)
4. `thm:optimal-code` states `ell = H(Y)` exactly, which holds only for dyadic `p_y`; add the dyadic assumption or write `H(Y) <= ell < H(Y)+1`. (logic m4)
5. The "`-log2 eps`" simplification in section 6.6 references an ambiguous "the above"; tighten the antecedent to the binary-entropy expression. (logic m5)
6. "Map" is used for both total (`Y^X`, the `|Y|^|X|` count) and partial (`X -> Maybe Y`, `Dod(f)`) functions; state once that "map" means a partial function lifted to `X -> Maybe Y` with total as the `Dod(f)=X` case. (logic m6, prose m13)
7. `rho` has only one worked instance (uniform); give a second contrasting instance or a Monte Carlo so the range `[0,1]` is exercised. (methodology m7)
8. The entropy map's "maximum-entropy / minimum space" optimality is asserted without an optimization program or proof of the max-conditional-entropy property; either write the program or soften to "construction." (methodology m8)
9. Composition independence requires independently sampled hash seeds per stage; in a shared-hash realization the product formulas become bounds. Add a remark. (methodology m9)
10. `\Maybe{Y}` renders as `m(Y)`, an idiosyncratic notation, and `nothing` vs `Dod` vs `pfun` are never reconciled in one place; state `m(Y) := Y union {nothing}` once. (prose m10)
11. `\BL` is an algorithm keyword (`$\ell$`) used in math mode as a bit-length function and visually collides with the scalar `ell = H(Y)`; define a dedicated math operator for bit length. (prose m11)
12. `prelim.tex` defines a set as "unordered" but `gloss.tex` defines it as "ordered" (latent contradiction; `gloss.tex` is not loaded). Fix or remove `gloss.tex`. (prose m12)
13. Theorem-qualifying content sits in unnumbered remarks (composition order condition; `P`-known-a-priori); promote into hypotheses or numbered remarks. (prose m14)
14. Wording/typo nits: "optimally space-efficient code" -> "space-optimal"; "the singular hash set proves" -> "establishes/witnesses"; `gloss.tex` "poular"/"a a"; `def:randomoracle` `B^infty` vs `def:entropy-map` finite-hash codomain unreconciled. (prose m15)
15. The `-log2 eps` membership floor is attributed to Cover-Thomas; the primary source is Carter et al. 1978 (and Pagh-Pagh-Rao 2005 for the tight AMQ bound). Add the primary cites for the floor. (citation m16)
16. Source-coding cite `shannon1948` is correct; optionally pair the prefix-free/Kraft framing with Cover-Thomas ch.5. (citation m17)
17. The Iverson bracket and Huffman/Golomb/Elias codes are named without citation; optional standard cites. (citation m18)
18. `@Unpublished` companion entries (`aset`, `arelation`) lack any locator; add a repo note if they become public. (citation m19)
19. Duplicate PDF destination anchors (`equation.2.1`, `equation.3.1`, ...) from the proof/example equation-counter reset; in-PDF links to renumbered equations may misnavigate. Give those environments a distinct counter prefix or accept as benign. (format m20)
20. One overfull hbox (6.1pt) at `shm.tex` lines 77 to 80. Trivial rewrap. (format m21)
21. The glossary apparatus is active (`glossaries` loaded, `\makeglossaries` called, `makeglossaries` required in the build) but prints nothing (`\loadglsentries{gloss}` is commented and there are no `\gls` calls); `gloss.tex` is dead weight. Remove the glossary machinery or actually print it. (format m22)
22. `defs.tex` is not loaded by `main.tex` (the active environments come from `envnotation.sty`); its `pdftitle={The approximate map abstract data type}` never reaches the PDF (so the output has no correct title metadata) and it duplicates the theorem definitions with different numbering. Delete `defs.tex` and add a correct `\hypersetup{pdftitle=...}` to `main.tex`. (format m23)

## Suggestions

1. Restructure so the composition algebra (section 5) is the climax and the abstract's lead result; present the entropy-map/SHM material as a shorter, honestly-scoped "construction" coda. (prose, novelty)
2. Add a one-figure Monte Carlo validating the composition rates (cheap, high value). (methodology)
3. Cite and contrast the modern retrieval line (Dietzfelbinger-Pagh, binary fuse, BuRR, RecSplit) so the SHM's `-log2 eps + mu` claim is situated against constructions that achieve the floor in linear time. (novelty, literature-context)
4. Sharpen the Bloomier-filter differentiation: "Bloomier is a construction; we give the model and its composition closure." (novelty)
5. Coordinate ownership of the Kronecker-factorization theorem with the data_type companion so the two papers do not appear to claim it independently. (novelty, citation)
6. Remove the unused `minted`/`multicol` includes and the orphaned `defs.tex`/`gloss.tex` to simplify the build and eliminate the shell-escape requirement. (format)

## Detailed Notes by Domain

### Logic and Proofs
The composition algebra (section 5) is correct and is the paper's strongest material: `thm:comp-fnr`, `thm:comp-fpr`, both overlap corollaries, and the `k`-fold corollary all verify (checked symbolically: `rho=0 -> eps1 eps2`, `rho=1 -> eps1(1-fn2)`, two-stage example `0.00118`, approximate-NOT `0.0975`). The FNR theorem is confirmed to be the correct Maybe-type specialization of the foundation's full-channel `thm:composition_rates` (the foundation's `fn'*eps` cross term vanishes because a dropped positive cannot be revived); the `rho` FPR result is new and independently re-derived as correct. Problems concentrate in sections 6 to 7: C1 (wrong `p` formula, critical), M1 (inconsistent SHM proof), M2 (`E[log2 T]` asserted), M3 (Jensen direction / unproven lower bound), M4 (Kronecker baseline/count), plus minor scope and assumption issues (m1 to m6). `prop:loss_decomp` and `prop:binom_errors` are clean.

### Novelty and Contribution
Real novelty: (i) arbitrary-codomain generalization with explicit Maybe-type semantics, (ii) the composition theorem with the `rho` parameter and model-order elevation (the best and most defensible result), and (iii) the unifying function-space/Kronecker lens (an organizing contribution, not a new theorem). Differentiation from Bloomier is adequate but too soft; differentiation from the in-family relations paper is clean; differentiation from the data_type paper is articulated but rests on a missing citation and a shared Kronecker headline. The entropy-map/SHM (Contribution 4) is the weakest axis: largely imported from the foundation and `bernoulli-hash-function`, and close to known retrieval structures. The contribution is currently mis-weighted (the abstract gives the SHM equal billing with the composition theorem).

### Methodology
Pure theory, no experiments. Sections 2 to 5 modeling is sound and reproducible (reproduced by hand). The headline space bound `-log2 eps + mu` is reproducible from section 7's correct `p`, independent of the broken section 6.6 formula (this is the cross-verification result that keeps C1 from being fatal to the paper). Major gaps: no validation of `rho` or the SHM bound (M5, the paper concedes this), and the SHM's exponential expected trials make "concrete algorithm" an overclaim (M6). Independence-of-stages and the entropy-map optimality are under-justified (m7 to m9).

### Writing and Presentation
Sections 1 to 5 are strong; sections 6 to 7 are a clear register break (M7) with terse, self-referential proof prose and a notational dialect (`hash`, `BL`, `mod t`) that diverges from the earlier sections. The abstract over-promises the SHM (M8). Notation-consistency defects (`m(Y)` rendering, `BL` as a misused keyword, `Dod`/`Dom` drift, a latent set-definition contradiction) are all minor. The "two perspectives, one theorem" conclusion paragraph is genuinely good.

### Citations and References
Bibliography is clean and accurate: 15 entries, all used, no undefined citations or references, entries spot-checked correct. The consequential gap is two companion papers (data_type, composition) referenced in prose but absent from the bib (M8 in the unified list); the data_type omission undercuts a contribution-level boundary claim. The AMQ membership-floor attribution to Cover-Thomas is imprecise (m15). Other gaps are optional polish.

### Formatting and Production
Builds to a clean 24-page PDF with zero undefined refs/cites, but only with `-shell-escape`, which the documented command omits, so the documented build fails outright (M9). `minted`/`multicol` are loaded but unused, so the cleanest fix is removal. Cosmetic items: one 6.1pt overfull box, duplicate PDF anchors from proof equation-renumbering, an active-but-empty glossary apparatus, and an orphaned `defs.tex` whose stale (and wrong) PDF title never reaches the output.

## Literature Context Summary
The paper sits at the junction of approximate-membership/retrieval data structures and information theory. Its most direct external prior art is the Bloomier filter (Chazelle 2004, cited), which it correctly frames as an instance of the Bernoulli map; the differentiation rests on the probabilistic model and composition algebra, which is genuine open ground (no external "algebra of approximate maps" exists). The singular hash map's space target `-log2 eps + mu` is the classical membership floor (Carter et al. 1978; the modern retrieval line, binary fuse / BuRR / RecSplit, achieves it in linear time and is uncited). Within the family, the paper legitimately extends `bernoulli_sets` (foundation), cleanly defers `n`-ary relations to `bernoulli_relations`, and shares the exponential-type/Kronecker boundary with `bernoulli_data_type` (which is not yet citable here). The composition algebra is the paper's unique ground; the construction half is derivative.

## Review Metadata
- Agents used: literature-scout (broad + targeted, merged), logic-checker, novelty-assessor, methodology-auditor, prose-auditor, citation-verifier, format-validator (7 specialist lenses).
- Cross-verifications performed: 4. (1) Logic-checker C1/M1/M3 space-complexity bundle routed to methodology-auditor, who reproduced the headline bound from the correct `p` and confirmed C1 is the broken intermediate; result: headline survives, C1 stands as critical. (2) Foundation composition cross-check (logic m1) verified symbolically: the Maybe-type FNR theorem is the correct specialization of the foundation's full-channel theorem. (3) Prose register-break (M7) routed to novelty-assessor: confirmed the rough prose coincides with the weakest novelty axis, so it is a framing problem, not hidden strength. (4) SHM overclaim flagged independently by methodology-auditor, prose-auditor, and novelty-assessor (three-way agreement).
- Disagreements noted: 0. The specialists were consistent; where they touched the same issue (the SHM, the section 6/7 errors) they agreed on substance and severity.
- Self-verification: the full manuscript was re-read; every critical and major finding's quoted text was confirmed against the source (line numbers verified); the "correct" composition results and worked examples were re-derived symbolically and numerically.
- Build: 24-page PDF, clean with `-shell-escape` + `makeglossaries`; fails under the documented command.
