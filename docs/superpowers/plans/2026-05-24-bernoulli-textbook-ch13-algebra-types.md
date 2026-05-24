# Bernoulli Textbook Chapter 13: The Algebra of Approximate Types (Plan 13)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 13 of Part III (~20 pp): the unification chapter. State the type-driven algebra for $\Bernoulli{T}$: $\Bernoulli{T \times U} \cong \Bernoulli{T} \otimes \Bernoulli{U}$ for products, $\Bernoulli{T + U}$ for sums, $\Bernoulli{L T}$ for lists, $\Bernoulli{T \to U}$ for functions. Recognize chapter 6 set composition, chapter 9 n-ary maps, chapter 10 sketches, chapter 12 relations as instances of ONE algebra. Theory-only (no notebook). Closes Part III with the integration check at Task 9.

**Architecture:** Replace `book/chapters/ch13-algebra-types.tex` stub with a fully drafted chapter containing 5 sections, learning-outcomes opener, 10-12 exercises, bibliographic entries. Task 9 runs the Part III integration check.

**Tech Stack:** LaTeX (book class), alex.sty, biblatex+biber. NO notebook (per master spec, chapter 13 is theory-only).

**Scope:** Chapter 13 + Part III integration check.

**Spec source of truth:** `docs/superpowers/specs/2026-05-23-bernoulli-textbook-part3-design.md` §4 chapter 13 row.

**Base SHA:** `2897511` (HEAD at end of Plan 12).

**Source material:**
- `papers/bernoulli_data_type/sections/` (primary source for the type-driven algebra)
- All of Part II and Part III chapters 9-12 (the instances being unified)
- Chapter 4 §4.4 Kronecker theorem (the algebraic backbone)

**Lessons inherited from Plans 1-12:**

1. **Page discipline.** Chapter 13 target ~20pp; expect 22-26pp.

2. **Soul-voice hook (BLOCKING):** Respect the full banned-phrase list.

3. **Notation:** alex.sty + standard algebraic-type symbols ($\times, +, L, \to, \otimes$).

4. **Use "structure-preserving map" language** rather than the formal categorical "functor" until §13.5 bibliographic notes (per Part III spec §3.5 risk mitigation).

5. **Part III integration check (Task 9)** mirrors Plan 4 Task 10 (Part I) and Plan 8 Task 10 (Part II).

---

## File Structure

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch13-algebra-types.tex             # rewritten from stub
│   │   └── ch13/                               # NEW directory
│   │       ├── algebraic-types-recap.tex       # §13.1 (~3 pp)
│   │       ├── bernoulli-of-composite.tex      # §13.2 (~6 pp)
│   │       ├── composition-functor.tex         # §13.3 (~5 pp)
│   │       ├── closing-part3.tex               # §13.4 (~2 pp)
│   │       ├── bibliographic-notes.tex         # §13.5 (~2 pp)
│   │       └── exercises.tex                   # 10-12 exercises (~2 pp)
│   └── references.bib                          # extended (towell-bernoulli-data-type already present from chapter 1 bib)
```

NO notebook for chapter 13.

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:algebra-types` | `ch13-algebra-types.tex` (Plan 0 stub) | (forward refs from prior chapters; ch10 §10.5 bridge for example) |
| `sec:algebraic-types-recap` | `ch13/algebraic-types-recap.tex` (Task 2) | (internal) |
| `sec:bernoulli-of-composite` | `ch13/bernoulli-of-composite.tex` (Task 3) | (internal) |
| `sec:composition-functor` | `ch13/composition-functor.tex` (Task 4) | (internal) |
| `sec:closing-part3` | `ch13/closing-part3.tex` (Task 5) | (internal) |

Backward references that should resolve (most of the book):
- Chapter 4 §4.4 Kronecker theorem (`\Cref{thm:kronecker}`)
- Chapter 5/6 set theory
- Chapter 9 n-ary framework (`\Cref{ch:approximate-functions}`, `\Cref{thm:n-ary-kronecker}`)
- Chapter 10 sketches (`\Cref{ch:sketches-estimators}`)
- Chapter 12 relations (`\Cref{ch:approximate-relations}`)

---

## Tasks

### Task 1: Read sources and write chapter scaffolding

