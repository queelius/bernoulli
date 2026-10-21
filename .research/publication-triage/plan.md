# Bounded Publication Triage Implementation Plan

**Goal:** Decide whether one existing conventional research paper can be finished
with approximately one working week or less of additional author effort.

**Architecture:** Independent candidate notes and reproducible finite audits;
one integrated claim ledger and final publication decision. Canonical manuscripts
and package source remain read-only unless a finalist warrants essential fixes.

**Tech stack:** Existing Python environment, exact rational enumeration, pytest,
primary-source literature. No new product dependencies are anticipated.

**Spec:** The user's active /goal and [state.md](state.md).

## Tasks and ownership

- [x] Root: codec/privacy audit under candidates/codec-privacy/. Reproduce the
  coincidence statistic, compare with the exact Bayes classifier, distinguish
  frozen retrieval from fresh response simulation, inspect actual stored code,
  and compare DTE/honey-encryption and probabilistic-data-structure privacy work.
- [x] Hash auditor: candidates/hash-construction/ only. Test existing finite
  construction/optimality claims and closest prior art; no new data structure.
- [x] Readout auditor: candidates/quantum-readout/ only. Reproduce existing
  derived-bit predictions, check conditional semantics and nearest forward
  noisy-circuit/readout predecessors; no hardware campaign.
- [x] Root: integrate verified bibliography, claim ledger, effort estimates,
  reproducibility commands, and go/no-go assessment.
- [x] Independent reviewer: challenge the strongest candidate or the decisive
  rejection evidence. Address material findings and run appropriate checks.
- [x] If and only if a finalist passes: complete essential work, focused LaTeX
  manuscript, and current official venue assessment. Otherwise close no-go.

No finalist passed. The conditional manuscript/venue stage was therefore
closed as not warranted, not left as unfinished work.

## Review focus and completion gate

Exact truth versus random construction versus frozen observations; equal class
priors versus arbitrary priors; public versus secret codecs; returned values
versus full stored representations; rejected/invalid codewords; source reuse;
claims of Bayes optimality; asymptotic versus finite claims; numerical evidence
versus proofs; empirical application value versus relabeling established results.

Tests must target independent oracles/counterexamples rather than duplicate the
implementation. Record source hashes and commands. Do not expand to a fourth
candidate, commit unrelated changes, or seek a venue to compensate for absent
contribution. Journal review time and PhD eligibility are not promised.
