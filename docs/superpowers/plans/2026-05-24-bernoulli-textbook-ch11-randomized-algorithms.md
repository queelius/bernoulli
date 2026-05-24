# Bernoulli Textbook Chapter 11: Randomized Algorithms (Plan 11)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 11 of Part III (~24 pp): formal treatment of randomized algorithms. Retire chapter 3 §3.4's informal Miller-Rabin walkthrough by recasting it formally as a $\Bernoulli{\BoolType}$. Distinguish Las Vegas (random runtime, exact output) from Monte Carlo (fixed runtime, random output). Frame RP and BPP via the chapter 7 PPV framework. Cover sample complexity (Chernoff bound, union bound).

**Architecture:** Replace `book/chapters/ch11-randomized-algorithms.tex` stub with a fully drafted chapter containing 6 sections, learning-outcomes opener, 10-12 exercises, bibliographic entries, and a paired Python notebook implementing Miller-Rabin formally + Las Vegas vs Monte Carlo timing comparison.

**Tech Stack:** LaTeX (book class), alex.sty, biblatex+biber. Python 3.11+ + numpy + matplotlib + sympy (for primality verification) for the notebook.

**Scope:** Chapter 11 only. Part III integration check is Plan 13 Task 10.

**Spec source of truth:** `docs/superpowers/specs/2026-05-23-bernoulli-textbook-part3-design.md` §4 chapter 11 row.

**Base SHA:** `fc2a1a0` (HEAD at end of Plan 10).

**Source material:**
- `book/chapters/ch03/miller-rabin.tex` (§3.4 the informal walkthrough being formalized)
- `book/chapters/ch07/binomial-estimator.tex` (§7.2 binomial estimator; chapter 11 §11.4 builds on it)
- `book/chapters/ch09/n-ary-channels.tex` (§9.2 n-ary framework; RP/BPP use this)
- External literature (cite via Bibliographic Notes): Motwani-Raghavan 1995; Mitzenmacher-Upfal (in bib); Karger 1993 (min-cut).

**Lessons inherited from Plans 1-10:**

1. **Page discipline.** Chapter 11 target ~24pp; expect 26-30pp realistic.

2. **Soul-voice hook (BLOCKING):** Respect the full banned-phrase list at `$CLAUDE_PLUGIN_ROOT/hooks/check-banned-phrases.sh`.

3. **Notation:** Standard alex.sty; chapter 3 Miller-Rabin notation ($n$ for the integer being tested, $a$ for a witness, $k$ for number of rounds); chapter 7 estimator notation; new bigO/asymptotic.

4. **The §3.4 deferral retirement is the chapter's central pedagogical promise** (mirror chapter 7's relationship to chapter 1 §1.4). §11.1 explicitly closes the §3.4 deferral.

5. **Per-task review:** standard Path A pattern.

---

## File Structure

After this plan:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch11-randomized-algorithms.tex      # rewritten from stub
│   │   └── ch11/                                # NEW directory
│   │       ├── miller-rabin-formal.tex          # §11.1 (~3 pp)
│   │       ├── las-vegas-vs-monte-carlo.tex     # §11.2 (~5 pp)
│   │       ├── rp-bpp.tex                       # §11.3 (~6 pp)
│   │       ├── sample-complexity.tex            # §11.4 (~5 pp)
│   │       ├── bridge.tex                       # §11.5 (~1 pp)
│   │       ├── bibliographic-notes.tex          # §11.6 (~2 pp)
│   │       └── exercises.tex                    # 10-12 exercises (~2 pp)
│   └── references.bib                           # extended (motwani-raghavan, karger-1993)
└── python/
    └── notebooks/
        └── ch11-randomized-algorithms.ipynb     # Miller-Rabin formal + LV vs MC timing
