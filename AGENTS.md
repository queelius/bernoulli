# Working in the Bernoulli workspace

## Purpose

This is the central integration repository for Alexander Richard Towell's
**Bernoulli model**: a framework for random approximate values, sets, maps,
relations, and algebraic types with explicit error models. The papers develop
the theory; the Python package implements it; the book connects the theory,
applications, and executable examples. Treat these as related research projects
whose definitions and results must remain consistent.

The checkout is a single Git repository. Individual papers and the retired C++
library are incorporated as **Git subtrees**, with standalone upstream repos.
The book and Python package currently live directly in this repository.

## Navigation and existing guidance

Read [CLAUDE.md](CLAUDE.md) for the detailed workspace overview. Before editing a
component, read its local `AGENTS.md` if present and its existing `CLAUDE.md` or
README. Apply the most specific applicable guidance within that component.

| Area | Location and starting points |
|---|---|
| Research papers | `papers/`; start with [papers/CLAUDE.md](papers/CLAUDE.md), then the paper's own guidance. The collection guide defines notation, topic ownership, and build exceptions. |
| Paper status | `papers/.papermill/state.md` and each paper's `.papermill/state.md`, where present. Read these for recorded status and update relevant state after substantive paper work. |
| Python implementation | `bernoulli-py/src/bernoulli/`; configuration in `bernoulli-py/pyproject.toml`, roadmap in `bernoulli-py/PHASING.md`. Distribution name: `bernoulli-types`; import name: `bernoulli`. |
| Tests and experiments | `bernoulli-py/tests/`, `bernoulli-py/experiments/`; experiment reports and `SYNTHESIS.md` preserve research findings. |
| Book and notebooks | `book/book.tex`, `book/README.md`, `book/Makefile`, and `bernoulli-py/notebooks/`. Design and review records live under `docs/superpowers/`. |
| Provenance and publication metadata | `docs/PROVENANCE.md`, `docs/zenodo/`, and component `CITATION.cff`, `.zenodo.json`, and `LICENSE` files. |
| Historical material | `archived/bernoulli-cpp/`, `bernoulli_data_type.zip`, and PDF archives. Reference material, not active implementation targets. |

Paper directories cover the following domains:

| Directory under `papers/` | Subject |
|---|---|
| `bernoulli_sets/` | Foundational set model, axioms, and error distributions |
| `bernoulli_composition/` | Set operations, error propagation, and uncertain rates |
| `bernoulli_classification_measures/` | Classification measures induced by approximate sets |
| `bernoulli_entropy/` | Entropy and space lower bounds |
| `bernoulli-hash-function/` | Bernoulli hash construction and space optimality |
| `bernoulli-phf/` | Perfect hash filters; manuscript root is `paper/main.tex` |
| `bernoulli_maps/` | Approximate maps and their algebra |
| `bernoulli_relations/` | Approximate relations and relational operations |
| `bernoulli_data_type/` | Two manuscripts: `bernoulli_model/` and `algebraic_types/` |
| `bernoulli-quantum-readout/` | Quantum readout errors and classical post-processing |

Some older READMEs and plans predate consolidation. The active Python tree is
`bernoulli-py/`, including its notebooks; old root-level `python/` and
`src/bernoulli/` paths are obsolete. Check actual source and configuration before
repeating implementation status, counts, or build claims from historical docs.
The package-unification decisions are recorded in
`docs/superpowers/specs/2026-06-05-bernoulli-package-unification.md`.

## Research and implementation principles

- Preserve the distinction between an exact object, its random approximation,
  an observed realization, and the parameters describing its errors.
- State independence and conditioning assumptions when deriving or implementing
  composition formulas. Marginal error rates alone do not establish independence.
  Distinguish exact identities, conservative bounds, and empirical estimates.
- Keep **model order** (partition blocks) distinct from **k-fold composition**
  (repeated application) and from the number of free parameters.
- Follow the Boolean foundation through sets, maps, relations, and algebraic
  types. Keep proofs, implementation behavior, examples, and notation aligned;
  use the cross-paper topic table instead of duplicating results arbitrarily.
