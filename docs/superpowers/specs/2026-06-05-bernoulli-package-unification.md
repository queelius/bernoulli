# Spec: Bernoulli Python Package Unification

**Date:** 2026-06-05
**Author:** Alexander Towell
**Status:** Planning (approved direction; Stage 0 ready to execute)

## Problem

Three directories in the monorepo all claim to be "the Bernoulli code," and two of them ship a Python package literally named `bernoulli` with different public APIs:

- `bernoulli-cpp/` (348K): the original header-only C++17 reference (full model, mature Doxygen design docs) that currently does not compile.
- `python/` (575M, almost all `.venv`): a 40-line placeholder package (`Bernoulli(value=True)`) plus 15 valuable book-companion notebooks.
- `src/bernoulli/` (103M, mostly `.venv`): the genuine package, about 2,800 LOC, 440 passing tests (ruff + mypy strict clean), 16 validation experiments, a phased roadmap (`PHASING.md`), zero runtime deps, and a planned cffi C core (`c/` is currently a README only).

The notebooks `import bernoulli` and therefore bind to the stub, not the real package. Three separate virtualenvs and a non-compiling C++ tree complete the tangle.

## Decisions (locked)

1. **One layered package.** A stable core API for the PyPI audience; the notebooks import that same API for the book-companion audience; `experiments/` sits on top as the internal research layer and is free to churn. API discipline wins ties.
2. **Archive the C++ tree.** `bernoulli-cpp/` is retired (moved to `archived/`). Its headers and design docs remain a port source for the C core, but it is no longer a build or release target. (`maph` stays the active C++ research sandbox.)
3. **Full build-out.** Consolidate AND execute roadmap Phases 2 to 5 plus the cffi C core. Multi-session.
4. **Promote to a clean top-level project dir**, replacing both `src/` and `python/`.

## Names

| Role | Name | Notes |
|---|---|---|
| Monorepo project dir | `bernoulli-py/` | Parallels `bernoulli-cpp/`. |
| PyPI distribution | `bernoulli-types` | Available; on-brand (book title, "random approximate types"). The bare `bernoulli` is taken on PyPI. |
| Import / package | `bernoulli` | Unchanged, so existing code/tests/notebooks/experiments do not move. `pip install bernoulli-types` then `import bernoulli`. |

Fallbacks (free on PyPI) if install-name == import-name is preferred: `pybernoulli`, `bernoulli-framework` (both would change the import name and incur churn).

## Target layout

```
bernoulli-py/
├── pyproject.toml        # name="bernoulli-types", packages=["bernoulli"], deps=[],
│                         #   extras: [c] (cffi), [notebooks], [dev]
├── README.md  PHASING.md  LICENSE  CHANGELOG.md
├── src/bernoulli/        # the package (src-layout, import name bernoulli)
│   ├── atom.py  algebra.py  measures.py  harness.py
│   ├── sets/  maps/  sketches/  relations/  estimators/  algorithms/
│   └── _c/               # cffi loader + pure-Python fallback dispatch
├── c/                    # plain-C hot paths (portable, manylinux/macos friendly)
├── tests/                # hypothesis + the existing 440 tests
├── experiments/          # the 16 validation experiments + SYNTHESIS (research layer)
└── notebooks/            # the 15 book-companion notebooks, importing the real bernoulli
```

`python/` and `src/` are removed; `bernoulli-cpp/` moves to `archived/bernoulli-cpp/`. The three `.venv`s collapse to one.

## Stage 0: Consolidate (do first, one reviewable unit)

Pure housekeeping, but it carries the only real risk (notebook rewiring), so it lands before any feature work and is independently valuable (it makes the notebooks real and kills the duplicate-package confusion today).

