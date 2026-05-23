# Bernoulli Textbook Chapter 9: Approximate Functions and n-ary Channels (Plan 9)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 9 of Part III (~26 pp): the type-lifting foundation. Generalize the noisy-bit atom ($\Bernoulli{\BoolType}$) to general algebraic types via n-ary channels. Generalize chapter 4 §4.4's Kronecker theorem and chapter 8 §8.2's BSC capacity to model-order $K$ on input domain and $L$ on output. Provides the foundation that chapters 10 (sketches), 11 (randomized algorithms), 12 (relations), and 13 (algebra of types) depend on.

**Architecture:** Replace `book/chapters/ch09-approximate-functions.tex` stub with a fully drafted chapter containing 6 sections, learning-outcomes opener, 10-12 exercises, supporting bibliographic entries, and a paired Python notebook simulating n-ary channels and computing their capacity.

**Tech Stack:** LaTeX (book class), alex.sty notation, biblatex+biber. Python 3.11+ + numpy + scipy + matplotlib for the notebook.

**Scope:** Chapter 9 only. Part III integration check deferred to Plan 13.

**Spec source of truth:** `docs/superpowers/specs/2026-05-23-bernoulli-textbook-part3-design.md` §3.3 (n-ary channels) and §4 (chapter 9 row).

**Base SHA:** `7cbbfb1` (HEAD at end of Plan 8).

**Source material:**
- `papers/bernoulli_maps/sections/` (n-ary channel formalism, primary source)
- `book/chapters/ch02/model-order.tex` (§2.4 closing sentence on n-ary as Part III trailhead)
- `book/chapters/ch04/kronecker.tex` (§4.4 Kronecker theorem to generalize)
- `book/chapters/ch08/bsc-capacity.tex` (§8.2 BSC capacity to generalize)
- `book/chapters/ch05/from-atom-to-set.tex` (§5.1 predicate framing to recall)

**Lessons inherited from Plans 1-8:**

1. **Page discipline.** Chapter 9 target ~26pp; expect 28-34pp realistic.

2. **Soul-voice hook (BLOCKING):** Respect the full banned-phrase list from the soul-voice hook at `$CLAUDE_PLUGIN_ROOT/hooks/check-banned-phrases.sh`. Substring matching applies.

3. **Notation:** $K$ (uppercase) for model-order; $L$ for output cardinality; $Q$ for $K \times L$ channel matrix; $\otimes$ for Kronecker tensor; $\Bernoulli{T}$ for type-lifted noisy values. Document the $K$ vs $k$ convention (Bloom $k$ stays lowercase).

4. **Cross-references:** Chapter 9 generalizes chapter 4 §4.4 and chapter 8 §8.2; use `\Cref` to those targets prominently. Forward references to chapters 10-13 use chapter-level `\Cref{ch:N}` where Plan 0 stubs exist.

5. **Per-task review cycle:** Spec + quality reviewers; combined where appropriate; fix subagent if substantive issues surface.

---

## File Structure

After this plan:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch09-approximate-functions.tex    # rewritten from stub
│   │   └── ch09/                             # NEW directory
│   │       ├── atom-to-function.tex          # §9.1 (~4 pp)
│   │       ├── n-ary-channels.tex            # §9.2 (~6 pp)
│   │       ├── n-ary-kronecker.tex           # §9.3 (~6 pp) the headline theorem
│   │       ├── n-ary-capacity.tex            # §9.4 (~5 pp)
│   │       ├── bridge-to-sketches.tex        # §9.5 (~2 pp)
│   │       ├── bibliographic-notes.tex       # §9.6 (~2 pp)
│   │       └── exercises.tex                 # 10-12 exercises (~2 pp)
│   ├── preamble.tex                          # may be extended (K, L macros if needed)
│   └── references.bib                        # extended with bernoulli-maps paper
└── python/
    └── notebooks/
        └── ch09-approximate-functions.ipynb  # n-ary channel simulator + capacity
```

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:approximate-functions` | `ch09-approximate-functions.tex` (Plan 0 stub) | chapter 5 §5.5 forward; chapter 8 §8.5 forward |
| `sec:atom-to-function` | `ch09/atom-to-function.tex` (Task 2) | (internal) |
| `sec:n-ary-channels` | `ch09/n-ary-channels.tex` (Task 3) | (internal); chapter 10-13 backward |
| `thm:n-ary-kronecker` | `ch09/n-ary-kronecker.tex` (Task 4) | chapter 13 backward |
| `sec:n-ary-capacity` | `ch09/n-ary-capacity.tex` (Task 5) | (internal) |
| `sec:bridge-to-sketches` | `ch09/bridge-to-sketches.tex` (Task 6) | (internal) |

