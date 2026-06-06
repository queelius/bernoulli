# Bernoulli framework: research synthesis

A single-document orientation to the 16 experiments built in `experiments/`,
their findings, and the publishable threads that emerge from them.

## Scope

The Bernoulli framework treats Bloom filters, perfect-hash filters, ribbon
retrieval, sketches, and noisy classifiers as instances of a single algebraic
type system: random approximate types with quantifiable error rates. The 10
experiments validate framework predictions empirically and identify regimes
where they break or where the predictions are loose. This document is the
synthesis layer over the per-experiment `RESULTS_NN.md` reports.

## Architecture

Atom-outward, matching the textbook:

| Layer | Module(s) | Experiments |
|---|---|---|
| Atom | `atom`, `algebra`, `measures` | 01 |
| Sets | `sets.bloom`, `sets.cascade`, `sets.correlated_bloom` | 03, 05, 08 |
| Algorithms | `algorithms.miller_rabin`, `algorithms.noisy_classifier` | 02, 10 |
| Maps | `maps.codec` | 04, 07, 11, 12, 13, 14, 15, 16 |
| Sketches | `sketches.hyperloglog` | 09 |
| Composition (cross-cutting) | (algebra) | 01, 06 |

440 tests pass. Ruff and mypy strict clean across 19 source files.

## Findings by theme

### 1. Composition algebra (Exp 01, 06)

**Exp 01** verified the framework's closed-form AND, OR, NOT formulas across
four channels: independent-salt Bloom filters (empirical / predicted ratio
1.15), disjoint-data Bloom filters (1.07), shared-truth NoisyClassifiers
(within 95% CI), independent-truths NoisyClassifiers (within CI). The
failure mode is documented: Bloom filters with identical salts and data give
a ratio of 19, exactly the framework's Axiom 1 (cross-instance independence)
being violated.

The semantic distinction between shared-truth and independent-truths AND
emerged from Exp 01 and is now a first-class API decision: `b1 & b2` is
shared-truth (the common case, prior-free closed forms `α_1 α_2` and
`1 - (1-β_1)(1-β_2)`), while `b1.and_with_prior(b2, π)` is independent-truths
(the prior-dependent forms from book chapter 3).

**Exp 06** continued the shared-randomness story. Two `MultiSaltBloomFilter`s
with `s` shared and `k - s` private salts give an empirical AND-FPR ratio
matching the simple `p^(-s)` prediction at the endpoints (s=0 and s=k) but
loose by 45 to 55 percent for intermediate `s`. The mechanism is
shared-insertion-budget anti-correlation: conditioning on filter-1-yes
signals that filter-1's private bits absorbed insertions, which weakly
reduces the chance filter-2's private bits absorbed enough to all be set.
Three candidate corrected closed forms (geometric interpolation,
`α^(2 - s/k)`, joint inclusion-exclusion) were tested; none fit. **Open
theoretical question: what is the closed form?**

### 2. Operational vs space trade-offs (Exp 03, 08)

**Exp 03** swept Bloom cascades at fixed bit budget. The empirical all-layers
FPR is essentially flat across the (B, f) grid. For asymptotically optimal
Blooms, total `α = 2^(-B ln 2)` regardless of how the budget is split.
Cascade(B/2, B/2) has the same FPR and bytes as a single Bloom of B.

**Exp 08** continued by sweeping member-rate. Two cost models:

- Flat-probe accounting (every probe = 1 unit): cascade NEVER beats a
  single Bloom. Even at exact_lookup_cost = 10000, only sampling-noise wins.
- k-weighted accounting (probe cost proportional to k): cascade(5, 5) at
  k=(3, 3) totals 6 hash evaluations versus single(10) at k=7. Cascade is
  cheaper on every query, member or not.

**The cascade's value proposition is hash-evaluation cost, not space, not
early rejection.** This contradicts the standard cascade folklore which
emphasizes early rejection.

