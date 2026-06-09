# Multi-Agent Review Report

**Date**: 2026-06-09
**Paper**: A Forward (eps, omega) Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes
**Recommendation**: ready (with two recommended minor wording fixes before journal submission)

**Note on agents**: The Task tool for recursive specialist subagents is unavailable in this context (consistent with project memory: "papermill reviewer has no recursive subagents here"). The orchestrator performed all six specialist passes single-context, with each lens recorded as its own report in this directory, and independently re-verified every numeric and quoted claim against the manuscript and by exact arithmetic plus Monte Carlo. Citation/novelty coverage claims are tagged [needs external verification] for the orchestrator's live web pass.

## Summary

**Overall Assessment**: The paper retained its "ready" status. The new Section 3.6 (`sec:operator`) is correct on its three load-bearing claims, well written, and a net positive: it speaks the QC audience's operator/assignment-matrix language and makes the parity-result-as-intersection-of-two-traditions framing visible, while honestly disclaiming theorem-level novelty and pre-empting a coherence misread. The addition introduced no build, label, citation, or math regression. There is one genuine (minor) imprecision: the closing sentence of the spectral paragraph mislabels the asymmetric `1-2r_i` as a per-bit "eigenvalue," when in the asymmetric case the assignment-matrix eigenvalue is `1-eps-omega`, not `1-2r_i`. The corollary itself is correct; only the prose label overreaches.

**Strengths**:
1. Section 3.6's three core claims all verify independently (logic-checker, methodology-auditor): eq:assignment is exactly the transpose of eq:channel and is column-stochastic; the symmetric channel has eigenvalues `{1, 1-2q}` with the parity mode `(1/2,-1/2)`; the parity-spectral identity matches Monte Carlo.
2. The honesty clause (line 573 to 578) cleanly forecloses a coherence/quantum-advantage misread: classical probability vectors, no Born square, diagonal sector only, eigenvalue not phase (novelty-assessor, logic-checker). Goal 1c satisfied.
3. The addition strengthens venue fit by translating the framework's objects into the mitigation literature's assignment-matrix language, sharpening the "forward complement to inverse mitigation" thesis (novelty-assessor).
4. Production-clean build: 14 pp, 0 undefined refs/cites, 0 bad boxes, 0 bibtex warnings (format-validator). Both worked tables and the spectral identity reproduce exactly (methodology-auditor).

**Weaknesses**:
1. The asymmetric extension of the eigenvalue framing (line 569 to 571) conflates an eigenvalue with a flip-channel bias (logic-checker L1, methodology-auditor M1). Minor, a one-line wording fix.
2. The symbol `A` and the phrase "assignment matrix" are now bound to two matrices that are transposes of each other (row-stochastic at line 269/271, column-stochastic at line 535) (prose-auditor P1). Minor notation collision.
3. "is exactly the assignment matrix ... the transpose of eq:channel" reads as mildly self-contradictory at the surface (prose-auditor P2). Minor wording.

**Finding Counts**: Critical: 0 | Major: 0 | Minor: 4 | Suggestions: 5

## Critical Issues
None.

## Major Issues
None.

## Minor Issues

### M-1. Asymmetric `1-2r_i` mislabeled as a per-bit eigenvalue (source: logic-checker L1, cross-verified by methodology-auditor M1)
- **Location**: main.tex 569 to 571 (closing sentence of the "spectrum" paragraph)
- **Quoted text**: "the asymmetric \cref{cor:parity-asym} is the same coefficient with the per-bit eigenvalue $1-2q_i$ replaced by the latent-conditioned $1-2r_i$, $r_i\in\{\eps_i,\omega_i\}$."
- **Problem**: The eigenvalue identity is correctly scoped to the symmetric channel earlier in the paragraph (line 547). The closing sentence extends it to the asymmetric corollary by calling `1-2r_i` "the per-bit eigenvalue." But the asymmetric assignment matrix `[[1-eps_i,om_i],[eps_i,1-om_i]]` has nontrivial eigenvalue `1-eps_i-om_i` (verified: 0.88 for (0.02,0.10), 0.84 for (0.04,0.12)), which is neither `1-2eps_i` nor `1-2om_i`. The object `1-2r_i` is correctly the bias `E[S_i]` of the latent-conditioned flip indicator `F_i` (which the proof of cor:parity-asym genuinely uses, reading (ii)/(iii)), but it is not the eigenvalue (reading (i)). The corollary and its proof are correct; only the prose label is wrong.
- **Suggestion**: Replace "the per-bit eigenvalue $1-2q_i$ replaced by the latent-conditioned $1-2r_i$" with "the per-bit **flip-channel bias** $1-2q_i$ replaced by the latent-conditioned $1-2r_i$" (i.e. keep the (ii)/(iii) bias/Walsh reading, and note the eigenvalue reading (i) is exact only when `eps_i=om_i`).
- **Cross-verified**: yes, by methodology-auditor (reproduced the `1-eps-om` eigenvalue independently); both concur on minor severity. No disagreement.

