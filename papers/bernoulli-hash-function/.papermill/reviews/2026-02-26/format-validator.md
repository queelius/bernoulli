# Format Validator Report

## Overall Assessment

The paper uses standard LaTeX with a well-structured Makefile build. Several formatting issues exist, including a dead glossary file, potential pgfplots overflow issues, and minor label/reference concerns.

## Findings

### MAJOR-1: gloss.tex is never included
- **Location**: gloss.tex, main.tex
- **Problem**: The file gloss.tex defines glossary entries using \newglossaryentry and \newacronym, but: (a) main.tex never \input{gloss}, (b) no \usepackage{glossaries} is loaded, and (c) no glossary entries are referenced anywhere in the manuscript. The Makefile lists gloss.tex as a source dependency, so changes to it trigger rebuilds, but it has no effect on the output.
- **Suggestion**: Either integrate the glossary (add \usepackage{glossaries}, \input{gloss}, \makeglossaries, \printglossary) or remove gloss.tex from the project and the Makefile.
- **Severity**: Major (dead code in the build system).

### MAJOR-2: pgfplots factorial computation may overflow
- **Location**: Section 3.5, fig_adaptive_fpr (shf.tex lines 395-413)
- **Quoted text**: "x^4 * (1-x)^45 * 50! / (4! * 45!)" and "exp(19*ln(x) + 180*ln(1-x) + ln(200!) - ln(19!) - ln(180!))"
- **Problem**: pgfplots uses TeX's floating-point arithmetic, which has limited precision. The expression "50! / (4! * 45!)" computes 50! directly, which is approximately 3 * 10^64 -- far beyond TeX's floating-point range (typically ~10^{16} for pgfmath). The second plot uses ln(200!) which is also extremely large. The exp() form may work if the logarithms cancel sufficiently, but this is fragile.
- **Suggestion**: Use the logarithmic form consistently for all curves: compute the Beta PDF as exp(alpha-1)*ln(x) + (beta-1)*ln(1-x) - lnBeta(alpha,beta)), where lnBeta is computed via lgamma. Alternatively, precompute the normalization constants and hardcode them. The (m=50, p=5) curve is the most likely to fail numerically.
- **Severity**: Major -- the paper may fail to build or produce incorrect plots on some TeX distributions.

### MINOR-1: Figure 1 (fig_shs) references old file naming
- **Location**: img/fig_shs.tex, img/fig_shs.pdf
- **Problem**: The figure file is named "fig_shs" (Singular Hash Set), reflecting the old paper title. While this does not affect compilation, it is inconsistent with the current "BHF" naming.
- **Suggestion**: Rename to fig_bhf.tex and fig_bhf.pdf for consistency.

### MINOR-2: The figure from img/fig_shs.tex is never included in the manuscript
- **Location**: main.tex, all section files
- **Problem**: Searching for \input{img/fig_shs} or \includegraphics{fig_shs} in the manuscript files yields no results. The figure exists in the img/ directory but is not included anywhere in the paper. The state.md mentions "1 TikZ figure (img/fig_shs.tex)" but it does not appear in the compiled document.
- **Suggestion**: Either include the figure in an appropriate section (e.g., Section 3 to illustrate the acceptance predicate) or remove it from the repository.

### MINOR-3: Missing \usepackage for some features
- **Location**: main.tex, defs.tex
- **Problem**: defs.tex uses \mathbbm{1} (indicator function macro, line 21) which requires the bbm package. The bbm package IS loaded by alex.sty (line 15), so this works. However, defs.tex also uses \mathsmaller in fig_shs.tex which requires the relsize package. If the figure is ever included, this would cause a build failure.
- **Suggestion**: If fig_shs.tex is to be included, add \usepackage{relsize} to main.tex.

### MINOR-4: Theorem numbering may be inconsistent
- **Location**: Throughout
- **Problem**: The paper uses [section] option in alex.sty for theorem numbering. This means theorems are numbered X.Y where X is the section number. However, the state.md references "Theorems 3.5-3.9" while the actual theorem labels are thm:success_adaptive_set, thm:success_adaptive_map, thm:fpr_distribution, thm:adaptive_moments, thm:adaptive_complexity. The user's focus areas reference "Theorems 3.5-3.9" which may not match the compiled numbering if other theorems or definitions share the same counter.
- **Suggestion**: Verify the compiled numbering matches the user's expectations.

### MINOR-5: No page numbers visible in hypersetup
- **Location**: main.tex, line 33
- **Problem**: hypersetup has colorlinks=false, which means hyperlinks are boxed (default) or invisible. Combined with hidelinks option on hyperref (line 18), all links are invisible. This is fine for a printed paper but makes the PDF less navigable.
- **Suggestion**: Consider colorlinks=true with subtle colors for the digital version.

## Build System

- **Makefile**: Well-structured with all, draft, clean, cleanall, watch, wc, help targets.
- **Dependencies**: Correctly lists all source files.
- **Build command**: pdflatex + bibtex + 2x pdflatex (standard).
- **Known requirement**: alex.sty must be in the same directory (it is).

## Label Resolution

All \cref and \Cref references appear to have corresponding \label definitions. No obvious broken references detected from static analysis. Full verification requires a build.