- [ ] Read sources: `papers/bernoulli_data_type/sections/` (skim); `book/chapters/ch04/kronecker.tex` (§4.4); `book/chapters/ch09/n-ary-kronecker.tex` (§9.3); Part III spec §4 chapter 13.

- [ ] Replace `book/chapters/ch13-algebra-types.tex` with the scaffold:

```latex
\chapter{The Algebra of Approximate Types}
\label{ch:algebra-types}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item State the type-driven algebra for $\Bernoulli{T}$ over
    products, sums, lists, and functions; identify the structural
    isomorphism $\Bernoulli{T \times U} \cong \Bernoulli{T} \otimes
    \Bernoulli{U}$.
  \item Recognize chapter~6 set composition, chapter~10 sketches, and
    chapter~12 relations as instances of one type-driven algebra.
  \item Close Part~III with the unified view: the Part~I noisy bit is
    the atom; everything from chapter~5 onward is the type lift.
\end{itemize}
\end{quote}

% Section 13.1
\input{chapters/ch13/algebraic-types-recap}

% Section 13.2
\input{chapters/ch13/bernoulli-of-composite}

% Section 13.3
\input{chapters/ch13/composition-functor}

% Section 13.4
\input{chapters/ch13/closing-part3}

% Section 13.5
\input{chapters/ch13/bibliographic-notes}

% Exercises
\input{chapters/ch13/exercises}
```

- [ ] Create `book/chapters/ch13/` + 6 placeholder files (`algebraic-types-recap.tex`, `bernoulli-of-composite.tex`, `composition-functor.tex`, `closing-part3.tex`, `bibliographic-notes.tex`, `exercises.tex`). Each: `% Placeholder. Drafted in Plan 13 Task N.` (N = 2-7).

- [ ] Build exit 0.

- [ ] Commit:

```
book: scaffold chapter 13 (algebra of approximate types) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener, five section subfile inputs plus exercises, with matching
empty placeholders. Theory-only chapter (no notebook). Section drafts
land in subsequent Plan 13 tasks.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §13.1 Algebraic Types Recap (~3 pp)

**Files:** Modify `book/chapters/ch13/algebraic-types-recap.tex`.

**Content checklist (4 items):**

1. **The type constructors.** Products $T \times U$ (pairs); sums $T + U$ (tagged unions); lists $L T$ (sequences); functions $T \to U$. Brief recap from standard ADT framing. Half a page.

2. **Why this matters here.** Each approximate-structure we have built (sets, maps, sketches, relations) lives at one type constructor. Sets at $\{\top, \bot\}$; maps at functions $T \to U$; relations at products $T \times U$; sketches at lists or counters. The unification of chapter 13 explains why composition rules transfer across these instances. One page.

3. **The lift $\Bernoulli{-}$.** Read as a type-level operation: given a type $T$, $\Bernoulli{T}$ is the type of random approximate values over $T$. The operation preserves structure: products go to tensor products, sums to direct sums, etc. (Stated, motivated in §13.2.) Half a page.

4. **Signpost.** §13.2 specifies the lift on each type constructor; §13.3 packages it as a structure-preserving map.

**Labels:** `\section{Algebraic Types Recap}` with `\label{sec:algebraic-types-recap}`.

**Target length:** ~3 pp (700-900 prose words). Standard workflow.

---

### Task 3: §13.2 $\Bernoulli{T}$ for Composite $T$ (~6 pp)

**Files:** Modify `book/chapters/ch13/bernoulli-of-composite.tex`.

**Purpose:** Lift $\Bernoulli{-}$ through each type constructor. The chapter's longest section.

**Content checklist (5 items):**

1. **$\Bernoulli{T \times U} \cong \Bernoulli{T} \otimes \Bernoulli{U}$ (product types).** The Kronecker theorem of chapter 4 §4.4 and chapter 9 §9.3 IS this isomorphism. Explicit: a $\Bernoulli{T \times U}$ instance has a $(K_T K_U) \times (L_T L_U)$ channel matrix that factors as $Q_T \otimes Q_U$ under independence. State as `\label{thm:bernoulli-product}`. Cite `\Cref{thm:kronecker}` and `\Cref{thm:n-ary-kronecker}`. One page.

2. **$\Bernoulli{T + U}$ (sum types).** A tagged-union codomain: the noisy output reports a tag plus a value. Channel matrix is block-diagonal in the obvious sense; the two summands' channels are independent. Half a page.

3. **$\Bernoulli{L T}$ (list types).** A list of $T$-values; each position has its own $\Bernoulli{T}$. For lists of fixed length $n$, this is just $\Bernoulli{T \times T \times \cdots \times T}$ ($n$ factors). For variable-length lists, the list length is itself an attribute that may be noisy (CountMin counters, HyperLogLog cardinality). Half a page.

4. **$\Bernoulli{T \to U}$ (function types).** A function $T \to U$ approximated noisily: per input $t \in T$, a $\Bernoulli{U}$ on the output. This is the chapter 9 framework as a type constructor. Equivalent to $\prod_{t \in T} \Bernoulli{U}$. One page.

5. **The four type constructors give four composition rules.** Summary table:
   - Product: tensor product of channels.
   - Sum: block-diagonal channel.
   - List: product over positions (and possibly the length).
   - Function: product over inputs.
   Each gives a way to compose $\Bernoulli{T}$ instances by structure. One page.

6. **Worked example.** A 3-class classifier producing a labeled count: type $\{$cat, dog, bird$\} \times \mathbb{N}$. Channel matrix factors via product. Compose. Half a page.

**Labels:** `\section{Bernoulli of T for Composite T}` with `\label{sec:bernoulli-of-composite}`. Theorem `\label{thm:bernoulli-product}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 4: §13.3 The Composition Functor (~5 pp)

