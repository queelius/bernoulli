# Relations revision: mathematical audit

Date: 2026-10-13. Scope: sections/properties.tex, sections/rel_algebra.tex,
and (after root expanded ownership) code/validate.py plus
code/test_math_validation.py. No commits and no manuscript build performed;
root owns final integration and build.

## Corrections made

- **Independent tuples are a scoped special case.** The operator section now
  distinguishes tuple identity from source identity, fixed construction from
  repeated sampling, and independent input constructions from a self-join.
  Selection preserves rates within existing truth classes; it does not make
  a two-rate model first-order.
- **Projection profiles include true-member count.** Fibers are subsets of the
  candidate universe, not merely exact or observed positive tuples. On a full
  Cartesian candidate universe, coordinate projection has constant fan-in;
  restrictions can make fan-in vary. The sufficient marginal partition is
  (k,j), and equal profiles need not be the minimal rate partition. With
  fixed (epsilon,tau)=(.05,.9) and k=3, j=1 gives TPR .90975 while j=2
  gives .9905. Uniform fan-in alone cannot supply a uniform TPR.
- **Projection source-overlap law.** Added thm:project_sources:
  P(Y_s=1)=1-q(A_s) and
  Cov(Y_s,Y_t)=q(A_s\A_t) q(A_t\A_s) q(A_s∩A_t)[1-q(A_s∩A_t)],
  under independent canonical source bits. Pairwise disjoint supports are
  necessary and sufficient for mutual independence only when all participating
  source probabilities are strictly between zero and one. The formula itself
  remains valid at boundary rates. The two-tuple symmetry example has disjoint
  tuple fibers but one shared source. No novelty claim is attached.
- **Join dependence is conditional, not universal.** Shared-left covariance is
  a(1-a)b1 b2, strictly positive exactly when a is interior and both partners
  have positive acceptance probability. Disjoint-source joins remain
  independent. The three negative membership regions and their query weights
  are explicit; the both-absent corner need not understate other regions when
  a channel is noninformative or inversely informative.
- **Worked-example scope repaired.** The displayed true rows do not determine
  candidate fiber size. The independent projection illustration is separate
  from the dependent join-then-project pipeline.

- **Symmetric diagonal fixed.** An off-diagonal orbit has two trials; a diagonal
  orbit has one. Diagonal rates remain (epsilon,tau) after symmetric OR closure.
- **Actual orbit size replaces maximum size in equalities.** OR-closure rates
  use h(O)=|O|; a bound h(O)<=m gives bounds, not equality at m.
  The representation is dependent within orbits and independent between them
  under the independent-tuple construction.
- **Reflexivity is a forced-tuple constraint.** It is not itself the class of all
  unions of a fixed equivalence. Known diagonal insertion is distinct from
  singleton OR closure.
- **Single-valuedness theorem replaced.** For v>=2, a defined row survives with
  q1=(1-epsilon)^(v-1)+(1-tau)(v-1)epsilon(1-epsilon)^(v-2);
  an undefined row survives with
  q0=(1-epsilon)^v+v epsilon(1-epsilon)^(v-1).
  With d defined and u undefined keys the exact probability is q1^d q0^u.
  A lost true value plus one spurious value is still single-valued.
  The old (1-epsilon)^(v-1) check remains valid for the distinct
  no-spurious-value event (or defined-row preservation at tau=1).
  v<=1, zero rates, and empty factors are explicit.
- **Transitivity preservation repaired.** Removed claims that it vanishes
  “fastest,” the argument treating true premises as reported premises, and an
  unjustified product over overlapping triples. Added
  thm:transitive_preservation, the sufficient upper bound
  (1-min(epsilon,tau)^2(1-max(epsilon,tau)))^floor(n/3) for fixed interior rates.
  The proof uses vertex-disjoint triple violation events. Boundary cases need
  separate treatment; empty exact relation with epsilon=0 is a counterexample
  to unconditional vanishing.
