# Bernoulli Textbook Chapter 10: Sketches and Estimators (Plan 10)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 10 of Part III (~28 pp): three canonical sketches (CountMin, HyperLogLog, MinHash) constructed from scratch, each cast as a $\Bernoulli{T}$ instance under the chapter 9 framework. Each comes with construction, $\Bernoulli{T}$ type, error bound, composition rule. The chapter is the catalog instance of Part III's type lift.

**Architecture:** Replace `book/chapters/ch10-sketches-estimators.tex` stub with a fully drafted chapter containing 6 sections, learning-outcomes opener, 10-12 exercises, bibliographic entries, and a substantive Python notebook implementing all three sketches from scratch.

**Tech Stack:** LaTeX (book class), alex.sty, biblatex+biber. Python 3.11+ + numpy + matplotlib + hashlib + scipy (already tracked) for the notebook.

**Scope:** Chapter 10 only. Part III integration check is Plan 13's Task 10.

**Spec source of truth:** `docs/superpowers/specs/2026-05-23-bernoulli-textbook-part3-design.md` §4 chapter 10 row.

**Base SHA:** `8e0830c` (HEAD at end of Plan 9).

**Source material:**
- `book/chapters/ch09/` all sections (the framework this chapter instantiates)
- `book/chapters/ch05/bloom-from-scratch.tex` (the predecessor sketch; CountMin/HyperLogLog/MinHash follow the same "construction + analysis + composition" template)
- External literature (cite via Bibliographic Notes; do not subsume): Cormode-Muthukrishnan 2005 (CountMin); Flajolet et al 2007 (HyperLogLog); Broder 1997 (MinHash); Cormode-Yi survey for context.

**Lessons inherited from Plans 1-9:**

1. **Page discipline.** Chapter 10 target ~28pp; expect 32-38pp realistic (three sketches each warrant detailed treatment).

2. **Soul-voice hook (BLOCKING):** Respect the full banned-phrase list at `$CLAUDE_PLUGIN_ROOT/hooks/check-banned-phrases.sh`. Substring matching applies.

3. **Notation:** Each sketch introduces its own conventional notation:
   - CountMin: $w$ (width), $d$ (depth/rows), $\epsilon$ (error parameter), $\delta$ (failure probability), $\hat{f}_a$ (estimated frequency of item $a$).
   - HyperLogLog: $m$ (register count), $\alpha_m$ (bias correction), $\rho(x)$ (leading-zero count), $\hat{n}$ (cardinality estimate).
   - MinHash: $k$ (signature length), $J(A, B)$ (Jaccard similarity), $h$ (hash family). Note: $k$ here may collide with chapter 5 Bloom $k$; use $k_{\mathrm{sig}}$ if disambiguation matters in cross-references.
   - Each sketch's $\Bernoulli{T}$ type from chapter 9.

4. **The chapter 5 Bloom filter is the reader's mental model.** Each sketch follows the same template (construction, analysis, error bound, composition); reference back to §5.2 frequently.

5. **External literature is cited, not subsumed.** Use Bibliographic Notes for full attribution.

---

## File Structure

After this plan:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch10-sketches-estimators.tex      # rewritten from stub
│   │   └── ch10/                             # NEW directory
│   │       ├── sketches-as-bernoulli.tex     # §10.1 (~3 pp)
│   │       ├── countmin.tex                  # §10.2 (~6 pp)
│   │       ├── hyperloglog.tex               # §10.3 (~7 pp)
│   │       ├── minhash-lsh.tex               # §10.4 (~6 pp)
│   │       ├── bridge.tex                    # §10.5 (~2 pp)
│   │       ├── bibliographic-notes.tex       # §10.6 (~2 pp)
│   │       └── exercises.tex                 # 10-12 exercises (~2 pp)
│   └── references.bib                        # extended (cormode-muthukrishnan, flajolet-et-al, broder-1997)
└── python/
    └── notebooks/
        └── ch10-sketches-estimators.ipynb    # CountMin + HyperLogLog + MinHash from scratch
```

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:sketches-estimators` | `ch10-sketches-estimators.tex` (Plan 0 stub) | chapter 9 §9.5 forward; chapter 12 backward |
| `sec:sketches-as-bernoulli` | `ch10/sketches-as-bernoulli.tex` (Task 2) | (internal) |
| `sec:countmin` | `ch10/countmin.tex` (Task 3) | (internal) |
| `sec:hyperloglog` | `ch10/hyperloglog.tex` (Task 4) | (internal) |
| `sec:minhash-lsh` | `ch10/minhash-lsh.tex` (Task 5) | (internal); chapter 12 §12.3 backward |
| `sec:ch10-bridge` | `ch10/bridge.tex` (Task 6) | (internal) |

