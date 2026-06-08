# Post-Salvage Review: "The Abstract Data Type of the Approximate Relation"

**Date**: 2026-06-07 (post-salvage cycle)
**Paper**: `papers/bernoulli_relations/`, *The abstract data type of the approximate relation* (Alexander Towell)
**Reviewer pass**: thesis / proof / general review of the CURRENT (salvaged) state
**Prior review**: `.papermill/reviews/2026-06-07/review.md` (pre-salvage salvageability assessment, superseded by this pass)

## Verdict: MINOR-REVISIONS

The salvage worked. This is now a coherent, internally consistent, honestly-scoped paper whose load-bearing results I independently re-derived and cross-checked against both the Monte Carlo harness and the sibling composition paper. **Every closed-form rate is correct.** The three prior errors are genuinely fixed. The residual issues are all cosmetic or expository (terminology drift in one section opening, two dead macros, a couple of expository soft spots); none blocks correctness and none is critical. With the handful of MINOR fixes below the paper is submittable as a Zenodo preprint and is close to ICDT/PODS-workshop quality on the writing.

I found **zero critical** and **zero major** issues. Findings are MINOR and SUGGESTION only.

---

## 1. Thesis coherence

**Verdict: coherent and consistently argued.** The relation-as-Bernoulli-set / operator-propagation / invariant-preservation thesis is stated identically in the abstract, the intro contributions list, the section bodies, and the application, and every headline claim is backed by a theorem.

- **Abstract to body traceability** (all verified present and matching):
  - "selection is rate-transparent" maps to `thm:select`.
  - "projection amplifies the FPR to `1-(1-ε)^k` and raises the model order while preserving element-wise independence" maps to `thm:project` plus `thm:project_order`.
  - "join does NOT preserve element-wise independence; shared-component tuples are correlated" maps to `thm:join_dependence` (the `1/a` factor).
  - "reflexivity, symmetry, single-valuedness, transitivity preserved with probability tending to 0; symmetric closure as the cheap repair" maps to `thm:reflexive`, `thm:symmetric_preservation`, `thm:symmetric_closure`, `thm:functional`, and section `sec:transitive`.
  - "single-valued special case is the approximate partial function (dictionary)" maps to `def:approx_pfun`, section `sec:map`.

- **No residual over-claim.** I scanned specifically for the three banned over-claims:
  - **Entropy/space bound**: appears only as a deferral cite to `bernoulliEntropy` (abstract, intro "Companion papers", section `sec:trapdoor_rel_model`). Not derived here.
  - **Perfect-hash-map / optimal construction**: deferred to `phf` and "a further companion"; the application explicitly says "The construction is not new machinery" (oblivious_rel_model.tex:8).
  - **Map composition**: the old map-composition machinery is cut; section `sec:map` (properties.tex:215, and the comment block 217-223) states map composition is "owned, and proved correctly, by the maps paper" and only cites `ω_{g∘f} = 1-(1-ω₁)(1-ω₂)`.
  - Automated check `we (prove|show|...) (entropy|space bound|perfect hash|map composition)` returned no hits.

- **Probabilistic-databases distinction (intro "Related work", intro.tex:62-78): accurate and fair.** The contrast is correctly drawn: probabilistic/uncertain DBs (Suciu et al.; Trio; MayBMS) model uncertainty *in the data* (tuples carry probabilities/lineage; a DB denotes a distribution over possible worlds), whereas here an *objective base relation* is exact and the error is injected by a *space-saving representation*. The claim that the possible-worlds literature "does not ask whether an approximated symmetric relation stays symmetric, or how a projection's fan-in amplifies a structural FPR" is a fair characterization of the distinction in object, not a strawman. The three system citations (Trio/CIDR 2005, MayBMS/SIGMOD 2009, Suciu et al. 2011 Morgan & Claypool) are bibliographically well-formed. **NEEDS VERIFICATION (no web access):** that these are the most apt representatives and that no closer prior art exists on *representation-induced* relational error propagation (e.g., Bloom-filter join/semijoin selectivity error, approximate query processing). Flagged for you to spot-check, not asserted.

