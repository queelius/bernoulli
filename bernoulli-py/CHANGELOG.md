# Changelog

All notable changes to `bernoulli-types` (import name `bernoulli`).
Format loosely follows Keep a Changelog; this project uses semantic versioning.

## [Unreleased]

### Added
- Phase 2 (sets), pure-Python core: `bernoulli.sets.composition` (`SetRates`,
  `Partition`, and union / intersection / complement / difference rate
  propagation using the book chapter 6 three-region formulas, with the bare
  product exposed as the `Partition.sparse()` limit) and
  `bernoulli.sets.entropy_bound` (the `-log2(fpr)` floor, the Bloom `1.44x`
  overhead, and the BHF model from chapters 8 and 14). Hypothesis property
  tests cover both.
- `bernoulli.bench`: a timing harness (`benchmark`, `bench_membership`,
  `BenchResult`) complementing `bernoulli.harness` (which measures rates).
  Reports best-of-N throughput and per-op latency, reusable from notebooks and
  experiments.
- Phase 3 (maps): `bernoulli.maps.MinimalPerfectHash` (a BBHash minimal perfect
  hash, about 3 bits/key at gamma=2) and `bernoulli.maps.PerfectFilter`, the
  book chapter 14 Bernoulli hash function: a perfect hash plus an r-bit
  fingerprint per slot, giving `fnr = 0` and `fpr = 2^-r` at `mu + r` bits per
  key. Validated against `entropy_bound` (measured bits/key equals
  `bhf_bits_per_key` with the measured perfect-hash overhead as `mu`); beats the
  Bloom filter at tight FPR targets.
- Phase 3 (maps), retrieval and codecs: surfaced `bernoulli.maps.codec`
  (`DenseCodec`, `PaddedCodec`, `PrefixCodec`, `shannon_entropy`) through the
  `bernoulli.maps` namespace, and added `bernoulli.maps.GF2Retrieval` (a static
  `keys -> r-bit` retrieval by GF(2) peeling) and
  `bernoulli.maps.EncodedRetrieval` (retrieval composed with a codec). The codec
  controls the non-member value distribution independent of storage frequency
  (the maph CODESPACE_NONMEMBERS result): a value never stored still appears for
  non-members in proportion to its codespace share.
- Phase 4 (relations): `bernoulli.relations.BernoulliRelation`, a relation as a
  Bernoulli set of tuples with a relational algebra that is the chapter 6 set
  algebra lifted to tuples. `select` is a noiseless restriction (rates
  unchanged); `join` propagates rates by the intersection composition (the bare
  product `fpr_R * fpr_S` is only the `Partition.sparse()` limit); `project`
  drives the false-negative rate down by the fiber multiplicity
  (`fnr ** fiber_size`, averaged over projected tuples).

### Fixed
- Composed set rates are clamped to `[0, 1]` to absorb floating-point overshoot
  in the three-region weighted sums (surfaced by a hypothesis property test at
  operand rates near 1).

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
