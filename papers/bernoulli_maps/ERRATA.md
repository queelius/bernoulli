# Errata: The algebra of the random approximate map model

Date: 2026-10-21. Author: Alexander Towell.

This is the final version of the preprint. It will be deposited on Zenodo as a
new version under concept DOI 10.5281/zenodo.19105389, superseding version
10.5281/zenodo.19105390 (v1.0.0, 2026-03-19). It is superseded by the monograph
*Bernoulli Types: Two-Sided Error in Approximate Membership, Retrieval, and
Computation*, Chapter 9 (Approximate Functions and n-ary Channels), with the
space-optimal construction in Chapter 14 and the trapdoor material in
Chapter 17 (<https://metafunctor.com/latex/bernoulli-monograph/book.html>).
License unchanged: CC BY 4.0.

Section numbers below refer to this build. The success-probability error was
cited as "Section 6.6" in the 2026-05-29 review and the October 2026 program
strategy; in the current source it is Section 6.5.

## Corrections

1. **Section 6.5, Probability of success (`sections/entropy_maps.tex`).**
   The previous version stated
   `p = C(m, (1-w)m) e^{m(1-w)} (1-e)^{mw}` with the per-element estimate
   `-H_b(w) - w log2(1-e) - (1-w) log2 e`. This contradicted Section 7: at
   w = 0 it gives `e^m` instead of `e^(m-1)`, it has no value term, and it
   forces the unstored keys to be rejected. It is replaced by the
   hash-and-check value used in Section 7, applied to a designated stored set
   S of `r = ceil((1-w)m)` keys: `p = e^(r-1) 2^(-r mu_S)`, with a two-sided
   bound on the expected code length. A remark explains the old formula: it
   is the exact-r binomial term of a different scheme (fixed target, any r
   keys stored), whose correct success event is "at least r keys hit", and
   whose exponent is the relative entropy
   `H_b(w) - w log2(1-e) - (1-w) log2 e` (with `H_b <= 0` as defined), so the
   printed estimate also had the entropy term's sign reversed. Checked
   numerically: at m = 20000, e = 0.05, w = 0.3 the tail exponent is 2.1666
   bits per element, the relative entropy 2.1663, the printed estimate 3.9288.
2. **Section 7.3, space theorem and proof (`sections/shm.tex`).** The theorem
   gave a "lower bound" `-(1-w) log2 e + (1-w) mu` for uniformly distributed
   code lengths and an "upper bound" `-(1-w) log2 e + mu` for degenerate code
   lengths, and the proof derived only an upper bound (Jensen). With equal code
   lengths the value term is actually `(1-w) mu`, so the labels were wrong. The
   theorem now states `-(1-w) log2 e + (1-w) mu_S + O(1/m)` bits per element,
   with `(r/m) mu_S <= mu`, equality to `(r/m) mu` for equal lengths or a
   uniformly random stored set, and a two-sided bound
   `log2(1/p) - 1/ln 2 <= E[log2 Q] <= log2(1/p)` (lower half from
   `P(Q <= a) <= a p`).
3. **Section 7.2, proof notation (`sections/shm.tex`).** The proof mixed
   `mod t`, `mod BL(v)` and `trunc`, required `N < max BL(v_j)` (backwards),
   and stated value matches as `h(1||k) mod BL(v) = v` (type-incorrect). It now
   uses `trunc(h(k || b_n), k)`, a random oracle or `N >= max(k, BL(v_j))`, and
   prefix matches of `h(1 || k_j || b_n)` against codewords. The result
   `p = e^(m-1) / 2^(m mu)` is unchanged.
4. **Section 5.1, closure under composition (`sections/composition_new.tex`).**
   The lemma claimed that the composition of independent approximate maps is an
   approximate map, but proved only that each output is correct with positive
   probability. It is now stated in marginal form. New Lemma 5.2: if a stored
   `g~` is queried at the same intermediate value y for two inputs
   (`f(x1) = f(x2) = y`), both composed outputs share one outcome, so
   `P(both correct) = (1-w1)^2 (1-w2)` and the correctness indicators have
   covariance `(1-w1)^2 w2 (1-w2) > 0`, violating element-wise independence
   (Assumption 1). Independence holds when intermediate values at the queried
   inputs are distinct with probability one, or when `g~` draws fresh
   randomness per query. A remark extends this to coinciding false-positive
   values. Checked exactly: w1 = 0, w2 = 1/10 gives P(both) = 9/10 versus
   product 81/100.
5. **Section 5.3.2, set operations (`sections/composition_new.tex`).** The text
   said union error rates "follow from the complement and intersection
   formulas", but only the intersection TPR was given. It now gives the three
   intersection false-positive rates by latent block (`(1-w_A) e_B` on A\B,
   `e_A (1-w_B)` on B\A, `e_A e_B` outside both) and states that a single
   (false positive, false negative) pair does not propagate through set
   formulas.
6. **Section 4.3, Kronecker theorem (`sections/special_cases.tex`).** The
   parameter-count baseline `N(|Y|^|X| - 1)` for an undefined order N is
   replaced by `|Y|^|X| - 1` (an arbitrary distribution over Y^X given the
   latent function), noting the full unconstrained channel has
   `|Y|^|X| (|Y|^|X| - 1)` entries.
7. **Abstract, Section 1, Sections 6 and 7 introductions, Section 8.** The
   singular hash map was called "a concrete algorithm achieving the
   information-theoretic lower bound". It is now described as a seed-search
   construction whose expected space approaches `-log2 e + mu` at exponential
   expected construction cost (`E[Q] = 2^(m mu) / e^(m-1)`), with a new
   construction-cost remark in Section 7. The "Contributions" paragraph is
   renamed "Contents" and states that no result is claimed as new. The entropy
   map's maximum-conditional-entropy property is marked as asserted, not proved.
   The introduction notes that Bloom-type structures fit the model only
   conditionally on the realized structure.
8. **Status and errata box** inserted after the abstract (`status_errata.tex`).

## Citations added

Each DOI was checked against the Crossref REST API on 2026-10-21 (title and
authors match), unless marked otherwise.

- `silverman1955`: R. Silverman, *On binary channels and their cascades*, IRE
  Trans. Information Theory 1(3):19-27 (1955). 10.1109/TIT.1955.1055138.
- `carbin2013rely`: M. Carbin, S. Misailovic, M. C. Rinard, *Verifying
  quantitative reliability for programs that execute on unreliable hardware*,
  OOPSLA 2013, 33-52. 10.1145/2509136.2509546.
- `carter1978`: L. Carter, R. Floyd, J. Gill, G. Markowsky, M. Wegman, *Exact
  and approximate membership testers*, STOC 1978, 59-65. 10.1145/800133.804332.
- `esposito2020recsplit`: E. Esposito, T. M. Graf, S. Vigna, *RecSplit:
  Minimal Perfect Hashing via Recursive Splitting*, ALENEX 2020, 175-185.
  10.1137/1.9781611976007.14.
- `lehmann2025seeds`: H.-P. Lehmann, P. Sanders, S. Walzer, J. Ziegler,
  *Combined Search and Encoding for Seeds, with an Application to Minimal
  Perfect Hashing*, ESA 2025, LIPIcs 351, 109:1-109:18.
  10.4230/LIPIcs.ESA.2025.109 (DataCite DOI; not in Crossref; verified via the
  DataCite API).
- `bhf`: A. Towell, *The Bernoulli Hash Function: Optimal Bernoulli Sets and
  Bernoulli Maps*, Zenodo concept DOI 10.5281/zenodo.20602261 (DataCite).
- `bernoulliComposition`: A. Towell, *Composition of Bernoulli sets*, Zenodo
  concept DOI 10.5281/zenodo.19105387 (DataCite). Fixes the uncited companion
  reference flagged in the 2026-05-29 review.

Existing entries updated: `dietzfelbinger2008` gained its DOI
10.1007/978-3-540-70575-8_32 (Crossref verified) and LNCS series data;
`chazelle2004` (Bloomier filter, SODA 2004) gained the author-hosted URL. SODA
2004 has no Crossref DOI, so that entry is verified only against the
author-hosted PDF (see `.research/publication-triage/verified-bibliography.json`).

## Claims withdrawn or narrowed

- The composition "closure" theorem: only marginal rates are closed; the joint
  (independent-element) law is not preserved with shared intermediates.
- The singular hash map as a "concrete algorithm achieving" the lower bound:
  it is an exponential-time existence construction; practical retrieval
  structures reach the same scale in linear time.
- The "function-space viewpoint unifies the entire landscape" phrasing and the
  contributions list as novelty claims.

## Build

`TEXINPUTS=".:./sty:" pdflatex main.tex && bibtex main && TEXINPUTS=".:./sty:" pdflatex main.tex && TEXINPUTS=".:./sty:" pdflatex main.tex`

Result: 0 LaTeX errors, 0 undefined references, 0 undefined citations, 0
BibTeX warnings; 26 pages. The status box renders on page 1. Two small
overfull hboxes (1.3pt, 6.1pt) remain.

## Known remaining issues (not fixed in the freeze)

- Algorithm 1 searches only for a membership salt; the value-matching step
  analyzed in Theorem 7.1 is not in the pseudocode, and the FNR > 0 variant
  (designated stored set) is described only in the text.
- The symbol k denotes both the hash-truncation length and keys `k_j` in
  Section 7.
- No Monte Carlo validation of the `rho`-dependent composition FPR.
- The unused `FancySet{P}`/`FancySet{R}` definitions at the start of
  Section 6.5, the inactive glossary machinery, and the orphaned `defs.tex` and
  `gloss.tex` are left in place.
