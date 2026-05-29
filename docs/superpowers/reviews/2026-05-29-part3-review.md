# Part III Review (chapters 9-13)

Date: 2026-05-29
Reviewer: bookwright reviewer orchestrator (Part III scope)
Auditors applied: spec, quality, math, cross-ref (per-chapter, inline)

This review evaluates all five chapters of Part III ("From Sets to Maps")
of *Bernoulli Types: An Algebra of Approximate Computation* against the
Part III design spec
(`docs/superpowers/specs/2026-05-23-bernoulli-textbook-part3-design.md`)
and the master spec
(`docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`). The
four auditor roles were applied per chapter and the findings are
synthesized below by chapter and by cross-chapter coherence. The
documented deferred items (`ch:composition` x 1, `ch:sketches` x 5,
`sec:noisy-bit` x 2) match `book/book.log` exactly and are not flagged.

## Summary

- **Total findings: 32** (0 BLOCKERs, 7 MAJORs, 15 MINORs, 10 NOTEs).
- **Top high-priority items:**
  1. (MAJOR) §13 ex 13-1 (`chapters/ch13/exercises.tex` lines 40-53): the matrix $Q_1 = \begin{pmatrix} 1-\fprate_1 & \fprate_1 \\ \fnrate_1 & 1-\fnrate_1 \end{pmatrix}$ in the exercise statement contradicts the canonical chapter 4 \S4.5 convention `def:bernoulli-bool`, which writes $Q = (\tprate, \fnrate; \fprate, \tnrate) = (1-\fnrate, \fnrate; \fprate, 1-\fprate)$. The exercise's verification claim that "the $(\top, \top) \to (\top, \top)$ entry equals $(1 - \fnrate_1)(1 - \fnrate_2)$" requires the diagonal to be $(1-\fnrate, 1-\fprate)$, which only holds under the chapter 4 ordering. The matrix as written in ex 13-1 has $1-\fprate$ in position (1,1), so the Kronecker product entry there would be $(1-\fprate_1)(1-\fprate_2)$, not the claimed value. Either the matrix needs the rows swapped to match chapter 4, or the verification claim needs to be restated as $(1-\fprate_1)(1-\fprate_2)$ to match the matrix.
  2. (MAJOR) §11.4 lines 196-204 (`chapters/ch11/sample-complexity.tex`): the loosening claim $\exp(-k\fprate_0^2/(2(1/2 + \fprate_0))) \le \exp(-2 k \fprate_0^2 / 3)$ "when $\fprate_0 \le 1/2$" is wrong. Symbolic computation gives the loosening valid only when $\fprate_0 \le 1/4$. (Compute $\fprate_0^2/[2(1/2 + \fprate_0)] - 2\fprate_0^2/3 = \fprate_0^2 (1 - 4\fprate_0) / [3(2\fprate_0 + 1)]$, which is non-negative iff $\fprate_0 \le 1/4$.) For the worked BPP case $\fprate_0 = 1/6$ the loosening is valid, so the headline $k \ge 108 \ln(1/\delta)$ and the worked $k \approx 1492$ at $\delta = 10^{-6}$ both check; but a reader who applies the bound at the upper end of the BPP range $\fprate_0 \in (0, 1/2)$ will get an invalid inequality.
  3. (MAJOR) §11 ex 11-5 lines 110-126: the KL-divergence value $D(1/2 \| 1/3) \approx 0.0817$ "in natural-log units" is wrong, and the symbolic expression $(1/2) \log_2(3/2) + (1/2) \log_2(3)$ does not compute to that value either. The correct binary KL $D(1/2 \| 1/3) = (1/2) \ln(3/2) + (1/2) \ln(3/4) \approx 0.0589$ nat, or equivalently $\approx 0.0850$ in $\log_2$ units. The symbolic expression in the exercise drops a sign on the second term (it should be $\log_2(3/4)$, not $\log_2(3)$). However, the coarser Hoeffding bound $\exp(-k/18)$ that the exercise actually uses to compute $k \approx 125$ is the right form (additive Hoeffding for a Bernoulli sum with mean-deviation $1/6$ gives $\exp(-2k(1/6)^2) = \exp(-k/18)$, and $k \ge 10 \cdot 18 \cdot \ln 2 \approx 124.8$). So the final numerical answer is right; only the intermediate KL expression and its claimed numeric value are wrong.
- **Chapters with most findings:** Chapter 11 (10), Chapter 13 (8), Chapter 10 (6), Chapter 12 (5), Chapter 9 (3).

Overall the chapters are in solid shape. Every numerical claim except
the §11 ex 11-5 KL value verified independently with Python checks. The
§9.3 worked example (joint $(1,2,1)$ given blocks $(B_1, B_2, B_1)$ on
the $90\%$-accuracy symmetric matrix gives $0.9^3 = 0.729$) and the §9.4
4-state strongly-symmetric capacity $\log_2 4 - H(0.9, 0.0333, 0.0333,
0.0333) \approx 1.373$ both check exactly. The §10.2 CountMin
$(w = \lceil e/\epsilon \rceil, d = \lceil \ln(1/\delta) \rceil)$ bound
recovers $\epsilon \le 0.272$ and $\delta \le 0.00674$ for the worked
$(w, d) = (10, 5)$ as stated. The §10.3 HyperLogLog $1.04/\sqrt{m}$
relative-error scaling, the $\alpha_{256} \approx 0.7183$
bias-correction, and the worked example's $\hat n \approx 7240$ from the
Z = 6.5 sum all check. The §10.4 MinHash variance $J(1-J)/k$ and the
Hoeffding tail $2 \exp(-2k \epsilon^2)$ check with the worked $J = 30/170
\approx 0.176$, variance $7.26 \times 10^{-4}$, and Hoeffding bound at
$\epsilon = 0.05$ equal to $2/e \approx 0.736$. The §11.1 Miller-Rabin
$(1/4)^k$ composition gives $k = 10$ rounds for $\delta = 10^{-6}$ and
$k = 20$ for $\delta = 10^{-12}$ as stated. The §11.4 Chernoff bound's
intermediate computation (corrected for the loosening range above) gives
$k \approx 1492$ rounds for BPP amplification at the conventional
$\fprate_0 = 1/6$ to $\delta = 10^{-6}$, matching the text. The §12.3
MinHash-LSH worked example numbers (per-pair Hoeffding $\exp(-16)
\approx 1.1 \times 10^{-7}$, LSH survival probabilities $0.434$, $0.019$,
$1.2 \times 10^{-4}$ at $J = 0.7, 0.5, 0.3$, candidate-set total $\approx
743$) all check.

The two Part III climaxes (the §9.3 n-ary Kronecker theorem and the
§13.3 four-row composition-functor table) both land. The Miller-Rabin
thread carries from §3.4 informal to §11.1 formal (closing the
chapter 3 deferral as the spec called for), and the §12.3 MinHash-LSH
discussion connects back to §10.4 (the chapter 10 MinHash construction)
exactly as the spec's forward-reference map promised. No em-dashes
(U+2014). No "easy to see", "obviously", "trivially". No banned phrases.
No label collisions.

The findings below are sorted by severity within each chapter, then by
location.

## Findings by chapter

### Chapter 9: Approximate Functions and n-ary Channels (~25 pp; target ~26 pp)

**spec-auditor:** all checklist items per spec §4 chapter 9 row are
realized. Six sections (§9.1 From Approximate Sets to Approximate
Functions, §9.2 N-ary Channels with the model-order $K$ definition, §9.3
The n-ary Kronecker Theorem with full proof and parameter-count
corollary, §9.4 Capacity for n-ary Channels including the
strongly-symmetric closed form, §9.5 Bridge to Sketches, §9.6
Bibliographic Notes). Learning outcomes box has three bullets per spec
format. The notation convention ($K$ uppercase for model-order vs $k$
lowercase for hash count, etc.) is explicitly fixed at §9.2 lines
123-156, addressing Open Action Item 2 of the spec. 11 exercises with
3/5/3 difficulty distribution.

