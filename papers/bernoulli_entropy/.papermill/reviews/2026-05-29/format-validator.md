# Format Validator Report, bernoulli_entropy

**Reviewer role**: Build verification, label resolution, venue formatting
**Date**: 2026-05-29
**Build command run**: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex` in `/home/spinoza/github/bernoulli/papers/bernoulli_entropy`.

## Build verification
- **Result: clean.** All three pdflatex passes and bibtex exited 0. Output: `main.pdf`, **6 pages**, 333 KB.
- **Undefined references/citations**: none (grep of final-pass log: zero "undefined", zero "There were undefined references").
- **Overfull/underfull boxes**: **zero** reported in the final pass. Notably tidy for a math paper; the microtype configuration is doing its job.
- **Missing glyphs / font warnings**: none.
- **bibtex**: ran on `plain.bst` with `references.bib`, no warnings or errors (`main.blg` clean).

## Label and cross-reference resolution
- All `\cref`/`\Cref` targets resolve: `sec:intro_ent`, `sec:prelim_ent`, `sec:entropy`, `sec:entropy:pos_neg`, `sec:space_comp`, `sec:conclusion_ent`, `thm:joint_entropy_fp_fn`, `pst:approx_l_b`, `rem:general_lower_bound`, `fig:space_lower_bound`, `asm:element_indep`, `asm:fpr_fnr_r_indep`, and the equation labels. No `??` markers in the PDF; no "Reference ... undefined" in the log.
- `\numberwithin{equation}{section}` and `[section]` theorem numbering are consistent (equations and theorems both numbered within sections).
- Table of contents generates correctly (`main.toc` present and well-formed).

## Findings

### MINOR-1: cleveref name for `axiom` introduces stray spaces
- **Location**: `alex.sty` lines 539-540: `\crefname{axiom}{ axiom }{ axioms }` / `\Crefname{axiom}{ Axiom }{ Axioms }` (leading and trailing spaces inside the braces).
- **Problem**: Any `\cref{asm:...}` renders with irregular surrounding whitespace (e.g., "By \cref{asm:element_indep}" can produce double-spacing). Cosmetic, surfaces in this paper because it references the two axioms several times.
- **Scope**: The defect is in the shared `alex.sty`, not in this paper's own sources, so fixing it touches the family. Flagging for the maintainer. (Also noted by prose-auditor MINOR-4.)
- **Suggestion**: Trim to `\crefname{axiom}{axiom}{axioms}` in the style file.

### MINOR-2: Label prefix `pst:` for a Proposition is idiosyncratic
- **Location**: `space_complexity.tex` line 17, `\label{pst:approx_l_b}`.
- **Problem**: The environment is a `proposition` but the label uses prefix `pst:` (suggesting "postulate"). alex.sty does define a `postulate` environment, so the prefix likely predates a switch to `proposition`. Purely a naming hygiene issue; resolution works.
- **Suggestion**: Rename to `prop:approx_l_b` for consistency with the environment. Optional.

### SUGGESTION-1: No target venue selected; formatting is generic `article`
- The document uses the stock `article` class at 11pt with 1in margins, not a venue style (no IEEEtran, no `acmart`, no LIPIcs). The state file lists no target venue. This is fine for a working draft. When a venue is chosen, expect to re-fit (e.g., STOC/SODA would want `acmart` and a ~10-page two-column or LIPIcs format; an information-theory venue like IEEE Trans. IT would want IEEEtran). No action now; noting for the record.

### SUGGESTION-2: Figure is inline TikZ/pgfplots, no external asset dependency
- The single figure (`fig:space_lower_bound`) is generated inline via pgfplots from closed-form expressions, with no `img/` directory required (none exists; `\graphicspath{{img/}}` is harmless). This is good for reproducibility (the figure is the formulas). The two plotted curves match the stated formulas exactly (verified). No action.

## Reproducibility of the build
- Self-contained: `main.tex` + 5 section files + `references.bib` + local `alex.sty`. No `-shell-escape`, no `makeglossaries`, no minted, no external data files. A clean clone builds with the standard triple. This is the simplest, most portable build in the family.

## Confidence
High. The build is clean and fully reproduced; all labels resolve; the only findings are two cosmetic naming issues (one inherited from the shared style file) and forward-looking venue notes.
