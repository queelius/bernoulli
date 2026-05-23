# Bernoulli Textbook Chapter 8: Information-Theoretic Bounds + Part II Integration (Plan 8)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 8 of Part II (~22 pp): a light-substantive chapter on the information-theoretic lower bound for approximate-set space cost ($-\log_2 \fprate$ bits per element for an FNR-zero set with FPR $\fprate$), the standard Bloom filter's $\approx 1.44$ overhead, and the forward bridge to chapter 14's BHF (the constructive achievement of the entropy floor). Then run the Part II integration check that verifies all cross-references across chapters 5-8 resolve.

**Architecture:** Replace `book/chapters/ch08-information-bounds.tex` stub with a fully drafted chapter containing 6 sections, a learning-outcomes opener, 10-12 exercises, supporting bibliographic entries, and a paired light Python notebook (`python/notebooks/ch08-information-bounds.ipynb`) that plots entropy floor vs Bloom cost across $\fprate$ and shows the 44% overhead empirically.

**Tech Stack:** LaTeX (book class), alex.sty notation, biblatex+biber. Python 3.11+ + numpy + matplotlib + scipy (now tracked since Plan 7) for the light notebook.

**Scope:** Chapter 8 + Part II integration check. After Plan 8, Part II is complete (Milestone 1's Part II portion of the textbook).

**Spec source of truth:** `docs/superpowers/specs/2026-05-17-bernoulli-textbook-part2-design.md` §3.4 (chapter 8 light substantive) and §4 (chapter 8 row).

**Base SHA:** `31a8d0e` (HEAD at end of Plan 7).

**Source material:**
- `papers/bernoulli_entropy/sections/entropy.tex` (the entropy lower-bound theorem)
- `papers/bernoulli_entropy/sections/space_complexity.tex` (the standard-Bloom gap to the floor)
- `book/chapters/ch02/bsc.tex` (§2.1 BSC for chapter 8 §8.2 channel capacity context)
- `book/chapters/ch05/bloom-from-scratch.tex` (§5.2; Bloom filter for the gap calculation)
- `book/chapters/ch05/one-sided-two-sided.tex` (§5.4; perfect-filter line, FNR-zero axis)

**Lessons inherited from Plans 1-7:**

1. **Page discipline.** Chapter 8 target ~22pp; expect 24-28pp realistic. The chapter is "light substantive": the entropy floor's PROOF can be sketched (chapter 8 §8.3 spec note); only the entropy floor's STATEMENT and its consequences need rigorous treatment.

2. **Soul-voice hook (BLOCKING):** Respect the full banned-phrase list from the soul hook. The hook does substring matching, so watch for accidental joins like "th." + ".the intersection of" across word boundaries; prefer "intersecting" or rephrase when set intersection appears next to a word ending in "t".

3. **Notation:** alex.sty macros throughout. The chapter-2 BSC notation ($Q$, channel matrix) returns in §8.2. The chapter-5 Bloom notation $(m, k, n)$ returns in §8.4. New macros for entropy: $H(X)$, $I(X;Y)$, $C$ (capacity). Verify alex.sty has these in Task 0; add `\providecommand` blocks if missing.

4. **Chapter 8 is the "light" chapter.** Per master spec, the notebook is light (one experiment: entropy floor vs Bloom cost across $\fprate$, ratio plot). The entropy-floor theorem PROOF can be sketched if necessary; the standard-Bloom $\log_2 e \approx 1.44$ overhead must be derived rigorously. Pedagogical priority: the reader must WANT chapter 14 by the end of chapter 8.

5. **The Part II integration check (Task 10)** mirrors Plan 4 Task 10's structure: verify full book builds cleanly, count undefined references (expect ZERO new, plus the known `ch:composition` Part-II-internal label and any chapter-2/Part-III forward references already in the build), confirm running threads, soul-voice audit, page-count audit per chapter.

---

## File Structure

After this plan completes:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch08-information-bounds.tex          # rewritten from stub
│   │   └── ch08/                                # NEW directory
│   │       ├── entropy-refresher.tex            # §8.1 (~3 pp)
│   │       ├── bsc-capacity.tex                 # §8.2 (~3 pp)
│   │       ├── entropy-floor.tex                # §8.3 (~6 pp) - the headline theorem
│   │       ├── bloom-gap.tex                    # §8.4 (~4 pp)
│   │       ├── what-comes-next.tex              # §8.5 (~2 pp)
│   │       ├── bibliographic-notes.tex          # §8.6 (~2 pp)
│   │       └── exercises.tex                    # 10-12 exercises (~2 pp)
│   ├── preamble.tex                             # may be extended with entropy macros
│   └── references.bib                           # may be extended (bernoulli-entropy paper)
└── python/
    └── notebooks/
        └── ch08-information-bounds.ipynb        # light notebook: entropy floor vs Bloom cost
```

---

## Cross-Reference Map (Plan 8 closing inventory)

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:information-bounds` | `ch08-information-bounds.tex` (Plan 0 stub) | chapter 5 §5.5 forward, chapter 6 §6.5 forward, chapter 7 §7.5 forward |
| `sec:entropy-refresher` | `ch08/entropy-refresher.tex` (Task 2) | (internal) |
| `sec:bsc-capacity` | `ch08/bsc-capacity.tex` (Task 3) | (internal) |
| `sec:entropy-floor` | `ch08/entropy-floor.tex` (Task 4) | (internal); chapter 14 backward |
| `sec:bloom-gap` | `ch08/bloom-gap.tex` (Task 5) | (internal); chapter 14 backward |
| `sec:ch8-what-comes-next` | `ch08/what-comes-next.tex` (Task 6) | (internal) |
| `thm:entropy-floor` | `ch08/entropy-floor.tex` (Task 4) | chapter 14 backward |

Backward references (all resolve):
- Chapter 2: `\Cref{ch:binary-channels}`, `\Cref{sec:bsc}`, `\Cref{def:bsc}`
- Chapter 5: `\Cref{ch:approximate-sets}`, `\Cref{def:bloom-filter}`, `\Cref{thm:bloom-optimal-k}`, `\Cref{sec:one-sided-two-sided}`, `\Cref{def:one-sided}`
- Chapter 6 if needed: `\Cref{sec:perfect-filter-line}`, `\Cref{def:perfect-filter-line}`
- Chapter 7 if needed: cross-walks back

Forward references via `\Cref{ch:N}`: chapter 14 (Optimal Bernoulli Sets / BHF), chapter 15 (perfect hash filters).

---

## Per-Task Drafting Discipline

Standard Path A pattern. Per-task review cycle: spec-compliance reviewer + quality reviewer (or combined for shorter sections); fix subagent if substantive issues surface.

---

## Tasks

### Task 0: Verify macro coverage

**Purpose:** Confirm alex.sty has macros for $H, I, C$ (entropy, mutual information, capacity); extend `book/preamble.tex` if not.

- [ ] Grep alex.sty:
```bash
grep -nE "\\\\Entropy|\\\\MutualInfo|\\\\Capacity|\\\\providecommand.*H|\\\\newcommand.*\\\\H\\b" book/alex.sty
```

- [ ] If $H, I, C$ macros are missing, extend `book/preamble.tex`:

```latex
% Information-theory macros for Part II chapter 8.
\providecommand{\Entropy}{H}
\providecommand{\MutualInfo}{I}
\providecommand{\Capacity}{C}
```

(These render as upright capitals matching the information-theory convention. If alex.sty has alternates, use those; otherwise add the providecommand.)

- [ ] Build to verify (`cd book && make cleanall && make`, exit 0).

- [ ] Commit IF preamble was modified; otherwise skip:

```
book: extend preamble with information-theory macros for chapter 8

Add \providecommand blocks for H, I, C (entropy, mutual information,
channel capacity) as chapter 8 will use them. alex.sty is shared with
the papers and not modified.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 1: Read sources and write chapter scaffolding

- [ ] Read source files: `papers/bernoulli_entropy/sections/entropy.tex` and `space_complexity.tex`, `book/chapters/ch02/bsc.tex` (BSC context), `book/chapters/ch05/bloom-from-scratch.tex` and `one-sided-two-sided.tex` (Bloom/perfect-filter context). Plus Part II spec §3.4 and §4 chapter 8 row.

- [ ] Replace `book/chapters/ch08-information-bounds.tex` with the scaffold:

```latex
\chapter{Information-Theoretic Bounds}
\label{ch:information-bounds}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item State Shannon entropy $\Entropy(X)$ and channel capacity for
    the BSC; relate them to the noisy-bit object of Part~I.
  \item Derive the $-\log_2 \fprate$ bits-per-element lower bound for
    any FNR-zero approximate set with false-positive rate $\fprate$.
  \item Quantify the standard Bloom filter's $\approx 1.44 \times$
    space overhead relative to the entropy floor, and identify the
    construction (chapter~14's BHF) that closes the gap.
\end{itemize}
\end{quote}

% Section 8.1
\input{chapters/ch08/entropy-refresher}

% Section 8.2
\input{chapters/ch08/bsc-capacity}

% Section 8.3
\input{chapters/ch08/entropy-floor}

% Section 8.4
\input{chapters/ch08/bloom-gap}

% Section 8.5
\input{chapters/ch08/what-comes-next}

% Section 8.6
\input{chapters/ch08/bibliographic-notes}

% Exercises
\input{chapters/ch08/exercises}
```

- [ ] Create `book/chapters/ch08/` + 7 placeholders: `entropy-refresher.tex`, `bsc-capacity.tex`, `entropy-floor.tex`, `bloom-gap.tex`, `what-comes-next.tex`, `bibliographic-notes.tex`, `exercises.tex`. Each: `% Placeholder. Drafted in Plan 8 Task N.` with N substituted (2..8).

- [ ] Build (exit 0).

- [ ] Commit:

```
book: scaffold chapter 8 (information-theoretic bounds) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener (three bullets: entropy and BSC capacity, the entropy floor
for FNR-zero sets, the standard Bloom 1.44x overhead), six section
subfile inputs plus exercises, with matching empty placeholders.
Section drafts land in subsequent Plan 8 tasks.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §8.1 Shannon Entropy Refresher (~3 pp)

**Files:** Modify `book/chapters/ch08/entropy-refresher.tex`.

**Purpose:** One-page Shannon entropy refresher (no derivations beyond the most basic), the binary entropy function $H(p) = -p \log_2 p - (1-p)\log_2(1-p)$, mutual information $I(X;Y)$, and BSC entropy $H(\fprate)$. Stated, not derived. Cover-Thomas as the depth reference.

**Content checklist (4 items):**

1. **What is entropy?** $H(X) = -\sum_{x} \Pr[X = x] \log_2 \Pr[X = x]$. Units: bits. The "average number of yes/no questions needed to identify $X$." One paragraph + formula.

2. **Binary entropy function.** $H(p) = -p \log_2 p - (1-p)\log_2(1-p)$ for $p \in [0, 1]$. Concave; maximum $1$ at $p = 1/2$; $H(0) = H(1) = 0$. Half a page (formula + a few sentences).

3. **Mutual information (brief).** $I(X;Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)$. Symmetric in $X, Y$. Measures how much $X$ tells you about $Y$. Half a page.

4. **The chapter's plan.** §8.2 uses these tools to derive BSC capacity. §8.3 uses them to derive the entropy floor for approximate-set space cost. One paragraph.

**Labels:** `\section{Shannon Entropy Refresher}` with `\label{sec:entropy-refresher}`.

**Header cross-reference comment block.**

**Target length:** ~3 pp (700-900 prose words).

**Workflow:** Standard. Commit:

```
book: draft chapter 8.1 Shannon Entropy Refresher (~3 pp)

One-page Shannon entropy refresher: H(X), the binary entropy function
H(p) with its concavity and unit-bit-at-p=1/2 maximum, mutual
information I(X;Y) as the symmetric reduction in uncertainty. Stated
without derivation; Cover and Thomas as the depth reference.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 3: §8.2 Channel Capacity in the BSC (~3 pp)

**Files:** Modify `book/chapters/ch08/bsc-capacity.tex`.

**Source reading:** `book/chapters/ch02/bsc.tex` (chapter 2's BSC formal definition); `book/chapters/ch01/three-faces.tex` (the BSC running thread).

**Purpose:** Apply §8.1's tools to derive the BSC capacity $C = 1 - H(\fprate)$. Connect to the BSC running thread from Part I.

**Content checklist (4 items):**

1. **Recall the BSC.** Cross-reference `\Cref{sec:bsc}` and `\Cref{def:bsc}`. Input $X \in \{\top, \bot\}$, output $Y \in \{\top, \bot\}$, crossover $\fprate$. Channel matrix $Q$ symmetric. One paragraph.

2. **Capacity definition.** $C = \max_{P_X} I(X;Y)$, the maximum mutual information over input distributions. For the BSC, the maximum is achieved at the uniform input ($P_X(\top) = P_X(\bot) = 1/2$). One paragraph.

3. **The result.** $C = 1 - H(\fprate)$. Derivation sketch: $H(Y|X) = H(\fprate)$ (the output uncertainty given input is just the BSC's flip uncertainty); $H(Y) = 1$ at the uniform input (output is also uniform); $I(X;Y) = H(Y) - H(Y|X) = 1 - H(\fprate)$. One page.

4. **Interpretation.** At $\fprate = 0$ (no noise): $C = 1$ (one bit per channel use). At $\fprate = 1/2$ (maximum noise): $C = 0$ (no information). Plot $C$ vs $\fprate$. The BSC running thread's quantitative summary. Half a page.

5. **Forward bridge.** The Shannon source-coding theorem says any encoding of $n$ random binary source symbols requires at least $n H(p)$ bits (where $p$ is the source's bit-1 frequency). §8.3 applies this to approximate-set representation: the bits in the bitmap have a constrained distribution governed by $\fprate$ that forces a per-element entropy floor. One paragraph.

**Labels:** `\section{Channel Capacity in the BSC}` with `\label{sec:bsc-capacity}`. Proposition: `\label{prop:bsc-capacity}`.

**Header cross-reference comment block.**

**Target length:** ~3 pp (700-900 prose words).

**Workflow:** Standard. Commit:

```
book: draft chapter 8.2 Channel Capacity in the BSC (~3 pp)

Recall §2.1's BSC; capacity definition C = max_P I(X;Y) over input
distributions; derivation sketch that the BSC capacity is
C = 1 - H(fpr), achieved at uniform input. Plot C vs fpr showing
endpoints (1 at fpr=0, 0 at fpr=1/2). Forward bridge to §8.3:
Shannon source-coding underlies the entropy floor for approximate
sets.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 4: §8.3 The Entropy Floor for Approximate Sets (~6 pp)

**Files:** Modify `book/chapters/ch08/entropy-floor.tex`.

**Source reading:** `papers/bernoulli_entropy/sections/entropy.tex` (the lower-bound theorem). This is the chapter's most substantive section.

**Purpose:** State and prove (or sketch) the entropy lower bound: any FNR-zero approximate set with false-positive rate $\fprate$ over a universe of size $|\Universe| = N$ representing a set $A$ with $|A| = n$ requires at least $n \log_2(1/\fprate) = -n \log_2 \fprate$ bits to represent. State as a theorem with `\label{thm:entropy-floor}`.

**Content checklist (6 items):**

1. **Setup.** Universe $\Universe$ with $|\Universe| = N$. The reader's true set $A \subseteq \Universe$ with $|A| = n$. An approximate-set representation $R$ (a bit-string of length $L$) plus a query algorithm $\mathrm{query}(R, x)$ returning $\top$ or $\bot$. The approximate set is FNR-zero if every $x \in A$ has $\mathrm{query}(R, x) = \top$. It has FPR $\fprate$ if $\Pr_{x \sim \Universe \setminus A}[\mathrm{query}(R, x) = \top] \le \fprate$ (under uniform sampling). One page.

2. **Theorem statement.** For any FNR-zero approximate-set representation $R$ of $A$ with FPR $\le \fprate$, $L \ge n \log_2(1/\fprate)$. State with `\label{thm:entropy-floor}`. One paragraph.

3. **Proof sketch (the section's core).** Counting argument:
   - For any representation $R$, the query algorithm partitions $\Universe$ into the "accepted" set $A_R = \{x : \mathrm{query}(R, x) = \top\}$.
   - FNR-zero means $A \subseteq A_R$.
   - FPR $\le \fprate$ means $|A_R \setminus A| \le \fprate \cdot |\Universe \setminus A| \approx \fprate \cdot N$ (for $N \gg n$).
   - So $|A_R| \le n + \fprate N$. With $\fprate$ small and $N \gg n$, the dominant term may flip; the result is more delicate. The standard form requires that across all possible $A$ with $|A| = n$, the number of possible $A_R$ is at least $\binom{N}{n}$.
   - Counting how many $A_R$ a given $R$ can produce, and how many $R$ are required to cover all $\binom{N}{n}$ choices of $A$, gives $2^L \ge \binom{N}{n} / \binom{N}{|A_R|}$, and asymptotic analysis yields $L \ge n \log_2(1/\fprate)$.
   - The full derivation is in Carter-Wegman 1978 and reformulated in the `towell-bernoulli-entropy` paper. Sketch the argument; refer to the paper for the full proof. Two pages.

4. **Form of the bound.** $L / n \ge -\log_2 \fprate$ bits per element. At $\fprate = 0.01$: $\log_2(100) \approx 6.64$ bits per element minimum. At $\fprate = 0.001$: $\approx 9.97$ bits. Half a page.

5. **Discussion: why is the floor in $\fprate$ and not also in $\fnrate$?** The theorem is for FNR-zero approximate sets specifically. Two-sided approximate sets can drop below this floor by spreading error across both directions; the bound for general two-sided sets involves both rates. One page (state without proof; refer forward to chapter 14).

6. **Connection to chapter 14.** Chapter 14's BHF achieves this floor (asymptotically). The standard Bloom filter falls $\approx 1.44 \times$ short; §8.4 derives this gap. One paragraph.

**Labels:** `\section{The Entropy Floor for Approximate Sets}` with `\label{sec:entropy-floor}`. Theorem `\label{thm:entropy-floor}`.

**Header cross-reference comment block.**

**Target length:** ~6 pp (1400-1800 prose words; the proof sketch is the longest single block).

**Workflow:** Standard. Commit:

```
book: draft chapter 8.3 The Entropy Floor for Approximate Sets (~6 pp)

The chapter's headline theorem (thm:entropy-floor): any FNR-zero
approximate set with FPR fpr requires at least n log_2(1/fpr) bits.
Proof sketched via the counting argument (any representation R
defines an accepted superset A_R of A; the number of A_R that any
single R can describe vs the number of A's that need representing
gives the bound). Full derivation deferred to the bernoulli-entropy
paper. Form of the bound: -log_2(fpr) bits per element. Brief
discussion of why the floor is asymmetric in fpr vs fnr.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 5: §8.4 The Bloom Filter's Gap (~4 pp)

**Files:** Modify `book/chapters/ch08/bloom-gap.tex`.

**Source reading:** `papers/bernoulli_entropy/sections/space_complexity.tex`; `book/chapters/ch05/bloom-from-scratch.tex` (§5.2's optimal-$k$ result).

**Purpose:** Compute the standard Bloom filter's actual space cost and compare to the floor. Derive the $\log_2 e \approx 1.443$ overhead constant.

**Content checklist (5 items):**

1. **Setup.** §5.2's optimal Bloom filter: $m$ bits, $n$ items, optimal $k = (m/n)\ln 2$. The minimum $\fprate$ achievable is $\fprate^* = 2^{-(m/n)\ln 2}$. One paragraph.

2. **Invert: bits per element at target FPR.** Solve $\fprate = 2^{-(m/n)\ln 2}$ for $m/n$: $m/n = \log_2(1/\fprate) / \ln 2 = \log_2(1/\fprate) \cdot \log_2 e$. One paragraph.

3. **Compare to the floor.** Entropy floor (§8.3): $m_{\min}/n = -\log_2 \fprate = \log_2(1/\fprate)$ bits per element. Bloom: $m/n = \log_2(1/\fprate) \cdot \log_2 e$. Ratio: $\log_2 e \approx 1.4427$. Half a page.

4. **The 44% overhead in absolute terms.** At $\fprate = 0.01$: floor is $\approx 6.64$ bits/element, Bloom is $\approx 9.59$ bits/element, gap is $\approx 2.95$ bits/element. At $\fprate = 0.001$: floor $\approx 9.97$, Bloom $\approx 14.38$, gap $\approx 4.41$. The overhead grows in absolute terms as $\fprate$ shrinks. Half a page.

5. **The gap is structural.** The standard Bloom filter pays the overhead because it uses $k$ independent hash functions and treats each hash position as independent. A constructive scheme that achieves the floor must abandon the "$k$ independent hashes into a flat bitmap" structure and use a more structured representation (chapter 14's BHF uses perfect-hash-based encoding). Half a page.

6. **Forward bridge.** §8.5 surveys what comes next; chapter 14 closes the gap. Half a paragraph.

**Labels:** `\section{The Bloom Filter's Gap}` with `\label{sec:bloom-gap}`. Proposition `\label{prop:bloom-overhead}`.

**Header cross-reference comment block.**

**Target length:** ~4 pp (900-1200 prose words).

**Workflow:** Standard. Commit:

```
book: draft chapter 8.4 The Bloom Filter's Gap (~4 pp)

Compute the standard Bloom filter's actual space cost from §5.2's
optimal-k result: m/n = log_2(1/fpr) * log_2 e bits per element.
Compare to §8.3's entropy floor: m_min/n = log_2(1/fpr) bits per
element. Ratio: log_2 e ≈ 1.443, the standard "44% overhead"
constant of the Bloom-filter literature. Absolute overhead at
fpr = 0.01 is 2.95 bits/element; at fpr = 0.001 is 4.41 bits/element.
The gap is structural (k independent hashes into a flat bitmap);
chapter 14's BHF abandons this structure to close the gap.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 6: §8.5 What Comes Next (~2 pp)

**Files:** Modify `book/chapters/ch08/what-comes-next.tex`.

**Purpose:** Brief signpost forward. Names Part III (chapters 9-13: maps, sketches, randomized algorithms, relations, algebraic types) and the constructive closing of Parts IV-V (chapter 14 BHF, chapter 15 perfect hash filters).

**Content checklist (4 items):**

1. **Closing Part II.** Part II started with the approximate set as a noisy bit per universe element (chapter 5). It developed the algebra (chapter 6), the proper estimation of rates and derived measures (chapter 7), and the information-theoretic floor (this chapter). The atom is now fully understood at the set level. One paragraph.

2. **Part III: maps.** Chapter 9 lifts $\Bernoulli{\BoolType}$ to $\Bernoulli{T}$ for arbitrary algebraic types $T$. The model-order ceiling at 2 (chapter 2) lifts; n-ary channels appear. Chapters 10-13 develop sketches, randomized algorithms, relations, and the formal algebraic-type framework. One paragraph.

3. **Part IV: optimal constructions.** Chapter 14 constructs the BHF, the approximate set that achieves the §8.3 entropy floor. Chapter 15 constructs perfect hash filters (the FPR-zero counterpart). One paragraph.

4. **Part V: the boundary.** Chapter 16 catalogues what is NOT Bernoulli: systems with correlated errors, time-varying rates, etc. Chapters 17-18 explore cipher maps and encrypted search. One paragraph.

**Labels:** `\section{What Comes Next}` with `\label{sec:ch8-what-comes-next}`.

**Target length:** ~2 pp (400-600 prose words). Short by design.

**Workflow:** Standard. Commit:

```
book: draft chapter 8.5 What Comes Next (~2 pp)

Closing of Part II: the atom is now understood at the set level
(algebra, estimation, information-theoretic floor). Forward-look at
Part III (maps, lifting to general algebraic types T), Part IV
(constructive achievement of the entropy floor via BHF in ch14, FPR-
zero perfect hash filters in ch15), and Part V (chapter 16's
not-Bernoulli boundary, chapters 17-18 on cipher maps and encrypted
search).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 7: §8.6 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch08/bibliographic-notes.tex`; possibly extend `book/references.bib`.

**Content (4 paragraphs):**

1. **`towell-bernoulli-entropy` paper:** the chapter's primary source for the entropy floor. Add bib entry.

2. **Carter-Wegman (1978/1979):** universal hashing and perfect-hashing prior art that informs the floor proof. `\cite{carter-wegman-1979}` (already in bib from Plan 5).

3. **Cover-Thomas (2006):** standard reference for entropy and channel capacity. `\cite{cover-thomas}` (already in bib).

4. **Mitzenmacher (2002) "Compressed Bloom Filters":** the line of work showing that compression can recover part of the 1.44 overhead; useful pointer for readers who want to know more before chapter 14's full BHF treatment. Add bib entry if cited.

**New bib entries:**

```bibtex
@misc{towell-bernoulli-entropy,
  author = {Alexander Towell},
  title  = {Entropy and space complexity of random approximate sets},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/bernoulli_entropy}}
}

@article{mitzenmacher-2002,
  author  = {Michael Mitzenmacher},
  title   = {Compressed {Bloom} Filters},
  journal = {IEEE/ACM Transactions on Networking},
  volume  = {10},
  number  = {5},
  pages   = {604--612},
  year    = {2002}
}
```

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline{toc}{section}{Bibliographic Notes}` + `\label{sec:bib-notes-ch8}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard. Commit:

```
book: draft chapter 8.6 Bibliographic Notes (~2 pp); extend bib

Attribute the entropy floor to the towell-bernoulli-entropy paper
(new bib entry); cite Carter-Wegman (already in bib) for the
universal-hashing prior art underlying the floor proof;
Cover-Thomas for entropy and channel capacity; Mitzenmacher (2002)
on compressed Bloom filters as a forward pointer to chapter 14.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 8: Chapter 8 Exercises (11)

**Files:** Modify `book/chapters/ch08/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Entropy of biased coin.** Compute $H(p)$ for $p \in \{0.01, 0.5, 0.99\}$.

2. **BSC capacity computation.** For $\fprate \in \{0.01, 0.1, 0.5\}$, compute $C = 1 - H(\fprate)$.

3. **Entropy floor evaluation.** For target $\fprate \in \{0.1, 0.01, 0.001\}$, compute the entropy floor $-\log_2 \fprate$ in bits per element.

**Medium (★★ × 5):**

4. **Notebook-tied gap plot.** Use the chapter 8 notebook (`python/notebooks/ch08-information-bounds.ipynb`) to plot Bloom filter cost vs entropy floor for $\fprate \in [10^{-5}, 10^{-1}]$. Verify the ratio is constant at $\approx 1.443$.

5. **Mutual information of BSC.** Show $I(X; Y) = H(Y) - H(Y|X) = H(P_X(\top)(1-\fprate) + P_X(\bot)\fprate) - H(\fprate)$ for an input distribution $P_X$. Maximize over $P_X$; recover $C = 1 - H(\fprate)$ at $P_X$ uniform.

6. **The 1.44 constant.** Derive that $\log_2 e = 1/\ln 2 \approx 1.443$ by elementary manipulation.

7. **Entropy floor for sparse universes.** If the universe size $N$ is comparable to the set size $n$ (say $N = 10 n$), does the entropy floor still hold in the form $-n \log_2 \fprate$? Discuss the regime where the floor's asymptotic form is accurate vs where finite-$N$ corrections matter.

8. **Two-sided floor.** Sketch (without proof) why an FPR-FNR-symmetric approximate set can have a lower space cost than $-n \log_2 \fprate$ at the same maximum error. (Hint: the two-sided set can split its error budget across both directions, halving each.)

**Challenging (★★★ × 3):**

9. **The floor as a counting argument.** Reproduce the counting-argument proof sketch from §8.3 in your own words, identifying the load-bearing step (the bound on the number of accepting sets $A_R$ that a single representation $R$ can produce).

10. **Compressed Bloom filter.** Mitzenmacher (2002) showed that ARITHMETIC compression of the standard Bloom filter's bit array can recover the 1.44 overhead. Sketch why this works: under the optimal $k$, half the bitmap bits are 1 and half are 0, so the bit array has 1 bit of entropy per array bit; arithmetic compression recovers the $\log_2 e$ overhead by encoding the bitmap at its true entropy rate. Reference Mitzenmacher (2002) for the full argument.

11. **Entropy floor for the union.** §6.1 derived the FPR of $\tilde A \cup \tilde B$. Apply the §8.3 floor to the union: the bits required to represent $A \cup B$ approximately at FPR $\fprate_\cup$ are at least $|A \cup B| \cdot \log_2(1/\fprate_\cup)$. Show this is consistent with the cost of representing $A$ and $B$ separately. Identify when union representation is more efficient than separate representation.

**Workflow:** Standard. Commit:

```
book: draft chapter 8 exercises (11 with star difficulty markers)

3 warm-ups (entropy of biased coin, BSC capacity, entropy floor
evaluation), 5 medium (notebook gap plot, mutual information of BSC,
the 1.44 constant derivation, sparse-universe regime, two-sided
floor sketch), 3 challenging (counting-argument proof retracing,
compressed Bloom filter, entropy floor for the union operation).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 9: Chapter 8 Notebook (`ch08-information-bounds.ipynb`)

**Files:** Create `python/notebooks/ch08-information-bounds.ipynb`. Light notebook per master spec.

**Content checklist (~10 cells):**

1. **Title** (markdown).
2. **Setup** (code): imports + seeded RNG.
3. **Binary entropy function** (code): define `H(p)`; plot $H(p)$ vs $p \in [0, 1]$.
4. **BSC capacity** (code): plot $C(\fprate) = 1 - H(\fprate)$ vs $\fprate \in [0, 0.5]$.
5. **Entropy floor vs Bloom cost** (code): for $\fprate \in [10^{-5}, 10^{-1}]$ (log-spaced), compute and plot:
   - Floor: $-\log_2 \fprate$ bits per element.
   - Bloom optimal: $\log_2(1/\fprate) \cdot \log_2 e$ bits per element.
   - Plot both as line plots on log-$\fprate$ axis.
6. **The 1.44 ratio** (code): plot the ratio (Bloom cost) / (floor) vs $\fprate$; verify constant at $\approx 1.443$.
7. **Absolute overhead in bits** (code): plot (Bloom cost) $-$ (floor) vs $\fprate$ to show the absolute overhead grows as $\fprate$ shrinks.
8. **Discussion** (markdown): the 44% gap is structural; chapter 14's BHF closes it; chapter 15's BPHF lives on the FPR-zero axis instead.
9. **Open question** (markdown): can the gap be closed without abandoning the bitmap structure? Compressed Bloom filters do recover part of it; full elimination requires BHF (chapter 14).

**Numerical sanity targets:**
- At $\fprate = 0.01$: floor = 6.6439, Bloom = 9.5851, ratio = 1.4427. Verify.
- At $\fprate = 0.001$: floor = 9.9658, Bloom = 14.3776, ratio = 1.4427. Verify.

**Workflow:**

1. Read `python/notebooks/ch07-classification-measures.ipynb` for style.
2. Draft notebook as valid nbformat-4 JSON.
3. Execute:
```bash
cd python && uv run jupyter nbconvert --to notebook --execute notebooks/ch08-information-bounds.ipynb --output ch08-information-bounds.ipynb 2>&1 | tail -20
```
4. Verify outputs.
5. Commit:

```
python: add chapter 8 notebook (information-theoretic bounds)

Light notebook: binary entropy H(p) plot, BSC capacity C(fpr) plot,
entropy floor vs Bloom cost line plot across fpr in [10^-5, 10^-1]
log-spaced, the constant 1.44 ratio plot, absolute-overhead plot.
Verifies the log_2 e overhead at fpr = 0.01 (6.64 floor, 9.59 Bloom)
and fpr = 0.001 (9.97 floor, 14.38 Bloom).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 10: Part II Integration Check

**Purpose:** Mirror Plan 4 Task 10 for Part II. Verify all cross-references across chapters 5-8 resolve under the full book build.

**IMPORTANT CONTEXT:** Two known forward references CANNOT be resolved in Plan 8:
- `ch:composition`: chapter 4's forward reference into Part II (predates Part II drafting; resolves when Part II's composition is fully drafted; chapter 6 §6.3-§6.4 is the relevant content but the label `ch:composition` may not exist; check if it's been renamed to `ch:set-composition`).
- Chapter 16/17/18 forward references from chapters 5-8 (Part V is not yet drafted).

Both are out of scope for Plan 8. Document them in the integration-pass record.

**Steps:**

1. **Clean build.**
```bash
cd book && make cleanall && make
```
Confirm exit 0. Save log to `/tmp/plan8-final-build.log`.

2. **Verify undefined references.**
```bash
grep -n "Reference.*undefined\|Citation.*undefined" book/book.log
```
Expected: ONLY `ch:composition` (if it persists) and possibly chapter-16/17/18 forward references. If any OTHER undefined references, list explicitly.

3. **Verify Part II cross-references.**

Chapter labels (each defined exactly once):
```bash
grep -rn "\\\\label{ch:approximate-sets}\|\\\\label{ch:set-composition}\|\\\\label{ch:classification-measures}\|\\\\label{ch:information-bounds}" book/chapters/
```

Section labels for Part II (chapters 5, 6, 7, 8): verify each section file defines its `\label{sec:...}` exactly once.

Forward references from later sections into earlier (and Part II to Part I): grep for chapter-5 labels in chapters 6-8; chapter-6 in chapter 7-8; chapter-7 in chapter 8.

4. **Page-count audit.**
```bash
pdfinfo book/book.pdf | grep Pages
```

Per-chapter page counts for chapters 5-8 from `book.toc`. Verify each is within $\pm 30\%$ of spec target:
- Chapter 5: ~28pp target, allow 22-37
- Chapter 6: ~24pp target, allow 19-31
- Chapter 7: ~28pp target, allow 22-37
- Chapter 8: ~22pp target, allow 17-29

Total Part II should be ~110pp.

5. **Running threads inventory.**

Bloom filter (Part II's running example) should appear in chapters 5, 6, 7, 8 (all four). BSC thread should appear in chapter 8 §8.2.

```bash
echo "=== Bloom filter ==="
grep -rln -i "bloom filter" book/chapters/ch05/ book/chapters/ch06/ book/chapters/ch07/ book/chapters/ch08/
echo "=== BSC ==="
grep -rln "binary symmetric channel\|\\bBSC\\b" book/chapters/ch08/
```

6. **Soul-voice audit.**
```bash
python3 -c "
import re, glob
files = glob.glob('book/chapters/ch0[5678]/**/*.tex', recursive=True) + glob.glob('book/chapters/ch0[5678]-*.tex')
bad = False
for f in files:
    with open(f, encoding='utf-8') as fh:
        text = fh.read()
    if chr(0x2014) in text:
        print(f'FAIL: em-dash in {f}'); bad = True
    if re.search(r'\blever\s*age\b', text, re.IGNORECASE):
        print(f'FAIL: lever+age in {f}'); bad = True
    banned_buzzword_substr = 'at' + ' the ' + 'inter' + 'section of'
    if banned_buzzword_substr in text.lower():
        print(f'FAIL: buzzword crossroad-substring in {f}'); bad = True
print('audit complete' if not bad else 'AUDIT FOUND VIOLATIONS')
"
```

7. **Write and commit the integration-pass record** at `docs/superpowers/plans/2026-05-22-bernoulli-textbook-ch08-information-bounds-integration-pass.md` documenting:
- Clean build (PASS/FAIL)
- Undefined references (the known `ch:composition` plus any others)
- Per-chapter page counts
- Running-thread inventory
- Soul-voice audit results
- Open follow-ups (for the polish plan)

Commit:

```
book: Part II integration pass record (Plan 8 close)

Records the final integration verification for Part II (chapters 5-8):
clean build, undefined references limited to known pre-existing forward
references, all chapter 5-8 cross-references resolve, Bloom filter
thread carries through all four chapters, soul-voice hook audit clean.
Per-chapter page counts and noted follow-ups for the polish plan.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Self-Review

Spec coverage:
- Part II spec §4 chapter 8 row: each section has its own task.
- Part II spec §3.4 (chapter 8 "light substantive"): §8.3 proof is sketched (not full) per the spec.
- Master spec exercise discipline: Task 8.
- Master spec light notebook: Task 9.
- Part II integration check: Task 10 (mirrors Plan 4 Task 10).

Placeholder scan: none.

Type and label consistency: chapter 5/6/7 labels are correctly invoked from chapter 8 backward references; chapter 14/15 forward references use existing `\Cref{ch:N}` from Plan 0 stubs.
