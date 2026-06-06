# Experiment 04: Codec entropy and non-member output
Empirical validation of two claims for `bernoulli.maps.codec`:

1. **Shannon source-coding bound:** Huffman expected length `L`
   satisfies `H(Y) <= L < H(Y) + 1` for the value distribution
   used to build it.
2. **Codec controls the non-member output distribution:** for a
   structure where non-member queries effectively decode a uniform
   M-bit pattern, the probability that a non-member returns `v`
   equals the codec's codespace fraction for `v`.

All cells use N = 30000 uniform M-bit pattern draws per
codec. Seed = 2026. Elapsed: 0.4s.

## Value distributions

### D1: uniform (max entropy)

| value | p_v |
|---|--:|
| v0 | 0.125 |
| v1 | 0.125 |
| v2 | 0.125 |
| v3 | 0.125 |
| v4 | 0.125 |
| v5 | 0.125 |
| v6 | 0.125 |
| v7 | 0.125 |

H(Y) = 3 bits

### D2: heavily skewed (90/10)

| value | p_v |
|---|--:|
| v0 | 0.9 |
| v1 | 0.01429 |
| v2 | 0.01429 |
| v3 | 0.01429 |
| v4 | 0.01429 |
| v5 | 0.01429 |
| v6 | 0.01429 |
| v7 | 0.01429 |

H(Y) = 0.7497 bits

### D3: Zipf s=1.0

| value | p_v |
|---|--:|
| v0 | 0.3679 |
| v1 | 0.184 |
| v2 | 0.1226 |
| v3 | 0.09198 |
| v4 | 0.07359 |
| v5 | 0.06132 |
| v6 | 0.05256 |
| v7 | 0.04599 |

H(Y) = 2.62 bits

### D4: two-mode (40/40, rest spread)

| value | p_v |
|---|--:|
| v0 | 0.4 |
| v1 | 0.4 |
| v2 | 0.03333 |
| v3 | 0.03333 |
| v4 | 0.03333 |
| v5 | 0.03333 |
| v6 | 0.03333 |
| v7 | 0.03333 |

H(Y) = 2.039 bits

## Per-distribution results
Columns: `H(Y)` is the entropy of the value distribution; `L`
is the expected codeword length under the distribution; `L - H`
is the source-coding gap (Huffman: <= 1 bit). `TV` and `KL` are
the total-variation and KL divergences between the codec's
predicted non-member distribution and the simulated one.

### D1: uniform (max entropy)

| codec | M | H(Y) | L | L - H(Y) | TV | KL(sim||pred) |
|---|--:|--:|--:|--:|--:|--:|
| DenseCodec(M=3) | 3 | 3 | 3 | 0 | 0.008467 | 0.0003026 |
| PaddedCodec(M=4, default=mode) | 4 | 3 | 4 | 1 | 0.002967 | 8.13e-05 |
| PrefixCodec(M=4, Huffman) | 4 | 3 | 3 | 0 | 0.0045 | 9.426e-05 |

#### Predicted vs simulated for DenseCodec(M=3)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.125 | 0.1264 | 0.0014 |
| v1 | 0.125 | 0.1264 | 0.001433 |
| v2 | 0.125 | 0.1262 | 0.001233 |
| v3 | 0.125 | 0.1239 | 0.001133 |
| v4 | 0.125 | 0.1216 | 0.003367 |
| v5 | 0.125 | 0.121 | 0.003967 |
| v6 | 0.125 | 0.1293 | 0.0043 |
| v7 | 0.125 | 0.1251 | 0.0001 |

#### Predicted vs simulated for PaddedCodec(M=4, default=mode)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.5625 | 0.5636 | 0.001067 |
| v1 | 0.0625 | 0.06237 | 0.0001333 |
| v2 | 0.0625 | 0.06283 | 0.0003333 |
| v3 | 0.0625 | 0.0605 | 0.002 |
| v4 | 0.0625 | 0.06393 | 0.001433 |
| v5 | 0.0625 | 0.06257 | 6.667e-05 |
| v6 | 0.0625 | 0.06257 | 6.667e-05 |
| v7 | 0.0625 | 0.06167 | 0.0008333 |

