# Novelty Assessment Report

## Summary

Assessed as a companion paper whose declared role is the set-theoretic
compositional algebra of Bernoulli sets, the contribution is real but uneven. The
cardinality-weighted false-negative rate of the union, the false-positive rate of
the intersection, the closed-form subset and equality probabilities, and the
interval-propagation extension are the genuine advances and have no direct
precedent I could locate. The union FPR, the complement swap, and the monoid and
closure framing are largely re-presentations of folklore (independent-error OR,
De Morgan, semigroup structure of set operations) and should be claimed more
modestly. Per the family-context instructions, I do not treat the shared
foundation (axioms, distributions, asymptotic limits from `bernoulliSets`) as a
novelty deficit; those are legitimately inherited.

## Contribution Analysis

### Contribution 1: Closed-form error rates for complement, union, intersection, and set difference, plus the induced monoidal structure
- **Paper's claim**: "closed-form error rates for complement, union, intersection, and set difference, together with the monoidal structure they induce" (Introduction, contribution list item 1).
- **Closest prior work**: For the *union FPR* `1-(1-e1)(1-e2)` and the qualitative fact that intersection-by-AND introduces false positives: folklore in the AMQ literature, documented in Broder and Mitzenmacher (2004) and implicit wherever independent Bloom filters are OR-ed. For monoid and semigroup structure of set operations: classical algebra. For the *cardinality-weighted* union FNR and intersection FPR: no direct precedent located.
- **Relationship**: mixed. Union FPR and complement: parallel to known results (the result is standard; only the parameterized framing is the paper's). Cardinality-weighted union FNR and intersection FPR: genuinely new within the located literature. Monoid framing: known skeleton applied to a new (rate-carrying) object.
- **Assessment**: The novel core is the *cardinality dependence*. The AMQ literature almost always studies same-set or same-array filters, where the overlap structure does not enter. By parameterizing two distinct objective sets with arbitrary overlap and deriving the FNR-of-union and FPR-of-intersection as functions of `|A1 ∩ A2|`, the paper computes something the standard Bloom-filter treatments do not. That is worth stating prominently and is currently buried under the (less novel) union FPR. The monoid and closure results are correct and tidy but their novelty is the rate propagation, not the algebra.
- **Severity**: minor (framing: the union FPR and monoid parts are overclaimed relative to folklore; the genuinely new weighted formulas are under-emphasized).
- **Confidence**: high on the folklore status of union FPR; medium on the absence of precedent for the weighted formulas (no live search this pass).

### Contribution 2: Exact formulas for relational predicates (subset and equality probabilities) on Bernoulli sets
- **Paper's claim**: "exact formulas for the relational predicates (subset and equality probabilities) on Bernoulli sets" (Introduction, item 2).
- **Closest prior work**: None located. The AMQ and probabilistic-database literatures study membership and cardinality queries on approximate sets, but I am not aware of a standard closed form for `P(Ã ⊆ B̃)` or `P(Ã = B̃)` as element-factorized products over partition blocks.
- **Relationship**: genuinely new (within located literature).
- **Assessment**: This is the cleanest novelty in the paper. The element-wise factorization into block products is natural given Axiom 1 but the resulting predicate probabilities, and the infinite-universe corollaries (probability of exact equality or subset tends to 0), are a contribution a theoretician in this area would find new and quotable. This should arguably be promoted in the abstract and introduction as a headline, co-equal with the set operations.
- **Severity**: none (genuinely novel).
- **Confidence**: medium-high (pending a forward-citation search on "subset probability approximate sets" and probabilistic-database set-containment semantics).

### Contribution 3: Interval-arithmetic extension propagating uncertain rates through set operations
- **Paper's claim**: "an interval arithmetic extension that propagates uncertain rates through set operations, yielding guaranteed bounds on output error rates" (Introduction, item 3).
- **Closest prior work**: Interval arithmetic itself (Moore 1966; Hickey, Ju, Van Emden 2001, both cited). No located precedent applies interval arithmetic specifically to AMQ error-rate composition.
- **Relationship**: new application combination of standard tools.
- **Assessment**: Moderate novelty. The idea (replace point rates with intervals, evaluate at monotonicity-appropriate endpoints) is a direct application of textbook interval arithmetic; the contribution is recognizing that the composition formulas are simple enough for endpoint evaluation to be tight (no dependency-problem blowup for the unweighted ones). This is useful and reasonable to claim, but it should be framed as "applying interval arithmetic to the composition formulas," not as a new method. As currently written (Section 5) it is appropriately modest, though the weighted-case treatment is incomplete (see logic M2).
- **Severity**: minor (the section is honest, but the contribution-list phrasing "an interval arithmetic extension" slightly oversells what is a clean application).
- **Confidence**: high.

## Missing Comparisons

These are positioning gaps, not novelty defects. None of them is prior art that
defeats a contribution; each is context a reviewer at a top venue will expect.

1. **Bloom-filter union and intersection folklore (Broder and Mitzenmacher 2004;
   Bloom 1970).** The paper's own motivation invokes Bloom filters, yet never
   states the known same-array OR union behavior that its union FPR generalizes.
   A reader cannot see what is new (the cardinality-weighted FNR and intersection
   FPR for *distinct* sets) without the folklore baseline stated for contrast.
   This is the single most important missing comparison.
2. **Mergeable sketches and set-sketch composition (HyperLogLog union,
   Count-Min).** For PODS or VLDB framing, the literature on composing
   approximate set or multiset summaries is the natural neighbor; the paper's
   monoidal-fold observation (`n`-ary union as a fold) directly echoes
   sketch mergeability.
3. **Cardinality estimation from filters.** The open problem (estimating
   `|A1 ∩ A2|` from the approximate sets) has a literature (inclusion-exclusion
   on HLL, Swamidass-Baldi count estimators) that should be cited when that
   thread is named, both to credit prior work and to show the open problem is
   tractable.

## Strengths

- **The cardinality-weighted intersection FPR and union FNR are a real
  contribution.** They compute error behavior that the standard same-set filter
  analyses do not, by handling arbitrary overlap between two distinct objective
  sets. This is the paper's strongest and most defensible novelty.
- **The subset and equality probability formulas appear genuinely new** and are
  clean, with attractive infinite-universe corollaries. Under-advertised.
- **The closure-and-typing-grammar result** (which set expressions are
  guaranteed to yield a positive vs negative Bernoulli set) is a tidy structural
  contribution. The algebraic skeleton is classical, but the rate-aware typing of
  approximate-set expressions is a fresh and useful framing.
- **Scope discipline is good.** The paper stays within its declared lane
  (composition) and correctly defers axioms, classification measures, and entropy
  to the sibling papers, consistent with its companion role. No inappropriate
  duplication of the foundation paper was found.

## Net Novelty Risk

- **Safe** (genuinely new within located literature): cardinality-weighted union
  FNR and intersection FPR; subset and equality probabilities and their
  infinite-universe limits; the rate-carrying closure and typing grammar.
- **Needs more modest framing** (folklore or classical skeleton): union FPR,
  complement swap, monoid and semigroup structure, "interval arithmetic
  extension" as a method.
- **At risk only of a positioning complaint, not a priority loss**: absent a
  Bloom-filter folklore comparison, a top-venue reviewer may ask "isn't the union
  just OR of filters?" The answer is yes for FPR and no for the weighted FNR, but
  the paper must make that distinction itself.
