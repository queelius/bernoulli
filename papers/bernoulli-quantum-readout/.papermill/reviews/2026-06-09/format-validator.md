# Format Validator

**Date**: 2026-06-09
**Scope**: Build verification, label/ref resolution, page count, venue-format fit; regression from the 3.6 addition.

## Build (clean from scratch)

Ran: `pdflatex; bibtex; pdflatex; pdflatex` on a cleaned tree (removed aux/bbl/blg/out/log first).

- **Exit status**: 0 on all passes.
- **Undefined references**: 0.
- **Undefined citations**: 0.
- **Overfull/underfull boxes**: 0.
- **bibtex warnings/errors**: 0.
- **LaTeX warnings** (excluding font/hyperref noise): 0.
- **`??` in log**: none.
- **No `-shell-escape` needed**: confirmed no `_minted-main` directory is created; the paper uses no `minted`. (A stray `_minted-main/*.pygtex` exists under the *sibling* `bernoulli-phf` paper per repo git status, unrelated to this paper.)

## Label / cross-reference resolution

The 3.6 addition defines three new labels, all resolved and referenced cleanly:
- `sec:operator` (line 515)
- `eq:assignment` (line 530), referenced at line 548.
- `eq:parity-spectral` (line 559) [defined; not back-referenced, which is fine for a display equation].

All 31 labels in the file are defined exactly once; every `\cref`/`\Cref`/`\eqref`/`\ref` target resolves to a defined label (cross-checked the full label list against the full reference list). No collisions, no duplicates, no dangling targets.

## Page count

- **14 pages** (was 13 before the 3.6 addition; the new subsection adds about 1 page).

## Venue-format fit (target: *Quantum*, or PRX Quantum)

- The paper uses a standalone `article` class with `natbib`+`plainnat`, not a venue template. For *Quantum* the submission template is `quantumarticle`; for PRX Quantum it is REVTeX. **Neither is used yet.** This is expected at the draft/Zenodo-preprint stage and is a pre-submission conversion task, not a defect of this revision. Flagging so it is on the radar before an actual journal submission.
- 14 pages is within normal range for both venues for a research/perspective article. *Quantum* has no hard page limit; PRX Quantum is also flexible. No length concern.
- Title, author block, ORCID, abstract, and bibliography are all present and well formed. `hyperref` `pdftitle`/`pdfauthor` set; 0 PDF-string warnings.

## Finding F1 (suggestion, pre-submission), venue template not yet applied

**Location**: preamble (line 1, `\documentclass[11pt]{article}`).
**Problem**: A *Quantum* submission needs `\documentclass{quantumarticle}`; PRX Quantum needs REVTeX (`\documentclass[prxquantum,...]{revtex4-2}`). The current standalone `article` setup is correct for a Zenodo preprint but must be converted at submission. The `cleveref` + `natbib` choices are compatible with `quantumarticle`; REVTeX would need citation-command adjustments.
**Suggestion**: When ready to submit, port to `quantumarticle` (lighter lift than REVTeX given the current natbib/cleveref usage). Severity: suggestion; not a regression.

## Verdict
Production-clean build: 0 undefined refs/cites, 0 bad boxes, 0 bibtex warnings, 14 pp. The 3.6 addition introduced no build, label, or formatting regression. The only format item is the pre-submission venue-template conversion (F1), expected at this stage.
