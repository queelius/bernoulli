# Design: Part I (The Atom) of the Bernoulli Textbook

**Author:** Alexander Towell
**Date:** 2026-05-02
**Status:** Design (pre-implementation)
**Parent spec:** `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`
**Scope:** Section-level outline for chapters 1-4 (Part I, ~105 pp). Authoritative for Plan 1 (the implementation plan that drafts these chapters).

## 1. Purpose

Part I introduces the framework's atom, `Bernoulli[bool]`, and lands two payoffs: the unification thesis (chapter 3, Miller-Rabin worked from first principles) and the formal axiomatic foundation (chapter 4, Kronecker factorization). By the end of Part I, the reader has seen the same noisy bit treated at four progressively tighter levels of formality and has an explicit definition that retroactively justifies everything in chapters 1-3.

Inherits from the parent spec: B+D audience (adjacent-field grad students through smart-undergrad self-study readers), pedagogical monograph in MacKay tradition, single voice, intuition-first, citations to underlying papers via chapter-end Bibliographic Notes.

## 2. Structural Decisions

Two structural choices, settled before this spec:

**(γ) Atom-outward formalism trajectory.** No formal definition appears in chapter 1. Channel matrices enter in chapter 2 as partial formalism. Operator algebra enters in chapter 3. Full axiomatization arrives in chapter 4. The formal `Bernoulli[bool]` definition lands in §4.5 as the synthesis. The reader sees the framework discovered, not asserted.

**(E) Multi-framed openings, Miller-Rabin climax.** Chapter 1 introduces three framings (biased coin, BSC, classifier verdict). Chapter 2 stays channel-flavored (BSC and asymmetric variants). Chapter 3 climaxes with a 7-page Miller-Rabin walkthrough that delivers the unification thesis. Chapter 4 axiomatizes.

## 3. Cross-Cutting Commitments

Four commitments apply across all four chapters:

### 3.1 Three Running Threads

The biased coin, BSC, and classifier verdict are introduced in §1.1 and return at named points so each thread feels carried, not abandoned:

| Thread | Introduced | Returns | Closes |
|---|---|---|---|
| BSC | §1.1 | §2.1 (formal), §3.3 (worked composition) | §4.4 (Kronecker example with m BSCs) |
| Biased coin | §1.1 | §2.2 (asymmetric callback), §3.1 (AND-gate example) | §4.5 (formal-definition worked example) |
| Classifier verdict | §1.1 | §1.2 (vocabulary cross-walk) | §4.2 (Axiom 1 violation: correlated classifiers) |

### 3.2 Notation Strategy (Three-Tier)

- **Light sidebar in §1.2** introducing ε, ω, τ, η (the alex.sty macros) without ceremony.
- **Distributed notation notes** when new symbols enter: Q in §2.1 (channel matrix), ⊗ in §4.4 (Kronecker product), the formal `Bernoulli[bool]` type in §4.5.
- **Consolidated cheat sheet** in Appendix B (per master spec, the Five Core Principles cheat sheet expands to also list notation).

### 3.3 Learning Outcomes Box Per Chapter

A 3-bullet box at the start of each chapter, ~5 lines, in B+D-style "after this chapter you can..." form. Anchors expectations for self-study readers; instructors find it useful for course adoption.

### 3.4 Exercise Depth

10-12 exercises per chapter with difficulty markers ★ / ★★ / ★★★. Approximate distribution per chapter: 3 warm-ups (★), 5 medium (★★), 3 challenging or extension (★★★). Mix of conceptual, computational (often notebook-tied), and proof exercises. Selected solutions land in Appendix D (per master spec).

## 4. Chapter 1: The Noisy Bit (~25 pp, has notebook)

