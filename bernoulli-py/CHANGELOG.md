# Changelog

All notable changes to `bernoulli-types` (import name `bernoulli`).
Format loosely follows Keep a Changelog; this project uses semantic versioning.

## [Unreleased]

## [0.3.0] - 2026-10-21

First release intended for PyPI. Phases 1 through 5 are implemented in pure
Python; the planned C acceleration does not exist yet.

### Added
- `bernoulli.formula`: exact error rates of Boolean formulas over independent
  noisy bits (`Var`, `Not`, `And`, `Or`, `variables`, `output_probability`,
  `error_probability`, `error_profile`, `worst_case_rates`, `marginal_rates`).
  Read-once formulas take one signal-probability pass (Parker and McCluskey
  1975); repeated variables are handled exactly by conditioning on their
  observations. This is the supported way to get rates through a whole formula,
  where reusing one `(fpr, fnr)` pair per gate is not exact (for
  `(x0 & x1) | x2` at latent word 010 with rates 0.02 and 0.10, the exact
  error is 0.03764 and pair reuse gives 0.020392).
- The top-level `bernoulli` namespace now exports the stable API of every
  phase: `BernoulliBool`, `SetRates`, `Partition`, `MembershipOracle`,
  `BloomFilter`, `PerfectHashFunction`, `ApproximateMap`, `MinimalPerfectHash`,
  `PerfectFilter`, `DenseCodec`, `PaddedCodec`, `PrefixCodec`, `GF2Retrieval`,
  `EncodedRetrieval`, `BernoulliRelation`, `CountMinSketch`, `HyperLogLog`,
  `MinHash`, and the modules `algebra`, `formula` and `measures`. Research
  utilities (`harness`, `bench`, `sets.cascade`, `sets.correlated_bloom`) stay
  in their submodules.
- `py.typed` marker (PEP 561), so type checkers use the package's annotations.
- Tests for the public exports, for importing every submodule first in a fresh
  interpreter (circular-import guard), and for the README and all module
  docstring examples, which now run as part of the suite.
- CI: `.github/workflows/bernoulli-py.yml` runs pytest with branch coverage,
  ruff and mypy on Python 3.11 to 3.13, and builds and checks the
  distributions.
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
- Phase 5 (sketches): `bernoulli.sketches.CountMinSketch` (a one-sided
  `Bernoulli<int>` frequency estimator: never undercounts, overestimate bounded
  by `e/width * N` with probability `1 - e**-depth`) and
  `bernoulli.sketches.MinHash` (a `Bernoulli<float>` Jaccard estimator: per-hash
  signature minima, element-wise-min union merge), joining the existing
  `HyperLogLog`.

### Fixed
- `BernoulliBool.or_with_prior` returned an FNR of 0 for priors below about
  1.1e-16, because `1 - (1 - prior)**2` rounded to 0 there; the conditional
  rate is now computed with the common factor `prior` cancelled analytically,
  which also holds at subnormal priors. `and_with_prior` uses the same
  cancelled form (dividing out `1 - prior`) for precision near `prior = 1`; its
  old form never rounded to 0.
- Documentation overstated composition. The `bernoulli.atom` docstring
  described a conservative "min bound" that the code never implemented and
  called the operators "never wrong", and the old README repeated it. The
  docstrings of `bernoulli.atom`, `bernoulli.sets.composition` and
  `bernoulli.relations` now state when each formula is exact (one gate; `&`
  and `|` on read-once AND/OR trees of observations of one bit; nested set
  operations only with point-mass partitions) and point to `bernoulli.formula`
  otherwise.
- `experiments/14_coincidence_oracle.py` regenerated the inverted May
  conclusion ("Dense defends best at t >= 2") although `RESULTS_14.md` carried
  the 2026-05-17 correction. The generator now writes the corrected text and
  correction note, and refuses to write a report whose codec ordering
  contradicts its own numbers. `experiments/SYNTHESIS.md` is corrected to
  match (Thread A claim 6 and the summary), its counts and paths are updated,
  and the Exp 11 Le Cam agreement is described as a consistency check rather
  than a finding.
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
- The version has one source, `src/bernoulli/_version.py`, which the build
  reads (`[tool.hatch.version]`).
- README rewritten to match the code: what is implemented and what is not,
  credited predecessors, runnable examples, and stated limits.
- Package metadata: project URLs (hub, monograph, source, issues, changelog),
  keywords led by standard terms, classifiers, `license = "MIT"` with
  `license-files` (PEP 639), and `CHANGELOG.md` and `CITATION.cff` in the sdist.

### Removed
- The `[c]` extra, which installed cffi with no C code to bind, and the
  `[numerics]` extra, which installed numpy that the package never imports. The
  `[c]` extra returns when the C core exists.
- The `Programming Language :: C` classifier (there is no C code) and the
  `License ::` classifier (superseded by the SPDX `license` field).

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
