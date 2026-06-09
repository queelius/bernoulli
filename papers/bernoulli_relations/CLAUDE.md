# CLAUDE.md

## Project Overview

Research paper: **"The abstract data type of the approximate relation"** by Alexander Towell. Models the approximate relation as a Bernoulli random approximate set over the tuple universe, then derives how error propagates through the relational operators (selection is rate-transparent; projection amplifies the false-positive rate to `1-(1-eps)^k` in the fan-in and raises the model order; a join breaks element-wise independence), and when structural invariants (reflexive, symmetric, functional, transitive) survive approximation, with a trapdoor-database / encrypted-search application. The entropy space bound, the perfect-hash-map construction, and map composition are deferred to the companion papers (`bernoulli_entropy`, `bernoulli-phf`, `bernoulli_maps`).

## Build

Modular-sty paper: every `pdflatex` invocation needs `TEXINPUTS=".:./sty:"` (the
`.sty` packages live in `sty/`) and `-shell-escape` (minted is loaded).

```bash
TEXINPUTS=".:./sty:" pdflatex -shell-escape main.tex && bibtex main && \
  TEXINPUTS=".:./sty:" pdflatex -shell-escape main.tex && \
  TEXINPUTS=".:./sty:" pdflatex -shell-escape main.tex
```

Uses modular `sty/` packages from the local `sty/` directory (self-contained, no
external dependencies). As of the 2026-06-09 deepening round the build is clean:
24 pages, 0 undefined references, 0 LaTeX warnings.

## Structure

- `main.tex`: document root, uses `\subfile{}` includes.
- `sections/`: active section files (current as of the 2026-06 salvage).
  - `intro.tex`: introduction (gap, contributions, related work, companions, organization).
  - `relations.tex`: classical relations and the relational operators (select, project, join, compose).
  - `approx_rel_model.tex`: the random approximate relation model (ADT, Bernoulli set over the tuple universe; subset/equality predicates deferred to `bernoulliComposition`).
  - `rel_algebra.tex`: error propagation through the operators (selection transparent; projection amplifies FPR and raises model order; join breaks element-wise independence), the worked example, the pgfplots fan-in figure, and the Monte Carlo "Empirical validation" subsection (cites `code/validate.py`).
  - `properties.tex`: invariant preservation (reflexive, symmetric plus symmetric closure, single-valued/functional, transitive), the closure dichotomy (sec 5.5: class-induced invariants, the OR-closure, the canonical test `thm:canonical_test` showing the invariant itself is free, the `log2 m` recall surcharge, `lem:no_quotient`, the transitivity cascade, the deletion closed form), and the approximate partial function (compressed; classical recap deferred to the maps companion).
  - `oblivious_rel_model.tex`: application, the trapdoor relational database (cipher relation, rank-ordered encrypted search, threat/leakage model). Filename retains historical 'oblivious'; the prose uses trapdoor/cipher.
  - `conclusion.tex`: contributions, the "decomposability, not arity" takeaway, CQA positioning, open directions (added 2026-06-09).
- `code/validate.py`: Monte Carlo validation harness (projection amplification, join incl. asymmetric operands and independence-failure correlation, symmetric closure and preservation, OR-closure m=2..4, canonical test, deletion rate, reflexive/functional preservation, deterministic transitivity cascade incl. non-power-of-2 k). Pure Python plus numpy; prints an analytical-vs-empirical table.
- `code/validate_quotient.py`: canonical test vs OR-closure vs naive comparison (rates, storage halving, deterministic symmetry).

**Deleted in the 2026-06 salvage** (superseded/orphaned): `predicates.tex` (its
subset/equality rates are the set-level results of the composition paper, and the
draft carried a sign error in the equality formula; now a one-paragraph cite of
`bernoulliComposition` at the end of `approx_rel_model.tex`); `test.tex` and
`constrained_ras.tex` (never written / orphaned). There is no `unused/` directory.

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