```

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:randomized-algorithms` | `ch11-randomized-algorithms.tex` (Plan 0 stub) | (forward from various chapters) |
| `sec:miller-rabin-formal` | `ch11/miller-rabin-formal.tex` (Task 2) | (internal); ch3 §3.4 backward |
| `sec:las-vegas-vs-monte-carlo` | `ch11/las-vegas-vs-monte-carlo.tex` (Task 3) | (internal) |
| `sec:rp-bpp` | `ch11/rp-bpp.tex` (Task 4) | (internal) |
| `sec:sample-complexity` | `ch11/sample-complexity.tex` (Task 5) | (internal); ch7 §7.2 backward |
| `sec:ch11-bridge` | `ch11/bridge.tex` (Task 6) | (internal) |

Backward references that should resolve:
- Chapter 3: `\Cref{ch:boolean-algebra}`, `\Cref{sec:miller-rabin}`, `\Cref{eq:mr-fpr}`, `\Cref{eq:mr-k-round}`, `\Cref{thm:composition}`
- Chapter 7: `\Cref{sec:binomial-estimator}`, `\Cref{prop:binomial-unbiased}`, `\Cref{prop:binomial-variance}`, `\Cref{sec:derived-measures}`, `\Cref{def:ppv}`
- Chapter 9: `\Cref{ch:approximate-functions}`, `\Cref{sec:n-ary-channels}`, `\Cref{def:n-ary-channel}`
- Chapter 4: `\Cref{sec:axiom-1}`, `\Cref{ax:element-indep}` (for sample-complexity independence)

---

## Tasks

### Task 1: Read sources and write chapter scaffolding

- [ ] Read sources: `book/chapters/ch03/miller-rabin.tex` (§3.4 informal); `book/chapters/ch07/binomial-estimator.tex` (§7.2); `book/chapters/ch09/n-ary-channels.tex` (§9.2); Part III spec §4 chapter 11 row.

- [ ] Replace `book/chapters/ch11-randomized-algorithms.tex` with the scaffold:

```latex
\chapter{Randomized Algorithms}
\label{ch:randomized-algorithms}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Restate Miller-Rabin formally as a $\Bernoulli{\BoolType}$
    with $\fnrate = 0$ and $\fprate \le 1/4$ per round, closing
    chapter~3 \S3.4's informal walkthrough with a formal proof.
  \item Distinguish Las Vegas (random runtime, exact output) from
    Monte Carlo (fixed runtime, random output) and identify when each
    is appropriate.
  \item State the RP and BPP complexity classes via the chapter~7
    PPV framework, and apply the Chernoff bound for sample-complexity
    analysis.
\end{itemize}
\end{quote}

% Section 11.1
\input{chapters/ch11/miller-rabin-formal}

% Section 11.2
\input{chapters/ch11/las-vegas-vs-monte-carlo}

% Section 11.3
\input{chapters/ch11/rp-bpp}

% Section 11.4
\input{chapters/ch11/sample-complexity}

% Section 11.5
\input{chapters/ch11/bridge}

% Section 11.6
\input{chapters/ch11/bibliographic-notes}

% Exercises
\input{chapters/ch11/exercises}
```

- [ ] Create `book/chapters/ch11/` + 7 placeholders. Each: `% Placeholder. Drafted in Plan 11 Task N.` (N = 2-8).

- [ ] Build exit 0. Commit:

