# Prose Auditor Report

**Date**: 2026-02-26
**Paper**: Bernoulli sets: a model for sets with random errors

## Overall Assessment

The writing is generally clear and well-organized. The paper follows a logical progression from definitions to axioms to derived results to applications. The prose is competent technical writing. However, there are several issues with consistency, clarity, and presentation quality.

## Major Issues

### M1. Section 2 (Algebra of Sets) is too long for a background section
**Location**: Section 2, 148 lines
**Problem**: This section reviews elementary set theory (definitions of sets, ordered pairs, Cartesian products, functions, power sets, indicator functions, set operations) that any reader of a mathematics/CS journal paper would know. At 5+ pages, it delays the paper's actual contribution (Section 3) until page 7-8. The approximate sets subsection (Section 2.1) contains material relevant to the paper's contribution, but the pure set theory review does not.
**Suggestion**: Cut Section 2 to ~1 page. Remove the definitions of ordered pairs, Cartesian products, tuples, $n$-fold products, power notation, binary relations, subset, set builder notation, functions, and power sets. Keep only: (a) the notation used in the paper (universal set, complement, union, intersection, indicator function), (b) the approximate sets subsection (Section 2.1) which introduces FPR/FNR/TPR/TNR.

### M2. Inconsistent notation for approximate sets
**Location**: Throughout
**Problem**: The paper uses multiple notations for approximate sets:
- $\tilde{A}$ (tilde notation)
- $\tilde{A}^\varepsilon_\tau$ (superscript/subscript)
- $\tilde{X}[\varepsilon][\tau]$ (bracket notation)
- $\hat{A}$ (hat notation in Section 2.1)
- $\tilde{A}_+$, $\tilde{A}_-$ (positive/negative)
- $\mathcal{A}^{\pm}$ via the \ASet macro

Section 2.1 introduces approximate sets with $\hat{A}$ notation, but Section 3 switches to $\tilde{A}$ and $\tilde{R}$. The transition is never explained. The $\hat{\cdot}$ notation reappears for observed rates ($\hat{\varepsilon}$, $\hat{\tau}$) which creates ambiguity.
**Suggestion**: Settle on one primary notation and use it consistently. The $\tilde{A}^\varepsilon_\tau$ notation is the most information-rich. Explain at first use that $\hat{A}$ in Section 2 is informal and $\tilde{A}$ is the formal probabilistic notation.

### M3. The "probability space" subsection (Section 3.3) is confusing
**Location**: Section 3.3 (sec:prob_model), lines 243-300 of bernoulli_model.tex
**Problem**: This subsection attempts to formalize the probability space but introduces heavy notation ($\vec{A}$, $\tilde{\vec{A}}^\varepsilon_\tau$, $x_{(j)}$) that is used only in this subsection and never again. The Boolean vector notation adds complexity without adding insight. The key content (joint probability factorization, conditional independence) could be stated in 3-4 lines rather than 40+.
**Suggestion**: Compress to: "The sample space is $\Omega = 2^U$. By Axiom 1, the conditional probability of observing $\tilde{A} = B$ given objective set $A$ factorizes as $P(\tilde{A} = B | A) = \prod_{x \in U} P(1_{\tilde{A}}(x) = 1_B(x) | 1_A(x))$." Move the vector notation to an appendix if desired.

## Minor Issues

### m1. Missing tilde in Section 2.1
**Location**: Section 2.1, line 92
**Quoted text**: "Suppose $\hat{A}$ is used as an approximation of $A$."
**Problem**: This is the only section using $\hat{A}$ for approximate sets. The rest of the paper uses $\tilde{A}$.

### m2. Sentence fragment after Definition 2.5
**Location**: Section 2, line 57-58
**Quoted text**: "Since every $x \in X$, given a pair $(x,y) \in f$, $y$ may also be denoted by $f(x)$."
**Problem**: Grammatically awkward. "Since every $x \in X$" is not a complete clause.
**Suggestion**: "Since $f$ is total on $X$, for each $(x,y) \in f$ we write $y = f(x)$."

