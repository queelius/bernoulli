# Novelty Assessor Report, bernoulli_maps

**Specialist**: novelty-assessor (contribution clarity, differentiation, significance)
**Date**: 2026-05-29
**Framing instruction honored**: This is an EXTENSION paper in a 9-paper family. Shared foundations (the two axioms, binomial error-counts, the composition theorem skeleton) are inherited from `bernoulli_sets` by design and are NOT counted against novelty. Novelty is assessed relative to the paper's declared role: approximate maps as first-class objects, the algebra of map composition, special functions, entropy of maps, and the singular hash map.

## Verdict summary

The paper has a real and clearly-owned contribution: the **compositional algebra of approximate maps** (the FNR/FPR of `g circ f`, the `rho` overlap parameter, model-order elevation), plus the **function-space/Kronecker unification** that ties Booleans, sets, maps, and relations into one model. This is genuine open ground, the closest external prior art (Bloomier filters, DMC channel products) does not provide it. The weaker axes are the entropy map and the singular hash map, which restate constructions close to known retrieval data structures and to the author's own foundation paper. The differentiation from the two closest in-family papers (`relations`, `data_type`) is articulated but partly rests on a companion paper that is not yet citable.

## Contribution-by-contribution assessment

The paper lists four contributions (intro). My assessment of each:

### Contribution 1: "function-space viewpoint ... unifying Booleans, sets, maps ... Kronecker factorization"
- **Novelty**: Moderate, and primarily *expository/organizing*. The mathematical fact (independent per-input channels => tensor-product joint matrix) is standard information theory (product of discrete memoryless channels). What is new is using it as the *single organizing principle* for the whole Bernoulli family and reading off the parameter-count collapse (exponential to linear) as the signature of the independence axiom.
- **Significance**: High *within the family* (it is the conceptual spine connecting the papers), modest *outside* it. This is a legitimate "viewpoint" contribution, but the paper should not imply the Kronecker fact itself is novel.
- **Differentiation**: Adequate against external work; the danger is overclaiming. `thm:kronecker` is presented as a theorem (fine) but its content is the standard tensor factorization (logic-checker M4 flags count errors).

### Contribution 2: "the Bernoulli map model ... with model order"
- **Novelty**: This is the legitimate core generalization, from codomain `B` (sets) to arbitrary `Y` (maps), with the Maybe-type lifting and the positives/negatives partition. The *model order* definition (minimum number of i.i.d. blocks) is inherited in spirit from the foundation but applied to maps.
- **Significance**: High for the family; it is what makes "map" a first-class Bernoulli object.
- **Differentiation from Bloomier (Chazelle 2004)**, the closest external prior art: The Bloomier filter already stores `f: S -> R` with arbitrary values on members and garbage on non-members. The Bernoulli map's differentiator is **not the data structure** but the **probabilistic model**: explicit per-element FPR/FNR as a *type signature* (`f*_{eps}^{fnr}`), the binomial error-count distributions, and (crucially) the composition algebra. **The paper states this but too softly.** The intro says Bloomier "is exactly the generalization that the Bernoulli map model formalizes," which is generous to Bloomier and undersells the model's own contribution. The differentiation should be sharpened to: "Bloomier gives one construction; we give the *model* (error distributions, type-level rates, composition closure) of which Bloomier is an instance."

### Contribution 3: "the composition theorem ... `fnr = 1-(1-fn1)(1-fn2)` ... `rho` ..."
- **Novelty**: **This is the strongest and most defensible contribution.** There is no standard "algebra of approximate maps under composition" in the literature. The FNR product rule generalizes the foundation's set-composition result (logic-checker m1 confirms it is the correct Maybe-type specialization), but the **FPR result with the `rho` overlap parameter is genuinely new** to this paper, the foundation's sets are total indicators with no `Dod(g)` overlap question, so `rho` has no analog there. The two overlap corollaries (`rho=0` => `eps1 eps2`, `rho=1` => `eps1(1-fn2)`) and the `k`-fold corollary with the precision/recall trade-off remark are clean, useful, and original.
- **Significance**: High. This is the paper's best claim to a citable result and should be foregrounded as *the* contribution.
- **Differentiation**: Excellent; nothing external provides this.