**quality-auditor (cold read):** §9.1 motivates the type-lifting cleanly
with the predicate-as-membership recap and two concrete examples
(3-class classifier, infinite-state counter). §9.2's formal n-ary
channel definition explicitly recovers chapter 2's BSC and asymmetric
channel as $K = L = 2$ specializations. §9.3's Kronecker theorem proof
sketch (4 steps) mirrors chapter 4 §4.4 step-for-step, with the
deterministic-rates regime restriction clearly stated. §9.4's
strongly-symmetric closed form $C = \log_2 L - H(\mathbf{r})$ generalizes
the chapter 8 BSC capacity $C = 1 - H(\fprate)$ at the $L = 2$ specialization.

**math-auditor:** verified all numerical claims independently. §9.3
worked example with the 3-class classifier $Q = 0.9 I + 0.0333 (J - I)$:
joint $(Y_1, Y_2, Y_3) = (1, 2, 1)$ given $(B_1, B_2, B_1)$ gives
$0.9 \cdot 0.9 \cdot 0.9 = 0.729$ as stated, and the off-diagonal joint
$(2, 2, 1)$ gives $0.05 \cdot 0.9 \cdot 0.9 = 0.0405$ as stated. The
parameter-count contrast at $m = 3$ ($K(L^m - 1) = 78$ unconstrained) and
$m = 10$ ($3(3^{10} - 1) = 177144 \approx 1.77 \times 10^5$) both check.
§9.4 4-state strongly-symmetric capacity at $p_e = 0.1$: $H(\mathbf{r})
= -0.9 \log_2 0.9 - 3 \cdot 0.0333 \log_2 0.0333 \approx 0.137 + 0.490 =
0.627$, $C = 2 - 0.627 = 1.373$ as stated. The BSC capacity comparison
at $p_e = 0.1$ gives $1 - H_2(0.1) = 0.531$ as stated.

**cross-ref-auditor:** all DEFINED labels match `\label{}` declarations.
All RESOLVED labels exist (`sec:from-atom-to-set`, `def:bernoulli-bool`,
`thm:kronecker`, `cor:parameter-reduction`, `ax:element-indep`,
`ax:block-rates-indep`, `def:bsc`, `def:asymmetric-channel`,
`def:model-order`, `thm:boolean-ceiling`, `prop:bsc-capacity`,
`sec:bsc-capacity`, `sec:entropy-refresher`, `sec:bloom-from-scratch`,
`sec:miller-rabin` all check). No label collisions. The five `ch:sketches`
references in §9.5 and §9 exercises are the documented deferred items
matching the build-log baseline.

#### Findings (chapter 9)

- **MINOR** §9.2 line 178 ($K = 2$, $L = 2$ symmetric BSC matrix): The matrix $Q_{\mathrm{BSC}} = \begin{pmatrix} 1-\fprate & \fprate \\ \fprate & 1-\fprate \end{pmatrix}$ in Example 1 is presented with row 1 = $B_1 = \{\top\}$ per §9.2 convention. The diagonal $(1-\fprate)$ in row 1 represents the symmetric case where $\fprate = \fnrate$, and the chapter 4 §4.5 canonical Bernoulli[Bool] matrix `def:bernoulli-bool` writes $(\tprate, \fnrate; \fprate, \tnrate) = (1-\fnrate, \fnrate; \fprate, 1-\fprate)$, so the (1,1) entry should be labeled $1 - \fnrate$ to match. In symmetric BSC the two labels coincide, so the matrix is correct, but the asymmetric Example 2 then correctly uses $1 - \fnrate$ in position (1,1). The symmetric Example 1 could use the same labeling discipline for consistency. (NOTE in Part II terms; the chapter 4 convention is already canon.)
- **MINOR** §9.4 line 281-286 (worked example rounding): the diagonal contribution is computed as $-0.9 \log_2 0.9 \approx 0.137$ to three decimal places, and the off-diagonal contribution as $-3 \cdot 0.0333 \log_2 0.0333 \approx 0.490$. Both values are correct, but the next sum is given as $H(\mathbf{r}) \approx 0.137 + 0.490 = 0.627$, which is also correct ($0.6275$ to four places). The final capacity is $C \approx 2 - 0.627 = 1.373$, correct. The arithmetic chain is right; the rounding precision is consistent.
- **NOTE** §9.5 bridge-to-sketches (lines 56-79): the type-lifting framing of CountMin, HyperLogLog, and MinHash as $\Bernoulli{T}$ instances with different output-type shapes ($T = \mathbb{N}$ upper-triangular vs $T = \mathbb{N}$ band vs $T = [0, 1]$ continuous) is excellent forward-pointing pedagogy. The bridge is dense (one paragraph per sketch); a small table would compress this into a single page-of-eyes summary, but the prose works as is.

### Chapter 10: Sketches and Estimators (~24 pp; target ~28 pp)

**spec-auditor:** all six sections present per spec §4 chapter 10 row.
§10.1 sketches as $\Bernoulli{T}$ (the unifying lens); §10.2 CountMin
construction with the $w = \lceil e/\epsilon \rceil, d = \lceil
\ln(1/\delta) \rceil$ parameters and Markov-plus-union-bound proof; §10.3
HyperLogLog leading-zero trick, multi-register harmonic mean, and $1.04 /
\sqrt{m}$ standard error; §10.4 MinHash collision identity, Hoeffding
bound, and LSH bands; §10.5 bridge to chapters 11, 12, 13; §10.6
bibliographic notes. 11 exercises with 3/5/3 distribution. Chapter is at
~24 pp, somewhat under the spec's 28 pp target but within reasonable
tolerance (-14%).

**quality-auditor (cold read):** the chapter reads cleanly. The three
sketches share a common template (problem setup, construction with
pseudocode, error-bound theorem, $\Bernoulli{T}$ type identification,
merge/composition rule) that §10.1 names explicitly. The §10.3 single-
register $\hat n = 2^R$ estimator with its O(1) standard deviation in
$\log_2 n$ units, the multi-register stochastic-averaging fix, and the
harmonic-mean rationale are presented in three motivated steps. The §10.4
MinHash collision identity $\Pr[\min h(A) = \min h(B)] = J(A, B)$ proof
is short and combinatorial as the source paper has it. The LSH band
discussion is appropriately compact for a chapter focused on the sketch
constructions themselves.

**math-auditor:** verified all numerical claims. §10.2 worked $w=10, d=5$
gives $\epsilon \le e/10 \approx 0.272$ and $\delta \le e^{-5} \approx
0.00674$ as stated. The stream profile $f_{a_1} = 400, \ldots, f_{a_{50}}
= 4$ sums to $990$, padded to $F = 1000$ as stated. §10.3 worked example
at $m = 256, n = 10000$: load per bucket $\approx 39$, $\log_2 39 \approx
5.29$, $\alpha_{256} = 0.7213/(1 + 1.079/256) = 0.7183$ matches the $0.7182$
stated, and $\hat n = 0.7182 \cdot 256^2 / 6.5 = 7242$ matches $\approx
7240$. The $1.04/\sqrt{m}$ standard error at $m = 256$ is $0.065$ and at
$m = 2048$ is $0.023$, matching the table. §10.4 worked $|A| = |B| = 100$,
$|A \cap B| = 30$: $J = 30/170 = 0.1765$, $\Var{\hat J} = 0.176 \cdot
0.824 / 200 = 7.27 \times 10^{-4}$, SE $\approx 0.027$, all check. The
Hoeffding bound at $\epsilon = 0.05, k = 200$ gives $2 \exp(-2 \cdot 200
\cdot 0.0025) = 2/e \approx 0.736$ as stated.

**cross-ref-auditor:** all DEFINED labels match declarations; no
collisions. The chapter has the most forward references of Part III
(chapters 11, 12, 13), all chapter-level labels that exist via Plan 0
stubs.

#### Findings (chapter 10)

