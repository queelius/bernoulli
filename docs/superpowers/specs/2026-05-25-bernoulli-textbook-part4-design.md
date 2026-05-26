# Design: Part IV (Optimality and Construction) of the Bernoulli Textbook

**Author:** Alexander Towell
**Date:** 2026-05-25
**Status:** Design (pre-implementation)
**Parent spec:** `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`
**Sibling specs:** Part I (`2026-05-02`), Part II (`2026-05-17`), Part III (`2026-05-23`)
**Scope:** Section-level outline for chapters 14-15 (Part IV, ~60 pp).

## 1. Purpose

Part IV is the constructive payoff to Part II's chapter 8 entropy floor and chapter 6's perfect-filter line. Two chapters:

- **Chapter 14: Optimal Bernoulli Sets (BHF).** Constructs the Bernoulli Hash Function (BHF), an approximate-set representation that achieves chapter 8 §8.3's entropy floor of $-\log_2 \fprate$ bits per element on the FNR-zero axis. Closes the standard Bloom filter's $\log_2 e \approx 1.443$ overhead derived in §8.4.

- **Chapter 15: Perfect Hash Filters (BPHF).** Constructs the Bernoulli Perfect Hash Filter (BPHF), a constructive realization on the FPR-zero axis (chapter 6 §6.4 perfect-filter-line concept) for a designated input set.

Together these two chapters give the constructive twin of Part II's analytical foundation: where Parts I-III named the right object and proved the bound, Part IV builds the constructions that meet the bound.

## 2. Inherited Commitments

Same as Parts II and III: B+D audience; monograph format; alex.sty notation; learning-outcomes box per chapter; 10-12 exercises with star markers (3/5/3); Path A subagent-driven Plan execution; soul-voice hook discipline.

## 3. Part IV-Specific Decisions

### 3.1 Construction Discipline

Both chapters follow the same structural template: name the problem (achieving a target on the perfect-filter line), state the construction, derive its space/time costs, prove it meets the target, give a worked example.

### 3.2 Source Material per Chapter

- **Chapter 14:** `papers/bernoulli-hash-function/` (primary source, includes the embedded `maph` C++ library); chapter 8 §8.3 entropy floor and §8.4 Bloom gap; chapter 5 §5.2 Bloom filter (the predecessor).
- **Chapter 15:** `papers/bernoulli-phf/` (primary source); chapter 6 §6.4 perfect-filter line; Carter-Wegman perfect hashing.

### 3.3 Notebook Discipline

- Ch 14: substantive notebook (BHF construction; demonstrate reaching the entropy bound).
- Ch 15: substantive notebook (BPHF; ranked search).

## 4. Chapter Outlines

### Chapter 14: Optimal Bernoulli Sets (BHF) (~30 pp, has notebook)

**Learning outcomes:** state the BHF construction; derive its space cost as $\lceil -\log_2 \fprate \rceil$ bits per element (matching the chapter 8 entropy floor exactly); compare to the standard Bloom filter's $\log_2 e \approx 1.443$ overhead; identify the trade-offs (BHF gives optimal space at the cost of construction time).

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 14.1 | The Optimality Question | ~3 | fresh | Recall ch 8 §8.3 floor and §8.4 Bloom gap. Open question: can the gap be closed constructively? |
| 14.2 | The BHF Construction | ~7 | reformulate `bernoulli-hash-function/` | Perfect hash function $\phi$ from designated set $A$ to $[n]$. Per-element fingerprint of $r = \lceil -\log_2 \fprate \rceil$ bits. Membership test: hash query, compare fingerprint. |
| 14.3 | Space Analysis | ~6 | reformulate paper | The BHF achieves the entropy floor exactly: $|A| \cdot r$ bits + perfect-hash overhead (asymptotically negligible). |
| 14.4 | False-Positive Rate Analysis | ~5 | reformulate paper | $\fprate \le 2^{-r}$ by fingerprint-collision argument; FNR = 0 by construction. |
| 14.5 | Construction Time and Trade-offs | ~4 | reformulate paper | Building the perfect hash function is $O(n)$ expected; BHF is appropriate when the set is static or rarely updated. |
| 14.6 | Bridge | ~2 | fresh | Chapter 15 covers the FPR-zero counterpart (BPHF) for ranked search. |
| 14.7 | Bibliographic Notes | ~2 | fresh | `bernoulli-hash-function`, Carter-Wegman, BBHash perfect-hash literature. |
| Exercises | ~2 | fresh | 11 with star markers. |

