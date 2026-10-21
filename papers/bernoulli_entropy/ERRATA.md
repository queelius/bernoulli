# Errata: Entropy and space complexity of random approximate sets

Date: 2026-10-21. Author: Alexander Towell.

This is the final version of the preprint. It will be deposited on Zenodo as a
new version under concept DOI 10.5281/zenodo.20602259, superseding version
10.5281/zenodo.20602260. It is superseded by the monograph *Bernoulli Types:
Two-Sided Error in Approximate Membership, Retrieval, and Computation*,
Chapter 8, "Information-Theoretic Bounds"
(<https://metafunctor.com/latex/bernoulli-monograph/book.html>).
License unchanged: CC BY 4.0. Title unchanged.

A "Status and errata (October 2026)" box (`status_errata.tex`) now follows the
abstract and summarizes the items below.

## Corrections

1. **Two-sided space bound called open (abstract, `sections/intro.tex`,
   `sections/space_complexity.tex` Remark "The two-sided case",
   `sections/conclusion.tex`).** The previous version said the lower bound for
   approximate sets with both false positives and false negatives
   (0 < tau < 1) "remains open" and that the scaling -tau log2(epsilon) "is not
   a valid information-theoretic lower bound". Both statements were wrong.
   Pagh and Rodler (ESA 2001, Prop. 1) show that a lossy dictionary for n keys
   from a universe of size 2^w with at most gamma n false negatives and false
   positive rate epsilon needs (1 - gamma) n log2(1/(epsilon + n/2^w)) - O(n)
   bits, which is -tau log2(epsilon) - O(1) bits per element in the
   large-universe limit. The remark now states this result, and notes the
   remaining modelling difference (their bound limits the number of false
   negatives; the Bernoulli model fixes an expected rate), which this version
   does not bridge.
2. **Lower-bound proof stated a limit as an exact inequality
   (`sections/space_complexity.tex`, proof of Prop. 4.1).** The proof derived
   B >= log2 C(n,p) - log2 C(p + epsilon(n-p), p) and then wrote
   B >= -p log2(epsilon). The right-hand side converges to -p log2(epsilon)
   from below (for p = 3, epsilon = 0.1 it is 9.253 at n = 100 against the
   limit 9.966), so the correct statement is B >= -p log2(epsilon) - o(1) as
   n -> infinity. The proof also now names the regime (fixed set size, growing
   universe) and notes it differs from the constant-density regime of
   Theorem 3.1.
3. **Randomized extension asserted without citation (same proof).** The single
   sentence "follows from Yao's minimax principle" is replaced by a short
   sketch of the standard averaging argument, credited to Yao (FOCS 1977): draw
   the set uniformly, view the structure as a distribution over deterministic
   encodings, bound the conditional entropy of the set given the state by the
   expected log fiber size, and apply Jensen's inequality (the fiber bound is
   concave in the accepted fraction of negatives, whose expectation is at most
   epsilon). The bound then holds for the expected length of a prefix-free
   encoding. No novelty is claimed for this step.
4. **Dense-set remark (`sections/space_complexity.tex`, opening).** "O(u) bits
   are needed to code the set" now reads "O(u) bits suffice (an exact bit
   vector)", since the claim is an upper bound.
5. **Missing credit for constructions (`sections/space_complexity.tex`).** The
   perfect hash filter is now described as a minimal perfect hash function
   with a log2(1/epsilon)-bit fingerprint per element, the construction
   described by Dietzfelbinger and Pagh (ICALP 2008, Sec. 1). Constructions
   meeting the bound up to lower-order terms are credited to Pagh, Pagh, and
   Rao (SODA 2005) and Dietzfelbinger and Pagh (2008). The footnote on the
   brute-force seed construction (the Bernoulli hash function, earlier called
   the singular hash set) now cites the single-seed analysis of Lehmann,
   Sanders, Walzer, and Ziegler (ESA 2025). The Bloom filter cost now cites
   Broder and Mitzenmacher (2004).
6. **Contribution framing (`sections/intro.tex`).** "We make two
   contributions" is replaced by a "Content" paragraph: the joint-entropy
   result is an elementary consequence of element independence and the
   binomial entropy expansion, and the space bound is classical. The related
   work paragraph now cites Pagh and Rodler, Pagh, Pagh, and Rao,
   Dietzfelbinger and Pagh, Yao, and Broder and Mitzenmacher. The abstract no
   longer calls the Bernoulli set model "a compositionally closed framework":
   set operations on Bernoulli sets raise the model order, so a single
   false-positive and false-negative rate pair is not closed under composition
   (see the corrected composition preprint).
