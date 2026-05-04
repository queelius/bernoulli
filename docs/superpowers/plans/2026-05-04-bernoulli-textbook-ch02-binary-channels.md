# Bernoulli Textbook Chapter 2: Binary Channels and Model Order (Plan 2)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 2 of Part I (~24 pp): the formal channel framework. The Binary Symmetric Channel as the canonical example, the Asymmetric Binary Channel as the second-order generalization, channel composition as matrix product, and model order as the partition-block concept that caps Boolean predicates at order 2.

**Architecture:** Replace the existing `book/chapters/ch02-binary-channels.tex` stub with a fully drafted chapter containing 5 sections, a learning-outcomes opener, 10-12 exercises with star difficulty markers, and supporting bibliographic entries. The chapter has a notebook (`python/notebooks/ch02-binary-channels.ipynb`) drafted as a separate task. Build verification at every section commit ensures the book continues to compile cleanly.

**Tech Stack:** LaTeX (book class), alex.sty notation package, biblatex with biber backend. Python 3.11+ + numpy + matplotlib for the notebook (uses the `bernoulli` package's eventual API but stubbed for chapter-2-level content). The build pipeline established in Plans 0-1 is the test harness.

**Scope:** Chapter 2 only. Cross-chapter integration with chapters 1, 3 is deferred to Plan 4 (which drafts chapter 1 last and runs the Part I integration check). This plan's cross-references forward to chapter 3 (composition theorem, Boolean algebra under noise) must use the labels Plan 3 will create; verification happens in Plan 4.

**Spec source of truth:** `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §5 (chapter 2 outline) and §8 (reference map).

**Source material (papers to reformulate):**
- `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` for model order, BSC, asymmetric channel formalism (§2.1, §2.2, §2.4 backbone)
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Theorem 3.7 (composition_rates) for §2.3 channel composition (chapter 3's composition theorem also reformulates this; ch 2 takes the matrix-product perspective; ch 3 takes the Boolean-algebra perspective)
- `papers/CLAUDE.md` model-order-vs-DOF clarification for §2.4

**Lessons inherited from Plan 1:**

The chapter 4 review cycle surfaced recurring failure modes that this plan must guard against:

1. **Conflation of distinct independence properties.** Chapter 2 introduces channel composition (§2.3). When chapter 3 builds on this with the composition theorem, both chapter 2 and chapter 3 must distinguish channel composition (matrix product, serial pipeline) from independence assumptions (element-wise via Axiom 1; rate stability via Axiom 2). Chapter 2 should be careful not to over-claim what channel composition gives without independence.

2. **Source paper notation drift.** The papers use (FPR, TPR) = (α, β) in places; the book uses (FPR, FNR) = (ε, ω). When reformulating, MATCH the alex.sty macros (`\fprate`, `\fnrate`, `\tprate`, `\tnrate`) and add a footnote acknowledging the source paper's choice if the difference is visible.

3. **Mathematical rigor in worked examples.** Chapter 4 had multiple math errors caught at review (subscript bugs, wrong matrix dimensions, Markov contrast inconsistency). Each worked example in chapter 2 should be verifiable: write the matrix, write the entries, sum probabilities, check.

4. **Forward references to chapter 1, 3 will not resolve.** Document expected unresolved labels in each section's header comment block.

5. **Python notebook scope.** The notebook is a teaching artifact for chapter 2 specifically. Use the `bernoulli` package's `Bernoulli[T]` placeholder where convenient; build out only what the chapter needs. No premature library design.

---

## File Structure

After this plan completes, the following files exist in the repository:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch02-binary-channels.tex           # rewritten from stub to ~24 pp chapter scaffold
│   │   └── ch02/                              # NEW directory
│   │       ├── bsc.tex                        # §2.1 (~6 pp)
│   │       ├── asymmetric-channel.tex         # §2.2 (~5 pp)
│   │       ├── channel-composition.tex        # §2.3 (~5 pp)
│   │       ├── model-order.tex                # §2.4 (~7 pp)
│   │       ├── bibliographic-notes.tex        # §2.5 (~1-2 pp)
│   │       └── exercises.tex                  # 10-12 exercises
│   └── references.bib                          # extended if new bib entries needed
└── python/
    └── notebooks/
        └── ch02-binary-channels.ipynb         # paired notebook
```

The chapter follows the same subdirectory pattern Plan 1 established for chapter 4: thin chapter file inputs section subfiles. This isolates per-section commits and keeps each subagent's working scope small.

`python/notebooks/ch02-binary-channels.ipynb` is the chapter's notebook. It demonstrates building 2x2 channel matrices, composing two BSCs and verifying the formula derived in §2.3, plotting BSC capacity, and visualizing partition blocks.

---

## Per-Task Drafting Discipline

Every section drafting task follows the same internal structure (matching Plan 1):

1. **Read paper source(s)** named in the task header.
2. **Read prior context** from earlier in the chapter (if §2.X is being drafted, read §2.1 through §2.{X-1} as already drafted in the file).
3. **Read sibling-chapter context** when relevant (chapter 4 sections inform chapter 2's references to axioms; chapter 3 sections inform forward references).
4. **Draft the section** to the page-length target, content checklist, and notation requirements specified in the task.
5. **Verify forward and backward references** specified in the task are present.
6. **Build the book** with `cd book && make cleanall && make` and confirm exit code 0.
7. **Self-review** against the section's content checklist.
8. **Commit** with the message format specified in the task.

---

## Tasks

### Task 1: Read source material and write chapter scaffolding

**Files:**
- Modify: `book/chapters/ch02-binary-channels.tex` (currently a one-line stub)

**Source reading (all):**
- `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` (model order, BSC, asymmetric channels)
- `papers/bernoulli_sets/sections/bernoulli_model.tex` (Theorem 3.7 composition_rates for §2.3 source)
- `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §5 and §8

- [ ] **Step 1: Read all sources end-to-end**

Use `Read` on the four file paths above. Note: the chapter assumes Q is the channel matrix convention. Verify the convention used in the source papers and in chapter 4 (already drafted). Chapter 4 §4.4 and §4.5 use Q[input_block, output_label]; chapter 2 must match.

- [ ] **Step 2: Replace the stub with chapter scaffolding**

Open `book/chapters/ch02-binary-channels.tex` (currently a 4-line stub from Plan 0) and replace its contents with:

```latex
\chapter{Binary Channels and Model Order}
\label{ch:binary-channels}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Define a binary channel formally and write its $2 \times 2$
    transition matrix.
  \item Distinguish symmetric (BSC) from asymmetric (Z-channel and
    general) binary channels and connect each to model order.
  \item Compose two binary channels via matrix product and read off
    the resulting channel.
  \item State the Boolean ceiling at order 2: any predicate over the
    input domain $\{\top, \bot\}$ has model order at most 2.
\end{itemize}
\end{quote}

% Section 2.1
\input{chapters/ch02/bsc}

% Section 2.2
\input{chapters/ch02/asymmetric-channel}

% Section 2.3
\input{chapters/ch02/channel-composition}

% Section 2.4
\input{chapters/ch02/model-order}

% Section 2.5
\input{chapters/ch02/bibliographic-notes}

% Exercises
\input{chapters/ch02/exercises}
```

- [ ] **Step 3: Create the `book/chapters/ch02/` subdirectory**

```bash
mkdir -p book/chapters/ch02
```

- [ ] **Step 4: Create empty stubs for each section subfile**

```bash
for slug in bsc asymmetric-channel channel-composition model-order bibliographic-notes exercises; do
  echo "% Drafted in Task: see plan 2026-05-04-bernoulli-textbook-ch02-binary-channels.md" > "book/chapters/ch02/${slug}.tex"
done
```

- [ ] **Step 5: Verify the chapter still builds with the new structure**

Run: `cd book && make cleanall && make`
Expected: exit code 0; `book.pdf` exists; the chapter shows the title, the learning-outcomes box, and five empty section slots (currently no `\section{}` headers because subfiles are empty).

- [ ] **Step 6: Verify no new build warnings**

Run: `cd book && grep -i 'undefined\|error' book.log | head -10`
Expected: only pre-existing warnings (forward references to chapters not yet drafted, including the ch04 forward refs to ch1-3 stubs). No new errors traceable to the chapter 2 scaffold.

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch02-binary-channels.tex book/chapters/ch02/
git commit -m "$(cat <<'EOF'
book: scaffold chapter 2 (binary channels) section subfiles

Replace ch02 stub with chapter scaffold: title, learning-outcomes box
with four bullets, six section input lines. Create empty subfile stubs
in chapters/ch02/ for incremental drafting, matching the chapter 4
pattern. Build still green; sections will land in subsequent commits.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Draft §2.1 The Binary Symmetric Channel (~6 pp)

**Files:**
- Modify: `book/chapters/ch02/bsc.tex`

**Spec target:** spec §5 row 2.1.

**Sources:**
- `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` (BSC fragments)
- The chapter 4 BSC examples in `book/chapters/ch04/kronecker.tex` (BSC running thread). Read these to ensure §2.1's BSC presentation is consistent with what chapter 4 assumed.

**Content checklist:**
- Section header `\section{The Binary Symmetric Channel}\label{sec:bsc}`.
- Comment block at top noting expected unresolved `\Cref` forward refs.
- BSC formal definition: input domain $\{0, 1\}$ (or $\{\top, \bot\}$), output domain $\{0, 1\}$, single crossover parameter $\fprate$.
- Channel transition matrix $Q$ introduced together with the BSC (merged from former §2.1 + §2.2 per spec).
- Notation note: $Q$ as the per-query channel matrix; rows indexed by input, columns by output; row-stochastic.
- Worked numerical example: BSC with $\fprate = 0.05$. Display $Q$. Compute the joint probability of correct/incorrect output for a single query.
- Connection to chapter 1's three faces of the noisy bit (each was a BSC instance under the symmetric special case).
- Forward reference to §2.2 (asymmetric channel as the natural generalization).

**Notation requirements:** Use `\fprate` for the crossover. Use `Q` for the channel matrix. The convention is $Q[\text{input}, \text{output}]$ with rows indexed by input block (B_1 = {⊤}, B_2 = {⊥}); see chapter 4 for the established convention.

**Length target:** ~6 pp.

**Cross-references:**
- Backward to §1.1 (chapter 1 stub) `\Cref{sec:three-faces}` for the noisy bit framings (will resolve in Plan 4).
- Forward to §2.2 `\Cref{sec:asymmetric-channel}` (will resolve in Task 3).
- Forward to §2.3 `\Cref{sec:channel-composition}` (will resolve in Task 4).
- Forward to §2.4 `\Cref{sec:model-order}` (will resolve in Task 5).

- [ ] **Step 1: Read the spec target**

Read spec §5 row 2.1.

- [ ] **Step 2: Read paper source**

Read `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex`. Find BSC discussion.

- [ ] **Step 3: Read chapter 4 BSC running thread for consistency**

Read `book/chapters/ch04/kronecker.tex` BSC subsection (around lines 270-340). Note Q convention used there.

- [ ] **Step 4: Draft the section**

Replace `book/chapters/ch02/bsc.tex` content with `\section{The Binary Symmetric Channel}\label{sec:bsc}` plus comment block plus ~6 pp of prose meeting the checklist.

- [ ] **Step 5: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; PDF builds; §2.1 renders with formal definition, channel matrix, worked example.

- [ ] **Step 6: Verify cross-references**

Run: `grep -E '\\\\Cref|\\\\ref' book/chapters/ch02/bsc.tex`
Expected: at least 3 cross-references.

- [ ] **Step 7: Verify Q convention matches chapter 4**

Open the rendered PDF and visually compare §2.1's BSC matrix with chapter 4's BSC matrix. They should be identical: $Q = \begin{pmatrix} 1 - \fprate & \fprate \\ \fprate & 1 - \fprate \end{pmatrix}$.

- [ ] **Step 8: Self-review against checklist**

Re-read the section. For each checklist item, confirm presence.

- [ ] **Step 9: Commit**

```bash
git add book/chapters/ch02/bsc.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 2.1 The Binary Symmetric Channel (~6 pp)

Six-page section introducing the BSC formally: input/output domains,
single crossover parameter epsilon, channel transition matrix Q with
notation note. Worked numerical example with epsilon = 0.05. Connects
to chapter 1's three faces of the noisy bit as instances of the
symmetric special case, sets up section 2.2's asymmetric generalization.

Q convention matches chapter 4's BSC running thread: rows indexed by
input block, columns by output label.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Draft §2.2 The Asymmetric Binary Channel (~5 pp)

**Files:**
- Modify: `book/chapters/ch02/asymmetric-channel.tex`

**Spec target:** spec §5 row 2.2.

**Sources:**
- `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` (Z-channel and asymmetric channel discussion)

**Content checklist:**
- Section header `\section{The Asymmetric Binary Channel}\label{sec:asymmetric-channel}`.
- Comment block at top.
- Z-channel as a specific asymmetric channel: $\fnrate = 0$ (or $\fprate = 0$), one-sided error model. Bloom filter as the canonical Z-channel instance.
- General asymmetric channel: independent $\fprate$ and $\fnrate$ parameters.
- $Q$ for the general asymmetric: $Q = \begin{pmatrix} 1 - \fnrate & \fnrate \\ \fprate & 1 - \fprate \end{pmatrix}$ (verify the convention against chapter 4 and §2.1; if chapter 4 uses different rows for B_1/B_2, MATCH it).
- Biased-coin running-thread callback: a coin with different heads-bias and tails-bias is an asymmetric binary channel (the running thread the spec §3.1 commits to).
- Bloom filter and medical-test instances as motivating examples.
- Worked numerical example: asymmetric channel with $\fprate = 0.05$ and $\fnrate = 0.10$.
- Forward reference to §2.4 (model order, where the BSC vs asymmetric distinction will be formalized as order 1 vs order 2, with the spec's correction that BSC is the symmetric special case of order-2 not "first-order").

**Notation requirements:** $\fprate$, $\fnrate$ from alex.sty.

**Cross-references:**
- Backward to §2.1 (BSC) `\Cref{sec:bsc}`.
- Backward to §1.1 (chapter 1 stub) `\Cref{sec:three-faces}` for biased-coin callback.
- Forward to §2.4 `\Cref{sec:model-order}`.

**Length target:** ~5 pp.

- [ ] **Step 1: Read the spec target**

Read spec §5 row 2.2.

- [ ] **Step 2: Read source**

Read `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` Z-channel section.

- [ ] **Step 3: Read prior context**

Read `book/chapters/ch02/bsc.tex` (just drafted) so §2.2 flows from §2.1.

- [ ] **Step 4: Draft the section**

Replace `book/chapters/ch02/asymmetric-channel.tex` content with `\section{The Asymmetric Binary Channel}\label{sec:asymmetric-channel}` plus comment block plus ~5 pp of prose meeting the checklist.

- [ ] **Step 5: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0.

- [ ] **Step 6: Verify cross-references**

Run: `grep -E '\\\\Cref|\\\\ref' book/chapters/ch02/asymmetric-channel.tex`
Expected: at least 3 cross-references; backward to §2.1 should resolve, others expected unresolved.

- [ ] **Step 7: Verify the biased-coin callback is present**

Run: `grep -i 'coin' book/chapters/ch02/asymmetric-channel.tex`
Expected: at least one mention. The biased-coin running-thread return is required by spec §3.1 of the Part I design.

- [ ] **Step 8: Self-review against checklist**

- [ ] **Step 9: Commit**

```bash
git add book/chapters/ch02/asymmetric-channel.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 2.2 The Asymmetric Binary Channel (~5 pp)

Five-page section introducing the Z-channel (one-sided error model;
Bloom filter as canonical instance) and the general asymmetric binary
channel with independent epsilon and omega parameters. Biased-coin
running-thread callback: a coin with different heads-bias and
tails-bias is an asymmetric binary channel. Worked numerical example
with epsilon = 0.05 and omega = 0.10. Forward references model order
(2.4) where the BSC vs asymmetric distinction will be formalized.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Draft §2.3 Composition of Channels (~5 pp)

**Files:**
- Modify: `book/chapters/ch02/channel-composition.tex`

**Spec target:** spec §5 row 2.3.

**Sources:**
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Theorem 3.7 (composition_rates), the matrix-product form of channel composition.

**Content checklist:**
- Section header `\section{Composition of Channels}\label{sec:channel-composition}`.
- Comment block at top.
- Channel composition as serial pipeline: input goes through channel $Q_1$, output goes through channel $Q_2$, joint channel is $Q_{\text{total}} = Q_2 Q_1$ (matrix product, NOT Kronecker product; the latter is for parallel queries and lives in chapter 4).
- Worked example: composing two BSCs gives a third BSC. Specifically: $Q_1$ with crossover $\fprate_1$, $Q_2$ with crossover $\fprate_2$. The composition has crossover $\fprate_{\text{total}} = \fprate_1(1 - \fprate_2) + (1 - \fprate_1)\fprate_2$.
- Verify the formula by computing $Q_2 Q_1$ explicitly for the BSC case.
- Note: this is SERIAL composition (matrix product), distinct from PARALLEL composition (Kronecker product, in chapter 4 §4.4). DO NOT conflate. (Lesson from Plan 1.)
- Forward reference to chapter 3 §3.3 (the composition theorem $\eta_{\text{total}} = 1 - \prod(1 - \eta_i)$ as the Boolean-algebra perspective on the same idea).
- Forward reference to chapter 4 §4.4 (Kronecker theorem as the parallel-queries analog).

**Notation requirements:** Use $Q$ for channel matrices. Be explicit about matrix product vs Kronecker product.

**Cross-references:**
- Backward to §2.1 (BSC) `\Cref{sec:bsc}`.
- Backward to §2.2 `\Cref{sec:asymmetric-channel}`.
- Forward to §3.3 (chapter 3 stub) `\Cref{sec:composition-theorem}`.
- Forward to §4.4 (chapter 4) `\Cref{sec:kronecker}` and `\Cref{thm:kronecker}` (resolves now since chapter 4 is drafted).

**Length target:** ~5 pp.

- [ ] **Step 1: Read the spec target**

Read spec §5 row 2.3.

- [ ] **Step 2: Read source**

Read `papers/bernoulli_sets/sections/bernoulli_model.tex` Theorem 3.7.

- [ ] **Step 3: Read prior context**

Read `book/chapters/ch02/bsc.tex` and `asymmetric-channel.tex` so §2.3 builds on them.

- [ ] **Step 4: Read chapter 4 §4.4 for Kronecker contrast**

Read `book/chapters/ch04/kronecker.tex` so §2.3's serial-vs-parallel contrast is precise.

- [ ] **Step 5: Draft the section**

Replace `book/chapters/ch02/channel-composition.tex` with `\section{Composition of Channels}\label{sec:channel-composition}` plus ~5 pp meeting checklist.

- [ ] **Step 6: Verify the BSC composition formula**

Compute by hand: with $Q = \begin{pmatrix} 1-\fprate & \fprate \\ \fprate & 1-\fprate \end{pmatrix}$, the matrix product $Q_2 Q_1$ should give a BSC with the formula above. Verify your draft's algebra.

- [ ] **Step 7: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0.

- [ ] **Step 8: Verify the serial-vs-parallel distinction is explicit**

Run: `grep -i 'kronecker\|parallel\|serial' book/chapters/ch02/channel-composition.tex`
Expected: explicit prose distinguishing matrix-product (serial) from Kronecker (parallel). The §4.4 Kronecker theorem must be cited.

- [ ] **Step 9: Self-review against checklist**

- [ ] **Step 10: Commit**

```bash
git add book/chapters/ch02/channel-composition.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 2.3 Composition of Channels (~5 pp)

Five-page section: channel composition as serial pipeline via matrix
product Q_total = Q_2 * Q_1. Worked example: composition of two BSCs
yields a third BSC with explicit formula epsilon_total =
epsilon_1 (1 - epsilon_2) + (1 - epsilon_1) epsilon_2.

Explicitly distinguishes serial composition (matrix product, this
section) from parallel queries (Kronecker product, chapter 4.4).
Forward references the composition theorem (chapter 3.3) as the
Boolean-algebra perspective on the same idea.

Sets up section 3.3 directly (the composition theorem for chained
identities-with-error).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Draft §2.4 Model Order (~7 pp)

**Files:**
- Modify: `book/chapters/ch02/model-order.tex`

**Spec target:** spec §5 row 2.4.

**Sources:**
- `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` (model order definition, partition-block view)
- `papers/CLAUDE.md` model-order-vs-DOF clarification (referenced in spec)

**Content checklist:**
- Section header `\section{Model Order}\label{sec:model-order}`.
- Comment block at top.
- Definition: model order = number of partition blocks of the input domain. Each block has its own per-block error rate.
- Connection back to §2.1, §2.2: BSC has model order 1 in the older "symmetric/asymmetric" terminology, but per the chapter-4-aligned terminology (and the spec's §5 row 2.4) the BSC is the symmetric special case of order-2 (since the input domain $\{\top, \bot\}$ has 2 partition blocks). Asymmetric channel is the general order-2 case.
- **The Boolean ceiling**: any predicate over $\{\top, \bot\}$ has model order at most 2. Rigorous statement: the input domain has cardinality 2, so the maximum number of distinct partition blocks is 2.
- Distinction between model order (partition granularity) and parameter count (constrained by independence). This is the key clarification flagged in `papers/CLAUDE.md`.
- N-ary preview: a single closing sentence noting that for input domains larger than $\{\top, \bot\}$ the same machinery generalizes to $n$-ary channels with model order up to the cardinality of the input domain. Forward reference to chapter 9 (Part III).
- DO NOT spend a section on n-ary content; this is Part I. (Spec explicitly removed the n-ary preview section.)

**Notation requirements:** Use $n$ for model order, $B_1, \ldots, B_n$ for partition blocks. Match chapter 4's conventions.

**Cross-references:**
- Backward to §2.1, §2.2, §2.3.
- Backward to §4.3 (where the partition blocks were used) `\Cref{sec:axiom-2}` (chapter 4 drafted).
- Forward to chapter 9 (Part III) for n-ary channels (single sentence reference, no full content).

**Length target:** ~7 pp.

- [ ] **Step 1: Read sources**

Read `papers/bernoulli_data_type/bernoulli_model/sections/order_and_channels.tex` (model order discussion) and `papers/CLAUDE.md` (the model-order-vs-DOF clarification).

- [ ] **Step 2: Read prior context**

Read `book/chapters/ch02/bsc.tex`, `asymmetric-channel.tex`, `channel-composition.tex`. Also re-read the relevant chapter 4 sections for the order-2 framing: `book/chapters/ch04/axiom-2.tex` (uses partition blocks), `book/chapters/ch04/kronecker.tex` (uses model order in the corollary).

- [ ] **Step 3: Draft the section**

Replace `book/chapters/ch02/model-order.tex` with `\section{Model Order}\label{sec:model-order}` plus ~7 pp meeting checklist.

- [ ] **Step 4: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0.

- [ ] **Step 5: Verify the Boolean ceiling is stated rigorously**

Run: `grep -i 'ceiling\|order 2\|order at most' book/chapters/ch02/model-order.tex`
Expected: explicit statement of the Boolean ceiling.

- [ ] **Step 6: Verify n-ary content is contained to a single sentence**

Run: `grep -i 'n-ary\|Part III\|chapter 9' book/chapters/ch02/model-order.tex`
Expected: brief mention only (one sentence). DO NOT introduce n-ary content as a section.

- [ ] **Step 7: Self-review against checklist**

- [ ] **Step 8: Commit**

```bash
git add book/chapters/ch02/model-order.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 2.4 Model Order (~7 pp)

Seven-page section formalizing model order as the number of partition
blocks of the input domain. Per the chapter-4-aligned terminology, the
BSC is the symmetric special case of order-2 (input domain cardinality
2 yields 2 partition blocks); asymmetric channel is the general order-2
case. The Boolean ceiling theorem: any predicate over the input domain
{T, F} has model order at most 2.

Distinguishes model order (partition granularity) from parameter count
(constrained by independence axioms), per the papers/CLAUDE.md
clarification.

Single closing sentence on n-ary channels as the chapter 9 trailhead;
no n-ary content in Part I.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Draft §2.5 Bibliographic Notes (~1-2 pp)

**Files:**
- Modify: `book/chapters/ch02/bibliographic-notes.tex`
- Modify: `book/references.bib` (only if new entries needed)

**Spec target:** spec §5 row 2.5.

**Sources:** None (entirely fresh). Bibtex entries reused from chapter 4's references.bib as much as possible.

**Content checklist:**
- Section header `\section*{Bibliographic Notes}` with TOC entry via `\addcontentsline{toc}{section}{Bibliographic Notes}`.
- One paragraph on Shannon (1948) as the canonical channel-coding reference. Cite Shannon directly if a bib entry is added; otherwise cite Cover & Thomas (already in references.bib).
- One paragraph on the Bernoulli papers (cite `towell-bernoulli-data-type` for the model-order treatment that backs §2.4).
- One paragraph on the model-order-vs-DOF distinction, noting it as a clarification flagged in the companion paper's documentation.
- Brief cross-reference to chapter 4 Bibliographic Notes (which already cited Cover & Thomas and the Bernoulli papers).

**Bibtex entries:**
- If Shannon (1948) entry is needed, add to `references.bib`:
  ```bibtex
  @article{shannon-1948,
    author  = {Claude E. Shannon},
    title   = {A Mathematical Theory of Communication},
    journal = {Bell System Technical Journal},
    volume  = {27},
    number  = {3},
    pages   = {379--423},
    year    = {1948}
  }
  ```
- All other citations (`cover-thomas`, `towell-bernoulli-sets`, `towell-bernoulli-data-type`) already exist from chapter 4.

**Cross-references:**
- Optional: backward to chapter 4 Bibliographic Notes via `\Cref{sec:bibliographic-notes}` if such a label exists in chapter 4. Otherwise prose reference.

**Length target:** ~1-2 pp.

- [ ] **Step 1: Read existing references.bib to see what's already available**

Run: `grep -E '@(book|article|misc)' book/references.bib`
Expected: list of existing entries. Verify `cover-thomas`, `towell-bernoulli-sets`, `towell-bernoulli-data-type` are present.

- [ ] **Step 2: Decide on Shannon citation**

If you want to cite Shannon directly, add the entry above to `references.bib`. Otherwise, reference Cover & Thomas as the modern treatment.

- [ ] **Step 3: Draft the section**

Replace `book/chapters/ch02/bibliographic-notes.tex` content with `\section*{Bibliographic Notes}` (with TOC entry) plus ~1-2 pp meeting checklist.

- [ ] **Step 4: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; biber resolves all citations cleanly.

- [ ] **Step 5: Verify all cited entries resolve**

Run: `grep "Citation.*undefined" book/book.log | head -5`
Expected: no undefined citations for chapter 2.

- [ ] **Step 6: Self-review against checklist**

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch02/bibliographic-notes.tex book/references.bib
git commit -m "$(cat <<'EOF'
book: draft chapter 2.5 Bibliographic Notes (~1-2 pp)

Brief notes section: Shannon (1948) as the canonical channel-coding
reference; the Bernoulli papers (towell-bernoulli-data-type for the
model-order treatment); the model-order-vs-DOF clarification flagged
in the companion paper documentation.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Draft 10-12 exercises with star difficulty markers

**Files:**
- Modify: `book/chapters/ch02/exercises.tex`

**Spec target:** spec §5 row 2.4 exercises subsection + §3.4 cross-cutting commitment.

**Sources:** None (entirely fresh). Difficulty marker macros from chapter 4's `book/chapters/ch04/exercises.tex` (defined locally there; can be defined locally here too).

**Content checklist:**
- Section header `\section*{Exercises}` with TOC entry.
- 11 exercises in `enumerate`, distribution 3 ★ / 5 ★★ / 3 ★★★.
- Specific exercises (per spec §5 row 2.4):
  - **★ × 3**: write Q for given $\fprate$ and $\fnrate$; compose two BSCs by hand; identify the model order of a given example.
  - **★★ × 5**: derive BSC capacity $1 - H(\fprate)$; show Bloom filter as $\fnrate = 0$ channel; prove that two-BSC composition is a BSC; characterize when an asymmetric channel reduces to a BSC; construct a model-order-2 channel from two model-order-1 channels.
  - **★★★ × 3**: prove the Boolean ceiling rigorously; show channel composition is associative but not commutative (with counterexample); explore a 3-input partition (foreshadows ch 9 without entering Part III content).

**Notation:** Use the same `\exstar`, `\exstarstar`, `\exstarstarstar` macros chapter 4 defined (or redefine locally if cleaner).

**Cross-references:**
- Backward to §2.1, §2.2, §2.3, §2.4, and to chapter 4 sections (axiom-1, axiom-2, kronecker) where appropriate.
- Some exercises reference §3.x sections (chapter 3 stubs); document expected unresolved.

**Length target:** ~1-2 pp rendered.

- [ ] **Step 1: Read chapter 4 exercises file for macro pattern**

Read `book/chapters/ch04/exercises.tex` to see how difficulty markers are defined and used.

- [ ] **Step 2: Read the spec exercise checklist**

Read spec §5 row 2.4 exercises subsection.

- [ ] **Step 3: Draft exercises**

Replace `book/chapters/ch02/exercises.tex` with `\section*{Exercises}` (with TOC entry) plus 11 exercises in `enumerate` with difficulty markers.

- [ ] **Step 4: Build and verify**

Run: `cd book && make cleanall && make`
Expected: exit code 0; exercises render with difficulty markers.

- [ ] **Step 5: Verify exercise distribution**

Run: `grep -c "exstar" book/chapters/ch02/exercises.tex`
Expected: at least 11 occurrences of difficulty markers.

Manually count: 3 ★, 5 ★★, 3 ★★★.

- [ ] **Step 6: Self-review against the spec checklist**

For each exercise, verify it maps to a section content area, the difficulty marker matches the work required, and it's solvable from chapter content alone.

- [ ] **Step 7: Commit**

```bash
git add book/chapters/ch02/exercises.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 2 exercises (11 with star difficulty markers)

11 exercises distributed as 3 star (warm-up), 5 two-star (medium),
3 three-star (challenging or extension), matching the cross-cutting
exercise discipline from the Part I spec. Difficulty markers defined
locally (matching chapter 4's pattern). Topics: Q matrix construction,
BSC composition, model order identification, BSC capacity derivation,
Bloom filter as Z-channel, model-order-2 construction, Boolean ceiling
proof, channel composition algebra, 3-input partition exploration
(foreshadows chapter 9 without leaking Part III content).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: Draft `python/notebooks/ch02-binary-channels.ipynb`

**Files:**
- Create: `python/notebooks/ch02-binary-channels.ipynb`

**Spec target:** Part I spec §5 (chapter 2 notebook commitment); §6 of master design spec (notebook discipline).

**Sources:** None. The `bernoulli` Python package from `python/` is in placeholder state; use numpy directly for the channel matrix work, with a stub `Bernoulli` import for symbolic continuity with the library.

**Content checklist:**
- Markdown cell with chapter title, section pointer, brief intro.
- Section: Build channel matrices in numpy. Define `make_bsc(epsilon)` and `make_asymmetric(epsilon, omega)` helpers. Display matrices with `print` or matplotlib.
- Section: Compose two BSCs. Verify §2.3's formula $\fprate_{\text{total}} = \fprate_1 (1 - \fprate_2) + (1 - \fprate_1) \fprate_2$ numerically. Plot the composition over $\fprate_1$ for fixed $\fprate_2$.
- Section: Plot BSC capacity $1 - H(\fprate)$ vs crossover $\fprate$. Use matplotlib.
- Section: Explore the $(\fprate, \fnrate)$ parameter space. 2D plot or heatmap showing some derived quantity.
- Section: Visualize partition blocks for inputs of size 2, 3, 4 (the size-4 case foreshadows chapter 9 without leaking Part III content; clearly labeled "preview").
- Closing markdown cell: cross-reference to the next chapter notebook (chapter 3).

**Format:** `.ipynb` JSON. Verify it parses (could use Python `json.load` to check) and opens cleanly in Jupyter.

**Length target:** ~10-15 cells, runnable end-to-end.

- [ ] **Step 1: Inspect chapter 1 notebook (if drafted) for pattern**

Run: `ls python/notebooks/`
If `ch01-noisy-bit.ipynb` exists, read it for pattern. Otherwise, drafting from scratch.

- [ ] **Step 2: Inspect the `bernoulli` Python package**

Run: `cat python/src/bernoulli/__init__.py python/src/bernoulli/core.py 2>/dev/null | head -50`
Expected: stub `Bernoulli[T]` placeholder. Use numpy primarily; import `Bernoulli` symbolically for library-continuity if desired.

- [ ] **Step 3: Write the notebook**

Create `python/notebooks/ch02-binary-channels.ipynb` as a JSON file containing the cells described above.

- [ ] **Step 4: Verify the notebook is valid JSON**

Run: `python3 -c "import json; json.load(open('python/notebooks/ch02-binary-channels.ipynb'))"`
Expected: no error.

- [ ] **Step 5: Verify the notebook is runnable (light check)**

Run: `cd python && jupyter nbconvert --to notebook --execute notebooks/ch02-binary-channels.ipynb --output /tmp/ch02-test.ipynb 2>&1 | head -20`
Expected: no execution errors. (If jupyter is not installed, skip this step and note as DONE_WITH_CONCERNS.)

- [ ] **Step 6: Self-review against checklist**

Open the notebook and confirm each section is present.

- [ ] **Step 7: Commit**

```bash
git add python/notebooks/ch02-binary-channels.ipynb
git commit -m "$(cat <<'EOF'
python: add chapter 2 notebook (binary channels)

Paired notebook for chapter 2. Sections: build channel matrices in
numpy; compose two BSCs verifying section 2.3's formula; plot BSC
capacity vs crossover; explore (epsilon, omega) parameter space;
visualize partition blocks for inputs of size 2, 3, 4 (the size-4
case is a chapter 9 preview, clearly labeled).

Uses numpy directly with a symbolic Bernoulli import for library
continuity. The bernoulli package is still in placeholder state;
no premature library design.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 9: Final chapter 2 integration verification

**Files:** none modified (verification only).

- [ ] **Step 1: Full clean rebuild**

Run: `cd book && make cleanall && make`
Expected: exit code 0; `book/book.pdf` exists.

- [ ] **Step 2: Verify chapter 2 page count is in spec range**

Inspect `book.toc` or render PDF, count chapter 2 pages.
Expected: 22-28 pages (target ~24, ±15% acceptable).

If under 22, flag as concern. If over 28, flag as concern.

- [ ] **Step 3: Verify all internal cross-references resolve**

Run: `grep -E "Reference.*undefined" book/book.log | head -20`
Expected: warnings ONLY for forward references to chapters 1, 3 sections (still stubs). NO undefined references for in-chapter-2 cross-refs (intra-§2.X labels and references to chapter 4 should all resolve).

- [ ] **Step 4: Verify all citations resolve**

Run: `grep -E "Citation.*undefined" book/book.log | head -10`
Expected: no undefined citations.

- [ ] **Step 5: Verify no banned phrases**

Run: `python3 -c "import os, glob; banned=[chr(0x2014), 'lever'+'age']; hits=[]; [hits.append((f,b)) for f in glob.glob('book/chapters/ch02/**/*.tex', recursive=True) for b in banned if b in open(f).read()]; print('CLEAN' if not hits else f'FOUND: {hits}')"`
Expected: `CLEAN`.

- [ ] **Step 6: Verify the working tree state**

Run: `git status -s`
Expected: empty (apart from possibly `M papers/CLAUDE.md` and `M book/book.pdf`).

- [ ] **Step 7: Verify the notebook is valid**

Run: `python3 -c "import json; json.load(open('python/notebooks/ch02-binary-channels.ipynb'))"`
Expected: no error.

- [ ] **Step 8: Verify the commit log shows expected Plan 2 commits**

Run: `git log --oneline 544a560..HEAD`
Expected: ~8-12 commits (one per task, plus any review-fix commits).

- [ ] **Step 9: No commit needed (verification only)**

This task creates no new commits.

---

## Self-Review

**Spec coverage check.** Each spec §5 row maps to a task:

| Spec §5 row | Task |
|---|---|
| Learning outcomes box | Task 1 (in chapter scaffolding) |
| 2.1 BSC | Task 2 |
| 2.2 Asymmetric Binary Channel | Task 3 |
| 2.3 Composition of Channels | Task 4 |
| 2.4 Model Order | Task 5 |
| 2.5 Bibliographic Notes | Task 6 |
| Exercises (10-12, marked) | Task 7 |
| Notebook | Task 8 |
| Cross-cutting commitments (notation, references) | distributed across all tasks; verified in Task 9 |
| Forward and backward references (§8 of spec) | distributed; final cross-ref verification in Task 9 |

**Placeholder scan.** No "TBD", "TODO", "implement later" in plan-level prose.

**Type and naming consistency check.**
- Section labels (`sec:bsc`, `sec:asymmetric-channel`, `sec:channel-composition`, `sec:model-order`) consistent across Tasks 2-7.
- File paths (`book/chapters/ch02/<slug>.tex`) consistent.
- Q convention (rows by input block, columns by output label) matches chapter 4 (verified in Task 2 Step 7).
- Difficulty marker macros (`\exstar`, `\exstarstar`, `\exstarstarstar`) match chapter 4's pattern.
- Notebook filename `ch02-binary-channels.ipynb` matches chapter source filename `ch02-binary-channels.tex`.

**Scope check.** Plan 2 covers chapter 2 only. Cross-references TO chapters 1 and 3 use tentative labels that will be verified in Plan 4's integration check.

**Ambiguity check.**
- "Use cleveref": `\Cref{...}` is the canonical macro.
- The Q matrix convention is potentially confusable; Task 2 explicitly verifies it against chapter 4.
- Serial vs parallel composition is the most likely conflation point (per Plan 1 lessons); Task 4 has an explicit verification step.

---

## Plan complete

The plan is saved to `docs/superpowers/plans/2026-05-04-bernoulli-textbook-ch02-binary-channels.md`.

After this plan executes, chapter 2 is a fully drafted ~24 pp deliverable plus its companion notebook. The next plan to write is **Plan 3: Chapter 3 (Boolean Algebra Under Noise)**, drafting ~28 pp including the Miller-Rabin worked walkthrough (the second of Part I's two named climaxes).
