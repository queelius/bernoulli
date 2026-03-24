# CLAUDE.md

## Project Overview

Research paper: **"The algebra of the random approximate map model"** by Alexander Towell. Defines the semantics of *approximate maps* (probabilistic partial functions) that approximate objective maps with specified false positive and false negative rates. Derives expected precision for information retrieval, generalizes to approximate relations and compositions, and demonstrates applications to Encrypted Search with rank-ordered queries.

## Build

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

Uses modular `sty/` packages from local `sty/` directory (self-contained, no external dependencies).

## Structure

- `main.tex` — Document root, uses `\subfile{}` includes
- `sections/` — Section files:
  - `intro.tex` — Introduction
  - `approxmaps.tex`, `approx_maps.tex` — Approximate map model definition
  - `composition.tex` — Map composition and error propagation
  - `special_functions.tex` — Special function classes
  - `disc_fun.tex` — Discriminating functions
  - `singular_hash_map.tex` — Singular hash map implementation
  - `sections/unused/` — Archived/inactive sections (rank-ordered search, random algebraic, notes)
- `defs.tex`, `gloss.tex` — Definitions and glossary
- `references.bib` — Bibliography
- `research/` — Computational artifacts

## Key Notation

Uses modular packages: `functionnotation.sty`, `setnotation.sty`, `approxsetnotation.sty`, `relationnotation.sty`, `approxrelationnotation.sty`, `envnotation.sty`, `algorithmnotation.sty`.

- Approximate maps: `\APFun{f}[\fprate][\tprate]` — approximate function with error rates
- Map approximation: $\tilde{f} : X \to Y$ approximates $f : X \to Y$
- Custom: `\amapsto` — approximate mapsto arrow

## Key Conceptual Distinction

**Model order vs. parameter count**: A map $f: X \to Y$ has its graph as a subset of $X \times Y$; per-element membership is binary. For a single Boolean, the $2 \times 2$ confusion matrix has 2 parameters (maximum). For $m$ joint Booleans (e.g., paired approximate map outputs), a general fourth-order channel on 4 symbols has 12 parameters, but element-wise independence forces a Kronecker product factorization reducing this to 4. Composition raises model order (Lemma in `sections/composition_new.tex`), but the Bernoulli axiom constrains the parameter growth. See discussion in `sections/special_cases.tex`.

## Cross-Paper Connections

This paper occupies a specific position in the Bernoulli framework:

| Topic | Paper |
|-------|-------|
| Set-level error model (FPR/TPR, PMF, precision) | `bernoulli_sets/` |
| **Function spaces $X \to Y$, approximate maps, composition** | **This paper** |
| Relational algebra (join, project, approximate relations) | `bernoulli_relations/` |
| Algebraic types (Bool, sum, product, unit, absurd) | `bernoulli_data_type/` |

**Boolean connection**: The function space $\{\top,\bot\} \to \{\top,\bot\}$ yields exactly 4 maps (id, not, const-true, const-false). Approximating these — e.g., an approximate NOT gate — illustrates the composition theorem directly: $\widetilde{\mathrm{NOT}} \circ \widetilde{\mathrm{NOT}}$ is a two-fold composition whose error rates follow the composition formula from `bernoulli_sets/`. This paper is the natural home for approximate Boolean functions and their compositions as maps.
