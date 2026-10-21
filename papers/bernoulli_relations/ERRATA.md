# Errata: Error contracts for approximate relations

Date: 2026-10-21. Author: Alexander Towell.

This is the final version of the preprint. It will be deposited on Zenodo as a
new version under concept DOI 10.5281/zenodo.20602265, superseding version
10.5281/zenodo.20618109 (v5, 2026-06-10). It is superseded by the monograph
*Bernoulli Types: Two-Sided Error in Approximate Membership, Retrieval, and
Computation*, Chapter 12, "Approximate Relations"
(<https://metafunctor.com/latex/bernoulli-monograph/book.html>).
License unchanged: CC BY 4.0.

**Title change.** v5 was titled *The abstract data type of the approximate
relation*. This version is titled *Error contracts for approximate relations*,
matching the narrower scope of the October 2026 revision.

## Corrections

The mathematical corrections below come from the October 2026 revision
(committed as `30aa1e2`; evidence in `.research/relations-revision/math-audit.md`
and `claims.md` at the monorepo root). They are listed relative to v5. The
freeze itself adds only the status box, the citations below, and this file.

1. **Projection (`sections/rel_algebra.tex`).** v5 said projection raises the
   model order "while preserving element-wise independence". Projected tuples
   whose fibers share a source are correlated; the covariance is now given
   exactly (`thm:project_sources`). Rate profiles must record the true-member
   count of the fiber as well as its fan-in: at (epsilon, tau) = (.05, .9) and
   fan-in 3, one true member gives TPR .90975 and two give .9905.
2. **Join (`sections/rel_algebra.tex`).** v5 said a query assuming independent
   rows "understates the joint error". The shared-left covariance a(1-a)b1 b2 is
   positive only under stated interior-rate conditions, disjoint-source joins
   stay independent, and the all-absent corner need not understate other regions.
3. **Transitivity (`sections/properties.tex`).** v5 said transitivity's
   preservation probability vanishes (and vanishes fastest), using an argument
   that treated true premises as reported premises and a product over
   overlapping triples. Replaced by a sufficient upper bound
   (1 - min(epsilon,tau)^2 (1 - max(epsilon,tau)))^floor(n/3) over
   vertex-disjoint triples for fixed interior rates. The empty relation with
   epsilon = 0 is a counterexample to unconditional vanishing. The vanishing
   statements for reflexivity, symmetry and single-valuedness are kept, with
   their interior-rate hypotheses stated.
4. **Closure dichotomy (`sections/properties.tex`).** v5 claimed a dichotomy
   between free equivalence-induced invariants and cascading transitivity.
   Withdrawn; the retained theorems concern specific orbit constructions and
   simultaneous-addition rounds (ceil(log2 k) rounds, binom(k+1,2) final size
   for a path). A diagonal orbit has one trial, not two; OR-closure equalities
   use the actual orbit size, with a maximum size giving bounds only.
5. **Single-valuedness (`sections/properties.tex`).** The v5 preservation
   probability is replaced by the exact formula q1^d q0^u over defined and
   undefined rows. The old (1-epsilon)^(v-1) expression is kept only for the
   distinct no-spurious-value event. Deletion repair (uniform tie-breaking
   sampled once per row) is now specified.
6. **Space surcharge (`sections/properties.tex`).** The v5 "log2 m-bit surcharge
   buying an m-trial recall boost" is restated as conditional rate accounting
   under an assumed -log2(epsilon) cost scale; it is not a space lower bound,
   and the zero-false-negative membership bound cannot price a recall improvement.
7. **Partial functions (`sections/properties.tex`).** The v5 definition
   equated the approximate partial function with the full Cartesian universe
   and specified only domain rates. It is now a random relation whose every
   realization is single-valued, with wrong-value errors separated from domain
   false positives and negatives. The unsupported map-composition closure claim
   is replaced by a scoped companion citation.
8. **Encrypted search (`sections/oblivious_rel_model.tex`).** The claim that
   false-positive and false-negative rates characterize leakage or security is
   withdrawn; rates specify functionality only.

Added in the October revision (not corrections): query error contracts
(`sections/query_contracts.tex`) and a stored partitioned-Bloom calibration
study (`sections/calibration.tex`, `code/`, `data/calibration/`).

## Citations added in the freeze

Each DOI was checked against the Crossref REST API on 2026-10-21 (title and
authors match).

- `fuhr1997pra`: N. Fuhr and T. Rölleke, *A probabilistic relational algebra
  for the integration of information retrieval and database systems*, ACM TOIS
  15(1):32-66 (1997). 10.1145/239041.239045.
- `dalvi2007efficient`: N. Dalvi and D. Suciu, *Efficient query evaluation on
  probabilistic databases*, VLDB Journal 16(4):523-544 (2007).
  10.1007/s00778-006-0004-3.
- `benjelloun2008uldb`: O. Benjelloun, A. Das Sarma, A. Halevy, M. Theobald,
  J. Widom, *Databases with uncertainty and lineage*, VLDB Journal
  17(2):243-264 (2008). 10.1007/s00778-007-0080-z.
- `mullin1990semijoins`: J. K. Mullin, *Optimal semijoins for distributed
  database systems*, IEEE TSE 16(5):558-560 (1990). 10.1109/32.52778.
- `suciu2011` (existing entry): added DOI 10.2200/S00362ED1V01Y201105DTM016;
  Crossref now resolves it to the Springer reissue 10.1007/978-3-031-01879-4
  (same title and authors).

The sentences crediting them are in the introduction, paragraphs "Position
relative to probabilistic databases" and "Sensitivity and approximate membership".

## Claims withdrawn or narrowed

- Element-wise independence after projection (item 1).
- Universal understatement of join error under row independence (item 2).
- Unconditional vanishing of transitivity preservation (item 3).
- The local-versus-cascading closure dichotomy (item 4).
- Error rates as a security characterization (item 8).
- No novelty is claimed for the operator formulas or the one-sided contracts:
  they are elementary consequences of probabilistic relational algebra,
  lineage, dissociation, and monotone certificate theory.

## Build

`TEXINPUTS='.:./sty:' pdflatex -shell-escape main.tex; bibtex main;` then two
more `pdflatex` passes. Result: 0 errors, 0 undefined references, 0 undefined
citations, 0 BibTeX warnings, 28 pages. The status box renders on page 2,
directly after the abstract.

## Known remaining issues (not fixed in the freeze)

- Originality of the one-sided query-calibration formulation remains
  unestablished (see `.research/relations-revision/assessment.md`).
- The canonical-versus-ordered byte saving mostly reflects representative
  deduplication; against conservative certificate sizing it is 16 bytes.
- The historical filename `sections/oblivious_rel_model.tex` is kept on purpose.
