# Bernoulli Textbook Chapter 3: Boolean Algebra Under Noise (Plan 3)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 3 of Part I (~28 pp): Boolean operations under noise (AND, OR, NOT), the composition theorem at the Boolean algebra layer, and the Miller-Rabin worked walkthrough that delivers the unification thesis. Chapter 3 contains one of Part I's two named climaxes (the Miller-Rabin walkthrough at §3.4; chapter 4's §4.4 Kronecker theorem was the other).

**Architecture:** Replace the existing `book/chapters/ch03-boolean-algebra-noise.tex` stub with a fully drafted chapter containing 6 sections, a learning-outcomes opener, 10-12 exercises, supporting bibliographic entries, and a paired Python notebook. Build verification at every section commit ensures the book continues to compile cleanly.

**Tech Stack:** LaTeX (book class), alex.sty notation package, biblatex with biber backend. Python 3.11+ + numpy + matplotlib for the notebook (Miller-Rabin implementation in ~25 lines). The build pipeline established in Plans 0-2 is the test harness.

**Scope:** Chapter 3 only. Cross-chapter integration with chapter 1 is deferred to Plan 4 (which drafts chapter 1 last and runs the Part I integration check). This plan's cross-references forward to chapter 1 sections must use tentative labels; verification happens in Plan 4.

**Spec source of truth:** `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §6 (chapter 3 outline) and §8 (reference map).

**Source material (papers to reformulate):**
- `papers/bernoulli_data_type/bernoulli_model/sections/logic_gates.tex` for AND truth table with full error propagation (§3.1 backbone)
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Theorem 3.7 (composition_rates) for §3.3 (chapter 2 §2.3 reformulated this from the matrix-product perspective; chapter 3 §3.3 takes the Boolean-algebra perspective: $\eta_{\text{total}} = 1 - \prod(1 - \eta_i)$)
- `papers/bernoulli_composition/sections/set_theory.tex` for set-operation error rates (informs §3.5 bridges)
- The Miller-Rabin walkthrough (§3.4) is FRESH writing: papers have only a one-line reference per the explorer's report.

**Lessons inherited from Plans 1 and 2:**

The chapter 4 review cycle surfaced recurring failure modes that this plan must guard against:

1. **Conflation of distinct independence properties.** Chapter 3 invokes BOTH Axiom 1 (element-wise across distinct inputs) AND Axiom 2 (per-block rate stability) in the AND derivation. Each invocation must be precise; do not blur "the independence axioms" generically. The §3.1 AND derivation specifically uses Axiom 2 (per-block rate stability across queries on the SAME block); §3.3's composition theorem assumes both. Be explicit.

2. **Distinguish chain-stage independence from element-wise independence.** Plan 1's §4.2 review caught that "chain composition" examples (k channels in series, one query through the chain) describe chain-stage independence, not strictly element-wise independence in the Axiom 1 sense. §3.3's composition theorem is at the chain-stage level. Frame this honestly.

3. **The Miller-Rabin example needs a careful framing.** Per the §4.2 review feedback (Axiom 1 mis-invocation issue), Miller-Rabin's k random witnesses are *samples* of the predicate "is n composite?" (the input n is fixed across rounds; randomness enters via the witness draw), not *distinct elements* of the predicate's input domain. To apply Axiom 1 cleanly, recast the test as a predicate $\tilde{P}: \{2, ..., n-2\} \to \{\text{composite}, \text{probably prime}\}$ on the witness pool. Make this recasting explicit in §3.4.

4. **Match Q convention to chapters 2 and 4.** Q has rows by input block, columns by output label. Chapter 3 uses Q implicitly when discussing channel composition; verify any matrix appearance matches.

5. **Match composition formula to chapters 2 and 4.** §3.3's $\eta_{\text{total}} = 1 - \prod(1 - \eta_i)$ is the Boolean-algebra rephrasing of chapter 2 §2.3's matrix-product composition. The connection should be explicit.

6. **Forward references to chapter 1 will not resolve.** Document expected unresolved labels in each section's header comment block.

7. **Page count discipline.** Plans 1 and 2 came in 30-40% over their spec page targets. Chapter 3's spec target is ~28pp; expect 32-38pp. Hold the line on the §3.4 Miller-Rabin walkthrough at 7pp (the climax should breathe but not bloat).

---

## File Structure

After this plan completes:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch03-boolean-algebra-noise.tex      # rewritten from stub to ~28 pp chapter scaffold
│   │   └── ch03/                                # NEW directory
│   │       ├── and-under-noise.tex              # §3.1 (~5 pp)
│   │       ├── or-not.tex                       # §3.2 (~4 pp)
│   │       ├── composition-theorem.tex          # §3.3 (~6 pp)
│   │       ├── miller-rabin.tex                 # §3.4 (~7 pp) CLIMAX
│   │       ├── bridge-to-sets.tex               # §3.5 (~4 pp)
│   │       ├── bibliographic-notes.tex          # §3.6 (~1-2 pp)
│   │       └── exercises.tex                    # 10-12 exercises
│   └── references.bib                           # extended with Miller (1976), Rabin (1980), CLRS, Mitzenmacher-Upfal
└── python/
    └── notebooks/
        └── ch03-boolean-algebra-noise.ipynb     # paired notebook
```

The chapter follows the same subdirectory pattern Plans 1 and 2 established. Thin chapter file inputs section subfiles. This isolates per-section commits and keeps each subagent's working scope small.

`python/notebooks/ch03-boolean-algebra-noise.ipynb` is the chapter's notebook. It demonstrates bit-level AND/OR/NOT under simulated noise, verifies §3.3's composition theorem on a 5-stage chain, implements Miller-Rabin in ~25 lines, and shows empirical FPR_k vs theoretical (1/4)^k.

---

## Per-Task Drafting Discipline

Every section drafting task follows the same internal structure (matching Plans 1 and 2):

1. **Read paper source(s)** named in the task header.
2. **Read prior context** from earlier in the chapter and prior chapters (chapter 4 sections inform §3.1's axiom invocations; chapter 2 §2.3 informs §3.3's composition theorem).
3. **Draft the section** to the page-length target, content checklist, and notation requirements specified in the task.
4. **Verify forward and backward references** specified in the task are present.
5. **Build the book** with `cd book && make cleanall && make` and confirm exit code 0.
6. **Self-review** against the section's content checklist.
7. **Commit** with the message format specified in the task.

