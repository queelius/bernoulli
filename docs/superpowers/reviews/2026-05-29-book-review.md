# Book-Level Review (chapters 1-18)

Date: 2026-05-29
Reviewer: bookwright reviewer orchestrator (book scope)
Synthesis of: five Part-level reviews from 2026-05-28 (Part I) and 2026-05-29 (Parts II-V)
Method: spec, quality, math, and cross-ref auditor lenses applied per chapter; per-Part orchestrators chunked the work; numerical claims independently verified with Python where applicable.

## Aggregate counts

| Part | Chapters | Findings | BLOCKER | MAJOR | MINOR | NOTE |
|---|---|---|---|---|---|---|
| I | 1-4 | 38 | 1 | 7 | 19 | 11 |
| II | 5-8 | 34 | 0 | 6 | 17 | 11 |
| III | 9-13 | 32 | 0 | 7 | 15 | 10 |
| IV | 14-15 | 27 | 1 | 6 | 12 | 8 |
| V | 16-18 | 33 | 0 | 7 | 19 | 7 |
| **Total** | **1-18** | **164** | **2** | **33** | **82** | **47** |

Per-chapter Part-level reports (each linked from this synthesis):
- `docs/superpowers/reviews/2026-05-28-part1-review.md`
- `docs/superpowers/reviews/2026-05-29-part2-review.md`
- `docs/superpowers/reviews/2026-05-29-part3-review.md`
- `docs/superpowers/reviews/2026-05-29-part4-review.md`
- `docs/superpowers/reviews/2026-05-29-part5-review.md`

## BLOCKERs (must fix before publication)

### B1. §3.4 Miller-Rabin bound notation reuse
**File:** `book/chapters/ch03/miller-rabin.tex` lines 184-188.
**Issue:** Displayed inequality writes $\fprate_k \le \fprate^k \le (1/4)^k$, reusing $\fprate$ for two different quantities (per-round FPR vs aggregate $k$-round FPR). Middle term should be $\prod_i \fprate_i$, which the next paragraph already uses correctly.
**Fix:** Five-minute notation correction.

### B2. §15.2 BPHF FNR derivation mathematically unsupported
**File:** `book/chapters/ch15/bphf-construction.tex` lines 218-247.
**Issue:** Text claims per-member rank-collision probability is "at most $\binom{n}{2} \cdot 2^{-r}$" but $\binom{n}{2} \cdot 2^{-r}$ is the expected number of colliding pairs over the whole set, not the per-member probability. Correct per-member union bound is $(n-1) \cdot 2^{-r}$. At $r = \lceil \log_2 n \rceil$ this is $\Theta(1)$, not $2^{-r}$. Headline bound $\fnrate \le 2^{-r}$ does not follow. Ex 15-9 explicitly confirms the gap.
**Compounded by:** §15.2 also hand-waves the $\fprate = 0$ claim (the rank-equality check $R[\phi(x)] = \rho(x)$ under uniform $\rho$ delivers FPR $= 2^{-r}$, identical to BHF; the discriminator that drives FPR to 0 is mentioned in one sentence but never specified in pseudocode), and §15.2 vs §15.4 are inconsistent about $\rho$'s domain (chapter 15 §2 treats $\rho$ as defined on $\Universe$; §4 uses sort-position rank defined only on $A$).
**Fix:** Substantive rewrite of §15.2. Either reformulate the construction so the analysis actually works (likely requires citing the bernoulli-phf paper for the real construction including the discriminator), or split into two operations (a "bare" BPHF with FPR $= 2^{-r}$, $\fnrate = 0$ and a "full" BPHF with the discriminator pushing FPR to 0 at extra cost). Chapter 15 cannot ship as drafted.

## MAJORs by Part (33 total)

### Part I (7)