### Contribution 4: "the entropy map ... and the singular hash map achieving `-log2 eps + mu`"
- **Novelty**: **Weakest axis.** (a) The `-log2 eps + mu` space law is essentially the foundation's space result (the `-log2 alpha + mu` "space-accuracy duality" the family attributes to `bernoulli_entropy` and `bernoulli-hash-function`); within the family this is not new to the maps paper, it is imported. (b) The singular hash map is a hash-collision construction very close to known succinct *retrieval* structures (Dietzfelbinger-Pagh 2008, and the modern binary fuse / BuRR / RecSplit line) that already hit the same `r + log(1/eps)` floor, in linear time rather than the SHM's exponential expected trials (methodology M6). The SHM's distinctive feature is the "singular" collision idea (one salt makes all keys collide into a shared bucket), which is a clean pedagogical device but not obviously an advance over existing retrieval.
- **Significance**: Moderate within the family (it concretizes the optimal construction *for maps* specifically), low as an external contribution.
- **Differentiation**: **Insufficient.** The paper does not cite or contrast the modern retrieval line, and presents the SHM as "a concrete algorithm that ... achieves the information-theoretic lower bound" without acknowledging that practical structures already do this. The entropy-map/SHM material overlaps heavily with `bernoulli-hash-function` (the family's designated home for "space-optimal construction") and the paper should clarify why both papers contain a singular-hash construction.

## Differentiation from the two closest in-family papers (requested)

### vs `bernoulli_relations` (`arelation`, cited)
- **Boundary is clean.** Maps = single-valued (unique first coordinate); relations = general `n`-ary with join/project/select. The maps paper's only relational content is section 5.4 ("Relations as `n`-ary predicates"), which is explicitly a teaser deferring to the companion ("The full treatment ... is developed in the companion paper on approximate relations"). No novelty conflict. The conclusion's "relational algebra operators ... merit further investigation" correctly cedes that ground.
- **Verdict**: well-differentiated.

### vs `bernoulli_data_type` (referenced in prose, NOT in bib)
- **Boundary is articulated** via the "Two perspectives, one theorem" paragraph (conclusion): maps = *denotational* (a map is a point in `Y^X` approximated per-input); data_type = *constructive* (types built from Bool via sum/product/exponential). They converge at the exponential type `A -> B`.
- **Concern (novelty)**: The maps paper's claimed unique angle is "the function-space viewpoint with Kronecker factorization, stated denotationally." But data_type also uses the Kronecker factorization (the conclusion says "Product types preserve the Kronecker factorization ... the exponential type `A -> B` is precisely the function space studied here"). So the *same theorem* lives in both papers, from "opposite directions." This is defensible (different framings of one fact across companion papers is normal in a family), but the maps paper leans on it as a headline contribution (Contribution 1), which makes the overlap with data_type more load-bearing than the relations overlap. The reader cannot check the boundary because **data_type is not citable** (no bib entry, no title given beyond "a companion paper on random approximate algebraic types"). 
- **Verdict**: adequately differentiated *in intent*, but the shared Kronecker-factorization headline plus the missing citation make this the one place where novelty attribution between two family papers is fuzzy. Recommend: (i) add the data_type bib entry, (ii) state explicitly which paper *owns* the Kronecker factorization theorem (suggest: data_type proves it constructively, maps states it denotationally and cites data_type, or vice versa), so the two papers do not appear to independently claim the same result.

## Is unclear writing hiding a weak contribution? (cross-check lens for prose findings)
Routed from prose-auditor: sections 6 to 7 are the roughest prose. My read: the rough writing in section 6/7 is *not* hiding a strong contribution; it coincides with the *weakest* novelty axis (entropy map / SHM, Contribution 4), which is largely imported from the foundation/`bernoulli-hash-function` and overlaps known retrieval work. The polished sections (1 to 5) carry the genuine novelty (the composition algebra). So clarity and novelty are *aligned* here: the paper is clearest where it is most original and roughest where it is least original. This supports foregrounding Contribution 3 and trimming/deferring Contribution 4.

## Recommendations to strengthen the novelty claim
1. **Foreground the composition algebra (Contribution 3) as the primary result.** It is the one thing no external or in-family paper provides. The `rho` parameter and the model-order-elevation lemma are the citable nuggets.
2. **Sharpen the Bloomier differentiation**: "Bloomier is a construction; we give the model and its composition closure."
3. **Right-size Contribution 1**: present the Kronecker view as an organizing principle, not a novel theorem, and coordinate ownership with `data_type`.
4. **Down-scope or better-differentiate Contribution 4**: cite the modern retrieval line, reframe SHM as a theoretical achievability construction, and clarify the overlap with `bernoulli-hash-function`.
5. **Add the `data_type` citation** so the maps-vs-data_type boundary is checkable.

## Significance bottom line
Within the Bernoulli family this paper is structurally important (it is the function-space layer and the home of the composition algebra). As a standalone external contribution, its weight rests almost entirely on the composition algebra; the construction half is derivative. The contribution is real but currently *mis-weighted* in the framing (the abstract and intro give equal billing to the SHM, which is the weakest part).
