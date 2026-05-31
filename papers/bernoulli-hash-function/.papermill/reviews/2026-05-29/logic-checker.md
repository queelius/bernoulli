# Logic Checker Report

**Paper:** The Bernoulli Hash Function
**Date:** 2026-05-29
**Focus (per area chair):** optimality / threshold-predicate theorems and the
space-achievability argument.

## Overall Assessment

The logical spine of the paper is sound and, relative to the 2026-02-26 pass,
markedly stronger. The two prior critical defects in this domain are resolved:
the space-complexity proof (Thm `thm:space`) no longer uses the incorrect
second-order Taylor expansion, and the appendix order-statistic PMF derivation
(`thm:os_pmf_detailed`) no longer contains the informal "Wait---" self-
correction and now normalizes correctly. The unsalted-value-hash inconsistency
(prior C3) is also fixed: Algorithms 1, 2, 3 and `Find` all hash `1 || x || b`.

What remains are two *incorrect printed closed-form identities* whose asymptotic
consequences are nonetheless correct (so the headline theorems stand), one
genuine residual algorithmic gap in the adaptive *map* path, and a few precision
items. I verified the central claims numerically (geometric expectation and
entropy asymptotics, order-statistic PMF normalization); see notes inline.

## Findings

### MAJOR-1: Adaptive map lookup uses a salt the construction does not store
- **Location:** `sections/construction.tex`, Alg. `alg:make_shf_adaptive`
  (output tuple `(N, t)`, lines 124-135 for sets and 137-161 for maps) versus
  `Find` (`alg:find`, line 225: `c <- h(1 || x || b)`).
- **Quoted text:** Adaptive output is "A Bernoulli map `M~` coded as a tuple
  `(N, t)`." `Find` computes "`c <- h(1 \cat x \cat b)`" and the prose states
  "the hash of `1 || x || b` was constrained during construction to begin with
  `Encode(v)`."
- **Problem:** For the adaptive *map* (mu > 0), construction searches for a salt
  `b` with at least `p` value-matching keys (line 146 uses `h(1 || x_i || b)`),
  but the stored tuple is `(N, t)` with no `b`. `Find` then needs `b` to recover
  the value (line 225). For the adaptive *set* the salt is genuinely unnecessary
  (`b = epsilon`), so `(N, t)` is fine; but for the map the construction has
  selected a nonempty `b` and must store it, or `Find` cannot decode. The
  comparison table (`tab:predicate_comparison`) likewise lists adaptive "Stored
  params" as `(N, t)`, which is correct only for sets.
- **Suggestion:** For the adaptive map, store `(N, t, b)` and update both the
  algorithm's `\KwOut`, the `Find` precondition, and the table footnote ("`(N,t)`
  for sets; `(N,t,b)` for maps"). This also slightly changes the adaptive *map*
  space accounting (it is no longer salt-free), which should be noted in
  `sec:adaptive_space`.
- **Severity:** Major. It is a real inconsistency between the map construction
  output and the map lookup, of the same family as the prior C3 (which was fixed
  for the fixed-threshold path but not propagated to the adaptive map path).

