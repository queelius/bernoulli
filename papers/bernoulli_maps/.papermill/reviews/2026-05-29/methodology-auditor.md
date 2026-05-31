# Methodology Auditor Report, bernoulli_maps

**Specialist**: methodology-auditor (experimental design, statistical rigor, reproducibility)
**Date**: 2026-05-29
**Note**: This is a pure-theory paper. There are no experiments, datasets, or simulations in the manuscript. "Methodology" here means: the soundness of the probabilistic modeling assumptions, the reproducibility of the analytic derivations, and whether the quantitative claims (error rates, space bounds) are stated in a way that could be empirically checked or falsified.

## Verdict summary

The modeling methodology in sections 2 to 5 is sound: the assumptions (element-wise independence, composability, Maybe-type channel) are stated explicitly and the derived quantities (loss decomposition, binomial counts, composition rates) follow correctly from them and are in principle Monte-Carlo-checkable. The methodology weakens sharply in sections 6 to 7: the central space-complexity claim is supported by a chain of derivations with a broken link (the section 6.6 success probability), and the paper provides no validation of any kind, while itself acknowledging that the most load-bearing parameter (`rho`) and the composition bounds remain empirically unverified.

## Cross-verification of logic-checker bundle (C1, M1, M2, M3)

The area chair routed the section 6/7 space-complexity findings here to check whether the **headline bound `-log2 eps + mu` bits/element is reproducible** despite the broken intermediate steps.

