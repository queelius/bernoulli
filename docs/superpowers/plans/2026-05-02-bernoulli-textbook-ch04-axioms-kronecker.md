# Bernoulli Textbook Chapter 4: Two Axioms and Kronecker Factorization (Plan 1)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 4 of Part I (~28 pp): the formal axiomatization of the Bernoulli framework, the Kronecker factorization theorem, and the formal `Bernoulli[bool]` definition that retroactively justifies chapters 1-3.

**Architecture:** Replace the existing `book/chapters/ch04-axioms-kronecker.tex` stub with a fully drafted chapter containing 7 sections, a learning-outcomes opener, 10-12 exercises, and supporting bibliographic entries. Build verification at every section commit ensures the book continues to compile cleanly. No notebook (per spec, ch 4 is intentionally theory-only).

**Tech Stack:** LaTeX (book class), alex.sty notation package, biblatex with biber backend. The build pipeline established in Plan 0 (scaffolding) is the test harness; "the test" for prose is `make cleanall && make` returning a clean PDF with the new chapter rendered.

**Scope:** Chapter 4 only. Cross-chapter integration with chapters 1-3 is deferred to Plan 4 (which drafts chapter 1 last and runs the Part I integration check). This plan's cross-references *forward* to Part II and *backward* to chapters 1-3 must match the spec's §8 reference map; verification that the actual chapter-1-3 prose matches happens in Plan 4.

**Spec source of truth:** `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §7 (chapter 4 outline) and §8 (reference map).

**Source material (papers to reformulate):**
- `papers/bernoulli_sets/sections/bernoulli_model.tex` for Axioms 1-2 formal statements (§4.2, §4.3)
- `papers/bernoulli_sets/sections/bernoulli_model.tex` parametric parsimony remark (§4.4 corollary)
- `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` for model order context (§4.4 background)
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Example 3.5 (Boolean universe with full PMF) for §4.5 worked example

---

## File Structure

After this plan completes, the following files exist in `book/`:

```
book/
├── chapters/
│   └── ch04-axioms-kronecker.tex      # rewritten from stub to ~28 pp chapter
├── references.bib                      # extended with new bibtex entries cited in ch 4
└── book.pdf                            # rebuilt; ch 4 now renders fully
```

Decomposition: Chapter 4 lives in a single `.tex` file. Section subdivisions are in-file (`\section{}`, `\subsection{}`); separate per-section files would be over-engineered for a 28 pp chapter. The file is organized top-to-bottom matching the spec's section order: opener, §4.1, §4.2, ..., §4.7, exercises.

`references.bib` already exists (created in Plan 0) with two placeholder entries. This plan adds entries for: Kronecker (1860s product paper, historical), Cover and Thomas (channel coding), and citations to the Bernoulli paper sections being reformulated.

`book/figures/ch04/` is NOT created. Chapter 4 is theory; no figures are needed (a future revision could add an axiom-dependency diagram if useful, but that is out of scope here).

---

## Per-Task Drafting Discipline

Every section drafting task follows the same internal structure:

1. **Read paper source(s)** named in the task header.
2. **Read prior context** from earlier in the chapter (if §4.X is being drafted, read §4.1 through §4.{X-1} as already drafted in the file).
3. **Draft the section** to the page-length target, content checklist, and notation requirements specified in the task.
4. **Verify forward and backward references** specified in the task are present.
5. **Build the book** with `cd book && make cleanall && make` and confirm exit code 0.
6. **Self-review** against the section's content checklist.
7. **Commit** with the message format specified in the task.

This is the prose analog of TDD: the "test" is the build (must compile) plus the content checklist (must contain specified material). The checklist serves as the failing-test-first criterion.

---

## Tasks

### Task 1: Read source material and write chapter scaffolding

**Files:**
- Modify: `book/chapters/ch04-axioms-kronecker.tex` (currently a one-line stub)

**Source reading (all):**
- `papers/bernoulli_sets/sections/bernoulli_model.tex` (Axioms 1-2; parametric parsimony remark; Example 3.5 Boolean universe)
- `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` (model order, channel matrix Q context)
- `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §7 and §8

- [ ] **Step 1: Read all sources end-to-end**

Use `Read` on the four file paths above. Note: the `\theoremstyle{plain}` and theorem environments come from `alex.sty` (already loaded in `book/preamble.tex`).

- [ ] **Step 2: Replace the stub with chapter scaffolding**

Open `book/chapters/ch04-axioms-kronecker.tex` and replace its current contents (a one-line placeholder from Plan 0) with:

```latex
\chapter{Two Axioms and Kronecker Factorization}
\label{ch:axioms-kronecker}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item State Axioms 1 and 2 of the Bernoulli model formally.
  \item Prove the Kronecker factorization theorem and derive the parameter
    count drop from $n(2^m - 1)$ to $2m$.
  \item Write the formal definition of $\Bernoulli{\Bool}$ and recognize
    every example from chapters 1--3 as an instance.
\end{itemize}
\end{quote}

% Section 4.1
\input{chapters/ch04/why-axioms}

% Section 4.2
\input{chapters/ch04/axiom-1}

% Section 4.3
\input{chapters/ch04/axiom-2}

% Section 4.4
\input{chapters/ch04/kronecker}

% Section 4.5
\input{chapters/ch04/bernoulli-bool-formal}

% Section 4.6
\input{chapters/ch04/what-comes-next}

% Section 4.7
\input{chapters/ch04/bibliographic-notes}

% Exercises
\input{chapters/ch04/exercises}
```

