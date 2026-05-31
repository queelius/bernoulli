# Logic Checker Report, bernoulli_maps

**Specialist**: logic-checker (proof correctness, logical chain integrity, claim support)
**Date**: 2026-05-29
**Scope**: All definitions, lemmas, theorems, corollaries, and their proofs across sections 2 to 7. Special attention (per area-chair instruction) to whether the map-composition error algebra is consistent with the foundation's composition theorem (`bernoulli_sets`, `thm:composition_rates`).

## Verdict summary

The core of the paper, the composition algebra in section 5 (`composition_new.tex`), is **correct and well-proved**. Theorems 5.x (FNR and FPR of `g circ f`), the two overlap corollaries, and the `k`-fold corollary are sound, and they are the correct Maybe-type specialization of the foundation's full-channel composition theorem. The Kronecker factorization theorem (Theorem 4.x in `special_cases.tex`) is correct in substance.

The problems are concentrated in **section 6 (entropy maps)** and **section 7 (singular hash map)**, which contain one critical-grade error (a "probability of success" formula that is dimensionally and probabilistically wrong as written), one major gap (the SHM success-probability proof is internally inconsistent in its notation and skips the value-collision accounting it claims to perform), and several major imprecisions (an undefined `Expect{log2 T}` approximation asserted without derivation, a Jensen-inequality step that points the wrong way for a claimed lower bound).

---

## CRITICAL findings

### C1. The "probability of success" formula in section 6.6 is incorrect (source: logic-checker)
- **Location**: `entropy_maps.tex`, subsection "Probability of success" (sec:prob-success), the displayed equation for `p(eps, fnr)`.
- **Quoted text**:
  > "The probability of success given a rate-distortion $\fnrate$ on positives and $\fprate$ on negatives is given by
  > \[ p(\fprate,\fnrate) = \binom{m}{(1-\fnrate)m} \fprate^{m(1-\fnrate)} (1-\fprate)^{m \fnrate}\,. \]"
- **Problem**: Multiple independent defects make this expression unusable as written.
  1. **Wrong base in the power factors.** The probability that one bit string `b` simultaneously codes all `(1-fnr)m` stored keys is, by the paper's own section 7 derivation, a product of per-key collision probabilities of order `eps` and `2^{-BL(v)}`, giving `eps^{(stored-1)} / 2^{(sum BL)}`. It is NOT `eps^{m(1-fnr)} (1-eps)^{m fnr}`. The factor `(1-eps)^{m fnr}` has no derivation anywhere and contradicts section 7, where the false-negative keys are simply *dropped* (not "succeed with probability `1-eps`"). The two sections model the same object and disagree.
  2. **Binomial coefficient misuse.** `binom{m}{(1-fnr)m}` counts subsets of stored keys, but the quantity being defined is a *single* bit string's success probability for a *fixed* outcome (which keys are stored). A coefficient counting which keys are dropped does not belong in a per-trial success probability; if a marginalization over which keys are dropped were intended, the binomial weight would also need the `fnr` Bernoulli factors `fnr^{m fnr}(1-fnr)^{m(1-fnr)}`, which are absent. As written the expression mixes a combinatorial count with collision probabilities of incompatible types.
  3. **Non-integer arguments.** `(1-fnr)m` and `m fnr` are written as exact integers in both the binomial lower index and the exponents, with no floor/ceiling or "assume integer" caveat, so the formula is ill-defined for generic `fnr`.
