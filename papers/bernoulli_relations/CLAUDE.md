# Relations manuscript guidance

## Current scope

**Error contracts for approximate relations**, Alexander Richard Towell.
The October 2026 revision supersedes earlier claims of a general closure dichotomy,
independent projected tuples, universal vanishing invariant preservation, and
cryptographic leakage characterized by FP/FN rates. The current draft is a
mathematically scoped synthesis and a stored-filter calibration study. It is not
submission-ready on present novelty evidence.

Use `.papermill/state.md` for current metadata and review history. Historical
June reviews saying every proof was correct or the paper was effectively ready
are retained only as provenance; substantive errors were found and repaired.
Root `.research/relations-revision/` holds the active revision evidence, and
`.research/dependence-calculus/` holds the completed prior investigation.

## Build and verification

Every LaTeX pass requires `TEXINPUTS=".:./sty:"`. The preamble loads minted,
so the current command also uses `-shell-escape`. Run pdflatex, bibtex, and two
more pdflatex passes as shown in README.md. Inspect warnings and rendered pages.
Do not infer a clean build from a stale PDF.

Research code is standalone; it does not import the `bernoulli` package.
Run the focused tests and coverage, numerical validation, stored-filter run,
and exact recorded-occupancy audit described in README.md. The existing
`bernoulli-py/.venv` has the required testing tools. Avoid allocating the entire
Monte Carlo sample tensor; `validate_quotient.py` uses bounded batches.

## Active structure

- `main.tex`: title, abstract, local notation packages, section includes.
- `sections/relations.tex`: finite set semantics and positive-query lineage.
- `sections/approx_rel_model.tex`: exact truth, construction randomness, frozen
  source identity, scoped independence, repeated queries and conditioning.
- `sections/rel_algebra.tex`: selection, projection by (fan-in,true-count), source
  covariance, join sharing, worked example, ideal-coin numerical validation.
- `sections/properties.tex`: exact scoped preservation formulas; canonical
  representatives, OR repair, deletion, limited transitive completion results;
  partial-function semantics as an invariants subsection.
- `sections/query_contracts.tex`: boundary-certificate contracts, marginal-only
  coupling bounds, shared-rate Jensen bound, degree-two binary witnesses, and
  a known edge-cover hardness application.
- `sections/calibration.tex`: concrete filter, model qualifications, results,
  prior inference comparisons, and limitations.
- `sections/oblivious_rel_model.tex`: limited encrypted-search functionality
  discussion; the historical filename does not imply a security theorem.
- `sections/conclusion.tex`: established evidence and remaining research gap.
- `code/`: ideal-law validation and stored-filter experiment, with pytest tests.
- `data/calibration/`: reproducible configuration, hashes, occupancies, timing,
  query outcomes, and summary; inspect its README before regeneration.

## Assumptions that must stay explicit

1. Fix exact truth, then sample a construction once. Repeated keys reuse bits.
2. Distinct tuples can alias one source; independent sources do not imply
   independent query outputs. Shared physical slots need not alias outcomes.
3. The sharp sensitivity formulas apply to separate one-sided models. With
   both error directions they are generally upper bounds, not equalities.
4. Maxima range over all source truth profiles. Additional integrity constraints
   can exclude boundary profiles, so sharpness must be rechecked.
5. Partitioned Bloom independence is conditional under ideal random functions.
   Domain-separated BLAKE2b and simulations do not prove this assumption.
6. Floating-point screening is not certified rounding. The recorded occupancy
   bounds have a separate exact rational audit; fixed-profile float inference
   remains numerical.
7. Byte comparisons count serialized filter payload/header, with the query mode
   and common workload supplied externally. Key counts are not memory bounds.
8. Canonical-versus-ordered savings mostly measure representative reduction and
   repair overhead. Compare conservative contract sizing before attributing
   savings to the sharp probability formula.

## Attribution and related papers

Provenance, weighted model counting, dissociation, monotone sensitivity/certificate
identities, graph dynamic programming, and perfect-hash-plus-fingerprint AMQs are
established. The exact novelty of this application remains unestablished. Cite
the verified bibliography and distinguish an elementary consequence from a new
algorithm. The sets, composition, maps, entropy, PHF, BHF and book manuscripts are
useful sources of ideas but not automatic proof authorities: the revision ledger
records separate BHF order-statistic and map-composition counterexamples.

Notation uses `\Relation`, `\ARelation`, `\Set`, `\fprate`, `\tprate`,
`\fnrate`, and local packages under `sty/`. Existing theorem labels are retained
where practical even when their old names (such as closure_dichotomy) overstate
what the revised theorem actually proves.
