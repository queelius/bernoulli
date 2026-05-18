# Design: Part II (From Bits to Sets) of the Bernoulli Textbook

**Author:** Alexander Towell
**Date:** 2026-05-17
**Status:** Design (pre-implementation)
**Parent spec:** `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`
**Sibling spec:** `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md`
**Scope:** Section-level outline for chapters 5-8 (Part II, ~110 pp). Authoritative for Plans 5-8 (the per-chapter implementation plans that draft these chapters and run the Part II integration check).

## 1. Purpose

Part II lifts the framework from the noisy bit (Part I) to the random approximate set. The atom from Part I becomes the membership predicate of an approximate set; the algebra of Part I's noisy bits becomes the set-operation error propagation of chapter 6; chapter 7 develops the classification measures (PPV, NPV, recall, F1) that chapter 1 §1.4 explicitly deferred for proper estimator and CI treatment; chapter 8 sets up the information-theoretic bounds whose constructive achievement is the climax of Part IV (the BHF).

By the end of Part II, the reader has seen: an approximate set as a noisy bit per universe element (chapter 5, Bloom filter from scratch); the algebra of set operations under noise (chapter 6, including the cancellation phenomena and the perfect filter line); the proper statistical treatment of classification measures and their finite-sample uncertainty (chapter 7); the information-theoretic floor on space per element for a target error rate (chapter 8, setting up "space-accuracy duality" as one of the Five Core Principles).

Part II is the publishable second part. With Part I + Part II + Part III (~330 pp) the book is a graceful exit per the master spec's Milestone 1.

## 2. Inherited Commitments (from Part I spec)

The following commitments carry forward unchanged from the Part I design spec (`2026-05-02-part1-design.md`) and are NOT re-debated here:

- **Audience:** B+D (adjacent-field grad students through smart undergraduates).
- **Format:** Pedagogical monograph in the MacKay tradition, single voice, intuition-first, citations to underlying papers via chapter-end Bibliographic Notes.
- **Notation:** alex.sty macros throughout. `\fprate` = ε, `\fnrate` = ω, `\tprate` = τ, `\tnrate` = η. New macros for Part II are added on demand to `book/preamble.tex` (not alex.sty, which is shared with the papers); see §3.1 below.
- **Learning-outcomes box** per chapter, 3 bullets in B+D style.
- **10-12 exercises per chapter** with ★/★★/★★★ markers, approximately 3/5/3 distribution.
- **Build pipeline:** LaTeX (book class), biblatex with biber backend, the Makefile established by Plan 0.
- **Per-task discipline (Path A):** spec-compliance reviewer + quality reviewer + fix loop per section. Already battle-tested across Plans 1-4.
- **Soul-voice constraints:** No Unicode em-dash (U+2014), no "lever" + "age" as a single word.

## 3. Part II-Specific Decisions

Decisions that are NEW to Part II and not predetermined by Part I:

### 3.1 Predicate-First Bridge from Atom to Set

Part II opens chapter 5 by the predicate framing: an approximate set is a function $\tilde A : U \to \{\top, \bot\}$ from the universe $U$ to the noisy-bit object of Part I. Each evaluation $\tilde A(x)$ is a $\Bernoulli{\BoolType}$ instance, with its own per-element error rates (which Axiom 2 then constrains to be per-block-stable). The Bloom filter is the canonical example: $\tilde A(x)$ checks all $k$ hashes; output is $\top$ iff all $k$ bits are set.

This framing has three pedagogical payoffs:
1. The atom-outward trajectory continues seamlessly. The noisy bit IS the atom; the approximate set IS a function whose codomain is the atom.
2. The membership predicate is observable in code (the `__contains__` method). Readers see the abstraction as data structure plus probabilistic guarantee, which matches their intuition.
3. The Bloom filter falls out of the predicate framing as the simplest non-trivial instance, not as a separate "data structure to learn."

