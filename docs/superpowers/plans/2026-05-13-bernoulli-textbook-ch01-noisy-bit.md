# Bernoulli Textbook Chapter 1: The Noisy Bit + Part I Integration (Plan 4)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 1 of Part I (~25 pp): the multi-framed opening that introduces the three running threads (BSC, biased coin, classifier verdict), names "the abstract noisy bit" as the atomic Bernoulli object, walks the reader through informal FPR/FNR quantification and sampling, and previews the trajectory through chapters 2-4. Then run the Part I integration check that verifies every forward/backward reference across chapters 1-4 resolves under the full book build.

**Architecture:** Replace the existing `book/chapters/ch01-noisy-bit.tex` stub (4 lines) with a fully drafted chapter containing 6 sections, a learning-outcomes opener, 10-12 exercises, supporting bibliographic entries, and a paired Python notebook. Plan 4 is the final Part I plan: it both drafts chapter 1 AND verifies that all four chapters of Part I compose into a coherent build with zero `Reference X undefined` warnings.

**Tech Stack:** LaTeX (book class), alex.sty notation package, biblatex with biber backend. Python 3.11+ + numpy + matplotlib for the notebook (BSC simulator, empirical FPR/FNR convergence plot, confidence-interval coverage check). The build pipeline established in Plans 0-3 is the test harness.

