# Reproduction and verification

Author: Alexander Richard Towell. Date: 2026-10-14.

Only the candidate audit directory was written. The existing environment at
`bernoulli-py/.venv` was reused; no packages were installed. Versions: Python
3.12.3, NumPy 2.4.6, pytest 9.0.3, coverage 7.14.1, Hypothesis 6.155.2,
Ruff 0.15.16, mypy 2.1.0.

From `/home/spinoza/github/bernoulli`, the original scripts were run exactly as
follows; both exited 0:

```bash
PYTHONDONTWRITEBYTECODE=1 bernoulli-py/.venv/bin/python papers/bernoulli-quantum-readout/code/readout_figure.py > .research/publication-triage/candidates/quantum-readout/evidence/original_readout_stdout.txt
PYTHONDONTWRITEBYTECODE=1 bernoulli-py/.venv/bin/python papers/bernoulli-quantum-readout/code/crosstalk_validation.py > .research/publication-triage/candidates/quantum-readout/evidence/original_crosstalk_stdout.txt
```

From `/home/spinoza/github/bernoulli/.research/publication-triage/candidates/quantum-readout`,
the independent audit and its checks were run:

```bash
PYTHONDONTWRITEBYTECODE=1 /home/spinoza/github/bernoulli/bernoulli-py/.venv/bin/python audit.py > evidence/independent_audit_stdout.txt
PYTHONDONTWRITEBYTECODE=1 COVERAGE_FILE=.coverage /home/spinoza/github/bernoulli/bernoulli-py/.venv/bin/python -m pytest -q test_audit.py --cov=audit --cov-branch --cov-report=term-missing --cov-report=json:coverage.json --basetemp=.pytest-tmp -o cache_dir=.pytest_cache > validation.txt 2>&1
/home/spinoza/github/bernoulli/bernoulli-py/.venv/bin/ruff check --isolated audit.py test_audit.py > ruff.txt 2>&1
/home/spinoza/github/bernoulli/bernoulli-py/.venv/bin/mypy --strict --cache-dir .mypy_cache audit.py > mypy.txt 2>&1
```

The audit run exited 0 and writes `results.json`. Final pytest: **17 passed in
6.86 seconds**. Coverage reports **99%** combined statement/branch coverage:
146/147 statements and 37/38 branches. The missing statement is line 250,
the `main()` invocation under `if __name__ == '__main__'`; the independent
script run exercises that path. Both `run_audit()` and `main()` themselves are
tested. Ruff passes; strict mypy passes for the audit implementation.

The tests cover all 16 two-bit Boolean truth tables at all four input words;
50 deterministic Hypothesis examples of independent parity, including empty
and boundary-rate cases; exact central-moment expansion of dependent laws;
two independent correlated pairs where the all-pair baseline is exact;
zero pair covariances with unequal parity laws; conditioned output rates;
source reuse; invalid channel inputs; calibration agreement; and integration
with the canonical chain-model code. All mathematical audit probabilities
use `Fraction`, apart from comparisons to the original NumPy implementation
and serialization of final decimal results.

An initial lint run flagged two lambda assignments; these were changed to
ordinary named functions and the final checks passed. No mathematical or
statistical assertion failed. The earlier pre-final suite had 16 tests; the
17th verifies the new all-pair-cumulant baseline against an exact four-bit
distribution with two independent correlated pairs.

Calibration reproducibility is offline after checkout: `evidence/hanoi.json`
is the original official JSON. Its SHA256 and immutable URL appear in
`evidence/calibration_provenance.json`. Both `main` and the pinned last-changing
commit returned identical bytes. The source-rate loader uses Python's AST
parser and `literal_eval`; the calibration loader uses JSON. Neither uses
regular expressions or executes the canonical source to extract data.

The original readout Monte Carlo used seed 7 and one million trials for each
of 26 prefix sizes; its maximum reported deviation was 0.000953. The original
chain-crosstalk Monte Carlo used seed 11 and two million trials per event rate;
all five assertions against exact values passed. These are model checks, not
new hardware measurements.

No package source or canonical manuscript was changed, so a package-wide test
run or LaTeX rebuild was not needed for this read-only manuscript audit.
`git diff --stat -- papers/bernoulli-quantum-readout bernoulli-py` was empty at
completion. The five read canonical files are fingerprinted in
`source_manifest.json`. Existing unrelated repository modifications were
preserved.