**Learning outcomes box** (~0.5 pp): name a noisy bit when you see one; quantify it with FPR/FNR; sample to estimate; recognize the noisy bit as the atomic Bernoulli object.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 1.1 | Three Faces of a Noisy Bit | ~5 | fresh | Open with biased coin, BSC, classifier verdict. End with an explicit "the abstract noisy bit" paragraph naming the unifying object. The chapter's atom-naming moment. |
| 1.2 | Quantifying the Noise | ~5 | reformulate `algebra_of_sets.tex` Table 1 | Informal FPR/FNR via TP/FP/TN/FN contingency table. Notation sidebar (ε, ω, τ, η). Cross-walk to precision/recall (classifier-verdict thread). |
| 1.3 | A First Look at the Boolean Universe | ~4 | qualitative reformulation of `bernoulli_model.tex` Example 3.5 | 2x2 outcome matrix walked narratively. No PMF, no joint distribution. Full formalization deferred to §4.5. |
| 1.4 | Sampling and Estimating Rates | ~3 | fresh | Single page on binomial counts, single page on CLT existence (no derivation), one page hooking the notebook. Defers everything substantive to Part II ch 7. |
| 1.5 | Why "Atom"? | ~5 | fresh | Trajectory preview: chapters 2-4 unfold the algebra of how atoms compose. Brief Miller-Rabin tease (one paragraph). |
| 1.6 | Bibliographic Notes | ~1-2 | fresh | Shannon, contingency tables in medical statistics, Miller (1976), our papers. |

### Chapter 1 Notebook (`ch01-noisy-bit.ipynb`)

- Simulate BSC and biased coin in Python (numpy).
- Plot empirical FPR/FNR convergence vs. sample size n.
- Confidence interval coverage check (does the empirical CI contain the true rate at the claimed coverage?).
- Open question for reader: what if rates vary across samples? (Forward reference to ch 16 negative-space chapter.)

### Chapter 1 Exercises (10-12, with difficulty markers)

- **★ x 3**: confusion-matrix to rate conversion; identify three real-world systems as `Bernoulli[bool]`; compute FPR/FNR for a given joint table.
- **★★ x 5**: empirical estimation under varying n (notebook-tied); a coin with bias p mapped to `Bernoulli[bool]` (find ε, ω); show NOT-bit has rates (ω, ε); a classifier's ROC curve as a `Bernoulli[bool]` family parameterized by threshold; sample-size formula for a confidence interval at given precision.
- **★★★ x 3**: argue informally that a stationary noisy bit has rates that converge under iid sampling; construct a system that looks like a noisy bit but isn't (sets up ch 16); construct a stress test for the notebook's empirical estimator.

## 5. Chapter 2: Binary Channels and Model Order (~24 pp, has notebook, restructured to 5 sections)

**Learning outcomes box** (~0.5 pp): define a binary channel formally; write its 2x2 transition matrix; distinguish symmetric from asymmetric and connect this to model order; state the Boolean ceiling at order 2.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 2.1 | The Binary Symmetric Channel | ~6 | reformulate paper BSC fragments + fresh matrix framing | (Merged from former §2.1 + §2.2.) BSC formal definition AND channel matrix Q introduced together. Notation note: Q. |
| 2.2 | The Asymmetric Binary Channel | ~5 | reformulate `order_and_channels.tex` | Z-channel and general asymmetric. Biased-coin callback: a coin with different heads-bias and tails-bias is an asymmetric binary channel. Bloom filter and medical-test instances. |
| 2.3 | Composition of Channels | ~5 | fresh, paper has fragments | (NEW SECTION.) Channel composition as matrix product Q_total = Q_2 Q_1. Worked example: composing two BSCs gives a third BSC; explicit formula. Sets up §3.3 directly. Stays bool-disciplined; n-ary channel composition deferred to Part III. |
| 2.4 | Model Order | ~7 | reformulate `order_and_channels.tex` | Number of partition blocks of the input domain. Boolean ceiling: max model order is 2 because the input domain has 2 elements. Single closing sentence on n-ary as the trailhead for Part III, no Part III content. |
| 2.5 | Bibliographic Notes | ~1-2 | fresh | Shannon (1948), Cover and Thomas channels chapter, model-order-vs-DOF clarification flagged in `papers/CLAUDE.md`. |

### Chapter 2 Notebook (`ch02-binary-channels.ipynb`)