- **MAJOR** §10 ex 10-11 line 221 (`chapters/ch10/exercises.tex`): the LSH parameter sweep exercise opens with "The locality-sensitive hashing (LSH) scheme from \Cref{sec:ch10-bridge} partitions a length-$k$ MinHash signature into $b$ bands of $r$ rows each (so $k = b \cdot r$)." But LSH is defined and discussed in §10.4 (`sec:minhash-lsh`), not §10.5 (`sec:ch10-bridge`). The bridge mentions LSH only by name in a forward-pointing sentence. Change the reference to `\Cref{sec:minhash-lsh}`. (The cross-ref-auditor confirms `sec:minhash-lsh` is the correct label; the LSH construction including bands is at lines 251-300 of `minhash-lsh.tex`.)
- **MINOR** §10.3 line 311 (worked example sketch dump): the prose presents a representative register array "concentrated in this range, with distribution $M \approx (5, 5, 6, 4, 7, 5, 6, 5, 4, 6, 5, 7, 5, 6, 5, 4, \ldots)$ for the first sixteen entries, and a full sum $\sum_j 2^{-M[j]}$ on the order of $256/39 \approx 6.5$." The 16-entry sample is illustrative and matches a plausible seed-0 realization. The $Z = 6.5$ estimate is correct: if $M[j] \approx \log_2(n/m) \approx \log_2(39) \approx 5.29$ then $2^{-M[j]} \approx 1/39$, summed over $m = 256$ buckets gives $256/39 \approx 6.56$. The chained estimate $\hat n = 0.7182 \cdot 65536 / 6.5 \approx 7240$ matches. A reader who tries the actual seed 0 with a real hash will get a slightly different $Z$; the "verified in the chapter notebook with seed 0" note flags this, but the reader who runs it independently may see a different value. Consider adding "values to two significant figures" or "approximate to within the seed".
- **MINOR** §10.4 line 320 (Hoeffding bound calibration): the worked example at $\epsilon = 0.05, k = 200$ gives Hoeffding bound $2/e \approx 0.736$, which the prose then calls "loose at this scale because Hoeffding ignores the $J(1-J)$ factor". The bound is correct but the prose understates: at $J = 0.176$, the exact tail $\Pr[|\hat J - J| \ge 0.05]$ via the binomial CDF is approximately $0.075$, so the Hoeffding bound is loose by about an order of magnitude in probability. One sentence quantifying this would help.
- **MINOR** §10.4 lines 159-165 (signature streaming): "The signature is also \emph{streaming}: items can be inserted into $A$ one at a time, with each insertion updating each $\sigma_i$ in $O(1)$ via $\sigma_i \gets \min(\sigma_i, h_i(a))$. Deletion is not supported." This is correct but the next sentence "an item that once attained the minimum cannot be removed without rescanning the set" reads as a price of the construction. Consider mentioning the connection to the chapter 11 Las Vegas / Monte Carlo trade-off: a Las Vegas signature with deletion would be different.
- **NOTE** §10.1 lines 99-136 (the "Why the chapter 9 framework unifies them" subsection): the three sketches each have their channel matrix $Q$ structure named (CountMin upper triangular, HyperLogLog log-normal band, MinHash binomial rows). The three structural pictures are useful, but the relevant material for each sketch is then re-derived in §10.2-§10.4 individually. Consider a small synoptic table here ("Sketch | Output type | $Q$ structure | Composition rule") to anchor the comparison; the §10.5 bridge does some of this but a chapter-opening summary would help readers pace the chapter.
- **NOTE** §10.6 bibliographic notes: the four paragraphs (CountMin, HyperLogLog, MinHash, LSH) are appropriately concise and cite each original source. The Cormode-Yi survey reference suggested in the spec is mentioned as "the wider database literature" rather than cited specifically; consider adding the explicit citation for completeness.

### Chapter 11: Randomized Algorithms (~23 pp; target ~24 pp)

**spec-auditor:** all six sections present per spec §4 chapter 11 row.
§11.1 Miller-Rabin formal (recasts the §3.4 informal walkthrough as a
formal $\Bernoulli{\BoolType}$ instance with $\fnrate = 0, \fprate \le
1/4$, citing Rabin 1980); §11.2 Las Vegas vs Monte Carlo with the
$f : X \to Y$ remark; §11.3 RP, coRP, ZPP, BPP definitions and their
perfect-filter-line/interior reading; §11.4 sample complexity (the
multiplicative Chernoff bound with MGF + Markov proof, applied to
Miller-Rabin and BPP amplification, compared to the Chebyshev / variance
bound); §11.5 bridge; §11.6 bibliographic notes. 11 exercises with 3/5/3
distribution.

**quality-auditor (cold read):** the chapter reads cleanly. The §11.1
formalization of Miller-Rabin retires the chapter 3 §3.4 deferral
exactly as the spec called for: per-round bound $\fprate \le 1/4$ is now
cited to Rabin 1980 with the Miller 1976 deterministic-under-GRH
ancestor, the $k$-round bound is a corollary of the chapter 3
composition theorem, and the proof sketch clearly identifies the
division of labor between number theory (the strong-liar bound) and the
framework (the rest). §11.2's "two definitions" and "trade-off" are
presented with the right level of formal/intuitive balance. §11.3's
"complexity classes as locations on the rate plane" framing (RP on the
FNR-zero axis, coRP on the FPR-zero axis, ZPP at the origin, BPP in the
interior) is the chapter's organizing observation and is sustained
across all four classes. §11.4's Chernoff bound is stated as a theorem
with explicit proof sketch.

**math-auditor:** verified all numerical claims. The Miller-Rabin
round-count derivation is correct: $\log_2(10^6)/2 \approx 9.97$ giving
$k = 10$ for $\delta = 10^{-6}$, $\log_2(10^{12})/2 = 19.93$ giving $k =
20$. The BPP amplification calculation at $\fprate_0 = 1/6$: with the
loosened bound $\exp(-k \fprate_0^2 / 3) = \exp(-k/108)$, $k \ge 108
\ln(1/\delta) \approx 1492$ at $\delta = 10^{-6}$, matching the text's
$\approx 1490$. The §11.3 PPV computation at workload prevalence $\pi =
0.01$ with the BPP $2/3$-vs-$1/3$ gap gives $\PPV \ge 2 \cdot 0.01 /
(0.01 + 1) = 0.0198/1.01 \approx 0.0196$ as stated. The §11 ex 11-1
$(1/4)^{15} \approx 9.31 \times 10^{-10}$ check. The §11 ex 11-7
randomized quicksort constant $2 \ln 2 \approx 1.386$ matches the text's
$\approx 1.39$, and Markov gives $\Pr[T_n \ge 10 n \log_2 n] \le 0.139$
as stated. The §11 ex 11-8 PPV at $\pi = 0.1$ with both-sided $1/3$
error gives $(0.1 \cdot 2/3) / (0.1 \cdot 2/3 + 0.9 \cdot 1/3) =
0.1818$, matching the stated $\approx 0.182$. The §11 ex 11-10 Karger
amplification at $n = 100, \delta = 0.01$ gives $r \ge 4950 \ln(100)
\approx 22796$, matching the stated $\approx 22800$.

**cross-ref-auditor:** all DEFINED labels match declarations; no
collisions. All RESOLVED labels exist (`def:bernoulli-bool`,
`thm:composition`, `sec:miller-rabin`, `ax:element-indep`,
`def:perfect-filter-line`, `def:ppv`, `def:npv`, `sec:bsc`,
`sec:one-sided-two-sided`, `sec:perfect-filter-line`,
`sec:binomial-estimator` all check).

#### Findings (chapter 11)

- **MAJOR** §11.4 lines 196-204 (`chapters/ch11/sample-complexity.tex`): the loosening
  ```
  exp(-mu(eps')^2/2) = exp(-k eps_0^2 / [2(1/2 + eps_0)])
                    <= exp(-2 k eps_0^2 / 3)   when eps_0 <= 1/2
  ```
  is invalid at the upper end of the stated range. Symbolic algebra:
  $\fprate_0^2 / [2(1/2 + \fprate_0)] - 2 \fprate_0^2 / 3 = \fprate_0^2 (1 - 4 \fprate_0) / [3(2 \fprate_0 + 1)]$, which is non-negative iff $\fprate_0 \le 1/4$. So the bound $\le \exp(-2k\fprate_0^2/3)$ holds only for $\fprate_0 \le 1/4$, not $\fprate_0 \le 1/2$. For the worked BPP $\fprate_0 = 1/6$ the bound is valid (since $1/6 < 1/4$); the final coefficient $108 \ln(1/\delta)$ and the $k \approx 1492$ at $\delta = 10^{-6}$ are correct. The reader who applies the bound at, say, $\fprate_0 = 1/3$ gets an invalid inequality. Tighten the stated range to $\fprate_0 \le 1/4$.
