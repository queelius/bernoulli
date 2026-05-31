# Methodology Auditor Report

**Paper:** The Bernoulli Hash Function
**Date:** 2026-05-29

## Overall Assessment

This is a theory-only paper: definitions, algorithms, and proofs, with no
implementation or experiments (a known, accepted state per the area chair). The
methodology is the construction-plus-analysis pattern, and it is generally
well-executed. The five algorithms are precisely specified. Since 2026-02-26,
the prior methodological critical (value hash not salted in Algs 1-2) is fixed
for the fixed-threshold path. The reproducibility picture is improved by the
expanded external bibliography, though the foundational definitions still rest
on unpublished companion papers.

Two methodological issues remain worth raising: the absence of even a minimal
empirical sanity check for claims that are explicitly framed as *practical*
(the adaptive threshold and "feasible for small m"), and a residual algorithmic
inconsistency in the adaptive *map* path (cross-filed with logic-checker).

## Findings

### MAJOR-1: Claims of practicality are unsupported by any experiment
- **Location:** `sections/discussion.tex`, "Practical considerations" (lines
  86-101), esp. item 3 ("for very small sets (m <= 10), the construction is
  feasible") and item 4 ("The adaptive threshold variant is practical for *any*
  set size ... O(m log m)"); and `sections/shf.tex` Fig. `fig:adaptive_fpr`
  (claimed concentration of the FPR).
- **Problem:** The paper makes concrete operational claims (construction is
  feasible for small m; the adaptive variant is practical at any size; the FPR
  concentrates around p/(m+1) with variance O(1/m)) but provides no empirical
  evidence. These are exactly the claims a small experiment would either confirm
  or qualify, and they are cheap to produce: the adaptive set construction is
  O(m log m) and trivially implementable. A reviewer at a top venue will expect
  at least a figure validating the predicted salt-length PMF (Thm 6.2) and the
  Beta-distributed adaptive FPR (Thm 3.7) against simulation.
- **Suggestion:** Add a short empirical subsection or appendix with three
  micro-experiments under a concrete hash (e.g. SHA-256 truncated): (a) measured
  salt length vs the PMF `q^{2^n-1}(1 - q^{2^n})` for small m and a few eps;
  (b) measured adaptive FPR histogram vs Beta(p, m-p+1) for a couple of (m,p);
  (c) wall-clock construction time vs m for the fixed-threshold predicate to
  substantiate the "feasible for m <= 10" claim and show where it breaks down.
  The repository already has `code/` and `data/` directories, so the harness
  location is established.
- **Severity:** Major. The theoretical results stand without experiments, but
  the *practicality* claims do not, and the paper makes them explicitly.

### MAJOR-2 (cross-filed with logic-checker MAJOR-1): Adaptive map stores no salt
yet the lookup needs one
- **Location:** `sections/construction.tex`, Alg. `alg:make_shf_adaptive`
  (map branch, lines 137-161; output `(N, t)`) versus `Find` (line 225).
- **Problem:** The adaptive map construction searches for a salt `b` with >= p
  value-matching keys (line 146, `h(1 || x_i || b)`), but returns only `(N, t)`.
  `Find` requires `b` to recover the value. The set path is fine (`b = eps`);
  the map path is not. This is the adaptive-path analogue of the prior C3 that
  was fixed only for the fixed-threshold algorithms.
- **Suggestion:** Store `(N, t, b)` for the adaptive map; update the algorithm
  output, the `Find` precondition, the comparison table's "Stored params" row
  (currently `(N, t)`), and the adaptive-map space note in `sec:adaptive_space`.
- **Severity:** Major (single underlying defect, counted once in synthesis).

### MINOR-1: Companion papers remain unpublished; foundational results not self-
contained
- **Location:** `references.bib` (bernoulli_sets, bernoulli_maps,
  bernoulli_data_type, phf, pmf, oph, es) and `sections/prob_model.tex`,
  `sections/operations.tex`, which cite the companions for full derivations.
- **Problem:** The Bernoulli set/map definitions, the FP/FN distributions
  (Sec. 7), and the algebraic background (Sec. 8) are imported from companions
  with no stable identifier (year-only `@article`, `note = {Companion paper}`).
  A referee cannot verify the foundations independently. This is unchanged from
  the prior pass, though the paper does restate the essential definitions inline
  (Defs 2.3, 2.5), which mitigates it for the parts the proofs actually use.
- **Suggestion:** Post the companions (arXiv or institutional) and add
  identifiers/URLs. For a self-contained submission, also give a one-line proof
  or citation for the FP/FN binomial distributions in Sec. 7 (they are
  elementary given the axioms).
- **Severity:** Minor (reproducibility of *foundations*; the BHF-specific
  results are self-contained modulo this).

### MINOR-2: Cardinality estimator stated without bias/variance and with a sign
description that is easy to misread
- **Location:** `sections/entropy.tex`, lines 71-77.
- **Quoted text:** "the method-of-moments estimator of the cardinality is
  `m_hat = -BL(S~) / log2(eps)` ... For maps, replace `log2 eps` with
  `log2 eps - mu` in the denominator (both terms are negative, so `m_hat`
  remains positive)."
- **Problem:** The estimator is asserted with no properties (the finite-universe
  estimator in Sec. 7, `m_hat = (|S~| - eps*u)/(1 - eps - fnr)`, *is* shown
  unbiased, but this length-based one is not). The map correction is now
  *parenthetically* explained ("both terms are negative"), which is an
  improvement over the prior draft, but the bare substitution
  "`log2 eps` -> `log2 eps - mu`" still reads as a sign hazard: the intended
  denominator is `log2(eps) - mu < 0`, giving `m_hat = -BL/(log2 eps - mu)`. It
  would be clearer written with explicit positive quantities.
- **Suggestion:** Write `m_hat = BL(S~) / (log2(1/eps) + mu)` for maps (all
  quantities positive), and add one line on consistency (BL concentrates, so
  m_hat is consistent) or label it heuristic.
- **Severity:** Minor.

### MINOR-3: Exhaustive within-length salt enumeration vs random sampling not
justified
- **Location:** `sections/construction.tex`, Algs 1-2 (the `for n; for j=1..2^n`
  enumeration) and `sections/entropy.tex` Thm 6.1 proof ("the search order is
  randomized within each length level").
- **Problem:** The constructions enumerate all `2^n` salts of length `n` before
  length `n+1`. The max-entropy proof relies on the successful salt being uniform
  within its length level, which requires the *randomized* within-level order
  asserted in Sec. 6 but written as a deterministic `j = 1..2^n` loop in Sec. 4.
  The two should be reconciled so the entropy argument's hypothesis is visibly
  satisfied by the stated algorithm.
- **Suggestion:** State in Alg 1-2 that within each length level salts are tried
  in a uniformly random order (or sampled without replacement, which the text
  says), so Thm 6.1's uniformity hypothesis is met by construction.
- **Severity:** Minor.

## Reproducibility Assessment

| Dimension | Status | Note |
|---|---|---|
| Algorithms | GOOD | 5 algorithms, complete pseudocode |
| Assumptions | GOOD | Random oracle assumption explicit (Asm 2.1) |
| Parameters | GOOD | m, eps, fnr, mu, N, t, p all defined |
| Proofs | FAIR/GOOD | Self-contained modulo companions; key proofs verifiable |
| Empirical validation | POOR | None; practicality claims unsupported |
| Companion availability | POOR | Unpublished, no identifiers |
| Build | GOOD | `make` succeeds, 27 pp, 0 overfull boxes |

## Note on Prior Pass

Prior methodology MAJOR-3 (Alg 1 value hash unsalted) is RESOLVED for Algs 1-2.
Prior MINOR on the cardinality estimator sign is PARTIALLY addressed (now has a
parenthetical). The empirical-validation gap (prior MAJOR-1) is UNCHANGED.