1. **§3.5 line 60** Bloom filter formula $p = 1 - (1 - 1/n)^k$ drops the $m$ (hash count) from the standard formula $1 - (1 - 1/b)^{m \cdot k}$. Either correct or replace with a forward pointer to chapter 5.
2. **§3.1 / §3.2 / §4.5 AND closure reconciliation.** §3.1 gives both a prior-mixed FPR formula and a distribution-free upper bound; §3.2 Proposition 3.2.1 and §4.5 silently assume AND is $\Bernoulli{\BoolType} \times \Bernoulli{\BoolType} \to \Bernoulli{\BoolType}$ with a single derived rate. Pick a convention and use it consistently.
3-7. Additional MAJORs in Part I report: (3) chapter 1 §1.2 contingency table label slip; (4) chapter 2 §2.4 model-order vs DOF clarification flagged-but-still-ambiguous; (5) chapter 4 §4.4 Kronecker conditional-vs-unconditional caveat under-explained for first-time reader; (6) chapter 3 §3.3 composition theorem statement could be tightened; (7) chapter 4 §4.5 examples sub-block formalism shorthand.

### Part II (6)

1. **§6.3 prop:mixed-intersection-escape internally inconsistent.** Title says "Mixed-axis intersection escapes the line"; proof concludes "In neither case does the result fall on the FNR-zero or FPR-zero axis." But boundary regime gives $(0, \fnrate_B)$, which sits on the FPR-zero axis. Proposition needs to distinguish "leaves FNR-zero, lands on FPR-zero" (boundary case, line preserved) from "leaves line entirely" (non-boundary).
2. **§6.4 prop:fnr-zero-closure part (4) vacuous hypothesis.** Both operands required FNR-zero with FPR > 0; part (4) further requires B to be FPR-zero. Forces B to be exact (excluded from framework). Only "otherwise" clause has content.
3. **§6.2 intersection FPR worked example materially incomplete.** Proof derives $\fprate_A \cdot \fprate_B$ only for "$x \notin A$ AND $x \notin B$" regime; worked example computes $0.01 \cdot 0.02 = 0.0002$ without specifying $A = B$. For different objective sets, boundary terms can contribute $(1 - \fnrate_A) \cdot \fprate_B = \fprate_B$ when $\fnrate_A = 0$.
4-6. Additional MAJORs: chapter 7 §7.4 PPV formula's prior-vs-data distinction in the worked CI; chapter 8 §8.3 entropy floor proof sketch missing the standard "approximate set as Boolean function" framing for first-time reader; chapter 6 §6.4 perfect-filter-line definition's $\fnrate = 0$ vs "achievable in the limit" should be sharper.

### Part III (7)

