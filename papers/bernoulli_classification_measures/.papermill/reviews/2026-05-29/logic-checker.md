# Logic and Proof Review

**Paper**: Binary classification measures for random approximate sets
**Reviewer role**: logic-checker (performed by area chair; Task delegation unavailable in this environment)
**Date**: 2026-05-29

## Summary

The logical chain is sound and the derivations are correct. I independently re-derived and numerically verified every closed-form result (PPV, NPV, accuracy, Youden's J, F1, both expectations and variances) against high-sample Monte Carlo. Agreement is to 4 to 5 decimal places in every case, including a deliberate small-count stress test where the delta method is most strained. One genuine internal inconsistency exists in a notational definition (Proposition 2.1 vs Corollary 2.5). It does not affect any downstream result because the theorems are parameterized directly in tau and epsilon.

## Verified Results (all confirmed correct)

| Result | Location | Check |
|---|---|---|
| E[PPV] second-order delta | Thm 3.1, eq (3.2); App A | Matches MC to 1e-5 at p=100,n=9900; holds even at p=n=20 (|diff| < 2e-4) |
| Var[PPV] first-order delta | eq (3.3); App A | Form matches standard (grad)^T Sigma (grad) with diagonal Sigma |
| E[ACC], Var[ACC] | Thm 3.2 | Exact; MC confirms E and Var to 3+ sig figs |
| E[NPV], Var[NPV] | Thm 3.3 | Correct by the stated PPV-dual substitution (t_n, f_n) |
| E[J] = tau - eps, Var[J] | sec 3, eq (3.13) | MC confirms; independence of TPR_p and alpha_n is valid (disjoint populations) |
| E[F1] second-order delta | Thm 3.4, eq (3.14); App B | MC confirms to 1e-4 across epsilon grid |
| Var[F1] first-order delta | eq (3.15); App B | MC confirms |
| Interval PPV bounds | Ex 3.2 | Monotonicity argument correct; bounds match the true min/max over the 4 vertices exactly |
| Interval accuracy vertices | Ex 3.1 | Multilinearity argument is valid; vertex enumeration is the correct guaranteed-bound method |
| Accuracy reparameterization | Ex 3.1 (table) | eps(gamma,lambda) = (1-gamma)/(1-lambda) verified; boundary behavior at lambda to 1 correctly described |
| PPV limit observations (1-3) | sec 3 list | All three hold: large-set zeroth order; eps != 0, n to inf gives PPV to 0; eps to 0 gives PPV to 1 |

The appendix PPV proof is fully rigorous: gradient and Hessian of f(t,f)=t/(t+f) are correct, the second-order Taylor expectation correctly drops the first-order term (zero mean), the cross term vanishes by TP-FP independence, and the substitution of binomial variances yields eq (3.2). The trace form (1/2) tr(H Sigma) used in the F1 proof is the correct compact statement of the same second-order expansion.

## Findings

### MINOR-1 (logic / notation): Inconsistent definition of the sample rate beta

- **Location**: Preliminaries, Proposition 2.1 (line 26) versus Corollary 2.5 (line 95).
- **Quoted text (Prop 2.1)**: "The expected sample rates satisfy $\Expect{\alpha} = \fprate$ and $\Expect{\beta} = \tprate$."
- **Quoted text (Cor 2.5)**: "the \emph{true positive rate} is given by $\TPR_p = 1 - \beta_p$."
- **Problem**: The two statements are mutually inconsistent. If `TPR = 1 - beta` (Cor 2.5), then beta is the **false-negative** sample rate and its expectation must be `\fnrate` (omega = 1 - tau), not `\tprate` (tau). The symmetry with `alpha` (the false-positive sample rate, `E[alpha] = epsilon`) confirms beta should be the false-negative sample rate. As written, Prop 2.1 sets `E[beta] = tau`, which would make `1 - beta` have expectation `1 - tau = omega`, i.e. the false-negative rate, contradicting the label "true positive rate" in Cor 2.5.
- **Impact**: Cosmetic to the results. beta appears only in these two lines; every theorem is stated directly in tau and epsilon, so no formula inherits the error. But it is a real internal contradiction that a careful reader will catch.
- **Suggestion**: Change Prop 2.1 to `$\Expect{\beta} = \fnrate$` (recommended; makes beta the false-negative analogue of alpha and keeps Cor 2.5 correct). Alternatively, if beta is intended as the true-positive sample rate, change Cor 2.5 to `$\TPR_p = \beta_p$`. The first option is the conventional one.

### MINOR-2 (logic exposition): Independence asserted for Youden's J without restating its basis

- **Location**: sec 3, "by the independence of $\mathrm{TPR}_\p$ and $\alpha_n$".
- **Problem**: The independence of TPR_p (a function of the positive population) and alpha_n (a function of the negative population) is correct and follows from element-wise independence across the disjoint positive and negative sets, but the text invokes it without a one-clause justification. The same disjoint-population independence underlies the zero covariance in the PPV proof (where it *is* justified). 
- **Impact**: Very minor; the claim is true.
- **Suggestion**: Add a half-sentence: "since TPR_p depends only on the p positives and alpha_n only on the n negatives, which are disjoint and independent by Axiom 2.1."

### SUGGESTION-1: State the delta-method singularity is benign in the validated regime

- The PPV ratio t/(t+f) is undefined at t=f=0 (no positive predictions). In the paper's validation regime (positive Bernoulli set, omega=0, so TP = p = 100 deterministically), the denominator is never zero, which I confirmed (P(den=0) = 0). For generality it would be worth one sentence noting the approximation requires P(TP+FP=0) negligible, which holds when p tau or n epsilon is moderately large (the same condition already stated for delta-method validity).

## Cross-checks performed
- Recomputed E[PPV], E[F1] from the stated gradients/Hessians symbolically and numerically: identical to the paper's eqs.
- Confirmed the appendix restatement variances (sigma_t^2 = p omega tau, sigma_f^2 = n epsilon eta) equal the main-text forms (1-tau) t-bar and (1-eps) f-bar and the proof-body forms p tau (1-tau), n eps (1-eps). All three notations are consistent.
