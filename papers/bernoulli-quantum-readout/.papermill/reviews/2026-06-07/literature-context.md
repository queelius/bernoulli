# Literature Context Packet

**Paper**: A Forward (epsilon, omega) Calculus for Quantum Readout Error
**Date**: 2026-06-07

**Provenance note**: In this run the orchestrator could not dispatch the two
literature-scout subagents (no recursive Task tool available), and had no live
web search. This packet is therefore assembled from the orchestrator's own
domain knowledge and from internal analysis of the manuscript's bibliography.
Claims that would normally be scout-verified against the live literature are
marked **[needs external verification]**. The em-dash character is avoided per
the file-writing constraint.

## Field landscape (readout-error modeling and mitigation)

The dominant paradigm for readout error on near-term superconducting devices is
**assignment-matrix (confusion-matrix) mitigation**: build the stochastic matrix
A mapping ideal to observed outcome distributions, then (approximately) invert it
to correct measured counts. The paper's cites cover the canonical line:

- **M3 (nation2021m3)**: scalable, matrix-free iterative correction that avoids
  materializing the full 2^n x 2^n matrix; the de facto practical tool in Qiskit.
- **bravyi2021mitigating**: multiqubit treatment; introduces correlated-readout
  modeling, including (to the orchestrator's recollection, **[needs external
  verification]**) a continuous-time Markov process (CTMP) model for correlated
  measurement errors. This is the citation the paper's CTMP TODO is seeking.
- **Tensored / local assignment-matrix mitigators** (the eq:kron factorization):
  standard practice, A = tensor Q_i over independently-read qubits.

All of these are **inverse** (data -> ideal), **numerical**, **per-circuit**.
The paper positions itself as the **forward / symbolic / design-time** complement,
which is a coherent and, structurally, an under-occupied niche: the mitigation
literature is overwhelmingly about cleaning measured data, not about symbolically
predicting the error of a *derived* bit before any data are taken.

## Asymmetry and the physics

- **tannu2019mitigating** and **hicks2021readout** establish that readout error is
  state-dependent / asymmetric, driven by T1 relaxation during the measurement
  window, biasing 1->0 misreads. This is well accepted; the asymmetry itself is
  not contested. The paper's claim is not that asymmetry is unknown but that the
  *forward propagation of both rates through Boolean post-processing* is not
  packaged as a reusable calculus.
- **Open question for the author [needs external verification]**: tensored
  mitigation tools retain per-qubit asymmetric 2x2 channels, so they do *carry*
  two rates at the single-qubit level. The paper's "they symmetrize" criticism is
  fair for single-rate folklore and summarized reporting but may overstate the
  case against the full mitigation tooling. The novelty is the *forward symbolic
  propagation through connectives*, not "we noticed readout is asymmetric."

## Syndrome / QEC reliability context

- **fowler2012surface** anchors the syndrome-extraction setting. In fault-
  tolerance threshold analyses, measurement error on syndrome bits is standard
  and modeled per-round; decoders (MWPM, union-find, belief propagation) consume
  noisy syndromes. The paper's contribution is *not* a decoder or a threshold
  result; it is the closed-form per-syndrome-bit flip probability and a
  correction to the "n times q" back-of-envelope. **[needs external
  verification]**: whether any QEC-architecture paper already states the
  1/2(1 - prod(1-2q_i)) syndrome-flip form symbolically. The formula itself is
  elementary noisy-parity, so it is plausible it appears somewhere; the paper's
  defensible claim is the *reusable calculus*, not the single formula.

## Adjacent theoretical frameworks

- **Effectus theory / Adams-Jacobs (cho2015effectus, adams2015typetheory)**: a
  categorical "algebra of predicates" unifying classical, probabilistic, and
  quantum logic. It provides *structure* (effect algebras, predicate calculus)
  but not device-level (epsilon, omega) *rate-propagation rules*. The paper's
  distinction (structure vs numbers) is fair and is the most important neighbor
  to keep separate. **[needs external verification]** that no effectus-derived
  work instantiates concrete readout rates.
- **Asymmetric quantum hypothesis testing / channel certification
  (pucha2021certification)**: two-sided (type I / type II) single-measurement
  models. The paper's distinction (single decision vs composition over many bits)
  is structurally sound.

## Classical lineage of the math

- **Noisy Boolean formula reliability (vonneumann1956, pippenger1988)** owns the
  reliability-of-formulas tradition. The exact +-1-encoding parity-bias identity
  1/2(1 - prod(1-2q_i)) is **folklore / coding-theory / Fourier-analysis of
  Boolean functions** (e.g. it is the standard "probability a sum of independent
  bits is odd"). The paper correctly disclaims originality on the formula; the
  precise canonical pointer is arguably O'Donnell-style Boolean-function analysis
  rather than von Neumann specifically. **[needs external verification]** for the
  most appropriate primary citation.
- **Bloom filters (bloom1970)** and the author's Bernoulli framework supply the
  classical-probabilistic-data-structure side of the unification. The one-sided
  (omega = 0) Bloom corner and the asymmetric interior point being the *same*
  object is the paper's signature observation. Internally coherent; the framework
  references are unpublished and locator-free (see citation-verifier).

## Novelty bottom line (for the synthesis)

The structural niche the paper claims (forward, symbolic, asymmetric, reusable,
unified with Bernoulli/Bloom) is plausibly under-occupied and the framing is
honest. The **one load-bearing risk that could not be closed in this run** is the
existence of a direct competitor: a prior forward closed-form asymmetric Boolean
readout calculus, or QEC tooling that already propagates two-sided readout rates
symbolically through syndrome logic. A targeted live search is required before
the "missing piece" claim should be considered settled.

## Items the author already flagged (known gaps, not new findings)

1. A stable primary citation for CTMP-style correlated readout (likely
   bravyi2021mitigating; confirm).
2. An empirical hardware/simulator study (explicitly out of scope for this draft).
