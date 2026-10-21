# Relations manuscript revision plan

**Goal:** Turn the inherited relations draft into a coherent, mathematically scoped research manuscript incorporating the dependence-calculus findings and a concrete approximate-filter probe. Submission readiness remains an outcome to assess, not an assumption.

**Spec:** The user's request to continue publication development, treating the spun-off relations paper as potentially rough and incomplete; `.research/dependence-calculus/synthesis.md` supplies the completed research assessment.

**Architecture:** Separate exact relation, construction randomness, frozen realization, and source identities. Retain independent-tuple formulas as a scoped special case. Make query-level contracts and invariant-preserving representations the central thread; treat existing lineage/inference machinery as prior art. A reproducible experiment should exercise stored bits and query computations, not only simulated coins.

**Stack:** Existing LaTeX manuscript and bibliography; Python reference artifacts and pytest; existing bernoulli-py package where its semantics are appropriate.

## Constraints

- Preserve unrelated changes and the prior research record.
- User has authorized routine local research, experiments, and manuscript edits without intermediate design approval.
- No external publishing, submission, commits, or unrelated API refactoring.
- Make exact assumptions visible; do not equate hash domain separation with a proof of statistical independence.
- Build and inspect the complete paper. Run relevant experiment tests, existing numerical validations, and the Python package suite when code uses that package.

## Work and ownership

- [x] Root: rewrite abstract, introduction, exact/random semantics, contribution scope, bibliography, and conclusion; integrate a new query-contract section from checked proofs.
- [x] Mathematics worker: own `sections/properties.tex` and `sections/rel_algebra.tex` for a scoped theorem audit and repairs; report findings in this research directory. Retain existing labels where possible.
- [x] Experiment worker: own new `code/filter_calibration.py`, `code/test_filter_calibration.py`, and generated results under `data/calibration/`. Compare a real canonical-orbit representation with ordered tuple plus OR repair at explicit query targets; record limitations and avoid oracle-backed simulations.
- [x] Root: integrate empirical section, demote unsupported security claims/application to appropriately limited scope, update paper guidance and publication state using a structured YAML parser.
- [x] Review: check complete argument, proofs, experiment interpretation, citations, clean build, and rendered PDF. Deliver revised draft with remaining publication gap stated plainly.

## Review focus

Variable orbit sizes; probability-zero conditioning classes; both FP/FN present versus separate one-sided models; projection after aliases; marginal storage claims versus physical memory; the distinction between exact identities, approximations, empirical agreement and novelty.
