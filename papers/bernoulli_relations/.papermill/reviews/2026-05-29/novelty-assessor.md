# Novelty Assessor Report, bernoulli_relations

**Agent**: novelty-assessor (contribution clarity, differentiation, significance)
**Date**: 2026-05-29
**Verdict**: There is a genuine and worthwhile contribution here, but it is currently buried under (a) re-derivations of sibling-paper results and (b) an abstract that promises four papers' worth of material. Assessed relative to the paper's *declared role* as the relational-algebra extension of the Bernoulli family.

## How I am scoring novelty
Per the review brief, this is an **extension** paper. Shared foundations (the Bernoulli axioms, FPR/FNR, binomial error counts, CLT) are NOT counted against novelty; they are the inherited substrate. I assess only: does the paper add something the foundation and siblings do not already own, and is that addition clearly delineated?

## The genuine, defensible contributions (novelty PRESENT)

### N+1. Approximate relation as an ADT over a Cartesian-product universe
Framing a relation as an approximate set of tuples over `X_1 x ... x X_n`, with the vocabulary of *correspondence / complementary correspondence* and *false (complementary) correspondence*, is a clean and non-trivial specialization. No sibling owns "relation as approximate set of tuples." This is real, if modest, novelty. **Clearly the paper's to claim.**

### N+2. Error propagation through *relational-algebra* operators (join, project, select, relational composition)
This is the strongest novelty and the paper's reason to exist. The foundation and `bernoulli_composition` cover set operations (union/intersection/complement/difference); none covers **join and projection**, where the operator's *combinatorial structure* (which tuples co-occur, how projection collapses rows) reshapes the error regime. The example in relations.tex (join then project of two concrete tables) is a good scaffold. **This material is unique to this paper and should be its center of gravity.** Right now it is underdeveloped: the join/project sections define the *exact* operators thoroughly but contain almost no *approximate* propagation results (the propagation theorems that exist are about maps and predicates, not joins).

### N+3. Invariant-preserving (constrained) approximate relations
The properties.tex question (can a random approximation preserve reflexivity / symmetry / transitivity / functionality, and at what rate?) and the constrained_ras.tex treatment (Cartesian products, power sets, disjoint unions must preserve structural invariants) are **novel relative to both the family and the probabilistic-database literature**. Probabilistic DBs do not typically ask "does my approximation remain an equivalence relation." This is a distinctive angle with no competitor. Currently it is the least finished part (placeholder proofs, the `\sections` typo, orphaned from the build), which is a shame because it is the most original.

### N+4. Oblivious relational model / database as a bridge to encrypted search
A legitimate application angle connecting the model to the author's encrypted-search and trapdoor-computing lines. Novel as an *integration*, though it leans on external machinery and is presently a TODO-laden sketch.

## Where novelty is OVER-CLAIMED or DUPLICATED (the problems)

### N-1 (MAJOR). Two whole sections re-derive results owned by sibling papers
- **Map composition** (properties.tex, "Random approximate maps" subsection): the composition theorem with TPR `\tprate_1\tprate_2` and an FPR interval is the **central result of `bernoulli_maps`** (the sibling's abstract states exactly `fnrate_{g∘f}=1-(1-fnrate_1)(1-fnrate_2)`). Per the family's Cross-Paper Topic Placement table, "function spaces, approximate maps, map composition" belongs to `bernoulli_maps`. Re-deriving it here (with an unfinished proof, per logic-checker ML-2) both duplicates the sibling and dilutes this paper's identity. **Fix**: state that a partial function is a single-valued relation, cite `bernoulli_maps` for the composition result, and keep only what is *relational* (e.g., composition as join+project, which IS this paper's territory).
- **Subset / equality predicate rates** (predicates.tex): the subset-rate derivation and equality-rate formula overlap "relational predicates, interval arithmetic," which the topic table assigns to `bernoulli_composition`. (And per methodology cross-check MA-X, the equality formula as written is actually incorrect.) **Fix**: cite `bernoulli_composition`; do not re-host these unless the multi-attribute generalization is genuinely new, in which case state precisely what is new.

This is a **framing/attribution** problem, not a fundamental lack of novelty (this is the prose-auditor's point too, see cross-routing). The paper has novel material; it is just spending its pages on borrowed material.

### N-2 (MAJOR). No differentiation from probabilistic databases
The single nearest body of external work (probabilistic/uncertain databases: Suciu et al., Trio, MayBMS) is **not mentioned anywhere**. Any database or theory referee will immediately ask how an "approximate relation with false-correspondence rates" differs from a tuple-independent probabilistic database. There is a clean answer (in probabilistic DBs the *data* is uncertain; here the *base relation is objective* and the uncertainty is a property of a space-saving *representation*, a membership oracle with FPR/FNR), but the paper must state it. Without this paragraph the contribution looks either unaware of or redundant with prior art. See citation-verifier CV-3 and literature context A1.

### N-3 (MAJOR). The abstract promises far more than the body delivers (and more than this paper should own)
The abstract advertises: entropy lower bound on bits-per-relation; join/project error propagation; partial-function composition; an approximate-set-based implementation; a **perfect-hash-map** projection mechanism; and an **oblivious-database / rank-ordered Encrypted Search with fuzzy-set extensions** application. Of these:
- the bits-per-relation lower bound is owned by `bernoulli_entropy`/`bernoulli-hash-function`;
- the perfect-hash-map construction is owned by `bernoulli-phf`/`bernoulli-hash-function`;
- partial-function composition is owned by `bernoulli_maps`;
- the join/project propagation (the part this paper *should* deliver) is the **least developed** in the body;
- the Encrypted Search application is a TODO-laden orphaned file not in the build.
So the abstract simultaneously **over-claims scope** (promising sibling-owned material) and **mis-weights** (foregrounding what is least finished). **Fix**: rewrite the abstract to claim only N+1..N+4, defer entropy/PHF/optimal-construction claims to the siblings with citations, and lead with join/project error propagation.

## Significance (relative to declared role)
Conditional on the contributions being completed and properly fenced from the siblings, the significance is **moderate and legitimate**: a relational-algebra layer over Bernoulli sets is a natural and useful capstone for the family, and the invariant-preservation angle (N+3) is genuinely interesting. It is not a high-significance standalone result, but as the relational extension of an established framework it earns its place, provided the duplication and over-claiming are fixed.

## Cross-verification handoff
The question "is the duplication/over-claim a novelty deficit or merely a framing problem?" is routed to the prose-auditor. My position: it is **primarily a framing problem** (the novel core exists; it is mis-presented), so the fix is structural (re-fence, re-cite, re-weight the abstract), not a demand for new ideas. I also flag for prose-auditor that the unclear writing in predicates.tex and properties.tex is partly *hiding* the weak/duplicated parts; clarifying the prose will make the over-claim more obvious and easier to correct.

## Summary for synthesis
- Major: 3 (N-1 sibling-duplication of map composition and predicates; N-2 no probabilistic-DB differentiation; N-3 abstract over-claims scope and mis-weights)
- The contribution is real (N+1..N+4) but currently undifferentiated and over-promised. None of this is fatal to novelty; all of it is addressable by re-fencing against the siblings, adding the probabilistic-DB contrast, completing the join/project material, and rewriting the abstract to match what this paper alone owns.
