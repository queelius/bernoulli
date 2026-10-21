# Reproduce the codec audit

Run from `/home/spinoza/github/bernoulli` with the existing development environment:

```bash
bernoulli-py/.venv/bin/python .research/publication-triage/candidates/codec-privacy/run_audit.py
bernoulli-py/.venv/bin/python -m pytest .research/publication-triage/candidates/codec-privacy/test_exact_audit.py --cov=exact_audit --cov-branch --cov-report=term-missing
bernoulli-py/.venv/bin/ruff check --config bernoulli-py/pyproject.toml .research/publication-triage/candidates/codec-privacy
```

The driver uses only the standard library and the existing local Bernoulli
package. Pytest/coverage/ruff are development dependencies. It records hashes
of the source inputs, including the companion manuscript in the adjacent
`trapdoor-computing` checkout. No input source is edited. `results.json` is
regenerated; exact probabilities are rational strings. Pickle sizes are specific
to the recorded Python implementation/version and are not resident-memory or
optimized-format measurements.

The seven tests include 3,000 exact probability cases, all 16 binary/two-release
decision rules for the decisive optimality counterexample, exact span oracles,
and integration checks on the existing codec and stored retrieval. They verify
counterexamples and scoped identities, not production input validation for a
new public API. The audit helpers intentionally take well-formed finite inputs.

Existing-package checks, run from `bernoulli-py/`:

```bash
.venv/bin/python -m pytest tests/test_codec.py tests/test_retrieval.py --cov=bernoulli.maps.codec --cov=bernoulli.maps.retrieval --cov-branch --cov-report=term-missing
```

Recorded: **62 passed**; combined statement/branch coverage **88%** (codec 85%,
retrieval 96%). Missing paths include error handling, absent/default cases,
Huffman boundary cases and failed peeling/retry paths. Passing tests do not
prove a privacy model or independence. The exact audit helper has **100%**
statement/branch coverage. See `package-coverage.json` for the executed package
lines. No core-package feature or canonical manuscript was changed.

Input/output semantics and the publication assessment are in
[assessment.md](assessment.md). The source hashes preserve which version was
audited; they do not assert that the sibling project is submitted or published.
