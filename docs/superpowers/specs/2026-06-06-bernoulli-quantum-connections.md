# Concept Note: Bernoulli Types and Quantum Mechanics

**Date:** 2026-06-06
**Author:** Alexander Towell
**Status:** Research concept note (post-brainstorm and literature scan). Captures the validated connections, a candidate research direction, and a monograph/paper integration plan. One prior-art verification step remains open before the research direction is committed.

## Provenance

A brainstorm pressure-tested four proposed analogies between the Bernoulli model (random approximate types carrying rates `(epsilon, omega)`) and quantum mechanics. A four-way parallel literature scan then gated the one analogy that looked like a research direction. This note records the outcome and the plan.

## Thesis

The Bernoulli model is the classical, post-measurement (diagonal) sector of quantum mechanics: its latent value is a non-contextual local hidden variable, and the model is exact precisely where the density matrix is diagonal in the measurement basis, which is the qubit readout sector. This one observation (a) explains which quantum analogies are sound and which are empty, (b) maps the framework's axioms onto the physics that forbids hidden variables (Bell, Kochen-Specker, Fine's theorem), giving the negative-space chapter its most rigorous example, and (c) identifies one open research direction: a forward, asymmetric `(epsilon, omega)` composition calculus for quantum readout error and for the classical post-processing of measurement outcomes.

## 1. The conceptual backbone: the latent value as a hidden variable

The Bernoulli atom posits a definite pre-existing truth `t` (or a latent function value `f(x)`), garbled by a classical channel `Q`, and recovered by Bayes. That commits the model to a single joint distribution over the truth and all observations, which is exactly the textbook hidden-variable assumption. The pre-measurement quantum state is strictly richer: it is a density matrix `rho`, and the Bernoulli model only ever sees `diag(rho)` in the measurement basis. The off-diagonal coherences (relative phase, the capacity for interference) have no slot in the model. A latent-value-plus-noise model can only add probabilities; it can never make them cancel, so any interference-bearing pre-measurement state is outside the model's expressive range by construction.

Consequences:

- **Faithfulness is a theorem, not a judgment.** The latent value is a faithful description precisely when `rho` is diagonal in the measurement basis: an eigenstate, a classical mixture, or a post-decoherence state. That diagonal sector is exactly readout. Decoherence is the process that zeroes the off-diagonals and makes the Bernoulli model become exact. This is why the readout direction (Section 5) is sound and the bare "Bernoulli is decohered quantum mechanics" framing is true but inert.

- **The axioms map onto the physics that kills hidden variables.**
  - Axiom 1 (cross-instance independence) corresponds to locality. Two entangled qubits are not two independent `Bernoulli<bool>` instances; their correlations exceed anything a factorized Bernoulli composition can produce. The Bell inequality is the quantitative bound on how far they sit outside the model, and Axiom 1 is precisely the premise that Bell experiments falsify.
  - The global-joint-distribution assumption corresponds to non-contextuality. Fine's theorem (Fine 1982) states that a joint distribution over all observables exists if and only if a local hidden variable model exists if and only if the Bell/CHSH inequalities hold. The Bernoulli latent value asserts exactly that a joint distribution over all query answers exists.
  - The obstructions are entanglement (Bell) and incompatible observables in dimension at least 3 (Kochen-Specker). A single qubit measured in a fixed basis does admit a hidden-variable model; the obstructions appear with entanglement and with dimension at least 3.

- **The composition theorem presupposes a resampleable latent value.** Classical amplification (majority vote over `k` independent noisy looks, error vanishing) requires a stable value sitting there to be resampled. A superposition has none: the first measurement collapses it, and re-measuring in the same basis returns the collapsed outcome, not a fresh independent sample. So "repeat to denoise" fails on a quantum state, which is exactly why one must amplify the amplitude coherently before measuring rather than average outcomes after. Grover does not beat the composition theorem; it operates in the regime where the theorem's premise does not hold.

## 2. The four analogies, pressure-tested

1. **Bernoulli is the measured/decohered shadow of a quantum channel.** True but inert. Correct, and it frames the model's place, but it is true of all classical probability and yields no leverage in either direction. Keep as one framing sentence; not a result.

