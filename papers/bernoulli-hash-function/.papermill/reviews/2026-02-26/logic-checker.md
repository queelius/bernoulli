# Logic Checker Report

## Overall Assessment

The paper's logical chain is largely sound but contains several gaps of varying severity. The core results (success probabilities, asymptotic space complexity, adaptive threshold FPR distribution) are correct. However, the space complexity proof relies on a Taylor expansion approximation without rigorous error bounds, the "lower bound not violated" argument is informal, and the appendix PMF derivation contains an acknowledged error in mid-proof that undermines confidence.

## Findings

### CRITICAL-1: Taylor expansion in space complexity proof lacks rigor
- **Location**: Section 5, Theorem 5.2 (thm:space), lines 49-59 of space.tex
- **Quoted text**: "We approximate E[N] via a second-order Taylor expansion of log2 around E[Q]"
- **Problem**: The proof approximates E[log2(Q)] using a Taylor expansion of log2 around E[Q], then drops higher-order terms. For a geometric random variable Q ~ Geom(p) with very small p (which is exactly the regime of interest, since p = eps^m / 2^{m*mu}), the variance is (1-p)/p^2, which is enormous relative to the mean 1/p. The second-order correction term is -(log2 e)(1-p)/p * (1/E[Q]), which for small p is approximately -log2(e). But there is no bound on the remainder of the Taylor expansion, and log2 is not well-approximated by a quadratic when the variance-to-mean ratio is large. The claim that E[N]/m -> -log2(eps) + mu is likely correct but the proof as written is not rigorous.
- **Suggestion**: Either (a) use Jensen's inequality to bound E[log2(Q)] from above and below (log2 is concave, so E[log2(Q)] <= log2(E[Q]) = -log2(p), giving the upper bound directly; for the lower bound, use the fact that the geometric distribution concentrates), or (b) use the known result that for Q ~ Geom(p), E[floor(log2(Q))] = -log2(p) + O(1) (see e.g., Knuth, Sedgewick, or Flajolet's analysis of digital search trees), or (c) at minimum, state the approximation is heuristic and cite a rigorous asymptotic result.
- **Severity**: Critical -- this is the central optimality claim and the proof does not rigorously support it.

### CRITICAL-2: Appendix PMF derivation contains acknowledged error
- **Location**: Appendix B, Theorem B.2 (thm:os_pmf_detailed), lines 150-163 of appendix.tex
- **Quoted text**: "Wait---this is the continuous-approximation version (when draws are distinct with high probability). For the exact discrete case with possible ties, the correct derivation uses the discrete order statistic formula directly."
- **Problem**: The proof begins with a multinomial argument, then the author interrupts with "Wait---this is the continuous-approximation version" and pivots to a different argument. This self-correction in the middle of a formal proof is inappropriate in a mathematical paper. The initial multinomial argument gives (m/N) * C(m-1, p-1) * (j/N)^{p-1} * ((N-1-j)/N)^{m-p}, which is indeed NOT the correct discrete PMF (it assumes each value is hit at most once, which is the continuous approximation). The corrected formula uses combinatorial counting (choosing p-1 from {0,...,j-1} and m-p from {j+1,...,N-1}), which assumes sampling WITHOUT replacement, but the hash residues are sampled WITH replacement (i.i.d. from {0,...,N-1}). The paper then adds "but without replacement (since the random oracle makes collisions negligible for N >> m)", which is an approximation, not an exact result.
- **Suggestion**: Either (a) present the exact PMF for the p-th order statistic of m i.i.d. discrete uniform on {0,...,N-1} (which involves inclusion-exclusion and is more complex), or (b) clearly state that the formula is an approximation valid for N >> m and cite the conditions under which it holds, or (c) simply cite David & Nagaraja (2003) for the exact discrete order statistic PMF without rederiving it. The "Wait---" interruption must be removed regardless.
- **Severity**: Critical -- the proof is incomplete and contains informal self-correction that undermines the mathematical rigor of the paper.