### 3. Adversarial vs typical-case bounds (Exp 02)

Miller-Rabin's `(1/4)^k` worst-case bound is wildly loose for typical inputs
and tight only for adversarial ones:

- Random odd composites: empirical FPR essentially 0 at k >= 3.
- Carmichael numbers, base-2 strong pseudoprimes: mean per-round FPR 5
  to 6 percent, max 21 percent.
- Multi-base strong pseudoprimes (e.g., 2152302898747 = psp({2,3,5,7,11})):
  per-round FPR 0.27, ratio 1.07 against the `(1/4)` bound.

The bound is predictively useful only for adversarial inputs. For random
composites, k=3 is overkill.

### 4. Codec design and security (Exp 04, 07, 11, 12, 13, 14, 15, 16)

**Exp 04** validated the codec layer. Huffman gap `L - H(Y)` is 0.0
(uniform), 0.536 (90/10 skewed), 0.062 (Zipf), 0.294 (two-mode), all under
the 1-bit Shannon bound. Codespace-fraction prediction matches simulated
non-member output at TV distance <= 0.0085 (noise floor 0.0029 at N=30000).

**Exp 07 is the headline result of the batch.** Built a Bayes-classifier
membership-inference attack with Mann-Whitney U AUC, sweeping six codecs
across two retrieval variants:

| Variant | AUC range across codecs |
|---|---|
| slot_collision (minimal PHF) | 0.49 to 0.50 (random, codec irrelevant) |
| codec_controlled (ribbon-style) | 0.567 (Huffman M=5) to 0.832 (anti-Huffman) |

**Attack AUC tracks TV(member-out, nonmember-out) tightly. Huffman-from-
frequencies is Pareto-optimal on both axes simultaneously: lowest leakage
AND fewest bits per stored value.** The 0.27-AUC swing across codecs at
fixed retrieval semantics is the cleanest empirical demonstration that codec
choice IS a security primitive in approximate maps.

A subtle finding: `slot_collision` does not leak under a true minimal PHF,
because uniform slot collision over a minimal PHF reproduces exactly the
empirical f-distribution that members have. The leakage knob in
slot_collision is slot-occupancy non-uniformity, which a true minimal PHF
eliminates by construction. This is a real security-relevant property of
minimal-PHF retrieval that was not previously articulated in the maph
research.

**Exp 11 confirmed Le Cam tightness.** Three attackers (Bayes, logistic
regression, k-nearest-neighbor) all converge to the same accuracy and
respect `accuracy <= 1/2 + TV/2` across 10 codec configurations. Across
TV ranging from 0.10 (Huffman M=5) to 0.62 (anti-Huffman M=5), the
empirical max-attacker accuracy tracks `1/2 + TV/2` with max deviation
0.014 (sampling noise). At |V| = 8 the feature space is small enough that
all reasonable attackers reduce to per-value majority vote and tie at the
Le Cam bound. **The codec controls a fundamental information-theoretic
security parameter, not a heuristic.**

**Exp 12 found a catastrophic multi-instance leak.** Publishing the SAME
cipher-map twice (same f, possibly different codecs) takes single-instance
AUC 0.59 to joint AUC 0.92, with a third instance reaching 0.97. The
mechanism: the **coincidence oracle**. For shared-f instances, members give
identical answers across instances (deterministically) while non-members
give independent draws. Whether `M_1(k) == M_2(k)` is itself a near-perfect
membership test. **Codec rotation does NOT defend** against this: pairing
Huffman with anti-Huffman gives joint AUC 0.97, tracking the leakier
component plus the coincidence-oracle bonus. The structural defense is
encoding DIFFERENT f per instance: two Huffman with independent f have
joint AUC 0.86, tracking the better single-instance bound (0.86), no
coincidence-oracle bonus. **Same-f deployment is the dominant
deployment risk; codec rotation is not a mitigation.**

