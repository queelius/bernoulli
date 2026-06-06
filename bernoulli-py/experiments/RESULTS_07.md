# Experiment 07: Cipher-map membership-inference attack vs codec choice

A cipher-map is a function ``lookup: U -> V`` built from a
build set ``S`` with values ``f: S -> V``. There is no
membership oracle: every key gets some answer. The codec
controls what non-members see. This experiment runs a
Bayes membership-inference attack against two structural
variants and several codecs, measuring how the codec choice
shapes the attacker's leverage.

Setup: ``|S| = 2000`` keys, ``|V| = 8`` values,
train = 5000, test = 5000, base rate ``pi_S = 0.5``,
seed = 2026, elapsed = 11.3s.

## Value distribution `p_f`

| value | p_v |
|---|--:|
| v0 | 0.4286 |
| v1 | 0.1866 |
| v2 | 0.1147 |
| v3 | 0.08121 |
| v4 | 0.06213 |
| v5 | 0.04992 |
| v6 | 0.04149 |
| v7 | 0.03535 |

## Variants

* **slot_collision** (minimal PHF retrieval). Non-members
  get the value at a uniformly chosen used slot. The
  non-member output equals the empirical f-distribution.
* **codec_controlled** (ribbon retrieval). Non-members
  decode a uniform M-bit pattern. The non-member output
  equals the codec's codespace allocation.

## Headline results

| variant | codec | bits | TV(member, nonmember) | attack acc | attack AUC |
|---|---|--:|--:|--:|--:|
| slot_collision | DenseCodec(M=3, uniform 1/8) | 3 | 0.0267 | 0.4974 | 0.504 |
| slot_collision | PaddedCodec(M=4, default=v0, share 9/16) | 4 | 0.0081 | 0.498 | 0.4982 |
| slot_collision | PaddedCodec(M=5, default=v0, share 25/32) | 5 | 0.0163 | 0.5004 | 0.5044 |
| slot_collision | PrefixCodec(M=4, Huffman from p_f) | 4 | 0.0202 | 0.494 | 0.4932 |
| slot_collision | PrefixCodec(M=5, Huffman from p_f) | 5 | 0.0138 | 0.494 | 0.4981 |
| slot_collision | PrefixCodec(M=4, anti-Huffman: short codes for rare values) | 4 | 0.0125 | 0.4984 | 0.4915 |
| codec_controlled | DenseCodec(M=3, uniform 1/8) | 3 | 0.3416 | 0.6806 | 0.7369 |
| codec_controlled | PaddedCodec(M=4, default=v0, share 9/16) | 4 | 0.1912 | 0.5962 | 0.6154 |
| codec_controlled | PaddedCodec(M=5, default=v0, share 25/32) | 5 | 0.3392 | 0.67 | 0.6937 |
| codec_controlled | PrefixCodec(M=4, Huffman from p_f) | 4 | 0.1365 | 0.5742 | 0.5903 |
| codec_controlled | PrefixCodec(M=5, Huffman from p_f) | 5 | 0.1034 | 0.5568 | 0.5674 |
| codec_controlled | PrefixCodec(M=4, anti-Huffman: short codes for rare values) | 4 | 0.5508 | 0.7762 | 0.832 |

## Per-cell observed distributions

### slot_collision / DenseCodec(M=3, uniform 1/8)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.4165 | 0.4342 |
| v1 | 0.1885 | 0.1896 |
| v2 | 0.1265 | 0.1344 |
| v3 | 0.079 | 0.069 |
| v4 | 0.068 | 0.0638 |
| v5 | 0.047 | 0.046 |
| v6 | 0.0385 | 0.032 |
| v7 | 0.036 | 0.031 |

### slot_collision / PaddedCodec(M=4, default=v0, share 9/16)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.4145 | 0.4174 |
| v1 | 0.203 | 0.2056 |
| v2 | 0.115 | 0.1092 |
| v3 | 0.083 | 0.0838 |
| v4 | 0.063 | 0.0632 |
| v5 | 0.0425 | 0.043 |
| v6 | 0.0445 | 0.0456 |
| v7 | 0.0345 | 0.0322 |

### slot_collision / PaddedCodec(M=5, default=v0, share 25/32)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.4285 | 0.4374 |
| v1 | 0.187 | 0.1794 |
| v2 | 0.113 | 0.11 |
| v3 | 0.0695 | 0.0682 |
| v4 | 0.0625 | 0.059 |
| v5 | 0.0455 | 0.0488 |
| v6 | 0.0515 | 0.0506 |
| v7 | 0.0425 | 0.0466 |

### slot_collision / PrefixCodec(M=4, Huffman from p_f)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.431 | 0.4262 |
| v1 | 0.196 | 0.1964 |
| v2 | 0.1225 | 0.1334 |
| v3 | 0.0745 | 0.0668 |
| v4 | 0.046 | 0.0416 |
| v5 | 0.0565 | 0.0608 |
| v6 | 0.0415 | 0.0382 |
| v7 | 0.032 | 0.0366 |

### slot_collision / PrefixCodec(M=5, Huffman from p_f)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.435 | 0.4272 |
| v1 | 0.179 | 0.18 |
| v2 | 0.1115 | 0.1078 |
| v3 | 0.0775 | 0.0752 |
| v4 | 0.0695 | 0.0698 |
| v5 | 0.055 | 0.0582 |
| v6 | 0.0345 | 0.0382 |
| v7 | 0.038 | 0.0436 |

