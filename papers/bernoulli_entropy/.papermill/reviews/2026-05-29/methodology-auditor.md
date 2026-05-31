# Methodology Auditor Report, bernoulli_entropy

**Reviewer role**: Experimental design, statistical rigor, reproducibility
**Date**: 2026-05-29
**Note**: This is a pure-theory paper with no experiments, datasets, or code artifacts. The audit therefore targets (a) the rigor and stated validity regimes of the asymptotic derivations, (b) the soundness of the probabilistic modeling assumptions, and (c) reproducibility of the analytical claims (which I checked by independent numerical computation).

## Reproducibility of analytical claims (independent check)
I re-derived and numerically verified every quantitative claim:
- **Binomial entropy asymptotic** (`eq:binomial_entropy_asymp`): reproduced. Exact-minus-asymptotic error is O(1/n) across n in {100, 500, 1000, 1e4, 2e4} and p in {0.05, 0.1, 0.3, 0.5}.
- **Joint-entropy closed form**: the algebra reproduces exactly; the error-term combination is an exact identity.
- **Lower-bound asymptotic** (Prop 4.1): reproduced; `B/p -> -log2(eps)` for fixed p as n -> infinity, across p in {2,3,5} and eps in {0.1, 0.01}.
- **Bloom efficiency** ln2 approx 0.69 and figure curves: reproduced.

A short numerical appendix or a one-line "verified numerically" footnote would let a reader reproduce these without redoing the asymptotics. Currently the paper offers no reproducibility aid; for asymptotic claims this is acceptable but a sanity-check table would strengthen it.

## Findings

### MAJOR-1: Theorem 3.1 and Proposition 4.1 use different, unreconciled asymptotic regimes
- **Location**: Thm 3.1 (`sections/entropy.tex` line 29-30) versus Prop 4.1 (`sections/space_complexity.tex` line 51).
- **Quoted text (Thm 3.1)**: "the asymptotic term holds as $u \to \infty$ with $m/u$ bounded away from $0$ and $1$ (so that both $m$ and $u - m$ grow with $u$)."
- **Quoted text (Prop 4.1)**: "For fixed $\p$ as $n \to \infty$".
- **Problem**: The entropy theorem requires the positive count m to grow proportionally with the universe (constant density). The lower-bound proposition requires the objective set size p to stay *fixed* while the universe n grows (vanishing density). These are opposite density regimes, and the paper uses `m` (Thm) and `\p`/`p` (Prop) for what is conceptually the same quantity (number of true positives / objective set size) without ever noting that the two results live in different limits. A reader who tries to combine them (e.g., "plug the entropy into the space bound") will be silently mixing incompatible regimes. I verified the incompatibility matters: in the constant-density regime (p = n/10), the lower-bound expression does *not* approach -log2(eps); it falls short by a constant (approx 0.93 bits at eps=0.05). So the fixed-p assumption in Prop 4.1 is load-bearing, not cosmetic.
- **Suggestion**: (a) Unify notation: use `m` consistently for the objective-set size in both results, or explicitly say "p (denoted m in Section 3)". (b) Add a sentence in Section 4 noting that the bound is stated in the fixed-set-size / growing-universe regime (appropriate for "a finite set inside a countably infinite universe"), distinct from the constant-density regime of Section 3. This prevents an invalid cross-application.

### MINOR-1: The "dense set" preamble of Section 4 is informal and disconnected
- **Location**: `sections/space_complexity.tex` lines 6-12.
- **Quoted text**: "If the finite cardinality of a universe is $u$ and the set is \emph{dense} ... then $\mathcal{O}(u)$ bits are needed to code the set, which is independent of $\p$, the false positive rate, and the false negative rate."
- **Problem**: This opening claim is stated without proof or citation and is not used anywhere afterward. "Dense" is undefined; the O(u) claim (essentially: store a bitmask) is intuitive but appears as an orphan. It also switches the universe symbol to `u` while the rest of the section uses `n`, and uses `\p` for the set size. The transition to the main (countably infinite) result is abrupt.
- **Suggestion**: Either delete the paragraph (it adds little) or convert it into a brief, labeled remark with a one-line justification ("a dense set is coded by its u-bit indicator vector") and reconcile the symbols (`u` vs `n`).

### MINOR-2: Modeling assumption, fixed expected rates vs. random block rates, is not delineated for the entropy result
- **Location**: `sections/preliminaries.tex` (Axiom 2 introduces random rates alpha_i) versus Thm 3.1 (treats eps, omega as fixed numbers).
- **Problem**: Axiom 2 (conditional independence of *random* block error rates) is restated, but Thm 3.1 then uses *deterministic* eps, omega. The entropy is therefore conditional on the rates as well as on m, but this conditioning is never stated. The methodology of "which quantities are random and which are conditioned on" is left implicit. (Logic-checker MINOR-1 flags the same gap from the proof-correctness angle.)
- **Suggestion**: State the conditioning explicitly in the theorem ("for fixed rates eps, omega"), and note whether marginalizing over the random alpha_i of Axiom 2 is in or out of scope. If out of scope, say so; if it is the same as Section 3.1's POS marginalization, point to it.

### SUGGESTION-1: Add a numerical sanity-check figure or table for the entropy result
- Result 1 is the paper's only novel result and currently has no figure (Section 4 has the space-complexity figure). A small plot of exact vs. asymptotic joint entropy over u (showing the O(1/n) gap closing) would (i) demonstrate the result is correct, (ii) give the entropy section visual parity with the space section, and (iii) provide the reproducibility aid the paper lacks. This is cheap and directly raises confidence.

### SUGGESTION-2: State explicitly that no empirical claims are made
- The abstract and intro are appropriately theoretical, but a single sentence ("all results are analytical; no experiments are required") would set reader expectations for a paper with one figure that is a plot of two formulas, not data.

## Statistical/probabilistic rigor
- The independence-to-additivity step is correctly grounded in Axiom 1. The conditional-independence-given-POS step in Section 3.1 is correctly invoked.
- The CLT/local-limit reasoning underlying the binomial entropy expansion is delegated to Cover & Thomas; acceptable, though the exact expansion is folklore rather than a numbered theorem there (see citation-verifier).
- Yao's-minimax step (Prop 4.1) is a methodological reduction (deterministic to randomized) stated without the hard-distribution setup; flagged in detail by logic-checker MAJOR-2.

## Confidence
High on the reproducibility verification (everything checks out numerically). Medium-high on the regime-mismatch finding: the mismatch is real and verified, the fix is editorial, and the underlying results remain individually valid.
