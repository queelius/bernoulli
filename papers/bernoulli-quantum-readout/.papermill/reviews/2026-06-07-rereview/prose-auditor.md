# Prose auditor (re-review)

Date: 2026-06-07 (re-review of revision commit 6f136b7)
Scope: read the new passages (Subsection 4.4, the M1 sign-rule paragraph, the
self-contained unification paragraph, the rewritten rem:t1) for clarity and
notation regressions, and check the prior prose minors/suggestions.

## New passages: clarity

- Subsection 4.4 ("The asymmetric case: a number the symmetric rule cannot
  give"): clear and well-motivated. The opening sentence honestly states why
  Table 1 alone is insufficient ("every value in it is reproducible from the
  single-rate identity we attribute to prior art ... We now make it appear"). The
  caption and the closing paragraph are consistent with the table values. The
  framing "wrong on both sides at once" is vivid and accurate. Good.
- The M1 sign-rule passage (sec:scope item 2) is dense but correct and readable.
  The chain "parity flips only under an odd number of bit flips: positively
  correlated misreads make coincident flips more likely and so push the parity
  error below the independent value, while negatively correlated misreads push it
  above" is a clean explanation of a subtle point. The "two-sided anchor, not a
  worst case" phrase lands well.
- The self-contained unification paragraph (sec:related) reads cleanly and is
  genuinely self-contained: a reader can reconstruct the Bernoulli error model
  from the one sentence given, then see the Bloom-filter corner and the readout
  interior point as two instances. No dangling reference to unread companion
  papers for the core claim.
- rem:t1 now carries the concrete 84%/62% datapoint, which makes the physics
  motivation more vivid without adding length problems.

## Prior prose minors / suggestions: status

- m4 (rate-subscript overload, index vs connective): partially addressed by
  context, not by an explicit one-line note. The head of sec:calculus (line ~290)
  adds "It is convenient to also track the conditional flip probabilities," which
  helps, but there is still no single sentence stating that subscripts are either
  qubit indices or connective tags. Minor, optional. PARTIAL.
- m5 (q / r / q_i play three roles): sec:worked still uses q for the symmetric
  per-measurement rate, cor:parity-asym uses r_i, thm:parity uses q_i. The new
  Subsection 4.4 helps by writing r_i = eps_i / omega_i explicitly and using
  q = rbar = 0.07 for the symmetrized baseline, which implicitly bridges q and r.
  No explicit one-line bridge was added. Minor, optional. PARTIAL.
- m6 (long em-dash-chained sentences): the abstract and several closing sentences
  remain long. The revision did not shorten them; the new Subsection 4.4 also
  contains a couple of long sentences (e.g. the closing "This is the bookkeeping
  ... no 2^4 x 2^4 assignment matrix in sight"). Stylistic, not a defect. NOT
  ADDRESSED (optional).
- P4 (abstract names four neighbors, sec:related delivers five): RESOLVED. The
  abstract now names exactly five neighbors (matrix-inversion mitigation,
  effectus theory, noisy-Boolean-formula identities, asymmetric quantum
  hypothesis testing, relaxation-physics), matching paragraphs (a)-(e).
- P5 ("n times per-measurement error" folklore aired four times): NOT ADDRESSED.
  The folklore still appears in the abstract, intro, sec:worked caption, and
  conclusion (four times). Stylistic, optional; the repetition is arguably
  rhetorical reinforcement of the paper's main corrective. Carrying forward.
- P6 (long title): NOT ADDRESSED. Title unchanged. Optional.

## New prose findings introduced by the revision

None that rise to a finding. The new prose is clear, accurate, and consistent
with the math and captions. The only stylistic carryover is sentence length,
which is a pre-existing trait, not a regression.

## Notation consistency check

- The new Table 2 uses (eps, omega) per qubit and r_i for the conditioned flip
  rate, consistent with cor:parity-asym. No new symbol was introduced without
  definition. The symmetrized baseline q = rbar = 0.07 is defined in the prose
  before the table. Consistent.
- tab:syndrome-asym and sec:worked-asym labels resolve; cleveref renders them as
  "Table 2" and "Subsection 4.4" correctly. No broken cross-reference.

## Verdict

The new passages are well-written and accurate. P4 resolved. The remaining prose
items (m4, m5, m6, P5, P6) are optional stylistic carryovers, unchanged by the
revision, none blocking. No new prose issue introduced.