- **Why critical**: this is a stated theorem-grade result ("The probability of success ... is given by ...") on which the subsection's geometric-trial argument and the `log2 E[T]` space estimate then depend. A reader cannot reconstruct the `-log2 eps` simplification (claimed two paragraphs later) from this `p`. The correct per-trial success probability is the one in section 7 Theorem `thm:shm-success` (`p = eps^{m-1}/2^{m mu}`); section 6.6 should either reproduce that or be removed.
- **Suggestion**: Delete the `binom{...} eps^{...}(1-eps)^{...}` expression and replace it with the section 7 result, restricted to the `(1-fnr)m` stored keys: `p = eps^{(1-fnr)m - 1} / 2^{(1-fnr)m mu}` (or the exact count of stored keys). Then the geometric-trials and `log2 E[T]` discussion follows consistently. Reconcile section 6.6 and section 7 so they state the *same* `p`.
- **Confidence**: high.
- **Cross-verification requested**: methodology-auditor (can the stated `p` be reproduced as a probability at all, i.e., is it in `[0,1]` and does it integrate correctly?).

---

## MAJOR findings

### M1. The SHM success-probability proof (Theorem 7.x) is notationally inconsistent and does not prove what it claims (source: logic-checker)
- **Location**: `shm.tex`, proof of `thm:shm-success`.
- **Quoted text** (the setup):
  > "Suppose we have a set $\Fun{f} \coloneqq \{(k_1,v_1),\ldots,(k_m,v_m)\}$ and $k_1$ hashes to $y = \hash(k_1) \mod t$, where $\hash \colon \BitSet^* \to \BitSet^N$ ... and $N < \max{\BL(v_1),\ldots,\BL(v_m)}$."
  and later
  > "The probability that $\hash(1 \cat k_1) \mod \BL(v_1) = v_1$ is given by $\frac{1}{2^{\BL(v_1)}}$."
- **Problems**:
  1. **`mod t` vs `mod BL(v)` vs truncation.** The construction in Algorithm 1 uses `trunc(hash(x cat b_n), k)` (a `k`-bit truncation). The proof instead writes `hash(k_1) mod t`, then `hash(1 cat k_1) mod BL(v_1)`. Three different reduction operations (`mod t`, `mod BL(v_1)`, `trunc(...,k)`) appear for what should be one mechanism. `hash(...) mod BL(v_1)` reduces modulo a *bit length* (a small integer like 5), which cannot equal a value `v_1`; the intended statement is surely "the first `BL(v_1)` bits of the hash equal the codeword for `v_1`," i.e., `trunc(hash(1 cat k_1), BL(v_1)) = Encode(v_1)`. As written it is type-incorrect.
  2. **`N < max BL` hypothesis is backwards.** If the hash output has `N` bits and `N < max_j BL(v_j)`, then for the key whose value needs `max BL` bits there are not enough hash bits to encode it, so the event "first `BL(v_j)` bits equal the codeword" is undefined. The hypothesis should be `N >= max_j BL(v_j)` (enough bits), or the random-oracle `B^infty` model should be used (as section 6 does). This looks like a typo for `>`, but it inverts the proof's feasibility.
  3. **The `1 cat k_j` concatenation is unexplained.** The leading `1` prepended to each key is never motivated (it appears to be a tag separating the "membership" hash from the "value" hash), and the membership collision uses `k_j` while the value collision uses `1 cat k_j`. Whether these are independent is asserted ("every one of these probabilities are independent") but the two events share the same key `k_j` and, depending on the hash model, the same hash evaluation; independence needs the random-oracle assumption stated explicitly per concatenation tag.
- **Net effect**: the final formula `p = eps^{m-1} / 2^{m mu}` is *plausibly correct* under a clean random-oracle model (it matches the heuristic: one key fixes the `k`-bit bucket for free, the other `m-1` keys must collide in `k = -log2 eps` bits each, and all `m` values must match their `BL(v_j)`-bit codes), but the written proof does not establish it rigorously. The conclusion is likely right; the derivation is not trustworthy as printed.
- **Suggestion**: Rewrite the proof against the random oracle `h: B^* -> B^infty` and the actual `trunc(., k)` operation from Algorithm 1. State events as bit-prefix matches: (a) the `k`-bit membership prefix of `1 cat k_j` agrees across all `m` keys (probability `2^{-k(m-1)} = eps^{m-1}` given one key fixes the target), and (b) each value prefix matches (`prod_j 2^{-BL(v_j)} = 2^{-m mu}`). Drop `mod t`, `mod BL`, and the `N < max BL` line; use the random oracle throughout.
- **Confidence**: high that the proof as written is inconsistent; medium-high that the final formula is the intended and correct one.
- **Cross-verification requested**: methodology-auditor.

