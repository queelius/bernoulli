# Bernoulli Textbook Chapter 5: Approximate Sets and Predicates (Plan 5)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 5 of Part II (~28 pp): the predicate framing that lifts the noisy-bit atom of Part I to an approximate set, the Bloom filter constructed from scratch as the canonical instance, the predicate algebra connecting back to chapter 4's Kronecker theorem, and the one-sided vs two-sided distinction that sets up chapters 6 and 15. Chapter 5 is the opening of Part II and the foundation that chapters 6, 7, 8 build on.

**Architecture:** Replace `book/chapters/ch05-approximate-sets.tex` stub with a fully drafted chapter containing 5 sections, a learning-outcomes opener, 10-12 exercises, supporting bibliographic entries, and a paired Python notebook (`python/notebooks/ch05-approximate-sets.ipynb`) that builds a Bloom filter from scratch. Build verification at every section commit; Path A subagent-driven discipline per task.

**Tech Stack:** LaTeX (book class), alex.sty notation package, biblatex with biber backend. Python 3.11+ + numpy + matplotlib for the notebook (Bloom filter implementation in ~50 lines, empirical FPR vs theoretical $(1 - e^{-kn/m})^k$).

**Scope:** Chapter 5 only. The Part II integration check is deferred to Plan 8 Task 10. Forward references from §5.5 to chapters 6, 7, 8, 14 should use labels (those chapter labels exist as Plan 0 scaffolding stubs); the per-chapter `\Cref{ch:N}` will resolve at build time, but the section-level forward references into chapters 6-8 will be unresolved until Plans 6-8 land.

**Spec source of truth:** `docs/superpowers/specs/2026-05-17-bernoulli-textbook-part2-design.md` §3 (Part II-specific decisions), §4 (chapter outlines, focus on the chapter 5 row), §5 (reference map). Master spec is `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`.

**Base SHA:** `fb9ae8c` (HEAD at the end of Plan 4). Main-branch-direct workflow per Plans 1-4.

**Source material (papers to reformulate):**
- `papers/bernoulli_sets/sections/algebra_of_sets.tex` for §5.2 (the Bloom filter falls out of the set-membership predicate framing).
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Axioms 1-2 and the partition-block structure for §5.3 (the predicate algebra).
- `papers/bernoulli_sets/sections/adt.tex` for §5.1 framing (the abstract data type as the membership predicate).
- The Bloom-filter optimality and the `\fnrate = 0` discipline are in `papers/bernoulli-hash-function/` and `papers/bernoulli_composition/`. §5.4 cites them; do not subsume.

**Lessons inherited from Plans 1-4:**

1. **Page count discipline.** Plans 1-3 came in 30-43% over target; Plan 4 (chapter 1) came in exactly on target by holding sections to their lower-bound word counts. Chapter 5 target is ~28 pp; expect 28-36 pp realistic, aim for the lower end.
2. **Soul-voice hook (BLOCKING).** No Unicode em-dash (U+2014); use commas, colons, periods, parentheses. No "lever" + "age" as a single word. The pre-commit hook blocks violations.
3. **Notation discipline.** Use alex.sty macros directly: `\fprate` = $\varepsilon$, `\fnrate` = $\omega$, `\tprate` = $\tau$, `\tnrate` = $\eta$. For set notation, use alex.sty's `\ASet` for the approximate set $\tilde A$ (verify in Task 0); use $U$ for the universe, $A$ for the underlying true set. For the Bloom filter, use $(m, k, n)$ per classic Bloom-filter literature, with a one-paragraph notation note in §5.2 flagging that $n$ here is set size, not the chapter-1 sample size.
4. **Cross-reference discipline.** Header comment block at the top of every section file listing which labels resolve already vs forward. Use `\Cref{...}` not hardcoded section numbers.
5. **Build verification per task.** `cd book && make cleanall && make` exit 0 before every commit.
6. **Per-task review cycle (Path A).** Each section task triggers a spec-compliance reviewer + a quality reviewer + a fix subagent if substantive issues surface.

---

## File Structure

After this plan completes:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch05-approximate-sets.tex      # rewritten from stub to ~28 pp chapter scaffold
│   │   └── ch05/                          # NEW directory
│   │       ├── from-atom-to-set.tex       # §5.1 (~4 pp)
│   │       ├── bloom-from-scratch.tex     # §5.2 (~7 pp)
│   │       ├── predicate-algebra.tex      # §5.3 (~5 pp)
│   │       ├── one-sided-two-sided.tex    # §5.4 (~5 pp)
│   │       ├── what-comes-next.tex        # §5.5 (~3 pp)
│   │       ├── bibliographic-notes.tex    # §5.6 (~2 pp)
│   │       └── exercises.tex              # 10-12 exercises (~2 pp)
│   ├── preamble.tex                       # MAY be extended with set-notation macros if alex.sty doesn't cover
│   └── references.bib                     # extended with bloom-1970 (already present), survey refs
└── python/
    └── notebooks/
        └── ch05-approximate-sets.ipynb    # Bloom filter from scratch, empirical FPR, optimal k