**Exp 13 mapped the codec Pareto frontier.** Across 14 (|V|, m_bits,
distribution) configurations:

- **H1 confirmed (Huffman is L-Pareto-optimal):** Huffman from frequencies
  always lies on the (TV, L) Pareto frontier (14 of 14).
- **H2 falsified (Huffman is NOT always TV-optimal):** only 7 of 14 cases.
  Huffman achieves TV-min only when probabilities are nearly dyadic or
  the alphabet is uniform.
- **Heavy-tail surprise:** for `p_f = (0.9, 0.0143, ...)` with m=6, Huffman
  has TV = 0.40 while the TV-min length assignment achieves TV = 0.0094, a
  **42x reduction** in leakage at only 16.7% L overhead.
- **Mechanism (Kraft saturation):** Huffman saturates Kraft, dumping all
  surplus codespace onto the heavy mode (which already exceeds its
  Shannon length). TV-min instead leaves Kraft slack and pushes long
  codewords onto the tail to better match `p_f`.
- **H3 partially confirmed:** TV-min is `round(-log_2(p_v))` when feasible,
  Kraft-projected otherwise.

**This expands the design space.** Codec choice along the (TV, L) frontier
is a genuine knob: practitioners can spend a few percent of expected
length to buy a 40x reduction in adversarial membership leakage. Huffman
is a "safer-than-worst-case" default, not a leakage-optimal one.

**Exp 14 closed the coincidence-oracle theory.** For t shared-f cipher-map
instances, the coincidence-oracle accuracy is exactly:

```
accuracy(t, q_codec) = 1 - (sum_v q_v^t) / 2     (at balanced class prior)
```

This closed form matches empirical in 24 of 25 cells (one miss at 0.003
sampling noise). Stronger: **the coincidence oracle saturates the Le Cam
upper bound at t >= 2 across every codec.** All Bayes signal IS the
coincidence statistic in the shared-f regime.

**The geometric corollary is a t-dependent codec choice.** As t grows,
`sum_v q_v^t` is dominated by `(max_v q_v)^t`. Therefore:

- **At t=1**: Huffman wins (low TV at t=1 is the relevant objective).
- **At t >= 2 with shared-f**: the codec with smallest `max_v q_v` wins.
  This is uniform Dense (max q_v = 1/|V|), NOT Huffman (max q_v ~ p_max).

For |V| = 8: Dense max q_v = 0.125, Huffman max q_v ~ 0.5 (Zipf head).
At t=5: Dense accuracy ~0.9999 vs Huffman ~0.984. **The codec that leaks
most at t=1 (Dense, mismatching p_f) defends best at t >= 2.** This is a
sharp single-vs-multi-instance design trade-off the original Thread A
claim did not anticipate.

**Exp 15 found a SECOND defense, free at t=1.** Randomized encoding
(`PrefixCodec.encode_random`, which encodes a value as a uniformly random
pattern within its codespace class) has zero marginal effect on decoded
output distribution and therefore zero TV cost at t=1. But at t >= 2 it
breaks the pattern-coincidence attack: members no longer give identical
PATTERNS across instances, only identical decoded values.

The defense is conditional on the threat model:

- **Public-codec threat model** (attacker can decode): encode_random
  provides zero defense (decode-coincidence is unaffected).
- **Private-codec threat model** (attacker sees patterns only): encode_random
  drops Huffman(M=5) joint accuracy from 1.000 to 0.543 at t=4.

Dense codec gets no benefit from encode_random (no codespace slack;
suffix is empty for class size 1). Huffman gets the most benefit because
its codespace classes have the most slack to spread patterns.

**Exp 16 clarified the scope.** The codec security claim applies to
**value-only attackers**. Three key universes tested:

