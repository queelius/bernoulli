# Claim–evidence ledger: relations revision

Updated 2026-10-13. This ledger supplements, rather than overwrites, the completed
dependence-calculus investigation.

| Claim | Status and evidence | Scope / attribution |
|---|---|---|
| The inherited relations draft needed substantive mathematical repairs | Confirmed: `math-audit.md`, 486 focused tests, corrected theorem text | Diagonal symmetry, single-valuedness, variable orbit sizes, transitivity, projection and independence, partial functions, and the CLT. June reviews are superseded. |
| Source identity is essential for query error | Proved and checked: repeated-source examples, projection covariance, joint join law | Established Boolean lineage/provenance principle; not claimed as novel. |
| Independent one-sided truth-uniform error equals 1−(1−α)^s0 / 1−(1−β)^s1 | Proved, 1,970 exact rational identities on all 197 monotone functions through four variables | Elementary monotone certificate consequence; exact original formulation unlocated, originality unestablished. Additional truth constraints can destroy sharpness. |
| Marginal-only envelope is min(1,αs0), with weighted analogue | Proved by certificates and attaining event couplings | Known union-bound mechanism. Two-sided channels inherit upper bounds, not both exact identities. |
| Conditional common-rate dependence permits a mean-rate contract | Proved by conditional application plus Jensen; tiny Bloom exhaustive check | Special dependence model; not a claim for arbitrary correlations. Borrowing source and hypotheses recorded in `related-ideas.md`. |
| Binary-witness/source-occurrence≤2 homogeneous contracts are inexpensive | Proved path/cycle independent-domination formula; 305 graph checks | Known graph structure and dynamic programming. No new general inference solver. |
| A 5% tuple budget can fail a 5% query budget badly | Concrete stored-filter experiment: boundary-profile FPR 0.32915 versus all-false 0.02646 | One fixed 12-cycle family, one-sided errors, nonadaptive keys. |
| Calibrated filters are compatible with the target model | 160 builds ×128 bundles/profile; canonical boundary FPR 0.04907, ordered OR 0.05103; construction-level intervals include ideal predictions | Empirical agreement is not proof of BLAKE2b independence, nor statistical certification that every concrete-hash error is ≤0.05. |
| Recorded ideal conditional query envelopes are ≤0.05 | Independent exact rational audits of all 320 calibrated recorded builds | Ideal random-function model, conditional on inserted-key history. Generic float screening is not a certificate. |
| Canonical representation uses fewer bytes at equal ideal query target | 3,752 versus 8,482 serialized bytes, 55.8% reduction | Mainly representative deduplication plus OR-repair rate cost, not an optimality result or a large benefit of the sensitivity formula itself. Common workload/mode context and Python overhead excluded. |
| Sharp contract improves storage substantially over conservative certificate sizing here | **Not supported**: same sizing routine gives 3,752 versus 3,768 bytes, a 16-byte / 0.425% difference | Sizing calculation only; no fourth physical experiment. This limits the novelty/impact claim. |
| Error rates characterize encrypted-search security | **Withdrawn** | Rates specify functionality. A concrete adversarial security definition and leakage analysis would be separate work. |
| The manuscript is ready for original-research submission | **Not supported** | Independent review supports a defensible working synthesis and reproducible probe; new theoretical significance or practical benefit still required. |

## Failed or rejected approaches

- Treating tuple occurrences as independent: counterexamples include repeated
  operands, projection of canonical symmetric sources, and map composition with
  colliding intermediate inputs.
- Calling all constraint repair a local-versus-cascading dichotomy: the checked
  statements concern particular orbit and simultaneous-addition constructions.
- Pricing a two-sided recall improvement using a zero-FN membership lower bound:
  replaced by explicitly conditional rate/space accounting.
- Importing the BHF discrete order-statistic theorem: rejected by the exact
  N=2,m=2,p=1 counterexample. Its continuous limit is a different statement.
- Equating floating occupancy screening with certification: a rounded 1/3 example
  refutes the generic claim; recorded builds have a separate rational audit.
- Subtracting a near-one failure probability to obtain tiny success probabilities:
  review found zero outputs at p=2^-60; regression tests and stable direct-success
  accumulation address this numerical implementation issue.

Proofs, experiments, numerical checks, and novelty judgments are separate evidence
types. None of the simulation results is offered as a proof of the source law.
