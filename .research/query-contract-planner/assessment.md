# Publication decision: do not submit this candidate as original research

**Completed 2026-10-14.** The investigation found a useful finite contract and a
working implementation, but did not establish an original publication
contribution. Integrity constraints materially improve a weak membership-filter
budget. Nearly all of that improvement survives an elementary constraint-aware
union bound; familiar retrieval representations capture the remaining practical
opportunity. The tested complete application gains little storage while paying
substantial query cost compared with exact IDs.

This is a scoped negative result, not an impossibility theorem for every
constraint, query, allocation, or application. The previous conclusions remain:
generic dependence/lineage machinery was not novel, and the earlier cycle
experiment saved only 16 bytes / 0.425% through sharper budgeting.

## Question tested and information available

The final class is

\[
Q(u,v,C)=\exists z\in C:\ R(u,z)\land R(v,z),\qquad u\ne v.
\]

Each exact row has one value. A caller supplies two exact row keys and a
candidate set C from a public finite catalog. The application compares content
identities in Git file manifests: a key is (snapshot,path), and the value is the
blob object identifier. Equality is equality of those identifiers; the model
does not assert that underlying file hashes are collision-free.

Two pinned snapshots provide 1840 rows and 904 distinct values. A pool of 276
LaTeX-file content identifiers supplies 32 varying candidate sets of 64 values.
Each catalog is tested with two, one, or zero singly-false witnesses, equal
values outside C, and a true intersection. Every query template repeats each
membership operand three times; the implementation resolves source identity
and probes its frozen source once per witness. A self-join needs a different
contract and is rejected by this interface. Duplicate candidate values are
canonicalized before capacity selection. These are stratified generated requests
on real repository data, not a production query trace.

The constructor sees exact rows, the declared domain, and the maximum candidate
count. The query path receives only the frozen representation, exact key
directory, domain information, and query parameters. It has no exact-value
oracle unless the selected representation is explicitly the exact baseline.
It stores no per-C answer or presence cache. The theorem covers any fixed C
within the declared capacity, selected independently of the construction seed;
the measurements sample 32 such sets, not all of them.

Functionality constrains the exact database. Approximate membership answers
can accept several candidate values for a row; we do not claim that the noisy
membership relation itself preserves the functional dependency. The code covers
total rows. Presence metadata for partial rows is a theoretical extension only.

## What was proved, and why it is not a new calculus

For independent distinct absent-tuple errors of rate p and K>=2 candidates, the
sharp false-positive envelope is

\[
1-(1-p)^2(1-p^2)^{K-2}.
\]

Only two witnesses can have one absent atom. Every other false witness needs
two errors. The ordinary unrestricted certificate Kp can therefore be very
pessimistic. But the constraint-aware union bound

\[
2p+(K-2)p^2
\]

captures the important improvement. At query target epsilon, the extra saving
from the sharp product is at most

\[
\log_2\!\left(\frac{-\log(1-\epsilon)}{\epsilon}\right)
\]

continuous fingerprint bits per row: **0.03684214 bits at epsilon=.05**. This
comparison concerns the common-rate logarithmic cost proxy; integer widths can
cross a threshold, and it is not a theorem for every heterogeneous allocator.

The finite alternative stores one row-specific fingerprint, using a random
degree-at-most-three polynomial over P=2^61-1 with four uniform coefficients.
The 32-byte coefficient seed and packed fingerprints are real stored data.
Reducing outputs modulo M=2^b gives exact pair-collision probability

\[
q=\frac1M+\frac{M-1}{MP^2}.
\]

Four distinct tuple inputs give two independent collisions within a false
witness. The union bound gives 2q+(K-2)q² without independence between
witnesses. True matches always accept, so FN=0. Injective tuple encoding and
distinct canonical rows are necessary. This is an unconditional fixed-query
guarantee over uniform coefficients, not a guarantee after seed disclosure,
adaptive choices, or arbitrary construction rejection.

These are elementary uses of cardinality constraints, read-once lineage,
limited-independent hashing, and the union bound. The broader multiway
cardinality theorem and heterogeneous dynamic program are recorded in
[theory.md](theory.md), with proofs and counterexamples, without an originality
claim. The exact binary-linear alternative is precisely the established
Crapo–Rota Critical Theorem.

The [primary literature audit](literature.md) and [24-entry bibliography](references.bib)
cover FD-aware probabilistic planning (SPROUT and related work), constrained
probability inference, Monkey and Bloom-collection allocation, retrieval,
Ribbon/BuRR, finite Bloom analysis, and current filter-aware join planning.
The final approximate-answer semantics differ from filters used only to prune
an ultimately exact join. That distinction alone does not supply a new theorem
or an effective new algorithm.

## Complete application comparison

Manifest results below use a 5% query target and 64 separately seeded builds.
Query latency is for the boundary profile with two singly-false witnesses;
other profiles are retained in the raw results. The latency column includes
the common 9.07 μs per-query candidate-validation cost. Timings are prototype
measurements in Python, with a ctypes/C binary-fuse baseline; they are not
optimized native throughput comparisons. The methods satisfy the same upper
target under their respective models, not identical empirical error rates.

| Representation / allocation | Payload bytes | Total bytes | Build ms | Query + preparation μs |
|---|---:|---:|---:|---:|
| Bloom, ordinary source-deduplicated union | 3472 | 173562 | 89.61 | 258.19 |
| Bloom, constraint-aware union | 2008 | 172098 | 49.48 | 240.31 |
| Bloom, sharp constrained product | 2002 | 172092 | 42.93 | 238.33 |
| Finite row fingerprints, ordinary union | 2587 | 172677 | 6.85 | 102.99 |
| Finite row fingerprints, constrained union | 1437 | 171527 | 5.62 | 97.06 |
| Binary fuse, constrained nominal model | 2604 | 172694 | 2.47 | 68.35 |
| Exact packed value IDs | 2317 | 172407 | 2.39 | 12.17 |

