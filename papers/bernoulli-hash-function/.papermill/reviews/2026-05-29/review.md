# Multi-Agent Review Report

**Date**: 2026-05-29
**Paper**: The Bernoulli Hash Function: Optimal Bernoulli Sets and Bernoulli Maps
**Author**: Alexander Towell (SIUE; ORCID 0000-0001-6443-9897)
**Recommendation**: minor-revision

## Summary

**Overall Assessment**: This is a strong, near-complete application paper in the
Bernoulli type-theory family, and it has improved substantially since the
2026-02-26 review. All three prior critical defects are resolved: the buggy
Taylor expansion in the space proof is gone (replaced by a correct Jensen +
floor-bound argument), the "Wait---" self-correction in the appendix is removed
and the order-statistic PMF now normalizes correctly, and the unsalted value-
hash inconsistency is fixed across the fixed-threshold algorithms. The paper
builds cleanly (27 pages, 0 overfull boxes), the bibliography has nearly doubled
to include the Carter et al. lower bound and the modern filter literature, and
the adaptive-threshold contribution has matured into the paper's strongest and
most original result. No new critical issues were found. The remaining work is a
handful of major-but-localized fixes (one residual algorithmic inconsistency in
the adaptive *map* path, a framing/credit adjustment, and two expected map
citations) plus polish.

**Strengths**:
1. The adaptive-threshold construction and the accompanying "price of FPR
   certainty" theorem (Delta = m*log2(1/eps)) are genuinely novel and elegant:
   they reframe the classical -log2(eps) lower bound as the information cost of
   committing to a fixed FPR. (source: novelty-assessor, logic-checker,
   literature-context)
2. The unified set/map treatment (set = map with mu = 0) gives one space-
   optimality proof for both, a clean organizing principle. (source:
   novelty-assessor)
3. All three prior critical issues are resolved and verified against the live
   text and numerically. (source: logic-checker, prose-auditor)
4. The paper compiles cleanly with no overfull boxes and no undefined
   references; prior dead code (gloss.tex) and the dangling figure are gone.
   (source: format-validator)
5. The five algorithms are precisely specified, and the comparison table plus
   three pgfplots figures summarize the three predicates effectively. (source:
   methodology-auditor, prose-auditor)
6. The maximum-entropy / obliviousness property and the careful "adaptive is not
   max-entropy" remark are well-judged and matter for the encrypted-search
   application. (source: logic-checker, novelty-assessor)

**Weaknesses**:
1. The adaptive *map* construction returns the tuple (N, t) with no salt, but
   `Find` needs the salt b to recover values; the set path is fine but the map
   path is broken. (source: logic-checker, methodology-auditor)
2. The intro's contribution 3 still frames "achieving the lower bound" as the
   novelty, although the discussion correctly attributes efficient achievability
   to Pagh-Pagh-Rao (2005). (source: novelty-assessor)
3. The closest map prior art (Bloomier filter) and the closest retrieval theory
   (Dietzfelbinger-Pagh) are not cited, despite the unified map claim. (source:
   citation-verifier, novelty-assessor)
4. Explicit "practical" claims (feasible for m <= 10; adaptive practical at any
   size; FPR concentrates) have no empirical support. (source:
   methodology-auditor)
5. Two displayed closed-form identities (E[log2 Q] in the space proof; H(Q) in
   the interpretation remark) are wrong as exact identities, though their O(1)
   asymptotic consequences are correct. (source: logic-checker)
6. Sections 7 and 8 remain thin, restating companion results with little BHF-
   specific content. (source: prose-auditor)

**Finding Counts**: Critical: 0 | Major: 3 | Minor: 11 | Suggestions: 2

(The 3 majors are distinct underlying issues. M1 is reported by two specialists,
logic-checker and methodology-auditor, and is counted once.)

## Critical Issues

None. The three prior-pass critical issues (Taylor expansion error, appendix
"Wait---" derivation, unsalted value hash) are all resolved.

## Major Issues

