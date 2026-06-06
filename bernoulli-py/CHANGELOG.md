# Changelog

All notable changes to `bernoulli-types` (import name `bernoulli`).
Format loosely follows Keep a Changelog; this project uses semantic versioning.

## [Unreleased]

### Changed
- Repository consolidation (Stage 0): this package, formerly at `src/bernoulli/`,
  is now the single Python tree at `bernoulli-py/`. The teaching stub at
  `python/` and its placeholder API are removed; the 15 book-companion
  notebooks moved into `bernoulli-py/notebooks/`. The C++ reference at
  `bernoulli-cpp/` is archived (`archived/bernoulli-cpp/`) and retained as a
  port source for the planned C core.
- PyPI distribution name set to `bernoulli-types` (the bare `bernoulli` is
  taken on PyPI). Import name is unchanged: `pip install bernoulli-types`,
  then `import bernoulli`.

## [0.2.0]

### Added
- Phase 1 (the atom): `bernoulli.atom.BernoulliBool`, `bernoulli.algebra`
  (composition theorem, k-fold chains, Miller-Rabin pattern),
  `bernoulli.measures` (PPV, NPV, Youden's J, F1, MCC). Pure Python, zero
  runtime dependencies.
- Early concretes toward later phases: `sets/{bloom, cascade,
  correlated_bloom}`, `maps/codec`, `sketches/hyperloglog`, `algorithms/`.
- 16 validation experiments under `experiments/` and a test suite
  (`tests/`, ruff and mypy strict clean).