### M2. The `Expect{log2 T}` space estimate in section 6.6 is asserted, not derived, and is self-contradictory about what it computes (source: logic-checker)
- **Location**: `entropy_maps.tex`, sec:prob-success, the paragraph after the geometric distribution.
- **Quoted text**:
  > "The expected code size is $\Expect{\log_2 \RV{T}}$, which is non-linear and problematic but may be approximated with [displayed binary-entropy expression] bits per element ... This result is not the result of computing $\Expect{\log_2 \RV{T}}$, nor the expectation of its Taylor approximation. It is simply $\log_2 \Expect{\RV{T}}$."
- **Problem**: The text first calls the displayed expression an "approximation" of `E[log2 T]`, then explicitly states it is *not* `E[log2 T]` nor a Taylor approximation of it, but rather `log2 E[T]`. By Jensen, `log2 E[T] >= E[log2 T]`, so `log2 E[T]` is an *upper bound*, not an approximation, of the expected code size, and the sign of the gap is the opposite of what "approximation" suggests. Moreover the displayed expression `-H_b(fnr) - fnr log2(1-eps) - (1-fnr) log2 eps` is presented without the intermediate `log2 E[T]` computation that would let a reader check it against the (also-wrong, see C1) `p(eps,fnr)`. The subsection conflates "the quantity we want" (`E[log2 T]`) with "the quantity we can compute" (`log2 E[T]`) without bounding the gap.
- **Suggestion**: State plainly: "We bound expected code size by `log2 E[T]` (a Jensen upper bound on `E[log2 T]`)." Then derive the displayed expression *from* `E[T] = 1/p` using the corrected `p`. If `E[log2 T]` itself is wanted, give the gap (it is `O(1/m)`, as section 7 correctly notes; section 6 should borrow that bound).
- **Confidence**: high.

### M3. Section 7 space theorem: the Jensen step yields an upper bound but is used to support a "lower-bound" claim, and `ell = floor(log2 n)` is conflated with `E[log2 Q]` (source: logic-checker)
- **Location**: `shm.tex`, `thm:shm-space` and its proof.
- **Quoted text**:
  > "By Jensen's inequality (since $\log_2$ is concave), $\Expect{\log_2 \RV{Q}} \leq \log_2 \Expect{\RV{Q}}$, so $\Expect{\log_2 \RV{Q}} \leq \log_2 \frac{2^{m \mu}}{\fprate^{m-1}}$."
  and the theorem statement:
  > "the \emph{expected} bit length of the Singular Hash Map asymptotically obtains a space complexity with a lower-bound given by $-(1 - \fnrate) \log_2 \fprate + (1 - \fnrate) \mu$ ... and an upper-bound given by $-(1 - \fnrate) \log_2 \fprate + \mu$."
