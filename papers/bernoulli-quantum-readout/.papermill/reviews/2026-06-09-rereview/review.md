# Focused Re-Review Report

**Date**: 2026-06-09 (re-review)
**Paper**: A Forward $(\epsilon,\omega)$ Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes
**Author**: Alexander Towell
**Scope**: targeted re-review of (1) the four prior-review minor fixes (M-1, M-2/M-3, C2, M-4) and (2) the NEW Subsection 4.5 "Validation on real device calibration" (`sec:worked-real`, `fig:realcalib`), plus a full regression pass on the pgfplots-bearing build.
**Recommendation**: **ready** (conditional on the qiskit citation before journal submission)

## Summary

**Overall Assessment**: The new real-device validation figure is a genuine strengthening of the paper. The closed form is reproduced on real published calibration rates, and the empirical claim is stated with unusual care: it never claims a live hardware run, and explicitly labels the validation a Monte Carlo of the calibrated channels. The math in the figure was independently re-verified by the orchestrator and reproduces exactly from `code/readout_figure.py`. The build is production-clean: 14 pages, pgfplots compiles with zero warnings, no undefined refs/cites, no label collisions, no overfull boxes. All four prior-review minors are confirmed fixed. The only items remaining are one required-for-submission citation (the qiskit/ibm_hanoi data source is named in prose but not formally `\cite`d) and one stale-scope sentence that now mildly undersells the figure.

