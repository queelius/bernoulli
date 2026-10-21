# Editorial review responses

2026-10-15. Internal revision record, not a journal response letter. Three agents
first assessed the same draft independently, without earlier favorable reviews
or one another's reports. Each then challenged the revision from its assigned
perspective. The main agent evaluated recommendations and owns the final edits.

| Lens | First report | Revision report |
|---|---|---|
| Readability | [Round 1](readability/round-1.md) | [Round 2 and closure](readability/round-2.md) |
| Scientific validity | [Round 1](validity/round-1.md) | [Round 2](validity/round-2.md) |
| Methods and reproducibility | [Round 1](methods/round-1.md) | [Round 2](methods/round-2.md) |

Criteria are in `criteria.md`; primary editorial guidance is in `sources.json`.
Baseline sources, PDFs, and package remain in `baseline/`. The final manuscript
shares its abstract, body, and backmatter between canonical and venue wrappers.
Review reports pin the versions they assessed. Narrow later corrections are
identified explicitly rather than retroactively changing review hashes.

## Readability findings

| ID | Decision | Change and evidence |
|---|---|---|
| R1: singleton first | Accept | Opening gives the complete mechanism; singleton is Proposition 1, followed by Figure 1. Aggregate certificate is secondary. Round 2 orientation test passes. |
| R2: notation/support | Accept | Define symbols and concatenation before Eq. (1). Distinguish selected positions from sets of possible complete views. Consistent adjacent-domain terminology. |
| R3: ambiguous table | Accept | Each row states equality, input class, insertion count, widths, and share count; seeded row explicitly says singleton. Define mismatch and count factors. |
| R4: late scope discussion | Accept | Data-identifier game and source Eq. (27) appear beside the two-world comparison, before methods and implications. |
| R5: repeated disclaimers | Accept | Group limits with the claims they qualify; discussion opens with the protocol-specific finding. |
| R6: abstract arc | Accept optional improvement | Target, execution, deterministic mechanism, extension, evidence, scope, implication. |
| R7: hierarchy | Accept in substance | Four sections, no isolated subsection. Keep two theorem/proof pairs; marginal uniformity becomes an explanatory paragraph. No extra premise table needed. |
| R8: definitions/display | Accept | Definitions and Eq. (1) appear together on page 2 in both final PDFs. |
| R9: occupied zero | Accept required fix | Zero contributes to occupied count but does not change XOR. Arithmetic was already correct; reviewer targeted recheck closes wording. |
| R10: repeated interval caveat | Accept optional trim | Remove final redundant sentence; methods/caption still distinguish proof, checks, and probability estimation. |

## Validity findings

| ID | Decision | Change and evidence |
|---|---|---|
| V1: aggregate feasibility/value | Accept | State `c*kappa<=m`; give differing-neighbor histories conditional on a reachable disjoint history; allow zero information when aggregates already coincide. Counts above `m/kappa` exclude certificate. No prevalence claim added. |
| V2: admissible comparison | Accept | Publisher and secret fixed internally, not given to observer. Two eligible neighbors distinct from publisher. Same positions/prefix follow source derivation; whole-ledger equality not required. |
| V3: precise target | Accept | Source Section 6.2 controlled adjacent-ID recovery motivates opening/conclusion. Distinguish neighbor ID from signer, named edge/path, data ID, and query-privacy game. |
| V4: public singleton objection | Objection rejected on source evidence | Timeout, full filter/count publication, occupancy, and honest-administrator model admit execution. Add explicit honest timeline. |
| V5: proof/conditioning | No defect found | Union, atomic failure, frozen words, distinct positions, and conditioning retained. No random-support occurrence assumption needed. |
| V6: predecessor contrast | No defect found | Original GBF padding plus OT has a different public view. Statistic-level protections do not establish complete repair. |
| V7: mask independence insufficient | Accept required fix | Require fresh uniform secret masks independent of identifiers and one another. PRF precedent stated separately. Reviewer rechecks final source and PDF. |

## Methods findings

| ID | Decision | Change and evidence |
|---|---|---|
| M1: optimized execution skips work | Accept required artifact fix | Reproduced before fix: assertion-contained insertions vanished and success-shaped counts were written. A module-level `if not __debug__` guard now rejects before experiments/output. CLI/environment regressions and reviewer script/import/runpy checks pass. Normal results unchanged. |
| M2: count conditioning | Accept optional improvement | State fixed positions/prefixes, factors `4*8^2` and `4^2*8^2`, singleton seeds 0–63, and PRNG limitations. |
| M3: full-array oracle | Accept compact improvement | Hand-derived full array covers prefix, occupied zero, and overlap. A deliberate prefix-bit mutation fails (`prefix-mutation-check.txt`). Independent reviewer checks 244,816 tiny transitions; supplemental review evidence only. |
| M4: reproducible AST provenance | Accept clarification | Document `ast.dump` arguments, UTF-8/no newline, and omission of empty Python 3.12 `FunctionDef.type_params` for historical hash compatibility. Both digests reproduced; direct AST equality also verified. |
| M5: precompiled optimized bytecode | Accept optional hardening | Initial `sys.flags.optimize` guard missed bytecode compiled with optimization but loaded by a normal interpreter. Regression first fails, then passes with module-local `__debug__` check. See `optimized-bytecode-red.txt`. |

The mathematical module and original ten tests are byte-identical to historical
files. The two experiment functions are AST-identical. The guard is an engineering
correction, not novelty. Seven artifact tests bring the focused suite to 17;
unit/subprocess integration checks, lint, typing, reproduction, and clean-source
rebuild are recorded in final verification.

Normal-compilation coverage reports 121/121 statements and 48/48 branches;
the compile-time guard is outside that denominator and is checked separately.
An earlier 123/50 coverage result refers to the intermediate `sys.flags` guard,
not the final artifact. The historical experiment driver stays unchanged;
use the corrected portable supplement for the paper's reproduction.

No full protocol implementation, operational trace study, or broad experiment
campaign was added: none is required for the conditional identity. Author review
and declarations remain pending. Internal review agreement and coverage do not
establish originality, complete protocol security, journal acceptance, or PhD credit.
