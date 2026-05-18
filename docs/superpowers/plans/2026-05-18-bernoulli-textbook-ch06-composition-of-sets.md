# Bernoulli Textbook Chapter 6: Composition of Sets (Plan 6)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 6 of Part II (~24 pp): the algebra of set operations ($\cup, \cap, \setminus, \complement$) for approximate sets, with error-rate propagation derived from chapter 3 §3.3's composition theorem applied to chapter 5's predicate framing. Includes the cancellation phenomena (composition can escape the perfect-filter line) and a formal treatment of the perfect-filter line as a closed subalgebra under some operations but not others.

**Architecture:** Replace `book/chapters/ch06-set-composition.tex` stub with a fully drafted chapter containing 6 sections, a learning-outcomes opener, 10-12 exercises, supporting bibliographic entries, and a paired Python notebook (`python/notebooks/ch06-set-composition.ipynb`) that simulates set ops on two Bloom filters and verifies the closed-form composition formulas.

**Tech Stack:** LaTeX (book class), alex.sty notation package, biblatex with biber backend. Python 3.11+ + numpy + matplotlib for the notebook.

**Scope:** Chapter 6 only. Part II integration check deferred to Plan 8.

**Spec source of truth:** `docs/superpowers/specs/2026-05-17-bernoulli-textbook-part2-design.md` §4 chapter 6 row.

**Base SHA:** `a132cfe` (HEAD at the end of Plan 5).

**Source material:**
- `papers/bernoulli_composition/sections/set_theory.tex` (set-operation error propagation; the main reformulation source for §6.1, §6.2)
- `papers/bernoulli_composition/sections/uncertain_rates.tex` (cancellation phenomena, fragments for §6.3)
- `book/chapters/ch03/composition-theorem.tex` (§3.3, the underlying composition theorem)
- `book/chapters/ch05/` (the predicate framing and Bloom filter, especially §5.4 perfect-filter line setup)

**Lessons inherited from Plans 1-5:**

1. **Page discipline.** Chapter 6 target is ~24 pp; expect 26-30 pp realistic. Plan 5 chapter 5 came in at 32pp on a 28pp target (+14%). Hold sections to lower-end word counts.

2. **Soul-voice hook (BLOCKING):** No Unicode em-dash (U+2014); no "lever" + "age" as a single word.

3. **Notation:** alex.sty macros throughout. The chapter-5 notation (`\ASet{A}`, `\Universe`, `\fprate`, `\fnrate`) carries forward. The deterministic-rates regime invoked in §5.3 applies throughout chapter 6.

4. **Cross-reference discipline.** Header comment block at the top of every section file. Use `\Cref{...}` not hardcoded section numbers.

5. **Per-task review cycle (Path A).** Each section task triggers spec + quality reviewers + fix subagent if substantive issues surface. Lower-risk sections (bib notes, signpost) can use a combined reviewer to save round-trips.

6. **Math sanity:** Numerical worked examples must be verified by hand. Plan 5 caught arithmetic errors in §5.2 ($(1-e^{-2})^{20}$) and §5.4 (Bloom space estimate); these are easy to slip and reviewers catch them when prompted to verify.

---

## File Structure

After this plan completes:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch06-set-composition.tex       # rewritten from stub to ~24 pp chapter scaffold
│   │   └── ch06/                          # NEW directory
│   │       ├── union.tex                  # §6.1 (~5 pp)
│   │       ├── other-set-ops.tex          # §6.2 (~5 pp) - intersection, complement, difference
│   │       ├── cancellation.tex           # §6.3 (~5 pp)
│   │       ├── perfect-filter-line.tex    # §6.4 (~4 pp)
│   │       ├── what-comes-next.tex        # §6.5 (~1 pp)
│   │       ├── bibliographic-notes.tex    # §6.6 (~2 pp)
│   │       └── exercises.tex              # 10-12 exercises (~2 pp)
│   └── references.bib                     # may be extended with composition-paper refs
└── python/
    └── notebooks/
        └── ch06-set-composition.ipynb     # light notebook: set-op simulator on two Bloom filters