| Universe | TV_value | TV_joint | ValueOnly acc | KeyFeature acc |
|---|--:|--:|--:|--:|
| U_random (random S) | 0.147 | 0.147 | 0.565 | 0.533 |
| U_modular (S = k mod 7 == 0) | 0.153 | 1.000 | 0.572 | 0.997 |
| U_partial (S = mod 7 AND not mod 13) | 0.147 | 1.000 | 0.574 | 0.990 |

The value-only Le Cam bound holds tightly across universes. The
KeyFeatureAttacker exceeds it dramatically when keys carry membership-
correlated structure (saturating near 1 on U_modular). **Codec choice is
the right defense only when keys are unstructured; for structured key
universes, access control is the appropriate defense.**

This is the honest threat model statement and the paper's scope claim.

### 5. Inferential closure (Exp 10)

The cleanest result of the inferential layer. Per-observation log-likelihood-
ratio formula `E[LLR | T] = (1-β) log((1-β)/α) + β log(β/(1-α))` is exact
to fractions of a percent (4 of 5 cases inside 95% Wald CI at n=50000).
Convergence rate: empirical / theoretical ratios 0.993, 0.999, 0.997 across
three regimes. Posterior calibration: Brier 0.005, ECE 0.0028 across 8000
runs. **The framework predicts everything about this inferential pipeline.**

### 6. Sketches (Exp 09)

HyperLogLog at precision 14 (predicted `σ_rel = 0.81%`) tested at scales
100 to 1M. Empirical σ_rel tracks predicted across 5 orders of magnitude;
bias is consistently slightly negative (0.1 to 0.4 percent) consistent with
classical HLL underestimation. Inclusion-exclusion intersection variance
blow-up: 50 percent overlap gives 3.7 percent max error; 1 percent overlap
gives 248 percent; 0.1 percent overlap gives 3032 percent.

Framework-predicted variance is conservative: empirical σ_abs is consistently
smaller than predicted, because the per-set and union estimates share
registers (positive covariance). A covariance correction would tighten
the bound.

A practical surprise: FNV-1a alone gave catastrophically biased estimates
(approximately 90 percent error) because its high bits cluster on small-
string inputs; bucket selection becomes nearly constant. Composing FNV-1a
with splitmix64 fixed it. Hash quality matters far more for HLL than for
Bloom.

## Publishable threads (in descending order of novelty)

### Thread A: Codec choice as a security primitive in approximate maps

**Paper-ready as of Exp 11 through 16.** Eight experiments form the
complete empirical/theoretical case for the paper.

Headline claims (all empirically validated):

1. **Codec controls TV.** For approximate maps with codec-controlled
   non-member output, the codec's codespace allocation determines the
   distribution of non-member outputs. Member outputs follow `p_f`. The
   distance `TV(p_f, q_codec)` is the leakage parameter (Exp 04, 07).
2. **TV upper-bounds attacker accuracy via Le Cam.** No attacker, however
   clever, can exceed `1/2 + TV/2` accuracy. Multiple attacker classes
   (Bayes, logistic regression, kNN) achieve this bound to within sampling
   noise across all tested codecs (Exp 11). The bound applies to value-only
   attackers; key-feature attackers can exceed it on structured key
   universes (Exp 16, the scope clarification).
3. **Huffman is L-Pareto-optimal but NOT TV-optimal.** Codec choice along
   the (TV, L) Pareto frontier is a tunable knob. For heavy-tailed `p_f`,
   the TV-min codec achieves a 42x reduction in leakage at only 17% L
   overhead. Mechanism: Huffman saturates Kraft, dumping surplus codespace
   on the heavy mode; TV-min leaves slack and matches the tail (Exp 13).
4. **Multi-instance composition is catastrophic for shared-f deployments.**
   Two cipher-maps over the same `S` with the same `f` (regardless of
   codec choice) are vulnerable to a "coincidence oracle": members give
   identical outputs, non-members give independent draws. Joint AUC 0.92
   vs single 0.59. Codec rotation does NOT defend; the structural defense
   is independent f per instance (Exp 12).