---

## Tasks

### Task 1: Read source material and write chapter scaffolding

**Files:**
- Modify: `book/chapters/ch03-boolean-algebra-noise.tex` (currently a one-line stub)

**Source reading:**
- `papers/bernoulli_data_type/bernoulli_model/sections/logic_gates.tex` (AND truth table)
- `papers/bernoulli_sets/sections/bernoulli_model.tex` (Theorem 3.7 composition_rates)
- `papers/bernoulli_composition/sections/set_theory.tex` (set-operation error rates, informing §3.5)
- `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §6 and §8

- [ ] **Step 1: Read all sources end-to-end**

Use `Read` on the four file paths above.

- [ ] **Step 2: Replace the stub with chapter scaffolding**

Open `book/chapters/ch03-boolean-algebra-noise.tex` (currently a 4-line stub from Plan 0) and replace its contents with:

```latex
\chapter{Boolean Algebra Under Noise}
\label{ch:boolean-algebra}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Derive AND, OR, and NOT under noise from first principles, using
    the per-block rate parameters of the input $\Bernoulli{\BoolType}$
    instances.
  \item State and apply the composition theorem
    $\eta_{\mathrm{total}} = 1 - \prod_{i=1}^k (1 - \eta_i)$ for chained
    identities-with-error.
  \item Analyze Miller-Rabin's $k$-round error from first principles by
    treating one witness as a $\Bernoulli{\BoolType}$ instance and
    composing.
  \item Locate the hidden independence assumption that
    \Cref{ch:axioms-kronecker} will make explicit.
\end{itemize}
\end{quote}

% Section 3.1
\input{chapters/ch03/and-under-noise}

% Section 3.2
\input{chapters/ch03/or-not}

% Section 3.3
\input{chapters/ch03/composition-theorem}

% Section 3.4
\input{chapters/ch03/miller-rabin}

% Section 3.5
\input{chapters/ch03/bridge-to-sets}

% Section 3.6
\input{chapters/ch03/bibliographic-notes}

% Exercises
\input{chapters/ch03/exercises}
```

- [ ] **Step 3: Create the `book/chapters/ch03/` subdirectory**

```bash
mkdir -p book/chapters/ch03
```

- [ ] **Step 4: Create empty stubs for each section subfile**

```bash
for slug in and-under-noise or-not composition-theorem miller-rabin bridge-to-sets bibliographic-notes exercises; do
  echo "% Drafted in Task: see plan 2026-05-04-bernoulli-textbook-ch03-boolean-algebra.md" > "book/chapters/ch03/${slug}.tex"
done
```

- [ ] **Step 5: Verify the chapter still builds with the new structure**

Run: `cd book && make cleanall && make`
Expected: exit code 0; `book.pdf` exists.

- [ ] **Step 6: Verify no new build errors**

Run: `grep -i 'error' book/book.log | head -5`
Expected: no fatal errors. Existing forward-reference warnings are expected.

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch03-boolean-algebra-noise.tex book/chapters/ch03/
git commit -m "$(cat <<'EOF'
book: scaffold chapter 3 (Boolean algebra under noise) section subfiles

Replace ch03 stub with chapter scaffold: title, learning-outcomes box
with four bullets, seven section input lines (AND under noise, OR/NOT,
composition theorem, Miller-Rabin walkthrough, bridge to sets,
bibliographic notes, exercises). Create empty subfile stubs in
chapters/ch03/ for incremental drafting, matching the chapter 2 and
chapter 4 patterns. Build still green; sections will land in
subsequent commits.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Draft §3.1 AND Under Noise (~5 pp)

**Files:**
- Modify: `book/chapters/ch03/and-under-noise.tex`

**Spec target:** spec §6 row 3.1.

**Sources:**
- `papers/bernoulli_data_type/bernoulli_model/sections/logic_gates.tex` (AND truth table with error propagation; primary source)

**Content checklist:**
- Section header `\section{AND Under Noise}\label{sec:and-under-noise}`.
- Comment block at top noting expected unresolved `\Cref` forward refs.
- Two noisy bits, each a $\Bernoulli{\BoolType}$ instance with rates $(\fprate_1, \fnrate_1)$ and $(\fprate_2, \fnrate_2)$.
- Truth table for AND: 4 cases (true inputs ⊤⊤, ⊤⊥, ⊥⊤, ⊥⊥), with each case giving the probability of observing each output (⊤ or ⊥).
- Closed-form output rates for AND: derived. Specifically, AND of two `Bernoulli[bool]` instances produces a new `Bernoulli[bool]` instance with rates derivable from the input rates.
- **Explicit flag**: this derivation invokes Axiom 2 (per-block rate stability across the two queries) AND Axiom 1 (independence of error events across distinct inputs). Forward-reference §4.2 (`\Cref{sec:axiom-1}`) and §4.3 (`\Cref{sec:axiom-2}`) for the axioms; note "we will prove the proof structure in §4.4".
- Worked example: biased-coin AND example (the running-thread callback per spec §3.1). Two coins, each with bias parameters; compute AND output rates numerically.
- Forward reference to §3.2 (OR/NOT will follow), §3.3 (composition theorem), §3.4 (Miller-Rabin uses AND-like composition).

**Notation:** $\fprate$, $\fnrate$, $\tprate$, $\tnrate$ from alex.sty. $\Bernoulli{\BoolType}$ for the type.

**Cross-references:**
- Backward to §1.1 `\Cref{sec:three-faces}` for biased-coin running-thread (chapter 1 stub; Plan 4).
- Backward to §4.2 `\Cref{sec:axiom-1}` and `\Cref{ax:element-indep}` (resolves; chapter 4 drafted).
- Backward to §4.3 `\Cref{sec:axiom-2}` and `\Cref{ax:block-rates-indep}` (resolves).
- Forward to §3.2 `\Cref{sec:or-not}` (resolves in Task 3).
- Forward to §3.3 `\Cref{sec:composition-theorem}` (resolves in Task 4).
- Forward to §3.4 `\Cref{sec:miller-rabin}` (resolves in Task 5).
- Backward to chapter 2 §2.1 `\Cref{sec:bsc}` for the per-input-block channel framing (resolves).

**Length target:** ~5 pp.

- [ ] **Step 1: Read the spec target**

Read spec §6 row 3.1.

- [ ] **Step 2: Read paper source**

Read `papers/bernoulli_data_type/bernoulli_model/sections/logic_gates.tex`. Note the AND truth table with cases 1-4 and per-output error probabilities.

- [ ] **Step 3: Read prior context**

Read chapter 2 §2.1 (`book/chapters/ch02/bsc.tex`) for Q convention and biased-coin framing. Read chapter 4 §4.2 (`book/chapters/ch04/axiom-1.tex`) for Axiom 1's exact form. Read chapter 4 §4.5 (`book/chapters/ch04/bernoulli-bool-formal.tex`) for the formal `Bernoulli[bool]` definition.

- [ ] **Step 4: Draft the section**

Replace `book/chapters/ch03/and-under-noise.tex` content with `\section{AND Under Noise}\label{sec:and-under-noise}` plus comment block plus ~5 pp meeting checklist.

- [ ] **Step 5: Verify the AND output rate derivation algebraically**

For two independent `Bernoulli[bool]` instances $b_1, b_2$ with rates $(\fprate_i, \fnrate_i)$, the AND output:

- $\Pr(b_1 \wedge b_2 = \top \mid \text{true}_1 \wedge \text{true}_2) = (1-\fnrate_1)(1-\fnrate_2)$ (true positive)
- $\Pr(b_1 \wedge b_2 = \top \mid \neg(\text{true}_1 \wedge \text{true}_2)) = \text{depends on case}$ (false positive)

Specifically, the FP rate of $b_1 \wedge b_2$ is the probability that AT LEAST ONE input is false but both are reported true. This needs careful case work.

If "true" means "the input element is in the objective set" and the AND is interpreted at the input-block level (both elements positive ⇒ output should be ⊤; otherwise ⊥), then:
- For input $(\top, \top)$: output is correctly ⊤ with probability $(1-\fnrate_1)(1-\fnrate_2)$.
- For input $(\top, \bot)$: output is incorrectly ⊤ when first reports correctly and second incorrectly: $(1-\fnrate_1) \cdot \fprate_2$.
- For input $(\bot, \top)$: similar, $\fprate_1 \cdot (1-\fnrate_2)$.
- For input $(\bot, \bot)$: output is incorrectly ⊤ when both report incorrectly: $\fprate_1 \cdot \fprate_2$.

The FP rate of AND depends on the input distribution; see how the source paper formulates this carefully and reformulate.

- [ ] **Step 6: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0.

- [ ] **Step 7: Verify cross-references**

Run: `grep -E '\\\\Cref|\\\\ref' book/chapters/ch03/and-under-noise.tex`
Expected: at least 6 cross-references.

- [ ] **Step 8: Self-review against checklist**

- [ ] **Step 9: Commit**

```bash
git add book/chapters/ch03/and-under-noise.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 3.1 AND Under Noise (~5 pp)