New notation: $\tilde A$ for an approximate set (alex.sty's `\ASet`); $A$ for the underlying true set; $U$ for the universe; $\tilde A(x) = \mathbf{1}\{x \in \tilde A\}$ as the membership predicate. Verify alex.sty's coverage; add `\providecommand` blocks to `book/preamble.tex` for any gaps.

### 3.2 Bloom Filter as Part II Running Example

The Bloom filter threads through chapters 5, 6, 7, and is referenced in chapter 8. It is introduced in §5.2 as the canonical FNR-zero approximate set; revisited in §6.1 (union of two Bloom filters), §6.4 (the FNR-zero "perfect filter" line as an algebraic constraint); §7.4 (Bloom filter's PPV depends on the workload's prevalence); §8.5 (the entropy floor; the BHF achieves it, the standard Bloom filter falls short). The thread does for Part II what the BSC does for Part I: a single concrete example readers can name on every page.

The Part I running threads (biased coin, BSC, classifier verdict) make cameos:
- The classifier verdict thread (§1.1 Face 3) is the natural worked example for chapter 7's PPV/NPV/F1 development.
- The BSC thread (§1.1 Face 2, §2.1 formal) is the natural worked example for chapter 8's entropy treatment of a binary noisy channel.
- The biased coin thread does NOT return in Part II; it had its closing in §4.5. Honest restraint avoids the "force the thread to return" failure mode.

### 3.3 Chapter 7 Does Double Duty

Chapter 1 §1.4 deferred the proper treatment of binomial estimators, CIs, and the Wald-vs-Wilson trade-off to chapter 7 ("the full treatment of estimation lives in chapter 7"). Chapter 7 must deliver on that deferral AND develop PPV, NPV, recall, F1, and the prevalence-dependence point.

Sequencing within chapter 7: §7.1 quick recap (the §1.4 setup with the cleaner notation Part II now has). §7.2 binomial estimator: bias, variance, MLE (proves what §1.4 stated). §7.3 confidence intervals: Wald, Wilson, Clopper-Pearson; the discreteness sawtooth from the §1.4 notebook explained rigorously. §7.4 derived measures: PPV, NPV, F1 as random variables; delta-method CIs; prevalence dependence as the central caveat. §7.5 the classification-measures companion paper as the depth reference. ~28 pp; the longest chapter of Part II.

### 3.4 Chapter 8 is the "Light Substantive" Chapter

Master spec marks ch8 as "light" (notebook is light: entropy calculator, optimal-rate plots). The information-theoretic floor is stated and the consequence (an approximate set with error rate ε needs at least $-\log_2 \varepsilon$ bits per element) is derived. The construction that achieves the bound is NOT in chapter 8 (that is chapter 14, the BHF). Chapter 8's job is to make the reader want chapter 14.

Sequencing: §8.1 Shannon entropy refresher (one page). §8.2 the noisy-channel coding theorem in the BSC special case, as motivation. §8.3 the lower bound: any approximate set with FPR ε needs at least $-\log_2 \varepsilon$ bits per element. §8.4 the gap: standard Bloom filter costs $\approx 1.44 \cdot \log_2(1/\varepsilon)$ bits per element, a $44\%$ overhead. §8.5 forward-reference to chapter 14: the BHF construction closes the gap. ~22 pp; the shortest chapter of Part II.

### 3.5 Notebook Discipline

Per master spec table:
- Ch5: substantive notebook (`ch05-approximate-sets.ipynb`). Bloom filter from scratch in Python; empirical FPR vs theoretical $(1 - e^{-kn/m})^k$; the optimal $k$ derivation.
- Ch6: light notebook (`ch06-set-composition.ipynb`). Set-operation error propagation simulator; verifies the closed-form composition formulas.
- Ch7: substantive notebook (`ch07-classification-measures.ipynb`). PPV/NPV/F1 as random variables; bootstrap CIs; delta-method CIs; comparison of Wald / Wilson / Clopper-Pearson on the §1.4 sawtooth example.
- Ch8: light notebook (`ch08-information-bounds.ipynb`). Entropy floor vs standard Bloom filter cost across ε; ratio plot showing the $44\%$ overhead.

## 4. Chapter Outlines

Compact tables. Section lengths sum to chapter targets; see §6 for the page budget rationale.

### Chapter 5: Approximate Sets and Predicates (~28 pp, has notebook)

**Learning outcomes box:** define an approximate set as a function $U \to \Bernoulli{\BoolType}$; recognize the Bloom filter as one such function; compute its empirical and theoretical FPR; state the FNR-zero condition that distinguishes "one-sided" approximate sets.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 5.1 | From Atom to Set | ~4 | fresh | The predicate framing. An approximate set is a function from the universe to the noisy-bit atom of Part I. Backward reference to chapter 4 §4.5 (the formal $\Bernoulli{\BoolType}$ type). |
| 5.2 | The Bloom Filter From Scratch | ~7 | reformulate `bernoulli_sets/algebra_of_sets.tex` + fresh Bloom-filter derivation | Construction: $m$ bits, $k$ hash functions. Membership check: all $k$ bits set. FPR derivation: $(1 - (1 - 1/m)^{kn})^k \approx (1 - e^{-kn/m})^k$. The optimal $k = (m/n) \ln 2$. Insertion-only. |
| 5.3 | The Predicate Algebra | ~5 | reformulate `bernoulli_sets/bernoulli_model.tex` | A predicate $\tilde A(x)$ is a $\Bernoulli{\BoolType}$ instance with per-element rates that, under Axiom 2, are per-block-stable. The block structure for an approximate set is $\{A, U \setminus A\}$. Connection back to chapter 4's Kronecker theorem: $n$ queries factor as the Kronecker product. |
| 5.4 | One-Sided vs Two-Sided Approximate Sets | ~5 | fresh | The Bloom filter has $\fnrate = 0$ (one-sided). General Bernoulli sets allow $\fnrate > 0$ (two-sided). When is each appropriate? FNR-zero buys safety (set membership is conservative); FNR-positive buys space (smaller representation). |
| 5.5 | What Comes Next | ~3 | fresh | Chapter 6 builds the algebra of set operations on top. Chapter 7 develops classification measures. Chapter 8 derives the information-theoretic floor. Chapter 14 constructs the optimal representation (BHF). |
| 5.6 | Bibliographic Notes | ~2 | fresh | Bloom (1970); `bernoulli_sets` paper; survey of approximate-set data structures (Mitzenmacher-Upfal §5). |
| Exercises | 10-12 | ~2 | fresh | 3/5/3 distribution. |

### Chapter 6: Composition of Sets (~24 pp, light notebook)

**Learning outcomes box:** derive union, intersection, complement, difference error rates for approximate sets from chapter 3's Boolean algebra; recognize the "perfect filter line" (the FNR-zero constraint surface) as a closed subalgebra; identify when set composition leaves the FPR ε-near-zero regime.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 6.1 | Union of Approximate Sets | ~5 | reformulate `bernoulli_composition/set_theory.tex` | Two Bloom filters' union by bit-OR: FPR_total = 1 - (1 - ε_1)(1 - ε_2), FNR_total = 0 if both are one-sided. Worked example. |
| 6.2 | Intersection, Complement, Difference | ~5 | reformulate `bernoulli_composition/set_theory.tex` | Intersection: FPR_total = ε_1 ε_2 (cleaner than union). Complement swaps FPR and FNR (as in §1.1 exercise 6 and §3.2). Difference: $A \setminus B = A \cap \bar B$. Each operation's algebra derived. |
| 6.3 | Cancellation and the Loss of One-Sidedness | ~5 | fresh; papers have fragments in `bernoulli_composition/uncertain_rates.tex` | Complement of a one-sided set is one-sided in the OTHER direction: FNR-zero becomes FPR-zero. Composition can escape the perfect-filter line; this matters for chapter 7's PPV story and chapter 15's perfect hash filters. |
| 6.4 | The Perfect Filter Line | ~4 | fresh; connects `bernoulli_composition/set_theory.tex` to ch 14-15 forward | FNR = 0 defines a one-dimensional subalgebra under the union and intersection (but not under complement). This is the "perfect filter" constraint Surface that chapter 15 explores constructively. |
| 6.5 | What Comes Next | ~1 | fresh | Chapter 7 measures the quality of an approximate set. Chapter 8 bounds its space. |
| 6.6 | Bibliographic Notes | ~2 | fresh | `bernoulli_composition` paper; the composition theorem precedent in `bernoulli_sets`. |
| Exercises | 10-12 | ~2 | fresh | 3/5/3 distribution. |

### Chapter 7: Classification Measures (~28 pp, has notebook)

**Learning outcomes box:** define PPV, NPV, recall, F1 in terms of FPR/FNR and prevalence; estimate them from samples with proper confidence intervals (Wilson, Clopper-Pearson, delta-method); recognize the prevalence-dependence of precision and the discreteness sawtooth from §1.4.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 7.1 | The §1.4 Setup Revisited | ~3 | reformulate ch1 §1.4 | Single-page recap of binomial estimators and the Wald CI from chapter 1. Now treated with the cleaner notation and the predicate framing of chapter 5. |
| 7.2 | The Binomial Estimator: Properties | ~5 | reformulate `bernoulli_classification_measures/preliminaries.tex` | Unbiasedness, variance, MLE. The deferral from §1.4 is now retired. |
| 7.3 | Confidence Intervals Properly | ~5 | fresh + `bernoulli_classification_measures/appendix.tex` for variance forms | Wald, Wilson, Clopper-Pearson, Jeffreys. The discreteness sawtooth from §1.4 explained rigorously. |
| 7.4 | Derived Measures: PPV, NPV, F1 | ~7 | reformulate `bernoulli_classification_measures/measures.tex` | PPV, NPV, F1 as functions of FPR, FNR, and prevalence. Each as a random variable; delta-method CIs. Prevalence dependence as the central caveat. Bloom filter PPV under varying workloads. |
| 7.5 | Worked Application: Bloom Filter Diagnostics | ~3 | fresh | Tie back to §5.2's Bloom filter. Given a Bloom filter with measured ε and a workload with measured prevalence, compute PPV and a CI. |
| 7.6 | Bibliographic Notes | ~2 | fresh | `bernoulli_classification_measures` paper; Pepe (2003) for medical diagnostic testing; Manning-Raghavan-Schütze for IR vocabulary. |
| Exercises | 10-12 | ~2 | fresh | 3/5/3 distribution. |

### Chapter 8: Information-Theoretic Bounds (~22 pp, light notebook)

**Learning outcomes box:** state Shannon entropy and the noisy-channel coding theorem in the BSC case; derive the $-\log_2 \varepsilon$ bits-per-element lower bound for an approximate set with FPR $\varepsilon$; quantify the standard Bloom filter's $44\%$ space overhead.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 8.1 | Shannon Entropy Refresher | ~3 | fresh | One page on $H(X)$, mutual information $I(X;Y)$, and the BSC capacity $1 - H(\varepsilon)$. Stated, not derived. Cover and Thomas as the depth reference. |
| 8.2 | Channel Capacity in the BSC | ~3 | fresh | $C = 1 - H(\varepsilon)$. The BSC running thread from Part I returns here. |
| 8.3 | The Entropy Floor for Approximate Sets | ~6 | reformulate `bernoulli_entropy/entropy.tex` | Theorem: any approximate set with FPR $\varepsilon$ requires at least $-n \log_2 \varepsilon$ bits to represent (where $n$ is the underlying set's size). Proof sketch via the source-coding theorem. |
| 8.4 | The Bloom Filter's Gap | ~4 | reformulate `bernoulli_entropy/space_complexity.tex` | Standard Bloom filter cost $\approx 1.44 \cdot n \log_2(1/\varepsilon)$ bits. The $44\%$ overhead is the gap to the entropy floor. |
| 8.5 | What Comes Next | ~2 | fresh | The constructive achievement of the entropy bound is chapter 14 (the Bernoulli Hash Function). Chapter 15 builds on it for one-sided perfect filters. |
| 8.6 | Bibliographic Notes | ~2 | fresh | `bernoulli_entropy` paper; Cover and Thomas; Carter and Wegman (perfect hashing). |
| Exercises | 10-12 | ~2 | fresh | 3/5/3 distribution. |

## 5. Forward and Backward Reference Map

| From | To | Form |
|---|---|---|
| §5.1 | ch 4 §4.5 (formal `\Bernoulli{\BoolType}` type) | backward |
| §5.2 | ch 1 §1.1 Face 3 (classifier-verdict thread context) | backward, light |
| §5.3 | ch 4 §4.4 (Kronecker theorem) | backward |
| §5.5 | ch 6 (set composition), ch 7 (classification measures), ch 8 (entropy floor), ch 14 (BHF) | forward |
| §6.1 | ch 3 §3.3 (composition theorem) | backward |
| §6.3 | ch 7 §7.4 (PPV story), ch 15 (perfect filters) | forward |
| §6.4 | ch 14 (BHF), ch 15 (PHF) | forward |
| §7.1 | ch 1 §1.4 (the deferred treatment) | backward, **retires** the §1.4 deferral |
| §7.3 | ch 1 §1.4 notebook (the Wald sawtooth) | backward |
| §7.4 | ch 5 §5.2 (Bloom filter), ch 1 §1.2 (precision/recall cross-walk) | backward |
| §8.2 | ch 2 §2.1 (BSC), ch 1 §1.1 Face 2 | backward |
| §8.5 | ch 14 (BHF) | forward |

Forward references to Parts III-V (chapters 9-18) MUST resolve. Most labels exist (the Plan 0 scaffold defined `\label{ch:N}` for every chapter). Verify in Plan 5 Task 0.

## 6. Page Budget

| Chapter | Target | Fresh writing share | Notes |
|---|---|---|---|
| Ch 5 | ~28 pp | ~50% | Bloom-filter derivation entirely fresh; predicate algebra reformulated from `bernoulli_sets` |
| Ch 6 | ~24 pp | ~40% | Set-op reformulation from `bernoulli_composition`; the perfect-filter-line section is fresh |
| Ch 7 | ~28 pp | ~60% | CI section fresh; PPV/NPV/F1 reformulated from `bernoulli_classification_measures` |
| Ch 8 | ~22 pp | ~50% | Entropy bound reformulated from `bernoulli_entropy`; framing fresh |
| **Total** | **~102** | **~50%** | Part I came in 28% over; expect Part II ~130 pp actual; within the 90-150 pp envelope per part |

Part I + Part II = ~210 pp actual against the Milestone 1 target of 330 pp (which covers I+II+III). Part III then has ~120 pp budget; that aligns with master spec section 5's chapter count (5 chapters: 9, 10, 11, 12, 13).

## 7. Sequencing for Plans 5-8

Per Part I's lesson (drafting chapter 1 last, with full knowledge of chapters 2-4, worked well), draft Part II in dependency order:

1. **Chapter 5 first** (Plan 5). Establishes the predicate framing and the Bloom filter, which chapters 6, 7, 8 all build on.
2. **Chapter 6** (Plan 6). Set-operation algebra; uses chapter 3 §3.3 composition theorem and the Bloom filter from §5.2.
3. **Chapter 7** (Plan 7). Classification measures; retires the §1.4 deferral; uses Bloom-filter framing from §5.2.
4. **Chapter 8** (Plan 8). Entropy bounds; uses BSC from chapter 2 and Bloom filter from §5.2.
5. **Part II integration check** (Plan 8 Task 10, mirroring Plan 4 Task 10).

Each plan follows Path A discipline (subagent-driven per task, spec + quality reviewers, fix loop). Plan-numbering: Plans 5, 6, 7, 8.

## 8. Open Action Items

Items deferred for resolution during Plan implementation:

1. **alex.sty macro coverage for set notation.** `\ASet` and similar may or may not exist. Plan 5 Task 0 verifies; add local `\providecommand` in `book/preamble.tex` for gaps (do not modify alex.sty, which is shared with the papers).
2. **Bloom filter notation conventions.** The classic Bloom filter literature uses $n$ for items, $m$ for bits, $k$ for hashes. These conflict with chapter 1's $n$ = sample size. Resolve: keep the classic $(m, k, n)$ inside chapter 5 §5.2 with a one-paragraph notation note flagging the variable reuse; in other chapters, use $n_{\text{items}}$ if ambiguity matters.
3. **Chapter 8's depth.** "Light" per master spec, but the entropy lower bound has a non-trivial proof (source-coding theorem reduction). Decide during Plan 8 drafting whether the proof goes in the main text or an appendix.

## 9. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Chapter 7 ballooning to swallow chapter 1's deferral + PPV/NPV/F1 + CIs in 28 pp. | Hard cap at 32 pp; if overshoot, push delta-method derivation to Appendix D. |
| Chapter 5's Bloom-filter derivation duplicates content in `bernoulli-hash-function` paper. | Reformulate at pedagogical depth (not paper depth); cite the paper for the formal optimality proof. |
| Chapter 8's "light" framing tempts hand-waving. | The entropy floor's statement and the gap-to-Bloom-filter calculation must both be rigorous; only the source-coding-theorem PROOF can be sketched. |
| Predicate-first framing in §5.1 is unfamiliar to readers expecting data-structure-first. | §5.1 explicitly previews §5.2 (Bloom filter as the canonical instance); the abstraction is named before the example, but the example arrives within four pages. |

## 10. Out of Scope

Part II does not, and should not become:

- A general primer on information theory (chapter 8 uses entropy and BSC capacity informally; Cover and Thomas remains the depth reference).
- A general primer on classification (chapter 7 develops PPV/NPV/F1 via the Bernoulli-set framing; Hastie-Tibshirani-Friedman remains the breadth reference).
- A survey of approximate data structures (chapter 5 introduces the Bloom filter; chapter 14 covers the BHF; HyperLogLog, CountMin, MinHash are chapter 10 in Part III).
- The constructive optimal-set chapter (chapter 14 / Part IV). Chapter 8 sets up the bound; chapter 14 achieves it.

## 11. Success Criteria for Part II

Part II succeeds if:

1. A reader who has finished Part I can finish chapters 5-8 in two focused weeks and emerge able to (a) build a Bloom filter from scratch and derive its FPR, (b) state the composition theorem for set operations, (c) compute PPV and a proper CI for a classifier on a workload of given prevalence, (d) state the information-theoretic floor for approximate-set space cost.
2. Chapter 7's retiring of the §1.4 deferral feels earned: the reader who paused on the Wald sawtooth in the §1.4 notebook now understands precisely why and what to use instead.
3. The Bloom filter running thread feels carried, not contrived. A reviewer can point at any of §6.1, §7.4, §8.4 and say "yes, this is doing real pedagogical work tying back to §5.2."
4. Chapter 8 leaves the reader wanting chapter 14. The $44\%$ overhead is the right kind of unfinished business.