#### Predicted vs simulated for PrefixCodec(M=4, Huffman)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.125 | 0.1249 | 0.0001 |
| v1 | 0.125 | 0.1249 | 0.0001333 |
| v2 | 0.125 | 0.1278 | 0.002833 |
| v3 | 0.125 | 0.1234 | 0.001567 |
| v4 | 0.125 | 0.1231 | 0.001933 |
| v5 | 0.125 | 0.1256 | 0.0005667 |
| v6 | 0.125 | 0.1242 | 0.0007667 |
| v7 | 0.125 | 0.1261 | 0.0011 |

### D2: heavily skewed (90/10)

| codec | M | H(Y) | L | L - H(Y) | TV | KL(sim||pred) |
|---|--:|--:|--:|--:|--:|--:|
| DenseCodec(M=3) | 3 | 0.7497 | 3 | 2.25 | 0.0077 | 0.0002236 |
| PaddedCodec(M=4, default=mode) | 4 | 0.7497 | 4 | 3.25 | 0.004833 | 0.0001681 |
| PrefixCodec(M=4, Huffman) | 4 | 0.7497 | 1.286 | 0.536 | 0.004867 | 0.0001699 |

#### Predicted vs simulated for DenseCodec(M=3)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.125 | 0.1218 | 0.003167 |
| v1 | 0.125 | 0.1283 | 0.003333 |
| v2 | 0.125 | 0.1271 | 0.002133 |
| v3 | 0.125 | 0.1235 | 0.0015 |
| v4 | 0.125 | 0.1244 | 0.0006333 |
| v5 | 0.125 | 0.1227 | 0.002333 |
| v6 | 0.125 | 0.1249 | 6.667e-05 |
| v7 | 0.125 | 0.1272 | 0.002233 |

#### Predicted vs simulated for PaddedCodec(M=4, default=mode)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.5625 | 0.5645 | 0.001967 |
| v1 | 0.0625 | 0.06253 | 3.333e-05 |
| v2 | 0.0625 | 0.0624 | 0.0001 |
| v3 | 0.0625 | 0.06533 | 0.002833 |
| v4 | 0.0625 | 0.06123 | 0.001267 |
| v5 | 0.0625 | 0.06147 | 0.001033 |
| v6 | 0.0625 | 0.06077 | 0.001733 |
| v7 | 0.0625 | 0.0618 | 0.0007 |

#### Predicted vs simulated for PrefixCodec(M=4, Huffman)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.5 | 0.4997 | 0.0003 |
| v1 | 0.0625 | 0.06347 | 0.0009667 |
| v2 | 0.0625 | 0.0623 | 0.0002 |
| v3 | 0.0625 | 0.06213 | 0.0003667 |
| v4 | 0.0625 | 0.0643 | 0.0018 |
| v5 | 0.0625 | 0.06073 | 0.001767 |
| v6 | 0.0625 | 0.06027 | 0.002233 |
| v7 | 0.125 | 0.1271 | 0.0021 |

### D3: Zipf s=1.0

| codec | M | H(Y) | L | L - H(Y) | TV | KL(sim||pred) |
|---|--:|--:|--:|--:|--:|--:|
| DenseCodec(M=3) | 3 | 2.62 | 3 | 0.3803 | 0.005533 | 0.0001041 |
| PaddedCodec(M=4, default=mode) | 4 | 2.62 | 4 | 1.38 | 0.005267 | 0.0001352 |
| PrefixCodec(M=4, Huffman) | 4 | 2.62 | 2.682 | 0.06184 | 0.008533 | 0.0003152 |