Five-page section deriving the AND of two Bernoulli[bool] instances
from the truth table. Worked biased-coin example (running-thread
callback per Part I spec section 3.1). Explicit flag that the
derivation invokes both Axioms 1 and 2; forward-reference to chapter
4.2 / 4.3 for formal axiom statements.

Closed-form output rates derived case-by-case for the four input
patterns; FP rate depends on input distribution as the source paper
notes.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Draft §3.2 OR and NOT (~4 pp)

**Files:**
- Modify: `book/chapters/ch03/or-not.tex`

**Spec target:** spec §6 row 3.2.

**Sources:** Mostly fresh writing. The papers don't work OR or NOT explicitly; OR follows from De Morgan's laws applied to AND.

**Content checklist:**
- Section header `\section{OR and NOT}\label{sec:or-not}`.
- Comment block at top.
- NOT under noise: NOT swaps $\fprate$ and $\fnrate$. Trivial derivation. Note that NOT is its own inverse: $(\text{NOT})^2 = \text{identity}$ as an operation on `Bernoulli[bool]`.
- OR via De Morgan: $b_1 \vee b_2 = \neg(\neg b_1 \wedge \neg b_2)$. Derive OR rates from AND rates via De Morgan substitution.
- OR via direct derivation (truth table): also derive directly so reader sees both paths agree.
- Boolean algebra closure under noise: AND, OR, NOT generate all of Boolean algebra. The set of `Bernoulli[bool]` instances is closed under these operations (each operation produces a new `Bernoulli[bool]`).
- Forward reference to §3.3 (composition theorem applies these operations chained).

**Notation:** $\neg b$ for NOT, $b_1 \wedge b_2$ for AND, $b_1 \vee b_2$ for OR.

**Cross-references:**
- Backward to §3.1 `\Cref{sec:and-under-noise}`.
- Backward to chapter 4 §4.5 `\Cref{def:bernoulli-bool}` for the formal type.
- Forward to §3.3 `\Cref{sec:composition-theorem}`.

**Length target:** ~4 pp.

- [ ] **Step 1: Read spec §6 row 3.2.**

- [ ] **Step 2: Read prior context**

Read `book/chapters/ch03/and-under-noise.tex` (just drafted) and chapter 4 §4.5.

- [ ] **Step 3: Draft the section**

Replace `book/chapters/ch03/or-not.tex` content with `\section{OR and NOT}\label{sec:or-not}` plus comment block plus ~4 pp meeting checklist.

- [ ] **Step 4: Verify OR via De Morgan and via direct derivation give the same result**

Worked check: with AND rates $(\fprate_{\wedge}, \fnrate_{\wedge})$, NOT swaps to $(\fnrate_{\wedge}, \fprate_{\wedge})$. So $\neg b_1 \wedge \neg b_2$ has rates derived from $b_1, b_2$'s rates with FPR/FNR swapped. Then the outer NOT swaps again. The result should match a direct truth-table derivation of OR.

- [ ] **Step 5: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0.

- [ ] **Step 6: Self-review**

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch03/or-not.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 3.2 OR and NOT (~4 pp)

