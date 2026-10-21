# Research synthesis: dependence-aware Bernoulli query contracts

**Decision, 2026-10-13:** the research question has a useful restricted answer, backed by proofs and an executable artifact. A standalone submission is **not yet warranted**. Generic dependence-aware lineage, conditioning, and bounded probability inference substantially overlap established work. The strongest result developed here is a sharp one-sided contract over unknown exact databases. Its exact prior formulation was not located, but it is an elementary consequence of known Boolean certificate structure; originality and publication significance remain unestablished.

The recommended publication route is to strengthen the existing relations manuscript with these distinctions and results, then demonstrate a concrete benefit for a real constraint-preserving approximate representation. This run does not claim to have produced an accepted, submission-ready, or independently novel paper.

## Answer to the research question

Approximate queries can have compact sound contracts when their representation records **which occurrences reuse a random source**, and the contract states what dependence information is available. Marginal rates alone cannot support products. A query fixed independently of construction randomness can be represented by a Boolean lineage over frozen source bits; aliases read the same bit. This is existing probabilistic-database methodology, with a Bernoulli encoding interpretation.

For a fixed exact database, the problem is weighted Boolean probability inference: exact answer false gives FPR equal to acceptance probability; exact answer true gives FNR equal to one minus acceptance probability. Source-aware dissociation and conditioning supply sound bounds under independent source bits. Arbitrary-dependence Frechet/union bounds are available when independence is absent. Exact general inference remains hard.

A different and practically relevant goal is a **single guarantee over every exact database consistent with the source aliases**, without inventing a prior over those databases. For a nonconstant monotone query lineage F and independent one-sided errors, the strongest result here is

\[
\sup_{F(x)=0}\Pr(F(Y^+(x))=1)=1-(1-\alpha)^{s_0(F)},
\]
\[
\sup_{F(x)=1}\Pr(F(Y^-(x))=0)=1-(1-\beta)^{s_1(F)}.
\]

Here s0 is the maximum number of individually pivotal source bits at a false exact input, and s1 is its true-input counterpart. The two equalities concern separate pure-FP and pure-FN models. They remain upper bounds with both error types present, but generally cease to be sharp.

**Proof idea:** extend a false exact input to a maximal false input. Monotonicity cannot decrease acceptance probability. At that boundary, any remaining zero flipping is sufficient for a false positive, so the error is exactly the independent union probability over those zeros. The dual argument uses minimal true inputs. Heterogeneous rates replace the homogeneous power by a maximum of products over boundary certificates. With arbitrary dependence and homogeneous marginal bounds, the sharp envelope instead becomes min(1, alpha·s0), with the dual FN formula.

For normalized positive DNF, s1 is the maximum minimal-witness size. The parameter s0 is the maximum size of an inclusion-minimal transversal, not a minimum hitting set. For binary witnesses forming a graph, s0=n−i(G), where i is the minimum size of a maximal independent set. Thus a compact scalar need not be cheap to compute. When every source occurs in at most two binary witnesses, graph components are paths/cycles and

\[
s_0=\text{number of singleton witnesses}+\sum_c(n_c-\lceil n_c/3\rceil).
\]

This yields linear graph work and a two-number contract for that restricted class. The underlying graph algorithms are standard. [Full proofs and qualifications](attempts/002-theory/technical-note.tex) are in the six-page internal note.

## What changed during the investigation

