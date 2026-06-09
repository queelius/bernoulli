---
title: "The abstract data type of the approximate relation"
stage: drafting
format: latex
authors:
  - name: "Alexander Towell"
    email: "lex@metafunctor.com"
    orcid: "0000-0001-6443-9897"

thesis:
  claim: >-
    An approximate relation is a Bernoulli random approximate set over the tuple
    universe, so the set model's per-tuple false-positive and true-positive rates
    transfer wholesale to relations. From that footing the relational operators
    have closed-form error propagation: selection is rate-transparent; projection
    amplifies the false-positive rate to 1-(1-eps)^k in the fan-in k and raises
    the model order while preserving element-wise independence; and a join does
    NOT preserve element-wise independence (output tuples sharing an input
    component are positively correlated by the factor 1/a, so a query result that
    assumes independent rows understates the joint error). Structural invariants
    (reflexivity, symmetry, single-valuedness, transitivity) survive approximation
    only with probability tending to zero as the universe grows, with the
    symmetric closure as the cheap deterministic repair at a doubled rate cost.
  novelty: >-
    Operator-level and invariant-level error propagation for approximate
    relations: in particular the join independence-failure correlation and the
    projection fan-in amplification, plus the per-invariant preservation rates.
    Distinct from probabilistic/uncertain databases (Trio, MayBMS), which model
    uncertainty IN THE DATA; here an objective base relation is exact and the
    error is injected by a space-saving representation of it.
  refined: true

prior_art:
  last_survey: null
  key_references:
    - "Towell, Bernoulli Sets (foundation)"
    - "Towell, Composition of Bernoulli Sets (intersection/union/subset/equality rates)"
    - "Towell, The Algebra of the Random Approximate Map Model (map composition)"
    - "Towell, The Perfect Hash Filter (the cipher-relation construction)"
    - "Suciu et al., Probabilistic Databases; Widom (Trio); Huang et al. (MayBMS)"
  gaps: >-
    The probabilistic-database literature does not ask whether an approximated
    invariant survives, nor how a projection's fan-in amplifies a structural FPR,
    because in that setting the relation has no underlying exact truth to be
    faithful to and no representation-induced error to propagate.

experiments:
  - id: "mc-validation"
    kind: "monte-carlo"
    script: "code/validate.py"
    status: "passing"
    notes: >-
      Validates the Phase-C results by direct per-tuple Bernoulli simulation
      (2e6 trials/estimate, eps=0.05, omega=0.10): projection FPR/TPR by fan-in,
      join FNR and the both-absent FPR corner, the join shared-component
      correlation (empirical P(both)=0.7288 matches the correlated model 0.729,
      NOT the independent 0.6561; factor 1/a=1.111 confirmed), symmetric closure
      FPR/TPR, reflexive tau^|A|, functional (1-eps)^(|Y|-1). All fit rows agree
      to 3-4 digits (worst abs error 0.000686).

venue:
  target: "Information Systems (Elsevier)"
  decided: "2026-06-09"
  candidates:
    - name: "Information Systems (Elsevier)"
      tier: primary
      fit: "best match. Scope explicitly covers foundational data-management work from SIGMOD/PODS/VLDB/ICDE/ICDT/EDBT plus algorithms and data models, with no systems-implementation requirement. The post-review reframing (concede the marginal rates as standard probabilistic-DB extensional marginals, credit the shared-lineage correlation, pin the contribution on the invariant-preservation fidelity analysis) fits a foundations-of-approximate-relational-data paper."
    - name: "EDBT (conference)"
      tier: alternative
      fit: "the realistic conference route, more accessible than ICDT/PODS and within Information Systems' cited scope; faster and more visible in the DB community than a journal cycle."
    - name: "Information Processing Letters (Elsevier)"
      tier: backup-short
      fit: "the invariant-preservation rates (reflexive tau^|A|, symmetric closure, functional, transitive) are crisp, short, self-contained results that fit IPL's short-paper format; fast turnaround."
    - name: "ACM TODS"
      tier: stretch
      fit: "top DB journal, theory-friendly, but very selective; the join independence-failure is conceptually known probabilistic-DB territory, so only with a very strong framing."
    - name: "Zenodo preprint (Bernoulli type theory collection)"
      tier: default
      fit: "the family's default; the monograph is the primary publication and the focused papers are Zenodo preprints. Already minted (concept 10.5281/zenodo.20602265)."
  avoid:
    - name: "VLDB Journal"
      reason: "requires a systems component the pure-theory paper does not have."
    - name: "ICDT / PODS"
      reason: "top database-theory venues; the headline join result is conceptually the known probabilistic-DB shared-lineage correlation, so a stretch (per the 2026-06-09 review)."
  strategy: >
    Primary: Information Systems, framed as foundations of approximate-relational
    data, with the invariant-preservation analysis as the contribution and the
    probabilistic-DB concession up front. For speed or DB-community visibility,
    EDBT (conference) or IPL (short) are faster routes. The post-review reframing
    is a prerequisite for any of these; it pre-empts the known-PDB-territory
    objection.