**Files:** Modify `book/chapters/ch13/composition-functor.tex`.

**Purpose:** Package $\Bernoulli{-}$ as a structure-preserving map ("functor") on the category of algebraic types.

**Content checklist (5 items):**

1. **What is a structure-preserving map?** For any operation on types (product, sum, list, function), the lift $\Bernoulli{-}$ takes the operation on $T, U$ to a corresponding operation on $\Bernoulli{T}, \Bernoulli{U}$. Half a page (informal; the formal categorical name is "functor" but defer to §13.5).

2. **The isomorphism table.**
   - $\Bernoulli{T \times U} \cong \Bernoulli{T} \otimes \Bernoulli{U}$
   - $\Bernoulli{T + U} \cong \Bernoulli{T} \oplus \Bernoulli{U}$
   - $\Bernoulli{L T} \cong L \Bernoulli{T}$ (modulo length)
   - $\Bernoulli{T \to U} \cong T \to \Bernoulli{U}$ ($\Bernoulli{-}$ is a "monad" in the type-theoretic sense; state without categorical formalism)
   One page.

3. **Why this matters operationally.** Composition by type-structure is mechanical: you don't need to re-derive composition rules for each new sketch or data structure; you compose them via the algebra. One page.

4. **Examples from prior chapters as instances.**
   - Chapter 6 set composition $\subseteq$ chapter 13 algebra for $\Bernoulli{T \to \BoolType}$ (i.e., approximate predicates).
   - Chapter 10 CountMin $\subseteq$ chapter 13 algebra for $\Bernoulli{\mathbb{N}}$.
   - Chapter 12 relations $\subseteq$ chapter 13 algebra for $\Bernoulli{T \times U \to \BoolType}$.
   - Chapter 9 n-ary channels are the underlying $\Bernoulli{T}$ at finite enumeration $T$.
   One page.

5. **The Bernoulli framework as one thing.** The chapter's payoff: every approximate structure in the book is $\Bernoulli{T}$ for some $T$. The book's title is now justified: "an algebra of approximate computation." Half a page.

**Labels:** `\section{The Composition Functor}` with `\label{sec:composition-functor}`. Optional propositions `\label{prop:product-iso}`, `\label{prop:sum-iso}`, etc.

**Target length:** ~5 pp (1100-1500 prose words).

**Workflow:** Standard.

---

### Task 5: §13.4 Closing Part III (~2 pp)

**Files:** Modify `book/chapters/ch13/closing-part3.tex`.

**Content (3 items):**

1. **Recap the journey.** Atom (Part I), sets (Part II), maps and types (Part III). Each part lifts the previous via more general type structure.

2. **The full type system.** Part I's $\Bernoulli{\BoolType}$ generalized to chapter 9's $\Bernoulli{T}$ for any algebraic type $T$. Chapter 13 closes the algebra.

