# Methodology Auditor Report, The Perfect Hash Filter

**Date**: 2026-05-29
**Scope**: Experimental design, statistical rigor, reproducibility, and the relationship between the paper's empirical claims and the code in the repository. Calibrated to an early (~25%) draft.

## Summary

The paper makes quantitative claims (FPR `= 2^-M`; bits/element formulas; Bloom-filter crossover at `2^-3`/`2^-4`; relative-efficiency tables and plots) but contains zero experiments validating any of them. The abstract promises "a C++ implementation and compare it to the theoretical analysis," but no such comparison exists in the manuscript, and the C++ section the paper does contain points at a stale, non-existent codebase rather than the substantial (~12.8k-LOC) `maph` library that actually sits in the same repository. The efficiency tables and figures in `rd_ph_filter.tex` are presented as results but are analytic evaluations with no stated provenance and, in `adt.tex`, point at CSV data files that do not exist. For an implementation paper, the single highest-value methodological move is to connect the paper's predictions to measurements from the already-present `maph` benchmarks.

Severity counts: Critical: 1 | Major: 3 | Minor: 2

---

## Critical

### C1. Abstract promises an empirical comparison that does not exist; zero experiments
- **Location**: Abstract (`main.tex` line 148): "Finally, we provide a C++ implementation and compare it to the theoretical analysis." Completeness table in `state.md`: "Experiments | 0%".
- **Problem**: There is no experimental section. No measured false-positive rate vs the predicted `2^-M`; no measured bits/key vs the predicted `-(1/r) log2 eps + alpha(r)`; no construction-time or query-throughput numbers; no comparison plot against a real Bloom filter (let alone cuckoo/xor/ribbon). The two figures in `rd_ph_filter.tex` (`fig:abs_eff` table, `fig:rel_eff_bf_PHF`, `fig:rel_eff`) are closed-form curve evaluations, not measurements, and are not labeled as such. The abstract's claim is therefore unsupported.
- **Suggestion**: Either (a) add an experiments section, or (b) remove the empirical-comparison sentence from the abstract until one exists. Given the repo already contains a benchmarkable library (see M1), option (a) is within reach and is the most valuable single addition to the paper.
- **Cross-verified**: Yes (logic lens). The analytic claims the experiments would validate are themselves currently defective (union sign error C1, estimator sign error M2), so experiments must wait on, or be co-developed with, the proof fixes; a measurement against a wrong formula would mislead.

---

## Major

### M1. The paper's C++ section is disconnected from the repository's actual implementation
- **Location**: `sections/cpp_imp.tex` (whole); `main.tex` line 161 includes it as Section "A C++ implementation."
- **Quoted text**: `cpp_imp.tex` line 12: "TODO: break up each function/class/maybe method into separate listings"; the commented-out `\inputminted` paths point to `code/random_approximate_sets_adt/include/approximate_set/dynamic/aset.hpp` (lines 21, 33, 265), and the live `minted` block (lines 94 to 130) is hand-written pseudo-C++ with syntax errors (e.g. `template PerfectHashFn` on line 99, mismatched braces `{` where `}` is meant on lines 110/118, an undeclared `X`/`seed` usage).
- **Problem**: The repository contains a real, substantial C++20 library, `maph` (`include/maph/*.hpp`, `src/maph_cli.cpp`, `benchmarks/`, `tests/v3/`, totaling ~12.8k LOC, with a README claiming O(1) memory-mapped lookups and SIMD batch ops). The paper never mentions `maph`. Instead `cpp_imp.tex` references a different, older tree (`random_approximate_sets_adt/`, `rd_ph_filter.hpp`) that does not exist in the repo. So the "C++ implementation" the paper describes is neither the real code nor compilable; the real code is undocumented by the paper. This is a reproducibility and provenance failure: a reader cannot map any paper claim to runnable code.
- **Suggestion**: Decide which implementation the paper documents. If `maph` is the intended artifact, rewrite `cpp_imp.tex` around its real API and cite the repository; delete the stale pseudo-listings. Confirm the `maph` library implements the PHF construction as described (perfect hash + fingerprint) before claiming it as the realization. If a separate minimal `rd_ph_filter.hpp` is intended as the pedagogical artifact, add it to the repo and make the listing paths resolve.

