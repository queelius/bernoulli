# Literature Context Packet

**Paper**: *The abstract data type of the approximate relation* (Alexander Towell)
**Compiled**: 2026-06-09
**Note on method**: The orchestrating reviewer runs single-context with **no live web search** and **no recursive subagents** in this environment (confirmed: the Task tool is unavailable inside this context). The two literature scouts could not be dispatched. The context below is assembled from the reviewer's training knowledge and from the manuscript's own positioning. **Every external-prior-art claim is tagged `[VERIFY]`** and must be checked personally by the area chair, who has web access.

---

## 1. The target neighborhood

The paper draws on three literatures at once:

1. **Approximate membership query (AMQ) structures**: Bloom filters (cited, Bloom 1970), counting/cuckoo/quotient filters, perfect hash filters (the author's own `phf`). The set-level error model (FPR, no false negatives in a plain Bloom filter; FPR *and* FNR in the more general Bernoulli/PHF model) is mature and well understood **in isolation, for a single membership test**.

2. **Relational query processing with filters**: Bloom filters as a join accelerator. This is the literature most likely to be raised by an ICDT/PODS/Information-Systems referee as the competing baseline.

3. **Probabilistic / uncertain databases**: the paper's explicitly chosen contrast class (Suciu et al. 2011; Trio/Widom 2005; MayBMS/Huang et al. 2009).

---

## 2. Competing / adjacent approaches (the novelty risk)

### 2a. Bloom joins / Bloomjoin and semijoin filtering `[VERIFY]`
- **Bloomjoin** (distributed query processing): a Bloom filter of one relation's join-key column is shipped to the other site to pre-filter tuples before the actual join. Attributed in training memory to **Mackert & Lohman** (R* distributed query optimizer work, mid-1980s) and the broader semijoin-reduction literature. `[VERIFY]` the exact attribution and whether any of that work analyzes the *false-positive rate of the join output* rather than just the *communication-cost reduction*.
- Bloom filters are pervasive in modern join implementations (for example, "runtime filters" / "min-max + Bloom" sideways-information-passing in Spark, Impala, Snowflake). `[VERIFY]` whether any published analysis there characterizes the **output false-positive rate as a function of operand FPRs**, and crucially whether any of it observes the **dependence among join outputs sharing a probe**.
- **Assessment of the risk the area chair flagged.** The framing "approximate relation = AMQ over the tuple universe, propagate the per-tuple FPR through the operators" is, on its own, **plausibly incremental** relative to the Bloomjoin literature: the projection OR-amplification `1-(1-ε)^k` is the standard "union of independent FP trials" identity, just renamed for a relational projection (see 2b). The genuinely differentiating result is **`thm:join_dependence` (the independence-failure / shared-component correlation)**. The reviewer's honest read: *if* there is prior work that already notes the dependence among Bloom-join outputs that share a probe (folklore is possible), the paper's headline shrinks to "a clean, validated statement of a known caveat." If there is **not**, which the reviewer weakly believes is the case because Bloomjoin analyses are overwhelmingly about communication/selectivity and not the joint output law, then the result is a real, citable contribution. **This is the single most important `[VERIFY]` for the venue decision.**

### 2b. Projection / OR-of-filters FPR amplification `[VERIFY]`
- `1-(1-ε)^k` is the false-positive rate of a logical **OR over `k` independent AMQ trials**; it is identical in form to the FPR of a **union of `k` Bloom filters** (or `k` insertions causing an OR over bit-tests). This identity is standard. The paper's contribution here is **not the formula** but its **framing as a relational projection operator** (the fiber/fan-in reading) and the observation that the resulting structure is a *higher-model-order* Bernoulli relation while *preserving independence*. `[VERIFY]` whether duplicate-elimination / projection over approximate relations has been analyzed this way before. Reviewer's read: the formula is known; the relational-operator packaging is likely novel-by-framing, which is a weaker form of novelty.

### 2c. Sketch-based / approximate query processing (AQP) `[VERIFY]`
- AGMS / fast-AGMS sketches, Count-Min, and the join-size-estimation literature (Alon-Gibbons-Matias-Szegedy and successors) estimate **join sizes / aggregates** with error bounds; they do **not** model per-tuple membership of an exact base relation through a lossy representation. `[VERIFY]` the boundary, but the reviewer is fairly confident AQP solves a *different* problem (cardinality/aggregate estimation, not membership fidelity of the materialized relation) and therefore **does not subsume** the paper. It should nonetheless be *cited and distinguished*; its absence is a gap a DB-theory referee will notice.

### 2d. Independence-failure in approximate-set composition `[VERIFY]`
- The general phenomenon, that derived events reusing a shared underlying random trial are correlated, is elementary probability and appears throughout the streaming/sketch literature (for example, correlated estimators, the need for independent hash families). The paper's value is in **localizing it to the relational join** and quantifying the exact `1/a` factor and its query-planning consequence. `[VERIFY]` whether any approximate-relational or Bloom-join paper has already stated *this specific* localization.

---

## 3. State of the art: probabilistic / uncertain databases

- **Suciu, Olteanu, Ré, Koch (2011), *Probabilistic Databases*** (Morgan & Claypool) is the canonical monograph. Trio (Widom, CIDR 2005) and MayBMS (Huang et al., SIGMOD 2009) are canonical systems. All three model **uncertainty in the data**: tuples carry probabilities/lineage, a database denotes a distribution over possible worlds, and query answers are marginal probabilities over those worlds. `[VERIFY]` the bibliographic details (they are well-formed in the .bib); these citations are standard and almost certainly correct.
- **Is the paper's distinction real?** The reviewer judges **yes, in object**: possible-worlds semantics asks "given uncertain data, what is the probability of an answer?"; this paper asks "given an *exact* relation stored lossily, with what fidelity do operators and invariants survive?" These are different questions. **However**, the boundary is not airtight on one axis: a **tuple-independent probabilistic database** with per-tuple probability `p` is formally close to a Bernoulli relation with `τ = p` on members. A sharp referee could argue that the *marginal* operator analysis (join FNR, projection FPR) is recoverable as a special case of tuple-independent-PDB query evaluation. `[VERIFY]` whether the tuple-independent-PDB literature already derives the marginal answer probabilities for join/project (it very likely does, as "extensional query evaluation on independent tuples"). **If so, the marginal-rate results are NOT differentiating against PDBs**, and the paper must lean its novelty entirely on (a) the **invariant-preservation** results and (b) the **joint/correlation** result `thm:join_dependence`, neither of which the PDB marginal-probability machinery addresses. This is the crux of the positioning and is developed as a finding in the unified review.

---

## 4. Invariant preservation under approximate representation `[VERIFY]`

- The reviewer is **not aware** of prior work asking whether **reflexivity / symmetry / transitivity / single-valuedness (a functional dependency) survive** when a relation is stored in a lossy AMQ structure, with closed-form preservation probabilities. The functional-dependency-under-uncertainty and constraint-repair literatures exist, but they concern *dirty data* / *inconsistent databases* (uncertainty in the data again), not *representation-induced* violation of an invariant that holds exactly in the base relation. `[VERIFY]` against the AMQ literature and the constraint-under-uncertainty literature. Reviewer's read: **this is the paper's most clearly novel angle** and the least at risk of being subsumed.

## 5. Encrypted-search / searchable-encryption framing `[VERIFY]`
- "Bloom-filter-backed encrypted index with FPR as a confidentiality knob" is **well-trodden**: Goh's Z-IDX (secure indexes, 2003) is the canonical Bloom-filter-based searchable-symmetric-encryption construction; the SSE literature is large. The application section is honestly scoped ("not new machinery") and defers the full construction to `phf`, so this is **novelty-by-framing only**, which is appropriate. `[VERIFY]` that the leakage-model framing does not overstate; the section is brief and defers, so the risk is low.

---

## 6. Venue norms (ICDT / PODS / Information Systems)

- **ICDT / PODS** are *theory* venues. Their typical currency is **data-model semantics, complexity results (dichotomy theorems, lower bounds), expressiveness, and query-evaluation hardness**. A paper whose contributions are **closed-form error-rate propagation formulas + invariant-preservation probabilities, validated by Monte Carlo**, is *atypical* for ICDT/PODS: it has no complexity/lower-bound result, no new logic or data-model semantics, and its proofs are short probability-algebra arguments rather than the combinatorial/logical machinery these venues reward. `[VERIFY]` recent ICDT/PODS programs for precedent, but the reviewer's honest read is that **ICDT/PODS is a stretch** for the current scope.
- **Better-fit venues**: an **Information Systems / DB systems** journal or a **systems/IR** venue (where AMQ-in-joins and encrypted search are native), or, consistent with the family's stated strategy (the monograph is primary; focused papers are Zenodo preprints), a **Zenodo preprint**. If a database-theory venue is genuinely the target, the paper would need a sharper theoretical hook: for example, a **lower bound** (information-theoretic minimum bits to preserve an invariant at a given rate, partly deferred to `bernoulliEntropy`), or a **dichotomy** for which invariants admit a cheap closure vs. not (symmetry does, transitivity does not; this is gestured at but not formalized as a theorem).

---

## 7. Consolidated `[VERIFY]` list for the area chair

1. **`[VERIFY]` (highest priority)** Bloomjoin / runtime-filter literature (Mackert & Lohman; Spark/Impala/Snowflake runtime filters; semijoin reduction): does any published work characterize the **false-positive rate of the join output** and, in particular, the **dependence among join outputs that share a probe**? This decides whether `thm:join_dependence` is novel or folklore.
2. **`[VERIFY]`** Tuple-independent probabilistic databases (extensional/safe query evaluation): is the **marginal** join-FNR / projection-FPR analysis already a special case of independent-tuple PDB query evaluation? If yes, the marginal-rate results do not differentiate from PDBs.
3. **`[VERIFY]`** Any prior work on **invariant preservation (reflexive/symmetric/transitive/functional)** under lossy/approximate (AMQ) storage of an exact relation. Reviewer believes this is unaddressed; confirm.
4. **`[VERIFY]`** Sketch-based AQP (AGMS, Count-Min for joins): confirm it targets cardinality/aggregate estimation, not membership fidelity, hence does not subsume, but should be cited and distinguished.
5. **`[VERIFY]`** Projection/duplicate-elimination FPR amplification `1-(1-ε)^k`: is the OR-of-filters identity already framed as a relational projection operator anywhere?
6. **`[VERIFY]`** Searchable-encryption framing: Goh Z-IDX and Bloom-filter SSE as the right prior art for the application (low risk; section is honestly deferred).
7. **`[VERIFY]`** Bibliographic correctness of `suciu2011`, `widom2005trio`, `huang2009maybms`, `codd1970`, `bf` (all appear well-formed and standard).
