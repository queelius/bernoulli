---
title: Error contracts for approximate relations
stage: drafting
format: latex
authors:
- name: Alexander Richard Towell
  email: lex@metafunctor.com
  orcid: 0000-0001-6443-9897
thesis:
  claim: A relation approximation needs explicit construction randomness and source identity. Monotone
    boundary certificates give truth-uniform one-sided query contracts; a tractable binary-witness
    class supports calibration of symmetry-preserving stored filters. Independent-tuple operator
    and invariant formulas are scoped special cases.
  novelty: Unestablished. Lineage, dissociation, certificate/sensitivity identities, graph inference,
    and canonical representatives are established. This draft is a rigorous synthesis and one reproducible
    stored-filter calibration study. A substantial original research contribution has not yet been
    demonstrated.
  refined: true
prior_art:
  last_survey: '2026-10-13'
  key_references:
  - 'Green, Karvounarakis, Tannen (2007): provenance semirings'
  - 'Dalvi and Suciu (2012): probabilistic query inference dichotomy'
  - 'Gatterbauer and Suciu (2014): sound dissociation bounds'
  - 'Flesca, Furfaro, Parisi: probabilistic databases under integrity constraints'
  - 'Blanc et al. (2022), Gopalan et al. (2016): sensitivity/certificates and noise'
  - 'Dietzfelbinger and Pagh (2008): retrieval and approximate membership'
  - 'Barthe et al. (2016), Li et al. (2023): union bounds and conditional independence'
  gaps: The prior categorical claim that probabilistic databases do not study constraints is withdrawn.
    The exact one-sided query-calibration formulation was not located, but its elementary derivation
    does not establish originality. See the verified literature ledger and relations-revision assessment.
experiments:
- id: mc-validation
  kind: ideal-independent-coin validation
  script: code/validate.py
  status: passing
  notes: Corrected diagonal, row-preservation, and source-covariance cases; 486 exact/numerical unit
    tests and 2,000,000-trial CLI validation. Does not validate a physical filter model.
- id: stored-filter-calibration
  kind: stored partitioned Bloom experiment
  script: code/filter_calibration.py
  status: passing
  notes: 160 accepted builds per method, 128 disjoint bundles for each of three 12-cycle profiles.
    Source-conditioned ideal hash guarantees; BLAKE2b measurements. Query-calibrated canonical/ordered
    payloads 3752/8482 bytes. Exact rational audit checks all recorded conditional envelopes. General
    float screening alone is not a certificate.
venue:
  target: null
  decided: null
  candidates:
  - name: Information Systems
    tier: conditional fit
    fit: Relevant to relational data representation and evaluation, if a defensible original method
      or substantial empirical contribution is developed. Current draft is not submission-ready.
  - name: Journal of Logical and Algebraic Methods in Programming
    tier: conditional alternative
    fit: Potential fit if extended into a formal contract system with a significant new result and
      adequate comparison; not justified by repackaging known probability laws.
  strategy: Keep this as a working draft. Establish incremental value beyond canonicalization and
    conservative certificate bounds before selecting a venue. Do not submit or publish externally
    without user instruction.
  historical_note: Earlier June 2026 Information Systems readiness recommendations are superseded.
    The previous state recorded a Zenodo concept identifier 10.5281/zenodo.20602265; its public status
    was not re-audited in this revision.
review_history:
- date: '2026-05-29'
  type: multi-agent-review
  findings_critical: 5
  findings_major: 14
  findings_minor: 13
  findings_suggestions: 6
  recommendation: not-ready
  notes: 'Build is doubly broken. Five subfiled section files (intro, rel_algebra, test, unused/optimality,
    unused/oblivious_rel_model) do NOT exist, so pdflatex aborts at the intro before bibtex ever
    runs; and there is no references.bib, so bibtex would fail too. Logic errors: def:approx_pfun
    conditions an event on its own negation; the rate-argument order is inconsistent across sections;
    the equality-predicate formula carries a spurious -tau1 tau2 omega1 omega2 term (should be the
    plain sum). Several proofs are unfinished (one body is literally "?"). The genuine novel core
    (join/project error propagation, invariant preservation) is real but the least developed and
    partly duplicates the sibling maps and composition papers.'
  report_path: .papermill/reviews/2026-05-29/review.md
