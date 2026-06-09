# Novelty Assessor Report

**Paper**: *The abstract data type of the approximate relation*
**Date**: 2026-06-09
**Scope**: Contribution clarity, differentiation, significance, for a **database-theory venue** (ICDT / PODS / Information Systems). Citation/novelty findings I cannot web-verify are tagged `[VERIFY]` for the area chair.

## The four claimed contributions (intro.tex:31-60)

1. **Operator error propagation** (selection transparent; projection FPR `1-(1-ε)^k`; join breaks independence).
2. **Invariant preservation** (reflexive/symmetric/functional/transitive rates + symmetric closure repair).
3. **The approximate partial function** as the single-valued special case.
4. **A trapdoor-database application** (cipher relations, encrypted search, leakage model).

## Novelty triage, contribution by contribution

### Contribution 1, operator propagation: SPLIT verdict
The contribution is not uniform in novelty, and the paper should not present it as one undifferentiated block.

- **Selection transparency**: trivial (correctly labeled "the trivial case" at rel_algebra.tex:67). Zero novelty claim; fine.
- **Projection FPR `1-(1-ε)^k`**: the **formula is standard** (FPR of an OR over `k` independent AMQ trials; identical to a union of `k` Bloom filters). `[VERIFY]` that no prior work frames it as a relational projection operator. Novelty here is **by-framing only** (the fiber/fan-in packaging and the model-order observation), which is weak. **A DB-theory referee will recognize the formula.** The paper does not currently concede this; it should, to avoid the appearance of claiming a known identity as new.
- **Join independence failure (`thm:join_dependence`)**: **this is the real contribution and the paper's spine.** The observation that two join outputs sharing an operand component reuse the same Bernoulli trial and are positively correlated by exactly `1/a`, with the query-planning consequence (an independence-assuming planner understates the all-correct probability), is sharp, correct, validated, and not addressed by the marginal-probability machinery of probabilistic databases. **`[VERIFY]` (highest priority)**: whether the Bloomjoin / runtime-filter literature already notes the dependence among join outputs sharing a probe. If it does not (the literature scout's weak belief), this is a genuine, citable result. If it does, the contribution shrinks to "a clean, validated statement of folklore." **The entire venue case turns on this `[VERIFY]`.**

### Contribution 2, invariant preservation: STRONGEST and most differentiated
The reviewer is **not aware** of prior work asking whether reflexivity/symmetry/transitivity/single-valuedness survive when an exact relation is stored in a lossy AMQ structure, with closed-form preservation probabilities and a symmetry-closure-vs-transitivity-cascade contrast. `[VERIFY]` against the AMQ and constraint-under-uncertainty literatures. The constraint-repair / inconsistent-database literature concerns *dirty data* (uncertainty in the data), not *representation-induced* invariant violation over an exact base, so it does not subsume. **This is the cleanest novelty in the paper and is currently UNDER-sold** relative to the operator material, which is the reverse of the right emphasis for a DB-theory venue.

### Contribution 3, approximate partial function: borderline, partly sibling-owned
The single-valued special case is a legitimate corollary of `thm:functional`. But the **full partial-function ADT exposition** (properties.tex:215-297: classical recap, `(|Y|+1)^{|X|}` counting, Dom/Image/Range, the `Z₁×Z₂→Q` table example, `def:approx_pfun`) is heavy, largely classical, and overlaps the maps paper's territory. Map *composition* is correctly deferred to `bernoulliMaps` (properties.tex:217), which is the right call. The remaining ADT material is not novel; it is scaffolding. **Trim to the single-valuedness link and `def:approx_pfun`.**

### Contribution 4, trapdoor-database application: novelty-by-framing, honestly scoped
The section explicitly says "The construction is not new machinery" (oblivious_rel_model.tex:8) and defers to `phf`. Bloom-filter-backed encrypted indexes (Goh Z-IDX `[VERIFY]`, the SSE literature) are well-trodden. The contribution is locating the leakage profile in the Bernoulli rates and connecting it to `thm:join_dependence` (oblivious_rel_model.tex:84-86), which is a nice touch. Appropriately modest; no over-claim. Fine as-is.

## The central positioning question (the area chair's GOAL 1)

**Is the prob-DB distinction airtight?** Largely yes *in object*, with one soft seam:

- **The distinction is real and correctly stated** (intro.tex:62-78): probabilistic/uncertain DBs (Suciu et al.; Trio; MayBMS) model uncertainty *in the data* (possible-worlds, tuple probabilities, lineage); here the base relation is *exact* and the error is *representation-induced*. The questions (invariant survival, fan-in FPR amplification) are genuinely outside the possible-worlds frame. This is not a strawman.
- **The soft seam (`[VERIFY]`, NA-MAJOR-1)**: a **tuple-independent probabilistic database** with per-tuple probability `p` is formally close to a Bernoulli relation with `τ=p`. The *marginal* operator results (join FNR `1-τ_Rτ_S`, projection FPR `1-(1-ε)^k`) look recoverable as **extensional query evaluation on independent tuples**, which the PDB literature very likely already does. If so, the **marginal-rate results do not differentiate from PDBs**, and the paper's defensible novelty narrows to (a) invariant preservation and (b) `thm:join_dependence`'s *joint* law, neither of which PDB marginal-probability evaluation addresses. **The paper should pre-empt this**: state explicitly that the marginal rates coincide with tuple-independent-PDB extensional evaluation, and that the contribution is the *joint* law (correlation) and the *invariant* survival, which possible-worlds marginals do not give. As written, the related-work paragraph leaves this opening for a referee to exploit.

## Significance for the target venue

The differentiated core (join correlation + invariant fragility/closure dichotomy) is a **real but modest** contribution. For ICDT/PODS specifically it lacks the venue's usual currency (a complexity/lower-bound/dichotomy theorem). The symmetry-admits-cheap-closure / transitivity-does-not contrast is *gestured at* but not formalized as a **dichotomy theorem**, which is exactly the kind of result that would lift this from "useful formulas" to "DB-theory contribution." See the unified review's venue verdict.

## Findings

**NA-MAJOR-1** `[VERIFY]` (intro.tex:62-78): pre-empt the tuple-independent-PDB objection. The marginal operator rates appear recoverable from extensional evaluation over independent tuples; the related-work paragraph should concede this and pin the novelty on the *joint* law (`thm:join_dependence`) and invariant preservation, which possible-worlds marginals do not cover. Area chair to `[VERIFY]` whether independent-tuple PDB evaluation already yields the marginal join/project rates.

**NA-MAJOR-2** `[VERIFY]` (intro.tex:36-44; rel_algebra.tex:96-153): the projection `1-(1-ε)^k` amplification is a standard OR-of-filters identity. The paper presents it as a contribution without conceding the formula is known. Add one sentence acknowledging the identity and claiming only the relational-projection framing / model-order reading. Area chair to `[VERIFY]` no prior relational-projection framing exists.

**NA-MINOR-1** (emphasis): the **invariant-preservation** results (the strongest novelty) are under-weighted relative to the operator section. Consider leading the abstract/intro contributions list with the invariant fragility + closure dichotomy, not only the join.

**NA-MINOR-2** (properties.tex:215-297): the partial-function ADT exposition is largely classical/sibling-owned scaffolding. Trim to `def:approx_pfun` and the single-valuedness link.

## Verdict
Real differentiated core (join correlation; invariant preservation), but its venue-defining novelty rests on two `[VERIFY]` items the area chair must check personally (Bloomjoin dependence prior art; independent-tuple-PDB marginal evaluation). Two framing concessions would make the positioning airtight. No fabricated-novelty or plagiarism concerns.
