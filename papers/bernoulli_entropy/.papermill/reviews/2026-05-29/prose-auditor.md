# Prose Auditor Report, bernoulli_entropy

**Reviewer role**: Writing quality, narrative arc, notation consistency
**Date**: 2026-05-29

## Overall
The writing is clean, terse, and professional, appropriate for a short technical note. Sentences are well-formed; the abstract and intro are crisp; the IMRaD-style organization (intro / preliminaries / two result sections / conclusion) is standard and easy to follow. The principal weaknesses are (1) notation inconsistency for the central object (the objective set) and its size, (2) a narrative gap, the two results never connect, and (3) a few orphaned or symbol-clashing passages in Section 4.

## Findings

### MAJOR-1: The objective set is named with three different symbols
- **Location**: `sections/preliminaries.tex` and `sections/space_complexity.tex`.
- **Quoted text**: Axiom 1 (line 17): "mutually independent given the objective set $A$". Axiom 2 (line 23): "Given the objective set $R$, the random error rates...". Prop 4.1 proof (line 28): "an objective set $S$ of size $\p$ is drawn."
- **Problem**: Within a 6-page paper the "objective set" appears as A, R, and S. (`A` also appears as the approximate-set indicator `1_{tilde A}` vs. objective `1_A`, so `A` is doing double duty.) This is the kind of inconsistency that makes a reader stop and check whether three different things are meant. Axiom 2's `R` is especially jarring since the surrounding text uses `A`.
- **Suggestion**: Pick one symbol for the objective set (the family convention appears to be `A` for the abstract set; `S` is conventional in the lower-bound literature). Recommend: use `A` in preliminaries (matching `1_A`) and either keep `S` in the lower-bound proof with a one-word bridge ("objective set S (the set A of the model)") or switch the proof to `A`. Fix `R` in Axiom 2 to match.

### MAJOR-2: Objective-set size is `m` in Section 3 and `\p` in Section 4 with no bridge
- **Location**: `sections/entropy.tex` (uses `m` throughout) vs. `sections/space_complexity.tex` (uses `\p`, rendered as plain `p`).
- **Problem**: The number of true positives / size of the objective set is the same conceptual quantity in both results but is typeset as `m` (Section 3) and `p` (Section 4). Worse, `p` is heavily overloaded elsewhere: `\Fun{p}_{\POS}(p | u)` uses `p` as both the pmf name and the summation variable for the positive count, and `p(1-p)` in the binomial expansion uses `p` as the generic success probability. A reader meets `p` as: generic binomial parameter, objective-set size, positive-count dummy, and pmf symbol. (Logic-checker and methodology-auditor flag the cross-section regime consequence; here the concern is purely readability.)
- **Suggestion**: Standardize the objective-set size to `m` across both sections (the entropy section's choice), freeing `p` for the generic binomial parameter only. Rename the pmf to `\Pr` or `f_{POS}` to avoid `p_{POS}(p|u)`.

### MINOR-1: The two results have no narrative bridge
- **Location**: transition from `sections/entropy.tex` to `sections/space_complexity.tex`; conclusion.
- **Problem**: Section 3 (entropy) and Section 4 (space) are presented as two parallel facts with no connective tissue. The intro motivates entropy via coding ("any lossless representation ... requires at least this many bits"), which *sounds* like it sets up the space bound, but the space bound is about the data structure's size, not about coding the error pattern, and the paper never reconciles the two notions of "bits." The reader expects the entropy to feed the space argument and it does not.
- **Suggestion**: Add one or two sentences at the start of Section 4 distinguishing the two quantities ("Section 3 measured the uncertainty *in the error pattern*; we now ask how many bits the *data structure itself* must occupy. These are different quantities: ...") or, better, draw an actual link if one exists. Even acknowledging the non-link would repair the narrative.

### MINOR-2: Section 4 opening paragraph clashes with the section's own notation
- **Location**: `sections/space_complexity.tex` lines 6-12.
- **Quoted text**: "If the finite cardinality of a universe is $u$ ... $\mathcal{O}(u)$ bits ... independent of $\p$, the false positive rate, and the false negative rate."
- **Problem**: Uses `u` for universe size, while the main proof of the same section uses `n`. Uses `\p` before the proof introduces it. Stranded paragraph (never reused). Reads as a leftover.
- **Suggestion**: Reconcile `u`/`n`; integrate or cut (see methodology-auditor MINOR-1).

### MINOR-3: "binary channels" attribution to Shannon is slightly loose
- **Location**: `sections/intro.tex` line 45.
- **Quoted text**: "Shannon~\cite{shannonBSC} introduced the entropy of binary channels".
- **Problem**: Shannon 1948 introduced entropy and channel capacity in general; "the entropy of binary channels" specifically is a narrowing that the cited title ("A Mathematical Theory of Communication") does not match, and the bib key `shannonBSC` (BSC = binary symmetric channel) hints at a mis-scoped mental model. The entropy used in the paper is the entropy of a *distribution* (binomial), not of a *channel*.
- **Suggestion**: Reword to "Shannon introduced entropy as a measure of uncertainty" (citing 1948), and reserve channel language for the conclusion's mutual-information / channel-capacity discussion. Consider renaming the bib key from `shannonBSC` to `shannon1948`.

### MINOR-4: cleveref renders "axiom" with surrounding spaces
- **Location**: produced by `alex.sty` `\crefname{axiom}{ axiom }{ axioms }` (leading/trailing spaces in the names), surfacing wherever `\cref{asm:...}` is used (e.g., entropy proof "By \cref{asm:element_indep}").
- **Problem**: Cosmetic: the rendered text reads "By  axiom 2.1" with irregular spacing in some contexts. Minor typographic blemish inherited from the shared style file.
- **Suggestion**: This is a style-file issue (out of scope for this paper's sources), but worth noting to the family maintainer: trim the spaces in the `\crefname`/`\Crefname` definitions for `axiom`.

### SUGGESTION-1: Tighten the abstract's last two sentences
- The abstract ends with two short sentences ("The Bloom filter achieves ln2 approx 69% ..." / "The general case ... remains an open problem."). These are fine but could be merged for flow. Minor.

### SUGGESTION-2: The footnote on the Singular Hash Set is dense
- **Location**: `sections/space_complexity.tex` line 78 footnote.
- The footnote packs three ideas (brute-force optimality, impracticality, analytic purpose) into one breath. Splitting into two sentences would read more easily. Optional.

## Notation consistency summary (cross-checked against alex.sty)
- All macros resolve and render (build is clean). The issues are *choice* inconsistencies (A/R/S; m/p; u/n), not undefined commands.
- `\fprate` = epsilon, `\fnrate` = omega, `\tprate` = tau are used consistently.
- `\FP_m`, `\FN_m` subscripting is consistent within Section 3.

## Confidence
High. Prose quality is good; the findings are concrete and mostly mechanical (symbol unification, one orphan paragraph, one narrative bridge). None require rethinking content.
