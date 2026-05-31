# Citation Verifier Report

**Paper:** The Bernoulli Hash Function
**Date:** 2026-05-29

## Overall Assessment

The bibliography has grown from 11 to 16 entries since the prior pass, and the
two most important prior omissions are fixed: Carter et al. (1978) is now cited
for the lower bounds, and Pagh-Pagh-Rao (2005) plus cuckoo, XOR, and ribbon
filters are now cited in the comparison. Bibliography integrity is good: every
`\cite` key resolves, and the build produces no undefined-citation warnings.

Remaining issues are: two uncited entries (`manning`, `oph`), the seven self-
citations still lack stable identifiers, and a few expected references are
absent (Bloomier filter, Dietzfelbinger-Pagh, Bellare-Rogaway).

## Citation Inventory (verified against build)

Keys cited in text (14): bernoulli_sets, bernoulli_maps, bernoulli_data_type,
phf, pmf, es, bloom1970, bf_survey, order_statistics, carter1978, pagh2005,
cuckoo_filter, xor_filter, ribbon_filter.

Keys defined but NOT cited (2): `manning`, `oph`.

Build status: no "undefined citation" or "undefined reference" warnings;
`main.bbl` generated; all `\cref`/`\Cref` resolve.

## Findings

### MAJOR-1: Missing the closest map prior art and retrieval theory
- **Location:** `sections/discussion.tex` comparison; `references.bib`.
- **Problem:** The paper claims a unified *map* construction but cites no
  approximate-map structure. Two expected references are absent:
  - **Bloomier filter:** Chazelle, Kilian, Rubinfeld & Tal (2004), "The Bloomier
    Filter: An Efficient Data Structure for Static Support Lookup Tables" (SODA).
    The canonical approximate-map / function-retrieval structure.
  - **Dietzfelbinger & Pagh (2008):** "Succinct Data Structures for Retrieval
    and Approximate Membership" (ICALP). The closest theory to the BHF's
    "value encoded in the hash evidence" mechanism.
- **Suggestion:** Add both and reference them in the comparison and in the map
  discussion. This is the single most defensible citation gap remaining.
- **Severity:** Major (cross-filed with novelty-assessor MAJOR-2).

### MINOR-1: Two uncited bibliography entries
- **Location:** `references.bib`: `manning` (Introduction to Information
  Retrieval) and `oph` (Cryptographic perfect hash function, 2017).
- **Problem:** Neither key appears in any `\cite` across the sources (verified by
  grep over `sections/` and `main.tex`). `manning` was flagged unused in the
  prior pass and is still unused; `oph` is newly unused. With `plainnat`,
  uncited entries simply do not appear in the rendered bibliography, so this is
  harmless to the output but is dead weight in the `.bib`.
- **Suggestion:** Either cite them where relevant (`manning` fits the encrypted-
  search / IR framing in `sec:discussion`; `oph` fits the obliviousness lineage)
  or remove them from `references.bib`.
- **Severity:** Minor.

### MINOR-2: Self-citations lack stable identifiers
- **Location:** `references.bib`: bernoulli_sets, bernoulli_maps,
  bernoulli_data_type, phf, pmf, oph, es (7 of 16).
- **Problem:** All are `@article` with `year` and (for some) `note = {Companion
  paper}`, no journal, venue, DOI, arXiv id, or URL. The paper's foundational
  ADT definitions trace to these. A referee cannot retrieve them. Unchanged from
  prior pass.
- **Suggestion:** Add arXiv ids or repository URLs. For the family papers, even
  a `howpublished`/`url` to the public monorepo would suffice. Where a result is
  load-bearing (FP/FN distributions, the lower bounds), keep the inline
  restatement so the paper remains verifiable without the companion.
- **Severity:** Minor (verifiability of foundations).

### MINOR-3: Random oracle model uncited
- **Location:** `sections/prelim.tex`, Def. 2.2 / Asm 2.1.
- **Problem:** The random-oracle assumption is central and standard but
  uncited. Expected reference: Bellare & Rogaway (1993), "Random Oracles are
  Practical" (CCS).
- **Suggestion:** Add the citation at Def. 2.2.
- **Severity:** Minor.

### MINOR-4: Discrete order-statistic PMF could cite a primary source
- **Location:** `sections/appendix.tex`, Thm `thm:os_pmf_detailed`; `shf.tex`
  Thm `thm:fpr_distribution` (cites order_statistics for the continuous limit).
- **Problem:** The continuous Beta limit cites David & Nagaraja (2003), good. The
  exact *discrete* PMF is derived from scratch (correctly, in the N >> m regime).
  A pointer to a discrete-order-statistics reference (e.g. Arnold, Balakrishnan
  & Nagaraja 2008) would let the reader cross-check.
- **Suggestion:** Add a one-line citation for the discrete case.
- **Severity:** Minor.

## Bibliography Integrity Checklist

| Check | Result |
|---|---|
| All cited keys exist in references.bib | YES |
| All bib entries are cited | NO (manning, oph unused) |
| External entries have complete metadata | YES (bloom1970, bf_survey, carter1978, pagh2005, cuckoo_filter, xor_filter, ribbon_filter, order_statistics, manning) |
| Self-citation entries have venue/identifier | NO (7 entries) |
| Undefined-citation warnings at build | NONE |

## Status vs Prior Pass

| Prior citation finding | Status |
|---|---|
| MAJOR missing Carter et al. (1978) | RESOLVED (cited at both lower bounds) |
| MAJOR missing Pagh/cuckoo/XOR/ribbon | RESOLVED (all cited in discussion) |
| MAJOR self-citations lack identifiers | OPEN (MINOR-2 here) |
| MINOR missing Bellare-Rogaway | OPEN (MINOR-3 here) |
| MINOR discrete order-stat citation | OPEN (MINOR-4 here) |
| MINOR Manning unused | OPEN (now joined by oph; MINOR-1) |
| (new) Bloomier / Dietzfelbinger-Pagh | OPEN (MAJOR-1 here) |