### slot_collision / PrefixCodec(M=4, anti-Huffman: short codes for rare values)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.437 | 0.4436 |
| v1 | 0.184 | 0.1838 |
| v2 | 0.1115 | 0.1136 |
| v3 | 0.0765 | 0.079 |
| v4 | 0.0635 | 0.0588 |
| v5 | 0.0575 | 0.0536 |
| v6 | 0.0355 | 0.0368 |
| v7 | 0.0345 | 0.0308 |

### codec_controlled / DenseCodec(M=3, uniform 1/8)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.4195 | 0.1208 |
| v1 | 0.1785 | 0.1368 |
| v2 | 0.123 | 0.1218 |
| v3 | 0.081 | 0.1298 |
| v4 | 0.078 | 0.1218 |
| v5 | 0.0545 | 0.1198 |
| v6 | 0.036 | 0.1262 |
| v7 | 0.0295 | 0.123 |

### codec_controlled / PaddedCodec(M=4, default=v0, share 9/16)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.428 | 0.5618 |
| v1 | 0.1985 | 0.0706 |
| v2 | 0.1065 | 0.0628 |
| v3 | 0.081 | 0.0614 |
| v4 | 0.06 | 0.0612 |
| v5 | 0.042 | 0.0612 |
| v6 | 0.045 | 0.0632 |
| v7 | 0.039 | 0.0578 |

### codec_controlled / PaddedCodec(M=5, default=v0, share 25/32)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.439 | 0.7782 |
| v1 | 0.1835 | 0.032 |
| v2 | 0.122 | 0.0286 |
| v3 | 0.0735 | 0.0314 |
| v4 | 0.06 | 0.0328 |
| v5 | 0.0485 | 0.0298 |
| v6 | 0.038 | 0.0326 |
| v7 | 0.0355 | 0.0346 |

### codec_controlled / PrefixCodec(M=4, Huffman from p_f)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.44 | 0.501 |
| v1 | 0.187 | 0.122 |
| v2 | 0.119 | 0.0616 |
| v3 | 0.0805 | 0.0664 |
| v4 | 0.056 | 0.0626 |
| v5 | 0.0465 | 0.0632 |
| v6 | 0.038 | 0.0588 |
| v7 | 0.033 | 0.0644 |

### codec_controlled / PrefixCodec(M=5, Huffman from p_f)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.419 | 0.4936 |
| v1 | 0.1935 | 0.1278 |
| v2 | 0.111 | 0.1226 |
| v3 | 0.0825 | 0.067 |
| v4 | 0.071 | 0.0592 |
| v5 | 0.048 | 0.0652 |
| v6 | 0.0415 | 0.032 |
| v7 | 0.0335 | 0.0326 |

### codec_controlled / PrefixCodec(M=4, anti-Huffman: short codes for rare values)

| value | P(y | in_S) | P(y | not in S) |
|---|--:|--:|
| v0 | 0.409 | 0.0622 |
| v1 | 0.1905 | 0.0654 |
| v2 | 0.122 | 0.0672 |
| v3 | 0.0855 | 0.0614 |
| v4 | 0.0625 | 0.1258 |
| v5 | 0.046 | 0.1306 |
| v6 | 0.047 | 0.2512 |
| v7 | 0.0375 | 0.2362 |

## Findings

### slot_collision: leakage is bounded by sample noise

In the slot-collision model, non-members get the value at
a uniformly chosen used slot. Mathematically the non-member
distribution equals the empirical f-distribution, the same
as the member distribution, so the codec is irrelevant: TV
distance and attack AUC across all codecs are at the
sampling-noise floor. Observed: max TV = 0.0267,
max AUC = 0.5044. The attack is essentially random
in this variant, regardless of codec.

### codec_controlled: codec choice is the lever

In the codec-controlled (ribbon retrieval) model, the
non-member distribution is the codec's codespace allocation,
independent of f. The attacker's leverage is exactly the
TV distance between the member-output distribution
(approximately ``p_f``) and the codec's codespace allocation.

* Best (lowest attack AUC): **PrefixCodec(M=5, Huffman from p_f)** with
  AUC = 0.5674 and TV = 0.1034.
* Worst (highest attack AUC): **PrefixCodec(M=4, anti-Huffman: short codes for rare values)** with
  AUC = 0.832 and TV = 0.5508.

The Huffman-from-``p_f`` codecs minimize attack AUC, with
remaining leakage attributable to integer-codeword-length
quantization (the codec cannot match ``p_f`` exactly when
all codewords are integer-bit prefixes). The dense and
anti-Huffman codecs leak much more: their codespace
allocation is far from ``p_f``, so non-member outputs are
easily distinguished from member outputs.

Quantitatively, attack AUC tracks TV distance closely.
This is the cipher-map design rule: pick a codec whose
codespace allocation matches the value distribution that
members see.

### Codec choice and security/space trade-off

The Huffman codec uses fewer expected bits per stored value
than the dense codec at the same alphabet size, *and* leaks
less to the membership-inference attack: the security
improvement is essentially free under codec-controlled
non-member behaviour. The padded codec, in contrast, sits
between dense and Huffman in both axes.

Limitation: this experiment uses the canonical encoding (the
first stored pattern in each value's class). For finer-grained
control of leakage, randomized encoding (``encode_random`` in
the codec) would spread stored patterns within each class; this
is left for future work.
