# Papermill State: The Perfect Hash Filter

## Meta

| Field | Value |
|-------|-------|
| **Title** | The Perfect Hash Filter |
| **Subtitle** | An efficient implementation of the positive Bernoulli set and Bernoulli map abstract data types |
| **Authors** | Alexander Towell (atowell@siue.edu) |
| **ORCID** | 0000-0001-6443-9897 |
| **Affiliation** | Southern Illinois University Edwardsville |
| **Status** | Draft, core theory complete; builds clean |
| **Venue** | Undetermined (Zenodo preprint per family strategy) |
| **Repo started** | 2019-01-14 |
| **Last updated** | 2026-06-07 |
| **Pages** | 37 |
| **Build system** | pdflatex + makeglossaries + bibtex (shell-escape for minted) |

## Thesis

The Perfect Hash Filter (PHF) is the perfect-hash instance of the well-known
minimal-perfect-hash-plus-fingerprint approximate-membership construction. The
contribution is its treatment within Bernoulli type theory: it is a faithful
implementation of the positive Bernoulli set ADT (and, lifted, the Bernoulli
map), so it inherits the framework's error model, composition theory, and space
bounds; a $k$-perfect variant gives it a derived false negative rate, making it a
genuine two-rate Bernoulli set; and its space approaches the information-theoretic
floor of $-\log_2 \fprate$ bits per element as $\fprate \to 0$, against the Bloom
filter's $1/\ln 2 \approx 1.44$ overhead.

## Structure (all 8 sections subfiled and compiled)

| # | Section file | Title | State |
|---|---|---|---|
| 1 | `intro.tex` | Introduction | Complete. Contributions list, two axioms, "Relation to the Bernoulli framework" paragraph (Five Principles + BHF link). |
| 2 | `related_work.tex` | Related work | Complete. AMQ prior art; honest "what this paper contributes". |
| 3 | `rd_ph_filter.tex` | Rate-distorted perfect hash filter | Complete. FPR theorem, space bounds, Bloom comparison, numeric worked example, entropy/cardinality estimation. |
| 4 | `typed_phf.tex` | The typed Perfect Hash Filter | Complete. Injection into $\BitSet^*$. |
| 5 | `k_perfect_hashing.tex` | $k$-perfect hashing and false negatives | Complete. $\omega$ derived from balls-into-bins; binary asymmetric channel. |
| 6 | `pmf.tex` | Approximate hash map | Complete. Perfect Map Filter; two rates; space + entropy bounds. |
| 7 | `apps_postings_list.tex` | Applications | Complete. Boolean + fuzzy/rank-ordered retrieval. |
| 8 | `cpp_imp.tex` | A C++ implementation | Partial. Prose + interface; some listings still commented out. |
| 9 | `adt.tex` | Abstract data type of the Bernoulli set | Mature. $\sigma$-algebra, Boolean algebra, union/difference space complexity. |

The old "4 of 8 compiled / `rd_ph_filter` excluded / ~10 pages" assessment is
obsolete. `variation.tex` is gone; `adt.tex` is the closing section.

## Build Command

```bash
cd paper && \
  pdflatex -shell-escape main.tex && \
  makeglossaries main && \
  bibtex main && \
  pdflatex -shell-escape main.tex && \
  pdflatex -shell-escape main.tex
```

Current result: **37 pages, 0 undefined refs/citations, 0 bibtex warnings.**

### Build dependencies
- `.sty` packages in `paper/sty/` (self-contained); `\fprate`/`\fnrate` come from
  `approx_data_type_notation.sty` (required by `approxsetnotation`).
- Glossary files: `gls-custom.tex`, `gls-approxset.tex`, `gls-set.tex`,
  `gls-hashing.tex`.
- `img/phfilter.tex` is a Phase A stub for the never-committed original figure.
- External: `pdflatex`, `bibtex`, `makeglossaries` (makeindex backend),
  `pygmentize`.

## Salvage phases

- **A (correctness, done)**: fixed `dummyref`, the `thm:fpr`/`thm:fnr` vs
  `thm:fp_rate` mismatch, and the union space-complexity sign error; restored the
  build with a stub figure.