#### Predicted vs simulated for DenseCodec(M=3)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.125 | 0.1244 | 0.0006 |
| v1 | 0.125 | 0.1268 | 0.0018 |
| v2 | 0.125 | 0.1244 | 0.0006 |
| v3 | 0.125 | 0.1266 | 0.001567 |
| v4 | 0.125 | 0.1235 | 0.0015 |
| v5 | 0.125 | 0.1272 | 0.002167 |
| v6 | 0.125 | 0.123 | 0.002 |
| v7 | 0.125 | 0.1242 | 0.0008333 |

#### Predicted vs simulated for PaddedCodec(M=4, default=mode)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.5625 | 0.5595 | 0.003033 |
| v1 | 0.0625 | 0.0635 | 0.001 |
| v2 | 0.0625 | 0.06413 | 0.001633 |
| v3 | 0.0625 | 0.06313 | 0.0006333 |
| v4 | 0.0625 | 0.06027 | 0.002233 |
| v5 | 0.0625 | 0.06357 | 0.001067 |
| v6 | 0.0625 | 0.06283 | 0.0003333 |
| v7 | 0.0625 | 0.0631 | 0.0006 |

#### Predicted vs simulated for PrefixCodec(M=4, Huffman)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.25 | 0.251 | 0.0009667 |
| v1 | 0.25 | 0.2458 | 0.0042 |
| v2 | 0.125 | 0.1273 | 0.002267 |
| v3 | 0.125 | 0.1221 | 0.0029 |
| v4 | 0.0625 | 0.06367 | 0.001167 |
| v5 | 0.0625 | 0.06313 | 0.0006333 |
| v6 | 0.0625 | 0.06107 | 0.001433 |
| v7 | 0.0625 | 0.066 | 0.0035 |

### D4: two-mode (40/40, rest spread)

| codec | M | H(Y) | L | L - H(Y) | TV | KL(sim||pred) |
|---|--:|--:|--:|--:|--:|--:|
| DenseCodec(M=3) | 3 | 2.039 | 3 | 0.9611 | 0.006967 | 0.0001857 |
| PaddedCodec(M=4, default=mode) | 4 | 2.039 | 4 | 1.961 | 0.004 | 0.0001107 |
| PrefixCodec(M=4, Huffman) | 4 | 2.039 | 2.333 | 0.2944 | 0.0061 | 0.0001669 |

#### Predicted vs simulated for DenseCodec(M=3)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.125 | 0.1263 | 0.0013 |
| v1 | 0.125 | 0.1257 | 0.0006667 |
| v2 | 0.125 | 0.1218 | 0.003167 |
| v3 | 0.125 | 0.1267 | 0.0017 |
| v4 | 0.125 | 0.1267 | 0.001733 |
| v5 | 0.125 | 0.1246 | 0.0004333 |
| v6 | 0.125 | 0.1216 | 0.003367 |
| v7 | 0.125 | 0.1266 | 0.001567 |

#### Predicted vs simulated for PaddedCodec(M=4, default=mode)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.5625 | 0.5619 | 0.0006 |
| v1 | 0.0625 | 0.06423 | 0.001733 |
| v2 | 0.0625 | 0.0639 | 0.0014 |
| v3 | 0.0625 | 0.06123 | 0.001267 |
| v4 | 0.0625 | 0.06203 | 0.0004667 |
| v5 | 0.0625 | 0.0611 | 0.0014 |
| v6 | 0.0625 | 0.06223 | 0.0002667 |
| v7 | 0.0625 | 0.06337 | 0.0008667 |

#### Predicted vs simulated for PrefixCodec(M=4, Huffman)

| value | predicted | simulated | abs error |
|---|--:|--:|--:|
| v0 | 0.25 | 0.2474 | 0.002567 |
| v1 | 0.25 | 0.2497 | 0.0003 |
| v2 | 0.0625 | 0.063 | 0.0005 |
| v3 | 0.0625 | 0.06077 | 0.001733 |
| v4 | 0.0625 | 0.064 | 0.0015 |
| v5 | 0.0625 | 0.061 | 0.0015 |
| v6 | 0.125 | 0.128 | 0.002967 |
| v7 | 0.125 | 0.1261 | 0.001133 |