- **MAJOR** §11 ex 11-5 lines 110-126 (`chapters/ch11/exercises.tex`): the binary KL divergence claim "$D(1/2 \| 1/3) = (1/2) \log_2(3/2) + (1/2) \log_2(3) \approx 0.0817$ in natural-log units" has two errors. First, the symbolic expression $(1/2) \log_2(3/2) + (1/2) \log_2(3)$ does not correspond to the binary KL: the correct binary KL is $D(p \| q) = p \log(p/q) + (1-p) \log((1-p)/(1-q))$, giving $D(1/2 \| 1/3) = (1/2) \log(3/2) + (1/2) \log(3/4)$ (the second term has $3/4$, not $3$, since $(1 - 1/2)/(1 - 1/3) = (1/2)/(2/3) = 3/4$). Second, the numeric value $0.0817$ matches neither expression: the correct value is $0.0589$ in natural-log units or $0.0850$ in $\log_2$ units. The exercise's coarser Hoeffding form $\exp(-k/18)$ that drives the final answer $k \approx 125$ is correct (additive Hoeffding for mean-deviation $1/6$ gives $\exp(-2k/36) = \exp(-k/18)$, and $k \ge 10 \cdot 18 \cdot \ln 2 \approx 124.8$), so the headline value is right; only the intermediate KL expression and its claimed numeric value are wrong.
- **MAJOR** §11.4 lines 109-117 (proof sketch): "the constant $1/3$ is the value that makes the inequality tight at $\epsilon = 1$." This is wrong. At $\epsilon = 1$, $\phi(1) = 2 \ln 2 - 1 \approx 0.3863$, not $1/3 \approx 0.3333$. The constant $1/3$ is a clean lower bound on $\phi(\epsilon)/\epsilon^2$ over $(0, 1]$; the tightness point is $\epsilon \approx 1.82$ where $\phi(\epsilon)/\epsilon^2 = 1/3$ from below; on $(0, 1]$, the ratio $\phi(\epsilon)/\epsilon^2$ stays at or above $0.3863$. So the bound is correct but the explanation of why $1/3$ was chosen is wrong. A correct rationale: $1/3$ is the standard textbook constant for $\phi(\epsilon) \ge \epsilon^2 / 3$ valid on $(0, 1]$ (e.g., Mitzenmacher-Upfal); the constant is not tight at any specific $\epsilon$ in $(0, 1]$ but is the largest constant of this clean form that yields a valid bound on the full interval.
- **MINOR** §11.4 line 184-185 (BPP amplification setup): "Let $A$ be a BPP algorithm with per-run accuracy bounded by $1/2 + \epsilon_0$ on every input, where $\epsilon_0 > 0$ is the margin above the $1/2$ threshold." The notation $\epsilon_0$ for the BPP margin is introduced and used through line 209. But §11.4 line 199 then defines $\epsilon' = \epsilon_0 / (1/2 + \epsilon_0)$, using $\epsilon'$ as the multiplicative-deviation parameter. The reader has to track three meanings of $\epsilon$: the Chernoff parameter, the BPP margin $\epsilon_0$, and the rescaled $\epsilon'$. Consider renaming one of these (e.g., $\gamma$ for the BPP margin) to disambiguate.
- **MINOR** §11.3 lines 89-90 ("The constant $1/2$ in the first line is conventional; any constant in $(0, 1)$ would give the same class by amplification"): this is correct but the qualifier "by amplification" is forward-referencing §11.3 \Cref{thm:rp-amplification}. The reader who reads §11.3 linearly encounters this claim before seeing the theorem. A pointer "(see \Cref{thm:rp-amplification} below)" would close the loop.
- **MINOR** §11.3 line 145 ("On every input, at least one of the two algorithms is allowed to be definite on a random fraction $\ge 1/2$ of its coin sequences"): the proof of $\mathrm{ZPP} = \mathrm{RP} \cap \mathrm{coRP}$ here sketches the right idea but glosses over which of $A_+$ and $A_-$ is definite at a given coin sequence. The argument is: if $x \in L$, $A_+$ accepts on $\ge 1/2$ of coins (so on $\ge 1/2$ of coin sequences $A_+$ is definite); if $x \notin L$, $A_-$ rejects on $\ge 1/2$. So at every input, one of the two has definite-output probability $\ge 1/2$, and the expected wait time is $\le 2$. The current prose is a bit telegraphic; a sentence naming which algorithm is definite in which case would help.
- **MINOR** §11.4 line 226 (loose constant): "the constant $108$ looks large; in practice the proof can be tightened by using \eqref{eq:chernoff-lower} with its better $\mu \epsilon^2 / 2$ exponent throughout and the per-step inequalities at their tightest, which trims the constant to single digits." The actual exact bound from the lower-tail Chernoff is $\exp(-k\fprate_0^2/[2(1/2+\fprate_0)]) = \exp(-k/8)$ at $\fprate_0 = 1/6$ for the BPP case (no loosening), giving $k \ge 8 \ln(1/\delta) / \fprate_0^2$, which at $\fprate_0 = 1/6$ is $k \ge 8 \cdot 36 \ln(1/\delta) = 288 \ln(1/\delta)$. Wait, this is actually larger than 108, not smaller. (Re-check: the bound $\exp(-k\fprate_0^2/[2(1/2+\fprate_0)])$ at $\fprate_0=1/6$ has exponent $k/48$, so $k \ge 48 \ln(1/\delta)$.) The single-digit tightening claim seems to refer to a different (Hoeffding-style) bound, not the Chernoff path. Clarify which path leads to the single-digit constant.
- **MINOR** §11 ex 11-3 (line 71): the exercise asks the reader to identify the smallest complexity class containing each of \textsc{Compositeness}, \textsc{Primes}, and \textsc{BipartiteMatchingExists}. The answer for \textsc{Primes} via Miller-Rabin is actually RP (Miller-Rabin gives a coRP algorithm for \textsc{Compositeness}, equivalently RP for \textsc{Primes}). But the deterministic AKS algorithm of 2002 places \textsc{Primes} in P, which is strictly smaller than RP. The exercise solution should note this distinction: "via Miller-Rabin alone, RP; with AKS, P."
- **NOTE** §11.5 (`chapters/ch11/bridge.tex`): the bridge correctly summarizes the four sections as one $\Bernoulli{\BoolType}$ arc. The hand-off to chapter 12 (relations) and chapter 13 (type algebra) is appropriate. No issues.
- **NOTE** §11.1 lines 23-29 (introductory paragraph): the sentence "The exposition there was deliberately informal in one specific respect: the per-round bound $\fprate \le 1/4$ was stated as a fact about strong-liar sets and then applied. The number-theoretic origin of that bound was acknowledged but deferred. This section closes the deferral." This is the correct framing of the §3.4-to-§11.1 transition, and is exactly what the spec called for.

### Chapter 12: Approximate Relations (~17 pp; target ~22 pp)

**spec-auditor:** all five sections present per spec §4 chapter 12 row.
§12.1 from approximate sets to relations (the pair-universe lift); §12.2
composition of approximate relations (natural join, projection,
selection) with the headline join theorem $\fprate_{\bowtie} = \fprate_1
\fprate_2$ for FNR-zero inputs; §12.3 approximate joins in databases
(MinHash-LSH similarity join); §12.4 bridge; §12.5 bibliographic notes.
11 exercises with 3/5/3 distribution. Chapter is at ~17 pp, significantly
under the spec's 22 pp target (-23%); §12.4 bridge is one paragraph
shorter than its siblings, and §12.1 could be expanded with the chapter 9
binary-function lens explicitly worked out.

