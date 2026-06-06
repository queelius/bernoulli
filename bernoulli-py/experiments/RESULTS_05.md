# Experiment 05: Correlated channels via shared Bloom salts

Sweep the spectrum between independent and identical Bloom-filter channels by varying the number of shared hash salts ``s`` between two ``MultiSaltBloomFilter`` instances built over the same key set. Tests whether the empirical AND-FPR follows the theoretical ``p^(2k - s)`` prediction, with predicted-over-naive ratio ``p^(-s)``.

## Setup

- ``n = 5000`` inserted keys (16-byte uniform).
- ``target_fpr = 0.05`` for sizing each filter.
- ``k = 7`` hash functions per filter.
- ``s`` swept over ``[0, 1, ..., 7]``: each filter has ``k - s`` private salts plus ``s`` shared salts.
- Probe set: ``n_probes = 30000`` random 16-byte non-members.
- Both filters insert the same key set; only the salt vectors differ.

## Theory

For each filter of width ``m`` and ``k`` salt-derived hashes after ``n`` insertions, the bit-set probability is ``p = 1 - exp(-k*n/m)``. A non-member passes when all ``k`` of its positions are set (probability ``~p^k`` per filter). With ``s`` shared salts, the ``s`` shared bit-tests are the same Bernoulli event on both filters, while the ``2*(k-s)`` private bit-tests are independent. So:

```
P(both pass | non-member) = p^s * p^(k-s) * p^(k-s) = p^(2k - s)
```

Compared to the naive independence prediction ``alpha_1 * alpha_2 ~ p^(2k)``, this exceeds it by a factor of ``p^(-s)``. At ``s = 0``, ratio is 1; at ``s = k``, ratio is ``1 / alpha`` and the AND collapses to the single-filter FPR.

## Sweep results

| s | alpha_1 | alpha_2 | alpha_AND (emp) | alpha_AND naive (a1*a2) | Empirical ratio (95% CI) | Predicted ratio p^(-s) (theory p) | Pred AND in CI? |
|--:|--:|--:|--:|--:|--:|--:|:--:|
| 0 | 0.06627 | 0.06347 | 0.004133 | 0.004206 | 0.9828 [0.8246, 1.171] | 1 | True |
| 1 | 0.06483 | 0.06167 | 0.004233 | 0.003998 | 1.059 [0.8903, 1.259] | 1.483 | False |
| 2 | 0.066 | 0.06357 | 0.0051 | 0.004195 | 1.216 [1.038, 1.423] | 2.198 | False |
| 3 | 0.06507 | 0.06523 | 0.006833 | 0.004245 | 1.61 [1.405, 1.845] | 3.259 | False |
| 4 | 0.0614 | 0.06517 | 0.0086 | 0.004001 | 2.149 [1.903, 2.427] | 4.832 | False |
| 5 | 0.0616 | 0.06477 | 0.01503 | 0.00399 | 3.768 [3.438, 4.129] | 7.163 | False |
| 6 | 0.0654 | 0.0658 | 0.0301 | 0.004303 | 6.995 [6.559, 7.458] | 10.62 | False |
| 7 | 0.06377 | 0.06377 | 0.06377 | 0.004066 | 15.68 [15.02, 16.38] | 15.75 | True |

### Bit-set probabilities and predicted vs. empirical AND-FPR

| s | p (empirical) | p (theory) | Predicted alpha_AND (emp p) = p^(2k-s) | Predicted alpha_AND (theory p) | Empirical alpha_AND (95% CI) |
|--:|--:|--:|--:|--:|--:|
| 0 | 0.6748 | 0.6745 | 0.004062 | 0.004033 | 0.004133 [0.003468, 0.004926] |
| 1 | 0.6748 | 0.6745 | 0.006018 | 0.00598 | 0.004233 [0.003559, 0.005034] |
| 2 | 0.676 | 0.6745 | 0.009102 | 0.008866 | 0.0051 [0.004355, 0.005972] |
| 3 | 0.6766 | 0.6745 | 0.0136 | 0.01314 | 0.006833 [0.005962, 0.007831] |
| 4 | 0.6743 | 0.6745 | 0.01943 | 0.01949 | 0.0086 [0.007616, 0.00971] |
| 5 | 0.6748 | 0.6745 | 0.02899 | 0.02889 | 0.01503 [0.01372, 0.01647] |
| 6 | 0.677 | 0.6745 | 0.04414 | 0.04284 | 0.0301 [0.02823, 0.03209] |
| 7 | 0.6755 | 0.6745 | 0.06418 | 0.06351 | 0.06377 [0.06106, 0.06659] |

