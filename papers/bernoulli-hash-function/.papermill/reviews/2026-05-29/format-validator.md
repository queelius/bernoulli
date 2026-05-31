# Format Validator Report

**Paper:** The Bernoulli Hash Function
**Date:** 2026-05-29
**Build:** `cd .../bernoulli-hash-function && make`

## Build Result

- **Status:** SUCCESS. `make` (pdflatex + bibtex + pdflatex x2) exits 0.
- **Output:** `main.pdf`, 27 pages, 704,612 bytes.
- **Overfull hboxes:** 0.
- **Undefined references / citations:** none.
- **Label resolution:** all `\cref`/`\Cref` resolve; `main.bbl` generated.

The prior pass's two MAJOR build issues are resolved: `gloss.tex` is gone (no
`\usepackage{glossaries}`, no `\input{gloss}`, no Makefile reference), and the
pgfplots figures now compile cleanly (the factorial / log-gamma expressions in
`fig:adaptive_fpr` build without error on this TeX Live).

## Findings

### MINOR-1: Duplicate PDF destinations for appendix equations A.1 to A.4
- **Location:** `main.log` (pdfTeX warnings), arising from `sections/entropy.tex`
  Thm `thm:L_pmf` (`eq:L_pmf`) and `sections/appendix.tex` Thm
  `thm:pmf_detailed` displaying the *same* salt-bit-length PMF, plus the two
  `\section`s under `\appendix`.
- **Quoted text (log):** "pdfTeX warning (ext4): destination with the same
  identifier (name{equation.A.1}) has been already used, duplicate ignored"
  (repeated for A.2, A.3, A.4).
- **Problem:** Four equations in the appendix collide with hyperref destination
  names already used earlier, so the corresponding hyperlinks point to the first
  occurrence. Cosmetic, but it produces warnings on every build and slightly
  degrades PDF navigation. The root cause is that `thm:pmf_detailed` restates
  `thm:L_pmf` verbatim (the same PMF equation appears twice in the document).
- **Suggestion:** Easiest fix: in the appendix, reference the earlier result
  ("recall `eq:L_pmf`") instead of re-displaying the identical equation, which
  removes the duplication and the redundancy at once. Alternatively, ensure each
  displayed equation that needs a destination has a unique `\label`, or load
  `hyperref` with `hypertexnames=false`.
- **Severity:** Minor.

### MINOR-2: Two pgfplots figures rely on TeX floating-point factorials
- **Location:** `sections/shf.tex`, Fig. `fig:adaptive_fpr` (lines ~405-423):
  `x^4 * (1-x)^45 * 50! / (4! * 45!)` and
  `exp(19*ln(x) + 180*ln(1-x) + ln(200!) - ln(19!) - ln(180!))`.
- **Problem:** These build on the current TeX Live (verified: 0 errors), but
  `50!` (approx 3e64) and `ln(200!)` push pgfmath near its range. On a stricter
  or older distribution the direct-factorial curve (m=50, p=5) is the most
  likely to fail or render incorrectly. This is the same fragility the prior
  pass flagged; it has not bitten this environment but remains a portability
  risk for an external venue's build.
- **Suggestion:** Use the log-gamma form uniformly for all four curves (the
  orange m=200 curve already does). Compute the Beta PDF as
  `exp((a-1)*ln(x) + (b-1)*ln(1-x) + lngamma(a+b) - lngamma(a) - lngamma(b))`.
  This removes the explicit factorials and is robust across distributions.
- **Severity:** Minor.

### MINOR-3: hyperlinks invisible (hidelinks + colorlinks=false)
- **Location:** `main.tex`, lines 18 and 33: `\usepackage[hidelinks]{hyperref}`
  with `colorlinks=false`.
- **Problem:** All internal links (cref, toc, citations) render with no visual
  cue. Fine for print; reduces navigability of the digital PDF. Stylistic.
- **Suggestion:** Optional: `colorlinks=true` with subtle colors for the
  e-print version. No change needed for a camera-ready print target.
- **Severity:** Minor / optional.

## Asset and Dead-Code Check

| Item | Status |
|---|---|
| `gloss.tex` | REMOVED (prior MAJOR-1 resolved) |
| `img/` directory | EMPTY; `fig_shs` figure removed (prior figure findings resolved) |
| Figures in document | 3 inline TikZ/pgfplots (adaptive FPR, price-of-certainty, space comparison); none reference external files |
| `\input` graph | main.tex inputs defs + 10 section files, all present |
| Makefile | `all/draft/clean/cleanall/watch/wc/help`; dependency list no longer references gloss |
| alex.sty / defs.tex | present and loaded; `\PDF`, `\OS`, `\betadist`, algorithm keywords defined |

## Theorem Numbering Note

The paper uses `[section]` numbering. Adaptive theorems live in Section 3
(thm:success_adaptive_set, thm:success_adaptive_map, thm:fpr_distribution,
thm:adaptive_moments, thm:adaptive_complexity) and render as 3.x. The space and
price-of-certainty theorems (thm:space, thm:adaptive_space, thm:price_certainty)
render as 5.x. References by label are robust regardless of the compiled numbers.

## Status vs Prior Pass

| Prior format finding | Status |
|---|---|
| MAJOR gloss.tex dead code | RESOLVED |
| MAJOR pgfplots factorial overflow | NOT TRIGGERED here; portability risk remains (MINOR-2) |
| MINOR fig_shs old naming | RESOLVED (figure removed) |
| MINOR fig_shs never included | RESOLVED (removed; no dangling include) |
| MINOR relsize needed if fig included | MOOT (figure removed) |
| MINOR invisible hyperlinks | OPEN (MINOR-3, optional) |
| (new) duplicate appendix eq destinations | OPEN (MINOR-1) |