- Build channel transition matrices in numpy.
- Compose two BSCs and verify the formula derived in §2.3.
- Plot BSC capacity 1 - H(ε) vs. crossover ε.
- Explore the (ε, ω) parameter space for asymmetric channels.
- Visualize partition blocks for inputs of size 2, 3, 4 (latter foreshadows ch 9 without entering Part III).

### Chapter 2 Exercises (10-12)

- **★ x 3**: write Q for given ε, ω; compose two BSCs by hand; identify the model order of a given example.
- **★★ x 5**: derive BSC capacity 1 - H(ε); show Bloom filter as ω = 0 channel; prove that two-BSC composition is a BSC; characterize when an asymmetric channel reduces to a BSC; construct a model-order-2 channel from two model-order-1 channels.
- **★★★ x 3**: prove the Boolean ceiling rigorously; show channel composition is associative but not commutative (with counterexample); explore a 3-input partition (foreshadows ch 9 without Part III content).

## 6. Chapter 3: Boolean Algebra Under Noise (~28 pp, has notebook)

**Learning outcomes box** (~0.5 pp): derive AND, OR, NOT under noise; state and apply the composition theorem η_total = 1 - prod(1 - η_i); analyze Miller-Rabin's k-round error from first principles; locate the hidden independence assumption that ch 4 will make explicit.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 3.1 | AND Under Noise | ~5 | reformulate `logic_gates.tex` | Two noisy bits ANDed; closed-form output rates. Biased-coin example (AND of two coin-flips). Explicitly flag that the derivation invokes Axiom 2; proof in §4.4. |
| 3.2 | OR and NOT | ~4 | fresh | NOT trivially swaps ε and ω. OR via De Morgan AND a direct derivation, so the reader sees both paths. |
| 3.3 | The Composition Theorem | ~6 | reformulate `bernoulli_sets` Theorem 3.7 + fresh η_total form | η_total = 1 - prod(1 - η_i) for sequential identity-with-error composition. BSC running-thread example: composing m BSCs and watching the rate evolve. Channel-matrix product view connects to §2.3. |
| 3.4 | Miller-Rabin: A Worked Walkthrough | ~7 | fresh; papers have one-line reference only | **PART I CLIMAX 1.** Step 1: state the witness predicate (is_prime). Step 2: characterize the witness as `Bernoulli[bool]` with FNR = 0, FPR ≤ 1/4. Step 3: apply §3.3 composition for k rounds, FPR_k ≤ (1/4)^k. Step 4: pseudocode plus numerical worked example for n = 341 (or comparable Carmichael-adjacent case). Step 5: pedagogical reframe: primality testing is not a separate technique; it is this framework applied. |
| 3.5 | Composition is the Bridge to Sets | ~4 | fresh | Forward references made specific: a Bloom filter's m hashes are k-fold composition (ch 5); set-operation error rates fall out of this Boolean algebra (ch 6); approximate function composition is composition lifted to maps (ch 9). Three named bridges, one per Part II chapter and one to Part III. |
| 3.6 | Bibliographic Notes | ~1-2 | fresh | Miller (1976), Rabin (1980), CLRS, Mitzenmacher and Upfal, our papers. |

### Chapter 3 Notebook (`ch03-boolean-algebra-noise.ipynb`)

- Bit-level AND, OR, NOT under simulated noise.
- Verify §3.3 composition theorem on a 5-stage chain.
- Implement Miller-Rabin in roughly 25 lines.
- Empirical FPR_k vs. theoretical (1/4)^k.
- Open question: what if witnesses aren't independent? (Forward reference to ch 16.)

### Chapter 3 Exercises (10-12)

- **★ x 3**: derive OR rates from AND via De Morgan; compute FPR after 3-stage AND chain; compute Miller-Rabin's k for FPR ≤ 10^-6.
- **★★ x 5**: verify §3.3 on a specific 4-stage example by hand; show NOT is its own inverse on `Bernoulli[bool]`; implement Miller-Rabin in 20 lines and check empirical FPR; prove the composition theorem assuming Axiom 1; construct a 3-bit ANDed-confidence example.
- **★★★ x 3**: explain why §3.1's AND derivation tacitly assumes Axiom 2; show AND, OR, NOT under noise satisfies De Morgan's laws (with the right error-rate conventions); construct a system where the composition theorem fails (preview of ch 16).