## 2. Proof correctness

I independently re-derived every load-bearing result by exact probability algebra and cross-checked against `code/validate.py` (which I ran: 23 fit rows PASS, **worst absolute error 0.000686** over 2×10⁶ trials; the one deliberate MISMATCH row is the join independence-failure demonstration, behaving exactly as predicted). All correct.

- **Selection transparency** (`thm:select`): correct. Restriction to `U_θ` selects a sub-collection of i.i.d. trials; rates unchanged, independence preserved, model stays first-order. Proof is clean.

- **Projection FPR `1-(1-ε)^k`** (`thm:project` (i)): correct. OR over `k` distinct (hence independent) fiber tuples, each a true negative firing w.p. `ε`; miss-all `= (1-ε)^k`. Verified: k=2 to 0.097500, k=3 to 0.142625, k=8 to 0.336580. The `≥ ε_R` bound is right.

- **Projection TPR `1-(1-τ)^j(1-ε)^{k-j}`** (`thm:project` (ii)): **correct, including the multiple-true-fiber-tuple case (j ≥ 2).** I checked this specifically because it is the subtlest part. The fiber is partitioned into `j ≥ 1` genuine members (each missed w.p. `1-τ`) and `k-j` non-members (each missed w.p. `1-ε`); by independence the projection misses `s` iff all `k` trials miss, `= (1-τ)^j(1-ε)^{k-j}`. The formula correctly handles `j ≥ 2` (validate.py exercises (3,2) and (5,2): analytical 0.990500 / 0.991426, both PASS). The "TPR is boosted because a non-member fiber tuple can itself false-positive and rescue a genuine member" reading is accurate.

- **Model-order claim** (`thm:project_order`): correct. Distinct projected tuples have disjoint fibers (since `t|_Y = s` and `t|_Y = s'` are incompatible for `s ≠ s'`), so the per-tuple acceptances are functions of disjoint independent trial sets, hence mutually independent, hence element-wise independence preserved; but the per-tuple rate depends on fan-in `k(s)`, which is non-constant, hence one rate-block per attained fan-in value, hence higher model order. The model-order vs. parameter-count remark (rel_algebra.tex:233-240) is consistent with the `bernoulliSets` framing. `cor:uniform_fanin` (the first-order recovery at constant `k`) is correct.

- **Join FNR `ω_R+ω_S-ω_R ω_S`** (`thm:join` (i)): correct, and **the deferral to composition is accurate.** I read `bernoulli_composition/sections/set_theory.tex`: `thm:intersect_fnrate` gives exactly `ω = 1-(1-ω₁)(1-ω₂)`. The join is a logical AND of two independent operand membership tests, so its FNR is the intersection FNR. `1-τ_R τ_S = 1-(1-ω_R)(1-ω_S) = ω_R+ω_S-ω_R ω_S`, algebra verified (=0.19 at ω=0.1).

- **Join FPR three-region framing** (`thm:join` (ii)): **correctly stated, including the deferral.** The both-absent corner is `ε_R ε_S`; the one-absent regions contribute `ε_R τ_S` and `τ_R ε_S`; the full unconditional FPR is the prevalence-weighted average of all three, which the theorem *correctly* says is "the intersection rate of two Bernoulli sets [bernoulliComposition]" and **does not** claim `ε_R ε_S` is the whole FPR. It explicitly warns "the value `ε_R ε_S` alone is only the both-absent corner and understates the rate whenever a one-absent region has positive prevalence" (rel_algebra.tex:308-311). I confirmed against `bernoulli_composition` `thm:intersect_fprate`: `ε = w₁(1-ω₁)ε₂ + w₂ε₁(1-ω₂) + w₃ε₁ε₂`, i.e. exactly the three weighted regions, with `w₃ε₁ε₂` the both-absent corner. The deferral citation is precise and honest.