```

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:set-composition` | `ch06-set-composition.tex` (already in Plan 0 stub) | already referenced from ch5 §5.5 |
| `sec:union-of-sets` | `ch06/union.tex` (Task 2) | (chapter 6 internal) |
| `sec:other-set-ops` | `ch06/other-set-ops.tex` (Task 3) | (chapter 6 internal) |
| `sec:cancellation` | `ch06/cancellation.tex` (Task 4) | (chapter 6 internal) |
| `sec:perfect-filter-line` | `ch06/perfect-filter-line.tex` (Task 5) | (chapter 6 internal); chapter 15 backward when that lands |
| `sec:ch6-what-comes-next` | `ch06/what-comes-next.tex` (Task 6) | (chapter 6 internal) |

**Backward references** (all resolve):
- Chapter 3: `\Cref{ch:boolean-algebra}`, `\Cref{sec:composition-theorem}`, `\Cref{thm:composition}`, `\Cref{eq:composition-theorem}`, `\Cref{sec:bridge-to-sets}`
- Chapter 5: `\Cref{ch:approximate-sets}`, `\Cref{sec:from-atom-to-set}`, `\Cref{sec:bloom-from-scratch}`, `\Cref{def:bloom-filter}`, `\Cref{sec:predicate-algebra}`, `\Cref{thm:bloom-optimal-k}`, `\Cref{sec:one-sided-two-sided}`, `\Cref{def:one-sided}`
- Chapter 4: `\Cref{sec:axiom-1}`, `\Cref{ax:element-indep}`, `\Cref{sec:axiom-2}`, `\Cref{ax:block-rates-indep}` for the independence framing where needed

**Forward references** to chapters 7, 8, 14, 15 use chapter-level `\Cref{ch:N}` (exist via Plan 0 stubs).

---

## Tasks

### Task 1: Read sources and write chapter scaffolding

**Files:** Modify `book/chapters/ch06-set-composition.tex`; create `book/chapters/ch06/` plus 7 placeholders.

**Source reading:**
- `papers/bernoulli_composition/sections/set_theory.tex`
- `papers/bernoulli_composition/sections/uncertain_rates.tex`
- `book/chapters/ch05/` all section files (for inheritance check)
- Part II spec §4 chapter 6 row

**Steps:**

- [ ] Read sources end-to-end.
- [ ] Replace `book/chapters/ch06-set-composition.tex` with scaffold:

```latex
\chapter{Composition of Sets}
\label{ch:set-composition}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Derive the error rates of $\cup, \cap, \setminus, \complement$
    for approximate sets by applying the composition theorem of
    \Cref{thm:composition} to the predicate framing of
    \Cref{ch:approximate-sets}.
  \item Recognize the cancellation phenomena that let composed sets
    escape the perfect-filter line.
  \item State the closure properties of the perfect-filter line and
    name which set operations preserve one-sidedness.
\end{itemize}
\end{quote}

% Section 6.1
\input{chapters/ch06/union}

% Section 6.2
\input{chapters/ch06/other-set-ops}

% Section 6.3
\input{chapters/ch06/cancellation}

% Section 6.4
\input{chapters/ch06/perfect-filter-line}

% Section 6.5
\input{chapters/ch06/what-comes-next}

% Section 6.6
\input{chapters/ch06/bibliographic-notes}

% Exercises
\input{chapters/ch06/exercises}
```

- [ ] Create `book/chapters/ch06/` and 7 placeholder files (`union.tex`, `other-set-ops.tex`, `cancellation.tex`, `perfect-filter-line.tex`, `what-comes-next.tex`, `bibliographic-notes.tex`, `exercises.tex`), each containing `% Placeholder. Drafted in Plan 6 Task N.` with N substituted (2, 3, 4, 5, 6, 7, 8).
- [ ] Build: `cd book && make cleanall && make`. Exit 0.
- [ ] Commit:

