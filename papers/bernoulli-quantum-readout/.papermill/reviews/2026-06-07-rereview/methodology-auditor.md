# Methodology auditor (re-review)

Date: 2026-06-07 (re-review of revision commit 6f136b7)
Scope: did the revision close the two methodology Majors, M1 (independence never
framed/bounded) and M2 (worked example symmetric so asymmetry never shown)?

## M1: independence assumption now framed as the reference point

RESOLVED (as framing; a quantitative bound is still future work, which the paper
now states explicitly and correctly).

sec:scope item 2 was rewritten. It now:
1. Names the independent prediction as the "correlation-free reference": exact
   given the per-qubit marginals alone.
2. Gives a directional sign rule for the perturbation under correlation, on a
   parity: positively correlated misreads push the parity error below the
   independent value, negatively correlated push it above (verified correct by
   logic-checker).
3. Calls the independent rate a "two-sided anchor, not a worst case," and names
   "bounding the perturbation for a given CTMP generator" as the natural next
   step.
4. Cites bravyi2021mitigating for the CTMP correlated model, discharging the
   prior `% TODO`.

The prior M1 complaint was that the paper criticized the linear rule for
inaccuracy while never characterizing its own inaccuracy under crosstalk. The
revision answers the symmetric question with a directional (sign-determined)
statement rather than leaving it blank. That is exactly the "even a single
directional statement would close this" remedy the prior review proposed. A
closed-form magnitude bound is genuinely future work and is now labeled as such,
which is the honest scope move.

This is a framing/positioning fix, not a new derivation, so there is no new math
to audit. The one substantive claim (the sign) is correct.

## M2: the asymmetric worked example now exists

RESOLVED.

The prior M2 complaint: every number in the paper was reproducible from the
symmetric single-rate identity that the paper itself attributes to prior art, so
the headline asymmetric machinery never produced a concrete number. The revision
adds Subsection 4.4 and Table 2: a four-ancilla T1-biased syndrome with
inhomogeneous channels (qubits 1,2 at (0.02,0.10), qubits 3,4 at (0.04,0.12)),
evaluated on four latent words plus a symmetrized baseline. This:
- Exercises cor:parity-asym (the paper's most original result) on numbers.
- Shows the latent-assignment dependence the symmetric identity cannot express:
  three tau=0 words carry visibly different error (0.110, 0.234, 0.315).
- Makes the "single-rate model is wrong on both sides" claim concrete (symmetrized
  0.226 overstates the cold corner ~2x and understates the hot one).

The example is well-chosen for methodology: the asymmetry is physically motivated
(omega > eps from T1 relaxation, consistent with rem:t1), the inhomogeneity is
realistic (two qubit classes), and the symmetrized baseline is the fairest
one-rate competitor (the mean of the deployed rates). The numbers are exact
(confirmed by logic-checker). This is precisely the "demonstrate, do not assert"
fix M2 asked for.

## Reproducibility note (prior suggestion S-meth-1)

Still not shipped: there is no ancillary generator script or notebook cell for
Table 1 or Table 2. The values are simple enough to recompute by hand (and I did),
so this remains an optional enhancement, not a defect. Carrying forward as a
suggestion, not a finding.

## New methodology findings introduced by the revision

None. The revision added an example and a framing paragraph; both are sound,
honestly scoped, and consistent with the rest of the paper. No experiment was
added that would need design scrutiny (the paper remains theory/perspective by
design, sec:scope item 5).

## Verdict

Both methodology Majors (M1, M2) are resolved. M1 as a directional framing plus
a discharged CTMP citation (a magnitude bound remains correctly labeled future
work); M2 as a concrete, correct, well-motivated asymmetric example. No new
methodology issues.