### MAJOR-1: Lower bound non-violation argument is informal (Remark 5.5)
- **Location**: Section 5.5, Remark 5.5 (rem:lb_not_violated), lines 162-177 of space.tex
- **Quoted text**: "The information-theoretic lower bound of -log2 eps + mu bits per element assumes a fixed, predetermined false positive rate eps."
- **Problem**: The remark claims the adaptive threshold does not violate the lower bound because the FPR is random rather than fixed. This is the right intuition but the argument is purely informal. There is no formal statement of what "the lower bound assumes a fixed FPR" means precisely. The information-theoretic lower bound (as in Carter et al. 1978) applies to any data structure that, for EVERY input set S, achieves FPR at most eps. If the adaptive threshold achieves FPR <= eps^* with probability 1 for some eps^*, then the lower bound applies to eps^*. If it does not guarantee any worst-case FPR bound, then the comparison with the lower bound is meaningless. The claim that "the missing m(-log2 eps) bits of information are encoded in the randomness of eps itself" is hand-waving.
- **Suggestion**: Make the argument precise. State: (a) what the lower bound's formal statement is (for any data structure D such that for all x not in S, Pr[D says x in S] <= eps, the space is at least n*log2(1/eps)), (b) why the adaptive threshold does not satisfy this hypothesis (because the FPR is a random variable, not a guaranteed bound), and (c) what guarantee the adaptive threshold DOES provide (e.g., the expected FPR is eps^* and the FPR concentrates around eps^* with variance O(1/m)). Consider citing the formal lower bound statement from Carter et al. (1978) or Pagh et al. (2005).
- **Severity**: Major -- the paper's most surprising claim (O(log N / m) -> 0 bits/element) rests on this argument.

### MAJOR-2: Success probability proof for equality predicate has subtle gap
- **Location**: Section 3, Theorem 3.1 (thm:success_eq), lines 62-76 of shf.tex
- **Quoted text**: "The first key fixes the target hash h_0; each of the remaining m-1 keys must hash to h_0"
- **Problem**: The proof says the value-matching factor is prod_i 2^{-BL(v_i)} and then writes this as 2^{-m*mu} where mu = (1/m) * sum BL(v_i). But 2^{-sum BL(v_i)} = 2^{-m*mu} only when mu is defined as the average. This is correct. However, the proof conflates two different hash evaluations: the acceptance test uses h(x || b) mod 2^k, but the value matching uses "the first BL(v_i) bits of a second hash". The algorithm (Alg 1, line 47-48) uses h(1 || x^(i)) mod 2^{BL(v^(i))}, which does NOT depend on b. This means the value-matching constraint is the SAME for every candidate salt b. The success probability should be: (probability that all values match) * (probability that all keys hash to same residue) = (product of 2^{-BL(v_i)} for i=1..m) * eps^{m-1}. But since the value-matching is salt-independent, if the values don't match, NO salt will ever work. The paper seems to assume the value hash is also salted (h(1 || x_i || b)), but Algorithm 1 uses h(1 || x^(i)) without b.
- **Suggestion**: Clarify whether the value hash depends on b or not. Algorithm 1 (line 47) uses h(1 || x^(i)), while Algorithm 2 (line 89) uses h(1 || x_i). Neither includes b. But the success probability theorem assumes value matching is independent per trial. If value matching does not depend on b, then either all trials satisfy value matching or none do, and the geometric search model breaks. This needs to be resolved -- either the algorithm should salt the value hash, or the success probability formula needs to be conditioned on value matching.
- **Severity**: Major -- affects the correctness of the success probability and the validity of the geometric search model for maps.

