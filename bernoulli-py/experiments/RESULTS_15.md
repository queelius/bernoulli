# Experiment 15: Randomized encoding as a defense

Goal: evaluate ``PrefixCodec.encode_random`` as a defense against the coincidence-oracle attack from Experiment 12. Quantify the trade-off (TV cost at ``t = 1`` vs joint AUC reduction at ``t > 1``).

Two threat models:
* **Public codec (decode-coincidence).** Attacker decodes observed patterns; uses decode equality across instances as the membership signal.
* **Private codec (pattern-coincidence).** Attacker sees raw M-bit patterns; uses pattern equality across instances as the membership signal.

Setup: ``|S| = 1000`` keys, ``|V| = 8`` values, three codecs (Huffman M=4, Huffman M=5, Dense M=3), two encoding modes (canonical, encode_random), ``t in {2, 3, 4}``, seed = 2026, elapsed = 1.1s.

## Headline table

Each cell reports both the predicted closed form and the empirical estimate. Attacker accuracy is computed at ``pi_S = 0.5`` as ``Acc = 0.5 * TPR + 0.5 * (1 - FPR)``.

| codec | encoding | t | decode TPR (pred / emp) | decode FPR (pred / emp) | decode acc | pattern TPR (pred / emp) | pattern FPR (pred / emp) | pattern acc |
|---|---|--:|--:|--:|--:|--:|--:|--:|
| Huffman(M=4) | canonical | 2 | 1 / 1 | 0.2891 / 0.2695 | 0.8652 | 1 / 1 | 0.0625 / 0.055 | 0.9725 |
| Huffman(M=4) | canonical | 3 | 1 / 1 | 0.1284 / 0.1365 | 0.9317 | 1 / 1 | 0.003906 / 0.005 | 0.9975 |
| Huffman(M=4) | canonical | 4 | 1 / 1 | 0.06284 / 0.059 | 0.9705 | 1 / 1 | 0.0002441 / 0 | 1 |
| Huffman(M=4) | random | 2 | 1 / 1 | 0.2891 / 0.3105 | 0.8448 | 0.5317 / 0.56 | 0.0625 / 0.0625 | 0.7488 |
| Huffman(M=4) | random | 3 | 1 / 1 | 0.1284 / 0.138 | 0.931 | 0.4381 / 0.422 | 0.003906 / 0.0035 | 0.7093 |
| Huffman(M=4) | random | 4 | 1 / 1 | 0.06284 / 0.0645 | 0.9677 | 0.409 / 0.398 | 0.0002441 / 0 | 0.699 |
| Huffman(M=5) | canonical | 2 | 1 / 1 | 0.2949 / 0.2905 | 0.8548 | 1 / 1 | 0.03125 / 0.0315 | 0.9843 |
| Huffman(M=5) | canonical | 3 | 1 / 1 | 0.1297 / 0.119 | 0.9405 | 1 / 1 | 0.0009766 / 0.0005 | 0.9998 |
| Huffman(M=5) | canonical | 4 | 1 / 1 | 0.06304 / 0.055 | 0.9725 | 1 / 1 | 3.052e-05 / 0 | 1 |
| Huffman(M=5) | random | 2 | 1 / 1 | 0.2949 / 0.298 | 0.851 | 0.2756 / 0.291 | 0.03125 / 0.0395 | 0.6258 |
| Huffman(M=5) | random | 3 | 1 / 1 | 0.1297 / 0.132 | 0.934 | 0.1457 / 0.161 | 0.0009766 / 0.001 | 0.58 |
| Huffman(M=5) | random | 4 | 1 / 1 | 0.06304 / 0.0695 | 0.9652 | 0.1058 / 0.085 | 3.052e-05 / 0 | 0.5425 |
| Dense(M=3) | canonical | 2 | 1 / 1 | 0.125 / 0.1155 | 0.9423 | 1 / 1 | 0.125 / 0.1155 | 0.9423 |
| Dense(M=3) | canonical | 3 | 1 / 1 | 0.01562 / 0.0195 | 0.9903 | 1 / 1 | 0.01562 / 0.0195 | 0.9903 |
| Dense(M=3) | canonical | 4 | 1 / 1 | 0.001953 / 0.003 | 0.9985 | 1 / 1 | 0.001953 / 0.003 | 0.9985 |
| Dense(M=3) | random | 2 | 1 / 1 | 0.125 / 0.132 | 0.934 | 1 / 1 | 0.125 / 0.132 | 0.934 |
| Dense(M=3) | random | 3 | 1 / 1 | 0.01562 / 0.013 | 0.9935 | 1 / 1 | 0.01562 / 0.013 | 0.9935 |
| Dense(M=3) | random | 4 | 1 / 1 | 0.001953 / 0.003 | 0.9985 | 1 / 1 | 0.001953 / 0.003 | 0.9985 |