Wait. The decomposition decision was "single .tex file" earlier in this plan, but the scaffolding above suggests subfiles. Reconsider: for a 28-page chapter, splitting into subfiles aids per-section editing and reduces git diff churn during drafting. The trade is one extra subdirectory and 8 small files. Decision: USE SUBFILES. Update the file structure section above mentally; create `book/chapters/ch04/` as a new subdirectory.

Replace the stub `ch04-axioms-kronecker.tex` with the content above (which inputs the subfiles).

- [ ] **Step 3: Create the `book/chapters/ch04/` subdirectory**

```bash
mkdir -p book/chapters/ch04
```

- [ ] **Step 4: Create empty stubs for each section subfile**

Each file gets a single line as a placeholder so the build does not break:

```bash
for slug in why-axioms axiom-1 axiom-2 kronecker bernoulli-bool-formal what-comes-next bibliographic-notes exercises; do
  echo "% Drafted in Task: see plan 2026-05-02-bernoulli-textbook-ch04-axioms-kronecker.md" > "book/chapters/ch04/${slug}.tex"
done
```

- [ ] **Step 5: Verify the chapter still builds with the new structure**

Run: `cd book && make cleanall && make`
Expected: exit code 0; `book.pdf` exists; the chapter shows the title, the learning-outcomes box, and seven empty sections (currently no `\section{}` headers because subfiles are empty).

- [ ] **Step 6: Verify the `\Bernoulli{\Bool}` macro from alex.sty resolves**

Run: `cd book && grep -i 'undefined' book.log | head -5`
Expected: no "undefined control sequence" warnings related to `\Bernoulli` or `\Bool`. If present, escalate as BLOCKED with the missing-macro detail; do NOT add the macro definition without checking alex.sty first.

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch04-axioms-kronecker.tex book/chapters/ch04/
git commit -m "$(cat <<'EOF'
book: scaffold chapter 4 (axioms and Kronecker) section subfiles

Replace ch04 stub with chapter scaffold: title, learning-outcomes box,
seven section input lines, one exercises input line. Create empty
subfile stubs in chapters/ch04/ for incremental drafting. Build still
green; sections will land in subsequent commits.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Draft §4.1 Why Axioms? (~3 pp)

**Files:**
- Modify: `book/chapters/ch04/why-axioms.tex` (currently a one-line stub)

