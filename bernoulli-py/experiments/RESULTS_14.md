# Experiment 14: Coincidence-oracle closed form

**Goal.** Derive and validate the closed-form accuracy for the coincidence-oracle attacker in a t-instance, shared-``f`` cipher-map deployment. The coincidence oracle is the simplest possible attacker: predict ``k in S`` iff all t observed outputs are equal. It gives a clean theoretical lower bound on the Bayes-optimal attacker's accuracy, and extends the empirical observation in experiment 12 to a closed form parameterized by the codec's codespace.

## Closed form

Under the codec_controlled cipher-map retrieval variant (non-member outputs are i.i.d. draws from ``q_codec(v) = 2^(-l_v)``, with ``sum_v q_v <= 1``):

* For ``k in S``: all t outputs equal ``f(k)`` deterministically (canonical encoding).
* For ``k not in S``: outputs are i.i.d. ~ ``q_codec``.

Coincidence event ``C`` = 'all t outputs equal'. Then:

* ``P(C | k in S) = 1``.
* ``P(C | k not in S) = sum_v q_v^t``.

The coincidence-oracle attacker predicts ``k in S`` iff ``C``. At balanced prior ``pi = 1/2``, accuracy is

    accuracy(t, q_codec) = pi * P(C | S) + (1 - pi) * (1 - P(C | not S))
                         = 1/2 * 1 + 1/2 * (1 - sum_v q_v^t)
                         = 1 - (sum_v q_v^t) / 2.

**Asymptotic decay.** ``sum_v q_v^t`` is dominated by ``(max_v q_v)^t``. So accuracy approaches 1 - ``(max_v q_v)^t / 2`` exponentially in ``t``. The *base* of the decay is ``max_v q_v``.

**Setup.** ``|S| = 2000`` keys, ``|V| = 8`` values, n_test_per_class = 5000, seed = 2026, elapsed = 10.2s.

## Headline table: predicted vs empirical

| codec | t | max q_v | sum q_v^t | predicted acc | empirical acc | 95% CI | in CI? | empirical joint TV | Le Cam UB |
|---|--:|--:|--:|--:|--:|---|:-:|--:|--:|
| Dense(M=3) | 1 | 0.125 | 1 | 0.5 | 0.5 | [0.4902, 0.5098] | yes | 0.3602 | 0.6801 |
| Dense(M=3) | 2 | 0.125 | 0.125 | 0.9375 | 0.9348 | [0.9298, 0.9395] | yes | 0.8696 | 0.9348 |
| Dense(M=3) | 3 | 0.125 | 0.01562 | 0.9922 | 0.9932 | [0.9914, 0.9946] | yes | 0.9864 | 0.9932 |
| Dense(M=3) | 4 | 0.125 | 0.001953 | 0.999 | 0.999 | [0.9982, 0.9995] | yes | 0.998 | 0.999 |
| Dense(M=3) | 5 | 0.125 | 0.0002441 | 0.9999 | 0.9998 | [0.9993, 0.9999] | yes | 0.9996 | 0.9998 |
| Dense(M=4) | 1 | 0.5625 | 1 | 0.5 | 0.5 | [0.4902, 0.5098] | yes | 0.2162 | 0.6081 |
| Dense(M=4) | 2 | 0.5625 | 0.3438 | 0.8281 | 0.8316 | [0.8241, 0.8388] | yes | 0.6632 | 0.8316 |
| Dense(M=4) | 3 | 0.5625 | 0.1797 | 0.9102 | 0.9063 | [0.9004, 0.9119] | yes | 0.8126 | 0.9063 |
| Dense(M=4) | 4 | 0.5625 | 0.1002 | 0.9499 | 0.949 | [0.9445, 0.9531] | yes | 0.898 | 0.949 |
| Dense(M=4) | 5 | 0.5625 | 0.05632 | 0.9718 | 0.9731 | [0.9697, 0.9761] | yes | 0.9462 | 0.9731 |
| Padded(M=4,v0) | 1 | 0.5625 | 1 | 0.5 | 0.5 | [0.4902, 0.5098] | yes | 0.2052 | 0.6026 |
| Padded(M=4,v0) | 2 | 0.5625 | 0.3438 | 0.8281 | 0.8295 | [0.822, 0.8367] | yes | 0.659 | 0.8295 |
| Padded(M=4,v0) | 3 | 0.5625 | 0.1797 | 0.9102 | 0.9083 | [0.9025, 0.9138] | yes | 0.8166 | 0.9083 |
| Padded(M=4,v0) | 4 | 0.5625 | 0.1002 | 0.9499 | 0.9493 | [0.9448, 0.9534] | yes | 0.8986 | 0.9493 |
| Padded(M=4,v0) | 5 | 0.5625 | 0.05632 | 0.9718 | 0.9712 | [0.9677, 0.9743] | yes | 0.9424 | 0.9712 |
| Huffman(M=4,p_f) | 1 | 0.5 | 1 | 0.5 | 0.5 | [0.4902, 0.5098] | yes | 0.1152 | 0.5576 |
| Huffman(M=4,p_f) | 2 | 0.5 | 0.2891 | 0.8555 | 0.8543 | [0.8472, 0.8611] | yes | 0.7086 | 0.8543 |
| Huffman(M=4,p_f) | 3 | 0.5 | 0.1284 | 0.9358 | 0.9341 | [0.9291, 0.9388] | yes | 0.8682 | 0.9341 |
| Huffman(M=4,p_f) | 4 | 0.5 | 0.06284 | 0.9686 | 0.9682 | [0.9646, 0.9715] | yes | 0.9364 | 0.9682 |
| Huffman(M=4,p_f) | 5 | 0.5 | 0.03129 | 0.9844 | 0.9835 | [0.9808, 0.9858] | yes | 0.967 | 0.9835 |
| AntiHuffman(M=4) | 1 | 0.25 | 1 | 0.5 | 0.5 | [0.4902, 0.5098] | yes | 0.575 | 0.7875 |
| AntiHuffman(M=4) | 2 | 0.25 | 0.1719 | 0.9141 | 0.912 | [0.9063, 0.9174] | yes | 0.8802 | 0.9401 |
| AntiHuffman(M=4) | 3 | 0.25 | 0.03613 | 0.9819 | 0.9852 | [0.9826, 0.9874] | NO | 0.9704 | 0.9852 |
| AntiHuffman(M=4) | 4 | 0.25 | 0.008362 | 0.9958 | 0.9958 | [0.9943, 0.9969] | yes | 0.9916 | 0.9958 |
| AntiHuffman(M=4) | 5 | 0.25 | 0.002018 | 0.999 | 0.9989 | [0.998, 0.9994] | yes | 0.9978 | 0.9989 |

