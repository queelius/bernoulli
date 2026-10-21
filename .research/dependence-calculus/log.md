# Research log

Goal: see `goal.md`. Evaluation: self-evaluation. Logs are append-only.

## Initialization — 2026-10-13

Read workspace and paper guidance. Recorded preexisting worktree modifications; no existing source changes will be reverted. Using the research-agent workflow with user-selected research root. User explicitly authorized autonomous local research and implementation, overriding intermediate skill approval gates. No research output existed here at initialization.

Initial decomposition: local semantic audit, external novelty audit, formal candidate selection, executable validation, comparison, and synthesis.

## Cycle 1 — 2026-10-13: audit and novelty falsification

Read active composition and relations sources and bernoulli-py atom semantics. Composition already states cross-set independence; relations explicitly shows join dependence. Local explanatory claims sometimes conflate cross-element and cross-set independence. The atom methods explicitly assume fresh independent shared-truth observations; reuse does not satisfy that assumption. Literature branch found established dissociation, correlated lineage and current named-source programming work. Result: broad calculus novelty hypothesis refuted. Next: constraint-preserving aliasing as a narrower question.

## Cycle 2 — 2026-10-13: rate-preserving constraints and inference cost

Theory branch derived exact projected-output covariance, a path/cycle tractable class, and a fixed cubic-neighbor query whose symmetry quotient reduces exact FPR to counting edge covers. Primary counting references and correlated DB precedent checked by literature branch. Exact rational checks confirm K4 error 23/64 after quotient versus 1695/4096 before. Result: mathematically useful but not a demonstrated new complexity result. Next: executable comparisons and strongest nearby alternative.

## Cycle 3 — 2026-10-13: reference prototype

Implemented typed monotone lineage, select/project/join, source quotienting, exact enumeration, arbitrary-dependence Frechet bounds, published dissociation, witness packing, conditioning, and degree-two exact DP. Test-first failure observed before engine existed; replaced initial file-existence smoke check with behavioral fixtures. Current run: 21 tests pass, including exhaustive 256 three-variable DNFs at 27 probability vectors. No existing package APIs changed. Numerical soundness is to floating-point tolerance, not outward rounding. Next: benchmark runtime/memory/tightness, test coverage, adversarial review, and investigate one-sided truth-robust contracts.

## Cycle 4 — 2026-10-13: sharper truth-uniform contracts

Derived exact homogeneous and heterogeneous one-sided worst-case error via maximal false/minimal true profiles; identified sensitivity and minimal-transversal parameters. Derived sharp arbitrary-dependence counterpart and the binary/degree-two graph formula. Exact-rational checker passed 1,970 contract checks over 197 monotone functions and 305 graph cases. Implemented the restricted scalar contract. Literature audit located close sensitivity/certificate predecessors but not the exact displayed equality; originality remains inconclusive. Reflection: useful model-level calibration result, insufficient alone for a confident standalone novelty claim.

## Cycle 5 — 2026-10-13: adversarial review and measured evaluation

Independent review confirmed compiler and graph semantics, caught recursion through irrelevant/conditionally eliminated source IDs, and clarified refinement applies to a fixed ordering prefix. Reproduced failures, repaired them, and added regression tests. Direct-constructor normalization was also enforced. Final prototype suite: 28 passing tests, 100% inference-core statement/branch coverage, strict mypy and Ruff clean. Existing package: 470 passed, 3 skipped, 90% coverage, lint/type checks clean. Benchmark rerun after fixes produced 175 comparisons and five calibration examples, with no bound-reference failure to 1e-12. Scientific figure inspected. Reflection: known methods work as expected; measurements support utility and semantics, not a new solver claim.

## Cycle 6 — 2026-10-13: synthesis and conclusion

Prepared six-page internal LaTeX/PDF note, 24-entry verified bibliography, local claim audit, claim–evidence ledger, reproducible source/data/plots, and publication assessment. Corrected the technical note's Cai–Lu–Xia bibliography and clarified empty conditioning-class conventions; PDF rebuilt and visually verified. Final artifact existence and benchmark source hashes checked. Outcome: restricted mathematical answer and research artifact achieved; standalone novel submission not warranted on current evidence. Recommended integrating the useful results into the relations work and testing query-level calibration on a real compressed construction at equal query-error targets. Research run concluded; `synthesis.md` is the primary handoff. No external submission or publication.
