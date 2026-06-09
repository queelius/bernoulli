# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Monorepo for **Bernoulli type theory** by Alexander Towell: a probabilistic
framework for *random approximate sets, maps, relations, and algebraic types*
with quantifiable false-positive / false-negative error rates. Bloom filters,
perfect hash filters, encrypted search, and approximate relational algebra are
all special cases.

The repo holds these co-developed trees:

| Path | Role | Remote |
|---|---|---|
| `papers/` | 9 academic papers (LaTeX) plus a `pdf-archive/` of superseded drafts. Each paper is its own git subtree. | One remote *per paper* (see below) |
| `book/` | Pedagogical monograph (LaTeX, book class). See `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`. | (subtree migration deferred) |
| `bernoulli-py/` | The Python package: import name `bernoulli`, PyPI distribution `bernoulli-types`. The reference implementation (research artifact + PyPI library) and the book's executable companion (`notebooks/`). See `bernoulli-py/README.md` and `PHASING.md`. | (subtree migration deferred) |
| `archived/bernoulli-cpp/` | Retired header-only C++17 reference (does not compile). Kept as a design reference and port source for the planned C core; not built or released. Still a git subtree. | `bernoulli-cpp` |
| `bernoulli_data_type.zip` | Legacy frozen archive of the original `bernoulli_data_type` repo before split. Do not edit. | (none) |

Theory and implementation are mutually informing: the papers define the model
(axioms, error propagation, space-accuracy duality), and `bernoulli-py/` is the
reference implementation. The unification that promoted `bernoulli-py/` (from
the former `src/bernoulli/` and `python/` trees) and archived the C++ is
specified in `docs/superpowers/specs/2026-06-05-bernoulli-package-unification.md`.

## Routing: Where to Start

- **"Work on paper X"** or **questions about LaTeX, notation, citations, paper structure** → read `papers/CLAUDE.md` first (188 lines, covers all 9 papers, notation systems, build commands, cross-paper topic placement, conceptual layering, the Five Core Principles, terminology). Then read that paper's own `CLAUDE.md` (7 of 9 papers have one).
- **"Work on the Python package"** or **questions about `bernoulli.atom`, `BernoulliBool`, the phases, the C core** → read `bernoulli-py/README.md` and `bernoulli-py/PHASING.md`. The retired C++ reference is at `archived/bernoulli-cpp/` (design reference / port source only).
- **"Push paper X to its standalone GitHub repo"** → see "Subtree Workflow" below.
- **"Where does topic Y belong?"** → `papers/CLAUDE.md` has a Cross-Paper Topic Placement table; that is authoritative.
- **"Work on the textbook"** or **questions about chapter prose, the build, the companion notebooks** → read `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md` for the full design, then `book/README.md` for the LaTeX build and `bernoulli-py/README.md` for the package and its `notebooks/`.

## Python Package (`bernoulli-py/`)

The single Python tree. Import name `bernoulli`; PyPI distribution name
`bernoulli-types` (the bare `bernoulli` is taken on PyPI). Zero runtime
dependencies; optional plain-C acceleration via cffi (the `[c]` extra) with
pure-Python fallbacks. Built atom-outward in phases mirroring the book's five
parts; see `bernoulli-py/PHASING.md`. Status: alpha 0.2.0 (Phase 1, the atom,
complete; sets / maps / sketches partially landed).

Layout: `src/bernoulli/` (the package, src-layout), `tests/` (pytest +
hypothesis), `experiments/` (16 validation experiments, the research layer),
`notebooks/` (15 book-companion notebooks), `c/` (C hot paths, Phase 2+).

### Build and verify

```bash
cd bernoulli-py
uv venv
VIRTUAL_ENV="$PWD/.venv" uv pip install -e ".[dev]"   # package + pytest/ruff/mypy/hypothesis
.venv/bin/pytest          # the test suite (currently green: 0 failures)
.venv/bin/ruff check src tests
.venv/bin/mypy            # strict, clean across the source tree
```

Extras: `[dev]` (test/lint/type), `[notebooks]` (jupyter, numpy, scipy,
matplotlib, sympy), `[c]` (cffi, Phase 2+).

### Archived C++ reference

The original header-only C++17 library is retired at `archived/bernoulli-cpp/`.
It does not compile and is not built or released; it is kept as a design
reference and as the port source for the planned plain-C core (algorithmic
ideas port; the C++ bindings do not). `maph` (`~/github/repos/maph/`) is the
active C++ research sandbox.

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
| `bernoulli-cpp` | `archived/bernoulli-cpp` (retired) | `queelius/bernoulli-cpp` |
| `bernoulli-sets` | `papers/bernoulli_sets` | `queelius/bernoulli_sets` |
| `bernoulli-composition` | `papers/bernoulli_composition` | `queelius/bernoulli_composition` |
| `bernoulli-classification` | `papers/bernoulli_classification_measures` | `queelius/bernoulli_classification_measures` |
| `bernoulli-entropy` | `papers/bernoulli_entropy` | `queelius/bernoulli_entropy` |
| `bernoulli-hash` | `papers/bernoulli-hash-function` | `queelius/bernoulli-hash-function` |
| `bernoulli-phf` | `papers/bernoulli-phf` | `queelius/bernoulli-phf` |
| `bernoulli-maps` | `papers/bernoulli_maps` | `queelius/bernoulli_maps` |
| `bernoulli-relations` | `papers/bernoulli_relations` | `queelius/bernoulli_relations` |
| `bernoulli-data-type` | `papers/bernoulli_data_type` | `queelius/bernoulli_data_type` |
| `bernoulli-quantum-readout` | `papers/bernoulli-quantum-readout` | `queelius/bernoulli-quantum-readout` |

Push a single subtree's changes upstream:

```bash
git subtree push --prefix=papers/bernoulli_sets bernoulli-sets main
git subtree push --prefix=archived/bernoulli-cpp bernoulli-cpp main   # retired
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

| Paper | Implements as (`bernoulli-py/src/bernoulli/`) |
|---|---|
| `bernoulli_sets/` (axioms, FPR/FNR, higher-order composition) | `atom.py` (BernoulliBool), `algebra.py`, `sets/` |
| `bernoulli_composition/` (set-operation error propagation) | `sets/` composition (Phase 2) |
| `bernoulli_classification_measures/` (PPV, NPV, Youden's J) | `measures.py` |
| `bernoulli_entropy/` (information-theoretic lower bound) | `sets/` entropy bound (Phase 2) |
| `bernoulli-hash-function/` (space-optimal BHF construction) | `maps/` perfect filter (Phase 3) |
| `bernoulli-phf/` (perfect hash filter; embedded `maph`) | `maps/` (Phase 3) |
| `bernoulli_maps/` (approximate function spaces) | `maps/` protocols, `maps/codec.py` |
| `bernoulli_relations/` (approximate relational algebra) | `relations/` (Phase 4) |
| `bernoulli_data_type/` (algebraic types, `bernoulli<T>` ADT) | the package overall |

The retired C++ headers (`archived/bernoulli-cpp/include/bernoulli/*.hpp`) are
the original reference implementations of these results, kept as a port source.

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
- `archived/`: retired components (e.g. `archived/bernoulli-cpp/`). Read for reference; do not revive or regenerate without a decision.
- `papers/pdf-archive/`: compiled PDFs of superseded drafts (e.g., `bernoulli_sets_higher_order.pdf`). Read for reference, do not regenerate.
- LaTeX build artifacts inside paper directories (`main.aux`, `main.log`, `main.bbl`, `main.pdf`, `_minted-*/`, `main.synctex.gz`). These are covered by per-paper `.gitignore`s; never `git add` them.
