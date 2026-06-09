# Novelty Assessor

**Date**: 2026-06-09
**Scope**: Does Section 3.6 strengthen or dilute the contribution? Does the load-bearing novelty claim still hold with the addition?

## Does 3.6 strengthen or dilute?

**Strengthens, net.** Section 3.6 does three things that help the paper's positioning:

1. **Speaks the venue's language.** A *Quantum* / PRX Quantum audience thinks in assignment matrices, confusion matrices, and spectra, not in Bernoulli channels. The "dictionary" paragraph (line 523 to 544) translates the paper's `Q_i`/forward-calculus objects into the mitigation literature's `A_i`/assignment-matrix objects, making the "forward complement to inverse mitigation" thesis concrete at the level of one shared matrix whose only difference is direction. This directly serves the central positioning against the inverse paradigm.

2. **Locates the parity result at a real intersection.** The spectral paragraph (line 546 to 571) makes explicit that the lead result (the syndrome/parity identity) is simultaneously (i) a spectral coefficient of the tensored assignment matrix on the parity mode and (iii) the Walsh-Hadamard object the classical noisy-Boolean-formula tradition computes. That is a genuine, non-trivial framing payoff: it shows the quantum-operator and classical-Fourier readings of the same number coincide, which is exactly the cross-domain unification the paper sells.

3. **Self-polices the framing.** The honesty clause (line 573 to 578) is well judged for novelty hygiene: it denies the coherence/quantum-advantage misread before a skeptical referee can raise it.

**Dilution risk is low and controlled.** The intro to 3.6 (line 517 to 521) front-loads the honest disclaimer "The recasting is bookkeeping, not new theorems." This is the right call: the spectral reading is known folklore (the second eigenvalue of a symmetric 2x2 stochastic matrix is `1-2q`, and the Walsh coefficient of a biased bit is its mean) and claiming it as novel would have damaged credibility. By explicitly framing it as a re-reading that *exposes* an intersection rather than a new theorem, the subsection adds expository value without inflating the contribution.

## Novelty claim status (goal 4)

The load-bearing claim, "no reusable forward asymmetric (eps,omega) Boolean calculus exists in the QC readout literature," is **not weakened** by 3.6. If anything 3.6 sharpens the contrast: it shows the field's own central object (the assignment matrix) is the same matrix, used in the opposite (inverse) direction. The claim itself remains a literature-coverage assertion that I cannot verify offline.

- **N1 [needs external verification]**: "no reusable forward asymmetric (eps,omega) Boolean calculus in the QC readout literature." The 2026-06-07 live prior-art pass (per state.md) found no competitor and named `koh2024readout` as nearest inverse neighbor. Nothing in 3.6 changes the claim, but the orchestrator should re-confirm no forward symbolic rate-propagation tool has appeared.

- **N2 [needs external verification]**: The spectral framing claims the parity identity is "the same Walsh-spectrum object the classical noisy-Boolean-formula tradition computes" (line 565 to 566, citing vonneumann1956/pippenger1988). This is a reasonable attribution (von Neumann and Pippenger analyze noisy formula reliability; the `1-2q` contraction per noisy gate is the standard tool), but whether those specific works phrase it as a Walsh/Fourier spectrum is worth a light external check. Low risk; the odonnell2014 cite (in Section 3.4) carries the explicit Fourier attribution and is the safer anchor.

## Finding (minor, N3), eigenvalue claim is folklore, ensure it reads as such

The triple-identity is correct and the intro disclaims novelty, but a terse referee might still read "That single number is three things at once" (line 551) as a claimed insight. The disclaimer at line 519 covers it. Optional: a half-clause ("a standard observation for 2x2 stochastic matrices") at the eigenvalue sentence would inoculate fully. Severity: suggestion.

## Verdict
Section 3.6 is a net positive for the contribution: it improves venue fit and makes the unification visible, while honestly disclaiming theorem-level novelty. The core novelty claim is intact. No major novelty concern introduced.