## Findings

### Closed-form vs empirical

Across all (5 codecs) x (5 values of t) = 25 configurations, the closed-form predicted accuracy lies inside the empirical Wilson 95% CI for **24 / 25** cells.

The closed form ``acc(t, q_codec) = 1 - sum_v q_v^t / 2`` is exact under the codec_controlled retrieval variant, and matches empirical accuracy up to sampling noise.

### Coincidence oracle vs Bayes-optimal (Le Cam) bound

The coincidence oracle gives a closed-form *lower bound* on the Bayes-optimal attacker's accuracy. Le Cam's ``1/2 + joint_TV/2`` is the *upper bound*. The gap ``Le_Cam_UB - coincidence`` measures how much extra signal is left on the table.

| codec | t | coincidence acc | Le Cam UB | gap |
|---|--:|--:|--:|--:|
| Dense(M=3) | 1 | 0.5 | 0.6801 | 0.1801 |
| Dense(M=3) | 2 | 0.9375 | 0.9348 | -0.0027 |
| Dense(M=3) | 3 | 0.9922 | 0.9932 | 0.001012 |
| Dense(M=3) | 4 | 0.999 | 0.999 | -2.344e-05 |
| Dense(M=3) | 5 | 0.9999 | 0.9998 | -7.793e-05 |
| Dense(M=4) | 1 | 0.5 | 0.6081 | 0.1081 |
| Dense(M=4) | 2 | 0.8281 | 0.8316 | 0.003475 |
| Dense(M=4) | 3 | 0.9102 | 0.9063 | -0.003856 |
| Dense(M=4) | 4 | 0.9499 | 0.949 | -0.0008901 |
| Dense(M=4) | 5 | 0.9718 | 0.9731 | 0.00126 |
| Padded(M=4,v0) | 1 | 0.5 | 0.6026 | 0.1026 |
| Padded(M=4,v0) | 2 | 0.8281 | 0.8295 | 0.001375 |
| Padded(M=4,v0) | 3 | 0.9102 | 0.9083 | -0.001856 |
| Padded(M=4,v0) | 4 | 0.9499 | 0.9493 | -0.0005901 |
| Padded(M=4,v0) | 5 | 0.9718 | 0.9712 | -0.0006399 |
| Huffman(M=4,p_f) | 1 | 0.5 | 0.5576 | 0.0576 |
| Huffman(M=4,p_f) | 2 | 0.8555 | 0.8543 | -0.001169 |
| Huffman(M=4,p_f) | 3 | 0.9358 | 0.9341 | -0.001691 |
| Huffman(M=4,p_f) | 4 | 0.9686 | 0.9682 | -0.0003822 |
| Huffman(M=4,p_f) | 5 | 0.9844 | 0.9835 | -0.0008569 |
| AntiHuffman(M=4) | 1 | 0.5 | 0.7875 | 0.2875 |
| AntiHuffman(M=4) | 2 | 0.9141 | 0.9401 | 0.02604 |
| AntiHuffman(M=4) | 3 | 0.9819 | 0.9852 | 0.003266 |
| AntiHuffman(M=4) | 4 | 0.9958 | 0.9958 | -1.909e-05 |
| AntiHuffman(M=4) | 5 | 0.999 | 0.9989 | -9.101e-05 |