```
book: scaffold chapter 6 (composition of sets) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener, six section subfile inputs (union, other-set-ops, cancellation,
perfect-filter-line, what-comes-next, bibliographic-notes), plus an
exercises subfile, with matching empty placeholders. Section drafts
land in subsequent Plan 6 tasks.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §6.1 Union of Approximate Sets (~5 pp)

**Files:** Modify `book/chapters/ch06/union.tex`.

**Source reading:** `papers/bernoulli_composition/sections/set_theory.tex` (union of approximate sets); `book/chapters/ch03/composition-theorem.tex` (composition theorem to apply); `book/chapters/ch05/bloom-from-scratch.tex` (Bloom filter for the worked example).

**Purpose:** Derive the error rates of $\tilde A \cup \tilde B$ from chapter 3 §3.3's composition theorem applied to the predicate framing.

**Content checklist:**

1. **Definition of union for approximate sets.** $\tilde A \cup \tilde B$ is the approximate set whose membership predicate is $\tilde A(x) \lor \tilde B(x)$ (the Boolean OR of the two membership predicates). One paragraph.

2. **Operational view (Bloom filter):** for two Bloom filters $B_1, B_2$ over the same universe $\Universe$ with the same hash family and same $m$, the union is computed by bit-wise OR of the bit arrays. This is the canonical implementation; mention briefly.

3. **FPR derivation.** A false positive for $\tilde A \cup \tilde B$ at $x \notin A \cup B$ means BOTH $x \notin A$ AND $x \notin B$ AND the predicates report $\top$ for at least one. The structural form: $\fprate_{\cup} = 1 - (1 - \fprate_A)(1 - \fprate_B)$ under independence of the two predicates' error events at $x$. Derive from $\Pr[\text{at least one false-positive event}] = 1 - \Pr[\text{neither}]$.

4. **FNR derivation.** A false negative for $\tilde A \cup \tilde B$ at $x \in A \cup B$ requires $\tilde A(x) = \bot$ AND $\tilde B(x) = \bot$. Two sub-cases depending on whether $x$ is in $A$, $B$, or both. State $\fnrate_{\cup}$ cleanly, noting it depends on the prior distribution over which set $x$ comes from when both could contain it.

5. **Worked example.** Two Bloom filters with $\fprate_1 = 0.01, \fprate_2 = 0.02$, both FNR-zero (one-sided). Union: $\fprate_{\cup} = 1 - 0.99 \cdot 0.98 = 0.0298$. FNR: still 0 (both operands are FNR-zero). One paragraph.

6. **Reference back to chapter 3.** This is the composition theorem (`\Cref{thm:composition}` from §3.3) applied to the OR gate, which §3.2 already analyzed. The union derivation is the same Boolean algebra under noise, now interpreted at the set level. Half a paragraph.

7. **Signpost:** §6.2 covers intersection, complement, difference.

**Labels:** `\section{Union of Approximate Sets}` with `\label{sec:union-of-sets}`; theorem or proposition labels (`\label{thm:union-fpr-fnr}` or similar) for the closed-form rate formulas.

**Notation:** $\tilde A \cup \tilde B$ for the union; $\fprate_A, \fprate_B$ for operand rates; $\fprate_{\cup}, \fnrate_{\cup}$ for output.

**Target length:** ~5 pp (1100-1400 prose words).

**Workflow:** Read sources → draft → build (exit 0) → commit:

```
book: draft chapter 6.1 Union of Approximate Sets (~5 pp)

Definition of union for approximate sets via OR of membership
predicates. FPR derivation from independence: 1 - (1 - eps_A)(1 - eps_B).
FNR derivation: combines the two operands' FNRs under the prior over
which set x comes from. Worked example with two FNR-zero Bloom filters
(eps_1 = 0.01, eps_2 = 0.02) giving eps_union = 0.0298, FNR_union = 0.
Composition theorem of §3.3 invoked as the underlying machinery.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

Then dispatch spec + quality reviewers; fix subagent if substantive issues.

---

### Task 3: §6.2 Intersection, Complement, Difference (~5 pp)

**Files:** Modify `book/chapters/ch06/other-set-ops.tex`.

**Source reading:** Same as Task 2 plus `papers/bernoulli_composition/sections/set_theory.tex` (intersection and complement coverage).

**Content checklist:**

1. **Intersection.** $\tilde A \cap \tilde B$ membership predicate is $\tilde A(x) \land \tilde B(x)$ (AND). FPR derivation: $\fprate_{\cap} = \fprate_A \cdot \fprate_B$ (assuming independence). FNR derivation: $\fnrate_{\cap} = 1 - (1 - \fnrate_A)(1 - \fnrate_B)$ (dual structure to union). Quick observation: intersection FPR is generally MUCH smaller than the operand FPRs (multiplicative), whereas union FNR is additive in the same sense.

