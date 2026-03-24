# CLAUDE.md — The Bernoulli Hash Function

## Paper

**Title:** The Bernoulli Hash Function: Optimal Bernoulli Sets and Bernoulli Maps
**Author:** Alexander Towell
**Repo:** `queelius/bernoulli-hash-function`

## What This Paper Is About

The Bernoulli Hash Function (BHF) is a hash-based construction that implements **Bernoulli sets** (approximate sets with FPR/FNR) and **Bernoulli maps** (approximate key-value maps). The set is the special case where value bit-length μ=0.

Key results:
- **Generalized acceptance predicate**: threshold test `h(x‖b) mod N ≤ t` generalizes the equality test `h(x‖b) = h₀`. Gives finer FPR granularity and eliminates subset enumeration when FNR > 0.
- **Information-theoretic optimality**: achieves the space lower bound of `−log₂ε + μ` bits per element.
- **Maximum entropy**: the salt is drawn from the distribution that maximizes entropy subject to the space constraint.

## Key Conceptual Distinction

**Model order vs. parameter count**: The BHF satisfies the Bernoulli axioms, so its error behaviour is fully characterized by 2 parameters (FPR and FNR) regardless of how many hash evaluations are composed internally. Element-wise independence forces the joint confusion matrix of multiple tests to factor as a Kronecker product, so composing BHF instances (e.g., via set union) yields tractable formulas with linearly many parameters, not exponentially many. See `bernoulli_sets/` Remark on parametric parsimony.

## Companion Papers

This paper cites but does not re-derive the Bernoulli set/map ADT definitions:
- `bernoulli_sets/` — Bernoulli set algebra (FPR/FNR model, set operations, error propagation)
- `bernoulli_maps/` — Bernoulli map algebra (approximate key-value maps)
- `bernoulli_data_type/` — Type-theoretic generalization

These live in the parent directory `../` of the original working location.

## Build

```bash
make          # pdflatex + bibtex + pdflatex + pdflatex
make clean    # remove build artifacts
```

## File Layout

| File | Purpose |
|------|---------|
| `main.tex` | Document root — preamble, package loading, section includes |
| `defs.tex` | Paper-specific macros: `\PDF`, `\MakeBHF`, `\Contains`, `\Find`, `\sampler`, algorithm keywords |
| `alex.sty` | Unified notation package from `bernoulli_sets/` — `\ASet`, `\fprate`, `\fnrate`, theorem envs |
| `gloss.tex` | Glossary entries |
| `references.bib` | Bibliography |

### Sections (in order)

| # | File | Content |
|---|------|---------|
| 1 | `sections/intro.tex` | Three contributions, relation to companions |
| 2 | `sections/prelim.tex` | Bit strings, hash functions, random oracle, Bernoulli set/map definitions |
| 3 | `sections/shf.tex` | **Centerpiece** — acceptance predicates (equality vs threshold), success probability, FPR granularity, simplified search |
| 4 | `sections/construction.tex` | Algorithms: MakeBHF (both predicates), Contains, Find |
| 5 | `sections/space.tex` | Space complexity proof (general for maps, set as μ=0 corollary) |
| 6 | `sections/entropy.tex` | Max entropy, salt bit-length PMF, cardinality estimation, entropy-space tradeoff |
| 7 | `sections/prob_model.tex` | FP/FN distributions (cites companions for full treatment) |
| 8 | `sections/operations.tex` | Intersection/union convergence on BHF instances |
| 9 | `sections/discussion.tex` | Obliviousness, comparison with Bloom/PHF, encrypted search |
| A | `sections/appendix.tex` | Bit-length sampler, PMF derivation details |

## Notation

Uses `alex.sty` with options `[fancy,section]`. Key macros:
- `\ASet{S}`, `\PASet{S}`, `\NASet{S}` — approximate / positive-approximate / negative-approximate sets
- `\fprate`, `\fnrate`, `\tprate`, `\tnrate` — error rates
- `\Prob`, `\Expect`, `\Var`, `\Entropy` — probability operators
- `\PDF{p}[X]` — PMF notation (defined in `defs.tex`, not in `alex.sty`)

## History

This paper was consolidated from two earlier drafts:
- `oblivious_set_singular_hash_set/` — the Singular Hash Set (complete, ~19 pages)
- `oblivious_map_singular_hash_map_1_/` — the Singular Hash Map (incomplete)

The "Singular Hash" name was replaced with "Bernoulli Hash" because the generalized threshold predicate is no longer singular (one hash target). The "oblivious" notation was replaced with Bernoulli notation from `alex.sty`.
