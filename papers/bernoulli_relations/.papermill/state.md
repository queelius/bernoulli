---
title: "The abstract data type of the approximate relation"
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

related_papers:
  - path: "~/github/bernoulli/papers/bernoulli_sets"
    rel: "extends"
    label: "Foundation paper: Bernoulli set model"
  - path: "~/github/bernoulli/papers/bernoulli_maps"
    rel: "companion"
    label: "Sibling extension paper (maps); relations generalize maps to multi-attribute"
---

## Notes

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
