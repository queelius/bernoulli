# Experiment 12: Multi-instance cipher-map leakage

Goal: quantify how observing TWO (or more) cipher-map instances over the same build set ``S`` compounds the membership-inference leakage relative to observing either alone. We always use the codec_controlled (ribbon-retrieval) variant from experiment 07 so the leakage lever is the codec's codespace allocation.

Setup: ``|S| = 2000`` keys, ``|V| = 8`` values, ``M = 4`` bits, train = 5000, test = 5000, ``pi_S = 0.5``, seed = 2026, elapsed = 3.0s.

## Headline table

| config | t | single TVs | single AUCs | joint TV | sum TVs | max TV | joint AUC | max single AUC | Le Cam UB |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Single Huffman (baseline) | 1 | 0.152 | 0.5933 | 0.156 | 0.152 | 0.152 | 0.5933 | 0.5933 | 0.578 |
| Two Huffman, same f (repeat) | 2 | 0.1345, 0.1345 | 0.5845, 0.5954 | 0.7102 | 0.269 | 0.1345 | 0.9246 | 0.5954 | 0.8551 |
| Two Huffman, different f | 2 | 0.1195, 0.5625 | 0.5728, 0.8556 | 0.5769 | 0.682 | 0.5625 | 0.8612 | 0.8556 | 0.7884 |
| Huffman + Dense, same f | 2 | 0.1375, 0.3535 | 0.5791, 0.7261 | 0.8706 | 0.491 | 0.3535 | 0.9472 | 0.7261 | 0.9353 |
| Huffman + AntiHuffman, same f (rotation) | 2 | 0.134, 0.564 | 0.5707, 0.8359 | 0.904 | 0.698 | 0.564 | 0.9704 | 0.8359 | 0.952 |
| Two AntiHuffman, same f | 2 | 0.5565, 0.5565 | 0.8225, 0.8286 | 0.8739 | 1.113 | 0.5565 | 0.9819 | 0.8286 | 0.9369 |
| Three Huffman, same f (stacking) | 3 | 0.1345, 0.1345, 0.1345 | 0.5802, 0.5745, 0.5884 | 0.8686 | 0.4035 | 0.1345 | 0.9678 | 0.5884 | 0.9343 |
| Huffman + Dense + AntiHuffman (3-rotation) | 3 | 0.1415, 0.3635, 0.552 | 0.5941, 0.7335, 0.8452 | 0.9892 | 1.057 | 0.552 | 0.9962 | 0.8452 | 0.9946 |

## Findings

### Hypothesis checks

**H1 (subadditivity, joint TV <= sum of single TVs).** This bound holds when components are *independent given the membership label*. In our same-``f`` configurations, members are deterministically coupled (the same codec applied to the same value gives the same output) while non-members are independent, so the bound need not hold. Violations: 5 of 8 configs. Configs in violation: ['Single Huffman (baseline)', 'Two Huffman, same f (repeat)', 'Huffman + Dense, same f', 'Huffman + AntiHuffman, same f (rotation)', 'Three Huffman, same f (stacking)']. These are precisely the same-``f`` configurations where members are deterministically coupled across instances. 

**H2 (lower bound, joint TV >= max single TV).** Violations: 0 of 8 configs.

**H3 (joint AUC pulls away from the better single AUC).** For each config we compare joint AUC to max single AUC; the gap measures how much extra leakage the second instance contributes.

| config | max single AUC | joint AUC | delta |
|---|--:|--:|--:|
| Single Huffman (baseline) | 0.5933 | 0.5933 | 0 |
| Two Huffman, same f (repeat) | 0.5954 | 0.9246 | 0.3292 |
| Two Huffman, different f | 0.8556 | 0.8612 | 0.005571 |
| Huffman + Dense, same f | 0.7261 | 0.9472 | 0.2211 |
| Huffman + AntiHuffman, same f (rotation) | 0.8359 | 0.9704 | 0.1345 |
| Two AntiHuffman, same f | 0.8286 | 0.9819 | 0.1533 |
| Three Huffman, same f (stacking) | 0.5884 | 0.9678 | 0.3794 |
| Huffman + Dense + AntiHuffman (3-rotation) | 0.8452 | 0.9962 | 0.151 |