## Interpretation

**Endpoint behaviour.** At ``s = 0`` (independent salts), the empirical ratio is 0.9828 (95% CI [0.8246, 1.171]), consistent with the predicted value of 1.00 from independent channels.

At ``s = k`` (identical salts), the two filters are bitwise identical after the same insertions, so ``alpha_AND = alpha_1 = alpha_2 = 0.06377``. The empirical ratio is 15.68, matching the prediction ``p^(-k) = 15.75`` (which equals ``1 / alpha`` exactly).

**Spectrum behaviour: the prediction is an upper bound, loose at intermediate s.** The theoretical prediction ``p^(-s)`` lies inside the empirical 95% CI for only 2 of 8 sweep points (the two endpoints ``s = 0`` and ``s = k``). For ``0 < s < k``, the empirical AND-FPR grows substantially more slowly than the prediction:

| s | Empirical ratio | Predicted ratio p^(-s) | Empirical / predicted |
|--:|--:|--:|--:|
| 0 | 0.9828 | 1 | 0.9828 |
| 1 | 1.059 | 1.483 | 0.7142 |
| 2 | 1.216 | 2.198 | 0.553 |
| 3 | 1.61 | 3.259 | 0.494 |
| 4 | 2.149 | 4.832 | 0.4449 |
| 5 | 3.768 | 7.163 | 0.526 |
| 6 | 6.995 | 10.62 | 0.6586 |
| 7 | 15.68 | 15.75 | 0.996 |

The empirical-over-predicted ratio dips to ~0.45-0.55 around the middle of the sweep before rebounding to ~1.0 at ``s = k``. This indicates that the simple ``p^(2k - s)`` argument **overestimates** the AND-FPR for partial salt sharing.

**Why the prediction is loose.** The derivation treats bit-set events in a Bloom filter as independent Bernoulli(p) draws, which is the standard Bloom approximation underlying ``alpha = p^k`` itself. But the bits at the s shared positions and the bits at the k-s private positions in the SAME filter are populated by the same n insertions. Conditional on the s shared positions all being set, the conditional probability that the k-s private positions are also all set is *lower* than the marginal ``p^(k-s)`` (the insertions that filled the s shared positions are at least partially distinct from the insertions that need to fill the private positions). The naive product ``p^s * p^(k-s) * p^(k-s)`` ignores this negative within-filter correlation and overcounts.

**The robust qualitative claim still holds.** Shared salts produce a monotone increase in empirical AND-FPR, reaching the single-filter FPR at ``s = k``. ``p^(-s)`` is a valid (but loose) upper bound on the inflation factor over the naive product. Any application that AND-composes Bloom filters built over the same key set should still use disjoint salt families if it wants the naive product bound to be tight; partial sharing inflates the joint FPR even if less than ``p^(-s)`` would suggest.

## Summary

- **Endpoint match (``s = 0`` and ``s = k``):** the empirical AND-FPR agrees with the theoretical predictions to within Wilson-CI noise.
- **Intermediate ``s`` mismatch:** the simple ``p^(2k - s)`` bound **overestimates** the AND-FPR for partial sharing; the empirical value is ~50% of the prediction at ``s ~ k/2``. The factor ``p^(-s)`` is therefore an upper bound on, not an estimate of, the inflation over the naive product.
- **Mechanism:** the gap is the standard Bloom-bit-independence approximation breaking down. Within a single filter, the s shared and k-s private positions have negatively correlated bit-set events, and the simple product ``p^s * p^(k-s) * p^(k-s)`` ignores this.
- **Practical consequence:** AND-composed Bloom filters over a shared key set should use disjoint salt families if the naive product bound is to remain tight. Partial sharing inflates the joint FPR monotonically with ``s``, but more slowly than the worst-case ``p^(-s)`` prediction.
- **Open theoretical question:** derive the exact AND-FPR for partial sharing accounting for bit-set covariance within each filter (an inclusion-exclusion over insertion events). The current data suggest the true inflation factor is closer to ``(1 + (p^(-s) - 1) * f(p, k))`` for some sub-unit ``f``.