2. **Complement.** $\complement \tilde A$ membership predicate is $\neg \tilde A(x)$. Trivial swap: $\fprate_{\complement} = \fnrate_A$, $\fnrate_{\complement} = \fprate_A$. State this as a proposition; backward-reference chapter 3 §3.2 (NOT under noise) where the same result appeared at the noisy-bit level.

3. **Difference.** $\tilde A \setminus \tilde B = \tilde A \cap \complement \tilde B$. Composition: apply intersection then complement formulas. Worked example.

4. **Worked numerical example.** Two Bloom filters, $\fprate_1 = 0.01, \fnrate_1 = 0, \fprate_2 = 0.02, \fnrate_2 = 0$. Intersection: $\fprate_{\cap} = 0.01 \cdot 0.02 = 0.0002$, $\fnrate_{\cap} = 1 - 1 \cdot 1 = 0$. So the intersection of two FNR-zero Bloom filters is still FNR-zero AND has a vastly smaller FPR. Good.

5. **Signpost:** §6.3 discusses cancellation phenomena that can break these clean formulas.

**Labels:** `\section{Intersection, Complement, Difference}` with `\label{sec:other-set-ops}`; propositions for each operation's rate formulas.

**Target length:** ~5 pp (1100-1400 prose words).

**Workflow:** Standard task pattern; commit:

```
book: draft chapter 6.2 Intersection, Complement, Difference (~5 pp)

Intersection: FPR_cap = eps_A * eps_B (multiplicative, very small);
FNR_cap = 1 - (1-omega_A)(1-omega_B). Complement: trivial swap of
FPR and FNR (proposition with backward ref to §3.2 NOT-under-noise).
Difference: A \ B = A intersect complement(B). Worked example: two
FNR-zero Bloom filters at eps = 0.01, 0.02 give intersection FPR of
0.0002 with FNR still 0.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 4: §6.3 Cancellation and the Loss of One-Sidedness (~5 pp)

**Files:** Modify `book/chapters/ch06/cancellation.tex`.

**Source reading:** `papers/bernoulli_composition/sections/uncertain_rates.tex` (cancellation, fragments). This is partly fresh writing.

**Content checklist:**

1. **The phenomenon.** Composition can ESCAPE the perfect-filter line: starting with one-sided approximate sets, the result of a composition can have BOTH rates positive (or even swap which rate is zero). Concrete trigger: complement of a one-sided set is one-sided in the OTHER direction (FNR-zero becomes FPR-zero).

2. **Worked example: complement of Bloom union.** $\complement(\tilde A \cup \tilde B)$ for two FNR-zero Bloom filters. The union is still FNR-zero with $\fprate_{\cup} = 1 - (1-\fprate_A)(1-\fprate_B)$. The complement swaps: $\fnrate' = \fprate_{\cup}$ (was the union FPR) and $\fprate' = 0$ (was the union FNR). So we've moved from "FNR-zero" to "FPR-zero" by applying complement. Half a page.

3. **Worked example: intersection of one set and the complement of another.** Compose intersection ($\fprate_{\cap} = \fprate_A \cdot \fprate_B$) with complement. The chain produces both rates nonzero in general. Show the algebra.

4. **The "escape" structurally.** The perfect-filter line is two axes in the $(\fprate, \fnrate)$ plane (FNR-zero axis and FPR-zero axis). Some operations (union, intersection of one-sided same-direction sets) PRESERVE the axis you're on. Other operations (complement, intersection of one-sided opposite-direction sets) MOVE you between axes or off both. State this geometrically.

5. **Why this matters.** Chapter 7 (PPV/NPV) is sensitive to one-sidedness; chapter 15 (perfect hash filters) achieves FPR-zero on a designed-in set; chapter 14 (BHF) achieves the entropy floor on the FNR-zero axis. Composition discipline is the price for staying near the floor. Reference forward.

6. **Signpost:** §6.4 makes the perfect-filter line concept precise.

**Labels:** `\section{Cancellation and the Loss of One-Sidedness}` with `\label{sec:cancellation}`.

**Target length:** ~5 pp (1100-1400 prose words).

**Workflow:** Standard task pattern; commit:

```
book: draft chapter 6.3 Cancellation and the Loss of One-Sidedness (~5 pp)

