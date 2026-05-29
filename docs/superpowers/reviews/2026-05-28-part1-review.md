# Part I Review (chapters 1-4)

Date: 2026-05-28
Reviewer: bookwright reviewer orchestrator (Part I scope)
Specialists dispatched: spec-auditor, quality-auditor, math-auditor, cross-ref-auditor across chapters 1, 2, 3, 4

This review evaluates all four chapters of Part I ("The Atom") of
*Bernoulli Types: An Algebra of Approximate Computation* against the
Part I design spec (`docs/superpowers/specs/2026-05-02-bernoulli-textbook-part1-design.md`)
and the master spec (`docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`).
The four auditor roles were applied in series across each chapter and the
findings are synthesized below by chapter and by cross-chapter coherence.

## Summary

- **Total findings: 38** (1 BLOCKER, 7 MAJORs, 19 MINORs, 11 NOTEs).
- **Top high-priority items:**
  1. (BLOCKER) §3.4 line 184-188: the chained inequality `fprate_k <= fprate^k <= (1/4)^k` reuses `\fprate` (single symbol) to mean two different things (per-round rate and worst-case 1/4 bound) and writes the middle term as a power of a single rate when, by the section's own wording, per-round rates may differ. The correct form is `fprate_k = prod_i fprate_i <= (1/4)^k`. Reads as a typo to a careful reader and is a regression-risk magnet.
  2. (MAJOR) §3.5 line 60 (Bloom filter formula): the foreshadowing formula `p = 1 - (1-1/n)^k` is presented without distinguishing the hash count from the bit-array size from the insert count. The variables `n` and `k` clash with the standard Bloom analysis. Reads as wrong even though chapter 5 will set it right.
  3. (MAJOR) §3.1 lines 220-247: the closed-form FPR of AND under noise mixes a distribution-dependent ratio (eq. `eq:and-fpr-general`) with an "input-distribution-free bounds" claim that does not produce a single rate. §4.5 then declares AND a type-closed binary operation `Bernoulli[bool] x Bernoulli[bool] -> Bernoulli[bool]`. The mismatch is reconcilable but is not reconciled in the text.
- **Chapters with most findings:** Chapter 3 (15), Chapter 4 (10), Chapter 2 (7), Chapter 1 (6).

The chapters are in strong shape overall. No content checklist items from
the Part I design spec are missing. All three running threads (BSC,
biased coin, classifier verdict) carry across all four chapters at their
named return points. The two Part I climaxes (§3.4 Miller-Rabin and §4.4
Kronecker) are present and substantive. The math is numerically correct
across every checked computation. The cross-reference baseline (the
three documented deferred items: `ch:composition`, `ch:sketches` x 5,
`sec:noisy-bit` x 2) matches the build log exactly; no new undefined
references appear in Part I scope. No em-dashes, no banned
soul-voice phrases, no "easy to see" / "obviously" handwaves.

The findings below are sorted by severity within each chapter, then by
location.

## Findings by chapter

### Chapter 1: The Noisy Bit (~21 pp; target ~25 pp)

**spec-auditor:** all checklist items present in spec §4 are realized.
Three faces (§1.1), FPR/FNR contingency table (§1.2), Boolean universe
qualitative walk (§1.3), sampling+CLT hook (§1.4), why-atom trajectory
(§1.5), Bibliographic Notes (§1.6), 11 exercises with 3/5/3 difficulty
distribution. Notation sidebar lands in §1.2 as specified.

**quality-auditor (cold read):** the chapter reads cleanly. Three
framings are distinct and motivated. The §1.5 atom argument is
substantive, not handwave. The Miller-Rabin tease lives in one
paragraph as the spec required.

**math-auditor:** verified all numerical claims independently. Spam
filter table (FPR=0.05, FNR=0.125, precision=35/38≈0.921, recall=0.875)
is correct in every cell. Joint table in exercise 3 sums to 1.

**cross-ref-auditor:** all DEFINED labels match `\label{}` declarations;
no collisions. All RESOLVED labels exist in the book tree. Header
comment blocks are accurate and up to date with Plan 4 closure.

#### Findings (chapter 1)