**quality-auditor (cold read):** §12.1 reads cleanly. The classical
correspondence between a relation and its membership predicate is the
right entry point, and the chapter 5 framework lifts to relations
mechanically. §12.2 derives the join, projection, and selection rules
with the right level of detail. The projection-inflation observation (a
projection over a $|U|$-cardinality second attribute inflates $\fprate$
to $1 - (1 - \fprate)^{|U|}$) is the most useful pedagogical point in
the section and is the price of the lift to relations. §12.3 instantiates
the framework on MinHash-LSH with substantial numerical detail,
recovering the chapter 10 sketch construction as one implementation of
the §12.2 framework.

**math-auditor:** verified all numerical claims. §12.2 worked example
friend-and-coworker: $\fprate_{\bowtie} = 0.05 \cdot 0.02 = 0.001$ as
stated. §12.3 worked example: per-pair Hoeffding at $J = 0.3, \theta =
0.5, k = 200$ gives $\exp(-2 \cdot 200 \cdot 0.2^2) = \exp(-16) \approx
1.1 \times 10^{-7}$ as stated. LSH band rates at $(b, r) = (20, 10)$
for $J = 0.7, 0.5, 0.3$: $J^{10}$ values $0.0282, 9.77 \times 10^{-4},
5.90 \times 10^{-6}$, $(1 - J^{10})^{20}$ values $0.564, 0.981, 0.9999$,
LSH-pass probabilities $0.436, 0.019, 0.000118$ all check (text claims
$0.434, 0.019, 1.2 \times 10^{-4}$). Candidate-set total $1000 \cdot
0.434 + 10000 \cdot 0.019 + 989000 \cdot 1.2 \times 10^{-4} \approx 434 +
190 + 119 = 743$ as stated. §12 ex 12-2 projection FPR at $\fprate = 0.01,
|U| = 100$: $1 - 0.99^{100} = 0.6340$ as stated. §12 ex 12-6 three-way
join at $\fprate_i = 0.05$: $0.05^3 = 1.25 \times 10^{-4}$ as stated.
§12 ex 12-8 AND with two FNR-zero inputs: $0.01 \cdot 0.05 = 5 \times
10^{-4}$ as stated. §12 ex 12-7 LSH parameter sweep at $r = 4, b = 30$:
$0.85^4 \approx 0.522$, recall $1 - (1-0.522)^{30} \approx 1.000$,
precision-side bound $1 - (1-0.0915)^{30} \approx 0.944$ all check. At
$r = 8, b = 10$: recall $\approx 0.959$ (text claims $0.957$),
precision-side $\approx 0.081$ (text claims $0.082$) check.

**cross-ref-auditor:** all DEFINED labels match declarations; no
collisions. All RESOLVED labels exist. The §12.2 reference to
`prop:intersection-fpr-fnr` (chapter 6 §6.2) resolves correctly. The
header comment block in `ch12/exercises.tex` mentions
`sec:entropy-lower-bound` as a label used in ex 12-9, but the body uses
the prose form "Chapter~8 \S8.3" instead; the actual label in chapter 8
is `sec:entropy-floor`, not `sec:entropy-lower-bound`. This is a
documentation discrepancy in the header but not an actual bug.

#### Findings (chapter 12)

