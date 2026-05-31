# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Collection of related research papers by Alexander Towell on **random approximate sets** (Bernoulli sets): a probabilistic framework for modeling sets with quantifiable false positive/negative error rates. Applications include Bloom filters, perfect hash filters, encrypted search, and approximate relational algebra.

## Where to Start

- **"Work on paper X"**: read this file for cross-paper context (notation, topic placement, layering), then read that paper's own `CLAUDE.md` if it has one (7 of 9 do; see the table below). The per-paper file is more specific about section order, current draft state, and section-by-section purpose.
- **"What is the status of paper X?"**: read `papers/.papermill/state.md` (collection-level: thesis, phase, venue per paper) and `<paper>/.papermill/state.md` if it exists (per-paper detail). Do not infer status from git log or by reading the LaTeX.
- **"Where does topic Y belong?"**: use the **Cross-Paper Topic Placement** table below. It is authoritative; do not duplicate content across papers.
- **"How does paper X build?"**: see **Build Commands** below. Most papers use the standard `pdflatex && bibtex && pdflatex && pdflatex` triple. Three deviate (Makefile, shell-escape, sub-paper layout), as noted in the table.
- **"Push paper X upstream"** or subtree workflow: see `../CLAUDE.md` (the parent monorepo file) for the remote-name table and `git subtree push` commands. Do not duplicate that here.

## Papers

| Directory | Title | Status | Notation | Build | CLAUDE.md |
|---|---|---|---|---|---|
| `bernoulli_sets/` | Bernoulli sets: a model for random approximate sets | **Primary, actively maintained** | `alex.sty` (unified) | `pdflatex` manual | yes |
| `bernoulli_composition/` | Composition of Bernoulli sets | **Companion to bernoulli_sets** | `alex.sty` (unified) | `pdflatex` manual | yes |
| `bernoulli_classification_measures/` | Binary classification measures for random approximate sets | **Companion to bernoulli_sets** | `alex.sty` (unified) | `pdflatex` manual | no |
| `bernoulli_entropy/` | Entropy and space complexity of random approximate sets | **Companion to bernoulli_sets** | `alex.sty` (unified) | `pdflatex` manual | no |
| `bernoulli-hash-function/` | The Bernoulli Hash Function: Optimal Bernoulli Sets and Maps | Standalone (~95% complete) | `alex.sty` (unified) | `make` | yes |
| `bernoulli-phf/` | The Perfect Hash Filter | Standalone (early, ~25%) | Modular `sty/` packages | `pdflatex` manual (shell-escape); LaTeX is in `paper/` subdir, not at top level | yes |
| `bernoulli_maps/` | The algebra of the random approximate map model | Standalone (early) | Modular `.sty` packages | `pdflatex` manual | yes |
| `bernoulli_relations/` | The abstract data type of the approximate relation | Standalone (early) | Modular `.sty` packages | `pdflatex` manual | yes |
| `bernoulli_data_type/` | Random approximate values over algebraic types | Standalone (early) | Modular `.sty` packages | two sub-papers, build each separately | yes |

**Structural deviations from the standard layout** (assume the standard pattern and you will look in the wrong place):
- `bernoulli-phf/` is a C++ project that *contains* the paper at `bernoulli-phf/paper/main.tex`. The top-level directory has `include/`, `src/`, `tests/`, `CMakeLists.txt`, etc.
- `bernoulli_data_type/` has no top-level `main.tex`. It contains **two parallel sub-papers**, each a complete LaTeX project: `bernoulli_model/` (foundational framework) and `algebraic_types/` (type-theoretic extension).

### Consolidation History

- `random_approximate_set_model/` was merged into `random_approximate_sets/` (content in `sections/unused/`)
- `bernoulli_sets_higher_order/` was merged into `bernoulli_sets/` (archive.zip preserves originals)
- `bernoulli_sets/` was split into 4 papers (2026): set-theoretic composition extracted to `bernoulli_composition/`, classification measures extracted to `bernoulli_classification_measures/`, entropy/space complexity extracted to `bernoulli_entropy/`. Original `entropy.tex`, `set_theory.tex`, `relational.tex`, `uncertain_rates.tex` remain in `bernoulli_sets/sections/` but are no longer `\input`'d.
- `random_approximate_sets/` was fully superseded by the 4-paper family and deleted (2026-03). Its modular `sty/` packages were copied into each paper that needed them (`bernoulli_maps/sty/`, `bernoulli_relations/sty/`, `bernoulli-phf/paper/sty/`, `bernoulli_data_type/algebraic_types/sty/`). Two minor unique items were the epistemological discussion (~50 lines in `aset_adt.tex`) and a Boolean search application (archived in `bernoulli_sets/sections/unused/bool_search.tex`).

### Deleted Directories

| Directory | When | Reason |
|---|---|---|
| `random_approximate_set_model/` | 2025 | Merged into `random_approximate_sets/` |
| `bernoulli_sets_higher_order/` | 2025 | Merged into `bernoulli_sets/` |
| `random_approximate_sets/` | 2026-03 | Superseded by 4-paper family |

## Build Commands

