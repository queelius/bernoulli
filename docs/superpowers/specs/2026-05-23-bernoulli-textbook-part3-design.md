# Design: Part III (From Sets to Maps) of the Bernoulli Textbook

**Author:** Alexander Towell
**Date:** 2026-05-23
**Status:** Design (pre-implementation)
**Parent spec:** `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`
**Sibling specs:** Part I (`2026-05-02`), Part II (`2026-05-17`)
**Scope:** Section-level outline for chapters 9-13 (Part III, ~120 pp). Authoritative for Plans 9-13 (per-chapter implementation plans).

## 1. Purpose

Part III is the major abstraction step of the book: it lifts $\Bernoulli{\BoolType}$ (the atomic noisy bit of Part I, generalized to approximate sets in Part II) to $\Bernoulli{T}$ for arbitrary algebraic types $T$. The model-order ceiling at 2 (chapter 2 §2.4) breaks here: n-ary channels enter formally in chapter 9, then sketches in chapter 10 give concrete instantiations (CountMin, HyperLogLog, MinHash), chapter 11 treats randomized algorithms rigorously (Miller-Rabin from §3.4 now formal, plus RP, BPP, Las Vegas vs Monte Carlo), chapter 12 covers approximate relations, and chapter 13 axiomatizes the algebra of approximate types.

By the end of Part III, the reader has seen the framework's full generality: $\Bernoulli{T}$ for any algebraic type, the composition algebra for maps and relations, the sketch family as a special case, and the formal type system that lets all of these compose by construction.

Part III closes Milestone 1 (~330 pp Parts I + II + III). After Part III the book is publishable as a graceful exit.

## 2. Inherited Commitments

Same as Part II spec: B+D audience; monograph format; alex.sty notation; learning-outcomes box per chapter; 10-12 exercises with star markers (3/5/3); biber/biblatex; Path A subagent-driven Plan execution discipline; soul-voice hook constraints (full banned-phrase list in `$CLAUDE_PLUGIN_ROOT/hooks/check-banned-phrases.sh`).

## 3. Part III-Specific Decisions

### 3.1 Lifting from Atom to Algebraic Type

The central conceptual move of Part III: $\Bernoulli{T}$ is the type of random approximate values over $T$. For $T = \BoolType$ this is the Part I atom. For $T = \{1, 2, \ldots, K\}$ (a finite enum) this is an n-ary channel. For $T = \mathbb{N}$ this is a CountMin-style estimator. For general algebraic types ($\Sigma$ for sum, $\Pi$ for product, $L$ for lists, $T \to U$ for functions), chapter 13 develops the compositional algebra.

The lifting is type-driven: the structure of $T$ governs the structure of the channel matrix (now no longer 2x2) and the composition rules. The Kronecker theorem from chapter 4 §4.4 generalizes to: $\Bernoulli{T \times U} \cong \Bernoulli{T} \otimes \Bernoulli{U}$ under the right axioms.

### 3.2 Running Examples for Part III

- **CountMin (chapter 10):** the simplest non-trivial sketch. Multi-row counters with hash-based collisions; query returns over-estimates.
- **HyperLogLog (chapter 10):** cardinality estimator. Probabilistic but very space-efficient; logarithmic-in-cardinality space.
- **MinHash (chapter 10):** Jaccard similarity estimator. Compose into LSH for approximate nearest neighbor.
- **Miller-Rabin (chapter 11):** chapter 3 §3.4's worked example, now formal. Cast as a $\Bernoulli{\BoolType}$ via repeated witness sampling.
- **Approximate set difference (chapter 12):** revisits chapter 6 §6.2 from the relation perspective.

