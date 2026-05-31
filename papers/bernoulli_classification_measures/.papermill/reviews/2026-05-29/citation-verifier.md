# Citation and Reference Review

**Paper**: Binary classification measures for random approximate sets
**Reviewer role**: citation-verifier (performed by area chair)
**Date**: 2026-05-29

## Bibliography integrity: PASS

- `references.bib` has 11 entries. I confirmed by direct count and by checking each key's citation usage in the source.
- 9 entries are cited; 2 are unused: `feller2` (Feller, vol. 2) and `coverThomas` (Cover and Thomas). This matches the known pre-existing item. Because the document uses `\bibliographystyle{plain}` with `\bibliography` (not a print-all style), the unused entries do **not** appear in the rendered bibliography. They are harmless `.bib` clutter.
- BibTeX ran clean: no warnings, no missing fields that break the build, no undefined `\cite` keys in the LaTeX log.

## Per-citation check

| Key | Used | Where | Notes |
|---|---|---|---|
| bernoulliSets | yes (x11) | throughout | Companion; Unpublished. Inherited foundation. Fine. |
| bernoulliComposition | yes (x2) | interval section | Companion; Unpublished. Fine. |
| fawcettROC | yes | related work, sec 3 | Real (Fawcett 2006, Pattern Recognition Letters). Correct. |
| powersEval | yes | related work, sec 3 | Real (Powers 2011). Correct. |
| casellaBerger | yes | Thm 3.1 (delta method) | Real (Casella and Berger, 2nd ed). Appropriate anchor for the delta method. |
| bf | yes (x2) | intro, conclusion | Real (Bloom 1970, CACM). Correct. |
| phf | yes | conclusion | Author working paper; "available upon request". Acceptable for a companion but weak as a citable source (see below). |
| basicinterval | yes | interval section | Real (Hickey, Ju, Van Emden 2001, JACM). Correct. |
| mooreInterval | yes | interval section | Real (Moore, Interval Analysis 1966). Correct. |
| feller2 | NO | unused | Remove or use. |
| coverThomas | NO | unused | Remove or use. |

## Findings

### MINOR-1: Two unused bibliography entries
- **Location**: `references.bib` keys `feller2`, `coverThomas`.
- **Problem**: Declared but never cited. No effect on the rendered PDF (plain style omits uncited entries) but they signal incomplete cleanup.
- **Suggestion**: Either remove them, or cite them where relevant. `feller2` could support the binomial/CLT statements in the preliminaries or Appendix C; `coverThomas` is more naturally used in the entropy companion paper, so likely just remove it here.

### MAJOR-1 (cross-listed with novelty-assessor MAJOR-1/2): Missing prior-art citations
- **Problem**: Two pieces of directly relevant prior art are absent (see literature-context.md and novelty-assessor.md):
  1. A standard **PPV-vs-prevalence / base-rate** source, to back the sentence "well known in medical testing." Currently uncited.
  2. **Goutte and Gaussier (2005), ECIR**, "A probabilistic interpretation of precision, recall and F-score" (and optionally Brodersen et al. 2010 on balanced-accuracy posteriors), as the closest prior distributional treatment of these measures.
- **Impact**: The related-work coverage (only Fawcett and Powers) is thin for the claims made. This is the most consequential citation gap.
- **Suggestion**: Add the two items above and one sentence each distinguishing them. Verify the Goutte and Gaussier details against an index before citing (I flag it as likely-real but unconfirmed here).

### MINOR-2: `phf` citation is not externally retrievable
- **Location**: conclusion, `\cite{phf}`.
- **Quoted bib note**: "Working paper. Available from the author upon request."
- **Problem**: An "upon request" reference is hard for a reviewer or reader to verify. Within the family this is acceptable, but if a Zenodo DOI or arXiv id exists for the perfect-hash-filter paper, use it.
- **Suggestion**: Replace with a DOI/URL if available, consistent with how `bernoulliSets` will eventually be cited.

### SUGGESTION-1: Give the companion papers stable identifiers
`bernoulliSets` and `bernoulliComposition` are `@Unpublished` with no DOI/URL. Since this paper already has a Zenodo DOI (10.5281/zenodo.19104550), the companions likely do too. Adding `doi`/`url` fields would let the bibliography resolve for external readers and is consistent with the family's deposition.

## No fabricated or mismatched citations found
Every `\cite` resolves to a bib entry whose author/title is consistent with how it is used in text. No quotation of a nonexistent work. The only issues are omissions (missing prior art) and two unused entries.
