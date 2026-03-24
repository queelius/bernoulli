# Prose Auditor Report

## Overall Assessment

The writing is generally clear and well-organized. The paper follows a logical progression from definitions to constructions to analysis. The notation is consistent (thanks to alex.sty). However, there are significant prose issues: an informal self-correction in a proof, some grammatical errors, inconsistent article usage ("a BHF" vs "an BHF"), and several sections that are too terse.

## Findings

### CRITICAL-1: "Wait---" interruption in formal proof
- **Location**: Appendix B, Theorem B.2, lines 160-163 of appendix.tex
- **Quoted text**: "Wait---this is the continuous-approximation version (when draws are distinct with high probability). For the exact discrete case with possible ties, the correct derivation uses the discrete order statistic formula directly."
- **Problem**: A formal mathematical proof contains the word "Wait---" followed by a self-correction. This reads like a draft note that was never cleaned up. It severely undermines the paper's professional quality and mathematical rigor.
- **Suggestion**: Remove the "Wait---" paragraph entirely. Either present the correct derivation from the start, or structure the proof as: (a) present the exact discrete formula, (b) note the continuous approximation as a corollary. The current structure (present wrong derivation, interrupt, present different derivation) is unacceptable in a finished paper.
- **Severity**: Critical -- this is the most visible prose defect and gives the impression of an unfinished draft.

### MAJOR-1: Inconsistent article usage ("a BHF" vs "an BHF")
- **Location**: Multiple locations throughout
- **Examples**:
  - Section 4, Algorithm 4 input: "S~ is an BHF-coded Bernoulli set" (should be "a BHF-coded")
  - Section 6.3, line 71: "Given an BHF with bit length..." (should be "a BHF")
  - Section 6, Appendix A: "A random bit length n of an BHF encoding" (should be "a BHF")
- **Problem**: "BHF" is pronounced "bee-aitch-eff" (starting with a consonant sound), so the correct article is "a", not "an". This error appears at least 3 times.
- **Suggestion**: Search-and-replace "an BHF" with "a BHF" throughout.
- **Severity**: Major -- repeated grammatical error.

### MAJOR-2: Several sections are too terse
- **Location**: Section 7 (prob_model), Section 8 (operations)
- **Problem**: Section 7 is 44 lines and consists entirely of results cited from companion papers with no original analysis. Section 8 is 54 lines with two straightforward convergence theorems. These sections feel like placeholders. If they exist only to reference companion papers, they could be integrated into the preliminaries or discussion.
- **Suggestion**: Either expand these sections with original content relevant to the BHF (e.g., how the BHF's specific structure affects the distributions, practical implications of the convergence results) or merge them into other sections.
- **Severity**: Major -- two sections that add little value to the paper.

### MINOR-1: Abstract mentions "adaptive threshold" details before the reader has context
- **Location**: Abstract, lines 60-63 of main.tex
- **Quoted text**: "We also introduce an adaptive variant that sets t to the p-th order statistic of the hash residues, eliminating the salt search entirely for sets and achieving O(log N / m) -> 0 bits per element---at the cost of a random (Beta-distributed) false positive rate."
- **Problem**: The abstract introduces p-th order statistics, Beta distributions, and O(log N / m) notation before the reader has any context. While technically correct, this is dense for an abstract. The phrase "p-th order statistic of the hash residues" requires specialized knowledge to parse.
- **Suggestion**: Simplify the abstract's description of the adaptive threshold: e.g., "We also introduce an adaptive variant that eliminates the salt search entirely for sets, achieving vanishing per-element space cost at the expense of a random (rather than fixed) false positive rate."

### MINOR-2: The word "salt" is used before being defined
- **Location**: Section 1, line 6 of intro.tex vs Definition 3.1
- **Problem**: The introduction uses "salt" informally ("a bit string b discovered by search") but the formal definition of the acceptance predicate (Definition 3.1) does not define "salt" as a term -- it just uses b as "a salt b in B*". The concept is clear from context but a formal definition would be cleaner.
- **Suggestion**: Add a brief definition of "salt" in the preliminaries or at its first use in Section 3.

### MINOR-3: Inconsistent notation for "bits per element"
- **Location**: Multiple sections
- **Problem**: The paper uses both "bits per element" (text) and the siunitx notation "\si{bits \per element}" (in equations via the \per command). This is fine, but the siunitx usage is unusual for a CS theory paper -- it is more common in physics/engineering. Some readers may find it distracting.
- **Suggestion**: This is a style choice; no change needed, but be aware that some reviewers may object.

### MINOR-4: Section 9.2 comparison with Bloom filter has incorrect space formula
- **Location**: Section 9.2, line 31 of discussion.tex
- **Quoted text**: "It achieves log2(e) / eps bits per element"
- **Problem**: The Bloom filter achieves approximately -log2(e) * log2(eps) bits per element (i.e., about 1.44 * (-log2 eps)), not "log2(e) / eps". The formula in the paper is dimensionally wrong -- log2(e)/eps for eps=0.01 would be 144 bits/element, which is absurd.
- **Suggestion**: Correct to "-log2(e) * log2(eps)" or equivalently "log2(e) * log2(1/eps)" or approximately "1.44 * (-log2 eps)" bits per element.
- **Severity**: Minor but factually incorrect.

### MINOR-5: Figure 1 references old "Singular Hash Set" notation
- **Location**: img/fig_shs.tex
- **Problem**: The TikZ figure file is named "fig_shs.tex" (SHS = Singular Hash Set) and references h*(x_i || b) mod 4 with eps = 2^{-4}. The figure still uses the old naming convention and shows a specific example that may not match the paper's current notation.
- **Suggestion**: Rename the figure file and verify the figure's notation matches the paper's current conventions.

### SUGGESTION-1: Add a "Notation" table or subsection
- The paper uses many symbols (eps, delta, mu, m, N, t, p, b, h, h*, h_k, etc.). A notation summary table at the end of the preliminaries would help readers.

### SUGGESTION-2: The paper would benefit from a running example
- A concrete example (e.g., m=3 elements, eps=0.25, N=4) carried through from construction to space analysis would make the abstract framework more accessible.
