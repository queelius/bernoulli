# Logic Checker Report

**Date**: 2026-02-26
**Paper**: Bernoulli sets: a model for sets with random errors

## Summary

The paper presents 24 theorems, 3 propositions, 14 corollaries, and 2 axioms. The logical structure is generally sound: theorems build on axioms and prior results in a clear dependency chain. Most proofs are correct. I identify one critical issue and several minor issues below.

## Critical Issues

### C1. Theorem 3.3 (composition rates): theorem statement and proof contain an algebraic error
**Location**: Section 3.3, Theorem 3.3 (thm:composition_rates), lines 141-152 of bernoulli_model.tex
**Quoted text (theorem statement)**: "...a true positive rate $\tau\tau' + \omega\varepsilon'$ and false positive rate $\varepsilon\tau' + \eta\varepsilon'$."
**Quoted text (proof, line 148)**: "$\tau' \cdot \tau + \omega' \cdot \varepsilon = \tau\tau' + \omega\varepsilon'$"
**Quoted text (proof, line 151)**: "$\varepsilon' \cdot \tau + \eta' \cdot \varepsilon = \varepsilon\tau' + \eta\varepsilon'$"

**Problem**: The proof correctly derives the composed rates via the law of total probability as:
- Composed TPR = $\tau'\tau + \omega'\varepsilon$ (inner TPR times outer TPR, plus inner FNR times outer FPR)
- Composed FPR = $\varepsilon'\tau + \eta'\varepsilon$ (inner FPR times outer TPR, plus inner TNR times outer FPR)

However, the proof then claims these equal $\tau\tau' + \omega\varepsilon'$ and $\varepsilon\tau' + \eta\varepsilon'$ respectively, and the theorem statement uses these latter expressions. These equalities are FALSE in general.

**Verification**: Let $\varepsilon = 0.1$, $\tau = 0.9$ (outer), $\varepsilon' = 0.3$, $\tau' = 0.6$ (inner), so $\omega = 0.1$, $\omega' = 0.4$, $\eta = 0.9$, $\eta' = 0.7$.
- Correct composed TPR: $\tau'\tau + \omega'\varepsilon = 0.6 \times 0.9 + 0.4 \times 0.1 = 0.58$
- Theorem's TPR: $\tau\tau' + \omega\varepsilon' = 0.9 \times 0.6 + 0.1 \times 0.3 = 0.57$
- Correct composed FPR: $\varepsilon'\tau + \eta'\varepsilon = 0.3 \times 0.9 + 0.7 \times 0.1 = 0.34$
- Theorem's FPR: $\varepsilon\tau' + \eta\varepsilon' = 0.1 \times 0.6 + 0.9 \times 0.3 = 0.33$

