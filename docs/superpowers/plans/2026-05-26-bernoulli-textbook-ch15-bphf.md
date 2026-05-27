# Bernoulli Textbook Chapter 15: Perfect Hash Filters (BPHF) (Plan 15)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 15 of Part IV (~28 pp): the FPR-zero axis counterpart to chapter 14's BHF. The Bernoulli Perfect Hash Filter (BPHF) gives constructive realization on the perfect-filter line's FPR-zero side, with ranked search as the canonical application.

**Architecture:** Replace `book/chapters/ch15-perfect-hash-filters.tex` stub with a fully drafted chapter containing 6 sections, learning-outcomes opener, 10-12 exercises, bibliographic entries, paired notebook. Plan 15 closes Part IV.

**Tech Stack:** LaTeX (book class), alex.sty, biblatex+biber. Python 3.11+ for notebook (BPHF + ranked-search demo).

**Scope:** Chapter 15 only. Part IV integration check at Task 10 (mirrors Plans 4/8/13 integration patterns).

**Spec source of truth:** `docs/superpowers/specs/2026-05-25-bernoulli-textbook-part4-design.md` §4 chapter 15 row.

**Base SHA:** `d28faf0` (HEAD at end of Plan 14).

**Source material:**
- `papers/bernoulli-phf/` (primary source; the BPHF paper with embedded library)
- `book/chapters/ch14/` (the BHF predecessor; chapter 15 mirrors structure on the FPR-zero axis)
- `book/chapters/ch06/perfect-filter-line.tex` (§6.4 perfect-filter-line concept)
- `book/chapters/ch08/entropy-floor.tex` (§8.3 floor that BPHF parallels on the FPR-zero side)
- Carter-Wegman, BBHash, BDZ perfect-hashing literature (already cited in chapter 14)

**Lessons inherited from Plans 1-14:**

1. **Page discipline.** Chapter 15 target ~28pp; expect 30-34pp.

2. **Soul-voice hook (BLOCKING):** Respect the full banned-phrase list at `$CLAUDE_PLUGIN_ROOT/hooks/check-banned-phrases.sh`. Substring matching applies.

3. **Notation:** $\phi$ for perfect hash function (chapter 14 carry-over); rank value $\rho(a)$ for the per-element data BPHF stores; $r$ for the number of bits per rank; $A$ for designated set; $n = |A|$.

4. **Chapter 14 is the structural template.** Each chapter 15 section mirrors a chapter 14 counterpart on the FPR-zero axis. The two chapters together are the constructive dual of Parts II-III's analytical foundation.

5. **Ranked search is the BPHF's "killer app."** Chapter 14's BHF answers membership; chapter 15's BPHF answers ranked retrieval (top-k). §15.4 makes this concrete.

---

## File Structure

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch15-perfect-hash-filters.tex      # rewritten from stub
│   │   └── ch15/                               # NEW directory
│   │       ├── bhf-to-bphf.tex                 # §15.1 (~3 pp)
│   │       ├── bphf-construction.tex           # §15.2 (~7 pp)
│   │       ├── space-time-analysis.tex         # §15.3 (~5 pp)
│   │       ├── ranked-search.tex               # §15.4 (~6 pp)
│   │       ├── bridge-to-part5.tex             # §15.5 (~2 pp)
│   │       ├── bibliographic-notes.tex         # §15.6 (~2 pp)
│   │       └── exercises.tex                   # 10-12 exercises (~2 pp)
│   └── references.bib                          # extended (towell-bernoulli-phf paper)
└── python/
    └── notebooks/
        └── ch15-bphf.ipynb                     # BPHF construction + ranked-search demo
```

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:perfect-hash-filters` | `ch15-perfect-hash-filters.tex` (Plan 0 stub) | (forward refs from ch5, ch6, ch14 already exist) |
| `sec:bhf-to-bphf` | `ch15/bhf-to-bphf.tex` (Task 2) | (internal) |
| `sec:bphf-construction` | `ch15/bphf-construction.tex` (Task 3) | (internal) |
| `sec:space-time-analysis` | `ch15/space-time-analysis.tex` (Task 4) | (internal) |
| `sec:ranked-search` | `ch15/ranked-search.tex` (Task 5) | (internal) |
| `sec:bridge-to-part5` | `ch15/bridge-to-part5.tex` (Task 6) | (internal) |
| `def:bphf` | `ch15/bphf-construction.tex` (Task 3) | (internal) |