- **Join independence failure, factor `1/a`** (`thm:join_dependence`): correct. This is the paper's sharpest result and it holds. For two outputs `(r,s₁),(r,s₂)` sharing left component `r` (with `A={r∈R̃}`, `P(A)=a`, `B_i={s_i∈S̃}` independent of `A` and each other): `P(both) = P(A∩B₁∩B₂) = a·P(B₁)·P(B₂)` (the shared `A` is counted once), whereas the product of marginals is `(a P(B₁))(a P(B₂)) = a²P(B₁)P(B₂)`; ratio `1/a > 1` for `0<a<1`. Positive correlation, joint exceeds product. Verified empirically: P(both)=0.728758 ≈ correlated 0.729, NOT independent 0.6561; factor 1.110742 ≈ 1/a=1.1111. The follow-up caveat (rel_algebra.tex:359-362) is itself correct and worth keeping: marginal rates of `thm:join` remain exactly right per single tuple, and the FP *count* expectation still works tuple-by-tuple by linearity (which does not need independence); only higher moments and the all-correct probability feel the correlation.

- **Invariant rates** (all correct):
  - **Reflexive `τ^|A|`** (`thm:reflexive`): `|A|` independent diagonal trials, each a TP w.p. `τ`; all-fire `= τ^|A|`. Verified |A|=3 to 0.729, |A|=8 to 0.430467.
  - **Symmetric preservation** (`thm:symmetric_preservation`): `(τ²+ω²)^P((1-ε)²+ε²)^N`. Each unordered pair needs its two ordered trials to *agree*; positive pair agrees w.p. `τ²+ω²`, negative pair w.p. `(1-ε)²+ε²`; pairs disjoint, hence product. Correct. (Bases 0.82 and 0.905 at the illustrative rates.) Each base is a sum of two squares of complementary probabilities, hence `< 1` for interior rates, hence tends to 0. Correct.
  - **Symmetric closure** (`thm:symmetric_closure`): FPR `1-(1-ε)²`, TPR `1-(1-τ)²`, the OR over the two ordered trials. **The prior bug (TPR left as unchanged `τ`) is fixed**: both slots now carry the doubling, and the proof explicitly notes "the same doubling that raises the FPR of the OR also raises the TPR ... not the unchanged `τ`" (properties.tex:118). Verified 0.0975 / 0.990, both PASS in MC.
  - **Functional `(1-ε)^{|Y|-1}`** (`thm:functional`): single-valuedness breaks only via a *false positive* adding a spurious second value (a false negative on the true value leaves 0 values, still single-valued, correctly excluded from the product). `|Y|-1` non-true values, each an independent FP trial; no-spurious `= (1-ε)^{|Y|-1}` per key, product over defined keys `= (1-ε)^{|Dom|(|Y|-1)}`. Correct (|Y|=4 to 0.857375). The asymmetry argument (only FPs hurt) is right.
  - **Transitivity** (section `sec:transitive`): handled honestly, no spurious closed form. The reasoning (≈|A|³ coupled triple constraints; preservation decays fastest; manufactured-conclusion pairs each contribute a factor near `ε`; transitive closure is a genuine cascade with no fixed per-pair cost) is qualitatively correct and appropriately hedged. **Unstated assumption worth a word** (see MINOR-4): the "factor near `ε`" leading-behavior claim treats the manufactured-conclusion trials as approximately independent, which the same paragraph elsewhere says they are not; the prose is careful enough that this reads as heuristic, but one clause would seal it.

- **def:approx_rel** (approx_rel_model.tex:37-51): **the prior "conditions on its own negation" defect is fixed.** Condition (i) is now `P((R^∁)_ω^ε(X) | R(X)) = ω`, the event "tuple is in the complement-approximation" (= "tuple is not in R̃") conditioned on the *objective* membership `R(X)`. This is `P(missed | genuine member) = ω = FNR`. Correct, and the complement-approximation's rate slots are correctly swapped (`[ω][ε]`, since complementation exchanges FPR with FNR). Condition (ii) conditions on `R^∁(X)` (genuine non-member) giving `ε`. Both correct.

