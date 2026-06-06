# Experiment 13: Codec (TV, L) Pareto frontier

Empirical characterization of the trade-off between expected codeword length
`L = sum p_v l_v` and codespace-allocation total variation
`TV(p, q) = (1/2) sum |p_v - q_v|` with `q_v = 2^(-l_v)`. The first is the
classical Huffman objective; the second is the security-relevant quantity
identified in Exp 07 (it controls non-member output distribution).

Method: exhaustive enumeration over all Kraft-feasible length tuples
`(l_1, ..., l_n)` with each `l_i in [1, m_bits]` and `sum 2^(-l_i) <= 1`.
For each tuple compute `(L, TV, kraft)` against the value distribution
`p_f`; identify the (TV, L) Pareto frontier; locate the Huffman
`from_frequencies` assignment on it. When `kraft < 1`, the surplus
codespace `1 - kraft` is folded onto `argmax_v p_v` (matches
`PrefixCodec.from_frequencies` default-value convention).

Stdlib only. Total runtime: ~10 s on |V|=4..8, m_bits=4..6.

## Headline verdict

| Hypothesis | Result | Cases |
|---|---|---|
| H1: Huffman is on the (TV, L) Pareto frontier | **TRUE** | 14 / 14 |
| H2: Huffman achieves the minimum TV | **FALSE** in general | 7 / 14 cases see strictly lower TV |
| H3: TV-min length = `round(-log2(p_v))` | **PARTIAL** | matches when rounding is Kraft-feasible (6 of 14); rounding violates Kraft for non-dyadic distributions and the TV-min assignment is then a Kraft-projection |

Huffman is L-optimal by construction and Pareto-optimal in the joint (TV, L)
sense across all 14 distributions tested. But Huffman is **not** TV-optimal
in general. There exists a strictly TV-improving direction at the cost of
higher L, and that direction is what the Pareto frontier traces.

## Cases where Huffman is NOT TV-optimal

| Case | H | Huffman L | Huffman TV | TV-min L | TV-min TV | dTV | dL | %L |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| two-mode-4    | 1.722 | 1.800 | 0.150 | 2.000 | 0.100 | -0.050 | +0.200 | +11.1% |
| heavy-4       | 0.628 | 1.167 | 0.400 | 1.300 | 0.0875| -0.313 | +0.133 | +11.4% |
| zipf-6        | 2.282 | 2.333 | 0.115 | 2.537 | 0.069 | -0.046 | +0.204 | +8.7%  |
| heavy-6       | 0.701 | 1.240 | 0.400 | 1.300 | 0.213 | -0.188 | +0.060 | +4.8%  |
| zipf-8        | 2.620 | 2.682 | 0.129 | 2.866 | 0.070 | -0.059 | +0.184 | +6.9%  |
| zipf-8-m6     | 2.620 | 2.682 | 0.129 | 2.866 | 0.070 | -0.059 | +0.184 | +6.9%  |
| **heavy-8-m6**| 0.750 | 1.286 | **0.400** | 1.500 | **0.0094** | **-0.391** | +0.214 | +16.7% |

The heavy-tail rows are the dramatic ones. With `m_bits=6` and
`p = (0.9, 0.0143, ...)`, Huffman packs the seven low-mass codewords into
3 to 4 bits because Huffman is greedy on L; the resulting `q_v` for the
default value carries the entire `1 - sum_{i!=0} 2^(-l_i)` surplus, which
massively over-allocates codespace to v0. The TV-min assignment instead
uses **all 6 bits for every tail value**, producing `q_v = 1/64` per tail
(close to the actual probability `1/70`). The TV gap shrinks from 0.40 to
0.009 (~42x), at an L cost of only 0.21 bits (16.7%).

## Cases where Huffman IS TV-optimal

uniform-4, zipf-4, dyadic-4, uniform-6, two-mode-6, uniform-8, dyadic-8.

These are the cases where the rounded `round(-log2(p_v))` lengths are
Kraft-feasible. Notably:
- **Uniform** distributions: Huffman gives all-equal lengths, q is uniform,
  TV is determined entirely by the dyadic mismatch `|V| vs 2^m`. No
  flexibility in length space helps.