**Spec target:** `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §7 row 4.1.

**Sources:** none (entirely fresh writing).

**Content checklist:**
- Opens with a recap of the implicit independence invocations from chapters 1-3:
  - §3.1 (AND under noise) implicitly invoked Axiom 2 (per-input-block error-rate independence)
  - §3.3 (composition theorem) implicitly invoked Axiom 1 (element-wise independence)
- Names the assumption explicitly: "we have been assuming Axiom 2 since §3.1; let us make it explicit."
- Sets up the chapter trajectory: §4.2 Axiom 1, §4.3 Axiom 2, §4.4 the theorem they justify, §4.5 the formal definition they make possible.
- Tone: motivational, brief. This is a chapter opener, not a results section.

**Notation requirements:** None new. May reference $\fprate$, $\fnrate$ if invoking specific results from chapter 3.

**References:**
- Backward to §3.1 (use `\Cref{sec:and-under-noise}` placeholder; the actual label will be created in Plan 3)
- Backward to §3.3 (`\Cref{sec:composition-theorem}` placeholder)
- Forward to §4.2, §4.3, §4.4, §4.5

Use `\Cref{...}` (cleveref) for cross-references. Where the target label does not yet exist (chapters 1-3 are stubs), use a tentative label that matches the slug pattern in the spec; Plan 4's integration pass verifies all labels resolve.

**Length target:** ~3 pages of LaTeX (when rendered).

- [ ] **Step 1: Read the spec target**

Read §7 row 4.1 of the spec. Note the purpose statement and the page target.

- [ ] **Step 2: Read prior context**

Read `book/chapters/ch04-axioms-kronecker.tex` (the chapter scaffold) to confirm the section's place in the chapter.

- [ ] **Step 3: Draft the section**

Open `book/chapters/ch04/why-axioms.tex` and replace its content with a `\section{Why Axioms?}\label{sec:why-axioms}` header followed by ~3 pp of motivational prose meeting the content checklist above.

The section should NOT introduce new mathematical content. It should narrate the recap and set expectations.

- [ ] **Step 4: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; `book.pdf` exists. Open the PDF, navigate to chapter 4 §4.1, verify the section renders with its title and prose.

- [ ] **Step 5: Verify forward and backward references**

Run: `grep -E '\\\\Cref|\\\\ref' book/chapters/ch04/why-axioms.tex`
Expected: at least four references (two backward to ch 3 sections, plus forward references to §4.2-4.5).

Tentative labels for ch 3 sections (created in Plan 3) follow the `sec:and-under-noise`, `sec:composition-theorem` pattern. Cleveref will warn about undefined references; that is expected and will be resolved in Plan 4.

- [ ] **Step 6: Self-review against the content checklist**

Re-read the section. For each checklist item, confirm it is present. If any item is missing, revise the prose now.

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch04/why-axioms.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 4.1 Why Axioms? (motivational opener)

Three-page motivational section recapping the implicit independence
invocations from ch 3 (AND under noise tacitly used Axiom 2; the
composition theorem tacitly used Axiom 1) and setting up the chapter
trajectory. No new math; chapter 4's payload starts in 4.2.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Draft §4.2 Axiom 1: Element-Wise Independence (~5 pp)

**Files:**
- Modify: `book/chapters/ch04/axiom-1.tex`

**Spec target:** spec §7 row 4.2.

**Sources:** `papers/bernoulli_sets/sections/bernoulli_model.tex` Axiom 1 statement.

**Content checklist:**
- Formal statement of Axiom 1 in a `\begin{axiom}...\end{axiom}` environment from `alex.sty`. The statement says: queries on distinct elements of the input domain induce mutually independent error events.
- Consequence proposition: under Axiom 1, the joint distribution over $n$ independent queries factors as a product of $n$ marginal distributions.
- Two illustrative examples:
  1. The Bloom filter's independence assumption is exactly Axiom 1; without it, the false-positive analysis breaks.
  2. Miller-Rabin's $k$-round bound $\fprate_k \leq (1/4)^k$ from §3.4 requires Axiom 1; without it, the bound becomes a sum-of-correlations expression that is weaker.
- **Classifier-verdict callback** (the running-thread return): a violation example. Two binary classifiers trained on overlapping data have correlated errors; Axiom 1 fails; the joint error rate is NOT the product of marginal rates. Show numerically what the inflation factor looks like for a representative correlation.
- Forward reference to §4.4 (the Kronecker theorem rests on Axiom 1).

**Notation:** Use $\PE$ (probability) and $\indep$ (independence) macros from alex.sty if defined; otherwise use $\Pr$ and $\perp\!\!\!\perp$.

**References:**
- Backward to §3.4 (Miller-Rabin bound) using `\Cref{sec:miller-rabin}`
- Backward to ch 5 implicit (Bloom filter), but ch 5 is Part II and not yet stubbed beyond the placeholder. Use a tentative `\Cref{ch:approximate-sets}` or write narratively: "the Bloom filter we will analyze in Part II..."
- Forward to §4.4

**Length target:** ~5 pp.

- [ ] **Step 1: Read the source**

Read `papers/bernoulli_sets/sections/bernoulli_model.tex`. Locate Axiom 1's formal statement (cf. the explorer's report identifying it on or near `\begin{axiom}` blocks).

- [ ] **Step 2: Read prior context**

Read `book/chapters/ch04/why-axioms.tex` to ensure the chapter trajectory is clear.

- [ ] **Step 3: Draft the section**

Replace `book/chapters/ch04/axiom-1.tex` content with `\section{Axiom 1: Element-Wise Independence}\label{sec:axiom-1}` followed by ~5 pp meeting the content checklist.

Use the `axiom` environment from alex.sty (or the closest-matching theorem-style environment if alex.sty defines `\newtheorem{axiom}` differently; check `book/alex.sty` first).

- [ ] **Step 4: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; chapter 4 §4.2 renders with the formal axiom block, the consequence proposition, two examples, and the classifier-verdict violation.

- [ ] **Step 5: Verify references and notation**

Run: `grep -E '\\\\Cref|\\\\ref' book/chapters/ch04/axiom-1.tex`
Expected: at least 2 cross-references.

Run: `grep -E '\\\\PE|\\\\Pr|\\\\indep' book/chapters/ch04/axiom-1.tex`
Expected: probabilistic notation appears; if `\PE` is undefined in alex.sty (check first), use `\Pr` instead.

- [ ] **Step 6: Self-review against the content checklist**

Re-read and verify all six checklist items are present. The classifier-verdict callback is the easiest to forget; verify it appears.

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch04/axiom-1.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 4.2 Axiom 1 (element-wise independence)

Five-page section: formal axiom statement, consequence proposition
(joint distribution factors), two examples (Bloom filter independence
assumption; Miller-Rabin k-round bound), and the classifier-verdict
violation as the running-thread return point for ch 4.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Draft §4.3 Axiom 2: Conditional Independence of Block Error Rates (~5 pp)

**Files:**
- Modify: `book/chapters/ch04/axiom-2.tex`

**Spec target:** spec §7 row 4.3.

**Sources:** `papers/bernoulli_sets/sections/bernoulli_model.tex` Axiom 2 statement.

**Content checklist:**
- Formal statement of Axiom 2 in an `\begin{axiom}...\end{axiom}` environment.
- Consequence: per-input-block error rates are stable across queries; one channel matrix $Q$ per input-block-pair.
- Connection to chapter 2's model order: the partition blocks from §2.4 are exactly the blocks Axiom 2 ranges over.
- Worked illustration: a model-order-2 channel with two blocks $B_1 = \{\top\}$ and $B_2 = \{\bot\}$, showing how Axiom 2 implies the channel matrix Q has consistent rows for repeated queries within each block.
- Brief contrast: a Markov-correlated channel violates Axiom 2 because the per-query error rate within a block depends on history.

**Notation:** Use $Q$ for channel matrices (introduced in §2.1), $\fprate, \fnrate$ for the matrix entries.

**References:**
- Backward to §2.4 (model order, partition blocks) `\Cref{sec:model-order}`
- Backward to §2.1 (channel matrix Q) `\Cref{sec:bsc}`
- Forward to §4.4

**Length target:** ~5 pp.

- [ ] **Step 1: Read the source**

Read `papers/bernoulli_sets/sections/bernoulli_model.tex` and locate Axiom 2.

- [ ] **Step 2: Read prior context**

Read `book/chapters/ch04/why-axioms.tex` and `book/chapters/ch04/axiom-1.tex` so the section sits coherently after Axiom 1.

- [ ] **Step 3: Draft the section**

Replace `book/chapters/ch04/axiom-2.tex` with `\section{Axiom 2: Conditional Independence of Block Error Rates}\label{sec:axiom-2}` plus ~5 pp meeting the checklist.

- [ ] **Step 4: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; §4.3 renders correctly after §4.2.

- [ ] **Step 5: Verify references**

Run: `grep -E '\\\\Cref|\\\\ref' book/chapters/ch04/axiom-2.tex`
Expected: at least 3 cross-references (backward to §2.1, §2.4; forward to §4.4).

- [ ] **Step 6: Self-review against the content checklist**

Verify all five checklist items are present, especially the Markov-correlated violation example.

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch04/axiom-2.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 4.3 Axiom 2 (conditional independence of block rates)

Five-page section: formal axiom statement, consequence (one channel
matrix Q per input-block-pair, stable across queries), connection to
chapter 2's model order, worked model-order-2 illustration, and a
Markov-channel violation contrast.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Draft §4.4 The Kronecker Factorization Theorem (~7 pp), CHAPTER CLIMAX

**Files:**
- Modify: `book/chapters/ch04/kronecker.tex`

**Spec target:** spec §7 row 4.4. This is one of two named Part I climaxes (the other is §3.4).

**Sources:**
- `papers/bernoulli_sets/sections/bernoulli_model.tex` parametric parsimony remark (the idea exists; the theorem statement and proof do not)
- `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` for context

**Content checklist:**
- Theorem statement in a `\begin{theorem}...\end{theorem}` environment, formally:
  > Under Axioms 1 and 2, the joint confusion matrix $Q^{(m)}$ describing $m$ independent queries on a Bernoulli set factors as the Kronecker product $Q^{(m)} = Q_1 \otimes Q_2 \otimes \cdots \otimes Q_m$, where each $Q_i$ is the per-query $|B| \times |B|$ confusion matrix on the input partition blocks.
- **Notation note** for the Kronecker product symbol $\otimes$ at first use.
- Full proof in a `\begin{proof}...\end{proof}` environment. Constructive: shows that under Axiom 1 (independence) the joint distribution factors, and under Axiom 2 (block-rate stability) each marginal is a copy of the per-query channel matrix; the tensor product is the unique matrix realization of this factored joint distribution.
- Corollary in a `\begin{corollary}...\end{corollary}` environment: parameter count drops from $n(2^m - 1)$ (general $n$-th-order $m$-query channel) to $2m$ (under Axioms 1-2).
- Proof of the corollary: short counting argument.
- **BSC running-thread example**: $m$ independent BSCs with identical crossover $\fprate$ compose to a tensor channel whose matrix is $Q^{\otimes m}$ where $Q = \begin{pmatrix} 1 - \fprate & \fprate \\ \fprate & 1 - \fprate \end{pmatrix}$. Compute the resulting joint matrix for $m = 2$ explicitly.
- Worked $m=2$ verification example (separate from the BSC one): a 2-query Bernoulli[bool] with general parameters; confirm the theorem produces the factored joint distribution.

**Notation:** $\otimes$ for Kronecker product (notation note at first use); $Q^{(m)}$ for joint matrix; $Q_i$ for per-query matrix; $|B|$ for block count.

**References:**
- Backward to §4.2 (Axiom 1 used in proof) `\Cref{sec:axiom-1}`
- Backward to §4.3 (Axiom 2 used in proof) `\Cref{sec:axiom-2}`
- Backward to §3.1 (the AND derivation that tacitly used the theorem) `\Cref{sec:and-under-noise}`
- Backward to §2.1 (BSC for the running-thread example) `\Cref{sec:bsc}`

**Length target:** ~7 pp. This is the longest section in chapter 4.

- [ ] **Step 1: Read all sources carefully**

Read both paper sources end-to-end, paying attention to:
- The exact form of the parametric parsimony remark in `bernoulli_model.tex`
- The model-order definition in `order_and_channels.tex` (since the theorem references partition blocks)
- The notation conventions used in the papers for joint distributions

- [ ] **Step 2: Read prior context**

Read `book/chapters/ch04/axiom-1.tex` and `axiom-2.tex` so the proof references them precisely.

- [ ] **Step 3: Draft the theorem statement and proof**

Open `book/chapters/ch04/kronecker.tex` and write:

```latex
\section{The Kronecker Factorization Theorem}\label{sec:kronecker}

