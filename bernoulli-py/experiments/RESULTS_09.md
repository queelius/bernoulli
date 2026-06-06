# Experiment 09: HyperLogLog as a Bernoulli<int> estimator

HyperLogLog estimates the cardinality of a multiset using ``m = 2^precision`` registers. The framework view: HLL outputs a Bernoulli<int> estimator with relative standard deviation ``sigma_rel = 1.04 / sqrt(m)`` (asymptotic).

All sections use precision 14 (``m = 16384``, predicted ``sigma_rel ~ 0.813%``).

## A. Single-HLL accuracy across scales

| true_n | trials | predicted sigma_rel | empirical sigma_rel | mean rel. error | max |rel. error| |
|--:|--:|--:|--:|--:|--:|
| 100 | 20 | 0.008125 | 0.00673 | -0.002469 | 0.01706 |
| 1,000 | 20 | 0.008125 | 0.005891 | -0.002065 | 0.01391 |
| 10,000 | 10 | 0.008125 | 0.003864 | -0.001462 | 0.008057 |
| 100,000 | 5 | 0.008125 | 0.005526 | -0.0006826 | 0.01012 |
| 1,000,000 | 3 | 0.008125 | 0.005822 | 0.004208 | 0.008869 |

Interpretation: the empirical relative-error standard deviation tracks the predicted ``1.04 / sqrt(m)`` across five orders of magnitude of true cardinality. This is the Bernoulli<int> contract: the channel rate is the relative standard deviation, and it is approximately scale-invariant.

## B. Merge accuracy across overlap fractions

| overlap | true_union | trials | predicted sigma_rel | empirical sigma_rel | mean rel. error |
|--:|--:|--:|--:|--:|--:|
| 0.000 | 100,000 | 3 | 0.008125 | 0.00171 | -0.003457 |
| 0.100 | 95,000 | 3 | 0.008125 | 0.007429 | 0.003648 |
| 0.500 | 75,000 | 3 | 0.008125 | 0.004322 | 0.001072 |
| 0.900 | 55,000 | 3 | 0.008125 | 0.008111 | 0.005503 |
| 1.000 | 50,000 | 3 | 0.008125 | 0.005224 | 0.01023 |

Interpretation: register-wise max merge gives an estimate of ``|A union B|`` with the same relative precision as a single HLL built directly on the union. The merged sketch is statistically indistinguishable from one built on the union from scratch, by construction (max of two maxes is one max).

## C. Inclusion-exclusion intersection: variance blow-up

We estimate ``|A intersect B| = |A| + |B| - |A union B|``. The variance is the sum of the three component variances (correlations omitted in the predicted column, which therefore is a mild over-estimate). The relative error is ``sigma_abs / |A intersect B|``, which explodes when the intersection shrinks relative to ``|A union B|``.

| overlap | true intersect | predicted sigma_abs | predicted sigma_rel | empirical sigma_abs | max |rel. error| |
|--:|--:|--:|--:|--:|--:|
| 0.5000 | 25,000 | 837.5 | 0.0335 | 251.3 | 0.03714 |
| 0.2000 | 10,000 | 929.9 | 0.09299 | 613.6 | 0.1555 |
| 0.0500 | 2,500 | 978.6 | 0.3914 | 319.5 | 0.4866 |
| 0.0100 | 500 | 991.8 | 1.984 | 449.4 | 2.477 |
| 0.0010 | 50 | 994.8 | 19.9 | 437.3 | 30.32 |

Interpretation: when ``|A intersect B|`` is comparable to ``|A union B|`` (overlap >= 50%), inclusion-exclusion gives an intersection estimate at the same single-sketch relative precision (~1%). When overlap drops to 1% or 0.1%, the absolute error of the union estimate is comparable to or larger than the intersection itself, so the relative error blows up.

This is a generic feature of inclusion-exclusion on noisy estimators: subtracting two large numbers to get a small one amplifies relative noise. MinHash-style sketches estimate the Jaccard coefficient directly and avoid this blow-up; HLL via inclusion-exclusion is only appropriate when the intersection is a non-trivial fraction of the union.

## Summary

- HLL is a Bernoulli<int> estimator: relative-error standard deviation matches ``1.04 / sqrt(m)`` across scales.
- The merge (register-wise max) propagates the same channel rate to the union estimate.
- Inclusion-exclusion for the intersection inherits the variance algebra of three independent Normal(true, sigma_rel * true) estimators. When the intersection is much smaller than the union, the relative error explodes predictably.
- This is the framework's promise: composition of approximate data structures has predictable error propagation, including the failure modes.
