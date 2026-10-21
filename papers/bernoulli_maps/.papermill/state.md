---
title: "The algebra of the random approximate map model"
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
    findings_critical: 1
    findings_major: 9
    findings_minor: 22
    findings_suggestions: 6
    recommendation: "major-revision"
    notes: >-
      Core composition algebra (Section 5) is original and correct (the Maybe
      specialization of the foundation composition theorem; cross term
      vanishes as it should) and should be foregrounded. Critical: the Section
      6.6 success-probability formula is wrong and contradicts Section 7. Build
      fails as documented because minted needs -shell-escape, but minted and
      multicol are unused, so the fix is to remove them (otherwise clean 24
      pp). The singular hash map is over-claimed as a concrete algorithm
      (expected trials are exponential) and its Section 7 proof is not rigorous.
      Companion papers (data_type, composition) are cited in prose but absent
      from the bibliography.
    report_path: ".papermill/reviews/2026-05-29/review.md"

related_papers:
  - path: "~/github/bernoulli/papers/bernoulli_sets"
    rel: "extends"
    label: "Foundation paper: Bernoulli set model and composition theorem"
  - path: "~/github/bernoulli/papers/bernoulli_data_type"
    rel: "companion"
    label: "Maps as a computational basis type; full type-theoretic treatment"
---

## Notes

Initialized by papermill on 2026-05-29.

### Discovered structure
- Format: latex, build `TEXINPUTS=".:./sty:" pdflatex main.tex && bibtex main && (pdflatex x2)`.
  NOTE: `sty/` must be on TEXINPUTS (true for every modular-sty paper here). `minted`/`multicol`
  were removed 2026-05-29 (used only in sections/unused/), so `-shell-escape` is NO LONGER needed.
- Notation: modular `sty/` packages (functionnotation, setnotation, approxsetnotation,
  relationnotation, approxrelationnotation, envnotation, algorithmnotation)
- Sections (8, via `\subfile{}`): intro_new, prelim, bernoulli_map, special_cases,
  composition_new, entropy_maps, shm, conclusion
- Bibliography: `references.bib`, 15 entries
- Built PDF: 24 pages, clean (`main.pdf`; verified 2026-05-29 after the minted/multicol removal,
  0 errors and 0 undefined refs/cites)
- Supporting assets: research/ (Mathematica, SVG, DIA files)

### Note on stale collection state
The collection-level `papers/.papermill/state.md` lists OLD section names (approxmaps,
approx_maps, disc_fun, singular_hash_map) and "9 bib entries". The paper has since been
revised: the actual compiled structure is the 8 `_new`/`shm`/`entropy_maps` sections above
with 15 bib entries. This per-paper state reflects the current source.

### Thesis (working, from cross-paper topic placement)
Approximate maps (functions X -> Y) as first-class objects with error: the algebra of map
composition, special functions (Boolean functions, discrete functions), entropy of maps, and
the singular hash map construction. The thesis YAML block is left empty for
`papermill:thesis`.

### Related Work and Software
Extension paper building on `bernoulli_sets/`. Reference implementation:
`bernoulli-cpp/bernoulli_map.hpp` (the most general type in the library). Connects to
trapdoor computing: Bernoulli maps ARE cipher maps at the mathematical level.

### Freeze (2026-10-21)
Final preprint version prepared for re-deposit on Zenodo (concept 10.5281/zenodo.19105389). Status and errata box
added after the abstract (`status_errata.tex`); corrections listed in `ERRATA.md`: Section 6.5 success probability
replaced (the review's critical C1), Section 7 space theorem restated with a two-sided bound, composition closure
scoped to marginal rates with new Lemma 5.2 (shared intermediates break independence), set-operation rates per
latent block, Kronecker baseline fixed, novelty claims removed, predecessors credited (Bloomier, retrieval,
channel cascades, Rely, Carter et al., seed search). Build clean, 26 pages. Superseded by monograph Chapter 9
(with Chapters 14 and 17). No further revisions planned.