- Use the local LaTeX notation system: some papers use `alex.sty`, others modular
  `sty/` packages. Reuse existing macros rather than introducing parallel notation.
- In related security work, use **trapdoor computing** for the paradigm and
  **cipher** for constructs. Preserve established external terms such as ORAM
  and oblivious transfer. Related work lives in `~/github/trapdoor-computing/`;
  the C++ research sandbox is `~/github/repos/maph/`.
- Prefer principled, scalable solutions: typed interfaces and protocols,
  structured data and parsers, and behavior derived from structure. Avoid regex
  parsing of structured data, stringly typed interfaces, and manually maintained
  feature lookup tables.
- Keep the Python core usable without optional dependencies. The planned C
  acceleration is optional and must retain pure-Python fallbacks; roadmap prose
  is not evidence that a C backend already exists.

## Validation

Run unit and integration tests for code changes, add tests for new features, and
inspect coverage for missing cases. The Python tests share one pytest suite;
there is no separately configured integration-test target. Include property
tests for algebraic laws and reproducible statistical checks where appropriate.
Exercise limiting cases such as zero error and rates at parameter boundaries.

Run these commands from `bernoulli-py/`. Reuse `.venv` when present; for initial
setup, create it with `uv venv` and install development dependencies with
`VIRTUAL_ENV="$PWD/.venv" uv pip install -e ".[dev]"`.

```bash
.venv/bin/python -m pytest --cov=bernoulli --cov-branch --cov-report=term-missing
.venv/bin/ruff check src tests
.venv/bin/mypy
```

Test, lint, and type-check settings live in `pyproject.toml`. Run affected
experiments or companion notebooks when changing the results or examples they
support; they are not automatically covered by pytest. Report the commands
actually run and any failures or unverified claims.

For manuscript changes, build the affected document and inspect unresolved
citations, references, and layout:

- Book: `make -C book`; its current Makefile uses `pdflatex` and **biber**.
  `make -C book draft` is a single pass, not a complete bibliography check.
- Bernoulli hash paper: `make -C papers/bernoulli-hash-function`.
- Most other papers: run `pdflatex main.tex`, `bibtex main`, then two more
  `pdflatex main.tex` passes from the manuscript directory.
- Consult `papers/CLAUDE.md` for exceptions: modular styles need
  `TEXINPUTS=".:./sty:"`; the PHF paper needs `-shell-escape` and
  `makeglossaries`; the two data-type manuscripts have separate build roots.
- Keep canonical manuscripts venue-neutral. Derive venue-specific versions
  under `venues/<venue-slug>/` using their local instructions and regeneration
  scripts where available.

## Git, artifacts, and operational work

- Inspect `git status` before editing and preserve unrelated work, including
  existing PDF changes and archive moves. Stage specific intended files.
- Perform subtree operations from this repository's root. Verify the prefix,
  remote, and branch using `git remote -v` and the mapping in `CLAUDE.md`:
  remote names often use hyphens while paper directories use underscores.
  A root push and a subtree push publish to different repositories.
- Preserve archives and the retired C++ tree. Do not regenerate archived drafts
  or revive retired components as part of ordinary maintenance.
- Avoid committing incidental LaTeX outputs, caches, environments, or generated
  binaries. Some PDFs are already tracked; rebuilding does not make those
  changes part of the requested work automatically.
- `docs/PROVENANCE.md` is generated. Update its source manifest in
  `docs/zenodo/generate_metadata.py` and regenerate when changing provenance.
  Check each component's actual license rather than assuming one workspace license.
- Prefer available MCP tools to equivalent CLI operations. Carry out authorized
  operational work with tools; reserve manual steps for actions that actually
  require the user's identity, judgment, or non-trivial expenditure.

## Author identity

Use **Alexander Richard Towell** for new author metadata and Git identity.
**Alexander Towell**, **Alex Towell**, and **queelius** refer to the same person;
pronouns are he/him. Primary email: `lex@metafunctor.com`. ORCID:
`0000-0001-6443-9897`. GitHub: `https://github.com/queelius`. Website:
`https://metafunctor.com`. Institution: Southern Illinois University Edwardsville
(SIUE). Preserve source attribution when quoting or citing existing publications.
