# Novelty Assessor Report

## Overall Assessment

The paper makes a genuine but incremental contribution. The unification of sets and maps under a single construction is clean. The threshold predicate generalization is a natural extension. The adaptive threshold variant is the most novel contribution and is interesting. However, the paper's central claim -- achieving the information-theoretic space lower bound -- is a known achievability result. The novelty lies in the specific construction mechanism, not in the achievability itself.

## Findings

### MAJOR-1: Space-optimality achievability is known
- **Problem**: The paper's third contribution ("information-theoretic optimality") frames the result as if achieving the lower bound is new. However, Carter et al. (1978) established the lower bound, and Pagh, Pagh & Rao (2005) showed it is achievable (with polynomial construction time, unlike the BHF). The paper does not cite or discuss these prior results.
- **Suggestion**: Clearly distinguish the BHF's contribution from prior achievability results. The novelty is the specific salt-search construction with maximum entropy (not just space optimality), and the adaptive variant. Frame accordingly.
- **Severity**: Major -- the paper risks appearing to claim credit for a known result.

### MAJOR-2: Comparison with modern filters is absent
- **Problem**: The discussion (Section 9) compares only with Bloom filters and the author's own PHF. It omits cuckoo filters (Fan et al. 2014), XOR filters (Graf & Lemire 2020), ribbon filters (Dillinger & Walzer 2021), and binary fuse filters -- all of which are closer to the lower bound than Bloom filters and have practical construction times.
- **Suggestion**: Add a comparison table or paragraph covering modern filter constructions. This would better position the BHF's contribution: it achieves the exact bound (unlike practical filters) but requires exponential construction time (unlike practical filters). The adaptive variant is the bridge.
- **Severity**: Major -- incomplete related work undermines the contribution's positioning.

### MINOR-1: The "unified construction" contribution is straightforward
- **Problem**: The first contribution (unified set/map construction where set is mu=0) is natural and not particularly surprising. Any filter that stores per-element data can trivially be extended to a map by concatenating value bits.
- **Suggestion**: De-emphasize this as a standalone contribution; present it as a design choice rather than a contribution.
- **Severity**: Minor -- does not undermine the paper but inflates the contribution count.

### MINOR-2: The adaptive threshold is the strongest contribution but is underdeveloped
- **Problem**: The adaptive threshold (Section 3.5) is the most novel element. It eliminates salt search, achieves O(log N / m) -> 0 space, and has a clean Beta-distributed FPR. However, it receives only one subsection in Section 3 and brief treatment in Sections 5 and 6. It deserves more development: applications, empirical evaluation, formal comparison with other approaches.
- **Suggestion**: Consider expanding the adaptive threshold treatment. It could be the paper's main contribution rather than a variant.
- **Severity**: Minor -- missed opportunity to strengthen the paper.

## Contribution Summary

| Contribution | Novelty | Significance |
|---|---|---|
| Unified set/map construction | Low | Low -- straightforward generalization |
| Threshold predicate | Medium | Medium -- natural but useful generalization |
| Adaptive threshold | High | High -- novel construction with strong properties |
| Space optimality proof | Low-Medium | Medium -- known achievability, but specific construction and max entropy are new |
| Maximum entropy property | Medium | Medium -- relevant for encrypted search applications |

## Recommendation

The paper should be reframed around the adaptive threshold as the primary contribution, with the fixed-threshold constructions serving as background. The space optimality of the fixed-threshold construction should be presented as confirming a known result via a specific mechanism, not as a new discovery. The comparison with the literature needs substantial expansion.
