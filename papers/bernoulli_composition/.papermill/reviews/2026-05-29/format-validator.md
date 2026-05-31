# Format Validation Report

## Summary

The manuscript is production-clean. It compiles end to end with the documented
three-pass `pdflatex` + `bibtex` sequence, every cross-reference and citation
resolves, there are no "??" placeholders in the output PDF, and all `\input`
files and the notation package are present. No target venue is selected, so venue
compliance is assessed only generically. The only items worth noting are a set of
defined-but-unreferenced labels (a tidiness issue, not a build issue).

[Build status: success.]

## Build Results

- **Format**: latex (article class, 11pt).
- **Build command**: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex` (run from the paper directory).
- **Result**: success. All three `pdflatex` passes and the `bibtex` pass returned exit code 0.
- **Errors**: 0.
- **Warnings**: 0 substantive. The only log line of note is a benign
  `microtype` informational message ("I cannot find a spacing list for font"),
  which does not affect output, plus the standard `rerunfilecheck` package load
  line. No "rerun to get cross-references right," no undefined references, no
  multiply-defined labels on the final pass.
- **Output**: `main.pdf`, 15 pages, 360 KB.

## Critical Issues

None. The paper builds.

## Major Issues

None.

## Minor Issues

### m1. Numerous defined-but-unreferenced labels
- **Location**: across `sections/`.
- **Quoted output**: 55 labels defined, 28 distinct labels referenced. Unreferenced labels include `thm:setdiff_rates`, `cor:equality_prob`, `cor:intersect_negative`, `fig:union_fpr`, `rem:monoid`, `rem:parametric_parsimony`, `rem:composed_order`, `sec:union`, `sec:intersection`, `sec:complement`, `sec:setdiff`, `sec:closure`, `ex:numerical_union`, `def:subset_pred`, `def:eq_pred`, `def:proper_subset_pred`, `eq:union_fpr`, `eq:intersect_fpr`, `eq:intersect_fnr`, `eq:setdiff_fpr`, `eq:setdiff_fnr`, `eq:grammar_exp`, `eq:grammar_nexp`, `eq:fpr_clt`, `asm:fpr_fnr_r_indep`, `thm:uncertain_rates_union`.
- **Problem**: None of these cause a build problem; LaTeX permits unreferenced labels. But a headline theorem (`thm:setdiff_rates`), the only figure (`fig:union_fpr`), and the equality corollary (`cor:equality_prob`) being unreferenced means the prose never points the reader to them by number. Equation labels (`eq:union_fpr`, etc.) that exist only so the summary table's caption can reference them collectively are fine to leave. The theorem, figure, and corollary labels signal missing in-text cross-references (see prose report m5).
- **Fix**: Add in-text references to the figure and to the set-difference and equality results; the remaining equation and section labels are acceptable anchors and can stay.
- **Severity**: minor
- **Confidence**: high

### m2. Author-name formatting is inconsistent across bibliography entries
- **Location**: `references.bib`.
- **Quoted output**: `basicinterval` uses initials ("T. Hickey and Q. Ju and M. H. Van Emden") while `mooreInterval` ("Ramon E. Moore") and `coverThomas` ("Thomas M. Cover and Joy A. Thomas") use full given names.
- **Problem**: With `bibliographystyle{plain}` this produces slightly inconsistent author rendering. Cosmetic only.
- **Fix**: Use full given names consistently, or accept the `plain` style's normalization.
- **Severity**: minor
- **Confidence**: high

## Reference Resolution

- **Undefined references**: none. Every `\ref`, `\cref`, and `\Cref` target
  resolves; `sec:intervals` (referenced from `intro.tex` and `set_theory.tex`)
  resolves to `uncertain_rates.tex`. No "??" appears in the PDF text.
- **Unused labels**: 27 defined labels are never referenced (see m1). Not a build
  defect.
- **Missing citation keys**: none. All six `\cite` keys (`bernoulliSets`,
  `bernoulliMeasures`, `bernoulliEntropy`, `basicinterval`, `mooreInterval`,
  `coverThomas`) appear in `references.bib`; all six entries are cited. No phantom
  keys, no orphan entries.

## Venue Compliance

No target venue is selected in the state file (candidates listed: ACM TALG, TCS,
PODS, VLDB). Generic observations against top-tier CS-theory norms:

- **Document class**: generic `article`, 11pt, 1-inch margins. Each candidate
  venue has its own class (`acmart` for TALG, PODS, and ACM VLDB-track;
  Elsevier `elsarticle` for TCS). A class switch will be required at submission
  and may change page count and float placement.
- **Citation style**: `natbib` with `square,numbers` and `bibliographystyle{plain}`.
  ACM venues expect `ACM-Reference-Format`; TCS expects the Elsevier number style.
  Convertible at submission.
- **Length**: 15 pages in `article` 11pt is comfortable; under `acmart`
  two-column it would shrink substantially and sit well within typical limits.
- **Required sections**: abstract present; keywords are set in PDF metadata
  (`hypersetup` `pdfkeywords`) but not displayed as a keyword list, which most
  venues want visible. Add a `\keywords{...}` block once the class is chosen.
- **No ACM CCS concepts / no `\begin{CCSXML}`**: required by ACM venues; add when
  targeting TALG, PODS, or ACM VLDB.

## Asset Inventory

- **Referenced figures**: 1 referenced (`fig:union_fpr`) / 1 present. The figure
  is inline TikZ + pgfplots, compiled from `main.tex` itself; there is no external
  image file to be missing.
- **`\includegraphics` usage**: none (so `graphicspath{{img/}}` is currently
  inert; harmless).
- **`\input` files**: all six present and accounted for (`intro`,
  `preliminaries`, `set_theory`, `relational`, `uncertain_rates`, `conclusion`).
- **Notation package**: `alex.sty` present in the paper root (749 lines), loads
  cleanly as `\usepackage[fancy,section]{alex}`.
- **Missing assets**: none.
