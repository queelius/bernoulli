# Formatting and Production Review

**Paper**: Binary classification measures for random approximate sets
**Reviewer role**: format-validator (performed by area chair)
**Date**: 2026-05-29

## Build verification: PASS

Ran the prescribed build from a clean state:
```
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```
- Exit code 0 on all passes.
- Output: `main.pdf`, 14 pages (matches the state file's recorded page count).
- BibTeX: clean, no warnings.

## Reference and label resolution: PASS

- No "undefined references" or "undefined citations" in the final log.
- No "multiply defined" labels.
- `cleveref` / `\Cref` cross-references all resolve (intro references to thm:approx_expected_precision, thm:f1_approx, the figures, and the appendix labels all bind correctly).
- `\numberwithin{equation}{section}` is active; equation numbering is per-section as intended.

## Typesetting quality: PASS

- **Overfull/underfull boxes: 0.** Clean across the whole document (microtype is enabled with protrusion and expansion, which helps).
- `hyperref` configured with `pdftitle`, `pdfauthor`, keywords; metadata present.
- Figures: TikZ/pgfplots figures (figs 2, 3, 4) compile inline from the committed CSVs. Figure 1 includes `img/out.pdf_tex` (a TikZ-exported SVG via `\input{img/out.pdf_tex}` with `out.pdf`); both assets are present in `img/`.

## Findings

### MINOR-1: Figure 1 uses a fragile `\def\svgwidth` / pdf_tex inclusion with a commented-out scale
- **Location**: Measures, fig:prec_vs_fprate_and_fnrate. `\def\svgwidth{\columnwidth/2}` with `%\def\svgscale{0.75}` commented out, then `\input{img/out.pdf_tex}`.
- **Problem**: The `out.pdf_tex` mechanism (Inkscape SVG export) depends on `out.pdf` sitting at the path the `.pdf_tex` expects and on the `\svgwidth` macro being set. It works in this build, but it is the most brittle part of the production pipeline and is the one figure not regenerable from committed source (no SVG or generating script for `out.pdf`).
- **Impact**: Builds today; portability risk if the figure must be regenerated or the venue requires source figures.
- **Suggestion**: Either commit the source SVG (and a note on regeneration) or, better for consistency, reimplement fig 1 as a native pgfplots figure like figs 2 to 4 (it shows PPV histograms, which pgfplots can render from a CSV). This also removes the `tikzscale`/`out.pdf_tex` dependency.

### MINOR-2: Generic `article` class, no venue selected
- **Location**: `\documentclass[11pt,final,hidelinks]{article}`. Note: `hidelinks` is passed but `hyperref` later sets `colorlinks=true` with colored link/cite/url colors, so `hidelinks` is effectively overridden.
- **Problem**: No target venue is selected (state file confirms). The colored links (magenta/green/blue) are fine for a preprint but most archival venues want black or subdued links. The `hidelinks` class option and the `colorlinks=true` hyperref setup are in mild tension (the latter wins).
- **Suggestion**: Decide on link styling once a venue is chosen; for a neutral preprint, either keep colored links and drop `hidelinks`, or switch to subdued/black links for camera-ready. Low priority until a venue is chosen.

### SUGGESTION-1: `\appendices` from the `appendix` package with `article`
The appendices render correctly (A, B, C). Confirmed labels `sec:proof_approx_expected_precision`, `sec:proof_f1`, `app:samp` resolve. No action needed; noting it works.

### SUGGESTION-2: Reproducibility assets (cross-listed with methodology-auditor)
Only `code/f1_sim.py` is committed. For a clean production package, add the PPV and prevalence-curve generators so every figure is regenerable. This is a methodology/repro point but also a production-completeness one.

## Summary
Production is in good shape: clean build, correct page count, zero bad boxes, all labels and citations resolve. The only real production risk is the single SVG-derived figure (fig 1); everything else is native and reproducible.
