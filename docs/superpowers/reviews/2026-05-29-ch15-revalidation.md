# Chapter 15 (BPHF) B2 Revalidation Review

**Date:** 2026-05-29
**Reviewer:** bookwright reviewer orchestrator (scoped, four-lens inline)
**Scope:** chapter 15 only (commit `f75895d`, "fix(ch15): BLOCKER B2, rewrite BPHF chapter on the corrected model")
**Target model:** the corrected Option-A model (bare rank table = BHF in the general query model; FPR=0 only in the witness model; true perfect hash gives the exact corner; k-perfect hash is the FNR dial with `FNR ≈ 1 − m/n`; per-element space `⌈log2 n⌉`; crossover at FPR = 1/n).

## VERDICT: PASS-WITH-NOTES

The B2 rewrite holds up. The corrected model is implemented consistently across all eight files. Every numerical claim recomputes correctly. No residue of the old (wrong) model survives anywhere. The only findings are two header-comment-block accuracy items (MINOR) and a small set of cold-read polish notes (NOTE). Nothing blocks the chapter from shipping.

## Finding counts

| Severity | Count |
|---|---|
| BLOCKER | 0 |
| MAJOR | 0 |
| MINOR | 2 |
| NOTE | 4 |

## Residual old-model claims

**None survived.** This is the highest-priority result and it is clean. All eight files were searched for each known old-model artifact:

- **"FNR ≤ 2^{-r}" as the BPHF false-negative bound**: NOT PRESENT. The eq:bphf-fnr label resolves to `FNR ≈ 1 − m/n` (`bphf-construction.tex:303-304`). The only places `FNR` appears near `2^{-r}` are correct-model statements: `bhf-to-bphf.tex:33` (a header comment recalling the *BHF* result FNR-zero / FPR≤2^{-r}), notebook claim 1 (the bare construction *is* the BHF, `FPR ≈ 2^{-r}`), and `exercises.tex:244` (the bare general-model construction has `FNR = 0` but `FPR = 2^{-r}`). All three correctly attach `2^{-r}` to the FPR axis, never the FNR axis.
- **"rank collision among members causes false negatives"**: NOT PRESENT, and actively debunked. `bphf-construction.tex:199-202` ("a perfect hash gives every member its own slot"), `exercises.tex:221-234` ("The rank-collision red herring"), and notebook Claim 3 (`assert both, 'a rank collision must NOT cause a false negative under a perfect hash'`) all state the corrected position.
- **"second-stage / build-time discriminator delivering FPR=0"**: NOT PRESENT. No occurrence of "discriminator" in any file. The one "second-stage check" hit (`bhf-to-bphf.tex:87`) is the application-side verification a *BHF* user runs to absorb its false positives, unrelated to the removed FPR=0 mechanism.
- **"witness stored alongside the rank (2·log2 n bits)" / "crossover at 1/n²"**: NOT PRESENT. No `2 log2 n` double-store, no `n^2` anywhere. The witness is the rank itself (`bphf-construction.tex:241-244`, notebook cell 2 "the rank is itself the witness"). Crossover is stated as FPR = 1/n in prose (`space-time-analysis.tex:301-302`) and asserted in the notebook (`assert r_cross == r, 'BHF and BPHF widths must tie at FPR = 1/n'`).
- **"birthday rank-collision argument"**: NOT PRESENT. No occurrence of "birthday".

## Findings (severity-tagged)

### MINOR

- **MINOR, `space-time-analysis.tex:66`**: the body defines `\label{eq:bphf-rank-bits}` (the `L_R = n·r` equation) but this label is absent from the file's DEFINED header-comment block (`space-time-analysis.tex:6-10`). The header is incomplete. The label is unique and never referenced elsewhere, so it does not break the build; it is a header-accuracy gap only.
- **MINOR, `bridge-to-part5.tex:20` and `exercises.tex:21`**: both RESOLVED header-comment blocks list `\Cref{ch:bhf} -- chapter 14`, but (a) the body of neither file actually uses `\Cref{ch:bhf}`, and (b) no `ch:bhf` label exists anywhere in the book. Chapter 14's real chapter label is `ch:optimal-bernoulli-sets`. The header comments name a nonexistent label for a reference the body never makes. Harmless to the build (the body is clean), but the RESOLVED lists are inaccurate. Recommend either deleting the two `ch:bhf` header lines or correcting them to `ch:optimal-bernoulli-sets`.

### NOTE (cold-read polish, non-blocking)

