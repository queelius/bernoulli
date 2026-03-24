# Format Validator Report (Post-Revision)

**Date**: 2026-02-26
**Paper**: Bernoulli sets

## Build Status

```
Engine: pdflatex
Output: 39 pages
Errors: 0
Warnings: 4
  - Overfull \hbox (8.02pt) at bernoulli_model.tex lines 255-257
  - Overfull \hbox (8.68pt) at bernoulli_model.tex lines 289-291
  - Overfull \hbox (7.74pt) at set_theory.tex lines 629-632
  - Package microtype: spacing list not found for TS1/lmr/m/n/10.95
Undefined references: 0
Undefined citations: 0
Multiply defined labels: 0
```

## Formatting Checks

| Check | Status | Notes |
|---|---|---|
| Clean build | PASS | 0 errors |
| Label resolution | PASS | All labels resolve |
| Citation resolution | PASS | All citations resolve |
| Hyperref | PASS | hypertexnames=false set |
| pdftitle | PASS | Matches document title |
| Date | PASS | Shows "2026" |
| Page count | 39 | Down from 43 (removed 2 sections) |
| Bibliography | 23 entries | 3 orphaned in .bib but excluded from .bbl |

## Issues

### Figure 1 caption placement
- **Location**: algebra_of_sets.tex lines 46-52
- **Problem**: \caption before \input, placing caption above figure
- **Severity**: Minor

### Overfull hboxes (3)
- All under 9pt, acceptable for draft
- The two in bernoulli_model.tex (lines 255-257, 289-291) are in the Membership Boolean remark where long inline math causes overflow
- The one in set_theory.tex (lines 629-632) is in the convergence remark

### Dead \index{} commands
- 3 instances (entropy.tex:124,128; algebra_of_sets.tex:7)
- Nomencl/index package is commented out (main.tex:24-25)
- Harmless but dead code

### Commented-out code
- main.tex line 24-25: nomencl package commented out
- distributions.tex has scattered commented-out lines (harmless)

## Post-Revision Improvements

1. **hypertexnames=false**: Previously reported as needed; now set in main.tex
2. **pdftitle**: Now matches document title
3. **Boolean search section**: Cleanly removed; no orphaned labels or references

## Overall: Build is clean. One minor formatting issue (Figure 1 caption).
