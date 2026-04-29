# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Monorepo for **Bernoulli type theory** by Alexander Towell: a probabilistic
framework for *random approximate sets, maps, relations, and algebraic types*
with quantifiable false-positive / false-negative error rates. Bloom filters,
perfect hash filters, encrypted search, and approximate relational algebra are
all special cases.

The repo holds two co-developed trees:

| Path | Role | Remote |
|---|---|---|
| `papers/` | 9 academic papers (LaTeX) plus a `pdf-archive/` of superseded drafts. Each paper is its own git subtree. | One remote *per paper* (see below) |
| `bernoulli-cpp/` | Header-only C++17 reference library (`bernoulli<T>` template, Bloom filter, perfect hash variants). Also a git subtree. | `bernoulli-cpp` |
| `book/` | Pedagogical monograph (LaTeX, book class) under active drafting. See `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`. | (subtree migration deferred) |
| `python/` | Teaching-oriented Python companion library (`bernoulli` package). | (subtree migration deferred) |
| `bernoulli_data_type.zip` | Legacy frozen archive of the original `bernoulli_data_type` repo before split. Do not edit. | (none) |

Theory and implementation are mutually informing: the papers define the model
(axioms, error propagation, space-accuracy duality), the C++ library is the
reference implementation. Currently the **theory documentation is much more
mature than the C++ code**. See "C++ Library Status" below.

## Routing: Where to Start

- **"Work on paper X"** or **questions about LaTeX, notation, citations, paper structure** → read `papers/CLAUDE.md` first (188 lines, covers all 9 papers, notation systems, build commands, cross-paper topic placement, conceptual layering, the Five Core Principles, terminology). Then read that paper's own `CLAUDE.md` (7 of 9 papers have one).
- **"Work on the C++ library"** or **questions about `bernoulli<T>`, `bloom_filter.hpp`, header structure** → read `bernoulli-cpp/README.md` and `bernoulli-cpp/docs/mainpage.md`.
- **"Push paper X to its standalone GitHub repo"** → see "Subtree Workflow" below.
- **"Where does topic Y belong?"** → `papers/CLAUDE.md` has a Cross-Paper Topic Placement table; that is authoritative.
- **"Work on the textbook"** or **questions about chapter prose, the build, the Python companion library** → read `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md` for the full design, then `book/README.md` and `python/README.md` for build commands.

## C++ Library Status

The library at `bernoulli-cpp/` is **under active reorganization and does not
currently compile**. `BUILD_TESTING` defaults to OFF, and `tests/CMakeLists.txt`
is a placeholder. The five test sources (`test_hash_set.cpp`,
`test_hash_map.cpp`, `test_bernoulli_value.cpp`,
`test_bernoulli_relation.cpp`, `utils.hpp`) are present but not wired up.

Treat broken builds here as expected scaffolding state, not a regression. If
you re-enable tests, do so deliberately rather than as a side effect of
"fixing" CMakeLists.

### Build (documentation works; compilation is the WIP)

```bash
cd bernoulli-cpp
cmake -S . -B build
cmake --build build --target docs        # Doxygen → build/docs/html/index.html
cmake --build build                      # builds the INTERFACE library (header-only, no objects)
```

To attempt the disabled tests once compilation is fixed:

```bash
cmake -S . -B build -DBUILD_TESTING=ON
cmake --build build
ctest --test-dir build
```

### Header layout

`bernoulli-cpp/include/bernoulli/` is the single public header tree (header-only,
C++17). Key entry points:

- `bernoulli_bool.hpp`: the atomic Bernoulli type (`bernoulli<bool>`)
- `bernoulli_set.hpp`, `bernoulli_set_concept.hpp`, `bernoulli_set_expressions.hpp`: approximate sets
- `bernoulli_map.hpp`: approximate maps (most general type)
- `bernoulli_relation.hpp`: approximate relations
- `bernoulli_value.hpp`: values with error
- `bloom_filter.hpp`, `entropy_bloom_filter.hpp`, `space_optimal_bloom_filter.hpp`: concrete approximate-set implementations
- `hash_set.hpp`, `hash_map.hpp` (+ `*_builder.hpp`): perfect-hash-based variants
- `bool_coder.hpp`, `random_bernoulli_bool.hpp`, `random_binary_perf.hpp`, `rate_span.hpp`: supporting machinery
- `detail/`: internal helpers

The Doxygen documentation pages in `bernoulli-cpp/docs/pages/` (`bernoulli_bool.md`,
`bernoulli_set.md`, `bernoulli_map.md`, `bernoulli_model.md`, `codec.md`,
`noisy_logic.md`, `regular_type.md`) are the conceptual entry points and are
the most useful starting reading even though tests don't yet build.

## Papers

Build pattern (default for most papers):

