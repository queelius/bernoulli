# Query-contract opportunity test implementation plan

**Goal:** Settle whether constrained error budgeting survives competent physical
representations, then assess the finite-hash alternative.

**Architecture:** Typed functional-row schema and parameterized intersection
queries; frozen serialized representations; isolated reproducible driver with
exact rational audits and construction-level summaries.

**Tech stack:** Python 3.12 environment in bernoulli-py/.venv, stdlib, pytest and
coverage; pinned upstream C binary fuse filter through a small local bridge.

**Spec:** [design.md](design.md). State and decisions remain in this directory;
the user explicitly authorized autonomous execution. No commits or publishing
are required; preserve all unrelated edits and previous research artifacts.

- [x] Prove/verify constrained formula, aliases, and edge cases; record novelty.
- [x] Write failing tests for contracts and finite value storage, then implement.
- [x] Pin and test actual binary fuse storage/serialization independently.
- [x] Extract a reproducible manifest workload and synthetic controls; test the
  driver on a tiny complete run before the main experiment.
- [x] Measure equal-target storage and cost, FP/FN validity and tightness, exact
  conditional envelopes, metadata and candidate generation; separate effects.
- [x] Evaluate finite shared-hash alternative with exhaustive constructions and
  adversarial dependent collision events.
- [x] Run relevant unit/integration tests and inspect coverage, obtain an
  independent critical review, address material findings.
- [x] Write evidence-backed publication decision and best remaining direction;
  update manuscript only if a clearly attributable contribution warrants it.

Review focus: empty domains/partial rows; repeated operands; float threshold
rounding; conditioning on construction retries; seed and dictionary overhead;
concrete modern-filter guarantees vs an ideal model; benchmark language costs;
fixed-key guarantees vs adaptive selection; experiments cannot prove novelty.

Completed 2026-10-14. The publication gate did not pass; the relations manuscript
was not updated. See [assessment.md](assessment.md) for results and scope,
[review.md](review.md) for verification and limitations, and [state.md](state.md)
for the next research gate. A substantial general planner was intentionally not
built after the compact opportunity experiment failed to establish its value.