3. **Forward to Parts IV-V.** Chapters 14-15 give constructive realizations achieving the entropy floor (BHF, BPHF). Chapter 16 catalogues the boundary cases. Chapters 17-18 cipher maps and encrypted search.

**Labels:** `\section{Closing Part III}` with `\label{sec:closing-part3}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 6: §13.5 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch13/bibliographic-notes.tex`.

**Content (3-4 paragraphs):**

1. **`towell-bernoulli-data-type` paper** (already in bib from chapter 1) as primary source.

2. **Category-theoretic ADT references.** Mention the categorical "functor" name for the structure-preserving map; cite Mac Lane "Categories for the Working Mathematician" if helpful (add bib entry if cited).

3. **Algebraic data types tradition** (Hudak, ML, Haskell). Cite informally; add bib entry only if cited.

**Possibly add:**

```bibtex
@book{maclane-categories,
  author    = {Saunders {Mac Lane}},
  title     = {Categories for the Working Mathematician},
  publisher = {Springer},
  edition   = {2nd},
  year      = {1998}
}
```

(Add only if cited.)

**Section style:** standard, with `\label{sec:bib-notes-ch13}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 7: Chapter 13 Exercises (11)

**Files:** Modify `book/chapters/ch13/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Channel matrix for $\Bernoulli{\BoolType \times \BoolType}$.** Write the $4 \times 4$ channel matrix for an approximate pair of Booleans, as the Kronecker product of two $2 \times 2$ channels.

2. **Identify the type for each prior approximate structure.** For each of (a) Bloom filter, (b) CountMin, (c) MinHash, (d) approximate join, name the type $T$ for which it is a $\Bernoulli{T}$ instance.

3. **Block-diagonal channel for $\Bernoulli{\BoolType + \BoolType}$.** State the channel-matrix shape for a sum type with two summands of identical noisy-bit structure.

**Medium (★★ × 5):**

4. **Composition isomorphism for products.** Prove $\Bernoulli{T \times U} \cong \Bernoulli{T} \otimes \Bernoulli{U}$ at the channel-matrix level, using `\Cref{thm:kronecker}` and `\Cref{thm:n-ary-kronecker}`.

5. **Sketches as $\Bernoulli{T \to \BoolType}$ vs $\Bernoulli{T}$.** Identify which sketch is which type (CountMin is the latter as a counter; Bloom is the former as a predicate).

6. **$\Bernoulli{-}$ as a monad.** Explain informally why $\Bernoulli{T \to U} \cong T \to \Bernoulli{U}$ qualifies $\Bernoulli{-}$ as a "monad" in the programming-language sense.

7. **Composition rules for lists.** Derive the composition rule for $\Bernoulli{L T}$ where the list length is also noisy (a HyperLogLog-style cardinality estimate plus per-element approximate values).

8. **Type for an approximate database.** A database has tables, indexes, and queries. Identify what type a $\Bernoulli{\text{Database}}$ instance lives at, via algebraic-type structure.

**Challenging (★★★ × 3):**

9. **Categorical functor.** State the technical definition of "functor" from category theory, and verify $\Bernoulli{-}$ satisfies it for the four type constructors.

10. **Universal property of $\Bernoulli{-}$.** State a universal property characterizing $\Bernoulli{-}$ up to isomorphism. (Open-ended; one approach: $\Bernoulli{-}$ is the free monad on a particular signature.)

11. **Boundary case for the algebra.** Construct an approximate structure that does NOT fit any of the four type constructors. (Counterexample-style; forward-references chapter 16.)

**Target length:** ~2 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 8: (no notebook, theory chapter)

Skip to Task 9.

---

### Task 9: Part III Integration Check

**Purpose:** Mirror Plan 4 Task 10 (Part I) and Plan 8 Task 10 (Part II). Verify chapters 9-13 cross-references resolve under the full book build.