## Summary findings

### Shannon source-coding bound

Huffman gap `L - H(Y)` per distribution (must be in `[0, 1)` by
Shannon's source-coding theorem):

| distribution | H(Y) | L (Huffman) | gap |
|---|--:|--:|--:|
| D1: uniform (max entropy) | 3 | 3 | 0 |
| D2: heavily skewed (90/10) | 0.7497 | 1.286 | 0.536 |
| D3: Zipf s=1.0 | 2.62 | 2.682 | 0.06184 |
| D4: two-mode (40/40, rest spread) | 2.039 | 2.333 | 0.2944 |

Max observed Huffman gap: 0.536. Within `[0, 1)`: **True**.

Note: the Huffman codeword lengths assigned by `from_frequencies`
are integers, so `L` is always an integer-weighted sum. For the
two-symbol case (D2 reduced to {v0, others}) Huffman gives both
values length 1, matching `L = 1` regardless of how skewed the
distribution is, which is the canonical example of the
Shannon-Huffman gap. Arithmetic / range coding closes that gap
in continuous-message regimes; the codec module here is the
discrete per-value variant.

### Codec controls the non-member distribution

TV distance between predicted (codec codespace) and simulated
(uniform M-bit decode) non-member distributions, per (distribution,
codec) cell:

| distribution | codec | TV | KL |
|---|---|--:|--:|
| D1: uniform (max entropy) | DenseCodec(M=3) | 0.008467 | 0.0003026 |
| D1: uniform (max entropy) | PaddedCodec(M=4, default=mode) | 0.002967 | 8.13e-05 |
| D1: uniform (max entropy) | PrefixCodec(M=4, Huffman) | 0.0045 | 9.426e-05 |
| D2: heavily skewed (90/10) | DenseCodec(M=3) | 0.0077 | 0.0002236 |
| D2: heavily skewed (90/10) | PaddedCodec(M=4, default=mode) | 0.004833 | 0.0001681 |
| D2: heavily skewed (90/10) | PrefixCodec(M=4, Huffman) | 0.004867 | 0.0001699 |
| D3: Zipf s=1.0 | DenseCodec(M=3) | 0.005533 | 0.0001041 |
| D3: Zipf s=1.0 | PaddedCodec(M=4, default=mode) | 0.005267 | 0.0001352 |
| D3: Zipf s=1.0 | PrefixCodec(M=4, Huffman) | 0.008533 | 0.0003152 |
| D4: two-mode (40/40, rest spread) | DenseCodec(M=3) | 0.006967 | 0.0001857 |
| D4: two-mode (40/40, rest spread) | PaddedCodec(M=4, default=mode) | 0.004 | 0.0001107 |
| D4: two-mode (40/40, rest spread) | PrefixCodec(M=4, Huffman) | 0.0061 | 0.0001669 |

Max observed TV distance: 0.008533. Sampling-noise floor
(roughly `1 / (2 * sqrt(N))` for the worst single bin):
0.002887. Sample size N = 30000.

The simulated distribution exactly matches the codec's
codespace allocation up to sampling noise. This is expected by
construction: the simulator draws uniform M-bit patterns and
decodes them, which is exactly the model under which
`codespace_fraction(v)` is the per-value probability. The
interesting empirical question -- whether *ribbon retrieval's*
non-member output matches this simulator -- was answered
affirmatively by the maph project; see the
`docs/CODESPACE_NONMEMBERS.md` reference and Experiment 03 here.

What this experiment establishes for the Python codec is that
the predictive bookkeeping is correct: `codespace_fraction(v)`
is the actual probability of `v` under uniform M-bit decoding.
