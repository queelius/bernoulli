# CLAUDE.md — rd_ph_filter (Perfect Hash Filter)

## Paper Overview

**Title**: The Perfect Hash Filter
**Author**: Alexander Towell
**Status**: Draft, actively maintained

The Perfect Hash Filter (PHF) is a practical data structure implementing the **positive Bernoulli set** abstract data type from the `bernoulli_sets/` paper. It is an alternative to the Bloom filter with different space/time trade-offs.

## Key Conceptual Distinction

**Model order vs. parameter count**: The PHF satisfies the Bernoulli axioms, so its error behaviour is fully characterized by its FPR (and FNR in the k-perfect case). Composing PHF instances with other Bernoulli sets yields higher-order models, but element-wise independence constrains the joint confusion matrix to factor as a Kronecker product, keeping parameters linear. See `bernoulli_sets/` Remark on parametric parsimony.

## Relationship to Bernoulli Sets

This paper is a **concrete implementation** paper for the theory developed in `bernoulli_sets/`. Key connections:

| Bernoulli sets concept | PHF realization |
|---|---|
| Positive Bernoulli set ($\fnrate = 0$) | Standard PHF: stores hash fingerprints at perfect-hash indices |
| False positive rate $\fprate$ | Determined by fingerprint bit-width: $\fprate \approx 2^{-b}$ for $b$-bit fingerprints |
| False negative rate $\fnrate$ | Arises from imperfect (k-)perfect hashing: collisions cause missed elements |
| Information-theoretic lower bound $-\log_2 \fprate$ bits/element | PHF approaches this asymptotically; Bloom filter achieves $\ln 2 \approx 0.69$ efficiency |
| Bernoulli set ADT (Section 3.1 of `bernoulli_sets/`) | PHF satisfies the ADT axioms: `contains(x, ctor(A))` has the prescribed error rates |
| `phf` and `shs` citations in `bernoulli_sets/` | Refer to this paper and the singular hash set |

## Build

```bash
cd paper && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

**Note**: Requires `minted` package (and therefore `--shell-escape` or `pygmentize`) and glossaries (`makeglossaries`). Modular `.sty` packages are in `paper/sty/` (self-contained, no external dependencies).

## Structure

```
rd_ph_filter/
├── paper/
│   ├── main.tex                    # Document root (uses \subfile{})
│   ├── references.bib              # Bibliography (needs cleanup)
│   ├── sections/
│   │   ├── intro.tex               # Introduction
│   │   ├── k_perfect_hashing.tex   # k-perfect hashing techniques
│   │   ├── cpp_imp.tex             # C++ implementation details
│   │   ├── adt.tex                 # Abstract data type (~28 KB, substantial)
│   │   ├── rd_ph_filter.tex        # Main PHF derivation (~27 KB, NOT included in main.tex)
│   │   ├── pmf.tex                 # Probability mass function (NOT included)
│   │   ├── apps_postings_list.tex  # Applications (NOT included)
│   │   └── variation.tex           # Variations (NOT included)
│   ├── img/                        # Figures
│   ├── research/                   # Earlier approximate_hash_set version
│   ├── todo.txt, todo2.txt         # Active work notes
│   └── gls-*.tex                   # Glossary definition files
├── include/rd_ph_filter/
│   └── rd_ph_filter.hpp            # C++ template implementation
└── tests/                          # Test directory
```

**Important**: Only 4 of 8 section files are included in `main.tex`: `intro`, `k_perfect_hashing`, `cpp_imp`, `adt`. The others (`rd_ph_filter`, `pmf`, `apps_postings_list`, `variation`) exist but are NOT compiled.

## Notation

Uses modular `.sty` packages (NOT `alex.sty`):
- `setnotation.sty`, `approxsetnotation.sty`, `functionnotation.sty`
- `relationnotation.sty`, `algorithmnotation.sty`, `matrixnotation.sty`
- `envnotation.sty`, `obliviousnotation.sty`
- Glossary system (`glossaries` package with custom `.tex` entries)

Core notation is compatible with `bernoulli_sets/`:
- `\ASet{A}` for approximate sets, `\fprate`/`\fnrate` for error rates
- Additional: `\gls{gls-phf}` for "Perfect Hash Filter" glossary term

## Key Concepts

1. **Perfect hash function**: A hash function $h: S \to \{0,\ldots,m-1\}$ that is injective on a known set $S$
2. **k-perfect hash function**: Allows up to $k$ collisions per bucket; trades space for construction time
3. **Rate distortion (two sources)**:
   - **FPR**: Fingerprint collision — a non-member's hash matches a stored fingerprint ($\fprate \approx 2^{-b}$)
   - **FNR**: Perfect hash collision — a member collides with another member and loses its slot (arises with k-perfect hashing)
4. **Space efficiency**: PHF achieves $-\log_2 \fprate$ bits/element asymptotically (optimal), vs. Bloom filter's $-(1/\ln 2)\log_2 \fprate$

## Known Issues

- `references.bib` contains placeholder URLs (`http://example.com`) for self-citations
- Several sections exist but are not included in main.tex — may need integration or archival
- Glossary entries may reference undefined terms if section files are reorganized
- The `\subfile{}` document class pattern differs from `bernoulli_sets/`'s `\input{}` pattern
- `todo.txt` and `todo2.txt` contain active research notes on k-collision handling and Boolean algebra

## Cross-Paper References

- `bernoulli_sets/` cites this paper as `\cite{phf}` — the PHF is a primary motivating example
- The space complexity bound in `bernoulli_sets/sections/entropy.tex` ($-\log_2 \fprate$ bits/element) is proven here for the positive case
- The Bloom filter comparison ($\ln 2 \approx 0.69$ absolute efficiency) appears in both papers
- `bernoulli_sets/sections/adt.tex` (excluded from compilation) contains an expanded ADT treatment that overlaps with this paper's `adt.tex`
