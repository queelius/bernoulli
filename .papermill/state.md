# Papermill State

## Meta
- **initialized**: 2026-03-18
- **last_refreshed**: 2026-03-18
- **format**: LaTeX (pdflatex)
- **build**: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- **repo**: https://github.com/queelius/bernoulli_classification_measures

## Author
- **name**: Alexander Towell
- **email**: lex@metafunctor.com
- **orcid**: 0000-0001-6443-9897
- **institution**: Southern Illinois University Edwardsville
- **degrees**: MS Computer Science (SIUE, 2015), MS Mathematics (SIUE, 2023)

## Paper
- **title**: Binary classification measures for random approximate sets
- **stage**: drafting (near-complete)
- **pages**: 14
- **line_count**: ~840 (source .tex files)

## Thesis
The Bernoulli set axioms (element-wise independence, homogeneous rates) guarantee that true positive and false positive counts are independent binomial random variables over disjoint populations. This structure makes the delta method directly applicable to any classification measure expressible as a ratio of these counts. We exploit this to derive closed-form expected values and variances for PPV, NPV, F1, accuracy, and Youden's J. The key practical consequence is prevalence sensitivity: data structures with nominally small FPR can have near-zero precision when the positive base rate is low, a regime common in information retrieval and database applications.

### Thesis structure
1. **Structural insight**: Bernoulli axioms produce independent binomials over disjoint populations
2. **Method**: Delta method applied systematically to ratio-of-binomials measures
3. **Results**: Closed-form E[.] and Var[.] for PPV, NPV, F1, accuracy, Youden's J
4. **Consequence**: Prevalence sensitivity has practical design implications for approximate data structures

## Structure
| File | Section | Purpose | Lines |
|------|---------|---------|-------|
| `main.tex` | (root) | Document root, preamble, macros | 96 |
| `sections/intro.tex` | 1. Introduction | Motivation, contribution, related work, organization | 30 |
| `sections/preliminaries.tex` | 2. Preliminaries | Bernoulli axioms, binomial error count theorems | 99 |
| `sections/measures.tex` | 3. Binary classification measures | PPV, accuracy, NPV, Youden's J, F1, summary table, interval measures | 409 |
| `sections/appendix.tex` | A-C. Appendices | PPV proof (A), F1 proof (B), sampling distribution framework (C) | 187 |
| `sections/conclusion.tex` | 4. Conclusion | Summary, open problems (MCC, correlated errors) | 19 |

## Notation
- Uses `alex.sty` (unified package, `\usepackage[fancy,section]{alex}`)
- Key macros: `\ASet`, `\Set`, `\fprate` (ε), `\tprate` (τ), `\fnrate` (ω), `\tnrate` (η)
- RV macros: `\PPV`, `\NPV`, `\ACC`, `\Fone`, `\TP`, `\FP`, `\FN`, `\TN`
- Lowercase deterministic: `\ppv`, `\npv`, `\acc`, `\fone` (via `\SetKwFunction` or `\mathrm`)
- Operators: `\Expect{}`, `\Var{}`, `\Prob{}`

## Data & Simulations
| File | Description |
|------|-------------|
| `data/prec_vs_fprate{1,2,3}.csv` | Theoretical E[PPV] curves at λ=0.1%, 1%, 10% |
| `data/ppv_sim_vs_theory.csv` | Monte Carlo PPV validation (N=50000, p=100, n=9900) |
| `data/f1_theory.csv` | Theoretical E[F1] curve (λ=1%) |
| `data/f1_sim_vs_theory.csv` | Monte Carlo F1 validation (N=50000, p=100, n=9900) |
| `code/f1_sim.py` | F1 simulation script (numpy, seed=42) |

## Figures
| Label | Description | Page |
|-------|-------------|------|
| `fig:prec_vs_fprate_and_fnrate` | PPV histograms for several (ε,τ) pairs | 4 |
| `fig:ppv_vs_fprate` | E[PPV] vs ε at three prevalences | 5 |
| `fig:ppv_theory_vs_sim` | PPV theory vs Monte Carlo | 6 |
| `fig:f1_theory_vs_sim` | F1 theory vs Monte Carlo | 8 |

## References
- 11 entries in `references.bib`
- 9 cited in paper (2 unused: `feller2`, `coverThomas`)
- Key: `bernoulliSets` (companion), `bernoulliComposition` (companion), `casellaBerger` (delta method), `fawcettROC`, `powersEval`

## Companion Papers
This paper is part of a 4-paper family:
1. `bernoulli_sets`: Core model (axioms, distributions, composition theorem)
2. `bernoulli_composition`: Set-operation error rates, monoidal structure, interval arithmetic
3. **`bernoulli_classification_measures`**: this paper
4. `bernoulli_entropy`: Joint entropy, space complexity lower bounds

## DOI
- **doi**: 10.5281/zenodo.19104550
- **url**: https://zenodo.org/record/19104550
- **minted**: 2026-03-18

## Venue
- **target**: not yet selected
- **candidates**: to be evaluated

## Reviews
- None yet

## Open Problems (from conclusion)
1. Matthews correlation coefficient (MCC) under Bernoulli model: more complex ratio of binomials
2. Correlated error models (relaxing element-wise independence)
3. Prevalence interaction with higher-order composition algebra
