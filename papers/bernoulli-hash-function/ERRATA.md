# Errata: The Bernoulli Hash Function: Optimal Bernoulli Sets and Bernoulli Maps

Date: 2026-10-21. Author: Alexander Towell.

This is the final version of the preprint. It will be deposited on Zenodo as a
new version under concept DOI 10.5281/zenodo.20602261, superseding version
10.5281/zenodo.20602262. It is superseded by the monograph *Bernoulli Types:
Two-Sided Error in Approximate Membership, Retrieval, and Computation*,
Chapter 14, "Optimal Bernoulli Sets (BHF)"
(<https://metafunctor.com/latex/bernoulli-monograph/book.html>).
License unchanged: CC BY 4.0. The title is unchanged; "Optimal" now refers
only to matching the known space bound to leading order in expectation.

Evidence for the corrections: the October 2026 audit in
`.research/publication-triage/candidates/hash-construction/` (assessment.md,
audit_hash.py, results.json) and `.research/relations-revision/related-ideas.md`,
plus exact rational checks rerun for this freeze.

## Corrections

1. **Exact threshold law (`sections/shf.tex`, Theorem 3.7; `sections/appendix.tex`, Appendix B).**
   The previous version stated, as the exact law of the p-th order statistic of
   i.i.d. uniform residues, the without-replacement (distinct-residue) PMF. It
   fails at N=2, m=2, p=1: it gives P(T=0)=1, while enumeration gives
   (3/4, 1/4). This version states the binomial-tail law
   P(T <= j) = sum_{a=p}^m C(m,a) ((j+1)/N)^a (1-(j+1)/N)^(m-a), equivalently
   the regularized incomplete Beta function at (j+1)/N, so T+1 has the law of
   ceil(N U) with U ~ Beta(p, m-p+1). The old formula is kept in the appendix,
   labeled as the law conditioned on distinct residues, with the total
   variation bound m(m-1)/(2N). The "shifted beta-binomial" assertion is
   withdrawn. Checked against exhaustive enumeration for all N <= 5, m <= 4.
2. **Recall of the adaptive threshold (new `sections/shf.tex` subsection "Recall, dependence, and the accuracy contract").**
   The previous version never stated that the adaptive rule accepts only about
   p of the m members. In the continuous limit its recall is p/m and its mean
   FPR is p/(m+1), so recall minus FPR is p/(m(m+1)) <= 1/(m+1). Exact values
   are given (N=m=100: recall 0.0158 vs FPR 0.0157 at p=1; FPR 0.9943 at
   p=100).
3. **Dependence of the adaptive structure (same subsection).** Non-member
   tests are independent only conditional on T; unconditionally two distinct
   non-members have covariance Var((T+1)/N) (3/64 at N=m=2, p=1), so the
   adaptive structure is a mixture of Bernoulli sets, not a Bernoulli set in
   the sense of the paper's Definition 2.4.
4. **"Price of FPR certainty" (`sections/space.tex`, Section 5.6).** The
   theorem, its interpretation ("the price of FPR certainty, not of
   membership encoding"), and its figure compared a recall-1 fixed-threshold
   structure with a recall-p/m adaptive one. They are withdrawn and replaced by
   a same-contract theorem: with an FPR cap (t*+1)/N and at least r accepted
   members, the adaptive acceptance event equals the fixed-threshold count
   event, with success probability s = P(Bin(m, eps*) >= r), expected trials
   1/s, and expected salt length -log2 s + O(1). Example: m=4, r=3, eps*=1/5
   gives s = 17/625 (checked by enumeration).
5. **Lower-bound remark (`sections/space.tex`, Remark in Section 5.5).** The
   claim that a random per-build FPR takes the adaptive rule outside the
   membership lower bound is withdrawn. For a fixed non-member the acceptance
   probability is the expectation of the conditional FPR, and the standard
   approximate-membership formulation already allows randomized structures
   (Pagh, Pagh, and Rao). The small cost reflects the weaker recall.
6. **Log moment of the geometric search (`sections/space.tex`, proof of Theorem 5.2).**
   The printed closed form E[log2 Q] = -log2 p - (log2 e)(1-p) ln(1-p)/p is
   the entropy of Q, not its log moment; at p=1/2 it gives 2, while
   E[log2 Q] = 0.7326 and E[floor(log2 Q)] = 0.6328. Replaced by the proved
   bounds -log2 p - log2 e <= E[log2 Q] <= -log2 p, hence
   -log2 p - log2 e - 1 <= E[L] <= -log2 p. The O(1) conclusion is unchanged.
7. **Entropy of the salt index (`sections/space.tex`, Remark "Entropy of the salt index").**
   Sign error fixed: H(Q) = -log2 s - (1-s) log2(1-s)/s, which is 2 bits at
   s=1/2 (the printed formula gave 0).
8. **Effect of false negatives (`sections/space.tex`, Section 5.4).** The
   success probability was given as that of one fixed subset; it is the
   binomial tail P(Bin(m, eps) >= r) >= eps^r. The claim of matching the lower
   bound is narrowed to leading order in log2(1/eps); the false-negative lower
   bound itself holds only up to O(1) bits per element.
9. **Lower bounds with false negatives (`sections/prelim.tex`, Theorems 2.1 and 2.2).**
   The false-negative case was attributed to Carter et al. It is the lossy
   dictionary bound of Pagh and Rodler (ESA 2001, Prop. 1), stated with its
   O(1)-bits-per-element slack.
10. **Search for FNR > 0 (`sections/shf.tex`, Theorem 3.4 and Remark; `sections/intro.tex`).**
    The "exponential" advantage of the threshold predicate was against naive
    subset enumeration only; a hash-and-count equality test is also linear per
    salt. The theorem and introduction now say so.
11. **Maximum entropy (`sections/entropy.tex`, Theorem 6.1).** The proof
    claimed the threshold t is uniformly distributed; for the fixed-threshold
    predicate t is a public parameter chosen in advance. The theorem now
    states uniformity of the salt given its length, a symmetry fact that is
    not a compression bound or a privacy theorem. The adaptive-entropy remark
    no longer claims that the entropy loss is "precisely" H(T); the adaptive
    entropy sum now runs over the correct support j = 0..N-1.
12. **Adaptive map construction (`sections/construction.tex`, Algorithm 3; `sections/shf.tex`, Theorem 3.6).**
    The map path returned (N, t) without the salt, which Find needs; it now
    returns (N, t, b). The count of value-matching keys is Poisson-binomial
    (binomial only for equal value lengths; Bin(m, 2^-mu) was described as an
    approximation, which it is not). The text now notes that keys outside the
    value-matching set whose residues fall below t are accepted with wrong
    values.
13. **Claims of optimality and novelty (abstract, `sections/intro.tex`, `sections/discussion.tex`).**
    The abstract no longer says the BHF "optimally" implements the ADTs or
    proves achievability as a new result; the contributions list and
    discussion credit the predecessors below. The discussion's misattribution
    (Pagh, Pagh, and Rao's achievability result cited to Carter et al.) is
    fixed, and the adaptive variant is no longer described as a practical
    near-zero-space construction. A new "Relation to prior work" paragraph
    was added to the introduction.

Also changed (not errors of substance): the companion-paper BibTeX entries
now point to their Zenodo concept DOIs, and the 2017/2018 unpublished
manuscripts are marked as such (removes six BibTeX "empty journal" warnings).
The per-element space figure no longer plots the adaptive variant.

## Citations added

Each DOI was checked against the Crossref REST API on 2026-10-21 (title and
authors match), unless marked otherwise.

- `pagh2001lossy`: R. Pagh, F. F. Rodler, *Lossy Dictionaries*, ESA 2001,
  LNCS, pp. 300-311. DOI 10.1007/3-540-44676-1_25.
- `dietzfelbinger2008retrieval`: M. Dietzfelbinger, R. Pagh, *Succinct Data
  Structures for Retrieval and Approximate Membership (Extended Abstract)*,
  ICALP 2008, LNCS, pp. 385-396. DOI 10.1007/978-3-540-70575-8_32.
- `esposito2020recsplit`: E. Esposito, T. M. Graf, S. Vigna, *RecSplit:
  Minimal Perfect Hashing via Recursive Splitting*, ALENEX 2020, pp. 175-185.
  DOI 10.1137/1.9781611976007.14.
- `lehmann2024shockhash`: H.-P. Lehmann, P. Sanders, S. Walzer, *ShockHash:
  Towards Optimal-Space Minimal Perfect Hashing Beyond Brute-Force*, ALENEX
  2024, pp. 194-206. DOI 10.1137/1.9781611977929.15.
- `lehmann2025seeds`: H.-P. Lehmann, P. Sanders, S. Walzer, J. Ziegler,
  *Combined Search and Encoding for Seeds, with an Application to Minimal
  Perfect Hashing*, ESA 2025, LIPIcs 351, 109:1-109:18.
  DOI 10.4230/LIPIcs.ESA.2025.109. **Registered with DataCite, not Crossref**
  (Crossref returns 404); title and authors checked via api.datacite.org.
- `chazelle2004bloomier`: B. Chazelle, J. Kilian, R. Rubinfeld, A. Tal, *The
  Bloomier Filter: An Efficient Data Structure for Static Support Lookup
  Tables*, SODA 2004. **No Crossref DOI exists** (Crossref search finds no
  record); cited with the author-hosted URL, which the October 14 audit
  examined (`.research/publication-triage/verified-bibliography.json`).

Already present and now cited in context: Carter et al. 1978 and Pagh, Pagh,
and Rao (SODA 2005; no Crossref DOI).

## Claims withdrawn or narrowed

- The adaptive threshold's "vanishing per-element space" as a space saving.
- "Price of FPR certainty" theorem, its interpretation, and its figure.
- A random per-build FPR evading the membership lower bound.
- The exact discrete order-statistic PMF and the shifted beta-binomial law.
- The closed forms for E[log2 Q] and H(Q).
- "Eliminates the combinatorial subset enumeration" as an algorithmic advance.
- Information-theoretic optimality and maximum entropy as contributions.

## Build

`make` (pdflatex, bibtex, pdflatex, pdflatex with `-interaction=nonstopmode
-halt-on-error`). Result: 0 LaTeX errors, 0 undefined references, 0 undefined
citations, 0 BibTeX warnings; 30 pages. The status box renders on page 2,
directly after the abstract (it is too tall to share page 1 with the
abstract).

## Known remaining issues (not fixed in the freeze)

- The threshold construction with FNR > 0 accepts the members whose residues
  fall below t, so the set of false negatives depends on the salt; the
  per-member independence of false negatives assumed by the Bernoulli set
  definition is not separately proved for this construction.
- The maps analysis for FNR > 0 and for unequal value lengths is sketched
  ("about mu bits per accepted key"), not proved.
- The equality-predicate success-probability rows of Table 1 use the
  zero-false-negative formulas.
- No experiments; all space claims are leading-order analysis under the
  random oracle assumption. A real digest reduced modulo a non-power-of-two N
  is not exactly uniform without rejection sampling.
