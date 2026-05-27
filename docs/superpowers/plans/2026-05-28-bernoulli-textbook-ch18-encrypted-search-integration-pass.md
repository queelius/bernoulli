# Plan 18 Final Integration Pass Record (Full Book)

Date: 2026-05-27
Plan: docs/superpowers/plans/2026-05-28-bernoulli-textbook-ch18-encrypted-search.md
HEAD at integration: 92a0efe9c84351d2ae6e91319fbadaf7cd8a5ebb

## Full-book verification results

- Clean build: PASS (exit code 0). `make cleanall && make`; output `book.pdf` 546 pages, 2,084,896 bytes; log saved at `/tmp/plan18-final-build.log` (2,836 lines).

- Total PDF: 546 pages.

- Body pages (chapters 1-18, excluding frontmatter and appendices): pages 1 to 528 (Appendix A begins at 529). Body total = 528 pages.

- Per-part totals (computed from `book.toc` part-start pages and chapter spans):

  | Part | Title | Chapters | Pages | Spec |
  |---|---|---|---|---|
  | I | The Atom | 1-4 | 136 (pp 1-136) | ~110 |
  | II | From Bits to Sets | 5-8 | 112 (pp 137-248) | ~110 |
  | III | From Sets to Maps | 9-13 | 124 (pp 249-372) | ~120 |
  | IV | Optimality and Construction | 14-15 | 62 (pp 373-434) | ~60 |
  | V | The Boundary and Beyond | 16-18 | 94 (pp 435-528) | ~110 |
  | **Body total** | | **1-18** | **528** | **~510** |
  | Frontmatter + appendices | | | 18 | |
  | Total PDF | | | **546** | |

  Part V is under target by ~16 pages (94 vs ~110). The shortfall is in chapter 16 (~28 pp; spec target was ~32 pp) and chapter 18 (~30 pp; spec target was ~37 pp). All other parts are within or above their spec targets; the book is well within the master spec's overall page envelope.

  Per-chapter spans within Part V:
  - ch16 (Approximate but Not Bernoulli): pp 437-464 = 28 pages.
  - ch17 (Cipher Maps and Trapdoor Computing): pp 465-498 = 34 pages.
  - ch18 (Encrypted Search as Relaxed Trapdoor): pp 499-528 = 30 pages.

- Undefined references: 8 warnings in `book.log`. Categorization:

  Expected pre-existing forward refs (documented across Plans 4, 8, 13, 15, 17):
  - `ch:composition` x 1 in chapter 4 (defined as `ch:set-composition` in chapter 6).
  - `ch:sketches` x 5 in chapter 9 prose (defined as `ch:sketches-estimators` in chapter 10).

  Pre-existing slug mismatch introduced in Plan 17 (now visible because Plan 18 ran a clean build):
  - `sec:noisy-bit` x 2 in chapter 17 (`ch17/what-is-cipher-map.tex` line 95, `ch17/bernoulli-error-model.tex` line 54). Chapter 1 introduces the noisy bit but uses the slugs `sec:quantifying-noise` and `sec:sampling-rates`. There is no `sec:noisy-bit` label anywhere in the book. This is a slug error that survived Plan 17 (chapter 17 was never previously clean-built end-to-end in a context that surfaced it). Added to the polish plan below.

  No other unexpected undefined references.

- Chapter labels 1-18: PASS. All 18 chapter-level labels are defined exactly once, in the canonical files:

  | Chapter | Label | File |
  |---|---|---|
  | 1 | `ch:noisy-bit` | `ch01-noisy-bit.tex` |
  | 2 | `ch:binary-channels` | `ch02-binary-channels.tex` |
  | 3 | `ch:boolean-algebra` | `ch03-boolean-algebra-noise.tex` |
  | 4 | `ch:axioms-kronecker` | `ch04-axioms-kronecker.tex` |
  | 5 | `ch:approximate-sets` | `ch05-approximate-sets.tex` |
  | 6 | `ch:set-composition` | `ch06-set-composition.tex` |
  | 7 | `ch:classification-measures` | `ch07-classification-measures.tex` |
  | 8 | `ch:information-bounds` | `ch08-information-bounds.tex` |
  | 9 | `ch:approximate-functions` | `ch09-approximate-functions.tex` |
  | 10 | `ch:sketches-estimators` | `ch10-sketches-estimators.tex` |
  | 11 | `ch:randomized-algorithms` | `ch11-randomized-algorithms.tex` |
  | 12 | `ch:approximate-relations` | `ch12-approximate-relations.tex` |
  | 13 | `ch:algebra-types` | `ch13-algebra-types.tex` |
  | 14 | `ch:optimal-bernoulli-sets` | `ch14-optimal-bernoulli-sets.tex` |
  | 15 | `ch:perfect-hash-filters` | `ch15-perfect-hash-filters.tex` |
  | 16 | `ch:not-bernoulli` | `ch16-not-bernoulli.tex` |
  | 17 | `ch:cipher-maps-trapdoor` | `ch17-cipher-maps-trapdoor.tex` |
  | 18 | `ch:encrypted-search` | `ch18-encrypted-search.tex` |