Four-page section: NOT swaps FPR and FNR (trivial derivation, NOT is
its own inverse). OR derived via De Morgan substitution (NOT(AND of
NOTs)) and verified by direct truth-table derivation. Boolean algebra
closure under noise: AND, OR, NOT operations on Bernoulli[bool]
instances produce new Bernoulli[bool] instances.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Draft §3.3 The Composition Theorem (~6 pp)

**Files:**
- Modify: `book/chapters/ch03/composition-theorem.tex`

**Spec target:** spec §6 row 3.3.

**Sources:**
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Theorem 3.7 (composition_rates), primary source.
- Chapter 2 §2.3 `book/chapters/ch02/channel-composition.tex` is the matrix-product perspective; §3.3 is the Boolean-algebra perspective on the same idea.

**Content checklist:**
- Section header `\section{The Composition Theorem}\label{sec:composition-theorem}`.
- Comment block at top.
- Setup: chained applications of identity-with-error. $k$ copies of an identity channel, each with per-stage TNR $\eta_i$ (or per-stage error rate $1 - \eta_i$). The end-to-end correctness probability is $\prod_i \eta_i$.
- **Composition theorem** in `\begin{theorem}` environment: $\eta_{\text{total}} = 1 - \prod_{i=1}^k (1 - \eta_i)$ for the end-to-end ERROR rate. (The TNR formulation is $\tnrate_{\text{total}} = \prod_i \tnrate_i$; the error formulation is $\eta_{\text{total}} = 1 - \tnrate_{\text{total}}$.)
- Proof: by induction on $k$, or by direct probability argument using independence at each stage.
- BSC running-thread example: composing $m$ BSCs and watching the rate evolve. Connect explicitly to chapter 2 §2.3's matrix-product result (the $\fprate_{\text{total}} = \fprate_1 + \fprate_2 - 2\fprate_1\fprate_2$ formula is the BSC special case).
- Channel-matrix product view: the composition theorem is a Boolean-algebra rephrasing of $Q_{\text{total}} = Q_2 Q_1$ for chained channels. Explicitly note the connection to chapter 4 §4.4 (Kronecker theorem is the parallel analog).
- Honest note about independence: §3.3's composition theorem assumes the per-stage error events are mutually independent. This is chain-stage independence (per the Plan 1 §4.2 review lesson), which differs from element-wise independence (Axiom 1) but is closely related and often co-occurs. In well-behaved implementations both hold.
- Forward reference to §3.4 (Miller-Rabin uses §3.3 with $k$ rounds).

**Notation:** $\eta_i$ for per-stage error rate, $\tnrate_i$ for per-stage TNR. Match chapter 4's convention (Q has TNR on the diagonal for the negative block).

**Cross-references:**
- Backward to §2.3 `\Cref{sec:channel-composition}` (resolves).
- Backward to §3.1, §3.2.
- Backward to §4.4 `\Cref{sec:kronecker}` and `\Cref{thm:kronecker}` (resolves).
- Forward to §3.4 `\Cref{sec:miller-rabin}` (resolves in Task 5).

**Length target:** ~6 pp.

- [ ] **Step 1: Read spec §6 row 3.3.**

- [ ] **Step 2: Read source paper**

Read `papers/bernoulli_sets/sections/bernoulli_model.tex` Theorem 3.7.

- [ ] **Step 3: Read prior context**

Read chapter 2 §2.3 for the matrix-product perspective. Read §3.1 (just drafted) for the AND truth-table machinery. Read chapter 4 §4.4 for the Kronecker contrast.

- [ ] **Step 4: Draft the section**

Replace `book/chapters/ch03/composition-theorem.tex` content with `\section{The Composition Theorem}\label{sec:composition-theorem}` plus comment block plus ~6 pp meeting checklist.

- [ ] **Step 5: Verify the BSC example matches chapter 2 §2.3**

For BSC composition with $m=2$ stages and equal crossover $\fprate$:
- Direct from §3.3 formula: $\eta_{\text{total}} = 1 - \prod (1 - \eta_i)$ with $\eta_i = \fprate$. Wait, this isn't quite right because $\eta$ in the composition theorem is the CHAIN error rate, not the per-stage FPR.
- Actually, $\eta = \fprate$ is the per-stage error rate (probability of incorrect transmission), so $\eta_{\text{total}} = 1 - (1-\fprate)^2 = 2\fprate - \fprate^2$ for $m=2$.
- Chapter 2 §2.3 derived $\fprate_{\text{total}} = \fprate_1 + \fprate_2 - 2\fprate_1\fprate_2$.
- For $\fprate_1 = \fprate_2 = \fprate$: $2\fprate - 2\fprate^2$.
- Discrepancy: §3.3's formula gives $2\fprate - \fprate^2$; §2.3 gives $2\fprate - 2\fprate^2$. **Verify which is correct and reconcile.**

The reconciliation: §3.3's $\eta_{\text{total}} = 1 - \prod(1-\eta_i)$ is the probability of AT LEAST ONE error along the chain. But for BSC, an even number of flips returns to the original, so the actual error rate of the composed BSC is the probability of an ODD number of flips, which gives the §2.3 formula. The §3.3 formula is correct for IDENTITY-WITH-ERROR composition (where any single error in the chain corrupts the result), but BSC composition has the extra structure that two flips cancel. **Make this distinction explicit in §3.3 prose:** the composition theorem is for identity-with-error composition; BSC composition has the additional cancellation structure.

This is an important nuance worth catching here rather than letting the next reviewer flag it.

- [ ] **Step 6: Build and verify**

Run: `cd book && make cleanall && make`

- [ ] **Step 7: Verify the chain-stage vs element-wise independence framing is honest**

The prose should NOT claim §3.3's theorem follows from Axiom 1 alone. It assumes chain-stage independence, which is closely related but operationally distinct. (Plan 1 §4.2 review's lesson.)

- [ ] **Step 8: Self-review**

- [ ] **Step 9: Commit**