% Opening prose: we have axioms; here is what they buy us. The independence
% structure forces a Kronecker product representation of the joint confusion
% matrix on m queries.

% Notation note: introduce \otimes for Kronecker product.

\begin{theorem}[Kronecker Factorization]
\label{thm:kronecker}
% Statement here.
\end{theorem}

\begin{proof}
% Constructive proof, ~1-1.5 pp.
\end{proof}
```

Then add the corollary:

```latex
\begin{corollary}[Parameter Reduction]
\label{cor:parameter-reduction}
% Statement: parameter count drops from n(2^m - 1) to 2m.
\end{corollary}

\begin{proof}
% Counting argument, ~0.5 pp.
\end{proof}
```

Then add the BSC and 2-query worked examples in `\paragraph{}` blocks or `\begin{example}...\end{example}` environments (check alex.sty for `\newtheorem{example}`).

- [ ] **Step 4: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; the theorem environment, proof, corollary, and examples render with proper numbering. Inspect the PDF to confirm the math typesets correctly.

- [ ] **Step 5: Verify the proof's logic**

Re-read the proof. Check:
- Each step cites either Axiom 1 or Axiom 2 explicitly
- The factorization is constructive (the proof produces $Q^{(m)}$, not just asserts it exists)
- The transition from "joint distribution factors" to "matrix is Kronecker product" is justified
- The corollary's parameter count is verified for the worked $m=2$ example

If the proof feels rushed or hand-wavy, expand it. If it overflows 1.5 pp, consider moving details to a sketch with a footnote pointing forward to a (future) appendix.

- [ ] **Step 6: Verify references and notation**

Run: `grep -E '\\\\Cref|\\\\ref' book/chapters/ch04/kronecker.tex`
Expected: at least 4 cross-references (backward to §4.2, §4.3; backward to §3.1; backward to §2.1).

Run: `grep -E '\\\\otimes' book/chapters/ch04/kronecker.tex`
Expected: $\otimes$ appears multiple times; first occurrence has the notation note.

- [ ] **Step 7: Self-review against the content checklist**

Re-read and verify all seven checklist items are present. This is the chapter climax; if any item is missing or weakly developed, revise.

- [ ] **Step 8: Commit**

```bash
git add book/chapters/ch04/kronecker.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 4.4 Kronecker Factorization Theorem (climax 2)

