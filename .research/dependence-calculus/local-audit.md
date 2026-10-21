# Local claim audit

Checked against active sources on 2026-10-13. This audit distinguishes a theorem with explicit assumptions from misuse outside those assumptions. Canonical manuscripts and public package APIs were not changed by this research run.

| Location | Finding | Recommended treatment |
|---|---|---|
| `papers/bernoulli_composition/sections/set_theory.tex`, cross-set independence assumption | The active manuscript already requires independent construction randomness for the binary composition formulas. | Preserve it. Do not characterize the whole paper as silently assuming independence. Explain that a compound expression can reuse a source and thereby violate this assumption at an internal node. |
| Same file, `rem:parametric_parsimony` around line 475 | Text attributes factorization of per-set channels to element-wise independence, whose axiom concerns distinct elements within a set. | Cite and require cross-set independence for the factorization across operands. Marginal rates and within-set independence do not imply it. |
| Same file, `rem:monoid` around line 658 | Union/intersection are associative on realized sets. Independent rate pairs alone are insufficient for all expression rewrites or reuse. | Distinguish algebra of random objects on a common probability space from an algebra of marginal summaries with fresh-draw semantics. Source-aware lineage retains the needed identities. |
| `papers/bernoulli_relations/sections/rel_algebra.tex`, projection independence theorem around line 201 | Correct for the explicitly tuple-independent inputs in that section. | State that the theorem cannot be reapplied after canonical symmetry or a join without checking source supports. Add the derived covariance proposition as the appropriate replacement for orbit-independent sources. |
| Same file, join dependence theorem around line 321 | Correctly identifies the source of dependence between outputs sharing a tuple. | Extend this account through subsequent projection and reuse. The dependence itself is established probabilistic-database lineage behavior. |
| `papers/bernoulli_relations/sections/properties.tex`, canonical test around line 276 | Homogeneous orbit representatives preserve tuple FPR/TPR and impose the invariant. The rate claim is sound. | Qualify “free”: marginal rates and representative storage do not account for query-level inference cost. Distinct orbits are independent only under an explicit construction model. |
| `papers/bernoulli_relations/sections/intro.tex`, paragraph beginning “The genuinely new territory” | The categorical dismissal of probabilistic-database work on invariants/constraints is too broad. | Compare specifically with integrity-constraint and correlated-lineage work. A fixed exact relation corrupted by an encoding is a useful interpretation, not a reason existing possible-world machinery cannot apply. |
| `bernoulli-py/src/bernoulli/atom.py` | Binary methods explicitly use independent noisy observations of the **same** truth. They neither track observation provenance nor accept arbitrary distinct facts without a prior/model. The module-level “min bound” description is stale relative to the methods. | Retain the explicit method assumptions; do not use `b & b` as a frozen-observation error contract. Research test demonstrates 0.04 from the independent interpretation versus 0.2 for a repeated source of rate 0.2. Fix docs separately if integrating the new API. |
| `bernoulli-py/src/bernoulli/relations/relation.py` | Stores exact tuples plus propagated rate annotations; `contains` is exact. It is not a physical random encoding or a sampler over jointly dependent approximate query answers. | Avoid claiming the existing class validates a shared-randomness construction. The new research relation stores explicit finite candidate tuple lineages and has a separate declared probabilistic model. |

## Proposed integration into the relations manuscript

1. Introduce a source map from tuple occurrences to frozen construction outcomes, with truth-homogeneous aliases and a separate independence assumption for distinct sources.
2. State projection independence in terms of disjoint source supports. Give the exact covariance formula and a two-tuple symmetry example.
3. Distinguish fixed-profile FP/FN from worst-case rates over unknown exact databases. Include the boundary-certificate theorem, heterogeneous version, and sharp arbitrary-dependence alternative.
4. Give the binary-witness/occurrence-two class as a worked tractable contract family. Attribute its graph algorithms and explain the cost of obtaining a compact contract outside that class.
5. Present strict-symmetry counting hardness as an application of established correlated-lineage/Holant results, not a new counting theorem.
6. Replace broad novelty language with a contribution statement tied to a demonstrated benefit. The current synthetic artifact alone does not establish a systems contribution or standalone publication readiness.

The exact technical statements and proofs are in `attempts/002-theory/technical-note.tex`. The source comparison and qualifications are in `attempts/001-literature/findings.md`.