Backward references (all resolve):
- Chapter 5: `\Cref{ch:approximate-sets}`, `\Cref{def:bloom-filter}`, `\Cref{thm:bloom-optimal-k}`
- Chapter 9: `\Cref{ch:approximate-functions}`, `\Cref{sec:n-ary-channels}`, `\Cref{def:n-ary-channel}`, `\Cref{thm:n-ary-kronecker}`, `\Cref{sec:n-ary-capacity}`
- Chapter 7 if needed: `\Cref{thm:delta-method}` (for HyperLogLog variance derivation)

---

## Tasks

### Task 1: Read sources and write chapter scaffolding

- [ ] Read sources: `book/chapters/ch09/` all section files (the framework); `book/chapters/ch05/bloom-from-scratch.tex` (the predecessor sketch); Part III spec §4 chapter 10 row.

- [ ] Replace `book/chapters/ch10-sketches-estimators.tex` (4-line stub) with the scaffold:

```latex
\chapter{Sketches and Estimators}
\label{ch:sketches-estimators}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Construct CountMin, HyperLogLog, and MinHash sketches from
    scratch, and identify each as a $\Bernoulli{T}$ instance under the
    chapter~9 framework.
  \item State the error bound and confidence parameter for each
    sketch, and derive the space/accuracy trade-off.
  \item Compose sketches via the type-driven algebra (the chapter~13
    unification).
\end{itemize}
\end{quote}

% Section 10.1
\input{chapters/ch10/sketches-as-bernoulli}

% Section 10.2
\input{chapters/ch10/countmin}

% Section 10.3
\input{chapters/ch10/hyperloglog}

% Section 10.4
\input{chapters/ch10/minhash-lsh}

% Section 10.5
\input{chapters/ch10/bridge}

% Section 10.6
\input{chapters/ch10/bibliographic-notes}

% Exercises
\input{chapters/ch10/exercises}
```

- [ ] Create `book/chapters/ch10/` + 7 placeholder files (`sketches-as-bernoulli.tex`, `countmin.tex`, `hyperloglog.tex`, `minhash-lsh.tex`, `bridge.tex`, `bibliographic-notes.tex`, `exercises.tex`). Each: `% Placeholder. Drafted in Plan 10 Task N.` with N substituted (2-8).

- [ ] Build exit 0.

- [ ] Commit:

```
book: scaffold chapter 10 (sketches and estimators) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener (three bullets: construct CountMin/HyperLogLog/MinHash, error
bounds and trade-offs, compose via type algebra), six section subfile
inputs plus exercises, with matching empty placeholders.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §10.1 Sketches as $\Bernoulli{T}$ (~3 pp)

**Files:** Modify `book/chapters/ch10/sketches-as-bernoulli.tex`.

**Content checklist (4 items):**

1. **What is a sketch?** A function from a (potentially long) stream or multiset of items to a compact summary, with bounded reconstruction error. Recall §9.5's preview.

2. **Three canonical sketches, three types.**
   - CountMin estimates frequency of a specific item: $T = \mathbb{N}$ (count); always overestimates (one-sided like Bloom).
   - HyperLogLog estimates cardinality of a multiset: $T = \mathbb{N}$ (count); approximate in both directions; logarithmic-in-cardinality space.
   - MinHash estimates Jaccard similarity of two sets: $T = [0, 1]$; symmetric error bounds.

3. **Why the chapter 9 framework unifies them.** Each is a function $\Universe^* \to T$ (input is a stream, output is a value of type $T$). The query algorithm and its error structure define a channel matrix $Q$ (typically large or infinite-dimensional but structured). Composition rules follow from chapter 9 §9.3.

4. **Signpost.** §10.2-§10.4 build each sketch; §10.5 hands off to chapter 13's full type algebra.

**Labels:** `\section{Sketches as $\Bernoulli{T}$}` with `\label{sec:sketches-as-bernoulli}`.

**Target length:** ~3 pp (700-900 prose words).

**Workflow:** Standard. Commit.

---

### Task 3: §10.2 CountMin (~6 pp)

**Files:** Modify `book/chapters/ch10/countmin.tex`.

**Purpose:** Construct CountMin from scratch.

**Content checklist (7 items):**

1. **Problem setup.** Frequency estimation on a stream: at each query for item $a$, return $\hat{f}_a$ approximating the true count $f_a$. One paragraph.

2. **The construction.** $d$ hash functions $h_1, \ldots, h_d : \Universe \to \{1, \ldots, w\}$ (pairwise independent). A $d \times w$ counter table $C$ initialized to zero. Update for item $a$: $C[i][h_i(a)] += 1$ for each $i$. Query for item $a$: $\hat{f}_a = \min_i C[i][h_i(a)]$. One page with pseudocode in `algorithm2e`.

3. **The error bound (the headline).** Theorem: With probability $\ge 1 - \delta$, $\hat{f}_a \le f_a + \epsilon F$ where $F = \sum_b f_b$ is the stream length, by choosing $w = \lceil e/\epsilon \rceil$ and $d = \lceil \log(1/\delta) \rceil$. State as `\label{thm:countmin-bound}`. One page with proof sketch via Markov's inequality + union bound. Cite Cormode-Muthukrishnan.

4. **The $\Bernoulli{T}$ type.** $T = \mathbb{N}$; the channel matrix $Q$ has rows indexed by true counts and columns by estimated counts. CountMin is one-sided in the same sense as Bloom: $\hat{f}_a \ge f_a$ always; over-estimation only. Half a page.

5. **Composition: merging two CountMin sketches.** Two CountMin tables $C_1, C_2$ with the same $(w, d, h_1, \ldots, h_d)$: merge via entry-wise add. The merged sketch's query gives the sum of counts. This is a $\Bernoulli{T}$ composition under chapter 9 §9.3. Half a page.

6. **Worked example.** $w = 10$, $d = 5$, stream of 1000 items with frequencies. Compute $\hat{f}_a$ for a specific item; compare to true count. Half a page.

7. **Signpost.** §10.3 covers HyperLogLog (cardinality, not per-item frequency).

**Labels:** `\section{CountMin}` with `\label{sec:countmin}`. Definition `\label{def:countmin}`, theorem `\label{thm:countmin-bound}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 4: §10.3 HyperLogLog (~7 pp)

