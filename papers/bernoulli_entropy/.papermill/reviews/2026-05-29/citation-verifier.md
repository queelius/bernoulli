# Citation Verifier Report, bernoulli_entropy

**Reviewer role**: Citation accuracy, missing references, bibliography integrity
**Date**: 2026-05-29
**Method**: Cross-checked every `\cite` key against `references.bib` and against the rendered `main.bbl`; assessed each entry's metadata; checked claim-to-citation correctness; identified missing must-cites.

## Bibliography integrity (mechanical)
- **8 cite keys used**: `bernoulliComposition` (x1), `bernoulliSets` (x4), `bf` (x3), `carterExact` (x5), `coverThomas` (x2), `phf` (x1), `shannonBSC` (x2), `shs` (x1).
- **8 keys defined** in `references.bib`; **8 rendered** in `main.bbl`.
- **No orphan entries** (every defined key is cited) and **no dangling cites** (every cited key is defined). Build produced no "undefined citation" warnings. Bibliography is internally clean.

## Per-entry metadata check
| Key | Type | Assessment |
|---|---|---|
| `bernoulliSets` | Unpublished | Companion paper. Fine as Unpublished; ideally add a URL/arXiv id or "in preparation" before submission. |
| `bernoulliComposition` | Unpublished | Same. |
| `shannonBSC` | article | Shannon 1948, BSTJ, vol 27(3), pp 379-423. Metadata correct. **Key name `shannonBSC` is misleading** (suggests "binary symmetric channel"); the work is the general theory. Recommend rename to `shannon1948`. The paper's prose also mis-scopes it (see prose-auditor MINOR-3). |
| `coverThomas` | book | Cover & Thomas 2e, Wiley 2006. Correct. Caveat: the O(1/n) binomial-entropy expansion the paper attributes to it is *folklore* and not a numbered result in that text; a page/equation anchor or a more specific source would be more honest (see MISSING-3). |
| `carterExact` | inproceedings | Carter, Floyd, Gill, Markowsky, Wegman, "Exact and Approximate Membership Testers," STOC 1978, pp 59-65. Metadata correct; correct primary source for the -log2(eps) bound. Good. |
| `bf` | article | Bloom 1970, CACM 13(7), pp 422-426. Correct. |
| `phf` | Unpublished | Author's Perfect Hash Filter working paper. "Available from the author upon request" is weak for a citation a reader may want to follow; provide a stable reference if possible. |
| `shs` | Unpublished | Author's Singular Hash Set working paper. Same caveat. |

## Claim-to-citation correctness
- `carterExact` for the lower bound: **correct attribution.**
- `bf` for the Bloom filter and its space cost: **correct.**
- `coverThomas` for the binomial entropy expansion: **acceptable but imprecise** (folklore; not a labeled theorem there).
- `shannonBSC` for "entropy of binary channels": citation is the right paper, but the *claim wording* mis-scopes Shannon's contribution (prose issue, not a wrong citation).
- `bernoulliSets` for the axioms and the FP/FN binomial distributions: **correct** (companion foundation).
- `bernoulliComposition` for the future compositional extension: **correct, forward reference.**

## Missing references

### MAJOR (MISSING-1): Yao 1977 is invoked in a proof but absent from the bibliography
- **Location**: `sections/space_complexity.tex` line 25: "the extension to randomized data structures follows from Yao's minimax principle."
- **Problem**: A named principle is used as a load-bearing proof step with **no citation**. Confirmed absent from the 8-entry bib.
- **Fix**: Add **Yao, A. C.-C., "Probabilistic Computations: Toward a Unified Measure of Complexity," Proc. 18th FOCS, 1977, pp 222-227** and cite it at that sentence. (See logic-checker MAJOR-2 for the accompanying need to instantiate the principle.)

### MAJOR (MISSING-2): Pagh, Pagh & Rao 2005 (optimal Bloom replacement) is the modern tight bound and is uncited
- **Location**: the lower-bound claim and the "Bloom is 69% efficient relative to the optimum" framing (`space_complexity.tex` lines 16-23, 72-78).
- **Problem**: The paper asserts -log2(eps) is "the optimum" and that Bloom reaches only ln2 of it, but never cites the result that establishes this bound is *achievable* to within (1+o(1)): **Pagh, R., Pagh, A., Rao, S. S., "An Optimal Bloom Filter Replacement," SODA 2005 / SIAM J. Comput.** This is the standard modern reference pairing a matching upper bound with the lower bound and is the natural citation for "Bloom is not optimal." Its absence weakens the contextualization of both the lower bound and the efficiency claim.
- **Fix**: Cite PPR 2005 alongside `carterExact` for the bound, and when stating Bloom's 69% efficiency, to indicate that near-optimal constructions exist (the author's own `phf`/`shs` are the family's instances).

### MINOR (MISSING-3): No citable source for the "Bloom optimum m/n = -log2(eps)/ln2 / 69%" folklore
- **Location**: `space_complexity.tex` lines 72-78 and the figure caption.
- **Problem**: The Bloom-filter optimal bits-per-element and the ln2 occupancy result are stated as known but uncited.
- **Fix**: Cite a standard source, e.g., **Broder & Mitzenmacher, "Network Applications of Bloom Filters: A Survey," Internet Mathematics 1(4), 2004**, or **Mitzenmacher & Upfal, *Probability and Computing***, for the m/n formula. Low effort, closes a small gap.

### MINOR (MISSING-4): One sentence of modern-AMQ context would help
- A single citation cluster acknowledging cuckoo filters (Fan et al., CoNEXT 2014), quotient filters, or XOR filters (Graf & Lemire, ACM JEA 2020) would situate the paper in the 2026 landscape rather than the 1970s-2005 arc. Optional but recommended for a paper read outside the family.

## Self-citation balance
Four of eight entries are the author's own (`bernoulliSets`, `bernoulliComposition`, `phf`, `shs`). For a companion paper this is expected, but three external citations (Shannon, Cover-Thomas, Carter et al.) plus Bloom is thin for an information-theory/data-structures paper. Adding Yao, PPR, and Broder-Mitzenmacher would both fill genuine gaps and improve the external/self ratio.

## Confidence
High. Mechanical integrity verified directly against bbl/aux. The two MAJOR missing references (Yao, PPR) are near-certain must-cites; metadata for the existing external entries is accurate.
