# Methodology Audit Report

## Summary

This is a pure-theory companion paper with no empirical experiments, one worked
numerical example, and one analytic figure. Judged by the standard appropriate to
a theory paper (derivations must be reproducible from the text, assumptions
explicit, claims scoped), the methodology is mostly sound. The principal
methodological weakness is the practical applicability gap: the headline
operations (union FNR, intersection FPR, set-difference FPR) depend on partition
weights `w1, w2, w3` that require the unknown objective-set cardinalities, and the
paper acknowledges this but does not carry through any of the three proposed
remedies far enough to make the formulas usable. A second issue is that the
single numerical example exercises only the easy (unweighted) part of one formula
family.

## Critical Issues

None. No empirical claims are made that could be untrustworthy, and the analytic
derivations are reproducible (I reproduced every formula; see the logic report).

## Major Issues

### M1. The central formulas are not operational as presented: the partition weights require unknown cardinalities, and no remedy is developed to closure
- **Location**: Section 3, `rem:unknown_partitions`; Section 6 (Conclusion), "Open problems".
- **Quoted text**: "The partition weights $w_1, w_2, w_3$ require knowledge of the objective set cardinalities $|A_1|$, $|A_2|$, and $|A_1 \cap A_2|$, which are typically unknown in practice. Three approaches handle this: (a) ... interval-valued rates; (b) worst-case bounds ... optimizing the weights over the feasible region; (c) the cardinalities may be estimated from the approximate sets themselves ... with computable bias from the error rates."
- **Problem**: The paper's stated practical payoff (Conclusion: "A practitioner building a system on Bloom filters need not re-derive the error analysis ... yielding closed-form error rates and confidence intervals for any set-theoretic expression") is undercut by this gap. For the *weighted* rates (union FNR, intersection FPR, difference FPR) the practitioner cannot evaluate the formula without `|A1 ∩ A2|`, which is exactly what an approximate-set system does not know exactly. Approach (b) (optimize over the simplex `w1+w2+w3=1`) is the one remedy that is always available and would yield guaranteed worst-case bounds, but it is mentioned in a single clause and never worked out. Approach (c) is stated as a research direction in the Conclusion, confirming it is not delivered here.
- **Impact**: Without at least the worst-case optimization carried through, a reader cannot apply the weighted formulas to real filters; only the unweighted ones (union FPR, intersection FNR, complement) are directly usable. This is a significant limit on the paper's claimed practical reach.
- **Fix**: Develop approach (b) explicitly: maximize and minimize each weighted rate over the probability simplex of `(w1,w2,w3)`. Because each weighted rate is linear in the weights, the optimum is at a simplex vertex, giving the closed-form worst-case bound `max_i (coefficient_i)` and best-case `min_i (coefficient_i)`. This is a few lines and turns three "not usable without oracle cardinalities" formulas into usable guaranteed bounds.
- **Severity**: major
- **Confidence**: high

### M2. The cross-set independence assumption is strong and its practical validity is never examined
- **Location**: Section 3, `asm:cross_set_indep`.
- **Quoted text**: "The Bernoulli sets $\tilde{A}_1$ and $\tilde{A}_2$ are constructed using independent randomness".
- **Problem**: Every set-operation result depends on cross-set independence. In practice approximate sets are frequently *not* independent: two Bloom filters built with the same hash family and seed share their randomness, so their per-element errors are perfectly correlated, not independent; deduplicated or derived filters share structure. The paper neither flags when independence fails nor states what breaks. This matters because the union FPR `1-(1-e1)(1-e2)` is correct only under independence; for identical filters the union FPR equals `e1` (not `1-(1-e1)^2`). A methodology paper offering practitioners closed-form composition must state the independence precondition prominently and warn about the common shared-seed failure mode.
- **Impact**: A practitioner could misapply the formulas to correlated filters and get systematically wrong (over-optimistic or over-pessimistic) error estimates.
- **Fix**: Add a short paragraph after `asm:cross_set_indep` giving the canonical violation (shared hash seed yields correlated errors), stating that the formulas require independent construction, and noting that correlated composition is out of scope.
- **Severity**: major
- **Confidence**: high

## Minor Issues

