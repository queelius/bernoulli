# Reproduction and final checks

Run from `.research/publication-triage/candidates/hash-construction/`:

```bash
/home/spinoza/github/bernoulli/bernoulli-py/.venv/bin/python audit_hash.py > results.json
/home/spinoza/github/bernoulli/bernoulli-py/.venv/bin/python -m pytest --cov=audit_hash --cov-branch --cov-report=term-missing --cov-report=json:coverage.json
/home/spinoza/github/bernoulli/bernoulli-py/.venv/bin/ruff check audit_hash.py test_audit_hash.py
/home/spinoza/github/bernoulli/bernoulli-py/.venv/bin/python -m mypy --strict audit_hash.py test_audit_hash.py
```

The exact audit itself uses only Python's standard library; the tests use the
existing pytest development environment. `results.json` is stdout in JSON,
not a manually edited collection of results. The end-to-end test compares CLI
output with the exact report. Tested on Python 3.12.3 / pytest 9.0.3.

Final results: **20 passed**, **98%** combined statement/branch coverage, Ruff
clean, strict mypy clean. The uncovered print line is exercised in a subprocess
by the CLI integration test, which the pytest coverage process does not collect.
No core-package change or manuscript change was made; no full-package suite,
LaTeX build, or practical filter throughput benchmark is claimed.

The investigator's turn stopped while finishing its documentation. The root
completed the reference registry and commands, and fixed a type-check failure
by expressing displacement directly as an integer-count ratio using Fraction.
Tests, coverage, lint and strict typing were then rerun successfully. The
original numerical report is unchanged. Source hashes for the manuscript
inputs are in `source_manifest.json`; retained primary-source Bloomier
material is read-only evidence.