0.1 **Audit the notebooks** (done). Result: 14 of 15 notebooks are entirely self-contained. Each hand-rolls the very structures the package ships (`BloomFilter`, `HyperLogLog`, `MinHash`, `CountMin`, `miller_rabin`, `BHF`, `BPHF`, PPV/NPV) on numpy/scipy/matplotlib/hashlib/sympy, and imports nothing from either package. Only `ch02` imports the package, inside a `try/except ImportError` that sets a `_BERNOULLI_AVAILABLE` flag and never calls the symbol (and it imports `Bernoulli`, the stub name; the real package exports `BernoulliBool`). So getting the notebooks to RUN under the new layout is trivial (0.4). The substantive notebook work, making them demonstrate the library instead of re-implementing it, is per-phase Build-out, not Stage 0 (see Notebooks below).

0.2 **Create `bernoulli-py/`** by promoting `src/bernoulli/`: `git mv` its `src/bernoulli/` package, `tests/`, `experiments/`, `c/`, `pyproject.toml`, `PHASING.md`, `README.md`, `LICENSE` up and out of the double-nesting.

0.3 **Set the PyPI name** in `pyproject.toml` to `bernoulli-types` (keep `packages`/import as `bernoulli`); add a `CHANGELOG.md`; confirm extras `[c]`, `[notebooks]`, `[dev]`.

0.4 **Move the notebooks** (`python/notebooks/`) into `bernoulli-py/notebooks/`. Per the 0.1 audit this is nearly a no-op for execution: 14 run unchanged, and `ch02` needs a one-line `Bernoulli` -> `BernoulliBool` rename so its availability flag stays honest. Confirm every notebook executes end to end. Making the notebooks actually import and demonstrate the package is deferred to per-phase Build-out (Notebooks, below); it is not required for Stage 0.

0.5 **Delete the `python/` stub** package (`core.py`, the placeholder); salvage anything else in `python/` worth keeping (its `notebooks/README.md`, LICENSE).

0.6 **Archive `bernoulli-cpp/`** to `archived/bernoulli-cpp/`. It is a git subtree (remote `bernoulli-cpp` -> `queelius/bernoulli-cpp`); leave the remote configured but unused and note the retirement in CLAUDE.md (no destructive history surgery).

0.7 **One venv, clean ignores.** Collapse to `bernoulli-py/.venv`; confirm `.gitignore` covers `.venv/`, `.mypy_cache/`, `.ruff_cache/`, `.coverage`, `__pycache__/`, `*.so`, cffi build artifacts.

0.8 **Update the docs of record:** the monorepo `CLAUDE.md` (Repository Overview, the python/src/bernoulli-cpp rows, the subtree table), the textbook design spec `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`, and any `book/` references to `python/` or `bernoulli-cpp/`.

0.9 **Green gate:** `pytest` (the 440 tests) passes under the new layout; `ruff check` and `mypy --strict` clean; every notebook executes top to bottom; the book still builds.

**Stage 0 exit:** one project dir, one package, notebooks importing the real package, C++ archived, one venv, docs consistent.

## Stages 1 to 5: Build-out

The package is further along than `PHASING.md` claims (it says Phases 2 to 5 are "scaffolded"; in fact several concretes already exist), so each phase is finish + harden + C-accelerate + notebook-integrate, not greenfield. Current state per phase:

| Phase | Book | Exists today | To do |
|---|---|---|---|
| 1 Atom | I (1 to 4, 7) | atom, algebra, measures (done, 0.2.0) | verify under new layout |
| 2 Sets | II (5 to 6, 8) | sets/{bloom, cascade, correlated_bloom} | composition, entropy_bound; first C (bit array, hashing, k-hash); hypothesis tests; ch5/6/8 notebook parity |
| 3 Maps & codecs | III (9), IV (14 to 15) | maps/{codec (706 LOC), protocol} | PerfectHashFunction, ApproximateMap, PerfectFilter, RibbonRetrieval, EncodedRetrieval; C (GF(2) elimination, ribbon ops, PHF eval); ch9/14/15 notebooks |
| 4 Relations | III (12) | (none) | relations/{BernoulliRelation, algebra}: select/project/join with rate propagation; ch12 notebook |
| 5 Sketches | III (10 to 11) | sketches/hyperloglog | CountMin, MinHash; estimators/{MillerRabin recast, LasVegas, MonteCarlo}; C (counters, registers, permutations); ch10/11 notebooks |

