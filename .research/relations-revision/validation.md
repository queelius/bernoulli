# Final validation — 2026-10-13

The revised manuscript is a **27-page working draft**. The final LaTeX/BibTeX
build has zero undefined references/citations, zero LaTeX warnings, and zero
overfull/underfull boxes. All pages were rendered and visually inspected via
contact sheets; title, mathematical statements, both tables and final discussion
were inspected at larger scale. A crowded numeric table was adjusted and
re-rendered. Source/result/PDF hashes are retained in `verification.json`.

## Fresh root verification

From repository root:

```bash
COVERAGE_FILE=.research/relations-revision/.coverage \
bernoulli-py/.venv/bin/python -m pytest papers/bernoulli_relations/code \
  --cov=filter_calibration --cov=validate --cov-branch \
  --cov-report=term-missing --cov-report=json:.research/relations-revision/coverage.json -q
```

**540 tests passed**: 486 mathematical validation tests and 54 filter tests.
For the two instrumented research modules, combined statement/branch coverage
is **99.45%**; statement coverage is 596/598 (99.67%), branch coverage 126/128
(98.44%). The two uncovered statements/branches are module entry-point guards;
separate full CLI runs exercise both. Coverage is inspected evidence of tested
paths, not a mathematical correctness proof.

The filter regression cases include tiny rates 2^-30, 2^-60, and 2^-120, checked
against exact rational expressions. This catches the previously found loss of
positive probabilities when subtracting a near-one failure probability from one.

Ruff passes for the filter, mathematical harness, quotient harness, and their
test files. Strict mypy passes for the filter implementation. The diff whitespace
check passes with `cr-at-eol` enabled for the collection dashboard's existing
CRLF format; no repository setting was changed.

## Model and experiment checks

- `check_contracts.py`: 1,970 exact rational contract identities on 197 monotone
  functions; 305 degree-at-most-two graph checks.
- `check_theory.py`: 256 projection covariance cases; eight weighted paths,
  87 weighted cycles; cubic K4 edge-cover example (41 edge covers, canonical
  FPR 23/64 versus prequotient 1695/4096).
- `check_borrowed_models.py`: the BHF discrete-law counterexample, a small
  conditional-rate Bloom example, and 16 ideal fingerprint conditional cases.
- `validate.py --trials 2000000 --seed 20260608`: worker's full integration run
  passed all fitted rows; maximum discrepancy 0.000429. Its deliberately wrong
  independence prediction remains a documented mismatch. Root reran its tests.
- `validate_quotient.py`: root's full 200,000-construction simulation passed
  after batching to avoid large temporary arrays. Canonical FPR/TPR were
  0.05001/0.90005, OR FPR/TPR 0.09751/0.99001. The script counts keys, not bytes.
- `filter_calibration.py`: full final run of 480 accepted filters and 1,440
  build/profile rows. All payload hashes, construction attempts, and observed
  query outcomes match the pre-numerical-fix run. Timing values were refreshed.
  Current implementation SHA matches `results.json`:
  `450db465c25a17d9d19dbd5b42641c339405f058e5897a635461ae2c19d236ed`.
- Exact recorded-occupancy audit: all 480 actual source budgets pass as rational
  inequalities; all 320 calibrated query envelopes are ≤1/20. Minimum margins
  are 0.00000566036476458546 (canonical) and 0.00000466555413427775 (ordered).
- Conservative-budget sizing audit: 3,752 versus 3,768 bytes, 16 bytes / 0.425%.
  This is a sizing comparison, not a fourth measured method.

To reproduce the last two checks:

```bash
bernoulli-py/.venv/bin/python -m pytest \
  papers/bernoulli_relations/code/test_filter_calibration.py -q -s \
  -k 'exact_recorded or dependence_budget'
```

No `bernoulli-py` package implementation was imported or modified by the new
filter artifact. The preceding research run's package suite (470 passed,
3 skipped, 90% overall coverage) was therefore not repeated here; current
verification targets the changed research modules and their CLI integrations.

## Limits preserved in the manuscript

The mathematical guarantee uses ideal independent hash functions conditional on
inserted-key histories. BLAKE2b experiments do not establish that law for all
keys, truth profiles, or adaptive workloads. The constructor's floating screening
is not a generic exact certificate; recorded builds receive a separate rational
audit. Synthetic lineage benchmarks use ordinary floating arithmetic and a
published symmetric dissociation baseline, not optimized scaled dissociation.
The current empirical family is narrow. None of these checks establishes novelty.

Unrelated pre-existing edits were preserved. No commit, push, submission, or
external publication was performed.
