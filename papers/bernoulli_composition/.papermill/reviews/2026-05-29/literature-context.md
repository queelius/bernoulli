# Literature Context Packet (merged scouts)

**Paper**: Composition of Bernoulli sets (Alexander Towell)
**Date**: 2026-05-29
**Scouts merged**: literature-scout-broad + literature-scout-targeted

> **Tooling caveat (important for calibration).** In this review pass the
> orchestrator did not have live web search available. The two scouts were
> grounded in (a) the paper's own bibliography, (b) the *foundation* paper's
> bibliography (`bernoulli_sets/references.bib`, which is rich: Bloom 1970,
> Broder/Mitzenmacher survey, Cuckoo/Xor/Ribbon filters, Carter/Wegman,
> Count-Min, Mitzenmacher/Upfal, Bose et al. on Bloom FPR), and (c) standard
> domain knowledge to the January 2026 cutoff. Findings about *specific*
> competing papers are reported at medium or low confidence and flagged for a
> live-search pass. Findings about textbook-level prior art (Bloom union and
> intersection, interval arithmetic, Kronecker channel products) are high
> confidence because they are standard.

---

## Field Overview

The paper draws on three mature areas.

1. **Approximate membership query (AMQ) data structures.** Bloom filters
   (Bloom 1970) and their descendants (counting, cuckoo, quotient, xor, ribbon
   filters) are the canonical probabilistic sets. The survey by Broder and
   Mitzenmacher (2004) is the standard entry point; Bose et al. (2008)
   corrected the classical false-positive-rate formula. A well-known folklore
   result is that the union of two Bloom filters (bitwise OR on the same bit
   array) yields a filter for the union of the two sets, and the intersection
   (bitwise AND) over-approximates the set intersection. The union FPR
   composition `1-(1-e1)(1-e2)` is the standard independent-error-channels
   formula and recurs throughout this literature whenever independent filters
   are OR-ed.

2. **Binary channels and information theory.** At the per-element level a
   Bernoulli set is a binary asymmetric channel (Shannon 1948); composing
   channels by multiplying transition matrices is textbook (Cover and Thomas
   2006, cited). Warner's randomized response (1965) is the same per-element
   object.

3. **Interval arithmetic.** Moore (1966, cited) founded the field; Hickey, Ju
   and Van Emden (2001, cited) give the modern algebraic treatment used here.
   The dependency problem the paper invokes is the central, well-documented
   pitfall of naive interval evaluation.

The distinctive move of the Bernoulli program, and of this paper specifically,
is to treat approximate set-level error rates as first-class, parameterized,
and closed under a Boolean algebra, deriving closed-form FPR and FNR for every
set operation (not just OR of same-array Bloom filters). This includes the
weighted (cardinality-dependent) false-negative rate of the union and the
false-positive rate of the intersection, both of which depend on the overlap
`|A1 ∩ A2|`. That cardinality-weighted treatment is the part least likely to
have a direct precedent in the AMQ literature, which usually assumes same-set
or same-array filters.

---

## Related / Comparable Work

### Bloom (1970), "Space/Time Trade-offs in Hash Coding with Allowable Errors"
- **Relevance**: Foundational AMQ structure; the canonical instance of a
  positive Bernoulli set (FNR = 0).
