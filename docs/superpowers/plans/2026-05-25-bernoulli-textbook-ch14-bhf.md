# Bernoulli Textbook Chapter 14: Optimal Bernoulli Sets (BHF) (Plan 14)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 14 of Part IV (~30 pp): the constructive realization of the chapter 8 §8.3 entropy floor. The Bernoulli Hash Function (BHF) is an FNR-zero approximate set that achieves $\lceil -\log_2 \fprate \rceil$ bits per element, closing the $\log_2 e \approx 1.443$ overhead of the standard Bloom filter.

**Architecture:** Replace `book/chapters/ch14-optimal-bernoulli-sets.tex` stub with a fully drafted chapter containing 6 sections, learning-outcomes opener, 10-12 exercises, bibliographic entries, and a paired Python notebook implementing the BHF construction.

**Tech Stack:** LaTeX (book class), alex.sty, biblatex+biber. Python 3.11+ for the notebook (perfect-hash + fingerprint construction).

**Scope:** Chapter 14 only. Part IV integration deferred to Plan 15.

**Spec source of truth:** `docs/superpowers/specs/2026-05-25-bernoulli-textbook-part4-design.md` §4 chapter 14 row.

**Base SHA:** `42ad1d3` (HEAD at end of Plan 13 / Milestone 1).

**Source material:**
- `papers/bernoulli-hash-function/` (primary source; includes embedded `maph` C++ library)
- `book/chapters/ch08/entropy-floor.tex` (§8.3 floor this construction achieves)
- `book/chapters/ch08/bloom-gap.tex` (§8.4 the gap being closed)
- `book/chapters/ch05/bloom-from-scratch.tex` (§5.2 the predecessor)
- `book/chapters/ch06/perfect-filter-line.tex` (§6.4 perfect-filter-line)

**Lessons inherited from Plans 1-13:**

1. **Page discipline.** Chapter 14 target ~30pp; expect 32-36pp.

2. **Soul-voice hook (BLOCKING):** Respect the full banned-phrase list.

3. **Notation:** $\phi$ for perfect hash function; $r = \lceil -\log_2 \fprate \rceil$ for fingerprint bits; $\sigma$ for fingerprint; $A$ for the designated set; $n = |A|$.

---

## File Structure

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch14-optimal-bernoulli-sets.tex      # rewritten from stub
│   │   └── ch14/                                 # NEW directory
│   │       ├── optimality-question.tex           # §14.1 (~3 pp)
│   │       ├── bhf-construction.tex              # §14.2 (~7 pp) the headline
│   │       ├── space-analysis.tex                # §14.3 (~6 pp)
│   │       ├── fpr-analysis.tex                  # §14.4 (~5 pp)
│   │       ├── construction-time.tex             # §14.5 (~4 pp)
│   │       ├── bridge.tex                        # §14.6 (~2 pp)
│   │       ├── bibliographic-notes.tex           # §14.7 (~2 pp)
│   │       └── exercises.tex                     # 10-12 exercises (~2 pp)
│   └── references.bib                            # extended (towell-bernoulli-hash-function exists from Plan 5)
└── python/
    └── notebooks/
        └── ch14-bhf.ipynb                        # BHF construction
```

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:optimal-bernoulli-sets` | `ch14-optimal-bernoulli-sets.tex` (Plan 0 stub) | (forward refs from ch5/6/8 already exist) |
| `sec:optimality-question` | `ch14/optimality-question.tex` (Task 2) | (internal) |
| `sec:bhf-construction` | `ch14/bhf-construction.tex` (Task 3) | (internal); chapter 15 backward |
| `sec:space-analysis` | `ch14/space-analysis.tex` (Task 4) | (internal) |
| `sec:fpr-analysis` | `ch14/fpr-analysis.tex` (Task 5) | (internal) |
| `sec:construction-time` | `ch14/construction-time.tex` (Task 6) | (internal) |
| `sec:ch14-bridge` | `ch14/bridge.tex` (Task 7) | (internal) |
| `def:bhf` | `ch14/bhf-construction.tex` (Task 3) | (internal); chapter 15 backward |
| `thm:bhf-optimality` | `ch14/space-analysis.tex` (Task 4) | (internal) |

Backward references that should resolve:
- Chapter 8: `\Cref{thm:entropy-floor}`, `\Cref{sec:entropy-floor}`, `\Cref{prop:bloom-overhead}`, `\Cref{sec:bloom-gap}`
- Chapter 6: `\Cref{def:perfect-filter-line}`, `\Cref{sec:perfect-filter-line}`
- Chapter 5: `\Cref{def:bloom-filter}`, `\Cref{thm:bloom-optimal-k}`

---

## Tasks

### Task 1: Read sources and write chapter scaffolding

