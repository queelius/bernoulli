# Logic Checker Report, bernoulli_entropy

**Reviewer role**: Proof correctness, logical chain integrity, claim support
**Date**: 2026-05-29
**Verification**: All asymptotic claims independently re-derived and checked numerically (overflow-safe binomial computations).

## Summary

The paper contains one theorem (joint entropy, Thm 3.1) and one proposition (space lower bound, Prop 4.1) with proofs, plus a remark, an example, and two axioms restated from the companion paper. Both proofs are essentially correct. Result 1 is fully rigorous up to its stated asymptotic regime. Result 2 (the lower-bound proof) is correct but its final step is stated slightly more strongly than the derivation literally supports: the derived inequality converges to the claimed bound *from below*, so the conclusion is an asymptotic (n -> infinity) bound carrying a vanishing slack, which the prose does not flag.

## Findings

### MAJOR-1: Lower-bound proof concludes an asymptotic bound as if exact; convergence is from below
- **Location**: `sections/space_complexity.tex`, Prop 4.1 proof, the final display chain (lines 48-58) ending "giving `-log2(epsilon)` bits per element."
- **Quoted text**: "For fixed $\p$ as $n \to \infty$, $\binom{n}{\p} \sim n^\p / \p!$ and $\binom{\p + \fprate n}{\p} \sim (\fprate n)^\p / \p!$, so $B \geq \log_2 \frac{n^\p}{(\fprate n)^\p} = \p \log_2 \frac{1}{\fprate} = -\p \log_2 \fprate$, giving $-\log_2 \fprate$ bits per element."
- **Problem**: The honestly-derived inequality is `B >= log2 C(n,p) - log2 C(p+eps(n-p), p)`. I evaluated the RHS exactly: for fixed p it approaches `-p*log2(eps)` **monotonically from below** (e.g., p=3, eps=0.1: RHS = 9.253, 9.889, 9.958, 9.965 bits at n = 1e2..1e5, target 9.96578, always below). Replacing both binomials by their leading asymptotics `~ x^p/p!` *raises* the RHS to its limit. So the chain "`B >= [RHS] = -p log2 eps`" is not a valid finite-n inequality; only `B >= -p log2(eps) - o(1)` holds, i.e., the bound is asymptotic in the universe size with a vanishing additive slack. The *result* is correct (it is the standard way such bounds are stated), but the proof should say the bound holds as `n -> infinity` (equivalently for the countably infinite universe), not present it as an exact per-element inequality.
- **Suggestion**: Change the last sentence to make the asymptotic explicit, e.g.: "Hence `B >= -p log2(eps) - o(1)` as `n -> infinity`, i.e., at least `-log2(eps)` bits per element in the countably-infinite-universe limit." Optionally bound the lower-order term. This is a one-line fix; the mathematics is sound.
- **Cross-check (methodology-auditor)**: I asked whether the regime is reproducible. It is: holding p fixed while n -> infinity is exactly the "fixed finite objective set inside a countably infinite universe" model the proposition states, so the regime is internally consistent. The slack is genuinely o(1) and vanishes, so the bound is honest. Conclusion: keep the finding at MAJOR for rigor of *statement*, but it is not an error of *fact*. Both agree the result holds.

### MAJOR-2: "Yao's minimax principle" invoked without justification or citation
- **Location**: `sections/space_complexity.tex`, Prop 4.1 proof, line 25.
- **Quoted text**: "It suffices to prove the bound for deterministic encodings; the extension to randomized data structures follows from Yao's minimax principle."
- **Problem**: This is the load-bearing step that upgrades the result from deterministic to randomized data structures (the generality the proposition claims via "expected bit length"). It is asserted in one sentence with no citation and no statement of how the principle applies (what is the distribution over inputs, what is the cost measure, why does the deterministic bound transfer). Yao 1977 is not in the bibliography (confirmed: 8-entry bib has no Yao). For an information-theoretic lower-bound paper, this is the step a referee will scrutinize most. As written it is a correct-sounding but unsupported claim.
- **Suggestion**: (a) Cite Yao, "Probabilistic Computations," FOCS 1977. (b) Add one or two sentences instantiating the principle: fix the hard input distribution (uniform over size-p subsets of [n]), note that a randomized data structure is a distribution over deterministic ones, and that its expected cost on the worst input is at least its expected cost under the hard distribution, which is at least the deterministic bound. This makes the reduction checkable.