### MINOR-1: Incorrect closed form for E[log2 Q] in the space proof
- **Location:** `sections/space.tex`, Thm `thm:space`, lines 65-68.
- **Quoted text:** "Since `Q ~ Geom(p)`, `E[log2 Q] = -log2 p - (log2 e)(1-p)
  log(1-p)/p -> -log2 p` as `p -> 0`."
- **Problem:** `E[log2 Q]` has no elementary closed form, and the stated
  equality is numerically false. For Q geometric on {1,2,...} with mean 1/p, the
  true `E[log2 Q] + log2 p` approaches roughly -0.83 as p -> 0, whereas the
  printed expression `-(log2 e)(1-p)log(1-p)/p` approaches +log2 e approx +1.44.
  (Checked numerically at p = 0.5, 0.3, 0.1, 0.05, 0.01: the gap is large and
  grows.) The expression appears to be a misremembered geometric-entropy term.
- **Why this is only minor:** The lower-bound half of the proof needs only
  `E[log2 Q] = -log2 p + O(1)`, which *is* true (verified numerically: the
  additive gap is bounded). Combined with `floor(log2 x) >= log2 x - 1` and the
  Jensen upper bound `E[L] <= log2 E[Q] = -log2 p`, the conclusion
  `E[L] = -log2 p + O(1)` is correct. The defect is a false intermediate
  identity, not a broken result.
- **Suggestion:** Replace the equality with the bound actually used:
  "Since `Q ~ Geom(p)`, `E[log2 Q] = -log2 p + O(1)` (the geometric distribution
  concentrates on the scale 1/p); combined with the floor bound,
  `E[L] = -log2 p + O(1)`." Alternatively, cite the exact identity
  `E[L] = sum_{n>=1} q^{2^n - 1}` from `thm:expected_size` (which I verified
  equals `E[floor log2 Q]` exactly) and bound that sum directly.

### MINOR-2: Incorrect entropy closed form in Remark `rem:info_interp`
- **Location:** `sections/space.tex`, Remark `rem:info_interp`, lines 255-261.
- **Quoted text:** "`H(Q) = [-log2 p + (1-p)log2(1-p)/p] = -log2 p + O(1)
  = m log2(1/eps*) + O(1)`."
- **Problem:** The displayed closed form is not the entropy of a geometric
  variable. The correct entropy (support {1,2,...}) is
  `H(Q) = [-(1-p)log2(1-p) - p log2 p]/p`, i.e. the first term also carries the
  1/p factor. The printed expression omits it. Numerically the two disagree
  (e.g. at p = 0.1, true H = 4.690, printed expression = 1.954). There is also a
  stray empty denominator `\frac{...}{\phantom{x}}` in the LaTeX, a typesetting
  artifact.
- **Why this is only minor:** The asymptotic claim `H(Q) = -log2 p + O(1)` is
  correct (verified: `H(Q) + log2 p -> log2 e approx 1.4427`), so the remark's
  punch line (the salt's entropy equals the gap Delta) holds.
- **Suggestion:** Either write the correct closed form
  `H(Q) = -log2 p - ((1-p)/p) log2(1-p)` or drop to the asymptotic statement
  `H(Q) = -log2 p + O(1)`. Remove the `\phantom{x}` denominator.

### MINOR-3: FNR search complexity for the equality predicate is still stated as
worst case without foregrounding the hash-and-count improvement
- **Location:** `sections/shf.tex`, Thm `thm:fnr_search` (lines 129-152) and the
  following Remark (lines 154-162).
- **Problem:** The theorem gives `O(C(m,p) * m)` for the equality predicate,
  then the very next remark concedes a hash-and-count approach achieves `O(m)`.
  A theorem whose bound is immediately undercut by the adjacent remark reads as
  an overstatement of the threshold predicate's advantage. This was MINOR in the
  prior pass and is unchanged.
- **Suggestion:** Fold the remark's content into the theorem statement: state
  the bound "for the subset-enumeration algorithm of Alg. 1," and note the
  achievable `O(m)` alternative, so the genuine difference (constant factor /
  no implicit search over targets) is what the threshold predicate buys.

### MINOR-4: Random oracle definition omits explicit cross-input independence
- **Location:** `sections/prelim.tex`, Def. `def:randomoracle`, lines 31-38.
- **Quoted text:** "outputs are independent and uniformly distributed over its
  range for every distinct input."
- **Problem:** This is actually improved over the prior draft (it now says
  "independent and uniformly distributed"). The phrase "over its range for every
  distinct input" is slightly ambiguous about whether independence is across
  inputs or across prefix bits. This is a very small wording nit.
- **Suggestion:** "...whose outputs on distinct inputs are mutually independent,
  each uniformly distributed over the range." Optionally cite Bellare-Rogaway
  (1993).

### MINOR-5: Overloaded symbol N
- **Location:** throughout. `N` is the threshold modulus (Sec. 3) and `NatSet`
  is the naturals; the salt bit-length RV is now `L` (good, the prior overload
  of `N` for the bit-length RV is resolved). The residual collision is `N`
  (modulus) appearing near `\NatSet`.
- **Suggestion:** No action strictly required; consider `M` or `R` for the
  modulus if a clash is felt. Noting for completeness; the prior MINOR on this is
  largely resolved.

## Verification Notes (what I checked numerically)

1. **Order-statistic PMF (appendix `eq:os_pmf_detailed`)** sums to 1 across
   `(N,m,p) = (10,4,2), (20,5,3), (12,6,1), (8,3,3)`. Correct. Prior C2 resolved.
2. **`E[L] = sum_{n>=1} q^{2^n-1}` (Thm `thm:expected_size`)** equals
   `E[floor log2 Q]` exactly at p = 0.2, 0.05, 0.01. Correct.
3. **Asymptotics** `E[log2 Q] = -log2 p + O(1)` and `H(Q) = -log2 p + O(1)`
   both verified (bounded additive gap). Headline space and price-of-certainty
   results are sound.
4. **Adaptive moments** `E[eps] = p/(m+1)`, `Var = p(m-p+1)/((m+1)^2(m+2))` are
   the standard Beta(p, m-p+1) moments. Correct.
5. **Set lower bound vs map lower bound** with mu = 0 recovers the set bound.
   Consistent. The FNR factor `(1-fnr)` in `post:set_lb`/`post:map_lb` matches
   the effect-of-false-negatives derivation in `sec:space`.

## Proof Chain Status

1. Bernoulli set/map defs, lower bounds (Sec. 2): OK, now cited to carter1978.
2. Acceptance predicate, FPR = |A|/N (Sec. 3): OK.
3. Success probabilities, equality and threshold (Thm 3.1, 3.2): OK now that the
   value hash is salted in the algorithms.
4. FPR granularity (Thm 3.3): immediate, OK.
5. FNR search complexity (Thm 3.4): correct but overstated, see MINOR-3.
6. Adaptive set (Thm 3.5): OK, p_ad = 1, salt unneeded for sets.
7. Adaptive map (Thm 3.6) and Alg 3 / Find: success-prob analysis OK, but the
   stored-tuple vs Find salt mismatch is a real gap, see MAJOR-1.
8. Adaptive FPR distribution and moments (Thm 3.7, 3.8): OK.
9. Space complexity (Thm 5.2): conclusion OK; intermediate identity wrong,
   see MINOR-1.
10. Finite correction, effect of false negatives (Sec. 5.3-5.4): OK.
11. Adaptive space (Thm 5.5) and price of certainty (Thm 5.7): OK; the
    "lower bound not violated" remark is now formal (prior M4 resolved). The
    interpretation entropy line has a wrong closed form, see MINOR-2.
12. Max entropy (Thm 6.1): informal but directionally sound; the adaptive-not-
    max-entropy remark (`rem:adaptive_not_max_entropy`) is a careful and correct
    clarification.
13. Salt PMF (Thm 6.2, App A): elegant and correct (telescoping verified).
14. Adaptive PMF (App B): correct in the N >> m regime, now stated as such.
15. Convergence (Thm 8.1, 8.2): straightforward and correct.
