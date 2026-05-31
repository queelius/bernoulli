# Format Validator Report, bernoulli_relations

**Agent**: format-validator (build verification, label resolution, venue formatting)
**Date**: 2026-05-29
**Verdict**: Does not build. Fatal before reaching bibliography. Multiple independent build-blockers.

## Build attempts (reproduced)

Command per CLAUDE.md: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`

### Attempt 1: as documented (no flags)
```
! Package minted Error: You must invoke LaTeX with the -shell-escape flag.
==> Fatal error occurred, no output PDF file produced!
EXIT CODE 1
```
The documented build command is itself wrong: `main.tex` loads `\usepackage{minted}`, which requires `-shell-escape`. The build command in both `CLAUDE.md` and `.papermill/state.md` omits the flag, so following the documented instructions fails on the first line.

### Attempt 2: add `-shell-escape` (the obvious fix)
```
! LaTeX Error: File `sections/intro.tex' not found.
==> Emergency stop.
==> Fatal error occurred, no output PDF file produced!
EXIT CODE 1
```
The first `\subfile{sections/intro}` points to a file that does not exist. The build dies here and never reaches `\bibliography{references}`.

## CRITICAL build-blockers (each independently fatal)

### C-F1. Missing subfiled section files (5 of 10)
`main.tex` issues ten `\subfile{}` calls. Five target files that are absent from disk:

| `\subfile{}` target | On disk? |
|---|---|
| `sections/intro.tex` | MISSING |
| `sections/relations.tex` | present |
| `sections/approx_rel_model.tex` | present |
| `sections/rel_algebra.tex` | MISSING |
| `sections/properties.tex` | present |
| `sections/predicates.tex` | present |
| `sections/test.tex` | MISSING |
| `sections/unused/optimality.tex` | MISSING (the `unused/` dir does not exist) |
| `sections/unused/oblivious_rel_model.tex` | MISSING (file exists one level up at `sections/oblivious_rel_model.tex`) |
| `sections/appendix.tex` | commented out (not a blocker) |

LaTeX aborts on the first missing file (`intro`). Even after stubbing `intro`, it will abort again on `rel_algebra`, then `test`, then the two `unused/` paths. The paper cannot compile until all five are created or the `\subfile{}` lines are removed/redirected. This is a larger defect than the state file recorded (the state file noted only the missing bibliography).

**Fix**: create the five missing files (even as one-line stubs to restore a clean build), OR comment out the four `\subfile{}` lines whose content is not ready and redirect the fifth (`sections/unused/oblivious_rel_model` to the existing `sections/oblivious_rel_model.tex`). Bring `main.tex`'s subfile list into 1:1 correspondence with files on disk.

### C-F2. No `references.bib`, yet `\bibliography{references}` is declared (the top reported issue per brief)
`main.tex` line 121 declares `\bibliography{references}`, but no `references.bib` exists anywhere in the tree (confirmed by `find ... -name '*.bib'`: none). Consequences once the C-F1 blockers are cleared:
- `bibtex main` fails (currently it even fails to open `main.aux`, because the earlier fatal error prevents the `.aux` from being written).
- Every `\cite` renders as `[?]`.
- `natbib` plus `cleveref` emit "There were undefined references" / "Citation undefined" on every pass.

The distinct citation keys that must be defined in a created `references.bib` are: `aset`, `bf`, `phf`, `approxrel`. The foundation paper `bernoulli_sets/references.bib` already defines `bf` and `phf` verbatim, so a `references.bib` can be seeded by copying the relevant entries from the foundation paper and adding an `aset` entry (the foundation paper itself), an `approxrel` self-reference, plus the external anchors flagged by the citation verifier.

This is a known, pre-existing gap (recorded in the state file), not a regression. It is reported here as the headline formatting issue per the review brief. Note, however, that it is currently *masked* by C-F1: the build dies before bibtex runs, so fixing the bibliography alone will not produce a PDF.

### C-F3. `\sections{...}` typo (would be fatal if the file were built)
`sections/constrained_ras.tex` line 4 calls `\sections{Random approximate sets with invariants}` (`\sections`, not `\section`). `\sections` is undefined and would throw "Undefined control sequence." This file is *not currently subfiled* by `main.tex`, so it does not block today's build, but it is dead/orphaned content (see M-F1) that, if wired in, breaks immediately.

## MAJOR issues

