# Format validator (re-review)

Date: 2026-06-07 (re-review of revision commit 6f136b7)
Scope: verify the build is clean after the revision, the four hyperref PDF-string
warnings are gone, and the new table/subsection introduced no label or layout
defects.

## Build

Command (the charter's build line) run fresh:
  pdflatex -interaction=nonstopmode main.tex
  bibtex main
  pdflatex -interaction=nonstopmode main.tex
  pdflatex -interaction=nonstopmode main.tex

Result: clean.
- Pages: 13 (up from 11 pre-revision; the +2 pages are the new Subsection 4.4
  and Table 2, plus the expanded sec:scope item 2 and the longer sec:related).
- Undefined references / citations: 0 (grep of the final pass log).
- Multiply-defined labels: 0.
- Overfull / underfull boxes: 0.
- bibtex: 0 warnings, 0 errors.

## Hyperref PDF-string warnings (prior minor m7)

RESOLVED. The fresh build (all three pdflatex passes) reports ZERO "Token not
allowed in a PDF string (Unicode)" warnings. Verified directly: build pass 1, 2,
and 3 each report a count of 0.

The fix is correctly in place:
- \hypersetup{pdftitle={A Forward (epsilon, omega) Calculus ...}} provides an
  ASCII pdftitle, so the math in the \title no longer leaks into the PDF string.
- The one math-bearing section heading, "The forward (eps, omega) calculus," is
  wrapped: \section{The forward \texorpdfstring{$(\eps,\omega)$}{(epsilon,
  omega)} calculus}. This is the only heading containing math; all others are
  plain text, so no further \texorpdfstring is needed.

(Note: a naive grep across /tmp matched stale logs from other papers in the
monorepo; the relevant fresh logs for THIS paper's three passes are all 0. The
prior four warnings are gone.)

## New table and subsection: label/layout integrity

- tab:syndrome-asym: defined (\label{tab:syndrome-asym}), resolves to "Table 2"
  via cleveref, newlabel present in main.aux. The table uses booktabs and a
  3-column tabular; it typesets without an overfull box.
- sec:worked-asym: defined (\label{sec:worked-asym}), resolves to "Subsection
  4.4", newlabel present in main.aux.
- tab:syndrome (Table 1) renumbered cleanly alongside the new Table 2; all
  \Cref{tab:syndrome} and \Cref{tab:syndrome-asym} references resolve to the
  correct numbers.
- No label collision between the two tables.

## All-labels resolution

Every \ref / \cref / \Cref target resolves; the .aux carries newlabel entries for
all theorem environments, equations, sections, and both tables. No "??" in the
output.

## New formatting findings introduced by the revision

None. The build is production-clean, the PDF-string warnings are eliminated, and
the new table and subsection integrate without any label or box defect.

## Verdict

Production-clean (13 pp, 0 undefined refs/cites, 0 bad boxes, 0 bibtex warnings,
0 hyperref PDF-string warnings). Prior minor m7 RESOLVED. No new formatting issue.
