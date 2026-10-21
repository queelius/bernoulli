# Opportunity-test design

This is a bounded research prototype, not a general SQL planner. The authorized
output is evidence for or against a publication, including an implemented
counter-baseline when it defeats the initial approach.

## Application and query

A versioned content manifest has key (snapshot, path) -> content identifier.
The parameterized positive query asks whether two supplied manifest rows have
the same identifier: exists z R(u,z) and R(v,z). Row keys are exact; queries may
use any pair of known keys, not only a cached benchmark list. Git tree entries
provide a documented local workload. Their object identifiers define equality;
the experiment does not assume cryptographic collision-freedom of file hashes.

The client supplies row pairs, using a serialized exact row-key directory. For
tuple-membership representations the evaluator enumerates an exact finite value
domain and probes (row,value) tuples. For direct value representations it reads
two stored codes. Domain enumeration, directory lookup, serialized directory and
schema, seeds, headers, and candidate costs are counted. Build-time exact values
are unavailable to approximate query methods. The exact baseline may store
dictionary-coded values because equality does not require recovering original
content identifiers.

## Cases and comparisons

1. Ordinary source-deduplicated certificate budget p <= delta/k.
2. Independent lineage budget 1-(1-p)^k <= delta.
3. Constraint-aware conservative certificate 2p+(k-2)p^2 <= delta.
4. Constraint-aware exact product 1-(1-p)^2(1-p^2)^(k-2) <= delta.
5. Modern binary fuse filters, smallest available 8/16-bit width satisfying
   each applicable ideal per-key contract, with implementation/model caveats.
6. Exact dictionary-coded values and finite universal linear value fingerprints.

The constrained formula is specialized to distinct total functional rows and
k>=2. Empty/partial rows and repeated operands are tested separately. Existing
lineage evaluation computes the product exactly because the witnesses are
read-once after alias deduplication; no new inference algorithm is claimed.

## Soundness and numerical decisions

Frozen one-sided filters have FN=0. For partitioned Bloom filters the contract is
conditional on inserted-key hashes under the ideal random-function model. Each
accepted build must pass the query bound using exact rational occupancies, not a
rounded float threshold. Rejection uses only inserted keys. Concrete BLAKE2b
behavior is measured, not claimed to instantiate full independence.

Value fingerprints use a truly specified finite family: uniform b by w binary
matrix, fixed values, two unequal codes collide with probability 2^-b. The seed
is stored and counted. Seeded pseudorandom runs estimate behavior of the
implementation; proof concerns the uniform finite seed distribution. Repeated
queries reuse the same stored result; adaptive conditional guarantees are not
asserted. Rank-based joint collision formulas are checked against known matroid
results and exhaustive finite constructions.

## Scope gate

Build only enough automatic schema/source extraction and width/rate selection
to compare these representations. If established retrieval dominates the first
case and the finite alternative is known, document that negative conclusion
instead of constructing a large planner or claiming a new theorem.

## Cycle 2 refinement: restricted candidate sets

The strongest surviving case is Q(u,v,C) with z restricted to the supplied
candidate catalog C. The primary contract requires two distinct row keys; the
query may repeat either atom syntactically, but normalization reuses its source.
A true row value outside C creates all-false membership bits. Two rows can share
that outside value, a counterexample to assuming that shared value hashing has
independent per-row errors. Self-joins over restricted C need the ordinary
one-row contract and are tested as a scope counterexample.

Add a row-specific retrieval baseline storing f(row, actual_value), with f a
degree-at-most-three polynomial over P=2^61-1 and output modulo 2^b. An injective
tuple code below P makes four distinct evaluations independent. Its exact
pair-collision probability is q=1/2^b+(2^b-1)/(2^b P^2). Each two-absent-atom
witness has probability q^2; at most two witnesses can have just one absent
atom. Thus 2q+(|C|-2)q^2 bounds every fixed false distinct-row query, without
cross-witness independence. Four uniform field coefficients occupy 32 bytes;
all coefficients, including a zero leading coefficient, are allowed. No
conditional guarantee after revealing stored fingerprints is asserted.

This construction is standard polynomial k-wise hashing plus a union bound.
Its role is a finite, compact competent baseline and a test of the nearby
alternative, not a new theorem. Exact values and full-domain shared fingerprints
remain controls; the shared equality shortcut alone does not cover restricted C.
