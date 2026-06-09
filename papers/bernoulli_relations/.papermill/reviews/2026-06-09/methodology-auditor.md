# Methodology Auditor Report

**Paper**: *The abstract data type of the approximate relation*
**Date**: 2026-06-09
**Scope**: Experimental design, statistical rigor, reproducibility of the Monte Carlo validation, and the soundness of the modeling assumptions that the closed forms rest on.

## The validation harness (code/validate.py)

**Ran it directly**: `python3 code/validate.py`, seed 20260608, 2,000,000 trials/row. Result: **23 fit rows PASS, worst absolute error 0.000686** (tolerance 0.005); the single MISMATCH row is the deliberate negative control. Reproduced cleanly; no external dependencies beyond numpy.

### What the harness does well (strengths)
- **Faithful per-tuple model.** `draw_membership` (validate.py:53-63) realizes exactly the per-tuple law of `asm:ber_trial`: a member is reported w.p. `τ`, a non-member w.p. `ε`. This is the right primitive and it matches the manuscript's stated model.
- **The negative control is the right design.** The harness does not merely confirm the formulas it wants; it includes the **independent model that the paper predicts FAILS** (validate.py:150-152) and shows the empirical `P(both)=0.728758` tracking the *correlated* value `0.729`, not the independent `0.6561`. Validating a "this assumption breaks" claim by exhibiting the broken assumption as a control is methodologically correct and rare. This is the harness's best feature.
- **Direct shared-trial construction** (validate.py:130-157): one trial drawn for the shared `r`, two independent trials for `s₁,s₂`, then `out1 = r & s1`, `out2 = r & s2`. This is precisely the mechanism of `thm:join_dependence`, simulated structurally rather than by plugging in the formula. The correlation factor `1/a` is *measured*, not assumed (factor_emp = 1.110742 vs predicted 1.111111).
- **Reproducible**: fixed seed, documented rates, CLI knobs for `--trials/--seed/--tol`, self-documenting header. Good practice.

### Coverage gaps and design notes
- **MA-MINOR-1 (coverage)**: the harness validates **8 of the paper's closed forms** but **not `thm:symmetric_preservation`** (the `(τ²+ω²)^P((1-ε)²+ε²)^N` symmetry-preservation rate). The table at rel_algebra.tex:450-479 transcribes only the symmetric *closure* rows, not the symmetric *preservation* row. I closed this gap by independent re-derivation plus a one-off MC (positive-pair agreement 0.8199 vs analytical 0.8200; see logic-checker report), so the result is confirmed, but **the shipped harness does not cover it.** Add a `validate_symmetric_preservation` case (two ordered trials per pair, count agreement) so every theorem in the paper has a harness row. Cheap and closes the one uncovered theorem.
- **MA-MINOR-2 (single rate point)**: all validation uses one rate pair (`ε=0.05, ω=0.10`). The formulas are exact algebra so a single point is *sufficient* for a correctness check, but a referee may want to see the harness exercise an **asymmetric operand case** (`ε_R ≠ ε_S`, `ω_R ≠ ω_S`) for the join, since the manuscript states the asymmetric three-region FPR but the harness only runs symmetric operands. I independently verified the asymmetric join FNR (`ω_R=.1, ω_S=.2 → 0.28`); adding it to the harness would make the asymmetric claim reproducible from the shipped code.
- **MA-MINOR-3 (Monte Carlo error not reported)**: the table reports point estimates and absolute error but no standard error / CI. At 2e6 trials the SE on a rate near 0.1 is ~0.0002, comfortably below the observed errors, so the agreement is statistically sound. Stating the SE (or a `±` band) in the caption of `tbl:validation` would make "agree to three to four decimal places" a quantified claim rather than an eyeballed one. Optional.

## Modeling-assumption audit

- **asm:ber_trial (approx_rel_model.tex:58-62)**: the i.i.d.-Bernoulli-per-tuple assumption is the foundation of every binomial/CLT result and every operator proof. It is **realistic for the cited constructions** (Bloom filters, perfect hash filters) and the paper says so (approx_rel_model.tex:63). **However the assumption's wording is garbled** ("an related test"; the operator names "related test" / "is-not-relation test" are assigned confusingly). The *logic* is correct (FP-on-non-member mean `ε`, FN-on-member mean `ω`), but a methodologist re-deriving from the assumption statement will trip on it. Routed to prose-auditor (PA-MAJOR-1); flagged here because it is the load-bearing assumption.
- **Independence-of-the-two-approximations** assumption for the join (rel_algebra.tex:24): stated and used correctly. This is the standard "two independent filters" assumption and is appropriate; worth noting that in a real system two filters built with *correlated* hash seeds would violate it, but the paper's claim is explicitly about independent operands, so this is in-scope.
- **The "exact predicate carries no randomness" assumption** (rel_algebra.tex:26-30): correctly isolates the only randomness as the operand membership tests. This is what makes the operator analysis clean and it is honestly stated.

## Reproducibility verdict
**Strong.** The harness is real, faithful, reproducible from a fixed seed, includes a negative control, and matches the analytics to 3-4 digits. The only methodological gaps are coverage (one theorem unvalidated by the shipped script; symmetric and asymmetric variants under-exercised) and the absence of a reported MC standard error. None of these undermines a single result; they are completeness items.

## Findings
- **MA-MINOR-1**: add a `thm:symmetric_preservation` case to validate.py (currently the only paper theorem with no harness row).
- **MA-MINOR-2**: add an asymmetric-operand join case (`ε_R≠ε_S`) to make the three-region/asymmetric FNR claim reproducible from the shipped code.
- **MA-MINOR-3**: report Monte Carlo standard error (or a `±` band) in the `tbl:validation` caption to quantify the agreement claim.

## Cross-verification note (logic, routed here per protocol)
Per the orchestrator's cross-verification routing (methodology audits logic findings for reproducibility): I confirmed `thm:join_dependence` is not only algebraically correct but **structurally reproduced** by the harness's shared-trial construction, and that the covariance form `a(1-a)P(B₁)P(B₂)` I derived matches the empirical covariance implied by the table. The logic and the methodology agree: the independence failure is real, measured, and reproducible.