**Files:** Modify `book/chapters/ch10/hyperloglog.tex`.

**Purpose:** Construct HyperLogLog from scratch.

**Content checklist (7 items):**

1. **Problem setup.** Cardinality estimation: given a stream that may contain duplicates, estimate $n = |\{$distinct items$\}|$. Why exact counting is too expensive ($\Theta(n)$ space lower bound for exact distinct count). One paragraph.

2. **The leading-zero trick.** For a uniformly random hash $h(a) \in [0, 1]$, $\Pr[\rho(h(a)) \ge k] = 2^{-k}$ where $\rho$ counts leading zeros in the binary representation. So the maximum $\rho$ across $n$ items grows as $\log_2 n$. Half a page.

3. **Single-register estimator.** Track $\hat{\rho} = \max_a \rho(h(a))$. Estimate $\hat{n} = 2^{\hat{\rho}}$. Very high variance (one observation). One page.

4. **Multiple registers (the construction).** Hash each item to one of $m$ buckets via the first few hash bits; for each bucket, track the max $\rho$ of remaining bits. Combine via harmonic mean: $\hat{n} = \alpha_m m^2 / \sum_j 2^{-\rho_j}$ where $\alpha_m$ is a bias correction. One page with pseudocode.

5. **The error bound.** Standard error $\approx 1.04/\sqrt{m}$ (relative). With $m = 2048$ registers (12-bit prefix), accuracy $\approx 2.3\%$. State as `\label{prop:hyperloglog-error}`. Half a page; cite Flajolet et al.

6. **The $\Bernoulli{T}$ type.** $T = \mathbb{N}$; the channel matrix $Q$ has rows indexed by true cardinality $n$ and columns by estimated $\hat{n}$. Approximately log-normal error structure. Half a page.

7. **Merge operation and composition.** Two HyperLogLog sketches with same $m$ and hash family: merge via entry-wise max on the register array. Result is a HyperLogLog sketch of the union of the two streams. Composition under chapter 9 §9.3. Half a page.

8. **Worked example.** $m = 256$, simulate a stream of 10000 unique items; compute $\hat{n}$ and the estimation error. One page.

**Labels:** `\section{HyperLogLog}` with `\label{sec:hyperloglog}`. Definition `\label{def:hyperloglog}`, proposition `\label{prop:hyperloglog-error}`.

**Target length:** ~7 pp (1600-1900 prose words; the longest section).

**Workflow:** Standard.

---

### Task 5: §10.4 MinHash and LSH (~6 pp)

**Files:** Modify `book/chapters/ch10/minhash-lsh.tex`.