**Scope:** Chapter 1 plus the Part I integration check. Out of scope: chapter 5 onward (covered by future plans), the negative-space chapter 16 (which is only referenced as a forward pointer from chapter 1's notebook open question).

**Spec source of truth:** `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §4 (chapter 1 outline) and §8 (reference map). Master spec is `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`.

**Base SHA:** `c66ecd8` (HEAD at the end of Plan 3). Plan 4 builds linearly from this commit; main-branch-direct workflow per Plans 1-3.

**Source material (papers to reformulate):**
- `papers/bernoulli_sets/sections/algebra_of_sets.tex` Table 1 (TP/FP/TN/FN contingency table) for §1.2.
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Example 3.5 (Boolean universe with PMF) for §1.3, taken qualitatively only; full PMF lives in §4.5 already.
- Chapter 4 §4.5 (`book/chapters/ch04/bernoulli-bool-formal.tex`) for the formal-definition target that §1.3 sets up.

**Lessons inherited from Plans 1-3:**

The chapter-2 and chapter-3 review cycles consolidated five recurring lessons that Plan 4 must respect:

1. **Page count discipline.** Plans 1-3 came in 30-43% over their spec page targets. Chapter 1's spec target is ~25 pp; expect 30-35 pp. The biggest risk areas are §1.1 (the three framings tempt repetition) and §1.5 (the trajectory preview tempts duplication of §4.6).

2. **Q convention.** Q rows are indexed by input block ($B_1 = \{\top\}$, $B_2 = \{\bot\}$), columns by output label. Chapter 1 does not formally introduce Q (that is §2.1's job), but if any informal matrix appears in §1.2 or §1.3, it must follow this convention to avoid surprising the reader in chapter 2.

3. **No formal definitions in chapter 1.** Per the atom-outward trajectory ($\gamma$ structural decision in the Part I spec): no formal `Bernoulli[bool]` definition, no formal axioms, no Kronecker product. Chapter 1 uses ε, ω, τ, η informally and names the unifying object descriptively as "the abstract noisy bit". The formal definition lives in §4.5; §1.5 explicitly previews this without delivering it.

4. **Soul-voice hook constraints (inherited from Plans 1-3).** No Unicode em-dash (U+2014); use commas, colons, periods, or parentheses. No "lever" + "age" as a single word; use "draw on", "make use of", "exploit", or similar. The soul-voice hook blocks file writes that violate these rules.

5. **Forward references must use labels that ALREADY exist in chapters 2-4.** Chapter 1 is drafted last, so its forward references to chapters 2-4 will all resolve immediately under the full build. This is a feature: Plan 4's integration check exercises every cross-Part-I reference at least once. Conversely, chapter 1's labels (`sec:three-faces`, `sec:boolean-universe-first-look`, etc.) are the targets that chapters 2-4 have been pointing at; introducing them in §1.1 and §1.3 closes those forward references.

---

## File Structure

After this plan completes:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch01-noisy-bit.tex                  # rewritten from stub to ~25 pp chapter scaffold
│   │   └── ch01/                                # NEW directory
│   │       ├── three-faces.tex                  # §1.1 (~5 pp)
│   │       ├── quantifying-noise.tex            # §1.2 (~5 pp)
│   │       ├── boolean-universe-first-look.tex  # §1.3 (~4 pp)
│   │       ├── sampling-rates.tex               # §1.4 (~3 pp)
│   │       ├── why-atom.tex                     # §1.5 (~5 pp)
│   │       ├── bibliographic-notes.tex          # §1.6 (~1-2 pp)
│   │       └── exercises.tex                    # 10-12 exercises
│   └── references.bib                           # extended if new sources cited (sensitivity/specificity literature, Wasserman, etc.)
└── python/
    └── notebooks/
        └── ch01-noisy-bit.ipynb                 # BSC simulator, empirical FPR/FNR convergence, CI coverage check
```

The chapter follows the same subdirectory pattern as Plans 1-3. The thin chapter file inputs section subfiles. This isolates per-section commits and keeps each subagent's working scope small.

`python/notebooks/ch01-noisy-bit.ipynb` is the chapter's paired notebook. It simulates a BSC and a biased coin in Python (numpy), plots empirical FPR/FNR convergence vs sample size $n$, runs a confidence-interval coverage check (does the empirical CI contain the true rate at the claimed coverage?), and ends with the "what if rates vary across samples?" open question that forward-references chapter 16 (the negative-space chapter).

---

## Cross-Reference Map (Plan 4 closing inventory)

By the end of Plan 4, every label in this table must resolve under the full book build:

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:noisy-bit` | `ch01-noisy-bit.tex` line 2 (already present) | `ch04/what-comes-next.tex`, `ch04/bernoulli-bool-formal.tex` |
| `sec:three-faces` | `ch01/three-faces.tex` (Task 2) | `ch02/bsc.tex`, `ch02/asymmetric-channel.tex`, `ch02/channel-composition.tex`, `ch02/model-order.tex`, `ch03/and-under-noise.tex`, `ch03/or-not.tex`, `ch03/composition-theorem.tex`, `ch03/bridge-to-sets.tex`, `ch04/bernoulli-bool-formal.tex` |
| `sec:quantifying-noise` | `ch01/quantifying-noise.tex` (Task 3) | (chapter 1 internal) |
| `sec:boolean-universe-first-look` | `ch01/boolean-universe-first-look.tex` (Task 4) | `ch04/bernoulli-bool-formal.tex` |
| `sec:sampling-rates` | `ch01/sampling-rates.tex` (Task 5) | (chapter 1 internal; notebook references this section) |
| `sec:why-atom` | `ch01/why-atom.tex` (Task 6) | (forward-only, internal) |

Labels in chapters 2-4 already drafted (verified to resolve at Plan 3 head):

- `sec:bsc`, `def:bsc`, `sec:asymmetric-channel`, `sec:channel-composition`, `sec:model-order`, `def:model-order`, `thm:boolean-ceiling`, `ex:bsc-capacity` (chapter 2)
- `sec:and-under-noise`, `sec:or-not`, `sec:composition-theorem`, `thm:composition`, `sec:miller-rabin`, `sec:bridge-to-sets` (chapter 3)
- `ch:axioms-kronecker`, `sec:why-axioms`, `sec:axiom-1`, `ax:element-indep`, `sec:axiom-2`, `ax:block-rates-indep`, `sec:kronecker`, `thm:kronecker`, `cor:parameter-reduction`, `sec:bernoulli-bool-formal`, `def:bernoulli-bool`, `ex:biased-coin-formal`, `sec:what-comes-next`, `prop:stable-Q` (chapter 4)

Task 10 (the integration check) verifies the full table.

---

## Per-Task Drafting Discipline

Every section drafting task follows the same internal structure (matching Plans 1-3):

1. **Read paper source(s)** named in the task header.
2. **Read prior context** from earlier in the chapter and the relevant chapters 2-4 sections.
3. **Draft the section** to the page-length target, content checklist, and notation requirements specified in the task.
4. **Verify forward and backward references** specified in the task are present.
5. **Build the book** with `cd book && make cleanall && make` and confirm exit code 0.
6. **Self-review** against the section's content checklist.
7. **Commit** with the message format specified in the task.

Each task is then reviewed by two subagents (Path A discipline): a **spec-compliance reviewer** that checks the draft against the Part I spec §4 content checklist and length target, and a **quality reviewer** that reads the draft as a smart-undergrad reader and flags pedagogical, logical, or mathematical issues. Findings produce a follow-up fix commit if anything substantive surfaces.

---

## Tasks

### Task 1: Read source material and write chapter scaffolding

**Files:**
- Modify: `book/chapters/ch01-noisy-bit.tex` (currently a 4-line stub from Plan 0)

**Source reading:**
- `papers/bernoulli_sets/sections/algebra_of_sets.tex` (TP/FP/TN/FN contingency table for §1.2)
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Example 3.5 (Boolean universe; qualitative version for §1.3)
- `book/chapters/ch04/bernoulli-bool-formal.tex` (§4.5 formal definition; §1.3 sets up §4.5)
- `book/chapters/ch04/what-comes-next.tex` (§4.6 Part II preview; §1.5 must avoid duplicating it)
- `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §4 and §8

- [ ] **Step 1: Read all sources end-to-end**

Use `Read` on the five file paths above. Confirm the §4.5 formal definition matches what §1.3 will preview and §1.5 will tease.

- [ ] **Step 2: Replace the stub with chapter scaffolding**

Open `book/chapters/ch01-noisy-bit.tex` and replace its contents with:

```latex
\chapter{The Noisy Bit}
\label{ch:noisy-bit}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Recognize a noisy bit when you see one, whether it arrives as a
    biased coin, a binary symmetric channel, or a binary classifier's
    verdict.
  \item Quantify a noisy bit with its false-positive and false-negative
    rates, and sample to estimate them.
  \item Name the noisy bit as the atomic object of the framework, and
    point at the trajectory that develops its algebra across the
    remaining chapters of Part~I.
\end{itemize}
\end{quote}

% Section 1.1
\input{chapters/ch01/three-faces}

% Section 1.2
\input{chapters/ch01/quantifying-noise}

% Section 1.3
\input{chapters/ch01/boolean-universe-first-look}

% Section 1.4
\input{chapters/ch01/sampling-rates}

% Section 1.5
\input{chapters/ch01/why-atom}

% Section 1.6
\input{chapters/ch01/bibliographic-notes}

% Exercises
\input{chapters/ch01/exercises}
```

- [ ] **Step 3: Create the `book/chapters/ch01/` subdirectory**

```bash
mkdir -p book/chapters/ch01
```

- [ ] **Step 4: Create empty placeholder section files so the scaffold builds before the section drafts land**

For each of the seven filenames listed in the File Structure section (`three-faces.tex`, `quantifying-noise.tex`, `boolean-universe-first-look.tex`, `sampling-rates.tex`, `why-atom.tex`, `bibliographic-notes.tex`, `exercises.tex`), write a one-line placeholder:

```latex
% Placeholder. Drafted in Plan 4 Task N.
```

Use the Write tool for each file.

- [ ] **Step 5: Build the book to confirm scaffolding is clean**

```bash
cd book && make cleanall && make
```

Expected: exit code 0. The book PDF compiles. Chapter 1 in the table of contents shows only the learning outcomes box (the seven section subfiles are empty placeholders).

- [ ] **Step 6: Commit**

```bash
git add book/chapters/ch01-noisy-bit.tex book/chapters/ch01/
git commit -m "$(cat <<'EOF'
book: scaffold chapter 1 (the noisy bit) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener, seven section subfile inputs (three-faces, quantifying-noise,
boolean-universe-first-look, sampling-rates, why-atom,
bibliographic-notes, exercises), and matching empty placeholders. The
section drafts land in subsequent Plan 4 tasks.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: §1.1 Three Faces of a Noisy Bit (~5 pp)

**Files:**
- Modify: `book/chapters/ch01/three-faces.tex` (replace placeholder)

**Source reading:** None beyond the chapter scaffold and the spec. §1.1 is fresh writing.

**Purpose:** Open the chapter, and the book, with three concrete instances of the same abstract object. End with the explicit "abstract noisy bit" naming paragraph that establishes the atom. Introduce the three running threads (biased coin, BSC, classifier verdict) and label them so chapters 2-4 can reference them.

**Content checklist:**
1. Open with a short paragraph describing the scenario the chapter develops: three concrete systems, each producing a single Boolean output that may be wrong, and the question of what they share.
2. **Face 1: The biased coin.** Describe a coin that lands heads with probability $\omega$ when flipped after being held "in" the hand, and lands heads with probability $1 - \tau$ when flipped after being held "out". (The framing: input is "in/out", output is heads/tails, but the coin may be biased differently in each case.) Two paragraphs.
3. **Face 2: The binary symmetric channel.** Describe a transmission line that sends a single bit, occasionally flipping it with crossover probability $\fprate$. Same flip probability in both directions. Two paragraphs, with one paragraph noting that this is the simplest noisy channel and that the symmetry is a strong constraint.
4. **Face 3: The classifier verdict.** Describe a binary classifier (the running example: a spam filter) that emits "spam" or "ham" for each input message, with a false-positive rate ($\fprate$, ham mis-flagged as spam) distinct from a false-negative rate ($\fnrate$, spam missed). Two paragraphs.
5. **The unifying observation.** A short closing subsection: each of these three systems takes a Boolean input and returns a possibly-wrong Boolean output. The error behavior is characterized by at most two numbers: the false-positive rate and the false-negative rate. Name this abstract object: "We will call the abstract structure that all three share \emph{a noisy bit}." This sentence is the atom-naming moment of the book.
6. End with a 1-paragraph signpost: §1.2 quantifies, §1.3 walks the Boolean universe, §1.4 samples, §1.5 explains why this is the framework's atom.

**Labels and references this section creates:**
- `\section{Three Faces of a Noisy Bit}` with `\label{sec:three-faces}` (this is the label that chapters 2-4 have been pointing at)
- Three subsection (or paragraph) anchors: the biased coin, the BSC, the classifier verdict. (Optional `\label{}`s; if added, name them `subsec:biased-coin-intro`, `subsec:bsc-intro`, `subsec:classifier-intro`; chapters 2-4 currently reference only `sec:three-faces`, so the subsection labels are optional.)

**Notation discipline:**
- Use $\fprate$ for false-positive rate (alex.sty macro).
- Use $\fnrate$ for false-negative rate (alex.sty macro).
- Use $\omega$ informally for biased-coin upward bias and $\tau$ for downward (the classifier-verdict thread will reuse these in §1.2).
- Do NOT define $Q$ (the channel matrix); that is §2.1's job. Use prose for the channel description.
- Do NOT use $\Bernoulli{\BoolType}$; the atom-naming uses the descriptive name "a noisy bit". The formal type name first appears in §4.5.

- [ ] **Step 1: Read the spec §4 chapter-1 outline and §3.1 running-threads commitment**

- [ ] **Step 2: Draft `three-faces.tex` to the content checklist above**

Target length: ~5 pp (roughly 1100-1400 words including the learning-outcomes signpost paragraph).

Open with a header comment block listing cross-reference resolution status (matching the convention used in chapters 2-4):

```latex
% §1.1 Three Faces of a Noisy Bit
%
% Cross-reference resolution status:
%
% ALREADY DEFINED (within chapter 1, by this section):
%   \label{sec:three-faces}              -- this section
%
% FORWARD REFS to later chapter 1 sections (resolve in Plan 4 Tasks 3-7):
%   \Cref{sec:quantifying-noise}         -- §1.2 (Task 3)
%   \Cref{sec:boolean-universe-first-look} -- §1.3 (Task 4)
%   \Cref{sec:sampling-rates}            -- §1.4 (Task 5)
%   \Cref{sec:why-atom}                  -- §1.5 (Task 6)
%
% FORWARD REFS to chapters 2-4 (already resolved at Plan 3 HEAD):
%   \Cref{sec:bsc}                       -- chapter 2 §2.1
%   \Cref{sec:asymmetric-channel}        -- chapter 2 §2.2
%   \Cref{ch:axioms-kronecker}           -- chapter 4
```

- [ ] **Step 3: Build the book**

```bash
cd book && make cleanall && make
```

Expected: exit code 0. Eight previously-unresolved `\Cref{sec:three-faces}` warnings (chapters 2-4) now resolve.

- [ ] **Step 4: Verify forward references**

```bash
grep -c "Reference.*undefined" book/book.log || echo "no undefined references in log"
```

The number of undefined references should drop by exactly 8 (the count of `sec:three-faces` references in chapters 2-4) from the Plan 3 HEAD baseline.

- [ ] **Step 5: Commit**

```bash
git add book/chapters/ch01/three-faces.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 1.1 Three Faces of a Noisy Bit (~5 pp)

The atom-naming moment of the book. Three concrete framings (biased
coin, binary symmetric channel, classifier verdict) share a structure
characterized by at most two error rates. The closing paragraph names
the abstract object "a noisy bit", which chapters 2-4 then unfold the
algebra of. The \label{sec:three-faces} introduced here is the label
that chapters 2-4 have been pointing at: this commit resolves the
eight outstanding forward references to that target.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Spec-compliance review (subagent)**

Dispatch a subagent (general-purpose) with this prompt:

> Read `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §4 (chapter 1 outline), focusing on the §1.1 row. Then read `book/chapters/ch01/three-faces.tex`. Verify: (a) the section delivers all six content-checklist items listed in Plan 4 Task 2 (three concrete framings, the abstract-noisy-bit naming sentence, the §1.1 signpost paragraph); (b) the section is approximately 5 pp; (c) the section defines `\label{sec:three-faces}`; (d) the three running threads (BSC, biased coin, classifier verdict) are each named and described in distinct subsections or labeled paragraphs; (e) no formal `Bernoulli[bool]` definition appears; (f) the section opens cleanly enough for a first-time reader of the book to follow without prior context. Report findings as a short bullet list. Do not edit any files.

- [ ] **Step 7: Quality review (subagent)**

Dispatch a separate subagent (general-purpose) with this prompt:

> You are an experienced technical-textbook reader reviewing chapter 1 of a book on Bernoulli types (random approximate computation). Read `book/chapters/ch01/three-faces.tex` cold (without reading any other chapter). For each of the three framings: does the description make immediate intuitive sense? Is the framing concrete enough for a reader to picture? Does the closing "we will call this a noisy bit" sentence feel earned by the three preceding framings? Are there any places where the prose silently assumes prior context the reader doesn't have? Does the section make me want to read §1.2? Report a short bullet list of findings (issues if any, what works well). Do not edit any files.

- [ ] **Step 8: Address review findings**

If either reviewer surfaces substantive issues, write a fix commit. Otherwise, proceed to Task 3.

---

### Task 3: §1.2 Quantifying the Noise (~5 pp)

**Files:**
- Modify: `book/chapters/ch01/quantifying-noise.tex` (replace placeholder)

**Source reading:**
- `papers/bernoulli_sets/sections/algebra_of_sets.tex` (Table 1: TP/FP/TN/FN contingency table). The §1.2 reformulation should track this table but with cleaner pedagogical voice.

**Purpose:** Introduce informal FPR and FNR via a contingency table. Set up the notation sidebar (ε, ω, τ, η as alex.sty macros). Cross-walk to precision and recall via the classifier-verdict thread. By the end of §1.2 the reader knows what a noisy bit's error rates ARE and how to read off a 2x2 confusion matrix.

**Content checklist:**
1. Open by recalling the §1.1 closing observation: a noisy bit is characterized by two error rates. Make precise what those rates measure.
2. **The contingency table.** Present a 2x2 table with the four cells: true positive (TP), false positive (FP), true negative (TN), false negative (FN). Each cell is the count of observed input-output pairs in that joint state across a sample of $n$ observations. Spend two paragraphs walking the reader through reading the table.
3. **From counts to rates.** Define the false-positive rate $\fprate$ as FP / (TN + FP), and the false-negative rate $\fnrate$ as FN / (TP + FN). Both rates are conditional: the conditioning is on the true state of the input. Define the complementary rates $\trate = 1 - \fprate$ (true-negative rate) and $\eta = 1 - \fnrate$ (true-positive rate, sometimes called sensitivity). One paragraph each.
4. **Notation sidebar.** A boxed sidebar (or `\paragraph{}` with a hanging indent) listing the four symbols ε, ω, τ, η and what each one means, plus the alex.sty macros (`\fprate`, `\fnrate`, etc.). Half a page. Forward-reference the consolidated cheat sheet in Appendix B (`\Cref{app:five-principles}` if the label exists in the appendix scaffold; otherwise prose only).
5. **Cross-walk to precision and recall.** Use the classifier-verdict thread: a spam filter's precision is TP / (TP + FP); recall is TP / (TP + FN), which is the same as $\eta$. Show the algebraic relationship between (precision, recall) and ($\fprate$, $\fnrate$). One page. This is where the classifier-verdict thread does pedagogical work.
6. **Worked numerical example.** Take a small confusion matrix from a 100-message spam-filter run (e.g., 40 spam / 60 ham, 35 TP, 5 FN, 3 FP, 57 TN) and compute all four rates plus precision and recall. Half a page.
7. End with a signpost: §1.3 walks the Boolean universe whose error rates §1.2 just defined.

**Labels and references this section creates:**
- `\section{Quantifying the Noise}` with `\label{sec:quantifying-noise}`
- Optional: `\label{tab:contingency}` on the 2x2 confusion matrix table.

**Notation discipline:**
- Use `\fprate`, `\fnrate`, `\trate`, `\eta` from alex.sty (or define `\trate` if not present; check first).
- Sample size symbol is $n$.
- Do NOT introduce $Q$.

- [ ] **Step 1: Read `papers/bernoulli_sets/sections/algebra_of_sets.tex` Table 1**

- [ ] **Step 2: Confirm alex.sty macro coverage**

```bash
grep -n "trate\|tnrate\|fprate\|fnrate\|sensitivity\|specificity" book/alex.sty
```

If `\trate` is not defined, use `\tnrate` or define it locally inside the section file with `\providecommand{\trate}{...}` (do not modify alex.sty).

- [ ] **Step 3: Draft `quantifying-noise.tex` to the content checklist above**

Target length: ~5 pp.

Header comment block (mirroring §1.1's pattern) listing cross-reference resolution status.

- [ ] **Step 4: Build and verify**

```bash
cd book && make cleanall && make
```

Expected: exit code 0.

- [ ] **Step 5: Commit**

```bash
git add book/chapters/ch01/quantifying-noise.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 1.2 Quantifying the Noise (~5 pp)

Informal FPR and FNR via a 2x2 contingency table, a notation sidebar
introducing the four alex.sty rate symbols, the precision/recall
cross-walk via the classifier-verdict running thread, and a worked
numerical example on a 100-message spam-filter run.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Spec-compliance review (subagent)**

Dispatch a subagent with this prompt:

> Read `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` §4 (chapter 1 outline) §1.2 row, then read `book/chapters/ch01/quantifying-noise.tex`. Verify: (a) the seven content-checklist items in Plan 4 Task 3 are all present; (b) the section is approximately 5 pp; (c) the notation sidebar introduces ε, ω, τ, η explicitly; (d) the precision/recall cross-walk uses the spam-filter classifier-verdict thread; (e) the worked numerical example produces internally consistent rate calculations; (f) the section defines `\label{sec:quantifying-noise}`; (g) no formal `Bernoulli[bool]` definition or channel matrix $Q$ appears. Report a short bullet list. Do not edit files.

- [ ] **Step 7: Quality review (subagent)**

Dispatch a separate subagent with this prompt:

> You are reading chapter 1 of a textbook on Bernoulli types. You have just read §1.1 (three framings of a noisy bit). Now read `book/chapters/ch01/quantifying-noise.tex` cold. Does the contingency table feel like the natural next step from §1.1's closing? Does the precision/recall cross-walk help or distract? Is the worked numerical example arithmetically correct (verify by hand from the numbers it gives)? Are the notation symbols introduced without unnecessary ceremony? Report findings. Do not edit files.

- [ ] **Step 8: Address review findings**

---

### Task 4: §1.3 A First Look at the Boolean Universe (~4 pp)

**Files:**
- Modify: `book/chapters/ch01/boolean-universe-first-look.tex` (replace placeholder)

**Source reading:**
- `papers/bernoulli_sets/sections/bernoulli_model.tex` Example 3.5 (Boolean universe with PMF; §1.3 takes the qualitative shape only)
- `book/chapters/ch04/bernoulli-bool-formal.tex` (§4.5; the formal version of §1.3's qualitative walk)

**Purpose:** Walk the reader narratively through the 2x2 outcome matrix without a PMF or joint distribution. The reader sees that there is a structure here ($\top \to \top$, $\top \to \bot$, $\bot \to \top$, $\bot \to \bot$) but is told explicitly that full formalization waits for §4.5. This is a deferral, executed gracefully.

**Content checklist:**
1. Open by stating: a noisy bit has two possible inputs and two possible outputs. The four input-output combinations are the universe of joint behavior. Set up the 2x2 outcome matrix.
2. **The four cells, narratively.** Walk through each cell: input $\top$ gives output $\top$ (correct positive); input $\top$ gives output $\bot$ (false negative); input $\bot$ gives output $\top$ (false positive); input $\bot$ gives output $\bot$ (correct negative). Connect the cells back to §1.2's contingency table: the four cells of the joint distribution and the four cells of the empirical contingency table are the same four cells. One page.
3. **Why this is a "universe".** The input domain $\{\top, \bot\}$ is the Boolean universe of size 2. This is the smallest non-trivial universe, and the chapter, and Part I as a whole, is the algebra OF this universe.
4. **The deferral.** Explicitly state: a fully formal description would assign a probability mass to each of the four cells, and the resulting joint distribution would be the channel matrix's entries times the prior. We do not formalize that here. §4.5 (`\Cref{sec:bernoulli-bool-formal}`) returns to this picture with the formal definition. The honest deferral. Half a page.
5. **A noisy-bit example, qualitatively.** Take a biased coin (the running thread): tell the reader its FPR is 0.1 and FNR is 0.2, and walk through what the four cells mean qualitatively. Don't compute joint probabilities yet; that's §4.5's job. Half a page.
6. End with a one-paragraph signpost: §1.4 takes the step from these conceptual cells to actual data, by sampling.

**Labels and references this section creates:**
- `\section{A First Look at the Boolean Universe}` with `\label{sec:boolean-universe-first-look}` (this is the label that `book/chapters/ch04/bernoulli-bool-formal.tex` lines 16 and 353 have been pointing at)
- Forward `\Cref{sec:bernoulli-bool-formal}` to §4.5 (this label exists)

**Notation discipline:**
- Use $\top$ and $\bot$ for Boolean values.
- Do NOT write a joint PMF; describe the four cells qualitatively.
- Do NOT introduce $Q$; describe the channel matrix without naming it.

- [ ] **Step 1: Read source material**

- [ ] **Step 2: Draft `boolean-universe-first-look.tex` to the content checklist**

Target length: ~4 pp.

Header comment block listing cross-reference resolution status.

- [ ] **Step 3: Build and verify**

```bash
cd book && make cleanall && make
```

Expected: exit code 0. The two `\Cref{sec:boolean-universe-first-look}` warnings in `ch04/bernoulli-bool-formal.tex` now resolve.

- [ ] **Step 4: Commit**

```bash
git add book/chapters/ch01/boolean-universe-first-look.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 1.3 A First Look at the Boolean Universe (~4 pp)

Qualitative narrative walk of the 2x2 outcome matrix (the four
input-output cells of a noisy bit). Explicit, honest deferral of the
full PMF and joint distribution to chapter 4 §4.5. The label
\label{sec:boolean-universe-first-look} defined here resolves the
two outstanding forward references from ch04/bernoulli-bool-formal.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Spec-compliance review (subagent)**

Dispatch a subagent:

> Read spec §4 §1.3 row, then `book/chapters/ch01/boolean-universe-first-look.tex`. Verify: (a) the six content-checklist items from Plan 4 Task 4; (b) approximately 4 pp; (c) NO PMF and NO joint distribution are computed; (d) the deferral to §4.5 is explicit; (e) the label `\label{sec:boolean-universe-first-look}` is defined; (f) the qualitative biased-coin example uses concrete numeric error rates without computing the joint. Report findings. Do not edit files.

- [ ] **Step 6: Quality review (subagent)**

Dispatch a subagent:

> Read `book/chapters/ch01/boolean-universe-first-look.tex` cold. Does the section earn the "deferral" without feeling like the author is hiding the ball? Is the four-cell walk concrete enough to be useful, abstract enough to feel like setup? Is the connection to §1.2's contingency table made clearly (the four cells of the joint distribution = four cells of the empirical table)? Report findings. Do not edit files.

- [ ] **Step 7: Address review findings**

---

### Task 5: §1.4 Sampling and Estimating Rates (~3 pp)

**Files:**
- Modify: `book/chapters/ch01/sampling-rates.tex` (replace placeholder)

**Source reading:** Fresh writing. Reference Plan 4's spec §4 §1.4 row.

**Purpose:** Single page on binomial counts, single page on CLT existence (no derivation), one page hooking the chapter 1 notebook. Defers everything substantive (estimator analysis, confidence-interval theory) to Part II chapter 7 (classification measures).

**Content checklist:**
1. Open by stating: we have defined what FPR and FNR mean (§1.2) and walked the joint structure (§1.3). What if we don't know the rates and want to estimate them from data?
2. **Binomial counts.** $n$ independent draws of a Bernoulli($\fprate$) variable, FP count distributed Binomial($n_0, \fprate$) where $n_0$ is the number of negative inputs. Empirical estimator $\hat{\fprate} = \mathrm{FP} / n_0$. State without derivation: this estimator is unbiased and has variance $\fprate(1 - \fprate) / n_0$. One page.
3. **CLT existence, no derivation.** A sentence stating that for large $n_0$, $\hat{\fprate}$ is approximately Normal with mean $\fprate$ and variance $\fprate(1 - \fprate)/n_0$. This gives an approximate $1 - \alpha$ confidence interval $\hat{\fprate} \pm z_{\alpha/2} \sqrt{\hat{\fprate}(1 - \hat{\fprate})/n_0}$. State the interval, do not derive it. Forward-reference Part II chapter 7 for the proper treatment. Half a page.
4. **Notebook hook.** One page describing what the chapter 1 notebook does: simulate a BSC with known crossover probability, sample $n$ times for $n$ ranging from 10 to 10000, plot $\hat{\fprate}$ vs $n$ to see the convergence, and run an empirical coverage check on the CI (does the empirical CI contain the true rate at the claimed coverage?). One page.
5. End with a one-paragraph signpost: §1.5 zooms back out and explains why this object, the noisy bit, deserves to be called the framework's atom.

**Labels and references this section creates:**
- `\section{Sampling and Estimating Rates}` with `\label{sec:sampling-rates}`
- Forward `\Cref{ch:classification-measures}` to chapter 7 (this label probably does NOT exist yet, since chapter 7 is in Part II; the reference can be prose-only ("we return to this in chapter 7") or use a placeholder `\Cref{}` that will resolve in a later plan). **Decision:** use prose-only references to chapter 7 to avoid creating new unresolved warnings.

**Notation discipline:**
- Sample size $n$, negative-input count $n_0$, positive-input count $n_1$.
- $\hat{\fprate}$ for the empirical FPR estimator (use `\hat{\fprate}`).
- $z_{\alpha/2}$ for the normal quantile.

- [ ] **Step 1: Draft `sampling-rates.tex` to the content checklist**

Target length: ~3 pp.

Header comment block listing cross-reference resolution status.

- [ ] **Step 2: Build and verify**

```bash
cd book && make cleanall && make
```

Expected: exit code 0.

- [ ] **Step 3: Commit**

```bash
git add book/chapters/ch01/sampling-rates.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 1.4 Sampling and Estimating Rates (~3 pp)

Binomial estimator for FPR/FNR on a single page, CLT-based
confidence-interval form on a half page (existence statement, no
derivation; full treatment deferred to Part II chapter 7), and a
one-page hook into the chapter 1 notebook (empirical convergence
plot, CI coverage check).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: Spec-compliance review (subagent)**

> Read spec §4 §1.4 row, then `book/chapters/ch01/sampling-rates.tex`. Verify: (a) approximately 3 pp; (b) binomial estimator stated without derivation; (c) CLT-based CI stated without derivation; (d) explicit deferral to chapter 7 (prose-only is fine); (e) notebook hook describes the BSC simulator, convergence plot, and CI coverage check; (f) `\label{sec:sampling-rates}` defined; (g) no derivations creep in beyond the page budget. Report findings.

- [ ] **Step 5: Quality review (subagent)**

> Read `book/chapters/ch01/sampling-rates.tex` cold. Is the page budget honored? Does the deferral to chapter 7 feel honest (not evasive)? Does the notebook hook make me actually want to open the notebook? Report findings.

- [ ] **Step 6: Address review findings**

---

### Task 6: §1.5 Why "Atom"? (~5 pp)

**Files:**
- Modify: `book/chapters/ch01/why-atom.tex` (replace placeholder)

**Source reading:**
- `book/chapters/ch04/what-comes-next.tex` (§4.6 Part II preview; §1.5 must NOT duplicate this)
- `book/chapters/ch04/bernoulli-bool-formal.tex` (§4.5; §1.5 teases its formal definition)
- `book/chapters/ch03/miller-rabin.tex` (one-paragraph tease of the §3.4 climax)

**Purpose:** Step back from the mechanics and explain WHY the noisy bit deserves the name "atom". Three commitments: chapters 2-4 unfold the algebra of how atoms compose (channels, Boolean operators, axioms); Part II takes the atom and builds approximate sets out of it; the Miller-Rabin tease shows that a randomized algorithm everyone already knows is, in fact, one of these atoms applied $k$ times.

**Content checklist:**
1. **Opening: what is an atom?** A noisy bit is atomic in the sense that it has no internal Bernoulli structure: it is a single Boolean input, a single Boolean output, two error rates. Anything more complex (a Bloom filter, a randomized algorithm, an asymmetric channel) is built from this object by composition. Half a page.
2. **Trajectory preview: chapters 2-4.**
   - Chapter 2 takes the same atom and gives it formal notation (channel matrix $Q$, model order). It shows the asymmetric variant and explains how chains of channels compose.
   - Chapter 3 takes the AND, OR, NOT operations from classical Boolean algebra and asks: what happens when the operands are noisy bits? The answer is the composition theorem.
   - Chapter 4 axiomatizes. It states the two independence axioms that justify everything chapters 1-3 have been doing, proves the Kronecker factorization theorem, and writes the formal definition $\Bernoulli{\BoolType}$.
   - Two pages, half a page per chapter.
3. **Miller-Rabin tease.** One paragraph: the Miller-Rabin primality test is the most famous randomized algorithm in CS. We will show in §3.4 that one round of Miller-Rabin is exactly a noisy bit with $\fnrate = 0$ and $\fprate \le 1/4$, and that the $k$-round bound $(1/4)^k$ falls out of the composition theorem. The "of course" moment after the "I had not thought of primality testing this way" moment.
4. **What Part II will do.** A short paragraph: Part II takes the atom, makes a SET out of it (a Bloom filter is a function from a set's universe to noisy bits), and develops the algebra of approximate sets. Half a page.
5. **What Part III will do.** A short paragraph: Part III takes the atom and lifts it from $\{\top, \bot\}$ to general algebraic types ($\Bernoulli{T}$ for arbitrary $T$). The model-order ceiling of 2 (chapter 2) is broken. Half a page.
6. End with a one-paragraph closing: §1.6 names the antecedents, and the rest of Part I unfolds the algebra you have just seen previewed.

**Labels and references this section creates:**
- `\section{Why ``Atom''?}` with `\label{sec:why-atom}`
- Forward `\Cref{ch:axioms-kronecker}`, `\Cref{sec:bernoulli-bool-formal}`, `\Cref{sec:kronecker}`, `\Cref{sec:miller-rabin}`, `\Cref{sec:composition-theorem}` (all resolve at Plan 3 HEAD).

**Notation discipline:**
- This is the FIRST place the formal type name $\Bernoulli{\BoolType}$ may appear in chapter 1, but ONLY in the trajectory-preview context "chapter 4 writes the formal definition $\Bernoulli{\BoolType} = (X, Y, Q)$ ..." and not in any computation or operator. Use sparingly.

- [ ] **Step 1: Read source material (especially ch04/what-comes-next.tex to avoid duplication)**

- [ ] **Step 2: Draft `why-atom.tex` to the content checklist**

Target length: ~5 pp.

Header comment block listing cross-reference resolution status.

- [ ] **Step 3: Build and verify**

```bash
cd book && make cleanall && make
```

Expected: exit code 0.

- [ ] **Step 4: Commit**

```bash
git add book/chapters/ch01/why-atom.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 1.5 Why "Atom"? (~5 pp)

The trajectory preview: chapters 2-4 unfold the algebra of how atoms
compose (channels, Boolean operators, axioms), the Miller-Rabin tease
sets up the §3.4 climax, and short paragraphs preview Part II
(approximate sets) and Part III (general algebraic types). Closes
chapter 1 with the reader knowing where the next ~80 pages will take
them.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Spec-compliance review (subagent)**

> Read spec §4 §1.5 row, then `book/chapters/ch01/why-atom.tex`. Verify: (a) six content-checklist items; (b) approximately 5 pp; (c) the Miller-Rabin tease is ONE paragraph, not more; (d) the trajectory preview covers chapters 2, 3, 4 in roughly half a page each; (e) §1.5 does NOT duplicate §4.6 (the Part II preview content is different in framing: §1.5 looks forward from chapter 1's vantage; §4.6 looks forward from chapter 4's vantage); (f) `\label{sec:why-atom}` defined. Report findings.

- [ ] **Step 6: Quality review (subagent)**

> Read `book/chapters/ch01/why-atom.tex` cold. Does the "atom" framing land? Does the Miller-Rabin tease tantalize without spoiling the §3.4 climax? Is the chapter-by-chapter preview informative or repetitive? Does it duplicate the §4.6 "what comes next" content too much (read `book/chapters/ch04/what-comes-next.tex` to check)? Report findings.

- [ ] **Step 7: Address review findings**

---

### Task 7: §1.6 Bibliographic Notes (~1-2 pp)

**Files:**
- Modify: `book/chapters/ch01/bibliographic-notes.tex` (replace placeholder)
- Possibly modify: `book/references.bib` (add new entries if needed)

**Source reading:**
- `book/references.bib` (existing entries: `shannon-1948`, `miller-1976`, `rabin-1980`, `cormen-clrs`, `mitzenmacher-upfal`, `bloomfilter`, `cover-thomas`, `towell-bernoulli-sets`, `towell-bernoulli-data-type`, `towell-bernoulli-book`)
- `book/chapters/ch02/bibliographic-notes.tex` and `book/chapters/ch03/bibliographic-notes.tex` for style/depth precedent

**Purpose:** Place chapter 1's content in the historical and disciplinary context. Cite Shannon (1948) for the channel framing, the medical-statistics tradition for the contingency table and sensitivity/specificity vocabulary, Miller (1976) for the primality tease, the underlying Bernoulli papers (`towell-bernoulli-sets`, `towell-bernoulli-data-type`, `towell-bernoulli-book`). 1-2 pages.

**Content checklist:**
1. **Shannon and channels.** One paragraph attributing the noisy-channel framing (§1.1 face 2, §2.1 formal) to Shannon (1948). Note that the BSC is among the simplest of Shannon's channels and is still the standard pedagogical entry point.
2. **Contingency tables, medical statistics, and the sensitivity/specificity tradition.** One paragraph noting that the 2x2 contingency table predates the modern probability framing and was developed in epidemiology and medical diagnostic testing. Cite Pepe (2003) or comparable if a citation is warranted; alternatively, prose-only acknowledgement.
3. **The classifier-verdict thread.** One paragraph noting that precision and recall arrive from information retrieval (cite Manning, Raghavan, Sch\"utze 2008, or comparable; verify the entry exists or add it).
4. **Primality testing and the tease for §3.4.** One paragraph attributing the Miller-Rabin algorithm to Miller (1976) and Rabin (1980); §3.6 expands on this. Cite `miller-1976` and `rabin-1980` (both exist in references.bib).
5. **Our papers.** One paragraph: chapter 1's noisy-bit object is formalized in `towell-bernoulli-sets` and reappears as a special case of the algebraic-type machinery in `towell-bernoulli-data-type`. The book itself is `towell-bernoulli-book`.

**Possible new bib entries (add only if cited):**

```bibtex
@book{manning-raghavan-schutze,
  author    = {Christopher D. Manning and Prabhakar Raghavan and Hinrich Sch\"utze},
  title     = {Introduction to Information Retrieval},
  publisher = {Cambridge University Press},
  year      = {2008}
}

@book{pepe-2003,
  author    = {Margaret S. Pepe},
  title     = {The Statistical Evaluation of Medical Tests for Classification and Prediction},
  publisher = {Oxford University Press},
  year      = {2003}
}
```

(Add to `book/references.bib` if cited; otherwise use prose-only attribution.)

**Labels:** Section anchor `\section*{Bibliographic Notes}` with `\addcontentsline{toc}{section}{Bibliographic Notes}` (matching ch02 and ch03 conventions). No `\label{}` needed.

- [ ] **Step 1: Read precedent bib-notes sections (ch02, ch03)**

- [ ] **Step 2: Draft `bibliographic-notes.tex`**

Target length: ~1-2 pp.

- [ ] **Step 3: Add new bib entries to `references.bib` if any are cited**

Only add `manning-raghavan-schutze` and/or `pepe-2003` if the prose actually `\cite{}`s them.

- [ ] **Step 4: Build and verify**

```bash
cd book && make cleanall && make
```

Expected: exit code 0. No `Citation X undefined` warnings.

- [ ] **Step 5: Commit**

```bash
git add book/chapters/ch01/bibliographic-notes.tex book/references.bib
git commit -m "$(cat <<'EOF'
book: draft chapter 1.6 Bibliographic Notes; extend bib if needed

Attribute the noisy-channel framing to Shannon (1948), the 2x2
contingency table tradition to epidemiology, the precision/recall
vocabulary to information retrieval, the primality tease to Miller
(1976) and Rabin (1980), and the formal Bernoulli model to our papers
(towell-bernoulli-sets, towell-bernoulli-data-type, this book itself).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Spec-compliance review (subagent)**

> Read `book/chapters/ch01/bibliographic-notes.tex` and the existing chapter-2 and chapter-3 bibliographic-notes sections. Verify: (a) approximately 1-2 pp; (b) the five content areas (Shannon channels, contingency tables, classifier verdict / IR, Miller-Rabin tease, our papers) are each addressed; (c) every `\cite{}` resolves to an entry in `book/references.bib`; (d) style and depth match ch02 and ch03 precedent. Report findings.

- [ ] **Step 7: Quality review (subagent)**

> Read `book/chapters/ch01/bibliographic-notes.tex` cold. Does it place chapter 1's content in honest historical context? Are there any attributions that feel forced or any that feel missing? Report findings.

- [ ] **Step 8: Address review findings**

---

### Task 8: Chapter 1 Exercises (10-12)

**Files:**
- Modify: `book/chapters/ch01/exercises.tex` (replace placeholder)

**Source reading:**
- `book/chapters/ch02/exercises.tex` and `book/chapters/ch03/exercises.tex` for style precedent
- Plan 4 spec section 4 "Chapter 1 Exercises" subsection

**Purpose:** 10-12 exercises with star difficulty markers, distributed approximately as 3 warm-ups (★), 5 medium (★★), 3 challenging or extension (★★★). Mix of conceptual, computational (notebook-tied), and reasoning exercises.

**Content checklist:** The spec §4 "Chapter 1 Exercises" subsection enumerates eleven candidate exercises. Use those as the exercise set (you may merge or split as judgment dictates, but keep the count at 10-12 and the distribution at roughly 3/5/3):

**Warm-up (★ × 3):**
1. Confusion-matrix to rate conversion (given counts, compute FPR, FNR, precision, recall).
2. Identify three real-world systems as noisy bits (the reader supplies examples and writes their estimated $\fprate$ and $\fnrate$; an explicit non-example is required as the fourth answer).
3. Given a joint $2 \times 2$ outcome table with row priors, compute FPR and FNR.

**Medium (★★ × 5):**
4. Empirical estimation under varying $n$ (notebook-tied): use the chapter notebook to estimate $\fprate$ and $\fnrate$ for $n \in \{10, 100, 1000, 10000\}$ and plot.
5. A biased coin with bias $p$ (heads with probability $p$ regardless of input): write its $\fprate$ and $\fnrate$ as a function of $p$.
6. Show that NOT on a noisy bit (swap the output) has $\fprate' = \fnrate$ and $\fnrate' = \fprate$.
7. A binary classifier's ROC curve as a family of noisy bits parameterized by the decision threshold $\theta$: write the $(\fprate(\theta), \fnrate(\theta))$ pair as $\theta$ varies and describe the curve qualitatively.
8. Sample-size formula: given a target standard error $s$ on $\hat{\fprate}$, derive the required $n_0$ (Normal-approx CLT bound).

**Challenging (★★★ × 3):**
9. Argue informally that under iid sampling, $\hat{\fprate} \to \fprate$ in probability. (LLN setup; no rigor required, but the argument should be sound.)
10. Construct a system that LOOKS like a noisy bit but is not one (no fixed rates; rates depend on history; correlated noise across queries). This forward-references the negative-space chapter 16.
11. Construct a stress test for the chapter 1 notebook's empirical estimator (what input parameters cause the CI coverage check to fail visibly? Why?).

**Labels:** Each exercise gets `\label{ex:ch1-N}` for $N = 1, \ldots, 11$ to enable forward references from later chapters if needed. The exercise environment uses `\providecommand{\exstar}{...}` etc. matching ch02 and ch03 patterns.

- [ ] **Step 1: Read ch02 and ch03 exercises.tex as style precedent**

- [ ] **Step 2: Draft `exercises.tex` with 10-12 exercises and difficulty markers**

Target length: ~2 pp (exercises are compact prompts).

- [ ] **Step 3: Build and verify**

```bash
cd book && make cleanall && make
```

Expected: exit code 0.

- [ ] **Step 4: Commit**

```bash
git add book/chapters/ch01/exercises.tex
git commit -m "$(cat <<'EOF'
book: draft chapter 1 exercises (11 with star difficulty markers)

3 warm-ups (confusion-matrix conversion, real-world system
identification, joint-table rate computation), 5 medium (notebook
empirical estimation, biased-coin parameterization, NOT swap, ROC
parameterization, sample-size formula), 3 challenging (LLN informal
argument, negative-example for ch 16 forward reference, notebook
stress test).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Spec-compliance review (subagent)**

> Read spec §4 "Chapter 1 Exercises" subsection, then `book/chapters/ch01/exercises.tex`. Verify: (a) 10-12 exercises; (b) approximately 3/5/3 distribution across ★/★★/★★★; (c) the eleven candidate exercises from the spec are all represented (allowing for slight merging or rewording); (d) every exercise has a difficulty marker; (e) notebook-tied exercises explicitly reference the notebook; (f) the negative-space forward reference to chapter 16 is present. Report findings.

- [ ] **Step 6: Quality review (subagent)**

> Read `book/chapters/ch01/exercises.tex` cold. For each exercise: is the prompt unambiguous? Is the difficulty marker fair? Are there any exercises that secretly require chapter 2-4 content? Are the ★★★ ones actually harder than the ★★ ones? Report findings.

- [ ] **Step 7: Address review findings**

---

### Task 9: Chapter 1 Notebook (`ch01-noisy-bit.ipynb`)

**Files:**
- Create: `python/notebooks/ch01-noisy-bit.ipynb`

**Source reading:**
- `python/notebooks/ch02-binary-channels.ipynb` and `python/notebooks/ch03-boolean-algebra-noise.ipynb` for structure and Python style precedent
- `python/notebooks/README.md`

**Purpose:** The paired notebook for chapter 1. Demonstrates BSC and biased-coin simulation, plots empirical FPR/FNR convergence vs sample size, runs a CI coverage check, and closes with the "what if rates vary?" open question that forward-references chapter 16.

**Content checklist (~12-15 cells):**
1. **Title cell** (markdown): "Chapter 1: The Noisy Bit. Companion notebook."
2. **Setup cell** (code): import numpy, matplotlib, set seed.
3. **BSC simulator cell** (code): function `simulate_bsc(epsilon, n, rng)` returning input array and output array.
4. **BSC empirical FPR/FNR cell** (code): run `simulate_bsc(epsilon=0.1, n=1000)`, compute empirical FPR and FNR from the four cells, compare to the true 0.1.
5. **Convergence plot cell** (code): for $n \in \{10, 100, 1000, 10000, 100000\}$, simulate and plot empirical $\hat{\fprate}$ vs $n$ with the true value as a horizontal reference line. Same for $\hat{\fnrate}$.
6. **Biased-coin asymmetric simulator cell** (code): function `simulate_asymmetric(fpr, fnr, n, rng)` returning input array and output array.
7. **Asymmetric empirical estimation cell** (code): run with $\fprate = 0.05$, $\fnrate = 0.2$, verify the recovered estimates.
8. **CI coverage check cell** (code): repeat the experiment $M = 1000$ times for fixed small $n$ (e.g., $n_0 = n_1 = 200$), construct the Wald 95% CI for $\fprate$ each time, count the fraction of intervals that contain the true 0.05. Expected: roughly 0.95, but with a known under-coverage at small $n$ when $\fprate$ is near 0.
9. **CI coverage plot cell** (code): vary $n_0$ across $\{20, 50, 100, 500, 2000\}$ and plot empirical coverage vs $n_0$.
10. **Discussion cell** (markdown): explain why coverage drifts from 0.95 at small $n_0$ (the Wald CI is known to under-cover for rates near 0 or 1). Forward-reference chapter 7 (Part II) for the proper treatment (Wilson, Clopper-Pearson intervals).
11. **Open question cell** (markdown): what if the rates vary across samples? What if the noise events are correlated? Both questions break the noisy-bit picture. The book returns to these in chapter 16 (the negative-space chapter). End the notebook with an explicit cross-reference to chapter 16.

**Numerical sanity targets:**
- Convergence plot: empirical $\hat{\fprate}$ should be within $\pm 0.01$ of true at $n \ge 10000$.
- CI coverage check: empirical coverage at $n_0 \ge 200$ should be in $[0.93, 0.97]$ for $\fprate = 0.05$.

**Run-to-completion requirement:** The notebook MUST execute end-to-end with no errors when run from a fresh Python kernel (the bernoulli/ python environment is set up via `uv sync` per Plan 0).

- [ ] **Step 1: Read precedent notebooks for cell structure**

```bash
ls python/notebooks/ && head -50 python/notebooks/ch02-binary-channels.ipynb
```

- [ ] **Step 2: Draft the notebook**

Use the Write tool to create the .ipynb file as valid JSON. Match cell structure to ch02 and ch03 notebooks.

- [ ] **Step 3: Execute the notebook end-to-end**

```bash
cd python && uv run jupyter nbconvert --to notebook --execute notebooks/ch01-noisy-bit.ipynb --output ch01-noisy-bit.ipynb 2>&1 | tail -20
```

Expected: exit code 0. Notebook is overwritten with executed outputs in place.

- [ ] **Step 4: Visually verify the notebook outputs**

```bash
jupyter nbconvert --to script python/notebooks/ch01-noisy-bit.ipynb --stdout | head -100
```

Spot-check the convergence and coverage numbers against the sanity targets.

- [ ] **Step 5: Commit**

```bash
git add python/notebooks/ch01-noisy-bit.ipynb
git commit -m "$(cat <<'EOF'
python: add chapter 1 notebook (the noisy bit)

BSC and asymmetric-channel simulators, empirical FPR/FNR convergence
plot, Wald CI coverage check across varying n, and the open question
that forward-references chapter 16 (negative-space examples: varying
rates, correlated noise).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Spec-compliance review (subagent)**

> Read spec §4 "Chapter 1 Notebook" subsection, then read the executed notebook at `python/notebooks/ch01-noisy-bit.ipynb` (use `jupyter nbconvert --to script ... --stdout` if you need the code as plain Python). Verify: (a) all four spec content bullets are present (BSC + biased coin simulators, convergence plot, CI coverage check, open question forward-referencing ch 16); (b) the notebook ran cleanly (output cells are populated); (c) numerical outputs match sanity targets. Report findings.

- [ ] **Step 7: Quality review (subagent)**

> Read the executed chapter 1 notebook cold. Does the narrative arc work (setup, simulate, converge, check coverage, ask open question)? Are the plots legible? Is the closing open question framed in a way that invites the reader forward without spoiling chapter 16? Report findings.

- [ ] **Step 8: Address review findings**

---

### Task 10: Part I Integration Check

**Files:** None modified directly. This task verifies the whole.

**Purpose:** Chapters 1-4 of Part I are now all drafted. Plan 4's closing task verifies the full book build is clean (zero undefined references, zero undefined citations across Part I) and runs a brief structural inspection.

- [ ] **Step 1: Clean build the full book**

```bash
cd book && make cleanall && make
```

Expected: exit code 0. Save the build log for inspection:

```bash
cp book/book.log /tmp/plan4-final-build.log
```

- [ ] **Step 2: Verify zero undefined references**

```bash
grep -c "Reference.*undefined\|Citation.*undefined\|reference.*on page.*undefined" book/book.log
```

Expected: 0. If non-zero, list the specific undefined references and resolve before proceeding.

- [ ] **Step 3: Verify all Part I cross-references resolve**

Run each of these (every label in the Cross-Reference Map table at the top of this plan must be defined exactly once):

```bash
grep -rn "\\\\label{ch:noisy-bit}\|\\\\label{sec:three-faces}\|\\\\label{sec:quantifying-noise}\|\\\\label{sec:boolean-universe-first-look}\|\\\\label{sec:sampling-rates}\|\\\\label{sec:why-atom}" book/chapters/ch01/
```

Expected: one match per label, exactly one file per label.

```bash
grep -rn "\\\\Cref{sec:three-faces}\|\\\\Cref{sec:boolean-universe-first-look}" book/chapters/ch02/ book/chapters/ch03/ book/chapters/ch04/
```

Expected: at least one match in chapter 2 (`sec:three-faces`), one match in chapter 3 (`sec:three-faces`), two matches in chapter 4 (`sec:three-faces` and `sec:boolean-universe-first-look`). Total: at least eight matches.

- [ ] **Step 4: Page-count audit**

```bash
pdfinfo book/book.pdf | grep Pages
```

Read off the total page count. Inspect that chapters 1, 2, 3, 4 fall within the spec page budgets ($\pm 30\%$):
- Chapter 1: target ~25 pp, allow 20-35 pp
- Chapter 2: target ~24 pp, allow 19-34 pp (was 32 at Plan 2 close)
- Chapter 3: target ~28 pp, allow 22-40 pp (was 40 at Plan 3 close)
- Chapter 4: target ~28 pp, allow 22-40 pp (was 38 at Plan 1 close)

Total Part I should be 90-150 pp. Spec target was ~105 pp.

To inspect per-chapter page counts, find the chapter starting pages from `book.toc` and difference:

```bash
grep -E "chapter.numberline" book/book.toc
```

- [ ] **Step 5: Running threads inventory**

For each of the three running threads, find every section where it is named or developed:

```bash
echo "=== BSC thread ==="
grep -rn "binary symmetric channel\|BSC" book/chapters/ch01/ book/chapters/ch02/ book/chapters/ch03/ book/chapters/ch04/ | wc -l

echo "=== Biased coin thread ==="
grep -rn "biased coin\|biased-coin" book/chapters/ch01/ book/chapters/ch02/ book/chapters/ch03/ book/chapters/ch04/ | wc -l

echo "=== Classifier verdict thread ==="
grep -rn "classifier\|spam filter\|spam-filter" book/chapters/ch01/ book/chapters/ch02/ book/chapters/ch03/ book/chapters/ch04/ | wc -l
```

Each thread should appear in chapter 1 (introduction) and at least two of chapters 2/3/4 (callbacks).

- [ ] **Step 6: Soul-voice hook audit**

Verify no banned tokens leaked into Part I:

```bash
python3 -c "
import re
for f in __import__('glob').glob('book/chapters/ch0?/**/*.tex', recursive=True) + __import__('glob').glob('book/chapters/ch0?-*.tex'):
    with open(f, encoding='utf-8') as fh:
        text = fh.read()
    if chr(0x2014) in text:
        print(f'FAIL: em-dash in {f}')
    if re.search(r'\blever\s*age\b', text, re.IGNORECASE):
        print(f'FAIL: lever+age in {f}')
print('audit complete')
"
```

Expected: only "audit complete" printed, no FAIL lines.

- [ ] **Step 7: Final commit (integration verification record)**

If steps 1-6 all pass, commit nothing (no source changes); instead, write a short integration-pass record to the plans directory:

```bash
cat > docs/superpowers/plans/2026-05-13-bernoulli-textbook-ch01-noisy-bit-integration-pass.md <<'EOF'
# Plan 4 Integration Pass Record

Date: 2026-05-13
Plan: docs/superpowers/plans/2026-05-13-bernoulli-textbook-ch01-noisy-bit.md
HEAD at integration: <fill in current SHA>

## Verification results

- Clean build: PASS (exit code 0)
- Zero undefined references: PASS
- Zero undefined citations: PASS
- All chapter 1 labels defined exactly once: PASS
- Forward references from chapters 2-4 to chapter 1 all resolve: PASS
- Page-count audit (per chapter and total): <fill in>
- Running threads inventory: <fill in counts>
- Soul-voice hook audit: PASS

## Open follow-ups

<fill in any noted but deferred items>
EOF
```

Fill in the placeholders, then commit:

```bash
git add docs/superpowers/plans/2026-05-13-bernoulli-textbook-ch01-noisy-bit-integration-pass.md
git commit -m "$(cat <<'EOF'
book: Part I integration pass record (Plan 4 close)

Records the final integration verification for Part I (chapters 1-4):
clean build, zero undefined references and citations, all chapter 1
labels defined, all chapter 2-4 forward references to chapter 1
resolved, soul-voice hook audit clean. Page counts and running-thread
inventory noted for future polish-plan reference.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 8: Final spec-compliance review (subagent)**

Dispatch a subagent for an end-of-Part-I review:

> Read `docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md` end-to-end. Then read `book/chapters/ch01-noisy-bit.tex`, the seven section files under `book/chapters/ch01/`, and the integration-pass record at `docs/superpowers/plans/2026-05-13-bernoulli-textbook-ch01-noisy-bit-integration-pass.md`. Verify: (a) Part I §14 Success Criteria items 1, 2, 3, and 5 are plausibly satisfied (item 4 is post-publication and not verifiable here); (b) the §3.1 three running threads each appear in chapter 1 and return in at least two of chapters 2/3/4 per the spec's §3.1 table; (c) the §8 Forward and Backward Reference Map is now fully closed (all targets have defined labels). Report findings in a short bullet list.

- [ ] **Step 9: Final quality review (subagent)**

Dispatch a subagent for a Part-I-as-a-whole quality review:

> Read `book/chapters/ch01-noisy-bit.tex` through the seven section files cold, then read just the chapter openers (the first ~2 pp of each) of chapters 2, 3, 4 (from `book/chapters/ch02-binary-channels.tex` and its `ch02/` subfile, etc.). As a smart-undergrad reader: does chapter 1 ease the reader into Part I? Does chapter 4's §4.5 formal definition feel earned by chapter 1's §1.3 deferral, ~80 pages back? Are the three running threads visible and helpful, or contrived? Report findings.

- [ ] **Step 10: Address review findings (if any)**

If the final reviews surface substantive issues, write follow-up fix commits. Otherwise, Part I is complete.

---

## Self-Review

After writing this plan, I checked the spec with fresh eyes against the task list:

**Spec coverage:**
- §4 chapter 1 §1.1-§1.6: each section has its own drafting task (Tasks 2-7).
- §4 chapter 1 notebook: Task 9.
- §4 chapter 1 exercises: Task 8.
- §3.1 three running threads: all three are introduced in Task 2 (§1.1) and reverified in Task 10 (integration check).
- §3.2 notation strategy three-tier: light sidebar in §1.2 (Task 3), distributed notes elsewhere (Tasks 4-6), consolidated cheat sheet in Appendix B (out of scope for Plan 4; Plan 0 scaffolded the appendix already).
- §3.3 learning outcomes box per chapter: in the chapter scaffold (Task 1 Step 2).
- §3.4 exercise depth (10-12 per chapter, 3/5/3 distribution): Task 8.
- §8 Forward and Backward Reference Map: Tasks 2, 4 (target labels created), Task 10 (verification).
- §14 Success Criteria 1-3 and 5: Task 10 Step 8 (Success Criterion 4 is post-publication, not verifiable here).
- §15 sequencing (chapter 1 last): respected by Plan 4 being Plan 4 (last of Part I plans).

**Placeholder scan:** None. Every step contains the actual content an engineer needs.

**Type and label consistency:** Labels match across this plan: `sec:three-faces`, `sec:quantifying-noise`, `sec:boolean-universe-first-look`, `sec:sampling-rates`, `sec:why-atom` appear consistently in Tasks 2-6 and in the Cross-Reference Map table. The two labels that close existing forward references from chapters 2-4 (`sec:three-faces`, `sec:boolean-universe-first-look`) match what chapters 2-4 are already referencing (verified by `grep` against the existing chapter files).

**One gap noted and resolved:** Plan 4 Task 8 exercise 4 is "notebook-tied" but the original spec says "empirical estimation under varying n (notebook-tied)". The notebook in Task 9 covers exactly this experiment (convergence plot), so Exercise 4's prompt should explicitly reference the notebook. Wording in Task 8 reflects this.