## 7. Chapter 4: Two Axioms and Kronecker Factorization (~28 pp, no notebook)

**Learning outcomes box** (~0.5 pp): state Axioms 1 and 2 formally; prove the Kronecker factorization theorem; derive the parameter count drop from n(2^m - 1) to 2m; write the formal definition of `Bernoulli[bool]` and recognize all of ch 1-3's examples as instances.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 4.1 | Why Axioms? | ~3 | fresh | Recap implicit independence invocations from chapters 1-3. Single sentence: "we have been assuming Axiom 2 since §3.1; let's make it explicit." |
| 4.2 | Axiom 1: Element-Wise Independence | ~5 | reformulate `bernoulli_sets` Axiom 1 | Formal statement; consequence: joint distribution over n queries factors. Without it, ch 3's Miller-Rabin bound breaks. Classifier-verdict callback: violation example via two correlated classifiers. |
| 4.3 | Axiom 2: Conditional Independence of Block Error Rates | ~5 | reformulate `bernoulli_sets` Axiom 2 | Formal statement; consequence: per-input-block error rates stable across queries; one channel matrix per block-pair. |
| 4.4 | The Kronecker Factorization Theorem | ~7 | fresh: papers have idea + remark, NOT theorem with proof | **PART I CLIMAX 2.** Theorem statement. Full proof. Corollary: parameter count drops from n(2^m - 1) to 2m. Worked 2-query example verified against the theorem. BSC running-thread example: m independent BSCs compose to a tensor channel whose matrix is Q^⊗m. Notation note: ⊗. |
| 4.5 | The `Bernoulli[bool]` Type, Formally | ~5 | fresh | Formal definition: `Bernoulli[bool]` = (X, Y, Q) under Axioms 1-2. Biased-coin worked example with full PMF (the §1.3 deferral lands here). Tie back: ch 1's noisy bit is a `Bernoulli[bool]`; ch 2's BSC is one with Q symmetric; ch 3's AND, OR, NOT are operations on `Bernoulli[bool]`. |
| 4.6 | What Comes Next | ~2 | fresh | Brief Part II preview. Five Core Principles status: Two Axioms ✓, Composition Closure ✓, Boolean Thread ✓; Space-Accuracy Duality and Parametric Parsimony arrive in Part II. |
| 4.7 | Bibliographic Notes | ~1-2 | fresh | Kronecker (1860s); Cover and Thomas; our papers. Note the formal Kronecker theorem statement is a fresh contribution. |

### Chapter 4 Notebook

None. Per master spec, ch 4 is intentionally theory-only. The chapter's value is conceptual; runnable code does not add pedagogical value here.

### Chapter 4 Exercises (10-12)

- **★ x 3**: state Axiom 1 in measure-theoretic notation; restate Axiom 2 as a property of Q; write the Kronecker product of two 2x2 matrices.
- **★★ x 5**: prove the parameter count corollary n(2^m - 1) → 2m; verify the Kronecker theorem on the 2-query example by hand; show a Markov channel violates Axiom 1; identify the implicit Axiom-2 assumption in §3.1's AND derivation; construct a `Bernoulli[bool]` from the biased coin and verify both axioms.
- **★★★ x 3**: prove Axiom 1 implies Axiom 2 does NOT hold automatically (counterexample); show that without Axiom 2, the channel-matrix view collapses; argue that the Kronecker theorem cannot be strengthened (the 2m bound is tight).

## 8. Forward and Backward Reference Map

Reference discipline across Part I:

