# Phasing: bernoulli (Python + C)

The package implements the framework atom-outward, mirroring the textbook's
five parts. Each phase ships a coherent slice and yields one or two natural
blog posts.

## Phase 1: The atom (book Part I, ch. 1 to 4, 7). Implemented in 0.2.0.

- `bernoulli.atom.BernoulliBool`: value with channel matrix `(alpha, beta)`
- `bernoulli.algebra`: closed-form AND / OR / NOT composition, Miller-Rabin
  pattern, k-fold chain composition theorem
- `bernoulli.measures`: PPV, NPV, Youden's J, F1, MCC, base-rate error

Pure Python. No C dependencies.

**Open research questions:** the AND's prior-dependent FPR has a known
closed form (book section 3.1), and the package implements both the
conservative distribution-free bound and the prior-form. No remaining theory
work for the atom. Calibration of single-classifier rates from observation
tables is a pedagogical exercise, not a research question.

**Blog posts unlocked:**
- "What's a Bernoulli<bool>?"
- "AND/OR/NOT under noise: De Morgan's law for noisy gates"
- "FPR is half the story: PPV, NPV, and Youden's J"

## Phase 2: Sets (book Part II, ch. 5 to 6, 8)

- `bernoulli.sets.MembershipOracle`: protocol mirroring maph's concept
- `bernoulli.sets.BloomFilter`: k-hash Bloom filter (Python + optional C)
- `bernoulli.sets.composition`: union, intersection, difference under
  the Bernoulli error model
- `bernoulli.sets.entropy_bound`: `-log2(epsilon) - mu` analyses

C-backed: bit array `set_bit/test_bit/popcount`, hash evaluation (xxhash,
FNV variants), k-hash position generation.

**Open research:**
- Optimal Bloom-filter sizing under heterogeneous query distributions
- Empirical comparison: classical Bloom vs. space-optimal Bloom (BHF) at
  realistic FPR targets

**Blog posts unlocked:**
- "Bloom filters are Bernoulli<set>"
- "How close to the entropy bound can you get?"
- "Composing approximate sets: when union FPR doubles and when it doesn't"

## Phase 3: Maps and codecs (book Part III, ch. 9; Part IV, ch. 14 to 15)

- `bernoulli.maps.PerfectHashFunction`: protocol
- `bernoulli.maps.ApproximateMap`: protocol mirroring maph
- `bernoulli.maps.PerfectFilter`: PHF + fingerprint composition
- `bernoulli.maps.PrefixCodec`: Huffman-style codec for value-to-bits
- `bernoulli.maps.RibbonRetrieval`: port of maph's ribbon system
- `bernoulli.maps.EncodedRetrieval`: codec-controlled non-member output

C-backed: GF(2) Gaussian elimination, ribbon band sparse matrix ops,
fingerprint storage, PHF evaluation.

**Open research (ready to investigate now in maph; port findings here):**
- Tighter bound on ribbon's non-member uniformity (maph open Q2)
- Security reduction for cipher-map use under codec choice (maph open Q4)
- Codec selection minimizing statistical-attack leakage

**Blog posts unlocked:**
- **"Codecs control non-member output: a measured claim"** (publication-grade,
  see `~/github/repos/maph/docs/CODESPACE_NONMEMBERS.md`)
- "A perfect filter is two layers"
- "When perfect filters beat Bloom"

## Phase 4: Relations (book ch. 12)

- `bernoulli.relations.BernoulliRelation`: multi-attribute approximate map
- `bernoulli.relations.algebra`: selection, projection, join under
  approximation, with rate propagation

**Open research:** join error propagation under correlated approximations
(when the two relations share a key or were built from overlapping data).

**Blog posts unlocked:**
- "Approximate joins"

## Phase 5: Sketches and estimators (book ch. 10 to 11)

- `bernoulli.sketches.CountMinSketch`
- `bernoulli.sketches.HyperLogLog`
- `bernoulli.sketches.MinHash`
- `bernoulli.estimators.MillerRabin` (re-cast from algebra)
- `bernoulli.estimators.LasVegas` / `MonteCarlo` adapters

C-backed: counter arrays, register update, hash-permutation evaluation.

**Blog posts unlocked:**
- "Sketches as Bernoulli<map>: one model, several knobs"

## C build strategy

- **Phase 1:** no C, pure Python.
- **Phase 2+:** opt-in `cffi` (api mode) build at install time. C source lives
  in `c/`. Pure-Python fallbacks for every operation, so `pip install bernoulli`
  succeeds even without a working C toolchain. `pip install bernoulli[c]`
  enables compilation and binds the accelerated implementations.
- **Why cffi over Cython or pybind11:** cffi keeps the C side as portable C
  source (no Python.h tangle, no C++ ABI drift), the Python side remains
  pure-Python except for one `_c.so`, and the binding code is generated, not
  hand-written.
- **Why not bind to maph's C++23 directly:** maph is the *research* playground,
  this package is a *production* artifact for PyPI, where users expect
  portable manylinux/macosx wheels. Plain C source compiles everywhere
  without C++23-capable toolchains. Algorithmic ideas port; bindings don't.

## Roadmap discipline

Each phase ships:
1. The protocol(s) (`Protocol`, runtime-checkable where useful)
2. At least one concrete implementation
3. Pure-Python first, C accelerator second
4. Property-based tests via `hypothesis`
5. Worked examples that match the textbook's chapter examples
6. A benchmark harness reusable from notebooks and paper experiments

No phase is "done" without all six.