- **B (honest framing, done)**: added `related_work.tex`; reframed the
  contribution as a Bernoulli-ADT realization plus $k$-perfect FNR analysis;
  qualified the $-\log_2 \fprate$ optimality (holds only as $\fprate \to 0$).
- **C (completeness, done)**: dropped the load-bearing `oph` dependency for the
  headline space theorem (now self-contained; `oph` is a non-load-bearing aside
  in the C++ subsection); derived the $k$-perfect FNR
  $\omega = 1 - (1-e^{-r})/r$ (`thm:k_omega`); completed the PMF space and
  entropy (PMF) bounds.
- **E (polish, done)**: threaded the Five Core Principles and the explicit
  relation to the Bernoulli Hash Function paper (`\cite{shs}`) into the intro;
  added the numeric worked example (`ex:dictionary`, $m=10^6$, $\fprate=2^{-16}$:
  $17.4427$ vs Bloom's $23.0831$ bits/element); fixed the bibliography
  (self-cites carry `year={2026}`; real GitHub URLs on `bsets`/`bmaps`/`emaps`/
  `shs`; `obset` retitled "cipher set").
- **D (experiments, TODO)**: the repo top level is a full `maph` C++23 project
  (`include/maph/`, `src/maph_cli.cpp`, populated `tests/`, `benchmarks/`,
  `examples/`, `integrations/`). Wire its measured numbers (perfect-hash overhead,
  FPR/FNR, space vs Bloom) into the paper. Not yet started.

## Open items

1. Phase D experiments (above).
2. `cpp_imp.tex`: a few code listings remain commented out.
3. `img/phfilter.tex` is a stub; a proper figure would help the worked example.
4. Final pre-submission polish (papermill:polish) once experiments land.

## Completeness Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Core argument | 95% | FPR, $k$-perfect FNR, space, and entropy results complete and self-contained. |
| Introduction | 100% | Framing, axioms, framework relation, BHF link. |
| Related work | 100% | Honest AMQ situating; contribution stated plainly. |
| Proofs/theory | 90% | All headline theorems proved; PMF and union-space results complete. |
| Implementation | 50% | C++ section partial (commented listings); separate `maph` codebase mature. |
| Experiments | 0% | Phase D. |
| Bibliography | 95% | 16 real external entries + 9 dated self-cites; no invented DOIs. |
| **Overall** | **~85%** | Theory complete and building; remaining work is experiments and polish. |

## Cross-Paper Context

- **Parent theory**: `bernoulli_sets/` (`\cite{bsets}`), the model this paper implements.
- **Space-optimal construction**: `bernoulli-hash-function/` (`\cite{shs}`); the
  PHF is the perfect-hash instance of the BHF, fingerprint equality as its
  acceptance predicate.
- **Map / entropy**: `bernoulli_maps/` (`\cite{bmaps}`), `bernoulli_entropy/`
  (`\cite{emaps}`).
- **Cited as** `\cite{phf}` elsewhere in the family.
- **Notation**: modular `.sty` packages in `paper/sty/` (not `alex.sty`).

## History

- **2026-02-24**: Papermill initialized; build fixed (glossary files,
  `\bibliographystyle{plainnat}`, makeindex backend). 10 pages then.
- **2026-05-29** (review + build-repair): review found not-ready (build was
  aborting on a missing `\input{img/phfilter.tex}`); a stub figure restored the
  build to 28 pages. Prioritized correctness, honest related work, optimality
  qualification, the union sign error, and the `oph` dependency.
- **2026-06-07** (Phase A–C salvage, committed): correctness fixed, related work
  added, `oph` dependency dropped, $k$-perfect FNR derived, PMF bounds completed.
  Build clean at 36 pages.
- **2026-06-07** (Phase E polish): Five Principles + BHF relation threaded,
  numeric worked example added, bibliography self-cites dated/URL'd, metadata
  synced. Build clean at **37 pages, 0 undefined refs/cites, 0 bibtex warnings**.
  Remaining: Phase D (maph experiments) and final polish.