- **MINOR** §1.1 line 54 (`three-faces.tex`): the sentence "The biased coin returns as a running example throughout Part~I, first in \Cref{sec:asymmetric-channel}..." attaches without a sentence break to the preceding paragraph; reads as two ideas in one run-on. Split.
- **MINOR** §1.2 line 131 (`quantifying-noise.tex`): the sidebar reads "In the biased-coin vocabulary of §1.1, $\tprate$ was written $\tau$ and $\fprate$ was written $\epsilon$." The §1.1 paragraph at line 43-45 uses $\tau$ for the in-bias and $\epsilon$ for the out-bias (FPR), so the mapping is right, but a careful reader who maps in/out to top/bot may flip the assignment. One clarifying sentence would close the loop.
- **MINOR** §1.2 line 181 ("the full development of these derived measures lives in the companion paper"): the phrasing "companion paper" reads as a generic reference; name the paper (`bernoulli_classification_measures`) inline or push to Bibliographic Notes.
- **NOTE** §1.3 line 51: the closing sentence of the introductory paragraph promises "how the rates of §1.2 fit on top of them" but the rates are not in fact placed on the four cells until §4.5. Consider sharpening to "how the rates of §1.2 will fit on top of them once the joint formalism is in hand (§4.5)."
- **NOTE** §1.4 lines 88-108: the Wald confidence interval is introduced with a clean derivation, but the section never says "Wald" before using it. A one-line gloss ("the resulting interval is called Wald") would help readers who arrive without the prior vocabulary.
- **NOTE** §1.5 line 70: the parenthetical "$B_1 = \{\top\}$, $B_2 = \{\bot\}$" appears before §2.4 defines the block partition. Reads fine but is the first place block notation slips into chapter 1; consider one half-sentence of forward gloss or leave the brackets undefined here.

### Chapter 2: Binary Channels and Model Order (~23 pp; target ~24 pp)

**spec-auditor:** all five sections present per spec §5. The BSC §2.1
combines formal definition and channel matrix as the spec called for.
§2.3 (Composition of Channels) is the fresh section that sets up §3.3.
§2.4 Model Order delivers the Boolean Ceiling theorem with proof.
Bibliographic Notes flag the model-order-vs-DOF clarification.
Exercises: 10 with 3/5/2 difficulty distribution (spec called for 3/5/3;
the third ★★★ exercise count is short by one).

**quality-auditor (cold read):** the chapter is the most matrix-heavy
of Part I and reads cleanly. Worked examples (BSC with eps=0.05;
asymmetric channel with fpr=0.05, fnr=0.10; BSC composition with
eps_1=0.05, eps_2=0.10) all have explicit arithmetic. The §2.4 ordering
discussion (BSC model-order-1 by partition count vs. order-2-with-symmetry
in the broader framework) is the chapter's most subtle move and is
handled clearly.

**math-auditor:** verified all numerical claims independently. BSC
composition gives 0.14 as stated; asymmetric matrix arithmetic checks;
BSC capacity 1-H(eps) is correctly stated (Cover-Thomas convention).

**cross-ref-auditor:** label hygiene is perfect. The forward reference
`\ref{ex:bsc-capacity}` in §2.1 line 304 resolves to the exercise label
in §2 exercises (medium tier).

#### Findings (chapter 2)

