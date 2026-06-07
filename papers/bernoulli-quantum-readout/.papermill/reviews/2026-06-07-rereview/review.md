# Multi-Agent Re-Review Report

**Date**: 2026-06-07 (re-review)
**Paper**: A Forward (epsilon, omega) Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes
**Author**: Alexander Towell
**Revision reviewed**: commit 6f136b7 (same-day revision of the 2026-06-07 first review)
**Recommendation**: ready

This re-review verifies each prior finding against the revised source (not just
its presence) and does a fresh regression pass over the edits. Every load-bearing
numerical and logical claim in the new material was recomputed independently by
the orchestrator (Python), the build was run fresh end to end, and the bib was
checked key by key.

---

## (a) Per-prior-finding resolution table

| Prior finding | What it was | Status | Evidence |
|---|---|---|---|
| **M1** | Independence assumed but failure never framed/bounded | **RESOLVED** | sec:scope item 2 rewritten: independent rate framed as the correlation-free "reference"/"two-sided anchor"; directional parity sign rule added (verified correct); CTMP `% TODO` discharged by citing bravyi2021mitigating. Magnitude bound correctly left as labeled future work. |
| **M2** | Worked example symmetric, so asymmetry never shown on a number | **RESOLVED** | New Subsection 4.4 + Table 2: four-ancilla T1-biased syndrome; all five values recomputed exactly (0.110, 0.175, 0.234, 0.315, sym 0.226); exercises cor:parity-asym on numbers a single-rate model provably cannot give. |
| **M3** | No-prior-forward-calculus novelty unverified offline | **RESOLVED** | Live prior-art pass (prior-art-followup.md) found no direct competitor; novelty stands. Hardened in text by naming koh2024readout (arXiv:2406.07611) as nearest inverse neighbor and distinguishing it. |
| **M4** | Unification rests on locator-free unpublished self-cites | **RESOLVED** | Four framework self-cites now carry real Zenodo DOIs (19105381/19105387/19105389/19104549); sec:related adds a self-contained one-paragraph Bernoulli-model statement so the unification stands without the companion papers. |
| m1 | AND FPR clause read as unconditional (a corner) | **RESOLVED** | thm:andor (i) now opens "Conditioned on all latent inputs being false (t_i=0 for every i), its false-positive rate is ...". |
| m2 | Five framework self-cites carry no DOI/URL | **RESOLVED** (4 of 5; the 5th expected) | Four DOIs wired. bernoulliRelations intentionally still without a DOI (not yet minted): per charter, expected and not a finding. |
| m3 | Parity-identity attribution loose | **RESOLVED** | Attribution split: exact pm1/Fourier identity -> odonnell2014; reliability tradition -> vonneumann1956/pippenger1988, in both thm:parity discussion and sec:related (c). |
| m4 | Rate subscripts overload index vs connective | **PARTIAL** | Context improved (head of sec:calculus), but no explicit one-line "subscripts are index or connective tag" note. Optional, non-blocking. |
| m5 | q / r / q_i play three roles | **PARTIAL** | Subsection 4.4 writes r_i=eps_i/omega_i explicitly and uses q=rbar=0.07, implicitly bridging; no explicit one-line bridge added. Optional, non-blocking. |
| m6 | Long em-dash-chained sentences | **NOT ADDRESSED** | Stylistic; unchanged. Non-blocking. |
| m7 | Four hyperref PDF-string warnings | **RESOLVED** | Fresh build: 0 PDF-string warnings across all three passes. pdftitle + texorpdfstring in place. |
| S1 (S-meth-1) | Ship a Table generator / notebook cell | **NOT ADDRESSED** | Optional ancillary artifact; carry forward. |
| S2 (N3) | Resolve audience ambiguity | **NOT ADDRESSED** | Optional framing choice; carry forward. |
| S3 (N4) | "they symmetrize" criticism possibly too strong | **PARTIAL** | sec:related (a) now distinguishes inverse mitigation precisely; the "symmetrize" criticism in intro/abstract is scoped to single-rate folklore and symmetrized summary reporting. Adequate. |
| S4 (C3) | Rename pucha2021certification | **RESOLVED** | Renamed to krawiec2021certification; zero dangling pucha key. |
| S5 (P4) | Abstract names 4 neighbors, sec:related 5 | **RESOLVED** | Abstract now names exactly five, matching (a)-(e). |
| S6 (P5) | Folklore aired four times | **NOT ADDRESSED** | Stylistic; unchanged. Non-blocking. |
| S7 (P6) | Shorten the long title | **NOT ADDRESSED** | Title unchanged. Optional. |