All totals include 170090 common bytes: 147183 for the exact row directory,
21700 for the content catalog, 1108 for the candidate-pool catalog, and 99 for
schema/framing. Query parameter inputs add 66144 bytes across the 160 requests;
they are transient input, not hidden representation storage. Extraction and
parameter generation took 33.94 ms; allocation took 1.89 ms. Candidate enumeration
is inside membership-query timing, with a separate empty-loop control retained.

The effects separate cleanly:

- Canonical source identity is held fixed across all physical methods. Its
  benefit is not counted as a new constraint-calculus gain.
- The exact functional constraint reduces ordinary Bloom payload by 1464 bytes.
  The competent constrained union bound already captures this.
- Replacing that union bound with the sharp product saves just **6 bytes**:
  0.299% of representation storage and **0.00349% overall**.
- Finite row fingerprints save **880 bytes / 0.5104% overall** against exact IDs,
  while taking about **8 times** the measured query cost including preparation.
  Excluding already-shared directory/catalog costs, their payload saving is
  **37.98%**. That alternative accounting could matter in another deployment;
  it does not disappear merely because this application's total saving is small.
- Three controlled workloads confirm that effects depend on domain and query
  sizes. Exact IDs dominate on the smallest case; the largest control gives
  about 2.05% total-byte saving for finite fingerprints with much slower queries.

See [summary.csv](summary.csv), [findings.json](findings.json), and the
[comparison figure](comparison.png). The first fixed-C experiment is preserved
under attempts/001-fixed-c/. It exposed a missing competent baseline: for one
fixed C, exact per-row membership-in-C flags plus shared value fingerprints can
avoid candidate scans. The final experiment varies C; it does not turn that
initial failed design into positive evidence.

## Guarantee validity, inference, and limitations

The three probabilistic implementations have different guarantees:

- Bloom acceptance is checked with exact rational occupancies against the
  query contract, conditional on inserted-key history under ideal independent
  random functions. Concrete BLAKE2b independence is not proved.
- Finite fingerprints have the stated finite-family theorem under uniform
  coefficients. Reproducible runs use seeded pseudorandom sampling; simulations
  do not prove its ideal distribution. No product identity is claimed for the
  four-wise family across all candidates.
- Binary fuse uses a pinned current implementation and nominal 2^-b rates as a
  practical baseline. Its records have no finite-family certificate. It is not
  promoted to an equal unconditional guarantee by labeling it a modern filter.

Exact small joint calculations and exhaustive finite constructions check the
formulas. For this normalized query, established lineage evaluation factorizes
exactly as a read-once product; a separate general probabilistic-database
deployment cannot improve that probability. The baseline is that factorized
method, not a claimed new WMC algorithm. Independently treating three syntactic
copies of each source would predict 0.00000763 in a K=64, p=1/64 false boundary
profile; the correct independent-distinct-source probability is 0.04556456.

The final experiment contains 2304 builds and 368640 primary queries, plus repeat
checks. All recorded FN and repeat-mismatch counts are zero. All exact
finite/ideal model contracts meet the 5% target. This is **not** an empirical
certification of the concrete hashes: one synthetic constrained-Bloom estimate
is 5.615%, and its uncertainty includes 5%. Confidence intervals use independent
construction means, not individual within-build queries. Numerically inverted
bounded-mean Chernoff intervals remain wide; normal SE bands are descriptive
only. Zero observed errors are not assigned zero uncertainty.

Full-run peak RSS was 36684 KiB and elapsed time 117.78 s. Per-method Python retained
and peak allocation measurements are saved. They exclude native C allocations;
the pinned fuse source's allocation formula and byte format are documented in
[vendor/README.md](vendor/README.md). Serialized size is the primary complete
storage measure. No universal memory or throughput scaling claim follows.

## Verification, decision, and best remaining direction

Independent critical review found genuine missing query-boundary checks, which
were reproduced and fixed. **610 relevant tests pass** (70 new, 540 previous
relations tests). Current code coverage is 92.95% of statements, 83.97% of
branches, 90.56% combined. CLI and defensive failure paths are the main gaps;
they are documented in [review.md](review.md). Every recorded payload was
rebuilt from its seed and exact bound, and 5760 representative query outcomes
were reproduced. See [verification.json](verification.json). The exact measured
driver source is archived, so later edge-case fixes do not obscure provenance.

Do not update the relations manuscript to claim a novel planner or new theorem
from this run, and do not choose a submission venue yet. The artifacts are
useful as correctness groundwork and an advisor-facing opportunity audit.
Neither more synthetic points nor a broader compiler interface would fix the
current novelty deficit.

The best remaining direction is **an application-led evaluation of finite
contracts where row IDs and catalog infrastructure are already available and
approximate final answers have a concrete storage benefit**. First identify
such an external workload and its actual constraint/query semantics; compare
exact packed values, retrieval, and modern filters using native implementations.
Reopen a publication candidate only if the finite guarantee changes an
operational decision and the gain survives these baselines. This is a proposed
next gate, not a positive result or a newly activated goal. A demand for adaptive
or dynamically updated guarantees would also require a fresh novelty audit
against the substantial adaptive-AMQ literature.

No manuscript, package source, or earlier research run was changed by this new
goal. Nothing was submitted, published, or sent externally.