Backward references that should resolve:
- Chapter 14: `\Cref{def:bhf}`, `\Cref{sec:bhf-construction}`, `\Cref{thm:bhf-optimality}`, `\Cref{prop:bhf-fpr}`
- Chapter 8: `\Cref{thm:entropy-floor}`
- Chapter 6: `\Cref{def:perfect-filter-line}`, `\Cref{def:one-sided}` (chapter 5)
- Chapter 5: `\Cref{def:bloom-filter}`

---

## Tasks

### Task 1: Read sources and write chapter scaffolding

- [ ] Read sources: `papers/bernoulli-phf/` (skim including embedded library README); `book/chapters/ch14/` (all section files for structural template); `book/chapters/ch06/perfect-filter-line.tex` (§6.4); `book/chapters/ch08/entropy-floor.tex` (§8.3); Part IV spec §4 chapter 15.

- [ ] Replace `book/chapters/ch15-perfect-hash-filters.tex` with the scaffold:

```latex
\chapter{Perfect Hash Filters (BPHF)}
\label{ch:perfect-hash-filters}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item State the Bernoulli Perfect Hash Filter (BPHF) construction
    as the FPR-zero counterpart of chapter~14's BHF on the
    perfect-filter line of \Cref{def:perfect-filter-line}.
  \item Derive its space and time costs, and the false-negative-rate
    structure that lets ranked search recover top-$k$ items at
    bounded miss probability.
  \item Apply BPHF to ranked retrieval and recognize when it is the
    right tool versus standard membership filters.
\end{itemize}
\end{quote}

% Section 15.1
\input{chapters/ch15/bhf-to-bphf}

% Section 15.2
\input{chapters/ch15/bphf-construction}

% Section 15.3
\input{chapters/ch15/space-time-analysis}

% Section 15.4
\input{chapters/ch15/ranked-search}

% Section 15.5
\input{chapters/ch15/bridge-to-part5}

% Section 15.6
\input{chapters/ch15/bibliographic-notes}

% Exercises
\input{chapters/ch15/exercises}
```

- [ ] Create `book/chapters/ch15/` + 7 placeholder files (`bhf-to-bphf.tex`, `bphf-construction.tex`, `space-time-analysis.tex`, `ranked-search.tex`, `bridge-to-part5.tex`, `bibliographic-notes.tex`, `exercises.tex`). Each: `% Placeholder. Drafted in Plan 15 Task N.` (N = 2-8).

- [ ] Build exit 0. Commit:

```
book: scaffold chapter 15 (perfect hash filters, BPHF) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener (three bullets: BPHF construction as FPR-zero dual of BHF,
space/time analysis with FNR structure, ranked-search application),
six section subfile inputs plus exercises, with matching empty
placeholders.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §15.1 From BHF to BPHF (~3 pp)

**Files:** Modify `book/chapters/ch15/bhf-to-bphf.tex`.

**Content checklist (4 items):**

1. **Recall chapter 14.** BHF lives on the FNR-zero axis of the perfect-filter line (chapter 6 §6.4). It achieves the chapter 8 §8.3 entropy floor: $\fnrate = 0$ exactly, $\fprate \le 2^{-r}$. Half a page; cite `\Cref{def:bhf}`, `\Cref{thm:bhf-optimality}`, `\Cref{prop:bhf-fpr}`, `\Cref{def:perfect-filter-line}`.

2. **The opposite axis.** What if we want $\fprate = 0$ instead (every reported positive is real) at the cost of $\fnrate > 0$ (some real positives missed)? This is the FPR-zero axis. Half a page.

3. **Construction sketch.** Use perfect hash $\phi : A \to [n]$ as before. But instead of storing a fingerprint, store a rank value: $\rho(a) \in [0, 1]$ or a small integer rank. The query algorithm exploits this rank to refuse false positives. One page.

4. **Chapter roadmap.** §15.2 detailed construction; §15.3 space/time; §15.4 ranked search; §15.5 bridge to Part V.

**Labels:** `\section{From BHF to BPHF}` with `\label{sec:bhf-to-bphf}`.

**Header cross-reference comment block.**

**Target length:** ~3 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 3: §15.2 The BPHF Construction (~7 pp)

**Files:** Modify `book/chapters/ch15/bphf-construction.tex`.

**Content checklist (6 items):**

1. **Two ingredients.** Perfect hash $\phi : A \to [n]$ (same as chapter 14). Per-element rank table $R : [n] \to \{0, 1\}^r$ where $r = \lceil \log_2 n \rceil$ bits (enough to distinguish $n$ ranks). Half a page.

2. **Construction.** For each $a \in A$, assign rank $\rho(a) \in [0, n)$ (the position of $a$ in some pre-determined ordering of $A$, e.g., by a secondary hash). Store $R[\phi(a)] := \rho(a)$. One page.

3. **Query.** For query $x$: compute $\phi(x) \in [n]$; recover candidate rank $R[\phi(x)]$; verify: does the rank "make sense" for $x$? Specifically: there must be an a-priori check that the rank value at slot $\phi(x)$ matches what $x$'s rank would be IF $x \in A$. If the check fails, return $\bot$ (correctly rejecting $x \notin A$). If it passes, return $\top$ (with a small false-negative possibility for some $a \in A$). One page with pseudocode in `algorithm2e`.

4. **Why $\fprate = 0$.** The construction's check eliminates false positives by design. Half a page.

5. **The $\fnrate > 0$ trade-off.** Some real members $a \in A$ may fail the check (e.g., if their rank collides ambiguously). Derive $\fnrate \le 2^{-r}$ for the standard construction. One page.

6. **Worked example.** $A = \{a_1, \ldots, a_{1000}\}$, $r = 10$ bits per rank, total $10000$ bits + perfect-hash overhead. $\fprate = 0$ exactly; $\fnrate \le 2^{-10} \approx 0.001$. One page.

**Labels:** `\section{The BPHF Construction}` with `\label{sec:bphf-construction}`. Definition `\label{def:bphf}`.

**Header cross-reference comment block.**

**Target length:** ~7 pp (1600-1900 prose words).

**Workflow:** Standard.

---

### Task 4: §15.3 Space and Time Analysis (~5 pp)

**Files:** Modify `book/chapters/ch15/space-time-analysis.tex`.

**Content checklist (5 items):**

1. **Space.** Rank table: $n r$ bits with $r = \lceil \log_2 n \rceil$. Perfect-hash overhead: same as chapter 14, $o(1)$ per element asymptotically. Total: $\log_2 n + o(1)$ bits per element. One page.

2. **Comparison to chapter 14 BHF.** BHF: $\lceil -\log_2 \fprate \rceil$ bits per element. BPHF: $\lceil \log_2 n \rceil$ bits per element. The two costs are different functions: BHF scales with target error rate, BPHF scales with set size. State as proposition `\label{prop:bphf-space}`. One page.

3. **Construction time.** $O(n)$ expected (same perfect-hash time + one-pass rank assignment).

4. **Query time.** $O(1)$ (hash + table lookup + comparison).

5. **The bit-cost picture.** A table comparing BHF and BPHF at $n = 10^6$:
   - BHF at $\fprate = 0.01$: $r = 7$ bits/element.
   - BPHF at $n = 10^6$: $r = 20$ bits/element.
   - BPHF costs more bits per element but in exchange gives $\fprate = 0$. Half a page.

**Labels:** `\section{Space and Time Analysis}` with `\label{sec:space-time-analysis}`. Proposition `\label{prop:bphf-space}`.

**Header cross-reference comment block.**

**Target length:** ~5 pp (1100-1500 prose words).

**Workflow:** Standard.

---

### Task 5: §15.4 Ranked Search Application (~6 pp)

**Files:** Modify `book/chapters/ch15/ranked-search.tex`.

**Content checklist (5 items):**

1. **The ranked-search problem.** Given a corpus and query, return the top-$k$ most relevant documents. Exact computation requires scoring all documents. Can a BPHF accelerate? One paragraph.

2. **BPHF for top-$k$.** Pre-compute scores per document, sort, assign rank to each. Build BPHF mapping document IDs to ranks. Query for document $d$: look up rank; if rank $\le k$ AND verification passes, $d$ is in top-$k$. One page.

3. **Why this is FPR-zero appropriate.** A false positive in ranked search means surfacing an irrelevant document as if it were top-$k$. The FPR = 0 guarantee of BPHF eliminates this exactly. Half a page.

4. **The $\fnrate$ cost.** Some top-$k$ documents may be missed due to BPHF's $\fnrate$. Bound the expected number of misses: with $\fnrate = 2^{-r}$ and target $k$ retrievals, expected misses $\le k \cdot 2^{-r}$. Half a page.

5. **Worked example.** Corpus of $n = 10^6$ documents, top-$k = 100$ retrieval, $r = 20$ bits. $\fnrate = 2^{-20} \approx 10^{-6}$. Expected misses $\le 100 \cdot 10^{-6} = 10^{-4}$, essentially zero. The BPHF gives perfect-precision top-$k$ retrieval with near-zero miss rate at $\sim 2.5$ MB total space for a million-doc corpus. Two pages.

**Labels:** `\section{Ranked Search Application}` with `\label{sec:ranked-search}`. Proposition `\label{prop:bphf-ranked-search}` on the expected-miss bound.

**Header cross-reference comment block.**

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 6: §15.5 Bridge to Part V (~2 pp)

**Files:** Modify `book/chapters/ch15/bridge-to-part5.tex`.

**Content (3 items):**

1. **Closing Part IV.** Chapter 14 (BHF) and chapter 15 (BPHF) are the two constructive realizations on the perfect-filter line. Together with chapter 8's entropy floor, they close the analytical-and-constructive picture for one-sided approximate sets.

2. **Part V preview.** Chapter 16 catalogues what is NOT Bernoulli (varying rates, correlated noise, etc.). Chapters 17-18 cover cipher maps and encrypted search, applications drawing on the Bernoulli framework.

3. **§15.6 names antecedents.**

**Labels:** `\section{Bridge to Part V}` with `\label{sec:bridge-to-part5}`.

**Header cross-reference comment block.**

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 7: §15.6 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch15/bibliographic-notes.tex`; extend `book/references.bib`.

