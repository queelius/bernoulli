# Limited-verification deduplication: bounded screen

Completed 2026-10-14. Decision: **no finalist from the two tested rounds**.
See [assessment](assessment.md), [results](results.json), and
[verified references](references.json). No canonical source or paper changed.

## Reproduce

From this directory:

```bash
../../../bernoulli-py/.venv/bin/python probe.py > experiment-output.json
../../../bernoulli-py/.venv/bin/python -m coverage run --branch --source=probe probe.py > experiment-output.json
../../../bernoulli-py/.venv/bin/python -m pytest test_probe.py --cov=probe --cov-branch --cov-append --cov-report=term-missing --cov-report=json:coverage.json
../../../bernoulli-py/.venv/bin/ruff check probe.py test_probe.py
../../../bernoulli-py/.venv/bin/mypy --strict probe.py
```

The driver writes `results.json` with all 168 pipeline rows and 21 summaries.
Run the first command once more after coverage if comparing recorded runtimes:
coverage instrumentation changes timings. Results and seed lists are otherwise
deterministic. Each run uses temporary local SQLite databases, then removes
them. All stored IDs are 16-byte unique identifiers in the finite model.

## Operational semantics

The application is batch ingestion of documents into a retained corpus. The
source corpus is already archived and can be revisited by an 8-byte ordinal.
This is motivated by Dolma's documented Bloom tagging and subsequent mixing,
but **is not a reproduction or modification of Dolma**. Our addition is an
authoritative SQLite table of successfully retained IDs, which costs storage
and writes even if no verification is performed. A real implementation using
content digests would also need to handle digest collisions; finite IDs here
are exact, not a proof of collision-free content hashing.

First pass: a Bloom-negative ID is processed, written to the exact log, and
inserted into the filter. A Bloom-positive arrival is provisionally suppressed
and offered to a sampler. It is **not** added to the exact log merely because it
arrived. Before final output, at most 64 selected occurrences/IDs are checked in
the exact log. An absent ID is processed and inserted immediately. Processing
succeeds, execution is sequential, no deletions occur, and there is no concurrent
writer. Deferred verification is allowed because the source is retained.

Metrics distinguish final omitted distinct documents from source occurrences
of those omitted documents. They do not count all initially suppressed copies
as permanent losses. Separate sequential tests show the transition from novel
false positive to true duplicate after an audit processes its first copy.

## Representations and costs

- `KeyedBloom` stores an actual `bytearray`; SHAKE256 of a construction seed and
  ID supplies locations. Construction and sampling PRNG streams have separate
  initialization seeds, recorded in the output. These are empirical seeded
  constructions, not a finite random-oracle proof or a cryptographic guarantee.
- The capacity is the configured full distinct workload size, known in this
  controlled experiment. It is an optimistic capacity forecast, not a new
  estimator. Nominal target FPR is .05; no measured number is replaced by that
  approximation. The larger-filter baseline uses at most 16 hash locations.
- The exact log is an actual `WITHOUT ROWID` SQLite table, measured by page
  count times page size. Its configured page cache is another 64 KiB for every
  method. Counts include exact checks and a 17-byte request/boolean-response
  payload lower bound; network framing and remote latency are not measured.
- Candidate generation occurs in the first pass. Reservoir sampling retains
  ID/offset records. Bottom-k distinct sampling also retains 128-bit priorities;
  frequency policies retain counts and a representative offset for all positive
  IDs. No full candidate stream is silently retained by a policy. Python
  reachable state and packed-record bytes are both reported. Python state is
  retained object size, **not** allocator RSS or a peak-memory measurement.
- Evaluator-only truth sets and input arrays are used to calculate losses and
  oracle bounds. Policies cannot consult them. The shared source's identifier
  bytes are reported separately. Document text, source decompression, actual
  downstream processing, and remote storage latency are outside this probe;
  processed-document counts expose work differences but do not benchmark those
  costs. Consequently the timing data do not establish a production advantage.

The larger filter spends exactly **2560 additional payload bytes**, the packed
size of 64 bottom-k records (16-byte ID + 8-byte offset + 16-byte priority).
This is below the prototype's measured bottom-k Python metadata, and excludes
its heap/index overhead. It performs no audits. It is a conservative RAM
comparison, not an equality of total disk use or CPU cost: accepting more
documents can enlarge the authoritative log and more hashes can cost time.

## Baselines and scope

The five audit policies are uniform arrival reservoir sampling; the same
reservoir with verified-positive caching; uniform distinct bottom-k sampling;
most frequent IDs; and least frequent IDs. Frequency ties use independent
sampling priorities, not numeric ID order. All are established baseline ideas,
not proposed contributions. Caching an audited false-positive ID as *absent*
would be wrong after successful processing; the implemented cache records that
the ID is now processed and merely avoids duplicate exact checks.

The reported `min(B,U)` rescue oracle is scoped to the fixed ordinary Bloom
bitmap and its observed candidate pool. It is **not** an upper bound on adaptive
filters that change fingerprints or rebuild; such a repair can correct other
keys. We inspected the published broom/TAF/cache work rather than implementing
its full auxiliary dictionary. That literature supplies feedback after errors,
including a colliding stored key in the broom construction. Our boolean exact
membership lookup does not supply that witness without additional organization.

These limitations are part of the no-go decision, not hidden prerequisites for
a claimed universal impossibility result.