- **Problem**: The proof derives only an *upper* bound on `E[log2 Q]` via Jensen. The theorem then states both a lower and an upper bound on expected bit length, but the proof never establishes the lower bound `-(1-fnr) log2 eps + (1-fnr) mu`; that line is argued informally ("the value bits scale proportionally ... contributing `(1-fnr)mu`") without an inequality. So the "lower-bound" half of the theorem is unproven. Separately, `ell = floor(log2 n)` (the bit length of the `n`-th trial's string) is the *realized* code length, while `E[log2 Q]` is its expectation; the proof slides between "the `n`-th trial maps to a string of length `floor(log2 n)`" and "expected bit length `= E[log2 Q]`" without stating that the stored object is the *successful* string whose index is `Q`. The asymptotic `(m-1)/m -> 1` step is fine; the bound *direction* and the lower-bound justification are the gap.
- **Suggestion**: (i) State the theorem as a single asymptotic equality `-log2 eps + mu` for `fnr = 0` (which the proof supports) and present the `fnr`-scaled lower/upper pair as a *separate* claim with its own two-sided argument, or relabel the "lower bound" as the uniform-bit-length *case* rather than a proven bound. (ii) Make explicit that the stored cost is `log2 Q` for the successful trial index `Q ~ Geo(p)`, then bound `E[log2 Q]`. (iii) Note the `O(1/m)` gap (already stated) applies to the Jensen step.
- **Confidence**: high.

### M4. Kronecker theorem: parameter-count comparison uses inconsistent "order" conventions and an off-by-framing in the general-channel baseline (source: logic-checker)
- **Location**: `special_cases.tex`, `thm:kronecker`.
- **Quoted text**:
  > "the number of free parameters is $n \cdot (|\Set{Y}| - 1)$, compared to $N(|\Set{Y}|^{|\Set{X}|} - 1)$ for a general $N$-th order channel on $\Set{Y}^{\Set{X}}$."
- **Problem**: The honest baseline for "a general channel on the function space" is a stochastic matrix of size `|Y|^|X| x |Y|^|X|`, which has `|Y|^|X| * (|Y|^|X| - 1)` free parameters (each of `|Y|^|X|` input rows has `|Y|^|X| - 1` free entries), not `N(|Y|^|X| - 1)`. The factor `N` (an unspecified "order") is doing undefined work here: `N` is never quantified, and the comparison `n(|Y|-1)` vs `N(|Y|^|X| - 1)` is not apples-to-apples (left side counts per-input-channel rows summed over blocks; right side counts something with a free `N`). Also, each `M_x` is a `|Y| x |Y|` *stochastic* matrix and so has `|Y|(|Y|-1)` free parameters per *fully general* per-input channel, reducing to `|Y|-1` only if every input row of `M_x` is identical (a symmetric per-input channel). The theorem asserts `|Y|-1` per block without stating that within-block channels are *row-homogeneous* (all latent values share one response row), which is a real and unstated assumption beyond "i.i.d. across inputs."
- **Why major not critical**: the *qualitative* claim (independence collapses an exponential parameter count to one linear in `|X|`) is correct and is the point. The defects are in the precise counts and the baseline, which a careful reader will trip over.
- **Suggestion**: Fix the baseline to `|Y|^{|X|}(|Y|^{|X|}-1)`; drop the free `N` or define it. State the within-block assumption precisely: each per-input channel `M_x` is itself a single shared stochastic matrix whose *row* structure is what `|Y|-1` (one row) or `|Y|(|Y|-1)` (full matrix) counts; reconcile with the body text in `special_cases.tex` line ~50 which uses the `4 x 4 -> 12 -> 4` example (that example counts `2 x (|Y|-1) = 2 x 1 = 2` per component, consistent only under the row-homogeneous reading).
- **Confidence**: high on the baseline error; medium on whether the author intends row-homogeneous channels (the CLAUDE.md "12 -> 4" discussion suggests yes).

---

## MINOR findings

### m1. Composition theorem is correctly the Maybe-type specialization of the foundation, but the relationship is not stated (source: logic-checker; this is the requested cross-check)
- **Location**: `composition_new.tex`, `thm:comp-fnr` and `thm:comp-fpr`; foundation `bernoulli_sets/sections/bernoulli_model.tex`, `thm:composition_rates`.
- **Verification performed**: The foundation's full binary-channel composition gives `tpr = t'*t + fn'*eps` (a positive can be dropped then re-promoted, or retained). The maps paper restricts to the Maybe-type channel: a positive input maps only to the correct value or to `Nothing`, never to a *wrong* value, and a `Nothing` stays `Nothing` under further composition. Under this restriction the "re-promotion" path `fn'*eps` vanishes (once a positive becomes `Nothing` it cannot be revived), so `tpr_{g circ f} = t1*t2`, i.e., `fnr = 1 - (1-fn1)(1-fn2)`. This **matches** `thm:comp-fnr` exactly. The FPR result `fpr_1[rho(1-fn2) + (1-rho)fpr2]` has no analog in the foundation (the foundation's sets are total indicator functions, so there is no `Dod(g)` overlap question); it is a genuine new result of this paper and I verified its derivation independently (Steps 1 to 3 of the proof are correct: `fpr1` to produce a false positive value, then survival through `g` conditioned on landing in/out of `Dod(g)`). Both theorems are **correct**.
- **Problem (minor)**: The paper never states that `thm:comp-fnr` is the foundation's `thm:composition_rates` specialized by forbidding wrong-value outputs. A reader who knows the foundation will wonder why the foundation's `fn'*eps` cross-term disappeared. One sentence ("In the Maybe-type model a dropped positive cannot be re-promoted, so the foundation's cross term vanishes and `tpr` is multiplicative") would close the loop and strengthen the family coherence.
- **Suggestion**: add that sentence after `thm:comp-fnr`.
- **Confidence**: high (this is a verification pass, not a defect hunt; the math checks out).

### m2. `Lemma (Composition raises the model order)` proves "in general second-order," but the remark immediately walks it back to first-order under uniform FPs (source: logic-checker)
- **Location**: `composition_new.tex`, `prop:higher-order` and the following remark.
- **Problem**: The lemma says the composition is "in general a second-order approximate map," and its proof correctly identifies two FP sub-populations (`rho`-in vs `rho`-out) with rates `eps1(1-fn2)` and `eps1 eps2`. The very next remark says that if `f`'s FP distribution is uniform, the marginal model is first-order. So "in general second-order" is true only when the FP distribution is input-dependent. The lemma statement should carry that qualifier ("when the false-positive distribution depends on `x`") rather than relegating the crucial condition to an unnumbered remark, since the headline "composition raises the order" is the take-away and is conditionally false.
- **Suggestion**: fold the condition into the lemma hypothesis.
- **Confidence**: high.

### m3. `Lemma (Closure under composition)` proves positivity, not closure (source: logic-checker)
- **Location**: `composition_new.tex`, `prop:closure`.
- **Problem**: The lemma claims the composition "is an approximate map of `g circ f`," but the proof only shows `P[correct] = (1-fn1)(1-fn2) > 0` and `P[Nothing on negatives] >= 1-eps1 > 0`. Showing both probabilities are positive does not establish the defining property of "approximate map" (that errors are per-element independent Bernoulli trials with well-defined rates). The closure content is really delivered by the *subsequent* theorems (which compute the rates) plus `prop:higher-order` (which addresses the i.i.d.-within-block structure). As stated, `prop:closure` proves a weaker fact than its name.
- **Suggestion**: either rename to "Composition is non-degenerate" or strengthen the proof to verify the element-wise independence assumption survives composition (it does, by independence of the two randomness sources, which is assumed). One added line citing `asm:independence` for each stage suffices.
- **Confidence**: high.

### m4. `thm:optimal-code` proof invokes Shannon source coding to get exact `H(Y)`, ignoring the integer-codeword gap (source: logic-checker)
- **Location**: `entropy_maps.tex`, `thm:optimal-code`.
- **Problem**: The theorem states expected length `ell = H(Y)` exactly. Shannon source coding gives `H(Y) <= ell < H(Y)+1` for prefix-free codes in general; equality holds only when all `p_y` are powers of two (dyadic), which is exactly the setting the paper restricts to elsewhere (`R = {2^{-k}}`). The theorem should state the dyadic assumption or write `ell -> H(Y)` (achievable in the limit / under dyadic probabilities), otherwise `ell = H(Y)` is false for generic distributions.
- **Suggestion**: add "when the `p_y` are dyadic (powers of two), as assumed in section 6.6" or relax to `H(Y) <= ell < H(Y)+1`.
- **Confidence**: high.

### m5. `p(eps,fnr)` is later "simplified" to `-log2 eps` but the algebra is not shown and does not obviously follow (source: logic-checker)
- **Location**: `entropy_maps.tex`, last line of sec:prob-success.
- **Quoted text**: "If we let $\fnrate \coloneqq 0$, the above simplifies to $-\log_2 \fprate$ ...".
- **Problem**: Setting `fnr = 0` in the displayed binary-entropy expression `-H_b(fnr) - fnr log2(1-eps) - (1-fnr) log2 eps` gives `-H_b(0) - 0 - log2 eps = -log2 eps` (since `H_b(0)=0`), which is correct. But this relies on the (separately problematic, C1/M2) displayed expression, not on the `p(eps,fnr)` formula two lines above it, and the text says "the above simplifies," ambiguously referencing which "above." Tighten the antecedent.
- **Confidence**: medium (the arithmetic works; the referent is ambiguous).

### m6. `Definition (Map)` defines a map as a *partial* function but the abstract and several theorems treat `f: X -> Y` as total (source: logic-checker)
- **Location**: `prelim.tex`, `def:map` ("a binary relation ... with the constraint that the first element ... is unique," then "also known as a partial function"); contrast `bernoulli_map.tex` which uses `f: X -> Y` (total) for the Kronecker/general model and `f: X -> Maybe{Y}` (partial) for the second-order model.
- **Problem**: The term "map" is used for both total (`Y^X`, the function-space counting `|Y|^|X|`) and partial (`X -> Maybe Y`, `Dod(f)`) functions, sometimes in the same section. This is internally reconcilable (lift total to partial via `Maybe`), but the switching is implicit. The second-order model's positives/negatives partition `X = P union N` only makes sense for *partial* `f`; the Kronecker theorem's `|Y|^|X|` count is for *total* `f`. A reader must infer which is meant.
- **Suggestion**: state once, early, that "map" means partial function lifted to `X -> Maybe Y`, and that total functions are the special case `Dod(f) = X` (so `N = empty`, `eps` irrelevant).
- **Confidence**: high.

## Items checked and found CORRECT (for the record)
- `prop:loss_decomp` (loss decomposition): correct application of law of total expectation under uniform `X`.
- `prop:binom_errors` (binomial error counts): correct; `FP ~ Bin(|N|, eps)`, `FN ~ Bin(|P|, fnr)`, independence from disjointness + Axiom 1. Clean.
- `thm:comp-fnr`, `thm:comp-fpr`, `cor:disjoint-fp`, `cor:full-overlap`, `cor:k-fold`: all correct (see m1). Example 5.x arithmetic (`0.01 * 0.118 = 0.00118`) checks. Example "approximate NOT" (`1 - 0.95^2 = 0.0975`) checks.
- BSC/BAC confusion-matrix identifications (`p1 = 1-eps, p2 = eps`; `p1 = 1-fnr, p2 = eps`): correct.
- `cor` (SHM, `fnr=0, mu=0` gives `-log2 eps`): correct given the (repaired) theorem.

## Cross-verification routing (for the area chair)
- **C1** and **M1**, **M2**, **M3** are all in the section 6 / section 7 space-complexity machinery and are mutually entangled (they all concern the same `p`, `T`/`Q`, and the `-log2 eps + mu` bound). Route the bundle to **methodology-auditor** to check whether the final headline bound `-log2 eps + mu` is *reproducible* from a corrected `p`, independent of the broken intermediate steps. My assessment: the headline bound is very likely correct; the derivations supporting it are not.
- **m1** is the requested foundation cross-check and is a positive result (consistency confirmed).
