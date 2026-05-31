# CLAUDE.md

## Project Overview

Research paper: **"The abstract data type of the approximate relation"** by Alexander Towell. Defines the semantics of *approximate relations* — probabilistic relations that approximate objective relations with false correspondences and false complementary correspondences. Derives entropy lower bounds, error propagation through relational operators (join, project), partial function composition, and demonstrates applications to trapdoor databases and Encrypted Search.

## Build

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

Uses modular `sty/` packages from local `sty/` directory (self-contained, no external dependencies).

## Structure

- `main.tex` — Document root, uses `\subfile{}` includes
- `sections/` — Active section files:
  - `intro.tex` — Introduction
  - `relations.tex` — Classical relation definitions
  - `approx_rel_model.tex` — Approximate relation model
  - `rel_algebra.tex` — Relational algebra (join, project, select)
  - `properties.tex` — Properties of approximate relations
  - `predicates.tex` — Approximate predicates
  - `test.tex` — Testing framework
  - `unused/optimality.tex` — Entropy/optimality bounds (included but in unused/)
  - `unused/oblivious_rel_model.tex`: Trapdoor relation model (filename retains historical 'oblivious')

## Key Notation

Uses modular packages: `functionnotation.sty`, `setnotation.sty`, `approxsetnotation.sty`, `probabilitynotation.sty`, `relationnotation.sty` (fancy mode), `approxrelationnotation.sty`, `envnotation.sty`.

- Relations: `\Rel{R}` — relation, approximate: `\ARel{R}`
- Sets: `\Set{A}`, approximate: `\ASet{A}`
- Rates: `\fprate`, `\fnrate`, `\tprate`, `\tnrate`

## Key Conceptual Distinction

**Model order vs. parameter count**: A relation $R \subseteq A \times B$ is a set of pairs, so each element's membership is a binary test. Composing relational operators (join, project) raises the model order because different tuples have different error regimes depending on their join structure. However, element-wise independence (Axiom 1) forces the joint confusion matrix to factor as a Kronecker product, so parameters grow linearly in the number of independent tests, not exponentially. A general fourth-order channel on 4 symbols has 12 parameters; under independence, it has 4. See `bernoulli_sets/` Remark on parametric parsimony and `bernoulli_composition/` Remark on parametric parsimony of composed sets.

## Cross-Paper Connections

| Topic | Paper |
|-------|-------|
| Set-level error model (FPR/TPR, precision) | `bernoulli_sets/` |
| Function spaces, approximate maps | `bernoulli_maps/` |
| **Relational algebra, approximate relations, joins** | **This paper** |
| Algebraic types (Bool, sum, product) | `bernoulli_data_type/` |

**Relationship to `bernoulli_sets/`**: A relation $R \subseteq A \times B$ is a set of pairs. An approximate relation inherits the Bernoulli set error model applied to the Cartesian product space. The relational predicates (subset, equality) in `bernoulli_sets/sections/relational.tex` provide the foundation; this paper extends to multi-attribute relations with join/project operations.

**Relationship to `bernoulli_maps/`**: A partial function is a special case of a relation (single-valued). Both papers cover approximate partial functions, but this paper emphasizes the relational algebra perspective while `bernoulli_maps/` emphasizes function composition.
