# CLAUDE.md: bernoulli-phf (The Perfect Hash Filter)

## Paper Overview

**Title**: The Perfect Hash Filter
**Subtitle**: An efficient implementation of the positive Bernoulli set and Bernoulli map abstract data types
**Author**: Alexander Towell (atowell@siue.edu)
**Status**: Draft, complete in its core theory; builds clean at 37 pages.

The Perfect Hash Filter (PHF) places each member of a static set at a unique
slot via a minimal perfect hash and stores a short fingerprint there. This
minimal-perfect-hash-plus-fingerprint structure is the well-known static
approximate-membership-query (AMQ) construction shared by Bloomier, xor, ribbon,
and cuckoo filters; **the base structure is not new**. The paper's contribution
is its treatment within Bernoulli type theory: realizing the PHF as a faithful
implementation of the positive Bernoulli set ADT, deriving a tunable false
negative rate via $k$-perfect hashing, lifting it to a key-value map (the Perfect
Map Filter), and tying its space to the information-theoretic bound.

## Salvage history (read before editing)

This paper was salvaged in phases. Phases A through C are done and committed:

- **A (correctness)**: fixed the `dummyref` placeholder, the `thm:fpr`/`thm:fnr`
  vs `thm:fp_rate` name mismatch, and the sign error in the union
  space-complexity proof; restored the build (a stub `img/phfilter.tex` stands in
  for the never-committed original figure).
- **B (honest framing)**: added a related-work section (`related_work.tex`) that
  states plainly the AMQ structure is established and reframes the contribution
  as the Bernoulli-ADT realization plus the $k$-perfect FNR analysis. Qualified the
  $-\log_2 \fprate$ optimality claim (it holds only as $\fprate \to 0$; the PHF
  does not attain it at finite $\fprate$).
- **C (completeness)**: dropped the load-bearing dependency on the unpublished
  `oph` manuscript for the headline space theorem (it is now self-contained via
  the random-oracle birthday argument; `oph` survives only as a non-load-bearing
  aside in the C++ subsection). Derived the $k$-perfect false negative rate
  $\omega = 1 - (1-e^{-r})/r$ from a balls-into-bins model
  (\cref{thm:k_omega}). Completed the PMF space and entropy (PMF) bounds.
- **E (polish)**: threaded the Five Core Principles and the explicit relation to
  the Bernoulli Hash Function paper into the intro; added a numeric end-to-end
  worked example (\cref{ex:dictionary}, $m=10^6$, $\fprate=2^{-16}$); fixed the
  bibliography self-cites (years + real GitHub URLs).

**Remaining work**: Phase D, the `maph` experiments (the repo is a full `maph`
C++ project; wire measured numbers into the paper), and final pre-submission
polish.

## All 8 sections are subfiled and compiled

`main.tex` subfiles every section in `sections/`, in this order:

| # | Section file | Title | Notes |
|---|---|---|---|
| 1 | `intro.tex` | Introduction | Contributions list, two axioms, "Relation to the Bernoulli framework" paragraph (Five Principles + BHF link) |
| 2 | `related_work.tex` | Related work | AMQ prior art; "What this paper contributes" subsection |
| 3 | `rd_ph_filter.tex` | Rate-distorted perfect hash filter | Core derivation: FPR theorem, space bounds, Bloom comparison, worked example, entropy/cardinality estimation |
| 4 | `typed_phf.tex` | The typed Perfect Hash Filter | Injection $\mathbb{X}\to\BitSet^*$ |
| 5 | `k_perfect_hashing.tex` | $k$-perfect hashing and false negatives | Two-rate second-order model; $\omega$ derivation; binary asymmetric channel |
| 6 | `pmf.tex` | Approximate hash map | Perfect Map Filter; two rates; space lower bound; entropy upper bound |
| 7 | `apps_postings_list.tex` | Applications | Boolean + rank-ordered (fuzzy) retrieval |
| 8 | `cpp_imp.tex` | A C++ implementation | Dynamic polymorphism, complement; some listings still commented out |
| 9 | `adt.tex` | Abstract data type of the Bernoulli set | $\sigma$-algebra, Boolean algebra, space complexity of unions/differences |