Composition can ESCAPE the perfect-filter line: complement of an
FNR-zero set is FPR-zero (rates swap); intersection of one set with
the complement of another generally has both rates nonzero. Two
worked examples: complement of a Bloom union, and an intersection
chain with a complement. Geometric framing: the perfect-filter line
is two axes; some operations preserve the axis, others move you
between them or off both. Forward-reference chapters 7, 14, 15.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 5: §6.4 The Perfect Filter Line (~4 pp)

**Files:** Modify `book/chapters/ch06/perfect-filter-line.tex`.

**Source reading:** Same as Task 4 plus chapter 5 §5.4 `book/chapters/ch05/one-sided-two-sided.tex` for the line's introduction.

**Content checklist:**

1. **Definition.** The perfect-filter line is the union of two coordinate axes in the $(\fprate, \fnrate) \in [0, 1]^2$ plane: the FNR-zero axis ($\fnrate = 0$) and the FPR-zero axis ($\fprate = 0$). Restate with `\label{def:perfect-filter-line}`.

3. **Closure properties of the FNR-zero axis.**
  - Union of two FNR-zero sets is FNR-zero. (From §6.1.)
  - Intersection of two FNR-zero sets is FNR-zero. (From §6.2.)
  - Complement of an FNR-zero set is FPR-zero (on the other axis).
  - Difference $A \setminus B$ when $A$ is FNR-zero and $B$ is FPR-zero (i.e., $B$ is a perfect filter): result is FNR-zero. Otherwise can leave the line.

3. **Closure properties of the FPR-zero axis.** Symmetric (by complement-swap). Mention briefly.

4. **The algebraic shape.** The two axes together form a non-convex subset of the rate plane; their intersection is the origin (the exact-set point). The line is preserved by some operations and escaped by others, as §6.3 showed. State as a proposition: "the FNR-zero axis is closed under union and intersection but not under complement."

5. **Forward-reference chapters 14 and 15.** The constructive realization of an approximate set ON the FNR-zero axis with the lowest possible space cost is chapter 14's BHF. Chapter 15's perfect hash filter is constructive realization on the FPR-zero axis for a designated input set.

**Labels:** `\section{The Perfect Filter Line}` with `\label{sec:perfect-filter-line}`; `\label{def:perfect-filter-line}`; closure proposition `\label{prop:fnr-zero-closure}`.

**Target length:** ~4 pp (900-1200 prose words). Keep tight; this is mostly classification of closure properties.

**Workflow:** Standard task pattern; commit:

```
book: draft chapter 6.4 The Perfect Filter Line (~4 pp)

Formal definition of the perfect-filter line as the union of the
FNR-zero and FPR-zero axes in the (FPR, FNR) plane. Closure
properties: each axis is closed under union and intersection;
complement maps between the two axes; difference generally escapes
unless one operand is a perfect filter. Forward-references chapter 14
(BHF on FNR-zero axis) and chapter 15 (BPHF on FPR-zero axis).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 6: §6.5 What Comes Next (~1 pp)

**Files:** Modify `book/chapters/ch06/what-comes-next.tex`.

**Content checklist:**

1. Chapter 7 (Classification Measures): the rates this chapter computed feed into PPV, NPV, F1 estimates. The chapter 1 §1.4 deferral on proper CIs gets retired.

2. Chapter 8 (Information-Theoretic Bounds): the operations of this chapter have a space-cost analog; the entropy floor for an FNR-zero set governs how much the operations can compress, and chapter 14 achieves the floor.

3. Closing one-paragraph: §6.6 names the antecedents.

**Labels:** `\section{What Comes Next}` with `\label{sec:ch6-what-comes-next}`.

**Target length:** ~1 pp (300-500 prose words). Short by design.

**Workflow:** Standard; commit:

```
book: draft chapter 6.5 What Comes Next (~1 pp)

