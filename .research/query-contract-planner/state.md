# Query-contract planner research state

Started 2026-10-13; completed 2026-10-14. **Status: complete.**
**Decision: no original-research submission warranted by this candidate.**

## Objective and inherited evidence

Determine whether integrity constraints and shared-source information improve
the complete storage–accuracy–runtime tradeoff of a useful approximate relational
query class enough to support an original publication. Both previous research
runs are preserved. Their generic lineage/calculus claims lacked novelty; the
earlier cycle experiment saved only 16 bytes / 0.425% through sharper budgeting.

## Final scope

Parameterized positive queries Q(u,v,C) = exists z in C: R(u,z) and R(v,z),
with distinct canonical rows and exactly one exact value per row. The application
compares content IDs in versioned Git manifests. The constructor sees the exact
database, domain, and candidate capacity. Queries see the frozen representation,
exact row directory, public catalog, and parameters; approximate execution has
no exact-value oracle. Constraints apply to the exact relation, not necessarily
to the noisy membership answers.

The fixed database and query are independent of construction randomness. Atoms
and candidate values are canonicalized; repeated execution reuses the same
frozen source. Adaptive conditioning, partial-row storage, and dynamic updates
are outside the implementation. All metadata and candidate preparation costs
are recorded. Application requests are stratified generated cases on real data,
not a production trace.

## Findings and decisive evidence

- The independent-source sharp envelope is 1-(1-p)^2(1-p²)^(K-2) for K>=2.
  The elementary constrained union bound 2p+(K-2)p² captures the main benefit.
  The sharp rule saves at most 0.03684214 continuous fingerprint bits per row
  at a 5% target under the common-rate logarithmic cost model.
- A finite four-wise polynomial row-fingerprint construction gives a sound
  union-bound contract without cross-witness independence. Seed cost is counted.
  Limited independence and the binary-linear Critical Theorem are established
  prior art, not contributions of this project.
- The manifest benchmark has 1840 rows, 904 distinct values, and varying C of
  size 64. A sharp Bloom product saves 6 bytes over the competent constrained
  union baseline (0.00349% of total storage). Finite row fingerprints save
  880 bytes against exact IDs (0.5104% total; 37.98% of payload) while taking
  about 8 times the prototype query latency including preparation.
- Full-domain equality is defeated by ordinary value retrieval. The fixed-C
  pilot omitted a simple per-row presence-flag baseline and is retained as a
  failed approach under attempts/001-fixed-c/. Varying C corrects that scope
  issue but does not establish novelty or a compelling application tradeoff.

## Completed artifacts and validation

- [Assessment](assessment.md), [claim ledger](claims.md), [theory](theory.md),
  [literature audit](literature.md), and 24-entry [bibliography](references.bib).
- Four workloads × nine methods × 64 builds = 2304 stored constructions;
  368640 primary queries plus repeats. No recorded false negatives or repeat
  mismatches. One synthetic empirical FP rate exceeds 5% with uncertainty
  spanning the target; finite, ideal, and nominal guarantees remain separate.
- 70 new tests plus 540 relevant relations regressions pass. New-code coverage:
  92.95% statements, 83.97% branches, 90.56% combined. Independent review found
  and helped resolve alias, domain, capacity, optional-method, and uncertainty
  defects; no material scoped-benchmark issue remains. See [review.md](review.md).
- All 2304 payloads, recorded exact bounds, and retry counts rebuilt;
  5760 representative queries reproduced. See [verification.json](verification.json).
  Exact measured source, seeds, inputs, charts, and reproduction commands remain
  available from [README.md](README.md).

## Next gate, not an active task

Find an external application where row/catalog infrastructure is already paid
for and approximate final answers have a concrete storage benefit. Compare exact
packed values, retrieval, and modern filters with native implementations. Reopen
a publication candidate only if the finite guarantee changes an operational
decision and the gain survives those baselines. More synthetic points or a
general planner interface do not resolve the current novelty deficit.

No manuscript, package source, or earlier research run was changed by this new
goal. Unrelated working-tree edits are preserved. Nothing was submitted,
published, or sent externally. No further experiment is running.
