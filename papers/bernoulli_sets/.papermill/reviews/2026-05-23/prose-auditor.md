# Prose Auditor Report

## Overall Quality

The writing is competent and the structural choices are sound. The narrative arc proceeds intuitively: classical sets, approximate sets, Bernoulli axioms, distributions of error counts. Notation (via alex.sty) is comprehensive and applied consistently in nearly all places. The Remark 3.5 ("Notational convention for alpha and beta") is a model of good practice: it explicitly addresses a previous reviewer concern by stating the asymmetry as a deliberate choice and listing the subscripted forms that always denote error rates.

## Findings

#### P1 (Major): Notation conflict in higher-order composition example
- **Location**: `sections/bernoulli_model.tex` line 157.
- **Quoted text**: `$\Set{A} \, \AT{\SetUnion}[\fprate][\tprate] \, \Set{B} \sim \AT{(\SetUnion[\Set{A}][\Set{B}])}[\tprate][\fprate]$ where $\AT{\SetUnion}[\fprate][\tprate]$ maps negatives to positives with probability $\fprate$ and maps positives to negatives with probability $\tprate$.`
- **Problem**: Two sub-issues. (a) The RHS subscript order `[\tprate][\fprate]` is reversed from the consistent convention `[\fprate][\tprate]` used everywhere else in the paper. (b) The prose says `\tprate` is the rate at which positives go to negatives. The rate at which positives become negatives is the FNR (`\fnrate`), not the TPR. The TPR is the rate at which positives remain positive. This is internally inconsistent.
- **Suggestion**: Standardize the subscript order to `[\fprate][\tprate]` on both sides and rewrite the prose: "where $\AT{\SetUnion}[\fprate][\tprate]$ retains positives with probability $\tprate$ and admits negatives with probability $\fprate$ (equivalently, maps positives to negatives with probability $\fnrate$ and negatives to positives with probability $\fprate$)."
- **Cross-reference**: This is logic-checker finding L1.

#### P2 (Minor): Opening sentence of Section 3 is convoluted (carried from prior review)
- **Location**: `sections/bernoulli_model.tex` line 7.
- **Quoted text**: "In the \emph{Bernoulli} set model, we describe the statistical properties of processes that \emph{generate} approximations of a certain kind that model many existing processes and generalizes to higher-order approximations under algebraic composition."
- **Problem**: This sentence was flagged in the 2026-03-19 review and remains unchanged. It nests three relative clauses, "of a certain kind that model many existing processes" is vague, and "processes ... generalizes" is a subject-verb agreement error (the subject is plural "processes", verb is singular "generalizes").
- **Suggestion**: Rewrite as proposed in the prior review: "The Bernoulli set model describes a class of random set-generating processes: those whose element-wise errors are independent and identically distributed within partition blocks. This class subsumes many practical implementations and is closed under algebraic composition."

#### P3 (Minor): Repetitive companion-paper paragraph (carried from prior review)
- **Location**: `sections/conclusion.tex` lines 20-23 vs `sections/intro.tex` lines 36-38.
- **Problem**: The conclusion repeats the introduction's companion-paper paragraph almost verbatim. The 2026-03-19 review flagged this. The text remains unchanged.
- **Suggestion**: Condense the conclusion's paragraph to one sentence: "The compositional algebra, classification measures, entropy, approximate maps, and algebraic data types are developed in companion papers."

#### P4 (Minor): Complement notation mismatch (carried from prior review)
- **Location**: `sections/appendix.tex` line 42 vs `sections/algebra_of_sets.tex` line 26.
- **Quoted text**: Notation reference: "$\Set{A}^C$"; body: "$A^c$".
- **Problem**: The body uses lowercase `c`, the notation reference uses uppercase `C`.
- **Suggestion**: Change appendix to `$\Set{A}^c$` to match the body convention.

