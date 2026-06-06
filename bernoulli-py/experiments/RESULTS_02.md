# Experiment 02: Adversarial Miller-Rabin

Per-composite empirical FPR of k-round Miller-Rabin on adversarial composites, compared against the worst-case `(1/4)^k` bound. Replicates and extends Experiment 01 Section D, which found the bound is loose by many orders of magnitude on random composites.

**Setup.** For each composite class and each k in [1, 2, 3, 5, 8, 10, 15, 20], every composite is tested with M=2000 independent k-round Miller-Rabin trials, each using k fresh uniformly-random bases in `[2, n-2]`. The empirical FPR per composite is `(# trials all k bases pass) / M`.

## Per-class summary

Each row is a (class, k) cell. `mean FPR` averages the empirical FPR across composites in the class; `max FPR` is the worst composite's FPR for that k. `ratio = empirical / (1/4)^k` measures how close the empirical comes to the worst-case bound (ratio=1 means the bound is tight).

### Carmichael numbers (< 10^6) (n=43 composites, M=2000 trials each)

| k | (1/4)^k | mean FPR | max FPR | mean ratio | max ratio |
|--:|--:|--:|--:|--:|--:|
| 1 | 0.25 | 0.04602 | 0.2145 | 0.1841 | 0.858 |
| 2 | 0.0625 | 0.004058 | 0.0375 | 0.06493 | 0.6 |
| 3 | 0.01562 | 0.0005698 | 0.0075 | 0.03647 | 0.48 |
| 5 | 0.0009766 | 1.163e-05 | 0.0005 | 0.01191 | 0.512 |
| 8 | 1.526e-05 | 0 | 0 | 0 | 0 |
| 10 | 9.537e-07 | 0 | 0 | 0 | 0 |
| 15 | 9.313e-10 | 0 | 0 | 0 | 0 |
| 20 | 9.095e-13 | 0 | 0 | 0 | 0 |

### Strong pseudoprimes to base 2 (< 10^6) (n=46 composites, M=2000 trials each)

| k | (1/4)^k | mean FPR | max FPR | mean ratio | max ratio |
|--:|--:|--:|--:|--:|--:|
| 1 | 0.25 | 0.06352 | 0.199 | 0.2541 | 0.796 |
| 2 | 0.0625 | 0.007098 | 0.0385 | 0.1136 | 0.616 |
| 3 | 0.01562 | 0.0009565 | 0.009 | 0.06122 | 0.576 |
| 5 | 0.0009766 | 1.087e-05 | 0.0005 | 0.01113 | 0.512 |
| 8 | 1.526e-05 | 0 | 0 | 0 | 0 |
| 10 | 9.537e-07 | 0 | 0 | 0 | 0 |
| 15 | 9.313e-10 | 0 | 0 | 0 | 0 |
| 20 | 9.095e-13 | 0 | 0 | 0 | 0 |

### Multi-base strong pseudoprimes (psp to first 3-7 primes) (n=5 composites, M=2000 trials each)

| k | (1/4)^k | mean FPR | max FPR | mean ratio | max ratio |
|--:|--:|--:|--:|--:|--:|
| 1 | 0.25 | 0.1973 | 0.2685 | 0.7892 | 1.074 |
| 2 | 0.0625 | 0.0407 | 0.0675 | 0.6512 | 1.08 |
| 3 | 0.01562 | 0.0094 | 0.0175 | 0.6016 | 1.12 |
| 5 | 0.0009766 | 0.0007 | 0.0015 | 0.7168 | 1.536 |
| 8 | 1.526e-05 | 0 | 0 | 0 | 0 |
| 10 | 9.537e-07 | 0 | 0 | 0 | 0 |
| 15 | 9.313e-10 | 0 | 0 | 0 | 0 |
| 20 | 9.095e-13 | 0 | 0 | 0 | 0 |

### Random odd composites (control, 10^4 to 10^6) (n=100 composites, M=2000 trials each)

| k | (1/4)^k | mean FPR | max FPR | mean ratio | max ratio |
|--:|--:|--:|--:|--:|--:|
| 1 | 0.25 | 0.000375 | 0.0185 | 0.0015 | 0.074 |
| 2 | 0.0625 | 1.5e-05 | 0.0015 | 0.00024 | 0.024 |
| 3 | 0.01562 | 0 | 0 | 0 | 0 |
| 5 | 0.0009766 | 0 | 0 | 0 | 0 |
| 8 | 1.526e-05 | 0 | 0 | 0 | 0 |
| 10 | 9.537e-07 | 0 | 0 | 0 | 0 |
| 15 | 9.313e-10 | 0 | 0 | 0 | 0 |
| 20 | 9.095e-13 | 0 | 0 | 0 | 0 |

## Notable composites: empirical FPR vs k

Per-composite curves for individual numbers of interest. The right-most column is the ratio of the empirical FPR at the largest k to `(1/4)^k`.