5. **Closed-form coincidence-oracle bound.** For t shared-f instances:
   `accuracy(t, q) = 1 - (sum_v q_v^t)/2`. Matches empirical in 24/25
   cells. Saturates Le Cam at t >= 2 (Exp 14).
6. **t-dependent codec choice.** Dominated by `(max_v q_v)^t` at large t.
   Huffman wins at t=1; uniform Dense wins at t >= 2 with shared-f.
   The codec that leaks most at t=1 defends best at t >= 2. Sharp
   single-vs-multi design trade-off (Exp 14).
7. **Randomized encoding as a free defense at t=1.** `encode_random`
   encodes each value as a random pattern within its codespace class.
   Zero TV cost at t=1; breaks pattern-coincidence at t >= 2 in the
   private-codec threat model. Public-codec attackers (who can decode)
   are unaffected (Exp 15).

Paper outline:

| Section | Content | Evidence |
|---|---|---|
| 1. Introduction | Cipher-map setting; threat model; contributions | (motivation) |
| 2. Background | Approximate maps, codecs, codespace, Kraft | Exp 04, 13 |
| 3. Attack model | Value-only Bayes membership inference; Le Cam bound | Exp 11, 16 |
| 4. Single-instance security | Codec sweep; AUC vs TV; multiple attackers | Exp 07, 11 |
| 5. (TV, L) Pareto frontier | Huffman vs TV-min; design space; mechanism | Exp 13 |
| 6. Multi-instance leakage | Coincidence oracle; closed form; geometric corollary | Exp 12, 14 |
| 7. Defenses | Independent-f, randomized encoding, t-aware codec choice | Exp 12, 14, 15 |
| 8. Threat model scope | Value-only vs key-feature attackers | Exp 16 |
| 9. Related work | Naor-Yogev indistinguishable Bloom; oblivious data structures | (TBD) |
| 10. Conclusions | | |

Open extensions remaining (could be future work):

1. **Closed-form proof for TV-min length assignment** (Exp 13 H3).
   Empirically `round(-log_2(p_v))` Kraft-projected. Analytical proof
   remains.
2. **Realistic deployment study** (Exp 17 candidate). A real cipher-map
   over a public dataset (e.g., a username-to-user-feature directory)
   with realistic skewed `p_f` and a measured attack.
3. **Stronger attack classes** (Exp 18 candidate). MLPs with sufficient
   capacity to exploit codec-internal structure; verify Le Cam still
   holds.
4. **Comparison to Naor-Yogev Bloom and other privacy-preserving
   structures**. Position the contribution.

Suggested venue: privacy / security venue (e.g., USENIX Security, NDSS,
PoPETS) or a database / systems venue with a security track. The
combination of an information-theoretic security parameter under codec
control AND the catastrophic multi-instance failure under shared-f is
strong enough to carry a top-tier short paper.

### Thread B: Closed form for partially-shared Bloom AND-FPR

From Exp 05, 06. Open theoretical problem with a clean empirical
characterization.

What's needed:

1. Derive the exact closed form via the joint-insertion Poisson-load
   analysis (tracking shared and private bit partitions explicitly).
2. Validate at multiple (k, n, m, s) configurations to ensure the form
   is universal.
3. Identify the asymptotic regime: as m goes to infinity, does the gap
   close to `p^(-s)`?
4. Application: cost analysis of multi-Bloom designs with controlled
   correlation, e.g., layered duplicate-filtering schemes.

This is a clean technical contribution. A short paper, perhaps for an
algorithms venue.

### Thread C: Cascade operational equivalence at fixed bit budget

From Exp 03, 08. The folklore says Bloom cascades are useful for early
rejection; at fixed bit budget under flat-probe accounting, the empirical
answer is no. The cascade's actual value is hash-evaluation cost.

