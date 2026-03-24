# Logic Checker Report

**Paper**: Bernoulli sets: a model for sets with random errors
**Date**: 2026-02-27

## Summary
The paper's logical structure is generally sound. The axiomatic development from two axioms (element-wise independence and conditional independence of block rates) to the derived results is well-organized. The proofs are mostly correct, though some have minor gaps in rigor.

## Findings

### Critical Issues
None.

### Major Issues

**M1. Space bound proof has a logical gap (Proposition 8.1, entropy.tex lines 130-162)**
- **Severity**: Major
- **Confidence**: High
- The proof uses $\binom{|Q(r^*)|}{p} \leq \binom{p + \fprate(n-p)}{p}$ where $Q(r^*)$ is the response set of a specific state $r^*$ found by pigeonhole. However, $|Q(r^*)| \leq p + \fprate(n-p)$ is not justified. The bound $\Expect{|Q(r)|} \leq p + \fprate(n-p)$ holds in expectation over random sets $S$, but $Q(r^*)$ is a fixed set and its size could be up to $n$.
- **Suggestion**: The standard approach (Carter et al. 1978) uses a counting argument: the total number of (set, state) pairs where the set is encoded by the state is $\binom{n}{p}$, and for each state $r$, at most $\binom{|Q(r)|}{p}$ sets can be encoded. Since $\sum_r \binom{|Q(r)|}{p} \geq \binom{n}{p}$ and the average $|Q(r)|$ is bounded, a convexity argument completes the proof. Consider citing the original result with attribution.

**M2. The claimed novelty of Remark 3.1 (BSC connection) is not fully distinguished from prior art (bernoulli_model.tex lines 40-44)**
- **Severity**: Major
- **Confidence**: Medium
- The remark says "The novelty of the present framework is not the per-element channel model...but the set-level compositional algebra." This is an important distinction, but the composition theorem itself (Theorem 3.1) IS a standard BSC channel composition (matrix multiplication of stochastic matrices). The novelty claim should more precisely identify what is new: the systematic derivation of partition-weighted error rates for set operations (Section 5), not the composition theorem per se.
- **Suggestion**: Strengthen the novelty claim by being more specific about which results are new vs. which are applications of classical channel theory.

### Minor Issues

**m1. Axiom 1 conflates two properties (bernoulli_model.tex lines 12-21)**
- The axiom states both mutual independence AND identical distribution within partition blocks. These are logically distinct properties and could be separated for clarity.
- **Suggestion**: Split into Axiom 1a (mutual independence) and Axiom 1b (identical distribution within blocks).

**m2. Proposition 3.1 lacks a proof (bernoulli_model.tex lines 63-69)**
- The proposition states that $E[\alpha] = \fprate$ and $E[\beta] = \tprate$, claiming this follows from Axiom 1. While straightforward, a one-line proof would complete the logical chain.
- **Suggestion**: Add "Proof: By Axiom 1, each $\mathbf{1}_{\tilde{A}}(x)$ for $x \notin A$ is Bernoulli($\fprate$). By linearity of expectation, $E[\alpha] = E[\frac{1}{n}\sum_{x \notin A} \mathbf{1}_{\tilde{A}}(x)] = \fprate$."

**m3. The proof of Theorem 3.2 (twofold composition) is overly terse (bernoulli_model.tex lines 175-181)**
- It simply says "follows by applying Theorem 3.1." The recursive claim deserves at least a sentence on why the composed set satisfies the Bernoulli axioms (i.e., why the outer approximation treats the inner set's indicators as conditioning variables).
- **Suggestion**: Add a sentence explaining that the inner approximation produces a set whose indicators are i.i.d. Bernoulli by Axiom 1, and the outer approximation operates on these indicators independently.

**m4. Mixed use of "false positive rate" for both the parameter and the random variable (throughout)**
- The paper uses $\fprate$ for the expected FPR and $\alpha$ for the random (sample) FPR, but the text sometimes says "false positive rate $\fprate$" when it means the parameter and sometimes when it means the expectation. This distinction is important for the interval arithmetic section.
- **Suggestion**: Be consistent: always say "expected FPR $\fprate$" for the parameter and "realized FPR $\alpha_n$" for the random variable.

**m5. The error term in the joint entropy (Theorem 8.1, eq. 8.1) has an implicit assumption (entropy.tex line 27)**
- The error term $\mathcal{O}(u/(m(u-m)))$ assumes both $m$ and $u-m$ grow. If $m$ is fixed as $u \to \infty$, the error is $\mathcal{O}(1/m)$, which may not be small.
- **Suggestion**: State the asymptotic regime explicitly (e.g., "as $u \to \infty$ with $m/u$ bounded away from 0 and 1").

### Suggestions
1. The paper would benefit from a theorem numbering summary or "roadmap" showing the dependency graph of the main results.
2. The relationship between model order (Definition 3.1) and the partition weights in Section 5 could be made more explicit. The composed set is higher-order precisely because the partition has more blocks.
