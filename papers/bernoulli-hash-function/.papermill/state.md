# Papermill State: The Bernoulli Hash Function

## Paper Identity

| Field | Value |
|-------|-------|
| **Title** | The Bernoulli Hash Function: Optimal Bernoulli Sets and Bernoulli Maps |
| **Author** | Alexander Towell |
| **Email** | atowell@siue.edu |
| **ORCID** | 0000-0001-6443-9897 |
| **Institution** | Southern Illinois University Edwardsville |
| **Repo** | `queelius/bernoulli-hash-function` |
| **Build system** | Makefile (pdflatex + bibtex) |
| **Notation** | `alex.sty` with `[fancy,section]` |

## Status

| Dimension | Assessment |
|-----------|------------|
| **Draft completeness** | ~95% — all 9 sections + appendix written and coherent |
| **Build** | Compiles to PDF (~598 KB) |
| **Proofs** | All key theorems proved (success probability, space complexity, max entropy, PMF, convergence) |
| **Algorithms** | 4 algorithms presented (MakeBHF-equality, MakeBHF-threshold, Contains, Find) + sampler |
| **Bibliography** | 8 entries — 3 companion papers, 3 self-citations, 2 external (Bloom 1970, Broder & Mitzenmacher 2004, Manning 2008) |
| **Figures** | 1 TikZ figure (`img/fig_shs.tex`) |
| **Venue** | Not yet targeted |

## Section Map

| # | File | Lines | Status | Content |
|---|------|-------|--------|---------|
| 1 | `sections/intro.tex` | 67 | Complete | 3 contributions, companion relations, organization |
| 2 | `sections/prelim.tex` | 113 | Complete | Bit strings, hash/RO, Bernoulli set/map defs, space lower bounds |
| 3 | `sections/shf.tex` | 167 | Complete | Acceptance predicates, success probability, FPR granularity, FNR search simplification, adaptive threshold |
| 4 | `sections/construction.tex` | 178 | Complete | 4 algorithms: MakeBHF (equality + threshold), Contains, Find |
| 5 | `sections/space.tex` | 125 | Complete | Space optimality proof (maps general, set corollary, finite correction, FNR effect) |
| 6 | `sections/entropy.tex` | 104 | Complete | Max entropy theorem, salt PMF, cardinality estimation, entropy-space tradeoff, FP/FN entropy |
| 7 | `sections/prob_model.tex` | 44 | Complete (summary) | FP/FN distributions, expected cardinality (cites companions) |
| 8 | `sections/operations.tex` | 54 | Complete | Intersection/union convergence on BHF instances |
| 9 | `sections/discussion.tex` | 72 | Complete | Obliviousness, Bloom/PHF comparison, practical considerations, encrypted search |
| A | `sections/appendix.tex` | 103 | Complete | Bit-length sampler, PMF derivation (telescoping, alternative via geometric) |

**Total:** ~1027 lines across sections.

## Key Results

1. **Generalized acceptance predicate** (Def 1): threshold test `h(x||b) mod N <= t` generalizes equality test; finer FPR lattice `{j/N}`
2. **Success probability** (Thm 1, 2): equality `v^{m-1}/2^{mu*m}`, threshold `v^m/2^{mu*m}`
3. **FPR granularity** (Thm 3): threshold achieves `{j/N : j=1..N}` vs equality `{2^{-k}}`
4. **Search simplification** (Thm 4): threshold O(m) per salt vs equality O(C(m,p)*m) when FNR > 0
5. **Space optimality** (Thm 5): `-log2(v) + mu` bits/element asymptotically, both predicates
6. **Maximum entropy** (Thm 6): BHF encoding is incompressible conditioned on length
7. **Salt PMF** (Thm 7): `P(N=n) = q^{2^n-1}(1-q^{2^n})` where `q=1-p`
8. **Intersection convergence** (Thm 8): intersecting positive BHFs recovers exact set
9. **Union convergence** (Thm 9): unioning negative BHFs recovers exact set

## Companion Papers

| Paper | Directory | Relationship |
|-------|-----------|-------------|
| Bernoulli sets | `../bernoulli_sets/` | Defines Bernoulli set ADT, set algebra, error propagation |
| Bernoulli maps | `../bernoulli_maps/` | Defines Bernoulli map ADT, map composition |
| Bernoulli data type | `../bernoulli_data_type/` | Type-theoretic generalization |

## Potential Improvements

### Content
- **Bibliography is thin**: only 2 external references (Bloom, Broder-Mitzenmacher). Could cite cuckoo filters, XOR filters, ribbon filters, Pagh/Rodler (cuckoo hashing), or other space-optimal filter work for richer comparison.
- **Companion papers lack publication venues**: all 3 companion refs + 3 self-citations are unpublished working papers with no journal/arxiv identifiers.
- **No experiments or empirical validation**: purely theoretical — even a small table showing construction time vs m for small sets would strengthen the practical claims.
- **Figure count is low**: only 1 TikZ figure. A diagram of the threshold vs equality lattice, or a plot of salt length distribution, would help.
- **Adaptive threshold (Sec 3.5)** is described but not analyzed as thoroughly as the other two predicates.

### Writing
- **Abstract** is strong and self-contained.
- **Notation** is consistent throughout (uses `alex.sty`).
- A few grammar/style nits likely exist but nothing structural.

### Build
- Makefile recently improved with `help`, `draft`, `watch`, `wc`, `cleanall` targets.

## Workflow Notes

- Build: `make` (full) or `make draft` (single-pass)
- Clean: `make clean` (keep PDF) or `make cleanall` (remove PDF)
- Word count: `make wc`

## Review History

- **2026-05-29** (multi-agent-review): **minor-revision**. Critical 0, Major 3, Minor 11, Suggestions 2. Builds clean via `make` (27 pp). Reconciled against the 2026-02-26 review: 3 of 3 prior criticals and 5 of 8 prior majors resolved, no regressions. New major: `MakeBHF-Adaptive` returns `(N, t)` but `Find` recomputes `h(1 || x || b)`, so the adaptive MAP path stores no salt and is not decodable (fix: store `(N, t, b)` for maps; sets are fine with `b=eps`). Contribution 3 overclaims optimality (credit Pagh-Pagh-Rao for efficient achievability; the genuine novelty is the maximum-entropy encoder and the adaptive trade-off). Missing closest map prior art (Bloomier filter, Dietzfelbinger-Pagh retrieval). Two printed closed-form identities in `space.tex` (Thm 5.2 `E[log2 Q]`, Remark `H(Q)`) are false as exact equalities, though their `O(1)` consequences hold. Report: `.papermill/reviews/2026-05-29/review.md`.

## Last Updated

2026-05-29 (multi-agent review; prior entry: 2026-02-26 papermill init)
