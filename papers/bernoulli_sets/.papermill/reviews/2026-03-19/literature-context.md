# Literature Context

**Date**: 2026-03-19
**Paper**: Bernoulli sets: a model for random approximate sets

## Field Survey

### State of the Art in Approximate Set Membership

The field of probabilistic data structures for approximate set membership is mature, with a rich taxonomy:

1. **Bloom filters** (Bloom 1970): The foundational one-sided-error structure. Well-analyzed FPR, space-optimal among hash-based approaches.
2. **Counting/spectral Bloom filters**: Extensions supporting deletion and multiplicity.
3. **Cuckoo filters** (Fan et al. 2014): Better locality, support deletion, competitive FPR.
4. **Quotient filters** (Bender et al. 2012): Cache-friendly alternative with similar guarantees.
5. **Xor filters** (Graf & Lemire 2020): Static, faster queries, near-optimal space.
6. **Ribbon filters** (Dillinger & Walzer 2021): Space-efficient, practical construction.
7. **Learned Bloom filters** (Kraska et al. 2018, Mitzenmacher 2018): ML-augmented filters trading model complexity for space.
8. **Count-min sketch** (Cormode & Muthukrishnan 2005): Frequency estimation with one-sided error.

The paper cites the major data structures adequately.

### Competing Theoretical Frameworks

1. **Information-theoretic lower bounds** (Carter et al. 1978): The $n \log_2(1/\varepsilon)$ lower bound for positive approximate sets. Cited indirectly through the companion paper.
2. **Binary symmetric/asymmetric channel theory** (Shannon 1948): The per-element error model is classical. The paper correctly acknowledges this (Remark 3.1).
3. **Randomized response** (Warner 1965): Social science parallel. Cited.
4. **No directly competing axiomatic framework** for approximate sets exists in the published literature. The closest analogue is the work on abstract data types for probabilistic data structures, but none formalize the two-axiom Bernoulli model with composition.

### Gap Assessment

The claimed gap -- "a foundational probabilistic model for approximate sets" -- is **largely valid**. While individual structures have well-understood error analyses, there is no published unified axiomatic framework that:
- Derives error-count distributions from first principles
- Provides a composition theorem for higher-order approximate sets
- Formulates an ADT that any implementation can model

The per-element binary channel model is classical, and the paper appropriately frames its novelty as the set-level model rather than the per-element channel.

### Potentially Missing References

1. **Learned Bloom filters** (Kraska et al. 2018; Mitzenmacher 2018): These violate element-wise independence, making them a natural counterpoint for the independence assumption discussion.
2. **Pagh, Pagh, and Rao (2005)**: Optimal Bloom filter replacements with near-optimal space.
3. **Carter, Floyd, Gill, Markowsky, and Wegman (1978)**: The information-theoretic lower bound (referenced in companion paper but not here; relevant to the ADT formulation).
4. **Swamidass & Baldi (2007)**: Mathematical correction to Bloom filter FPR analysis under hash correlation.

These are suggestions, not requirements. The paper's citation coverage is appropriate for its scope.