The equalities $\tau'\tau + \omega'\varepsilon = \tau\tau' + \omega\varepsilon'$ hold only when $\omega'\varepsilon = \omega\varepsilon'$, i.e., $(1-\tau')\varepsilon = (1-\tau)\varepsilon'$, which is not a general identity.

**Note on downstream impact**: Theorem 3.4 (two-fold composition with subscripted rates) appears to state the formula correctly using the subscript convention ($\varepsilon = \varepsilon_1\tau_2 + \eta_1\varepsilon_2$), which matches the correct formula when subscript 1 = inner and subscript 2 = outer. However, the Figure 3 plot of k-fold composition uses iterated application of the *same* rates ($\varepsilon = \varepsilon' = 0.05$, $\tau = \tau' = 0.90$), in which case the erroneous equality $\omega'\varepsilon = \omega\varepsilon'$ happens to hold (both sides equal $0.1 \times 0.05 = 0.005$). So the figure is correct despite the bug.

**Suggestion**:
1. Correct the theorem statement to: "...a true positive rate $\tau'\tau + \omega'\varepsilon$ and false positive rate $\varepsilon'\tau + \eta'\varepsilon$."
2. Remove the false equalities from the proof (lines 148 and 151). Simply state the correct formulas directly.
3. Verify Theorem 3.4 to ensure its subscript convention is consistent with the corrected Theorem 3.3.

**Confidence**: High (verified by counterexample)

## Major Issues

### M1. Proposition 3.1 silently assumes i.i.d. errors within partition blocks
**Location**: Section 3, Proposition 3.1 (prop:element_rates)
**Quoted text**: "By Axiom 1, for any single element $x \notin A$, $P(1_{\tilde{A}}(x) = 1) = \varepsilon$"
**Problem**: Axiom 1 states mutual independence of error events across elements. It does not state that each element has the same error probability. The rates $\varepsilon$ and $\tau$ are introduced in eqs (3.3)-(3.4) as *sample averages* over elements. For the proposition to hold, one needs the additional assumption that all elements within a partition block have identical error probabilities (i.i.d., not just independent). This is the standard assumption for Bloom filters and similar structures, but it is not stated as an axiom.
**Suggestion**: Add to Axiom 1 (or state separately) that errors are identically distributed within each partition block, not merely independent. This is implicitly assumed throughout but never stated.
**Confidence**: High

### M2. The claimed equality in the proof of Theorem 4.7 (PPV approximation) uses an unexplained Taylor remainder
**Location**: Section 4.2, Theorem 4.7 and Appendix A.2
**Problem**: The PPV approximation uses a second-order Taylor expansion of $f(t,f) = t/(t+f)$ around the means. The result is stated with "$\approx$" but no bound on the approximation error is given. For a mathematical paper, either the approximation should be qualified with an explicit error bound (e.g., "the error is $O(1/n^2)$") or the result should be stated as an asymptotic expansion.
**Suggestion**: Add a brief discussion of when the Taylor approximation is accurate (e.g., when the coefficient of variation of TP and FP is small) and provide an error bound.
**Confidence**: Medium

## Minor Issues

### m1. Multiple results stated without proof via "follows the same logic"
**Location**: Theorems 4.4, 4.5; Corollaries 4.3, 4.4; Theorem 4.9
**Problem**: At least five results are stated with "the proof follows the same logic as..." without even a one-line sketch. While this is common practice, a self-contained paper should either provide the proofs or state precisely which substitutions to make.
**Suggestion**: For each such result, add a parenthetical: "(replacing $\varepsilon$ with $\omega$, $n$ with $p$, and negatives with positives)."

### m2. Almost-sure convergence proof (Appendix A.1) has a gap
**Location**: Appendix, Section A.1 (app:cor_fpr_as_vareps)
**Quoted text**: "As $\epsilon$ goes to 0 $\lim_{n \to \infty} FP_n$ converges almost surely to $\varepsilon n$"
**Problem**: The Hoeffding bound gives convergence in probability for each fixed $\epsilon$. For almost-sure convergence, one needs summability of the tail probabilities. Since $\sum_n 2e^{-2\epsilon^2 n} < \infty$ for any fixed $\epsilon > 0$, the Borel-Cantelli lemma yields a.s. convergence, but this step is not stated.
**Suggestion**: Add: "Since $\sum_{n=1}^{\infty} 2e^{-2\epsilon^2 n} < \infty$, the Borel-Cantelli lemma yields almost sure convergence."

### m3. Entropy theorem cites wrong axiom
**Location**: Section 8, Theorem 8.1
**Quoted text**: "By Axiom 2, the random error counts $FP_m$ and $FN_m$ are conditionally independent given $m$ positives."
**Problem**: Conditional independence of FP and FN given fixed $m$ positives follows from Axiom 1 alone (element-wise independence), since FP depends on elements in $A^c$ and FN depends on elements in $A$, which are disjoint. Axiom 2 concerns independence of rate *parameters*, not of counts.
**Suggestion**: Replace "By Axiom 2" with "By Axiom 1 (element-wise independence), since $FP_m$ and $FN_m$ depend on disjoint sets of elements."

### m4. Asymptotic FNR subscript inconsistency
**Location**: Section 4.1, equation after Theorem 4.6
**Quoted text**: "$\beta_n \xrightarrow{d} \mathcal{N}(1-\tau, \tau(1-\tau)/p)$"
**Problem**: The subscript on $\beta$ is $n$ (number of negatives) but the variance uses $p$ (number of positives). The false negative rate should be subscripted by $p$.
**Suggestion**: Change $\beta_n$ to $\beta_p$.

### m5. Definition of model order: $n=0$ is degenerate
**Location**: Section 3, Definition 3.1
**Quoted text**: "A zeroth-order model ($n = 0$) is the exact set."
**Problem**: If the order equals the number of partition blocks and $n = 0$, the partition has zero blocks, which doesn't cover $U$. The intended meaning is "no errors," not "empty partition."
**Suggestion**: Rephrase: "We adopt the convention that $n = 0$ denotes the degenerate (exact) case with no error-bearing partition blocks."

## Logical Strengths

1. **Clean axiomatic structure**: The two-axiom foundation is elegant. Remark 3.2 correctly identifies which results need which axiom.
2. **De Morgan duality**: The union/intersection duality is correctly exploited throughout Section 5.
3. **Set difference derivation**: The reduction to complement + intersection (Theorem 5.5) is cleanly executed.
4. **Space complexity bound**: Proposition 8.1 gives a correct information-theoretic lower bound. The acknowledgment that the general case remains open (Remark 8.1) is appropriate.
5. **Closure grammar**: The formal grammar characterizing positive/negative-preserving expressions (eqs 5.13-5.14) is a nice contribution.
