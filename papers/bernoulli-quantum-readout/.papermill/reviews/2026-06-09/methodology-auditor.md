# Methodology Auditor

**Date**: 2026-06-09
**Scope**: Methodological soundness of the additions; reproducibility of the worked numbers; whether 3.6 changes the empirical posture.

## Reproducibility (re-verified this pass)

This is a methods/perspective paper with no hardware or simulator experiment, so "methodology" is the derivations and the worked tables. Both tables were recomputed from the stated formulas:

- **Table 1** (`tab:syndrome`, symmetric): all six rows match `(1/2)(1-(1-2q)^n)` and `nq` to the printed precision; relative overestimates 1.0/3.1/7.2/5.3/16.3/40.5% all reproduce. CORRECT.
- **Table 2** (`tab:syndrome-asym`, asymmetric T1-biased): the four latent words reproduce as 0.109979/0.174982/0.233842/0.315168 (printed 0.110/0.175/0.234/0.315); symmetrized single rate at q=0.07 reproduces 0.226496 (printed 0.226); the "almost three times" ratio is 2.866. The mean of the eight per-qubit rates is exactly 0.07, so the symmetrized-rate choice is honestly the best a one-rate model can do. CORRECT.
- **Section 3.6 spectral identity**: Monte Carlo (2M trials) confirms the parity-wrong probability to three places.

The numbers are exact and independently reproducible from the formulas alone. No data, no estimator, no statistical test is involved, so there is no statistical-rigor surface to audit.

## Does 3.6 change the empirical posture? No.

Section 3.6 is pure re-derivation in operator language; it introduces no new experiment, dataset, or estimator, and it explicitly says so (line 519, "bookkeeping, not new theorems"). The scope section (`sec:scope`) item 5 already concedes there is no empirical validation, and 3.6 makes no new empirical claim. So the addition does not move the paper's standing on the one real methodological limitation (no hardware/simulator study), which remains a future-work item per item 5.

## Finding M1 (cross-check of logic-checker L1), asymmetric eigenvalue claim

I independently reproduced logic-checker's L1: the asymmetric assignment matrix `[[1-eps,om],[eps,1-om]]` has nontrivial eigenvalue `1-eps-om` (e.g. 0.88 for (0.02,0.10)), which is not `1-2r_i` for either side. The corollary cor:parity-asym is methodologically sound (it applies thm:parity to the flip indicators `F_i` whose conditional means are `r_i`, which is exactly right), so this is a *labeling* imprecision in the prose extension at line 569 to 571, not a flaw in the derivation. I concur with L1's severity (minor) and fix.

## Finding M2 (suggestion), table-generator provenance

Per prior reviews (carried suggestion S1), the two tables are computed by hand-entered values with no checked-in generator script. The numbers are correct, but a small script under a `code/` or `research/` dir would make the exactness auditable by a referee and guard against future-edit drift, especially now that Table 2 has eight rate inputs. Optional, pre-existing.

## Verdict
Methodologically clean for a perspective/methods paper. All worked numbers reproduce exactly. Section 3.6 adds no empirical surface and no methodological risk. The single substantive item (L1/M1) is a prose-labeling fix, not a derivation error. No major methodology issue.