1. **Generic calculus candidate rejected as a novelty claim.** Source identities, Boolean provenance, read-once evaluation, conditioning, bounded-width inference, and dissociation have close predecessors. This includes [Gatterbauer–Suciu's probability bounds](https://arxiv.org/abs/1409.6052), [Kanagal–Deshpande's correlated-lineage inference](https://research.google/pubs/lineage-processing-on-correlated-probabilistic-databases/), and [2026 work on named uncertainty and BDD inference](https://arxiv.org/abs/2607.20801). The last concerns named epistemic uncertainty as well as inference; it should not be described as identical to frozen encoding-error semantics.
2. **Constraint/inference alternative proved, but novelty narrowed.** Canonical symmetry preserves tuple marginals while changing source sharing. Even projection can then create correlated outputs despite disjoint tuple fibers. A fixed cubic-neighbor query has easy read-once inference before symmetry and #P-hard edge-cover inference after it, despite identical individual witness probabilities. The counting mechanism is established Holant/correlated-database theory, so this is a useful application and scope clarification rather than a new counting theorem.
3. **Truth-uniform one-sided alternative developed.** The sensitivity formulas above distinguish fixed-profile inference from an encoding contract valid over unknown exact truths. [Gopalan et al.](https://www.cs.columbia.edu/~rocco/Public/GNSTW.pdf) already give pointwise sensitivity/noise bounds, and [monotone certificate–sensitivity equivalence](https://proceedings.mlr.press/v162/blanc22a.html) is standard. The exact one-sided equality was not located in this bounded search. That supports further consideration, not a claim of originality.

The [24-entry primary-source ledger](attempts/001-literature/findings.md) records what was actually verified, access limitations, and where comparisons are exact versus adjacent.

## Evidence and comparisons

- **Formal derivations:** boundary-certificate formulas; heterogeneous and arbitrary-dependence variants; projection covariance; the restricted graph algorithm; and strict-symmetry inference hardness.
- **Exact rational checks:** 1,970 homogeneous/heterogeneous contract checks over all 197 monotone functions on one through four inputs; 305 maximum-degree-two graphs; 256 covariance cases; eight weighted paths and 87 weighted cycles. These validate implementations and examples; the written proofs justify the general statements.
- **Research implementation:** 28 behavioral and integration tests pass, with 100% statement/branch coverage of `contracts.py`. An independent review also checked 8,000 compiler possible worlds and 983 graph/singleton sensitivity cases. It found two conditioning recursion cases, both fixed and covered by regression tests. The monotone-refinement claim was narrowed to extensions of a fixed conditioning-order prefix.
- **Existing package:** 470 tests pass, three skip, 90% combined statement/branch coverage; Ruff passes and strict mypy passes on 29 source files. No public package or canonical manuscript source was changed.
- **Measured comparisons:** 175 synthetic method/case comparisons against exact small-instance enumeration, dependence-robust bounds, published symmetric dissociation, witness packing, conditioning, and standard path/cycle DP. No claimed interval missed its reference at tolerance 1e-12; naive occurrence-product point estimates disagreed in 23 cases. Large-cycle reference values come from the DP being measured, not an independent exact solver. The full results disclose this limitation.

Two concrete findings illustrate the value of the distinctions:

| Example | Correct result | Incorrect or weaker treatment |
|---|---|---|
| AND of eight copies of one frozen source with FPR 0.05 | FPR 0.05 | Fresh-occurrence multiplication gives about 3.91×10⁻¹¹. |
| 16-source cyclic binary-witness query, source FPR 0.05 | All-false exact profile: FPR 0.0375062. Worst exact false-answer profile: FPR 0.401263. | Treating the all-false profile as a universal contract understates the worst case by more than a factor of ten. |

For the cycle example, a universal query-FPR target of 0.05 requires source FPR at most approximately **0.0051162** under the independent one-sided model. This demonstrates a model-level calibration difference, not a measured storage or real-filter advantage.

On the measured 16-source cycle, streaming exhaustive enumeration took about 282 ms, while standard path/cycle DP took about 0.030 ms and returned the same probability. The DP used more traced temporary memory than streaming enumeration (about 6.8 KB versus 2.4 KB); its benefit here is time. At 1,024 sources the DP took about 1.46 ms, comparable to the symmetric dissociation baseline's time, while giving an exact-model value instead of its broad interval. These are platform-specific Python measurements of known methods, not a new algorithmic speedup claim. See [results and plots](attempts/003-prototype/RESULTS.md).

## Limits that matter for publication

- **Independence must come from the construction.** Canonicalizing or naming sources establishes identity, not mutual independence across distinct IDs. No actual compressed Bloom/retrieval construction was validated against the independent-source model here.
- **The candidate universe is finite and explicit.** The prototype does not enumerate arbitrary unseen tuples or claim to solve physical database execution costs.
- **Worst-case truth is unrestricted after aliases.** Extra semantic constraints can exclude the maximizing profile; the unrestricted formula remains an upper bound but may cease to be sharp.
- **Adaptive queries are outside the model.** Fixed-query construction-randomness rates do not automatically survive conditioning on previously observed errors.
- **The code is numerical research software.** Real-arithmetic inequalities are proved; floating-point endpoints are tested to tolerance, not certified by outward rounding.
- **The comparisons are not a state-of-the-art systems evaluation.** They do not include optimized scaled dissociation, a production model counter, or real compressed data structures and workloads. Coverage and small exhaustive checks do not substitute for these comparisons or for novelty.

## Publication decision and next best task

Fold the source-identity semantics, projection qualification, and truth-uniform contract theorem into the existing relations work, with established methods clearly attributed. The [local audit](local-audit.md) identifies the exact claims to revise. Keep this technical note internal until the contribution is sharper.

The next empirical research question should be: **Does query-level certificate calibration change the best storage/error/runtime tradeoff between canonical-orbit testing and independent tuple testing plus repair, on a real approximate-relation construction with a justified dependence model?** Compare equal query-FP/FN targets, not merely equal tuple rates. Measure actual stored bytes, query runtime, construction costs, invariant violations, and error behavior across independent builds. Include a proper published probability-inference baseline and workloads with both mixed truth profiles and shared witnesses. A positive result would supply the practical contribution currently missing; a negative result would prevent overstating the framework's benefit.

For an expanded relational study with substantive implementation evidence, **Information Systems** is the best provisional fit among the previously discussed venues: its [official scope](https://shop.elsevier.com/journals/information-systems/0306-4379) covers data models/algorithms and requires compelling applications and serious experimental evidence. A formal specification contribution could instead fit **Journal of Logical and Algebraic Methods in Programming**, whose [official scope](https://shop.elsevier.com/journals/journal-of-logical-and-algebraic-methods-in-programming/2352-2208) includes quantitative correctness, specification, and algebraic methods. Neither recommendation is a readiness judgment or a prediction of acceptance.

## Outcome

The activated investigation is complete as a research and publication assessment: it tested the initial candidate, evaluated two nearby alternatives, produced proofs and reproducible code, and identified the remaining publication gap. **A standalone publishable novelty claim has not been established.** The remaining empirical and originality questions are explicit future research, not silently reported as completed. Nothing was submitted, published, or committed externally.
