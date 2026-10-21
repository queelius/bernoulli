---
title: "Entropy and space complexity of random approximate sets"
stage: drafting
format: latex
authors:
  - name: "Alexander Towell"
    email: "lex@metafunctor.com"
    orcid: "0000-0001-6443-9897"

thesis:
  claim: ""
  novelty: ""
  refined: null

prior_art:
  last_survey: null
  key_references: []
  gaps: ""

experiments: []

venue:
  target: null
  candidates: []

review_history:
  - date: "2026-05-29"
    type: "multi-agent-review"
    findings_critical: 0
    findings_major: 6
    findings_minor: 10
    findings_suggestions: 7
    recommendation: "minor-revision"
    notes: >-
      Both proofs correct, build clean (6 pp). Major items are editorial: the
      Yao minimax step that upgrades the bound to randomized structures is
      uncited (Yao 1977 absent); Pagh-Pagh-Rao (2005), the canonical "Bloom is
      not optimal" reference, is a missing must-cite; Sections 3 and 4 use
      opposite, unreconciled asymptotic regimes (constant density vs fixed set
      size); the lower bound is phrased as exact when it holds only up to o(1);
      the novel joint-entropy result is computed but unmotivated.
    report_path: ".papermill/reviews/2026-05-29/review.md"

related_papers:
  - path: "~/github/bernoulli/papers/bernoulli_sets"
    rel: "extends"
    label: "Foundation paper: axioms, distributions, composition theorem"
  - path: "~/github/bernoulli/papers/bernoulli-hash-function"
    rel: "extended-by"
    label: "BHF achieves the information-theoretic space bound derived here"
---

## Notes

Initialized by papermill on 2026-05-29.

### Discovered structure
- Format: latex, build `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- Notation: `alex.sty` (unified, `[fancy,section]`)
- Sections (5, via `\input{}`): intro, preliminaries, entropy, space_complexity, conclusion
- Bibliography: `references.bib`, 8 entries (minimal)
- Built PDF: ~6 pages (shortest in the family)
- Supporting assets: none

### Thesis (working, from collection state / cross-paper topic placement)
Information-theoretic properties of approximate sets: joint entropy of false-positive and
false-negative error counts, and the space-complexity lower bound bits/element =
-log2(alpha) + mu (the space-accuracy duality). Establishes Bloom-filter efficiency as a
corollary. The thesis YAML block is left empty for `papermill:thesis` to populate.

### Related Work and Software
Companion to `bernoulli_sets/`; one of the core 4-paper family. The space bound derived here
is the target achieved by the Bernoulli Hash Function (`bernoulli-hash-function/`). Reference
implementation: `bernoulli-cpp/entropy_bloom_filter.hpp`. NOTE: short paper (6 pp), so the
reviewer should weigh completeness/sufficiency of the space-complexity argument carefully.

### Freeze (2026-10-21)
Final preprint version, superseded by monograph Chapter 8 ("Information-Theoretic
Bounds"). Added a "Status and errata (October 2026)" box (`status_errata.tex`,
input after the abstract) and `ERRATA.md`. Main fix: the two-sided space bound is
no longer called open (Pagh and Rodler 2001, Prop. 1); the lower bound is stated
as asymptotic (minus o(1)); the randomized extension is credited to Yao 1977.
Build clean (0 errors, 0 undefined refs/cites), 8 pages. No further revisions planned;
the June 2026 "minor-revision" verdict above is superseded.