```
book: scaffold chapter 11 (randomized algorithms) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener (three bullets: Miller-Rabin formal, Las Vegas vs Monte Carlo,
RP/BPP and Chernoff sample complexity), six section subfile inputs
plus exercises, with matching empty placeholders.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §11.1 Miller-Rabin Formal (~3 pp)

**Files:** Modify `book/chapters/ch11/miller-rabin-formal.tex`.

**Purpose:** Recast §3.4's informal Miller-Rabin walkthrough as a formal $\Bernoulli{\BoolType}$. Retire §3.4's deferral.

**Content checklist (4 items):**

1. **Recap §3.4 informally.** One paragraph + cite `\Cref{sec:miller-rabin}`.

2. **Formal statement.** Theorem: for any odd composite $n > 2$, the Miller-Rabin witness predicate $W_n(a) := \mathrm{MillerRabinRound}(n, a)$ at randomly chosen $a \in \{2, \ldots, n-2\}$ is a $\Bernoulli{\BoolType}$ instance with $\fnrate = 0$ and $\fprate \le 1/4$. State as `\label{thm:miller-rabin-formal}`. Half a page.

3. **Proof sketch.** Cite Rabin (1980) for the number-theoretic $\fprate \le 1/4$ bound (do not subsume). Apply chapter 4 Axiom 1 to $k$ rounds: $\Pr[\text{all } k \text{ rounds say prime} \mid n \text{ composite}] \le (1/4)^k$. This gives $\fprate^{(k)} \le (1/4)^k$ via `\Cref{thm:composition}`. One page.

4. **What changed from §3.4.** §3.4 treated the bound as an assertion to apply; §11.1 frames it as a theorem with citations to the number-theoretic underpinnings. The formalization is the chapter 11 §11.1 contribution. Half a page.

**Labels:** `\section{Miller-Rabin Formal}` with `\label{sec:miller-rabin-formal}`. Theorem `\label{thm:miller-rabin-formal}`.

**Target length:** ~3 pp (700-900 prose words).

**Workflow:** Standard. Commit.

---

### Task 3: §11.2 Las Vegas vs Monte Carlo (~5 pp)

**Files:** Modify `book/chapters/ch11/las-vegas-vs-monte-carlo.tex`.

**Content checklist (5 items):**

1. **Definitions.** Las Vegas: random runtime, deterministic output (always correct). Monte Carlo: fixed runtime, random output (may be wrong with bounded probability). One page.

2. **Trade-off.** Worst-case-bounded runtime requires randomized output; deterministic output may have unbounded runtime in the worst case. One page.

3. **Examples.**
   - **Randomized quicksort** (Las Vegas): random pivot, expected $O(n \log n)$ runtime, always correct sorted output.
   - **Karger min-cut** (Monte Carlo): fixed $O(n^2)$ runtime, $\Pr[\text{correct}] \ge 2/(n(n-1))$ per trial; amplify by repetition.
   - **Miller-Rabin** (Monte Carlo): fixed $O(k \log^3 n)$ runtime, $\fprate \le (1/4)^k$.
   One page.

4. **Amplification.** Las Vegas can be converted to Monte Carlo by capping runtime and giving up. Monte Carlo can be converted to Las Vegas if a verifier exists (run until correct). Half a page.

5. **The $\Bernoulli{\BoolType}$ correspondence.** Monte Carlo decision algorithms ARE $\Bernoulli{\BoolType}$ instances; their error rates are the framework's $\fprate, \fnrate$. Las Vegas algorithms are at a different abstraction level. Half a page.

**Labels:** `\section{Las Vegas vs Monte Carlo}` with `\label{sec:las-vegas-vs-monte-carlo}`. Definition `\label{def:las-vegas}`, `\label{def:monte-carlo}`.

**Target length:** ~5 pp (1100-1400 prose words).

**Workflow:** Standard.

---

### Task 4: §11.3 RP, BPP, and Bernoulli Type (~6 pp)

**Files:** Modify `book/chapters/ch11/rp-bpp.tex`.

**Purpose:** Define randomized complexity classes RP and BPP, frame each via the chapter 7 PPV vocabulary.

**Content checklist (5 items):**

1. **RP (Randomized Polynomial time).** Language $L \in \mathrm{RP}$ if there exists polynomial-time randomized algorithm $A$ such that:
   - $x \in L \Rightarrow \Pr[A(x) = 1] \ge 1/2$.
   - $x \notin L \Rightarrow \Pr[A(x) = 1] = 0$.
   I.e., one-sided error in the $\fprate = 0$ direction. RP is the "Bloom filter" of complexity classes. State as `\label{def:rp}`. One page.

2. **coRP.** The mirror: $\fnrate = 0$ direction. RP $\cap$ coRP = ZPP (zero-error probabilistic polynomial). One page.

3. **BPP (Bounded-Error Probabilistic Polynomial).** Both-sided error: $\Pr[A(x) = 1 \mid x \in L] \ge 2/3$ and $\Pr[A(x) = 1 \mid x \notin L] \le 1/3$. The PPV/NPV framing of chapter 7. State as `\label{def:bpp}`. One page.

4. **Amplification: error reduction by repetition.** For $k$ independent repetitions and majority vote, BPP error drops as $\exp(-\Omega(k))$ by Chernoff. State precisely. One page.

5. **The $\Bernoulli{\BoolType}$ correspondence at scale.** Each language's decision algorithm IS a $\Bernoulli{\BoolType}$. RP is the FNR-zero axis (perfect filter line of chapter 6). BPP is the interior of the rate plane. The chapter 6 perfect-filter line classifies complexity classes by their error structure. One page.

**Labels:** `\section{RP, BPP, and Bernoulli Type}` with `\label{sec:rp-bpp}`. Definitions `\label{def:rp}`, `\label{def:bpp}`, `\label{def:corp}`, `\label{def:zpp}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 5: §11.4 Sample Complexity (~5 pp)

