# Plan 4 Integration Pass Record

Date: 2026-05-14
Plan: docs/superpowers/plans/2026-05-13-bernoulli-textbook-ch01-noisy-bit.md
HEAD at integration: 54370a761a03235cb979542adc2c06a8ebe3ed42

## Verification results

- Clean build: PASS (exit code 0). `make cleanall && make` produced
  `book.pdf` at 188 pages. Build log saved to `/tmp/plan4-final-build.log`.
- Undefined references: 1 occurrence, and it is the expected
  `ch:composition` Part II forward reference (book.log line 1145:
  `Reference 'ch:composition' on page 1 undefined on input line 29`).
  No other undefined reference. See "Known deferred items".
- Undefined citations: PASS (zero `Citation ... undefined` lines in
  book.log).
- All chapter 1 labels defined exactly once: PASS. The six labels and
  their single real `\label{}` definition site (header-comment `%`
  lines excluded):
  - `ch:noisy-bit` -- book/chapters/ch01-noisy-bit.tex:2
  - `sec:three-faces` -- book/chapters/ch01/three-faces.tex:26
  - `sec:quantifying-noise` -- book/chapters/ch01/quantifying-noise.tex:26
  - `sec:boolean-universe-first-look` -- book/chapters/ch01/boolean-universe-first-look.tex:24
  - `sec:sampling-rates` -- book/chapters/ch01/sampling-rates.tex:29
  - `sec:why-atom` -- book/chapters/ch01/why-atom.tex:37
- Forward references from chapters 2-4 to chapter 1 all resolve: PASS.
  Real `\Cref{}` uses (header-comment `%` lines excluded):
  `sec:three-faces` -- chapter 2: 4 (bsc.tex x3, asymmetric-channel.tex x1);
  chapter 3: 2 (and-under-noise.tex x2); chapter 4: 4
  (bernoulli-bool-formal.tex). `sec:boolean-universe-first-look` --
  chapter 4: 4 (bernoulli-bool-formal.tex). Total 14 real matches,
  every chapter 2/3/4 covered. book.log shows no
  `Reference sec:three-faces undefined` or
  `Reference sec:boolean-universe-first-look undefined`.
- Page-count audit: total PDF 188 pp. Part I = 134 pp (chapter 1 start
  p.3 through Part II start p.137), spec target ~105 pp, allowed band
  90-150 pp -- within band. Per-chapter spans from book.toc:
  - Chapter 1: pp. 3-26, 24 pp (target ~25, band 20-35) -- within band
  - Chapter 2: pp. 27-58, 32 pp (target ~24, band 19-34) -- within band
  - Chapter 3: pp. 59-98, 40 pp (target ~28, band 22-40) -- within band (at upper edge)
  - Chapter 4: pp. 99-136, 38 pp (target ~28, band 22-40) -- within band
- Running threads inventory (chapters in which each thread appears):
  - BSC thread: chapters 1, 2, 3, 4 (all four).
  - Biased coin thread: chapters 1, 2, 3, 4 (all four).
  - Classifier verdict thread: chapters 1, 2, 4. Not present in
    chapter 3. Spec requires chapter 1 plus at least two of
    chapters 2/3/4 -- satisfied (chapters 2 and 4).
- Soul-voice hook audit: PASS. 32 Part I `.tex` files audited, no
  em-dash (U+2014), no "lever+age" token; "audit complete" printed.

## Known deferred items

- `ch:composition`: forward reference from chapter 4 into Part II. The
  one real `\Cref{ch:composition}` is in
  `book/chapters/ch04/axiom-1.tex:29` ("the composition theorem of
  \Cref{ch:composition} prescribes"); `book/chapters/ch04/why-axioms.tex`
  documents it as an expected forward reference in its header-comment
  block (lines 8 and 11, both `%` comments). Cannot resolve in Plan 4
  (Part II not yet drafted). Resolves when the Part II composition
  chapter is written. 1 occurrence in book.log.

## Open follow-ups

- The final quality review found a biased-coin attribution error in
  chapter 4: `ch04/why-axioms.tex` cited "the biased-coin example from
  \S 1.3", attributing the example's origin to §1.3, when the coin is
  introduced in §1.1 (`sec:three-faces`) and only revisited in §1.3
  (`sec:boolean-universe-first-look`), where its full PMF was
  deliberately deferred. (`ch04/bernoulli-bool-formal.tex` was checked
  in the same pass and found already correct and internally
  consistent.) Fixed in this commit: origin now points at
  `sec:three-faces`, PMF-deferral at `sec:boolean-universe-first-look`.
- Chapter 3 is at the upper edge of its page band (40 pp, band
  22-40 pp). Not a failure, but flagged for the polish plan in case
  trimming is desired.
- The classifier verdict thread does not appear in chapter 3. This
  still satisfies the spec (chapter 1 plus chapters 2 and 4), but is
  noted in case the polish plan wants a chapter 3 callback for
  symmetry with the other two threads.
