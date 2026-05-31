# Format Validator Report

## Build Verification

Three-pass build succeeded:
```
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Output: `main.pdf` (411,457 bytes, 18 pages, letter size).

## Warnings

The only build warning is the benign:
```
Package microtype Warning: I cannot find a spacing list for font
```
This pertains to a font substitution in the PK font cache and does not affect output.

No undefined references. No undefined citations. No missing labels.

## PDF Metadata

- Title: "Bernoulli sets: a model for random approximate sets" (matches paper title)
- Author: "Alexander Towell"
- Subject: "computer science"
- Keywords: "probabilistic data structure, abstract data type, approximate set, bloom filter, perfect hash function, perfect hash filter"
- Creator: LaTeX with hyperref
- Producer: pdfTeX-1.40.25

The pdftitle in main.tex (line 41-42) matches `\title{}` (lines 58-61). Hypertexnames is set to false, which is correct for this document.

## Cross-references

All `\cref{}` invocations resolve. The labels:
- Sections: `sec:setalgebra`, `sec:asets`, `sec:bernoulli_model`, `sec:adt`, `sec:higher_order_model`, `sec:prob_model`, `sec:characteristics`, `sec:asymtotic` (typo, see F2)
- Definitions: `def:fprate`, `def:model_order`, `def:sample_fprate` (label-prefix conflict, see F1), `def:sample_tprate`, `def:pos_approx_set`, `def:neg_approx_set`
- Theorems: `thm:composition_rates`, `thm:twofold_composition`, `thm:fpbinom`, `thm:fpr`, `thm:fnbinom`, `thm:fnr`, `thm:approxfpr`
- Corollaries: `cor:tnbinom`, `cor:fpr_as_vareps`, `cor:tpbinom`
- Equations: `eq:approxfpr`, `eq:approxtpr`, `eq:conf_fpr`, `eq:conf_tpr`
- Example: `ex:boolean_universe`
- Remarks: `rem:bsc`, `rem:axiom_economy`, `rem:parametric_parsimony`, `rem:alpha_beta_convention`, `rem:latent_observed`, `rem:membership_boolean`
- Appendix: `app:cor_fpr_as_vareps`

## Findings

#### F1 (Suggestion): Equation labels under definitions use `def:` prefix
- **Location**: `sections/bernoulli_model.tex` lines 67, 72.
- **Quoted text**: `\label{def:sample_fprate}` and `\label{def:sample_tprate}` are applied to equation environments (line 66 starts `\begin{equation}`), not definition environments.
- **Problem**: The `def:` prefix is conventionally reserved for `\begin{definition}` environments. These labels mark equations within prose.
- **Suggestion**: Rename to `eq:sample_fprate` and `eq:sample_tprate`. (Carried from prior review.)

#### F2 (Suggestion): Section label typo
- **Location**: `sections/distributions.tex` line 173.
- **Quoted text**: `\label{sec:asymtotic}`
- **Problem**: Missing the 'p' in "asymptotic". The compiled output is unaffected but the source is non-searchable by the correct spelling.
- **Suggestion**: Rename to `\label{sec:asymptotic}` and update any `\cref{sec:asymtotic}` invocations. The current file shows the typo is referenced from `sections/set_theory.tex` (line 627) and `sections/uncertain_rates.tex` (line 42), but these are excluded files. The active paper does not reference this label; safe to rename in place.

#### F3 (Minor): Link colors enabled for print
- **Location**: `main.tex` lines 40-56.
- **Quoted text**: `colorlinks=true, linkcolor=magenta, citecolor=green, filecolor=blue, urlcolor=green`
- **Problem**: For most print venues, colored links are non-standard and may not print cleanly. The HTML/PDF web version is fine with colors.
- **Suggestion**: For print submission, switch to `colorlinks=false` or `allcolors=black`. Keep the current settings for the development/screen version. Some venues require black links.

#### F4 (Minor): Two-column / single-column formatting
- **Location**: `main.tex` line 1.
- **Quoted text**: `\documentclass[11pt,final,hidelinks]{article}`
- **Problem**: Single-column 11pt article style. This is fine for general journal submission, but venue-specific styles will require reformatting.
- **Suggestion**: Once a target venue is selected, update the documentclass and any margin/font specifications.

#### F5 (Suggestion): Two `\section` commands in appendix
- **Location**: `sections/appendix.tex` lines 8 and 28.
- **Quoted text**: `\section{Proof of corollary~\ref{cor:fpr_as_vareps}}` (line 8) and `\section{Notation Reference}` (line 28).
- **Problem**: Two top-level sections in the appendix. With `\appendices` declared in main.tex, these become Appendix A and Appendix B. This is fine, but the notation reference is more of a stand-alone reference than a proof, and could optionally be a separate appendix-style structure.
- **Suggestion**: Optional; the current structure is acceptable.

## Venue Formatting Considerations

Currently the paper uses the standard article class with `geometry={margin=1in}`. Common target venues require:
- **ACM**: `acmart` documentclass with two-column small format.
- **IEEE**: `IEEEtran` documentclass with two-column.
- **Algorithmica / Theory of Computing Systems**: LaTeX article-style, often Springer's `svjour3` class.
- **arXiv**: Article class is fine; submission requires source upload.

The 18 single-column 11pt pages will compress to roughly 10-12 two-column 9pt pages in most venue formats. Page-limit checks should be performed against the target venue.

## Recommendation

Build is clean. Address F1 and F2 (zero-cost label renames). F3-F5 are venue-dependent.