- **Relationship**: foundational / baseline.
- **Key point for review**: Bloom filters support union by bitwise OR with the
  union-FPR behavior the paper derives abstractly. The paper should cite Bloom
  even as a companion, because its motivating examples ("a practitioner building
  a system on Bloom filters") name Bloom filters explicitly.
- **Threat to novelty**: low. Bloom gives one data structure, not the
  parameterized set-algebra.
- **Confidence**: high (textbook).

### Broder and Mitzenmacher (2004), "Network Applications of Bloom Filters: A Survey"
- **Relevance**: Standard survey; discusses union and intersection of Bloom
  filters and the approximations involved.
- **Relationship**: competing / complementary background.
- **Key point**: The survey states the union-by-OR result and notes that
  intersection by AND is not exact (it introduces false positives), which is
  exactly the phenomenon the paper's intersection-FPR theorem quantifies.
- **Threat**: medium-low. It establishes that qualitatively the closure
  behavior is known folklore; the paper's contribution is the quantitative,
  parameterized, cardinality-weighted formulas plus the closure and monoid
  framing.
- **Confidence**: high that the survey discusses union and intersection; medium
  on exact statements without a live re-read.

### Bose et al. (2008), "On the False-Positive Rate of Bloom Filters"
- **Relevance**: Rigorous correction to the naive Bloom FPR; shows the field
  cares about exact error-rate derivations.
- **Relationship**: parallel rigor, different object.
- **Threat**: low (different problem: single-filter FPR exactness).
- **Confidence**: high.

### Cover and Thomas (2006), "Elements of Information Theory" (cited)
- **Relevance**: Channel-matrix product equals composition; Kronecker
  factorization of product channels.
- **Relationship**: foundational; cited precisely for the Kronecker-product
  parsimony claim.
- **Threat**: none (used correctly as a tool).
- **Confidence**: high.

### Moore (1966) / Hickey, Ju, Van Emden (2001) (both cited)
- **Relevance**: Interval arithmetic foundations and modern algebra.
- **Relationship**: foundational tool for Section 5.
- **Threat**: none.
- **Note**: The paper's claim that "the formulae are simple enough to ensure
  dependencies are satisfied" rests on monotonicity arguments that hold for the
  simple formulas but are only partly developed for the weighted ones. See the
  methodology and logic findings.
- **Confidence**: high.

### Probabilistic / approximate databases and sketches
- **Relevance**: PODS and VLDB audiences (candidate venues) know
  probabilistic-database query semantics and AMQ sketches (Count-Min,
  HyperLogLog). These also compose approximate set or multiset summaries.
- **Relationship**: adjacent application domain.
- **Threat**: low to the math, but important for positioning. If the paper
  targets PODS or VLDB it should connect its algebra to probabilistic-database
  query composition and to set-sketch mergeability (for example HyperLogLog
  union). Not doing so is a related-work gap, not a novelty defect.
- **Confidence**: medium (no live search this pass).

---

## State of the Art (relevant slices)

- **Union of independent AMQ filters**: FPR composes as `1-(1-e1)(1-e2)`. This is
  folklore (high confidence). The paper's Union-FPR theorem reproduces it and is
  correct.
- **Intersection of AMQ filters**: known to introduce false positives. The
  quantified, cardinality-weighted FPR
  `w1(1-w1)e2 + w2 e1(1-w2) + w3 e1 e2` (omega for FNR) is the paper's own; I
  found no standard closed form stated this way in the AMQ background. This is
  the strongest novelty locus (medium confidence pending live search).
- **Relational predicates (subset and equality probabilities) on approximate
  sets**: the element-factorized exact probabilities (a product over partition
  blocks) appear original to the Bernoulli program. No standard AMQ reference
  computes `P(Ã ⊆ B̃)` in closed form. Medium-high confidence this is new framing.
- **Interval-valued error rates for AMQ composition**: applying interval
  arithmetic to propagate uncertain FPR and FNR through set operations is a
  clean combination of two standard tools and is plausibly new. Medium
  confidence.

---

## Research Gaps (relevant to evaluating this paper)

1. **Cardinality-dependent error of composed approximate sets.** The AMQ
   literature largely treats union via same-array OR and rarely gives the
   FNR-of-union or FPR-of-intersection as functions of `|A1 ∩ A2|`. The paper
   fills this gap; the gap's existence supports the paper's novelty.
2. **A Boolean-algebra / monoid view of approximate sets with computable rate
   propagation.** Sketch mergeability is studied operation by operation; a
   unified closed algebra with closure theorems and a typing grammar
   (positive and negative classes) is uncommon. Supports novelty.
3. **Estimating partition weights from the approximate sets themselves.** The
   paper names this as an open problem; the literature on cardinality estimation
   from filters (for example Swamidass-Baldi count estimators, HyperLogLog
   intersection via inclusion-exclusion) is directly relevant and should be
   cited when that program is pursued.

---

## Direct Claim Comparisons (for the novelty-assessor)

| Paper claim | Closest prior result | Delta |
|---|---|---|
| Union FPR `1-(1-e1)(1-e2)` | Folklore for OR of independent filters (Broder/Mitzenmacher) | Paper states it as a theorem inside a parameterized algebra; delta is framing, not result. Should cite. |
| Union FNR (cardinality-weighted) | No standard closed form located | The paper's own; strong novelty (medium conf.). |
| Intersection FPR (cardinality-weighted) | AND-of-filters introduces FPs (qualitative, survey) | Paper gives the quantitative law; strong novelty locus. |
| Set difference rates via `A1 ∩ A2^c` | Derived from above plus complement | Standard composition once union, intersection, complement are in hand; modest. |
| Monoid / closure / typing grammar | Semigroup and monoid structure of set ops is classical; applying it to Bernoulli sets with rate propagation is new | Novelty is the rate-carrying closure, not the algebraic skeleton. |
| Subset and equality probabilities | Not located in AMQ literature | Plausibly original; novelty (medium-high conf.). |
| Interval propagation of uncertain rates | Moore / Hickey et al. (tools) | New application combination; modest-to-moderate novelty. |

---

## Confidence Notes

- **High confidence**: Bloom 1970, the Broder/Mitzenmacher survey, and the
  interval-arithmetic foundations are directly relevant, and the first two are
  missing from this paper's bibliography. The union-FPR formula is folklore.
  Channel and Kronecker tools are used correctly.
- **Medium confidence**: that the cardinality-weighted intersection FPR and the
  subset and equality probability formulas have no direct precedent. They look
  original within the Bernoulli program, but a live forward-citation search of
  the Broder/Mitzenmacher survey and recent filter papers (2018 to 2025) should
  run before asserting priority in a camera-ready.
- **Could not verify (no web this pass)**: whether any 2018 to 2025 paper (for
  example on mergeable sketches, filter algebra, or probabilistic-database set
  semantics) states the weighted intersection law or the subset probability. A
  targeted live-search pass on these terms is recommended.
