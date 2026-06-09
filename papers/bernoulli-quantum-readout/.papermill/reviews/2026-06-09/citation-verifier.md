# Citation Verifier

**Date**: 2026-06-09
**Scope**: Citations introduced or affected by Section 3.6; bibliography integrity regression; arXiv-as-journal hygiene.

## Section 3.6 citations

Section 3.6 introduces **no new bibliography entries**. It cites four already-present keys:
- `nation2021m3`, `bravyi2021mitigating` (line 525, the dictionary paragraph, for the assignment-matrix-that-mitigation-inverts framing). Roles consistent with their existing use in the intro and related-work (a).
- `vonneumann1956`, `pippenger1988` (line 566, for "the same Walsh-spectrum object the classical noisy-Boolean-formula tradition computes"). Consistent with their use in Section 3.4 and related-work (c).

All four keys resolve in `references.bib`. No dangling `\cite`. The build reports 0 undefined citations.

## Bibliography integrity (regression pass)

- 18 entries in `references.bib`, all 18 cited, all 18 appear in the compiled `main.bbl` (`grep -c bibitem` = 18). No placeholders, no `% TODO`.
- No new uncited entries; no newly-cited-but-missing keys. The addition is citation-neutral.
- `bernoulliRelations` remains the only framework self-cite without a DOI (known, tracked in state.md as not-mint-ready). Pre-existing, not a regression.

## Finding C1 (minor, pre-existing), arXiv entries as @article with journal = "arXiv preprint arXiv:..."

**Location**: `references.bib` keys `koh2024readout`, `adams2015typetheory`, `cho2015effectus`.
**Quoted field**: `journal = {arXiv preprint arXiv:2406.07611}` (and the 1511.09230, 1512.05813 analogues).
**Problem**: Under `plainnat` these render with the literal string "arXiv preprint arXiv:NNNN.NNNNN" in the journal slot. The conventional form for a preprint is `@misc` with `eprint`/`archivePrefix` (or `howpublished`), which yields a cleaner "arXiv:NNNN [quant-ph]" rendering and is what *Quantum* / PRX Quantum referees expect. Cosmetic, but a venue-submission polish item.
**Suggestion**: Convert the three arXiv entries to `@misc{..., howpublished={arXiv:2406.07611}, year=...}` or add `eprint`/`archivePrefix` fields. Severity: minor; **pre-existing**, not introduced by the 3.6 addition.

## Items flagged [needs external verification]

These are content-accuracy questions I cannot resolve offline (no live web). All are **pre-existing** cites the orchestrator already plans to verify; none is new to 3.6, but two are load-bearing for 3.6's framing:

- **C2 [needs external verification]**: `vonneumann1956` / `pippenger1988` actually computing the parity/Walsh "spectrum" object as 3.6 claims (line 565 to 566). The reliability-of-noisy-formulas attribution is standard and safe; the specific "Walsh-spectrum" phrasing is the part to spot-check. The explicit Fourier attribution is anchored on `odonnell2014` (Section 3.4), which is the more defensible cite for the Walsh/Fourier claim.
- **C3 [needs external verification]**: `nation2021m3` (PRX Quantum 2(4):040326, 2021) and `bravyi2021mitigating` (Phys Rev A 103, 042605, 2021) bibliographic details and the claim that they "calibrate and invert" the assignment matrix. Consistent with my training knowledge (M3 is matrix-free scalable mitigation; Bravyi et al. is the multiqubit/CTMP paper), but venue/page/year should be confirmed.
- **C4 [needs external verification]**: `koh2024readout` arXiv:2406.07611 (mid-circuit plus feedforward readout mitigation) and `tannu2019mitigating` 84%/62% all-zero/all-one fidelity datapoint. Both pre-existing; carried from prior reviews.

## Verdict
Citation-clean with respect to the 3.6 addition: no new entries, no dangling cites, no integrity regression. One minor pre-existing hygiene item (C1, arXiv-as-journal). Content-accuracy of the four reused cites is consistent with my offline knowledge but flagged for the orchestrator's external pass (C2 to C4).
