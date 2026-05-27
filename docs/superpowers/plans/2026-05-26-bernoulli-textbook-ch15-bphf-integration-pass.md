# Plan 15 Integration Pass Record (Part IV)

Date: 2026-05-27
Plan: docs/superpowers/plans/2026-05-26-bernoulli-textbook-ch15-bphf.md
HEAD at integration: c983d067df0c783e5e500d355c5d188b1f62ebbd

## Verification results

- Clean build: PASS (`cd book && make cleanall && make` exit 0)
- Total PDF: 460 pages
- Undefined references: 6 total, all expected and documented:
  - `ch:composition` (1 occurrence, chapter 4 `why-axioms.tex` / `axiom-1.tex`; predates Plan 4)
  - `ch:sketches` (5 occurrences, chapter 9 prose; chapter 10's actual label is `ch:sketches-estimators`)
- Undefined citations: 0 (PASS)
- Chapter 14-15 labels defined exactly once:
  - `ch:optimal-bernoulli-sets` at `book/chapters/ch14-optimal-bernoulli-sets.tex:2`
  - `ch:perfect-hash-filters` at `book/chapters/ch15-perfect-hash-filters.tex:2`
  - PASS
- Per-chapter page counts:
  - Chapter 14 (BHF): pages 375 to 406 = 32 pages (target ~30, band 24-39, PASS)
  - Chapter 15 (BPHF): pages 407 to 436 = 30 pages (target ~28, band 22-37, PASS)
- Running threads inventory:
  - BHF: present in all 7 chapter-14 section files (defining) plus all 7 chapter-15 section files (referring back). The thread carries forward as designed.
  - BPHF: present in all 7 chapter-15 section files (defining).
  - Perfect-filter line concept: cited explicitly in 4 chapter-14 section files and 3 chapter-15 section files; the chapter 6 §6.4 concept is the unifying thread that links chapter 8's entropy floor (Part II) to Part IV's two constructive realizations.
- Soul-voice hook audit: PASS (17 files audited, zero violations)

## Known deferred items

Three known forward-reference issues recorded across previous integration passes; none introduced by Plan 15:

1. `ch:composition` (chapter 4 `why-axioms.tex` / `axiom-1.tex`): chapter 6's actual label is `ch:set-composition`. The chapter 4 references were not renamed when Part II was drafted. Documented in Plan 4, Plan 8, Plan 13 integration records.
2. `ch:sketches` (chapter 9 §9.5 prose): chapter 10's actual label is `ch:sketches-estimators`. Five occurrences in `book/chapters/ch09/bridge-to-sketches.tex` (or similar). Documented in Plan 13 integration record.
3. Chapter 16-18 forward references from chapters 14-15: Part V is undrafted; chapter-level forward references to `ch:not-bernoulli`, `ch:cipher-maps-trapdoor`, `ch:encrypted-search` resolve via Plan 0 stubs to the placeholder chapter files. No new undefined references introduced by Plan 15.

## Part IV status

**Part IV (Optimality and Construction) is complete.** With Parts I + II + III + IV drafted, only Part V (chapters 16-18) remains for full master-spec coverage.

Per-Part page totals at Plan 15 close:

| Part | Chapters | Pages | Spec target |
|---|---|---|---|
| Part I | 1-4 | 136 | ~110 |
| Part II | 5-8 | 112 | ~110 |
| Part III | 9-13 | 124 | ~120 |
| Part IV | 14-15 | 62 | ~60 |
| **Total body** | **1-15** | **434** | **~400** |
| Including frontmatter (ix pages) + ch 16-18 stubs (6 pages) + appendix stubs (16+ pages) | | **460 PDF** | |

Master spec total target (Milestones 1 + 2 combined): ~500 pages. Currently drafted body 434/500 = 87% complete; Part V chapters 16-18 remain (~110 pp target per master spec, more realistically ~70 pp given the chapters are conceptually smaller than Parts I-IV).

## Open follow-ups for polish plan

1. **Rename `ch:sketches` references in chapter 9** (5 occurrences in `book/chapters/ch09/bridge-to-sketches.tex` and possibly other ch9 files) to `ch:sketches-estimators`.
2. **Decide `ch:composition` in chapter 4**: either rename the 2 chapter-4 references to `ch:set-composition`, or add a label alias to chapter 6 §6.1 introduction.
3. **Reconcile +8.5% overshoot vs spec target** (currently 434pp body vs ~400pp spec for chapters 1-15). Probably ship as is, but flag for editorial review.
4. **Full-book integration pass once Parts IV-V are drafted** (currently single-page stubs for chapters 16-18 and appendices).
