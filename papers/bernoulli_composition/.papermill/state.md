---
title: "Composition of Bernoulli sets"
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
    findings_major: 8
    findings_minor: 12
    findings_suggestions: 6
    recommendation: "major-revision"
    notes: >-
      Math verified correct (all formulas re-derived and Monte Carlo checked).
      Major-revision driven by rigor and positioning, not wrong results:
      union/intersection rates need the unknown overlap |A1 cap A2| but the
      always-available simplex-vertex worst-case bound is never carried out;
      Bloom (1970) and Broder-Mitzenmacher are invoked but uncited; three
      proofs have stated-but-unproven steps; cross-set independence (shared
      hash seeds give correlated errors) is never examined.
    report_path: ".papermill/reviews/2026-05-29/review.md"

related_papers:
  - path: "~/github/bernoulli/papers/bernoulli_sets"
    rel: "extends"
    label: "Foundation paper: axioms, distributions, higher-order composition theorem"
  - path: "~/github/bernoulli/papers/bernoulli_classification_measures"
    rel: "companion"
    label: "Sibling in the core 4-paper family (classification measures)"
  - path: "~/github/bernoulli/papers/bernoulli_entropy"
    rel: "companion"
    label: "Sibling in the core 4-paper family (entropy/space)"
---

## Notes

Initialized by papermill on 2026-05-29.

### Discovered structure
- Format: latex, build `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- Notation: `alex.sty` (unified, `[fancy,section]`)
- Sections (6, via `\input{}`): intro, preliminaries, set_theory, relational, uncertain_rates, conclusion
- Bibliography: `references.bib`, 6 entries (minimal, mostly companion refs)
- Built PDF: ~15 pages
- Supporting assets: none (text-only)

### Thesis (working, from collection state / cross-paper topic placement)
Derives the set-theoretic compositional algebra of Bernoulli sets: closed-form error
rates for complement, union, intersection, and set difference; monoidal structure under
union and intersection; exact relational predicates (subset, equality probabilities); and
interval arithmetic for uncertain rate parameters. The thesis YAML block is intentionally
left empty for the `papermill:thesis` skill to populate/refine.

### Related Work and Software
Companion to `bernoulli_sets/` (the primary paper, which supplies the axioms and error-count
distributions assumed here). One of the core 4-paper family: bernoulli_sets,
bernoulli_composition, bernoulli_classification_measures, bernoulli_entropy. Reference C++
implementation: `bernoulli-cpp/` (`bernoulli_set_expressions.hpp`).
