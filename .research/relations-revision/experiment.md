# Stored-filter query calibration experiment

Date: 2026-10-13. Artifact: `papers/bernoulli_relations/code/filter_calibration.py`.
Results: `papers/bernoulli_relations/data/calibration/`.

## Outcome and scope

This experiment supplies a concrete stored-filter demonstration for the revised
relations paper. It uses immutable partitioned Bloom bit arrays, serialized and
reloaded before all measured queries. Membership does not consult an exact set
or sample a coin. A fixed construction gives the same response on every repeated
lookup. The representation actually stores one canonical key per true symmetry
orbit, or both ordered keys followed by OR repair at query time.

At a nominal query false-positive target of 0.05, canonical per-source sizing at
0.05 gives a 0.32915 observed query FPR on the extremal mixed profile. Sensitivity
calibration gives 0.04907, compared with 0.05103 for calibrated ordered storage
with OR repair. The latter point estimate is slightly above the target; its
construction-level interval includes both the target and its conditional-model
prediction. These are empirical compatibility results, not a finite-sample proof
that the concrete hash implementation has FPR at most 0.05.

The calibrated canonical payload is 3,752 bytes versus 8,482 bytes for ordered
OR repair: a measured 55.8% reduction for this representation and workload.
This establishes an actual serialized-storage benefit at the same ideal-model
query contract, with empirical behavior consistent with that contract. It does
not establish a new filter design, a general optimum, or superiority to modern
compressed-set implementations.

The 55.8% comparison reflects canonicalization and the extra OR-repair source
budget together. It does **not** measure the benefit of independence over a
dependence-robust union bound. Holding canonical representation fixed gives
3,752 versus 3,768 bytes for those two budgets, only a 16-byte (0.425%) sizing
reduction; this separate calculation is detailed below.

## Workload and source identities

Each query bundle has twelve distinct off-diagonal symmetry orbits. Write their
membership bits as `X_0,...,X_11`. Its Boolean lineage is

`F(X) = OR_{i=0}^{11} (X_i AND X_{(i+1) mod 12})`.

An exact witness relation can encode the twelve adjacent pairs of source tuples;
the corresponding fixed positive relational query existentially selects a
witness and tests its two relation atoms. Each source participates in two
witnesses. The witness cycle is a cycle on *source IDs*, not an assertion that
the stored binary relation itself is a twelve-vertex graph cycle. Repeated
occurrences read the same source bit. Reversing a tuple addresses its symmetry
orbit rather than creating a fresh canonical source.

The cycle has `s0 = 12 - ceil(12/3) = 8`. The three exact truth profiles are:

- `all_false`: twelve absent sources.
- `boundary_false`: sources 0, 3, 6, and 9 are true; the other eight are absent.
  This is a smallest maximal independent set of the witness cycle. Any absent
  source flipping to true makes the query true, so this profile attains the
  homogeneous ideal one-sided envelope.
- `true_edge`: sources 0 and 1 are true, the other ten absent. The query is true
  and has zero false negatives by the one-sided Bloom property.

There are 128 disjoint bundles per profile, with no source shared across bundles.
They all query the same constructed filter. The exact relation also contains
2,048 unqueried background orbits. Total true orbits are
`2048 + 128*(4+2) = 2816`, giving 5,632 true ordered tuples. The exact witness
table and input relation are common workload inputs and are excluded from filter
payload accounting.

## Filter construction and conditional guarantee

An ordered key is two unsigned 64-bit integers, encoded with a fixed-width
structured representation. Canonical keys sort the two coordinates. Diagonal
orbits have one orientation; unit tests cover them, although the measured
workload uses only size-two orbits.

Each Bloom filter has `k` disjoint byte-aligned partitions of `m` bits and one
hash position per partition. The implementation uses keyed BLAKE2b with a public
128-bit salt, separate partition and retry domains, and rejection range reduction
from 128 bits. The latter removes modulo bias *under the ideal-hash model*.
This is deliberately separate from the package's existing FNV/double-hash Bloom
implementation; no package implementation or API has been changed.

For `n` distinct inserted keys and desired ordered-key/source rate `a`, initial
sizing chooses `k = ceil(-log2(a))`, then rounds `m` upward to a multiple of eight
so that

`[1 - (1 - 1/m)^n]^k <= a`.

