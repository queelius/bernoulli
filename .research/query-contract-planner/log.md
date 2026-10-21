# Research log

## 2026-10-13 — cycle 1: test the representation baseline first

Created a new research goal and isolated artifact directory, retaining both prior
research runs and all unrelated working-tree edits. The user supplied explicit
autonomous implementation and review authorization. The research/design skills
are used to keep the question, evidence, and tests explicit; their generic
intermediate approval gates do not override that authorization.

Selected functional/bounded-cardinality intersection as the first falsifiable
case. Dispatched independent literature and mathematical audits. Early agreement:
the constrained truth-profile improvement looks real, but value retrieval is a
critical and potentially decisive baseline. The next experiment will include it
before any general planner is attempted.

## Cycle 2 — finite restricted-candidate contract

Full-domain equality was defeated by standard retrieved value fingerprints and
exact dictionary IDs. Restricting the existential value to a query parameter C
exposed a real shared-value-hash failure when equal values lie outside C.
Implemented row-specific degree-at-most-three polynomial fingerprints over
F_(2^61-1), with exact modulo collision rate and a constraint-aware union bound.
The literature audit attributes the hash family to established limited
independence and the linear-rank alternative to the Critical Theorem. No novelty
is claimed for either.

The theory audit checked 19502 negative truth profiles, 1100 heterogeneous cases,
327 finite linear-hash cases, and 240 fixed queries over every cubic over F7.
The product-vs-union upper bound limits the extra continuous saving to 0.03684
bits at a 5% target. This determines the next step: measure representation and
metadata effects rather than build a general planner.

## Cycle 3 — physical pilot and independent review

The first actual stored-filter experiment completed in 274.88 seconds, peak RSS
29896 KiB, with 32 builds per method and four workloads. It is archived under
attempts/001-fixed-c/. Bloom filters pass an exact rational occupancy audit;
binary fuse is a pinned nominal-hash comparator; finite row fingerprints carry
an unconditional finite-family theorem. These are not identical concrete-hash
guarantees and remain labeled separately.

Independent review identified unsafe aliases and candidate-code range handling,
missing candidate-capacity checks, overly narrow zero-observation intervals,
and a fixed-C baseline omission. Each executable defect was reproduced by a
failing test before correction. Coverage and schema/manifest tests were added.
The final workload varies C independently of construction seeds; no per-C
answer/presence cache is built. The final run uses 64 constructions and 32 cases
per truth profile. This is a correction to experimental scope, not a larger
sweep presented as research novelty.

## 2026-10-14 — cycle 4: complete evaluation and decision

Completed four workloads, nine stored representations/budgets, and 64 seeded
builds each: 2304 constructions and 368640 primary queries. Requests vary C and
cover five truth profiles, including equal values outside C and repeated atoms.
The application requests are stratified generated cases on two pinned Git
snapshots, not a production query trace. All query-parameter, directory, catalog,
seed, and framing costs are documented. The main run took 117.78 seconds with
36684 KiB peak RSS.

The constraint reduces ordinary Bloom payload by 1464 bytes in the application,
but the elementary constrained union bound captures nearly all the gain.
The sharp product saves only 6 further bytes (0.00349% of total storage).
Finite row fingerprints save 880 bytes (0.5104% total; 37.98% of payload) against
exact IDs and cost about 8 times as much query latency including preparation.
Neither established hash theory nor these prototype measurements establishes
an original publication contribution. One synthetic empirical FP estimate is
5.615%; its uncertainty includes the 5% target. Concrete hash experiments are
kept separate from finite-family and ideal-model theorems.

Independent review closed the remaining capacity/capability defects. There are
70 new tests and 540 relevant existing regressions, all passing; new-code
coverage is 92.95% of statements and 83.97% of branches. The verifier rebuilt
all 2304 payloads and exact recorded bounds, and reproduced 5760 representative
query outcomes. The exact measured driver is archived because two subsequent
edge-case fixes did not affect saved workloads. Charts were rendered and
inspected; provenance and reproduction commands are retained.

Final decision: no original-research submission or relations-manuscript update
is warranted. This is a scoped negative opportunity audit, not a general
impossibility result. The strongest remaining gate is an external application
where row/catalog infrastructure already exists and approximate final answers
yield a useful operational storage benefit after comparison with exact values,
retrieval, and modern native filters. Additional synthetic sweeps or a general
planner interface would not resolve the demonstrated novelty deficit.

Research state, claims, bibliography, review resolutions, and assessment are
complete. Prior research and all unrelated edits are preserved; nothing was
submitted or published externally.
