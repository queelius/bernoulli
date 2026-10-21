# Errata: The Perfect Hash Filter: An efficient implementation of the positive Bernoulli set and Bernoulli map abstract data types

Date: 2026-10-21. Author: Alexander Towell.

This is the final version of the preprint. It will be deposited on Zenodo as a
new version under concept DOI 10.5281/zenodo.20602263, superseding version
10.5281/zenodo.20602264. It is superseded by the monograph *Bernoulli Types:
Two-Sided Error in Approximate Membership, Retrieval, and Computation*,
Chapter 15, "Perfect Hash Filters"
(<https://metafunctor.com/latex/bernoulli-monograph/book.html>).
License unchanged: CC BY 4.0.

A "Status and errata (October 2026)" box now follows the abstract
(`paper/status_errata.tex`).

## Corrections

1. **Attribution of the construction (abstract, `sections/intro.tex`,
   `sections/related_work.tex`).** The previous version called the structure
   well known but did not say where it is stated. Section 1 of Dietzfelbinger
   and Pagh (ICALP 2008) describes exactly a minimal perfect hash function
   combined with ceil(log2(1/eps))-bit fingerprints, with about log2 e bits per
   element of overhead, and notes that the origin of the idea is unknown to
   them. This is now credited in the abstract, introduction and related work.
   The abstract's "Our contribution ... We make four contributions" is replaced
   by an explicit statement that no novelty is claimed for the structure or its
   analysis; the related-work summary adds that the analyses (fingerprint FPR,
   perfect-hash space bound, occupancy) are standard. The map form is credited
   to Bloomier filters and retrieval structures.
2. **Salt search and "combinatorial subset enumeration" (abstract, intro,
   related work, `sections/adt.tex`).** The previous version claimed that the
   Bernoulli hash function's salt search must enumerate combinatorially many
   subsets to admit false negatives, and presented this as the PHF's advantage.
   That is false: counting accepted members costs O(m) hash evaluations per
   salt (the hash-function paper itself concedes this). The claim is removed.
   Salt search is described as single-seed search with exponential expected
   construction work (Lehmann et al., ESA 2025), and "attains the floor exactly"
   is weakened to "up to lower-order terms".
3. **k-perfect false negative formula ignored seed rejection
   (`sections/k_perfect_hashing.tex`, Theorem 5.1).** Assumption 2 rejects seeds
   with a slot above occupancy k, but the proof used the unconditional binomial
   occupancy law. Counterexample: m = N = 2, k = 1. Every accepted placement is
   injective, so the true displacement probability is 0; the formula gives 1/4.
   The theorem is now stated as exact only when no seed is rejected (k >= m),
   and a new remark gives the exact law omega_k = 1 - E[O | max L <= k]/m.
4. **Fingerprint rescue (`sections/k_perfect_hashing.tex`).** A displaced
   member whose fingerprint equals the retained one is still accepted, so the
   membership false negative rate is (1 - 2^-M) omega_k, not omega_k.
   Counterexample: m = N = 2, k = 2, M = 1 gives displacement 1/4 but false
   negative rate 1/8. The output descriptions of Algorithms 4 and 5 are updated to match.
5. **False negatives are not element-wise independent
   (`sections/k_perfect_hashing.tex`, intro).** The previous version said the
   error counts are two independent binomials, FN ~ Bin(m, omega), making the
   k-perfect PHF "a genuine second-order Bernoulli set". Losses in a shared
   slot are dependent (a slot with L members displaces exactly L - 1).
   Counterexample: m = N = 2, k = 2, wide fingerprints: the FN count is 0 or 1
   with probability 1/2 each, whereas Bin(2, 1/4) gives (9/16, 6/16, 1/16). The
   text now says the variant has the stated marginal channel but is not an
   element-wise independent Bernoulli set.
6. **Space efficiency of k-perfect false negatives (`sections/rd_ph_filter.tex`
   footnote, new Remark in Sec. 5).** The previous footnote said k-perfect
   hashing is a more efficient way to admit false negatives than approximating
   a subset. For space this is backwards. At load factor r the single-fingerprint
   design spends M/(1 - e^-r) fingerprint bits per retained member, versus about
   M + log2 e for a minimal PHF on a lossy subset. At r = 1, M = 16 these are
   25.3 and 17.4 bits. The footnote and a new remark now say so; the advantage
   of k-perfect hashing is construction cost only.
7. **Maximum-entropy claims (`sections/rd_ph_filter.tex` Theorem 3.4,
   `sections/pmf.tex` Theorem 6.2).** The previous
   version said every bit of the code, including the perfect-hash seed, is an
   independent fair coin. The seed is the index of the first success, a
   geometric variable, whose bits are not uniform; for r < 1 the unused rows are
   fixed. The statements now hold for the fingerprint matrix of the minimal
   PHF, and for the seed only to leading order (entropy and expected length
   agree up to O(1) bits per structure).
8. **False-negative space bound (`sections/rd_ph_filter.tex`, Theorem 3.2).**
   The previous version asserted, without source, that a Bernoulli set with
   false negative rate omega "admits an encoding" of -(1 - omega) log2 eps bits
   per element, which the PHF "attains" at omega = 0. The bound is credited to
   Pagh and Rodler (ESA 2001, Prop. 1), stated as a lower bound up to
   lower-order terms that a lossy subset achieves, and the PHF is said to
   approach (not attain) the omega = 0 case as eps -> 0.

The k-perfect claims (items 3 to 6) were checked by exact rational enumeration
of all placements for m, N <= 4 and all k <= m, M in {1, 2}
(scratch script `kperfect_enum.py`, not part of the repository).

## Citations added

DOIs were checked on 2026-10-21 (title and authors match).

- `pagh2001lossy`: Rasmus Pagh and Flemming Friche Rodler, *Lossy
  Dictionaries*, Algorithms: ESA 2001, LNCS 2161, pp. 300-311 (2001).
  DOI 10.1007/3-540-44676-1_25. Crossref.
- `lehmann2025seeds`: Hans-Peter Lehmann, Peter Sanders, Stefan Walzer and
  Jonatan Ziegler, *Combined Search and Encoding for Seeds, with an
  Application to Minimal Perfect Hashing*, ESA 2025, LIPIcs 351, 109:1-109:18
  (2025). DOI 10.4230/LIPIcs.ESA.2025.109. Registered with DataCite, not
  Crossref (Crossref returns 404); verified through the DataCite REST API.

Existing entries now cited for new purposes (DOIs re-checked against
Crossref): `dietzfelbinger2008` (10.1007/978-3-540-70575-8_32, credited for
the construction itself) and `chd` (Belazzougui, Botelho and Dietzfelbinger,
*Hash, Displace, and Compress*, ESA 2009, 10.1007/978-3-642-04128-0_61,
credited for k-perfect hashing). `bloomier` and `pagh2005` (SODA 2004 and
2005) have no Crossref DOI; they were already in the bibliography.

## Claims withdrawn or narrowed

- Any contribution claim for the construction or its analyses (now: none).
- The PHF's advantage over salt search via "combinatorial subset enumeration".
- "The k-perfect PHF is a genuine second-order Bernoulli set" with binomial FN
  counts.
- "k-perfect hashing generates a more efficient solution" than a lossy subset.
- "Every bit of the code is an independent fair coin".

## Build

`cd paper && TEXINPUTS=".:./sty:" pdflatex -shell-escape main.tex && makeglossaries main && bibtex main && TEXINPUTS=".:./sty:" pdflatex -shell-escape main.tex && TEXINPUTS=".:./sty:" pdflatex -shell-escape main.tex`

Result: exit 0, 0 LaTeX errors, 0 undefined references, 0 undefined
citations, 0 BibTeX warnings, 37 pages. The status box renders at the top of
page 2 (the abstract fills page 1).

## Known remaining issues (not fixed in the freeze)

- `img/phfilter.tex` is still a stub figure.
- No experiments (the planned maph measurements were never added).
- The PMF entropy theorem leans on the companion map and entropy papers for the
  content-coding argument; that argument was not re-audited here.
- The comparisons to the Bernoulli hash function inherit that paper's framing;
  see its own ERRATA.md for the corrections there.
