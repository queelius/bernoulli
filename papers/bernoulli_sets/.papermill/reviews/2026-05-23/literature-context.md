# Literature Context Packet

## Field Survey (broad)

The probabilistic data structures literature has well-analyzed individual structures (Bloom 1970, Bender et al. 2012 quotient, Fan et al. 2014 cuckoo, Graf and Lemire 2020 xor, Dillinger and Walzer 2021 ribbon) and surveys (Broder and Mitzenmacher 2004; Tarkoma, Rothenberg, Lagerspetz 2012). What has not been published is a unified probabilistic axiomatization independent of the underlying structure, with explicit higher-order composition rules expressed as products of binary channel transition matrices and an ADT-level inheritance theorem.

The closest adjacent work:
- Mitzenmacher and Upfal (2005) on probabilistic methods for randomized algorithms supplies the analytical toolkit but does not abstract over the underlying structure.
- Shannon (1948) and Cover and Thomas (2006) give the per-element binary channel formalism that the paper explicitly cites as the classical antecedent.
- Warner (1965) provides the randomized response interpretation. The paper correctly notes this duality.

No prior work, to the best of our literature search, claims an axiomatic framework where: (i) two axioms entail the full distributional theory, (ii) higher-order composition reduces to channel matrix products, and (iii) any implementation conforming to the axioms inherits the theory automatically.

## Targeted Comparisons

Searches for "approximate set abstract data type", "Bernoulli set model", "axiomatic Bloom filter", and "compositional false positive rate" surface no direct competitors that combine the same three contributions. The Bose et al. (2008) bound and the Carter and Wegman (1979) universal hash families are construction-specific. The compositional encrypted-search work (Goh 2003, Curtmola et al. 2006) treats security parameters rather than error parameters compositionally.

The cipher-maps and maximizing-confidentiality papers in the trapdoor-computing program cite the Bernoulli framework as a single body of work (`bernoulli-types` in cipher-maps), referring to "Bernoulli Sets and Maps" as one citable artifact. Cipher-maps section 6 ("Relationship to the Bernoulli Model") leans on three facts that the present paper supplies (axioms, error accumulation under composition, Bernoulli Boolean as the atomic case) and on facts that live in companion papers (BHF construction, type hierarchy, optimal cipher map). The present paper supplies the foundational layer cleanly; the type hierarchy and BHF discussion are properly out of scope.

## Notation Conventions Across the Program

Both cipher-maps and the present paper use the same Greek letters for the rates:
- `\fprate = epsilon` (FPR)
- `\fnrate = omega` (FNR)
- `\tprate = tau` (TPR)
- `\tnrate = eta` (TNR)

This consistency is good. The wider trapdoor-computing program uses `\eta` for the cipher-map correctness parameter, which equals `1 - tprate` (i.e., the FNR for a positive Bernoulli set or a fixed-error parameter for a map). The two conventions do not clash because cipher-maps uses `\eta` outside Bernoulli notation contexts.

## Self-containment Reading

The 18-page paper deliberately scopes itself to:
- Two axioms,
- Binomial error counts and their normal limits,
- Higher-order composition via channel matrix products,
- ADT formulation with a single Boolean-universe example.

It defers (with citations) to companion papers:
- bernoulliComposition: set operations, monoidal structure, relational predicates, interval arithmetic.
- bernoulliMeasures: classification measures (PPV, NPV, accuracy, Youden's J).
- bernoulliEntropy: joint entropy and information-theoretic space complexity (-log2 fprate, ln 2 ~= 0.69 Bloom filter benchmark).
- bernoulliMaps: approximate functions and the algebraic Boolean construction.

This deferral is honest. The paper does not depend on results from any companion paper to establish its own claims. The forward citations are flagged as `@Unpublished` and `@Unpublished{phf, ... Working paper}`, which is correct labeling but a known weakness at submission time.

## Key Takeaways

1. The contribution is a legitimate gap-filler in the probabilistic data structures literature.
2. The novelty is properly scoped: the per-element channel model is classical, the set-level axiomatization and composition theorem are novel in combination.
3. The paper is self-contained for its stated scope; it does not import lemmas from unpublished companion work.
4. The notation matches the conventions used by the trapdoor-computing program; downstream papers (cipher-maps, maximizing-confidentiality) cite into it cleanly.
5. The user's expectation that this paper contains the `-log2(fprate)` lower bound and the Bloom filter `ln 2` efficiency is no longer accurate: those results were extracted to bernoulliEntropy.
