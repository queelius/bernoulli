# Error contracts for approximate relations

Alexander Richard Towell. Working draft, revised October 2026.

This manuscript separates exact relation truth, frozen construction randomness,
and shared source identity. It gives scoped operator and invariant calculations,
monotone query error contracts, and a reproducible stored-filter calibration study.
It is **not yet assessed as a submission-ready original research contribution**.
See [the current assessment](../../.research/relations-revision/assessment.md).

## Build

Run in this directory:

```bash
TEXINPUTS='.:./sty:' pdflatex -shell-escape -interaction=nonstopmode -halt-on-error main.tex
bibtex main
TEXINPUTS='.:./sty:' pdflatex -shell-escape -interaction=nonstopmode -halt-on-error main.tex
TEXINPUTS='.:./sty:' pdflatex -shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The output is `main.pdf`. The modular notation packages are local in `sty/`.
The preamble loads minted, so the historical build enables shell escape.

## Reproduce research checks

The following commands run from the **repository root**, using the existing
Python environment (pytest, pytest-cov and NumPy are needed for the full checks).
The filter experiment itself uses the standard library.

```bash
bernoulli-py/.venv/bin/python -m pytest papers/bernoulli_relations/code -q \
  --cov=filter_calibration --cov=validate --cov-branch --cov-report=term-missing
bernoulli-py/.venv/bin/python papers/bernoulli_relations/code/validate.py --trials 2000000 --seed 20260608
bernoulli-py/.venv/bin/python papers/bernoulli_relations/code/validate_quotient.py
bernoulli-py/.venv/bin/python papers/bernoulli_relations/code/filter_calibration.py --output /tmp/relations-calibration-rerun
bernoulli-py/.venv/bin/python -m pytest papers/bernoulli_relations/code/test_filter_calibration.py -q -s -k exact_recorded
bernoulli-py/.venv/bin/python .research/dependence-calculus/attempts/002-theory/check_contracts.py
bernoulli-py/.venv/bin/python .research/dependence-calculus/attempts/002-theory/check_theory.py
bernoulli-py/.venv/bin/python .research/relations-revision/check_borrowed_models.py
```

The full filter run uses 160 builds, 128 bundles per truth profile, a 12-cycle
query, target 0.05, and seed 20261013. Independent construction means are the
uncertainty units. Runtime varies; timing values are descriptive.

Recorded filter data include a source SHA, configuration, seeds, occupancies,
serialized byte counts, and per-build/per-profile outcomes. The exact audit
checks recorded occupancy bounds with rational arithmetic. Floating construction
screening by itself is not a numerical certificate. Ideal independent hash
functions and concrete BLAKE2b experiments are explicitly distinguished.

## Evidence and related work

- [Filter experiment and data](data/calibration/README.md)
- [Mathematical repairs](../../.research/relations-revision/math-audit.md)
- [Claim–evidence ledger](../../.research/relations-revision/claims.md)
- [Related-paper transfers and separate correction leads](../../.research/relations-revision/related-ideas.md)
- [Prior-art survey and verified bibliography](../../.research/dependence-calculus/attempts/001-literature/findings.md)
- [Reference lineage comparison](../../.research/dependence-calculus/attempts/003-prototype/RESULTS.md)

Known lineage, dissociation, sensitivity/certificates, and finite-state inference
are credited rather than claimed as new. Measured canonical-versus-ordered
storage savings concern those representations, not superiority to all filters
or a large advantage over conservative contract sizing.