```bash
# bernoulli_sets (no Makefile)
cd bernoulli_sets && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

# bernoulli_composition (companion to bernoulli_sets)
cd bernoulli_composition && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

# bernoulli_classification_measures (companion to bernoulli_sets)
cd bernoulli_classification_measures && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

# bernoulli_entropy (companion to bernoulli_sets)
cd bernoulli_entropy && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex

# bernoulli-hash-function (has Makefile)
cd bernoulli-hash-function && make

# bernoulli-phf (requires shell-escape, glossaries)
cd bernoulli-phf/paper && pdflatex -shell-escape main.tex && makeglossaries main && bibtex main && pdflatex -shell-escape main.tex && pdflatex -shell-escape main.tex

# All others: same pattern as bernoulli_sets
cd <paper_dir> && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

## Notation Systems

Two notation approaches coexist:

1. **`alex.sty`** (used by `bernoulli_sets/`, `bernoulli_composition/`, `bernoulli_classification_measures/`, `bernoulli_entropy/`, `bernoulli-hash-function/`): Single unified package loaded as `\usepackage[fancy,section]{alex}`. Provides all macros: `\ASet`, `\Set`, `\Card`, `\APFun`, `\fprate`, `\fnrate`, `\tprate`, `\tnrate`, theorem environments, paired delimiters.

2. **Modular `sty/` packages** (used by `bernoulli_maps/`, `bernoulli_relations/`, `bernoulli-phf/`, `bernoulli_data_type/`): Separate files per domain: `setnotation.sty`, `approxsetnotation.sty`, `functionnotation.sty`, `relationnotation.sty`, `envnotation.sty`, etc. Each paper has its own copy in a local `sty/` subdirectory.

Core notation is consistent across both: `\Set{A}` for sets, `\ASet{A}` for approximate sets, `\fprate`/`\fnrate` for error rates, `\RV{X}` for random variables.

## Architecture Pattern

Each paper follows the same structure (see "Structural deviations" above for the two papers that break it):
- `main.tex`: Document root with preamble, package loading, section includes
- `sections/`: One `.tex` file per section (included via `\input{}` or `\subfile{}`)
- `references.bib`: Bibliography
- `img/`: Compiled figures (PDF/PDF_TEX from TikZ or SVG)
- `data/`: CSV datasets for plots
- `research/`: Computational artifacts (Mathematica `.nb`, Maxima `.mac`, R `.Rmd`)
- `code/`: Monte Carlo simulations (C++)

## Papermill State

The collection is managed with the **papermill** plugin (state-tracked paper drafting). State files are the source-of-truth for paper status; prefer reading them over inferring from git log or LaTeX content.

- `papers/.papermill/state.md`: collection-level dashboard. Per-paper thesis, root file, build command, sections, bibliography status, phase, and venue. Read this first when asked about paper status.
- `<paper>/.papermill/state.md`: per-paper detail (currently present for `bernoulli_sets/`, `bernoulli_classification_measures/`, `bernoulli-hash-function/`, `bernoulli-phf/`).
- `<paper>/.papermill/reviews/YYYY-MM-DD/`: multi-agent editorial review output (specialist reports plus a unified `review.md`). Example: `bernoulli_sets/.papermill/reviews/2026-05-23/` contains the most recent review pass on the primary paper.

The papermill skills (`papermill:status`, `papermill:review`, `papermill:draft`, etc.) read and write these files. When editing manually, keep the relevant `state.md` in sync.

## Conceptual Layering

Papers build on a shared foundation:
1. **Set algebra** → Boolean algebra of classical sets (`bernoulli_sets`)
2. **Bernoulli model** → Random approximate sets with FPR/FNR parameterization, higher-order composition (`bernoulli_sets`)
3. **Error count distributions** → Binomial FP/FN counts, CLT, confidence intervals (`bernoulli_sets`)
4. **Set-theoretic composition** → Error propagation through union, intersection, complement, monoid structure (`bernoulli_composition`)
5. **Relational predicates** → Subset, equality probabilities (`bernoulli_composition`)
6. **Interval arithmetic** → Uncertain rate propagation through set operations (`bernoulli_composition`)
7. **Classification measures** → PPV, NPV, accuracy, Youden's J as random variables (`bernoulli_classification_measures`)
8. **Entropy & space** → Joint entropy of errors, information-theoretic lower bounds (`bernoulli_entropy`)
9. **Optimal constructions** → Threshold predicate, space-optimal Bernoulli sets/maps (`bernoulli-hash-function`), perfect hash filter implementation (`bernoulli-phf`)
10. **Extensions** → Relations (`bernoulli_relations`), maps (`bernoulli_maps`), ADTs (`bernoulli_data_type`)

## Core Principles

Five principles underpin the entire paper family:

1. **The Two Axioms.** Element-wise independence (Axiom 1) and conditional independence of block error rates (Axiom 2). Everything follows from these. The Kronecker factorization theorem makes this precise: the joint confusion matrix equals the tensor product of per-element channels.

2. **Parametric Parsimony.** An n-th order model on m joint tests has n(2^m - 1) parameters in general, but the independence axiom forces Kronecker factorization, reducing to at most 2m. Product types preserve this; sum types break it.

3. **Space-Accuracy Duality.** bits/element = -log2(alpha) + mu. Derived in `bernoulli_entropy/`, achieved by BHF in `bernoulli-hash-function/`.

4. **Composition Closure.** Bernoulli sets are closed under union, intersection, complement, and difference. Error rates have closed-form propagation formulas. The composition theorem eta_total = 1 - prod(1 - eta_i) governs chains.

5. **The Boolean Thread.** Membership queries return Bernoulli Booleans. AND/OR/NOT on Bernoulli Booleans have closed-form error rates. Bool is the atomic type from which all others are built.

## Cross-Paper Topic Placement

Each paper owns a specific domain. When deciding where new content belongs:

| Topic | Paper | Why |
|-------|-------|-----|
| Set algebra, Bernoulli axioms, error count distributions, CLT, confidence intervals, higher-order composition, ADT | `bernoulli_sets/` | Core model: axioms, distributions, composition theorem |
| Set-operation error rates (complement, union, intersection, difference), monoidal structure, relational predicates, interval arithmetic | `bernoulli_composition/` | Compositional closure of the model under set operations |
| PPV, NPV, accuracy, Youden's J, prevalence sensitivity, delta method | `bernoulli_classification_measures/` | Binary classification measures induced by the model |
| Joint entropy of error counts, space complexity lower bound, Bloom filter efficiency | `bernoulli_entropy/` | Information-theoretic properties of approximate sets |
| Function spaces $X \to Y$, approximate maps, map composition | `bernoulli_maps/` | Functions as first-class objects with error |
| Relational algebra (join, project, select), approximate relations | `bernoulli_relations/` | Multi-attribute relations and relational operators |
| Algebraic types (Bool, sum, product, unit, absurd), computational basis | `bernoulli_data_type/` | Type-theoretic generalization of all the above |
| Threshold predicate, generalized acceptance, space-optimal construction, unified set/map framework | `bernoulli-hash-function/` | Information-theoretically optimal Bernoulli set/map construction |
| Perfect hash filter, k-perfect hashing, C++ implementation, ranked search application | `bernoulli-phf/` | Concrete implementation and deployment of one optimal construction |

**The Boolean thread** connects all papers:
- `bernoulli_sets/` introduces $U = \{\top, \bot\}$ as the minimal worked example and shows that membership queries return Bernoulli Booleans
- `bernoulli_maps/` covers approximate Boolean functions ($\{\top,\bot\} \to \{\top,\bot\}$: id, not, const-true, const-false) and their compositions
- `bernoulli_data_type/` gives the full type-theoretic treatment: Bool as a type, approximate AND/OR/NOT as logic gates, and generalization to sum/product types

## Terminology

- **Model order** = number of partition blocks (0 = exact, 1 = symmetric channel, 2 = FPR/FNR, $n$ = general)
- **k-fold composition** = iterated application of approximate identity $\sigma^k$ (distinct from model order)
- **Parametric parsimony** = An $n$-th order model on a single Boolean test has $n$ parameters (one per block). For $m$ joint tests, a general $n$-th order channel has $n(2^m - 1)$ parameters, but element-wise independence (Axiom 1) forces a Kronecker product factorization, reducing the count to at most $2m$. Example: the union of two second-order Bernoulli sets yields a fourth-order model with 4 parameters (not 12). This distinction between model order (partition granularity) and parameter count (constrained by independence) is important across all papers. Confusion matrices and model order are orthogonal concepts: order constrains which rows are identical, independence constrains the internal structure of each row.
- These terms were corrected in `bernoulli_sets/` and are already consistent in `bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex`

## Connection to Trapdoor Computing

The Bernoulli framework provides the error model for the trapdoor computing paradigm (`~/github/trapdoor-computing/`). Bernoulli maps ARE cipher maps at the mathematical level: the BHF salt is the trapdoor key, the acceptance predicate implements the cipher map, and the space formula -log2(epsilon) + mu governs both. The composition theorem is Property 4 of cipher maps. The Bernoulli Boolean algebra is the trapdoor Boolean algebra.

## Things Not To Edit

- `pdf-archive/`: compiled PDFs of superseded drafts (e.g., `bernoulli_sets_higher_order.pdf`, `bernoulli-sets.pdf`). Read for reference, do not regenerate, do not delete.
- LaTeX build artifacts inside paper directories (`main.aux`, `main.log`, `main.bbl`, `main.pdf`, `_minted-*/`, `main.synctex.gz`). Covered by per-paper `.gitignore` files; never `git add` them by hand.
- `bernoulli_sets/sections/unused/`: archived content from earlier paper splits. Useful as a reference for what was moved where, but not part of the current build.

## Repository Structure

The `papers/` directory contains one git subtree per paper, each with its own GitHub remote. The parent `bernoulli` repo tracks shared infrastructure (notation packages, build patterns) plus all papers in a single working tree. The full remote-name table and `git subtree push/pull` commands live in `../CLAUDE.md` to avoid duplication.