### m3. "begin" typo in Section 4
**Location**: Section 4, line 11
**Quoted text**: "elements with higher probability of begin tested should be assigned smaller error rates"
**Problem**: "begin" should be "being."

### m4. Inconsistent use of "random approximate set" vs "approximate set"
**Location**: Throughout
**Problem**: The paper alternates between "random approximate set" and "approximate set" without clear distinction. Sometimes "approximate set" refers to a specific realization, sometimes to the random variable.
**Suggestion**: Establish early that $\tilde{A}$ is a *random* approximate set (the random variable) and a realization is an *approximate set* (a specific outcome). Use the terms consistently.

### m5. Figure 1 caption placement
**Location**: Section 4.2, Figure 1 (fig:prec_vs_fprate_and_fnrate)
**Problem**: The caption is placed *above* the figure (lines 309-315 of distributions.tex), which is LaTeX convention for tables but not for figures. Figures should have captions below.
**Suggestion**: Move the \caption command after the \input{img/out.pdf_tex} command.

### m6. The conclusion is thin
**Location**: Section 10 (Conclusion), 17 lines
**Problem**: For a 43-page paper, a 17-line conclusion is inadequate. It merely summarizes what was done without reflecting on implications, limitations, or specific future directions beyond vague gestures at "dependent error models" and "continuous universes."
**Suggestion**: Expand to discuss: (a) specific open problems (e.g., the general space bound of Remark 8.1), (b) connections to type theory (mentioned in passing), (c) potential impact on practical systems, (d) limitations of the element-wise independence assumption in specific applications.

### m7. Appendix section numbering is confusing
**Location**: Appendix
**Problem**: The appendix sections are titled "Proof of corollary 4.2" and "Proof of theorem 4.7" and "Sampling distribution of arbitrary functions" and "Notation Reference." They use \section commands that produce section numbers like A.1, A.2, A.3, A.4. The Notation Reference (A.4) is not a proof and seems out of place in what starts as a "proofs" appendix.
**Suggestion**: Split into Appendix A (Proofs) and Appendix B (Notation Reference). Or provide clearer framing.

### m8. The "uncertain rates" section title is vague
**Location**: Section 7
**Problem**: "Uncertain rates" doesn't convey the content (interval arithmetic for error-rate propagation).
**Suggestion**: "Interval Arithmetic for Uncertain Error Rates" or "Error Rate Propagation under Interval Uncertainty."

### m9. Missing period after displayed equations
**Location**: Multiple places
**Problem**: Several displayed equations that end sentences lack terminal punctuation. Examples include equation blocks in Section 2 (lines 80-84), Section 3.3 (line 135), and others.
**Suggestion**: Add periods or commas after displayed equations as appropriate per mathematical typesetting conventions.

### m10. "Bernoulli set" vs "Bernoulli set model" terminology
**Location**: Throughout
**Problem**: The paper uses "Bernoulli set" to mean both "the abstract model/framework" and "a particular random approximate set that satisfies the axioms." The abstract says "Bernoulli set model" but the body sometimes says "Bernoulli set" when it means "a random approximate set satisfying the Bernoulli axioms."
**Suggestion**: Use "Bernoulli set" for the object and "Bernoulli set model" for the framework consistently.

## Presentation Strengths

1. **Good use of examples**: The Boolean universe example (Example 3.1), the numerical union example (Example 5.1), and the accuracy reparameterization example effectively illustrate abstract concepts.

2. **Clean theorem-proof structure**: The paper follows a clear theorem-proof style with explicit labels and cross-references.

3. **Effective use of remarks**: The BSC remark, axiom economy remark, and monoidal structure remark provide valuable context without disrupting the main flow.

4. **Summary table**: Table 2 (set operation error rates) is a useful reference that consolidates the main results.

5. **Notation reference**: The appendix notation reference is helpful for readers.
