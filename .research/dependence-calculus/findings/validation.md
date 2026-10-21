# Final verification record

2026-10-13. Commands were actually executed; no test or publication outcome is inferred from a plan.

- `check_theory.py`: 256 exact covariance cases; eight weighted paths; 87 weighted cycles; K4 edge-cover count 41, quotient FPR 23/64, prequotient FPR 1695/4096.
- `check_contracts.py`: exact rational arithmetic, 1,970 checks over 197 monotone functions on one through four variables; 305 degree-at-most-two graph checks. JSON outputs persisted in the theory attempt folder.
- Research pytest: **28 passed**. Latest coverage: **211 statements and 64 branches, none missing** in `contracts.py`; `coverage.json` persisted. This coverage excludes benchmark/plot infrastructure and does not prove correctness.
- Research `mypy --strict contracts.py`: passes. Ruff selected E/F/I/B/UP/SIM checks: pass for engine, tests, benchmark, and summarizer.
- Existing package pytest with branch coverage: **470 passed, 3 skipped**, total coverage **90%**. Lowest existing module coverage includes harness 69% and algebra 76%; those unrelated gaps were not expanded during this investigation.
- Existing package Ruff: passes. Existing package strict mypy: passes on **29 source files**.
- Independent reviewer: checked 8,000 compiled relational possible worlds and 983 graph/singleton sensitivity cases. Two recursion defects were reproduced, corrected, and turned into tests. Final review reported no remaining high-confidence correctness finding within stated assumptions. Its auxiliary exploratory commands were not saved as a separate standalone script; the persisted root/theory suites are the reproducible validation surface.
- Benchmark: **175** method/case comparisons; **0** claimed intervals miss available references at absolute tolerance 1e-12; **23** occurrence-product estimates disagree. Benchmark metadata source hashes match final `contracts.py` and `benchmark.py`. Large-reference and baseline-strength limitations are stated in `RESULTS.md`.
- Scientific plot: `comparison.png` visually inspected; axes, legends, and labels legible with no overlap. SVG available for export.
- Technical note: six pages, rebuilt twice after bibliography correction. Final LaTeX log contains no undefined references/citations or overfull/underfull warnings. Theory branch visually inspected all pages, including affected pages after final correction.
- Bibliography: 24 primary-source entries, BibTeX parsed successfully in the literature branch; access and metadata uncertainties remain recorded explicitly in its ledger.
- Scope: only `.research/dependence-calculus/` research artifacts added by this run. All preexisting modified PDFs, removed archives, and other untracked files remain present in the worktree status. No commits, pushes, submissions, or publications performed.
