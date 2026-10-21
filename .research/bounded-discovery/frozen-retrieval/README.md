# Frozen-retrieval evidence and finalist reproduction

For the revised Comment, use the [portable supplement](../manuscript/venues/entropy-comment/supplement/README.md).
The historical `run_probe.py` below retains its audited bytes and uses assertions
for experiment operations: run it without `-O`, `-OO`, or `PYTHONOPTIMIZE`.
An editorial review found that optimization could skip those operations.
The portable runner now rejects optimized execution, including precompiled
optimized bytecode; historical normal-mode results remain valid.

Candidate 2 used exactly two discovery rounds. The first located the generic
joint-affine result in established linear coding theory. The second identified
a concrete GBFPlus endpoint-confidentiality counterexample. See
[literature](literature.md), [model](model.md), and the
[focused manuscript](../manuscript/main.tex).

## What is implemented

- `joint_probe.py`: exact small affine-solution enumeration and independent
  binary rank calculation. The ideal law is not the actual package's seeded
  free-fill distribution.
- `stored_probe.py`: a conditional three-query relation in the existing
  `GF2Retrieval` slot array. Private implementation fields are read for
  instrumentation. The known stored row and public seed guide query selection;
  this is not a practical unknown-key attack or a fixed-query FPR estimate.
- `gbfplus_probe.py`: Algorithm 4's share update and the public occupancy/XOR
  attack. `None` means unoccupied; zero is an occupied payload. It does not
  implement pairing operations, signatures, ledger access, or finalization.
  Snapshot provenance and authentic counts are premises. In the driver the
  singleton count is set to one only after a successful insertion.
- `run_probe.py`: exact checks, 64 separately seeded stored arrays, the package
  relation witnesses, and source hashes in `results.json`.
- `test_*.py`: exhaustive cases, uniform single-share marginals versus disjoint
  joint supports, repeated reads, overlaps, failure atomicity, input boundaries,
  and narrow padding/masking contrasts.

The original publisher PDF/XML and checksums live in `evidence/`. The retained
article is CC BY 4.0; attribution and original URL are in its source manifest.
The code is a reference reproduction of the relevant share operation, not the
authors' software or an end-to-end reproduction of their benchmark.

## Reproduce from the Bernoulli workspace root

The existing development environment has the editable `bernoulli-types`
package, pytest, coverage, Ruff, and mypy. Core experiment code otherwise uses
the standard library. Version information is in `verification.json`.

```bash
bernoulli-py/.venv/bin/python -m pytest .research/bounded-discovery/frozen-retrieval -q
bernoulli-py/.venv/bin/python .research/bounded-discovery/frozen-retrieval/run_probe.py
bernoulli-py/.venv/bin/ruff check .research/bounded-discovery/frozen-retrieval
MYPYPATH=bernoulli-py/src bernoulli-py/.venv/bin/mypy --strict .research/bounded-discovery/frozen-retrieval/*.py
make -C .research/bounded-discovery/manuscript
```

Coverage, isolated from the preexisting root `.coverage`:

```bash
COVERAGE_FILE=.research/bounded-discovery/frozen-retrieval/.coverage bernoulli-py/.venv/bin/python -m coverage run --branch --source=.research/bounded-discovery/frozen-retrieval --omit='*/test_*.py' -m pytest .research/bounded-discovery/frozen-retrieval -q
COVERAGE_FILE=.research/bounded-discovery/frozen-retrieval/.coverage bernoulli-py/.venv/bin/python -m coverage run --append --branch --source=.research/bounded-discovery/frozen-retrieval --omit='*/test_*.py' .research/bounded-discovery/frozen-retrieval/run_probe.py
COVERAGE_FILE=.research/bounded-discovery/frozen-retrieval/.coverage bernoulli-py/.venv/bin/python -m coverage report -m
```

Run the driver normally again after coverage if comparing its descriptive
timing. The measured scan excludes ledger download, parsing, and authenticity
verification and is not a systems-performance claim. Mathematical results,
seeds, arrays, and witness keys reproduce exactly; timing/platform/version
fields naturally vary.

## Verified output

- 19 tests passed; 100% statements, 98.89% branches, 99.68% combined coverage
  across the four experiment modules. The sole uncovered branch is the
  driver's non-executed `__main__` path. The three probe modules have 100%
  statement and branch coverage.
- 256 exhaustive singleton cases and 1,024 disjoint two-insertion cases,
  all recovering the predicted suffix or aggregate.
- 64 separately seeded arrays with κ=12, λ=32, domain width 20, m=64.
  Widths/κ follow the paper's §6.3 prototype; m is illustrative. Proofs hold
  for every valid choice, so the PRNG is not a security assumption.
- 8,736 finite systems corroborate the established affine-image identity.
- Three actual stored GF2Retrieval witnesses; output triples XOR to 90.
- 92 relevant existing retrieval, codec, Bloom, and correlated-Bloom tests pass.

No guarantee is inferred from a passing simulation. The manuscript gives the
short exact proofs and identifies the source premises they require.