```

The chapter follows the same subdirectory pattern as Plans 1-4. The thin chapter file `\input{}`s the section subfiles. This isolates per-section commits and keeps each subagent's working scope small.

`python/notebooks/ch05-approximate-sets.ipynb` is the chapter's paired notebook. It implements a Bloom filter in ~50 lines, populates it with $n$ items, queries it on $n$ in-set items (confirm FNR = 0) and $n$ out-of-set items (empirical FPR), and compares the empirical FPR to $(1 - e^{-kn/m})^k$. Includes the optimal-$k$ plot.

---

## Cross-Reference Map (Plan 5 closing inventory)

By the end of Plan 5, every label in this table must be defined or forward-referenced consistently:

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:approximate-sets` | `ch05-approximate-sets.tex` (already defined in Plan 0 stub) | self; §5.5 forward; chapter 6, 7, 8 backward (when those land) |
| `sec:from-atom-to-set` | `ch05/from-atom-to-set.tex` (Task 2) | (chapter 5 internal) |
| `sec:bloom-from-scratch` | `ch05/bloom-from-scratch.tex` (Task 3) | (chapter 5 internal); chapter 6, 7, 8 backward (when those land) |
| `sec:predicate-algebra` | `ch05/predicate-algebra.tex` (Task 4) | (chapter 5 internal) |
| `sec:one-sided-two-sided` | `ch05/one-sided-two-sided.tex` (Task 5) | (chapter 5 internal); chapter 15 backward (when that lands) |
| `sec:ch5-what-comes-next` | `ch05/what-comes-next.tex` (Task 6) | (chapter 5 internal) |

**Backward references chapter 5 makes** (all these labels already exist; verify in Task 0):

- `\Cref{ch:axioms-kronecker}`, `\Cref{sec:bernoulli-bool-formal}`, `\Cref{def:bernoulli-bool}`, `\Cref{sec:kronecker}`, `\Cref{thm:kronecker}`, `\Cref{sec:axiom-2}`, `\Cref{ax:block-rates-indep}` (chapter 4)
- `\Cref{ch:boolean-algebra}`, `\Cref{sec:composition-theorem}`, `\Cref{thm:composition}` (chapter 3)
- `\Cref{sec:three-faces}` (chapter 1, Face 3 for the classifier-verdict cameo)
- `\Cref{sec:quantifying-noise}` (chapter 1 §1.2 for the contingency table)

**Forward references chapter 5 makes** (labels in chapters 6-8, 14 currently exist only as Plan 0 stubs):

- `\Cref{ch:set-composition}`, `\Cref{ch:classification-measures}`, `\Cref{ch:information-bounds}`, `\Cref{ch:optimal-bernoulli-sets}`, `\Cref{ch:perfect-hash-filters}` exist as chapter-level labels in the stubs. Verify in Task 0.
- Section-level forward references into chapters 6, 7, 8 do NOT exist yet. §5.5 should use `\Cref{ch:N}` for chapter-level forward references (which resolve) and prose-only for sub-section forward references (which would not resolve).

---

## Per-Task Drafting Discipline

Every section drafting task follows the same internal structure (matching Plans 1-4):

1. **Read paper source(s)** named in the task header.
2. **Read prior context** from earlier in the chapter and the relevant Part I sections.
3. **Draft the section** to the page-length target, content checklist, and notation requirements specified in the task.
4. **Verify forward and backward references** specified in the task.
5. **Build the book** with `cd book && make cleanall && make` and confirm exit code 0.
6. **Self-review** against the section's content checklist.
7. **Commit** with the message format specified in the task.