| n | description | k=1 | k=2 | k=3 | k=5 | k=8 | k=10 | k=15 | k=20 | ratio at max k |
|---|---|---|---|---|---|---|---|---|---|---|
| 561 | smallest Carmichael (3 x 11 x 17) | 0.0135 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1105 | Carmichael (5 x 13 x 17) | 0.0285 | 0.0005 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1729 | Hardy-Ramanujan / Carmichael (7 x 13 x 19) | 0.0995 | 0.0085 | 0.0005 | 0 | 0 | 0 | 0 | 0 | 0 |
| 8911 | Carmichael (7 x 19 x 67) | 0.208 | 0.035 | 0.006 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2047 | smallest psp(2) (23 x 89) | 0.106 | 0.013 | 0.0005 | 0 | 0 | 0 | 0 | 0 | 0 |
| 25326001 | smallest psp({2, 3, 5}) | 0.101 | 0.0115 | 0.002 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3215031751 | smallest psp({2, 3, 5, 7}) | 0.24 | 0.0615 | 0.016 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2152302898747 | smallest psp({2, 3, 5, 7, 11}) | 0.2635 | 0.062 | 0.0185 | 0.0005 | 0.0005 | 0 | 0 | 0 | 0 |
| 3474749660383 | smallest psp({2, 3, 5, 7, 11, 13}) | 0.239 | 0.0605 | 0.0175 | 0.0005 | 0 | 0 | 0 | 0 | 0 |
| 341550071728321 | smallest psp({2, 3, 5, 7, 11, 13, 17}) | 0.125 | 0.0165 | 0.002 | 0 | 0 | 0 | 0 | 0 | 0 |

## Interpretation

**Resolution caveat.** With M=2000 trials per (n, k) cell, the smallest measurable nonzero empirical FPR is `1/M = 5e-4`. Any true rate below that produces an expected count of zero false positives, so an empirical FPR of 0 at large k tells us only that the true rate is small enough that Wilson's upper CI is on the order of `~1/M`. The cells where the empirical decays cleanly (small k, the multi-base class) are the ones with statistical resolution; cells reading 0 at k >= 8 are at the floor.

**Where the bound is wildly loose.** Random odd composites in `[10^4, 10^6]` have empirical FPR of order `1e-4` at k=1 and indistinguishable from zero at k >= 3, exactly replicating Experiment 01 Section D. Most random composites are caught by a single random base, so the AND chain short-circuits long before the worst-case bound matters.

**Where the bound is moderately loose.** Carmichael numbers have mean per-round FPR around 5%, with the worst Carmichael under `10^6` reaching ~21% (close to the 1/4 bound). For the average Carmichael, the bound overstates the true rate by an order of magnitude per round; for the worst, by a factor of about 1.2x. Base-2 strong pseudoprimes show similar mean behavior with a broader tail.

**Where the bound is genuinely tight.** Multi-base strong pseudoprimes -- composites adversarially constructed to pass Miller-Rabin for the first several primes -- have per-round empirical FPRs in the 0.13 to 0.26 range. `2152302898747` (psp({2,3,5,7,11})) and `3474749660383` (psp({2,3,5,7,11,13})) essentially saturate the 1/4 bound. For these inputs the k-round FPR really does decay as `(1/4)^k` to within statistical noise, which is the regime the Pomerance-Selfridge-Wagstaff bound was designed to be sharp on.

**At what k does the bound become predictively useful?** For an adversary choosing the worst-case input, the bound is sharp at every k. For the Carmichael class, the bound's mean ratio drops from 0.18 at k=1 to ~0.04 at k=3, so by k >= 3 the framework's predicted FPR is roughly 25x larger than the average actual FPR; but the maximum-over-class ratio stays around 0.5 even at k=3, meaning the bound is still within 2x of the worst observed Carmichael. The bound becomes 'essentially tight' (max ratio close to 1) only on multi-base adversarial inputs.

**Implications for the framework.** The Bernoulli framework tags Miller-Rabin's combined output as `one_sided_fpr(value, fpr=(1/4)^k)`. That label is correct as a **worst-case-over-inputs** channel rate. For random or natural-distribution inputs the realised FPR is many orders of magnitude smaller. A distribution-aware refinement would expose two rates: a worst-case `fpr` (the current `(1/4)^k`) and a typical-case `fpr_typical` parameterised by the input distribution -- effectively `0` for uniform-random-odd-composite priors, `(1/4)^k` for adversarial priors. The tradeoff is that claims using `fpr_typical` need an explicit input-distribution assumption, which the worst-case form avoids.

## Summary

- The `(1/4)^k` Miller-Rabin bound is **loose by many orders of magnitude** for random odd composites.
- It is **moderately loose on average, near-tight in the tail** for Carmichael numbers and base-2 strong pseudoprimes (worst Carmichael under 10^6 has per-round FPR ~21%, within 1.2x of the 1/4 bound).
- It is **essentially tight** for composites adversarially constructed to pass several small primes simultaneously: `2152302898747` (psp to {2,3,5,7,11}) and `3474749660383` (psp to {2,3,5,7,11,13}) achieve per-round FPRs of 0.25-0.26.
- The framework's labeling of Miller-Rabin as `fpr=(1/4)^k` is a worst-case channel rate, not a typical-case one. A distribution-aware variant of `BernoulliBool` would let users trade adversarial robustness for tighter predicted FPRs when an input prior is available.

_Elapsed: 13.7s_