**Purpose:** Construct MinHash from scratch; cover the LSH (Locality-Sensitive Hashing) extension for approximate nearest neighbor.

**Content checklist (7 items):**

1. **Problem setup.** Jaccard similarity estimation: $J(A, B) = |A \cap B| / |A \cup B|$. Exact computation is $O(|A| + |B|)$; can we sketch each set in $O(k)$ space and estimate $J$ from sketches alone? One paragraph.

2. **The MinHash trick.** For a hash $h$, $\Pr[\min_{a \in A} h(a) = \min_{b \in B} h(b)] = J(A, B)$ (assuming no collisions). State and prove (one-paragraph proof). Half a page.

3. **The construction.** Pick $k$ hash functions $h_1, \ldots, h_k$. For each set $A$, compute signature $\sigma(A) = (\min h_1(A), \ldots, \min h_k(A))$. Estimate $\hat{J}(A, B) = (1/k) |\{i : \sigma_i(A) = \sigma_i(B)\}|$. One page.

4. **Error bound.** Each component is Bernoulli($J$); $\hat{J}$ has variance $J(1-J)/k$. By Hoeffding, $\Pr[|\hat{J} - J| \ge \epsilon] \le 2 \exp(-2 k \epsilon^2)$. State as `\label{prop:minhash-error}`. Half a page.

5. **The $\Bernoulli{T}$ type.** $T = [0, 1]$ (similarity is in $[0, 1]$). Channel matrix $Q$ has rows indexed by true $J$ and columns by estimated $\hat{J}$. Binomial structure. Half a page.

6. **LSH for approximate nearest neighbor.** Group MinHash signatures into bands; collide bands as hash keys. Items in the same bucket are likely similar. Cite Indyk-Motwani 1998 (LSH original). One page.

7. **Worked example.** Two sets of size 100 with overlap 30 (true $J = 30/170 \approx 0.176$). $k = 200$ MinHash. Compute $\hat{J}$; compare to true. Half a page.

**Labels:** `\section{MinHash and LSH}` with `\label{sec:minhash-lsh}`. Definition `\label{def:minhash}`, proposition `\label{prop:minhash-error}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 6: §10.5 Bridge (~2 pp)

**Files:** Modify `book/chapters/ch10/bridge.tex`.

**Content checklist (3 items):**

1. **Recap.** Three sketches, three $\Bernoulli{T}$ instances. Each follows the same construction-analysis-composition pattern.

2. **Composition algebra.** Chapter 13 axiomatizes how $\Bernoulli{T \times U}, \Bernoulli{T + U}, \Bernoulli{L T}$ compose. The three sketches of this chapter are instances; the algebra makes them compose by structure.

3. **Forward.** Chapter 11 covers randomized algorithms (Miller-Rabin formalization). Chapter 12 lifts to relations. Chapter 13 unifies.

**Labels:** `\section{Bridge}` with `\label{sec:ch10-bridge}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 7: §10.6 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch10/bibliographic-notes.tex`; extend `book/references.bib`.

**Content (5 paragraphs):**

1. **Cormode-Muthukrishnan (2005):** CountMin original. Add bib entry.

2. **Flajolet et al (2007):** HyperLogLog original. Add bib entry.

3. **Broder (1997):** MinHash original. Add bib entry.

4. **Indyk-Motwani (1998):** LSH original. Add bib entry.

5. **Cormode-Yi survey:** broader sketch literature. Add bib entry if cited.

**New bib entries (verify not already in bib first):**

```bibtex
@article{cormode-muthukrishnan-2005,
  author  = {Graham Cormode and S. Muthukrishnan},
  title   = {An Improved Data Stream Summary: The Count-Min Sketch and its Applications},
  journal = {Journal of Algorithms},
  volume  = {55},
  number  = {1},
  pages   = {58--75},
  year    = {2005}
}

