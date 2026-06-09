# Literature Context Packet

**Date**: 2026-06-09
**Note on method**: The Task tool for live literature scouts is unavailable in this single-context review (consistent with the project memory "papermill reviewer has no recursive subagents here"). This packet is the orchestrator's offline survey from training knowledge. **Every coverage claim about "no competitor exists" is tagged [needs external verification]**; the orchestrator will run the live web pass personally.

## Field map: quantum readout-error handling

The mature response to readout error in superconducting QC is **inverse mitigation**: build an assignment (confusion) matrix relating ideal to observed outcome distributions and (approximately) invert it.

- **Tensored / local assignment matrix**: factor the joint assignment matrix as a Kronecker product of per-qubit 2x2 matrices, invert locally. Standard practice.
- **M3 (`nation2021m3`)**: matrix-free scalable mitigation that avoids forming the full 2^n matrix, solving the linear system in a subspace of observed bitstrings. PRX Quantum 2021. **[details consistent with training knowledge; confirm offline]**
- **Bravyi et al. (`bravyi2021mitigating`)**: multiqubit mitigation; introduces the **CTMP (continuous-time Markov process)** correlated-noise model for measurement crosstalk. Phys Rev A 103, 042605, 2021. **[consistent; confirm]**
- **Koh, Koh, Thompson (`koh2024readout`)**: readout error mitigation for **mid-circuit measurements and feedforward**, arXiv:2406.07611, 2024. This is the nearest neighbor that targets the same derived/fed-forward readouts the paper post-processes, but it is still inverse mitigation of measured outcomes. **[the most important competitor to confirm; needs external verification]**

All of the above answer the **inverse** question: given observed counts, recover the ideal distribution, numerically, per circuit.

## The gap the paper claims

There is no reusable, closed-form, **forward** calculus that, given per-qubit (eps,omega) rates, predicts the asymmetric error of a specific Boolean-derived bit (parity/AND/OR/majority/feed-forward) symbolically and before data. This is the load-bearing novelty claim.

- **[needs external verification]** I am not aware of a forward symbolic asymmetric rate-propagation calculus for post-processed measurement bits in the QC literature. The closest forward objects are error-budget/union-bound rules of thumb (the "n times per-measurement error" linearization the paper critiques), not a reusable two-rate calculus. I cannot rule out a recent (2024 to 2026) preprint; the orchestrator's live pass should confirm.

## Adjacent traditions the paper correctly positions against

- **Asymmetric quantum hypothesis testing / channel certification** (`krawiec2021certification`): a two-sided false-positive/false-negative model of a *single* measurement. Nearest neighbor of the atom; lacks the Boolean-composition layer. Plausible role. **[confirm bibliographic details]**
- **Effectus theory / Adams-Jacobs type theory** (`cho2015effectus`, `adams2015typetheory`): categorical algebra of predicates; a foundation for the structure of probabilistic/quantum logic, not a device readout-rate model. Correctly distinguished by "we propagate numbers, not just predicate structure."
- **Classical noisy-Boolean-formula reliability** (`vonneumann1956`, `pippenger1988`) and **analysis of Boolean functions** (`odonnell2014`): own the parity-bias / `1-2q` contraction identity under a single *symmetric* rate. The paper correctly cites these as prior art for the parity formula and claims only the asymmetric two-rate bookkeeping + quantum application + unification.
- **Relaxation-physics asymmetry** (`tannu2019mitigating`, `hicks2021readout`): establish state-dependent (T1-driven) readout bias, the source of omega>eps. The 84%/62% all-zero/all-one fidelity figure is attributed to Tannu & Qureshi. **[confirm this specific datapoint, needs external verification]**

## On the new Section 3.6 spectral framing

- The fact that a symmetric 2x2 stochastic matrix has eigenvalues `{1, 1-2q}` with the difference mode `(1/2,-1/2)` as the nontrivial eigenvector is standard linear-algebra folklore (Markov-chain spectral gap). The paper is right to disclaim it as "bookkeeping, not new theorems."
- The identification of the nontrivial eigenvalue with the Walsh-Hadamard coefficient of the flip distribution on the parity character is also standard in analysis of Boolean functions. The framing payoff is expository (it co-locates the operator-spectrum and Fourier readings), not a new result. **No overclaim risk** given the explicit disclaimer.

## Venue fit

- ***Quantum*** (the journal, quantum-journal.org): open-access, accepts research and perspective-style work; uses the `quantumarticle` class; no hard page limit. A clean forward-calculus + unification paper of 14 pp is plausible there, especially framed as bridging readout mitigation and classical probabilistic data structures. The main referee risk is "is the forward calculus enough of a contribution, or is it folklore arithmetic?" The paper's defense (reusability + asymmetry + cross-domain unification, all honestly scoped) is reasonable, but referees may push for an empirical/simulator demonstration (the paper concedes this as future work).
- **PRX Quantum**: higher-impact-bar, REVTeX, typically expects either a substantial methodological advance or strong empirical results. A perspective/methods paper with no hardware study is a harder sell here than at *Quantum*.

**Recommendation on venue**: *Quantum* is the better-matched first target; PRX Quantum is a stretch without an empirical section.