```bash
cd papers/<paper_dir> && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

Exceptions (`bernoulli-hash-function/` has a `Makefile`; `bernoulli-phf/paper/`
needs `-shell-escape` and `makeglossaries`) are documented in `papers/CLAUDE.md`.

Papermill state for the collection lives at `papers/.papermill/state.md`, with
per-paper state under `papers/<paper>/.papermill/state.md`.

## Subtree Workflow

Each top-level component has a dedicated GitHub remote. From the monorepo
root (`/home/spinoza/github/bernoulli`):

```bash
git remote -v        # full list
```

Current remotes (prefix → upstream repo):

| Remote | Prefix | GitHub |
|---|---|---|
| `origin` | (root) | `queelius/bernoulli` |
| `bernoulli-cpp` | `bernoulli-cpp` | `queelius/bernoulli-cpp` |
| `bernoulli-sets` | `papers/bernoulli_sets` | `queelius/bernoulli_sets` |
| `bernoulli-composition` | `papers/bernoulli_composition` | `queelius/bernoulli_composition` |
| `bernoulli-classification` | `papers/bernoulli_classification_measures` | `queelius/bernoulli_classification_measures` |
| `bernoulli-entropy` | `papers/bernoulli_entropy` | `queelius/bernoulli_entropy` |
| `bernoulli-hash` | `papers/bernoulli-hash-function` | `queelius/bernoulli-hash-function` |
| `bernoulli-phf` | `papers/bernoulli-phf` | `queelius/bernoulli-phf` |
| `bernoulli-maps` | `papers/bernoulli_maps` | `queelius/bernoulli_maps` |
| `bernoulli-relations` | `papers/bernoulli_relations` | `queelius/bernoulli_relations` |
| `bernoulli-data-type` | `papers/bernoulli_data_type` | `queelius/bernoulli_data_type` |

Push a single subtree's changes upstream:

```bash
git subtree push --prefix=papers/bernoulli_sets bernoulli-sets main
git subtree push --prefix=bernoulli-cpp        bernoulli-cpp    main
```

Pull updates the other direction:

```bash
git subtree pull --prefix=papers/bernoulli_sets bernoulli-sets main --squash
```

**Naming gotcha:** remote names use hyphens (`bernoulli-sets`); most paper
*directory* names use underscores (`bernoulli_sets`). The hyphenated paper
directories (`bernoulli-hash-function/`, `bernoulli-phf/`) match their remotes
exactly. Don't assume the directory name and remote name agree.

## How Theory and Implementation Map

| Paper | Implements as |
|---|---|
| `bernoulli_sets/` (axioms, FPR/FNR, higher-order composition) | `bernoulli_set.hpp`, `bernoulli_bool.hpp` |
| `bernoulli_composition/` (set-operation error propagation) | `bernoulli_set_expressions.hpp` |
| `bernoulli_classification_measures/` (PPV, NPV, Youden's J) | not yet implemented |
| `bernoulli_entropy/` (information-theoretic lower bound) | `entropy_bloom_filter.hpp` |
| `bernoulli-hash-function/` (space-optimal BHF construction) | `space_optimal_bloom_filter.hpp`, `hash_set.hpp`, `hash_map.hpp` |
| `bernoulli-phf/` (perfect hash filter; has its own embedded `maph` library) | `hash_set.hpp`, `hash_map.hpp` (+ `papers/bernoulli-phf/src/`) |
| `bernoulli_maps/` (approximate function spaces) | `bernoulli_map.hpp` |
| `bernoulli_relations/` (approximate relational algebra) | `bernoulli_relation.hpp` |
| `bernoulli_data_type/` (algebraic types, `bernoulli<T>` ADT) | header-only library overall |

## Connection to Trapdoor Computing

The Bernoulli framework is the *error model* for the trapdoor computing
paradigm (sibling repo at `~/github/trapdoor-computing/`). At the
mathematical level: **Bernoulli maps are cipher maps**. The BHF salt is the
trapdoor key, the acceptance predicate implements the cipher map, and the
space formula `−log₂(ε) + μ` governs both. The composition theorem
`η_total = 1 − ∏(1 − η_i)` is Property 4 of cipher maps. When working on a
paper here that touches obliviousness, encryption, or perfect filters, expect
to also reference or update files in the trapdoor-computing tree.

## Things Not To Edit

- `bernoulli_data_type.zip`: legacy snapshot of the pre-split repo, archival only.
- `papers/pdf-archive/`: compiled PDFs of superseded drafts (e.g., `bernoulli_sets_higher_order.pdf`). Read for reference, do not regenerate.
- LaTeX build artifacts inside paper directories (`main.aux`, `main.log`, `main.bbl`, `main.pdf`, `_minted-*/`, `main.synctex.gz`). These are covered by per-paper `.gitignore`s; never `git add` them.