This expression is the exact unconditioned marginal rate for ideal independent
uniform hash functions in disjoint partitions. Initial sizing alone would not
certify every realized occupancy. Therefore construction retries with fresh
salts until the product of occupied fractions satisfies

`p(C) = product_j(occupied_j / m) <= a`.

**Acceptance uses inserted-key hashes only. No absent-key or query answer is
examined to choose a salt.** Construction time includes retries and occupancy
checks; candidate counts are preserved in `builds.csv`.

In the ideal experiment, each candidate uses independent random functions.
Conditioning on all inserted-key hash outputs, including rejected candidates
and the accepted stopping index, leaves every fixed absent key's hash outputs
independent and uniform in the accepted candidate. Thus conditional on this
insertion history, distinct absent keys have independent Bloom responses of
rate `p(C)`. Repeated keys remain the same response. Conditioning more coarsely
on the bit arrays gives the same conditional absent-key response law.

The resulting ideal query envelopes are:

| Method | Source target | Conditional worst false-profile envelope |
|---|---:|---|
| Canonical naïve | `a = 0.05` | `1-(1-p(C))^8` |
| Canonical calibrated | `a = 1-0.95^(1/8) = 0.00639115095` | `1-(1-p(C))^8 <= 0.05` |
| Ordered + OR calibrated | `a = 1-0.95^(1/16) = 0.00320069771` | `1-(1-p(C))^16 <= 0.05` |

For ordered OR repair, an absent size-two orbit has conditional rate
`q(C) = 1-(1-p(C))^2`, and distinct orbits use disjoint absent ordered keys.
Substituting `q(C)` into the cycle contract produces the exponent sixteen.

The homogeneous sensitivity contract is exact at the boundary profile for each
fixed ideal construction. For the all-false profile, a two-state cycle dynamic
program computes the conditional query probability in linear time. It accumulates
disjoint first-witness success probabilities directly, avoiding subtraction of a
near-one no-witness probability. The ordered OR probability uses `expm1/log1p`
for the same reason. The artifact
averages these *conditional* predictions across accepted builds; it does not
substitute a mean rate into a nonlinear formula. Mixing over occupancy can
introduce dependence even in the ideal model.

These guarantees are explicitly conditional on ideal random functions. BLAKE2b
domain separation and the reproducible PRNG are concrete mechanisms, not proofs
of independent random-function behavior. For those mechanisms the report offers
measurements on fixed, nonadversarial keys. It does not certify adversarial or
adaptive workloads or all possible truth profiles of the concrete hash family.

## Run and numerical results

Default run: Python 3.12.3, seed 20261013, 160 independently salted accepted
constructions per method, 128 bundles per profile per build. Each reported
profile therefore has 20,480 measured query evaluations per method. The platform,
configuration, source hash, per-build salt, and payload hash are recorded.

Uncertainty uses the 160 *construction means* as replication units. The reported
interval is the sample mean plus or minus 1.95996 times the sample standard
deviation of construction means divided by `sqrt(160)`, clipped to `[0,1]`.
These are approximate pointwise 95% normal intervals. They do not treat 20,480
same-filter queries as independent trials, and they are not exact confidence
bounds or simultaneous confidence guarantees. All-false calibrated outcomes are
sparse (ten and eight positives respectively), so their normal intervals deserve
particular caution. The zero false-negative claim follows from construction,
not from the degenerate empirical interval for the true profile.

| Method | All-false FPR (approx. 95% CI) | Boundary FPR (approx. 95% CI) | Mean ideal boundary FPR |
|---|---|---|---:|
| Canonical naïve | 0.026465 [0.024263, 0.028667] | 0.329150 [0.322639, 0.335662] | 0.332236 |
| Canonical calibrated | 0.000488 [0.000194, 0.000782] | 0.049072 [0.045940, 0.052204] | 0.048999 |
| Ordered + OR calibrated | 0.000391 [0.000126, 0.000655] | 0.051025 [0.048152, 0.053899] | 0.049193 |

All six nontrivial ideal-model predictions fall inside their corresponding
empirical intervals. This agreement is evidence for this probe, not a proof of
the concrete-hash model assumptions. All true-edge queries return true. Across
all 480 accepted filters there are zero inserted-key false negatives, zero
true-query false negatives, zero repeated-query discrepancies, and zero
reversed-query discrepancies.

