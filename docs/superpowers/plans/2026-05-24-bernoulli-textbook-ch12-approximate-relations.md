# Bernoulli Textbook Chapter 12: Approximate Relations (Plan 12)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 12 of Part III (~22 pp): lift the approximate-set framework of Part II to relations. A relation is a subset of $T \times U$; an approximate relation is a $\Bernoulli{\BoolType}$ on $T \times U$. Composition via natural join under noise; standard approximate-join database algorithms (using MinHash from §10.4) appear as instances.

**Architecture:** Replace `book/chapters/ch12-approximate-relations.tex` stub with a fully drafted chapter containing 5 sections, learning-outcomes opener, 10-12 exercises, bibliographic entries, and a paired Python notebook demonstrating approximate joins.

**Tech Stack:** LaTeX (book class), alex.sty, biblatex+biber. Python 3.11+ + numpy + matplotlib for the notebook.

**Scope:** Chapter 12 only. Part III integration is Plan 13 Task 10.

**Spec source of truth:** `docs/superpowers/specs/2026-05-23-bernoulli-textbook-part3-design.md` §4 chapter 12 row.

**Base SHA:** `efe0180` (HEAD at end of Plan 11).

**Source material:**
- `papers/bernoulli_relations/sections/` (primary source)
- `book/chapters/ch05/` (approximate sets foundation)
- `book/chapters/ch10/minhash-lsh.tex` (§10.4 MinHash for §12.3 approximate joins)
- `book/chapters/ch06/` (set composition, especially intersection)
- `book/chapters/ch09/` (n-ary framework)

**Lessons inherited from Plans 1-11:**

1. **Page discipline.** Chapter 12 target ~22pp; expect 24-28pp.

2. **Soul-voice hook (BLOCKING):** Respect the full banned-phrase list. Substring matching.

3. **Notation:** alex.sty `\ARelation` (verified present in alex.sty from Task 0 of Plan 7) for the approximate relation $\tilde R$; `\Universe` for universes; standard $T \times U$ Cartesian product; $\bowtie$ for natural join (`\bowtie` is standard LaTeX).

4. **Chapter 5/6 sets are the structural template.** Each section mirrors a chapter 5/6 counterpart at the relation level.

---

## File Structure

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch12-approximate-relations.tex      # rewritten from stub
│   │   └── ch12/                                # NEW directory
│   │       ├── sets-to-relations.tex            # §12.1 (~3 pp)
│   │       ├── relation-composition.tex         # §12.2 (~6 pp)
│   │       ├── approximate-joins.tex            # §12.3 (~6 pp)
│   │       ├── bridge.tex                       # §12.4 (~1 pp)
│   │       ├── bibliographic-notes.tex          # §12.5 (~2 pp)
│   │       └── exercises.tex                    # 10-12 exercises (~2 pp)
│   └── references.bib                           # extended (towell-bernoulli-relations)
└── python/
    └── notebooks/
        └── ch12-approximate-relations.ipynb     # approximate-join simulator
```

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:approximate-relations` | `ch12-approximate-relations.tex` (Plan 0 stub) | (forward refs from prior chapters) |
| `sec:sets-to-relations` | `ch12/sets-to-relations.tex` (Task 2) | (internal) |
| `sec:relation-composition` | `ch12/relation-composition.tex` (Task 3) | (internal) |
| `sec:approximate-joins` | `ch12/approximate-joins.tex` (Task 4) | (internal); chapter 10 §10.4 backward |
| `sec:ch12-bridge` | `ch12/bridge.tex` (Task 5) | (internal) |

Backward references that should resolve:
- Chapter 5: `\Cref{ch:approximate-sets}`, `\Cref{sec:from-atom-to-set}`, `\Cref{def:one-sided}`
- Chapter 6: `\Cref{ch:set-composition}`, `\Cref{prop:union-fpr-fnr}`, `\Cref{prop:intersection-fpr-fnr}`
- Chapter 9: `\Cref{ch:approximate-functions}`, `\Cref{sec:n-ary-channels}`
- Chapter 10: `\Cref{sec:minhash-lsh}`, `\Cref{def:minhash}`, `\Cref{prop:minhash-error}`