1. **§13 ex 13-1 Bernoulli[Bool] matrix convention contradicts chapter 4 §4.5.** Exercise writes $Q_1 = [[1-\fprate_1, \fprate_1], [\fnrate_1, 1-\fnrate_1]]$; canonical from chapter 4 is $[[1-\fnrate, \fnrate], [\fprate, 1-\fprate]]$. Exercise's Kronecker entry verification claim requires canonical ordering.
2. **§11.4 BPP amplification loosening range claim.** Lines 196-204 state $\exp(-\mu \epsilon'^2 / 2) \le \exp(-2 k \epsilon_0^2 / 3)$ "when $\epsilon_0 \le 1/2$" but actually holds only when $\epsilon_0 \le 1/4$ (symbolic verification: difference factors as $\epsilon_0^2 (1 - 4\epsilon_0) / [3(2\epsilon_0 + 1)]$). Worked example at $\epsilon_0 = 1/6$ is fine; stated range is too generous.
3. **§11 ex 11-5 KL divergence arithmetic error.** Binary KL $D(1/2 \| 1/3) \approx 0.0817$ is wrong (correct: 0.0589 nats or 0.0850 bits); symbolic expression drops a sign (should be $\log_2(3/4)$ on second term). Headline $k \approx 125$ from Hoeffding is correct.
4-7. Additional MAJORs: chapter 9 §9.5 bridge-to-sketches subsection title vs content mismatch; chapter 10 §10.3 HyperLogLog's small-range correction stated without justification; chapter 12 §12.2 relation composition's join semantics need example; chapter 13 §13.3 functor laws stated without verification examples.

### Part IV (6)

1-3. Already listed under BLOCKER B2 (the §15.2 issues are tangled together).
4. **§14.2 BHF FPR derivation under non-uniform fingerprint distribution** not discussed; assumes uniform hash family without flagging the assumption explicitly.
5. **§15.4 ranked-search example** specifies "$r = 20$" but doesn't justify why this matches chapter 15's earlier $r = \lceil \log_2 n \rceil$ for $n = 10^6$ (yes it does: $\log_2 10^6 \approx 20$, but the text doesn't say so).
6. **§14.7 vs §15.6 bib notes overlap**: both cite Carter-Wegman without cross-reference; a reader of §15.6 hits the same citation twice without commentary.

### Part V (7)

1. **§16.6 lines 49-50 `Part~VI` typo (twice).** Should be `Part~V`. Visible structural typo immediately before chapter 17 opens.
2. **§17.1 / §17.4 Bloom-vs-BHF conflation.** §17.1 line 137-139 and §17.4 line 185-187 conflate Bloom (9.59 bits/element at $\fprate = 0.01$) with BHF (6.64 bits/element). §17.4's "830 KB" worked example total uses BHF arithmetic but labels the construction "Bloom-filter cipher map" (propagates a ~30% error).
3. **§16.2 "Bloom past capacity" worked example three internal numerical inconsistencies**: (a) fill ratio "30%" vs actual 51.8% at design parameters; (b) "rate $\approx 0.5$ late" vs actual 0.83 at $n = 5000$; (c) trajectory expectation "$\approx 230$" matches none of the natural readings.
4. **§17.3 "$O(\log n)$ bits/query" mixes two scalings.** Should distinguish per-query token leakage from per-deployment leakage budget.
5. **§18.4 Clopper-Pearson "0.95" understated.** Actual coverage at the worked parameters is $\approx 0.986$; stated as 0.95.
6-7. Additional MAJORs: §17.6 confidentiality plot axes need labels; §18.3 NPV vs F1 leakage formulas could be tightened.

## Cross-chapter coherence findings

### CR1. Q matrix convention drift (chapter 4 vs 13)
Chapter 4 §4.5 canonical: rows indexed by truth ($\top, \bot$); columns by report. Row 1 entries are $(1 - \fnrate, \fnrate)$, row 2 entries are $(\fprate, 1 - \fprate)$. Chapter 13 exercise 13-1 reverses this. Other Part III chapters mostly stay canonical; the exercise is the outlier. Fix: rewrite ex 13-1 to use canonical Q.

### CR2. Bloom-filter rate convention vs BHF rate convention (chapter 5 vs 14 vs 17)
Chapter 5 §5.2 gives Bloom space as $\approx 1.44 \cdot n \log_2(1/\fprate)$ bits (the post-fix value, $\approx 9.6n$ at $\fprate = 0.01$). Chapter 14 §14.3 gives BHF space as $\lceil -\log_2 \fprate \rceil$ bits per element ($\approx 6.64n$ at $\fprate = 0.01$). Chapter 17 §17.4 cites the Bloom number but uses BHF arithmetic in the worked example (the "830 KB" calculation). Either re-do §17.4 with the correct Bloom number, or re-label as BHF cipher map.

### CR3. Chapter 3 §3.4 vs chapter 11 §11.1 Miller-Rabin notation
§3.4 reuses $\fprate$ for both per-round and aggregate (BLOCKER B1); §11.1's formal restatement uses distinct symbols. Fix B1 in chapter 3, then check §11.1's recap uses the chapter-3 corrected notation rather than introducing fresh symbols.

### CR4. Chapter 6 §6.4 perfect-filter-line vs chapter 14/15 constructive realization
Chapter 6 §6.4 defines the perfect-filter line as $\{\fnrate = 0\} \cup \{\fprate = 0\}$. Chapter 14 says BHF realizes the FNR-zero axis; chapter 15 says BPHF realizes the FPR-zero axis (under BLOCKER B2 caveats). The cross-references all resolve. But the geometric framing in §6.4 has $\fprate$ on the y-axis and $\fnrate$ on the x-axis (or vice versa, depending on how you read the prose); chapters 14, 15 don't reference the orientation, so a reader checking the geometry has to re-derive it. Add an orientation sentence to §6.4.

### CR5. Notation sidebars
The previous fix (commit `58732ad`) scrubbed reader-facing LaTeX-macro names from chapters 1/2/7. The cross-ref-auditor for each Part confirmed: no remaining occurrences in chapters 3-18. The fix is complete and the soul-voice macro-leak hook has been doing its job since.

## Documented deferred items (acknowledged, NOT re-flagged)

All Part-level reports confirm these forward-reference slug mismatches are present in the build log and were left intact by their respective auditors:
- `ch:composition` (chapter 4 → chapter 6; chapter 6's actual label is `ch:set-composition`).
- `ch:sketches` × 5 (chapter 9 prose; chapter 10's actual label is `ch:sketches-estimators`).
- `sec:noisy-bit` × 2 (chapter 17; chapter 1's actual labels are `sec:quantifying-noise` / `sec:sampling-rates`).

Polish plan should resolve all three.

## Recommended next actions (prioritized)

### Tier 1: BLOCKERs (must fix before publication)
1. **B1.** Notation fix in `book/chapters/ch03/miller-rabin.tex` lines 184-188. Five-minute change.
2. **B2.** Substantive rewrite of `book/chapters/ch15/bphf-construction.tex` §15.2. Likely requires consulting the bernoulli-phf paper to reproduce the actual construction including the FPR-zero discriminator.

### Tier 2: MAJORs (should fix before publication; 33 items)
- Cross-chapter coherence (CR1-CR4) first, since they propagate.
- Then per-chapter MAJORs.
- Most are 30-60 minute edits; total work estimate: 25-35 hours.

### Tier 3: MINORs (polish plan; 82 items)
- Style consistency, tightening, typo cleanup.
- Most are 5-15 minute edits each; total work estimate: 15-20 hours.

### Tier 4: NOTEs (47 items)
- Editorial suggestions; some warrant the author's judgment call.
- No deadline; can be addressed selectively.

### Tier 5: Already-documented deferred items
- The three slug mismatches (`ch:composition`, `ch:sketches`, `sec:noisy-bit`); 30 minutes total.

### Total polish-plan estimate
- BLOCKERs: 1 + 6-12 hours.
- MAJORs: 25-35 hours.
- MINORs (selective): 10-15 hours.
- Documented deferred items: 0.5 hours.
- Appendix B (Five Core Principles cheat sheet) and D (Selected Exercise Solutions) population: out of scope of this review.

**Recommended sequence:** B1 first (5 min). Then B2 (substantive, may need 1-2 sessions). Then CR1-CR4 cross-chapter coherence. Then by-Part sweep of MAJORs in dependency order. MINORs and NOTEs in a final polish pass.

## Summary

The book is structurally sound: 18 chapters drafted, 528 body pages, 15 paired notebooks, all running threads carry as designed, soul-voice and macro-leak hooks clean across the source tree. Two BLOCKERs need attention: B1 (chapter 3 §3.4 notation) is trivial; B2 (chapter 15 §15.2 BPHF construction + analysis) is substantive and may benefit from another pass through the underlying bernoulli-phf paper. Beyond the BLOCKERs, the book is in a good state to enter a focused polish phase; the 33 MAJORs + 82 MINORs are typical for a 528-page first-draft monograph, and the cross-chapter coherence findings (CR1-CR5) are five well-defined items, none of them structural.