`variation.tex` from the old layout is gone; `adt.tex` is the final section. The
old "only 4 of 8 included" / "`rd_ph_filter` NOT included" claim is obsolete.

## Build

```bash
cd paper && \
  pdflatex -shell-escape main.tex && \
  makeglossaries main && \
  bibtex main && \
  pdflatex -shell-escape main.tex && \
  pdflatex -shell-escape main.tex
```

Requires `minted` (hence `-shell-escape` / `pygmentize`) and `glossaries`
(`makeglossaries`, makeindex backend). Current state: **37 pages, 0 undefined
refs/citations, 0 bibtex warnings**. Modular `.sty` packages are in `paper/sty/`
(self-contained); `\fprate`=$\varepsilon$ and `\fnrate`=$\omega$ come from
`approx_data_type_notation.sty` (required transitively by `approxsetnotation`).

## Relationship to the rest of the family

This is the **concrete implementation** paper for theory developed elsewhere:

| Framework concept | PHF realization |
|---|---|
| Positive Bernoulli set ($\fnrate=0$)~\cite{bsets} | Standard PHF: fingerprints at perfect-hash slots |
| False positive rate $\fprate$ | Fingerprint width: $\fprate = 2^{-M}$ |
| False negative rate $\fnrate=\omega$ | $k$-perfect collisions overwrite slots (\cref{thm:k_omega}) |
| Composition theorem $\eta_{\mathrm{total}}=1-\prod(1-\eta_i)$ | Induced FPR of a union of PHFs |
| Space-accuracy duality $-\log_2\fprate+\mu$ | PHF attains $-\log_2\fprate+\log_2 e$ (minimal), succinct as $\fprate\to0$ |
| Bernoulli map~\cite{bmaps} | Perfect Map Filter (`pmf.tex`) |
| Entropy / space lower bound~\cite{emaps} | `thm:approx_l_b`, `thm:mPHF_size`, `thm:pmf_lower_bound` |
| **Space-optimal Bernoulli set/map construction (BHF)**~\cite{shs} | The PHF is the **perfect-hash instance** of the BHF; fingerprint equality is its acceptance predicate |

The `shs` citation is the **Bernoulli Hash Function** paper
(`papers/bernoulli-hash-function/`): the "singular hash set" is the space-optimal
construction developed there, and the PHF is one concrete instance of it. The
Bloom filter's $1.44$ overhead is the gap succinct constructions close.

## Bibliography

`references.bib` has 16 real external entries (perfect hashing, Bloom/AMQ,
information-theoretic bounds, modern filters, fuzzy sets/IR) plus 9 author
self-cites. As of Phase E all self-cites carry `year={2026}`; `bsets`, `bmaps`,
`emaps`, `shs` carry their real GitHub `url`; `obset` is the **cipher set**
(formerly "oblivious", retired terminology). No invented DOIs. `aset` and `pmf`
are defined but currently uncited.

## Code side (Phase D target)

The repo top level is a full `maph` C++23 project, **not** the old single
`rd_ph_filter.hpp`: `include/maph/*.hpp`, `src/maph_cli.cpp`, `tests/` (19
files, populated), `benchmarks/`, `examples/`, `integrations/`, `CMakeLists.txt`.
This is the active C++ research sandbox for the PHF and the source of the planned
experiments. Wiring its measured numbers (perfect-hash overhead, FPR/FNR,
space vs Bloom) into the paper is Phase D.

## House style

Keep prose free of em-dashes (use commas, periods, colons, or parentheses) and
of the promotional adjectives the soul hook bans on sight (it matches them in any
context). Use `\gls{}` glossary terms, `\fprate`/`\fnrate`, and the modular
`sty/` notation. The soul hook scans only the diff, so appended clean text is
fine even where a file already contains banned characters.