review_history:
  - date: "2026-05-29"
    type: "multi-agent-review"
    findings_critical: 5
    findings_major: 14
    findings_minor: 13
    findings_suggestions: 6
    recommendation: "not-ready"
    notes: >-
      Build is doubly broken. Five subfiled section files (intro, rel_algebra,
      test, unused/optimality, unused/oblivious_rel_model) do NOT exist, so
      pdflatex aborts at the intro before bibtex ever runs; and there is no
      references.bib, so bibtex would fail too. Logic errors: def:approx_pfun
      conditions an event on its own negation; the rate-argument order is
      inconsistent across sections; the equality-predicate formula carries a
      spurious -tau1 tau2 omega1 omega2 term (should be the plain sum). Several
      proofs are unfinished (one body is literally "?"). The genuine novel core
      (join/project error propagation, invariant preservation) is real but the
      least developed and partly duplicates the sibling maps and composition
      papers.
    report_path: ".papermill/reviews/2026-05-29/review.md"
  - date: "2026-06-09"
    type: "multi-agent-review"
    findings_critical: 0
    findings_major: 5
    findings_minor: 9
    findings_suggestions: 4
    recommendation: "minor-revision (Zenodo/IS-journal); major-revision (ICDT/PODS)"
    notes: >-
      Full editorial pass on the salvaged draft. Build production-clean (21 pp,
      0 undefined refs/cites, 0 warnings, 0 overfull boxes); validate.py passes
      23/23 fit rows (worst abs err 0.000686); all 11 closed forms independently
      re-derived incl. the harness-skipped thm:symmetric_preservation and the
      covariance form. Zero critical, zero major LOGIC findings: every proof is
      correct. The 5 majors are positioning/structure: (1) marginal operator
      rates may be tuple-independent-PDB-recoverable [verify]; (2) projection
      1-(1-eps)^k is a known OR-of-filters identity presented as new [verify];
      (3) load-bearing asm:ber_trial wording is garbled; (4) Section 2
      mis-titled "Relational algebra" (it is preliminaries); (5) partial-function
      ADT mis-nested under invariants. Differentiated core (thm:join_dependence
      joint-law correlation + invariant preservation/closure) is real and
      validated. DB-theory-venue verdict: READY as Zenodo preprint;
      minor-revision for an IS journal; major-revision and a stretch for
      ICDT/PODS (lacks a complexity/lower-bound/dichotomy result). External
      prior-art [verify] items (Bloomjoin dependence; independent-tuple PDB
      marginals; AQP; searchable encryption) handed to the area chair, who has
      web access. Bib clean except one duplicate entry (aset = bernoulliSets).
    report_path: ".papermill/reviews/2026-06-09/review.md"
  - date: "2026-06-09-rereview"
    type: "focused-rereview"
    findings_critical: 0
    findings_major: 0
    findings_minor: 4
    findings_suggestions: 3
    recommendation: "minor-revision (IS-journal/Zenodo); major-revision-but-now-reachable (EDBT/ICDT)"
    notes: >-
      Focused re-review of the post-2026-06-09 changes. All five prior majors
      RESOLVED (framing concession crediting suciu2011 for the join/lineage
      correlation and disclaiming the marginal rates; asm:ber_trial restated;
      Section 2 retitled; ADT promoted to top-level Section 6; duplicate bib
      entry merged). The KEY addition is new Section 5.5 "A closure dichotomy"
      (thm:local_closure: monotone local invariant with orbit size m admits a
      one-pass OR-closure at FPR 1-(1-eps)^m, TPR 1-(1-tau)^m, |A|-independent;
      cor:invariant_space_cost: +log2 m bits/element via the entropy duality;
      thm:transitivity_cascade: path closure needs ceil(log2 k) passes and
      Theta(k^2) pairs, no bounded closure). Build regression-clean (22 pp, 0
      undefined/collision/warning/overfull; new labels 5.5 / 5.5.1 / 5.6 unique).
      Orchestrator independently re-verified ceil(log2 k) and C(k+1,2) for
      k=1..64 and the o(1) surcharge algebra. VERDICT: the dichotomy lifts the
      contribution from modest to solid; IS-journal effectively ready; EDBT/ICDT
      now reachable (it was a stretch before), gated on ONE external check.
      4 minors: (1) cor:invariant_space_cost wording overclaims a lower bound
      (it is achievability only); (2) thm:local_closure proof should state the
      within-orbit-closedness it relies on; (3) shipped validate.py covers only
      the m=2 closure case, not general-m or the cascade; (4) carried prior
      MINOR-4/5 (symmetric-preservation + asymmetric-join harness gaps).
      3 [needs external verification] items handed to the area chair: is the
      local-vs-cascading closure dichotomy genuinely new vs database-repair /
      consistent-query-answering / integrity-constraint-maintenance? This single
      check determines the EDBT/ICDT verdict.
    report_path: ".papermill/reviews/2026-06-09-rereview/review.md"

related_papers:
  - path: "~/github/bernoulli/papers/bernoulli_sets"
    rel: "extends"
    label: "Foundation paper: Bernoulli set model"
  - path: "~/github/bernoulli/papers/bernoulli_maps"
    rel: "companion"
    label: "Sibling extension paper (maps); relations generalize maps to multi-attribute"
---

## Notes

### 2026-06-08 salvage Phase D (current status; supersedes the stale sections below)
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