- [ ] Read `papers/bernoulli-hash-function/` (skim); `book/chapters/ch08/entropy-floor.tex` and `bloom-gap.tex`; `book/chapters/ch05/bloom-from-scratch.tex`; `book/chapters/ch06/perfect-filter-line.tex`; Part IV spec §4 chapter 14.

- [ ] Replace `book/chapters/ch14-optimal-bernoulli-sets.tex` with the scaffold:

```latex
\chapter{Optimal Bernoulli Sets (BHF)}
\label{ch:optimal-bernoulli-sets}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item State the Bernoulli Hash Function (BHF) construction, an
    FNR-zero approximate set built from a perfect hash plus
    per-element fingerprint.
  \item Derive its space cost as $\lceil -\log_2 \fprate \rceil$
    bits per element, matching chapter~8 \S8.3's entropy floor
    exactly.
  \item Recognize the BHF as the constructive payoff to the
    chapter~5 Bloom filter and chapter~8 \S8.4's $44\%$ gap.
\end{itemize}
\end{quote}

% Section 14.1
\input{chapters/ch14/optimality-question}

% Section 14.2
\input{chapters/ch14/bhf-construction}

% Section 14.3
\input{chapters/ch14/space-analysis}

% Section 14.4
\input{chapters/ch14/fpr-analysis}

% Section 14.5
\input{chapters/ch14/construction-time}

% Section 14.6
\input{chapters/ch14/bridge}

% Section 14.7
\input{chapters/ch14/bibliographic-notes}

% Exercises
\input{chapters/ch14/exercises}
```

- [ ] Create `book/chapters/ch14/` + 8 placeholder files. Each: `% Placeholder. Drafted in Plan 14 Task N.` (N = 2-9).

- [ ] Build exit 0. Commit:

```
book: scaffold chapter 14 (optimal Bernoulli sets, BHF) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener (three bullets: BHF construction, entropy-floor matching, gap
closure), seven section subfile inputs plus exercises, with matching
empty placeholders.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §14.1 The Optimality Question (~3 pp)

**Files:** Modify `book/chapters/ch14/optimality-question.tex`.

**Content checklist (4 items):**

1. **Recall the gap.** Chapter 8 §8.3 derived the entropy floor: $-\log_2 \fprate$ bits per element. Chapter 8 §8.4 showed the standard Bloom filter pays $\log_2 e \approx 1.443$ overhead. Half a page; cite `\Cref{thm:entropy-floor}` and `\Cref{prop:bloom-overhead}`.

2. **The open question.** Can a constructive scheme close the gap? Half a page.

3. **The answer (preview).** Yes. The BHF achieves the floor exactly. Sketch the idea: replace the multi-hash bitmap with a perfect hash plus per-element fingerprint. One page.

4. **Chapter roadmap.** §14.2 construction; §14.3 space; §14.4 FPR; §14.5 construction time; §14.6 bridge to BPHF.

**Labels:** `\section{The Optimality Question}` with `\label{sec:optimality-question}`.

**Header cross-reference comment block.**

**Target length:** ~3 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 3: §14.2 The BHF Construction (~7 pp)

**Files:** Modify `book/chapters/ch14/bhf-construction.tex`.

**Content checklist (6 items):**

1. **The two ingredients.** A perfect hash function $\phi : A \to [n]$ (bijection on $A$), and a per-element fingerprint table $F : [n] \to \{0, 1\}^r$ with $r = \lceil -\log_2 \fprate \rceil$. Half a page.

2. **Construction.** For each $a \in A$: store $F[\phi(a)] := g(a)$ where $g : \Universe \to \{0, 1\}^r$ is a secondary "fingerprint" hash function (uniform on $\{0, 1\}^r$). One page.

3. **Membership query.** For query $x$: compute $\phi(x) \in [n]$ (may be undefined for $x \notin A$; depends on perfect-hash construction); compute $g(x) \in \{0, 1\}^r$; return $\top$ iff $F[\phi(x)] = g(x)$. One page with pseudocode in `algorithm2e`.

4. **FNR = 0 (one-sidedness).** If $x \in A$ was inserted, $F[\phi(x)] = g(x)$ by construction; query returns $\top$. Half a page.

5. **FPR analysis preview.** For $x \notin A$: $\phi(x)$ maps to some slot (possibly any of $n$); fingerprint match probability is $2^{-r}$. Full analysis in §14.4. Half a page.

6. **Worked example.** $A = \{a_1, \ldots, a_{1000}\}$, target $\fprate = 0.01$, so $r = 7$ bits per element. Total space: $1000 \cdot 7 = 7000$ bits + perfect-hash overhead. Compare to Bloom at same target: $\sim 9600$ bits. One page.

**Labels:** `\section{The BHF Construction}` with `\label{sec:bhf-construction}`. Definition `\label{def:bhf}`.

**Header cross-reference comment block.**

**Target length:** ~7 pp (1600-1900 prose words).

**Workflow:** Standard.

---

### Task 4: §14.3 Space Analysis (~6 pp)

**Files:** Modify `book/chapters/ch14/space-analysis.tex`.

**Content checklist (5 items):**

1. **Fingerprint storage.** $n \cdot r$ bits where $r = \lceil -\log_2 \fprate \rceil$. One page.

2. **Perfect-hash storage.** A perfect hash function on $n$ keys requires asymptotically $O(n \log \log \log n / \log n)$ bits (Belazzougui et al). At reasonable $n$, this is small compared to $n r$. One page.

3. **Total bits per element.** $r + O(\log \log \log n / \log n) \to r$ as $n \to \infty$. The BHF achieves the entropy floor asymptotically. State as theorem `\label{thm:bhf-optimality}`. One page.

4. **Comparison table.** At $n = 10^6$ items and $\fprate \in \{0.01, 0.001, 10^{-6}\}$:
   - Entropy floor: 6.64, 9.97, 19.93 bits/element.
   - Standard Bloom: 9.59, 14.38, 28.76 bits/element.
   - BHF: 7, 10, 20 bits/element (rounded up to nearest bit + perfect-hash overhead).
   Half a page.

5. **The $\lceil \cdot \rceil$ rounding.** BHF's $r = \lceil -\log_2 \fprate \rceil$ rounds up to integer bits per fingerprint; the entropy floor is not necessarily integer. Discuss: BHF achieves the floor up to this rounding. One page.

**Labels:** `\section{Space Analysis}` with `\label{sec:space-analysis}`. Theorem `\label{thm:bhf-optimality}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 5: §14.4 False-Positive Rate Analysis (~5 pp)