| Method | Stored representatives | Partitions × bits/partition | Bit bytes | Header bytes | Payload bytes | Mean attempts | Mean build ms | Boundary query µs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Canonical naïve | 2816 | 5 × 3536 | 2210 | 40 | 2250 | 1.819 | 41.10 | 59.21 |
| Canonical calibrated | 2816 | 8 × 3712 | 3712 | 40 | 3752 | 1.913 | 66.10 | 76.63 |
| Ordered + OR calibrated | 5632 | 9 × 7504 | 8442 | 40 | 8482 | 1.675 | 130.87 | 113.18 |

Maximum attempts were 6, 6, and 8 respectively; total candidate builds were 291,
306, and 268. Maximum admitted ideal envelopes were 0.336577871, 0.049994340,
and 0.049995334. Every calibrated admitted filter therefore satisfied the
occupancy-based ideal certificate. A subsequent exact rational audit, described
below, verifies this claim for the recorded builds independently of rounding.

The header consists of 8 magic/version bytes, two 4-byte dimension fields, an
8-byte inserted-count field, and a 16-byte salt. The 40-byte overhead is charged
equally; Python object overhead and the common query/input tables are excluded.
Representation type is supplied by the caller and is not in the Bloom payload.
The timing order rotates across methods. Build timing includes deduplication,
hashing, occupancy checking, and rejected attempts, but excludes serialization
and validation. Query timing includes key encoding, all source lookups, and
Boolean witness evaluation. Each source is fetched once per query and reused
in both neighboring witnesses. Repeat/reverse validation runs outside timing.
These pure-Python timings are descriptive, not an optimized systems benchmark.

## Isolating the independence budget from representation savings

The main calibrated comparison changes the representation: a canonical filter
stores one key per symmetry orbit; ordered OR repair stores two and budgets for
two absent-key trials. Its 55.8% saving cannot be attributed to using the
independent sensitivity formula instead of the dependence-robust envelope.

To isolate that latter effect, `canonical_budget_sizing()` holds the canonical
representation, its 2,816 inserted representatives, the query target, the
partition sizing rule, and 40-byte header fixed. It uses the same
`bloom_dimensions()` function as actual construction, without building or timing
a fourth Monte Carlo method:

| Marginal budget assumption | Source target | Partitions × bits/partition | Bit bytes | Header bytes | Payload bytes |
|---|---:|---:|---:|---:|---:|
| Independent sources | `1-0.95^(1/8) = 0.00639115095` | 8 × 3712 | 3712 | 40 | 3752 |
| Arbitrary dependence, union bound | `0.05/8 = 0.00625` | 8 × 3728 | 3728 | 40 | 3768 |

The exact integer payload difference is 16 bytes. Relative to the conservative
budget it is `16/3768 = 0.4246284501%`. This is a **sizing comparison only**;
no separate conservative-budget query FPR or runtime has been measured.
The arbitrary-dependence contract still requires valid per-source marginal
bounds. This calculation supplies no new proof of concrete BLAKE2b marginals.
The dimensions are saved in `results.json` under `canonical_budget_sizing` and
can also be reproduced without a full experiment:

```bash
bernoulli-py/.venv/bin/python -m pytest papers/bernoulli_relations/code/test_filter_calibration.py -q -s -k dependence_budget
```

## Exact audit of recorded occupancy contracts

The original acceptance implementation compares floating-point products to
floating-point source targets. It is not an outward-certified numerical
procedure: products can round downward, and the irrational calibrated source
root can round upward. A generic floating acceptance decision is therefore not
itself proof of the mathematical query target.

The saved `builds.csv` contains every partition occupancy and integer partition
size, permitting a separate exact check without rerunning construction. For
each row the audit reconstructs `P = product_j occupied_j`, `M = m^k`, and
`p(C) = P/M` with Python integer and `Fraction` arithmetic. It then compares
`1-(1-P/M)^e` with the exact rational target `1/20`, using `e=8` for calibrated
canonical storage and `e=16` for calibrated ordered OR storage. The target is
read as an exact decimal from `results.json`, not converted through a binary
floating-point value.

All **320 calibrated accepted constructions pass the exact comparison**:

| Method | Build attaining maximum | Exact envelope, shown to 50 significant digits | Target minus maximum |
|---|---:|---|---|
| Canonical calibrated | 87 | 0.049994339635235414542456134700079588771459499643139 | 0.0000056603647645854575438652999204112285405003568612075 |
| Ordered + OR calibrated | 50 | 0.049995334445865722252929203196032769613029302625581 | 0.0000046655541342777470707968039672303869706973744190539 |