For the shared-``f`` regime, the gap is dominated by the coincidence-vs-pattern-distribution difference: the coincidence oracle ignores *which* value the t copies agree on, while a Bayes attacker exploits the conditional distribution of that shared value as well. Still, at large ``t`` the coincidence oracle saturates near 1 and the gap shrinks.

### Geometric argument: max_v q_v dominates at large t

As ``t`` grows, ``sum_v q_v^t`` is asymptotically dominated by the largest term ``(max_v q_v)^t``. Attacker accuracy is ``1 - (sum_v q_v^t) / 2``, so SMALLER ``sum_v q_v^t`` means HIGHER attacker accuracy and WORSE defense. The codec with the LARGEST ``max_v q_v`` (concentrated, Huffman-style) therefore defends BEST against multi-instance attacks; the codec with the SMALLEST ``max_v q_v`` (uniform Dense) defends WORST.

| codec | max q_v | (max q_v)^5 | sum q_v^5 | attacker error rate at t=5 |
|---|--:|--:|--:|--:|
| Dense(M=3) | 0.125 | 3.052e-05 | 0.0002441 | 0.0001221 |
| Dense(M=4) | 0.5625 | 0.05631 | 0.05632 | 0.02816 |
| Padded(M=4,v0) | 0.5625 | 0.05631 | 0.05632 | 0.02816 |
| Huffman(M=4,p_f) | 0.5 | 0.03125 | 0.03129 | 0.01564 |
| AntiHuffman(M=4) | 0.25 | 0.0009766 | 0.002018 | 0.001009 |

**Reading the table.** Higher attacker error rate = better defense. Concentrated codecs (Padded(v0), Dense(M=4), Huffman) have the largest ``sum_v q_v^t`` and therefore the highest attacker error rate. Uniform Dense(M=3) and AntiHuffman both spread the codespace across many values and have very small ``sum_v q_v^t``, giving very low attacker error rate (near-certain inference). The BASE of the exponential decay in the attacker's coincidence probability is ``max_v q_v``; the defender wants this LARGE.

### Defense implications

* **Single-instance regime.** Huffman codecs minimize ``TV(p_f, q_codec)``. Dense (uniform) codecs maximize it. So at ``t=1``, Huffman defends best (lower Le Cam attacker accuracy).
* **Multi-instance regime (``t >= 2``).** The coincidence oracle's accuracy is ``1 - (sum_v q_v^t) / 2``. The codec with the LARGEST ``max_v q_v`` (concentrated, Huffman-style) defends best at large ``t`` by maximizing the non-member coincidence probability. Huffman's ``max_v q_v ~= max_v p_v`` is large precisely because Huffman concentrates on the heavy mode.
* **No tradeoff.** Both single-instance (Le Cam) and multi-instance (coincidence oracle) optima favor Huffman-style concentrated codecs; there is no codec-choice regime change between ``t=1`` and ``t >= 2``. The Dense codec, which seemed superficially attractive because it minimizes ``sum_v q_v^t``, is actually the WORST defense at any ``t >= 2`` (lowest attacker error rate).
* **The deployment-side defense for multi-instance leakage is randomized encoding** (multiplicity ``K(x) > 1`` per Experiment 15), not codec retuning.
* **No codec defeats the coincidence oracle entirely.** As ``t`` grows, every codec's attacker accuracy approaches 1. Defenses are randomized encoding (private-codec threat), correlating non-member outputs across instances (shared seed) so members and non-members share the coincidence statistic, or not redeploying the same ``(S, f)`` pair across multiple ``t`` instances.

**Correction note (2026-05-17, R7 CRIT-1):** An earlier version of this writeup (and the matching docstring in `14_coincidence_oracle.py`) inverted the defender direction, claiming Dense defends best at large ``t``. That was wrong: smaller ``sum_v q_v^t`` means HIGHER attacker accuracy, not lower. The formula and numerical values are correct; only the recommendation was inverted. The cipher-maps paper (`papers/cipher-maps/paper/cipher_maps.tex`) carried the same inversion in its abstract, Corollary 8.x, and §10.6 paragraph until the 2026-05-17 commit fixed all five locations.
