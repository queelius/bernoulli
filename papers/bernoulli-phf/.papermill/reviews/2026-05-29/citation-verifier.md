# Citation Verifier Report, The Perfect Hash Filter

**Date**: 2026-05-29
**Scope**: Citation accuracy, missing references, bibliography integrity. All `\cite` keys and all `references.bib` entries audited.

## Summary

The bibliography is in better shape than the `state.md` "Bibliography 25%" rating suggests: it contains 16 real, well-formed external references (Bloom, CFGMW, FKS, Mehlhorn, CHD, cuckoo, xor, ribbon, Bloomier, Pagh-Pagh-Rao, Dietzfelbinger-Pagh, Zadeh, Manning, Zobel-Moffat, etc.), most with DOIs. The real problems are: (1) 9 of the 9 author self-citations are `@unpublished` placeholders, and several carry load-bearing quantitative claims; (2) a striking gap between the rich `.bib` and the prose, which cites only 7 keys total and engages essentially none of the real AMQ references; (3) two cited keys (`emaps`, plus the body's `\cite{}` empty calls) and a handful of `\cite` targets that resolve to placeholders; (4) the most important prior-art references for the paper's own construction (xor `graf2020`, Bloomier `bloomier`, cuckoo `fan2014`) are present in the file but never cited in the text.

Severity counts: Critical: 0 | Major: 3 | Minor: 3

---

## Citation inventory

**Keys actually cited in the manuscript** (across all sections): `bf`, `bsets`, `bmaps`, `emaps`, `obset`, `phf`, `shs`, plus `oph` (in `rd_ph_filter.tex`), `chd` (in `rd_ph_filter.tex`), and an empty `\cite{}` (twice). That is roughly 9 distinct keys.

**Keys defined in `references.bib`** (25 total): self-citations `aset, obset, oph, pmf, phf, bsets, bmaps, emaps, shs` (9, all `@unpublished`); perfect hashing `chd, simple, fks, mehlhorn1982` (4); Bloom/membership `bloom1970, bf` (2); info-theoretic bounds `carter1978, pagh2005, dietzfelbinger2008` (3); modern filters `fan2014, graf2020, dillinger2021, bloomier` (4); fuzzy/IR `zadeh1965, zobel2006, manning` (3).

**Net**: 16 real entries are present; about 11 of them are never cited (`bloom1970, simple, fks, mehlhorn1982, carter1978, pagh2005, dietzfelbinger2008, fan2014, graf2020, dillinger2021, bloomier, zadeh1965, zobel2006, manning` are mostly uncited in the compiled prose; only `bf` and `chd` are used). This is the inverse of the usual problem: the references exist but are not deployed.

---

## Major

### V1. All nine self-citations are unpublished placeholders, and several are load-bearing
- **Location**: `references.bib` lines 5 to 57 (`aset, obset, oph, pmf, phf, bsets, bmaps, emaps, shs`), all `@unpublished{... note={Manuscript in preparation}}` (or "This paper" for `phf`).
- **Problem**: Three of these carry quantitative or strong qualitative claims the paper relies on:
  - `oph` is cited in `rd_ph_filter.tex` line 230 as the source of "Theorem 3" for the perfect-hash space lower bound, which underlies the paper's headline space result. An unpublished, untitled-in-venue manuscript cannot support a load-bearing theorem.
  - `shs` is cited in `adt.tex` line 340 as "a theoretical data structure that optimally implements the abstract data types of the Bernoulli set and the oblivious set", a strong optimality claim resting on a non-existent paper.
  - `bsets` and `bmaps` are the family foundation (Bernoulli sets, Bernoulli map). These at least exist as real drafts in the same monorepo (`papers/bernoulli_sets/`, `papers/bernoulli_maps/`) and can be upgraded to proper citations now.
- **Suggestion**: Upgrade `bsets`, `bmaps` (and `phf` self) to real citations using the family papers' actual titles/years. For `oph` and `shs`: either prove the invoked results inline in this paper, or mark the dependent claims explicitly as "shown in forthcoming work" and weaken the abstract/`adt.tex` claims accordingly. The `state.md` note about `example.com` URLs is slightly stale: the current `.bib` entries have no URL fields, just "Manuscript in preparation" notes, which is cleaner but still uncitable.

### V2. The real prior-art references are present but never cited; key construction-level citations missing from the text
- **Location**: prose across all sections vs `references.bib`.
- **Problem**: The paper's own construction is the MPHF+fingerprint AMQ, yet:
  - `graf2020` (xor filter), `fan2014` (cuckoo filter), `dillinger2021` (ribbon filter), `pagh2005` (optimal Bloom replacement), `dietzfelbinger2008` (retrieval/AMQ), `carter1978` (the lower bound the paper invokes informally as a "postulate") are all in the `.bib` but cited nowhere in the compiled prose. `carter1978` is especially notable: the paper states the `-log2 eps` lower bound as `\begin{postulate}` (`rd_ph_filter.tex` line 210, `adt.tex` line 280) when it is in fact a published theorem (CFGMW 1978) that should be cited, not postulated.
  - `bloomier` (Bloomier filter) is the closest prior art for the Perfect Map Filter (`pmf.tex`) and is uncited there.
- **Suggestion**: Cite `carter1978` at both "postulate" sites and reclassify the lower bound as a known result. Add a related-work section deploying `graf2020, fan2014, dillinger2021, pagh2005, dietzfelbinger2008`. Cite `bloomier` in `pmf.tex`. This is low-effort because the entries already exist.

### V3. Empty `\cite{}` calls in the core section
- **Location**: `rd_ph_filter.tex` line 387 ("According to \cite{}, the probability mass of the perfect hash function is given by ..."), and the two `\tag{\ref{} revisited}` on lines 437 and 462.
- **Problem**: A specific pmf is asserted on an empty citation; two equation cross-tags reference an empty `\ref{}`. These render as `[?]` / `(??)` and signal an unfinished authority.
- **Suggestion**: Supply the source (likely `oph`) or derive the pmf; fill the `\ref{}` tags with the correct equation labels.

---

## Minor

### v1. `emaps` cited but corresponds to a tangential family paper
- **Location**: `k_perfect_hashing.tex` line 10 ("From the perspective of the entropy map framework~\cite{emaps}").
- **Problem**: `emaps` ("Entropy maps") is an `@unpublished` placeholder; the reference is decorative (the sentence works without it) and currently uncitable.
- **Suggestion**: Either drop the parenthetical or upgrade `emaps` if the paper exists.

### v2. `bloom1970` (the original Bloom paper) is unused while `bf` (a survey) carries all Bloom citations
- **Location**: Bloom claims cite `bf` (Broder-Mitzenmacher survey) at `intro.tex` line 11, `rd_ph_filter.tex` line 17, `adt.tex` line 330.
- **Problem**: The 1.44/`ln 2` space result and the structure itself are due to Bloom (1970, `bloom1970`, present in the `.bib`); citing only the survey is imprecise.
- **Suggestion**: Cite `bloom1970` for the original structure and bound; keep `bf` for the survey context.

### v3. Bibliography style/key hygiene
- **Location**: `references.bib`.
- **Problem**: `graf2020` is typed as `@inproceedings` but has `journal=` and `volume=`/`pages=` fields (it is a journal article in ACM JEA); `dillinger2021` has `year={2022}` with key `2021` (ITCS 2022). Minor field/key mismatches that BibTeX will mostly tolerate but should be tidied.
- **Suggestion**: Fix the entry type for `graf2020` to `@article`; reconcile the `dillinger2021`/2022 key-year.

---

## Notes

- No evidence of fabricated or hallucinated external citations: the 16 real entries are recognizable, correctly attributed works in this subfield with plausible DOIs (spot-checked against memory; `chd`, `bloom1970`, `carter1978`, `fan2014`, `graf2020`, `bloomier`, `fks`, `mehlhorn1982`, `zadeh1965`, `manning`, `zobel2006` all check out by author/venue/year).
- The fastest, highest-value citation work is purely deployment: the paper already owns the right references; it needs to cite them in a related-work section and at the lower-bound "postulate."