- date: '2026-06-09'
  type: multi-agent-review
  findings_critical: 0
  findings_major: 5
  findings_minor: 9
  findings_suggestions: 4
  recommendation: minor-revision (Zenodo/IS-journal); major-revision (ICDT/PODS)
  notes: 'Full editorial pass on the salvaged draft. Build production-clean (21 pp, 0 undefined refs/cites,
    0 warnings, 0 overfull boxes); validate.py passes 23/23 fit rows (worst abs err 0.000686); all
    11 closed forms independently re-derived incl. the harness-skipped thm:symmetric_preservation
    and the covariance form. Zero critical, zero major LOGIC findings: every proof is correct. The
    5 majors are positioning/structure: (1) marginal operator rates may be tuple-independent-PDB-recoverable
    [verify]; (2) projection 1-(1-eps)^k is a known OR-of-filters identity presented as new [verify];
    (3) load-bearing asm:ber_trial wording is garbled; (4) Section 2 mis-titled "Relational algebra"
    (it is preliminaries); (5) partial-function ADT mis-nested under invariants. Differentiated core
    (thm:join_dependence joint-law correlation + invariant preservation/closure) is real and validated.
    DB-theory-venue verdict: READY as Zenodo preprint; minor-revision for an IS journal; major-revision
    and a stretch for ICDT/PODS (lacks a complexity/lower-bound/dichotomy result). External prior-art
    [verify] items (Bloomjoin dependence; independent-tuple PDB marginals; AQP; searchable encryption)
    handed to the area chair, who has web access. Bib clean except one duplicate entry (aset = bernoulliSets).'
  report_path: .papermill/reviews/2026-06-09/review.md
- date: 2026-06-09-rereview
  type: focused-rereview
  findings_critical: 0
  findings_major: 0
  findings_minor: 4
  findings_suggestions: 3
  recommendation: minor-revision (IS-journal/Zenodo); major-revision-but-now-reachable (EDBT/ICDT)
  notes: 'Focused re-review of the post-2026-06-09 changes. All five prior majors RESOLVED (framing
    concession crediting suciu2011 for the join/lineage correlation and disclaiming the marginal
    rates; asm:ber_trial restated; Section 2 retitled; ADT promoted to top-level Section 6; duplicate
    bib entry merged). The KEY addition is new Section 5.5 "A closure dichotomy" (thm:local_closure:
    monotone local invariant with orbit size m admits a one-pass OR-closure at FPR 1-(1-eps)^m, TPR
    1-(1-tau)^m, |A|-independent; cor:invariant_space_cost: +log2 m bits/element via the entropy
    duality; thm:transitivity_cascade: path closure needs ceil(log2 k) passes and Theta(k^2) pairs,
    no bounded closure). Build regression-clean (22 pp, 0 undefined/collision/warning/overfull; new
    labels 5.5 / 5.5.1 / 5.6 unique). Orchestrator independently re-verified ceil(log2 k) and C(k+1,2)
    for k=1..64 and the o(1) surcharge algebra. VERDICT: the dichotomy lifts the contribution from
    modest to solid; IS-journal effectively ready; EDBT/ICDT now reachable (it was a stretch before),
    gated on ONE external check. 4 minors: (1) cor:invariant_space_cost wording overclaims a lower
    bound (it is achievability only); (2) thm:local_closure proof should state the within-orbit-closedness
    it relies on; (3) shipped validate.py covers only the m=2 closure case, not general-m or the
    cascade; (4) carried prior MINOR-4/5 (symmetric-preservation + asymmetric-join harness gaps).
    3 [needs external verification] items handed to the area chair: is the local-vs-cascading closure
    dichotomy genuinely new vs database-repair / consistent-query-answering / integrity-constraint-maintenance?
    This single check determines the EDBT/ICDT verdict.'
  report_path: .papermill/reviews/2026-06-09-rereview/review.md
- date: '2026-10-13'
  type: mathematical audit, primary literature review, stored-filter study, independent review
  recommendation: working draft; original research submission not yet warranted
  notes: Supersedes June correctness/readiness conclusions. Repaired diagonal symmetry, single-valuedness,
    variable orbits, shared-source projection, transitivity scope, CLT semantics, partial functions
    and security overclaims. Added checked query contracts and physical filter calibration. Independent
    reviewer confirms main proofs but identifies tiny-rate numerical comparator cancellation, fixed
    with regression tests and a full rerun before final handoff. The 55.8% representation comparison
    is not evidence of a comparable gain over conservative contract sizing (only 16 bytes in this
    case).
  report_path: ../../.research/relations-revision/assessment.md
related_papers:
- path: ~/github/bernoulli/papers/bernoulli_sets
  rel: extends
  label: 'Foundation paper: Bernoulli set model'
- path: ~/github/bernoulli/papers/bernoulli_maps
  rel: companion
  label: Sibling extension paper (maps); relations generalize maps to multi-attribute
verification:
  date: '2026-10-13'
  pdf_pages: 27
  latex_warnings: 0
  overfull_boxes: 0
  research_tests_passed: 540
  combined_statement_branch_coverage_percent: 99.44903581267218
  recorded_calibrated_builds_exactly_audited: 320
  filter_source_sha256: 450db465c25a17d9d19dbd5b42641c339405f058e5897a635461ae2c19d236ed
  report: ../../.research/relations-revision/validation.md
---

## Notes

### 2026-10-13 current assessment

