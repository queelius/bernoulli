# Candidate 1: limited-verification deduplication

**No-go for a low-effort conventional paper from this screen.** Limited checks
can recover useful documents, and a workload-specific frequency rule can win.
The surviving guarantees are elementary sampling facts, while generic gains
largely disappear against competent distinct sampling and spending metadata
RAM on the filter itself. This is not a theorem that useful budgeted adaptive
deduplication is impossible.

## Round 1: does repeated-error correction create a new allocation mechanism?

Potential contribution: an error-aware verification rule that controls permanent
document omissions cheaply under frozen/repeated query semantics. The decisive
question was whether correcting a discovered false positive provides an effect
beyond ordinary successful processing and known sampling identities.

**Exact ordinary-Bloom invariant.** Fix the initial bitmap, hash locations, and
arrival stream. Assume every negative arrival is successfully processed and
inserted; on a positive arrival a policy may suppress it or verify/process it.
For every policy the bitmap after every arrival is the same. Proof by induction:
the current verdict is the same; a negative arrival is inserted by all policies;
inserting a positive arrival sets only bits that were already set. This says
nothing about auxiliary insertion counters, nominal FPR estimates, exact logs,
adaptive fingerprints, deletion, or rebuilds.

Therefore a key first suppressed by a false positive remains positive until
verified, but once verified and processed it is a true member. A negative
exception cache for that key is stale. A verified-*positive* cache can avoid
repeated exact checks, which is ordinary caching. The proof is short, with no
demonstrated standalone novelty. Exhaustive enumeration covers **18,724**
initial-bitmap/stream/audit-policy combinations, and stored-filter tests include
repeated colliding keys under four seeds.

**Exact conditional omission law.** For a key known to be a persistent false
positive before its first successful processing, with f arrivals and independent
per-arrival audit probability q, final omission probability is (1-q)^f. At q=.1,
it is .9 for a singleton and approximately .00002656 at f=100. This is a
truncated geometric experiment, not a new Bernoulli result. A global hard audit
cap can make the coins dependent; the formula must not be applied unchanged to
the finite-budget batch experiment.