Scope-excluded by charter (not findings): absence of experiments (sec:scope item
5, by design); bernoulliRelations missing DOI (intentional, not yet minted).

## (b) Overall recommendation: **ready**

All four Majors are resolved, every blocking minor is resolved (m1, m3, m7),
the build is production-clean, and the revision introduced no new findings of any
severity. The remaining open items (m4, m5, m6, S1, S2, S6, S7) are all optional
stylistic or enhancement suggestions, none blocking, mostly unchanged stylistic
traits the author may keep by choice. For the stated Zenodo-preprint venue (and,
realistically, for a competitive archival venue too), the paper now clears the
bar: correct math, an asymmetric demonstration on numbers, a grounded and
self-contained novelty/unification story, and a clean build.

The single nudge below the recommendation: this is "ready" for the preprint as
written; an author polishing for a selective archival venue would still benefit
from the two one-line notation bridges (m4, m5) and from citing or dropping the
uncited XOR-PUF aside (see new-findings table). None of these block.

## (c) New findings introduced by the revision

| Severity | Count |
|---|---|
| Critical | 0 |
| Major | 0 |
| Minor | 0 |
| Suggestion | 1 |

The revision broke nothing. No theorem, proof, table value, label, or citation
regressed. The one item surfaced during the fresh pass is a pre-existing,
non-regression aside:

- **(suggestion, pre-existing, not a regression)** sec:related (c), line ~694:
  "the analysis of XOR-PUFs uses the same product form" is an uncited factual
  aside. Git confirms it was in the original draft (bafa230) and survived the
  revision unchanged; it was not flagged in the first review. It is not
  introduced by the edits and is not a regression. Optional fix: add a citation
  for the XOR-PUF product-form claim or drop the half-clause. Listed for
  completeness only.

---

## What the revision did, verified

### M1 (independence framing) -- RESOLVED
sec:scope item 2 now frames the independent prediction as the correlation-free
reference and gives a directional sign rule: positively correlated misreads push
the parity error below the independent value, negatively correlated push it
above. The orchestrator verified this sign independently (two-bit parity, fixed
marginals r, tunable joint p11: P(odd flips) = 2r - 2 p11, so p11 > r^2 gives a
value below the independent 2r(1-r), and p11 < r^2 above). The CTMP `% TODO` is
discharged by citing bravyi2021mitigating (the prior-art pass confirmed CTMP is
defined and used there). A magnitude bound is correctly labeled future work.

### M2 (asymmetric worked example) -- RESOLVED
New Subsection 4.4 and Table 2. Channels: qubits 1,2 at (eps,omega)=(0.02,0.10),
qubits 3,4 at (0.04,0.12). The orchestrator recomputed all five values from
eq:parity-asym independently:

| word | computed | printed |
|---|---|---|
| 0000 | 0.109979 | 0.110 |
| 1000 | 0.174982 | 0.175 |
| 0011 | 0.233842 | 0.234 |
| 1111 | 0.315168 | 0.315 |
| sym q=0.07 | 0.226496 | 0.226 |

