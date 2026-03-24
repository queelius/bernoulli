# Papermill State — Bernoulli Papers Collection

## Author

- **Name:** Alexander Towell
- **Email:** lex@metafunctor.com
- **ORCID:** 0000-0001-6443-9897
- **Institution:** Southern Illinois University Edwardsville
- **GitHub:** https://github.com/queelius
- **Scholar:** E9mnFzQAAAAJ

## Repository Type

Multi-paper collection. Nine active papers sharing a common theoretical framework (random approximate sets / Bernoulli sets). One retired paper retained as archive.

## Papers

### Tier 1: Core 4-Paper Family (alex.sty, actively maintained)

#### bernoulli_sets (Primary)

- **Title:** Bernoulli sets: a model for random approximate sets
- **Thesis:** The Bernoulli set model provides a compositionally closed probabilistic framework for random approximate sets: any set-theoretic operation on Bernoulli sets produces a Bernoulli set with computable error rates, enabling algebraic reasoning about complex approximate systems from simple axioms.
- **Root:** `bernoulli_sets/main.tex`
- **Notation:** `alex.sty` (unified, options: fancy, section)
- **Build:** `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- **Sections:** intro, algebra_of_sets, bernoulli_model, distributions, set_theory, relational, uncertain_rates, entropy, algebraic_structure, bool_search, appendix, conclusion (via `\input{}`)
- **Excluded:** adt.tex (fixed but kept out)
- **Unused:** sections/unused/ (bayesian_rates, bool_search archive, confusion_matrix_functions, images_model, monoids_notes, proof_subset_notes)
- **Bibliography:** 28 entries (mature, comprehensive)
- **Supporting:** img/ (5 TikZ), data/ (17 CSV), code/ (2 C++ Monte Carlo), research/ (Mathematica, SVG, R/Maxima)
- **Status:** Draft (post-revision), 43 pages. All major review issues resolved.
- **Phase:** revision
- **Venue:** Not yet targeted (candidates: ACM Trans. Algorithms, TCS, PODS, VLDB)
- **Per-paper state:** `bernoulli_sets/.papermill/state.md`

#### bernoulli_composition (Companion)

- **Title:** Composition of Bernoulli sets
- **Root:** `bernoulli_composition/main.tex`
- **Notation:** `alex.sty` (unified)
- **Build:** `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- **Sections:** intro, preliminaries, set_theory, relational, uncertain_rates, conclusion
- **Bibliography:** 6 entries (minimal, mostly companion refs)
- **Supporting:** None (text-only)
- **Status:** Draft, companion to bernoulli_sets
- **Phase:** drafting

#### bernoulli_classification_measures (Companion)

- **Title:** Binary classification measures for random approximate sets
- **Root:** `bernoulli_classification_measures/main.tex`
- **Notation:** `alex.sty` (unified)
- **Build:** `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- **Sections:** intro, preliminaries, measures, conclusion, appendix
- **Bibliography:** 11 entries (adequate)
- **Supporting:** img/ (figures), data/ (CSV datasets)
- **Status:** Draft, companion to bernoulli_sets
- **Phase:** drafting

#### bernoulli_entropy (Companion)

- **Title:** Entropy and space complexity of random approximate sets
- **Root:** `bernoulli_entropy/main.tex`
- **Notation:** `alex.sty` (unified)
- **Build:** `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- **Sections:** intro, preliminaries, entropy, space_complexity, conclusion
- **Bibliography:** 8 entries (minimal)
- **Supporting:** None
- **Status:** Draft, companion to bernoulli_sets
- **Phase:** drafting

### Tier 2: Application Papers (standalone)

#### bernoulli-hash-function

- **Title:** The Bernoulli Hash Function: Optimal Bernoulli Sets and Bernoulli Maps
- **Root:** `bernoulli-hash-function/main.tex`
- **Notation:** `alex.sty` (fancy, section) with `defs.tex` for paper-specific macros
- **Build:** `make` (Makefile, -interaction=nonstopmode, TEXINPUTS for sty/)
- **Sections:** intro, prelim, shf (centerpiece), construction, space, entropy, prob_model, operations, discussion, appendix (9 + appendix)
- **Bibliography:** 16 entries (good: 3 companions, 3 self-citations, 2 external classics)
- **Supporting:** img/ (1 TikZ), data/ (3 data files, 1 Python script), code/ (C++)
- **Status:** Draft ~95% complete, ~27 pages. All key theorems proved. No experiments yet.
- **Phase:** revision
- **Per-paper state:** `bernoulli-hash-function/.papermill/state.md`

#### bernoulli-phf

- **Title:** The Perfect Hash Filter
- **Root:** `bernoulli-phf/paper/main.tex`
- **Notation:** Modular `.sty` from `random_approximate_sets/sty/`, local `obliviousnotation.sty` stub
- **Build:** `cd paper && TEXINPUTS=".:../../random_approximate_sets/sty/:" pdflatex -shell-escape main.tex && makeglossaries main && bibtex main && pdflatex -shell-escape main.tex && pdflatex -shell-escape main.tex`
- **Sections compiled:** intro (stub), k_perfect_hashing (stub), cpp_imp (partial), adt (complete)
- **Sections excluded:** rd_ph_filter.tex (core derivation — should be included), pmf.tex, apps_postings_list.tex, variation.tex
- **Bibliography:** 8 entries (poor: 4 placeholder URLs, missing phf/shs citations)
- **Supporting:** research/, include/ (C++ header), tests/ (empty)
- **Status:** Early draft (~25% complete), 10 pages. Core derivation excluded; intro/kph stubs with broken refs. No experiments.
- **Phase:** early drafting
- **Per-paper state:** `bernoulli-phf/.papermill/state.md`

