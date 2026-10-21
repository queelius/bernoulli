# Errata: Composition of Bernoulli sets

Date: 2026-10-21. Author: Alexander Towell.

This is the final version of the preprint. It will be deposited on Zenodo as a
new version under concept DOI 10.5281/zenodo.19105387, superseding version
10.5281/zenodo.19105388 (v1.0.0). It is superseded by the monograph *Bernoulli
Types: Two-Sided Error in Approximate Membership, Retrieval, and Computation*,
Chapter 6 (Composition of Sets), with the Boolean groundwork in Chapter 3
(Boolean Algebra Under Noise)
(<https://metafunctor.com/latex/bernoulli-monograph/book.html>). The subset and
equality probabilities (Section 4) and the interval treatment (Section 5) have
no monograph counterpart. License unchanged: CC BY 4.0.

A "Status and errata (October 2026)" box now follows the abstract.

## Corrections

1. **Abstract, Introduction ("Contribution" renamed "Scope and prior work"),
   Conclusion (`main.tex`, `sections/intro.tex`, `sections/conclusion.tex`).**
   The previous version said every operation yields a Bernoulli set "whose
   error rates are computable functions of the operand rates" and that the
   formulas "apply immediately, yielding closed-form error rates and confidence
   intervals for any set-theoretic expression". The single (FPR, FNR) pair of a
   composed set is a cardinality-weighted marginal over operand regions; it does
   not determine the per-element rates, so reusing it as input to a further
   operation is wrong in general. The text now says the formulas apply region by
   region, and that the marginal pair is not valid input for further
   composition. Why: two-rate pairs do not propagate through arbitrary formulas
   (the same failure found in the quantum-readout paper).
2. **Section 3.5, new remark "Nested expressions" (`sections/set_theory.tex`).**
   Gives the counterexample: every operand with FPR 0.02 and FNR 0.10, the
   expression (A1 ∩ A2) ∪ A3; an element in A2 only is reported with
   probability 1 − (1 − 0.02·0.90)(1 − 0.02) = 0.03764, an element in none with
   1 − (1 − 0.02²)(1 − 0.02) = 0.020392. Both are negatives of the output, so no
   single FPR for A1 ∩ A2 reproduces both. Also states the exception: union-only
   expressions have a uniform FPR and intersection-only expressions a uniform
   FNR, which do compose.
3. **Section 3, cross-set independence (`sections/set_theory.tex`).** Now marked
   as an assumption added to the axioms (not implied by them), with its failure
   modes: a reused operand (A ∪ A has FPR ε, not 1 − (1 − ε)²) and filters
   sharing hash functions and seeds.
4. **Section 3.7, monoidal structure remark.** The fold is exact for realized
   sets and per-region rates; folding the marginal pairs of Table 1 is exact
   only for the uniform rate (union FPR, intersection FNR). Operands must be
   distinct and independent. The conclusion now states the monoid structure
   only at the level of realized sets.
5. **Section 3.7, asymptotics.** The previous text said composed rates "inherit
   the Bernoulli structure" so the binomial normal approximation applies. A
   marginal rate that averages regions has a Poisson-binomial error count; its
   variance is the sum of per-region variances, at most the binomial variance at
   the marginal rate.
6. **Section 4, subset corollary (`sections/relational.tex`).** The corollary
   for sets with FPR 0 called them "positive approximate sets", contradicting
   Section 3's convention (positive means FNR 0). Relabeled as sets with no
   false positives (negative Bernoulli sets); the math (1 − τ1 ω2)^|X| is
   unchanged. Added the positive (FNR 0) case, (1 − ε1 η2)^(|U| − |Y|).
7. **Section 5.1 (`sections/uncertain_rates.tex`).** Endpoint bounds hold for
   known partition weights; with uncertain weights the extremes of each
   weighted rate lie at vertices of the weight simplex.

## Citations added

Each DOI was checked against the Crossref REST API on 2026-10-21 (title and
authors match).

- `warner1965randomized`: S. L. Warner, *Randomized Response: A Survey
  Technique for Eliminating Evasive Answer Bias*, JASA 60(309) (1965).
  10.1080/01621459.1965.10480775
- `bloom1970`: B. H. Bloom, *Space/time trade-offs in hash coding with
  allowable errors*, CACM 13(7) (1970). 10.1145/362686.362692
- `broderMitzenmacher2004`: A. Broder, M. Mitzenmacher, *Network Applications of
  Bloom Filters: A Survey*, Internet Mathematics 1(4) (2004).
  10.1080/15427951.2004.10129096
- `papapetrou2010`: O. Papapetrou, W. Siberski, W. Nejdl, *Cardinality
  estimation and dynamic length adaptation for Bloom filters*, Distributed and
  Parallel Databases 28(2-3) (2010). 10.1007/s10619-010-7067-2
- `parker1975`: K. P. Parker, E. J. McCluskey, *Probabilistic Treatment of
  General Combinational Networks*, IEEE Trans. Computers C-24(6) (1975).
  10.1109/T-C.1975.224279
- `krishnaswamy2008ptm`: S. Krishnaswamy, G. F. Viamontes, I. L. Markov,
  J. P. Hayes, *Probabilistic transfer matrices in symbolic reliability analysis
  of logic circuits*, ACM TODAES 13(1) (2008). 10.1145/1297666.1297674
- `dalvi2007`: N. Dalvi, D. Suciu, *Efficient query evaluation on probabilistic
  databases*, VLDB Journal 16(4) (2007). 10.1007/s00778-006-0004-3

## Claims withdrawn or narrowed

- Novelty of the union/intersection/difference rules: withdrawn. They are the
  independent-OR/AND rules of Bloom filter analysis, combinational-logic signal
  probability, and probabilistic databases.
- "Closed-form error rates and confidence intervals for any set-theoretic
  expression": narrowed to region-by-region application.
- "Commutative monoids" of Bernoulli sets: narrowed to realized sets and
  per-region rates.

## Build

`pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`:
0 errors, 0 undefined references, 0 undefined citations, 0 BibTeX warnings,
16 pages. The status box renders on page 1.

## Known remaining issues (not fixed in the freeze)

- Remarks in `alex.sty` are unnumbered, so `\cref` to a remark label resolves to
  the enclosing subsection; references to remarks are written in words.
- The May 2026 review items on exposition (notation switches in Section 4,
  unnamed relational results, unproven monotonicity signs) are not addressed.
- Companion citations remain `@Unpublished` entries without DOIs.