The prose claims check out: 1111/0000 = 2.866 ("almost three times"); the three
tau=0 rows span 2.866 ("nearly three"); the symmetrized rate overstates the cold
corner (2.05x, "roughly twofold") and understates the hot one (0.226 < 0.315),
"wrong on both sides at once." The mean of the eight deployed rates is exactly
0.07, so the symmetrized baseline is honestly the fairest single-rate competitor.
This exhibits cor:parity-asym (the paper's most original result) on numbers a
single-rate model cannot produce, which is exactly what M2 demanded.

### M3 (novelty grounding) -- RESOLVED
The live prior-art pass (treated as confirmed per the charter) found no direct
competitor. The text is hardened by naming koh2024readout (arXiv:2406.07611,
mid-circuit/feedforward readout mitigation) as the nearest inverse neighbor and
distinguishing it as "still inverse mitigation ... not a forward symbolic rate
calculus." The contribution remains a correctly-disclaimed synthesis.

### M4 (unification support) -- RESOLVED
Four Zenodo DOIs wired into the framework self-cites (note + doi fields), and a
self-contained one-paragraph statement of the Bernoulli error model added to
sec:related so the unification claim stands without the companion papers (the
Bloom-filter omega=0 corner and the T1-biased interior point are both grounded
against the in-paper theorems).

---

## Detailed notes by domain

### Logic and proofs
All revised math is exact. Table 2 (five values) recomputed to the printed
digits; the M1 parity sign rule verified correct; Table 1 unchanged and still
exact; m1's FPR conditioning fix is correct. No prior result regressed. No new
logic issue. (logic-checker.md)

### Novelty and contribution
M3 and M4 both resolved: M3 by the confirmed prior-art pass plus the
koh2024readout hardening citation; M4 by real DOIs plus a self-contained model
paragraph. The new asymmetric example strengthens the novelty case by making the
two-rate contribution produce a number a single-rate model cannot.
(novelty-assessor.md)

### Methodology
M1 resolved as a directional framing plus a discharged CTMP citation (magnitude
bound correctly future work); M2 resolved with a concrete, correct,
physically-motivated asymmetric example. No experiment added, none needed (theory
paper by design). The Table generator (S-meth-1) is still not shipped (optional).
(methodology-auditor.md)

### Writing and presentation
New passages (Subsection 4.4, the sign-rule paragraph, the self-contained
unification paragraph, the expanded rem:t1) are clear and accurate. P4 (neighbor
count) resolved. m4/m5 partially addressed (no explicit one-line bridges); m6/P5/
P6 unchanged stylistic carryovers. No new prose issue. (prose-auditor.md)

### Citations and references
All five prior-art fixes present and consistent: krawiec rename (no dangling
pucha key), odonnell2014 added, koh2024readout added, parity attribution split,
Tannu 84/62 datapoint added. Four framework DOIs wired; bernoulliRelations
intentionally without one. Internal integrity perfect (18 keys cited, all
resolve, 0 bibtex warnings). One pre-existing uncited XOR-PUF aside carried
forward (not a regression). (citation-verifier.md)

### Formatting and production
Production-clean: 13 pp, 0 undefined refs/cites, 0 bad boxes, 0 bibtex warnings,
0 hyperref PDF-string warnings (m7 resolved). The new Table 2 and Subsection 4.4
labels resolve with no collision or overfull box. (format-validator.md)

---

## Review metadata

- Specialist reports written: logic-checker, methodology-auditor,
  novelty-assessor, prose-auditor, citation-verifier, format-validator.
- Independent computational checks by the orchestrator: Table 2 (all five values
  via eq:parity-asym), the 1111/0000 and symmetrized-baseline ratios, the M1
  two-bit parity sign rule, Table 1 spot-recompute (2 rows), full fresh LaTeX
  build (pdflatex + bibtex + 2 passes), bib key-by-key resolution, `% TODO` and
  dangling-`pucha` grep sweeps.
- Prior findings checked: 4 Majors + 7 minors + 7 suggestions = 18, plus the
  prior-art follow-up's five citation fixes.
- New findings introduced by the revision: 0 (one pre-existing, non-regression
  suggestion noted for completeness).
- Disagreements between specialists: 0.
- Recommendation: **ready**.