- **Repair claims narrowed.** The retained no-equivalence lemma only excludes
  a fixed equivalence whose arbitrary class unions represent all transitive
  relations. It excludes neither other encodings nor other repairs.
  The path theorem proves exactly ceil(log2 k) simultaneous squaring rounds
  and a final size binom(k+1,2); newly added pairs number
  binom(k+1,2)-k. No general repair-complexity lower bound is inferred.
  The old sec:closure_dichotomy label remains for compatibility but its title
  and claims now describe specific constructions rather than a dichotomy.
- **Canonical memory claims narrowed.** Canonicalization preserves marginal
  rates; representative independence is separate from tuple independence.
  Building a quotient reduces input-key count, whereas rewriting queries alone
  does not shrink an existing structure. Neither proves an exact byte reduction.
- **Space accounting scoped.** Exact rate inversion is retained:
  epsilon=1-(1-epsilon_target)^(1/m). At fixed m and small target, the log-rate
  change tends to log2 m. Calling that a per-input-key bit surcharge
  explicitly assumes -log2 epsilon accounting with fixed other costs.
  The familiar zero-FNR membership bound cannot price a two-sided recall
  improvement, since its TPR is already one. Total-memory comparisons need
  construction overhead, attainable TPR/FPR tradeoffs, and key counts.
- **Deletion semantics specified.** Uniform tie-breaking is independent of the
  membership trials, sampled once per row and reused. Its retained-true-value
  formula is proved via the integral for E[1/(1+K)], with the zero-FPR limit.
  Row size affects both rate and work.
- **Partial-function section condensed.** Preserved sec:map and
  def:approx_pfun, moved the material under invariants, replaced equality
  with the full Cartesian universe by a single-valued subset, allowed total
  functions as partial functions, and separated wrong-value errors from
  domain false positives/negatives. Unsupported map-composition claims were
  replaced by a scoped companion citation.

## Validation performed

From repository root:

    bernoulli-py/.venv/bin/python -m pytest \
      papers/bernoulli_relations/code/test_math_validation.py \
      --cov=validate --cov-branch --cov-report=term-missing -q

486 tests passed. Coverage of validate.py was 99% (209 statements, one missed;
38 branches, one partial). The uncovered line was its module entry-point
raise SystemExit(main()); the separate CLI run below exercised that path.
The tests exhaustively enumerate small independent-source laws for:

- defined and undefined row preservation, including rate endpoints;
- global row preservation and the no-spurious-value distinction;
- singleton and doubleton orbits, canonical rates, and deterministic symmetry;
- all pairs of supports on three sources, including degenerate probabilities;
- uniform-fan-in/mixed-member-count counterexample;
- join covariance at interior and boundary rates;
- transitivity preservation on four exact relations over three vertices;
- uniform deletion and its zero-rate limit;
- orbit rate inversion, bounded actual orbit sizes, and the asymptotic surcharge;
- simulation driver output and the deliberately incorrect independence model.

    bernoulli-py/.venv/bin/python papers/bernoulli_relations/code/validate.py \
      --trials 2000000 --seed 20260608

All fitted rows passed the existing tolerance 0.005; maximum absolute
discrepancy was 0.000429. The deliberate independent-join prediction remains
an expected mismatch (.6561 versus observed joint acceptance .728758,
consistent with the correct .729). The manuscript table now matches this
fresh run and includes singleton diagonal and defined/undefined row checks.

    bernoulli-py/.venv/bin/ruff check \
      papers/bernoulli_relations/code/validate.py \
      papers/bernoulli_relations/code/test_math_validation.py

All checks passed. git diff --check for the owned files also passed.

## Integration and limitations

- Root supplies asm:source_model and sec:query_contracts, referenced here.
  All earlier relevant theorem/section labels were retained.
- Root still needs the complete LaTeX/bibliography build and visual inspection.
  The wider empirical table and displayed rate equations need layout review.
- The independent-coin simulation validates algebra under the stipulated law,
  not the accuracy of that law for any compressed filter. The physical-filter
  experiment is separate and owned by the experiment worker.
- No full package tests were run by this worker: these changes do not import
  or modify the Python package. The focused validation suite and CLI run were
  the unit/integration checks for the changed research harness.
- No claim of a new lineage theorem, a universal repair dichotomy, a
  two-sided space lower bound, or complete publication readiness remains in
  these owned sections.
