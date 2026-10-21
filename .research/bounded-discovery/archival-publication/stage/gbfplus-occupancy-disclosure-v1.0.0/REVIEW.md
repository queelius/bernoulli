# Review scope and evidence

## Scientific record

The two propositions have ordinary written proofs. They have not been checked
in a proof assistant. Finite enumerations and independently derived executable
checks corroborate the specified implementation; they do not replace proofs
or validate unimplemented cryptographic and ledger mechanisms.

Successive internal AI-agent reviews on 2026-10-15 covered source fidelity,
mathematical validity, reproducibility, and readability. A final round used
three agents with fresh contexts and separate assignments, followed by targeted
checks of corrections. This is independence of agent context and checking
approach, not independence of human reviewers or external peer review.

## Material corrections before author approval

1. **Masking claim narrowed.** Uniform masks independent of an identifier do
   not suffice for full-view security if the prefix is correlated with the mask.
   The example `P=M` reveals `N` from `P || (N XOR M)` despite uniform suffix
   marginals. The manuscript now restricts the statistic and states joint
   independence from identifiers and prefixes. The oracle reconstructs this
   counterexample.
2. **Identity inference qualified.** The result does not *in general* reveal
   the publisher; in a registry of only two domains, the known neighbor can
   determine the other endpoint. The two-neighbor comparison requires eligible
   alternatives distinct from the publisher.
3. **Predecessor credit made explicit.** Dong, Chen and Wen (2013), Section 4.1,
   already distinguish value disclosure from membership acceptance. The
   contribution is GBFPlus's exposed selector and allowed partial-batch release,
   not that general distinction.
4. **Access and configuration clarified.** Public means visible to a reader of
   the permissioned ledger. The widths and share count are public parameters.
5. **Runtime false-success prevented.** The portable runner rejects Python
   optimization before it can omit assertion-contained experiment steps,
   including when an optimized bytecode file is executed normally. This was an
   artifact correctness repair, not a new scientific result.
6. **Exposition improved.** The singleton proof and worked example precede the
   qualified aggregate extension. Verification cases and supplement entry points
   are explicit. Every page was inspected after the review revisions.

No counterexample to either proposition under its stated premises was found.
That statement is the result of a bounded internal audit, not proof of novelty
or a claim that every possible objection has been excluded.

## Human approval and this release

Alexander Richard Towell reviewed and approved the five-page manuscript on
2026-10-18 and authorized archival publication on 2026-10-20. This archive
preserves the approved abstract, body, bibliography, mathematical module,
experiment functions, tests and expected data byte-for-byte. Only publication
metadata, availability, review-status and license text changed. Source hashes
and the approved PDF hashes are in `SOURCE-PINS.json`.

The release reruns the 17 unit/integration tests, deterministic reproduction,
coverage, Ruff, strict mypy, and the independent oracle from the staged packet.
Actual results and tool versions are in `verification/`. Normal coverage
targets 121 statements and 48 branches in the two runtime modules. The
compile-time optimization guard is excluded from that denominator but tested
separately through rejected subprocess executions.

The independent oracle covers 771,787 updates in its stated small state spaces
and reconstructs all 64 recorded full-word arrays. It checks atomic failure,
immutable occupied words, persistence of every row equation, exact occupancy
unions, certificate output, and frozen reads. Its additional mask/prefix example
is a negative control on an overbroad defense claim. None of these counts
measures operational attack prevalence.

## Remaining limitations

The source specification's honest-history, visibility and allowed-release
premises are necessary and are itemized in `supplement/source-premises.md`.
An implementation that forbids singleton release or hides/masks the relevant
payload needs a separate analysis. No deployment was attacked or measured.
The note does not break the distinct identifier-privacy game, recover a general
batch's individual identifiers, or supply a complete secure repair.

The literature check was bounded. Elementary sharing algebra and defenses are
known. The protocol-specific observation is a potential contribution; an
unindexed predecessor or later protocol correction may change that judgment.
Journal suitability, acceptance, and doctoral credit are not established.

OpenAI Codex assisted the derivations, implementation, source checking, writing,
reviews and packaging. A complete historical model-version record is not
available. This release has author approval, internal AI review, written
proofs and finite computational evidence; it has no external human peer review
or formal proof verification.
