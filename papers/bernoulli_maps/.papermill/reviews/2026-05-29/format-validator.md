# Format Validator Report, bernoulli_maps

**Specialist**: format-validator (build verification, label resolution, venue formatting)
**Date**: 2026-05-29
**Build environment**: TeX Live (pdflatex), local `sty/` packages, `minted`, `glossaries` with `xindy`.

## Verdict summary

The paper builds to a clean 24-page PDF with zero undefined references and zero undefined citations, but **only when invoked with `-shell-escape`**, which the documented build command in the paper's own `CLAUDE.md` and the per-paper `state.md` both omit. That is the one finding of real consequence: following the documented build command produces a fatal error and no PDF. Everything else is cosmetic: one minor overfull box, duplicate PDF-anchor warnings from the proof equation-renumbering, an inactive glossary apparatus, and an orphaned `defs.tex` whose stale PDF metadata never reaches the output.

## MAJOR findings

### M10. Documented build command is wrong: the paper requires `-shell-escape` but the recorded command omits it (source: format-validator)
- **Location**: build configuration. `bernoulli_maps/CLAUDE.md` and `.papermill/state.md` both record:
  > `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
  but `main.tex` loads `\usepackage{minted}` (line 39), which requires shell escape.
- **Observed**: Running the documented command fails on pass 1 with:
  > `! Package minted Error: You must invoke LaTeX with the -shell-escape flag.` ... `! ==> Fatal error occurred, no output PDF file produced!`
  Running `pdflatex -shell-escape main.tex && bibtex main && makeglossaries main && pdflatex -shell-escape main.tex && pdflatex -shell-escape main.tex` succeeds: 24-page PDF, exit 0, no undefined refs/cites.
- **Problem**: The recorded build is non-functional. Anyone (including future tooling or a co-author) following the documented command gets no PDF. Also note `makeglossaries` is needed in the chain because `glossaries` is loaded with `[acronyms,symbols]` and `\makeglossaries` is active (even though no entries are printed, see m22).
- **Why major**: a paper that does not build by its documented procedure is a reproducibility defect, and this is exactly the class of issue a format check exists to catch. (The collection-level `papers/CLAUDE.md` lists `bernoulli_maps` under "All others: same pattern as bernoulli_sets" = the plain triple, which is the wrong pattern for this paper. The state file's "Discovered structure" also records the plain command.)
- **Suggestion**: update both `bernoulli_maps/CLAUDE.md` and `.papermill/state.md` (and the collection note) to:
  `pdflatex -shell-escape main.tex && bibtex main && makeglossaries main && pdflatex -shell-escape main.tex && pdflatex -shell-escape main.tex`
  Alternatively, if `minted` is not actually used for code listings in the active sections (it appears to be loaded but no `\begin{minted}` block exists in the included sections), **remove `\usepackage{minted}` and `\usepackage{multicol}` if unused**, which would let the plain build command work and drop the shell-escape requirement entirely. (Verify: a grep of the included sections shows no `minted` environment; `minted` may be a dead include inherited from a template.)
- **Confidence**: high (reproduced both the failure and the fix).

## MINOR findings

### m20. Duplicate PDF destination anchors from proof/example equation renumbering (source: format-validator)
- **Location**: build log, repeated:
  > `pdfTeX warning (ext4): destination with the same identifier (name{equation.2.1}) has been already used, duplicate ignored` (also `equation.3.1`, etc.)
- **Cause**: `envnotation.sty` resets the equation counter to `(a),(b),...` inside `proof` and `example` environments (`\AtBeginEnvironment{proof}{\setcounter{equation}{0}...}`). Because `cleveref`/`hyperref` build anchors from section+equation numbers, the in-proof equation `(a)` in section 2 and the body equation `2.1` can collide on the `equation.2.1` hyperref name, so hyperref discards duplicates. Cross-references still resolve (the build has zero undefined refs), but in-PDF hyperlinks to those equations may jump to the wrong target.
- **Problem**: cosmetic to the printed page, but PDF navigation/links to renumbered equations are unreliable.
- **Suggestion**: give proof/example equations a distinct counter prefix (e.g., redefine `\theequation` inside those environments to include the environment counter, or use `\tagform@`-safe sub-numbering), or accept the warning as benign. Low priority.
- **Confidence**: high (cause confirmed from `envnotation.sty` and `defs.tex` counter-reset code).

### m21. One overfull hbox (source: format-validator)
- **Location**: build log: `Overfull \hbox (6.12671pt too wide) in paragraph at lines 77--80` of `shm.tex` (the remark after `thm:shm-success`).
- **Problem**: 6.1pt overflow, visible as a slightly-too-wide line. Trivial.
- **Suggestion**: minor rewrap or `\sloppy` locally. Lowest priority.
- **Confidence**: high.

### m22. Glossary apparatus is active but empty; `gloss.tex` is orphaned (source: format-validator)
- **Location**: `main.tex` loads `\usepackage[xindy,toc,acronyms,symbols]{glossaries}` and `defs.tex`/`envnotation.sty` call `\makeglossaries`, but `\loadglsentries{gloss}` is **commented out** (`main.tex:91`), and no `\printglossaries`/`\gls` calls exist in the sections.
- **Problem**: The build runs the full glossary machinery (and `makeglossaries` must be invoked) to produce nothing. `gloss.tex` (with 15 glossary/acronym entries) is dead weight and contains its own defects (the "set = ordered" contradiction flagged by prose-auditor m12, and typos "poular"/"a a"). This is wasted build surface and a maintenance trap.
- **Suggestion**: either (a) remove the `glossaries` package, the `\makeglossaries` calls, and `gloss.tex` if no glossary is intended, or (b) actually load and print the glossary. Right now it is half-wired.
- **Confidence**: high.

### m23. `defs.tex` is not loaded by `main.tex`; its PDF metadata and duplicate theorem definitions are dead code (source: format-validator)
- **Location**: `main.tex` does **not** `\input{defs}` (verified: no `defs` reference in `main.tex`). The active theorem/example/remark environments and counters come from `sty/envnotation.sty`. `defs.tex` separately defines the same environments and sets `\hypersetup{pdftitle={The approximate map abstract data type}, ...}`.
- **Problem**: 
  1. The `pdftitle` in `defs.tex` ("The approximate map abstract data type") never reaches the output because `defs.tex` is not loaded, so the compiled PDF has **no custom title metadata** (it falls back to hyperref defaults). Even if it were loaded, that title disagrees with the actual paper title ("The algebra of the random approximate map model"). Either way the PDF metadata is not set to the real title.
  2. `defs.tex` is a stale parallel definition file (different theorem-numbering: it numbers theorems globally, while the active `envnotation.sty` numbers by section). Keeping an unloaded `defs.tex` invites a future editor to "fix" it and silently change numbering.
- **Suggestion**: delete `defs.tex` (it is unused), and add a correct `\hypersetup{pdftitle={The algebra of the random approximate map model}, pdfauthor={Alexander Towell}}` to `main.tex` so the PDF carries proper metadata. (The `main.maf`/`main.mtc*` minitoc artifacts in the directory are also stale build droppings safe to gitignore.)
- **Confidence**: high (confirmed `defs.tex` is not input by `main.tex`).

### m24. No venue/document-class concern, but `\documentclass{article}` with manual title block is venue-neutral (source: format-validator)
- **Location**: `main.tex:2` `\documentclass[11pt,final,hidelinks]{article}` (the commented line 1 shows a prior IEEE `journal/compsoc` class).
- **Problem**: None for the stated target ("no venue selected; review against general theory standards"). Noting only that a prior IEEE class is commented out, so if IEEE is ever targeted, the `minted`/`glossaries`/`microtype` stack and the manual `\maketitle` will need revisiting. No action now.
- **Confidence**: high.

## Build verification checklist
- Compiles: PASS, but **only with `-shell-escape`** (M10). FAIL under the documented command.
- Page count: 24 pages (consistent with the ~27-page estimate in state.md, modulo the orphaned committed `bernoulli-maps-alt.pdf`).
- Undefined references: NONE (PASS).
- Undefined citations: NONE (PASS).
- Multiply-defined labels: NONE in the LaTeX sense; duplicate *PDF anchors* only (m20).
- Overfull/underfull boxes: 1 overfull hbox, 6.1pt (m21). Negligible.
- Glossary/acronym: machinery active, output empty (m22).
- PDF metadata: not set to the real title; `defs.tex` (which would set a wrong title) is not even loaded (m23).
- Float/figure resolution: no missing-figure errors; the paper has no included external figures in the active build (the foundation's tikz `kfold` figure is not in this paper). PASS.
