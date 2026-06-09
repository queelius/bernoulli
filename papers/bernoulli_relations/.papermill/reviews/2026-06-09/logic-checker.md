# Logic Checker Report

**Paper**: *The abstract data type of the approximate relation*
**Date**: 2026-06-09
**Scope**: Proof correctness, logical-chain integrity, claim support. Per the area chair's brief the core *numerics* are pre-verified (validate.py passes 23 rows, worst abs error 0.000686; independent re-derivation of `thm:symmetric_preservation`, `thm:join_dependence`'s `1/a`, `thm:project` TPR, asymmetric join FNR). My effort here is on proof **presentation, rigor, and any remaining gap**, not on recomputing.

## Independent re-derivation (confirming the math)

I re-derived every load-bearing closed form by exact algebra (`python3` one-off, independent of validate.py):

| Result | Theorem | Re-derived value | Status |
|---|---|---|---|
| Join correlation `P(both)/product = 1/a` | thm:join_dependence | 1.111111 = 1/0.9 | MATCH |
| Join covariance `a(1-a)P(B)^2` | thm:join_dependence | 0.072900 | MATCH (closed form holds) |
| Symmetric preservation bases `τ²+ω²`, `(1-ε)²+ε²` | thm:symmetric_preservation | 0.820000, 0.905000 | MATCH (this is the row validate.py SKIPS; MC confirms 0.8199) |
| Projection TPR, j≥2 | thm:project (ii) | (3,2)=0.990500, (5,2)=0.991426 | MATCH |
| Asymmetric join FNR (ω_R=.1, ω_S=.2) | thm:join (i) | 0.280000 = ω_R+ω_S-ω_Rω_S | MATCH |
| Functional, reflexive, symmetric closure | thm:functional/reflexive/symmetric_closure | all match | MATCH |

**Every closed form is correct.** I additionally confirmed the **covariance** form `Cov = a(1-a)P(B₁)P(B₂) > 0`, which the paper states only as a ratio; the covariance is positive and the closed form is clean, a strengthening the paper could cite verbatim.

## Proof-by-proof assessment (presentation and rigor)

- **thm:select** (selection rate-transparent), rel_algebra.tex:39-65. **Sound and cleanly presented.** The argument (restriction to a sub-universe selects a sub-collection of i.i.d. trials; no rescaling, no coupling) is correct and complete.

- **thm:project** (FPR `1-(1-ε)^k`, TPR `1-(1-τ)^j(1-ε)^{k-j}`), rel_algebra.tex:96-146. **Sound, and the subtle j≥2 case is handled correctly.** The proof partitions the fiber into `j` members and `k-j` non-members and composes the miss probabilities by independence over the *distinct* fiber tuples. The monotonicity bounds (`≥ε_R`, `≥τ_R`) are correctly justified by "dropping factors from a product over [0,1]." No gap.

- **thm:project_order** (preserves independence, raises model order), rel_algebra.tex:201-221. **Sound.** Disjointness of fibers for `s≠s'` (since `t|_Y=s` and `t|_Y=s'` are incompatible) gives mutual independence; the per-fan-in level sets are the rate blocks. The model-order/parameter-count remark (rel_algebra.tex:233-240) is consistent with the family framing. `cor:uniform_fanin` is correct.

- **thm:join** (FNR `1-τ_Rτ_S`; FPR three-region), rel_algebra.tex:252-312. **Sound, and the deferral is honest.** The FNR is the intersection FNR (logical AND of two independent member tests). The FPR is correctly presented as a *three-region prevalence-weighted average*, with the explicit warning (rel_algebra.tex:309-311) that the both-absent corner `ε_Rε_S` "alone is only the both-absent corner and understates the rate whenever a one-absent region has positive prevalence." The deferral to `bernoulliComposition` for the full weighted rate is accurate.

- **thm:join_dependence** (independence failure, factor `1/a`), rel_algebra.tex:318-348. **Correct and rigorous; the spine of the paper.** `P(A∩B₁∩B₂)=a·P(B₁)·P(B₂)` (shared `A` counted once) versus product-of-marginals `a²P(B₁)P(B₂)`; ratio `1/a>1` for `0<a<1`. The follow-up caveat (rel_algebra.tex:359-362) is itself correct and valuable: marginal rates remain exact per tuple, the FP *count* expectation still works by linearity (which does not need independence), and only higher moments / the all-correct probability feel the correlation. This is the right level of rigor.
  - **Minor presentation gap (LC-MINOR-1)**: the proof asserts `B_i` "independent of `A` and of each other" without re-invoking *why* (the two approximations `R̃`, `S̃` are independent, asm at rel_algebra.tex:24, and `s₁≠s₂` are distinct tuples of `S̃` hence independent by asm:ber_trial). One clause would make the proof self-contained rather than relying on the reader to recall the section preamble.