**Files:** Modify `book/chapters/ch14/fpr-analysis.tex`.

**Content checklist (4 items):**

1. **Setup.** For $x \notin A$: what is $\Pr[\text{BHF query returns} \top]$? One paragraph.

2. **The argument.** $\phi(x)$ either (a) collides with some $a \in A$ in the perfect-hash range (then comparison happens) or (b) maps outside the range (then false negative impossible since $F[\cdot]$ not defined, the construction returns $\bot$). Under (a), fingerprint match probability is $2^{-r}$. Half a page.

3. **The bound.** $\fprate \le 2^{-r}$. With $r = \lceil -\log_2 \fprate \rceil$, this gives $\fprate \le \fprate_{\text{target}}$ as designed. State as proposition `\label{prop:bhf-fpr}`. One page.

4. **Independence of fingerprint hash.** The argument requires $g$ to be uniform on $\{0, 1\}^r$ (or at least pairwise-independent). Discuss the hash-function assumption; cite Carter-Wegman. One page.

5. **Worked verification.** At $r = 7, \fprate = 0.01$: $2^{-7} = 1/128 \approx 0.00781 < 0.01$. The construction meets target. One page.

**Labels:** `\section{False-Positive Rate Analysis}` with `\label{sec:fpr-analysis}`. Proposition `\label{prop:bhf-fpr}`.

**Target length:** ~5 pp (1100-1500 prose words).

**Workflow:** Standard.

---

### Task 6: §14.5 Construction Time and Trade-offs (~4 pp)

**Files:** Modify `book/chapters/ch14/construction-time.tex`.

**Content checklist (4 items):**

1. **Building the perfect hash.** $O(n)$ expected time via the standard MWHC or BBHash algorithms (cite). Half a page.

2. **Building the fingerprint table.** $O(n)$ time (one pass over $A$). Half a page.

3. **Query time.** $O(1)$ (two hash evaluations and a comparison). Half a page.

4. **Trade-offs vs Bloom.** BHF gives optimal space but requires static or rarely-updated set. Bloom supports streaming insertions. Insertions into BHF require rebuilding the perfect hash. The trade-off table. One page.

5. **When to use which.** Decision tree: static set + space-critical → BHF; streaming + space-tolerant → Bloom. Half a page.

**Labels:** `\section{Construction Time and Trade-offs}` with `\label{sec:construction-time}`.

**Target length:** ~4 pp (900-1200 prose words).

**Workflow:** Standard.

---

### Task 7: §14.6 Bridge (~2 pp)

**Files:** Modify `book/chapters/ch14/bridge.tex`.

**Content:** §14.7 names antecedents; chapter 15 covers the FPR-zero counterpart (BPHF) for ranked search.

**Labels:** `\section{Bridge}` with `\label{sec:ch14-bridge}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 8: §14.7 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch14/bibliographic-notes.tex`; optionally extend `book/references.bib`.

**Content (3-4 paragraphs):**

1. **`towell-bernoulli-hash-function` paper** (already in bib from Plan 5) as primary source.

2. **Perfect-hashing literature:** Carter-Wegman (already in bib); Belazzougui-Botelho-Dietzfelbinger 2009 (BDZ algorithm) for the modern perfect-hash construction. Add bib entry.

