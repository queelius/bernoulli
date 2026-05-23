# Plan 8 Integration Pass Record, Part II

Date: 2026-05-23
Plan: docs/superpowers/plans/2026-05-22-bernoulli-textbook-ch08-information-bounds.md
HEAD at integration: de8c0261b3e1ca831a8e5f9d9ef4f0ea9f2556a1

## Verification results

- Clean build: PASS (exit code 0). Full `make cleanall && make` produced
  `book.pdf` (290 pages, 1,208,365 bytes). Log archived at
  `/tmp/plan8-final-build.log`.
- Undefined references: 1 found, all expected.
  - `ch:composition` at p. 1 (input line 29). This is the known pre-existing
    forward reference from chapter 4 prose to a Part II label that was never
    aliased after chapter 6 was assigned `ch:set-composition`. Documented in
    the Plan 4 Part I integration pass record. No new undefined references
    introduced by Plan 8.
- Undefined citations: PASS (none reported by the build log; the four
  `pdfTeX warning (dest): name{cite.0@…} replaced by a fixed one` messages
  for `rabin-1980`, `miller-1976`, `manning-raghavan-schutze`, `shannon-1948`
  are hyperref destination-collision warnings, not undefined-citation
  warnings, and predate Plan 8).
- All chapter 5-8 chapter labels defined exactly once: PASS.
  - `ch:approximate-sets` in `book/chapters/ch05-approximate-sets.tex:2`
  - `ch:set-composition` in `book/chapters/ch06-set-composition.tex:2`
  - `ch:classification-measures` in `book/chapters/ch07-classification-measures.tex:2`
  - `ch:information-bounds` in `book/chapters/ch08-information-bounds.tex:2`
- Forward references from chapter 6/7/8 to chapter 5/6/7 all resolve: PASS.
  Live references found:
  - ch06 to ch05: `\Cref{ch:approximate-sets}` (other-set-ops, union),
    `\Cref{def:bloom-filter}` (union)
  - ch06 to ch07: `\Cref{ch:classification-measures}` (cancellation,
    what-comes-next)
  - ch07 to ch05: `\Cref{sec:bloom-from-scratch}` (bloom-diagnostics),
    `\Cref{def:bloom-filter}` (bloom-diagnostics, derived-measures,
    setup-revisited), `\Cref{ch:approximate-sets}` (setup-revisited)
  - ch08 to ch05, ch06, ch07: `\Cref{ch:approximate-sets}`,
    `\Cref{ch:set-composition}`, `\Cref{ch:classification-measures}`
    (what-comes-next), `\Cref{def:bloom-filter}` (bloom-gap, entropy-floor,
    bibliographic-notes)
  Build log shows only `ch:composition` as undefined; every reference above
  resolves.
- Page-count audit:
  - Total book: 290 pp
  - Part II total: 251 minus 139 equals 112 pp (target ~110 pp). Within band.
  - Chapter 5 (139 to 169): 30 pp (target ~28 pp, band 22-37). PASS.
  - Chapter 6 (169 to 197): 28 pp (target ~24 pp, band 19-31). PASS.
  - Chapter 7 (197 to 227): 30 pp (target ~28 pp, band 22-37). PASS.
  - Chapter 8 (227 to 251): 24 pp (target ~22 pp, band 17-29). PASS.
- Running threads inventory:
  - Bloom filter thread: present in chapters 5, 6, 7, 8 (all four).
    Multiple files per chapter discuss it; the construction is defined in
    `ch05/bloom-from-scratch.tex` (`def:bloom-filter`) and revisited in
    ch06 (union, other-set-ops, cancellation, perfect-filter-line), ch07
    (setup-revisited, bloom-diagnostics, derived-measures), and ch08
    (bloom-gap, entropy-floor, what-comes-next).
  - BSC running thread: returns in chapter 8 in `bsc-capacity.tex` (§8.2)
    as required, with additional appearances in `entropy-refresher.tex`,
    `what-comes-next.tex`, `bibliographic-notes.tex`, and `exercises.tex`.
- Soul-voice hook audit: PASS. Scanned all `book/chapters/ch0[5-8]/**/*.tex`
  and the chapter top-level files for em-dashes (U+2014), the banned
  lever-suffix-age word, and the standard banned substrings; result: "audit
  complete", zero violations.

## Known deferred items

- `ch:composition`: chapter 4 (`why-axioms.tex`, `axiom-1.tex`) references
  a label name that was never created. The actual Part II chapter exists as
  chapter 6 with label `ch:set-composition`. Would resolve if chapter 4
  prose were updated to point at `ch:set-composition`, or an alias label
  were added in chapter 6. Out of scope for Plan 8 (per integration-pass
  guidance); recorded in the Plan 4 Part I record as well.
- Forward references into Part III, IV, and V chapters (9, 14, 15, 16, 17, 18):
  all use chapter-level labels defined in Plan 0 stubs (e.g.
  `ch:approximate-functions`, `ch:optimal-bernoulli-sets`,
  `ch:perfect-hash-filters`, `ch:not-bernoulli`, `ch:cipher-maps`,
  `ch:encrypted-search`); they resolve cleanly in this build. No
  section-level forward references into undrafted chapters were found in
  the build log.

## Open follow-ups

None. All four Part II chapters land within their page-count bands, all
internal Part II cross-references resolve, both Bloom-filter and BSC
running threads are properly maintained, and the soul-voice audit is
clean. The single undefined reference (`ch:composition`) is pre-existing
and already tracked; resolving it belongs to the cross-cutting polish
plan rather than Plan 8.
