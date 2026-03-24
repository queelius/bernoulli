# Citation Verifier Report

**Paper**: Composition of Bernoulli sets
**Date**: 2026-03-19

## Summary

The bibliography contains 6 entries. 5 are cited in the paper. 1 is unused. All cited references appear to be correctly attributed.

## Findings

### Minor: Unused bibliography entry `coverThomas`
- **Location**: `references.bib`, line 41
- **Problem**: The `coverThomas` entry (Cover & Thomas, "Elements of Information Theory", 2006) is defined but never cited in this paper. It is cited in the companion paper `bernoulli_sets/` for the channel matrix product theorem.
- **Suggestion**: Either cite it in the parametric parsimony remark (Remark 3.5, where the Kronecker product / channel composition connection is discussed) or remove it from this paper's bibliography to avoid a dangling entry.

### Verification of Cited References

| Key | Cited in | Attribution | Status |
|-----|----------|-------------|--------|
| `bernoulliSets` | intro, prelim, set_theory, uncertain_rates, conclusion | Companion paper axioms and distributions | CORRECT |
| `bernoulliMeasures` | conclusion | Companion paper on classification measures | CORRECT |
| `bernoulliEntropy` | conclusion | Companion paper on entropy | CORRECT |
| `basicinterval` | uncertain_rates | Hickey, Ju, Van Emden (2001) JACM interval arithmetic | CORRECT |
| `mooreInterval` | uncertain_rates | Moore (1966) foundational interval analysis | CORRECT |
| `coverThomas` | (unused) | Cover & Thomas (2006) information theory | UNUSED |

### Cross-Reference Accuracy
- All `\cref` cross-references resolve correctly (no undefined reference warnings in build log).
- The references to the companion paper's specific results (e.g., "[Axiom 1]", "[Prop. 1]", "[Def. 3]") in the preliminaries section use explicit citation annotations like `{\cite[Axiom~1]{bernoulliSets}}`, which is appropriate for cross-paper references.

### Missing References
- The parametric parsimony remark discusses Kronecker products of channel matrices but does not cite a source for this standard result. The companion paper cites Cover & Thomas for this; the same citation would be appropriate here.
- No references to the Bloom filter literature are included, despite the introduction and conclusion mentioning Bloom filters. The companion paper presumably covers these citations, but a brief citation here would make this paper more self-contained.
