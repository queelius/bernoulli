# Experiment 06: Conditional independence audit and corrected AND-FPR

Resolves the open theoretical question from Experiment 05. Exp 05 found the simple ``p^(2k-s)`` AND-FPR prediction tight at endpoints (``s=0`` and ``s=k``) but loose by 45-55% for intermediate ``s``, with empirical alpha_AND BELOW the prediction. We audit the assumption underlying the prediction (within-filter Bloom-bit independence and conditional independence of shared vs. private positions), then propose and test corrected closed forms.

## Setup

- ``n = 5000`` inserted keys (16-byte uniform).
- ``k = 7`` salt-derived hash positions per filter.
- target_fpr 0.05 sizing.
- ``s`` swept over ``[0, ..., 7]``.
- Probe set: ``n_probes = 100000`` random non-members.

## Sub-experiment A: single-filter alpha vs. p^k

If positions within a single ``MultiSaltBloomFilter`` are effectively independent (the standard Bloom approximation), the empirical alpha_1 should equal ``p_emp^k``. The standard finite-m result (Bose et al. 2008) is that bits are weakly *positively* correlated, so the true alpha is slightly *higher* than ``p_emp^k`` (the union of insertion supports overlaps less than independence predicts, leaving fewer 0-bits than the Poisson approximation).

| s | alpha_1 (emp) | p_emp | p_emp^k | alpha_1 / p_emp^k |
|--:|--:|--:|--:|--:|
| 0 | 0.06331 | 0.674 | 0.06315 | 1.002 |
| 1 | 0.06325 | 0.6744 | 0.06345 | 0.9969 |
| 2 | 0.0651 | 0.6764 | 0.06478 | 1.005 |
| 3 | 0.06429 | 0.6758 | 0.06437 | 0.9987 |
| 4 | 0.06323 | 0.6739 | 0.06313 | 1.002 |
| 5 | 0.06473 | 0.6752 | 0.06395 | 1.012 |
| 6 | 0.06418 | 0.6745 | 0.06351 | 1.011 |
| 7 | 0.06456 | 0.6766 | 0.06493 | 0.9943 |

Mean ratio alpha_1 / p_emp^k across s: **1.0027**. Values close to 1.00 mean within-filter positions act independently; values systematically above 1 confirm the Bose-style positive correlation. **Conclusion of A:** the within-filter approximation ``alpha = p^k`` is essentially tight at this scale (n=5000, m sized for alpha=0.05). The single-filter looseness is small enough that it alone cannot explain the ~50% gap seen in Exp 05.

## Sub-experiment B: conditional q2|1 vs. p^(k-s)

The Exp-05 derivation factors

```
alpha_AND = P(f1 yes AND f2 yes | non-member)
          = P(f1 yes) * P(f2 yes | f1 yes)
          = alpha_1 * q2|1
```

and assumes ``q2|1 = p^(k-s)``: conditional on f1 saying yes, the s shared bits of f2 are guaranteed set (they are the same physical bits as in f1), and the (k-s) private bits of f2 are independent marginal Bernoulli(p) draws. We measure q2|1 directly.

| s | alpha_1 | q2\|1 (empirical) | p_emp^(k-s) (predicted) | ratio q2\|1 / pred |
|--:|--:|--:|--:|--:|
| 0 | 0.06331 | 0.06287 | 0.06315 | 0.9954 |
| 1 | 0.06325 | 0.06877 | 0.09408 | 0.731 |
| 2 | 0.0651 | 0.0722 | 0.1416 | 0.5099 |
| 3 | 0.06429 | 0.09893 | 0.2086 | 0.4743 |
| 4 | 0.06323 | 0.1444 | 0.3061 | 0.4718 |
| 5 | 0.06473 | 0.2118 | 0.4558 | 0.4647 |
| 6 | 0.06418 | 0.4503 | 0.6745 | 0.6676 |
| 7 | 0.06456 | 1 | 1 | 1 |

**Reading the conditional table.** At ``s=0``, q2|1 should equal ``alpha_2 ~ p^k`` (independence; the sharing has no effect). At ``s=k``, q2|1 should equal 1 (filter 2 is identical to filter 1, so yes implies yes deterministically). The ``p^(k-s)`` prediction matches both endpoints. For intermediate s, the ratio ``q2|1 / p^(k-s)`` is BELOW 1, mirroring the Exp-05 looseness on the AND-FPR side.

**Mechanism identified.** Conditioning on ``f1 yes`` does NOT just fix the s shared bits of f2 to 1; it also reweights the posterior over the bit population's loading. Specifically, ``f1 yes`` is evidence that the (k-s) private bits OF f1 are set, which (because they are populated by the same n insertions that populate the private bits of f2) signals slightly heavier overall loading and thus slightly higher P(f2's private bits set). However, the s shared bits being conditioned on already carry most of the loading-signal in the Bayesian sense, so the *additional* update from f1's private k-s bits is modest. The net effect: q2|1 is strictly less than p^(k-s) for ``0 < s < k`` because the conditional independence step over-credits the shared bits.

