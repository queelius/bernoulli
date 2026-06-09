# Format Validator Report

**Paper**: *The abstract data type of the approximate relation*
**Date**: 2026-06-09
**Scope**: Build verification, label/reference resolution, venue formatting. All checks run directly against the source.

## Build (ran the prescribed sequence)
```
TEXINPUTS=".:./sty:" pdflatex -shell-escape main   -> exit 0
bibtex main                                          -> exit 0
TEXINPUTS=".:./sty:" pdflatex -shell-escape main     -> exit 0
TEXINPUTS=".:./sty:" pdflatex -shell-escape main     -> exit 0
```
**Status: CLEAN.** `Output written on main.pdf (21 pages, 588418 bytes).`

| Check | Result |
|---|---|
| Undefined references | **0** |
| Undefined citations | **0** |
| Dangling `\cref`/`\ref` (label-set difference) | **0** (21 ref targets, all in the 88 defined labels) |
| LaTeX warnings | **0** |
| "Rerun to get..." messages | **0** (rerunfilecheck: `main.out` unchanged) |
| Overfull \hbox | **0** (the prior 3.31pt box at relations.tex:36-37 is no longer present) |
| Underfull \hbox/\vbox | **0** |
| bibtex warnings/errors | **0** |
| Duplicate-destination warnings | **0** (`hypertexnames=false` in hypersetup clears the subfiles+hyperref anchor collisions) |

The only log notice is a benign `microtype` "I cannot find a spacing list for font" info, which is cosmetic and does not affect output.

## Label / reference resolution
- 88 labels defined; 21 distinct `\cref`/`\ref` targets used; **every target resolves**. No `??` in the PDF.
- All theorem/definition/figure/table cross-references (`thm:join_dependence`, `thm:project`, `thm:symmetric_closure`, `fig:proj_fpr`, `tbl:ex_join`, `tbl:validation`, `def:approx_pfun`, `cor:uniform_fanin`, `asm:ber_trial`, etc.) resolve to defined labels.

## Modular-sty build robustness
- The paper is a **MODULAR-STY** paper: every `pdflatex` needs `TEXINPUTS=".:./sty:"` and `-shell-escape` (minted). This is documented in CLAUDE.md and the per-paper state. **Verified**: with the correct TEXINPUTS the build is clean; the `\AT` macro used in `def:approx_rel` resolves because `approxsetnotation` transitively requires `approx_data_type_notation` (which defines `\AT`).
- **FV-MINOR-1 (robustness, not a current error)**: `def:approx_rel` (approx_rel_model.tex:42) depends on `\AT` and `\SetComplement`, which arrive only *transitively* (via `approxsetnotation → approx_data_type_notation`, and `setnotation` respectively). main.tex does not load `approx_data_type_notation` directly. The build is clean today, but if a future edit reorders or trims the `\usepackage` list (for example, dropping `approxsetnotation` after the predicate material was cut), `\AT` would silently break. **Suggestion**: either load `approx_data_type_notation` explicitly in main.tex, or (preferred, per prose-auditor PA-MINOR-1) rewrite condition (i) without `\AT`, removing the transitive dependency entirely.

## Venue formatting
- Document class is the generic `article` (11pt), not a venue style. The commented line (main.tex:1) shows an IEEE compsoc variant was once considered. For a **database-theory venue** the manuscript will need reformatting to the target style (ACM `acmart` for PODS/SIGMOD-adjacent, or LIPIcs for ICDT). **FV-MINOR-2**: no venue style is applied; this is expected for a preprint but is a required step before any DB-venue submission. Not a defect in the current (preprint) state.
- `minted` requires `-shell-escape`; acceptable for a preprint but note that some venue submission systems disallow shell-escape. If the paper has no code listings rendered by minted in the final body (the `_minted-main/` dir suggests a listing exists), confirm it is needed; if not, dropping minted simplifies the build (the sibling `bernoulli_maps` did exactly this).

## Production artifacts
- `.gitignore` is present and covers build artifacts. The working tree shows an uncommitted `main.maf` (minitoc auxiliary) and a `_minted-main/` pygtex artifact; these are build outputs and should be gitignored if not already (verify `main.maf` is covered).

## Verdict
**Build is production-clean**: 21 pages, zero undefined refs/cites, zero warnings, zero overfull boxes, zero bibtex warnings. The only findings are (FV-MINOR-1) a fragile transitive macro dependency in `def:approx_rel` worth hardening, and (FV-MINOR-2/style) the absence of a target-venue document class, which is the expected pre-submission step. Nothing blocks compilation or reproduction.