**Files:** Modify `book/chapters/ch11/sample-complexity.tex`.

**Purpose:** Derive how many samples to reach target error rate via Chernoff bound. Connects to chapter 7 §7.2 binomial estimator.

**Content checklist (5 items):**

1. **The question.** Given target error $\epsilon$ and confidence $1 - \delta$, how many samples? One paragraph.

2. **Chernoff bound (multiplicative form).** For $X = \sum X_i$ with $X_i$ iid Bernoulli($p$) and $\mu = np$:
$$\Pr[X \ge (1+\epsilon) \mu] \le \exp(-\mu \epsilon^2 / 3)$$
for $\epsilon \in (0, 1]$. State as `\label{thm:chernoff}`. One page with proof sketch (moment-generating function + Markov).

3. **Application: Miller-Rabin sample count.** For target $\fprate^{(k)} \le \delta$ at $\fprate \le 1/4$ per round: $(1/4)^k \le \delta$, so $k \ge \log_4(1/\delta)$. At $\delta = 10^{-6}$, $k \ge 10$. Half a page.

4. **Application: BPP amplification.** $k$ repetitions + majority vote: error drops below $\delta$ when $k \ge (3/\epsilon^2) \ln(1/\delta)$ by Chernoff applied to the majority count. One page.

5. **Connection to chapter 7 §7.2.** Same binomial estimator machinery; the Chernoff bound here is the tight version of the variance-based CI of §7.3. Half a page.

**Labels:** `\section{Sample Complexity}` with `\label{sec:sample-complexity}`. Theorem `\label{thm:chernoff}`.

**Target length:** ~5 pp (1100-1500 prose words).

**Workflow:** Standard.

---

### Task 6: §11.5 Bridge (~1 pp)

**Files:** Modify `book/chapters/ch11/bridge.tex`.

**Content (1 paragraph):** Chapter 12 lifts to relations; chapter 13 unifies all of Part III via the type algebra.

**Labels:** `\section{Bridge}` with `\label{sec:ch11-bridge}`.

**Target length:** ~1 pp (300-500 prose words).

**Workflow:** Standard.

---

### Task 7: §11.6 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch11/bibliographic-notes.tex`; extend `book/references.bib`.

**Content (4 paragraphs):**

1. **Miller (1976) and Rabin (1980)** (already in bib): primality testing.

2. **Motwani-Raghavan (1995):** standard reference on randomized algorithms. Add bib entry.

3. **Mitzenmacher-Upfal** (already in bib): Chernoff bounds.

4. **Karger (1993):** randomized min-cut. Add bib entry.

**New bib entries:**

```bibtex
@book{motwani-raghavan,
  author    = {Rajeev Motwani and Prabhakar Raghavan},
  title     = {Randomized Algorithms},
  publisher = {Cambridge University Press},
  year      = {1995}
}

@inproceedings{karger-1993,
  author    = {David R. Karger},
  title     = {Global Min-cuts in {RNC}, and Other Ramifications of a Simple Min-Cut Algorithm},
  booktitle = {SODA},
  pages     = {21--30},
  year      = {1993}
}
```

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline` + `\label{sec:bib-notes-ch11}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 8: Chapter 11 Exercises (11)

