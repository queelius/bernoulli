# Errata: Binary classification measures for random approximate sets

Date: 2026-10-21. Author: Alexander Towell.

This is the final version of the preprint. It will be deposited on Zenodo as a
new version under concept DOI 10.5281/zenodo.19104549, superseding version
10.5281/zenodo.19104550 (v1.0.0). It is superseded by the monograph *Bernoulli
Types: Two-Sided Error in Approximate Membership, Retrieval, and Computation*,
Chapter 7 (Classification Measures)
(<https://metafunctor.com/latex/bernoulli-monograph/book.html>). License
unchanged: CC BY 4.0.

A "Status and errata (October 2026)" box now follows the abstract.

## Corrections

1. **Abstract and Introduction (`main.tex`, `sections/intro.tex`).** The model
   was described as "a compositionally closed framework". A single (FPR, FNR)
   pair does not propagate through arbitrary set expressions: composed sets are
   higher-order, and their marginal pairs are not valid input for further
   composition (counterexample in the companion composition paper's errata:
   (A1 ∩ A2) ∪ A3 at FPR 0.02, FNR 0.10 gives per-element errors 0.03764 and
   0.020392 for two negatives). The phrase is removed.
2. **Abstract and Conclusion (`main.tex`, `sections/conclusion.tex`).** "The
   results apply to any data structure satisfying the Bernoulli axioms,
   including Bloom filters and perfect hash filters" implied those structures
   satisfy the axioms. They do so only approximately: errors at distinct
   elements share the random state of one build, so realized rates vary across
   builds and the classical Bloom filter rate is itself an approximation (Bose
   et al. 2008). The statement now says the results apply exactly under the
   axioms and approximately to those structures.
3. **Proposition 2.1 (`sections/preliminaries.tex`).** Said E[β] = τ while
   Corollary 2.5 defines TPR = 1 − β, which requires β to be the realized false
   negative rate with E[β] = ω. Corrected to E[β] = ω, with α and β named as the
   realized false positive and false negative rates. No downstream result used
   the wrong value.
4. **Interval PPV example (`sections/measures.tex`, Section 3.2).** Claimed
   "guaranteed bounds on the expected precision", but the bounds are computed
   from the large-set approximation pτ/(pτ + nε). They are guaranteed bounds on
   that ratio of expected counts and bound E[PPV] only up to the delta-method
   correction.
5. **Novelty framing (`main.tex`, `sections/intro.tex`).** "Contribution"
   renamed "Scope"; the abstract and introduction now say the results are known
   statistical results restated for the model. The prevalence effect is cited as
   the classical predictive-value relation of diagnostic testing rather than
   presented as a data-structures finding. Related work now cites Goutte and
   Gaussier (probabilistic precision/recall/F), Warner (randomized response, the
   per-element channel), and Bross (misclassification in 2 × 2 tables), and
   contrasts the inferred-from-counts setting with the known-rates sampling
   distributions used here.

## Citations added

Each DOI was checked against the Crossref REST API on 2026-10-21 (title and
authors match).

- `warner1965randomized`: S. L. Warner, *Randomized Response: A Survey
  Technique for Eliminating Evasive Answer Bias*, JASA 60(309) (1965).
  10.1080/01621459.1965.10480775
- `bross1954misclassification`: I. Bross, *Misclassification in 2 X 2 Tables*,
  Biometrics 10(4) (1954). 10.2307/3001619
- `goutte2005probabilistic`: C. Goutte, E. Gaussier, *A Probabilistic
  Interpretation of Precision, Recall and F-Score, with Implication for
  Evaluation*, ECIR 2005, LNCS (2005). 10.1007/978-3-540-31865-1_25
- `altman1994predictive`: D. G. Altman, J. M. Bland, *Statistics Notes:
  Diagnostic tests 2: predictive values*, BMJ 309(6947) (1994).
  10.1136/bmj.309.6947.102
- `bose2008fpr`: P. Bose et al., *On the false-positive rate of Bloom filters*,
  Information Processing Letters 108(4) (2008). 10.1016/j.ipl.2008.05.018

## Claims withdrawn or narrowed

- "Compositionally closed framework": withdrawn.
- Novelty of the measure distributions and the prevalence effect: withdrawn
  (standard delta method; classical predictive-value relation).
- Exact applicability to Bloom filters and perfect hash filters: narrowed to
  approximate applicability.
- Interval PPV "guaranteed bounds on the expected precision": narrowed to the
  ratio of expected counts.

## Build

`pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`:
0 errors, 0 undefined references, 0 undefined citations, 0 BibTeX warnings,
15 pages. The status box renders on page 1.

## Known remaining issues (not fixed in the freeze)

- Reproducibility gap from the May 2026 review: only `code/f1_sim.py` is
  committed; the PPV theory-vs-simulation figure and the prevalence curves have
  no generator script.
- Monte Carlo validation covers only FNR = 0.
- PPV is undefined when TP + FP = 0; the delta-method expectation ignores this
  event (negligible at the plotted sizes, not treated formally).
- Notation inconsistencies flagged in May (several symbols for the approximate
  set, calligraphic vs upright TPR) are unchanged.
- `phf` remains an unpublished working-paper citation; the PHF preprint now has
  concept DOI 10.5281/zenodo.20602263.