### m1. The single numerical example exercises only the unweighted union FPR computation in earnest; the weighted FNR is shown but no example covers intersection or difference
- **Location**: Section 3, `ex:numerical_union`.
- **Quoted text**: "Let $|U| = 1000$, $|A_1| = 100$, $|A_2| = 80$, and $|A_1 \cap A_2| = 30$. ... Thus $\tilde{A}_1 \cup \tilde{A}_2$ is a Bernoulli set ... with FPR $\approx 0.030$ and FNR $\approx 0.033$."
- **Problem**: The example is correct (I reproduced FPR 0.0298 and FNR 0.03307 exactly). But it covers only the union. The intersection FPR and the set-difference FPR are the more error-prone formulas (different weight definitions, mixed monotonicity) and would benefit most from a worked instance. A reader wanting to apply the intersection formula has no checked numeric template.
- **Fix**: Add a parallel worked example for the intersection (reusing the same cardinalities) and ideally the difference, so all three weighted formulas have a numeric anchor.
- **Severity**: minor
- **Confidence**: high

### m2. The biased-estimator claim in remedy (c) is asserted with "computable bias" but no bias expression is given
- **Location**: Section 3, `rem:unknown_partitions`, clause (c).
- **Quoted text**: "$|\tilde{A}_1 \cap \tilde{A}_2|$ is a biased estimator of $|A_1 \cap A_2|$ with computable bias from the error rates."
- **Problem**: The bias *is* computable (`E|Ã1 ∩ Ã2|` is a sum over the four objective regions of products of per-set inclusion probabilities), but the paper neither gives it nor cites where it is derived. Stating "computable" without the expression is a promissory note. Since the rest of the paper prides itself on closed forms, the omission stands out.
- **Fix**: Either give the one-line expectation `E|Ã1 ∩ Ã2| = |A1∩A2|τ1τ2 + |A1\A2|τ1e2 + |A2\A1|e1τ2 + |U\(A1∪A2)|e1e2` (a debiasing target) or explicitly defer it to the open-problems paragraph and drop "computable" from the in-line remark.
- **Severity**: minor
- **Confidence**: high

### m3. The figure illustrates only the simplest formula and reuses example parameters loosely
- **Location**: Section 3, `fig:union_fpr`.
- **Quoted text** (caption): "The thin dashed gray line shows the additive approximation $\fprate_1 + \fprate_2$ for $\fprate_1 = 0.01$".
- **Problem**: The plotted reference line is `x + 0.01` (i.e., `e1 + e2` with `e1=0.01`), which is the additive approximation for the lowest curve only. The caption says this clearly, but visually a reader may misread it as a reference for all four curves. The figure also only depicts the unweighted union FPR, reinforcing the imbalance noted in m1 (the hard formulas get no visualization).
- **Fix**: Either restrict the figure to comparing one curve against its additive approximation (and label accordingly) or add a second panel showing a weighted rate (e.g., intersection FPR vs overlap fraction).
- **Severity**: minor
- **Confidence**: medium

## Strengths

- **Derivations are fully reproducible.** Every error-rate formula can be
  rederived from the stated per-element probabilities and the law of total
  probability. I reproduced all of them analytically and by simulation with no
  discrepancies. For a theory paper this is the core reproducibility requirement
  and it is met.
- **The numerical example is exact and internally consistent.** FPR 0.0298 and
  FNR 0.03307 both reproduce. The interval example `[0.0298, 0.126]` also
  reproduces exactly.
- **Assumptions are mostly localized and named** (`asm:cross_set_indep`), even if
  their practical fragility is under-discussed.
- **The unknown-weights problem is acknowledged honestly** rather than swept
  aside; it is correctly surfaced both as a remark and as an open problem. The
  criticism above is that the acknowledgment is not converted into a usable
  bound, not that it is hidden.

## Reproducibility Checklist

- [x] Algorithm / derivation fully specified: **yes** (all formulas rederivable from text).
- [ ] Data described: **n/a** (no empirical data; theory paper).
- [ ] Hyperparameters listed: **n/a**.
- [ ] Code available: **no** (none needed; a reference C++ implementation
  `bernoulli_set_expressions.hpp` is named in project state but not referenced in
  the paper).
- [x] Statistical claims appropriate: **yes** (the asymptotic-normal claim is
  correctly inherited from the foundation paper and correctly specialized).
- [ ] Baselines adequate: **partial** (no comparison to the folklore Bloom-filter
  union/intersection behavior, which is the natural sanity baseline; see novelty
  and citation reports).