---

## Tasks

### Task 1: Read sources and write chapter scaffolding

- [ ] Read sources: `papers/bernoulli_relations/sections/` end-to-end (skim); `book/chapters/ch05/from-atom-to-set.tex` (§5.1); `book/chapters/ch10/minhash-lsh.tex` (§10.4); Part III spec §4 chapter 12.

- [ ] Replace `book/chapters/ch12-approximate-relations.tex` with the scaffold:

```latex
\chapter{Approximate Relations}
\label{ch:approximate-relations}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Define an approximate relation $\tilde R \subseteq T \times U$
    as a $\Bernoulli{\BoolType}$ on $T \times U$, and write its FPR
    and FNR.
  \item Compose approximate relations via natural join, projection,
    and selection; derive the propagation of FPR/FNR under each.
  \item Recognize standard approximate-join algorithms (MinHash-based
    similarity joins, in particular) as instances of the framework.
\end{itemize}
\end{quote}

% Section 12.1
\input{chapters/ch12/sets-to-relations}

% Section 12.2
\input{chapters/ch12/relation-composition}

% Section 12.3
\input{chapters/ch12/approximate-joins}

% Section 12.4
\input{chapters/ch12/bridge}

% Section 12.5
\input{chapters/ch12/bibliographic-notes}

% Exercises
\input{chapters/ch12/exercises}
```

- [ ] Create `book/chapters/ch12/` + 6 placeholders: `sets-to-relations.tex`, `relation-composition.tex`, `approximate-joins.tex`, `bridge.tex`, `bibliographic-notes.tex`, `exercises.tex`. Each: `% Placeholder. Drafted in Plan 12 Task N.` (N = 2-7).

- [ ] Build exit 0.

- [ ] Commit:

```
book: scaffold chapter 12 (approximate relations) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener (three bullets: define approximate relations, composition via
join/projection/selection, MinHash-based similarity joins as
instances), five section subfile inputs plus exercises, with matching
empty placeholders.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §12.1 From Approximate Sets to Approximate Relations (~3 pp)

**Files:** Modify `book/chapters/ch12/sets-to-relations.tex`.

**Content checklist (4 items):**

1. **Recap.** A relation $R \subseteq T \times U$ is just a set whose elements are pairs. An approximate relation $\tilde R$ is therefore an approximate set on the universe $T \times U$. The chapter 5 framework lifts unchanged. Half a page; cite `\Cref{ch:approximate-sets}`.

2. **The membership predicate.** $\tilde R(t, u) \in \{\top, \bot\}$ reports whether $(t, u)$ is in the relation, with FPR and FNR per the chapter 5 framework. One paragraph.

3. **Examples.**
   - "Friend-of" relation on persons: $\tilde R \subseteq P \times P$.
   - "Word-in-document" relation: $\tilde R \subseteq W \times D$ (an inverted index).
   - Both can be approximated for space (Bloom-filter-like representations) or for compute (sampling-based estimators).
   One page.

4. **What changes structurally?** The chapter 9 n-ary framework applies: the "input" is the pair $(t, u)$; the model order is $|T \times U|$ at the predicate level, two at the truth level. Half a page.

5. **Signpost.** §12.2 composes; §12.3 instantiates with similarity joins.

**Labels:** `\section{From Approximate Sets to Approximate Relations}` with `\label{sec:sets-to-relations}`.

**Header cross-reference comment block.**

**Target length:** ~3 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 3: §12.2 Composition of Approximate Relations (~6 pp)

**Files:** Modify `book/chapters/ch12/relation-composition.tex`.

**Purpose:** Derive natural join, projection, selection under noise.

**Content checklist (5 items):**

1. **Natural join.** $R_1 \bowtie R_2$ on common attribute. The output tuple $(t, u, v)$ is in $R_1 \bowtie R_2$ iff $(t, u) \in R_1$ AND $(u, v) \in R_2$. Approximate version: $\tilde R_1 \bowtie \tilde R_2$ membership predicate is $\tilde R_1(t, u) \land \tilde R_2(u, v)$. FPR/FNR derivation: by AND under noise (chapter 3 §3.1) lifted to relations. One page.

2. **FPR and FNR under join (the headline).** Theorem: for two FNR-zero approximate relations with FPRs $\fprate_1, \fprate_2$, the join has $\fnrate_\bowtie = 0$ and $\fprate_\bowtie = \fprate_1 \fprate_2$ (under cross-relation independence). State as `\label{thm:join-rates}`. One page; cite `\Cref{prop:intersection-fpr-fnr}` from chapter 6.

3. **Projection.** $\pi_T(\tilde R)$ projects onto attribute $T$: the result is the set $\{t : \exists u, (t, u) \in \tilde R\}$. Under noise: $\hat{t} \in \pi_T(\tilde R)$ if $\exists u$ s.t. $\tilde R(t, u) = \top$. FPR amplifies (any spurious pair gives a spurious projection); FNR stays at 0 if input was FNR-zero. One page.

4. **Selection.** $\sigma_P(\tilde R) := \{(t, u) \in \tilde R : P(t, u) = \top\}$ for a predicate $P$. If $P$ is exact: FPR/FNR unchanged. If $P$ is itself approximate: AND of two noisy predicates. Half a page.

5. **Worked example.** A friend-of relation as Bloom-like approximate relation; natural-join with a is-a-coworker relation; derive FPR of "friend-and-coworker" pairs. Half a page.

**Labels:** `\section{Composition of Approximate Relations}` with `\label{sec:relation-composition}`. Theorem `\label{thm:join-rates}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 4: §12.3 Approximate Joins in Databases (~6 pp)