```bash
git add book/chapters/ch03/composition-theorem.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 3.3 The Composition Theorem (~6 pp)

Six-page section: composition theorem at the Boolean-algebra layer.
Statement eta_total = 1 - prod(1 - eta_i) for k chained
identities-with-error. Proof by induction on k.

Worked example: BSC chain. The section explicitly notes that BSC
composition has additional cancellation structure (two flips return
to original), so the §3.3 formula and the §2.3 matrix-product formula
agree only for identity-with-error composition; BSC has the modified
formula 2*epsilon - 2*epsilon^2 (vs the §3.3 formula's
2*epsilon - epsilon^2 which would apply to non-cancelling identity-
with-error chains).

Honest note about chain-stage independence vs element-wise (Axiom 1)
independence: closely related, operationally distinct, both required
in well-behaved implementations.

Connects matrix-product (chapter 2.3, serial) and Kronecker (chapter
4.4, parallel) compositions as sister consequences.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Draft §3.4 Miller-Rabin: A Worked Walkthrough (~7 pp), CHAPTER CLIMAX

**Files:**
- Modify: `book/chapters/ch03/miller-rabin.tex`

**Spec target:** spec §6 row 3.4. **THIS IS PART I CLIMAX 1** (the unification thesis pays off here).

**Sources:**
- The Miller-Rabin walkthrough is FRESH writing. The papers have only a one-line reference (per the explorer's report).
- For the algorithm itself: standard references (Cormen et al, Mitzenmacher-Upfal, original Miller 1976 + Rabin 1980 papers).

**Content checklist:**
- Section header `\section{Miller-Rabin: A Worked Walkthrough}\label{sec:miller-rabin}`.
- Comment block at top.
- **Step 1: state the witness predicate.** A Miller-Rabin "is_prime" witness test takes a candidate integer $n$ and a witness $a \in \{2, ..., n-2\}$. Returns "composite" (definitive) or "probably prime" (uncertain).
- **Step 2: characterize as `Bernoulli[bool]` with FNR=0, FPR ≤ 1/4.** The test never falsely declares a prime composite (FNR = 0); it may declare a composite as "probably prime" (FPR ≤ 1/4 per round, by the Miller-Rabin theorem).
- **Predicate recasting (per §4.2 review lesson):** to apply Axiom 1 cleanly, recast as a predicate $\tilde{P}: \{2, ..., n-2\} \to \{\text{composite}, \text{probably prime}\}$ on the witness pool. Now distinct witnesses ARE distinct input elements, and Axiom 1's claim is that error events at distinct witnesses (events "$w_i$ is a strong liar") are independent.
- **Step 3: apply §3.3 composition for k rounds.** k independent witnesses, AND the results: declare "probably prime" only if all k say "probably prime". Per §3.3's composition (or, for the FNR=0 case, the simpler $\fprate_k \leq (1/4)^k$ bound).
- **Step 4: pseudocode + worked numerical example.** Pseudocode in ~15 lines. Worked example with a specific composite $n$ (e.g., $n = 341 = 11 \times 31$, which is a Carmichael-adjacent pseudoprime to base 2; a good pedagogical case where naive Fermat fails). Show k=1, k=5, k=20 round bounds.
- **Step 5: pedagogical reframe.** Primality testing is not a separate technique; it is the Bernoulli framework applied. The Miller-Rabin algorithm IS k-fold composition of `Bernoulli[bool]` witnesses. The (1/4)^k bound IS the composition theorem in the FNR=0 special case.
- Honest note that whether the within-witness-pool independence (Axiom 1 applied to the recast predicate) actually holds depends on the structure of $n$'s strong-liar set; the (1/4)^k bound is over the worst case.

**Notation:** Standard. $a$ for witness, $n$ for candidate, $k$ for round count.

**Cross-references:**
- Backward to §3.1 `\Cref{sec:and-under-noise}` (the AND of k witnesses).
- Backward to §3.3 `\Cref{sec:composition-theorem}` (the composition theorem applied).
- Backward to §4.2 `\Cref{sec:axiom-1}` and `\Cref{ax:element-indep}` for the predicate-recasting move.
- Backward to chapter 4 §4.5 `\Cref{def:bernoulli-bool}` for the formal type.
- Forward to §3.5 `\Cref{sec:bridge-to-sets}` (resolves in Task 6).
- Forward to chapter 11 (randomized algorithms in Part III) for the formal Las Vegas vs Monte Carlo treatment, single sentence.

**Length target:** ~7 pp. **Hold this line.** Plan 1 chapter 4 climax (§4.4) ran over budget; this climax should breathe but stay within 7-8pp.

- [ ] **Step 1: Read spec §6 row 3.4 carefully.**

- [ ] **Step 2: Read prior context**

Read §3.1 (AND), §3.3 (composition theorem). Read chapter 4 §4.2 (Axiom 1 framing), §4.5 (formal type).

- [ ] **Step 3: Verify the Miller-Rabin algorithm details**

Worked example for $n = 341 = 11 \times 31$:
- $n - 1 = 340 = 4 \times 85 = 2^2 \times 85$. So $d = 85$, $r = 2$.
- For witness $a$: compute $a^d \mod n$, then square repeatedly $r-1$ times. If any is $\pm 1$, declare "probably prime"; otherwise "composite".
- For $a = 2$: $2^{85} \mod 341 = ?$. Standard computation gives $2^{85} \mod 341 = 32$. Then $32^2 \mod 341 = 1024 \mod 341 = 1$. Since $32 \neq \pm 1$ but $32^2 = 1$, this is a "non-trivial square root of 1", which is a witness of compositeness. So Miller-Rabin with $a=2$ correctly identifies 341 as composite.
- (Note: the original Fermat test would fail for 341 with $a=2$ because $2^{340} \equiv 1 \pmod{341}$. Miller-Rabin's strength is catching exactly these Fermat liars.)

If the algorithm details are uncertain, consult Cormen et al chapter 31 or Mitzenmacher-Upfal for confirmation.

- [ ] **Step 4: Draft the section**

Replace `book/chapters/ch03/miller-rabin.tex` content with `\section{Miller-Rabin: A Worked Walkthrough}\label{sec:miller-rabin}` plus comment block plus ~7 pp meeting checklist. Structure as 5 numbered steps per the plan.

- [ ] **Step 5: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0.

- [ ] **Step 6: Verify the unification thesis lands**

The closing prose should explicitly say: primality testing is not a separate technique; it is this framework applied. Without this beat, the climax doesn't pay off.

- [ ] **Step 7: Verify the predicate-recasting is explicit**

The prose should make the input-domain recasting clear. (Plan 1 §4.2 review caught the conflation of "distinct elements" with "samples".)

- [ ] **Step 8: Self-review against checklist**

- [ ] **Step 9: Commit**

```bash
git add book/chapters/ch03/miller-rabin.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 3.4 Miller-Rabin worked walkthrough (climax 1)

