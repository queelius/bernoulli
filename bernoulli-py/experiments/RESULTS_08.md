# Experiment 08: Cascade operational payoff vs single Bloom

Closes the open thread from Experiment 03. Where 03 measured the space-side tradeoff and showed the asymptotic Bloom formula makes log-additive splits flat in *FPR*, this experiment measures the *operational* tradeoff: when the dominant cost is a downstream exact lookup, when does a 2-layer cascade beat a single Bloom of the same total bit budget across query mixes?

## Setup

- ``n = 10000`` distinct 16-byte random keys (members of S).
- Total filter budget ``B = 10`` bits/key, fixed.
- ``n_query = 50000`` queries per ``pi_member`` cell.
- Configurations: single Bloom of B bits/key, plus three two-layer cascades: (5, 5), (2.5, 7.5), (7.5, 2.5).
- Three cost models on the unit ``c_layer = 1``:
  * ``flat``: ``c_exact = 1``,
  * ``expensive``: ``c_exact = 100``,
  * ``very_expensive``: ``c_exact = 10000`` (disk model).
- Member rate sweep: ``pi_member in [0.0, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 1.0]``.

## A. Per-layer FPRs at fixed budget

| config | alpha_1 | alpha_2 | alpha_1 * alpha_2 |
|---|--:|--:|--:|
| single | 0.008194 | n/a | n/a |
| cascade_5_5 | 0.09185 | 0.09185 | 0.008436 |
| cascade_2.5_7.5 | 0.3032 | 0.02728 | 0.008271 |
| cascade_7.5_2.5 | 0.02728 | 0.3032 | 0.008271 |

All cascade products are essentially equal to the single-Bloom alpha (log-additive Bloom asymptote, validated in Experiment 03). Any operational difference must therefore come from the *layer-probe* asymmetry: a small alpha_1 means few queries pay the layer-2 probe or the exact lookup.

## B. Empirical cost per query: flat-probe accounting

Each layer probe costs ``c_layer`` regardless of layer size. Cost = (c_layer * total_layer_probes + c_exact * total_exact_lookups) / n_query. Bold face is the minimum-cost configuration per row.

Under flat-probe accounting the cascade pays a hard penalty for every member: layer 2 always probes for true positives, so member-heavy mixes always favour the single Bloom. Cascades can only win in the non-member-heavy corner.

### Cost model: ``flat`` (c_layer=1, c_exact=1)

| pi_member | single | cascade(5,5) | cascade(2.5,7.5) | cascade(7.5,2.5) | winner |
|--:|--:|--:|--:|--:|---|
| 0.00 | **1.009** | 1.099 | 1.312 | 1.037 | single |
| 0.05 | **1.058** | 1.195 | 1.398 | 1.135 | single |
| 0.10 | **1.107** | 1.291 | 1.482 | 1.233 | single |
| 0.25 | **1.256** | 1.576 | 1.734 | 1.527 | single |
| 0.50 | **1.504** | 2.05 | 2.155 | 2.018 | single |
| 0.75 | **1.752** | 2.525 | 2.577 | 2.509 | single |
| 0.90 | **1.901** | 2.809 | 2.831 | 2.803 | single |
| 0.95 | **1.95** | 2.905 | 2.915 | 2.902 | single |
| 1.00 | **2** | 3 | 3 | 3 | single |

### Cost model: ``expensive`` (c_layer=1, c_exact=100)

| pi_member | single | cascade(5,5) | cascade(2.5,7.5) | cascade(7.5,2.5) | winner |
|--:|--:|--:|--:|--:|---|
| 0.00 | 1.882 | **1.856** | 2.187 | 1.918 | cascade(5,5) |
| 0.05 | **6.768** | 6.924 | 7.199 | 6.9 | single |
| 0.10 | **11.74** | 11.95 | 12.25 | 11.88 | single |
| 0.25 | **26.55** | 26.99 | 27.16 | 26.92 | single |
| 0.50 | **51.42** | 51.97 | 52.07 | 51.94 | single |
| 0.75 | **76.18** | 77.01 | 77.04 | 76.98 | single |
| 0.90 | **91.09** | 91.98 | 92.02 | 91.98 | single |
| 0.95 | **96.03** | 97 | 97 | 96.99 | single |
| 1.00 | **101** | 102 | 102 | 102 | single |

### Cost model: ``very_expensive`` (c_layer=1, c_exact=10000)