#### P5 (Minor): Bernoulli set generative model vs. observed set
- **Location**: `sections/bernoulli_model.tex` lines 97-98.
- **Quoted text**: "We denote the second-order random approximate set generative model by $\tilde{R}$, with random false positive rate $\alpha$ and random true positive rate $\beta$ conditioned on the objective set $R$. The conditional distribution of $\tilde{R}$ given $R = X$ is denoted by $\tilde{X}$."
- **Problem**: The shift from "generative model" to "approximate set" is ambiguous. Is `\tilde{R}` a probability distribution (a model) or a random variable (a set-valued draw)? The text uses both interpretations. Later in the same section, `\tilde{X}[\fprate][\tprate]` is parameterized, suggesting it is a parameterized distribution; but Definition 3.2 says "A random approximate set with $\fnrate = 0$", treating it as a random variable.
- **Suggestion**: Be explicit. Either (a) use `\tilde{R}` for the random variable and `(\fprate, \tprate)` for the parameters, or (b) introduce a separate symbol for the parameterized distribution and the random variable drawn from it. The cleanest fix: state once that `\tilde{R}` refers to a random subset of U drawn from the parameterized Bernoulli model.

#### P6 (Minor): Notation reference includes unused or partly-used symbols
- **Location**: `sections/appendix.tex` lines 35-36, 82.
- **Problem**: Cartesian products `\Set{A} \times \Set{B}`, n-fold products `\Set{B}^n`, CDF `F_{\RV{X}}`, and `\Set{A} \setminus \Set{B}` (set difference) appear in the notation reference but not in the active paper body. These are vestiges of the pre-extraction manuscript.
- **Suggestion**: Trim the notation reference to symbols used in the active 18-page paper.

#### P7 (Suggestion): Remark 3.4 (parametric parsimony) phrasing
- **Location**: `sections/bernoulli_model.tex` lines 54-62.
- **Quoted text**: "the Kronecker factorization reduces this to $4$ (one response rate per block per set)."
- **Problem**: "One response rate per block per set" is dense. For two sets each with 2 blocks (positives/negatives), this is `2 * 2 = 4` rates, but the wording requires unpacking.
- **Suggestion**: Add a short parenthetical: "(two rates per set, one for positives and one for negatives, multiplied by two sets equals four)".

#### P8 (Suggestion): "Section ... derives ... derives" repetition in organization paragraph
- **Location**: `sections/intro.tex` lines 41-43.
- **Quoted text**: "\Cref{sec:setalgebra} reviews the algebra of sets. \Cref{sec:bernoulli_model} introduces the Bernoulli set model and its axioms, including the higher-order composition theorem. \Cref{sec:characteristics} derives the binomial distributions of error counts and their asymptotic normal limits."
- **Problem**: Three short sentences in parallel construction is fine, but the second sentence has been growing as content was added. Consider tightening for parallel rhythm.
- **Suggestion**: Optional. "Section 2 reviews the algebra of sets. Section 3 introduces the Bernoulli set model, its axioms, and the higher-order composition theorem. Section 4 derives the error-count distributions and confidence intervals."

## Notation Consistency Across the Trapdoor-Computing Program

Cross-checked with `trapdoor-computing/papers/cipher-maps/paper/cipher_maps.tex`:
- `\fprate`, `\fnrate`, `\tprate`, `\tnrate` (the four Greek-letter rates) match across both papers.
- Cipher-maps also uses `\hat{}` for observed rates (consistent).
- Cipher-maps introduces an additional symbol `\eta` for cipher-map correctness (FNR-like), which does not clash with the Bernoulli notation.

The trapdoor-computing program citation of this paper uses the key `bernoulli-types` rather than `bernoulli-sets`. This is bibliography-level, not prose-level, but is a coordination issue when the citing papers describe "Bernoulli Sets and Maps" as a single artifact and the present paper splits the framework into bernoulli_sets, bernoulli_maps, bernoulli_data_type, etc.

## Strengths

- The explanatory Remark 3.5 ("Notational convention for alpha and beta") is exactly the right kind of meta-text to defuse a previous reviewer concern.
- The Remark 3.1 (Relation to binary channels) is honest about classical precedent.
- Section structure progresses cleanly: classical sets, model, distributions.
- The alex.sty notation is comprehensive and applied with discipline (except for the line-157 issue).

## Recommendation

The writing is solid. The one major issue (P1) is technical, not narrative. The minor issues are mostly carryovers from the previous review that should be picked off before submission.
