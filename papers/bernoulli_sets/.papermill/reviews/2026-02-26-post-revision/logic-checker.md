# Logic Checker Report (Post-Revision)

**Date**: 2026-02-26
**Paper**: Bernoulli sets
**Scope**: Proof correctness, logical chain integrity, claim support

## Critical Fix Verification

### Theorem 3.3 (thm:composition_rates) -- VERIFIED CORRECT

The composition $\APFun{id}[\fprate][\tprate] \circ \APFun{id}[\fprate'][\tprate']$ with inner rates (primed) and outer rates (unprimed):

**Theorem statement**: TPR $= \tprate'\tprate + \fnrate'\fprate$, FPR $= \fprate'\tprate + \tnrate'\fprate$

**Proof derivation**:
- For $x \in A$: inner positive prob $\tprate'$, inner negative prob $\fnrate'$. Outer retains positive with $\tprate$, promotes negative with $\fprate$. Composed TPR $= \tprate'\tprate + \fnrate'\fprate$. MATCHES.
- For $x \notin A$: inner positive prob $\fprate'$, inner negative prob $\tnrate'$. Composed FPR $= \fprate'\tprate + \tnrate'\fprate$. MATCHES.

**Numerical verification**: $\fprate=0.1, \tprate=0.9, \fprate'=0.3, \tprate'=0.6$:
- TPR $= 0.6 \times 0.9 + 0.4 \times 0.1 = 0.58$
- FPR $= 0.3 \times 0.9 + 0.7 \times 0.1 = 0.34$

**Consistency with Theorem 3.4**: Under mapping $\fprate' \to \fprate_1, \tprate' \to \tprate_1, \fprate \to \fprate_2, \tprate \to \tprate_2$:
- Theorem 3.4 TPR $= \tprate_1\tprate_2 + \fnrate_1\fprate_2$ -- matches.
- Theorem 3.4 FPR $= \fprate_1\tprate_2 + \tnrate_1\fprate_2$ -- matches.

### K-fold Composition Figure -- VERIFIED

With $\fprate = 0.05, \tprate = 0.90$:
- TPR(0) = 1.0, TPR(1) = 0.90, TPR(2) = 0.815 -- all match figure data.
- Stationary point $\fprate/(\fprate + \fnrate) = 0.05/0.15 = 1/3$ -- matches figure annotation.

## All Proofs Checked

| Theorem/Result | Status | Notes |
|---|---|---|
| Axiom 1 (element-wise independence) | Sound | Now includes i.i.d. clause |
| Axiom 2 (conditional independence) | Sound | |
| Proposition 3.1 (element rates) | Sound | Follows from Axiom 1 (i.i.d.) |
| Theorem 3.3 (composition rates) | FIXED, correct | Previously had algebraic error |
| Theorem 3.4 (two-fold composition) | Correct | Consistent with Thm 3.3 |
| Theorem 4.1 (FP binomial) | Correct | |
| Theorem 4.2 (FPR distribution) | Correct | |
| Corollary 4.1 (FPR a.s. convergence) | Correct | Borel-Cantelli now explicit |
| Theorem 4.5 (CLT for rates) | Correct | |
| Theorem 4.7 (PPV approximation) | Correct | Error bound now stated |
| Theorem 5.1 (complement rates) | Correct | |
| Theorem 5.2 (union FPR) | Correct | |
| Theorem 5.3 (union FNR) | Correct | |
| Theorem 5.4 (intersection FNR) | Correct | |
| Theorem 5.5 (intersection FPR) | Correct | |
| Theorem 5.6 (set difference) | Correct | Verified via complement+intersection |
| Theorem 6.1 (subset probability) | Correct | But missing cross-set independence citation |
| Corollary 6.1 (equality probability) | Correct | |
| Theorem 8.1 (joint entropy) | Correct | Error term derivation verified |
| Proposition 8.1 (space lower bound) | Correct | Standard IT argument |
| Appendix proof (a.s. convergence) | Correct | Borel-Cantelli now explicit |
| Appendix proof (PPV Taylor) | Correct | |

## Remaining Issue

The relational section (Section 6) uses cross-set independence in the subset probability proof but cites only "element-wise independence." This is the same type of oversight that was correctly fixed in Section 5. Severity: minor.
