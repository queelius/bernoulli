# Errata: Bernoulli sets: a model for random approximate sets

Date: 2026-10-21. Author: Alexander Towell.

This is the final version of the preprint. It will be deposited on Zenodo as a
new version under concept DOI 10.5281/zenodo.19105381, superseding version
10.5281/zenodo.19105382 (v1.0.0). It is superseded by the monograph *Bernoulli
Types: Two-Sided Error in Approximate Membership, Retrieval, and Computation*,
Chapters 2 (Binary Channels and Model Order), 4 (Two Axioms and Kronecker
Factorization), 5 (Approximate Sets and Predicates), and 7 (Classification
Measures), at <https://metafunctor.com/latex/bernoulli-monograph/book.html>.
License unchanged: CC BY 4.0. Title unchanged.

A "Status and errata (October 2026)" box now follows the abstract
(`status_errata.tex`).

## Corrections

1. **Two rates do not propagate through set expressions (abstract,
   `sections/intro.tex`, `sections/bernoulli_model.tex` Section 3.2,
   `sections/conclusion.tex`).** The previous version said that compositions of
   Bloom filters and perfect hash filters "inherit the full theory
   automatically" and that "the entire probabilistic structure follows from the
   false positive and false negative rates alone". That holds for a single
   second-order Bernoulli set and for cascades of approximate identities, not
   for set-theoretic compositions. Section 3.2 now states the union case
   explicitly: with independent constructions, negatives of A ∪ B share the
   rate 1-(1-ε1)(1-ε2), but positives split into three latent classes with true
   positive rates 1-(1-τ1)(1-ε2), 1-(1-ε1)(1-τ2), and 1-(1-τ1)(1-τ2); for
   intersection the negatives split the same way. Composition raises the model
   order.
2. **Approximate union operator (`sections/bernoulli_model.tex`, Section 3.2,
   formerly line 157).** The right-hand side had its rate arguments swapped
   (`[\tprate][\fprate]`), and the prose said positives are mapped to negatives
   with probability τ. Positives are lost with probability ω = 1-τ. Flagged as
   M1 in the 2026-05-23 review; fixed now.
3. **Bloom filters satisfy Axiom 1 only conditionally
   (`sections/bernoulli_model.tex`, parametric-parsimony remark and new remark
   "Which implementations satisfy the axioms").** The previous version said the
   axioms "generally hold in practice" for Bloom filters and perfect hash
   filters because query outcomes for distinct elements come from independent
   hash evaluations. For a Bloom filter the false-positive indicators of
   distinct non-members are independent only given the realized bit array;
   unconditionally they are positively correlated through the random realized
   rate. Exact example (two cells, one hash function, two inserted keys,
   independent uniform hashes): a fixed absent key is a false positive with
   probability 3/4, two absent keys both with probability 5/8 > 9/16. This is
   the enumeration in `.research/relations-revision/check_borrowed_models.py`.
   The binomial results therefore apply to a Bloom filter conditionally on its
   realized rate. A perfect hash filter with ideal fingerprints independent of
   the construction does satisfy the axiom for negatives. The Kronecker
   factorization remark now says it needs mutually independent tests (for
   example, independently built structures) and is an assumption about the
   implementation.
4. **Maximum-entropy and worst-case claim withdrawn
   (`sections/distributions.tex`, Section 4.1).** The previous version said
   that "the binomial distribution maximizes entropy over {0,...,n} for a given
   mean" and that the resulting intervals are therefore "the widest possible"
   and "worst-case". The first statement is false (on {0,...,n} with fixed mean
   the maximum-entropy law is the truncated geometric family; the binomial is
   maximal only among sums of independent Bernoulli variables; for n = 2 and
   mean 1, the uniform law has entropy log2 3 > 1.5 bits, the Binomial(2, 1/2)
   entropy), and the
   conclusion does not follow: maximum entropy is not maximum variance.
   Positively correlated errors give a larger variance; for example, with n = 2
   and ε = 1/2, perfectly correlated errors give Var(FP) = 1 versus 1/2 under
   independence. The text now keeps only the correct statement that
   independence maximizes the joint entropy of the indicators for fixed
   marginals.
5. **Probability intervals, not confidence intervals
   (`sections/distributions.tex`, Section 4.1; abstract; introduction).** The
   intervals ε ± z·sqrt(ε(1-ε)/n) assume the expected rate is known and cover
   the realized rate with asymptotic probability γ. They are now described as
   probability (prediction) intervals for the realized rates; estimating an
   unknown rate from observed counts uses the standard binomial confidence
   intervals.
6. **Novelty claims removed (abstract; `sections/intro.tex`; the binary-channel
   remark in `sections/bernoulli_model.tex`; `sections/conclusion.tex`).**
   - The introduction's "The gap" paragraph (the literature "lacks a
     foundational probabilistic model for approximate sets") is replaced by a
     "Scope and prior work" paragraph crediting the predecessors below and
     stating that no new model or theorem is claimed.
   - "We introduce" and "A central finding of this work" phrasing is replaced
     by statements that the results are standard consequences of independence.
   - The binary-channel remark no longer claims novelty for the set-level
     derivations; the k-fold composition is identified as the classical
     cascade of binary channels.
   - Related work no longer says analyses treat each filter in isolation;
     Broder and Mitzenmacher already describe union and intersection of Bloom
     filters.
   - The conclusion no longer says the maps companion "shows that the entropy
     map is the information-theoretically optimal construction"; it points to
     that paper's October 2026 errata.

## Citations added

Each DOI was checked against the Crossref REST API on 2026-10-21 (title and
authors match).

- `bross1954misclassification`: Irwin Bross, *Misclassification in 2 X 2
  Tables*, Biometrics 10(4) (1954). DOI 10.2307/3001619. (Crossref gives the
  start page 478; the end page 486 is from the standard citation.)
- `hirota1981probabilistic`: Kaoru Hirota, *Concepts of probabilistic sets*,
  Fuzzy Sets and Systems 5(1):31-46 (1981). DOI 10.1016/0165-0114(81)90032-4.
- `donnet2006retouched`: Benoit Donnet, Bruno Baynat, Timur Friedman,
  *Retouched Bloom filters*, ACM CoNEXT 2006. DOI 10.1145/1368436.1368454.
- `laufer2011generalized`: Rafael P. Laufer, Pedro B. Velloso, Otto Carlos
  M. B. Duarte, *A Generalized Bloom Filter to Secure Distributed Network
  Applications*, Computer Networks 55(8):1804-1819 (2011).
  DOI 10.1016/j.comnet.2010.12.025.

DOIs added to existing entries (also Crossref-verified): `warner1965`
(10.1080/01621459.1965.10480775) and `broderMitzenmacher`
(10.1080/15427951.2004.10129096).

## Build

`pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`:
0 LaTeX errors, 0 undefined references, 0 undefined citations, 0 BibTeX
warnings; 20 pages (was 18). The status box renders on page 1.

## Known remaining issues (not fixed in the freeze)

- Minor items m1, m2, m5 to m9 and the suggestions from the 2026-05-23 review
  (notation, label names, the Ribbon preprint citation) are left as they were.
- Remarks are unnumbered in `alex.sty`, so cross-references to remarks use
  their names.
- Axiom 1 is stated both unconditionally and "given the error rates"; the
  paper does not fully separate the realized-rate and expected-rate readings.
  The new remark on implementations states which reading a Bloom filter
  satisfies; the monograph (Chapter 4 and Chapter 16) treats this properly.
