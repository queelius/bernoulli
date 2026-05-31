# Format Validator Report, The Perfect Hash Filter

**Date**: 2026-05-29
**Scope**: Build verification, label/citation resolution, figure/data file resolution, venue formatting. Build was actually attempted (not inferred).

## Summary

The manuscript **does not compile** in its committed state. The build aborts with a fatal error before producing any PDF, because `main.tex` now `\subfile`s `sections/rd_ph_filter.tex`, which `\input`s `img/phfilter.tex`, and the `img/` directory does not exist. The `state.md` claim that the paper "compiles to 10 pages" is stale: it predates the inclusion of `rd_ph_filter.tex` in the subfile list. Beyond the fatal stop, the first pass emits a large number of undefined-citation and undefined-reference warnings (the body cites placeholder/undefined keys and references labels that live in sections whose figures are missing). Two directories the paper depends on (`img/`, `data/`) are absent entirely. This is the top blocker to any further progress: nothing downstream can be evaluated on a rendered PDF until the build is restored.

Severity counts: Critical: 1 | Major: 2 | Minor: 3

---

## Critical

### F1. Fatal build failure: missing `img/phfilter.tex` (and the entire `img/` directory)
- **Location**: `sections/rd_ph_filter.tex` line 169 (`\input{img/phfilter.tex}`), reached via `main.tex` line 156 (`\subfile{sections/rd_ph_filter}`).
- **Evidence (actual build)**: Running the documented command
  `TEXINPUTS=".:./sty/:" pdflatex -shell-escape -interaction=nonstopmode -halt-on-error main.tex`
  from `paper/` aborts with:
  ```
  ! LaTeX Error: File `img/phfilter.tex' not found.
  ! Emergency stop.
  !  ==> Fatal error occurred, no output PDF file produced!
  l.169 \input{img/phfilter.tex}
  ```
  `ls img/` and `ls data/` both confirm the directories do not exist.
- **Problem**: The committed `main.tex` includes `rd_ph_filter.tex` (so the headline "known item: core section excluded" is partly resolved: it is now wired in), but its first figure depends on a TikZ file that was never created (or was lost when the old `random_approximate_sets/` tree was deleted). No PDF is produced at all. Every downstream label in `rd_ph_filter.tex` (`thm:fp_rate`, `fig:PHFilter`, `pst:approx_l_b`, the space theorems) is therefore unresolved everywhere, which cascades into the undefined-reference warnings below.
- **Suggestion**: Create `paper/img/phfilter.tex` (the TikZ source for the 3-element PHF figure described in the caption: a perfect-hash filter modeling `{x1,x2,x3}` at FPR `2^-3`, load factor `3/5`). As a stopgap to restore the build immediately, replace the `\input{img/phfilter.tex}` with a placeholder `\fbox{...}` or comment the figure body, but the real fix is to author the figure. Also create `paper/data/` with the four CSVs referenced by `adt.tex` (or convert those plots to closed-form, see F2).

---

## Major

### F2. `adt.tex` figure reads four non-existent CSV data files
- **Location**: `adt.tex` lines 540 to 546: `\addplot ... table [col sep=comma] {data/data1.csv}`, `{data/data.5.csv}`, `{data/data.25.csv}`, `{data/efficiency_fprate_union.csv}`.
- **Problem**: These plots cannot build once reached, because `data/` is absent. They are currently shielded inside a `\COMMENT{}` block (lines 484 to 550), so they do not break the build today, but they will the moment the block is activated, and they represent unrendered intended content.
- **Suggestion**: Add the CSVs under `paper/data/`, or replace with closed-form `\addplot {expr}` (the sibling live figure `fig:cor_union_same_fprate` at lines 552 to 580 already plots the same family of curves in closed form, so the CSV version may be redundant).

### F3. Duplicate `\label` and dangling references that will produce wrong cross-refs once the build runs
- **Location**: `adt.tex` line 514 and line 579 both define `\label{fig:cor_union_same_fprate}` (one in the commented block, one live). Compiled sections also reference labels that are undefined in the compiled set: `\cref{dummyref}` (`adt.tex` lines 99, 362, 411, 456), `\cref{thm:fpr,thm:fnr}` (`adt.tex` line 25), `\cref{sec:set_theory}` and `\cref{lst:asetunion}`/`\cref{lst:asetcomp}` (`cpp_imp.tex` lines 31, 31), `\cref{sec:apps}`/`\cref{sec:pmf}`/`\cref{sec:phf}` from the intro.
- **Evidence (actual build, first pass)**: warnings included `Reference 'sec:phf' ... undefined`, `Reference 'thm:fp_rate' ... undefined`, `Reference 'fig:PHFilter' ... undefined`, plus the duplicate-label condition.
- **Problem**: `dummyref` is a literal placeholder label cited four times in `adt.tex` (it stands in for the family's composition-theorem reference); it will render as `??`. `thm:fpr`/`thm:fnr` (note: spelled `thm:fp_rate` where actually defined, line 184) are referenced but the names do not match the definition, so even after the build is fixed these will mis-resolve. `lst:asetunion`/`lst:asetcomp` point at listings that are entirely commented out in `cpp_imp.tex`.
- **Suggestion**: Replace `dummyref` with the correct citation/label (the composition-theorem result, likely in `bsets`/`bernoulli_composition`). Reconcile `thm:fpr`/`thm:fnr` vs the actual `thm:fp_rate` label. Either restore the commented listings (so `lst:asetunion`/`lst:asetcomp` resolve) or remove the references to them.

---

## Minor

### f1. `state.md` build claim is stale
- **Location**: `.papermill/state.md` line 102 ("Paper compiles to 10 pages with warnings").
- **Problem**: With `rd_ph_filter.tex` now in the subfile list, the paper does not compile at all. The state file should record the current fatal-error state.
- **Suggestion**: Update `state.md` after the build is restored.

### f2. `\COMMENT{}` used to disable large blocks, including a whole algorithm and figures
- **Location**: `\newcommand{\COMMENT}[1]{}` in `main.tex` line 39; large `\COMMENT{}` blocks in `rd_ph_filter.tex` (lines 134 to 160, the membership algorithm) and `adt.tex` (lines 484 to 550).
- **Problem**: Disabling content via a gobbling macro is fragile (the content is not type-checked and silently vanishes); the membership-test algorithm `alg:PHF_has` is invisible in the PDF yet referenced conceptually.
- **Suggestion**: Either finish and enable these blocks or remove them; prefer `%` line comments or version control over a gobble macro for long-term-dead content.

### f3. No venue/document-class concerns yet (early draft)
- **Location**: `main.tex` line 1 (`\documentclass[11pt,final,hidelinks]{article}`).
- **Problem**: Generic `article` class is fine for a draft; `state.md` lists venue "Undetermined." `final` option with `microtype` is reasonable. No action needed until a venue is chosen, at which point the class, margins, and bibliography style will need to match submission requirements.
- **Suggestion**: Defer; revisit at venue-selection time.

---

## Build reproduction (for the record)

Command run from `paper/`:
```
TEXINPUTS=".:./sty/:" pdflatex -shell-escape -interaction=nonstopmode -halt-on-error main.tex
```
Result: exit 1, no `main.pdf` produced. Fatal error at `rd_ph_filter.tex` line 169 (`img/phfilter.tex` not found). Preceding warnings: ~7 undefined citations (`bsets`, `bmaps`, `bf`) and ~10 undefined references (`sec:phf`, `sec:typed_phf`, `sec:k_perfect`, `sec:pmf`, `sec:apps`, `sec:impl`, `sec:adt`, `thm:fp_rate`, `fig:PHFilter`) on the first pass (expected to mostly resolve on a successful multi-pass build, except the placeholder `dummyref` and the name-mismatched `thm:fpr`/`thm:fnr`).

**Minimal path to a building PDF**: (1) create or stub `img/phfilter.tex`; (2) replace `dummyref` and fix the `thm:fpr`/`thm:fnr` vs `thm:fp_rate` mismatch; (3) re-run the full `pdflatex / makeglossaries / bibtex / pdflatex x2` sequence. Steps (1) and (2) are the gate; everything else is warnings.
