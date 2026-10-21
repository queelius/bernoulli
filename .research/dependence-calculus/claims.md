# Claim–evidence ledger

Updated 2026-10-13. Mathematical correctness and novelty are separate columns.

| ID | Claim | Evidence / status | Novelty assessment |
|---|---|---|---|
| C1 | Marginal acceptance rates alone do not determine conjunction rates. | Fair identical, independent, complementary bits give 1/2, 1/4, 0; executable Frechet fixture. | Classical, not new. |
| C2 | Source-preserving relational lineage prevents treating repeated frozen observations as fresh trials. | `attempts/003-prototype/test_contracts.py`: aliasing, join/projection, symmetry tests pass. | Probabilistic DB lineage/provenance, established. |
| C3 | Projection of a tuple-independent input preserves independence; projection after canonical symmetry need not. | Exact covariance derivation in `attempts/002-theory/theory.md`; exhaustive rational checks and two-tuple fixture. | Useful scope clarification to existing manuscript; elementary corollary. |
| C4 | Canonical symmetry can preserve tuple and single-witness marginals while making a fixed query's exact acceptance probability #P-hard. | Fixed cubic-neighbor query and edge-cover reduction; Cai–Lu–Xia source verified by literature branch. K4 exact enumeration: 23/64 versus 1695/4096 independent oriented tuple result. | Applied consequence of known Holant/correlated DB results; not a new counting theorem. |
| C5 | Binary witness lineages with max source occurrence two admit linear-arithmetic path/cycle evaluation. | DP proof plus weighted exhaustive tests. | Standard weighted independent-set DP. |
| C6 | Disjunctive dissociation gives sound acceptance bounds under independent source IDs. | Gatterbauer–Suciu primary source; 256 three-variable DNFs × 27 rate vectors tested against enumeration. | Published method; explicitly attributed baseline. |
| C7 | Named uncertainty sources and bounded WMC are a timely new PL contribution. | Refuted by verified ICFP 2026 Liell-Cock–Staton paper among earlier work. | Do not claim. |
| C8 | Worst-case one-sided FP/FN rates over all exact databases have sensitivity / minimal-transversal characterizations. | Proved in technical note; 1,970 exact-rational checks across 197 monotone functions, plus graph checks. Implemented for the binary/degree-two class. | Exact matching prior formulation not located; elementary consequence of known boundary/certificate structure, standalone novelty unestablished. |
| C9 | A fixed-profile query probability is a universal error guarantee over exact databases. | Refuted: 16-source cycle with alpha=0.05 has all-false-profile FPR 0.0375062 but worst-profile FPR 0.401263. | Semantic distinction, useful for model-level calibration; not alone a new algorithm. |
| C10 | The prototype establishes a production/physical-filter guarantee or a new state-of-the-art solver. | Not supported. Synthetic inference only; real filter independence and optimized prior solver comparisons remain outside completed scope. | Do not claim. |

Scope of executable guarantees: fixed finite candidate universes; fixed exact truth; explicit mutual independence of distinct construction source IDs. Real-arithmetic results are sound under these assumptions. The float prototype is tested to numerical tolerance, not a certified floating-point interval implementation. No adaptive-query, arbitrary shared-hash, or actual compressed-filter independence guarantee is claimed.