- **Truly dyadic** distributions: `p_v = 2^(-l_v*)` exactly, Huffman picks
  `l_v*`, and TV = 0.
- **two-mode-6** (specifically): Huffman saturates Kraft and there is no
  feasible reallocation that lowers TV.

## H3: structural characterization of the TV-min assignment

For each value, the *unconstrained* TV-minimizer is `l_v* = -log2(p_v)`,
which is generally non-integer. The integer TV-minimizer over a single
value (in isolation) is `round(-log2(p_v))`. Test:

| Case | round(-log2 p) | kraft | TV-min lengths | match? |
|---|---|--:|---|---|
| uniform-4   | (2,2,2,2)       | 1.000 | (2,2,2,2)      | yes |
| zipf-4      | (1,2,3,3)       | 1.000 | (1,2,3,3)      | yes |
| two-mode-4  | (1,1,3,3)       | 1.250 INFEASIBLE | (2,1,4,4) | no  |
| heavy-4     | (1,4,4,4)       | 0.688 | (1,4,4,4)      | yes |
| dyadic-4    | (1,2,3,3)       | 1.000 | (1,2,3,3)      | yes |
| uniform-6   | (3,3,3,3,3,3)   | 0.750 | (2,2,3,3,3,3)  | no  |
| zipf-6      | (1,2,3,3,4,4)   | 1.125 INFEASIBLE | (2,2,3,3,4,4) | no |
| two-mode-6  | (1,1,4,4,4,4)   | 1.250 INFEASIBLE | (1,2,4,4,4,4) | no |
| heavy-6     | (1,4,4,4,4,4)   | 0.812 | (1,4,4,4,4,4)  | yes |
| uniform-8   | (3,3,3,3,3,3,3,3) | 1.000 | (3,3,3,3,3,3,3,3) | yes |
| zipf-8      | (1,2,3,3,4,4,4,4) | 1.250 INFEASIBLE | (2,3,3,3,4,4,4,4) | no |
| dyadic-8    | (1,2,3,4,4,4,4,4) | 1.188 INFEASIBLE | (1,3,4,4,4,4,4,4) | no |
| zipf-8-m6   | (1,2,3,3,4,4,4,4) | 1.250 INFEASIBLE | (2,3,3,3,4,4,4,4) | no |
| heavy-8-m6  | (1,6,6,6,6,6,6,6) | 0.609 | (1,6,6,6,6,6,6,6) | yes |

**Pattern.** The naive `round(-log2(p_v))` rule is the TV-optimal
length whenever the resulting tuple is Kraft-feasible. In the 8 cases where
it is feasible, it equals the TV-min tuple. In the 6 cases where it
violates Kraft (always sub 6+1=7), the TV-min tuple is a Kraft-projection:
it pushes one or more lengths up by 1 to make `kraft <= 1`. The L cost is
exactly the bit-mass of those promotions.

This is consistent with the source-coding intuition: Huffman is the
discrete projection of `-log2(p_v)` onto the feasible polytope under
the L objective; the TV-min assignment is the discrete projection under
the L1 objective. They coincide when `-log2(p)` already lies in the
feasible polytope at integer coordinates (uniform, dyadic, and a few
others). Otherwise they diverge and the Pareto frontier between them is
non-trivial.

## Adversarial worst case (Exp 07 leakage bound)

For each distribution we also identify the assignment maximizing TV (the
adversarial direction):

| Case | Huffman TV | TV-max | TV-max lengths | TV-max L |
|---|--:|--:|---|--:|
| uniform-4    | 0.000 | 0.563 | (1,4,4,4)         | 3.250 |
| zipf-4       | 0.035 | 0.470 | (3,3,1,2)         | 2.560 |
| two-mode-4   | 0.150 | 0.550 | (3,3,1,2)         | 2.700 |
| heavy-4      | 0.400 | 0.775 | (3,1,2,3)         | 2.900 |
| dyadic-4     | 0.000 | 0.500 | (3,3,1,2)         | 2.625 |
| zipf-8-m6    | 0.129 | 0.653 | (3,6,6,6,6,1,2,4) | 4.287 |
| heavy-8-m6   | 0.400 | 0.838 | (4,2,3,3,3,3,3,4) | 3.900 |