- **NOTE, `bphf-construction.tex:148-149`** and similar ("The shapes match; the consequences ... do not match the way the picture promises"): the "the picture promises" / "the way the symmetry of the picture suggests" phrasing recurs several times (lines 110, 148-149, 201, 221). It reads well once but the repetition of the same rhetorical hook across the section is slightly heavy on a cold read. Optional tightening.
- **NOTE, `space-time-analysis.tex:70`**: "doubly linear in the sense that the slot count is n and the per-slot width grows as log2 n": "doubly linear" is an imprecise label for an `n log n` quantity (one factor is logarithmic, not linear). The sentence then correctly states the growth rate is `n log2 n` (line 76), so the reader is not misled, but the phrase "doubly linear" is loose. Minor wording.
- **NOTE, `ranked-search.tex:103`**: `TopK(a) = Query(a) ∧ R[φ(a)] < k`. `Query(a)` already reads `R[φ(a)]`, so the composite re-reads the same slot for the `< k` test. This is correct and the prose (lines 111-114) describes both reads, but a reader may briefly wonder whether the rank value from `Query` is reused or re-fetched. A half-sentence noting the slot value is reused would remove the momentary ambiguity. Optional.
- **NOTE, `bphf-construction.tex:362-368`**: the closing comparison says an application that "can tolerate neither must pay the dictionary price for both." This is the correct conclusion, but it is the first time "pay the dictionary price for both" appears as a two-sided cost, and it is stated without a pointer to where that two-sided structure is treated. A reader may want a cross-reference. Non-blocking; the claim stands on the FPR-zero counting argument given just above (lines 258-270).

## Math verification

Every numerical claim in §15.2, §15.3, §15.4, and the exercises was recomputed independently in Python. All match the prose.

| Location | Claim | Recomputed | Match |
|---|---|---|---|
| §15.2 worked ex | `n=1000 → r=⌈log2 1000⌉ = ⌈9.966⌉ = 10` | 9.966 → 10 | yes |
| §15.2 | `2^10=1024 ≥ 1000 > 2^9=512` | 1024, 512 | yes |
| §15.2 | rank table `1000·10 = 10000 bits = 1250 bytes` | 10000 bits, 1250 B | yes |
| §15.2 | total w/ PH 2-3 bits/elem ≈ 12000-13000 bits ≈ 1500-1625 bytes | 12000-13000 bits, 1500-1625 B | yes |
| §15.2 | k-perfect `FNR ≈ 1 − 900/1000 = 0.10` | 0.10 | yes |
| §15.2 | BHF on same set @ FPR=0.01 → `r=7`, 7000 bits, FPR ≤ 2^-7 = 0.0078 | 6.644→7, 7000, 0.0078 | yes |
| §15.3 | `n=10^6 → r=⌈19.93⌉ = 20` | 19.9316 → 20 | yes |
| §15.3 | table `20·10^6 = 2·10^7 bits ≈ 2.5 MB` | 2.5 MB | yes |
| §15.3 | `n=10^9 → r=30`, `3·10^10 bits ≈ 3.75 GB` | 30, 3.75 GB | yes |
| §15.3 tab:bhf-bphf-bits | BHF @ {10^-2,10^-3,10^-6} = {7,10,20}; BPHF = 20 | {7,10,20}, 20 | yes |
| §15.3 | factor 20/7 ≈ 2.86; 20/10 = 2; 13 extra bits | 2.857, 2.0, 13 | yes |
| §15.3 | crossover @ n=10^6: 2^-20 ≈ 10^-6; general crossover FPR=1/n | 9.54e-7; 1/n | yes |
| §15.4 worked ex | `n=10^6, k=100 → r=20`; `2^20=1,048,576`, `2^19=524,288` | 20; 1048576; 524288 | yes |
| §15.4 | table `10^6·20 = 2·10^7 bits = 2.5 MB`; total w/ PH ≈ 2.7-2.9 MB | 2.5 MB; 2.75-2.88 MB | yes |
| §15.4 | E[misses] @ m=0.99n = `100·0.01 = 1` (returns ~99/100) | 1.0 | yes |
| ex 2 | FNR @ {0.99,0.9,0.5}n = {0.01,0.1,0.5} = {100,1000,5000} per 10^4 | matches | yes |
| ex 4 | `n=10000 → r=⌈13.288⌉ = 14`; general-model FP ≈ 10^5/n = 10; k-perfect m=0.9n FNR=0.1 | 14; 10; 0.1 | yes |
| ex 5 | `1−0.98=0.02`; E[misses]=`50·0.02 = 1` | 0.02; 1.0 | yes |
| ex 6 | `n=10^6, r=20` table = 2.5 MB | 2.5 MB | yes |
| ex 9 | uniform rank collision fraction `1 − e^-1 ≈ 0.63` | 0.6321 | yes |

