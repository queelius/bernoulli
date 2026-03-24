# Prose Auditor Report

**Paper**: Bernoulli sets: a model for sets with random errors
**Date**: 2026-02-27

## Summary
The writing is generally clear and well-structured. The paper follows a logical progression from axioms to derived results. However, there are notation inconsistencies, some sections that feel underdeveloped, and prose that could be tightened.

## Findings

### Major Issues

**P1. Notation inconsistency: E{} vs \Expect{} (multiple locations)**
- **Location**: distributions.tex lines 68, 435, 488; appendix.tex line 233
- **Quoted text**: `E\{\frac{\FP_n}{n}\} = \frac{1}{n}E\{\FP_n\} = \fprate` (line 68)
- **Problem**: The paper uses both `E\{...\}` (rendering as $E\{...\}$ with curly braces) and `\Expect{...}` (rendering as $\mathrm{E}[...]$ with square brackets) for the expectation operator. This is visually inconsistent.
- **Suggestion**: Replace all instances of `E\{...\}` with `\Expect{...}` for uniform notation.

**P2. The abstract is overlong and tries to summarize too many contributions**
- **Location**: main.tex lines 73-78
- **Problem**: The abstract attempts to list all eight contributions in one dense paragraph. This makes it hard to identify the central contribution.
- **Suggestion**: Restructure the abstract to emphasize the one central result (compositional rate computability) and mention 2-3 supporting results, moving the rest to the introduction.

### Minor Issues

**p1. Inconsistent use of "random approximate set" vs "Bernoulli set"**
- The paper introduces "Bernoulli set" as the formal term but frequently reverts to "random approximate set" or "approximate set" without qualification.
- **Suggestion**: After the introduction, consistently use "Bernoulli set" for the model and "approximate set" only for the informal concept.

**p2. Section 2 (Algebra of sets) is largely review and could be shortened**
- At 4+ pages, the set algebra review is longer than necessary for the target audience (researchers familiar with sets and probability).
- **Suggestion**: Reduce to 1-2 pages covering only the notation and definitions needed later.

**p3. The paragraph structure in Section 3 is uneven**
- Between the axioms and the ADT subsection, there are several equations (3.3-3.5) and a proposition without clear narrative connecting them.
- **Suggestion**: Add a brief connecting paragraph explaining the role of the sample rates before jumping to equations.

**p4. The conclusion's "Historical context" paragraph partially duplicates Remark 3.1**
- **Location**: conclusion.tex line 28 vs bernoulli_model.tex line 42
- Both mention BSC and Warner's randomized response.
- **Suggestion**: In the conclusion, simply reference Remark 3.1 rather than restating.

**p5. Some theorem statements are overly verbose**
- For example, Theorem 4.5 (distributions.tex lines 285-298) includes a parenthetical about the Taylor expansion validity that would read better as a separate remark.
- **Suggestion**: Move the parenthetical to a remark following the theorem.

**p6. The "Organization" paragraph lists sections by number but the main text doesn't use section numbers**
- **Location**: intro.tex lines 40-46
- The \Cref commands will produce "Section 2" etc., but the reader has to match these to the section titles.
- **Suggestion**: Include the section titles alongside the numbers.

**p7. The appendix notation reference (Appendix C) uses inconsistent formatting**
- Some items use em-dashes, others use colons. The section header style ("Basic Set Notation", "Common Sets") differs from the rest of the paper.
- **Suggestion**: Use a consistent format throughout the notation reference.

**p8. Orphaned sentence fragment in distributions.tex**
- **Location**: distributions.tex lines 134-138
- **Quoted text**: "In \cref{sec:set_theory}, we consider set-theoretic operations like \emph{complements}. The \emph{complement} operator applied to an approximate set of a set with countably infinite negatives is an approximate set of a set with countably infinite positives."
- This reads awkwardly as a transition between false negatives and the next corollary.
- **Suggestion**: Rewrite for clarity: "The complement of an approximate set of a set with countably infinite negatives produces an approximate set with countably infinite positives (Section 5.1); the following corollary addresses this dual."

### Suggestions
1. Consider adding a "Notation" subsection at the end of Section 2 that defines the key symbols ($\fprate$, $\fnrate$, $\tprate$, $\tnrate$) before they appear in Section 3, rather than defining them inline.
2. The paper is 40 pages. For journal submission, consider whether Sections 6 (relational), 7 (intervals), and 8 (entropy) could be condensed, since they extend rather than support the core contribution.