**Known forward references that cannot resolve** in Plan 13:
- `ch:composition` (chapter 4's forward into Part II; documented in Plan 8 integration record).
- Chapter 14-18 forward references from chapters 9-13 (Parts IV-V not yet drafted; section-level refs into those undrafted chapters should be prose-only).

Any OTHER undefined reference IS a failure to report.

**Steps:**

1. **Clean build.**
```bash
cd book && make cleanall && make
```
Confirm exit 0. Save log to `/tmp/plan13-final-build.log`.

2. **Verify undefined references.**
```bash
grep -n "Reference.*undefined\|Citation.*undefined" book/book.log
```
List each. Categorize as expected vs unexpected.

3. **Verify Part III cross-references.**

Chapter labels (each defined exactly once):
```bash
grep -rn "\\\\label{ch:approximate-functions}\|\\\\label{ch:sketches-estimators}\|\\\\label{ch:randomized-algorithms}\|\\\\label{ch:approximate-relations}\|\\\\label{ch:algebra-types}" book/chapters/
```

Forward references chapter 9 to 10/11/12/13; chapter 10 to 12; chapter 11 to 12/13; chapter 12 to 13: spot-check each set.

4. **Page-count audit.**
```bash
pdfinfo book/book.pdf | grep Pages
```
Per-chapter page counts. Check each within $\pm 30\%$ of spec target:
- Chapter 9: ~26pp target, allow 20-34
- Chapter 10: ~28pp target, allow 22-37
- Chapter 11: ~24pp target, allow 19-31
- Chapter 12: ~22pp target, allow 17-29
- Chapter 13: ~20pp target, allow 16-26

Total Part III should be ~120pp.

5. **Running threads inventory.**
Bloom filter (Part II + chapter 13 references back); n-ary channels (chapter 9 + downstream); CountMin/HyperLogLog/MinHash (chapter 10); Miller-Rabin (chapter 3 + chapter 11 formalization); approximate relations (chapter 12 + chapter 13).

6. **Soul-voice hook audit.**
```bash
python3 -c "
import re, glob
files = glob.glob('book/chapters/ch1[0-3]/**/*.tex', recursive=True) + glob.glob('book/chapters/ch09/**/*.tex', recursive=True) + glob.glob('book/chapters/ch0[9]-*.tex') + glob.glob('book/chapters/ch1[0-3]-*.tex')
banned_substr = 'at' + ' the ' + 'inter' + 'section of'
bad = False
for f in files:
    with open(f, encoding='utf-8') as fh:
        text = fh.read()
    if chr(0x2014) in text:
        print(f'FAIL: em-dash in {f}'); bad = True
    if re.search(r'\blever\s*age\b', text, re.IGNORECASE):
        print(f'FAIL: lever+age in {f}'); bad = True
    if banned_substr in text.lower():
        print(f'FAIL: buzzword crossroad-substring in {f}'); bad = True
print('audit complete' if not bad else 'AUDIT FOUND VIOLATIONS')
"
```
Expected: "audit complete", no FAILs.

7. **Write and commit the integration-pass record** at `docs/superpowers/plans/2026-05-24-bernoulli-textbook-ch13-algebra-types-integration-pass.md`:

```markdown
# Plan 13 Integration Pass Record (Part III)

Date: 2026-05-24
Plan: docs/superpowers/plans/2026-05-24-bernoulli-textbook-ch13-algebra-types.md
HEAD at integration: <SHA>

## Verification results

- Clean build: <PASS/FAIL> (exit code <N>)
- Undefined references: <expected vs unexpected>
- Undefined citations: <PASS/FAIL>
- Per-chapter page counts: <list>
- Running threads inventory: <list>
- Soul-voice hook audit: <PASS/FAIL>

## Known deferred items

- `ch:composition`: chapter 4 forward to Part II (predates).
- Chapter 14-18 forward refs from chapters 9-13.

## Milestone 1 status

Parts I + II + III drafted. Master spec Milestone 1 target ~330pp;
actual: <total pages>.

## Open follow-ups

<any items for the polish plan>
```

Commit:

```
book: Part III integration pass record (Plan 13 close)

Records the final integration verification for Part III (chapters
9-13): clean build, undefined references limited to known
pre-existing forward refs, all chapter 9-13 cross-references resolve,
running threads carry across the part, soul-voice hook audit clean.
With this record, Milestone 1 (Parts I + II + III) is complete.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Self-Review

Spec coverage: chapter 13 row each section has its own task; theory-only (no notebook) per master spec; Part III integration check at Task 9.

Type and label consistency: chapter 13 invokes chapter 4/5/6/9/10/11/12 labels; the `\Cref{ch:algebra-types}` label exists via Plan 0 stub.