### M2. Analytic "results" tables and figures have no stated provenance, and some reference missing data files
- **Location**: `rd_ph_filter.tex` `fig:abs_eff` (lines 273 to 296, a numeric table of `r*`, `e*(X)`, `e(X,Y)` to 6 digits) and `fig:rel_eff_bf_PHF` (lines 298 to 335); `adt.tex` `fig:efficiency_vs_fprate_union_paset` (lines 517 to 549) which does `\addplot ... table [col sep=comma] {data/data1.csv}` and three more CSVs.
- **Problem**: The 6-significant-figure optimal-load-factor table is presented without saying how `r*` was computed (it is presumably the argmax of the absolute-efficiency expression, solved numerically), so it is not reproducible as written. Worse, the union-efficiency figure in `adt.tex` reads four CSV files (`data/data1.csv`, `data/data.5.csv`, `data/data.25.csv`, `data/efficiency_fprate_union.csv`) and the `data/` directory does not exist in the repository, so this figure cannot build (it is currently inside a `\COMMENT{}` block, but the live `fig:cor_union_same_fprate` just below it duplicates the same caption/label, see format report).
- **Suggestion**: State the computation behind the optimization table (and ideally ship the script under `research/`). Either add the missing `data/` CSVs or convert the plots to closed-form `\addplot {expr}` (the sibling live figure already does this). Remove duplicate captions/labels.

### M3. Key assumptions are asserted but never validated, and the "deterministic algorithm" reconciliation is hand-waved at the crucial number
- **Location**: `rd_ph_filter.tex` lines 172 to 179 (cryptographic-hash assumptions); `adt.tex` lines 154 to 229 (compatibility of a deterministic generator with the probabilistic model).
- **Quoted text**: `rd_ph_filter.tex` line 179: "These assumptions ensure that the \gls{gls-phf} satisfies the element-wise independence axiom of the Bernoulli set model"; `adt.tex` line 206: "at `\Card{U} = 2`, the probability of this outcome is `$?$`."
- **Problem**: The independence axiom is *assumed* to follow from "cryptographic hash function," not argued, and is never checked empirically (a chi-square or measured-pairwise-correlation test on the implementation would substantiate it). The `adt.tex` discussion of how a deterministic implementation can be "compatible with the probabilistic model" is conceptually reasonable but lands on a "$?$" exactly where a number is needed, undercutting the methodological point it is trying to make.
- **Suggestion**: Add a small empirical independence check (measured FPR distribution across many random seeds vs the binomial prediction from the family's `bernoulli_sets` paper). Fill in the `\Card{U}=2` probability.

---

## Minor

### m1. No experimental protocol, datasets, or hardware described (because there are no experiments)
- **Location**: n/a (absent).
- **Problem**: When experiments are added, the paper will need the standard reproducibility scaffolding: key sets and sizes, target FPRs swept, MPHF construction used (the paper says it uses CHD, `chd`), hardware, repetitions, and seed handling.
- **Suggestion**: Plan the protocol now so the experiments section is reproducible from the outset.

### m2. The `k`-perfect placement model is stated without simulation support
- **Location**: `k_perfect_hashing.tex` lines 12 to 27.
- **Problem**: The placement-success probability `p(k)` (with the indexing concern raised in logic m4) is exactly the kind of combinatorial claim that a short Monte Carlo would either confirm or correct cheaply.
- **Suggestion**: Validate `p(k)` by simulation for small `m, N, k` before relying on it for the FNR analysis.

---

## Notes

- The repository's test/benchmark infrastructure (`tests/v3/`, `benchmarks/bench_*.cpp`, `bench_comparison.cpp`, `bench_ycsb.cpp`) is a real asset: measured throughput/latency and a Bloom/cuckoo comparison may already be obtainable from it. The methodological gap is largely one of *connecting existing code to the paper*, not building from nothing.
- Positively: the analytic framework (absolute vs relative efficiency, the load-factor optimization) is the right way to compare these structures, and matches subfield norms. It just needs measured validation and honest provenance.
