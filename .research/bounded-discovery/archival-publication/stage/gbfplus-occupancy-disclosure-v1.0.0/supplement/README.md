# Supplement S1: GBFPlus public-occupancy disclosure

Author: Alexander Richard Towell (ORCID 0000-0001-6443-9897).
Archival edition 1.0.0, 2026-10-20. See the root citation and publication record.

This is the focused companion to the Comment on Qin et al., *Privacy-Preserving
On-Chain Attestation for Cross-Domain Data Flows via GBFPlus*, Entropy 28:947
(2026), [DOI 10.3390/e28090947](https://doi.org/10.3390/e28090947).
It reproduces the stored-share update in Algorithm 4 and Table 1 of the Comment.
It is independently written reference code, not the original authors' software.

## Reproduce

Unzip this archive into an empty directory. From that directory, run:

```bash
python3 -S reproduce.py
```

This uses only the Python standard library and writes `reproduced-results.json`
in the current working directory. It does not need the Bernoulli repository,
network access, cryptographic libraries, or installed site packages. Run without
Python's `-O` option: the experiment checks use assertions. The runner rejects
optimization enabled by `-O`, `-OO`, or `PYTHONOPTIMIZE`, including precompiled
optimized bytecode run in an unoptimized interpreter, before constructing or
writing any result. Python 3.12.3 is the verified interpreter. The runner
preserves the prior experiment functions
unchanged; `provenance.json` records their syntax-tree and source-file hashes.

The output must contain:

| JSON field | Expected result |
|---|---|
| `gbfplus_exact.singleton_cases` | 256 |
| `gbfplus_exact.singleton_errors` | 0 |
| `gbfplus_exact.disjoint_batch_cases` | 1,024 |
| `gbfplus_exact.disjoint_batch_errors` | 0 |
| `gbfplus_exact.all_individual_share_marginals_uniform` | true |
| `gbfplus_exact.two_recipient_view_supports_disjoint` | true |
| `gbfplus_stored.instances` | 64 separately seeded stored arrays, each recovering its domain |

`reference-results.json` retains the previously audited output. All mathematical
results, seeds, positions, payloads, and recovered values agree with it. The
descriptive scan timing is intentionally variable and is not a performance
claim. Platform/version fields and runner hashes describe the current run.

The singleton enumeration fixes `m=7`, positions `(5,1,3)`, and prefix `1`;
it covers `4 × 8² = 256` suffix/free-word choices. The two-insertion enumeration
fixes positions `(0,4)` and `(1,5)` and prefixes `1` and `0`; it covers
`4² × 8² = 1,024` choices. The larger arrays use singleton seeds 0–63, drawing
12 positions, a 20-bit domain, a 12-bit prefix, and eleven 32-bit free words
per array. These are checks at stated fixed configurations, not an exhaustive
enumeration of hash positions or a survey of batch sizes.

## Tests and coverage

The optional validation environment is separate from runtime:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-validation.txt
.venv/bin/python -m pytest -q
COVERAGE_FILE=.coverage-validation .venv/bin/python -m coverage run --branch --source=gbfplus_probe,reproduce -m pytest -q
COVERAGE_FILE=.coverage-validation .venv/bin/python -m coverage report -m
.venv/bin/ruff check .
.venv/bin/mypy --strict gbfplus_probe.py reproduce.py test_gbfplus_probe.py test_reproduction.py
```

There are ten unchanged mathematical/representation tests and seven artifact tests.
They cover exhaustive suffix recovery, uniform individual shares versus
distinct joint supports, overlaps and abstention, unchanged previous rows,
atomic full-support failure, zero-valued occupied cells, boundary inputs, and
narrow padding/masking comparisons. The added tests compare every deterministic
experimental field, test output in a separate working directory, and execute
the runner with site packages disabled. The additional tests reject both
command-line, environment-based, and precompiled-bytecode optimization and check a hand-derived full
array, including the prefix, an occupied zero, and a subsequent overlapping row.
Coverage reports all 121 statements and 48 branches under normal compilation.
The compile-time `__debug__` guard's rejection path does not appear in that
normal-compilation total; subprocess regressions and a separately recorded
optimized execution verify its nonzero exit and absence of result output.
The final validation record accompanies the author-review package. Coverage
describes execution of this small implementation; it does not validate the
unimplemented cryptography, ledger, or publication policy.

## Assumptions and limits

`None` denotes an unoccupied cell; integer zero denotes an occupied zero word.
The insertion routine accepts distinct positions and explicit random words.
It neither derives positions cryptographically nor implements pairings,
signatures, ledger access, authentication, finalization, or the original paper's
benchmark. Honest history and an authentic successful-insertion count are
premises of the theorem, not established by `Snapshot` input validation.

For a singleton, public occupancy identifies all shares, whose XOR ends in the
adjacent-domain identifier. If occupied count equals insertion count times
shares per insertion, the same operation returns the aggregate domain XOR.
For larger batches this need not recover individual identifiers. Overlapping
supports cause this particular sufficient-condition attack to abstain.

Reading a frozen snapshot repeatedly repeats the same answer. The 64 constructions
use separate Python PRNG seeds, not cryptographic randomness. Exact proofs hold
for every admissible share realization; these finite checks do not prove security
or establish operational attack prevalence. Padding/masking tests address only
the stated statistic and do not establish a repaired protocol's security.

## Files and provenance

- `gbfplus_probe.py`: unchanged share update and public-only recovery operation.
- `reproduce.py`: two unchanged experiment functions, optimization guard, and standalone result writer.
- `test_gbfplus_probe.py`, `test_reproduction.py`: correctness and portability checks.
- `reference-results.json`: exact checks and all 64 saved arrays.
- `provenance.json`: original source/result hashes and the publisher PDF URL/hash.
- `source-premises.md`: specification premises that computation cannot establish.
- `requirements-validation.txt`: versions used for optional validation tools.

OpenAI Codex assisted with the research, implementation, tests, and packaging.
The author approved the manuscript on October 18 and authorized this archival
release on October 20, 2026. The software is MIT licensed; generated data and
original explanatory text are CC BY 4.0. See the root LICENSE.md. The source
paper is linked, attributed, and not bundled in this archive.

The historical function hashes use `ast.dump` without location attributes,
with the empty Python 3.12 `FunctionDef.type_params` field omitted for
compatibility with the earlier AST format. `provenance.json` specifies the
serialization, normalization, and verified interpreter. A raw Python 3.12 dump
includes the new field and therefore has a different digest; direct AST equality
between the historical and portable functions was also checked.