**Strengths**:
1. The figure's four series (cold/MC/lin/hot) reproduce coordinate-for-coordinate from the committed `code/readout_figure.py`; every headline number in caption and prose is exact (formula-vs-MC worst diff 9.53e-4 < 10^-3; n=27 cold 0.258, hot 0.369, gap 0.111, linearization +37%). (methodology-auditor, logic-checker)
2. The empirical claim is honestly hedged: "snapshot shipped with qiskit's fake-provider," "a direct Monte Carlo simulation of the same channels," "confirming the formula on real rates." It validates the closed form against simulation on real calibration, and claims nothing more. (prose-auditor, novelty-assessor)
3. All four prior-review fixes verified landed and correct: M-1 (asymmetric eigenvalue now `1-eps-om`, distinguished from the `1-2r_i` bias), M-2/M-3 (the symbol `A` disambiguated row- vs column-stochastic, `A_i` transpose stated), C2 (Walsh attribution split: vonNeumann/Pippenger for the bias-product tradition, O'Donnell for the Fourier framing), M-4 (arXiv entries in `@misc`). (logic-checker, citation-verifier)
4. Subsection 4.5 sits last in the worked-example arc (illustrative, then asymmetric, then real), a natural escalation that lands the paper's practical hook on hardware numbers. (prose-auditor)

**Weaknesses**:
1. The qiskit fake-provider / ibm_hanoi data source is named only in `\texttt{}` prose and the caption, with no formal `\cite`. For a journal submission that now rests an evidentiary figure on a named third-party dataset+software, this is a required citation. (citation-verifier) **[needs external verification]**
2. `sec:scope` item 5 ("Empirical validation") still reads "We make no empirical claim beyond the exactness of the derivations" and frames a "hardware or simulator study" as out of scope, which is now stale: the new figure IS a simulator validation on real rates. Minor self-undercut. (prose-auditor)

**Finding Counts**: Critical: 0 | Major: 0 | Minor: 2 | Suggestions: 2

## Critical Issues
None.

## Major Issues
None.

## Minor Issues

### m1. Data source named but not formally cited (source: citation-verifier) [needs external verification]
- **Location**: `main.tex` lines 723-724 (body) and 758 (caption); `references.bib` (no entry)
- **Quoted text**: "the \texttt{ibm\_hanoi} snapshot shipped with qiskit's fake-provider, dated $2025$-$02$-$26$" (line 723-724)
- **Problem**: The figure's entire evidentiary value rests on a real third-party calibration dataset delivered by named third-party software (qiskit / qiskit-ibm-runtime `FakeHanoi`). It is currently referenced only in prose and a `\texttt{}` mono span, not via `\cite`. Journals (Quantum included) expect software and datasets used as evidence to be formally cited with a version/DOI so the snapshot is locatable and the result reproducible.
- **Suggestion**: Add a `@misc` (or `@software`) entry for qiskit / qiskit-ibm-runtime (with the version that ships the `FakeHanoi` 2025-02-26 properties, and a DOI/URL) and `\cite` it at first mention in 4.5 and in the caption. Optionally a second locator for the device/snapshot provenance. The orchestrator should web-verify the canonical qiskit citation (Qiskit ships a standard `CITATION.bib`/Zenodo DOI) and the `FakeHanoi`/`ibm_hanoi` provenance, and that the 2025-02-26 calibration is the one shipped.
- **Cross-verified**: build inventory confirms 0 of 18 bib entries is qiskit/IBM; grep finds qiskit/hanoi in `main.tex` only at lines 723, 758 (prose/caption), never in a `\cite`.

### m2. Scope item 5 is now stale relative to the new figure (source: prose-auditor)
- **Location**: `main.tex` lines 932-938 (`sec:scope` item 5), against the new 4.5 at 718-777; cf. conclusion next-steps at 963-965
- **Quoted text**: "A hardware or simulator study comparing predicted derived-bit rates against measured ones ... would strengthen the claims but is out of scope for this draft. We make no empirical claim beyond the exactness of the derivations under the stated independence assumption." (lines 934-938)
- **Problem**: Section 4.5 now is a simulator study on real calibration rates, so the scope clause "out of scope for this draft" / "no empirical claim beyond ... exactness of the derivations" reads as if 4.5 did not happen. The conclusion (963-965) likewise still lists "empirical calibration of predicted against measured derived-bit rates" as a future next step. The distinction the author clearly intends (validated against *simulation on real rates*, not yet against *measured derived-bit error on live hardware*) is correct and worth keeping, but the current wording overshoots it and undersells the figure.
- **Suggestion**: Reword item 5 to acknowledge 4.5, e.g. "We validate the closed form against a Monte Carlo of a real device's published calibration (Sec. 4.5); what remains out of scope is a *live-hardware* study comparing predicted derived-bit rates against *measured* ones and quantifying the crosstalk/independence gap." Keep the conclusion's future-work bullet but narrow it to "measured" (live) derived-bit rates so it does not contradict 4.5.
- **Cross-verified**: not a correctness issue; this is a clarity/consistency observation. No second-specialist disagreement.

## Suggestions
1. The hot curve has a visible step at $n=22$ driven by a single outlier qubit ($\omega_{22}=0.1610$, a real and common IBM single-qubit readout outlier; next-highest $\omega\approx0.054$). The figure honestly renders it without comment. Optionally one half-sentence ("the step at $n=22$ is a single high-$\omega$ ancilla") would pre-empt a referee asking whether it is a plotting artifact. Purely optional. (methodology-auditor)
2. The phrase "visible at once on hardware numbers" (line 771) is defensible (the *rates* are hardware-derived) but slightly loose, since the validation curve is a simulation; "on real calibration numbers" would be marginally tighter. Optional. (prose-auditor)

## Detailed Notes by Domain

### Logic and Proofs (logic-checker)
No new theorems were added in 4.5; the figure applies `eq:parity-asym` (cor:parity-asym) forward. The M-1 fix is logically correct: the symmetric channel `eq:assignment` has nontrivial eigenvalue $1-2q_i$, but the asymmetric assignment matrix has eigenvalues $1$ and $1-\epsilon_i-\omega_i$, and the parity formula carries the $\pm1$ flip *bias* $1-2r_i$ (with $r_i\in\{\epsilon_i,\omega_i\}$), which only equals the eigenvalue in the symmetric case. That is exactly what lines 575-578 now say. The cold curve uses $r_i=\epsilon_i$ (latent all-$\ket0$) and the hot curve uses $r_i=\omega_i$ (latent all-$\ket1$), the two extreme latent words, consistent with `cor:parity-asym`. The MC overlay XORs independent per-qubit flip indicators at rate $\epsilon_i$ (the cold-word model), matching the cold curve, as it must.

### Novelty and Contribution (novelty-assessor)
The figure does not change the contribution claim; it instantiates the existing forward calculus on real rates. It does materially help the "the linearization overstates by tens of percent" hook by showing it on a real 27-qubit device (37% at n=27), and it makes the asymmetry concrete (the 0.11 cold/hot gap a single rate cannot represent). The honesty clauses (Sec. 2.2 diagonal-sector faithfulness, Sec. 6 scope) keep the claim from being read as a coherence/quantum-advantage result; 4.5 adds no overclaim. The unclear-writing-as-weak-contribution check is negative: the contribution is clear, and the figure is a demonstration, not a disguised new claim.

### Methodology (methodology-auditor)
Reproducibility is strong: `code/readout_figure.py` hardcodes the 27 `(eps_i, omega_i)` pairs inline (no network, no IBM account), documents the source fields (`prob_meas1_prep0` = eps, `prob_meas0_prep1` = omega), and prints exactly the four coordinate series embedded in `main.tex`. I re-ran it: every coordinate matches the manuscript; omega/eps mean ratio 2.44 (prose "near 2.4"); worst formula-vs-MC diff 9.53e-4 (caption "within $10^{-3}$"); n=27 cold 0.258 / hot 0.369 / gap 0.111 / linearization +37% (caption "by 37% at n=27"). The MC uses a fixed seed (rng default_rng(7)) and $10^6$ trials, so the overlay is itself reproducible. The one methodological caveat, already correct in the prose, is that "validation" here means closed-form vs. simulation of the same channel model on real rates, not vs. measured derived-bit error, which is the honest and correct reading.

### Writing and Presentation (prose-auditor)
4.5 is well-placed (it closes the worked-example escalation) and well-hedged. The title "Validation on real device calibration" is honest given the body immediately clarifies it is the qiskit fake-provider snapshot and a Monte Carlo of the channels; it is not "validation on real device" (which would imply a live run). The two prose issues are m2 (stale scope item 5 / conclusion) and the optional "hardware numbers" tightening. No notation drift introduced.

### Citations and References (citation-verifier)
All 18 bib entries are cited and all 18 resolve (0 undefined). The M-4 fix is in place: `koh2024readout`, `adams2015typetheory`, `cho2015effectus` are `@misc` with `howpublished = {arXiv:...}` rather than miscast as journal articles. The one gap is m1: the qiskit/ibm_hanoi data source is named in prose/caption but has no bib entry and no `\cite`. Tagged **[needs external verification]** for the orchestrator's web pass (canonical qiskit citation + FakeHanoi/ibm_hanoi 2025-02-26 provenance). No other citation regressions.

### Formatting and Production (format-validator)
Build verified clean from scratch (`pdflatex; bibtex; pdflatex; pdflatex`, all exit 0). pgfplots (`compat=1.18`) compiles without error or warning. Final document: **14 pages**. Log audit (pass 3): 0 undefined references, 0 undefined citations, 0 multiply-defined labels, 0 overfull/underfull boxes, 0 hyperref PDF-string warnings, 0 bibtex warnings. The new labels `sec:worked-real` and `fig:realcalib` resolve and do not collide with existing labels. The venue port at `venues/quantum/` already contains the figure (confirmed: `fig:realcalib`/`ibm_hanoi` present), so base and venue versions are in sync. No regression from the pgfplots load.

## Cross-Verification
- m1 (citation) routed conceptually to format-validator + logic-checker: confirmed it is purely a bibliography-hygiene/provenance gap, not a math or build issue (the figure builds and is correct without the cite; the cite is a submission-completeness requirement). No disagreement.
- m2 (stale scope) routed to novelty-assessor: confirmed the stale wording is not hiding a weak contribution. The contribution and the figure's role are both clear; it is a pure consistency edit. No disagreement.

## Venue Verdict

**Primary target unchanged: Quantum.** The new figure strengthens the submission but does not move the paper out of the *Quantum* tier. It validates the closed form against simulation on real calibration rates; it is not a live-hardware measurement of derived-bit error, and the paper (correctly, honestly) does not claim it is. *Quantum* values exactly this kind of reusable, correct, well-scoped tool, and an empirical-on-real-rates figure is a clear plus there.

**PRX Quantum reach: still a stretch, not yet unlocked.** The state file's own gating condition for a PRX Quantum / npj reach is "competitive only with the empirical figure added *and* a broader-impact framing," and PRX Quantum's bar is "lasting/profound impact" with "stronger empirical *or* broader results." The figure added here is a *simulator validation on a fake-provider snapshot* of real rates, not a live-hardware study nor a broadened result set, and the paper is explicitly a focused forward-calculus methods/perspective paper. That clears the "empirical figure added" half of the gate but not the "broader-impact framing / stronger empirical" half. Making PRX Quantum credible would need at least one of: (a) a genuine live-hardware run comparing *predicted vs measured* derived-bit error (which the conclusion still lists as future work and scope item 5 still defers), or (b) a materially broadened impact framing (e.g., a worked decoder-level or error-budget-pipeline impact, or the correlated/CTMP lift). As is, submit to **Quantum** (port `article` to `quantumarticle` from the in-sync `venues/quantum/` at submission); keep PRX Quantum as the documented stretch contingent on a live-hardware empirical upgrade.

## Review Metadata
- Build: pdflatex + bibtex + pdflatex x2, all exit 0; 14 pp; 0 undefined refs/cites, 0 bad boxes, 0 label collisions, 0 hyperref/bibtex warnings; pgfplots clean.
- Figure reproduction: `code/readout_figure.py` re-run; all four series and all headline numbers match `main.tex` exactly.
- Prior fixes verified: M-1, M-2/M-3, C2, M-4 all confirmed landed and correct.
- Cross-verifications performed: 2
- Disagreements noted: 0
- Tagged [needs external verification]: m1 (canonical qiskit citation + FakeHanoi/ibm_hanoi 2025-02-26 provenance).