**Content (3-4 paragraphs):**

1. **`towell-bernoulli-phf` paper** as primary source. Add bib entry.

2. **Perfect-hashing literature:** Carter-Wegman, Belazzougui et al (both already in bib from earlier chapters).

3. **Ranked-search literature:** Robertson-Spärck Jones probabilistic retrieval; Manning-Raghavan-Schütze chapter on retrieval (already cited in chapter 1 bib).

4. **`maph` C++ library** mentioned briefly as the production implementation (lives in `papers/bernoulli-phf/`).

**New bib entry:**

```bibtex
@misc{towell-bernoulli-phf,
  author = {Alexander Towell},
  title  = {The perfect hash filter},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/bernoulli-phf}}
}
```

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline` + `\label{sec:bib-notes-ch15}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 8: Chapter 15 Exercises (11)

**Files:** Modify `book/chapters/ch15/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **BPHF space for given $n$.** For $n = 10^6$, compute the per-element bit cost of BPHF.

2. **FNR computation.** For $r = 10$ bits per rank, compute the BPHF's FNR bound.

3. **BHF vs BPHF.** State in one paragraph each: when to use BHF, when to use BPHF.

**Medium (★★ × 5):**

4. **Notebook-tied BPHF build.** Use the chapter 15 notebook to build a BPHF for $n = 10000$ items; verify $\fprate = 0$ empirically; measure $\fnrate$.

5. **Top-$k$ miss rate.** For top-$k = 50$ on a corpus of $n = 10^6$ at $r = 16$, derive expected miss count.

6. **BPHF storage vs full index.** For $n = 10^6$ documents with $\log_2 n = 20$ bits each, compute BPHF space (in MB) and compare to a full sorted index ($n \log_2 n$ bits).

7. **Compose BPHF with BHF.** Can a BPHF on set $A$ and a BHF on set $B$ be composed to test "$x \in A$ and $x \in B$"? Sketch the construction and the resulting error rates.

8. **Update cost.** A BPHF on a dynamic ranked corpus: estimate amortized update cost (rank shifts when a document is reinserted).

**Challenging (★★★ × 3):**

9. **BPHF FNR exact derivation.** Derive the exact FNR for BPHF accounting for rank-collision structure (not just the upper bound $2^{-r}$).

10. **Adversarial ranks.** Suppose an adversary chooses the rank function $\rho$. Can they force $\fnrate$ above $2^{-r}$? Discuss.

11. **Hybrid filter.** Design a "hybrid" filter that interpolates between BHF (FNR-zero, low $\fprate$) and BPHF (FPR-zero, low $\fnrate$). What is its operating curve in the $(\fprate, \fnrate)$ plane?

**Target length:** ~2 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 9: Chapter 15 Notebook (`ch15-bphf.ipynb`)

**Files:** Create `python/notebooks/ch15-bphf.ipynb`.

**Content (~12-14 cells):**

1. **Title + setup**: numpy, hashlib, matplotlib.
2. **Reuse perfect-hash builder** from chapter 14 notebook.
3. **BPHF class** (code): `__init__(A, ranks)` builds perfect hash + rank table; `query(x)` returns predicted top-k membership.
4. **FPR=0 verification** (code): for $n = 1000$, query 100000 out-of-set items; verify FPR is exactly 0.
5. **FNR measurement** (code): query each $a \in A$, count misses, compare to bound $2^{-r}$.
6. **Ranked-search demo** (code): synthetic corpus of $n = 10^5$ documents with scores; pre-compute top-100; build BPHF; verify retrieval precision = 1.0.
7. **BHF vs BPHF comparison** (code): for the same set $A$, build both filters; compare per-element space cost and error rates.
8. **Discussion** (markdown): the two filters as constructive duals on the perfect-filter line.

**Numerical sanity targets:**
- FPR exactly 0 on out-of-set queries (assertion).
- FNR within order-of-magnitude of $2^{-r}$.
- Ranked-search precision = 1.0 on the demo corpus.

**Workflow:** Standard. Execute end-to-end.

---

### Task 10: Part IV Integration Check

**Files:** None modified directly; verification + integration-pass record.

Mirrors Plan 4 / Plan 8 / Plan 13 integration patterns.

**Steps:**

1. Clean build: `cd book && make cleanall && make`. Exit 0.
2. Verify undefined references: only the documented pre-existing ones (ch:composition, ch:sketches in ch9 prose).
3. Chapter 14 + 15 labels defined exactly once.
4. Per-chapter page counts within ±30% of spec target (ch14 ~30pp, ch15 ~28pp).
5. Cross-chapter refs (ch15 backward to ch14 + ch6 + ch8) all resolve.
6. Soul-voice audit on Part IV files.
7. Write integration-pass record at `docs/superpowers/plans/2026-05-26-bernoulli-textbook-ch15-bphf-integration-pass.md`.
8. Commit.

**Commit:**

```
book: Part IV integration pass record (Plan 15 close)

Records final integration verification for Part IV (chapters 14-15):
clean build, undefined references limited to documented pre-existing
forward refs, all chapter 14-15 cross-references resolve, BHF/BPHF
running thread carries across the part, soul-voice hook audit clean.
Part IV closes: the constructive realizations on the perfect-filter
line are drafted.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Self-Review

Spec coverage: chapter 15 row each section has its own task; substantive notebook in Task 9; integration check in Task 10.

Type and label consistency: chapter 14 BHF labels referenced; chapter 6 §6.4 perfect-filter-line referenced.