- **def:approx_pfun** (properties.tex:284-299): **fixed.** Condition (i) conditions on `∈ Dom(f)`, condition (ii) on `∉ Dom(f)`. No self-negation.

- **Equality/subset predicate deferral** (approx_rel_model.tex:99-115): **accurate.** The per-element agreement probabilities stated, positive tuple `τ₁τ₂ + ω₁ω₂` and negative tuple `ε₁ε₂ + η₁η₂`, match `bernoulli_composition` `cor:equality_prob` *exactly* (`(τ₁τ₂+ω₁ω₂)^|X|(ε₁ε₂+η₁η₂)^{|U\X|}`), and the "mutually exclusive, so no correction term" justification is the correct reading of why the prior draft's `-τ₁τ₂ω₁ω₂` term was a sign bug. The `cor:equality_prob` label is cited by name and resolves in the composition paper. Subset deferral likewise matches the composition subset theorem.

- **Inherited machinery** (`thm:fpbinom`, `thm:fpr`): correct restatements of the binomial FP count and the CLT-limiting realized FPR from the set model; proofs are short and right.

## 3. Build

Ran the prescribed sequence from the paper root:
```
TEXINPUTS=".:./sty:" pdflatex -shell-escape main  ->  exit 0
bibtex main                                         ->  exit 0
TEXINPUTS=".:./sty:" pdflatex -shell-escape main    ->  exit 0   (x2)
```
**Status: clean. 21 pages. 0 undefined references, 0 undefined citations, 0 Reference/Citation warnings, 0 "Rerun to get..." messages.** Every `\cref`/`\Cref` target resolves to a defined `\label` (checked the full label/ref set difference, empty). The bibliography resolves all 10 entries. The only typographic notice is a single **Overfull \hbox (3.31pt)** at `relations.tex:36-37` (the line introducing `R(x₁,…,xₙ)` / `⟨x₁,…,xₙ⟩ ∈ R` / `x R y` notation), cosmetic, see MINOR-3.

## 4. General review

The cross-paper consistency between `relations.tex` (operator *definitions* in the preliminaries) and `rel_algebra.tex` (operator *error analysis*) is sound: the join, projection, and composition definitions in section `sec:relations` are the exact objects whose error is propagated in section `sec:rel_algebra`, and the worked example in `rel_algebra.tex` (section `sec:rel_example`) correctly reuses the very tables `tbl:ex_r1/ex_r2/ex_join/ex_proj` from section `sec:relations`. I confirmed the example's shared-`r` rows `⟨a,c,c,d,b⟩` and `⟨a,c,c,d,d⟩` actually appear in `tbl:ex_join` and that they share left tuple `⟨a,c,c,d⟩ ∈ A`; the correlation illustration is faithful to the data.

Findings below, grouped by severity.

---

## CRITICAL
None.

## MAJOR
None.

## MINOR

### MINOR-1. Terminology drift in the section 4 opening: "correlation" vs "correspondence" vs "relation rate"
- **Location**: `sections/approx_rel_model.tex:9, 14, 38` (and `def:approx_rel`).
- **Quoted text**:
  - L9: "We say that a *positive* tuple is a *correlation* and a *negative* tuple is a *complementary correlation*."
  - L14: "...classified as a *true correspondence*, *false correspondence*, *true complementary correspondence*, and *false complementary correspondence*."
  - L38: "...with a *false relation rate* `ε` and *false complementary relation rate* `ω`..."