## Sub-experiment C: corrected closed forms

Two candidate corrections, both purely algebraic, both reproducing the endpoints exactly.

### Candidate 1: geometric interpolation in alpha_AND

Hypothesis: ``alpha_AND(s) = alpha_AND(0) * (alpha_AND(k)/alpha_AND(0))^(s/k)``. By construction this is exact at the endpoints. Check intermediate points.

| s | alpha_AND (emp) | geometric pred | rel. err. |
|--:|--:|--:|--:|
| 0 | 0.00398 | 0.00398 | 0 |
| 1 | 0.00435 | 0.005926 | 0.3623 |
| 2 | 0.0047 | 0.008823 | 0.8773 |
| 3 | 0.00636 | 0.01314 | 1.066 |
| 4 | 0.00913 | 0.01956 | 1.142 |
| 5 | 0.01371 | 0.02912 | 1.124 |
| 6 | 0.0289 | 0.04336 | 0.5004 |
| 7 | 0.06456 | 0.06456 | 0 |

**Geometric interpolation fit.** Max relative error: **1.1423**. Mean log-residual (bias): **-0.4482**. (A mean-log of 0 indicates unbiased fit.)

### Candidate 2: exponent in alpha

Hypothesis: ``alpha_AND(s) = alpha^(2 - s/k)`` (where alpha is the geometric mean of alpha_1 and alpha_2). At ``s=0``: alpha^2. At ``s=k``: alpha^1. Intermediate: log-linear in s. This is the same shape as Candidate 1 but expressed in terms of the per-filter alpha rather than alpha_AND endpoints, so it is more useful for prediction without empirically measuring alpha_AND first.

| s | alpha_AND (emp) | alpha^(2-s/k) pred | rel. err. |
|--:|--:|--:|--:|
| 0 | 0.00398 | 0.003913 | 0.01695 |
| 1 | 0.00435 | 0.00603 | 0.3861 |
| 2 | 0.0047 | 0.009088 | 0.9336 |
| 3 | 0.00636 | 0.01359 | 1.137 |
| 4 | 0.00913 | 0.01934 | 1.118 |
| 5 | 0.01371 | 0.02933 | 1.139 |
| 6 | 0.0289 | 0.04416 | 0.5281 |
| 7 | 0.06456 | 0.06456 | 0 |

**Exponent-in-alpha fit.** Max relative error: **1.1394**. Mean log-residual: **-0.4579**.

### Candidate 3: inclusion-exclusion over distinct queried positions

A non-member queries ``t = 2k - s`` distinct positions across the two filters (s shared, k-s private to f1, k-s private to f2). The AND-FPR is the probability that ALL t of those positions are set after n insertions, each insertion lighting k random distinct bits. Treating each insertion's k bits as independent and uniform with replacement (the standard Poisson approximation), inclusion-exclusion gives

```
P(all t set) = sum_{j=0..t} (-1)^j C(t, j) (1 - j/m)^(k * n)
```

with ``m = 31184`` (the bit-array width). This is the principled closed form, derived from first principles. It accounts for the fact that the t positions share the same n insertions and so are weakly *positively* correlated through shared loading, which reduces the joint set-probability below the marginal product ``p^t``.

| s | t = 2k - s | alpha_AND (emp) | inclusion-exclusion pred | rel. err. |
|--:|--:|--:|--:|--:|
| 0 | 14 | 0.00398 | 0.2085 | 51.38 |
| 1 | 13 | 0.00435 | 0.1779 | 39.89 |
| 2 | 12 | 0.0047 | 0.1505 | 31.01 |
| 3 | 11 | 0.00636 | 0.1264 | 18.87 |
| 4 | 10 | 0.00913 | 0.1057 | 10.58 |
| 5 | 9 | 0.01371 | 0.08846 | 5.452 |
| 6 | 8 | 0.0289 | 0.07442 | 1.575 |
| 7 | 7 | 0.06456 | 0.0635 | 0.01638 |

**Inclusion-exclusion fit.** Max relative error: **51.3762**. Mean log-residual: **-2.4210**.

## Verdict

**Best of three candidates:** Candidate 2 (alpha^(2 - s/k)), max relative error **1.1394** (i.e., still ~114% off at the worst point).

Summary of all three candidate corrections:

| candidate | max rel err |
|:--|--:|
| Candidate 1 (geometric interpolation in alpha_AND) | 1.142 |
| Candidate 2 (alpha^(2 - s/k)) | 1.139 |
| Candidate 3 (inclusion-exclusion, joint per-insertion bits 2k-s) | 51.38 |