(The Python printout showed `0.0999...` / `0.0100...` for two values; these are exact floating-point representations of 0.10 and 0.01 respectively and match the prose decimals.)

## Notebook (`python/notebooks/ch15-bphf.ipynb`)

Read in full with stored outputs. The notebook executes top to bottom with every `assert` passing and a final `All chapter 15 claims verified.` print. Its six claims encode the corrected model exactly:

- **Claim 1 (general model)**: `fp_general = 95`, expected `Q/n = 100`; `assert 0.5·exp < fp < 2·exp`. Encodes "the bare construction is the BHF, FPR ≈ 1/n ≈ 2^-r."
- **Claim 2 (witness model)**: `fp_witness = 0`; `assert fp_witness == 0`. Encodes FPR = 0 by construction.
- **Claim 3 (exact corner / no rank-collision miss)**: `misses = 0`; forced rank tie still retrieves both; `assert both`. Encodes true-perfect FNR=0 and the rank-collision red herring.
- **Claim 4 (k-perfect dial)**: `FNR = {0.000, 0.050, 0.100, 0.200}` matching `1 − m/n` at FPR=0; `assert abs(fnr − predicted) < 1e-9`.
- **Claim 5 (ranked search = witness model)**: recall `100/100`, off-corpus surfaced `0`; `assert recall == k` and `assert surfaced == 0`; expected misses `k(1 − m/n)`.
- **Claim 6 (crossover)**: table widths tie at FPR=1/n (`r_cross = 10 = r`); `assert r_cross == r`. No 1/n² confusion, no double-store witness.

The notebook narrative (cell 0) and the prose model agree point-for-point.

## Spec conformance (§15 design checklist)

Against `docs/superpowers/specs/2026-05-25-bernoulli-textbook-part4-design.md` chapter-15 outline (§63-69):

| Spec item | Status | Evidence |
|---|---|---|
| 15.1 From BHF to BPHF (recall ch14, lift to FPR-zero axis) | present | `bhf-to-bphf.tex` |
| 15.2 Construction (perfect hash + per-element rank value) | present | `bphf-construction.tex`, `def:bphf` |
| 15.3 Space and time analysis | present | `space-time-analysis.tex`, `prop:bphf-space` |
| 15.4 Ranked search / top-k application | present | `ranked-search.tex`, `prop:bphf-ranked-search` |
| 15.5 Bridge to Part V (ch16 not-Bernoulli, ch17-18 cipher maps) | present | `bridge-to-part5.tex` |
| 15.6 Bibliographic notes (`bernoulli-phf`, ranked-search lit) | present | `bibliographic-notes.tex` |
| 11 exercises with star markers (3/5/3) | present | `exercises.tex` (3★ / 5★★ / 3★★★) |
| Learning-outcomes box | present | `ch15-perfect-hash-filters.tex:4-16` |
| Substantive notebook (BPHF; ranked search) | present | `ch15-bphf.ipynb`, 6 claims, all asserts pass |
| Page budget ~28pp | within tolerance | ch15 occupies pages 406-435 in book.log (~30pp) |

All chapter wiring is in place: `ch15-perfect-hash-filters.tex` inputs all seven sections in the spec order (15.1→15.6 + exercises) and defines `\label{ch:perfect-hash-filters}`.

## Cross-reference integrity

- **Outgoing refs:** 28 distinct `\Cref/\eqref/\ref` targets used in the body across the eight files. 27 of 28 resolve to a unique `\label{}` in the `book/` tree. The 28th, `ch:bhf`, appears only in two RESOLVED *header comments* and never in any body `\Cref` (see MINOR finding above), so it is not a live undefined reference.
- **Label collisions:** none. Each of the 18 ch15 DEFINED labels appears exactly once in the `book/` tree.
- **book.log:** the only undefined-reference warnings in the entire book are the documented-deferred items: `ch:composition` (×1), `ch:sketches` (×5, ch9), `sec:noisy-bit` (×2, ch17). All fall on pages outside ch15's span (407-435). No multiply-defined labels. book.log (mtime 2026-05-30 12:00) is newer than the ch15 fix commit (05:03), so it reflects a current build.
- **Citations:** all four bib keys used in §15.6 (`towell-bernoulli-phf`, `carter-wegman-1979`, `belazzougui-2009`, `manning-raghavan-schutze`) exist in `book/references.bib`.

## Bottom line

The B2 rewrite is correct, internally consistent, and free of old-model residue. eq:bphf-fnr is `1 − m/n` and every dependent section and exercise is consistent with it. The notebook is paired and passing. The two MINOR findings are header-comment hygiene that does not affect the compiled book; the four NOTEs are optional polish. Ship.
