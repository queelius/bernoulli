# Methodology Auditor Report

## Overall Assessment

The paper is purely theoretical with no empirical evaluation. The methodology consists of definitions, constructions, and proofs. The mathematical framework is generally well-structured, but there are reproducibility concerns (reliance on unpublished companion papers) and some methodological gaps in the proofs.

## Findings

### MAJOR-1: No empirical validation
- **Location**: Entire paper
- **Problem**: The paper presents 5 algorithms but no implementation, benchmarks, or experimental results. Even for a theoretical paper, a small empirical study would strengthen claims about construction feasibility (e.g., "for very small sets (m <= 10), the construction is feasible" -- Section 9.3). How long does construction actually take for m=5,10,15,20? What is the actual salt length distribution vs. the theoretical prediction?
- **Suggestion**: Add a small experimental section or supplement showing: (a) construction time vs. m for the equality and threshold predicates, (b) empirical salt length distribution vs. Theorem 6.2, (c) empirical FPR distribution for the adaptive threshold vs. the Beta distribution. This would cost little effort and substantially strengthen the paper.
- **Severity**: Major -- purely theoretical claims about "feasibility for small sets" and "practical" adaptive threshold are unsupported.

### MAJOR-2: Companion paper dependency for foundational results
- **Location**: Section 2 (prelim), Section 7 (prob_model), Section 8 (operations)
- **Problem**: The paper relies heavily on three companion papers for foundational definitions and results (Bernoulli set/map definitions, space lower bounds, set algebra, error propagation). All three companions are unpublished self-citations with no journal, arxiv, or other stable identifier. A reader cannot verify the foundational claims without access to these papers.
- **Suggestion**: Either (a) provide stable links/identifiers for the companion papers (e.g., arxiv preprints), or (b) include the essential proofs inline (especially the space lower bounds, which are currently "postulates"), or (c) at minimum, provide enough detail that the results are self-contained for verification.
- **Severity**: Major -- the paper is not self-contained and relies on unverifiable sources.

### MAJOR-3: Algorithm 1 value-matching hash does not depend on salt
- **Location**: Section 4, Algorithm 1 (alg:make_shf_eq), line 47-48 of construction.tex
- **Quoted text**: "h(1 || x^(i)) mod 2^{BL(v^(i))} != Encode(v^(i))"
- **Problem**: The value-matching hash h(1 || x^(i)) does not include the salt b. This means value matching is salt-independent: either h(1 || x_i) matches v_i or it does not, regardless of which salt is tried. This contradicts the success probability formula (Theorem 3.1), which treats value matching as an independent per-trial event. If value matching is salt-independent, then: (a) for a map, you must first check whether all values match before even starting the salt search, and (b) if any value does not match, no salt will ever work.
- **Suggestion**: Either salt the value hash (use h(1 || x_i || b)) so that each trial is independent, or restructure the success probability analysis to condition on value matching. The adaptive threshold algorithm (Algorithm 3, line 146) DOES salt the value hash: "h(1 || x_i || b) mod 2^{BL(v_i)} = Encode(v_i)". This inconsistency between algorithms needs to be resolved.
- **Severity**: Major -- algorithmic inconsistency that affects the validity of the theoretical analysis.

### MINOR-1: The exhaustive search through all salt lengths is unusual
- **Location**: Section 4, Algorithms 1-2
- **Problem**: The construction enumerates salts in order of increasing bit length (0 bits, 1 bit, 2 bits, ...), testing all 2^n salts of length n before moving to length n+1. This is a valid but unusual search strategy. The more natural approach (generate random salts of increasing length) would be simpler and have the same expected search time.
- **Suggestion**: Clarify whether the exhaustive enumeration within each length level is essential for the maximum entropy argument, or whether random sampling would suffice. If exhaustive enumeration is needed for the entropy proof, state this explicitly.

### MINOR-2: The "method-of-moments estimator" for cardinality (Section 6.3) is stated without analysis
- **Location**: Section 6.3, line 74 of entropy.tex
- **Quoted text**: "the method-of-moments estimator of the cardinality is m_hat = -BL(S~) / log2(eps)"
- **Problem**: This estimator is stated without any analysis of its properties (bias, variance, consistency). Is it unbiased? What is its variance? The denominator should be -log2(eps) + mu for maps (the paper says "replacing log2 eps with log2 eps - mu", which gives the wrong sign).
- **Suggestion**: Either provide basic statistical properties of the estimator or remove the claim. Fix the sign in the map case.

### MINOR-3: The "entropy-space tradeoff" (Section 6.4) is vague
- **Location**: Section 6.4, lines 79-91 of entropy.tex
- **Problem**: The entropy-space tradeoff section describes padding the salt to hide cardinality, but the description is informal. "Setting a target bit length l >> -m*log2(eps)" -- how does one ensure the salt has a specific length? The construction finds the FIRST successful salt; it does not skip short salts.
- **Suggestion**: Describe a concrete mechanism (e.g., skip all salts shorter than l bits, or pad the salt after construction). The current description is too vague to implement.

## Reproducibility Assessment

- **Algorithms**: Clearly specified (5 algorithms with pseudocode) -- GOOD
- **Assumptions**: Random oracle assumption clearly stated -- GOOD
- **Parameters**: Well-defined (m, eps, mu, N, t, p) -- GOOD
- **Proofs**: Mostly self-contained modulo companion papers -- FAIR
- **Implementation**: No code or benchmarks provided -- POOR
- **Companion papers**: Not publicly accessible -- POOR