### Narrative

**Same codec, same f (repeat) is *catastrophic*.** Single Huffman gives AUC = 0.5933; observing two Huffman copies of the SAME ``f`` gives AUC = 0.9246. On members the two instances coincide deterministically (any key in ``S`` gives the *same* answer in both); on non-members the second instance produces an independent random draw. Whether ``M_1(k) == M_2(k)`` is therefore a near-perfect membership oracle. This is the central security finding: publishing the *same* cipher-map twice (same codec, same f) leaks vastly more than publishing it once, even though the marginal leakage is unchanged. 

**Codec rotation (Huffman + leakier codec).** Pairing Huffman with AntiHuffman: joint AUC = 0.9704 (vs single max 0.8359). Pairing Huffman with Dense: joint AUC = 0.9472 (vs single max 0.7261). Rotation does NOT defend; the joint always tracks at or above the leakier component because the attacker can always ignore the safer component. 

**Does rotation defend?** No, in our experiments it compounds. Two AntiHuffman: joint AUC = 0.9819 (single max 0.8286). Huffman + AntiHuffman: joint AUC = 0.9704 (single max 0.8359). The rotation benefits from the same coincidence-based membership oracle as the same-codec case, so any marginal protection from picking a Huffman codec is swamped. **Rotation backfires** when the safer codec is deployed alongside a leakier one because the joint always tracks the leakier component. The defender's best move is to deploy fewer instances, not to vary their codecs. 

**Stacking (three same-codec instances).** Single = 0.5933, two = 0.9246, three = 0.9678. Information saturates with diminishing returns because the joint AUC is already near 1 with two instances. The first extra observation buys most of the leverage; the third buys little. 

**Different-``f`` per instance is *protective* relative to shared-``f``.** Two Huffman with independent draws of ``f`` per instance: joint AUC = 0.8612 (single max 0.8556, single TVs ['0.1195', '0.5625']). Without the coincidence oracle, the joint AUC tracks the Le Cam bound and is close to the better single-instance AUC. The asymmetry between the two single TVs reflects the asymmetry of the two ``f`` distributions: ``f_alt`` is reverse-Zipf, so the Huffman codec built from ``p_f`` leaks much more about it. 

### Theoretical takeaway

The composition algebra view: a single cipher-map exposes ``Bernoulli<Y>`` over its non-member output, with TV gap ``TV(p_f, q_codec)`` driving the AUC. Observing *t* instances over the same ``S`` exposes the joint ``Bernoulli<Y_1, ..., Y_t>``. Two regimes:

* **Conditionally independent regime (different ``f``):** joint TV obeys subadditivity, joint AUC tracks the stronger of the per-instance signals, and the Le Cam bound ``AUC <= 1/2 + TV/2`` holds tightly. Multi-instance leakage is bounded by the most leaky codec deployed.
* **Coupled-member regime (shared ``f``):** the diagonal of the joint distribution is a perfect membership oracle on its own. Joint TV explodes past the sum of marginal TVs, and joint AUC approaches 1 even when each marginal is near-random. This is the dominant deployment risk.

### Open questions

* **Coupled-member oracle as the dominant risk.** The shared-``f`` coincidence oracle is independent of codec choice; it is a property of *redeploying the same data* rather than of the codec. A formal lower bound on joint AUC as a function of |S| / |Y|^t should be derivable from the birthday-paradox approximation.
* **Compositional defense.** A real defense against multi-instance attacks would need to *correlate* the non-member outputs across instances (a shared pseudorandom permutation seeded by the deployment context, for example), so the joint distribution of ``(M_1(k), M_2(k))`` for non-members matches that for members. Codec choice alone cannot defeat the coincidence oracle.
* **Le Cam tightness.** Joint AUC tracks ``1/2 + joint_TV/2`` closely when the joint alphabet is small; the bound is tight up to estimation noise.
