# Experiment 01: Composition validation
Empirical check that the Bernoulli framework's composition formulas hold for real data structures, and identification of regimes where they break.
## A. Two Bloom filters, same keys, different salts (independent channels)
- alpha_1 (empirical): 0.0481
- alpha_2 (empirical): 0.05063
- Predicted alpha_AND = alpha_1 * alpha_2: 0.002435
- Empirical alpha_AND: 0.0028
- Ratio (empirical / predicted): **1.15**
- n_probes: 30000
Interpretation: independent salts give independent hash channels, so the AND collapses to the product as predicted. A ratio near 1 confirms the framework's independence assumption.
## B. Two Bloom filters, disjoint keys, same salt (data independence)
- alpha_1: 0.0526
- alpha_2: 0.0522
- Predicted alpha_AND: 0.002746
- Empirical alpha_AND: 0.002933
- Ratio: **1.068**
Interpretation: same salt over different data still gives independent outputs on non-member queries. Sanity check.
## C. Two Bloom filters, same keys AND same salt (degenerate)
- alpha (single filter): 0.0523
- Naively predicted alpha_AND = alpha^2: 0.002735
- Empirical alpha_AND: 0.0523
- Ratio (empirical / naive prediction): **19.12**
Interpretation: identical filters share all randomness; the two channels are perfectly correlated. The empirical AND-FPR equals alpha (not alpha^2). This is exactly the failure mode the framework's Axiom 1 (cross-instance independence) flags. The ratio above 1 is the cost of the violated assumption.
## D. Miller-Rabin k-round AND chain on random odd composites
| k | n_composites | Worst-case bound (1/4)^k | Empirical FPR | Ratio |
|--:|--:|--:|--:|--:|
| 1 | 200 | 0.25 | 0 | 0 |
| 2 | 200 | 0.0625 | 0 | 0 |
| 3 | 200 | 0.01562 | 0 | 0 |
| 5 | 200 | 0.0009766 | 0 | 0 |
| 8 | 200 | 1.526e-05 | 0 | 0 |

Interpretation: the per-composite empirical FPR is far below the worst-case `(1/4)^k` bound. For random composites, most fail base-2 or base-3 immediately, so the chain converges to zero FPR much faster than the worst-case suggests. The bound is tight only for adversarially constructed Carmichael-like numbers.
## E. Shared-truth AND of two NoisyClassifiers (prior=0.5 population)
- Predicted FPR (shared-truth ``__and__`` = alpha_1*alpha_2): 0.008
- Empirical FPR estimate: 0.008333 (95% CI [0.007366, 0.009427])
- FPR within CI: **True**
- Predicted FNR (shared-truth = 1 - (1-beta_1)(1-beta_2)): 0.164
- Empirical FNR estimate: 0.1629 (95% CI [0.1588, 0.1672])
- FNR within CI: **True**
Interpretation: both classifiers query the same input (truth is the same property of the same n). The shared-truth formulas are prior-free; FPR collapses to alpha_1*alpha_2 and FNR to the union-of-misses formula.
## F. Independent-truths AND of two NoisyClassifiers (prior=0.5)
- Predicted FPR (and_with_prior, book eq. 3.3): 0.05733
- Empirical FPR estimate: 0.05739 (95% CI [0.05528, 0.05957])
- FPR within CI: **True**
- Predicted FNR: 0.164
- Empirical FNR estimate: 0.1591 (95% CI [0.1533, 0.1651])
- FNR within CI: **True**
- n_pos (true AND = True): 14938, n_neg: 45062
Interpretation: each query draws *two independent* inputs from the Bernoulli(pi) population and AND's the classifier outputs. This is the regime in which the prior-dependent FPR formula applies.

## Summary
- Composition formulas hold cleanly when channels are independent (sections A, B, E, F).
- Section C makes the independence assumption visible by violating it: shared randomness collapses the AND to a single channel.
- Section D shows the gap between worst-case and typical-case behavior of the Miller-Rabin chain on random composites.
- Sections E and F demonstrate that **shared-truth** and **independent-truths** AND give different FPRs from the same input rates. The framework now exposes both: ``b1 & b2`` (shared) and ``b1.and_with_prior(b2, pi)`` (independent).