Seven-page section, the formal payoff for Part I: theorem statement
that under Axioms 1-2 the joint confusion matrix on m queries factors
as a Kronecker product of per-query matrices; full constructive proof;
corollary deriving the parameter count drop from n(2^m - 1) to 2m;
BSC running-thread example with explicit m=2 computation; second
worked example for general 2-query verification.

Notation note for tensor product symbol introduced at first use.

The theorem is a fresh contribution; the papers have the parametric
parsimony idea as a remark but no formal theorem statement or proof.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Draft §4.5 The `Bernoulli[bool]` Type, Formally (~5 pp)

**Files:**
- Modify: `book/chapters/ch04/bernoulli-bool-formal.tex`

**Spec target:** spec §7 row 4.5.

**Sources:**
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Example 3.5 (Boolean universe with full PMF). This is the worked example that lands here.
- The deferral from §1.3: ch 1 introduced the Boolean universe qualitatively; this section gives it the formal treatment.

**Content checklist:**
- Formal definition of the type `Bernoulli[bool]` in a `\begin{definition}...\end{definition}` environment: a triple $(X, Y, Q)$ where $X$ is the input domain $\{\top, \bot\}$, $Y$ is the output domain $\{\top, \bot\}$, and $Q$ is a $2 \times 2$ stochastic matrix satisfying Axioms 1 and 2.
- **Notation note** for the formal type at first use.
- **Biased-coin worked example with full PMF** (the running-thread closer): a coin with bias $p$ for heads and observation noise. Compute the PMF over all four outcomes (TP, FP, TN, FN), express as a `Bernoulli[bool]` instance with explicit $Q$. This is the §1.3 deferral landing.
- Tie-back paragraph (one paragraph): chapter 1's noisy bit was a `Bernoulli[bool]`; chapter 2's BSC was a `Bernoulli[bool]` with $Q$ symmetric; chapter 2's asymmetric channel was a `Bernoulli[bool]` with $Q$ general; chapter 3's AND/OR/NOT operations are operations on `Bernoulli[bool]` instances, producing new `Bernoulli[bool]` instances (composition closure).
- Closing remark: the formal definition was earned by chapters 1-3, not asserted up front. This is the (γ) trajectory's payoff.