- **MINOR** §12.3 line 222-224 ("the S-curve is steep but not sharp at $\theta = 0.5$ with $(b, r) = (20, 10)$: most truly similar pairs at $J = 0.7$ survive, half of boundary pairs at $J = 0.6$ survive, and very few low-similarity pairs at $J = 0.3$ survive."): the "half of boundary pairs at $J = 0.6$" claim is wrong. At $J = 0.6$, $J^{10} = 0.00605$, $(1 - 0.00605)^{20} \approx 0.886$, LSH-pass probability $\approx 0.114$, that is, about $11\%$, not half. The "half" descriptor would fit $J \approx 0.65$ approximately, not $J = 0.6$. Either change "$J = 0.6$" to a value where LSH-pass is actually $\approx 0.5$ (numerically, the half-pass point is at $J \approx 0.62$ at $(b, r) = (20, 10)$ with $\theta = 0.5$), or change "half" to a more accurate descriptor.
- **MINOR** §12.2 lines 115-124 (proof of `thm:join-rates`): "If exactly one of the two pairs is outside its relation, the join's false-positive probability is $\fprate_1 \fprate_2 \cdot 0 + \fprate_i \cdot 1$ for the offending index; if both are outside, it is $\fprate_1 \fprate_2$." The arithmetic mixes the joint product $\fprate_1 \fprate_2$ with the per-input rate $\fprate_i$ in a way that does not parse cleanly. The intended argument: for the join to falsely report $\top$ on a non-join triple, both noisy relations must report $\top$; if pair $(t, u) \notin R_1$ but $(u, v) \in R_2$, the probability that both report $\top$ is $\fprate_1 \cdot 1 = \fprate_1$ (since $R_2$ correctly reports $\top$ on $(u, v) \in R_2$). The conditional rate "given the triple is not in the join" is then $\fprate_1$, $\fprate_2$, or $\fprate_1 \fprate_2$ depending on which case. The clean statement is: under the conditioning that the triple is not in the join, the relevant per-input truth values are fixed, so the join's conditional rate is the product of the per-input rates restricted to the noisy stages. The current prose phrasing is a bit confusing; a cleaner derivation by case analysis on which pairs are out-of-relation would help.
- **MINOR** §12.2 line 60-65 (cross-relation independence): the "cross-relation independence" assumption is named in the proof of `thm:join-rates` but is not stated as a formal hypothesis. The chapter 6 framework introduces a cross-structure independence assumption (§6.1 line 154 in Part II review baseline), and the relation lift uses the same assumption. A formal statement "Assume $\tilde R_1$ and $\tilde R_2$ have mutually independent per-query randomness (the cross-relation analog of chapter 6's cross-structure independence)" would tighten the theorem.
- **MINOR** §12.3 lines 162-173 ("FPR and FNR for the join classifier"): the analysis splits the pipeline error into per-pair MinHash and LSH-layer components, but does not give a clean closed-form aggregate. The chapter 7 PPV framework would let one combine the per-pair rate and the workload prevalence (here, the corpus's distribution of true Jaccard similarities) into a single pipeline classifier rate. A pointer to chapter 7 §7.4 would close this loop.
- **MINOR** §12.5 line 30 (bibliographic notes): the reference to `\textcite{towell-bernoulli-relations}` is the right primary source; the §12.5 prose says "the chapter compresses that manuscript into three sections by reading its rate calculations as the chapter~5 and chapter~6 frameworks specialized to pairs rather than as standalone derivations." This is correct framing, but the prose runs long; consider trimming to two sentences for tighter pedagogy.
- **NOTE** §12.4 bridge (`chapters/ch12/bridge.tex`): the bridge correctly summarizes §12.1-§12.3 and previews chapter 13. The pacing is consistent with chapter 10's bridge. No issues.

### Chapter 13: The Algebra of Approximate Types (~16 pp; target ~20 pp)

**spec-auditor:** all five sections present per spec §4 chapter 13 row.
§13.1 algebraic types recap (four constructors: product, sum, list,
function); §13.2 $\Bernoulli{T}$ for composite $T$ (the four
type-constructor rules); §13.3 the composition functor (the four-row
table as one structure-preserving map); §13.4 closing Part III (recap of
the three parts so far, forward to Parts IV and V); §13.5 bibliographic
notes. 11 exercises with 3/5/3 distribution. Chapter is at ~16 pp,
significantly under the spec's 20 pp target (-20%). The theory chapter
designation (no notebook per spec §3.5) is honored.

**quality-auditor (cold read):** §13.1 establishes the four type
constructors with a one-paragraph definition each and walks through how
the prior chapters' structures each instantiate one. §13.2 then derives
the lift on each constructor, with the product-type Kronecker
isomorphism `thm:bernoulli-product` as the headline. §13.3 packages the
four cases as a single structure-preserving map and identifies it as a
functor (with the term itself deferred to bibliographic notes). §13.4
closes Part III with the recap of how each of the three parts
specialized the framework. The chapter delivers the unification promise
of the spec's success criterion 2.

**math-auditor:** verified that the four type-constructor rules in §13.2
are internally consistent with chapters 4 and 9. The product-type
Kronecker formula $(Q_T \otimes Q_U)_{(j_T, j_U), (\ell_T, \ell_U)} =
(Q_T)_{j_T, \ell_T} \cdot (Q_U)_{j_U, \ell_U}$ is the standard Kronecker
definition, matching chapter 4 \Cref{thm:kronecker} and chapter 9
\Cref{thm:n-ary-kronecker}. The sum-type direct-sum formula
$\Bernoulli{T + U} \cong \Bernoulli{T} \oplus \Bernoulli{U}$ is
block-diagonal with $Q_T$ in upper-left and $Q_U$ in lower-right, which
is the standard tag-preserving sum. The list-type and function-type
rules are derived from the product and sum rules respectively. The
worked example with the labeled classifier (3-class label $\times$
$\mathbb{N}$ count) correctly applies the product rule.

**cross-ref-auditor:** all DEFINED labels match declarations; no
collisions. All RESOLVED labels exist. Forward references to Part IV/V
chapters (`ch:optimal-bernoulli-sets`, `ch:perfect-hash-filters`,
`ch:not-bernoulli`) all resolve via Plan 0 stubs.

#### Findings (chapter 13)

- **MAJOR** §13 ex 13-1 lines 40-53 (`chapters/ch13/exercises.tex`): the exercise writes the Bernoulli[Bool] matrix as
  ```
  Q_1 = [[1 - fpr_1, fpr_1], [fnr_1, 1 - fnr_1]]
  ```
  and claims that the Kronecker product's $(\top, \top) \to (\top, \top)$ entry equals $(1-\fnrate_1)(1-\fnrate_2)$. But the canonical Bernoulli[Bool] matrix in chapter 4 \S4.5 (\Cref{def:bernoulli-bool}, lines 51-58) writes
  ```
  Q = [[1 - fnr, fnr], [fpr, 1 - fpr]]
  ```
  with row 1 = $B_1 = \{\top\}$ and column 1 = $\top$. Under that canonical convention, the (1,1) entry is $1 - \fnrate$, so the $(\top, \top) \to (\top, \top)$ entry of $Q_T \otimes Q_U$ is $(1 - \fnrate_1)(1 - \fnrate_2)$, matching the verification claim. But the matrix as ex 13-1 writes it has $1 - \fprate_1$ in the (1,1) position, contradicting the chapter 4 convention. Either fix the matrix to swap the rows so $1 - \fnrate_1$ is in position (1,1) (matching chapter 4), or restate the verification claim as $(1 - \fprate_1)(1 - \fprate_2)$ to match the matrix as written. The chapter 4 convention is the canonical one; recommend fixing the matrix.
- **MAJOR** §13.4 line 35 (`chapters/ch13/closing-part3.tex`): "lifted the binary channel to $k \times k$ channels for finite codomains" uses lowercase $k$ for the model-order, contradicting the chapter 9 \S9.2 convention (lines 123-156) that explicitly fixes $K$ uppercase for model-order to distinguish it from lowercase $k$ used for Bloom hash counts (§5.2) and Miller-Rabin rounds (§3.4). Replace $k \times k$ with $K \times L$ to maintain the notation convention. The §13.2 prose at line 41 uses $(K_T K_U) \times (L_T L_U)$ correctly; the §13.4 closing wording slipped.
- **MAJOR** §13.4 line 59 ("characterized by a $|T| \times |T|$ channel matrix"): an n-ary channel can have $K \ne L$ (different input cardinality and output cardinality), as chapter 9 §9.2 explicitly emphasizes with the "$K = 5, L = 2$ channel" and "$K = \infty, L = \infty$ counter" examples. The "$|T| \times |T|$" presentation assumes domain and codomain are the same type. Correct to "characterized by a $|T| \times |Y|$ channel matrix where $T$ is the input type and $Y$ is the output type", or state more carefully that $T$ here is the domain and the codomain is implicit.
- **MAJOR** §13.2 lines 99-118 (sum types, tag-preserving case): the §13.2 development of $\Bernoulli{T + U} \cong \Bernoulli{T} \oplus \Bernoulli{U}$ assumes the tag is preserved, and the off-diagonal blocks of the block-diagonal channel matrix are zero. This is correct for the tag-preserving case. But the §13.2 prose then says "When the tag itself is noisy (a tag flip occurs with probability $\delta$), the channel matrix gains off-diagonal mass linking $T$-blocks to $U$-outputs and vice versa. The structural form is no longer pure block-diagonal but a sum of the two pure block-diagonal channels weighted by tag-preservation and tag-flip probabilities. We work with the tag-preserving case throughout, returning to tag errors in chapter~16's catalogue of boundary cases." The forward reference to chapter 16 is correct, but the tag-flip case is hard to compose with the type-algebra view: a tag-flipping channel violates the per-summand independence that makes the sum rule clean. The chapter 16 treatment will need to address this, and the §13.2 prose should signpost that the sum rule does *not* extend to the tag-flip case in any natural way (rather than reading as "we treat it later").
- **MINOR** §13 ex 13-2 (line 70-75): part (c) on MinHash says "a noisy similarity estimate in $[0, 1]$ per pair of sets, hence $T = [0, 1]$ for the per-pair estimator (or $T = (U \to \BoolType) \times (U \to \BoolType) \to [0, 1]$ for the full pairwise-similarity table)." The second form $T = (U \to \BoolType) \times (U \to \BoolType) \to [0, 1]$ is correct but reads as a heavy type. The alternative $T = \text{Set}(U) \times \text{Set}(U) \to [0, 1]$ would be cleaner if the chapter had introduced a notation for sets at the type level; the chapter 5 \S5.1 framework names a set as $A \subseteq \Universe$ but does not give a type-level name. Consider adopting $\text{Set}(U) = U \to \BoolType$ as a synonym for readability.
- **MINOR** §13.3 lines 75-85 (the monad mention): "The function row $\Bernoulli{T \to U} \cong T \to \Bernoulli{U}$ is worth pausing on. It says the noisy version of a function is the same as a function returning noisy values. Programmers will recognize this as the signature of a 'monad' in the type-theoretic sense...". The monad mention is appropriate as a forward-pointing pedagogical aside, and §13.5 bibliographic notes correctly defer the formal monad axioms to Wadler 1992. The §13 ex 13-6 then asks the reader to explain informally why $\Bernoulli{-}$ qualifies as a monad. The pedagogical sequence is fine; a single sentence in §13.3 saying "exercise 13-6 walks through the informal argument" would close the loop.
- **MINOR** §13 ex 13-5 (line 144-151) part (c): "the function row $\Bernoulli{T \to U} \cong T \to \Bernoulli{U}$ in both cases, with $U = \BoolType$ for (a) and $U = \mathbb{N}$ for (b)." This is correct (Bloom filter as $\Bernoulli{T \to \BoolType}$ and CountMin/HyperLogLog as $\Bernoulli{T \to \mathbb{N}}$). But the §13 ex 13-2 part (a) gives the same identification for Bloom filter as $T = U \to \BoolType$, raising the question of whether the type-level lift is on the input universe $T$ or on the codomain $\BoolType$. The two formulations $\Bernoulli{T \to \BoolType}$ and $T \to \Bernoulli{\BoolType}$ are by the function-row isomorphism equivalent, but the prose alternates between them; consider standardizing the presentation in exercises.
- **NOTE** §13.5 (`chapters/ch13/bibliographic-notes.tex`): the four paragraphs (manuscript, algebraic data types, categorical reading, where-to-go-for-more) are appropriately concise. The Mac Lane and Wadler references are well-placed.

## Cross-chapter coherence findings

These findings only surface when reading across chapters.

- **MAJOR** Bernoulli[Bool] matrix orientation convention: chapter 4 \S4.5 (\Cref{def:bernoulli-bool}, lines 51-58) writes the canonical matrix as
  ```
  Q = (tprate, fnrate; fprate, tnrate) = (1-fnr, fnr; fpr, 1-fpr)
  ```
  with row 1 = $B_1 = \{\top\}$ and column 1 = $\top$. Chapter 9 \S9.2 example 2 (lines 184-200) uses the same convention with the same labeling. Chapter 13 §13 ex 13-1 (lines 40-53) writes
  ```
  Q = (1 - fpr, fpr; fnr, 1 - fnr)
  ```
  which would only match the canonical convention if row 1 = $B_2 = \{\bot\}$, the opposite ordering. The exercise's verification claim that the $(\top, \top) \to (\top, \top)$ entry equals $(1-\fnrate_1)(1-\fnrate_2)$ further requires the canonical (row 1 = $\top$) ordering, which contradicts the matrix as written. The conflict needs resolution: either ex 13-1's matrix is rewritten in the canonical form, or the exercise's verification claim is restated. This is the same Bernoulli[Bool] type discussed across chapters 1, 4, 9, and 13; consistency of presentation is load-bearing.
- **MAJOR** N-ary channel notation drift (chapters 9 and 13): chapter 9 §9.2 lines 123-156 explicitly establish the convention that the model-order is uppercase $K$ (distinguishing it from lowercase $k$ for hash counts and round counts) and the output cardinality is uppercase $L$. Chapter 13 §13.4 line 35 then writes "$k \times k$ channels for finite codomains" (lowercase $k$, square) and line 59 writes "$|T| \times |T|$ channel matrix" (square, single type). Both formulations contradict §9.2's careful $K \times L$ convention. Fix the §13.4 wording to "$K \times L$ channels" or "$|T| \times |Y|$ channels" to match.
- **MINOR** Cross-chapter LSH discussion: §10.4 (`chapters/ch10/minhash-lsh.tex`) introduces LSH bands at lines 251-300 with the S-curve formula $p(J) = 1 - (1 - J^r)^b$. §12.3 (`chapters/ch12/approximate-joins.tex`) re-derives the same formula at lines 114-136. The two presentations are consistent but somewhat duplicative. §12.3 could compress its LSH description to a one-paragraph forward pointer to §10.4 and focus on the new content (the relation-classifier framing).
- **MINOR** Chapter 11 §11.1 title "Miller-Rabin Formal" vs spec title "Recall Miller-Rabin": the spec's §11.1 row was titled "Recall Miller-Rabin (~3 pp)" but the drafted section is titled "Miller-Rabin Formal" and is ~5 pp. The drafted title is more accurate to the content (which is more than just a recall: it includes the formal statement, the proof sketch citing Rabin 1980, and the explicit comparison to §3.4). The spec's "Recall" framing was a placeholder; the drafted title is the right one.
- **NOTE** Documented deferred cross-refs unchanged: `ch:composition` x 1 (chapter 4 forward ref), `ch:sketches` x 5 (chapter 9 forward refs to chapter 10's `ch:sketches-estimators`), `sec:noisy-bit` x 2 (chapter 17 forward refs to chapter 1). All are baseline-flagged in the build log and not new findings.
- **NOTE** Page budgets vs spec §6 budget table:

| Chapter | Spec §6 target | Estimated current |
|---|---|---|
| Ch 9  | ~26 pp | ~25 pp (-1) |
| Ch 10 | ~28 pp | ~24 pp (-4) |
| Ch 11 | ~24 pp | ~23 pp (-1) |
| Ch 12 | ~22 pp | ~17 pp (-5) |
| Ch 13 | ~20 pp | ~16 pp (-4) |
| Total | ~120 pp | ~105 pp (-15) |

  Chapter 12 and chapter 13 are most under spec; chapter 13's "theory
  chapter" designation in the spec allows tighter writing, and chapter 12
  could absorb additional material (e.g., a section on
  approximate-relation closure properties under union and difference,
  paralleling chapter 6's set-level treatment). Total Part III at ~105 pp
  is below the spec's ~120 pp target by ~12%. Within tolerance for the
  Plans 1-8 pattern that typically came in ~20% over spec, this is the
  first time the pattern reversed and the chapters came in under spec.

- **NOTE** Three running threads carry: the Miller-Rabin thread carries
  from §3.4 informal walkthrough to §11.1 formal restatement; the
  MinHash thread carries from §10.4 construction to §12.3 similarity-join
  application; the n-ary Kronecker theorem carries from §9.3 to §13.2's
  product-type isomorphism. All three threads are substantive returns,
  not just name-drops.

## Recommended next actions

Ordered by priority.

### BLOCKER

(None.)

### MAJOR (should fix before integration sign-off; may defer to a revise pass)

1. **§13 ex 13-1 Bernoulli[Bool] matrix orientation:** rewrite the matrix in ex 13-1 to match the chapter 4 \S4.5 canonical convention ($(1-\fnrate, \fnrate; \fprate, 1-\fprate)$), or restate the verification claim to match the as-written matrix. The chapter 4 canonical form is the standard; recommend fixing the matrix.
2. **§11.4 BPP amplification loosening range:** tighten the stated range "$\fprate_0 \le 1/2$" to the correct "$\fprate_0 \le 1/4$" at lines 196-204. The worked $\fprate_0 = 1/6$ case is valid and the headline $108 \ln(1/\delta)$ coefficient is right, so the BPP example is fine; only the stated range needs correction.
3. **§11 ex 11-5 KL divergence error:** correct the binary KL expression to $D(1/2 \| 1/3) = (1/2) \log_2(3/2) + (1/2) \log_2(3/4) \approx 0.0850$ in $\log_2$ units (or $0.0589$ nat), or remove the KL line and keep only the Hoeffding $\exp(-k/18)$ form that drives the final $k \approx 125$. The final answer is right; only the intermediate KL expression and its claimed numeric value are wrong.
4. **§11.4 line 113-114 Chernoff tightness claim:** rephrase "the constant $1/3$ is the value that makes the inequality tight at $\epsilon = 1$" to a correct statement. $\phi(1) = 2 \ln 2 - 1 \approx 0.386 > 1/3$, so the bound is not tight at $\epsilon = 1$. A correct rationale: $1/3$ is the standard textbook constant for $\phi(\epsilon) \ge \epsilon^2 / 3$ on $(0, 1]$; the bound is loose throughout the interval but tightens to equality at $\epsilon \approx 1.82$ (outside the stated range).
5. **§10 ex 10-11 cross-reference fix:** change `\Cref{sec:ch10-bridge}` to `\Cref{sec:minhash-lsh}` in the exercise opening. LSH is defined in §10.4 (`sec:minhash-lsh`), not §10.5 (`sec:ch10-bridge`).
6. **§13.4 N-ary notation:** replace "$k \times k$ channels" (line 35) and "$|T| \times |T|$ channel matrix" (line 59) with notation matching chapter 9 §9.2's convention ($K \times L$ or $|T| \times |Y|$).
7. **§13.2 sum-type tag-flip caveat:** strengthen the §13.2 prose on the tag-flip case to indicate that the sum rule does *not* extend cleanly to tag-flips, rather than reading as "we treat it later". The chapter 16 forward reference is correct; the §13.2 statement should make clear that the tag-flip case is a *failure* of the four-row algebra, not a future extension of it.

### MINOR (polish-pass additions)

Add to the polish-pass list:

- §9.2 line 178 (symmetric BSC matrix) label as $(1-\fnrate, \fnrate; \fprate, 1-\fprate)$ for cross-chapter consistency, even though symmetric case has $\fprate = \fnrate$.
- §10.3 line 311 (HyperLogLog worked example): qualify the representative register array as "approximate to within the seed".
- §10.4 line 320 (MinHash Hoeffding looseness): quantify the gap between the Hoeffding bound and the exact binomial tail at the worked $J = 0.176, k = 200, \epsilon = 0.05$ point.
- §10.4 lines 159-165 (MinHash streaming/deletion): connect the no-deletion property to the chapter 11 LV/MC trade-off as a pedagogical aside.
- §10.1 add a synoptic table at the chapter opening (sketch | output type | $Q$ structure | composition rule).
- §10.6 add explicit Cormode-Yi citation.
- §11.4 rename $\epsilon_0$ (BPP margin) to $\gamma$ to disambiguate from Chernoff $\epsilon$.
- §11.3 line 89 add forward pointer to `\Cref{thm:rp-amplification}` for the constant-invariance claim.
- §11.3 line 145 (ZPP proof): name which algorithm is definite in which case ($x \in L$ vs $x \notin L$).
- §11.4 line 226 (single-digit tightening claim): clarify which alternative path gives the single-digit constant.
- §11 ex 11-3 (\textsc{Primes} class): note that Miller-Rabin gives RP membership but AKS gives P membership.
- §12.3 line 222 "half of boundary pairs at $J = 0.6$" change to a numerically correct boundary value ($J \approx 0.62$ at the half-pass point).
- §12.2 lines 115-124 (proof of `thm:join-rates`): rewrite the case analysis more cleanly.
- §12.2 line 60-65 formalize cross-relation independence as a hypothesis.
- §12.3 lines 162-173 add pointer to chapter 7 §7.4 PPV framework for the workload-aggregated pipeline rate.
- §12.5 trim the manuscript-context paragraph.
- §13 ex 13-2 part (c) use $\text{Set}(U)$ notation if introduced, otherwise keep heavy type.
- §13.3 add pointer to ex 13-6 from the monad mention.
- §13 ex 13-5 standardize $\Bernoulli{T \to U}$ vs $T \to \Bernoulli{U}$ presentation across the function-row examples.

### NOTE (defer to a future revision or leave as-is)

- §9.5 bridge-to-sketches could add a sketch-comparison table.
- §10.1 the "Why the chapter 9 framework unifies them" subsection's three sketch-by-sketch summaries.
- §10.6 bibliographic notes appropriately concise.
- §12.4 bridge appropriately compact.
- §13.5 bibliographic notes well-organized.
- Chapter 9 §9.6 bibliographic notes well-cited.
- Chapter 11 §11.5 bridge clean.
- Chapter 11 §11.1 vs spec title difference (Miller-Rabin Formal vs Recall Miller-Rabin) is a content-driven retitling, not a spec violation.
- Cross-chapter LSH duplication between §10.4 and §12.3 could be compressed but works as is.
- Chapter 12 and chapter 13 are under spec but within tolerance.
- Documented deferred cross-refs unchanged.

## Specialist verdicts (consolidated)

- **spec-auditor:** Part III PASS. All content checklist items from
  spec §4 chapters 9-13 are realized. The Miller-Rabin thread carries
  from §3.4 to §11.1, the MinHash thread carries from §10.4 to §12.3,
  and the n-ary Kronecker theorem carries from §9.3 to §13.2. The §11.1
  formal restatement of Miller-Rabin retires the chapter 3 §3.4 deferral
  cleanly (success criterion 3). The §13.3 four-row composition-functor
  table delivers the unification of Part II's set composition, chapter
  10's sketches, and chapter 12's relations under one type-driven
  algebra (success criterion 2).
- **quality-auditor:** "minor polish needed" overall. No chapter
  requires substantive revision. Chapter 11 carries the heaviest
  revision load (3 MAJORs: the §11.4 loosening-range claim, the §11 ex
  11-5 KL value, the §11.4 Chernoff tightness wording). Chapter 13's
  ex 13-1 Bernoulli[Bool] matrix and §13.4's notation drift are the
  next two MAJORs. Chapters 9, 10, 12 are nearly publication-ready
  with only minor polish.
- **math-auditor:** PASS with corrections. Every numerical claim
  checked verifies independently except the §11 ex 11-5 KL value (which
  is wrong as stated; the headline $k \approx 125$ from the Hoeffding
  form is right). The §9.3 worked example (joint $(1,2,1)$ given
  $(B_1, B_2, B_1)$ = $0.729$), the §9.4 strongly-symmetric capacity
  ($C \approx 1.373$ at $L = 4, p_e = 0.1$), the §10.2 CountMin bound
  ($w = 10, d = 5$ giving $\epsilon \le 0.272, \delta \le 0.00674$),
  the §10.3 HyperLogLog standard error ($1.04/\sqrt{m}$ at $m = 256$
  giving $6.5\%$), the §10.4 MinHash variance and Hoeffding bound
  (variance $J(1-J)/k$ at the worked $J = 0.176, k = 200$ gives SE
  $0.027$ and Hoeffding $2/e \approx 0.736$), the §11.1 Miller-Rabin
  composition ($(1/4)^k$ giving $k = 10$ for $\delta = 10^{-6}$ and
  $k = 20$ for $\delta = 10^{-12}$), the §11.4 Chernoff applied to BPP
  ($108 \ln(1/\delta)$ giving $k \approx 1492$ for $\fprate_0 = 1/6,
  \delta = 10^{-6}$), and the §12.3 MinHash-LSH worked example (per-
  pair $\exp(-16) \approx 1.1 \times 10^{-7}$, LSH-pass probabilities
  $0.434, 0.019, 1.2 \times 10^{-4}$, candidate-set total $\approx 743$)
  all verify exactly.
- **cross-ref-auditor:** PASS with one correction (§10 ex 10-11 wrong
  cross-reference: `sec:ch10-bridge` should be `sec:minhash-lsh`). All
  DEFINED labels match declarations; no collisions. All RESOLVED labels
  exist (`def:bernoulli-bool`, `thm:kronecker`, `cor:parameter-reduction`,
  `ax:element-indep`, `ax:block-rates-indep`, `def:bsc`,
  `def:asymmetric-channel`, `def:model-order`, `thm:boolean-ceiling`,
  `prop:bsc-capacity`, `sec:entropy-refresher`, `sec:bloom-from-scratch`,
  `sec:miller-rabin`, `def:perfect-filter-line`, `def:ppv`, `def:npv`,
  `sec:binomial-estimator`, `prop:binomial-unbiased`,
  `prop:binomial-variance`, `prop:intersection-fpr-fnr`,
  `thm:entropy-floor`, `def:minhash`, `prop:minhash-collision`,
  `prop:minhash-error`, `def:bloom-filter`, plus the Part IV/V
  chapter-level stubs `ch:optimal-bernoulli-sets`,
  `ch:perfect-hash-filters`, `ch:not-bernoulli`). Two header
  comment-block staleness issues (`ch10/bibliographic-notes.tex` uses
  `ch:type-algebra` in a comment-only line; actual label is
  `ch:algebra-types`; `ch12/exercises.tex` uses `sec:entropy-lower-bound`
  in a comment-only line; actual label is `sec:entropy-floor` and body
  uses prose form). The three documented deferred items (`ch:composition`,
  `ch:sketches` x 5, `sec:noisy-bit` x 2) match the build log exactly.

## Overall recommendation

Part III is in solid shape. There are no BLOCKERs. The seven MAJOR
findings cluster around chapter 11's sample-complexity derivation (the
range of validity, the KL value, the tightness claim) and chapter 13's
type-algebra exposition (the Bernoulli[Bool] matrix orientation in ex
13-1, the n-ary channel notation drift in §13.4, the sum-type tag-flip
caveat in §13.2). The §10 ex 10-11 cross-reference fix is mechanical.
The 15 MINOR findings are appropriate polish-pass material; the 10 NOTE
items are deferrals.

The chapter 11 MAJORs are all in the sample-complexity section's fine
print: the worked BPP and Miller-Rabin examples themselves are right,
and the headline values $k = 10, 20$ rounds (Miller-Rabin) and $k
\approx 1492$ (BPP at $\delta = 10^{-6}$) all check. The chapter 13
MAJORs are also in the fine print: the matrix orientation in ex 13-1
trips a careful reader cross-referencing with chapter 4, and the §13.4
closing notation drifts away from the chapter 9 convention.

The chapters' pedagogical voice is consistent across all five. The
Miller-Rabin thread closing the §3.4 deferral, the MinHash thread
carrying from §10.4 to §12.3, and the n-ary Kronecker theorem carrying
from §9.3 to §13.2 are the three substantive Part III demonstrations of
the running-example device. The §11.1 formal Miller-Rabin and the §13.3
four-row composition-functor table are the Part III climaxes the spec
called for, and both land.

Recommend: schedule the seven MAJORs for a focused revision pass on the
chapter 11 sample-complexity section (3 findings), the chapter 13
ex 13-1 matrix and §13.4 notation (2 findings), the §10 ex 10-11
cross-reference fix (1 finding), and the §13.2 sum-type tag-flip
caveat (1 finding). Queue the 15 MINORs for a polish pass before
Milestone 1.
