# Publication assessment after the relations revision

**2026-10-13: substantially improved working draft; original-research submission
is not yet justified.** The paper now has a coherent question, explicit models,
corrected proofs, primary-source attribution, a real stored-filter experiment,
and reproducible checks. This supersedes the earlier June recommendations that
the paper was effectively ready for Information Systems.

## What is now defensible

The revised manuscript, **Error contracts for approximate relations**, connects
constraint-preserving representations to fixed source identities and query-wide
error budgets. It proves and scopes monotone one-sided contracts, supplies a
tractable binary-witness case, and separates construction conditioning from
unconditional independence. A partitioned Bloom implementation actually stores
bits, serializes and reloads them, and answers queries without an exact-set oracle.

The experiment exposes a practical specification failure: a 5% source target
produces roughly 33% error on a valid false query profile. Calibrated canonical
and ordered-OR representations agree empirically with their ideal-model
comparators. Exact rational audits certify the recorded conditional bounds under
that model. They do not prove finite BLAKE2b independence or an adaptive guarantee.

Related manuscripts contributed useful ideas about occupancy conditioning,
fingerprint retrieval, and storage/error accounting. Their assumptions were
checked rather than inherited wholesale; two separate cross-paper mathematical
problems are recorded in [related-ideas.md](related-ideas.md).

## What the evidence does not establish

Provenance, dependence-aware inference, dissociation, monotone certificates,
graph dynamic programming, and canonicalization are established. The exact
one-sided error identity was not found verbatim in the targeted search, but its
short derivation from known certificate structure makes that absence weak
evidence of research novelty. The independence-versus-sharing distinction is
important exposition, not by itself a new result.

The 55.8% byte saving (3,752 versus 8,482) mostly measures canonical deduplication
and avoidance of the ordered-OR penalty. Against a conservative certificate
union-bound budget, the same sizing routine changes only from 3,768 to 3,752
bytes: **16 bytes, about 0.425%**, in this workload. This limited marginal benefit
must remain visible. The synthetic inference speedup comes from standard
structured inference; it is not a new solver result.

One synthetic query family, one size and target, and one reference filter do not
establish broad workload benefit. Approximate construction-level intervals do
not prove the concrete family satisfies its ideal-model source law. Generic
floating-point screening is not outward certification, although recorded
occupancies have been checked exactly.

## Highest-value next research step

The strongest next question is whether **automatic extraction of source identity
and query contracts changes representation choices on meaningful constrained
relational workloads**, beyond canonicalization and conservative certificate
bounds. Start from concrete bounded-fanout query templates and a documented
application, not another arbitrary synthetic size sweep.

Compare canonical and repaired representations, the sharp and conservative
budgets, exact/structured lineage inference where feasible, published dissociation,
and a modern fingerprint/retrieval filter. Include mixed truth profiles and
construction costs. A useful compiler or allocation method must show an
incremental benefit that a small hand-written formula does not already deliver.
If that benefit is negligible, pivot toward a carefully delimited constrained-
truth problem or an explicit finite-hash guarantee; do not manufacture novelty
by renaming known results.

A companion maintenance task is to correct the BHF discrete order-statistic law
and map-composition independence claim. These are concrete correctness leads,
not proposed publication contributions.

## Venue recommendation

Do not select a submission date yet. **Information Systems** remains a reasonable
conditional fit if the work develops a substantive data-management method or
evaluation; its [official scope](https://shop.elsevier.com/journals/information-systems/0306-4379)
includes data models, algorithms, and related theory. **Journal of Logical and
Algebraic Methods in Programming** is a conditional alternative for a substantial
formal contract-system contribution within its
[official scope](https://shop.elsevier.com/journals/journal-of-logical-and-algebraic-methods-in-programming/2352-2208).
Neither recommendation asserts acceptance likelihood or present readiness.
The current text is suitable for internal or advisor review as a working paper.
Nothing was submitted or published externally in this revision.
