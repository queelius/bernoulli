# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research paper: **"Bernoulli sets: a model for random approximate sets"** by Alexander Towell. Formalizes *random approximate sets* (Bernoulli sets) — probabilistic sets that approximate an objective set with quantifiable false positive/negative rates. Establishes the axioms, derives binomial error-count distributions, asymptotic limits, confidence intervals, and the higher-order composition theorem. Applications include Bloom filters, perfect hash filters, and any implementation satisfying the Bernoulli axioms.

This paper absorbed content from the former `bernoulli_sets_higher_order` paper. Original files preserved in `archive.zip`. Set-theoretic composition (complement, union, intersection, difference, monoidal structure, relational predicates, interval arithmetic) was extracted to `bernoulli_composition/`. Classification measures (PPV, NPV, accuracy, Youden's J) were extracted to `bernoulli_classification_measures/`. Entropy and space complexity were extracted to `bernoulli_entropy/`.

## Build

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

`alex.sty` (in project root) provides all notation macros. Loaded as `\usepackage[fancy,section]{alex}`.

## Structure

- `main.tex` — Document root, uses `\input{}` includes
- `sections/` — 5 active section files (1:1 with main.tex includes); `entropy.tex`, `set_theory.tex`, `relational.tex`, `uncertain_rates.tex` retained but no longer `\input`'d
- `alex.sty` — Unified notation package
- `img/` — TikZ figures
- `data/` — CSV datasets (17 files)
- `code/` — C++ Monte Carlo simulations (`ppv.cpp`, `bin_class_measures_sim.cpp`)
- `research/` — Mathematica notebooks, Maxima scripts, R source, figure SVGs
- `archive.zip` — Old section files and drafts preserved from cleanup

## Section Order

1. intro → 2. algebra_of_sets → 3. bernoulli_model →
4. distributions → appendix

## Key Notation (from alex.sty)

- Sets: `\Set{A}`, approximate: `\ASet{A}`, positive: `\PASet{A}`, negative: `\NASet{A}`
- Rates: `\fprate` (FPR ε), `\fnrate` (FNR ω), `\tprate` (TPR τ), `\tnrate` (TNR η)
- Functions: `\APFun{f}[\fprate][\tprate]` — approximate function with error rates
- Cardinality: `\Card{A}`, random variables: `\RV{X}`
- Set ops: `\SetUnion`, `\SetIntersection`, `\SetComplement`, `\SetDiff`

## Conceptual Layers

1. **Set algebra** → 2. **Bernoulli model** (FPR/FNR axioms, model order = block count) → 3. **Higher-order models and k-fold composition** → 4. **Error count distributions** (binomial FP/FN/TP/TN, CLT, confidence intervals)

## Key Conceptual Distinction

**Model order vs. parameter count**: Model order counts partition blocks (how many distinct error regimes exist). A general $n$-th order channel on $k$ output symbols has $n(k-1)$ free parameters. For a single Boolean membership test ($k=2$), this gives $n$ parameters. But for $m$ joint tests ($k=2^m$), a general model has $n(2^m-1)$ parameters. Axiom 1 (element-wise independence) forces a Kronecker product factorization, reducing parameters from $n(2^m-1)$ to at most $2m$. Example: union of two second-order sets is fourth-order but has 4 parameters, not 12. These concepts are orthogonal: order constrains which confusion matrix rows are identical, independence constrains the internal structure of each row. See Remark 3.4 (parametric parsimony) in `sections/bernoulli_model.tex`.

## Scope Boundaries

This paper covers the **foundational model**. Content that belongs elsewhere:

- **Set-theoretic composition** (complement, union, intersection, difference, monoidal structure, relational predicates, interval arithmetic): `bernoulli_composition/`
- **Binary classification measures** (PPV, NPV, accuracy, Youden's J, delta method): `bernoulli_classification_measures/`
- **Entropy and space complexity** (joint entropy, Carter et al. lower bound): `bernoulli_entropy/`
- **Approximate Boolean functions** (AND, OR, NOT as maps): `bernoulli_maps/`
- **Algebraic types** (Bool as a type, sum/product types, computational basis): `bernoulli_data_type/`
- **Relational operators** (join, project over approximate relations): `bernoulli_relations/`

**What stays here**: The Bernoulli axioms, binomial distributions of error counts (FP/FN/TP/TN), asymptotic limits and confidence intervals, higher-order composition theorem (k-fold composition via channel matrices), abstract data type formulation, probability space, and the Boolean universe example.