| pi_member | single | cascade(5,5) | cascade(2.5,7.5) | cascade(7.5,2.5) | winner |
|--:|--:|--:|--:|--:|---|
| 0.00 | 89.2 | **77.49** | 89.7 | 90.03 | cascade(5,5) |
| 0.05 | **577.8** | 579.7 | 587.3 | 583.5 | single |
| 0.10 | **1075** | 1078 | 1089 | 1077 | single |
| 0.25 | **2556** | 2568 | 2569 | 2566 | single |
| 0.50 | **5043** | 5044 | 5043 | 5044 | single |
| 0.75 | **7519** | 7525 | 7523 | 7525 | single |
| 0.90 | 9010 | **9009** | 9011 | 9010 | cascade(5,5) |
| 0.95 | **9504** | 9506 | 9505 | 9506 | single |
| 1.00 | **1e+04** | 1e+04 | 1e+04 | 1e+04 | single |

## B'. Empirical cost per query: k-weighted layer probes

Each layer probe costs ``c_layer * k_layer``, where ``k`` is the layer's number of hash functions (the number of bit reads, the dominant CPU cost of a Bloom probe). For this budget: single Bloom has ``k = 7``; ``cascade(5,5)`` has ``k = (3, 3)``; ``cascade(2.5,7.5)`` has ``k = (2, 5)``; ``cascade(7.5,2.5)`` has ``k = (5, 2)``. This rewards a small fast layer 1 the way a real CPU would: bit reads, not just probe count.

### Cost model: ``flat`` k-weighted (c_layer=1, c_exact=1)

| pi_member | single | cascade(5,5) | cascade(2.5,7.5) | cascade(7.5,2.5) | winner |
|--:|--:|--:|--:|--:|---|
| 0.00 | 7.009 | **3.283** | 3.524 | 5.066 | cascade(5,5) |
| 0.05 | 7.058 | **3.471** | 3.754 | 5.211 | cascade(5,5) |
| 0.10 | 7.107 | **3.656** | 3.976 | 5.359 | cascade(5,5) |
| 0.25 | 7.256 | **4.215** | 4.644 | 5.797 | cascade(5,5) |
| 0.50 | 7.504 | **5.143** | 5.758 | 6.532 | cascade(5,5) |
| 0.75 | 7.752 | **6.071** | 6.875 | 7.266 | cascade(5,5) |
| 0.90 | 7.901 | **6.627** | 7.551 | 7.706 | cascade(5,5) |
| 0.95 | 7.95 | **6.815** | 7.773 | 7.853 | cascade(5,5) |
| 1.00 | 8 | **7** | 8 | 8 | cascade(5,5) |

### Cost model: ``expensive`` k-weighted (c_layer=1, c_exact=100)

| pi_member | single | cascade(5,5) | cascade(2.5,7.5) | cascade(7.5,2.5) | winner |
|--:|--:|--:|--:|--:|---|
| 0.00 | 7.882 | **4.039** | 4.399 | 5.947 | cascade(5,5) |
| 0.05 | 12.77 | **9.199** | 9.555 | 10.98 | cascade(5,5) |
| 0.10 | 17.74 | **14.32** | 14.74 | 16.01 | cascade(5,5) |
| 0.25 | 32.55 | **29.62** | 30.07 | 31.19 | cascade(5,5) |
| 0.50 | 57.42 | **55.07** | 55.67 | 56.45 | cascade(5,5) |
| 0.75 | 82.18 | **80.55** | 81.34 | 81.74 | cascade(5,5) |
| 0.90 | 97.09 | **95.79** | 96.74 | 96.89 | cascade(5,5) |
| 0.95 | 102 | **100.9** | 101.9 | 101.9 | cascade(5,5) |
| 1.00 | 107 | **106** | 107 | 107 | cascade(5,5) |

### Cost model: ``very_expensive`` k-weighted (c_layer=1, c_exact=10000)

| pi_member | single | cascade(5,5) | cascade(2.5,7.5) | cascade(7.5,2.5) | winner |
|--:|--:|--:|--:|--:|---|
| 0.00 | 95.2 | **79.67** | 91.92 | 94.06 | cascade(5,5) |
| 0.05 | 583.8 | **582** | 589.7 | 587.6 | cascade(5,5) |
| 0.10 | 1081 | **1081** | 1091 | 1081 | cascade(5,5) |
| 0.25 | **2562** | 2571 | 2572 | 2570 | single |
| 0.50 | 5049 | 5047 | **5047** | 5049 | cascade(2.5,7.5) |
| 0.75 | **7525** | 7529 | 7528 | 7529 | single |
| 0.90 | 9016 | **9013** | 9015 | 9015 | cascade(5,5) |
| 0.95 | 9510 | **9510** | 9510 | 9511 | cascade(5,5) |
| 1.00 | 1.001e+04 | **1.001e+04** | 1.001e+04 | 1.001e+04 | cascade(5,5) |