### Chapter 15: Perfect Hash Filters (BPHF) (~28 pp, has notebook)

**Learning outcomes:** state the BPHF construction; recognize it as the FPR-zero axis counterpart of chapter 14's BHF; derive its space cost; recognize "ranked search" as the natural BPHF application.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 15.1 | From BHF to BPHF | ~3 | fresh | Recall ch 14; lift to the FPR-zero axis via complement structure. |
| 15.2 | The BPHF Construction | ~7 | reformulate `bernoulli-phf/` | Perfect hash function plus per-element rank value. |
| 15.3 | Space and Time Analysis | ~5 | reformulate paper | Similar to chapter 14's analysis. |
| 15.4 | Ranked Search Application | ~6 | reformulate paper | Top-k retrieval as the canonical BPHF use case. |
| 15.5 | Bridge to Part V | ~2 | fresh | Forward to chapter 16 (not-Bernoulli) and chapters 17-18 (cipher maps, encrypted search). |
| 15.6 | Bibliographic Notes | ~2 | fresh | `bernoulli-phf`, ranked-search literature. |
| Exercises | ~2 | fresh | 11 with star markers. |

## 5. Forward and Backward Reference Map

| From | To | Form |
|---|---|---|
| §14.1 | ch 8 §8.3 entropy floor (`thm:entropy-floor`), §8.4 Bloom gap (`prop:bloom-overhead`) | backward |
| §14.2 | ch 5 §5.2 Bloom filter (`def:bloom-filter`) | backward |
| §14.4 | ch 6 §6.4 perfect filter line (`def:perfect-filter-line`) | backward |
| §15.1 | ch 14 §14.2 BHF | backward |
| §15.2 | ch 6 §6.4 perfect-filter line (`def:perfect-filter-line`) | backward |
| §15.5 | ch 16, 17, 18 | forward (Part V) |

## 6. Page Budget

| Chapter | Target | Notes |
|---|---|---|
| Ch 14 | ~30 pp | BHF construction + space analysis |
| Ch 15 | ~28 pp | BPHF + ranked search |
| **Total** | **~58** | Expect ~70pp actual (~20% over per Plans 1-13 pattern) |

Part IV is shorter than Parts II and III. Combined with Part V (~110pp target for chapters 16-18), Milestone 2 totals ~170pp.

## 7. Sequencing for Plans 14-15

- Plan 14: chapter 14 (BHF) first.
- Plan 15: chapter 15 (BPHF), depends on chapter 14.

## 8. Open Action Items

1. **Notation for perfect hash function.** Likely $\phi$ or $h^*$ for the perfect hash; check alex.sty in Plan 14 Task 0.
2. **Decide chapter 14's `ch:composition` follow-up** (recorded in Plan 13 integration): either rename chapter 4 refs to `ch:set-composition`, or add `ch:composition` as a label alias to chapter 6.

## 9. Out of Scope

- Full implementation details of the `maph` C++ library (cite the paper).
- Detailed comparison with cuckoo filter, quotient filter (mention briefly in §14.7 bib notes).

## 10. Success Criteria for Part IV

Part IV succeeds if:

1. The reader can describe both the BHF and the BPHF constructively after the chapter.
2. The reader recognizes that chapter 14 closes the chapter 8 §8.3 entropy-floor gap exactly (the 44% overhead from standard Bloom is gone).
3. The reader sees chapter 14 (FNR-zero) and chapter 15 (FPR-zero) as the two constructive realizations on the perfect-filter line (chapter 6 §6.4).