| Section | Reference | Target |
|---|---|---|
| §1.5 | forward, brief teaser | "one Miller-Rabin witness is exactly such a noisy bit" pointing at §3.4 |
| §2.4 | forward, single sentence | n-ary channels in Part III ch 9 |
| §3.1 | forward, explicit flag | "Axiom 2 justifies this; proof in §4.4" |
| §3.5 | forward, three named bridges | Bloom filter as composition (ch 5); set-op error propagation (ch 6); maps as composition lifted (ch 9) |
| §4.1 | backward | implicit independence invocations in chapters 1-3 |
| §4.2 | backward | Miller-Rabin's k-round bound (§3.4) breaks without Axiom 1 |
| §4.4 | backward | §3.1 AND derivation; §3.3 composition theorem |
| §4.5 | backward | ch 1's noisy bit; ch 2's BSC; ch 3's AND, OR, NOT |
| §4.6 | forward | Part II opening |

Notebook open questions in §1, §3 forward to ch 16 (the negative-space chapter).

## 9. Page Budget

| Chapter | Pages | Fresh writing share |
|---|---|---|
| Ch 1 | ~25 | ~60% (per explorer survey) |
| Ch 2 | ~24 | ~30% |
| Ch 3 | ~28 | ~50% (with §3.4 entirely fresh) |
| Ch 4 | ~28 | ~60% (with §4.4 theorem + proof entirely fresh) |
| **Total** | **~105** | **~50%** |

Slightly under the master spec's ~110 pp Part I target. The trim came from compressing §1.4 (sampling) which was over-budget for a chapter-1 hook, and from removing the standalone §2.5 n-ary preview (Part III leakage). Part I + Part II + Part III total still aligns with the master spec's 330 pp Milestone 1.

## 10. Sources Inventory

What can be reformulated from the existing papers vs. needs fresh writing:

**Reformulatable (~50% of Part I):**
- `bernoulli_sets/sections/algebra_of_sets.tex` Table 1: TP/FP/TN/FN contingency table (§1.2)
- `bernoulli_sets/sections/bernoulli_model.tex` Example 3.5: Boolean universe with PMF (§4.5; qualitative version in §1.3)
- `bernoulli_sets/sections/bernoulli_model.tex` Axioms 1-2: formal statements (§4.2, §4.3)
- `bernoulli_sets/sections/bernoulli_model.tex` Theorem 3.7 (composition_rates): channel matrix product form of composition (§3.3)
- `bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex`: model order, BSC, asymmetric channel formalism (§2.1, §2.2, §2.4)
- `bernoulli_data_type/bernoulli_model/sections/logic_gates.tex`: AND truth table with error propagation (§3.1)
- `bernoulli_composition/sections/set_theory.tex`: complement = swap FPR/FNR (referenced in §3.2)

**Fresh writing (~50%):**
- Three-framings opening (§1.1)
- Notation sidebar (§1.2) plus distributed notation notes
- Sampling and estimation introduction (§1.4)
- "Why Atom?" trajectory preview (§1.5)
- Channel matrix notation framing (§2.1)
- Composition of channels with worked BSC example (§2.3)
- η_total = 1 - prod(1 - η_i) form of the composition theorem (§3.3)
- OR and NOT explicit gates (§3.2)
- Miller-Rabin pedagogical walkthrough (§3.4)
- Composition-to-sets bridges (§3.5)
- Why-axioms motivation (§4.1)
- Kronecker factorization theorem statement and proof (§4.4)
- Formal `Bernoulli[bool]` definition tying back to chapters 1-3 (§4.5)
- "What Comes Next" Part II preview (§4.6)
- All learning outcomes boxes
- All exercises (~45 total across 4 chapters)

## 11. Open Action Items

Items deferred for resolution during or after Plan 1 implementation:

1. **Notation harmonization across paper sources.** The papers use slightly different conventions in different places (β asymmetry, "approximate set" vs. "Bernoulli set"). Plan 1 will resolve via the alex.sty macros uniformly; if friction emerges during drafting, surface for spec revision.
2. **Numerical worked example for §3.4.** "n = 341 or comparable Carmichael-adjacent case" needs to be pinned to a specific number. The choice should illustrate where Miller-Rabin's bound tightens (or doesn't) interestingly. Pin during §3.4 drafting.
3. **Citation of `bernoulli_sets` Theorem 3.7.** When the theorem is reformulated in §3.3, the citation form (inline citation? Bibliographic Notes only?) should follow the master spec's policy. Resolve via the §3.6 Bibliographic Notes draft.
4. **Whether §4.4's Kronecker proof goes in the main text or an appendix.** Currently scoped at 7 pp main text. If the proof balloons during drafting, consider sketch-in-text plus full-proof-in-appendix split. Surface for spec revision.

