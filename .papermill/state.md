# Papermill State — The Perfect Hash Filter

## Meta

| Field | Value |
|-------|-------|
| **Title** | The Perfect Hash Filter |
| **Authors** | Alexander Towell (atowell@siue.edu) |
| **ORCID** | 0000-0001-6443-9897 |
| **Affiliation** | Southern Illinois University Edwardsville |
| **Status** | Draft — incomplete, actively maintained |
| **Venue** | Undetermined |
| **Repo started** | 2019-01-14 |
| **Last updated** | 2026-02-24 |
| **Pages** | 10 (compiled sections only) |
| **Build system** | pdflatex + bibtex + makeglossaries (shell-escape for minted) |

## Thesis

The Perfect Hash Filter is a succinct, immutable data structure that implements the positive Bernoulli set abstract data type (from the `bernoulli_sets/` paper) using perfect hash functions and fingerprint arrays, asymptotically achieving the information-theoretic lower bound of $-\log_2 \varepsilon$ bits/element on space complexity.

## Structure

### Compiled sections (in `main.tex`)

| # | Section file | Title | Status | Lines |
|---|---|---|---|---|
| 1 | `intro.tex` | Introduction | Stub — references undefined labels (`sec:set_model`, `sec:phf`, `dummyref`) | 11 |
| 2 | `k_perfect_hashing.tex` | Perfect hash filters that trade time for space | Stub — only math fragments, no prose | 15 |
| 3 | `cpp_imp.tex` | A C++ implementation | Partial — dynamic polymorphism, union/intersection, but commented-out listings | 274 |
| 4 | `adt.tex` | Abstract data type of random approximate sets | Most complete — deterministic algorithm, algebraic properties, sigma-algebra, entropy | 579 |

### Excluded sections (exist but NOT compiled)

| Section file | Title | Lines | Notes |
|---|---|---|---|
| `rd_ph_filter.tex` | Rate-distorted perfect hash filter | 564 | Core derivation: PHF construction, FPR proof, space bounds, Bloom filter comparison. **Should be included.** |
| `pmf.tex` | Approximate hash map | 82 | Extends PHF to key-value maps (Perfect Map Filter). |
| `apps_postings_list.tex` | (Applications) | 124 | Information retrieval application. |
| `variation.tex` | (Variations) | 107 | Load factor variations, oblivious sets. |

### Other files

- `references.bib` — 8 entries; 4 self-citations have placeholder URLs (`http://example.com`)
- `todo.txt` — k-collision handling, RegularType concept, entropy/confidentiality notes
- `todo2.txt` — Boolean algebra / expressively complete connectives
- `research/approximate_hash_set/` — Earlier version of paper (preserved for reference)
- `include/rd_ph_filter/rd_ph_filter.hpp` — C++ header-only library (149 lines)
- `tests/` — Empty (no tests)

## Build Command

```bash
cd paper && \
  pdflatex -shell-escape main.tex && \
  makeglossaries main && \
  bibtex main && \
  pdflatex -shell-escape main.tex && \
  pdflatex -shell-escape main.tex
```

### Build dependencies
- `.sty` packages in local `paper/sty/` directory (self-contained)
- `obliviousnotation.sty` — local stub (no macros from this package are used)
- Glossary files: `gls-custom.tex`, `gls-approxset.tex`, `gls-set.tex`, `gls-hashing.tex` (created 2026-02-24)
- External: `pdflatex`, `bibtex`, `makeglossaries` (makeindex backend), `pygmentize`

## Known Issues

1. **Incomplete structure**: Only 4 of 8 sections compiled; `rd_ph_filter.tex` (the core derivation) is excluded
2. **Introduction is a stub**: References labels in excluded sections (`sec:set_model`, `sec:phf`, `dummyref`)
3. **`k_perfect_hashing.tex` is a stub**: Only math fragments, no developed prose
4. **Self-citations placeholder**: `references.bib` entries `aset`, `obset`, `oph`, `pmf` use `http://example.com`
5. **Missing bib entries**: `phf` and `shs` cited but not defined in `references.bib`
6. **Undefined cross-references**: `thm:fpr`, `thm:fnr`, `sec:set_model`, `sec:phf`, `sec:set_theory`, `lst:asetunion`, `lst:asetcomp` — all defined in excluded sections
7. **No C++ tests**: `tests/` directory is empty
8. **`cpp_imp.tex` commented-out listings**: Code listing includes are commented out (paths may be stale)

## Completeness Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Core argument | 40% | Main derivation (`rd_ph_filter.tex`) exists but is excluded from compilation |
| Introduction | 15% | Stub with broken references |
| Related work | 0% | No related work section |
| Proofs/theory | 50% | FPR/space proofs in `rd_ph_filter.tex`; ADT formalization in `adt.tex` |
| Implementation | 35% | C++ section exists but has commented-out code listings |
| Experiments | 0% | No experimental evaluation |
| Bibliography | 25% | 8 entries, 4 are placeholders |
| **Overall** | **~25%** | Early draft with substantial content in excluded sections |

## Cross-Paper Context

This paper is part of the `bernoulli/papers/` collection:
- **Parent theory**: `bernoulli_sets/` — defines the Bernoulli set model this paper implements
- **Cited as**: `\cite{phf}` in `bernoulli_sets/`
- **Sibling papers**: `bernoulli_maps/`, `bernoulli_relations/`, `bernoulli_data_type/`
- **Notation**: Uses modular `.sty` packages from local `paper/sty/` (not `alex.sty`)

## History

- **2026-02-24**: Papermill initialized. Fixed build: created glossary files, added `\bibliographystyle{plainnat}`, created `obliviousnotation.sty` stub, switched glossaries from `xindy` to `makeindex` backend. Paper compiles to 10 pages with warnings from excluded section cross-references.