3. **Comparison data structures:** cuckoo filter (Fan et al 2014), quotient filter (Bender et al 2012). Brief mention; add bib entries only if cited.

**Possible new bib entries:**

```bibtex
@article{belazzougui-2009,
  author  = {Djamal Belazzougui and Fabiano C. Botelho and Martin Dietzfelbinger},
  title   = {Hash, Displace, and Compress},
  journal = {ESA},
  year    = {2009}
}

@inproceedings{fan-cuckoo-2014,
  author    = {Bin Fan and Dave G. Andersen and Michael Kaminsky and Michael D. Mitzenmacher},
  title     = {Cuckoo Filter: Practically Better Than {Bloom}},
  booktitle = {CoNEXT},
  year      = {2014}
}
```

(Add only if cited in prose.)

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline` + `\label{sec:bib-notes-ch14}` matching ch01-ch13.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 9: Chapter 14 Exercises (11)

**Files:** Modify `book/chapters/ch14/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Fingerprint bits for target FPR.** For $\fprate \in \{0.01, 0.001, 10^{-6}\}$, compute $r = \lceil -\log_2 \fprate \rceil$.

2. **BHF space at $n = 10^6$, $\fprate = 0.001$.** Compute BHF space (in bits and MB), compare to Bloom at the same target.

3. **Verify FNR = 0.** Explain in two sentences why BHF cannot produce false negatives by construction.

**Medium (★★ × 5):**

4. **Notebook-tied BHF build.** Use the chapter 14 notebook to build a BHF for $n = 10000$ items at $\fprate = 0.01$. Verify empirical FPR matches theoretical $2^{-r}$.

5. **BHF vs Bloom space ratio.** Derive the asymptotic ratio (BHF cost) / (Bloom cost) at any target $\fprate$. Show it tends to $1/\log_2 e \approx 0.693$.

6. **Rounding gap.** For $\fprate = 0.06$, compute $r = \lceil -\log_2 0.06 \rceil = 5$, so actual BHF FPR is $2^{-5} = 0.03125$, not 0.06. Quantify the "wasted bits" from the integer rounding.

7. **Perfect-hash overhead.** Look up Belazzougui et al's perfect-hash space bound. For $n = 10^6$, what is the overhead per element in bits?

8. **Composition under BHF.** Can two BHFs be merged like two Bloom filters (bit-OR)? Discuss why not.

**Challenging (★★★ × 3):**

9. **BHF FPR exact analysis.** Derive the exact FPR (not the upper bound) including the perfect-hash range-vs-universe ratio.

10. **Dynamic BHF.** Sketch a dynamic variant supporting insertions: rebuild perfect hash on milestone insertions; amortize the cost. Derive expected time per insertion.

11. **Entropy-floor matching.** Prove that any FNR-zero approximate set using $r$ bits per fingerprint achieves FPR $\le 2^{-r}$ at best (i.e., BHF is asymptotically optimal in $r$).

**Target length:** ~2 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 10: Chapter 14 Notebook (`ch14-bhf.ipynb`)

**Files:** Create `python/notebooks/ch14-bhf.ipynb`.

**Content (~12-14 cells):**

1. Title + setup.
2. **Simple perfect hash via random probing** (code): a basic perfect-hash implementation suitable for pedagogical use (not BDZ; that's library-level). Build perfect hash $\phi$ on a small set $A$.
3. **Fingerprint table** (code): for each $a \in A$, store $F[\phi(a)] = g(a)$ where $g$ is a SHA256-based fingerprint hash to $r$ bits.
4. **BHF class** (code): combine perfect hash + fingerprint table; implement `contains(x)`.
5. **Empirical FPR verification** (code): at $n = 10000$, $\fprate = 0.01$, $r = 7$. Query 100000 random out-of-set items; verify empirical FPR $\approx 2^{-7} = 0.00781$.
6. **Space comparison** (code): compute BHF space in bits per element; compare to entropy floor and to standard Bloom.
7. **FPR vs $r$ sweep** (code): for $r \in \{4, 5, 6, 7, 8, 10\}$, verify empirical FPR matches $2^{-r}$.
8. **Discussion** (markdown): BHF as the constructive answer to chapter 8's entropy floor.

**Numerical sanity targets:**
- At $r = 7$: empirical FPR $\approx 0.00781$ within $\pm 0.001$ (large sample).
- BHF space at $n = 10000, \fprate = 0.01$: $\approx 7$ bits/element + perfect-hash overhead.

**Workflow:** Standard. Execute end-to-end.

---

## Self-Review

Spec coverage: chapter 14 row → each section has its own task; substantive notebook in Task 10.

Type and label consistency: chapter 8 entropy-floor labels referenced; chapter 5 Bloom labels referenced.