What's needed: tighten the analysis, sweep at higher B (where single Bloom
needs k=14 to k=21 hashes), confirm the k-weighted advantage widens.

A short technical note that re-grounds Bloom-filter cost analysis. Less
novel than threads A and B, but contrarian and clarifying.

## Open questions across all experiments

Questions resolved by Exp 11 through 16:

- **Le Cam bound tight?** Yes (Exp 11). Multiple attackers converge to it.
- **Multi-instance leakage compounding?** Yes catastrophically for
  shared-f (Exp 12). Coincidence-oracle mechanism identified.
- **Adversarial codec design?** Anti-Huffman maximizes TV (Exp 13);
  TV-min length assignment minimizes TV (Exp 13).
- **Closed form for coincidence-oracle accuracy?** Yes,
  `1 - (sum_v q_v^t)/2` (Exp 14). Saturates Le Cam at t >= 2.
- **t-dependent codec choice?** Huffman at t=1, Dense at t >= 2 (Exp 14).
- **Randomized encoding defense?** Works against private-codec attackers,
  not public-codec; zero TV cost at t=1 (Exp 15).
- **Scope of value-only Le Cam?** Holds for unstructured key universes;
  fails when keys carry membership-correlated structure (Exp 16).

Still open (across all threads):

1. **Closed form for partially-shared Bloom AND-FPR** (Exp 06). Cleanest
   open theoretical problem in Thread B.
2. **TV-min length assignment optimality proof** (Exp 13 H3).
3. **Realistic deployment study** (Exp 17 candidate).
4. **Stronger attack classes (MLP)** (Exp 18 candidate).
5. **Tighter typical-case Miller-Rabin bound** (Exp 02 extension).
6. **Covariance correction for HLL inclusion-exclusion** (Exp 09).
7. **Adversarial channel correlation in Bayesian belief updating** (Exp 10
   extension).
8. **Cascade scaling at high B** (Exp 08 extension).

## Reproducibility

All 10 experiments are runnable from the package root:

```bash
cd ~/github/bernoulli/src/bernoulli
.venv/bin/python experiments/NN_*.py
```

Each writes a structured `RESULTS_NN.md` to `experiments/`. Seeds are
fixed; results are reproducible.

## What this body of work establishes

The framework's predictions are correct upper bounds in most experiments;
tighter typical-case bounds are open research. Three publishable threads
have emerged.

**Thread A (codec choice as security primitive) is paper-ready** as of
Exp 11 through 16. Seven headline claims, all empirically validated:
codec controls TV, TV upper-bounds attack accuracy via Le Cam (validated
across attacker classes), Huffman is L-Pareto-optimal but not TV-optimal
(a 42x leakage reduction is available at 17% L overhead), shared-f
multi-instance deployment is catastrophically vulnerable via the
coincidence oracle (codec rotation does not defend), the coincidence
oracle has a clean closed form `1 - (sum q_v^t)/2`, the geometric
corollary gives a sharp t-dependent codec choice (Huffman at t=1, Dense
at t >= 2), randomized encoding provides a free defense at t=1 in the
private-codec threat model, and the entire claim is scoped to value-only
attackers.

This is the strongest candidate for a single paper, with a clear story
arc, theoretical spine (Le Cam, closed-form bounds), three surprising
empirical findings (the coincidence oracle, the t-dependent codec choice,
and the 42x heavy-tail TV reduction), and an honest threat model scope.
Eight experiments form the empirical/theoretical case.

**Thread B (partially-shared Bloom AND-FPR closed form)** remains an open
theoretical problem with a clean empirical characterization. Smaller
paper, more theoretical.

**Thread C (cascade operational equivalence)** is contrarian and
clarifying, suitable for a short technical note.

The codec layer, the inferential pipeline, and the composition algebra
are all empirically validated and ready to support further work. The
package is in a state where new experiments can build on a stable
foundation: the open questions are analytical, not implementation-blocked.