Each task is reviewed by two subagents: a spec-compliance reviewer (Part II spec §4 chapter 5 row, plus this plan's task checklist) and a quality reviewer (cold reader as smart-undergrad / adjacent-field grad student). Findings produce a follow-up fix commit if substantive issues surface.

---

## Tasks

### Task 0: Verify scaffolding state and macro coverage

**Files:** read-only inspection plus possible `book/preamble.tex` extension.

**Purpose:** Before any drafting, verify the Part II spec's Open Action Item 1 (alex.sty macro coverage for set notation) and confirm chapter-level forward-reference labels for chapters 6, 7, 8, 14, 15 exist.

- [ ] **Step 1: Check alex.sty for set-notation macros**

```bash
grep -nE "ASet|aSet|approxSet|\\\\Set\\b|tildeSet" book/alex.sty
```

Document what exists. Expected: `\ASet` (approximate set, $\tilde A$), `\Set` or `\BSet` (true set). If absent, plan to extend `book/preamble.tex` with `\providecommand` (do NOT modify alex.sty).

- [ ] **Step 2: Verify chapter-level labels for forward references**

```bash
grep -rn "\\\\label{ch:set-composition}\|\\\\label{ch:classification-measures}\|\\\\label{ch:information-bounds}\|\\\\label{ch:optimal-bernoulli-sets}\|\\\\label{ch:perfect-hash-filters}\|\\\\label{ch:approximate-sets}" book/chapters/
```

Expected: one match per label, each in the corresponding `chXX-*.tex` stub file. Document.

- [ ] **Step 3: Extend `book/preamble.tex` if needed**

If `\ASet` (or equivalent) is missing from alex.sty, add a `\providecommand` block to `book/preamble.tex` matching the existing style (the `\Bernoulli` and `\BoolType` block at the end). Example:

```latex
% Approximate-set macros for the textbook chapter 5 onward.
\providecommand{\ASet}{\tilde{A}}
\providecommand{\Universe}{U}
```

Use whatever names match what alex.sty already provides where possible. Build to verify.

- [ ] **Step 4: Build the book to confirm baseline is clean**

```bash
cd book && make cleanall && make
```

Expected: exit 0, same warnings as the Plan 4 closing build (the one expected `ch:composition` Part II forward reference; nothing new).

- [ ] **Step 5: Commit IF preamble was modified; otherwise skip**

If `book/preamble.tex` was extended:

```bash
git add book/preamble.tex
git commit -m "$(cat <<'EOF'
book: extend preamble with set-notation macros for Part II

Add \providecommand blocks for the approximate-set notation that
chapters 5 onward will use. alex.sty is shared with the papers and
not modified; book-specific extensions live in preamble.tex.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

If no preamble changes were needed, skip the commit and proceed to Task 1.

---

### Task 1: Read source material and write chapter scaffolding

**Files:**
- Modify: `book/chapters/ch05-approximate-sets.tex` (currently a 4-line stub)

**Source reading:**
- `papers/bernoulli_sets/sections/algebra_of_sets.tex` (the set-membership predicate framing and the Bloom filter derivation)
- `papers/bernoulli_sets/sections/bernoulli_model.tex` (axioms applied to predicate evaluation across the universe)
- `papers/bernoulli_sets/sections/adt.tex` (the abstract data type viewpoint, for §5.1)
- `docs/superpowers/specs/2026-05-17-bernoulli-textbook-part2-design.md` §3, §4 chapter 5 row, §5 reference map.

- [ ] **Step 1: Read all sources end-to-end**

- [ ] **Step 2: Replace the stub with chapter scaffolding**

Open `book/chapters/ch05-approximate-sets.tex` and replace its contents with:

```latex
\chapter{Approximate Sets and Predicates}
\label{ch:approximate-sets}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Define an approximate set as a function from a universe $U$ to
    the noisy-bit atom of Part~I, and recognize the membership
    predicate as a $\Bernoulli{\BoolType}$ instance per element.
  \item Construct a Bloom filter from scratch and compute its empirical
    and theoretical false-positive rates.
  \item State the one-sided vs two-sided distinction for approximate
    sets and identify when each is appropriate.
\end{itemize}
\end{quote}

% Section 5.1
\input{chapters/ch05/from-atom-to-set}

% Section 5.2
\input{chapters/ch05/bloom-from-scratch}

% Section 5.3
\input{chapters/ch05/predicate-algebra}

% Section 5.4
\input{chapters/ch05/one-sided-two-sided}

% Section 5.5
\input{chapters/ch05/what-comes-next}

% Section 5.6
\input{chapters/ch05/bibliographic-notes}

% Exercises
\input{chapters/ch05/exercises}
```

- [ ] **Step 3: Create the `book/chapters/ch05/` subdirectory**

```bash
mkdir -p book/chapters/ch05
```

- [ ] **Step 4: Create 7 placeholder section files**

For each of `from-atom-to-set.tex`, `bloom-from-scratch.tex`, `predicate-algebra.tex`, `one-sided-two-sided.tex`, `what-comes-next.tex`, `bibliographic-notes.tex`, `exercises.tex`, write a one-line placeholder:

```latex
% Placeholder. Drafted in Plan 5 Task N.
```

Substitute the actual task number: 2, 3, 4, 5, 6, 7, 8.

- [ ] **Step 5: Build to confirm scaffolding is clean**

```bash
cd book && make cleanall && make
```

Expected: exit 0. Chapter 5 in the table of contents now shows the learning outcomes box only (placeholders are empty).

- [ ] **Step 6: Commit**

```bash
git add book/chapters/ch05-approximate-sets.tex book/chapters/ch05/
git commit -m "$(cat <<'EOF'
book: scaffold chapter 5 (approximate sets and predicates) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener, seven section subfile inputs (from-atom-to-set,
bloom-from-scratch, predicate-algebra, one-sided-two-sided,
what-comes-next, bibliographic-notes, exercises), and matching empty
placeholders. Section drafts land in subsequent Plan 5 tasks.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: §5.1 From Atom to Set (~4 pp)

**Files:**
- Modify: `book/chapters/ch05/from-atom-to-set.tex`

**Source reading:**
- `papers/bernoulli_sets/sections/adt.tex` (the abstract data type viewpoint)
- `book/chapters/ch04/bernoulli-bool-formal.tex` (§4.5; the formal $\Bernoulli{\BoolType}$ that §5.1 lifts)
- `book/chapters/ch01/why-atom.tex` (§1.5; the "atom" framing $\Bernoulli{T}$ lifts beyond $\BoolType$)

**Purpose:** Lift the noisy-bit atom of Part I to an approximate set. An approximate set $\tilde A$ is a function $U \to \Bernoulli{\BoolType}$; each evaluation $\tilde A(x)$ is a noisy-bit instance. This is the central abstraction of Part II and the bridge from Part I.

**Content checklist (5 items):**

1. **Opening:** recall §1.5's "Part II: sets out of atoms" preview. The atom is the noisy bit; the natural next object is a noisy bit per universe element. That object is an approximate set.

2. **The predicate framing:** define $\tilde A : U \to \{\top, \bot\}$ where each evaluation $\tilde A(x)$ is a $\Bernoulli{\BoolType}$ instance with per-element error rates. The membership predicate IS a noisy bit. The notation: $A \subseteq U$ is the true set, $\tilde A$ is its approximate representation, $\tilde A(x) = \top$ means "the structure reports $x \in A$." Make this very concrete with two short paragraphs.

3. **The two error rates as set properties:** define $\fprate$ for an approximate set as $\Pr\{\tilde A(x) = \top \mid x \notin A\}$ (false positive: reports membership when there is none) and $\fnrate$ as $\Pr\{\tilde A(x) = \bot \mid x \in A\}$ (false negative: misses true membership). Per-element rates aggregate (under Axiom 2) to per-set rates.

4. **The block structure:** the input domain $U$ splits into two blocks under the predicate framing: $B_1 = A$ (in-set elements) and $B_2 = U \setminus A$ (out-of-set elements). Each block has its own conditional behavior. This connects directly to chapter 4 §4.4's Kronecker theorem: $n$ queries against $\tilde A$ factor as a Kronecker product of per-block channels. Forward-reference §5.3 for the detailed predicate algebra.

5. **Signpost:** §5.2 makes this concrete with the Bloom filter, the canonical approximate-set instance.

**Labels:** `\section{From Atom to Set}` with `\label{sec:from-atom-to-set}`.

**Notation discipline:**
- Use `\ASet` (or whatever macro Task 0 confirmed for $\tilde A$); $A$ for the true set; $U$ for the universe.
- Use `\fprate`, `\fnrate` for the error rates.
- Use $\Bernoulli{\BoolType}$ from `preamble.tex`.
- Do NOT introduce the Bloom filter yet; that is §5.2's job.
- Do NOT introduce the channel matrix $Q$ for the predicate (the matrix viewpoint can wait for §5.3).

**Target length:** ~4 pp (900-1200 prose words).

**Header cross-reference comment block** matching Plans 1-4 conventions; list labels defined, forward, and resolved.

- [ ] **Step 1: Read source material**
- [ ] **Step 2: Draft `from-atom-to-set.tex` to the content checklist**
- [ ] **Step 3: Build and verify (`cd book && make cleanall && make`, exit 0)**
- [ ] **Step 4: Commit**

```
book: draft chapter 5.1 From Atom to Set (~4 pp)

The predicate framing: an approximate set is a function from the
universe to the noisy-bit atom of Part I. Each evaluation is a
Bernoulli[bool] instance with per-element error rates that aggregate
under Axiom 2 to per-set rates. The block structure (in-set vs
out-of-set) connects directly to chapter 4 §4.4's Kronecker theorem.
Sets up the Bloom filter as the canonical instance in §5.2.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

- [ ] **Step 5: Spec-compliance review (subagent)**: verify the 5 checklist items + length + labels + notation discipline.
- [ ] **Step 6: Quality review (subagent)**: read cold; does the predicate framing land? Does the §5.2 signpost build expectation?
- [ ] **Step 7: Address review findings (fix subagent if substantive issues)**

---

### Task 3: §5.2 The Bloom Filter From Scratch (~7 pp)

**Files:**
- Modify: `book/chapters/ch05/bloom-from-scratch.tex`

**Source reading:**
- `papers/bernoulli_sets/sections/algebra_of_sets.tex` (the Bloom filter as a set-membership predicate)
- Optionally: `papers/bernoulli-hash-function/` (cite for optimality; do not subsume the full derivation)

**Purpose:** Construct the Bloom filter from scratch as the canonical instance of an approximate set. The Bloom filter has $\fnrate = 0$ (one-sided) and a computable $\fprate$; the derivation of the FPR formula and the optimal-$k$ result is the chapter's first major payoff.

**Content checklist (7 items):**

1. **Construction:** $m$ bits, all initially $0$. $k$ independent hash functions $h_1, \ldots, h_k : U \to \{1, \ldots, m\}$. Insert $x$: set bits $h_1(x), \ldots, h_k(x)$ to $1$. Query $x$: return $\top$ iff all $k$ bits $h_1(x), \ldots, h_k(x)$ are $1$. Pseudocode in algorithm2e.

2. **Why $\fnrate = 0$:** if $x$ was inserted, all $k$ bits ARE set; therefore the query returns $\top$. The Bloom filter never misses an inserted item. This is the one-sided property §5.4 will name.

3. **FPR derivation (the headline derivation):**
   - After inserting $n$ items, the probability a given bit is still $0$ is $(1 - 1/m)^{kn} \approx e^{-kn/m}$.
   - The probability the bit is $1$ is $1 - e^{-kn/m}$.
   - A query for $x \notin A$ returns $\top$ iff all $k$ queried bits are $1$.
   - Under the (standard, simplifying) assumption that the $k$ bit-checks are independent: $\fprate \approx (1 - e^{-kn/m})^k$.
   - Flag the independence assumption honestly: the $k$ bit-checks share the bitmap and are not strictly independent; the approximation is excellent for sparse filters and the deviation is well-studied.

4. **Optimal $k$:** minimize $(1 - e^{-kn/m})^k$ over $k$ for fixed $m, n$. The optimum is $k^* = (m/n) \ln 2$, giving $\fprate \approx (1/2)^{k^*} = 2^{-(m/n) \ln 2}$. Show the derivation; one paragraph of calculus.

5. **Notation note:** the variables $(m, k, n)$ are the standard Bloom-filter notation. Note that $n$ here is the size of the set being represented, NOT chapter 1's sample size. Use $n_{\text{items}}$ if cross-chapter ambiguity matters.

6. **Worked example:** for $m = 10000$, $n = 1000$, $k = 7$, compute $\fprate$ from the formula. Compare to the optimal $k$ and the resulting $\fprate$. (Optimal $k = (10000/1000) \ln 2 \approx 6.93$, rounded to $7$; optimal $\fprate \approx (1/2)^7 \approx 0.0078$.)

7. **Signpost:** §5.3 develops the predicate algebra in general (the Bloom filter is one instance); §5.4 contrasts one-sided and two-sided sets.

**Labels:** `\section{The Bloom Filter From Scratch}` with `\label{sec:bloom-from-scratch}`. Definition: `\label{def:bloom-filter}`. Theorem (optimal $k$): `\label{thm:bloom-optimal-k}` or similar.

**Notation discipline:**
- $(m, k, n)$ Bloom filter convention. Notation note in the text.
- $h_i : U \to \{1, \ldots, m\}$ for the hash functions.
- `\fprate`, `\fnrate` for the rates.
- Use `algorithm2e` for the insert/query pseudocode (alex.sty loads it; chapter 3 §3.4's Miller-Rabin pseudocode is precedent for style).

**Target length:** ~7 pp (1500-1800 prose words; the headline derivation is the longest single block in chapter 5).

- [ ] **Step 1: Read source material**
- [ ] **Step 2: Draft `bloom-from-scratch.tex`**
- [ ] **Step 3: Build and verify**
- [ ] **Step 4: Commit**

```
book: draft chapter 5.2 The Bloom Filter From Scratch (~7 pp)

The canonical approximate-set instance. Construction, the FNR-zero
property, the FPR derivation (approximately (1-e^{-kn/m})^k), and the
optimal k = (m/n) ln 2 result. Worked example for m=10000, n=1000.
Notation note flags the (m, k, n) variable reuse against chapter 1's
sample-size n.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

- [ ] **Step 5-7: spec review + quality review + fix loop**

---

### Task 4: §5.3 The Predicate Algebra (~5 pp)

**Files:**
- Modify: `book/chapters/ch05/predicate-algebra.tex`

**Source reading:**
- `papers/bernoulli_sets/sections/bernoulli_model.tex` (axioms applied to predicate evaluation)
- `book/chapters/ch04/bernoulli-bool-formal.tex` and `book/chapters/ch04/kronecker.tex` (the Kronecker theorem the predicate algebra invokes)

**Purpose:** Develop the predicate algebra in general. An approximate set's membership predicate is a $\Bernoulli{\BoolType}$ instance per element; under Axiom 2 the per-block rates are stable, and under chapter 4's Kronecker theorem the joint distribution over $n$ queries factors. This is where the chapter 5 abstraction earns its connection to chapter 4's formal machinery.

**Content checklist (5 items):**

1. **The predicate as $\Bernoulli{\BoolType}$:** restate $\tilde A(x)$ as a $\Bernoulli{\BoolType}$ instance with channel matrix
$$Q_x = \begin{pmatrix} 1 - \fnrate(x) & \fnrate(x) \\ \fprate(x) & 1 - \fprate(x) \end{pmatrix}$$
where $\fprate(x)$ and $\fnrate(x)$ may depend on $x$ in general. Two paragraphs.

2. **Axiom 2 gives block-stability:** under Axiom 2, $\fprate(x) = \fprate$ for all $x \in U \setminus A$ and $\fnrate(x) = \fnrate$ for all $x \in A$. Per-element rates collapse to per-block rates. One paragraph.

3. **The block partition $\{A, U \setminus A\}$:** the input domain $U$ splits into in-set and out-of-set blocks. Each block has its own channel matrix entry (row of $Q$). This is exactly the Kronecker setup of chapter 4 §4.4 with model order $2$.

4. **Joint distribution over $n$ queries factors via Kronecker:** by `\Cref{thm:kronecker}` (chapter 4), the joint behavior of $n$ independent queries on $\tilde A$ factors as a Kronecker product of per-block channels. The corollary: an approximate set's full probabilistic description needs $2$ parameters ($\fprate, \fnrate$), not $|U|$ parameters, regardless of $|U|$.

5. **Worked example:** for $|U| = 10$, $|A| = 3$, $\fprate = 0.1$, $\fnrate = 0.05$, compute the joint probability of a specific query pattern (e.g., $\tilde A$ reports membership for $4$ specific elements). Show how it factors. Half a page.

**Labels:** `\section{The Predicate Algebra}` with `\label{sec:predicate-algebra}`. Proposition (block-stability under Axiom 2): `\label{prop:block-stability}`. Corollary (Kronecker factorization for approximate sets): `\label{cor:kronecker-set}`.

**Notation discipline:**
- $Q$ for the channel matrix; chapter 2 introduced this and §5.3 reuses it freely.
- $\fprate(x), \fnrate(x)$ for per-element rates; $\fprate, \fnrate$ for per-block rates (after Axiom 2).
- $\otimes$ for the Kronecker product (chapter 4 introduced; reuse).
- alex.sty's `\Given` for conditional probability bars.

**Target length:** ~5 pp (1100-1400 prose words).

- [ ] **Steps 1-7** (standard task pattern)

Commit message:
```
book: draft chapter 5.3 The Predicate Algebra (~5 pp)

The predicate \tilde{A}(x) as a Bernoulli[bool] instance per element,
with channel matrix Q_x. Axiom 2 collapses per-element rates to
per-block rates over the partition {A, U \setminus A}. The chapter 4
Kronecker theorem then factors the joint distribution over n queries.
Corollary: an approximate set's full probabilistic description needs
only 2 parameters, regardless of universe size.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 5: §5.4 One-Sided vs Two-Sided Approximate Sets (~5 pp)

**Files:**
- Modify: `book/chapters/ch05/one-sided-two-sided.tex`

**Source reading:**
- `papers/bernoulli_composition/sections/set_theory.tex` (the perfect filter line, for context)
- `book/chapters/ch01/three-faces.tex` and `book/chapters/ch02/asymmetric-channel.tex` (the one-sided / two-sided distinction at the noisy-bit level)

**Purpose:** Define the one-sided vs two-sided distinction for approximate sets, and connect it to the perfect-filter line that chapters 6 §6.4 and 15 explore.

**Content checklist (5 items):**

1. **Definition:** a one-sided approximate set has $\fnrate = 0$ or $\fprate = 0$. The Bloom filter has $\fnrate = 0$. The "perfect filter" of chapter 15 has $\fprate = 0$ on a designated set (with $\fprate > 0$ otherwise). Two-sided sets have both rates positive.

2. **Why $\fnrate = 0$ is the natural one-sided default for membership data structures:** insertion-only data structures naturally lose information about which bits "belong" to which element, so false positives are unavoidable; but a bit-set query that returns $\top$ for an inserted item never miss. This is structural, not designed.

3. **The trade-off:** one-sided buys safety (the answer in one direction is exact); two-sided buys space (general approximate sets can be smaller; cardinality estimators and approximate counters are two-sided). Worked comparison: a one-sided $\fprate = 0.01$ Bloom filter at $m = 10n$ bits, vs a hypothetical two-sided set at $m = 5n$ bits with $\fprate = \fnrate = 0.05$. Same expected error count, half the space.

4. **The perfect filter line:** one-sided approximate sets occupy a one-dimensional surface in the $(\fprate, \fnrate)$ plane (the lines $\fnrate = 0$ and $\fprate = 0$). Operations like union and intersection (chapter 6) preserve one-sidedness in one direction but not the other. Forward-reference chapter 6 §6.4 and chapter 15.

5. **Signpost:** §5.5 surveys the rest of the chapter trajectory.

**Labels:** `\section{One-Sided vs Two-Sided Approximate Sets}` with `\label{sec:one-sided-two-sided}`. Definition: `\label{def:one-sided}`.

**Notation discipline:** standard alex.sty macros; introduce no new notation.

**Target length:** ~5 pp (1100-1400 prose words).

- [ ] **Steps 1-7** (standard task pattern)

Commit message:
```
book: draft chapter 5.4 One-Sided vs Two-Sided Approximate Sets (~5 pp)

Define the one-sided property (FNR = 0 or FPR = 0). The Bloom filter
is one-sided in FNR; chapter 15's perfect hash filter is one-sided in
FPR on a designated set. Trade-off: one-sidedness buys safety;
two-sided sets can be smaller. Forward-reference the perfect-filter
line in chapter 6 §6.4 and chapter 15's constructive realization.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 6: §5.5 What Comes Next (~3 pp)

**Files:**
- Modify: `book/chapters/ch05/what-comes-next.tex`

**Source reading:**
- The Part II spec §4 (chapters 6, 7, 8 outlines)
- Master spec §5 (chapters 14, 15 outlines, for the forward bridges)

**Purpose:** Preview the rest of Part II and the chapter 14 / 15 forward references. Mirror chapter 1 §1.5's role but at the start of Part II rather than Part I.

**Content checklist (5 items):**

1. **Chapter 6 (Composition of Sets):** the algebra of $\cup, \cap, \setminus, \complement$ for approximate sets. Error-rate propagation from chapter 3 §3.3's composition theorem. The perfect-filter line as a closed subalgebra.

2. **Chapter 7 (Classification Measures):** PPV, NPV, recall, F1 for approximate sets. Retires the chapter 1 §1.4 deferral on proper confidence intervals. Bloom filter PPV under varying workload prevalences.

3. **Chapter 8 (Information-Theoretic Bounds):** the entropy floor for approximate-set space cost. The standard Bloom filter falls $44\%$ short of the floor; chapter 14's BHF closes the gap.

4. **Chapter 14 forward look (one paragraph):** the Bernoulli Hash Function achieves the entropy lower bound. The "$44\%$ overhead" is the right kind of unfinished business; chapter 14 finishes it.

5. **Closing:** §5.6 names the antecedents; the next four chapters develop the algebra previewed here.

**Labels:** `\section{What Comes Next}` with `\label{sec:ch5-what-comes-next}`.

**Notation discipline:** use `\Cref{ch:N}` for chapter-level forward references (which resolve via Plan 0 stubs); use prose for section-level references that do not yet exist.

**Target length:** ~3 pp (700-900 prose words). Keep tight; this is the Part II analog of §1.5's signpost.

- [ ] **Steps 1-7** (standard task pattern)

Commit message:
```
book: draft chapter 5.5 What Comes Next (~3 pp)

Preview chapters 6 (set composition), 7 (classification measures, with
chapter 1 §1.4 deferral retired), 8 (information-theoretic bounds),
and 14 (the BHF that closes the 44% gap). Short paragraphs per
chapter, structured like chapter 1 §1.5's trajectory preview but at
the start of Part II rather than Part I.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 7: §5.6 Bibliographic Notes (~2 pp)

**Files:**
- Modify: `book/chapters/ch05/bibliographic-notes.tex`
- Possibly modify: `book/references.bib` (new entries)

**Source reading:**
- `book/chapters/ch01/bibliographic-notes.tex`, `ch02/bibliographic-notes.tex`, `ch03/bibliographic-notes.tex`, `ch04/bibliographic-notes.tex` for style and depth precedent.
- `book/references.bib` to confirm existing entries (`bloomfilter`, `mitzenmacher-upfal`, `towell-bernoulli-sets`).

**Purpose:** Place chapter 5's content in historical and disciplinary context.

**Content (4-5 paragraphs):**

1. **Bloom (1970) and the Bloom filter:** the original paper, the space-time trade-off, the broader hash-coding context. `\cite{bloomfilter}`.

2. **Survey context:** Mitzenmacher and Upfal §5 covers approximate-set data structures more broadly. `\cite{mitzenmacher-upfal}`. Optionally: Broder and Mitzenmacher's "Network Applications of Bloom Filters" survey (add `broder-mitzenmacher-2004` to the bib if cited).

3. **The set-as-predicate viewpoint:** the framing of an approximate set as a function $U \to \Bernoulli{\BoolType}$ is the contribution of the Bernoulli papers (`towell-bernoulli-sets`); pre-existing literature treated approximate sets as data structures with error rates, not as random functions. `\cite{towell-bernoulli-sets}`.

4. **One-sided / perfect filters lineage:** the perfect filter as $\fprate = 0$ on a designated set has its constructive realization in chapter 15 (the BPHF); the lineage runs through Carter-Wegman perfect hashing. Optional bib entry `carter-wegman-1979` if cited.

5. **Forward bridge:** the chapter 14 BHF and chapter 15 BPHF are taken up in their own bibliographic notes; the foundational paper for both is `bernoulli-hash-function` in the `bernoulli/papers/` tree.

**Possible new bib entries (add ONLY if cited):**

```bibtex
@article{broder-mitzenmacher-2004,
  author = {Andrei Broder and Michael Mitzenmacher},
  title = {Network Applications of {Bloom} Filters: A Survey},
  journal = {Internet Mathematics},
  volume = {1},
  number = {4},
  pages = {485--509},
  year = {2004}
}

@inproceedings{carter-wegman-1979,
  author = {J. Lawrence Carter and Mark N. Wegman},
  title = {Universal Classes of Hash Functions},
  booktitle = {STOC},
  pages = {106--112},
  year = {1979}
}
```

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline{toc}{section}{Bibliographic Notes}` matching ch02/ch03/ch04 precedent.

**Target length:** ~2 pp (400-600 prose words).

- [ ] **Steps 1-7** (combined spec + quality review acceptable for low-risk bib notes, mirroring Task 7 of Plan 4)

Commit message:
```
book: draft chapter 5.6 Bibliographic Notes (~2 pp); extend bib if needed

Attribute the Bloom filter to Bloom (1970), survey context to
Mitzenmacher-Upfal, the set-as-predicate viewpoint to the
towell-bernoulli-sets paper, and the perfect-filter lineage to
Carter-Wegman. Forward bridges to chapter 14 (BHF) and chapter 15
(BPHF) point at the bernoulli-hash-function paper.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 8: Chapter 5 Exercises (10-12)

**Files:**
- Modify: `book/chapters/ch05/exercises.tex`

**Source reading:**
- `book/chapters/ch01/exercises.tex`, `ch02/exercises.tex`, `ch03/exercises.tex`, `ch04/exercises.tex` for precedent.

**Purpose:** 10-12 exercises with `\providecommand{\exstar}{...}` block, 3 warm-up / 5 medium / 3 challenging distribution, mix of conceptual / computational / notebook-tied.

**Exercise set (11 exercises):**

**Warm-up (★ × 3):**

1. **Predicate-to-rates:** given a small approximate set ($U = \{1, \ldots, 10\}$, $A = \{2, 5, 7\}$) and a record of $\tilde A(x)$ outputs for each $x \in U$, compute $\fprate$ and $\fnrate$.

2. **Bloom filter parameters:** given $m = 8000$, $n = 1000$, $k = 5$, compute $\fprate$ from the formula. Then find the optimal $k$ for the same $m, n$ and compute the resulting $\fprate$.

3. **One-sided check:** for each of (a) a Bloom filter, (b) an exact set membership test (no noise), (c) a cardinality estimator (HyperLogLog), state whether it is one-sided in $\fnrate$, one-sided in $\fprate$, two-sided, or exact. Brief justification.

**Medium (★★ × 5):**

4. **Notebook-tied Bloom filter empirics:** use `python/notebooks/ch05-approximate-sets.ipynb` to build a Bloom filter with $m = 10000$, $n = 1000$, $k$ varying from $1$ to $15$. Plot empirical $\fprate$ vs theoretical $(1 - e^{-kn/m})^k$. Identify the empirical optimal $k$.

5. **Optimal-$k$ derivation:** derive $k^* = (m/n) \ln 2$ by taking $\partial/\partial k$ of $\log[(1 - e^{-kn/m})^k]$ and setting to zero. Verify the result for $m = 10000, n = 1000$.

6. **Predicate algebra exercise:** for an approximate set with $|U| = 6$, $|A| = 2$, $\fprate = 0.1$, $\fnrate = 0.05$, write the channel matrix $Q$ and use the Kronecker theorem (`\Cref{thm:kronecker}`) to compute the joint probability that $\tilde A$ reports membership for exactly $3$ specific out-of-set elements.

7. **Bit-check independence assumption:** §5.2's FPR derivation assumes the $k$ bit-checks are independent. Construct a small counter-example ($m = 4$, $n = 1$, $k = 2$) where the assumption is visibly false and compare the exact FPR to the formula.

8. **Two-sided vs one-sided space trade-off:** for $n = 1000$ and target expected error count of $10$ per workload of size $1000$, compare the space cost (bits) of (a) a one-sided Bloom filter with $\fprate = 0.01$ and (b) a hypothetical two-sided set with $\fprate = \fnrate = 0.005$. Make assumptions explicit.

**Challenging (★★★ × 3):**

9. **Counting-Bloom-filter sketch:** sketch how to extend a Bloom filter to support deletions (counting Bloom filter). Derive its $\fnrate$ (now non-zero in general) and show the trade-off vs the standard Bloom filter's space. (No formal proofs; argue from the construction.)

10. **Block-stability under non-uniform priors:** the predicate algebra of §5.3 assumes Axiom 2 gives block-stable rates. Construct an example where the rates depend on the input element's prior probability (e.g., a learned classifier with class-conditional accuracy). Argue informally why this violates Axiom 2 in spirit even if the underlying construction is technically deterministic.

11. **Forward to chapter 6:** the union of two Bloom filters by bit-OR has the formula $\fprate_{\text{total}} = 1 - (1 - \fprate_1)(1 - \fprate_2)$ (this is chapter 6 §6.1 material). Derive it from chapter 3 §3.3's composition theorem. Then describe one situation where the formula breaks (e.g., the two filters share hash functions over the same universe, so their FPR events are correlated).

**Labels:** `\label{ex:ch5-N}` for $N = 1, \ldots, 11$. `\providecommand` block matching ch02/ch03/ch04 style.

**Target length:** ~2 pp (~700-900 prose words for exercise prompts).

- [ ] **Steps 1-7** (standard task pattern with spec + quality reviewers; exercises are higher-risk than bib notes, two reviewers warranted)

Commit message:
```
book: draft chapter 5 exercises (11 with star difficulty markers)

3 warm-ups (predicate-to-rates, Bloom-filter parameters, one-sided
check), 5 medium (notebook empirics, optimal-k derivation, predicate
algebra with Kronecker, bit-check independence counter-example,
two-sided space trade-off), 3 challenging (counting Bloom filter
sketch, block-stability violation, forward derivation of union FPR
via composition theorem).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 9: Chapter 5 Notebook (`ch05-approximate-sets.ipynb`)

**Files:**
- Create: `python/notebooks/ch05-approximate-sets.ipynb`

**Source reading:**
- `python/notebooks/ch01-noisy-bit.ipynb`, `ch02-binary-channels.ipynb`, `ch03-boolean-algebra-noise.ipynb` for structure and style precedent
- `python/notebooks/README.md`

**Purpose:** The substantive paired notebook for chapter 5. Builds a Bloom filter from scratch in Python, verifies $\fnrate = 0$ empirically, plots empirical $\fprate$ vs the theoretical $(1 - e^{-kn/m})^k$, and demonstrates the optimal $k$.

**Content checklist (~15-18 cells):**

1. **Title cell** (markdown): "Chapter 5: Approximate Sets and Predicates. Companion notebook."
2. **Setup** (code): import numpy, matplotlib; seeded RNG following ch01/ch02/ch03 convention.
3. **Bloom filter class** (code): implement `class BloomFilter` with `__init__(m, k)`, `add(x)`, `__contains__(x)`. Use a simple hash family (e.g., `hashlib.sha256(x).digest()` split into $k$ pieces, mod $m$).
4. **FNR-zero verification** (code): build a Bloom filter with $m = 10000, k = 7$, insert $n = 1000$ items, query each inserted item, confirm all return $\top$ (FNR = 0).
5. **Empirical FPR** (code): query $10000$ random out-of-set items, count $\top$ responses. Compare to theoretical $(1 - e^{-kn/m})^k$.
6. **FPR vs $k$ sweep** (code): for $k \in \{1, 2, \ldots, 15\}$ at fixed $m = 10000, n = 1000$, compute empirical and theoretical FPR. Plot both. Identify the empirical optimal $k$.
7. **Optimal $k$ verification** (code): compute $k^* = (m/n) \ln 2$ for several $(m, n)$ pairs; verify the resulting FPR is near $(1/2)^{k^*}$.
8. **Discussion cell** (markdown): the bit-check independence assumption; when it breaks; the practical impact.
9. **Open question cell** (markdown): what happens to FPR when we run out of bits ($n \gg m$)? Forward-reference chapter 8 (entropy floor) and chapter 14 (BHF).

**Numerical sanity targets:**
- FNR-zero check: all $1000$ inserted items return $\top$ (no exceptions).
- Empirical FPR at $m = 10000, n = 1000, k = 7$: within $\pm 0.005$ of theoretical $\approx 0.0082$.
- Optimal $k$ identification: empirical curve minimum at $k \in \{6, 7, 8\}$ for $m = 10000, n = 1000$.

**Run-to-completion:** notebook MUST execute end-to-end from a fresh kernel.

- [ ] **Step 1: Read precedent notebooks**
- [ ] **Step 2: Draft the notebook (valid nbformat-4 JSON)**
- [ ] **Step 3: Execute end-to-end**

```bash
cd python && uv run jupyter nbconvert --to notebook --execute notebooks/ch05-approximate-sets.ipynb --output ch05-approximate-sets.ipynb 2>&1 | tail -20
```

Exit code 0; populated outputs.

- [ ] **Step 4: Verify numerical sanity (spot-check outputs)**
- [ ] **Step 5: Commit**

```
python: add chapter 5 notebook (approximate sets, Bloom filter from scratch)

Bloom filter class with insert and query, FNR-zero verification on
1000 inserted items, empirical FPR vs theoretical (1 - e^{-kn/m})^k
across k = 1..15 at fixed m, n. Optimal-k verification across several
(m, n) pairs. Open question forward-references chapter 8 (entropy
floor) and chapter 14 (BHF).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

- [ ] **Steps 6-7: spec + quality review subagents, fix loop if substantive issues**

---

## Self-Review

Spec coverage:
- Part II spec §4 chapter 5 row: each of §5.1, §5.2, §5.3, §5.4, §5.5, §5.6 has its own task (Tasks 2-7).
- Part II spec §3.1 (predicate-first bridge): §5.1's content checklist explicitly delivers it.
- Part II spec §3.2 (Bloom filter as Part II running example): §5.2 introduces it; §5.3, §5.4, §5.5 reference it.
- Part II spec §3.5 (notebook discipline): Task 9 substantive notebook with Bloom filter.
- Part II spec §5 reference map: each chapter-5-touching row mapped to a task; chapter-level forward refs to chapters 6, 7, 8, 14 use existing Plan 0 stub labels.
- Part II spec §8 Open Action Item 1 (alex.sty macro coverage): Task 0.
- Part II spec §8 Open Action Item 2 (Bloom filter notation conflict): §5.2 notation note in Task 3.
- Master spec exercise discipline (10-12, 3/5/3): Task 8.

Placeholder scan: none. Every step contains the actual content an engineer needs.

Type and label consistency: labels match across this plan (`sec:from-atom-to-set`, `sec:bloom-from-scratch`, `sec:predicate-algebra`, `sec:one-sided-two-sided`, `sec:ch5-what-comes-next` appear consistently in Tasks 2-6 and in the Cross-Reference Map table). `ch:approximate-sets` is already defined in the Plan 0 stub.