**Strong baseline.** Conditional on a fixed pool of K positive distinct IDs,
U of which remain unprocessed, a uniform sample of B distinct IDs recovers
B U/K on average (B<=K). Each ID has inclusion probability B/K, so linearity
of expectation proves the statement without independent novelty labels. Under
a uniformly hidden U-subset and no predictive information, sequentially
choosing distinct IDs cannot improve that expectation; symmetry gives a
minimax lower bound on final omissions. Distinct sampling and its advantage
over occurrence sampling are established, including [Gibbons 2001](https://www.vldb.org/conf/2001/P541.pdf).

For known independent novelty priors p_i and unit rewards/costs, choosing the
B largest p_i is optimal: observed labels do not update the other priors, and
an exchange argument sorts expected rewards. That is ordinary selection, not
new theory. Frequency is not a novelty probability: with one check, frequencies
(100,1) and priors (.001,.99), preferring the frequent ID has 990 times less
expected distinct recovery. The exact four-profile counterexample is tested.

Outcome: the generic theoretical opportunity failed. One second round was
justified to determine whether a useful empirical systems advantage survived.

## Round 2: does targeted auditing survive meaningful cost baselines?

The [application and cost model](README.md) uses actual stored Bloom bitmaps and
SQLite processed logs. Three controlled streams put novelty in the frequent
items, the rare items, or both. Eight independently initialized construction
seeds and separate sampling seeds give **168** pipeline runs. This is a small
adversarial screen, not a representative corpus benchmark or a hypothesis test
of production performance.

The exact numbers and timing breakdowns are in [results.json](results.json).
The stable qualitative results are:

- More checks help, but uniform occurrence checking wastes budget on repeated
  IDs. Caching the same sampled IDs preserves recovery and reduces exact calls;
  it does not create a new recovery guarantee.
- Uniform distinct sampling is the competent allocation baseline when the
  objective is distinct retained content. High-frequency sampling recovers all
  omitted documents in the deliberately hot-novel workload; low-frequency
  sampling does so in the deliberately cold-novel workload. Their ordering
  reverses with the workload. No generic new predictor was discovered.
- The no-audit means are 2.625, 30.875, and 31 omitted distinct IDs for hot-novel,
  cold-novel, and mixed streams. Using only 2560 bytes of additional bitmap RAM
  reduces them to **0, 1, and .5**, with no exact membership checks.
- That larger filter does **not** dominate every policy: low-frequency auditing
  reaches zero cold-novel omissions at 64 checks, while the larger filter leaves
  one on average. The remaining gain depends on deliberately supplied
  novelty-frequency structure; it is not evidence of a new general method.

The original authoritative log alone occupies tens of kilobytes; it is counted
for every method. Packed frequency metadata is 32 bytes per candidate ID and
can greatly exceed the filter payload. The larger-filter comparison uses only
packed bottom-k record bytes, not the substantially larger Python object
overhead. It can nevertheless be slower in this prototype because it performs
more hash/bit probes; we do not claim a runtime dominance.

**Published adaptive-filter qualification.** [Mo et al. 2026](https://doi.org/10.1145/3786324)
explicitly compare adaptive filters with false-positive caching under skew.
Their oracle reports false positives; the [2021 predecessor](https://par.nsf.gov/servlets/purl/10298693)
also explains how fingerprint extension can correct other keys and how a
colliding stored key is supplied. Our ordinary-Bloom invariant does not rule
out those collateral improvements. Implementing a faithful limited-feedback
version with all auxiliary state would be a different unresolved experiment,
not a result obtained here. The oracle comparator in this screen is expressly
limited to the fixed observed candidate pool.

Outcome: no incremental paper candidate survived the baseline/cost gate.
There is no third round and no expansion into a larger planner or framework.

## Prior art and classification

- **Established mathematics:** fixed-bitmap insertion idempotence, geometric
  first-check law, finite-population sample expectation, independent-prior
  ranking, ordinary cached lookup suppression.
- **Correct semantics/exposition:** a suppressed occurrence is not a processed
  document; verified false positives become members; duplicate-arrival counts
  and final distinct omissions are different objectives.
- **Established neighboring methods:** stable Bloom stream deduplication;
  distinct sampling; adaptive membership filters and their backing oracle;
  label-efficient learning where outcomes cost queries. We do not claim the
  label-efficient theorem directly solves mutable processed-set deduplication.
- **Potential research not established here:** a real corpus predictor whose
  incremental benefit survives same-RAM larger filters, or an adaptive
  fingerprint repair with valuable collateral corrections under a restricted
  verification budget and fully counted collision-witness access.

Dolma's official documentation establishes that approximate filtering can
remove documents in a real pipeline. Current LSHBloom research independently
studies probabilistic text deduplication and storage/quality tradeoffs. Neither
source establishes the exact sparse-auditing policy proposed in this screen;
the no-go relies on the elementary reduction and measured baselines, not a
false claim that one predecessor already contains the entire problem.

## Remaining effort and limits

Writing this up as an expository note would need roughly half to one author
day; that does not create a conventional research contribution. A credible
application study would need real document traces, validation of a usable
novelty signal, realistic authoritative-index and processing costs, and a fair
adaptive-filter implementation or new analysis. Engineering might take several
days, but the existence of an incremental result is still uncertain. We cannot
defensibly classify a finished conventional paper as a one-week finishing task.

No manuscript or venue recommendation is warranted. The useful assets are the
explicit model, counterexamples, two short exact lemmas, and reproducible
cost-aware baseline. The finite tests corroborate proofs and catch semantic
errors; simulations are not presented as proofs.

Validation: **25 tests pass**, including exact finite enumeration, repeated
collision semantics, source/authoritative-storage accounting, caching, and the
SQLite/filter pipeline. Combined driver-plus-test statement/branch coverage is
99%; the only uncovered line is the defensive assertion that would report a
counterexample to the proved bitmap invariant. Ruff and strict mypy pass. The
last driver run was uninstrumented for the recorded prototype timings; see
[verification.json](verification.json) for hashes and exact coverage totals.
