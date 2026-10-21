# Query contracts: completed opportunity audit

**Decision:** no original-research submission is warranted by this candidate.
Start with [assessment.md](assessment.md). The useful result is a verified,
finite four-wise row-fingerprint contract, with explicit assumptions and an
evaluation against exact storage and established filter baselines.

- [Theory, proofs, and counterexamples](theory.md)
- [Primary literature audit](literature.md) and [verified bibliography](references.bib)
- [Claim–evidence ledger](claims.md) and [independent review](review.md)
- [Results table](summary.csv), [computed findings](findings.json), [figure](comparison.png)
- [Exact artifact verification](verification.json) and [coverage](coverage.json)
- [Runtime and source provenance](provenance.json)
- [Research history](log.md), [design](design.md), [plan](plan.md)

## Reproduce

Run from `/home/spinoza/github/bernoulli`. Main experiments need Python 3.12,
a C compiler, and the existing relations `filter_calibration.py`. Tests use
pytest/pytest-cov; only the summarizer additionally needs matplotlib. The pinned
binary-fuse source and license are included. Git extraction uses two pinned
commits; `data/*/input.json` also preserves construction inputs and query
parameters for independent rebuilding without repeating Git extraction.

```bash
bernoulli-py/.venv/bin/python .research/query-contract-planner/code/experiment.py --builds 64 --per-profile 32 --output .research/query-contract-planner/reproduced
bernoulli-py/.venv/bin/python .research/query-contract-planner/verify_artifacts.py
bernoulli-py/.venv/bin/python .research/query-contract-planner/theory_checks.py
bernoulli-py/.venv/bin/python .research/query-contract-planner/summarize.py
COVERAGE_FILE=.research/query-contract-planner/.coverage bernoulli-py/.venv/bin/python -m pytest .research/query-contract-planner/code papers/bernoulli_relations/code/test_filter_calibration.py papers/bernoulli_relations/code/test_math_validation.py -q --cov=contracts --cov=value_store --cov=finite_rows --cov=fuse_baseline --cov=experiment --cov-branch --cov-report=term-missing --cov-report=json:.research/query-contract-planner/coverage.json
```

The verifier rebuilds **all 2304 recorded constructions** from their saved seeds,
checks payload hashes, retry counts and exact rational bounds, and replays all
build-zero queries. It reads exact values for reconstruction/validation only;
the approximate execution function does not receive them. Mathematical
counterexample/exhaustion commands are documented in theory.md.

The final measurements are under data/. Exact measured source is retained at
[measured-source/README.md](measured-source/README.md). Current code additionally
handles duplicate candidate parameters and unsupported tiny-target methods;
full rebuilding confirms the saved cases are unchanged. The fixed-C pilot is
retained under attempts/001-fixed-c/, with its scope failure documented.

## Contract scope

Exact database values and candidate parameters are fixed independently of the
construction seed. Rows are total and distinct; C is within the declared domain
and capacity. Repeated atoms and duplicate candidates reuse canonical sources.
Queries read frozen stored representations and draw no new randomness.

Finite row fingerprints have an unconditional theorem for uniform polynomial
coefficients. Bloom contracts use ideal random functions conditional on inserted
hashes and exact rational occupancy checks. The modern binary-fuse comparison
is nominal, not a proved finite contract. Seeded pseudorandom experiments are
evidence, not independence proofs. Adaptive queries, partial-row storage,
dynamic updates, and security/leakage guarantees are outside this artifact.

All prior research and manuscript edits are preserved. This run submitted and
published nothing externally.