### M-2. Symbol `A` overloaded across row- and column-stochastic conventions (source: prose-auditor P1)
- **Location**: main.tex 269/271/504 versus 534 to 535
- **Quoted text**: line 271 "Equation~\eqref{eq:kron} is the \emph{assignment matrix} $A$ of readout-error mitigation, in its tensored/local form."; line 534 to 535 "the joint assignment matrix is the Kronecker product $A=\bigotimes_i A_i$, which is \cref{eq:kron} in the column convention".
- **Problem**: `A` denotes the row-stochastic tensor `Q_1 (x) ... (x) Q_n` at line 269 and the column-stochastic tensor `(x) A_i` at line 535; both are called "the assignment matrix" though they are transposes. The mitigation literature's `A` is conventionally the column-stochastic one, so the line 271 usage is the non-standard side of the overload.
- **Suggestion**: Add a half-clause at line 534 to 535 noting the column-stochastic `A` is the transpose of the row-stochastic `A` of eq:kron and they carry the same content; or rename the column-stochastic joint matrix to keep symbols distinct.
- **Cross-verified**: orchestrator confirmed both joint matrices are written `A` and are transposes (eq:kron row-stochastic, line 535 column-stochastic). Holds.

### M-3. "is exactly the assignment matrix ... the transpose" surface contradiction (source: prose-auditor P2)
- **Location**: main.tex 523 to 533
- **Quoted text**: "The single-bit readout channel of \cref{def:atom} is exactly the \emph{assignment matrix} (confusion matrix) ... it is [eq:assignment] ... the transpose of \cref{eq:channel}."
- **Problem**: "is exactly X" followed by displaying X as the *transpose* of the channel reads as mildly self-contradictory; the intended "same information up to the row-vs-column convention" is recoverable but the word "exactly" overstates.
- **Suggestion**: "is the assignment matrix (confusion matrix) ... up to the row-vs-column-stochastic convention: written as the mitigation literature prefers it is [eq:assignment], the transpose of eq:channel."
- **Cross-verified**: orchestrator confirmed wording at lines 523 to 533. Holds.

### M-4. arXiv entries use @article with journal = "arXiv preprint arXiv:..." (source: citation-verifier C1; pre-existing, not a regression)
- **Location**: references.bib keys `koh2024readout`, `adams2015typetheory`, `cho2015effectus`
- **Quoted field**: `journal = {arXiv preprint arXiv:2406.07611}`
- **Problem**: Under plainnat the literal "arXiv preprint arXiv:NNNN" renders in the journal slot; the conventional preprint form is `@misc` with `eprint`/`howpublished`.
- **Suggestion**: Convert the three to `@misc` with `howpublished={arXiv:...}` (a pre-submission polish item).
- **Cross-verified**: pre-existing; predates this revision. Cosmetic.

## Suggestions
1. (logic-checker L2) Honesty clause line 577 to 578: "relaxation rate" is loose; `1-2q_i` is the eigenvalue/contraction factor. Prefer "relaxation eigenvalue" or "contraction factor." Cosmetic.
2. (novelty-assessor N3) Add a half-clause at the eigenvalue sentence (line 551) flagging the triple-identity as a standard observation for 2x2 stochastic matrices, to fully inoculate against a "claimed insight" misread. The intro disclaimer already covers it.
3. (methodology-auditor M2) Check in a small table-generator script (now that Table 2 has eight rate inputs) so the exactness is referee-auditable. Pre-existing S1.
4. (format-validator F1) Pre-submission: port from `article` to `quantumarticle` for a *Quantum* submission (lighter lift than REVTeX given current natbib/cleveref usage).
5. Carried optional items from prior reviews (m4/m5 notation bridges already applied; P5/P6 sentence-length/folklore-repetition; S2 audience framing; S7 title) remain as-is.

## Detailed Notes by Domain

### Logic and Proofs
Section 3.6's three load-bearing claims verify exactly: (a) eq:assignment = transpose of eq:channel, column-stochastic; (b) symmetric-channel eigenvalues `{1, 1-2q}` with parity eigenvector `(1/2,-1/2)`; (c) eq:parity-spectral matches Monte Carlo. The triple-identity (eigenvalue = ±1 bias = Walsh coefficient) is correct as scoped to the symmetric channel. Regression: Table 1 (six rows) and Table 2 (four words + symmetrized + ratio 2.866) reproduce exactly; no calculus regression. One minor wording fix (M-1).

