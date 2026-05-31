# Logic Checker Report, The Perfect Hash Filter

**Date**: 2026-05-29
**Scope**: Proof correctness, logical chain integrity, claim support across all eight section files (compiled and excluded). Quoted text verified against the manuscript.

## Summary

The core FPR theorem and the space-complexity derivation are essentially sound in outline and rest on a recognizable, correct idea (perfect-hash slot plus `M`-bit fingerprint gives FPR `2^-M`). However the manuscript is an early draft and the proofs are riddled with mechanical defects that currently break the logical chain: a sign error that propagates through a multi-step proof, a verbatim-duplicated theorem, an empty `\cite{}` standing in for the authority of a distributional claim, "???" left inside displayed proofs, and several appeals to results (`thm:fpr`, `thm:fnr`, `dummyref`, "Theorem 3 of `oph`") that are either undefined in this paper or live in unpublished manuscripts. None of these is fatal to the underlying mathematics, but as written several proofs do not stand.

Severity counts: Critical: 1 | Major: 4 | Minor: 4

---

## Critical

### C1. Sign error propagates through the union space-complexity proof (Theorem `thm:union_space_complexity`)
- **Location**: `sections/adt.tex`, Theorem `thm:union_space_complexity` (lines 367 to 455).
- **Quoted text**: the theorem statement uses the correct inclusion-exclusion FPR,
  "`\fprateob_1 + \fprateob_2 - \fprateob_1 \fprateob_2`" (lines 363, 373, 380),
  but the proof body switches sign to
  "`\fprateob_1 + \fprateob_2 + \fprateob_1 \fprateob_2\,.`" (line 413) and carries the `+` through line 421 and into the displayed efficiency on line 431, then silently reverts to `-` in the "(\ref{eq:union_space_complexity} revisited)" line 440.
- **Problem**: For two independent positive Bernoulli sets the induced FPR of the union is `eps_1 + eps_2 - eps_1*eps_2` (the probability that at least one of two independent fingerprint matches fires). The `+ eps_1 eps_2` form in the proof is wrong and, because the proof's whole point is to derive the efficiency expression from this quantity, the derivation does not actually reach the stated result: it starts from the wrong numerator and then the "revisited" tag asserts equality to the correct expression without justification. The corollary on line 462 to 467 compounds this: it divides by `\log_2 \fprateob_1 \fprateob_2` (i.e. `log2(eps_1)+log2(eps_2)`, the unweighted sum), which does not match the theorem's `alpha_1 log2 eps_1 + alpha_2 log2 eps_2` denominator unless `alpha_1 = alpha_2 = 1`, a case the theorem explicitly allows to vary.
- **Suggestion**: Fix the proof to use `eps_1 + eps_2 - eps_1 eps_2` throughout. Re-derive `eq:proof_union_ae` from the correct numerator. Either justify the corollary's `alpha_1=alpha_2=1` specialization explicitly or carry the `alpha` weights through. Replace the "(... revisited)" hand-wave with the actual algebra.
- **Cross-verified**: Yes (methodology lens). The inclusion-exclusion form is also the form the family's `bernoulli_composition` paper uses for union FPR, and the intro of this very paper relies on the composition theorem `eta_total = 1 - prod(1-eta_i)`, whose two-term expansion is `eps_1+eps_2-eps_1 eps_2`. The `+` sign is internally inconsistent with the paper's own framework, not merely with convention.

---

## Major

### M1. Verbatim-duplicated theorem with identical proof (cardinality estimator)
- **Location**: `sections/rd_ph_filter.tex`, lines 426 to 447 and 451 to 472.
- **Quoted text**: line 427 "An estimator of the cardinality of an approximated set represented by a \gls{gls-phf} is given by ... `\hat{m} = -\frac{\BL...}{-\log_2 \fprate + 1.44}`"; line 452 "A \emph{maximum likelihood estimator} of the cardinality ... `\hat{m} = -\frac{\BL...}{-\log_2 \fprate + 1.44}`". The two theorems and their proofs are word-for-word identical.
- **Problem**: The same result is stated and proved twice in immediate succession (the second merely re-labels it "maximum likelihood estimator"). One is redundant.
- **Suggestion**: Delete the first; keep a single theorem, and justify the "maximum likelihood" label (currently the proof is a method-of-moments / plug-in argument: it sets `BL` equal to its expectation and inverts, which is an MoM estimator, not obviously an MLE). Either rename to "moment estimator" or supply the likelihood argument.

### M2. Sign error in both estimator results
- **Location**: `sections/rd_ph_filter.tex`, lines 429 and 454 vs the proofs at 445 and 469.
- **Quoted text**: the theorem statements give `\hat{m} = -\frac{\BL(\PASet{S})}{-\log_2 \fprate + 1.44}` (leading minus), but both proofs conclude `\hat{m} = \frac{\BL(\PASet{S})}{-\log_2 \fprate + 1.44}` (no leading minus).
- **Problem**: With `eps < 1`, `-log2(eps) > 0`, so the denominator is positive and `BL > 0`; the cardinality estimate must be positive. The leading minus in the statement makes `\hat m` negative, which is nonsensical. The proof's unsigned version is the correct one.
- **Suggestion**: Remove the leading minus from both theorem statements.

