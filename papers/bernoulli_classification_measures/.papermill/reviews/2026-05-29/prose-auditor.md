# Writing and Presentation Review

**Paper**: Binary classification measures for random approximate sets
**Reviewer role**: prose-auditor (performed by area chair)
**Date**: 2026-05-29

## Overall

The writing is clear, economical, and well-organized. The narrative arc is sound: motivation (the PPV question), the enabling structure (binomial counts), the systematic derivation, validation, and design consequence. Section signposting via `\Cref` is consistent and the build is clean (no overfull/underfull boxes, no undefined references). The main weaknesses are several notation-consistency slips and a handful of awkward sentences. None obscure the mathematics.

## Notation consistency findings

### MINOR-1: True/false rate symbols typeset inconsistently (calligraphic vs upright)
- **Location**: Preliminaries line 94 vs Measures lines 154, 241, 247.
- **Quoted text (prelim)**: "$\TPR_p = 1 - \beta_p$" (the `\TPR` macro renders as a calligraphic T).
- **Quoted text (measures)**: "$\ACC_{\p + \n} = \lambda \mathrm{TPR}_\p + (1 - \lambda) \mathrm{TNR}_n$" (upright "TPR", "TNR" via `\mathrm`).
- **Problem**: The same random quantity (the true positive rate) is set as a calligraphic symbol in one place and as upright "TPR" in another. Likewise TNR. A reader may wonder if `\TPR_p` and `\mathrm{TPR}_\p` denote different objects.
- **Suggestion**: Pick one. Either always use the macro (`\TPR_\p`, `\TNR_\n`) or always use `\mathrm{TPR}`. Given the rest of the paper uses `\mathrm{TPR}` in the substantive theorem (accuracy), standardize on that, or define the macro to expand to upright text.

### MINOR-2: Four different symbols for the approximate set
- **Location**: across sections. `\tilde{\RV{R}}[\fprate]` (Thm 2.3), `\tilde{A}` (most of Section 2 and Appendix A), `\tilde{S}` (Appendix C and Measures line 169), `\ASet{A}` (Measures line 8).
- **Problem**: The central object is referred to by four notations. `\tilde{\RV{R}}[\fprate]` in Theorem 2.3 is especially jarring because R is introduced nowhere else in this paper (it is inherited from the foundation paper's "random approximate set R" notation).
- **Suggestion**: Settle on `\ASet{A}` (the unified-notation macro) or `\tilde{A}` throughout, and either define or remove `\tilde{\RV{R}}`. If Theorem 2.3 is quoted verbatim from the companion, adapt its notation to this paper.

### MINOR-3 (cross-listed with logic-checker MINOR-1): beta defined inconsistently
- **Location**: Prop 2.1 ("$\Expect{\beta} = \tprate$") vs Cor 2.5 ("$\TPR_p = 1 - \beta_p$").
- This is primarily a logic finding (see logic-checker), but it also reads as a notation slip. Recommend `$\Expect{\beta} = \fnrate$`.

## Prose findings

### MINOR-4: Repetitive theorem lead-ins
- **Location**: Measures, repeated pattern "is a performance measure defined as" (lines 17, 200) and "with an expectation given approximately by" (lines 31, 214, 272).
- **Problem**: The five measures are introduced with near-identical boilerplate. This is acceptable for a reference-style paper but reads mechanically.
- **Suggestion**: Vary the lead-ins slightly, or introduce the common pattern once ("each measure below is defined, then promoted to a random variable, then given closed-form moments") and drop the repetition.

### MINOR-5: "given approximately" doubly emphasized
- **Location**: Measures line 31, Appendix line 7: "given \emph{approximately} by".
- **Problem**: Italicizing "approximately" every time is heavy. The approximation status is clear from "second-order delta method" and the O(.) error term.
- **Suggestion**: Drop the emphasis after the first use.

### MINOR-6: Appendix A restatement adds variance definitions that differ in form from the theorem body
- **Location**: Appendix A line 13 states sigma_t^2 = p omega tau and sigma_f^2 = n epsilon eta, whereas Theorem 3.1 wrote them as (1-tau) t-bar and (1-eps) f-bar.
- **Problem**: Not an error (the forms are algebraically identical, which I verified), but presenting the same quantity in two notations within pages of each other adds avoidable cognitive load.
- **Suggestion**: Use one form. Prefer the explicit p tau (1-tau), n eps (1-eps) form used in the proof body for clarity.

### SUGGESTION-1: Define "prevalence", "base rate", and lambda together at first use
The terms "prevalence" and "base rate" are used interchangeably and lambda is introduced midway (Measures, before the accuracy theorem). Define all three in one place in the introduction, since prevalence sensitivity is the headline.

### SUGGESTION-2: Recall is mentioned but never tabulated as such
Recall is named in the F1 definition and the intro but does not appear by name in the summary table (it is the TPR row). One parenthetical "(recall)" next to the TPR row in Table 3.1 would help IR readers.

### SUGGESTION-3: Abstract could name the prevalence result as the headline
The abstract states the prevalence point in the third sentence as one of several. Given it is the paper's most quotable practical contribution, consider leading with it.

## Things that are good (for balance)
- The three numbered observations after eq (3.2) are an excellent, concrete reader aid.
- The reparameterization example (solve for FPR given a target accuracy and known base rate) turns the theory into a usable design knob and is well executed, including the correct boundary discussion at lambda to 1.
- Figure captions are informative and self-contained.
- `\cref`/`\Cref` usage is consistent and all references resolve.
