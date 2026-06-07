# Format and Production Validation

**Paper**: A Forward (epsilon, omega) Calculus for Quantum Readout Error
**Date**: 2026-06-07
**Reviewer role**: format-validator (build verification, label resolution, venue formatting)

## Build  -  CLEAN

Command run (the brief's exact command, from the paper directory):

```
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Engine pdflatex (TeX Live 2023). Results:

- **PDF produced**: main.pdf, 11 pages, ~467 KB.
- **Undefined references**: 0. The log contains no "undefined references"
  message and no "Reference ... undefined" warnings on the final pass.
- **Undefined citations**: 0. All 16 \cite keys resolve; bibtex emitted zero
  `Warning--` lines and zero errors.
- **Multiply-defined labels**: 0.
- **Overfull/Underfull hbox/vbox**: 0 reported in the final pass.
- **Rerun advisories**: the only "rerun" string in the log is the
  rerunfilecheck.sty package loading line, not an actual "Rerun to get
  cross-references right" warning; cross-references are settled after the
  standard 2 post-bibtex passes.

## Label and cross-reference resolution  -  CLEAN

I enumerated every \label and every \cref/\Cref/\ref/\eqref target:

- 27 labels defined (sections, equations, theorem-environments, the table).
- Every \cref/\Cref/\ref/\eqref target has a matching \label. No dangling
  reference. cleveref resolves all environment references with correct type
  names (Proposition/Theorem/Corollary/Definition/Section/Table).
- Equation numbering is section-scoped (\numberwithin{equation}{section}) and
  consistent; theorem environments share one counter (theorem/proposition/
  lemma/corollary/definition/example all on the [theorem] counter), so numbering
  reads 3.1, 3.3, 3.4, ... which is intentional and internally consistent.

## Warnings actually present  -  cosmetic only

The only warnings in the build are four hyperref "Token not allowed in a PDF
string (Unicode)" messages. These come from math content in the \title and
\section titles (the (epsilon, omega) and the "$" in the title) being fed into
PDF bookmark/metadata strings. They do **not** affect the rendered PDF; they only
mean the PDF outline/title metadata strips the math. **Minor (F1)**, easily
silenced by providing \texorpdfstring{...}{...} alternatives for the math in the
title and any section heading that contains math, or by setting
\hypersetup{pdftitle=...} explicitly. Purely cosmetic; not blocking.

## Venue formatting

- Document class: `article`, 11pt, 1in margins. Generic; no venue style is
  targeted in the source and the state file lists venue.target as null. This is
  appropriate for a Zenodo preprint (the stated publication strategy). If the
  paper is later submitted to a specific venue (PRX Quantum, Quantum, an IEEE
  venue), the class and bibliography style will need swapping; nothing in the
  current source obstructs that.
- natbib + plainnat with [numbers,square]: numeric square-bracket citations,
  standard and clean.
- No figures; one booktabs table (Table 1) typeset correctly (toprule/midrule/
  bottomrule, right-aligned numeric columns). The \phantom{0} alignment padding
  in the rel.-overestimate column is correct and renders aligned.
- hyperref colorlinks with blue link/cite/url colors: fine for a preprint;
  some venues require black links in the print version (trivial to toggle).

## Build artifacts / hygiene

The .gitignore covers build artifacts (per the brief). I generated main.aux,
.bbl, .blg, .log, .out, .pdf during verification; none should be committed and
the brief instructs not to commit any. No artifact is staged.

## Findings

- **Minor (F1)**: Four cosmetic hyperref "Token not allowed in a PDF string"
  warnings from math in the title/section headings. Add \texorpdfstring or an
  explicit \hypersetup{pdftitle=...} to silence; affects only PDF metadata, not
  the rendered document.

No Critical, Major, or blocking format findings. The paper builds cleanly to 11
pages with zero undefined references/citations, zero bad boxes, and fully
resolved cross-references. Production-ready for a preprint.