- Running threads inventory: PASS. Each design thread appears in every chapter the master spec listed.

  - **BSC (binary symmetric channel)**: present in chapters 1, 2, 3, 4, 8, 9. Files: `ch01/three-faces.tex`, `ch01/quantifying-noise.tex`, `ch01/sampling-rates.tex`, `ch01/why-atom.tex`, `ch02/bsc.tex`, `ch02/asymmetric-channel.tex`, `ch02/channel-composition.tex`, `ch02/model-order.tex`, `ch03/and-under-noise.tex`, `ch03/or-not.tex`, `ch03/composition-theorem.tex`, `ch03/miller-rabin.tex`, `ch04/kronecker.tex`, `ch04/bernoulli-bool-formal.tex`, `ch04/what-comes-next.tex`, `ch08/entropy-refresher.tex`, `ch08/bsc-capacity.tex`, `ch08/what-comes-next.tex`, `ch09/atom-to-function.tex`, `ch09/n-ary-channels.tex`, `ch09/n-ary-capacity.tex`, `ch09/n-ary-kronecker.tex`, `ch09/bridge-to-sketches.tex` (plus exercises + biblio in each). Carries from chapter 1's first introduction through chapter 9's generalization to n-ary channels as planned.

  - **Biased coin**: present in chapters 1, 2, 3, 4. Files: `ch01/boolean-universe-first-look.tex`, `ch01/three-faces.tex`, `ch01/quantifying-noise.tex`, `ch02/asymmetric-channel.tex`, `ch02/bsc.tex`, `ch03/and-under-noise.tex`, `ch04/why-axioms.tex`, `ch04/bernoulli-bool-formal.tex`, `ch04/what-comes-next.tex` (plus exercises + biblio). Four chapters as planned.

  - **Classifier verdict**: present in chapters 1, 2, 4. Files: `ch01/three-faces.tex`, `ch01/quantifying-noise.tex`, `ch02/bsc.tex`, `ch02/model-order.tex`, `ch04/axiom-1.tex`, `ch04/bernoulli-bool-formal.tex`, `ch04/what-comes-next.tex` (plus biblio). Three chapters as planned.

  - **Bloom filter**: present in 72 chapter-file matches across chapters 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18. The spec targeted "ch5 introduction + ch6 composition + ch7 diagnostics + ch8 gap + ch14 closure + ch16 adversary + ch18 application" (7 chapters); the realized thread additionally appears in chapters 9, 10, 11, 12, 13, 15, 17 as a structural example used to motivate the framework's general results. The thread is strictly broader than the spec target.

  - **Miller-Rabin**: present in chapters 3, 11. Files: `ch03/miller-rabin.tex`, `ch03/composition-theorem.tex`, `ch03/and-under-noise.tex`, `ch03/or-not.tex`, `ch03/bridge-to-sets.tex`, `ch11/miller-rabin-formal.tex`, `ch11/rp-bpp.tex`, `ch11/las-vegas-vs-monte-carlo.tex`, `ch11/sample-complexity.tex`, `ch11/bridge.tex` (plus exercises + biblio in each). Two chapters as planned: informal in ch3, formal in ch11.

  - **Bernoulli[T] type**: present in chapters 4, 9, 13. Files: `ch04/axiom-1.tex`, `ch04/why-axioms.tex`, `ch04/kronecker.tex`, `ch04/bernoulli-bool-formal.tex`, `ch04/what-comes-next.tex`, `ch09/bibliographic-notes.tex` (plus exercises), `ch13/bernoulli-of-composite.tex`, `ch13/bibliographic-notes.tex`, `ch13/exercises.tex`. Three chapters as planned: formal in ch4, lift to general T in ch9, unification in ch13.

- Soul-voice hook audit: PASS. 147 chapter files audited; zero em-dashes, zero lever+age occurrences, zero buzzword crossroad-substrings. Includes the new chapter 18 prose files and the chapter 18 notebook (audited separately during Sub-Task 10A).

- LaTeX-macro-leak audit (post-fix from Plan 17 close): PASS. Zero matches for `rendered as`, `alex.sty`, `texttt{alex`, `texttt{\textbackslash f`, or `texttt{\textbackslash t` in chapter prose (after excluding commented lines and Difficulty-marker macros documentation).

## Known deferred items

- `ch:composition`: chapter 4 forward ref into Part II (chapter 6's actual label is `ch:set-composition`); documented across Plans 4, 8, 13, 15.
- `ch:sketches` in chapter 9 prose (5 occurrences); chapter 10's actual label is `ch:sketches-estimators`.
- `sec:noisy-bit` in chapter 17 prose (2 occurrences); chapter 1 introduces the noisy bit under `sec:quantifying-noise` and `sec:sampling-rates`. This slug mismatch was introduced in Plan 17 and not surfaced by Plan 17's per-chapter integration check; it is a polish-plan item rather than a blocker.

## Milestone 2 / Full Book status

The Bernoulli textbook draft is COMPLETE per the master specification. Chapters 1-18 drafted (147 chapter files, 528 body pages, 546 total PDF pages); 15 companion Python notebooks executed end-to-end (chapters 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 18); all five Parts close cleanly. The book is publishable modulo the polish plan items below.

## Open follow-ups for polish plan

1. Rename `ch:sketches` references in chapter 9 prose to `ch:sketches-estimators` (5 occurrences in `ch09/*.tex`).
2. Decide `ch:composition` in chapter 4: either rename to `ch:set-composition` or add a `\label{ch:composition}` alias inside chapter 6.
3. Resolve `sec:noisy-bit` in chapter 17: either rename to `sec:quantifying-noise` (the closest chapter 1 section) or add a `\label{sec:noisy-bit}` alias inside `ch01/quantifying-noise.tex` (2 occurrences in `ch17/what-is-cipher-map.tex` and `ch17/bernoulli-error-model.tex`).
4. Populate appendix stubs: Appendix B (the Five Core Principles cheat sheet) and Appendix D (Selected Exercise Solutions). Appendices A and C have stubs in place.
5. Final proofreading pass for typos, notation consistency, and per-Part page-count balance (Part V is ~16 pp under spec target; could absorb additional notebook-tied worked examples).
6. ISBN, publisher metadata, and subtree push to the standalone GitHub repo. The monorepo holds the working copy; the standalone publication target is a separate concern.