@inproceedings{flajolet-et-al-2007,
  author    = {Philippe Flajolet and {\'E}ric Fusy and Olivier Gandouet and Fr{\'e}d{\'e}ric Meunier},
  title     = {HyperLogLog: The Analysis of a Near-Optimal Cardinality Estimation Algorithm},
  booktitle = {AofA: Analysis of Algorithms},
  pages     = {137--156},
  year      = {2007}
}

@inproceedings{broder-1997,
  author    = {Andrei Z. Broder},
  title     = {On the Resemblance and Containment of Documents},
  booktitle = {Compression and Complexity of Sequences},
  pages     = {21--29},
  year      = {1997}
}

@inproceedings{indyk-motwani-1998,
  author    = {Piotr Indyk and Rajeev Motwani},
  title     = {Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality},
  booktitle = {STOC},
  pages     = {604--613},
  year      = {1998}
}
```

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 8: Chapter 10 Exercises (11)

**Files:** Modify `book/chapters/ch10/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **CountMin parameter selection.** For $\epsilon = 0.01, \delta = 0.001$, compute the CountMin parameters $w, d$.

2. **HyperLogLog accuracy.** For $m \in \{64, 256, 1024\}$, compute the standard relative error $1.04/\sqrt{m}$.

3. **MinHash variance.** For $J = 0.5, k = 100$, compute $\Var[\hat{J}]$ and a $\pm 1$ standard-deviation confidence interval.

**Medium (★★ × 5):**

4. **Notebook-tied sketch comparison.** Use `python/notebooks/ch10-sketches-estimators.ipynb` to run CountMin, HyperLogLog, and MinHash on a synthetic stream; compare empirical vs theoretical error.

5. **CountMin bound proof.** Reproduce the Markov + union bound proof of `thm:countmin-bound`.

6. **HyperLogLog at low cardinality.** Why does HyperLogLog under-estimate for small $n$ (relative to $m$)? Cite the linear-counting correction; derive informally.

7. **MinHash for documents.** A document with 1000 distinct words has signature 200 hashes. Estimate the storage cost. Compare to storing the full word set.

8. **Channel matrix for CountMin.** Cast CountMin's $\Bernoulli{\mathbb{N}}$ type as a channel matrix; identify rows (true count) and columns (estimated count); describe the structure of $Q$.

**Challenging (★★★ × 3):**

9. **CountMin variance.** Derive $\mathbb{E}[\hat{f}_a - f_a]$ exactly (not just the upper bound). Use the linearity of expectation over the collisions.

10. **HyperLogLog merge.** Show that the merge of two HyperLogLog sketches (entry-wise max) is exactly a HyperLogLog sketch of the union stream. Justify via the underlying max-of-leading-zeros structure.

11. **LSH parameter sweep.** Given target precision/recall on approximate nearest neighbor, derive the LSH band parameter $r$ (number of bands) and width parameter $b$ (rows per band).

**Target length:** ~2 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 9: Chapter 10 Notebook (`ch10-sketches-estimators.ipynb`)

**Files:** Create `python/notebooks/ch10-sketches-estimators.ipynb`.

**Content (~18-22 cells: substantive notebook with three sketches):**

1. Title + setup.
2. **CountMin class** (code): implement `CountMin(w, d, seed)` with `update(item)`, `query(item)`, `merge(other)`.
3. **CountMin sanity check** (code): stream of items with known frequencies; verify $\hat{f}_a \ge f_a$ always; measure mean over-estimation.
4. **CountMin error bound check** (code): set $\epsilon = 0.01, \delta = 0.001$; run many trials; verify empirical failure rate $< \delta$.
5. **HyperLogLog class** (code): implement `HyperLogLog(m, seed)` with `update(item)`, `estimate()`, `merge(other)`.
6. **HyperLogLog accuracy** (code): true cardinality 10000; with $m = 256$ registers, expected relative error $\approx 6.5\%$; verify empirically.
7. **HyperLogLog merge** (code): two streams with overlap; merge sketches; verify cardinality estimate matches union cardinality.
8. **MinHash class** (code): implement `MinHash(k, seed)` with `signature(set)`, `similarity(other_sig)`.
9. **MinHash accuracy** (code): two sets with known $J$; $k = 200$; verify $\hat{J}$ close to $J$.
10. **Three-sketch summary** (code): plot space/accuracy trade-off for all three on a common axes.
11. **Discussion** (markdown): each sketch as a $\Bernoulli{T}$ instance; the chapter 13 unification preview.

**Numerical sanity targets:**
- CountMin $\epsilon = 0.01, \delta = 0.001$, stream length 10000: $\hat{f}_a - f_a \le 100$ always; empirical failure rate $< 0.001$.
- HyperLogLog $m = 256$, $n = 10000$: empirical relative error within $\pm 0.1$ of theoretical $0.065$.
- MinHash $J = 0.5, k = 200$: empirical $\hat{J}$ within $\pm 0.05$ of $0.5$.

**Workflow:** Standard. Execute end-to-end.

---

## Self-Review

Spec coverage: chapter 10 row → each section has its own task; substantive notebook → Task 9.

Type and label consistency: chapter 9 framework used uniformly; chapter 5 Bloom referenced as predecessor; chapter 12 forward reference noted for §10.4 MinHash.