Brief signpost to chapter 7 (rates feed into PPV/NPV/F1 with proper
CIs, retiring the chapter 1 §1.4 deferral) and chapter 8 (entropy
floor for the FNR-zero axis, achieved constructively in chapter 14).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 7: §6.6 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch06/bibliographic-notes.tex`; possibly extend `book/references.bib`.

**Content (3-4 paragraphs):**

1. **`towell-bernoulli-composition` paper:** the set-operation error propagation framework. Add bib entry if not present.

2. **Bloom filter union/intersection:** the bit-wise OR/AND implementation is folklore; cite Mitzenmacher-Upfal §5 or Broder-Mitzenmacher (2004) for survey context.

3. **De Morgan's laws under noise:** the complement-swap result has a precedent in chapter 3 §3.2; the connection to classical De Morgan is the right pedagogical bridge.

4. **Perfect filter literature:** Carter-Wegman perfect hashing (already in bib from Plan 5) as the predecessor; chapter 15 will cite the BPHF paper for the constructive realization.

**Possible new bib entries (add only if cited):**

```bibtex
@misc{towell-bernoulli-composition,
  author       = {Alexander Towell},
  title        = {Composition of {Bernoulli} sets},
  year         = {2026},
  note         = {Manuscript},
  howpublished = {\url{https://github.com/queelius/bernoulli_composition}}
}
```

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline{toc}{section}{Bibliographic Notes}` + `\label{sec:bib-notes-ch6}` matching ch01-ch05 precedent.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard; commit:

```
book: draft chapter 6.6 Bibliographic Notes (~2 pp); extend bib if needed

Attribute set-operation error propagation to the towell-bernoulli-
composition paper (new bib entry). Survey context to Mitzenmacher-
Upfal; perfect-filter precedent to Carter-Wegman.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 8: Chapter 6 Exercises (10-12)

**Files:** Modify `book/chapters/ch06/exercises.tex`.

**Source reading:** ch01-ch05 exercises for style precedent.

**Exercise set (11 exercises, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Union FPR computation.** Two FNR-zero Bloom filters with $\fprate_1 = 0.05, \fprate_2 = 0.10$. Compute $\fprate_{\cup}$ and $\fnrate_{\cup}$.

2. **Intersection FPR computation.** Same filters. Compute $\fprate_{\cap}$ and $\fnrate_{\cap}$.

3. **Complement-swap verification.** For an approximate set with $\fprate = 0.03, \fnrate = 0.07$, write the rates of its complement.

**Medium (★★ × 5):**

4. **Notebook-tied set-op verification.** Use `python/notebooks/ch06-set-composition.ipynb` to build two Bloom filters with $m = 5000, n = 500$, each at $\fprate \approx 0.01, \fnrate = 0$. Empirically compute the FPR of their union and compare to the closed-form $1 - (1 - \fprate_1)(1 - \fprate_2)$.

5. **Difference algebra.** Show $\fprate_{A \setminus B} = \fprate_A \cdot \fnrate_B$ when $B$ is FPR-zero (perfect filter, $\fprate_B = 0$). When $B$ is FNR-zero instead, derive the result.

6. **De Morgan under noise.** Verify $\complement(\tilde A \cup \tilde B)$ and $\complement \tilde A \cap \complement \tilde B$ give the same FPR/FNR formulas (when independence holds). The De Morgan duality holds for the rate algebra.

7. **Independence sensitivity.** §6.1's union FPR derivation assumes the two operands' error events are independent at a query $x$. Construct a small example where they are NOT independent (e.g., shared hash family) and show the formula breaks.

8. **Intersection escape.** Show how intersecting an FNR-zero set with an FPR-zero set generally produces BOTH rates positive. Derive the formula.

**Challenging (★★★ × 3):**

9. **Three-way composition.** Derive $\fprate$ for $\tilde A \cup \tilde B \cup \tilde C$ in two ways: (i) by chained pairwise union, (ii) directly from independence. Verify they agree. Then argue this is the composition theorem $\eta_{\text{total}} = 1 - \prod(1 - \eta_i)$ from chapter 3 §3.3 at $k = 3$.

10. **Perfect filter as inverse.** A perfect filter ($\fprate = 0$ on a designated input set) followed by an FNR-zero filter ($\fnrate = 0$) can produce an exact-set test on the intersection of their respective domains. Sketch the construction and the conditions under which it gives FPR = FNR = 0.

11. **Forward to chapter 14.** The chapter 8 entropy floor for an FNR-zero set with FPR $\fprate$ is $-\log_2 \fprate$ bits per element. Show that the union operation cannot beat this floor: $\tilde A \cup \tilde B$ at output FPR $\fprate_{\cup}$ requires at least $|A \cup B| \cdot (-\log_2 \fprate_{\cup})$ bits to represent, by the same entropy argument. (This sets up the BHF discussion of chapter 14.)

**Labels:** `\label{ex:ch6-N}` for $N = 1, \ldots, 11$. `\providecommand` block matching ch01-ch05.

**Target length:** ~2 pp (700-900 prose words).

**Workflow:** Standard; commit:

```
book: draft chapter 6 exercises (11 with star difficulty markers)

3 warm-ups (union, intersection, complement rate computations), 5
medium (notebook set-op verification, difference algebra, De Morgan
under noise, independence sensitivity, intersection escape from
perfect-filter line), 3 challenging (three-way composition via
composition theorem, perfect filter as inverse, entropy-floor bound
on union operation).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 9: Chapter 6 Notebook (`ch06-set-composition.ipynb`)

**Files:** Create `python/notebooks/ch06-set-composition.ipynb`.

**Source reading:** `python/notebooks/ch05-approximate-sets.ipynb` (Bloom filter implementation precedent); ch01-ch03 notebooks for style.

**Purpose:** Light notebook (per master spec): simulate two Bloom filters and verify the §6.1, §6.2 composition formulas empirically.

**Content checklist (~10-12 cells):**

1. **Title cell** (markdown).
2. **Setup** (code): imports + seeded RNG.
3. **Reuse Bloom filter class from chapter 5** (code): either re-import the class definition or restate it briefly. Note the per-index salt hash construction.
4. **Two filters cell** (code): build $B_1$ with item set $S_1$, $B_2$ with item set $S_2$ (overlapping universe). Use $m = 5000, k = 7, n_1 = n_2 = 500$.
5. **Union by bit-OR cell** (code): construct $B_1 \cup B_2$ via bit-OR of the bit arrays. Query $10000$ random items; compute empirical FPR. Compare to closed-form $1 - (1 - \fprate_1)(1 - \fprate_2)$.
6. **Intersection by bit-AND cell** (code): construct $B_1 \cap B_2$ via bit-AND. Query as above. Compare to $\fprate_1 \cdot \fprate_2$ (but flag that bit-AND ≠ predicate-AND; they may differ for Bloom filters; this is the "intersection of two Bloom filters is not generally a Bloom filter for the intersection of the underlying sets" gotcha that chapter 6 §6.2 should mention).
7. **Discussion cell** (markdown): the bit-AND/predicate-AND distinction; references chapter 6 §6.2.
8. **Open question cell** (markdown): what if the two filters use DIFFERENT hash families? Then bit-OR/AND no longer make sense. Forward-reference chapter 14 (BHF) and chapter 15 (BPHF) for hash-aligned constructions.

**Numerical sanity targets:**
- Union empirical FPR matches formula within $\pm 0.005$ for $m = 5000, n_1 = n_2 = 500, k = 7$.
- Bit-AND intersection FPR may NOT match $\fprate_1 \cdot \fprate_2$ exactly (because of the bit-AND/predicate-AND issue); flag this empirically.

**Run-to-completion:** notebook MUST execute end-to-end.

**Workflow:**

1. Read precedent notebooks.
2. Draft notebook as valid nbformat-4 JSON.
3. Execute:
   ```bash
   cd python && uv run jupyter nbconvert --to notebook --execute notebooks/ch06-set-composition.ipynb --output ch06-set-composition.ipynb 2>&1 | tail -20
   ```
4. Verify outputs.
5. Commit:

```
python: add chapter 6 notebook (set composition)

Two Bloom filters at m=5000, n=500, k=7. Union by bit-OR, empirical
FPR matches closed-form 1 - (1-eps_1)(1-eps_2). Intersection by
bit-AND: flag the gotcha that bit-AND of Bloom filters is NOT the
Bloom filter for the intersection of the underlying sets. Open
question forward-references chapters 14 and 15.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Self-Review

Spec coverage:
- Part II spec §4 chapter 6 row: each section has its own task (Tasks 2-7).
- Master spec "light notebook" for ch6: Task 9.
- 10-12 exercises: Task 8.

Placeholder scan: none.

Type and label consistency: Labels match across this plan; chapter 5's labels are correctly invoked from chapter 6's backward references.