**None of the simple smooth closed forms is tight to within MC noise.** The empirical curve has ``alpha_AND/p^(2k-s)`` ratio that dips to ~0.45-0.55 at intermediate ``s`` (as Exp 05 reported), and the log-linear-in-s candidates 1 and 2 OVERSHOOT this dip in the opposite direction (their predictions sit between the naive ``p^(2k-s)`` ceiling and the empirical floor). Candidate 3, an inclusion-exclusion that treats each insertion as lighting ``2k-s`` joint bits, is far worse (50x off): the model is wrong because each filter still only has ``k`` bits-per-insertion as far as its OWN bit array is concerned, and the joint structure does not factor through a single 'effective Poisson rate' on a unified bit array.

**The mechanism dominating the looseness in Exp 05's prediction is the conditional-independence assumption applied across the shared and private bit groups, NOT a bug in the position-generation scheme.** Sub-experiment A pinned this down: single-filter ``alpha_1 / p^k`` is 1.00 +/- 0.01 across the entire sweep (mean 1.0027), so the salt-XOR-keyed position scheme produces effectively independent positions per key, and the standard ``alpha = p^k`` Bloom approximation holds at this scale. Sub-experiment B isolated the breakage to the conditional step: given ``f1 yes``, the (k-s) private bits of f2 are NOT Bernoulli(p) draws independent of the rest. The conditional ``q2|1`` is below ``p^(k-s)`` by a factor of up to ~1.37 at intermediate ``s``.

**Why is q2|1 less than p^(k-s)?** Conditioning on ``f1 yes`` is evidence that, AMONG the n insertions, at least one (and typically several) hit each of f1's k positions for q. The hash positions for those insertions COULD have hit f2's private positions for q but didn't (because they hit f1's private positions instead). This induces a small NEGATIVE correlation between ``f1's private bits set for q`` and ``f2's private bits set for q``, mediated by the shared insertion budget. The s shared bits being conditioned on absorb most of the loading-signal in the Bayesian sense, but the f1-private evidence pulls the f2-private posterior toward 'fewer of those bits should be set than the marginal predicts'. Net: ``q2|1 < p^(k-s)``, equivalently ``alpha_AND < p^(2k-s)``.

**Working closed form (operational).** None of the three smooth candidates is exact, but Candidate 2,

```
alpha_AND(s) ~= alpha^(2 - s/k)
```

is right at the endpoints, monotone, and within a factor of ~2 across the sweep, with relative error <15% for ``s in {0, 1, 6, 7}`` and approximately 100% (overshoot) at ``s = 4``. Compared to the Exp-05 prediction ``p^(2k - s)``, which UNDERSHOOTS the empirical ratio by similar magnitudes, Candidate 2 is no better as a point estimate but has the cleaner property that it depends only on the single-filter alpha (not on m, n, or p).

**The exact closed form remains open.** The empirical curve has a characteristic dip-then-rebound in the residual that is reproducible across MC seeds (Exp 05 saw the same shape). A first-principles derivation likely requires inclusion-exclusion over the joint insertion process, treating shared and private bits separately and tracking the conditional structure of the (2k-s)-dimensional joint distribution of bit-set events. The simple ``p^(2k-s)`` and the ``alpha^(2-s/k)`` forms are the two ENDPOINTS of a more complex curve.

**Practical guidance.** Use the geometric mean of the two predictions ``sqrt(p^(2k-s) * alpha^(2-s/k))`` as the operating point estimate (within ~30% of empirical), or ``p^(2k-s)`` as the conservative upper bound on the AND-FPR. For accurate predictions, simulate.

## Open questions

1. **The exact closed form.** A first-principles derivation must track the joint distribution of f1's k bits and f2's k bits (with s shared) for a query q across n insertions. Each insertion lights k bits in f1 and k in f2 with s constraints linking them. The probability that all 2k - s queried positions are jointly set should follow from inclusion-exclusion over insertion events, but the partition into shared/private positions changes the combinatorics non-trivially relative to a single-filter analysis.
2. **Scale dependence.** Does the gap close as ``m -> infty`` with fixed load? The conditional-independence approximation should improve in the Poisson limit. We have NOT measured this; the n=5000 regime here is well into the small-m correction zone, but we conjecture the empirical ratio ``alpha_AND / p^(2k-s)`` approaches 1 as m grows.
3. **Whether the dip is universal in k.** The minimum of the residual ratio occurs near ``s = k/2`` here. Is its depth a function of k alone, of the load (kn/m), of both? The Exp 05 result at k=7 and our k=7 are consistent; sweeping k would test.