**Files:** Modify `book/chapters/ch11/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Miller-Rabin rounds for target FPR.** For target $(1/4)^k \le 10^{-9}$, compute minimum $k$.

2. **Las Vegas vs Monte Carlo identification.** For three algorithms (randomized quicksort, Karger min-cut, Miller-Rabin), state which is LV vs MC.

3. **RP/BPP membership.** Decide whether the following languages are in RP, coRP, ZPP, BPP:
   - Primes (via Miller-Rabin): coRP.
   - Bipartite matching existence (deterministic poly-time): P (so all of the above).

**Medium (★★ × 5):**

4. **Notebook-tied: Miller-Rabin formal vs informal.** Run the chapter 11 notebook implementation against §3.4's version on $n = 341$. Verify the formal version's FPR matches the §3.4 informal one.

5. **Chernoff bound application.** For BPP amplification: derive how many repetitions to reduce error from $1/3$ to $1/2^{10}$.

6. **The perfect-filter analog.** Show that RP is exactly the complexity-class analog of chapter 5 §5.4's FNR-zero approximate sets.

7. **Las Vegas to Monte Carlo conversion.** For randomized quicksort, derive the probability that runtime exceeds $10 n \log n$.

8. **PPV for a BPP decision algorithm.** For a BPP algorithm with both-sided error 1/3, compute PPV at workload prevalence 0.1 using chapter 7 §7.4 formula.

**Challenging (★★★ × 3):**

9. **ZPP = RP intersect coRP.** Prove ZPP is exactly RP intersect coRP via the LV/MC conversion lemma.

10. **Karger amplification.** Karger's algorithm gives min-cut with probability $\ge 2/(n(n-1))$. Derive number of repetitions for confidence $\ge 1 - \delta$.

11. **Chernoff bound proof.** Reproduce the moment-generating-function proof of `\Cref{thm:chernoff}`.

**Target length:** ~2 pp.

**Workflow:** Standard.

---

### Task 9: Chapter 11 Notebook (`ch11-randomized-algorithms.ipynb`)

**Files:** Create `python/notebooks/ch11-randomized-algorithms.ipynb`.

**Content (~14-16 cells):**

1. Title + setup (numpy, matplotlib, sympy for primality verification).
2. **Miller-Rabin class** (code): implement formal version with $k$ rounds. Function `miller_rabin(n, k, rng)` returning `True` (probably prime) or `False` (composite witness found).
3. **Sanity check** (code): verify against sympy.isprime on a range of $n$.
4. **Empirical FPR vs theoretical** (code): for known Carmichael numbers ($n = 561, 1105, 1729$), run $k = 5$ rounds 1000 times; verify empirical FPR matches theoretical $(1/4)^5 = 1/1024$.
5. **Las Vegas randomized quicksort** (code): implement with random pivot; measure runtime distribution.
6. **Monte Carlo Karger** (code): implement Karger's min-cut on a small graph; run many trials; show success rate.
7. **LV vs MC runtime comparison** (code): plot runtime distributions for quicksort (LV; mean $O(n \log n)$ but tail variance) vs Karger ($O(n^2)$ deterministic).
8. **Chernoff bound verification** (code): for BPP amplification, simulate majority-vote error vs Chernoff bound.
9. **Discussion** (markdown): each randomized algorithm as a $\Bernoulli{\BoolType}$; the chapter 13 unification preview.

**Numerical sanity targets:**
- Miller-Rabin formal version: zero false negatives on a range of known primes/composites.
- Carmichael number FPR check: empirical $\hat{\fprate}$ at $k=5$ within $\pm 0.001$ of $1/1024 \approx 0.00098$.
- Quicksort: median runtime $\approx 1.4 n \ln n$.

**Workflow:** Standard. Execute end-to-end.

---

## Self-Review

Spec coverage: each section has its own task; substantive notebook covered. Cross-chapter references resolve.