### M3. Distributional claim cites nothing (empty `\cite{}`)
- **Location**: `sections/rd_ph_filter.tex`, line 387 to 397.
- **Quoted text**: "According to \cite{}, the probability mass of the perfect hash function is given by `\RV{N} \sim \PDF{n \Given m, r}[\RV{N}] = q^{2^n-1}\left(1 - q^{2^n}\right)`".
- **Problem**: A specific, non-trivial pmf is asserted on the authority of an empty citation. The reader cannot check it, and the formula itself is suspicious: it is presented as the pmf of the bit length `N`, indexed by `2^n`, with `q` defined as a one-minus-falling-factorial-ratio (a collision-free probability). Neither the derivation nor a source is given, and the same `\cite{}` is empty. The two "revisited" tags on lines 437 and 462 also reference `\tag{\ref{} revisited}` with an empty `\ref{}`, so the equations they point back to are unresolved.
- **Suggestion**: Either derive the pmf (it looks like a geometric-type tail over the search for a collision-free seed, related to the `oph` random-oracle model) or cite the real source. Fill in the empty `\ref{}` tags so "revisited" points at the correct equation.

### M4. Load-bearing space theorem rests on an unpublished manuscript
- **Location**: `sections/rd_ph_filter.tex`, Theorem `thm:mPHF_size` proof, line 230.
- **Quoted text**: "according to Theorem~3 in \cite{oph}, the \emph{expected} lower-bound for a perfect hash function with a load factor `r` is given by `\log_2 \mathrm{e} - (\frac{1}{r} - 1) \log_2(\frac{1}{1-r})`".
- **Problem**: The paper's headline space result (and its corollary, and the entropy/estimator material that follows) is derived from "Theorem 3 of `oph`," where `oph` is `@unpublished{... note={Manuscript in preparation}}`. The result is therefore not independently checkable and the chain from premise to the abstract's "asymptotically achieves `-log2 eps` bits/element" claim is incomplete. Logically the argument is "assume oph's Theorem 3, then ...", which is fine as a conditional but is presented as established.
- **Suggestion**: Prove the perfect-hash load-factor bound inline (it is a standard occupancy/entropy computation) or state explicitly that the result is conditional on the companion paper and weaken the abstract accordingly.

---

## Minor

### m1. "???" inside a displayed proof step
- **Location**: `sections/adt.tex`, line 428: "Making these substitutions yields an absolute efficiency ???" immediately before the displayed `eq:proof_union_ae`.
- **Problem**: An unfinished proof step. Combined with C1, the step is also wrong.
- **Suggestion**: Complete and correct the algebra.

### m2. Undefined probability left as "`$?$`"
- **Location**: `sections/adt.tex`, line 206: "at `\Card{U} = 2`, the probability of this outcome is `$?$`."
- **Problem**: A specific probability is promised and left blank. The surrounding argument (a Bloom filter whose hash family collapses the whole universe to one hash) is a fine intuition but the quantitative punchline is missing.
- **Suggestion**: Either compute it or rephrase qualitatively.

### m3. FPR-proof condition 1 has a garbled sentence and a "?" placeholder
- **Location**: `sections/rd_ph_filter.tex`, line 199.
- **Quoted text**: "Since \ph$_{\Set{S}}$ perfectly hashes all `y \in \Set{S}` and `x \in \Set{S}`, no other member of `\Set{S}` hashes ?, and `\matrx{V}[i]` is explicitly set to the hash `h(x)`".
- **Problem**: The proof of FPR condition 1 (every true member is accepted) is correct in spirit but the sentence is broken ("hashes ?") and the macro `h{$x$}` (line 199, 201) is mis-typed (looks like a stray brace form rather than `h(x)`). The logic holds; the prose does not yet render it.
- **Suggestion**: Repair the sentence ("no other member of `S` hashes to slot `i`") and the `h(x)` macro.

### m4. `k`-perfect placement probability: indexing and bound need a check
- **Location**: `sections/k_perfect_hashing.tex`, lines 13 to 27.
- **Quoted text**: "`\RV{K}_j \sim \geodist((N - j + 1)/N)`" and "`p(k) = ... = \prod_{j=1}^{m-1}(1 - (j/N)^{k+1})`".
- **Problem**: The product runs `j = 1 .. m-1` but the geometric is written for the `j`-th element with success prob `(N-j+1)/N`; the indices in the geometric (`N-j+1`) and in the product (`(j/N)^{k+1}`) do not visibly correspond (one counts occupied-from-top, the other from the bottom), and the `j=1` term of the geometric gives success prob `1` while the product starts at `j=1` with factor `1-(1/N)^{k+1} < 1`. The off-by-one and the from-top vs from-bottom mismatch should be reconciled; the "coupon collector" label is also loose (this is an occupancy/insertion-with-bounded-probes model, not the classical coupon-collector expectation). The conclusion `p(k) -> 1` as `k -> infinity` is correct.
- **Suggestion**: State the placement model precisely (sequential insertion, slot uniform, at most `k+1` probes), align the two index conventions, and either drop or justify the "coupon collector" phrasing.

---

## Notes on what is correct

- The FPR theorem `thm:fp_rate` (FPR `= 2^-M`, `M` the fingerprint width) is correct: condition 2's argument (a non-member's `M`-bit fingerprint matches a uniformly random stored `M`-bit string with probability `2^-M`) is sound under the stated cryptographic-hash assumptions.
- The minimal-PHF corollary's arithmetic (`-log2 eps + 1.44` bits/element) is internally consistent with its premises once M4 is granted.
- The `sigma`-algebra / Boolean-algebra discussion in `adt.tex` (the image of a deterministic generator is generally not a sigma-algebra but generates one; positive/negative approximate sets are semirings, not Boolean algebras, because they are not closed under complement) is conceptually correct and is a genuine, careful observation. Definition of the sigma-algebra on line 51 to 53 is left as "closed under..." (unfinished) but the surrounding reasoning is right.
- The maximum-entropy-coder theorem (`rd_ph_filter.tex` line 404 to 416) is plausible but its proof trails off ("The second part is a bit string `b_n` of bit length `n`." with no conclusion); flagged under prose as incomplete rather than wrong.