### MINOR-1: Theorem 3.1 regime and the conditioning premise are mutually consistent, but "$\Entropy{\FP_m,\FN_m}$" hides a subtlety worth a clause
- **Location**: `sections/entropy.tex`, Thm 3.1 statement (lines 16-30) and proof.
- **Quoted text**: "By \cref{asm:element_indep}, the random error counts $\FP_m$ and $\FN_m$ are conditionally independent given $m$ positives."
- **Problem**: The entropy `H(FP_m, FN_m)` is a *conditional* entropy given m (and given fixed rates eps, omega treated as constants here, not the random block rates of Axiom 2). The additivity `H(FP_m,FN_m)=H(FP_m)+H(FN_m)` uses independence, which is correct. But the notation writes an unconditional `H(.,.)` for what is conditional on m and on the rates being deterministic. Section 3.1 then *does* handle random POS, which is good, but the rates are never marginalized. A reader could conflate the fixed-rate `eps` here with the random `alpha_i` of Axiom 2.
- **Suggestion**: Add a half-sentence after the theorem statement: "Here eps, omega are treated as fixed (the expected rates); m is given. Section 3.1 relaxes the fixed-m assumption." This removes the ambiguity for one line of cost.

### MINOR-2: Verified-correct items (recorded for completeness, no action)
- **Binomial entropy expansion** (`eq:binomial_entropy_asymp`): correct. Numerically, exact entropy minus asymptotic scales as O(1/n) (n=100,p=0.3: diff -0.00095; n=1e4,p=0.5: diff < 1e-5). 
- **Joint-entropy algebra**: the combination of the two half-expansions into `log2(2*pi*e) + (1/2)log2((u-m)*m*eps(1-eps)*omega(1-omega))` is algebraically exact (verified).
- **Error-term combination** `O(1/(u-m)) + O(1/m) = O(u/(m(u-m)))`: this is an *exact* identity `1/(u-m)+1/m = u/(m(u-m))`, not merely asymptotic. Correct.
- **Example (expected FP marginal)**: `E[FP] = eps*(u - E[POS]) = eps*E[NEG]`. Correct by linearity over the conditioning identity `E[FP_p] = (u-p)*eps`.
- **Bloom efficiency**: `optimal/Bloom = (-log2 eps)/(-(1/ln2)log2 eps) = ln2 approx 0.69`. Correct, and the figure's two curves (`-ln(x)/ln2` and `-ln(x)/ln2/ln2`) match the stated formulas.

### SUGGESTION-1: State the additive decomposition for the random-POS case as the chain rule it is
- **Location**: `sections/entropy.tex`, eq:joint_entropy_pos (lines 90-96).
- The decomposition `H(POS,FP,FN) = H(POS) + H(FP|POS) + H(FN|POS)` is the chain rule plus conditional independence of FP,FN given POS. It is correct but presented as a bare equation. Naming it ("by the chain rule and conditional independence given POS") would make the logical step explicit and self-contained.

## Logical chain integrity

- Intro contributions map exactly onto the two results (Thm 3.1, Prop 4.1) and the open problem (Rem 4.2). No overclaim in the contribution list.
- Abstract claims match the body: "decomposes additively," "closed-form asymptotic expansion," "restating and proving the classical result," "Bloom achieves ln2 approx 69%," "general case remains open." All supported.
- The open-problem framing (Rem 4.2 and conclusion) is logically careful: it correctly identifies *why* the pigeonhole step fails when false negatives are allowed (input sets are no longer subsets of Q(r)) and correctly labels the heuristic `-tau*log2(eps)` as *not* a valid lower bound. This is a strong, honest piece of reasoning.

## Confidence
High. Both proofs were re-derived and the asymptotics checked numerically across multiple parameter regimes. The two MAJOR items are about *rigor of statement and citation of a load-bearing step*, not about incorrect results.