- **Problem**: Three different naming schemes for the same family of concepts inside one section. The abstract and intro commit to **"correspondence"** ("false correspondences and false complementary correspondences"), and the rest of the paper uses **FPR/FNR/TPR** ("false-positive rate", etc.). The L9 "correlation/complementary correlation" coinage is used nowhere else and clashes with the *statistical* sense of "correlation" that the join section (`thm:join_dependence`) uses heavily ("positively correlated"). "False relation rate" (L38) is a third synonym for FPR. This is the single most noticeable consistency wart in the paper.
- **Suggestion**: Pick one. Recommend: drop the L9 "correlation/complementary correlation" sentence entirely (it adds nothing and collides with the join section's "correlation"), and in L38 say "false-positive rate `ε` and false-negative rate `ω` (true-positive rate `τ = 1-ω`)" to match the body's standing terminology, keeping the abstract's "false correspondence" as the one piece of relation-flavored prose if desired. Net: one vocabulary for the error events.

### MINOR-2. Two dead macros
- **Location**: `main.tex:106` (`\newcommand{\ExactMap}[1]{M(#1)}`), defined, never used in any section (grep-confirmed). Also `\ARelationType` in `sty/approxrelationnotation.sty:25`, defined, never used.
- **Problem**: Dead definitions. `\ExactMap` is a leftover from the cut map material. `\ARelationType` still hardcodes `\sigma` (the very pattern the salvage removed from `\ARelation`), so leaving it invites the old bug back if someone reaches for it.
- **Suggestion**: Delete `\ExactMap` from `main.tex`. Either delete `\ARelationType` from the package or, if kept for the family, give it the documented superscript convention rather than a bare `\sigma`. (Package-level dead macro is lower-stakes than the `main.tex` one.)

### MINOR-3. Single overfull hbox (3.31pt)
- **Location**: `sections/relations.tex:36-37` (the sentence defining the three membership notations).
- **Problem**: 3.31pt overrun into the margin. Trivial, but the build is otherwise box-clean and the paper advertises "0 warnings".
- **Suggestion**: Reword or allow a break. For example, split "If the relation is *binary*, we may denote that two elements `x` and `y` are related by `x R y`." into its own sentence, or insert a discretionary break. Optional but cheap to keep the "clean build" claim literally true.

### MINOR-4. Transitivity "factor near ε" leading-behavior is stated without flagging the independence caveat it locally relies on
- **Location**: `sections/properties.tex:188-191`.
- **Quoted text**: "...the trials are coupled, so the preservation probability decays the fastest of the four ... The leading, most fragile behavior is governed by the conclusion pairs that must be *manufactured* by false positives ... each contributing a factor near `ε ≪ 1`."
- **Problem**: The same paragraph correctly says the triple constraints' trials are *coupled* (a single pair `⟨y,z⟩` sits in many triples), yet the "each contributing a factor near `ε`" sentence reads as if the manufactured-conclusion events multiplied independently. It is meant heuristically (and the section is explicitly "the honest limiting behavior rather than a spurious closed form"), but a reader can mistake it for a derived bound.
- **Suggestion**: Add a half-sentence making the heuristic status explicit, e.g. "(heuristically, ignoring the overlap among triples, each such conclusion contributes a factor near `ε`; the true rate is smaller still once the coupling is accounted for)". This keeps the section's honesty intact and forecloses a misread.

## SUGGESTIONS (optional polish)

1. **`def:approx_pfun` heading mismatch** (`properties.tex:283-285`): the prose immediately above the definition says "The abstract data type of the *immutable approximate set* is given by the following definition," but the definition is of the approximate *partial function*. Copy-paste residue from the set ADT. Change "immutable approximate set" to "approximate partial function" (or drop the immutability clause). Cosmetic, not a correctness issue.

2. **Empty equation in section `sec:map`** (`properties.tex:240-242`): there is a commented-out body inside a live `\begin{equation}...\end{equation}` that renders as an empty numbered display:
   ```
   \begin{equation}
   %\Tuple{x_1,\ldots,x_n} \in \Set{X}[1] \times \cdots \times \Set{X}[n]
   \end{equation}
   ```
   This produces a stray equation number for nothing. Delete the empty `equation` environment (the surrounding sentence reads fine without it).

3. **Section `sec:map` partial-function definition is heavier than the section needs.** Now that map composition is deferred, the long classical partial-function exposition (counting `(|Y|+1)^|X|`, Dom/Image/Range, the `Z₁×Z₂→Q` table example) is somewhat front-loaded relative to the one result that matters here (`def:approx_pfun` as the single-valued special case). Consider trimming to the ADT and the single-valuedness link, or moving the classical recap earlier next to the relation preliminaries. Purely structural; the content is correct.

4. **Symmetric-closure cross-reference in the worked example.** `tbl:validation` (rel_algebra.tex:458) cites `thm:symmetric_closure` for the closure rows, which is good; consider one sentence in section `sec:rel_example` pointing the closure validation rows back to `sec:symmetric`, so the worked example and the invariant section visibly close the loop. Minor.

5. **Application forward-reference balance.** Section `sec:trapdoor_rel_model` leans on `thm:join_dependence` for the leakage-linkage claim (oblivious_rel_model.tex:84-86), which is good and correct. No change needed; noting it as a strength.

---

## Strengths (for the record)

1. The **join independence-failure result** (`thm:join_dependence`) is a genuine, sharp, correctly-proved contribution that the probabilistic-database framing does not subsume, and it is backed by a clean Monte Carlo confirmation of the exact `1/a` factor. This is the paper's spine and it holds.
2. **Honest scoping throughout.** Every result that belongs to a sibling paper (set-level intersection/union, subset/equality predicates, map composition, entropy bound, optimal construction) is deferred by an accurate citation that I verified against the target paper, not re-derived and not over-claimed. The join-FPR three-region deferral in particular is stated with exactly the right caveat.
3. **The validation harness is real and faithful.** `code/validate.py` reproduces all formulas to 3-4 digits and, importantly, includes the *negative* control (the independent model that the paper predicts FAILS) and shows the empirical data tracking the correlated model. This is the right way to validate a "this assumption breaks" claim.
4. The **model-order vs. parameter-count** thread is carried consistently from the set model into the relational operators and the invariants, giving the paper a coherent through-line beyond a list of formulas.

## Cross-verification log
- Re-derived all 11 load-bearing closed forms by exact algebra (`python3` one-off); all match the manuscript.
- Ran `code/validate.py` (2×10⁶ trials/row): 23 fit rows PASS, worst abs err 6.86e-4; 1 expected-mismatch demo row behaves as predicted.
- Read `bernoulli_composition/sections/set_theory.tex` and `relational.tex` to confirm the four deferral citations (intersection FNR, intersection FPR three regions, subset theorem, `cor:equality_prob`) are accurate; all four verified.
- Inspected `sty/relationnotation.sty` (`\Relation{m o o}` produces `R_{#2}^{#3}`) and `sty/approxrelationnotation.sty` (`\ARelation` delegates to `\Relation`) to confirm `[\fprate][\tprate]` renders FPR-subscript/TPR-superscript as documented, and that the prior `\sigma`-hardcoding/arg-discard is gone.
- Verified the three claimed bug fixes (`def:approx_pfun` conditioning, symmetric-closure TPR, `\ARelation` macro convention) against current text.
- Full label/ref closure check: 0 dangling references.

## Prior-art items flagged for YOUR verification (no web access)
- That Suciu et al. / Trio / MayBMS are the most apt prob-DB representatives and that the "uncertainty in the data vs. representation-induced error over an exact base" distinction is novel as stated.
- Whether there is closer prior art on representation-induced relational-operator error propagation specifically (Bloom-filter joins/semijoins, approximate query processing error bounds), which, if it exists, would belong in the related-work paragraph alongside the prob-DB contrast.
- `codd1970`, `bf` are standard and correctly cited; the five `@unpublished` self-cites are GitHub-URL placeholders consistent with the family's preprint style.