Backward references that should resolve:
- Chapter 2: `\Cref{sec:model-order}, \Cref{def:model-order}, \Cref{thm:boolean-ceiling}`
- Chapter 4: `\Cref{sec:kronecker}, \Cref{thm:kronecker}, \Cref{cor:kronecker-unconditional}, \Cref{sec:axiom-1}, \Cref{ax:element-indep}, \Cref{sec:axiom-2}, \Cref{ax:block-rates-indep}, \Cref{sec:bernoulli-bool-formal}, \Cref{def:bernoulli-bool}`
- Chapter 5: `\Cref{ch:approximate-sets}, \Cref{sec:from-atom-to-set}, \Cref{sec:predicate-algebra}`
- Chapter 8: `\Cref{sec:entropy-refresher}, \Cref{sec:bsc-capacity}, \Cref{prop:bsc-capacity}`

Forward via `\Cref{ch:N}`: chapters 10, 11, 12, 13 (Plan 0 stubs).

---

## Tasks

### Task 0: Verify macro coverage

**Purpose:** Confirm alex.sty has macros for $K$ (model-order), $L$ (output cardinality), n-ary tensor; extend `book/preamble.tex` if missing.

- [ ] Grep:
```bash
grep -nE "ModelOrder|modelOrder|nArySize" book/alex.sty
```

- [ ] alex.sty likely does NOT define $K, L$ as macros (they are just math variables). If a `\providecommand{\ModelOrder}{K}` or similar would be useful for cross-chapter consistency, add it; otherwise the chapter can use bare $K, L$ in math mode.

- [ ] If notation-collision risk between $K$ (model-order) and $k$ (Bloom hashes, Miller-Rabin rounds) is a concern, add a `\providecommand{\ModelOrder}{K}` for the chapter-9 sections to use; document in §9.2 that $K$ is uppercase to distinguish from $k$.

- [ ] Build (exit 0).

- [ ] Commit only if preamble was modified.

---

### Task 1: Read sources and write chapter scaffolding

