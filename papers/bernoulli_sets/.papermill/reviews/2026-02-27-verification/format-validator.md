# Format Validator Report

## Summary
The paper compiles cleanly with pdflatex. 40 pages, 24 citations, 6 figures, 2 tables. No undefined references or citations. Minor formatting issues: orphaned \index{} commands, PDF inclusion warnings from img/out.pdf, and some stylistic inconsistencies.

## Build Verification
- **Engine**: pdflatex
- **Build command**: pdflatex + bibtex + pdflatex + pdflatex
- **Result**: Compiles successfully, output written to main.pdf (40 pages)
- **Warnings**: microtype spacing warning for TS1/lmr font (benign); potential PDF inclusion warnings from img/out.pdf

## Label/Reference Resolution
- All \label{} definitions in compiled sections have corresponding \cref{} or \Cref{} references
- No undefined references
- No undefined citations
- hypertexnames=false correctly prevents hyperref naming conflicts

## Structural Issues

### 1. Orphaned \index{} commands (3 instances)
- sections/algebra_of_sets.tex line 7: `\index{set}`
- sections/entropy.tex line 125: `\index{information-theoretic lower-bound}`
- sections/entropy.tex line 129: `\index{false positive rate}`

makeindex is not enabled (the \makenomenclature line in main.tex is commented out, and \makeindex is not called). These \index{} commands are silently ignored.

**Suggestion**: Remove the \index{} commands or enable indexing if an index is desired.

### 2. Non-compiled section files
Two section files exist but are not included in main.tex:
- sections/algebraic_structure.tex (content folded into Section 5 remark)
- sections/adt.tex (content incorporated into Section 3.1)

Neither causes compilation issues. The non-compiled files contain labels that do not conflict with compiled labels.

### 3. img/out.pdf may cause PDF inclusion warnings
The img/out.pdf file (14KB) is included via pdf_tex from Inkscape/TikZ. Multi-object PDFs can generate pdfTeX warnings. This does not affect correctness.

## Formatting Details

### Package Loading
- microtype loaded with full settings (tracking, kerning, spacing)
- hyperref loaded with hypertexnames=false (prevents label conflicts)
- cleveref loaded after hyperref (correct order)
- natbib with [square, numbers] (produces [1]-style citations)

### Typography
- 11pt, lmodern font
- 1-inch margins
- Equation numbering by section (numberwithin{equation}{section})
- Theorem numbering by section via alex.sty

### Figures
All 6 figures compile correctly:
1. Figure 2.1: Venn diagram (img/aset_fp_fn.tex via \input)
2. Figure 4.1: PPV histogram (img/out.pdf_tex via \input)
3. Figure 4.2: PPV vs FPR (pgfplots, data/ CSV files)
4. Figure 4.3: PPV theory vs Monte Carlo (pgfplots, data/ CSV files)
5. Figure 3.2: k-fold composition (pgfplots, inline coordinates)
6. Figure 5.1: Union FPR (pgfplots, analytic functions)
7. Figure 8.1: Space lower bound (pgfplots, analytic functions)

(Note: 7 figures total, not 6 as stated in state.md)

### Tables
2 tables:
1. Table 2.1: Contingency table (algebra_of_sets.tex)
2. Table 4.1: Performance measures (distributions.tex)
3. Table 5.1: Set operation error rates (set_theory.tex)

(Note: 3 tables total, not 2 as stated in state.md)

## Minor Issues

1. The state.md counts are slightly off: "6 figures" should be 7; "2 tables" should be 3.
2. The appendix proof equation counter resets inside proofs (via alex.sty). This is intentional but may be confusing if readers reference proof-internal equations by their (a), (b), etc. labels.
