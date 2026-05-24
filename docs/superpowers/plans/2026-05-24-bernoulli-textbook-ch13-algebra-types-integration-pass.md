# Plan 13 Integration Pass Record (Part III)

Date: 2026-05-24
Plan: docs/superpowers/plans/2026-05-24-bernoulli-textbook-ch13-algebra-types.md
HEAD at integration: f3452bfb44c5d62967c23fe96d51778aa293fcaa

## Verification results

- **Clean build:** PASS (exit code 0). `make cleanall && make` from `book/`
  produced `book.pdf` at 402 pages. Build log archived at
  `/tmp/plan13-final-build.log`.

- **Undefined references:** 6 total, all categorized as expected:
  - `ch:composition` (1 occurrence, page 1): chapter 4's forward reference into
    Part II. Chapter 6's label is `ch:set-composition`; the chapter 4 references
    were never renamed. Documented as known deferred in Plan 4 and Plan 8
    integration records.
  - `ch:sketches` (5 occurrences, pages 271-274 and 1): chapter 9 forward
    references to chapter 10, written during Plan 9 before chapter 10's actual
    label (`ch:sketches-estimators`) was fixed. The 9 occurrences across
    `ch09/n-ary-capacity.tex`, `ch09/exercises.tex`, `ch09/bibliographic-notes.tex`,
    and `ch09/bridge-to-sketches.tex` (some in comments, 5 in active prose)
    should be renamed to `ch:sketches-estimators` in the Part III polish plan.
    Carrying as known deferred rather than fixing in this integration commit to
    keep Plan 13 scope mechanical.

- **Undefined citations:** PASS. No `Citation ... undefined` warnings in
  `book.log`. The four `pdfTeX warning (dest)` lines about
  `cite.0@rabin-1980`, `cite.0@miller-1976`, `cite.0@manning-raghavan-schutze`,
  `cite.0@shannon-1948` are hyperref dest-name fixups (citations resolve but
  hyperref's per-PDF-page anchor numbering is degenerate); they are not
  undefined citations.

- **Chapter 9-13 labels defined exactly once:** PASS.
  - `ch:approximate-functions` → `chapters/ch09-approximate-functions.tex:2`
  - `ch:sketches-estimators` → `chapters/ch10-sketches-estimators.tex:2`
  - `ch:randomized-algorithms` → `chapters/ch11-randomized-algorithms.tex:2`
  - `ch:approximate-relations` → `chapters/ch12-approximate-relations.tex:2`
  - `ch:algebra-types` → `chapters/ch13-algebra-types.tex:2`

- **Per-chapter page counts (Part III):**

  | Ch | Start | Next | Pages | Spec target | Band | Status |
  |----|-------|------|-------|-------------|------|--------|
  | 9  | 251   | 279  | 28    | ~26pp       | 20-34 | PASS |
  | 10 | 279   | 307  | 28    | ~28pp       | 22-37 | PASS |
  | 11 | 307   | 333  | 26    | ~24pp       | 19-31 | PASS |
  | 12 | 333   | 353  | 20    | ~22pp       | 17-29 | PASS |
  | 13 | 353   | 375  | 22    | ~20pp       | 16-26 | PASS |

  Part III total: 124 pages (target ~120pp; +3%).

- **Running threads inventory:**
  - **Bloom filter** (Part II thread): present in ch09 (`atom-to-function`,
    `n-ary-channels`, `exercises`), ch10 (`sketches-as-bernoulli`, `countmin`,
    `bibliographic-notes`, `exercises`), ch11 (`rp-bpp`, `exercises`), ch12
    (`sets-to-relations`, `relation-composition`, `exercises`), ch13
    (`composition-functor`, `exercises`). Carries across all five chapters
    as designed.
  - **n-ary channels** (chapter 9 forward): present in ch10 (`countmin`,
    `hyperloglog`, `minhash-lsh`, `sketches-as-bernoulli`, `bridge`,
    `bibliographic-notes`, `exercises`), ch11 (`bridge`, `rp-bpp`,
    `exercises`), ch12 (`sets-to-relations`, `relation-composition`,
    `approximate-joins`, `bridge`), ch13 (`algebraic-types-recap`,
    `bernoulli-of-composite`, `composition-functor`, `closing-part3`,
    `exercises`). Carries across all four downstream chapters.
  - **Miller-Rabin** (closed in chapter 11): present in
    `miller-rabin-formal.tex`, `las-vegas-vs-monte-carlo.tex`, `rp-bpp.tex`,
    `sample-complexity.tex`, `bridge.tex`, `bibliographic-notes.tex`,
    `exercises.tex`. Chapter 3 informal walkthrough is now formalized.
  - **CountMin / HyperLogLog / MinHash** (ch10 + ch13): all three appear in
    ch10 dedicated sections, and the type-driven recap in ch13
    (`algebraic-types-recap`, `bernoulli-of-composite`,
    `composition-functor`, `exercises`).
  - **Approximate relations** (ch12 + ch13): ch12 (`sets-to-relations`,
    `relation-composition`, `approximate-joins`, `bridge`,
    `bibliographic-notes`, `exercises`) and ch13 (`algebraic-types-recap`,
    `bernoulli-of-composite`, `composition-functor`).

- **Soul-voice hook audit:** PASS. 38 Part III `.tex` files scanned; no
  em-dashes, no banned lever-word, no banned crossroads buzzword.

## Known deferred items

- `ch:composition`: chapter 4 forward ref into Part II; chapter 6's label is
  `ch:set-composition` (never renamed); deferred per Plan 4 and Plan 8 records.
- `ch:sketches`: chapter 9 forward refs into chapter 10; chapter 10's label is
  `ch:sketches-estimators` (5 active-prose occurrences in
  `bibliographic-notes.tex`, `bridge-to-sketches.tex`, and `exercises.tex`).
  Carry to Part III polish plan as a one-line `sed`-style rename.
- Chapter 14-18 forward references from chapters 9-13 (Parts IV-V undrafted).
  No such references appear in Part III prose because Plan 9-13 work was
  scoped to avoid forward refs into undrafted parts.

## Milestone 1 status

**Parts I + II + III drafted.** Master spec Milestone 1 target ~330pp.

Actual: **402 pages** total (includes frontmatter and chapter 14-18 stubs and
appendix stubs). Per-part body text:

- Part I (ch 1-4): 136 pages
- Part II (ch 5-8): 112 pages
- Part III (ch 9-13): 124 pages
- Parts I+II+III drafted body: **372 pages** (+13% over the ~330pp target)

The 30+ page overshoot vs the spec target reflects the textbook's adopted
fuller-development style established during Parts I and II, not Plan 13
specifically; Part III itself landed within +3% of its ~120pp budget.

With this record, **Milestone 1 is complete**: the publishable spine of the
book is drafted. Parts IV and V (chapters 14-18) remain as planned future
work and currently exist as single-page stub files in `chapters/`.

## Open follow-ups for polish plan

1. Rename the 5 active-prose `ch:sketches` references in `ch09/` to
   `ch:sketches-estimators` (and update the comment-only occurrences for
   consistency).
2. Decide on `ch:composition` from chapter 4: either rename to
   `ch:set-composition`, or introduce a dedicated `\label{ch:composition}` if
   chapter 4's prose is meant to point at a different conceptual chapter than
   ch6.
3. Reconcile Milestone 1 total (372pp body) against the ~330pp spec target in
   the next pass: either accept the overshoot as the new baseline or identify
   per-chapter trim candidates.
4. Once Parts IV-V are drafted, schedule a full-book integration pass that
   includes appendices A-D (currently single-page stubs).