**Files:** Modify `book/chapters/ch12/approximate-joins.tex`.

**Purpose:** Concrete approximate-join algorithms (MinHash-based) as instances.

**Content checklist (5 items):**

1. **The similarity-join problem.** Given two large relations $R_1, R_2$, find all pairs $(r_1, r_2)$ with Jaccard similarity above threshold $\theta$. Exact computation is $O(|R_1| |R_2|)$; can we approximate in sub-quadratic time? One page.

2. **MinHash similarity join.** Compute MinHash signature for each row in both relations. For each pair $(r_1, r_2)$, $\hat{J}(r_1, r_2) = $ fraction of matching signature positions. The chapter 10 §10.4 framework gives the per-pair error. One page.

3. **LSH bands.** Hash MinHash signatures into bands; collide bands for candidate pairs. Sub-linear in expected output size. Recall `\Cref{sec:minhash-lsh}`. One page.

4. **FPR/FNR for the join.** False positive: a pair classified as "similar" when their true $J < \theta$. False negative: a similar pair missed. The MinHash error bound (`\Cref{prop:minhash-error}`) gives both; LSH band parameters $(r, b)$ tune the trade-off. One page.

5. **Worked example.** Two relations of 1000 rows each; similarity threshold $\theta = 0.5$; $k = 200$ MinHash, $b = 20, r = 10$. Estimate output size, FPR, FNR. One page.

**Labels:** `\section{Approximate Joins in Databases}` with `\label{sec:approximate-joins}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 5: §12.4 Bridge (~1 pp)

**Files:** Modify `book/chapters/ch12/bridge.tex`.

**Content:** §12.5 names antecedents; chapter 13 unifies all of Part III via the type algebra.

**Labels:** `\section{Bridge}` with `\label{sec:ch12-bridge}`.

**Target length:** ~1 pp (300-500 prose words).

**Workflow:** Standard.

---

### Task 6: §12.5 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch12/bibliographic-notes.tex`; extend `book/references.bib`.

**Content (3-4 paragraphs):**

1. **`towell-bernoulli-relations` paper** as primary source. Add bib entry.

2. **Database approximate-join literature:** Sarawagi-Kirpal 2004 (set similarity joins) and Xiao et al survey if cited.