2. **Grover's output is a tunable one-sided `Bernoulli<bool>`.** Solid at the output: a single measured outcome after `k` iterations is a `Bernoulli<bool>` with success probability `sin^2((2k+1) theta)`, `sin theta = sqrt(M/N)`, and with `O(1)` verification it is one-sided (`epsilon = 0`, `omega = cos^2((2k+1) theta)`), the dual of Bloom and Miller-Rabin on the coRP/Las Vegas axis. The deeper and more useful fact is that the iteration process is not Bernoulli composition (it is coherent), so Grover is best read as a counterexample to "all amplification is Bernoulli composition." A real disanalogy follows: classical composition is monotone (more rounds never hurt); Grover overshoots (the success probability oscillates, so over-iterating drives it back down). Coherence buys the speedup and costs monotonicity.

3. **Amplitude amplification equals the composition theorem, and the square-root is the Born square.** Precise and correct, and the strongest expository content, but textbook quantum computing. Classical OR-composition gives found-probability about `k p` (linear in `k`); coherent amplification accumulates amplitude about `(2k+1) sqrt(p)` (linear in `k`) and squares only at the end, giving found-probability about `4 k^2 p` (quadratic in `k`). To reach near certainty: classical `k` about `1/p`, quantum `k` about `1/sqrt(p)`. The quadratic gap is exactly probability equals amplitude squared, applied to a quantity that accumulates linearly. Fair only as oracle-query complexity with no intermediate measurement (the quantum Zeno point).

4. **`Q` is the quantum readout/assignment matrix; the n-ary channel is the multi-qubit confusion matrix; the Kronecker factorization is tensored mitigation.** Structurally exact and the only research seed. As stated it re-describes known practice, so the contribution must be the algebra, not the matrix. See Sections 3 and 5.

## 3. Literature scan: what is settled, what is open

Four parallel scouts (asymmetric readout, measurement-chain/Boolean composition, prevalence-aware confidence, and the core abstract-data-type framing) converged on a single shape: the ingredients are settled; the artifact is not.

**Settled (cite as motivation and prior art, never as a contribution):**

- Readout error is an asymmetric channel with `omega > epsilon` from T1 relaxation during the measurement window (Tannu and Qureshi, MICRO-52 2019; Hicks, Bauer, Nachman, PRA 103, 022407, 2021).
- The single-bit two-rate classical channel model of readout, and the matrix-inversion paradigm: M3 (Nation, Kang, Sundaresan, Gambetta, PRX Quantum 2, 040326, 2021), Bravyi et al. (PRA 103, 042605, 2021), Qiskit local/tensored mitigators. The tensored assignment matrix `A = tensor of A_i` is the linear-algebra shadow of the Kronecker factorization.
- The closed-form parity identity `Pr(parity = 1) = (1/2)(1 - product(1 - 2 q_i))` is classical prior art (von Neumann 1956; Pippenger 1988; noisy Boolean formulas, Mozeika and Saad, arXiv:1003.3806 and 1206.4851; XOR-PUF analysis). The AND/OR/XOR rate identities are therefore not original in isolation.
- The two-sided `(F_plus, F_minus)` single-measurement model already appears in asymmetric quantum hypothesis testing and channel certification (e.g. arXiv:1407.0884; "Excluding false negative error in certification of quantum channels," Sci. Rep. 11, 2021). This is the nearest neighbor of the atom and must be cited to preempt "this is just type I/II error."

**Open (the genuine contribution):** a typed, asymmetric, forward `(epsilon, omega)` calculus that propagates rates through Boolean, set, map, and relation operations in closed form, applied to readout and to the classical post-processing of measurement shots, together with the cross-domain unification with Bloom filters and cipher maps. The quantum-readout field handles derived-bit error either numerically per circuit (confusion-matrix inversion, probabilistic error cancellation) or by feeding soft information to numerical decoders, and it routinely symmetrizes away the asymmetry the calculus preserves. No reusable forward symbolic calculus exists there.

**Must cite and distinguish (a knowledgeable reviewer will raise these):**

