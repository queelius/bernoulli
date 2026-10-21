# Independent critical review and resolution

Date: 2026-10-14. Reviewer: independent `publication_review` agent, given scoped
artifact paths and the author's selection criteria, without the root's full
conversation history. Read-only review; no reviewer edits. This is an internal
critical audit, not external peer review or publication acceptance.

## Recommendation

The reviewer supports a **bounded no-go**. A short explanatory paper could be
assembled within a week, but the current evidence does not establish sufficient
incremental conventional-research value. The reviewer explicitly challenged the
root's initial emphasis on practical guarantees by examining the additional
graded, realizability, cogirth and randomized-full-support results. It found
useful synthesis and possible application-specific novelty, not an already
demonstrated substantive contribution needing only editorial completion.

The decision must leave room for a nontrivial theoretical advance as well as
a practical result. It must not claim that every surviving statement is known,
that all of the companion is false, or that no future publication is possible.

## Findings and resolution

1. **Missing OKVS predecessor.** Add Bienstock et al., USENIX Security 2023,
   Definition 4 and Theorem 1. Random decoding of non-input keys is explicitly
   studied. Its uniform-input-value assumption prevents claiming it subsumes
   arbitrary-value codec/span laws. **Addressed:** added to the codec assessment,
   bibliography and ledger; the root checked the official PDF definition.
2. **Do not equate two different span results.** Ribbon Lemma 5.4 uses the span
   of input-key coefficient rows with random free variables. The companion uses
   the span of stored value vectors with zero free variables. **Retained:** the
   audit states this distinction and makes no equivalence claim.
3. **Skewed theorem needs completeness.** A default that absorbs Kraft slack is
   a union of cylinders. For lengths (1,3), M=3, its full-span mass is 7/8,
   not the displayed 1/2. **Addressed:** documented as a local scope defect.
   The later full-support theorem already assumes completeness and survives.
4. **E1 statistic is non-identifying.** (.5,.5,0,0) and (.49,.51,0,0) both have
   TV .5 from uniform. Below-threshold TV bars do not validate uniformity on the
   hit classes. **Addressed:** assessment and ledger separate the support
   obstruction from the unverified per-class law.
5. **Joint privacy remains unproved.** Equal M1 marginals do not imply equal
   adaptive transcripts. Similar average cross-profile and rebuild TV distances
   also do not prove equal distributions of realized laws. For example, profile
   0 chooses Bernoulli(1/2+epsilon) or Bernoulli(1/2-epsilon) with equal
   probability; profile 1 always chooses Bernoulli(1/2). Mean cross-profile TV
   and profile 0's mean rebuild TV both equal epsilon, while many independent
   observations identify which realized-law family was chosen. **Addressed:**
   this counterexample and the remaining proof obligation are recorded here;
   the audit does not promote the marginal triangle bound to joint security.
6. **Counterexample scope.** A seed-aware Python row alias is not a refutation
   of a fixed-query average guarantee or an attack on the companion's particular
   C++ builder. Fresh responses versus frozen responses are different models,
   not an automatic attack on independent releases. **Retained:** both limits
   are explicit in assessment and machine-readable results.

The strongest theoretical escape route was assessed rather than discarded by
analogy. The balanced threshold is rank-nullity. The realizability statement
reexpresses the subspace law via relevant prefix projections; it does not solve
the remaining hit-geometry problem. Cogirth transports its deletion definition.
For complete codecs with full support, each hit mass is at least its Kraft
share; both distributions sum to one, so every mass equals its share for every
representative selection. This short proof supports correctness but weakens
the claimed technical depth. No identical-published-theorem assertion is made.

## Reviewer verification

- All seven codec audit tests passed.
- `run_audit.py`, with only its output write intercepted, reproduced the saved
  `results.json` exactly.
- The existing companion full-support verification passed; the root separately
  reran it and saved `candidates/codec-privacy/companion-full-support.txt`.
- The reviewer independently checked the Kraft-slack, E1-statistic and
  rebuild-distance counterexamples.
- The author-corrected submission status had no role in the recommendation.

The two other candidates have separate independent investigator reports and
reproductions. This review's deepest proof and novelty scrutiny concerned the
strongest remaining candidate, codec/privacy; it is not represented as a second
full literature audit of every candidate.