3. **Codd's relational model** as the classical foundation. Cite Codd 1970 if helpful.

**New bib entries:**

```bibtex
@misc{towell-bernoulli-relations,
  author = {Alexander Towell},
  title  = {The abstract data type of the approximate relation},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/bernoulli_relations}}
}
```

(Add Sarawagi-Kirpal etc. only if cited.)

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline` + `\label{sec:bib-notes-ch12}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 7: Chapter 12 Exercises (11)

**Files:** Modify `book/chapters/ch12/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Join FPR computation.** Two FNR-zero approximate relations with $\fprate_1 = 0.05, \fprate_2 = 0.10$. Compute $\fprate_\bowtie$ under cross-relation independence.

2. **Projection FPR amplification.** A relation with 100 attribute values for each row; FPR of $\tilde R(t, u)$ is 0.01 per pair. What is the FPR of $\hat{t} \in \pi_T(\tilde R)$?

3. **Selection composition.** A relation with FPR 0.02 selected by an exact predicate. State the output FPR.

**Medium (★★ × 5):**

4. **Notebook-tied join.** Use the chapter 12 notebook to perform a MinHash similarity join on two synthetic relations; compare empirical to theoretical FPR/FNR.

5. **De Morgan for relations.** Show $\complement(\tilde R_1 \cup \tilde R_2) = \complement \tilde R_1 \cap \complement \tilde R_2$ holds for the rate algebra of approximate relations.

6. **Three-way join.** Derive the FPR of $R_1 \bowtie R_2 \bowtie R_3$ for three FNR-zero relations.

7. **LSH for relations.** Given target precision/recall on a similarity-join task, derive the LSH parameters $(b, r)$.

8. **Composing relation with approximate predicate.** A relation with $\fprate = 0.01$ selected by an approximate predicate with $\fprate = 0.05$. Derive the joint FPR.

**Challenging (★★★ × 3):**

9. **Optimality of MinHash for similarity join.** Sketch why MinHash is optimal in the sense of achieving the entropy-floor analog (chapter 8 §8.3) for similarity sketches.

10. **Approximate equijoin via Bloom intersection.** For an equijoin (not similarity), can we use Bloom filters? Sketch the construction and its FPR.

11. **Approximate relation as $\Bernoulli{T \times U}$.** Recast chapter 12 throughout in chapter 13's framework: $\tilde R \in \Bernoulli{T \times U}$. Identify the composition isomorphisms.

**Target length:** ~2 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 8: Chapter 12 Notebook (`ch12-approximate-relations.ipynb`)

**Files:** Create `python/notebooks/ch12-approximate-relations.ipynb`.

**Content (~12-14 cells):**

1. Title + setup.
2. **Generate synthetic relations** (code): two relations of 1000 rows each, each row a set of 10 string tokens; rows can have varying overlap with rows in the other relation.
3. **MinHash signatures** (code): compute $k = 200$ MinHash signatures per row.
4. **Exact pairwise Jaccard** (code): compute exact $J(r_1, r_2)$ for all $1000 \times 1000 = 10^6$ pairs as ground truth.
5. **MinHash similarity join** (code): estimate $\hat{J}$ for all pairs from signatures; threshold at $\theta = 0.5$.
6. **Compare to ground truth** (code): compute FPR, FNR of the join classifier.
7. **LSH bucketing** (code): hash signatures into $b$ bands of $r$ rows; collide buckets; verify candidate count is sub-quadratic.
8. **Discussion** (markdown): each approximate join as a $\Bernoulli{T \times U}$; chapter 13 unification preview.

**Numerical sanity targets:**
- MinHash estimate within $\pm 0.05$ of true $J$ at $k = 200$.
- LSH band candidates: fewer than 100,000 (out of $10^6$ possible pairs) at $b = 20, r = 10$ for moderate similarity threshold.

**Workflow:** Standard. Execute end-to-end.

---

## Self-Review

Spec coverage: each section has its own task; substantive notebook covered. Chapter 10 MinHash and chapter 5/6 references resolve.