Seven-page section, the Part I unification-thesis climax: a full
walkthrough of the Miller-Rabin primality test as a Bernoulli[bool]
instance with FNR = 0 and FPR <= 1/4 per round.

Five-step structure: (1) state the witness predicate; (2) recast as a
predicate on the witness pool so Axiom 1 applies cleanly to distinct
witnesses; (3) apply the composition theorem for k rounds, giving
FPR_k <= (1/4)^k; (4) pseudocode plus numerical example with n = 341
(a Fermat pseudoprime that Miller-Rabin correctly identifies as
composite via non-trivial square root of 1); (5) pedagogical reframe:
primality testing is not a separate technique; it is the Bernoulli
framework applied.

The Miller-Rabin walkthrough is fresh writing for this textbook; the
papers contain only a one-line reference to Miller-Rabin as a positive
Bernoulli Boolean.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Draft §3.5 Composition is the Bridge to Sets (~4 pp)

**Files:**
- Modify: `book/chapters/ch03/bridge-to-sets.tex`

**Spec target:** spec §6 row 3.5.

**Sources:** Mostly fresh writing. Forward references to chapters 5, 6, 9.

**Content checklist:**
- Section header `\section{Composition is the Bridge to Sets}\label{sec:bridge-to-sets}`.
- Comment block at top noting forward refs to chapters 5, 6, 9.
- Forward references made specific (per spec):
  - **A Bloom filter's m hashes are exactly k-fold composition.** Each hash is a `Bernoulli[bool]` instance; the AND of the m hash results is the Bloom filter's membership query. Forward to chapter 5 §5.x.
  - **Set-operation error rates fall out of this Boolean algebra.** The error rates for set union, intersection, complement on `Bernoulli[Set]` instances are derivable from the AND, OR, NOT formulas. Forward to chapter 6.
  - **Approximate function composition is composition lifted to maps.** When `Bernoulli[Map[X,Y]]` arrives in chapter 9, the composition machinery generalizes from Boolean (output Y = bool) to arbitrary Y. Forward to chapter 9.
- Three named bridges, one per chapter, made concrete (not vague hand-waving).
- Closing transition to §3.6 (Bibliographic Notes).

**Cross-references:**
- Forward to chapter 5 `\Cref{ch:approximate-sets}` (chapter 5 stub from Plan 0; should resolve).
- Forward to chapter 6 (`\Cref{ch:set-composition}` if labeled, otherwise prose reference).
- Forward to chapter 9 (`\Cref{ch:approximate-functions}` if labeled, otherwise prose reference).
- Backward to §3.1, §3.3, §3.4.

**Length target:** ~4 pp.

- [ ] **Step 1: Read spec §6 row 3.5.**

- [ ] **Step 2: Verify chapter 5, 6, 9 stub labels**

Run: `grep -n 'label{ch:' book/chapters/ch[0-9]*-*.tex | head -20`
Expected: at least `ch:approximate-sets` should exist as a label in chapter 5's stub.

- [ ] **Step 3: Read prior context**

Read §3.4 just drafted.

- [ ] **Step 4: Draft the section**

Replace `book/chapters/ch03/bridge-to-sets.tex` content with `\section{Composition is the Bridge to Sets}\label{sec:bridge-to-sets}` plus ~4 pp meeting checklist.

- [ ] **Step 5: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0.

- [ ] **Step 6: Self-review**

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch03/bridge-to-sets.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 3.5 Composition is the Bridge to Sets (~4 pp)

Four-page transition section: three named bridges from Boolean
algebra under noise to Part II / III content. (1) Bloom filter's m
hashes as k-fold composition: each hash is a Bernoulli[bool], the AND
is the membership query. (2) Set-operation error rates derive from
the AND/OR/NOT formulas, forward to chapter 6 (set composition).
(3) Approximate function composition lifts from Boolean (Y = bool) to
arbitrary Y, forward to chapter 9 (approximate functions and n-ary
channels). Closing transition to bibliographic notes.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Draft §3.6 Bibliographic Notes (~1-2 pp)

**Files:**
- Modify: `book/chapters/ch03/bibliographic-notes.tex`
- Modify: `book/references.bib` (add new entries)

**Spec target:** spec §6 row 3.6.

**New bibtex entries needed:**

```bibtex
@article{miller-1976,
  author  = {Gary L. Miller},
  title   = {Riemann's Hypothesis and Tests for Primality},
  journal = {Journal of Computer and System Sciences},
  volume  = {13},
  number  = {3},
  pages   = {300--317},
  year    = {1976}
}

@article{rabin-1980,
  author  = {Michael O. Rabin},
  title   = {Probabilistic Algorithm for Testing Primality},
  journal = {Journal of Number Theory},
  volume  = {12},
  number  = {1},
  pages   = {128--138},
  year    = {1980}
}

@book{cormen-clrs,
  author    = {Thomas H. Cormen and Charles E. Leiserson and Ronald L. Rivest and Clifford Stein},
  title     = {Introduction to Algorithms},
  publisher = {MIT Press},
  edition   = {3rd},
  year      = {2009}
}

@book{mitzenmacher-upfal,
  author    = {Michael Mitzenmacher and Eli Upfal},
  title     = {Probability and Computing: Randomization and Probabilistic Techniques in Algorithms and Data Analysis},
  publisher = {Cambridge University Press},
  edition   = {2nd},
  year      = {2017}
}
```

**Content checklist:**
- Section header `\section*{Bibliographic Notes}` with TOC entry.
- Paragraph on Miller (1976) and Rabin (1980) for the original Miller-Rabin papers.
- Paragraph on Cormen et al (CLRS) and Mitzenmacher-Upfal as standard textbook treatments.
- Paragraph on the Bernoulli papers (cite `towell-bernoulli-sets` for the composition theorem source).
- Paragraph on the connection to chapter 2 §2.3 and chapter 4 §4.4: same composition algebra at three different abstraction layers (matrix product, Boolean algebra, Kronecker tensor).
- Cross-reference to chapter 4 bibliographic notes via `\Cref{sec:bib-notes-ch4}`.

