# Cover letter: submission to *Quantum*

Dear Editors,

Please consider the enclosed manuscript, "A Forward (epsilon, omega) Calculus for
Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes,"
for publication in *Quantum*.

**The gap.** A near-term quantum program rarely reports raw measurements; it
reports Boolean functions of them: syndrome parities, majority votes, feed-forward
conditionals. Readout error is asymmetric (T1 relaxation makes 1-to-0 misreads more
likely than 0-to-1), yet the error on these *derived* bits is today either
reconstructed numerically per circuit by inverse mitigation (M3, Bravyi et al.) or
estimated with a symmetrized, single-rate rule of thumb. There is no reusable,
closed-form, *forward* calculus that predicts a derived bit's error at design time
while preserving the asymmetry.

**The contribution.** We supply that calculus: closed forms for how a
false-positive / false-negative pair (epsilon, omega) propagates through NOT, AND,
OR, parity, chained composition, and independent-qubit (Kronecker) composition. The
lead result is the exact reliability of a quantum-error-correction syndrome bit, a
parity of n noisy ancillas, which flips with probability (1/2)(1 - prod_i (1 - 2 q_i)),
contrasted with the field's "about n times the per-measurement error" linearization
(an overestimate of tens of percent). We validate the closed forms against a direct
Monte Carlo simulation on the *real* readout calibration of a 27-qubit device
(ibm_hanoi): the formula is exact to within 1e-3, the linearization overestimates by
37% at n = 27, and the cold/hot asymmetry gap that a single rate discards is plainly
visible. The same calculus is the error model of Bernoulli type theory, so it also
unifies a quantum-hardware error model with the classical theory of Bloom filters.

**Scope, stated plainly.** The contribution is forward prediction and error
budgeting, complementary to (not competitive with) inverse mitigation; the closed
forms hold under per-bit channel independence, on the diagonal readout sector. We do
not claim the single-bit asymmetric channel or the parity identity as new; the new
artifact is the reusable forward asymmetric Boolean calculus, its application to
readout, and the cross-domain unification.

*Quantum* is the natural home: this is a reusable, symbolic methods contribution for
the quantum-computing community, the kind of tool the journal publishes. The work is
original and not under consideration elsewhere, and every result is reproducible
(the validation figure regenerates from a self-contained script that carries the
calibration snapshot inline).

Thank you for your consideration.

Alexander Towell
Southern Illinois University Edwardsville
atowell@siue.edu  |  ORCID 0000-0001-6443-9897