The paper is now **Error contracts for approximate relations**. The current
working draft corrects substantive mathematical scope errors and integrates
source semantics, truth-uniform query contracts, and a stored-filter study.
The previous claims that all proofs were correct and the paper was effectively
ready for Information Systems are historical and superseded. Novelty and
submission significance remain unestablished. Current evidence and follow-ups
are in the root `.research/relations-revision/` directory.

### 2026-06-08 salvage Phase D (historical; superseded by 2026-10-13)
Build is clean and the core is complete. The "KNOWN ISSUES" and "working thesis"
notes further down are historical (pre-salvage) and are kept only for provenance.

- **Build**: `TEXINPUTS=".:./sty:" pdflatex -shell-escape main.tex && bibtex main`
  then two more `pdflatex` passes. Status: 21 pages, 0 undefined references,
  0 LaTeX warnings, 0 duplicate-destination warnings (added
  `hypertexnames=false` to the hypersetup to clear the subfiles+hyperref
  duplicate anchors), one negligible 3.31pt overfull box (sub-character,
  pre-existing).
- **Sections on disk** (6, all built): intro, relations, approx_rel_model,
  rel_algebra, properties, oblivious_rel_model. `predicates.tex`, `test.tex`,
  and `constrained_ras.tex` were deleted as superseded/orphaned; there is no
  `unused/` directory.
- **Phase D additions**: `code/validate.py` (Monte Carlo harness validating the
  Phase-C results; all fit rows agree to 3-4 digits, the join independence
  failure is demonstrated); an "Empirical validation" subsection with a results
  table in `rel_algebra.tex`; a pgfplots fan-in figure (`fig:proj_fpr`)
  referenced from the projection theorem; a rehabbed trapdoor-database
  application (cipher relation, rank-ordered encrypted search, threat/leakage
  model) in `oblivious_rel_model.tex`; a typo and grammar sweep.
- **Thesis and venue**: now filled in the YAML frontmatter above.
- **Not yet done**: external prior-art survey (papermill:prior-art), a full
  editorial review pass on the salvaged draft.

---

Initialized by papermill on 2026-05-29.

### Discovered structure
- Format: latex, build `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- Notation: modular `sty/` packages
- Sections SUBFILED by main.tex (9): intro, relations, approx_rel_model, rel_algebra,
  properties, predicates, test, unused/optimality, unused/oblivious_rel_model
- Sections that ACTUALLY EXIST on disk (4): relations, approx_rel_model, properties,
  predicates. MISSING: intro.tex, rel_algebra.tex, test.tex, unused/optimality.tex,
  unused/oblivious_rel_model.tex (verified 2026-05-29).
- Bibliography: **MISSING**. `\bibliography{references}` is declared in main.tex but there is
  NO references.bib file.
- Built PDF: 15 pages (`main.pdf`; builds after the 2026-05-29 build-repair, see below)
- Supporting assets: none

### KNOWN ISSUES (build-blocking, verified 2026-05-29 review)
1. **Five subfiled section files do not exist** (intro, rel_algebra, test, and both unused/*).
   `pdflatex` aborts fatally at the missing `intro` before bibtex is reached. This is the
   PRIMARY blocker, more severe than the missing bib.
2. **No `references.bib`** (secondary blocker, masked by #1). Must be created for citations to
   resolve. Documented build command also omits `-shell-escape` despite minted.
Both are known, pre-existing gaps, not regressions.

### 2026-05-29 build-repair (now compiles to 15 pp)
The paper now builds. Changes:
- Lifted `\newcommand{\tsr}{\gamma}` from predicates.tex's subfile PREAMBLE (which the
  `subfiles` package ignores in the main build, so ~42 "Undefined control sequence" errors
  fired) into main.tex's preamble.
- Fixed the wrong subfile path `sections/unused/oblivious_rel_model` to
  `sections/oblivious_rel_model` (the file exists at the latter).
- Commented out the four never-written subfiles (intro, rel_algebra, test, unused/optimality)
  with TODO markers. THESE STILL NEED TO BE AUTHORED; the build excludes them only so the
  existing content compiles.
- Created `references.bib` (keys: aset, bf, phf, approxrel) and removed an empty `\cite{}`.
- Build command needs `TEXINPUTS=".:./sty:"` like the other modular-sty papers.
Remaining: 7 undefined `\cref`/`\ref` warnings point into the commented-out sections and will
resolve once those are written. The four existing content sections are unaffected.

### Thesis (working, from cross-paper topic placement)
Approximate relational algebra: the approximate relation as an abstract data type, relational
operators (join, project, select) with error propagation, and relational predicates over
multi-attribute Bernoulli relations. The thesis YAML block is left empty for
`papermill:thesis`.

### Related Work and Software
Extension paper building on `bernoulli_sets/`. Reference implementation:
`bernoulli-cpp/bernoulli_relation.hpp`.