### MAJOR-3: Eq. (19) in the appendix has an incorrect intermediate formula
- **Location**: Appendix B, Theorem B.2 (thm:os_pmf_detailed), Eq. (19), lines 117-124 of appendix.tex
- **Quoted text**: The double-sum formula in eq:os_pmf_detailed
- **Problem**: The intermediate formula (eq. 19) with inclusion-exclusion double sums has the binomial coefficients in the denominator with a ^{-1} exponent, which is unusual and likely a typesetting error. The formula reads: (-1)^{i+k} * C(p-1,i) * C(m-p,k) / C(j, p-1-i) * C(N-1-j, m-p-k))^{-1}. Having ^{-1} on the product of two binomial coefficients is confusing -- it is unclear whether each binomial is inverted separately or the product is inverted.
- **Suggestion**: Either remove this intermediate formula entirely (since the paper immediately simplifies to the closed form using Vandermonde) or carefully typeset it with explicit fractions to avoid ambiguity.
- **Severity**: Major -- mathematically ambiguous formula in a proof.

### MINOR-1: Space lower bounds stated as "postulates" rather than theorems
- **Location**: Section 2, Postulate 2.1 and 2.2 (post:set_lb, post:map_lb)
- **Problem**: The space lower bounds are stated as "postulates" with no citation or proof. These are well-known results (Carter et al. 1978 for sets). Calling them "postulates" suggests they are assumed without proof, which is technically fine, but citing the original source would strengthen the foundation.
- **Suggestion**: Either cite Carter et al. (1978) or note that these are derived in the companion papers. If they are proven in the companion papers, say so explicitly.

### MINOR-2: The FNR search complexity theorem is stated loosely
- **Location**: Section 3.4, Theorem 3.4 (thm:fnr_search), lines 129-152 of shf.tex
- **Quoted text**: "the same test requires O(C(m,p) * m) hash evaluations in the worst case, since each candidate h_0 (determined by each p-subset) must be checked against all elements"
- **Problem**: The worst case O(C(m,p) * m) for the equality predicate is correct only if you enumerate all p-subsets. But a more efficient approach exists: hash all m elements, group by residue, and check if any residue has >= p elements. This is O(m) per candidate salt, same as the threshold predicate. The paper overstates the complexity difference.
- **Suggestion**: Acknowledge that the O(C(m,p) * m) bound applies to the naive algorithm presented in Algorithm 1, and note that a hash-and-count approach reduces this to O(m) per salt for the equality predicate as well (though the equality predicate still has fewer valid residues per salt).

### MINOR-3: Random oracle definition is informal
- **Location**: Section 2.2, Definition 2.2 (def:randomoracle)
- **Quoted text**: "A random oracle h* : B* -> B^inf is a theoretical hash function whose output is uniformly distributed over its range for every unique input."
- **Problem**: The output of a random oracle is not a single infinite bit string -- it is a function that, for each new input, produces an independently uniformly random output. The definition should say the outputs are independent across inputs, not just "uniformly distributed."
- **Suggestion**: Add "with outputs independent across distinct inputs" to the definition.

### MINOR-4: The notation N is overloaded
- **Location**: Throughout
- **Problem**: N is used for both the modulus in the threshold predicate and the random variable for salt bit length (RV{N}). While the contexts are different (Section 3 vs Section 5-6), this overloading could confuse readers.
- **Suggestion**: Rename the salt bit length random variable to something like L or Lambda.

## Proof Chain Completeness

The logical chain from definitions through the main results is:

1. Definitions (Sec 2): Bernoulli set/map, space lower bounds -- OK (postulated)
2. Acceptance predicate (Sec 3): Well-defined -- OK
3. Success probabilities (Thm 3.1, 3.2): Correct modulo the value-matching issue (MAJOR-2) -- GAP
4. FPR granularity (Thm 3.3): Immediate from definitions -- OK
5. Search complexity (Thm 3.4): Correct but overstated -- MINOR
6. Adaptive threshold (Thm 3.5-3.9): Correct -- OK
7. Space complexity (Thm 5.2): Approximation without error bounds -- GAP (CRITICAL-1)
8. Entropy (Thm 6.1): Informal argument -- WEAK
9. Salt PMF (Thm 6.2, App A): Correct -- OK
10. Adaptive space (Thm 5.5): Correct but lower-bound argument informal -- GAP (MAJOR-1)
11. Convergence (Thm 8.1, 8.2): Correct -- OK
12. Adaptive PMF (App B): Contains errors -- GAP (CRITICAL-2)
