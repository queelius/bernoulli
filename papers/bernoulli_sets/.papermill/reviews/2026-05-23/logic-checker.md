# Logic Checker Report

## Verification Method

Each theorem, proposition, corollary, and definition was traced from premises to conclusion. Numerical data in the composition figure was independently recomputed.

## Findings

### Verified correct

- **Proposition 3.1** (expected sample rates). Linearity of expectation under Axiom 1 yields E[alpha] = fprate and E[beta] = tprate. Proof correct.
- **Theorem 3.2** (composition rates). Standard product of binary channel transition matrices. Proof correct, matches Cover and Thomas channel composition.
- **Theorem 3.3** (twofold composition). Direct application of 3.2; the recursion `\Set{A}^{\sigma^k} = (\Set{A}^{\sigma^{k-1}})^\sigma` is consistent.
- **Theorem 4.1** (FP_n binomial). Bernoulli trials with shared rate are binomial. Correct.
- **Theorem 4.2** (alpha_n distribution). Mean and variance match the scaled binomial. Correct.
- **Corollary 4.1** (TN_n distribution). Trivially follows. Correct.
- **Corollary 4.2** (alpha_n almost-sure convergence). Hoeffding + Borel-Cantelli proof in appendix is the standard one. Correct.
- **Theorem 4.3** (FN_p binomial), **Theorem 4.4** (beta_p), **Corollary 4.3** (TP_p): proofs by analogy with the FP side, valid.
- **Theorem 4.5** (asymptotic normality of alpha_n and TPR_p). Direct CLT application. Correct.
- **Confidence-interval theorem** (eq:conf_fpr, eq:conf_tpr). Standardization argument is the textbook construction. Correct.
- **Composition figure data** (line 226 onwards). I recomputed all 21 (k, TPR, FPR) tuples by the recurrence T_{k+1} = T_k * tau + (1 - T_k) * eps and F_{k+1} = F_k * tau + (1 - F_k) * eps with tau = 0.9, eps = 0.05. All 42 values match the figure data to 8 decimal places. Stationary point eps/(eps + omega) = 0.05/0.15 = 1/3 verified.
- **Boolean universe example** (line 297). The four PMF entries `\fnrate * \tnrate`, `\fnrate * \fprate`, `\tprate * \tnrate`, `\tprate * \fprate` correctly sum to 1 and correspond to the four outcomes by element-wise independence.

### Issues found

#### L1 (Major): Rate-argument order swap in higher-order composition example
- **Location**: `sections/bernoulli_model.tex` line 157.
- **Quoted text**: `$\Set{A} \, \AT{\SetUnion}[\fprate][\tprate] \, \Set{B} \sim \AT{(\SetUnion[\Set{A}][\Set{B}])}[\tprate][\fprate]$`
- **Problem**: The right-hand side has `[\tprate][\fprate]` (TPR first, FPR second). Everywhere else in the paper the convention is `[\fprate][\tprate]` (FPR first, TPR second). See line 103 `\tilde{X}[\fprate][\tprate]`, line 134 `\ctor{\fprate}{\tprate}`, line 163 `\APFun{id}[\fprate][\tprate]`, line 169 `\APFun{id}[\fprate][\tprate]`. The semantics intended on line 157 are also inconsistent: the prose says "maps negatives to positives with probability fprate and maps positives to negatives with probability tprate", but the FNR (not TPR) is the rate at which positives go to negatives.
- **Suggestion**: Rewrite as `\AT{(\SetUnion[\Set{A}][\Set{B}])}[\fprate][\tprate]` and replace "maps positives to negatives with probability tprate" with "with probability fnrate" (and use `\fnrate` to be precise), or restate as "retains positives with probability tprate". The Kronecker product factorization argument depends on this being correct.
- **Confidence**: High.

#### L2 (Minor): Theorem 4.2 PMF subscript inconsistency
- **Location**: `sections/distributions.tex` lines 58 vs 77.
- **Quoted text**: Theorem statement at line 58 reads `$p_{\alpha_n}(\fprateob | \fprate) = p_{\FP_n}(\fprateob n | \fprate)$` while the proof at line 77 reads `$p_{\alpha_n}(\fprateob_n | \fprate) = p_{\FP_n}(n \fprateob)$`.
- **Problem**: The proof uses `\fprateob_n` and drops the conditioning on `\fprate` from the RHS, while the theorem statement omits the subscript and keeps the conditioning. Pick one form.
- **Suggestion**: Standardize on the theorem statement form: `$p_{\alpha_n}(\fprateob | \fprate) = p_{\FP_n}(n \fprateob | \fprate)$`. Note also `\fprateob n` reads as `\hat{epsilon} n` which is correct meaning but `n \fprateob` reads better.
- **Confidence**: High.

#### L3 (Minor): Implicit conditioning on R in joint density factorization
- **Location**: `sections/bernoulli_model.tex` lines 122-127.
- **Quoted text**: `$f(\tilde{X}, \alpha, \beta) = f(\tilde{X} | \alpha, \beta) f(\alpha | R) f(\beta | R)$`.
- **Problem**: LHS has no explicit conditioning on R but RHS does. This is correct because `\tilde{X}` (line 98) is defined as `\tilde{R} | R = X`, so R is absorbed into the symbol, but a reader seeing this equation out of context will be confused.
- **Suggestion**: Add a brief parenthetical or rewrite both sides with R explicit, e.g. `$f(\tilde{R}, \alpha, \beta | R = X) = f(\tilde{R} | \alpha, \beta, R = X) f(\alpha | R = X) f(\beta | R = X)$`.
- **Confidence**: Medium (logically sound, notationally opaque).

## Confidence

- The two axioms entail all the stated distributional results. The chain of inference is clean.
- The composition theorem reduces to standard channel multiplication and is correctly stated.
- All numerical data is reproducible from the stated parameters.

## Cross-check Suggested

L1 should be cross-verified by the methodology auditor for whether the semantic mismatch in the prose accompanying the equation reveals a deeper confusion about which rate goes where, or is a stand-alone typo.