### Novelty and Contribution
3.6 strengthens the paper: it improves venue fit and makes the cross-domain unification visible while honestly disclaiming theorem-level novelty ("bookkeeping, not new theorems," line 519). The load-bearing claim ("no reusable forward asymmetric (eps,omega) calculus in QC readout") is not weakened; 3.6 sharpens the inverse-vs-forward contrast. Novelty coverage flagged [needs external verification] (N1, N2).

### Methodology
Clean for a perspective/methods paper. All worked numbers reproduce exactly; 3.6 adds no empirical surface and no new methodological risk. The one substantive item (M1 = L1) is a prose label, not a derivation error. The no-empirical-validation limitation is unchanged and honestly scoped (sec:scope item 5).

### Writing and Presentation
3.6 is clean, purposeful prose (dictionary/spectrum split + honesty clause). Two minor notation/wording items: symbol-`A` overload across conventions (M-2), and the "is exactly ... the transpose" surface contradiction (M-3). No problematic redundancy with Section 3.4 or related-work (c): the three views (proof / lineage / operator reading) are complementary.

### Citations and References
Citation-neutral addition: no new bib entries, no dangling cites, 18/18 cited and resolved, 0 undefined. One minor pre-existing hygiene item (M-4, arXiv-as-journal). Content accuracy of the four reused cites is consistent with offline knowledge; flagged C2 to C4 for the orchestrator's live pass.

### Formatting and Production
Production-clean: exit 0, 0 undefined refs/cites, 0 bad boxes, 0 bibtex warnings, 14 pp. Three new labels resolve cleanly; no collisions. Only format item is pre-submission venue-template conversion (F1).

## Literature Context Summary
The field's dominant paradigm is inverse matrix-inversion mitigation (M3, Bravyi/CTMP, Koh feed-forward), which recovers an ideal distribution from observed counts numerically per circuit. The paper's forward symbolic asymmetric calculus answers the complementary design-time question. Offline I am not aware of a competing forward symbolic rate-propagation calculus, but cannot rule out a recent preprint [needs external verification]. The 3.6 spectral framing (eigenvalue `1-2q` = Walsh-Hadamard coefficient) is standard linear-algebra/Boolean-analysis folklore, correctly disclaimed as bookkeeping. Venue: *Quantum* is the better-matched first target (open access, `quantumarticle`, perspective-friendly, no hard page limit); PRX Quantum is a stretch without an empirical section.

## Items tagged [needs external verification] (for the orchestrator's live web pass)
- **N1**: No competing reusable forward asymmetric (eps,omega) Boolean calculus exists in the QC readout literature (the load-bearing novelty claim).
- **N2 / C2**: That vonneumann1956 / pippenger1988 compute the parity/Walsh "spectrum" object as 3.6 states (line 565 to 566). odonnell2014 is the safer Fourier anchor.
- **C3**: nation2021m3 and bravyi2021mitigating bibliographic details and the "calibrate and invert the assignment matrix" role.
- **C4**: koh2024readout (arXiv:2406.07611, mid-circuit + feedforward) and the tannu2019mitigating 84%/62% all-zero/all-one fidelity datapoint. Both pre-existing, carried from prior reviews.

## Venue-Readiness Verdict (target: *Quantum*)
**Ready**, conditional on two cheap wording fixes that any careful referee would otherwise flag:
1. M-1: relabel the asymmetric `1-2r_i` as a flip-channel bias rather than an eigenvalue (one line). This is the only item with a correctness flavor; left as-is, a spectrally-literate *Quantum* referee will catch it.
2. M-2/M-3: disambiguate the `A` / "assignment matrix" overload and soften "is exactly ... the transpose" (two short clauses).

Everything else (M-4 arXiv hygiene, suggestions 1 to 5, the F1 venue-template port) is pre-submission polish, not blocking for the preprint. The core math is verified, the build is clean, the novelty claim is intact, and Section 3.6 improves rather than dilutes the paper. The novelty-coverage and citation-accuracy items remain pending the orchestrator's external web pass; if those clear, the paper is submission-ready for *Quantum* after the wording fixes and the template conversion.

## Review Metadata
- Specialist lenses applied: logic-checker, novelty-assessor, methodology-auditor, prose-auditor, citation-verifier, format-validator (all single-context; recursive Task subagents and live web search unavailable, per project memory).
- Cross-verifications performed: 1 (logic-checker L1 confirmed independently by methodology-auditor M1; both concur, no disagreement).
- Disagreements noted: 0.
- Independent numeric verification by orchestrator: eq:assignment transpose, symmetric eigenvalues/eigenvectors, asymmetric eigenvalue `1-eps-om`, parity-spectral identity (Monte Carlo 2M), Table 1 (6 rows), Table 2 (4 words + symmetrized + ratio). All reproduce exactly.