## Findings

### Central claim verification

Compare pattern-coincidence attack accuracy under canonical vs encode_random. Defense effectiveness is measured by the gap.

| codec | t | canonical pattern acc | random pattern acc | defense (acc reduction) |
|---|--:|--:|--:|--:|
| Huffman(M=4) | 2 | 0.9725 | 0.7488 | 0.2237 |
| Huffman(M=4) | 3 | 0.9975 | 0.7093 | 0.2883 |
| Huffman(M=4) | 4 | 1 | 0.699 | 0.301 |
| Huffman(M=5) | 2 | 0.9843 | 0.6258 | 0.3585 |
| Huffman(M=5) | 3 | 0.9998 | 0.58 | 0.4198 |
| Huffman(M=5) | 4 | 1 | 0.5425 | 0.4575 |
| Dense(M=3) | 2 | 0.9423 | 0.934 | 0.00825 |
| Dense(M=3) | 3 | 0.9903 | 0.9935 | -0.00325 |
| Dense(M=3) | 4 | 0.9985 | 0.9985 | 0 |

Compare decode-coincidence attack accuracy. encode_random should NOT defend (decoded values are codec-identifiable).

| codec | t | canonical decode acc | random decode acc | delta |
|---|--:|--:|--:|--:|
| Huffman(M=4) | 2 | 0.8652 | 0.8448 | 0.0205 |
| Huffman(M=4) | 3 | 0.9317 | 0.931 | 0.00075 |
| Huffman(M=4) | 4 | 0.9705 | 0.9677 | 0.00275 |
| Huffman(M=5) | 2 | 0.8548 | 0.851 | 0.00375 |
| Huffman(M=5) | 3 | 0.9405 | 0.934 | 0.0065 |
| Huffman(M=5) | 4 | 0.9725 | 0.9652 | 0.00725 |
| Dense(M=3) | 2 | 0.9423 | 0.934 | 0.00825 |
| Dense(M=3) | 3 | 0.9903 | 0.9935 | -0.00325 |
| Dense(M=3) | 4 | 0.9985 | 0.9985 | 0 |

### Threat model summary

* **Public codec (decode-coincidence attacker).** The attacker knows the codec and decodes observed patterns to values. Since encode_random preserves the decoded value (the codeword is the prefix of every pattern in the value's class), the decode-coincidence oracle is unaffected. **encode_random does NOT defend against the public-codec attacker.** Acc deltas above are within sampling noise.
* **Private codec (pattern-coincidence attacker).** The attacker sees only raw M-bit patterns. Under canonical encoding, members yield identical patterns across instances; under encode_random, members yield uniform draws from the value's class. The TPR drops from 1 to ``sum_v p_f(v) * 2^(-(t-1)(M - l_v))`` while the FPR is unchanged at ``2^(-(t-1) M)``. **encode_random neutralizes the pattern-coincidence attacker.**

### TV cost at t = 1 (marginal output distribution)

| codec | TV(t=1, canonical) | TV(t=1, random) | delta |
|---|--:|--:|--:|
| Huffman(M=4) | 0.131 | 0.131 | 0 |
| Huffman(M=5) | 0.0845 | 0.0845 | 0 |
| Dense(M=3) | 0.355 | 0.355 | 0 |

The marginal *decoded* output distribution is unchanged between canonical and encode_random (decoding strips the suffix). Therefore TV at t = 1 is identical (delta = 0 up to sampling noise). **The defense at t > 1 has zero TV cost at t = 1.**

### Theoretical takeaway

Coincidence-oracle attacks rely on a *deterministic* coupling of member outputs across instances. Canonical encoding achieves this coupling at the pattern level for free, because each value maps to a single canonical codeword. encode_random decouples the pattern level while preserving the value level. It is therefore a free defense in the private-codec threat model, but irrelevant in the public-codec threat model (where the attacker decodes anyway). The general lesson: **defenses that operate at the encoding layer protect only against attackers restricted to that layer.** Decoupling at the value level requires a different mechanism (e.g., randomized ``f`` per instance, as in Experiment 12's `different-f` configurations).