- [ ] Read source files: `papers/bernoulli_maps/sections/` end-to-end (this is the chapter's primary source); `book/chapters/ch02/model-order.tex` (§2.4); `book/chapters/ch04/kronecker.tex` (§4.4); `book/chapters/ch08/bsc-capacity.tex` (§8.2).

- [ ] Replace `book/chapters/ch09-approximate-functions.tex` with the scaffold:

```latex
\chapter{Approximate Functions and n-ary Channels}
\label{ch:approximate-functions}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Define $\Bernoulli{T}$ for a finite-enumeration type $T$, and
    write the $K \times L$ channel matrix $Q$ at model-order $K$.
  \item State and apply the n-ary Kronecker factorization theorem,
    which generalizes chapter~4 \S4.4 from model-order 2 to general $K$.
  \item Compute channel capacity for an n-ary channel, generalizing
    the BSC capacity $C = 1 - H(\fprate)$ of chapter~8 \S8.2.
\end{itemize}
\end{quote}

% Section 9.1
\input{chapters/ch09/atom-to-function}

% Section 9.2
\input{chapters/ch09/n-ary-channels}

% Section 9.3
\input{chapters/ch09/n-ary-kronecker}

% Section 9.4
\input{chapters/ch09/n-ary-capacity}

% Section 9.5
\input{chapters/ch09/bridge-to-sketches}

% Section 9.6
\input{chapters/ch09/bibliographic-notes}

% Exercises
\input{chapters/ch09/exercises}
```

- [ ] Create `book/chapters/ch09/` + 7 placeholder files (`atom-to-function.tex`, `n-ary-channels.tex`, `n-ary-kronecker.tex`, `n-ary-capacity.tex`, `bridge-to-sketches.tex`, `bibliographic-notes.tex`, `exercises.tex`). Each: `% Placeholder. Drafted in Plan 9 Task N.` with N substituted (2-8).

- [ ] Build exit 0.

- [ ] Commit:

```
book: scaffold chapter 9 (approximate functions and n-ary channels) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener (three bullets: T-valued type lifting, n-ary Kronecker
theorem, n-ary capacity), six section subfile inputs plus exercises,
with matching empty placeholders. Section drafts land in subsequent
Plan 9 tasks.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §9.1 From Approximate Sets to Approximate Functions (~4 pp)

**Files:** Modify `book/chapters/ch09/atom-to-function.tex`.

**Purpose:** Bridge from Part II's predicate framing (approximate set as a function $\Universe \to \{\top, \bot\}$) to Part III's $T$-valued framing (approximate function as $\Universe \to T$ for general $T$).

**Content checklist (5 items):**

1. **Opening recap.** Recall §5.1: an approximate set is a function whose membership predicate is a noisy bit. The codomain is $\{\top, \bot\}$. One paragraph.

2. **What if the codomain is bigger?** An approximate function generalizes: $\tilde f : \Universe \to T$ for some type $T$. Each evaluation $\tilde f(x)$ is a $\Bernoulli{T}$ instance. For $T = \BoolType$ this is exactly the predicate of Part II. For $T = \{1, 2, \ldots, K\}$ this is an n-ary classifier. For $T = \mathbb{N}$ this is a counter or estimator. One page.

3. **Two natural examples.**
   - A 3-class classifier (codomain $\{$cat, dog, bird$\}$) with confusion matrix among the three classes.
   - A counter that returns an estimate $\hat{n} \in \mathbb{N}$ given a multi-set query. Errors in either direction.
   Half a page each.

4. **What changes structurally.** The single $(\fprate, \fnrate)$ pair becomes a full channel matrix $Q$. The chapter 4 §4.4 Kronecker theorem extends; the chapter 8 §8.2 BSC capacity extends. Sets up §9.2 and §9.3.

5. **Signpost.** §9.2 formalizes; §9.3 generalizes Kronecker; §9.4 generalizes capacity.

**Labels:** `\section{From Approximate Sets to Approximate Functions}` with `\label{sec:atom-to-function}`.

**Header cross-reference comment block.**

**Target length:** ~4 pp (900-1200 prose words).

**Workflow:** Standard. Commit with HEREDOC similar to Plan 5-8 patterns.

---

### Task 3: §9.2 N-ary Channels (~6 pp)

**Files:** Modify `book/chapters/ch09/n-ary-channels.tex`.

**Source reading:** `papers/bernoulli_maps/sections/` (the chapter's primary reformulation source).

**Purpose:** Formalize the n-ary channel as a $K \times L$ row-stochastic matrix $Q$ at model-order $K$.

**Content checklist (6 items):**

1. **Definition: n-ary channel.** Input domain $X$ with model-order $K$ (partitioned into $K$ blocks $B_1, \ldots, B_K$ per chapter 4 axioms). Output domain $Y$ with $|Y| = L$ values. Channel matrix $Q$ is $K \times L$ row-stochastic ($Q_{ij} \ge 0$, rows sum to $1$). $Q_{ij}$ is the probability of output $j$ given input in block $B_i$. One page.

2. **Notation convention.** $K$ (uppercase) for model-order, distinguishing from the lowercase $k$ used elsewhere for Bloom-hash count and Miller-Rabin rounds. State explicitly. Half a page.

3. **Examples.**
   - $K = 2, L = 2$ (binary symmetric, recovers chapter 2 §2.1 BSC).
   - $K = 2, L = 2, \fprate \neq \fnrate$ (asymmetric, recovers chapter 2 §2.2).
   - $K = 3, L = 3$ (3-class classifier with $3 \times 3$ confusion matrix).
   - $K = \infty, L = \infty$ (counter or estimator with natural-number domain).
   One page covering all four with explicit $Q$ matrices for the finite cases.

4. **Constraints inherited from chapter 4 axioms.** Axiom 1 (element-wise independence) and Axiom 2 (per-block rate stability) lift unchanged to n-ary. Cite. Half a page.

5. **Parameter count.** $K \times L$ row-stochastic matrix has $K(L - 1)$ free parameters (each row of $L$ probabilities has $L - 1$ free given the constraint sum to $1$). Compare to chapter 4 §4.4's $2(2 - 1) = 2$ parameters at $K = L = 2$. Half a page.

6. **Signpost.** §9.3 generalizes Kronecker; §9.4 generalizes capacity.

**Labels:** `\section{N-ary Channels}` with `\label{sec:n-ary-channels}`. Definition `\label{def:n-ary-channel}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 4: §9.3 The n-ary Kronecker Theorem (~6 pp)

**Files:** Modify `book/chapters/ch09/n-ary-kronecker.tex`.

**Source reading:** `book/chapters/ch04/kronecker.tex` (the theorem to generalize).

**Purpose:** Generalize chapter 4's Kronecker factorization theorem from model-order 2 (Boolean) to model-order $K$. State and prove (or sketch).

**Content checklist (5 items):**

1. **Recall chapter 4 §4.4 theorem.** At model-order 2, the joint distribution over $m$ queries on a Bernoulli set factors as a Kronecker product. Half a page.

2. **The n-ary generalization.** For an n-ary channel of model-order $K$ with $K \times L$ matrix $Q$, the joint distribution over $m$ queries on inputs in blocks $B_{j_1}, \ldots, B_{j_m}$ factors as
   $$
   \Pr[Y_1, \ldots, Y_m \mid X_1 \in B_{j_1}, \ldots, X_m \in B_{j_m}]
   = \prod_{i=1}^m Q_{j_i, Y_i}
   $$
   under the deterministic-rates regime of chapter 4. State as theorem with `\label{thm:n-ary-kronecker}`. One page.

3. **Proof sketch.** Apply Axiom 1 (element-wise independence) at the n-ary level. The proof structure mirrors chapter 4's; the only change is that each row of $Q$ has $L$ entries instead of $2$. One page.

4. **Corollary: parameter count.** A model-order $K$, output-cardinality $L$ channel has $K(L - 1)$ parameters per channel; the joint over $m$ queries does NOT add parameters (just specifies which block each query draws from). State as `\label{cor:n-ary-parameter-count}`. Half a page.

5. **Worked example.** A 3-class classifier with $K = L = 3$. Compute the joint probability of an output sequence $(Y_1, Y_2, Y_3) = (1, 2, 1)$ given inputs $(X_1, X_2, X_3) = (B_1, B_2, B_1)$ for a specific $Q$. One page.

**Labels:** `\section{The n-ary Kronecker Theorem}` with `\label{sec:n-ary-kronecker}`. Theorem and corollary above.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 5: §9.4 Capacity for n-ary Channels (~5 pp)

**Files:** Modify `book/chapters/ch09/n-ary-capacity.tex`.

**Source reading:** `book/chapters/ch08/bsc-capacity.tex` (the BSC capacity result to generalize); Cover-Thomas chapter 7 for the n-ary case (cite, do not subsume).

**Purpose:** Generalize chapter 8 §8.2's $C = 1 - H(\fprate)$ to n-ary channels.

**Content checklist (5 items):**

1. **Recall chapter 8 §8.2.** $C = \max_{P_X} I(X; Y)$. For BSC, maximized at uniform input, giving $C = 1 - H(\fprate)$. Half a page.

2. **General n-ary case.** $C = \max_{P_X} I(X; Y)$ where the maximum is over input distributions $P_X$ on the $K$ blocks. No closed form in general; numerical optimization (Blahut-Arimoto algorithm; cite Cover-Thomas). One page.

3. **Special cases with closed forms.**
   - Symmetric n-ary channel (all rows of $Q$ are permutations of each other): $C = \log_2 L - H(\text{row})$. State the formula.
   - Strongly symmetric (additionally all columns are permutations): $C = \log_2 L - H(p_e, p_e/(L-1), \ldots, p_e/(L-1))$ where $p_e$ is the error probability.
   One page.

4. **Worked example.** A 4-state strongly symmetric channel with error probability $0.1$. Compute capacity. (Result: $\log_2 4 - H(0.9, 0.0333, 0.0333, 0.0333) \approx 2 - 0.6195 \approx 1.38$ bits per use.) Half a page.

5. **Bridge.** §9.5 sketches; chapter 10 instantiates with concrete sketches.

**Labels:** `\section{Capacity for n-ary Channels}` with `\label{sec:n-ary-capacity}`. Proposition `\label{prop:n-ary-capacity}`.

**Target length:** ~5 pp (1100-1500 prose words).

**Workflow:** Standard.

---

### Task 6: §9.5 Bridge to Sketches (~2 pp)

**Files:** Modify `book/chapters/ch09/bridge-to-sketches.tex`.

**Purpose:** Preview chapter 10 (sketches): each sketch is an approximate function from a stream/multiset to a low-dimensional summary.

**Content checklist (3 items):**

1. **What is a sketch?** A function from a sequence of items to a compact summary, with bounded reconstruction error. One paragraph.

2. **Sketches as $\Bernoulli{T}$.** CountMin is approximate counter ($T = \mathbb{N}$); HyperLogLog is approximate cardinality ($T = \mathbb{N}$); MinHash is approximate similarity ($T = [0, 1]$). Each fits the chapter 9 framework. One paragraph.

3. **Chapter 10 builds three sketches from scratch.** Each comes with a $\Bernoulli{T}$ type, an error bound, and a composition rule. Sets up chapter 10. One paragraph.

**Labels:** `\section{Bridge to Sketches}` with `\label{sec:bridge-to-sketches}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 7: §9.6 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch09/bibliographic-notes.tex`; extend `book/references.bib` with `towell-bernoulli-maps`.

**Content (4 paragraphs):**

1. **`towell-bernoulli-maps` paper:** the chapter's primary source. Add bib entry.

2. **Cover-Thomas (already in bib):** standard reference for n-ary channels and Blahut-Arimoto.

3. **Shannon (1948, already in bib):** the original channel-capacity framework.

4. **Brief forward.** Chapter 10's sketch literature is taken up in §10.6.

**New bib entry:**

```bibtex
@misc{towell-bernoulli-maps,
  author = {Alexander Towell},
  title  = {The algebra of the random approximate map model},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/bernoulli_maps}}
}
```

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 8: Chapter 9 Exercises (11)

**Files:** Modify `book/chapters/ch09/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Write a 3x3 channel matrix.** For a 3-class classifier with 90% accuracy and uniform off-diagonal errors, write $Q$.

2. **Parameter count.** For $K = 5, L = 3$, how many free parameters does the channel matrix have?

3. **Compute capacity at BSC limit.** Verify §9.4's general formula recovers $C = 1 - H(\fprate)$ at $K = L = 2$ for the BSC.

**Medium (★★ × 5):**

4. **Notebook-tied n-ary capacity.** Use `python/notebooks/ch09-approximate-functions.ipynb` to compute capacity for a 5-state symmetric channel with error probability $0.1$ via Blahut-Arimoto.

5. **Joint probability via n-ary Kronecker.** For a $K = 3$ channel with given $Q$, compute joint probability of output sequence $(1, 2, 1, 3)$ given input blocks $(B_1, B_2, B_3, B_1)$.

6. **Compose two n-ary channels.** Given two channels $Q_1$ ($K_1 \times L_1$) and $Q_2$ ($L_1 \times L_2$), show their composition is $Q_1 Q_2$ ($K_1 \times L_2$). Verify row-stochasticity is preserved.

7. **Sketch as n-ary channel.** Cast a CountMin sketch (chapter 10 preview) as an n-ary channel. What are the model-order and output cardinality?

8. **Asymmetric n-ary.** For a 3-class classifier where one class is rare (prior 0.01), derive how the PPV varies under workload prevalence. Connect to chapter 7 §7.4.

**Challenging (★★★ × 3):**

9. **Prove Axiom 2 carries from binary to n-ary.** Argue informally that chapter 4 §4.3 Axiom 2 statement transfers verbatim by replacing 2 with $K$.

10. **Channel capacity inequality.** Show that for any n-ary channel, $C \le \log_2 L$ (capacity is bounded by the output alphabet size). When is equality achieved?

11. **Approximate function from a Bloom-like construction.** Sketch a $T$-valued generalization of the Bloom filter: instead of bits, store small numerals, and report the most common one at query time. Derive the FPR/FNR analog as a $K \times L$ channel matrix.

**Target length:** ~2 pp.

**Workflow:** Standard.

---

### Task 9: Chapter 9 Notebook (`ch09-approximate-functions.ipynb`)

**Files:** Create `python/notebooks/ch09-approximate-functions.ipynb`.

**Content (~12 cells):**

1. Title + setup (imports, scipy.stats).
2. **N-ary channel class:** define `class NaryChannel(Q)` with `simulate(input_distribution, n_samples)` method.
3. **3-state symmetric channel example:** $K = L = 3$, identity-with-error matrix; simulate.
4. **Joint distribution check:** verify the n-ary Kronecker theorem empirically over 1000 trials.
5. **Capacity computation via Blahut-Arimoto:** implement (or use scipy) for arbitrary $Q$.
6. **Symmetric capacity:** verify §9.4's closed form for the 4-state strongly symmetric example. Should match the worked-example value ($\approx 1.38$ bits/use).
7. **BSC limit check:** confirm the n-ary capacity at $K = L = 2$ matches $1 - H(\fprate)$ from chapter 8 §8.2.
8. **3-class classifier example:** simulate a 3-class classifier on a prevalence-skewed workload; compute empirical confusion matrix vs the true $Q$.
9. **Discussion** (markdown): the chapter 9 framework as the foundation for chapter 10 sketches.

**Numerical sanity targets:**
- 4-state strongly symmetric, $p_e = 0.1$: capacity $\approx 1.38$ bits/use.
- BSC at $\fprate = 0.1$ via n-ary: capacity $\approx 1 - H(0.1) \approx 0.531$ bits/use.

**Workflow:** Standard. Execute end-to-end.

---

## Self-Review

Spec coverage: Part III spec §4 chapter 9 row → each section has its own task. Master spec substantive notebook → Task 9.

Type and label consistency: chapter 5/6/7/8 labels invoked correctly; chapter 4 §4.4 Kronecker labels referenced.