- Effectus theory and the Adams-Jacobs type theory for probabilistic and Bayesian reasoning (Cho, Jacobs, Westerbaan, arXiv:1512.05813; Adams and Jacobs, TYPES 2015, arXiv:1511.09230; Hayashi/Cho thesis, arXiv:1910.12198). This is the one existing "algebra of predicates" in which Boolean and probabilistic logic are special cases of the quantum case, the same structural DNA. It is a categorical foundation for quantum theory, not a readout-error data type, and carries no `(epsilon, omega)` rate propagation. This is the most important neighbor to distinguish.
- Tensored/local assignment-matrix mitigation (above): the Kronecker product must be positioned as the typed/symbolic lift, not the discovery that independent-qubit errors factor.
- The classical parity/noisy-formula identities (above): position originality as the asymmetric two-rate bookkeeping plus the quantum-measurement application plus the unification, not the parity formula.

**Scoping caveats (state up front):**

- Direction. The quantum field's task is inverse (de-noise an observed distribution back toward truth). The Bernoulli algebra is forward (predict and budget the error on a computed/derived bit). The value proposition is analytic propagation and error budgeting, not beating M3 at mitigation.
- Independence. The closed form holds under per-bit channel independence; real devices have measurement crosstalk (the reason CTMP-class models exist). Frame the calculus as the independent/tensor regime, with a correlated-channel extension as future work.

**Lead worked example:** the reliability of a syndrome bit, a parity of noisy measured ancillas, as the exact `(1/2)(1 - product(1 - 2 q_i))` versus the field's casual "about n times the per-measurement error" linearization. A clean, checkable place where the closed form is tighter than common practice.

Citation caveat: the quantum-computing citations above were surfaced by dispatched literature agents and are treated as leads pending direct verification (see Section 6). The physics-foundations citations (Bell 1964; Fine, PRL 48, 291, 1982; Kochen-Specker 1967; effectus theory) are well established.

## 4. Integration plan (A): monograph and the papers

Three insertions in the monograph, plus the matching papers. Each is expository and rests only on settled results, so each can land independently of the research direction.

- **ch11 (Randomized Algorithms).** A remark: Grover and amplitude amplification are the coherent upgrade of the composition theorem. Classical amplification composes probabilities (`1 - (1 - p)^k`); quantum amplification composes amplitudes (linear in `k`) and squares once at the end, so the quadratic speedup is exactly the Born square. The premise of the composition theorem, a stable latent value to resample, is what a superposition lacks, which is why one amplifies before measuring. Note the disanalogy: coherence makes the process non-monotone (overshoot). Mirror this into the randomized-algorithms paper material (RP/coRP/BPP, and BQP as the quantum sibling).

- **ch16 (Approximate but Not Bernoulli, the negative space).** The strongest and most original piece. Quantum contextuality and nonlocality are the most rigorous physical archetype of "approximate but not Bernoulli." The latent-value assumption is "a joint distribution over all query answers exists"; contextuality is "it does not." Fine's theorem makes the equivalence precise; Axiom 1 is locality; Bell and Kochen-Specker are the quantitative and structural failures. This gives the negative-space chapter its sharpest example. Mirror into the relevant paper (the classification-measures or the sets/relations material that discusses the model's limits).

- **ch1/ch9 (framing).** A short framing note: the Bernoulli model is the diagonal/readout sector of quantum mechanics; the latent value is a non-contextual local hidden variable, faithful exactly when `rho` is diagonal in the measurement basis. ch9 (approximate functions, channels) is the natural home for the channel-matrix correspondence.

- **Claim 1** appears only as a single framing sentence wherever the decohered-sector point is made; it is not given its own treatment.

## 5. Research direction (B): a forward (epsilon, omega) calculus for quantum readout

**Working thesis.** Quantum readout error is a classical asymmetric channel on the diagonal (latent-value) sector, and the classical post-processing of measurement outcomes (parity/syndrome extraction, majority vote, feed-forward conditionals, decoded logical bits) computes Boolean functions of noisy bits. A typed, asymmetric, forward `(epsilon, omega)` calculus propagates readout rates through that post-processing in closed form, including the asymmetric and one-sided (Z-channel) regimes that match T1-dominated readout, without materializing or inverting the full `2^n` assignment matrix. The same calculus is the one that governs Bloom filters and cipher maps, so the contribution unifies a classical-data-structure error model with a quantum-hardware error model.

