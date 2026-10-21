# Dependence-aware Bernoulli query research

Start with [the synthesis](synthesis.md) for the answer, publication assessment, and recommendation.

- [Claim–evidence ledger](claims.md)
- [Local manuscript/package audit](local-audit.md)
- [Primary-source literature audit](attempts/001-literature/findings.md) and [bibliography](attempts/001-literature/references.bib)
- [Proofs and derivations](attempts/002-theory/theory.md)
- [Six-page internal technical note](attempts/002-theory/technical-note.pdf), with [LaTeX source](attempts/002-theory/technical-note.tex)
- [Measured comparisons and plots](attempts/003-prototype/RESULTS.md)
- [Reference implementation](attempts/003-prototype/contracts.py) and [tests](attempts/003-prototype/test_contracts.py)
- [Resumable state](state.md) and [append-only research log](log.md)

The note is **not submission-ready**: mathematical correctness is supported, but standalone novelty and practical impact are not established. No external submission was made.

## Reproduce

From the workspace root, using its existing development environment:

```bash
bernoulli-py/.venv/bin/python .research/dependence-calculus/attempts/002-theory/check_theory.py
bernoulli-py/.venv/bin/python .research/dependence-calculus/attempts/002-theory/check_contracts.py
bernoulli-py/.venv/bin/python -m pytest .research/dependence-calculus/attempts/003-prototype/test_contracts.py
```

For research coverage, measurements, and plots:

```bash
cd .research/dependence-calculus/attempts/003-prototype
../../../../bernoulli-py/.venv/bin/python -m pytest --cov=contracts --cov-branch --cov-report=term-missing --cov-report=json:coverage.json test_contracts.py
../../../../bernoulli-py/.venv/bin/python benchmark.py --repeats 3
../../../../bernoulli-py/.venv/bin/python summarize.py
../../../../bernoulli-py/.venv/bin/mypy --strict contracts.py
../../../../bernoulli-py/.venv/bin/ruff check --line-length 100 --select E,F,I,B,UP,SIM contracts.py test_contracts.py benchmark.py summarize.py
```

Matplotlib is required only for `summarize.py`; it is available in this workspace's environment. The inference core uses only the Python standard library. Package tests import the existing editable `bernoulli` installation for one integration fixture. The prototype is deliberately not added to the public package API.

Build the technical note from `attempts/002-theory/` with two passes of `pdflatex -interaction=nonstopmode -halt-on-error technical-note.tex`. It uses standard TeX packages and an embedded bibliography; the fuller verified bibliography is separate.

## Scope

The model fixes a finite candidate universe and a query chosen independently of construction randomness. Repeated IDs share a frozen bit. Distinct IDs are mutually independent only where explicitly assumed. Frechet and the union-based sensitivity envelope tolerate arbitrary dependence; product formulas do not. Source aliases must have consistent exact truth. Two-sided errors, extra integrity constraints, adaptive queries, arbitrary hash implementations, and certified floating-point bounds require the distinctions stated in the proofs and synthesis.