7. **"Remain unexplored" (`sections/conclusion.tex`).** The mutual information
   between a Bernoulli set and its objective set, and the capacity of the
   element-wise channel, are no longer described as unexplored. Under
   element-wise independence and an independent membership prior they reduce
   to per-element quantities of a binary asymmetric channel, whose capacity is
   classical (Silverman 1955). The "Open problems" paragraph is now "The
   two-sided case" and "Further directions".
8. **Stale self-citations (`references.bib`).** The companion working papers,
   previously "available from the author upon request" or "companion paper",
   now cite their Zenodo concept DOIs: Bernoulli sets (10.5281/zenodo.19105381),
   composition (10.5281/zenodo.19105387), perfect hash filter
   (10.5281/zenodo.20602263), Bernoulli hash function, formerly "The singular
   hash set" (10.5281/zenodo.20602261). The Carter et al. entry gained its DOI.

## Citations added

Each DOI was checked against the Crossref REST API on 2026-10-21 (title and
authors match), unless marked otherwise.

- `paghRodlerLossy`: R. Pagh, F. F. Rodler, *Lossy Dictionaries*, Algorithms,
  ESA 2001, LNCS, pp. 300-311. 10.1007/3-540-44676-1_25.
- `paghPaghRao`: A. Pagh, R. Pagh, S. S. Rao, *An Optimal Bloom Filter
  Replacement*, SODA 2005. **No Crossref DOI exists** (SODA 2005 is not
  registered with Crossref); cited by the author-hosted PDF
  <https://www.rasmuspagh.net/papers/bloom.pdf>, which the October 2026
  publication-triage audit examined. Not Crossref-verifiable.
- `dietzfelbingerPagh`: M. Dietzfelbinger, R. Pagh, *Succinct Data Structures
  for Retrieval and Approximate Membership (Extended Abstract)*, ICALP 2008,
  LNCS, pp. 385-396. 10.1007/978-3-540-70575-8_32.
- `yaoMinimax`: A. C.-C. Yao, *Probabilistic Computations: Toward a Unified
  Measure of Complexity*, FOCS 1977, pp. 222-227. 10.1109/SFCS.1977.24.
  (Crossref spells the author "Chi-Chin"; the bib uses the standard
  "Chi-Chih".)
- `broderMitzenmacher`: A. Broder, M. Mitzenmacher, *Network Applications of
  Bloom Filters: A Survey*, Internet Mathematics 1(4):485-509, 2004.
  10.1080/15427951.2004.10129096.
- `silvermanBinary`: R. A. Silverman, *On Binary Channels and Their Cascades*,
  IRE Trans. Inf. Theory 1(3):19-27, 1955. 10.1109/TIT.1955.1055138.
- `lehmannSeeds`: H.-P. Lehmann, P. Sanders, S. Walzer, J. Ziegler, *Combined
  Search and Encoding for Seeds, with an Application to Minimal Perfect
  Hashing*, ESA 2025, LIPIcs 351, 109:1-109:18. 10.4230/LIPIcs.ESA.2025.109.
  **DataCite DOI** (LIPIcs does not register with Crossref); checked via
  api.datacite.org, title and authors match.
- DOI added to the existing `carterExact` entry: 10.1145/800133.804332
  (Crossref, title and authors match).
- Zenodo DOIs on the four self-citations were checked via DataCite.

## Claims withdrawn or narrowed

- The two-sided space bound is no longer called open, and the heuristic
  -tau log2(epsilon) is no longer called invalid.
- The lower bound is stated as asymptotic (minus o(1)), not exact.
- The randomized-structure extension is credited, not claimed.
- No novelty is claimed for the joint-entropy computation or the space bound.

## Build

`pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`:
0 LaTeX errors, 0 undefined references, 0 undefined citations, 0 BibTeX
warnings, no overfull boxes. 8 pages (was 6). The status box renders on page 1.

## Known remaining issues (not fixed in the freeze)

- The transfer of the Pagh-Rodler bound from a bounded false-negative count to
  the Bernoulli model's expected false-negative rate is stated, not proved.
- Editorial items from the 2026-05-29 review remain: the objective set is
  written A, R, and S in different places; its size is m in Section 3 and p in
  Section 4; the remark label renders as a section reference.
- The monograph's Chapter 8 (`book/chapters/ch08/entropy-floor.tex` and
  `bibliographic-notes.tex`) still calls the two-sided case open and should be
  corrected in the monograph.
