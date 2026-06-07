# Methodology Audit

**Paper**: A Forward (epsilon, omega) Calculus for Quantum Readout Error
**Date**: 2026-06-07
**Reviewer role**: methodology-auditor

This is a theory/perspective paper with **no experiments by design**
(sec:scope item 5 says so explicitly). Per the review brief, experimental and
statistical-rigor concerns are de-weighted. What remains in scope for a
methodology audit of a theory paper:

1. Are the modeling assumptions stated before they are used, and used
   consistently?
2. Is the independence assumption (the load-bearing one) tracked honestly
   throughout, including where it would fail?
3. Is the worked example (Table 1) a *reproducible computation*, i.e. would an
   independent party get the same numbers from the stated formulas?
4. Does the paper overclaim relative to what it actually establishes?

## Reproducibility of the one computation

Table 1 is the paper's only "result with numbers." It is fully reproducible:
the two formulas (eq:syndrome-exact, eq:syndrome-lin) are printed, the inputs
(six (q,n) pairs) are printed, and recomputing from the formulas reproduces all
six rows to every printed digit (independently confirmed). There is no hidden
data, no fitted parameter, no random seed. For a theory paper this is the
correct standard and the paper meets it. **No reproducibility finding.**

I would still encourage (Suggestion) shipping the trivial script that generates
Table 1 (5 lines of Python) as an ancillary file, so the table is regenerable
on demand and the "costs nothing, it is one product" claim is literally
executable. The framework already has a Python package (bernoulli-py); a
one-cell notebook would close the loop.

## Assumption hygiene (the real methodology question here)

The paper's central methodological move is to replace the quantum measurement
with a classical channel on the diagonal sector of the density matrix. This is
where a theory paper can quietly cheat. It does not.

- **Diagonal-sector faithfulness** is stated in the abstract, restated in the
  introduction ("Why this is sound, and where it stops"), proved-by-assertion in
  sec:channel ("Faithfulness is a hypothesis, stated honestly"), and bounded
  again in sec:scope item 3 (Bell / Kochen-Specker / Fine named as the
  obstructions outside scope). The "can only add probabilities, never cancel, so
  no slot for interference" argument is the right informal justification and is
  stated four times consistently. This is exemplary scope discipline.

- **Independence** is the assumption every closed form rests on. It is declared
  once at the head of sec:calculus ("We assume the channels are mutually
  independent") and is genuinely used by every proof. sec:scope item 2 names the
  failure mode (measurement crosstalk, the CTMP regime) and labels the
  correlated extension as future work. The honesty is good. **One methodological
  gap**: the paper never quantifies or bounds how wrong the independent calculus
  is when crosstalk is present. It says crosstalk "exists" and is "future work,"
  but offers no sensitivity statement, not even a qualitative "the independent
  prediction is a lower/upper bound on the correlated rate" claim. For a paper
  whose Table 1 thesis is "the field's linear rule overestimates by tens of
  percent," a reader will reasonably ask "and how far off is YOUR rule when the
  independence you assume fails?" That question is currently unanswered. This is
  a **Major** scope/positioning gap (not a correctness gap): the paper's own
  rule has an unquantified error bar of exactly the kind it criticizes the
  linear rule for, and the asymmetry of the criticism should be acknowledged or
  partially closed (even a single inequality or a one-paragraph worst-case
  crosstalk sketch would suffice).

- **Symmetric-rate simplification in Table 1.** Section 4 sets q_i = q "for
  clarity" while claiming the asymmetric corollary "handles the asymmetric and
  inhomogeneous case verbatim." That claim is true (cor:parity-asym is the
  general form and Table 1 is its all-equal specialization), but the paper's
  headline novelty is the *asymmetric* calculus, and the single worked example
  is *symmetric*. The asymmetry never appears in a number. This is a
  **Major** presentation/methodology gap: the paper would be substantially
  stronger if Table 1 (or a companion row/table) showed a genuinely asymmetric,
  inhomogeneous syndrome bit, so the two-rate machinery the paper is built to
  sell actually does visible work somewhere. As written, every number in the
  paper is reproducible from the *symmetric* single-rate identity that the paper
  itself says is classical and not its contribution.

## Overclaim check

The contribution statements are carefully hedged ("complementary to, not
competitive with" mitigation; "forward not inverse"; the explicit
not-claimed/claimed list in sec:scope item 4). I did not find an overclaim. If
anything the paper under-demonstrates its own novel piece (see the symmetric-
table point above).

## Findings

- **Major (M-meth-1)**: The independence assumption is the paper's load-bearing
  hypothesis, and the paper criticizes the linear rule for being inaccurate, yet
  never bounds or characterizes its own inaccuracy when independence fails
  (crosstalk). Add at least a qualitative sensitivity statement or a worst-case
  bound, or explicitly frame the independent prediction as a named reference
  point against which crosstalk corrections are measured.
- **Major (M-meth-2)**: The single worked example is symmetric (q_i = q), so the
  paper's headline asymmetric two-rate machinery never produces a concrete
  asymmetric number. Add an asymmetric/inhomogeneous instance (e.g. a syndrome
  bit with T1-biased ancillas at different epsilon_i, omega_i) so the novel
  content is demonstrated, not only asserted.
- **Suggestion (S-meth-1)**: Ship the 5-line Table 1 generator (or a bernoulli-py
  notebook cell) as an ancillary artifact so the computation is regenerable.

No Critical methodology findings. The theory paper's methodology (stated
assumptions, honest scope, reproducible single computation) is sound; the two
Major findings are about *demonstrating* the contribution, not about
correctness.
