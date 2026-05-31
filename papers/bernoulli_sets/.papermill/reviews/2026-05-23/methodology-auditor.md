# Methodology Auditor Report

## Approach

This is a theoretical paper. There are no experiments, datasets, or implementations to audit. Methodology audit focuses on: (a) the axiomatic methodology, (b) the proof methodology, (c) reproducibility of any computed quantities, (d) appropriateness of the abstractions.

## Axiomatic Methodology

The paper introduces two axioms (element-wise independence; conditional independence of block rates) and derives all results from them. Remark 3.2 (axiom economy) is excellent methodology: it explicitly notes that most results follow from Axiom 1 alone, and identifies precisely where Axiom 2 is needed (when R is uncertain). This is the kind of explicit dependency tracking that strengthens an axiomatic paper.

The axioms themselves are well chosen:
- Axiom 1 (element-wise independence) is the natural minimal assumption matching the physical structure of hash-based filters.
- Axiom 2 (conditional independence of block rates given R) is needed only when the rates themselves are uncertain, which is an extension addressed in companion papers.

The model-order definition (Definition 3.1) is a small but important methodological contribution: it provides a uniform parameterization of the complexity of the error model, with zeroth-order (exact), first-order (symmetric), and second-order (positive-negative) as natural cases of a general n-th order family.

## Proof Methodology

All proofs use standard probability theory tools (linearity of expectation, Bernoulli trial composition, CLT, Hoeffding inequality, Borel-Cantelli). The proofs are short, often condensed, but never wrong (per logic-checker). The "follows the same logic" pattern for Theorems 4.3, 4.4, and Corollaries 4.1, 4.3 is acceptable for symmetric results but could be tightened.

#### M1 (Minor): "Follows the same logic" proofs lack explicit substitution
- **Location**: `sections/distributions.tex` lines 132, 142, 156.
- **Quoted text**: "The proof follows the same logic as the proof for \cref{thm:fpr}, with $\FN_p \sim \bindist(p, \fnrate)$ in place of $\FP_n \sim \bindist(n, \fprate)$." and similar for other places.
- **Problem**: Three theorems and one corollary use this pattern. While correct, it is unfriendly to readers who want to verify each claim. The substitution should be spelled out explicitly: which variable replaces which, and at which step does each substitution apply.
- **Suggestion**: For each "by analogy" proof, add a one-line substitution mapping. For Theorem 4.4: "Substitute (FN, p, omega) for (FP, n, epsilon) throughout the proof of Theorem 4.2." For Corollary 4.3: "Substitute (TP, p, tau) for (FP, n, epsilon) and use TP_p = p - FN_p instead of TN_n = n - FP_n."

## Reproducibility

The composition figure (Figure 2) lists 42 data points. Each was independently recomputed from the stated parameters (fprate=0.05, tprate=0.90) by the recurrence T_{k+1} = T_k * tau + (1 - T_k) * eps. All 42 values match exactly. The stationary point eps/(eps + omega) = 1/3 is visible in the figure and verified.

The `code/` directory contains two C++ Monte Carlo simulations (`ppv.cpp` and `bin_class_measures_sim.cpp`). These are not referenced from the paper and pertain to classification measures (extracted to bernoulli_classification_measures). The `data/` directory contains 17 CSV files, none used by the active paper. These are vestiges of the pre-extraction manuscript.

#### M2 (Suggestion): Decide on the fate of code/ and data/
- **Problem**: 17 CSVs and 2 C++ simulations are present but unused by the compiled paper. They distract a code-reviewing reader and inflate the repository.
- **Suggestion**: Either (a) move them to the appropriate companion paper repository (bernoulli_classification_measures), or (b) keep them with a `README` explaining they support companion papers.

## Abstractions

The ADT formulation (Section 3.1) is the methodological centerpiece. The abstract type signature `\SetContains : U \times T \to \{0,1\}` together with the constructor `\ctor{\fprate}{\tprate} : 2^U \to T` and the two probability axioms (eqs. 3.5, 3.6) is a clean specification. The "interchangeable in the frequentist sense" claim (line 142) is the right strength: not pointwise equivalence (which would be false for two different filters with the same rates), but distributional equivalence in the limit.

#### M3 (Minor): "Frequentist sense" claim could be tightened
- **Location**: `sections/bernoulli_model.tex` line 142.
- **Quoted text**: "Two data types that model Bernoulli sets with the same expected error rates are interchangeable in the frequentist sense: at the limit of repeated independent runs, they produce the same distribution over outcomes."
- **Problem**: "The same distribution over outcomes" is slightly ambiguous. For two random positive approximate sets with rate fprate, individual realized sets differ, but the marginal distribution of `\mathbf{1}_{\tilde{A}}(x)` for any fixed x is identical. The joint distribution over `\{\mathbf{1}_{\tilde{A}}(x) : x \in U\}` is also identical under Axiom 1.
- **Suggestion**: Replace "at the limit of repeated independent runs, they produce the same distribution over outcomes" with "they induce the same joint distribution on `\{0,1\}^U` (the indicator vector of the approximate set)".

## Self-containment

The paper is methodologically self-contained: every derived result has its premises stated in the paper itself. No proof imports a lemma from a companion paper.

## Validity of the ADT abstraction for cipher-maps and trapdoor-computing

I checked whether downstream papers can safely take this paper's ADT as a black box. The cipher-maps paper (sec. 6, "Relationship to the Bernoulli Model") cites three facts: (i) the axioms, (ii) the composition formula `\eta_{g \circ f} \leq 1 - (1-\eta_f)(1-\eta_g)`, and (iii) the Bernoulli Boolean as the atomic case from which higher types are built. Facts (i) and (iii) are supplied here. Fact (ii) is the composition formula derived in Theorem 3.2 (in a form that gives equality, not inequality, under the deterministic-seed assumption in cipher-maps). The downstream usage is faithful.

## Recommendation

Methodologically the paper is sound. Tighten the "follows the same logic" proofs, clarify the frequentist-interchangeability claim, and decide on the code/ and data/ directories.