### M1. Adaptive map stores no salt, but the lookup requires one (source: logic-checker, methodology-auditor)
- **Location**: `sections/construction.tex`, Algorithm `alg:make_shf_adaptive`
  (map branch, lines 137-161; `\KwOut` line 125 reads "coded as a tuple
  `(N, t)`") versus `Find` (`alg:find`, line 225); and the comparison table
  `tab:predicate_comparison` (`sections/shf.tex` line 370).
- **Quoted text**: `\KwOut{ A Bernoulli map $\ASet{M}$ coded as a tuple
  $(N, t)$. }`; `Find` computes `$c \gets \hash(1 \cat x \cat b)$`; table row
  "Stored params ... Adaptive ... $(N, t)$".
- **Problem**: For the adaptive *map* (mu > 0), the construction searches for a
  salt b that yields at least p value-matching keys (line 146 uses
  `h(1 || x_i || b)`), then returns only `(N, t)`. But `Find` needs b to recompute
  `h(1 || x || b)` and decode the value. Without storing b, the adaptive map is
  not decodable. The set path (b = epsilon) is genuinely salt-free and correct.
  This is the adaptive-path analogue of prior critical C3, which was fixed only
  for the fixed-threshold algorithms.
- **Suggestion**: For the adaptive map, store `(N, t, b)`; update the algorithm
  `\KwOut`, the `Find` precondition, the comparison table's "Stored params" cell
  (it should read `(N, t)` for sets, `(N, t, b)` for maps), and add a sentence to
  `sec:adaptive_space` noting the adaptive *map* is not salt-free (so its per-
  element space is not the vanishing O(log N / m) that holds for sets).
- **Cross-verified**: Yes. Confirmed by reading the live algorithm output, the
  `Find` body, and the table row directly (area chair), and independently by the
  methodology-auditor. Logic-checker and methodology-auditor agree; no
  disagreement.

### M2. Contribution framing overclaims optimality relative to Pagh-Pagh-Rao (source: novelty-assessor)
- **Location**: `sections/intro.tex`, contribution 3 (lines 44-47) versus
  `sections/discussion.tex` (Pagh-Pagh-Rao paragraph, lines 78-84).
- **Quoted text**: "We prove that the BHF achieves the information-theoretic
  lower bound on space complexity while maximizing the entropy of its binary
  representation, under both predicate forms and for both sets and maps."
- **Problem**: In isolation, contribution 3 reads as if achieving the bound is
  the new result. The discussion correctly notes Pagh-Pagh-Rao (2005) already
  achieves the bound with polynomial construction, while the BHF fixed-threshold
  construction is exponential. The honest novelty is (a) a *maximum-entropy*
  encoder that meets the bound, valuable for obliviousness, and (b) the adaptive
  trade-off and the price-of-certainty characterization. The intro should carry
  that nuance so the reader is not misled before Section 9.
- **Suggestion**: Reword contribution 3 to foreground the maximum-entropy
  property and the adaptive trade-off, and add one clause crediting Pagh-Pagh-Rao
  for efficient achievability. Consider shifting the title/abstract emphasis from
  "optimal" (known) toward the adaptive construction (new).
- **Cross-verified**: Yes, by area chair against the prose-auditor's note that
  the abstract was already simplified. This is a framing problem, not hidden weak
  novelty: the underlying adaptive contribution is real (novelty-assessor rates
  it High/High), so the fix is rewording, not new work. No disagreement.

### M3. Missing closest map prior art: Bloomier filter and Dietzfelbinger-Pagh retrieval (source: citation-verifier, novelty-assessor)
- **Location**: `sections/discussion.tex` comparison subsection (lines 25-84);
  `references.bib`.
- **Problem**: The paper's contribution 1 is a unified *map* construction, yet
  the comparison cites only membership filters (Bloom, cuckoo, XOR, ribbon,
  Pagh-Pagh-Rao) and the author's own PHF/PMF. The canonical approximate-map
  structure, the Bloomier filter (Chazelle, Kilian, Rubinfeld & Tal 2004), and
  the closest retrieval theory (Dietzfelbinger & Pagh 2008) are absent. For a
  paper claiming a unified optimal map, these are expected comparisons.
- **Suggestion**: Add both references and a short paragraph contrasting the BHF
  map (value bits folded into the same hashed evidence that certifies
  membership) with the Bloomier filter (value stored in a separate spine) and
  retrieval structures. This sharpens the unification claim rather than diluting
  it.
- **Cross-verified**: Yes; both citation-verifier and novelty-assessor
  independently identify this gap. No disagreement.

## Minor Issues

### m1. Incorrect closed form for E[log2 Q] in the space proof (source: logic-checker)
- **Location**: `sections/space.tex`, Thm `thm:space`, lines 65-68.
- **Quoted text**: "Since `Q ~ Geom(p)`, `E[log2 Q] = -log2 p - (log2 e)(1-p)
  log(1-p)/p -> -log2 p` as `p -> 0`".
- **Problem**: E[log2 Q] has no elementary closed form, and the stated equality
  is numerically false (verified: at p in {0.5, 0.3, 0.1, 0.05} the printed
  expression diverges from the true E[log2 Q] by a growing margin). The proof
  needs only `E[log2 Q] = -log2 p + O(1)`, which is true, so the theorem stands.
- **Suggestion**: Replace the false identity with the bound actually used, or
  cite the exact `E[L] = sum_{n>=1} q^{2^n-1}` from Thm `thm:expected_size`
  (verified to equal E[floor log2 Q] exactly) and bound it.

### m2. Incorrect entropy closed form in Remark `rem:info_interp` (source: logic-checker)
- **Location**: `sections/space.tex`, Remark `rem:info_interp`, lines 255-261.
- **Quoted text**: "`H(Q) = [-log2 p + (1-p)log2(1-p)/p] = -log2 p + O(1)`".
- **Problem**: This is not the geometric entropy; the correct value is
  `H(Q) = [-(1-p)log2(1-p) - p log2 p]/p` (the first term also carries 1/p). At
  p = 0.1 the two differ (true 4.690 vs printed 1.954). The asymptotic claim
  `H(Q) = -log2 p + O(1)` is correct (verified: H(Q) + log2 p -> log2 e), so the
  remark's conclusion holds.
- **Suggestion**: Use the correct closed form or drop to the O(1) statement.

### m3. Stray `\phantom{x}` empty denominator (source: prose-auditor)
- **Location**: `sections/space.tex`, the displayed `H(Q)` equation in
  `rem:info_interp`.
- **Problem**: `\frac{...}{\phantom{x}}` renders a fraction bar over blank space,
  an editing artifact. (Same equation as m2.)
- **Suggestion**: Remove the `\frac{}{\phantom{x}}` wrapper.

### m4. FNR search complexity for the equality predicate is overstated (source: logic-checker)
- **Location**: `sections/shf.tex`, Thm `thm:fnr_search` (lines 129-152) and the
  following remark (lines 154-162).
- **Problem**: The `O(C(m,p)*m)` bound is immediately undercut by the adjacent
  remark conceding a hash-and-count `O(m)` approach. The theorem reads as an
  overstatement of the threshold predicate's advantage.
- **Suggestion**: Fold the remark into the theorem: state the bound is for the
  subset-enumeration algorithm of Alg. 1 and note the achievable O(m) variant.

### m5. Random oracle definition independence wording (source: logic-checker, citation-verifier)
- **Location**: `sections/prelim.tex`, Def. `def:randomoracle`, lines 31-38.
- **Problem**: Now says "independent and uniformly distributed" (improved), but
  the qualifier "over its range for every distinct input" is slightly ambiguous
  about whether independence is across inputs or across prefix bits.
- **Suggestion**: "...whose outputs on distinct inputs are mutually independent,
  each uniformly distributed over the range." Optionally cite Bellare-Rogaway.

### m6. Cardinality estimator lacks properties; map sign is a readability hazard (source: methodology-auditor)
- **Location**: `sections/entropy.tex`, lines 71-77.
- **Quoted text**: "`m_hat = -BL(S~)/log2(eps)` ... replace `log2 eps` with
  `log2 eps - mu` ... (both terms are negative, so `m_hat` remains positive)".
- **Problem**: No bias/variance/consistency given for this length-based
  estimator (the finite-universe estimator in Sec. 7 *is* shown unbiased). The
  parenthetical now clarifies the sign, but the bare substitution still reads as
  a sign hazard.
- **Suggestion**: Write `m_hat = BL(S~)/(log2(1/eps) + mu)` (all positive) and
  add one line on consistency or label it heuristic.

### m7. Within-length salt enumeration vs the entropy proof's randomization (source: methodology-auditor)
- **Location**: `sections/construction.tex`, Algs 1-2 (`for j=1..2^n`) versus
  Thm 6.1 proof asserting the within-level order is randomized.
- **Problem**: The entropy proof's uniformity hypothesis needs the successful
  salt to be uniform within its length level, but the algorithm writes a
  deterministic loop. Reconcile so the hypothesis is visibly met.
- **Suggestion**: State in Algs 1-2 that within each length level salts are tried
  in uniformly random order (the text already says "without replacement").

### m8. Companion papers lack stable identifiers (source: citation-verifier, methodology-auditor)
- **Location**: `references.bib` (bernoulli_sets, bernoulli_maps,
  bernoulli_data_type, phf, pmf, oph, es).
- **Problem**: Seven entries are year-only `@article` with no venue/DOI/URL. The
  foundational ADT definitions trace to these unverifiable sources. The paper
  does restate the load-bearing definitions inline, which mitigates it.
- **Suggestion**: Add arXiv ids or repository URLs.

### m9. Two uncited bibliography entries (source: citation-verifier)
- **Location**: `references.bib`: `manning` and `oph`.
- **Problem**: Neither key appears in any `\cite` (verified by grep). Harmless to
  output under plainnat, but dead weight. `manning` was flagged in the prior
  pass; `oph` is newly unused.
- **Suggestion**: Cite where relevant (manning in the IR/encrypted-search
  framing; oph in the obliviousness lineage) or remove.

### m10. Duplicate PDF destinations for appendix equations A.1-A.4 (source: format-validator)
- **Location**: `main.log` pdfTeX warnings, from `thm:pmf_detailed`
  (`sections/appendix.tex`) re-displaying the salt PMF already shown in
  `thm:L_pmf` (`sections/entropy.tex`).
- **Quoted text (log)**: "destination with the same identifier
  (name{equation.A.1}) has been already used, duplicate ignored".
- **Problem**: Four appendix equations collide with earlier hyperref
  destinations, so their links point to the first occurrence. Cosmetic; warns on
  every build. Root cause: the appendix restates an identical PMF equation.
- **Suggestion**: In the appendix, reference `eq:L_pmf` rather than re-display
  it (removes both the duplication and the redundancy), or give unique labels, or
  set `hypertexnames=false`.

### m11. pgfplots factorials are a portability risk (source: format-validator)
- **Location**: `sections/shf.tex`, Fig. `fig:adaptive_fpr` (`50!/(4!*45!)`,
  `ln(200!)`).
- **Problem**: Builds cleanly here (0 errors), but explicit factorials near
  pgfmath's range may fail on stricter/older TeX distributions, a risk for an
  external venue's build pipeline.
- **Suggestion**: Use the log-gamma form uniformly for all four curves (the
  m=200 curve already does).

## Suggestions

1. **Add a minimal empirical appendix** (cross-ref methodology-auditor MAJOR-1):
   measured salt-length PMF vs Thm 6.2, adaptive FPR histogram vs Beta(p,m-p+1),
   and construction time vs m. The `code/` and `data/` directories already exist.
   This is cheap and would convert the explicit "practical" claims from asserted
   to demonstrated. (Note: theory-only status is accepted per the area chair;
   this is an upgrade, not a blocker.)
2. **Add a notation table and a small running example** (m=3, eps=0.25, N=4)
   carried from construction through the space and adaptive analyses. The deleted
   `fig_shs` figure apparently illustrated exactly this; a refreshed version
   would aid accessibility. (source: prose-auditor)

## Detailed Notes by Domain

### Logic and Proofs
The proof spine is sound and much improved. The three prior critical defects are
gone; the order-statistic PMF normalizes (verified for four parameter triples),
the exact salt-length identity matches simulation, and the space and price-of-
certainty results are correct. The two residual math items (m1, m2) are false
*printed identities* whose O(1) consequences are nonetheless correct, so they do
not break any theorem; they should be corrected for rigor. The one substantive
logic gap is the adaptive-map salt (M1), which is an algorithm/lookup
inconsistency rather than a flawed proof. The adaptive-not-max-entropy remark is
a careful, correct clarification.

### Novelty and Contribution
Appropriate novelty for a family application paper. The adaptive threshold and
the price-of-certainty theorem are High/High; the threshold predicate is a
useful Medium; the unified construction is a clean but Low-novelty organizing
principle; exact-bound achievability is known (Pagh-Pagh-Rao), so the optimality
contribution's novelty is its maximum-entropy character. The needed fixes are
framing (M2) and related-work positioning (M3), not new research. Building on
`bernoulli_sets`/`bernoulli_entropy` is the paper's declared role and is not a
novelty deficit.

### Methodology
Theory-only (accepted). Algorithms are precise; assumptions explicit; build
clean. The gaps are the absence of empirical support for explicit practicality
claims (MAJOR-1), the adaptive-map salt inconsistency (cross-filed M1), and
unpublished foundations. Reproducibility of the BHF-specific results is good
modulo the companion-paper identifiers.

### Writing and Presentation
At or near submission quality. The prior pass's two worst prose defects ("Wait"
and "an BHF") are eliminated. Remaining items are polish: thin Sections 7-8, a
stray `\phantom{x}`, an optional em-dash in the abstract, and the suggested
notation table / running example.

### Citations and References
Bibliography integrity is good (16 entries, all cited keys resolve, no build
warnings). Carter et al. and the modern filters are now cited (prior majors
resolved). Open items: the Bloomier filter and Dietzfelbinger-Pagh (M3),
self-citation identifiers (m8), two uncited entries (m9), and optional
Bellare-Rogaway / discrete-order-statistics references.

### Formatting and Production
Builds to 27 pages with 0 overfull boxes and no undefined references. gloss.tex
and the dangling figure are removed. Open items are cosmetic: duplicate appendix
equation destinations (m10), the pgfplots factorial portability risk (m11), and
optional visible hyperlinks.

## Literature Context Summary

The paper sits in space-efficient approximate membership and retrieval. The
-log2(eps) lower bound is Carter et al. (1978) (now cited); efficient
achievability is Pagh-Pagh-Rao (2005) (now cited); practical filters (cuckoo,
XOR, ribbon, binary fuse) sit 8-44% above the bound with O(n) construction (now
cited except binary fuse and the Bloomier filter). The BHF fixed-threshold
variant hits the bound exactly but with exponential construction, making it a
theoretical achievability statement distinguished mainly by its maximum-entropy
property. The adaptive variant (p-th order statistic as a data-dependent
threshold, Beta-distributed FPR, vanishing space) has no direct prior-art
analogue and, with the price-of-certainty theorem, is the paper's strongest
original contribution. The chief remaining literature gap is the absence of the
canonical approximate-map structure (Bloomier filter) and retrieval theory
(Dietzfelbinger-Pagh), notable because the unified map is contribution 1.

## Prior-Review Reconciliation (2026-02-26 -> 2026-05-29)

| Prior finding | Severity | Status now |
|---|---|---|
| C1 Taylor expansion error in space proof | Critical | RESOLVED (Jensen + floor bound; verified) |
| C2 "Wait---" / wrong appendix PMF derivation | Critical | RESOLVED (clean derivation; PMF normalizes) |
| C3 Value hash unsalted in Algs 1-2 | Critical | RESOLVED for fixed-threshold; adaptive-map analogue remains (M1) |
| M1 Missing Carter et al. (1978) | Major | RESOLVED (cited at both lower bounds) |
| M2 Missing modern filters / Pagh | Major | RESOLVED (Pagh, cuckoo, XOR, ribbon cited) |
| M3 Bloom space formula wrong | Major | RESOLVED (now log2(e)*log2(1/eps)) |
| M4 Remark 5.5 informal lower-bound argument | Major | RESOLVED (formal; price-of-certainty Thm added) |
| M5 Companions lack identifiers | Major | OPEN (downgraded to m8; inline restatements mitigate) |
| M6 "an BHF" article error | Major | RESOLVED (none in sources) |
| M7 gloss.tex dead code | Major | RESOLVED (removed) |
| M8 Sections 7/8 too thin | Major | OPEN (downgraded to m, prose) |
| m1-m10 (various) | Minor | Mostly resolved (Bloom formula, fig_shs, abstract, salt term); a few persist |
| Empirical validation absent | Major (methodology) | OPEN (MAJOR-1 methodology; theory-only accepted) |

Net: 3 of 3 criticals resolved; 5 of 8 majors resolved, 3 carried forward at
reduced or equal severity; no regressions introduced. One genuinely new major
(M1 adaptive-map salt) surfaced because the C3 fix was not propagated to the
adaptive path.

## Review Metadata
- Agents used: literature scouts (broad + targeted), logic-checker,
  novelty-assessor, methodology-auditor, prose-auditor, citation-verifier,
  format-validator. In this environment the area chair executed each
  specialist's analysis directly (no Task dispatch available) and ran the build
  plus numerical verification.
- Build verification: `make` succeeds, 27 pages, 0 overfull boxes, no undefined
  refs/citations.
- Numerical verification performed: order-statistic PMF normalization (4 cases),
  exact salt-length identity vs simulation, geometric E[log2 Q] and H(Q)
  asymptotics, adaptive Beta moments.
- Cross-verifications performed: 3 (M1 logic-checker <-> methodology-auditor and
  area-chair read of the live algorithm; M2 novelty <-> prose framing; M3
  citation-verifier <-> novelty-assessor).
- Disagreements noted: 0.
- Hallucination check: all critical/major quoted text re-verified against the
  manuscript by the area chair; no discarded findings.