- **thm:reflexive** (`τ^{|A|}`), properties.tex:30-45. **Sound.** `|A|` independent diagonal TP trials, all-fire `= τ^{|A|}`, decays geometrically. Complete.

- **thm:symmetric_preservation** (`(τ²+ω²)^P((1-ε)²+ε²)^N`), properties.tex:54-87. **Sound** (and this is the row validate.py deliberately skips, so my independent re-derivation + the supplementary MC I ran are the only checks; both confirm). Each unordered pair's two ordered trials must *agree*; positive-pair agreement `τ²+ω²`, negative-pair agreement `(1-ε)²+ε²`; pairs disjoint, hence product. The "sum of two squares of complementary probabilities, hence `<1`" argument for the vanishing limit is correct.

- **thm:symmetric_closure** (FPR `1-(1-ε)²`, TPR `1-(1-τ)²`), properties.tex:95-119. **Sound, and the prior TPR bug is fixed.** Both slots carry the OR-doubling; the proof explicitly flags "the same doubling that raises the FPR ... also raises the TPR ... not the unchanged τ" (properties.tex:118). Complete.

- **thm:functional** (`(1-ε)^{|Y|-1}` per key), properties.tex:137-167. **Sound.** The asymmetry argument (only a false positive adds a spurious second value; a false negative on the true value leaves zero values, still single-valued, correctly excluded from the product) is right. Distinct keys index disjoint pair sets, hence independence and the product over `|Dom|` keys. Complete.

- **Transitivity** (sec:transitive, properties.tex:169-201). **Handled honestly; no spurious closed form, which is the correct editorial call.** The reasoning (≈`|A|³` coupled triple constraints; decays fastest; manufactured-conclusion pairs each near `ε`; transitive closure is a genuine cascade) is qualitatively correct. The independence caveat that a prior review wanted is now **present and explicit** (properties.tex:191: "as a first-order heuristic, ignoring the cross-triple coupling just noted, ... and the true rate is smaller still once that coupling is accounted for"). No remaining gap.

- **thm:fpbinom / thm:fpr** (inherited binomial FP count, CLT-limiting realized FPR), approx_rel_model.tex:66-95. **Correct restatements** of the set-model machinery. Short and right.

- **def:approx_rel / def:approx_pfun**: the prior "conditions on its own negation" defects are **fixed** (def:approx_rel condition (i) conditions on the objective `R(X)`; def:approx_pfun (ii) conditions on `∉ Dom(f)`). Both correct. See PROSE/notation report for a clarity finding on the `\AT[\fnrate][\fprate]` complement notation in condition (i).

## Findings

**LC-MINOR-1** (rel_algebra.tex:336): `thm:join_dependence` proof asserts `B_i` independent of `A` and each other without re-deriving from the stated assumptions. Add a half-clause citing the cross-approximation independence (rel_algebra.tex:24) and asm:ber_trial. Cosmetic; the result is correct.

**LC-SUGGESTION-1**: state the **covariance** `Cov = a(1-a)P(B₁)P(B₂)` alongside the `1/a` ratio in `thm:join_dependence`. It is a clean positive closed form, strengthens the "positively correlated" claim quantitatively, and I verified it holds exactly.

**LC-SUGGESTION-2**: `asm:ber_trial` (approx_rel_model.tex:60-61) is logically correct but its *operator names* are garbled ("an related test"; "is-not-relation test on any tuple in the relation"). This is a prose/notation defect, routed to the prose-auditor report (PA-MAJOR-1), flagged here because the assumption is load-bearing for every proof and a referee re-deriving from it will stumble on the wording.

## Verdict
**Zero critical, zero major logic findings.** All proofs are correct; the math is independently verified including the one row the harness skips. Findings are one minor presentation gap and two optional strengthenings. The logical chain from `def:approx_rel` through the operator theorems to the invariant theorems is intact.