### M-F1. Orphaned section files not referenced by `main.tex`
- `sections/constrained_ras.tex` (9.3 KB of theorem content on Cartesian products, power sets, disjoint unions) is on disk but never subfiled. Either intended content that was dropped from the build, or abandoned. The power-set false-positive-rate theorem here is substantive and currently invisible to the compiled paper.
- `sections/oblivious_rel_model.tex` exists at `sections/`, but `main.tex` asks for `sections/unused/oblivious_rel_model.tex`. The path mismatch means the oblivious-database application (the paper's headline application in the abstract) is not in the build at all.

### M-F2. Unresolved cross-references with placeholder keys
Independent of the bibliography, the following `\cref`/`\ref` targets have no matching `\label` anywhere in the manuscript and will render as `??`:
- `\cref{?}` (predicates.tex) and `\cref{??}` (predicates.tex, commented region): literal placeholder keys.
- `\cref{dummyrefs}` (predicates.tex).
- `\cref{sec:bool_search}` (predicates.tex): no such label.
- `\cref{sec:powerset}` (predicates.tex): no such label.
- `\cref{thm:true_subset_rate}` (predicates.tex): no such theorem labeled.
- `\ref{thm:subset}` (predicates.tex): no such theorem labeled.
- `\cref{table:mathrel_vsrelmodel}` (oblivious_rel_model.tex) vs. the defined label `tab:mathrel_vsrelmodel`: label/ref spelling mismatch (`table:` vs `tab:`), so even this one fails.

Every one of these produces a dangling reference. Several sit inside otherwise-complete derivations, so they are not merely cosmetic.

### M-F3. Glossary machinery loaded but unused
`main.tex` loads `\usepackage[xindy,toc,acronyms,symbols]{glossaries}` and calls `\printglossary`, but `\loadglsentries{gloss}` and `\include{defs}` are commented out and no glossary entries are defined. `\printglossary` with no entries, and with `xindy` selected, adds a `makeglossaries` step to the real build (not in the documented command) and yields an empty glossary. Either populate it or drop the package and `\printglossary`.

## MINOR issues

- **MIN-F1**. `\graphicspath{img}` (line 74) is missing the standard brace-group form `\graphicspath{{img/}}` used by the foundation paper. With no figures currently included this is latent, but it will not find `img/` assets when added.
- **MIN-F2**. Documented build command is incomplete on two counts: missing `-shell-escape` (minted) and missing `makeglossaries` (glossaries plus xindy). The correct invocation, once sources are fixed, resembles the `bernoulli-phf` pattern: `pdflatex -shell-escape main.tex && makeglossaries main && bibtex main && pdflatex -shell-escape main.tex && pdflatex -shell-escape main.tex`. Update `CLAUDE.md` and `state.md` accordingly.
- **MIN-F3**. No target venue selected (`state.md` venue: null). The `article` class with `[journal,compsoc]` commented out suggests an IEEE target was once considered. Formatting cannot be validated against a venue until one is chosen; the relational-algebra angle suits a database/theory venue (see literature context).
- **MIN-F4**. Stale build artifacts in the working tree: `main.log` (54 KB), `main.mtc`, `main.mtc0`. Per repo policy these are gitignored build artifacts and should not be tracked; confirm they are not staged.

## Label inventory (defined, for reference)
Defined and resolvable (once the build runs): `asm:ber_trial`, `def:approx_pfun`, `def:approx_rel`, `sec:map`, `sec:prob_model`, `sec:relations`, `tab:mathrel_vsrelmodel`, `tbl:ex_join`, `tbl:ex_proj`, `tbl:ex_r1`, `tbl:ex_r2`, `tbl:partialfunc`, `tbl:relation_derived`, `tbl:relation`, `thm:fpbinom`, `thm:fpr`. Resolvable cref consumers of these are fine; the broken set is listed in M-F2.

## Summary for synthesis
- Critical: 3 (C-F1 missing sections, C-F2 missing bibliography, C-F3 `\sections` typo in orphaned file)
- Major: 3 (M-F1 orphaned files including the abstract's headline application, M-F2 dangling cross-refs, M-F3 empty glossary)
- Minor: 4
The build is multiply broken. The missing-bibliography issue (the brief's headline) is real and must be fixed, but it is currently downstream of the missing-section-files fatal error; both must be resolved before any PDF is produced.