The comparisons use exact fractions; the displayed decimal expansions are only
for readability. All 160 naïve constructions meet their exact source target
`p(C)<=1/20` and hence their larger query envelope
`1-(1-1/20)^8`. As expected, all 160 naïve query envelopes exceed `1/20`; they
are not query-calibrated. In addition, all 480 accepted constructions have exact
`p(C)` below their recorded source targets even when those targets are interpreted
as their actual binary floating-point values.

Consequently adding an exact final acceptance check would reject **none of the
480 recorded accepted structures**. The acceptance rule has not been changed;
the separate tiny-probability correction changes the analytical comparator and
extracts the existing dimension formula for the sizing comparison above.
Replacing its floating stopping rule entirely could in principle admit an
earlier candidate that floating-point arithmetic rejected; rejected candidate
occupancies were not recorded, so that separate question is not established by
this audit. Retaining the existing screening followed by an exact check leaves
the recorded accepted outputs unchanged.

A principled future acceptance predicate uses a rational query budget `a/b`
directly and checks the integer inequality

`b * [M^e - (M-P)^e] <= a * M^e`.

For the naïve source budget, use exponent one. This avoids both the floating
occupancy product and the rounded irrational source root for certification;
approximate roots may still size the candidate bit arrays. This remedy concerns
numerical certification under the ideal-hash model. It does not turn BLAKE2b
domain separation into a proof of that model.

The exact audit is a regression test and prints the results with:

```bash
bernoulli-py/.venv/bin/python -m pytest papers/bernoulli_relations/code/test_filter_calibration.py -q -s -k exact_recorded
```

## Verification and reproduction

From the workspace root:

```bash
bernoulli-py/.venv/bin/python -m pytest papers/bernoulli_relations/code/test_filter_calibration.py --cov=filter_calibration --cov-branch --cov-report=term-missing -q
bernoulli-py/.venv/bin/ruff check --config bernoulli-py/pyproject.toml papers/bernoulli_relations/code/filter_calibration.py papers/bernoulli_relations/code/test_filter_calibration.py
bernoulli-py/.venv/bin/mypy --strict papers/bernoulli_relations/code/filter_calibration.py
bernoulli-py/.venv/bin/python papers/bernoulli_relations/code/filter_calibration.py
```

The tests pass: 54 tests, 99% branch-aware coverage. The sole uncovered executable
statement is the module's `if __name__ == "__main__"` call; `main()` itself is
exercised by an integration test, and the full experiment was invoked directly.
Ruff and strict mypy pass. Tests include frozen byte storage, inserted-key recall,
serialization round-trip, diagonal and off-diagonal symmetry, a forced range
rejection, stable calibration at boundary rates, exhaustive cycle probabilities
on every truth profile for sizes three through six at four rates, maximal-false
profiles on cycle sizes three through fourteen, construction-based uncertainty,
reproducible small runs, and structured output writing.

The tiny-rate regressions compare with exact rational formulas at `2^-30`,
`2^-60`, and `2^-120`, using relative tolerance with **zero absolute tolerance**
so an erroneous zero cannot pass. They cover the extremal 12-cycle (probability
`1-(1-p)^8`), an all-false three-cycle (probability `3p^2-2p^3`), and an actual
stored Bloom with twenty one-bit-occupied eight-bit partitions (`p=2^-60`).
Saturated ordered OR probability is tested separately. Before the correction,
the tiny OR probability was zero, and the complement-based cycle calculation
lost positive success mass; the regressions reproduced both failures.

The complete default experiment was rerun after those corrections. All 480
payload hashes and construction-attempt counts, and all measured query outcomes,
match the preceding run. The default conditional model predictions changed by
at most `3.82e-17`, so all displayed probability and payload entries are
unchanged. The timing table above uses the fresh run; timing variation is
expected and is not a controlled performance comparison between code versions.
The regenerated `results.json` source hash matches the corrected implementation,
and the exact recorded-occupancy audit passes on the regenerated data.

No `bernoulli` package code is imported, so its package suite was not required
for this standalone artifact. The parent revision performs separate manuscript
validation. No commits or external publication were performed.

Remaining publication limitation: this is one small, explicit workload family
and one reference filter. It closes the prior gap between simulated source coins
and real stored-bit execution, but broader scale studies, workload families,
adversarial checks, alternative filters, and novelty assessment remain open.