**Reproduction attempt (independent of the paper's section 6.6 algebra):**
- Stored keys: `m` (take `fnr = 0` first). Mechanism (from Algorithm 1 + Theorem 7.x): find a salt `b` such that all `m` keys collide in their `k = ceil(-log2 eps)` membership bits AND each key's value-bits match its codeword.
- Per-trial success probability under a random oracle: one key fixes the target bucket for free; the other `m-1` must match `k` bits each (`2^{-k(m-1)} = eps^{m-1}`); all `m` values must match `BL(v_j)` bits (`prod_j 2^{-BL(v_j)} = 2^{-m mu}`). So `p = eps^{m-1} 2^{-m mu}`. This is **section 7's** `p`, and it is the correct one.
- Trials to first success: `Q ~ Geometric(p)`, `E[Q] = 1/p = 2^{m mu} eps^{-(m-1)}`.
- Storage is the index of the successful salt, costing about `log2 Q` bits total. Using `log2 E[Q]` (a Jensen upper bound) `= m mu - (m-1) log2 eps`. Dividing by `m`: `mu - ((m-1)/m) log2 eps -> mu - log2 eps` as `m -> infinity`.
- **Conclusion**: the headline bound `-log2 eps + mu` **is reproducible** and correct, using section 7's `p`. It does **not** depend on the section 6.6 `binom{...}(1-eps)^{...}` formula, which is the broken one (logic-checker C1). 

**This confirms the logic-checker's assessment**: the final result stands, the section 6.6 intermediate (`p(eps,fnr)`) is wrong and contradicts section 7, and the cleanest fix is to delete section 6.6's formula and route everything through section 7's `p`. The `fnr`-scaled version `-(1-fnr) log2 eps + (1-fnr) mu` also reproduces if one simply substitutes "stored keys `= (1-fnr)m`" into the same derivation (the lower-bound, uniform-bit-length case); the upper bound `-(1-fnr) log2 eps + mu` requires the separate "degenerate bit length cannot be amortized" argument, which is asserted rather than derived (logic-checker M3). I concur with M3: the lower-bound half is not proven, only the `fnr=0` equality and the upper bound are.

**Net**: headline claim survives; the supporting methodology in section 6.6 is unsound and must be repaired or excised. Severity concurrence: C1 critical, M2/M3 major.

## MAJOR findings

### M5. No validation of any quantitative claim; the paper's own "future directions" concede the gap (source: methodology-auditor)
- **Location**: `conclusion.tex`, "Future directions"; whole paper.
- **Quoted text**:
  > "Monte Carlo validation of the composition error bounds, particularly the dependence on the parameter $\rho$ governing false-positive overlap, remains to be developed."
- **Problem**: The two most novel quantitative results, the `rho`-parametrized composition FPR (`thm:comp-fpr`) and the SHM asymptotic space bound (`thm:shm-space`), have no empirical check. For the composition FPR this matters because `rho` is defined as a probability "that depends on the implementation" (`def:rho`) and the only concrete instance given is the uniform case `rho = |Dod(g)|/|Y|`; without a simulation the reader cannot see that the closed form tracks a real construction. For the SHM, the geometric-trials model assumes an idealized random oracle and "without replacement" salt enumeration (Algorithm 1), and the `O(1/m)` Jensen gap is asserted; a small Monte Carlo over modest `m` would either confirm the convergence to `-log2 eps + mu` or expose constant-factor surprises. The `research/` directory contains Mathematica/SVG artifacts but none are referenced or reported in the text.
- **Why major**: for a theory paper the absence of experiments is not disqualifying, but the paper makes *asymptotic* and *implementation-dependent* claims (`rho`, the `O(1/m)` gap) that are exactly the kind that benefit from a sanity simulation, and the conclusion admits they are unvalidated. At minimum the paper should either (a) add a short Monte Carlo section for the composition rates (cheap: sample two independent Maybe-type maps, compose, estimate FPR/FNR, compare to the closed forms across `rho`), or (b) explicitly scope the paper as analytic and state that validation is deferred to a companion. Right now it does (b) only in one sentence.
- **Suggestion**: Add a one-figure Monte Carlo validating `thm:comp-fpr` across `rho in {0, 0.1, 0.5, 1}` and `thm:comp-fnr` for `k`-fold composition; this is a few dozen lines and would materially raise confidence. The SHM bound can be validated with a random-oracle simulation at `m = 10, 100, 1000`.
- **Confidence**: high.

### M6. The SHM construction's running-time / feasibility is unaddressed; `E[Q] = 2^{m mu} eps^{-(m-1)}` is astronomically large (source: methodology-auditor)
- **Location**: `shm.tex`, Algorithm 1 and `eq:exp_trials`.
- **Problem**: The expected number of trials `E[Q] = 2^{m mu}/eps^{m-1}` grows exponentially in `m`. For even modest maps (say `m = 30`, `mu = 8`, `eps = 2^{-8}`) this is `2^{240+232} = 2^{472}` expected trials. Algorithm 1's `for n = 0 to t` ... `for j = 1 to 2^n` enumerates bit strings, so the construction is exponential-time and infeasible beyond toy sizes. The text says only "the algorithm exhaustively searches for a bit string in the order of increasing size `n`." This is fine for an *existence/optimality* argument (the construction proves the space bound is *achievable in principle*), but the paper presents the SHM as "a concrete algorithm that realizes this bound" (intro contribution 4 and abstract), which overstates its operational status. The reproducibility concern: nobody can run this to check the claim; it is a thought-construction.
- **Suggestion**: reframe the SHM honestly as a *theoretical* construction establishing achievability (like a random-coding argument in information theory), not a practical algorithm. Add one sentence on the exponential expected trials and contrast with practical retrieval structures (binary fuse, BuRR) that hit the same floor in linear time. Do not claim it is "concrete" without that caveat. (This dovetails with the literature-context note that the modern retrieval line is the practical realization.)
- **Confidence**: high.

## MINOR findings

### m7. `def:rho` is well-posed but its "in general depends on the implementation" escape hatch is never closed (source: methodology-auditor)
- **Location**: `composition_new.tex`, `def:rho` and following paragraph.
- **Problem**: `rho` is the single quantity that makes the composition FPR non-trivial, yet the paper gives exactly one worked value (uniform FPs: `rho = |Dod(g)|/|Y|`). Methodologically, a parameter that "depends on the implementation" should come with at least two contrasting instances (e.g., uniform vs a structured FP distribution that concentrates inside or outside `Dod(g)`) so the reader sees the range `rho in [0,1]` is actually exercised. As written, `rho` reads as a free knob introduced to make the algebra close.
- **Suggestion**: give a second instance (e.g., a rate-distorted FP distribution biased toward short codewords, computing the resulting `rho`), or a Monte Carlo (see M5).
- **Confidence**: high.

### m8. The "entropy map" optimality is stated as a maximum-entropy property without an optimization or a comparison class (source: methodology-auditor)
- **Location**: `entropy_maps.tex`, intro paragraph and the three "defining properties."
- **Problem**: The entropy map is called "the canonical one: it achieves the maximum-entropy encoding subject to the rate constraint, using the minimum possible space," and "the least-structured element of the function space ... that still satisfies the Bernoulli axioms." These are appealing characterizations but no max-entropy *program* is written down (objective, constraints, the argmax), and "minimum possible space" is justified only later, asymptotically, by the SHM. The maximum-conditional-entropy property (defining property 3) is asserted, not proved. Methodologically this is a definition masquerading as an optimality theorem.
- **Suggestion**: either state the max-entropy optimization explicitly (maximize `H` of the per-element code subject to `E[length] <= -log2 eps + mu` and the rate constraints) and prove the entropy map is its solution, or soften the language to "a maximum-entropy *construction*" and defer the optimality to the SHM space theorem.
- **Confidence**: high.

### m9. Independence assumptions are reasonable but the "independent sources of randomness" for composition is the strongest and least examined (source: methodology-auditor)
- **Location**: `composition_new.tex`, the paragraph before `def:approx-comp` ("Independence means that the random outcomes ... are determined by independent sources of randomness").
- **Problem**: In any *hash-based* realization (the entropy map / SHM), `f*` and `g*` would share a hash family, and their errors could be correlated (e.g., a key that is "unlucky" in one stage may be systematically unlucky in another if the same seed is reused). The composition theorems assume stage-independence; the paper should note that this requires *independent* salts/seeds per stage and that seed reuse breaks the product formulas. This is the modeling assumption most likely to be violated in practice and it is stated in one clause.
- **Suggestion**: add a remark that independence requires independently sampled hash seeds per stage; otherwise the composed rates are only bounds.
- **Confidence**: medium-high.

## Reproducibility checklist
- Analytic derivations sections 2 to 5: reproducible by hand (I reproduced the composition rates and binomial counts). PASS.
- Analytic derivations section 6.6: NOT reproducible as written (C1/M2). FAIL until repaired.
- Analytic derivation section 7 headline bound: reproducible from section 7's `p` (I reproduced `-log2 eps + mu`). PASS; intermediate proof steps need tightening (logic M1/M3).
- Empirical claims: none made, none validated. The paper is honest that validation is future work, but the SHM "concrete algorithm" framing overpromises (M6).
- Code/data: `research/` artifacts exist but are not cited or reported; cannot be used to verify anything in the text.