**Cross-references:** All citations.

**Length target:** ~1-2 pp.

- [ ] **Step 1: Read existing references.bib**

Run: `grep -E '@(book|article|misc)' book/references.bib`
Expected: list of existing entries.

- [ ] **Step 2: Add new bibtex entries**

Append the four new entries above to `book/references.bib`.

- [ ] **Step 3: Draft the section**

Replace `book/chapters/ch03/bibliographic-notes.tex` content with `\section*{Bibliographic Notes}` (with TOC entry and `\label{sec:bib-notes-ch3}`) plus ~1-2 pp meeting checklist.

- [ ] **Step 4: Build and verify all citations resolve**

Run: `cd book && make cleanall && make`
Expected: exit code 0; biber resolves all 4 new citations.

Run: `grep "Citation.*undefined" book/book.log | head -5`
Expected: no undefined citations for chapter 3.

- [ ] **Step 5: Self-review**

- [ ] **Step 6: Commit**

```bash
git add book/chapters/ch03/bibliographic-notes.tex book/references.bib
git commit -m "$(cat <<'EOF'
book: draft chapter 3.6 Bibliographic Notes; add Miller, Rabin, CLRS, Mitzenmacher-Upfal bib entries

One-to-two page bibliographic notes section. Cites Miller (1976)
and Rabin (1980) for the original Miller-Rabin papers. Cites Cormen-
Leiserson-Rivest-Stein (CLRS, 3rd ed) and Mitzenmacher-Upfal (2nd ed)
for standard textbook treatments. Cites the Bernoulli papers for the
composition theorem source. Notes the same composition algebra
appears at three abstraction layers: matrix product (chapter 2.3),
Boolean algebra (chapter 3.3), Kronecker tensor (chapter 4.4).

Four new bibtex entries added to references.bib.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: Draft 10-12 exercises with star difficulty markers

**Files:**
- Modify: `book/chapters/ch03/exercises.tex`

**Spec target:** spec §6 row 3.4 exercises subsection.

**Specific exercises (per spec):**

**★ × 3 (warm-up):**
1. Derive OR rates from AND via De Morgan.
2. Compute FPR after 3-stage AND chain (worked).
3. Compute Miller-Rabin's k for FPR ≤ 10^-6.

**★★ × 5 (medium):**
4. Verify §3.3 on a specific 4-stage example by hand.
5. Show NOT is its own inverse on `Bernoulli[bool]`.
6. Implement Miller-Rabin in 20 lines and check empirical FPR.
7. Prove the composition theorem assuming Axiom 1.
8. Construct a 3-bit ANDed-confidence example.

**★★★ × 3 (challenging):**
9. Explain why §3.1's AND derivation tacitly assumes Axiom 2.
10. Show AND, OR, NOT under noise satisfies De Morgan's laws (with the right error-rate conventions).
11. Construct a system where the composition theorem fails (preview of ch 16 negative space).

**Length:** ~1-2 pp.

- [ ] **Step 1: Read chapter 4 and 2 exercises files for difficulty marker pattern**

The macros are now `\providecommand`-based (per the Task 7 §2.7 fix). Use the same pattern locally if the macros aren't available globally.

- [ ] **Step 2: Draft exercises**

Replace `book/chapters/ch03/exercises.tex` with `\section*{Exercises}` (with TOC entry) plus 11 exercises.

- [ ] **Step 3: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0.

- [ ] **Step 4: Verify distribution**

Run: `grep -c "exstar" book/chapters/ch03/exercises.tex`
Expected: at least 11.

- [ ] **Step 5: Self-review**

- [ ] **Step 6: Commit**

```bash
git add book/chapters/ch03/exercises.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 3 exercises (11 with star difficulty markers)

11 exercises distributed as 3 star (warm-up: De Morgan derivation,
3-stage AND chain, Miller-Rabin k for FPR <= 1e-6), 5 two-star
(medium: 4-stage verification, NOT involution, Miller-Rabin
implementation, composition theorem proof, 3-bit ANDed-confidence),
3 three-star (challenging: tacit Axiom 2 in AND derivation, De
Morgan's laws for noisy gates, composition theorem failure mode as
chapter 16 preview).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 9: Draft `python/notebooks/ch03-boolean-algebra-noise.ipynb`

**Files:**
- Create: `python/notebooks/ch03-boolean-algebra-noise.ipynb`

**Spec target:** Part I spec §6 (chapter 3 notebook commitment).