**Notation:** $\Bernoulli{\Bool}$ macro (use alex.sty's macro if defined; otherwise introduce as `\newcommand{\BernoulliBool}{\mathrm{Bernoulli}[\mathrm{bool}]}` in a notation comment).

**References:**
- Backward to §1.3 (Boolean universe qualitative) `\Cref{sec:boolean-universe-first-look}`
- Backward to §1.1 (noisy bit) `\Cref{sec:three-faces}`
- Backward to §2.1 (BSC) `\Cref{sec:bsc}`
- Backward to §2.2 (asymmetric channel) `\Cref{sec:asymmetric-channel}`
- Backward to §3.1, §3.2, §3.3 (Boolean algebra under noise) `\Cref{sec:and-under-noise}`, etc.
- Backward to §4.2, §4.3 (axioms cited in definition)

This section has the most cross-references in the chapter because its job is to retroactively unify everything.

**Length target:** ~5 pp.

- [ ] **Step 1: Read the source**

Read `papers/bernoulli_sets/sections/bernoulli_model.tex` Example 3.5 (Boolean universe). Note the joint distribution table and the four outcomes.

- [ ] **Step 2: Read prior context (entire chapter so far)**

Read `book/chapters/ch04/why-axioms.tex`, `axiom-1.tex`, `axiom-2.tex`, `kronecker.tex`. The formal definition must use exactly the axioms drafted in §4.2-4.3 and align with the notation introduced in §4.4.

- [ ] **Step 3: Draft the section**

Replace `book/chapters/ch04/bernoulli-bool-formal.tex` content with `\section{The \texorpdfstring{$\Bernoulli{\Bool}$}{Bernoulli[bool]} Type, Formally}\label{sec:bernoulli-bool-formal}` plus ~5 pp meeting the checklist.

The biased-coin worked example should compute the joint PMF table explicitly. Use a small `tabular` for the four outcomes.

- [ ] **Step 4: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; the definition, the biased-coin example, and the tie-back paragraph all render. The PMF table is well-formatted.

- [ ] **Step 5: Verify references**

Run: `grep -E '\\\\Cref|\\\\ref' book/chapters/ch04/bernoulli-bool-formal.tex`
Expected: at least 6 cross-references (backward to §1.1, §1.3, §2.1, §2.2, §3.x, §4.2-4.3). This is the integration section; its job is to point at everything that came before.

- [ ] **Step 6: Self-review against the content checklist**

Verify all five checklist items. The tie-back paragraph is the most important; it is what makes the (γ) trajectory pay off. If it reads as a perfunctory recap rather than a synthesis, revise.

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch04/bernoulli-bool-formal.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 4.5 Bernoulli[bool] Type, Formally

Five-page section: formal definition of Bernoulli[bool] as a triple
(X, Y, Q) under Axioms 1-2; biased-coin worked example with full PMF
(landing the deferral from chapter 1.3); tie-back paragraph showing
chapters 1-3 examples are all instances of the now-defined type.

The (gamma) trajectory's payoff: the formal definition is earned by
the chapters that preceded it.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Draft §4.6 What Comes Next (~2 pp)

**Files:**
- Modify: `book/chapters/ch04/what-comes-next.tex`

**Spec target:** spec §7 row 4.6.

**Sources:** none (entirely fresh).

**Content checklist:**
- Brief Part II preview: "now that we have `Bernoulli[bool]`, we go from bits to sets."
- Map of the Five Core Principles' status: Two Axioms ✓ (this chapter), Composition Closure ✓ (chapter 3), Boolean Thread ✓ (Part I overall); Space-Accuracy Duality and Parametric Parsimony arrive in Part II.
- One-paragraph forward-look at chapter 5 (approximate sets and predicates) and the Bloom filter as the canonical first construction.

**Notation:** None new.

**References:**
- Forward to chapter 5 (`\Cref{ch:approximate-sets}`). This label is in a chapter 5 stub from Plan 0; verify it exists.
- Forward to "Part II" generically (no `\partref` macro typically; use prose).

**Length target:** ~2 pp. Keep tight; this is a chapter closer.

- [ ] **Step 1: Read the spec target**

Read §7 row 4.6 of the spec. Note the brevity target.

- [ ] **Step 2: Read prior context**

Read `book/chapters/ch04/bernoulli-bool-formal.tex` to ensure the closer flows from the definition section.

- [ ] **Step 3: Draft the section**

Replace `book/chapters/ch04/what-comes-next.tex` content with `\section{What Comes Next}\label{sec:what-comes-next}` plus ~2 pp meeting the checklist.

- [ ] **Step 4: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; the closer renders cleanly.

- [ ] **Step 5: Verify references**

Run: `grep -E '\\\\Cref|\\\\ref' book/chapters/ch04/what-comes-next.tex`
Expected: at least one forward reference to chapter 5 or a Part II section.

- [ ] **Step 6: Self-review**

Re-read and verify the Five Core Principles status box is present and accurate.

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch04/what-comes-next.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 4.6 What Comes Next (Part I closer)

Two-page closer: Part II preview (bits to sets); Five Core Principles
status box (Two Axioms, Composition Closure, Boolean Thread now
visible; Space-Accuracy Duality and Parametric Parsimony arrive in
Part II); one-paragraph forward-look at the Bloom filter as the
canonical chapter-5 construction.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: Draft §4.7 Bibliographic Notes (~1-2 pp) and update references.bib

**Files:**
- Modify: `book/chapters/ch04/bibliographic-notes.tex`
- Modify: `book/references.bib`

**Spec target:** spec §7 row 4.7.

**Sources:** none (entirely fresh prose; new bib entries needed).

**Content checklist:**
- One paragraph on Kronecker (1860s; the original Kronecker product paper is hard to cite directly; cite a modern reference such as Horn and Johnson's *Topics in Matrix Analysis* or any current matrix-algebra textbook).
- One paragraph on Cover and Thomas (channel coding context; not a direct source but the canonical reference for information-theoretic background).
- One paragraph on the Bernoulli papers (cite `bernoulli-sets` for the axioms, `bernoulli-data-type` for the model-order treatment).
- Note: the formal Kronecker theorem statement (§4.4) is a fresh contribution of this book, not a citation. Make this explicit so future readers know not to attribute it to the underlying papers.

**New bibtex entries needed in `references.bib`:**

- `horn-johnson-matrix` (Horn and Johnson, *Topics in Matrix Analysis*, Cambridge, 1991)
- `cover-thomas` (Cover and Thomas, *Elements of Information Theory*, Wiley, 2nd ed. 2006)
- `kronecker-1858` (placeholder for the historical reference; if a stable citation cannot be found, omit and cite Horn and Johnson for the historical attribution)

The existing `references.bib` already has `towell-bernoulli-sets` and `towell-bernoulli-book` from Plan 0. Plan 1 extends with Horn-Johnson, Cover-Thomas, and `towell-bernoulli-data-type` (analog of `towell-bernoulli-sets`).

**References:**
- Cite `\textcite{}` (or `\cite{}`) for each bib entry mentioned in the prose.

**Length target:** ~1-2 pp.

- [ ] **Step 1: Add new entries to `references.bib`**

Append to `book/references.bib`:

```bibtex
@book{horn-johnson-matrix,
  author    = {Roger A. Horn and Charles R. Johnson},
  title     = {Topics in Matrix Analysis},
  publisher = {Cambridge University Press},
  year      = {1991}
}

@book{cover-thomas,
  author    = {Thomas M. Cover and Joy A. Thomas},
  title     = {Elements of Information Theory},
  publisher = {Wiley},
  edition   = {2nd},
  year      = {2006}
}

@misc{towell-bernoulli-data-type,
  author = {Alexander Towell},
  title  = {Random approximate values over algebraic types},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/bernoulli_data_type}}
}
```

- [ ] **Step 2: Draft the bibliographic notes section**

Replace `book/chapters/ch04/bibliographic-notes.tex` content with `\section*{Bibliographic Notes}` (no number, mark with `\addcontentsline{toc}{section}{Bibliographic Notes}`) plus ~1-2 pp meeting the checklist.

Cite each entry once with `\textcite{...}` or `\cite{...}` depending on the prose form.

- [ ] **Step 3: Build and verify citations resolve**

Run: `cd book && make cleanall && make`
Expected: exit code 0; the bibliographic notes section renders; all four citations resolve in the bibliography listing at the end of the book.

Run: `grep -E "Citation.*undefined|Reference.*undefined" book/book.log | head -5`
Expected: no undefined-citation warnings for the new entries.

- [ ] **Step 4: Self-review**

Verify all four checklist items are present, especially the explicit "the Kronecker theorem statement is a fresh contribution" note.

- [ ] **Step 5: Commit**

```bash
git add book/chapters/ch04/bibliographic-notes.tex book/references.bib
git commit -m "$(cat <<'EOF'
book: draft chapter 4.7 bibliographic notes; add Horn-Johnson, Cover-Thomas, bernoulli-data-type bib entries

One- to two-page bibliographic notes section citing Horn-Johnson for
the Kronecker product matrix-algebra background, Cover-Thomas for the
information-theoretic context, and the Bernoulli papers (sets and
data-type) for the axioms and model-order treatment. Explicit note
that the formal Kronecker theorem statement in section 4.4 is a fresh
contribution of this book, not a paper citation.

Three new bibtex entries added to references.bib.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 9: Draft 10-12 exercises with difficulty markers

**Files:**
- Modify: `book/chapters/ch04/exercises.tex`

**Spec target:** spec §7 (exercises sub-section) and §3.4 (cross-cutting exercise commitment).

**Sources:** none (entirely fresh).

**Content checklist:**
- Section header: `\section*{Exercises}` with TOC entry.
- 10-12 exercises in an `enumerate` environment, each marked with difficulty: `\exstar` for ★, `\exstarstar` for ★★, `\exstarstarstar` for ★★★.
- Difficulty markers: define `\newcommand{\exstar}{$\star$}`, `\newcommand{\exstarstar}{$\star\star$}`, `\newcommand{\exstarstarstar}{$\star\star\star$}` if not already in alex.sty (check first; if defined, use the existing macros).
- Distribution: 3 ★, 5 ★★, 3 ★★★. Total 11.
- Specific exercises (per spec §7):
  - **★ × 3**: state Axiom 1 in measure-theoretic notation; restate Axiom 2 as a property of $Q$; write the Kronecker product of two $2 \times 2$ matrices.
  - **★★ × 5**: prove the parameter count corollary $n(2^m - 1) \to 2m$; verify the Kronecker theorem on the 2-query example by hand; show a Markov channel violates Axiom 1; identify the implicit Axiom-2 assumption in §3.1's AND derivation; construct a `Bernoulli[bool]` from the biased coin and verify both axioms.
  - **★★★ × 3**: prove Axiom 1 implies Axiom 2 does NOT hold automatically (counterexample); show that without Axiom 2, the channel-matrix view collapses; argue that the Kronecker theorem cannot be strengthened (the $2m$ bound is tight).

**References:** exercises cite chapter sections via `\Cref{...}` where appropriate.

**Length target:** ~1-2 pp.

- [ ] **Step 1: Check alex.sty for difficulty-marker macros**

Run: `grep -E "exstar|difficulty" book/alex.sty`
Expected: either macros exist (use them) or none (define them in `book/preamble.tex` or inline at the top of `exercises.tex`).

- [ ] **Step 2: Draft the exercises**

Replace `book/chapters/ch04/exercises.tex` content with `\section*{Exercises}\addcontentsline{toc}{section}{Exercises}` followed by an `enumerate` of 11 exercises. Each exercise prefixed with its difficulty marker.

Selected solutions for some exercises will land in Appendix D in a future plan; do NOT add solutions here.

- [ ] **Step 3: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; exercises render with difficulty markers.

- [ ] **Step 4: Verify exercise distribution**

Run: `grep -c "exstar" book/chapters/ch04/exercises.tex`
Expected: at least 11 occurrences of difficulty markers (one per exercise).

Manually count: 3 ★, 5 ★★, 3 ★★★. If the distribution drifts, revise.

- [ ] **Step 5: Self-review against the spec checklist**

Re-read each exercise. For each, verify:
- It maps to a section content area
- The difficulty marker matches the work required
- The exercise is solvable from the chapter content alone (no external sources needed)

- [ ] **Step 6: Commit**

```bash
git add book/chapters/ch04/exercises.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 4 exercises (11 with star difficulty markers)

11 exercises distributed as 3 star (warm-up), 5 two-star (medium),
3 three-star (challenging or extension), matching the cross-cutting
exercise discipline from the Part I spec. Selected solutions will
land in Appendix D in a future plan.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 10: Final chapter integration verification

**Files:** none modified (verification only).

- [ ] **Step 1: Full clean rebuild**

Run: `cd book && make cleanall && make`
Expected: exit code 0; `book/book.pdf` exists and is significantly larger than the post-Plan-0 baseline (60 pages then; ~85+ pages now after chapter 4 fills in).

- [ ] **Step 2: Verify chapter 4 page count is in the spec range**

Open `book/book.pdf`. Locate chapter 4. Count its pages.
Expected: 25-32 pages (target was ~28; ±15% acceptable).

If under 25, the chapter is thinner than spec; review which sections may need expansion. If over 32, the chapter has bloated; trim §4.4 (the longest section) or move proof details to a footnote.

- [ ] **Step 3: Verify all internal cross-references resolve**

Run: `grep -E "Reference.*undefined|Citation.*undefined" book/book.log | head -20`
Expected: warnings ONLY for forward references to chapters 1-3 sections (which are still stubs). NO undefined references for in-chapter-4 cross-refs (all the §4.X labels should resolve to other §4.Y labels within ch 4).

If §4.X to §4.Y references fail, fix the labels.

- [ ] **Step 4: Verify all citations resolve**

Run: `grep -E "Citation.*undefined" book/book.log | head -10`
Expected: no undefined citations. All four bib entries (`towell-bernoulli-sets`, `towell-bernoulli-data-type`, `horn-johnson-matrix`, `cover-thomas`) should resolve.

- [ ] **Step 5: Verify no soul-voice violations were introduced**

The repository's soul-voice hook blocks banned phrases at write time, so this is a sanity recheck:

```bash
python3 -c "import os, glob; banned=[chr(0x2014), 'lever'+'age']; hits=[]; \
[hits.append((f,b)) for f in glob.glob('book/chapters/ch04/**/*.tex', recursive=True) for b in banned if b in open(f).read()]; \
print('CLEAN' if not hits else f'FOUND: {hits}')"
```

Expected: `CLEAN`. If `FOUND`, rewrite the offending text.

- [ ] **Step 6: Verify the working tree state**

Run: `git status -s`
Expected: empty (apart from possibly `M papers/CLAUDE.md` and `M book/book.pdf` if not committed; the PDF binary churn issue from Plan 0 still applies and is out of scope here).

- [ ] **Step 7: Verify the commit log**

Run: `git log --oneline 86053b2..HEAD`
Expected: 9 new commits (one per Tasks 1, 2, 3, 4, 5, 6, 7, 8, 9), in order, each focused on one section or scaffolding step.

- [ ] **Step 8: No commit needed (verification only)**

This task creates no new commits. It is the chapter completion checkpoint.

---

## Self-Review

**Spec coverage check.** Each spec §7 row maps to a task:

| Spec §7 row | Task |
|---|---|
| Learning outcomes box | Task 1 (in chapter scaffolding) |
| 4.1 Why Axioms? | Task 2 |
| 4.2 Axiom 1 | Task 3 |
| 4.3 Axiom 2 | Task 4 |
| 4.4 Kronecker Factorization | Task 5 |
| 4.5 Bernoulli[bool] formal | Task 6 |
| 4.6 What Comes Next | Task 7 |
| 4.7 Bibliographic Notes | Task 8 |
| Exercises (10-12, marked) | Task 9 |
| Cross-cutting commitments (notation strategy, references) | distributed across all tasks; verified in Task 10 |
| Forward and backward references (§8 of spec) | distributed; final cross-ref verification in Task 10 |

**Placeholder scan.** No "TBD", "TODO", "implement later", or "fill in details" in plan-level prose. Tasks 2-9 instruct subagents to draft prose to specified content checklists; the prose itself is authorial work, not pre-specifiable in the plan. This is the prose analog of "implement function X to spec," not a placeholder failure.

**Type and naming consistency check.**
- Section labels (`sec:why-axioms`, `sec:axiom-1`, `sec:axiom-2`, `sec:kronecker`, `sec:bernoulli-bool-formal`, `sec:what-comes-next`) consistent across Tasks 1-9.
- Theorem label `thm:kronecker` and corollary label `cor:parameter-reduction` introduced in Task 5; no conflicts elsewhere.
- File paths (`book/chapters/ch04/<slug>.tex`) consistent across Tasks 1-9.
- Bib entries (`towell-bernoulli-sets`, `towell-bernoulli-data-type`, `horn-johnson-matrix`, `cover-thomas`) consistent between Task 8 and Task 10 verification.
- Notation: `Q` for channel matrix (introduced §2.1, used §4.3-4.5); `\otimes` for Kronecker (introduced §4.4); `\Bernoulli{\Bool}` for the formal type (introduced §4.5). Consistent.

**Scope check.** This plan covers chapter 4 only. Chapters 1-3 prose is explicitly out of scope and lives in future plans 2, 3, 4. Cross-references TO chapters 1-3 use tentative labels that will be verified in Plan 4's integration check. Cross-references FROM ch 4 to Part II use either chapter-5 stub labels (which exist from Plan 0) or prose ("Part II will...").

**Ambiguity check.**
- "Use cleveref": `\Cref{...}` is the canonical macro; tasks specify this consistently.
- "Use the example environment": Task 5 says to check alex.sty for `\newtheorem{example}`; if not defined, the subagent should choose a sensible alternative (e.g., `\paragraph{Example.}` blocks). This is a known late-binding decision.
- "Use the axiom environment": Tasks 3 and 4 assume `\begin{axiom}...\end{axiom}` exists in alex.sty; if not, define it locally in `preamble.tex` as `\newtheorem{axiom}{Axiom}` and surface as a follow-up commit.

---

## Plan complete

The plan is saved to `docs/superpowers/plans/2026-05-02-bernoulli-textbook-ch04-axioms-kronecker.md`.

After this plan executes, chapter 4 is a fully drafted ~28 pp deliverable. The next plan to write is **Plan 2: Chapter 2 (Binary Channels and Model Order)**, drafting ~24 pp. Plan 2 should be written using `superpowers:writing-plans` after this plan completes; it does NOT need a separate brainstorm because the Part I spec already covers chapter 2 at full section-level detail.