### Tier 3: Extension Papers (standalone, early)

#### bernoulli_maps

- **Title:** The algebra of the random approximate map model
- **Root:** `bernoulli_maps/main.tex`
- **Notation:** Modular `.sty` packages (functionnotation, setnotation, approxsetnotation, relationnotation, approxrelationnotation, envnotation, algorithmnotation)
- **Build:** `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- **Sections compiled:** intro, approxmaps, approx_maps, composition, special_functions, disc_fun, singular_hash_map (7 of 12; adt, random_algebraic, rank_ordered_search, notes, appendix commented out)
- **Bibliography:** 9 entries (minimal)
- **Supporting:** research/ (H, SVG, DIA files)
- **Status:** Early draft
- **Phase:** drafting

#### bernoulli_relations

- **Title:** The abstract data type of the approximate relation
- **Root:** `bernoulli_relations/main.tex`
- **Notation:** Modular `.sty` packages
- **Build:** `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- **Sections compiled:** intro, relations, approx_rel_model, rel_algebra, properties, predicates, test (7; optimality, oblivious_rel_model unused)
- **Bibliography:** **MISSING** (no references.bib file; declared in main.tex, will fail on bibtex)
- **Supporting:** None
- **Status:** Early draft
- **Phase:** drafting

#### bernoulli_data_type (two sub-papers)

**bernoulli_model/**:
- **Title:** The Bernoulli Model: A Probabilistic Framework for Data Structures and Types
- **Root:** `bernoulli_data_type/bernoulli_model/main.tex`
- **Notation:** Inline macros (`\Ber`, `\Bool`, `\True`, `\False`)
- **Build:** `pdflatex main.tex && pdflatex main.tex` (no bibtex)
- **Sections:** intro, order_and_channels, prediction, lifting, set_indicator, logic_gates, bernoulli_maps (7 via `\subfile{}`)
- **Bibliography:** None
- **Status:** Draft, substantial but rough. Author placeholder.
- **Known issues:** trailing fragment in lifting.tex, minimal conclusion in logic_gates.tex, notation inconsistency

**algebraic_types/**:
- **Title:** The random approximate values over algebraic types
- **Root:** `bernoulli_data_type/algebraic_types/main.tex`
- **Notation:** Modular `.sty` packages
- **Build:** `pdflatex -shell-escape main.tex && pdflatex -shell-escape main.tex` (minted)
- **Sections:** intro (stub), bernoulli_type_2, prims, bernoulli_boolean_algebra, cpp (4 via `\subfile{}`)
- **Bibliography:** Declared but does not exist
- **Status:** Early draft with TODOs, placeholder text, broken refs
- **Known issues:** stub intro, broken cross-references, near-duplicate sections, extensive orphaned/ directory

### Deleted

#### random_approximate_sets (deleted 2026-03)

Fully superseded by the 4-paper family and deleted. Its modular `sty/` packages were copied into each dependent paper (`bernoulli_maps/sty/`, `bernoulli_relations/sty/`, `bernoulli-phf/paper/sty/`, `bernoulli_data_type/algebraic_types/sty/`). Two minor unique items were the epistemological discussion (~50 lines in `aset_adt.tex`) and a Boolean search application (archived in `bernoulli_sets/sections/unused/bool_search.tex`).

## Notation Systems

Two coexisting approaches:

1. **`alex.sty`** (unified single package) — bernoulli_sets, bernoulli_composition, bernoulli_classification_measures, bernoulli_entropy, bernoulli-hash-function. Options: `fancy`, `section`. Provides all macros.
2. **Modular `sty/`** (separate packages per domain) — bernoulli_maps, bernoulli_relations, bernoulli-phf, bernoulli_data_type/algebraic_types. Each paper has its own copy in a local `sty/` subdirectory (no shared source).

Core notation consistent: `\Set{A}`, `\ASet{A}`, `\fprate`/`\fnrate`, `\tprate`/`\tnrate`, `\RV{X}`.

## Conceptual Dependency

```
bernoulli_sets (core model, axioms, distributions, composition, ADT)
├── bernoulli_composition (set-operation algebra, relational predicates, intervals)
├── bernoulli_classification_measures (PPV, NPV, accuracy, Youden's J)
├── bernoulli_entropy (joint entropy, space complexity)
├── bernoulli-hash-function (optimal construction, threshold predicate)
├── bernoulli-phf (perfect hash filter implementation)
├── bernoulli_maps (approximate functions/maps)
├── bernoulli_relations (approximate relational algebra)
└── bernoulli_data_type (algebraic type generalization)
```

## Known Issues

| Issue | Paper | Severity |
|-------|-------|----------|
| No references.bib | bernoulli_relations | Build failure |
| No references.bib | bernoulli_data_type (both) | Build failure |
| 4 placeholder bib URLs | bernoulli-phf | Poor |
| Core section excluded (rd_ph_filter.tex) | bernoulli-phf | Major gap |
| Intro/kph stubs | bernoulli-phf | Incomplete |
| Orphaned duplicate files | bernoulli_data_type | Cleanup needed |
| Author placeholder | bernoulli_data_type/bernoulli_model | Metadata |

## Consolidation History

1. `random_approximate_set_model/` merged into `random_approximate_sets/` (content in sections/unused/)
2. `bernoulli_sets_higher_order/` merged into `bernoulli_sets/` (archive.zip preserves originals)
3. `bernoulli_sets/` split into 4 papers (2026): composition → `bernoulli_composition/`, classification → `bernoulli_classification_measures/`, entropy → `bernoulli_entropy/`
4. `random_approximate_sets/` retired (2026-02) then deleted (2026-03). Modular sty/ packages copied into each dependent paper as local copies.
