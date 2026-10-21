# Executable probe design

Scope: finite, explicitly enumerated candidate tuple universes; set semantics; exact selection predicates, projection, equijoin. The exact database is fixed. Each independent construction source is one frozen Bernoulli bit; repeated uses of a source, including canonical-orbit aliases, reuse that bit. Source identity never establishes independence by itself: mutual independence of distinct IDs is an explicit model assumption. No adaptive-query or real-hash guarantee is claimed.

Representation: a typed immutable monotone DNF (OR of witness sets of integer source IDs), using Boolean idempotence and absorption. A finite relation maps typed attribute tuples to lineage. A channel maps fixed truth and FP/FN rates to source acceptance probabilities. This is established probabilistic-database lineage, used as an audit and test substrate, not asserted as novel.

Methods: exhaustive independent-source weighted enumeration as small-instance oracle; arbitrary-dependence Frechet bounds; published symmetric disjunctive dissociation bounds; independent disjoint witness packing; optional Shannon conditioning; exact weighted path/cycle dynamic programming for binary witnesses with source occurrence degree at most two. Benchmark the latter against enumeration and bounds, measuring probability, interval width, runtime, peak traced allocation, and source count.

Test-first checks: aliasing must preserve repeated-source probabilities; join then project must retain shared witnesses; canonical symmetry can induce dependence between projected tuples; published bounds must cover exhaustive weighted enumeration across boundary/interior rates; path/cycle DP must equal independent enumeration; unsupported high-degree/higher-arity cases must be rejected. Keep prototype under research until its semantics and usefulness warrant package integration.

Publication hypothesis: a tractability boundary in witness size and alias multiplicity for originally read-once query lineages. Mathematical truth and novelty are separate validation tasks; no new solver is presumed.