**Why it is sound.** Readout is exactly the diagonal sector where the latent value is real (Section 1). The atom is the asymmetric two-rate channel; the composition rules are the existing Bernoulli AND/OR/NOT and Kronecker results; the application is the forward error budget of derived classical bits.

**Positioning.** Forward (prediction/budgeting), complementary to inverse mitigation (M3, CTMP); closed form under independence, with correlated extension as future work; distinguished from effectus theory (foundation, not a rate calculus), from tensored mitigation (numeric, inverse), from the classical parity identities (symmetric, single-rate), and from asymmetric quantum hypothesis testing (single measurement, no composition layer).

**Lead result to write first.** The syndrome-bit example of Section 3.

**Candidate venues.** A short methods/perspective paper bridging probabilistic data structures and quantum readout, or a quantum-information venue note. To be decided after the verification gate.

## 6. Open verification gate

Before committing the research direction, close two prior-art risks personally (not via dispatched agents):

1. Effectus theory and effect algebras: read enough of Adams-Jacobs and the effectus introduction to confirm they do not already provide a readout-error rate-propagation calculus, and write the one-paragraph distinction.
2. A targeted sweep of the QPL (Quantum Physics and Logic) proceedings, roughly 2020 onward, the one venue where a closer categorical or compositional hit could hide.

Also verify the decisive quantum-computing citations in Section 3 directly (the agent findings are leads, not verdicts).

### Verification outcome (2026-06-06)

- **Fine's theorem confirmed exactly** (Fine, PRL 48, 291, 1982): a deterministic hidden-variable model, a factorizable stochastic model, a single joint distribution over all observables returning the experimental probabilities, and the Bell inequalities are mutually equivalent. This is the precise anchor for the ch16 mapping (the latent value asserts the global joint distribution; its failure is contextuality/nonlocality).
- **Tannu and Qureshi confirmed** (MICRO-52, 2019): state-dependent (asymmetric) readout bias, measurement errors of 8 to 30 percent, exploited for mitigation. Sound motivation citation for asymmetric readout.
- **Effectus theory and readout error are disjoint literatures.** A combined search returns only matrix-inversion / CTMP mitigation and no effectus content, so the readout-error-rate calculus is not subsumed by effectus theory. The distinction to draw in writing: effectus theory is a categorical foundation in which predicates form effect algebras (Boolean and probabilistic logic as special cases of the quantum case); it models the structure of quantum and probabilistic theory and Bayesian conditioning, not device readout-error rates, and carries no `(epsilon, omega)` propagation.
- **QPL/EPTCS sweep (title level).** Proceedings located for the 20th to 22nd conferences (2023 to 2025); venue-restricted searches surfaced no compositional readout-error-rate calculus. The venue is categorical foundations (ZX, semantics), orthogonal to device readout-error rates.

Outcome: the gate is substantially closed. The research direction (B) is open as a bounded modeling and forward-analysis contribution, positioned against effectus theory, tensored mitigation, and the classical parity identities. Residual low-risk item: a full table-of-contents scan of QPL from 2020 onward at paper-writing time, since absence of evidence is weaker than presence.

## 7. Risks and honest scoping

- The single-bit asymmetric-channel primitive is not original; the algebra over it is the claim.
- Independent-qubit composition is not original (tensored matrices ship in Qiskit); the typed symbolic lift is the claim.
- The parity identity is classical prior art; the asymmetric two-rate bookkeeping plus the quantum application plus the unification is the claim.
- The contribution is a modeling/abstraction and forward-analysis contribution, not a mitigation method that outperforms existing tooling.

## 8. Next steps

1. User reviews this note.
2. Close the verification gate (Section 6).
3. Execute the monograph integration (A): ch16 first (highest value), then ch11, then the ch1/ch9 framing, then mirror into the matching papers.
4. If the gate confirms the opening, draft the research-direction paper (B), starting from the syndrome-bit worked example, and decide the venue.
