# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research paper: **"Composition of Bernoulli sets"** by Alexander Towell. Derives the set-theoretic compositional algebra of Bernoulli sets: closed-form error rates for complement, union, intersection, and set difference. Establishes monoidal structure under union and intersection, exact formulas for relational predicates (subset, equality probabilities), and interval arithmetic for uncertain rate parameters. Companion to `bernoulli_sets/`, which provides the axioms and distributions assumed here.

## Build

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

`alex.sty` (in project root) provides all notation macros. Loaded as `\usepackage[fancy,section]{alex}`.

## Structure

- `main.tex` — Document root, uses `\input{}` includes
- `sections/` — 6 section files (1:1 with main.tex includes)
- `alex.sty` — Unified notation package (copied from `bernoulli_sets/`)
- `references.bib` — Bibliography

## Section Order

1. intro → 2. preliminaries → 3. set_theory →
4. relational → 5. uncertain_rates → conclusion

## Key Notation (from alex.sty)

- Sets: `\Set{A}`, approximate: `\ASet{A}`, positive: `\PASet{A}`, negative: `\NASet{A}`
- Rates: `\fprate` (FPR ε), `\fnrate` (FNR ω), `\tprate` (TPR τ), `\tnrate` (TNR η)
- Cardinality: `\Card{A}`, random variables: `\RV{X}`
- Set ops: `\SetUnion`, `\SetIntersection`, `\SetComplement`, `\SetDiff`

## Key Conceptual Distinction

**Model order vs. parameter count**: Set-theoretic composition raises the model order (e.g., union of two second-order sets is fourth-order), but Axiom 1 (element-wise independence) forces a Kronecker product factorization of the joint confusion matrix, so parameter count grows linearly ($2m$ for $m$ sets) rather than exponentially ($2^m(2^m-1)$). This is why the closed-form formulas in `tab:set_ops` exist: each entry is a polynomial in the $2m$ per-set rates. See Remark on "Parametric parsimony of composed sets" in `sections/set_theory.tex`.

## Scope Boundaries

This paper covers **set-theoretic composition** of Bernoulli sets. Content that belongs elsewhere:

- **Axioms, distributions, CLT, confidence intervals, higher-order composition**: `bernoulli_sets/`
- **Binary classification measures** (PPV, NPV, accuracy, Youden's J): `bernoulli_classification_measures/`
- **Entropy and space complexity**: `bernoulli_entropy/`

**What stays here**: Error rates for complement, union, intersection, difference; closure properties; monoidal structure; De Morgan duality; partition weight analysis; relational predicates (subset, equality); interval arithmetic for uncertain rates.