- **MAJOR** §2.4 lines 134-165 (model order ambiguity): the chapter
  carefully distinguishes "BSC has model order 1 by finest-partition
  count, but order 2 in the broader framework". This subtle resolution
  is essentially right but reads inconsistently across the chapter.
  §2.1 line 144 says "the BSC has a single free parameter; the general
  order-2 channel has two" (treating BSC as order 2). §2.4 line 144
  says "the BSC's finest compatible partition has one block, so model
  order 1". §2.4 line 163 says "we will work in the order-2 framework
  throughout chapters 2--4, treating the BSC as a constrained member of
  that family". A reader who quotes any single sentence in isolation
  gets a different answer. One synthesizing sentence in §2.1 (saying
  "we adopt the order-2 framing throughout Part I, with BSC as the
  symmetric constrained subcase; the partition-count perspective is in
  §2.4") would lock this in.
- **MINOR** §2.1 line 296: "the *capacity* of the BSC ... is $1 - H_2(\fprate)$ bits per use, where $H_2(\fprate) = -\fprate \log_2 \fprate - (1-\fprate) \log_2(1-\fprate)$." The text defines $H_2$ but earlier line 95 references "the capacity formula $1 - H(\fprate)$" without the subscript-2. Standardize.
- **MINOR** §2.2 line 84 (footnote on Z-channel direction): the footnote uses `\omega` and `\varepsilon` for the rate symbols rather than the book's `\fprate` and `\fnrate`. Minor, but the rest of the book is consistent.
- **MINOR** §2.3 line 332: "the figure in the companion paper [bernoulli_sets] (Figure 3.1), which shows both TPR and FPR converging to..." names a figure the reader cannot see. Either describe what the figure shows in one sentence (and what to compare against in the text) or move the reference to Bibliographic Notes.
- **NOTE** §2.4 line 167-194: the Boolean Ceiling Theorem statement and proof are both clean; the proof is one paragraph and could be condensed to half that without losing rigor. Leave as-is is fine; flagging for the polish pass.
- **NOTE** §2 exercises: spec called for 3 challenging exercises (★★★); only 2 appear (exercise 7 wasn't moved up to the warm-up tier but it's also marked ★★★ in the source). Exercise count is at 10 of the spec's 10-12 range, so still in range. Recommend adding one more ★★★ exercise in a polish pass if time permits.
- **NOTE** §2.5 line 80-86: "Further reading" paragraph repeats the §2.4 model-order vs. degrees-of-freedom point already made in the chapter body. Trim or remove.

### Chapter 3: Boolean Algebra Under Noise (~29 pp; target ~28 pp)

**spec-auditor:** all six sections present per spec §6. §3.1 explicitly
flags Axiom 2; §3.4 has the 5-step Miller-Rabin walkthrough with
pseudocode and the n=341 numerical example pinned (Open Action Item 2
from the spec is resolved by this). §3.5 has the three named bridges
(Bloom filter, set operations, map composition) called for. 11
exercises with 3/5/3 difficulty distribution. The composition theorem's
BSC subtlety (cancellation invalidates `1 - prod(1-eps)`) is handled
carefully in §3.3.

**quality-auditor (cold read):** the chapter is the densest in Part I.
The §3.1 AND derivation is exhaustively case-split. The §3.3 composition
theorem is stated and proved with explicit BSC counterexample, which is
unusually honest pedagogy and is one of the chapter's strengths.
The §3.4 Miller-Rabin walkthrough delivers the unification thesis and
reads as the climax it is.

**math-auditor:** verified all numerical claims independently. AND
worked example (fnr_AND=0.164, fpr_AND≈0.057) checks. The §3.3 4-stage
example (fpr_AND4=0.541) checks. The §3.3 BSC comparison (0.18 vs 0.19
at eps=0.1) checks. Miller-Rabin n=341 with a=2: 2^85 mod 341 = 32; 32^2
mod 341 = 1; the algorithm correctly returns "composite". (1/4)^k for
k=1,5,20 produces the stated 0.250, 9.8e-4, 9.1e-13.

**cross-ref-auditor:** label hygiene is perfect. All chapter 4 forward
references resolve to existing labels.

#### Findings (chapter 3)

- **BLOCKER** §3.4 lines 184-188 (`miller-rabin.tex`): the displayed inequality reads
  ```
  fprate_k <= fprate^k <= (1/4)^k
  ```
  Here `\fprate` is used twice with two different meanings: once as a stand-in for the per-round rate (which the surrounding prose lets vary across rounds; the section says "each round is a Bernoulli[bool] instance with fnr_i=0 and fpr_i <= 1/4"), and once as the worst-case bound 1/4. The middle term `fprate^k` is only correct if every round has the same rate; otherwise it should be `prod_i fprate_i`. The very next paragraph (lines 191-198) gives the correct argument with the product `prod_i fprate_i`. A careful reader notices the inconsistency. Replace the middle term with `prod_i fprate_i` or with `(max_i fprate_i)^k`.
- **MAJOR** §3.1 lines 220-247 (`and-under-noise.tex`): the closed-form FPR of AND has two distinct treatments in the same section. Eq. `eq:and-fpr-general` gives the prior-mixed formula that depends on $\pi$; lines 233-247 give "the input-distribution-free bounds" that bound by `min(\fprate_1,\fprate_2)`. §4.5 then declares AND a binary closure operation `Bernoulli[bool] x Bernoulli[bool] -> Bernoulli[bool]`. But the closure type-signature requires a single derived rate, which the prior-dependent formula does not deliver. A reconciling sentence is needed: either "AND's effective FPR depends on $\pi$, so AND-as-closure produces a *family* of `Bernoulli[bool]` indexed by $\pi$" or "the input-distribution-free upper bound `min` is the operational rate we use in the closure claim". §3.1 takes neither stance crisply and §4.5 silently assumes the second.
- **MAJOR** §3.5 lines 56-74 (`bridge-to-sets.tex`): the Bloom filter formula `p = 1 - (1-1/n)^k` is stated with `n` = bit-array size and `k` = elements inserted. But §3.5 also uses `m` = number of hash functions ("the classical construction uses $m$ independent hash functions"). The standard Bloom analysis is `1 - (1 - 1/b)^{m*k}` where `b`=bit-array size, `k`=elements inserted, `m`=hashes per insert. The formula as written drops the `m` factor in the exponent. This is foreshadowing for chapter 5, but the formula is wrong as stated. Either remove the explicit formula and say "per-hash false-positive rate $p$ (formula deferred to chapter 5)" or correct the exponent to `m*k`.
- **MAJOR** §3.3 lines 240-248: "These two formulas are different. correct (§2.3): 0.18; naive (§3.3): 0.19. The naive formula overestimates the BSC's end-to-end error rate." Pedagogically this is the right move. But the prose calls the §3.3 formula "naive" three times in the same passage. Word choice undersells the theorem: §3.3 is correct for its model (identity-with-error), not naive. The discrepancy is structural (different assumption), not a bug in §3.3. Replace "naive" with "identity-with-error" or "at-least-one-error" to keep the §3.3 result respectable.
- **MAJOR** §3.3 line 244 ("the composition theorem of this section applies to a different underlying model: each stage either preserves correctness or destroys it, with no possibility of recovery"): this is correct, but appears *after* the worked-example comparison with BSC. Reorder: state the model assumption first, then compare with the BSC. As written, a reader who skims may conclude §3.3 is "wrong" when it is "right under different hypotheses".
- **MINOR** §3.1 line 197-198 (`and-under-noise.tex`): "the false-positive rate of the AND gate is the probability that the observed AND is $\top$ given that the true AND is $\bot$" then immediately defines `\pi_1 = \pi`, `\pi_2 = \pi` "assuming the two bits are drawn from the same prior for simplicity". The general formula (with distinct priors) is never written down despite the parenthetical promise. Either write it or drop the parenthetical.
- **MINOR** §3.2 line 168-173 (OR-via-De-Morgan derivation): the "swapped rates" for negated inputs use parameter names $(a_i, c_i)$ in the prose ("for two `Bernoulli[bool]` instances with rates $(a_1, c_1)$ and $(a_2, c_2)$"), and then says "now with the input FPRs equal to $\fnrate_1, \fnrate_2$ (the swapped values)". The dual letter scheme reads as a typo. Drop $(a_i, c_i)$ and use $(\fprate, \fnrate)$ throughout.
- **MINOR** §3.3 line 282: "$\Pr[\text{exactly 2 flips}] = \fprate^2$". For two stages with the same crossover $\fprate$, this is correct; for two stages with different crossovers $\fprate_1, \fprate_2$, it would be $\fprate_1 \fprate_2$. The earlier text fixed equal crossovers `$\fprate_1 = \fprate_2 = \fprate$`, so this is fine, but the reader who skips two lines may briefly stumble.
- **MINOR** §3.4 line 220 ("at $k=20$ rounds, the probability of a false positive is below $10^{-12}$"): the inequality is below $10^{-12}$ but the precise value is `9.1 × 10^{-13}`, i.e. an order of magnitude smaller. Tighten to "below $10^{-12}$ (in fact close to $10^{-13}$)" to land the practical point.
- **MINOR** §3.4 line 268 (Carmichael 561): exercise 6 mentions 561 is a Carmichael; §3.4 only mentions 341 as Fermat pseudoprime. One sentence in §3.4 saying "Carmichael numbers (such as 561) defeat the Fermat test for *every* witness coprime to $n$; Miller-Rabin still correctly identifies them as composite via the strong-liar bound" would tie the Carmichael case to the chapter prose.
- **MINOR** §3.5 line 91: the bridge to Miller-Rabin says "The Bloom filter's per-hash $\fprate$ is a design parameter controlled by the bit-array size and insertion count." A parenthetical pointing to chapter 5 would close the loop ("(see §5.x for the exact relationship)").
- **NOTE** §3.3 lines 400-430: the "chain-stage independence vs. element-wise independence" digression is correct and important but long; could compress to half the length without loss. Polish-pass item.
- **NOTE** §3.4 line 314-318: the table of error bounds for k=1,5,20 appears twice in the section (once at line 207-217, once at line 301-311). Both are correctly worded, but the second is the more useful framing (tied to the n=341 example). Consider merging.
- **NOTE** §3.4 line 380: "we have not given the most general treatment of randomized primality tests. The Las Vegas versus Monte Carlo distinction ... belongs to chapter 11." Good signposting; the §3.5 forward reference to chapter 11 should say the same.
- **NOTE** §3.6 lines 81-110: the "three abstraction layers, one composition algebra" section is pedagogically valuable and unique to this textbook (per the §3.6 closing line). Consider promoting to a body subsection rather than burying in Bibliographic Notes, where most readers will not see it.

### Chapter 4: Two Axioms and Kronecker Factorization (~30 pp; target ~28 pp)

**spec-auditor:** all seven sections present per spec §7. §4.1 motivates;
§4.2 states Axiom 1 with the classifier-verdict callback as the spec
called for; §4.3 states Axiom 2 with the Markov violation as the spec
called for; §4.4 has the Kronecker theorem statement, full proof,
parameter-count corollary, and the BSC running thread; §4.5 has the
biased-coin worked example that the §1.3 deferral pointed at. Open
Action Item 4 (whether to split proof to appendix) is resolved in favor
of keeping the proof in the main text; the §4.4 length of ~7 pp is at
the spec's upper bound but not over. 11 exercises with 3/5/3 difficulty
distribution.

**quality-auditor (cold read):** the chapter is the most formal in Part
I and earns the formal step. The conditional vs. unconditional split
for the Kronecker theorem (Theorem 4.4.1 and Corollary 4.4.2) is more
careful than the companion paper and is a genuine contribution. The
§4.5 biased-coin Example 4.5.1 retires the §1.3 deferral cleanly.

**math-auditor:** verified all numerical claims independently. §4.2
correlation arithmetic (joint = 0.064 with rho=0.6 at fpr=0.10) checks.
§4.3 Markov table (6x inflation for (+,+) outcome at fpr_0=0.05,
fpr_1=0.30) checks. §4.4 Q⊗Q matrix at eps=0.05 produces the stated
0.9025/0.0475/0.0025 entries. §4.5 biased-coin PMF (TP=0.54, FN=0.06,
FP=0.02, TN=0.38) sums to 1.000.

**cross-ref-auditor:** label hygiene is perfect. The cross-chapter
backward references (§4.1 to §3.3, §4.2 to §3.4, §4.4 to §3.1, §4.5 to
§1.1-§1.3 and §2.1-§2.2 and §3.1-§3.3) all resolve.

#### Findings (chapter 4)

- **MAJOR** §4.4 lines 220-236 (honesty note): "The parametric parsimony observation underlying this theorem appears as Remark 3.4 in the companion paper, which notes that Axiom 1 forces the joint confusion matrix to factor as a Kronecker product. The companion paper states this remark in a regime where rates are either deterministic or implicitly conditioned upon..." This is a substantive honesty note and a real contribution, but the prose is dense and reads as a confession buried after the proof. Promote to a clearly-marked "Comparison with the source paper" subsection (the way §2.5 handles the model-order-vs-DOF reconciliation) so the contribution is visible to a citation-reading reader.
- **MAJOR** §4.5 lines 295-310 (chapters 1-3 as instances): the recap of AND, OR, NOT type signatures is correct but the prose says "AND is a binary operation `Bernoulli[bool] x Bernoulli[bool] -> Bernoulli[bool]`" without addressing the §3.1 prior-dependence issue (see the related Chapter 3 MAJOR finding above). §4.5 silently assumes AND's effective FPR is a single number; §3.1 left it as a $\pi$-mixture. Either §4.5 should resolve the ambiguity ("AND's output is `Bernoulli[bool]` after specifying the input prior $\pi$, or after taking the worst-case upper bound") or §3.1 should pre-resolve it.
- **MINOR** §4.1 line 113-116 ("This is not merely an algebraic convenience. It is the theorem that makes the Bernoulli framework useful in practice."): the framing of Axiom 2 as the "second hidden assumption" comes after a long opening of Axiom 1. Consider one transition sentence between the §4.1 second and third subsections so the reader notices the structural shift from "what's hidden" to "what's bought".
- **MINOR** §4.2 line 22-30 (framing-note paragraph): the disclaimer that Axiom 1 governs "distinct input elements of a *single* approximate predicate", distinct from chain-stage independence, is correct but reads as a defensive prefix to the formal definition. Move to a Remark right after the axiom statement or fold into the existing classifier-verdict callback subsection.
- **MINOR** §4.3 line 27 ("we will derive as a formal consequence in `prop:stable-Q`"): in the §4.3 introduction, the future reference to `prop:stable-Q` appears before the proposition is stated. A one-sentence preview ("we state the formal axiom first, then derive the stability consequence") is given two sentences later, but the forward jump in line 27 is loud.
- **MINOR** §4.3 lines 308-319 (Markov channel table): the table caption is "Outcome pair | Probability | Axiom-2 product | Discrepancy". The "Discrepancy" column says "6x inflation" for (+,+) and "deflation" for (+,-), which is inconsistent column-labeling (one is a ratio, one is a direction). Standardize to ratio form ("6x", "0.74x") or symbolic ("inflated", "deflated") throughout.
- **MINOR** §4.4 line 23-30 (introduction): "The question is this. Given $m$ queries on a Bernoulli predicate, each on a distinct element of the universal set---what does the joint confusion matrix look like?" This is the right framing, but the next sentence introduces three notations (`n^m x 2^m`, the per-source-block convention `n(2^m - 1)`, and `nm` under axioms) in two paragraphs. The pedagogical sequence is: state the question, give the unconstrained count, then derive the reduction. As written, the unconstrained `n^m(2^m - 1)` count appears in a sentence before the per-source-block reduction `n(2^m - 1)` is named. A reader who only reads the first paragraph gets the larger number; a reader who reads the second sees the count drop without seeing why. Add one sentence between the two paragraphs that says "the per-source-block convention is the natural choice for the comparison to the Kronecker structure, because it counts only the axiom-induced reduction".
- **MINOR** §4.5 line 152 (footnote on Example 3.5 in the companion paper): the footnote helps but reads as an admission rather than a contribution. Consider rephrasing: "the textbook's joint distribution over (true value, observed report) pairs is a different presentation of the same content; see Example 3.5 of [bernoulli_sets] for the alternative PMF-over-realized-approximate-set-value formulation."
- **MINOR** §4.6 lines 73-78 (Parametric Parsimony status): the principle is "visible in Part I, completed in Part II". The §4.6 prose says "the full principle---why $2m$ parameters are not merely convenient but are, in an information-theoretic sense, the right number---requires the entropy-based lower bounds developed in Part II, chapter 8." Good signposting, but the principle name is "Parametric Parsimony", and the text never uses the words again. Consider one occurrence in chapter body §4.4 corollary discussion ("the corollary establishes Parametric Parsimony at the level of parameter count").
- **NOTE** §4.4 line 110-125 (scope notes): the two scope notes about repeated queries and the rate-conditional vs. unconditional distinction are dense and consume a page. They are correct and probably necessary, but consider moving the second (the Jensen-gap discussion) to a Remark after the proof rather than blocking the theorem statement.

## Cross-chapter coherence findings

These findings only surface when reading across chapters.

- **MAJOR** AND closure type signature (§3.1, §3.2 prop:boolean-closure, §4.5): three places describe what AND does to two `Bernoulli[bool]` instances. §3.1 gives a $\pi$-mixed FPR formula plus a distribution-free upper bound. §3.2 (Proposition 3.2.1, "Closure of Bernoulli[bool] under Boolean operations") asserts that every Boolean formula on `Bernoulli[bool]` instances is again `Bernoulli[bool]` with closed-form rates. §4.5 names AND as a type-closed binary operation. The three statements are reconcilable but the reconciliation is not in the text. The cleanest fix is: §3.1 picks one convention (the distribution-free worst-case bound, since it produces a single derived rate per output) and §3.2 and §4.5 cite that convention.
- **MAJOR** Composition theorem vs. matrix-product composition (§2.3, §3.3, §3.6, §4.4): the text has two composition formulas that look superficially similar but answer different questions. §2.3 gives the matrix-product formula `2*eps - 2*eps^2` for two BSCs; §3.3 gives the "at least one error" formula `2*eps - eps^2` for identity-with-error chains. §3.3 is exceptionally honest about the gap, including a numerical comparison. §3.6 "three abstraction layers" presents both as views of one composition algebra. §4.4 closing comment says they are "complementary, not competing". This is correct, but a single canonical summary box ("two composition formulas, two questions, two regimes") would let a reader who flips to any one section get the orientation. Currently the orientation is spread across §2.3, §3.3 last subsection, §3.6 second paragraph, and §4.4 last subsection.
- **MAJOR** Per-source-block convention (§4.3, §4.4): the parameter-count claim `n(2^m - 1)` appears in §2.4 ("Model order vs. parameter count"), §4.3 ("What Axiom 2 earns us"), and §4.4 ("Two axioms, one payoff" and Corollary 4.4.3). §4.4 finally introduces the "per-source-block convention" that explains the count. §2.4 and §4.3 use the count without naming the convention. A reader who reaches §2.4 first encounters `2(2^m - 1)` without the convention; reaching §4.4 they get the explanation but may not flip back. One pointer in §2.4 ("this is the per-source-block convention; see §4.4 for the definition") would close the loop.
- **MINOR** Notation symbol drift: the book consistently uses `\fprate, \fnrate, \tprate, \tnrate` for the four rates, but `\eta` (the per-stage rate symbol from the composition theorem) is introduced fresh in §3.3 without a notation note. `\eta` then disappears after §3.3. Either flag in §3.3 ("we write $\eta$ to denote a generic per-stage error rate, which becomes $\fprate$, $\fnrate$, or some mixture depending on application") or use the existing rate symbols throughout.
- **MINOR** Three threads carry: BSC carries from §1.1 -> §2.1 -> §3.3 -> §4.4. Biased coin carries from §1.1 -> §2.2 -> §3.1 (AND worked example) -> §4.5 (formal example 4.5.1). Classifier verdict carries from §1.1 -> §1.2 (cross-walk) -> §4.2 (correlated classifiers callback). The classifier-verdict thread is the thinnest; it does not have a substantive return in chapter 3. Spec §3.1 names §4.2 as its closing return; this is met but the thread feels less load-bearing than the other two. Consider a single sentence in §3.1 or §3.2 that uses a spam-filter or medical-classifier example to keep the thread alive between chapter 1 and chapter 4.
- **NOTE** Documented deferred cross-refs unchanged: `ch:composition` in §4.1 line 29 and §4.2 (footnote reference to ch:composition) remain documented forward refs as previously baselined. `ch:sketches` references in chapter 9 and `sec:noisy-bit` references in chapter 17 are outside Part I scope.
- **NOTE** Page budgets vs. spec §9 budget table:

| Chapter | Spec §9 target | Estimated current |
|---|---|---|
| Ch 1 | ~25 pp | ~21 pp (-4) |
| Ch 2 | ~24 pp | ~23 pp (-1) |
| Ch 3 | ~28 pp | ~29 pp (+1) |
| Ch 4 | ~28 pp | ~30 pp (+2) |
| Total | ~105 pp | ~103 pp (-2) |

  All within reasonable tolerance. Chapter 1 is at the low end and the
  spec's risk table predicted ch 1 might compress because of the §1.4
  deferral; this is consistent. No action required.

## Recommended next actions

Ordered by priority.

### BLOCKER (must fix before integration sign-off)

1. **Fix §3.4 lines 184-188** (`book/chapters/ch03/miller-rabin.tex`): rewrite the displayed inequality `fprate_k <= fprate^k <= (1/4)^k` to use `prod_i fprate_i` for the middle term (or qualify "where all rounds share the same rate"). The very next paragraph already gives the correct argument, so the displayed inequality just needs to match the prose.

### MAJOR (should fix before integration sign-off; may defer to a revise pass)

1. **§3.1 / §3.2 / §4.5 AND closure reconciliation:** pick one convention for AND's effective FPR (the distribution-free upper bound is recommended) and use it consistently. §3.1 currently presents both the $\pi$-mixed formula and the upper bound; §3.2 Proposition 3.2.1 and §4.5 silently assume closure under a single rate.
2. **§3.5 line 60 Bloom filter formula:** correct the exponent or remove the explicit formula in favor of a forward pointer to chapter 5.
3. **§3.3 lines 220-260 "naive" framing:** replace "naive §3.3 formula" with "identity-with-error §3.3 formula" or "at-least-one-error §3.3 formula" to keep the §3.3 result respectable while still distinguishing it from the BSC matrix product.
4. **§3.3 reorder model-assumption disclosure:** move the model-assumption statement (line 244 "the composition theorem of this section applies to a different underlying model...") above the BSC comparison so the reader sees the hypothesis before the discrepancy.
5. **§2.4 / §4.4 model-order vs. parameter-count first encounter:** one synthesizing sentence in §2.1 locking in the order-2 framing convention for Part I; one pointer in §2.4 pointing forward to §4.4's per-source-block convention.
6. **§4.4 promote honesty note:** the §4.4 lines 220-236 honesty note is a substantive contribution; promote to a clearly-marked "Comparison with the source paper" subsection.
7. **§4.5 chapters-1-3-as-instances:** address the AND closure ambiguity inherited from §3.1 (related to MAJOR finding 1 above).

### MINOR (polish-pass additions)

Add to the polish-pass list:

- §1.1 line 54 sentence split.
- §1.2 line 131 sidebar tau/epsilon mapping clarity.
- §1.2 line 181 name the companion paper.
- §1.4 line 88-108 name "Wald".
- §2.1 line 296 standardize `H` vs `H_2`.
- §2.2 line 84 standardize footnote notation.
- §2.3 line 332 describe Figure 3.1 or move to Bibliographic Notes.
- §2.5 lines 80-86 trim duplicated model-order paragraph.
- §3.1 line 197 either write the general formula or drop the parenthetical.
- §3.2 lines 168-173 drop $(a_i, c_i)$ dual letter scheme.
- §3.3 line 282 explicit "with equal crossovers" qualifier.
- §3.4 line 220 tighten "below $10^{-12}$" claim.
- §3.4 line 268 link to Carmichael 561.
- §3.5 line 91 parenthetical pointer to chapter 5.
- §4.1 transition sentence between subsections.
- §4.2 reposition framing-note paragraph.
- §4.3 line 27 future reference timing.
- §4.3 lines 308-319 standardize discrepancy column.
- §4.4 line 23-30 introduction sequencing of three notations.
- §4.5 line 152 rephrase footnote.
- §4.6 use the name "Parametric Parsimony" in the chapter body.

### NOTE (defer to a future revision or leave as-is)

- §1.3 line 51 sharpen promise.
- §1.4 introduce "Wald" name.
- §1.5 line 70 block notation gloss.
- §2.4 lines 167-194 Boolean Ceiling proof condense.
- §2 exercises add one ★★★ to hit spec target of 3.
- §2.5 trim further reading paragraph.
- §3.3 lines 400-430 chain-stage vs. element-wise digression compress.
- §3.4 line 314-318 merge duplicate k=1,5,20 table.
- §3.4 line 380 parallel signposting in §3.5.
- §3.6 "three abstraction layers" promote out of Bibliographic Notes.
- §4.4 lines 110-125 move Jensen-gap scope note after the proof.
- Cross-chapter notation: introduce or remove `\eta`.
- Cross-chapter threads: keep classifier verdict alive between chapters 1 and 4.
- Documented deferred cross-refs unchanged.
- Page budgets within tolerance.

## Specialist verdicts (consolidated)

- **spec-auditor:** Part I PASS with one exception (the §3.4 BLOCKER above is a notation typo, not a missing checklist item). All content checklist items from spec §§4-7 are realized; the page budget is within tolerance; the three running threads carry; the two Part I climaxes (Miller-Rabin §3.4 and Kronecker §4.4) are present and substantive.
- **quality-auditor:** "minor polish needed" overall. No chapter requires substantive revision. Chapter 3 has the heaviest revision load (the 5 MAJOR findings above), chapter 4 the second-heaviest (2 MAJORs plus the §4.4 honesty-note promotion). Chapters 1 and 2 are nearly publication-ready.
- **math-auditor:** PASS. Every numerical claim checked verifies independently. No regression of any baseline-flagged value. The §3.4 Miller-Rabin walkthrough for n=341 with witness a=2 produces the correct outputs at every step. The §4.4 Q⊗Q matrix at eps=0.05 produces the stated entries. The §4.2 correlation arithmetic (joint = 0.064) and the §4.3 Markov table (6x inflation) both check.
- **cross-ref-auditor:** PASS. All DEFINED labels match declarations; no collisions; all RESOLVED labels exist; the three documented deferred items (`ch:composition`, `ch:sketches` x 5, `sec:noisy-bit` x 2) match the book.log baseline. No new undefined references in Part I scope.

## Overall recommendation

Part I is in strong shape. The one BLOCKER (§3.4 displayed inequality)
is a notation typo that the author can fix in five minutes. The seven
MAJOR findings are clustered in chapter 3 and chapter 4 and represent
the editorial work most worth doing before sign-off. The 19 MINORs and
11 NOTEs are appropriate polish-pass material.

The book's pedagogical voice is consistent across all four chapters.
The "intuition first, formalism at the end of Part I" trajectory the
spec described is achieved. The §3.4 Miller-Rabin walkthrough and the
§4.4 Kronecker theorem-with-proof both deliver as the climaxes the spec
called for.

Recommend: fix the BLOCKER now, schedule the seven MAJORs for a
focused revision pass, and queue the rest for a polish pass before
Milestone 1.