Each phase ships the existing six-point discipline (Protocol; >=1 concrete impl; pure-Python first, C second; hypothesis property tests; worked examples matching the book chapter; a benchmark harness reusable from notebooks and experiments). No phase is done without all six.

## C-core track (cross-cutting, lands alongside Phases 2+)

- **cffi, api mode**, opt-in via `pip install bernoulli-types[c]`. Pure-Python fallbacks for every operation so `pip install bernoulli-types` succeeds without a C toolchain; `[c]` compiles and binds the accelerated paths. A single `_c.so`; the rest stays pure Python.
- **Plain C, not C++ bindings.** Portable C source in `c/`, compiling everywhere for manylinux/macos wheels. Algorithmic ideas port from `bernoulli-cpp` and `maph`; bindings do not.
- **Per-phase hot paths:** Phase 2 bit array/hashing; Phase 3 GF(2)/ribbon/PHF; Phase 5 counters/registers/permutations.
- A `_c/` dispatch layer in the package selects the C implementation when present, else the Python fallback, behind one stable Python API.

## Cross-cutting concerns

- **API layering (the "balance" decision).** The public surface (`from bernoulli import ...`, the documented submodules) is semver'd and stable for PyPI users. Notebooks import only the public surface. `experiments/` may reach into internals and churn freely; it is not part of the public contract.
- **Notebooks demonstrate the package, they do not re-implement it.** Today the 15 companion notebooks each hand-roll the structures the package ships (ch5/6/16 a local `BloomFilter`, ch10 a local `HyperLogLog`, ch3/11 a local Miller-Rabin, ch7 local PPV/NPV), with different internals (notebooks use hashlib/sha; the package uses FNV-1a plus Kirsch-Mitzenmacher double hashing). They run, but they are drifting copies that never exercise the library. The target, per the package README's stated intent, is that as each phase lands the corresponding chapter notebooks are rewritten to import and showcase the real symbol (`from bernoulli.sets import BloomFilter`), so the companion demonstrates the package and the two cannot silently diverge. This is per-phase work, gated by an execute-every-notebook CI job and, where cheap, an assertion that the notebook's numbers match the library's. (Open sub-decision: a reader can today run any chapter with zero installs because the notebooks are standalone; moving to import-the-library trades that for a true companion. Recommended: demonstrate the library, since the package is meant to be the executable companion, but keep each notebook's opening cell self-contained enough to read.)
- **Release.** Tag-driven build of sdist + manylinux/macos wheels (cffi) to PyPI as `bernoulli-types`. `CHANGELOG.md`, semver, `py.typed`.
- **CI.** test + ruff + mypy strict on pure-Python; a separate job that builds `[c]` and runs the same tests against the C paths; an "execute every notebook" job (nbmake or papermill) so book parity cannot silently rot.
- **Subtree.** After Stage 0, optionally give `bernoulli-py/` its own remote (e.g. `queelius/bernoulli-types`) for standalone development and PyPI CI, mirroring the per-component subtree pattern in CLAUDE.md.

## Risks

- **Notebook divergence, not notebook breakage.** The 0.1 audit retired the feared rewire risk: the notebooks are self-contained and run regardless of the package, so Stage 0 is safe. The real risk is the inverse, the notebooks and the package are parallel, drifting implementations of the same structures, and a companion that re-implements rather than demonstrates the library can fall out of sync. Mitigation is the per-phase notebook rewrite plus the execute-every-notebook CI job (see Notebooks).
- **Hidden coupling to `src/bernoulli/`'s nesting.** Imports, `pyproject` paths, and the experiments' `sys.path` assumptions may hardcode the old location; the green gate (0.9) catches these.
- **C portability.** Keeping the core pure-Python-first with fallbacks means a broken C toolchain never blocks `pip install`; this is a discipline to hold, not a one-time task.

## Sequencing

Stage 0 as one unit (it stands alone and de-risks the rest), then Phases 2 to 5 one phase per work session, with the C-core hot paths landing inside each phase. Each phase is independently shippable as a minor release of `bernoulli-types`.