**Content checklist:**
- Markdown intro cell: chapter title, brief intro, pointer to `book/chapters/ch03/`.
- Section: bit-level AND/OR/NOT under simulated noise. Define helpers; demonstrate truth tables under noise empirically.
- Section: verify §3.3's composition theorem on a 5-stage chain. Empirical vs theoretical comparison.
- Section: implement Miller-Rabin in ~25 lines. Test on small primes and small composites (including 341 as a Fermat-pseudoprime).
- Section: empirical FPR_k vs theoretical (1/4)^k. Run k=1..20 on random composites; plot empirical false-positive rate vs the bound.
- Section: open question on dependent witnesses (forward to ch 16). Show what happens when witnesses are correlated.
- Closing markdown cell: cross-reference to chapter 4 notebook (which doesn't exist; chapter 4 is theory-only by design, note this explicitly).

**Format:** `.ipynb` JSON. Verify it parses and runs end-to-end.

- [ ] **Step 1: Inspect existing notebooks for pattern**

Read `python/notebooks/ch02-binary-channels.ipynb` for style.

- [ ] **Step 2: Implement Miller-Rabin carefully**

Standard algorithm:

```python
def miller_rabin(n, a):
    """One round of Miller-Rabin with witness a. Returns 'composite' or 'probably prime'."""
    if n < 2 or n % 2 == 0:
        return 'composite' if n != 2 else 'probably prime'
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return 'probably prime'
    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return 'probably prime'
    return 'composite'
```

Test: `miller_rabin(341, 2)` should return `'composite'` (Miller-Rabin catches 341 as a Fermat pseudoprime).

- [ ] **Step 3: Write the notebook**

Create the notebook with cells implementing the checklist.

- [ ] **Step 4: Verify JSON validity**

Run: `python3 -c "import json; json.load(open('python/notebooks/ch03-boolean-algebra-noise.ipynb'))"`

- [ ] **Step 5: Verify execution (if jupyter available)**

Run: `cd python && jupyter nbconvert --to notebook --execute notebooks/ch03-boolean-algebra-noise.ipynb --output /tmp/ch03-test.ipynb 2>&1 | head -20`

- [ ] **Step 6: Self-review**

- [ ] **Step 7: Commit**

```bash
git add python/notebooks/ch03-boolean-algebra-noise.ipynb
git commit -m "$(cat <<'EOF'
python: add chapter 3 notebook (Boolean algebra under noise)

Paired notebook for chapter 3. Sections: bit-level AND/OR/NOT under
simulated noise; verify the composition theorem (section 3.3) on a
5-stage chain; implement Miller-Rabin in ~25 lines and test on
n = 341 (Fermat pseudoprime); empirical FPR_k vs theoretical (1/4)^k
for k = 1..20 on random composites; open question on dependent
witnesses (forward to chapter 16, negative space).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 10: Final chapter 3 integration verification

**Files:** none modified.

- [ ] **Step 1: Full clean rebuild**

Run: `cd book && make cleanall && make`
Expected: exit 0.

- [ ] **Step 2: Page count check**

Inspect `book.toc`. Expected: chapter 3 = ~28-36 pp (target 28; ±15% gives 24-32; based on Plan 1 and 2 patterns, expect 32-38).

- [ ] **Step 3: Cross-reference resolution**

Run: `grep -E "Reference.*undefined" book/book.log | head -20`
Expected: warnings ONLY for forward references to chapter 1 stubs. No undefined intra-chapter-3 refs.

- [ ] **Step 4: Citation resolution**

Run: `grep -E "Citation.*undefined" book/book.log | head -10`
Expected: zero undefined citations.

- [ ] **Step 5: Banned phrases**

```bash
python3 -c "import os, glob; banned=[chr(0x2014), 'lever'+'age']; hits=[]; \
[hits.append((f,b)) for f in glob.glob('book/chapters/ch03/**/*.tex', recursive=True) for b in banned if b in open(f).read()]; \
print('CLEAN' if not hits else f'FOUND: {hits}')"
```

Also for the notebook:
```bash
python3 -c "import json; nb=json.load(open('python/notebooks/ch03-boolean-algebra-noise.ipynb')); banned=[chr(0x2014),'lever'+'age']; hits=[]; [[hits.append((c.get('cell_type'),b,line)) for line in (c.get('source',[]) if isinstance(c.get('source'),list) else [c.get('source','')]) for b in banned if b in line] for c in nb['cells']]; print('CLEAN' if not hits else f'FOUND: {hits}')"
```

- [ ] **Step 6: Working tree state**

Run: `git status -s`
Expected: empty or only pre-existing M files.

- [ ] **Step 7: Notebook validity**

Run: `python3 -c "import json; json.load(open('python/notebooks/ch03-boolean-algebra-noise.ipynb'))"`

- [ ] **Step 8: Commit log**

Run: `git log --oneline 431bca5..HEAD`
Expected: ~10-12 Plan 3 commits.

- [ ] **Step 9: No commit (verification only).**

---

## Self-Review

**Spec coverage check.** Each spec §6 row maps to a task:

| Spec §6 row | Task |
|---|---|
| Learning outcomes box | Task 1 |
| 3.1 AND Under Noise | Task 2 |
| 3.2 OR and NOT | Task 3 |
| 3.3 Composition Theorem | Task 4 |
| 3.4 Miller-Rabin (climax) | Task 5 |
| 3.5 Bridge to Sets | Task 6 |
| 3.6 Bibliographic Notes | Task 7 |
| Exercises (10-12, marked) | Task 8 |
| Notebook | Task 9 |
| Cross-cutting commitments | distributed; verified Task 10 |

**Placeholder scan.** No "TBD", "TODO", "implement later" in plan-level prose.

**Type and naming consistency check.**
- Section labels (`sec:and-under-noise`, `sec:or-not`, `sec:composition-theorem`, `sec:miller-rabin`, `sec:bridge-to-sets`, `sec:bib-notes-ch3`) consistent across tasks.
- File paths (`book/chapters/ch03/<slug>.tex`) consistent.
- Difficulty marker macros use `\providecommand` per the Plan 2 §2.7 fix.
- Notebook filename matches chapter source filename pattern (`ch03-boolean-algebra-noise.ipynb` paired with `ch03-boolean-algebra-noise.tex`).
- Q convention assumed consistent with chapters 2 and 4 (rows by input block).
- Composition formulas: §3.3 uses $\eta_{\text{total}} = 1 - \prod(1 - \eta_i)$ at the Boolean-algebra layer; §2.3 uses $Q_{\text{total}} = Q_2 Q_1$ at the matrix-product layer; §4.4 uses Kronecker for parallel queries. The plan's Step 5 in Task 4 explicitly verifies these reconcile.

**Scope check.** Plan 3 covers chapter 3 only. Cross-references TO chapter 1 use tentative labels; verification in Plan 4.

**Ambiguity check.** The §3.3 composition theorem's exact form ($\eta_{\text{total}} = 1 - \prod(1-\eta_i)$ vs the BSC-specific $2\fprate - 2\fprate^2$) is the most likely conflation point. Task 4 Step 5 has explicit verification language; the implementer needs to handle this carefully.

---

## Plan complete

The plan is saved to `docs/superpowers/plans/2026-05-04-bernoulli-textbook-ch03-boolean-algebra.md`.

After this plan executes, chapter 3 is a fully drafted ~28-36 pp deliverable plus its companion notebook. The next plan to write is **Plan 4: Chapter 1 (The Noisy Bit) plus Part I integration**, drafting ~25 pp and verifying that all forward/backward references across chapters 1-4 resolve. Plan 4 is the final Part I plan.