## 12. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| §3.4 Miller-Rabin walkthrough overshoots 7 pp because the pedagogical version is detailed. | Hard cap at 7 pp main text. If overflow, push the numerical worked example to the notebook and keep the prose tight. |
| §4.4 Kronecker theorem proof is harder to write cleanly than expected (the papers have it as a remark, not a theorem). | Write the proof first during Plan 1 implementation; if it doesn't fit in 7 pp, use the Open Action Item 4 split. |
| Three running threads add cognitive overhead and require discipline to maintain. | Cross-reference map in §8 of this spec is the source of truth. Plan 1's per-chapter checklists must include "thread carries from prior chapter" as a verification step. |
| Exercise count of 10-12 per chapter inflates page estimates. | Exercises live in the chapter end and count toward chapter pages. Budget assumes ~1-2 pp of exercises per chapter. If exercise prose exceeds, compress narrative sections or move some to Appendix D. |
| The §1.3 deferral to §4.5 (Boolean universe full PMF) creates a long "memory load" for the reader. | §4.5 explicitly recapitulates the §1.3 example before formalizing, so the reader does not need to remember details from 80 pages back. |

## 13. Out of Scope

Part I does not, and should not become:

- A general introduction to information theory (chapter 2 uses the BSC and capacity informally; Cover and Thomas remains the depth reference).
- A general introduction to randomized algorithms (chapter 3 uses Miller-Rabin specifically; Mitzenmacher and Upfal remains the breadth reference).
- A primer on probability theory (chapter 4 axiomatizes the Bernoulli framework; basic probability is a stated prerequisite).
- A treatment of n-ary channels at the formal level (deferred to Part III ch 9 by user instruction in this brainstorm).
- A treatment of approximate sets (deferred to Part II).

If a chapter starts to drift into any of the above, that is a signal to trim or refactor rather than expand.

## 14. Success Criteria for Part I

Part I is successful if:

1. A B+D reader who knows undergraduate probability can finish chapters 1-4 in two focused weeks and emerge able to (a) recognize a `Bernoulli[bool]` in their own work, (b) state the composition theorem and the two axioms, (c) reproduce the Miller-Rabin bound from first principles.
2. The reader's first reaction to the §3.4 Miller-Rabin walkthrough is "I had not thought of primality testing this way" and the second reaction is "of course it is the framework applied."
3. The §4.5 formal definition feels earned by §1-3, not dropped on the reader.
4. At least one specific course adoption signal (instructor uses Part I as standalone reading; section problem sets get assigned).
5. The three running threads (BSC, biased coin, classifier verdict) feel carried, not contrived. A reviewer should be able to point at any thread's return and say "yes, this is doing real pedagogical work."

## 15. Sequencing for Plan 1

Plan 1 will draft the four chapters in dependency order. Recommended sequencing:

1. **Chapter 4 first** (especially §4.2, §4.3, §4.4, §4.5). Locking the formal definitions and theorems first prevents drift during chapters 1-3 drafting. Reformulation work plus the fresh Kronecker theorem.
2. **Chapter 2** (channels and model order). Mostly reformulation; the §2.3 fresh section sets up §3.3.
3. **Chapter 3** (Boolean algebra and Miller-Rabin). The §3.4 climax is the largest fresh block; better to have ch 4 locked before drafting it.
4. **Chapter 1** (noisy bit and intuition). Drafting last, with full knowledge of what the reader is being prepared for. Prevents the chapter-1-drift problem (writers often over-promise in chapter 1 because they don't yet know the rest of the book).

This is the recommended order; Plan 1 will commit to its own sequencing during writing.
