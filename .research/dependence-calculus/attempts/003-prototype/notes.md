# Local audit and prototype

Implemented immutable normalized monotone DNF, finite candidate relation select/project/join, explicit source quotienting, fixed-profile independent-source inference, arbitrary-dependence Frechet bounds, published symmetric dissociation, witness packing, prefix-monotone Shannon conditioning, standard path/cycle exact evaluation, and sharp homogeneous one-sided contracts for the binary/degree-two class.

Validation: 28 tests pass; inference-core statement/branch coverage 100%; strict mypy and Ruff pass. Test-first counterexamples exposed direct-constructor normalization and recursion through irrelevant/eliminated source IDs; all repaired. Independent review confirmed semantics and checked additional possible worlds and graph cases. The code is explicitly numerical, not interval-certified.

Experiments: `benchmark.py --repeats 3` produced 175 method/case comparisons. `summarize.py` produced quantitative tables, five truth-uniform calibration cases, and PNG/SVG scientific plots. `benchmark.json` includes source SHA-256 hashes, environment, measurement definitions and limitations. `RESULTS.md` summarizes actual measurements. No claimed bound missed the synthetic reference; the reference is independent enumeration only on small cases.

Outcome: useful verified research artifact, not a new inference algorithm or validated compressed-filter implementation. The sharp contract is a stronger semantic alternative than fixed-profile probability calculation, but standalone novelty and practical impact remain unestablished. Recommendation is manuscript integration plus a subsequent real-construction calibration study.
