# Prose Auditor Report

**Date**: 2026-03-19
**Paper**: Bernoulli sets: a model for random approximate sets

## Summary

The writing is generally clear and well-organized. The paper reads well as a foundational exposition. A few notation consistency issues and minor prose improvements are identified. No critical writing problems.

## Findings

### Major Issues

None.

### Minor Issues

**m1: alpha/beta notation overloading in Section 3** (severity: minor)
- In Definition 3.2, $\alpha_i$ denotes the response rate for partition block $B_i$. On line 33, the paper maps $\alpha_1 = \beta$ (TPR) and $\alpha_2 = \alpha$ (FPR) for the second-order model. The reuse of $\alpha$ as both a generic block rate subscript ($\alpha_i$) and the specific FPR statistic ($\alpha$) creates a name collision. A reader seeing "$\alpha_2 = \alpha$" must parse "$\alpha_2$" as the generic block rate for block 2 and "$\alpha$" as the specific FPR, which is confusing.
- **Location**: sections/bernoulli_model.tex, lines 24-33
- **Suggestion**: Use a different letter for generic block rates (e.g., $r_i$) or add a brief clarification that $\alpha$ without subscript always denotes FPR hereafter.

**m2: Complement notation inconsistency between body and notation reference** (severity: minor)
- The paper body uses $A^c$ for set complement (lowercase superscript c), while the notation reference in Appendix B uses $\Set{A}^C$ (uppercase C with set styling).
- **Location**: sections/appendix.tex line 42 vs sections/bernoulli_model.tex line 33
- **Suggestion**: Standardize to one form. The body convention $A^c$ is more common in probability; the notation reference should match.

**m3: Theorem 4.2 PMF subscript inconsistency** (severity: minor)
- The theorem statement writes $p_{\alpha_n}(\hat{\varepsilon} | \varepsilon)$ but the final line of the proof writes $p_{\alpha_n}(\hat{\varepsilon}_n | \varepsilon)$. The subscript $n$ on $\hat{\varepsilon}$ is spurious in the proof (the theorem already conditions on $N=n$).
- **Location**: sections/distributions.tex, line 58 vs line 77
- **Suggestion**: Remove the subscript $n$ from $\hat{\varepsilon}_n$ in line 77 to match the theorem statement.

**m4: Density decomposition equation lacks explicit conditioning** (severity: minor)
- The equation $f(\tilde{X}, \alpha, \beta) = f(\tilde{X} | \alpha, \beta) f(\alpha | R) f(\beta | R)$ is correct given the established notation ($\tilde{X}$ means $\tilde{R}$ given $R=X$), but a reader encountering it in isolation might wonder why $R$ appears on the right but not the left. A brief parenthetical "(recall $\tilde{X}$ denotes $\tilde{R}$ conditioned on $R = X$)" would aid readability.
- **Location**: sections/bernoulli_model.tex, lines 115-119
- **Suggestion**: Add a brief reminder of the notation convention.

### Suggestions

**s1: Remark 3.4 "one response rate per block per set" phrasing**
- The phrase "one response rate per block per set" in the parametric parsimony remark could be misread. In the union example, there are 4 blocks and 2 sets, giving 8 combinations, but only 4 unique parameters because the rate for each block in each set is determined by whether the element is in $A_i$ or not. The phrase could be "two parameters per set ($\varepsilon_i, \tau_i$), for a total of four" to be more explicit.
- **Location**: sections/bernoulli_model.tex, line 60

**s2: Notation reference scope**
- The notation reference includes symbols not used in the active paper (Cartesian product, $n$-fold product, CDF). Since this paper was trimmed from 43 to 18 pages, some notation reference entries are vestigial.
- **Location**: sections/appendix.tex, lines 35-36, 82
- **Suggestion**: Trim the notation reference to symbols actually used in the paper.

**s3: Conclusion companion papers paragraph is repetitive**
- The "Companion papers" paragraph in the conclusion (lines 20-23) repeats nearly verbatim the "Companion papers" paragraph from the introduction (lines 36-38). This repetition is unnecessary in an 18-page paper.
- **Location**: sections/conclusion.tex lines 20-23 vs sections/intro.tex lines 36-38
- **Suggestion**: In the conclusion, abbreviate to a single sentence with citations rather than restating the full descriptions.

## Narrative Arc Assessment

The paper follows a clean logical progression:
1. Introduction frames the gap and contribution
2. Section 2 establishes the classical set-theoretic foundation
3. Section 3 introduces the model (axioms, definitions, composition, probability space)
4. Section 4 derives the distributional consequences
5. Conclusion summarizes and points to companion work

This structure is effective. The balance between formal development and intuitive explanation is appropriate.

## Overall Assessment

The writing is solid. The identified issues are all minor and addressable with small edits.
