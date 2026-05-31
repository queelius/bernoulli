# Citation Verifier Report, bernoulli_maps

**Specialist**: citation-verifier (citation accuracy, missing references, bibliography integrity)
**Date**: 2026-05-29
**Method**: Cross-checked the 15 keys defined in `references.bib` against every `\cite*` in `main.tex` and `sections/*.tex`; checked bibliographic accuracy of each entry against reference knowledge; scanned prose for cited-by-name-but-not-by-key works. Build emitted zero undefined-citation and zero undefined-reference warnings (verified in the `pdflatex` pass-3 log).

## Verdict summary

Bibliography integrity is good: all 15 entries are used, there are no undefined citations, no unused entries, and the entries themselves are bibliographically accurate. The defects are (1) **two companion papers referenced in prose but absent from the bibliography** (the random-approximate-algebraic-types paper and the composition-of-Bernoulli-sets paper), which leaves load-bearing cross-paper claims uncitable, and (2) a few **imprecise attributions** to general textbooks where a primary source exists. None is critical; the first is major because the novelty boundary with `data_type` depends on it.

## MAJOR findings

### M9. Two companion papers are cited in prose but missing from `references.bib` (source: citation-verifier)
- **Location**: 
  - `intro_new.tex:36` and `conclusion.tex:17`, `special_cases.tex:105`: "A companion paper on random approximate algebraic types ..." (the `bernoulli_data_type` paper), referenced three times, **no bib key, no `\cite`**.
  - `intro_new.tex:35`: "companion papers on Bernoulli sets [aset] and their composition"; `composition_new.tex:445`: "developed systematically in the companion paper on composition of Bernoulli sets". This is the `bernoulli_composition` paper, **no bib key, no `\cite`**.
- **Problem**: Both are real papers in the same family (the foundation cites them as `bernoulliComposition` and `bernoulliEntropy`). Referencing them by description only means: (a) the reader cannot locate them; (b) the novelty boundary between this paper and `data_type` (which, per the novelty-assessor, share the Kronecker-factorization headline) is not checkable; (c) the "two perspectives, one theorem" conclusion paragraph points at a paper with no handle. By contrast `aset` and `arelation` *are* in the bib as `@Unpublished` companion entries, so the omission of `data_type` and `composition` is an inconsistency in how companions are handled.
- **Why major**: the data_type reference in particular underpins a contribution-level claim (Contribution 1 / the function-space viewpoint shared with data_type). An uncitable companion for a load-bearing boundary is a real gap.
- **Suggestion**: add `@Unpublished` entries mirroring the existing `aset`/`arelation` format:
  - `data_type` (title approx. "Random approximate values over algebraic types" or the algebraic-types sub-paper title), `\cite`d at the three prose locations.
  - `composition` (title "Composition of Bernoulli sets"), `\cite`d at `intro_new.tex:35` and `composition_new.tex:445`.
- **Confidence**: high.

## MINOR findings

### m16. The AMQ / membership space lower bound is attributed to Cover and Thomas, where a primary source is standard (source: citation-verifier)
- **Location**: `shm.tex` corollary (`-log2 eps` "information-theoretic lower-bound for first-order random positive approximate sets ... ~\cite{cover2006}"); also `entropy_maps.tex` sec:prob-success uses the same bound.
- **Problem**: The `-log2 eps` (equivalently `log2(1/eps)`) bits-per-element floor for approximate membership is classically Carter, Floyd, Gill, Markowsky, Wegman, "Exact and approximate membership testers" (STOC 1978), with the tight AMQ bound `n log2(1/eps)` due to Pagh, Pagh, Rao (2005). Cover and Thomas is a general information-theory text and does not state the AMQ-specific bound. Citing it is not wrong (the bound follows from source-coding principles) but it is imprecise for a result the paper leans on.
- **Suggestion**: add Carter et al. 1978 (and optionally Pagh-Pagh-Rao 2005) and cite them for the membership floor; keep Cover-Thomas for general source coding.
- **Confidence**: high.

### m17. `thm:optimal-code` attributes the source coding theorem correctly but the entry could be sharper (source: citation-verifier)
- **Location**: `entropy_maps.tex`, `thm:optimal-code` ("By Shannon's source coding theorem ... ~\cite{shannon1948}").
- **Problem**: Fine as-is; `shannon1948` is the correct primary source for source coding. (Noting only that the *prefix-free* / Kraft-McMillan framing the paper uses is usually paired with a coding text; Cover-Thomas ch.5 would be the standard companion cite. Optional.)
- **Confidence**: high.

### m18. No citation for the Iverson bracket or Huffman coding where introduced (source: citation-verifier)
- **Location**: `bernoulli_map.tex` `def:iverson` (Iverson bracket); `bernoulli_map.tex` remark on "generating a Huffman code"; `bernoulli_map.tex` Golomb/Elias codes.
- **Problem**: Minor scholarly-completeness gaps. The Iverson bracket (Knuth's popularization) and Huffman/Golomb/Elias codes are named without citation. For a theory paper these are common-knowledge enough to pass, but Huffman and Golomb in particular are cheap, standard cites if the author wants completeness.
- **Suggestion**: optional; add Huffman 1952 and Golomb 1966 if a fuller bibliography is desired. Not required.
- **Confidence**: medium.

### m19. `@Unpublished` companion entries lack any locator (source: citation-verifier)
- **Location**: `references.bib`, `aset` and `arelation` entries.
- **Problem**: Both are `@Unpublished` with `note={Companion paper}` and `year={2026}` but no URL, repository, or "in preparation" status. For an unpublished-companion citation this is acceptable, but if any of these reach a public repo (the family has per-paper GitHub remotes), adding a `note` with the repo or "available at ..." would help readers. Cosmetic.
- **Confidence**: medium.

## Bibliography integrity checklist
- All 15 defined keys are cited: PASS (verified: defined set == used set, both 15 keys, identical lists).
- No undefined citations: PASS (zero `Citation ... undefined` in build log).
- No unused bib entries: PASS.
- Entry accuracy (authors, venues, years): PASS. Spot-checked: Bloom 1970 CACM 13(7):422-426 correct; Chazelle et al. 2004 SODA correct; Carter-Wegman 1979 JCSS 18(2) correct; FKS 1984 JACM 31(3):538-544 correct; Dietzfelbinger-Pagh 2008 ICALP correct; Fan et al. 2014 CoNEXT correct; Shannon 1948 BSTJ correct; Cover-Thomas 2006 2nd ed correct; Song-Wagner-Perrig 2000 S&P correct; Curtmola et al. 2006 CCS correct. No errors found.
- Missing references for prose claims: 2 companion papers (M9); imprecise AMQ-bound attribution (m16).

## Net
Bibliography is clean and accurate. The one consequential gap is the two missing companion-paper entries (M9), of which the `data_type` omission matters most because the novelty boundary depends on it. Everything else is optional polish.