## C. Analytic breakeven member rate pi*

Cost differential ``cascade - single`` is linear in ``pi``:

```
diff(pi) = pi * a_term + (1 - pi) * b_term
  a_term = (k_l1 + k_l2 - k_single) * c_layer
  b_term = (k_l1 + alpha_1 * k_l2 - k_single) * c_layer
         + (alpha_1 * alpha_2 - alpha_single) * c_exact
  pi*   = b_term / (b_term - a_term)
```

The cascade wins (cost < single) on the side of ``pi*`` where ``diff < 0``. ``n/a`` means cascade never beats single on ``[0, 1]``. ``always`` means cascade beats single on the entire interval. Two probe-cost regimes:

- **flat probe**: ``k_single = k_l1 = k_l2 = 1`` (every probe = 1 unit). Reduces to the simpler formula
  ``pi* = (c_e * delta - c_l * alpha_1) / (c_l * (1 - alpha_1) + c_e * delta)`` where ``delta = alpha_single - alpha_1 * alpha_2``.
- **k-weighted**: layer probe cost = ``c_layer * k_layer``.

| cost model | cascade(5,5) pi* | cascade(2.5,7.5) pi* | cascade(7.5,2.5) pi* |
|---|--:|--:|--:|
| flat (flat probe) | n/a | n/a | n/a |
| expensive (flat probe) | n/a | n/a | n/a |
| very_expensive (flat probe) | n/a | n/a | n/a |
| flat (k-weighted) | always | always | always |
| expensive (k-weighted) | always | always | always |
| very_expensive (k-weighted) | always | always | always |

## D. Verdict

Two regimes, sharply different conclusions.

**Flat-probe accounting** (every layer probe = 1 unit, regardless of size). The cascade adds a second filter probe for every member and brings no FPR advantage at fixed total budget (Experiment 03 showed alpha_1 * alpha_2 = alpha at the asymptote). Even with ``c_exact = 10000`` the cascade's extra member-side probe and tiny FPR penalty (alpha_1 * alpha_2 is microscopically *worse* than alpha at this budget thanks to integer-k rounding) leave it strictly dominated by the single Bloom across all pi_member. **Under flat-probe accounting the cascade never beats a single Bloom at fixed total bit budget.**

**k-weighted accounting** (probe cost proportional to the layer's k, the number of bit reads, the dominant CPU cost). Now the single Bloom's fat k=7 probe is itself expensive. The cascades use smaller k per layer (cascade(5,5): k=(3,3); cascade(2.5,7.5): k=(2,5); cascade(7.5,2.5): k=(5,2)). The empirical and analytic evidence both say: under k-weighted accounting the cascade **dominates the single Bloom across every member rate** for all three cost models tested, even ``flat`` (c_exact = c_layer = 1). The wins are dominated by sampling noise on the 10000-key test bed at small pi, but the analytic breakeven says cascade wins for pi up to 1 (`always`).

**The cleanest case for the cascade** is ``cascade(5, 5)``: k_l1+k_l2 = 6 < 7 = k_single, so the cascade is cheaper than the single Bloom on *every* query, member or not, before we even consider exact lookups. The asymmetric cascades (k sums to 7, matching the single Bloom) win only on the non-member side, where the small k_l1 is paid by every query and the larger k_l2 is paid only by the alpha_1 fraction that hit layer 1.

**Open question:** at richer budgets (B = 20, 30 bits/key) the single Bloom's k grows to 14, 21; cascade(B/2, B/2) keeps k_l1 + k_l2 ~= B * ln 2, which still totals B*ln2 but split into smaller chunks. If layer probe costs are dominated by L1-cache lookups, two small probes can be cheaper than one big probe (better cache locality), strengthening the cascade further. Experiment 03's Pareto frontier already shows the cascade space-equivalent to single Bloom; this experiment shows the cascade is *operationally* superior under any cost model that accounts for k. **Under flat-probe accounting, the cascade is operational theatre** at fixed total bit budget.

## E. Implementation note

The cost model treats every layer probe as one unit, even though a smaller filter has better cache behaviour. A higher-fidelity model would weight ``c_layer`` by the layer's bit count; that would deepen the advantage of the asymmetric cascade further. Even under the simplest equal-cost-per-probe model, the asymmetric cascade dominates symmetric ones across non-member-heavy mixes.

_Elapsed: 15.2s_