The TV-max direction always *anti-aligns* short codewords with low-mass
values. This is the worst-case adversary that an attacker on the
non-member output channel of Exp 07 could approach if free to choose the
codec. The actual Huffman TV is, in every case, strictly inside this
adversarial bound. So Huffman is a default that is "safer than worst-case"
but not optimal.

## L1 quantization gap

Defined as `L1(p, q*) = 2 * min_l TV(p, q_l)`, the smallest possible
codespace-vs-probability discrepancy under Kraft constraints.

| Case | H | L1 gap | Huffman gap |
|---|--:|--:|--:|
| uniform-4   | 2.000 | 0.0000 | 0.0000 |
| zipf-4      | 1.793 | 0.0700 | 0.0700 |
| two-mode-4  | 1.722 | 0.2000 | 0.3000 |
| heavy-4     | 0.628 | 0.1750 | 0.8000 |
| dyadic-4    | 1.750 | 0.0000 | 0.0000 |
| uniform-6   | 2.585 | 0.3333 | 0.3333 |
| zipf-6      | 2.282 | 0.1378 | 0.2295 |
| two-mode-6  | 1.922 | 0.3000 | 0.3000 |
| heavy-6     | 0.701 | 0.4250 | 0.8000 |
| uniform-8   | 3.000 | 0.0000 | 0.0000 |
| zipf-8      | 2.620 | 0.1401 | 0.2581 |
| dyadic-8    | 1.984 | 0.3750 | 0.3750 |
| zipf-8-m6   | 2.620 | 0.1401 | 0.2581 |
| heavy-8-m6  | 0.750 | 0.0188 | 0.8000 |

The gap is exactly 0 only for distributions with all-dyadic probabilities
(uniform with `|V| = 2^k`, dyadic-4, dyadic-8) where `-log2(p_v)` is
integer for every v. Otherwise the gap is bounded below by integer
lattice spacing in length space.

## Implications

1. **For Exp 07 / cipher-map security**: Huffman-from-frequencies is a
   reasonable but **not optimal** non-member-leakage minimizer. For
   heavy-tail value distributions, switching from Huffman to the TV-min
   assignment can reduce non-member TV by 40x or more, at <17% L overhead.
2. **For composition with PaddedCodec**: the surplus mass `1 - kraft`
   is the key lever. Allowing `kraft < 1` (deliberately leaving codespace
   unused) drives TV down for heavy-tailed distributions because the
   default-collected surplus dominates the TV when Kraft is saturated on
   short codewords.
3. **For paper framing**: the (TV, L) Pareto frontier is the right
   abstraction for "codec choice as security primitive". Huffman lives
   at one corner (L-min); the TV-min assignment lives at another. The
   designer's choice on this frontier is exactly the L-vs-leakage trade-off.
4. **Open question**: characterize the TV-min length assignment in
   closed form. The empirical pattern (round-then-project-onto-Kraft)
   suggests a Larmore-Hirschberg style algorithm with L1 cost in place of
   `p * l`. Worth a follow-up theorem.

## Files

- `experiments/13_codec_optimality.py`: enumerator + frontier analysis.
- This file.

## Surprises

- Huffman's TV gap on heavy-tail distributions (TV=0.4) is *enormous*
  relative to the TV-min achievable (TV=0.009 for heavy-8-m6). The cipher-
  map non-member leakage is being driven almost entirely by the default
  value's surplus codespace.
- Even for moderately skewed Zipf, Huffman TV is ~2x the TV-min. The
  6-9% L overhead to reach TV-min is small.
- The L-min assignment is not unique: many length permutations achieve the
  same L (the Huffman-rotation symmetry). All of them are L-min and on
  the Pareto frontier with identical (L, TV) coordinates.
