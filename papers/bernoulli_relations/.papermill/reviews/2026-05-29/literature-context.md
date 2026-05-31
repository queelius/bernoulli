# Literature Context Packet, bernoulli_relations

**Compiled**: 2026-05-29
**Method**: Merged from a broad field survey and a targeted direct-comparison pass, deduplicated. (Scout passes performed by the area chair; external bibliographic lookups limited to the model's training knowledge, since this environment has no live web access. Findings below are orientation only, and any citation the author adds must be verified against primary sources.)

## Paper under review

"The abstract data type of the approximate relation" (Alexander Towell). Declared role: **extension** paper in the 9-paper Bernoulli / random-approximate-set family. Owns the relational-algebra domain: approximate relations as an ADT, error propagation through join / project / select / composition, relational predicates (subset, equality) over multi-attribute Bernoulli relations, and an oblivious-database application.

## A. Field survey (broad): competing and adjacent approaches

### A1. Probabilistic and uncertain databases
The dominant body of prior work the relational-algebra framing must be differentiated from.
- **Probabilistic databases** (Suciu, Olteanu, Re, Koch, *Probabilistic Databases*, Morgan & Claypool, 2011): tuples carry existence/attribute probabilities; query semantics is *possible worlds*; relational operators propagate a probability distribution over result tuples. This is the single most important comparison point: a referee from the DB community will ask "how is an approximate relation not just a tuple-independent probabilistic database?"
- **MystiQ / MayBMS / Trio (ULDBs)**: systems implementing possible-worlds semantics; Trio's "uncertainty + lineage" is closest in spirit to error-rate bookkeeping.
- **Key distinction to surface**: in probabilistic DBs the *uncertainty is about which tuples are really in the relation* (data uncertainty). In the Bernoulli model the *base relation is known/objective* and uncertainty is injected by a space-saving approximate representation (a membership oracle with FPR/FNR). The errors are a property of the *data structure*, not the *data*. This is a real and defensible distinction, but the manuscript does not currently state it.

### A2. Approximate membership / set-membership data structures
- **Bloom filters** (Bloom 1970); surveys by Broder & Mitzenmacher (2004); Tarkoma et al. (2012).
- **Cuckoo filter** (Fan, Andersen, Kaminsky, Mitzenmacher, CoNEXT 2014); **Quotient filter**; **Xor filter** (Graf & Lemire 2020); **Ribbon filter** (Dillinger & Walzer 2021).
- These are the concrete realizations of an "approximate set" with a false-positive rate; the relational paper treats relations as approximate sets of tuples, so these underlie every operator.

### A3. Approximate query processing / sketches
- **Count-Min sketch** (Cormode & Muthukrishnan 2005), **HyperLogLog** (Flajolet et al. 2007), **AMS sketches**: estimate aggregate query answers (counts, distinct counts, join sizes) with error bounds.
- Adjacent but different: sketches estimate *aggregates over* relations; this paper estimates *membership of tuples in* a relation and propagates per-tuple error through algebraic operators. Worth a one-line contrast.

### A4. Join-size and set-similarity estimation
- Classic selectivity estimation, MinHash / LSH for set similarity. Relevant to the join section because the *number of result tuples* of an approximate join is itself a random variable; the manuscript currently does not connect to this literature.

### A5. Oblivious / encrypted data structures (for the application section)
- **Searchable symmetric encryption** (Song, Wagner, Perrig 2000; Curtmola et al. 2006); **Oblivious RAM** (Goldreich, Ostrovsky 1996); **encrypted/oblivious databases** (CryptDB, Popa et al. 2011).
- The "oblivious relational model / oblivious database" application overlaps the author's own trapdoor-computing line (cipher maps) and the encrypted-search thesis. The novelty-relevant point is that obliviousness here rides on the approximate-set representation rather than on cryptographic primitives directly.

## B. Targeted survey: direct comparisons and overlapping claims

### B1. Within-family (the critical context per the review brief)
The foundation and siblings legitimately supply the shared model; do NOT score shared foundations as missing novelty.
- **bernoulli_sets** (foundation): axioms (element-wise independence; conditional independence of block rates), binomial FP/FN counts, CLT, confidence intervals, higher-order composition, ADT formulation, Boolean universe. Cite key `aset`. Theorems `thm:fpbinom` and `thm:fpr` in the manuscript are **restatements of foundation results applied to the product universe**, correctly so for an extension paper, but they should be cited as such rather than re-proved as if novel.
- **bernoulli_composition**: set-operation error propagation (union, intersection, complement, difference), monoid structure, relational predicates (subset, equality), interval arithmetic. **This is the most important sibling for novelty differentiation on the predicates section.** The subset-rate and equality-rate formulas in `predicates.tex` substantially overlap content owned by `bernoulli_composition` per the family's Cross-Paper Topic Placement table (which assigns "relational predicates, interval arithmetic" to composition). The relations paper must either cite composition for these or carve a clearly distinct multi-attribute angle.
- **bernoulli_maps** (sibling, "companion"): Bernoulli map `\APFun{f}: X -> Maybe Y`, model order, composition theorem `fnrate_{g of f} = 1-(1-fnrate_1)(1-fnrate_2)`, entropy map, singular hash map achieving `-log2(fprate)+mu`. **The map-composition theorem in this paper's `properties.tex` (Section "Random approximate maps") duplicates the maps paper's central result.** Per the topic table, function spaces / approximate maps / map composition belong to `bernoulli_maps`. The relations paper's legitimate niche is the *multi-attribute relational* operators (join, project, select) and the *relation-as-set-of-tuples* viewpoint; partial-function composition should be cited to `bernoulli_maps`, not re-derived.
- **bernoulli-hash-function / bernoulli-phf**: optimal constructions and the perfect-hash-filter implementation; the abstract's promised "perfect hash map" projection mechanism and the bits-per-relation lower bound are owned there. The abstract over-claims by promising these here.

### B2. Differentiating the genuine contribution
The defensible, non-overlapping core of this paper is:
1. The **approximate relation as an ADT** over an n-fold Cartesian-product universe (relation = approximate set of tuples), with the false-correspondence / false-complementary-correspondence vocabulary.
2. **Error propagation specifically through relational-algebra operators**: join, projection, and relational composition, where the *operator structure* (which tuples co-occur, how projection merges rows) changes the error regime. This is the part with no direct sibling and only loose ties to probabilistic-DB query semantics.
3. **Invariant-preserving approximate relations** (symmetric, reflexive, transitive, functional): when a base relation must satisfy an algebraic invariant, can a random approximation preserve it, and at what rate? This "constrained approximate relation" question is genuinely novel relative to both the family and the probabilistic-DB literature.
4. The **oblivious relational / database application** as a bridge to encrypted search.

### B3. Closest external prior art to cite (currently absent: there is no bibliography at all)
- Codd, "A relational model of data for large shared data banks" (CACM 1970), for the relational-model section, which currently has an empty `\cite{}`.
- Suciu et al., *Probabilistic Databases* (2011), mandatory differentiation.
- Bloom (1970); Broder & Mitzenmacher (2004), for the approximate-set substrate (`bf`).
- Fan et al., Cuckoo filter (2014) and one modern AMQ (xor/ribbon), to show the substrate is current.
- Cormode & Muthukrishnan, Count-Min (2005), to delimit aggregate-AQP from membership-propagation.
- Curtmola et al. (2006) and/or Popa et al. CryptDB (2011), for the oblivious-database application.

## C. Takeaways that drive the specialist reviews

1. **Novelty exists but is currently undifferentiated.** The paper's defensible core (relational-operator error propagation; invariant-preserving approximations; oblivious relations) is real, but in its present state the map-composition and predicate sections read as duplicates of `bernoulli_maps` and `bernoulli_composition`. Differentiation is a *framing/citation* fix, not a fundamental novelty deficit, provided the overlapping material is attributed and the join/project/invariant material is developed.
2. **The probabilistic-database comparison is unavoidable** for any database/theory venue and is entirely missing.
3. **Every external anchor is uncited** because there is no `references.bib`. This compounds the build-blocker into a substantive scholarship gap.
