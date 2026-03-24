# Citation Verifier Report

**Paper**: Bernoulli sets: a model for sets with random errors
**Date**: 2026-02-27

## Summary
The bibliography contains 25 entries. 22 are actively cited in the compiled manuscript. 3 entries are orphaned (from a removed section). The citations are generally accurate but there are missing references for key claims.

## Findings

### Major Issues

**C1. Orphaned bibliography entries (references.bib)**
- **Entries**: `songWagnerPerrig`, `curtmola`, `cashDynamic`
- **Problem**: These 3 entries are defined in references.bib but not cited anywhere in the compiled manuscript. They were previously cited in `sections/unused/bool_search.tex`, which has been removed from the build.
- **Suggestion**: Remove these entries from references.bib.

**C2. Missing citation for the space lower bound (Proposition 8.1)**
- **Location**: entropy.tex lines 122-162
- **Problem**: The $-\log_2 \fprate$ bits per element lower bound is a well-known result typically attributed to Carter, Floyd, Gill, Markowsky, and Wegman (1978), "Exact and Approximate Membership Testers." The paper presents this with its own proof but does not cite the original source.
- **Suggestion**: Add: `@inproceedings{carterFGMW1978, author={J. L. Carter and R. W. Floyd and J. Gill and G. Markowsky and M. N. Wegman}, title={Exact and Approximate Membership Testers}, booktitle={Proceedings of the 10th ACM Symposium on Theory of Computing (STOC)}, year={1978}, pages={59--65}}` and cite it in the proposition statement.

**C3. Missing citation for the delta method / Taylor expansion technique**
- **Location**: distributions.tex lines 285-298, appendix.tex lines 29-147
- **Problem**: The second-order Taylor expansion technique for the expected value of a ratio of random variables is the well-known "delta method" in statistics. No citation is provided.
- **Suggestion**: Cite a standard statistics reference, e.g., Casella & Berger "Statistical Inference" or van der Vaart "Asymptotic Statistics."

### Minor Issues

**c1. Self-citations to unpublished work (references.bib)**
- **Entries**: `phf` (Perfect Hash Filter) and `shs` (Singular Hash Set) are both listed as "Working paper. Available from the author upon request."
- **Problem**: These are not publicly verifiable. While self-citation is acceptable, readers cannot access these works.
- **Suggestion**: If possible, make these available as preprints (e.g., on arXiv) and update the citations.

**c2. Ribbon filter citation is an arXiv preprint (references.bib)**
- **Entry**: `ribbonFilter` is cited as "arXiv preprint arXiv:2103.02515" (2021)
- **Problem**: This paper has since been published in the proceedings of VLDB 2022.
- **Suggestion**: Update the citation to the published version.

**c3. No citation for the Borel-Cantelli lemma used in the appendix**
- **Location**: appendix.tex line 24
- **Problem**: The proof uses the Borel-Cantelli lemma without citation. While this is a standard result, a reference to Feller (1968) or a probability textbook would be appropriate.
- **Suggestion**: Add a brief citation, e.g., "by the Borel--Cantelli lemma (see Feller [1968])."

**c4. Missing reference for Warner's randomized response in references.bib**
- **CORRECTION**: This is actually correctly cited. Entry `warner1965` is present.

## Citation Count Summary
- Active citations in compiled text: 22
- Orphaned entries: 3 (songWagnerPerrig, curtmola, cashDynamic)
- Missing key citations: 2 (Carter et al. 1978 for space bound, delta method reference)
- Entries needing update: 1 (ribbonFilter)