These threads link Part III to Part II (CountMin and HyperLogLog generalize Bloom; MinHash composes via the algebra of chapter 13) and to Part I (Miller-Rabin formalization closes §3.4's deferral).

### 3.3 N-ary Channels (Chapter 9)

The headline conceptual move. Chapter 2 §2.4 stopped at model-order 2 with a single closing sentence on n-ary. Chapter 9 picks it up: input domain $X$ partitioned into $K$ blocks $\{B_1, \ldots, B_K\}$ (model-order $K$); output domain $Y$ with $L$ values; channel matrix $Q$ is $K \times L$ row-stochastic. The Kronecker tensor product generalizes; the parameter count goes from $n(2^m - 1)$ to $K \cdot L$ at model-order $K$.

### 3.4 Source Material per Chapter

Most of Part III draws on `papers/bernoulli_maps/`, `papers/bernoulli_relations/`, and `papers/bernoulli_data_type/`. Chapter 10 (sketches) is mostly fresh writing with the standard literature references (HyperLogLog: Flajolet et al 2007; CountMin: Cormode-Muthukrishnan 2005; MinHash: Broder 1997). Chapter 11 draws on `bernoulli_data_type` plus the standard randomized-algorithm texts (Motwani-Raghavan, Mitzenmacher-Upfal).

### 3.5 Notebook Discipline

Per master spec table:
- Ch 9: substantive notebook (n-ary channel construction, capacity computation).
- Ch 10: substantive notebook (CountMin, HyperLogLog, MinHash all from scratch in Python).
- Ch 11: substantive notebook (Miller-Rabin formal version vs the chapter 3 §3.4 informal one; Las Vegas vs Monte Carlo timing comparison).
- Ch 12: substantive notebook (approximate joins).
- Ch 13: no notebook (theory chapter).

## 4. Chapter Outlines

Compact tables (mirror Part II spec §4 format).

### Chapter 9: Approximate Functions and n-ary Channels (~26 pp, has notebook)

**Learning outcomes:** define $\Bernoulli{T}$ for finite-enum $T$; write the $K \times L$ channel matrix at model-order $K$; state the n-ary Kronecker factorization theorem; relate it to chapter 4 §4.4 and chapter 2 §2.4.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 9.1 | From Approximate Sets to Approximate Functions | ~4 | fresh | Recall §5.1 predicate framing; lift to $T$-valued functions. The codomain is no longer $\{\top, \bot\}$. |
| 9.2 | N-ary Channels | ~6 | reformulate `papers/bernoulli_maps/` | Model-order $K$ input domain. $K \times L$ channel matrix $Q$ row-stochastic. Examples: 3-ary, 10-ary, infinite-state (set as natural numbers). |
| 9.3 | The n-ary Kronecker Theorem | ~6 | fresh, paper has fragments | Generalize chapter 4 §4.4 to model-order $K$. Parameter count $K \cdot L$ per channel; joint over $m$ queries factors as Kronecker tensor product. |
| 9.4 | Capacity for n-ary Channels | ~5 | reformulate Cover-Thomas + paper fragments | Generalize §8.2's $C = 1 - H(\fprate)$ to n-ary: $C = \max_{P_X} I(X;Y)$ over input distributions. |
| 9.5 | Bridge to Sketches | ~2 | fresh | Forward to chapter 10: sketches are approximate functions from a stream/multiset to a low-dimensional summary. |
| 9.6 | Bibliographic Notes | ~2 | fresh | `bernoulli_maps`, Shannon channels at order $K$. |
| Exercises | ~2 | fresh | 11 with star markers. |

### Chapter 10: Sketches and Estimators (~28 pp, has notebook)

**Learning outcomes:** construct CountMin, HyperLogLog, MinHash from scratch; state the FPR/FNR analog (estimation error bounds with confidence levels); compose sketches via the chapter 9 algebra.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 10.1 | Sketches as $\Bernoulli{T}$ | ~3 | fresh | A sketch is an approximate value: a count, a cardinality, a similarity. The chapter 9 type-lifting gives each sketch a $\Bernoulli{T}$ type. |
| 10.2 | CountMin | ~6 | fresh + Cormode-Muthukrishnan ref | Multi-row counter; hash-based collisions; FP bound $\epsilon$ with probability $1 - \delta$. |
| 10.3 | HyperLogLog | ~7 | fresh + Flajolet et al ref | Cardinality estimator; leading-zero trick; merge operation. |
| 10.4 | MinHash and LSH | ~6 | fresh + Broder ref | Jaccard similarity estimator; LSH for approximate nearest neighbor. |
| 10.5 | Bridge | ~2 | fresh | Forward to chapter 13: sketches compose via type-driven algebra. |
| 10.6 | Bibliographic Notes | ~2 | fresh | CountMin, HyperLogLog, MinHash original papers; Cormode-Yi survey. |
| Exercises | ~2 | fresh | 11 with star markers. |

### Chapter 11: Randomized Algorithms (~24 pp, has notebook)

**Learning outcomes:** restate Miller-Rabin formally as a $\Bernoulli{\BoolType}$; distinguish Las Vegas (random runtime, exact output) from Monte Carlo (fixed runtime, random output); state RP and BPP via the chapter 7 PPV framework.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 11.1 | Recall Miller-Rabin | ~3 | reformulate §3.4 | The §3.4 informal walkthrough recast formally. |
| 11.2 | Las Vegas vs Monte Carlo | ~5 | fresh, classical | Random runtime vs random output; trade-offs; examples (Karger min-cut, randomized quicksort). |
| 11.3 | RP, BPP, and Bernoulli Type | ~6 | fresh | Randomized polynomial-time classes via the framework. |
| 11.4 | Sample Complexity | ~5 | fresh + Mitzenmacher-Upfal | How many samples to reach target error rate (Chernoff bound, union bound). |
| 11.5 | Bridge | ~1 | fresh | Forward to chapter 12 (relations) and chapter 13 (full algebra). |
| 11.6 | Bibliographic Notes | ~2 | fresh | Miller, Rabin, Motwani-Raghavan, Mitzenmacher-Upfal. |
| Exercises | ~2 | fresh | 11 with star markers. |

### Chapter 12: Approximate Relations (~22 pp, has notebook)

**Learning outcomes:** define an approximate relation $\tilde R \subseteq T \times U$ as a $\Bernoulli{\BoolType}$ on $T \times U$; compose relations via natural join under noise; recognize approximate-join algorithms in databases as instances.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 12.1 | From Approximate Sets to Approximate Relations | ~3 | reformulate `bernoulli_relations/` | A relation is a subset of $T \times U$; lifting to noisy form gives the relation analog of an approximate set. |
| 12.2 | Composition of Approximate Relations | ~6 | reformulate `bernoulli_relations/` | Natural join, projection, selection under noise. |
| 12.3 | Approximate Joins in Databases | ~6 | fresh | The standard approximate-join algorithms (e.g., based on MinHash from §10.4) as instances. |
| 12.4 | Bridge | ~1 | fresh | Forward to chapter 13. |
| 12.5 | Bibliographic Notes | ~2 | fresh | `bernoulli_relations`, approximate-database literature. |
| Exercises | ~2 | fresh | 11 with star markers. |

### Chapter 13: The Algebra of Approximate Types (~20 pp, no notebook)

**Learning outcomes:** state the type-driven algebra: $\Bernoulli{T \times U} \cong \Bernoulli{T} \otimes \Bernoulli{U}$ for products, $\Bernoulli{T + U}$ for sums, $\Bernoulli{L T}$ for lists, $\Bernoulli{T \to U}$ for functions; recognize the chapter 6 set composition, chapter 9 n-ary maps, chapter 10 sketches, and chapter 12 relations as instances of one algebra.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 13.1 | Algebraic Types Recap | ~3 | reformulate `bernoulli_data_type/` | $T \times U$ products, $T + U$ sums, lists, functions. Standard ADT framing. |
| 13.2 | $\Bernoulli{T}$ for Composite $T$ | ~6 | reformulate `bernoulli_data_type/` | Lift $\Bernoulli{}$ through each type constructor. |
| 13.3 | The Composition Functor | ~5 | fresh | $\Bernoulli{}$ is a functor on the algebraic-types category. Composition by structure. |
| 13.4 | Closing Part III | ~2 | fresh | Recap the journey: atom (Part I), sets (Part II), maps and types (Part III). Forward to Parts IV-V. |
| 13.5 | Bibliographic Notes | ~2 | fresh | `bernoulli_data_type`, category-theoretic ADT references. |
| Exercises | ~2 | fresh | 11 with star markers. |

## 5. Forward and Backward Reference Map

| From | To | Form |
|---|---|---|
| §9.1 | ch 5 §5.1 (predicate framing) | backward |
| §9.2 | ch 2 §2.4 (model order), ch 4 §4.4 (Kronecker) | backward |
| §9.3 | ch 4 §4.4 (Kronecker theorem) | backward, **generalizes** |
| §9.4 | ch 8 §8.2 (BSC capacity) | backward, **generalizes** |
| §10.1 | ch 9 (lifting) | backward |
| §10.4 | ch 12 §12.3 (approximate joins) | forward |
| §11.1 | ch 3 §3.4 (Miller-Rabin informal) | backward, **formalizes** |
| §11.4 | ch 7 §7.2 (binomial estimator) | backward |
| §12.1 | ch 5 §5.1, ch 9 (lifting to relations) | backward |
| §12.3 | ch 10 §10.4 (MinHash) | backward |
| §13.2 | all of Part II and §9-12 (instances) | backward, **unifies** |

## 6. Page Budget

| Chapter | Target | Notes |
|---|---|---|
| Ch 9  | ~26 pp | Generalization of chapter 4 + chapter 2 §2.4 |
| Ch 10 | ~28 pp | Three sketches from scratch |
| Ch 11 | ~24 pp | Miller-Rabin formal + LV/MC + RP/BPP |
| Ch 12 | ~22 pp | Relations + joins |
| Ch 13 | ~20 pp | Algebra + closing of Part III |
| **Total** | **~120** | Expect ~145pp actual (~20% over per Plans 1-8 pattern) |

Part I (134pp) + Part II (112pp) + Part III target (~120pp) = ~366pp Milestone 1 target. Over the ~330pp master target by ~10%; acceptable.

## 7. Sequencing for Plans 9-13

Standard dependency order:

1. **Chapter 9 first (Plan 9):** the type-lifting foundation; chapters 10, 11, 12, 13 depend on it.
2. **Chapter 10 (Plan 10):** sketches as instances of the chapter 9 framework.
3. **Chapter 11 (Plan 11):** randomized algorithms; uses §10.4 sample complexity but otherwise independent.
4. **Chapter 12 (Plan 12):** relations; uses §10.4 MinHash for §12.3 examples.
5. **Chapter 13 (Plan 13):** the unification chapter; written last with full knowledge of chapters 9-12.

Plan 13 Task 10 runs the Part III integration check (mirrors Plan 4 Task 10 and Plan 8 Task 10).

## 8. Open Action Items

1. **alex.sty macros for n-ary notation.** $K$ for model-order, $\otimes$ for Kronecker (already used in chapter 4), $\mathrm{Bernoulli}[T]$ for general types (already `\Bernoulli{T}` in preamble). Verify in Plan 9 Task 0.

2. **Notation conflicts.** $K$ for model-order might clash with $k$ for Bloom hash count (chapter 5) and $k$ for Miller-Rabin rounds (chapter 3). Use $K$ (uppercase) for model-order; $k$ (lowercase) for hash counts. Document the convention in §9.2.

3. **Forward references to chapter 14-18.** Most chapter-level labels exist via Plan 0 stubs. Section-level forward refs from Part III into Parts IV-V should use prose only (do not create section labels in unwritten chapters).

## 9. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Chapter 9 is heavy with notation (K, L, K x L matrices, n-ary tensor). | Spec §9.1 explicitly motivates with concrete examples (3-state, 10-state) before formalism. Use the "Part I atom is the K=2 case" framing throughout. |
| Chapter 10's three sketches are independent treatments; risk of feeling like a catalog. | Use the chapter 9 framework as the unifying lens (each sketch's structure is its $\Bernoulli{T}$ type). |
| Chapter 11's RP/BPP classes are not classical Bernoulli framework. | Soft-cap rigor at the level of stating the classes; the chapter 7 PPV framework gives the proper bridging vocabulary. |
| Chapter 13's category-theoretic framing risks alienating readers who haven't seen functors. | Use "structure-preserving map" language; defer the formal functor name to the bib notes. |
| Page budget overshoot per Plans 1-8 pattern (~20-30%). | Per-chapter hard cap at +30%; review per task. |

## 10. Out of Scope

Part III does not become:
- A general primer on randomized algorithms (Motwani-Raghavan remains the depth reference).
- A complete survey of probabilistic data structures (HyperLogLog++ variants, Cuckoo filters, etc.).
- A category-theory text (chapter 13 uses functor language; full categorical treatment is out of scope).

## 11. Success Criteria for Part III

Part III is successful if:

1. A reader who has finished Parts I and II can finish Part III in three focused weeks and emerge able to (a) describe an n-ary channel and its capacity, (b) construct CountMin/HyperLogLog/MinHash from scratch, (c) state Miller-Rabin's correctness formally via the Bernoulli framework, (d) write the type-driven algebra for $\Bernoulli{T}$ over composite types.

2. The reader sees that Part II's set composition, chapter 10's sketches, chapter 12's relations are all instances of one algebra (chapter 13's unification).

3. The chapter 11 Miller-Rabin formal treatment retires the chapter 3 §3.4 deferral cleanly (mirroring how chapter 7 retired chapter 1 §1.4).

4. By the end of chapter 13, the reader has the full type-theoretic vocabulary for the framework, and Parts IV-V's constructive (BHF, BPHF) and boundary (chapter 16) material lands without further setup.
