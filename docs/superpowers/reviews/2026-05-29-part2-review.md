# Part II Review (chapters 5-8)

Date: 2026-05-29
Reviewer: bookwright reviewer orchestrator (Part II scope)
Auditors applied: spec, quality, math, cross-ref (per-chapter, inline)

This review evaluates all four chapters of Part II ("From Bits to Sets")
of *Bernoulli Types: An Algebra of Approximate Computation* against the
Part II design spec
(`docs/superpowers/specs/2026-05-17-bernoulli-textbook-part2-design.md`)
and the master spec
(`docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`). The
four auditor roles were applied per chapter and the findings are
synthesized below by chapter and by cross-chapter coherence. The
documented deferred items (`ch:composition` x 1, `ch:sketches` x 5,
`sec:noisy-bit` x 2) match `book/book.log` exactly and are not flagged.

## Summary

- **Total findings: 34** (0 BLOCKERs, 6 MAJORs, 17 MINORs, 11 NOTEs).
- **Top high-priority items:**
  1. (MAJOR) §6.3 Proposition `prop:mixed-intersection-escape` is internally inconsistent. The proposition's title says "Mixed-axis intersection escapes the line", and the proof's last sentence says "In neither case does the result fall on the FNR-zero or FPR-zero axis of the operands." The proposition's own boundary regime gives the result $(0, \fnrate_B)$, which sits on the FPR-zero axis (B's axis), so it remains on the line. The §6.3 worked example at lines 155-156 makes the contradiction explicit: "The composition has landed at $(0, 0.02)$ on the FPR-zero axis." The proposition should distinguish "leaves the FNR-zero axis but lands on the FPR-zero axis" (boundary, line preserved as a whole) from "leaves the line entirely" (non-boundary, two-sided).
  2. (MAJOR) §6.4 Proposition `prop:fnr-zero-closure` part (4): the hypothesis of the proposition is that $\ASet{A}, \ASet{B}$ are FNR-zero (so $\fnrate_A = \fnrate_B = 0$). Part (4) then adds "$\ASet{B}$ is in addition FPR-zero (so $\fprate_B = 0$ also)". By the chapter 5 `def:one-sided` definition, FPR-zero requires $\fnrate > 0$; combining both forces $\ASet{B}$ to have both rates zero, which is the exact set and is excluded from the approximate-set framework. The proof itself ("$\ASet{A} \setminus \ASet{B}$ reduces to an exact-set test") confirms this is the degenerate case. Part (4) as stated only applies to vacuous instances; the substantive content "the difference of two FNR-zero sets generically leaves the line" lives only in the "otherwise" clause and needs to be the main statement, with the exact-set special case as a footnote.
  3. (MAJOR) §6.2 intersection FPR derivation is materially incomplete: the proof at lines 119-134 derives $\fprate_A \cdot \fprate_B$ for the regime "$x \notin A$ and $x \notin B$", and explicitly notes "the full intersection FPR mixes this contribution with two boundary regions where $x$ lies in exactly one operand set." But the worked example at lines 257-277 just substitutes $\fprate_A \cdot \fprate_B$ directly without specifying that $\ASet{A}$ and $\ASet{B}$ represent the same objective set. If they represent different sets, the boundary regions contribute terms like $(1 - \fnrate_A) \cdot \fprate_B$ which equals $\fprate_B$ when $\fnrate_A = 0$, so the intersection FPR can be substantially larger than $\fprate_A \cdot \fprate_B$. Either the worked example needs to assume $A = B$ explicitly, or the formula needs the full mixture form. This issue propagates: §8 ex 11 cites the same formula and §7.4 line 305 ("the multiplicative shape matters") leans on the simplified form.
- **Chapters with most findings:** Chapter 6 (12), Chapter 7 (8), Chapter 5 (7), Chapter 8 (7).

Overall the chapters are in solid shape. Every numerical claim verified
independently with Python checks (Bloom optimal-k formula, FPR table,
9.6n bits at FPR=0.01, $\log_2 e \approx 1.4427$ overhead, union/intersection
worked examples, F1 delta-method variance 7.02e-4 and CI [0.714, 0.818],
Bloom diagnostic PPV 0.9158 with CI [0.900, 0.932]). The two Part II
climaxes (§5.2 Bloom-filter-from-scratch derivation and §8.3 entropy
floor theorem) both land. The Bloom-filter running thread carries from
§5.2 to §6.1 (union worked example), §6.2 (intersection worked example),
§7.4 (Bloom PPV under workload), §7.5 (diagnostic application), §8.3
(floor table), and §8.4 (gap). The §1.4 deferral is cleanly retired in
§7.1-§7.4. The Wilson, Clopper-Pearson, and Jeffreys CIs are all
correctly derived. No em-dashes (U+2014). No "easy to see", "obviously",
or other handwaves. No banned phrases.

The findings below are sorted by severity within each chapter, then by
location.

## Findings by chapter

### Chapter 5: Approximate Sets and Predicates (~27 pp; target ~28 pp)

**spec-auditor:** all checklist items per spec §4 chapter 5 row are
realized. Six sections (§5.1 From Atom to Set, §5.2 Bloom Filter, §5.3
Predicate Algebra, §5.4 One-Sided vs Two-Sided, §5.5 What Comes Next,
§5.6 Bibliographic Notes). Learning outcomes box has three bullets per
spec format. 11 exercises with 3/5/3 difficulty distribution. The
$(m, k, n)$ notation note at §5.2 lines 100-112 addresses Open Action
Item 2 of the spec. The optimal-$k$ derivation and the n=1000, m=10000,
k=7 worked example are both present.

**quality-auditor (cold read):** reads cleanly. The §5.1 atom-to-set
predicate framing earns the abstraction (the "function from universe to
the noisy-bit atom of Part I" framing comes through). The §5.2 Bloom
filter derivation is detailed enough to reproduce on paper. The
notation-note paragraph in §5.2 is the right move. §5.4 articulates
the one-sided / two-sided distinction cleanly.

**math-auditor:** verified all numerical claims independently. $k^*=
(m/n)\ln 2 = 6.931$ for $m=10000, n=1000$ rounds to 7. FPR table at
k=5,6,7,8,9 (0.00943, 0.00844, 0.00819, 0.00846, 0.00913) matches
exactly. The optimal FPR at $k=7$ is $\approx 0.0082$ via
$(1-e^{-0.7})^7 = 0.5034^7$. The off-optimum k=20 calculation gives
0.0546 as stated. §5.4's $9.6n$ bit formula at FPR=0.01 verifies:
$\log_2(100)/\ln 2 = 9.585$.

**cross-ref-auditor:** all DEFINED labels match `\label{}` declarations.
All RESOLVED labels exist in the book tree (`prop:stable-Q`,
`def:bernoulli-bool`, `thm:kronecker`, `ax:element-indep`,
`ax:block-rates-indep`, `sec:bsc`, `sec:bridge-to-sets`,
`ch:perfect-hash-filters`, `ch:optimal-bernoulli-sets` all check). No
label collisions. Header comment-block accuracy issue in §5.3 (see
findings).

#### Findings (chapter 5)

- **MINOR** §5.1 header comment block (`from-atom-to-set.tex` lines 20-22): the FORWARD REFS list mentions only `\Cref{sec:bloom-from-scratch}` and `\Cref{sec:predicate-algebra}` (Tasks 3 and 4), but the body at line 189 uses `\Cref{sec:one-sided-two-sided}` (§5.4, Task 5). The forward ref is functional (the label resolves), but the header is incomplete. Add `\Cref{sec:one-sided-two-sided}` to the FORWARD list.
- **MINOR** §5.3 header comment block (`predicate-algebra.tex` lines 10-25): the RESOLVED list does not include `\Cref{prop:stable-Q}`, but the body uses it twice (lines 102, 133). Either add `\Cref{prop:stable-Q}` (chapter 4 §4.3) to RESOLVED or remove the body uses. The proposition is correctly defined in chapter 4 at line 144 of `book/chapters/ch04/axiom-2.tex`, so this is a header-staleness issue only.
- **MINOR** §5.2 line 195 (`bloom-from-scratch.tex`): "the approximation \eqref{eq:bloom-fpr} is an under-estimate". The §5.2 notes the bit-check independence assumption produces "$\eqref{eq:bloom-fpr}$ is an under-estimate", but the practical magnitude of the deviation is not quantified except by reference to exercise 7. A one-line numerical anchor ("the deviation at $m=4, n=1, k=2$ is approximately 2% above the formula") would help.
- **MINOR** §5.2 line 311 ("$k^* = 10 \ln 2 \approx 6.93$"): the value 6.93 rounds to 7, but the FPR table at lines 322-333 has the row labeled $k=7$ giving FPR $\approx 0.00819$, while the closing prose at line 315 gives $(1/2)^7 = 1/128 \approx 0.0078$. The two numbers ($0.00819$ and $0.0078$) refer to two different formulas (the exact $(1 - e^{-kn/m})^k$ approximation and the half-occupancy asymptotic $(1/2)^k$), but the text doesn't say so. A clarifying sentence ("the exact formula gives $0.00819$; the half-occupancy approximation gives $0.0078$; the agreement is to two significant figures") would close the loop.
- **MINOR** §5.4 line 130 ("$\log_2(100) / \ln 2 \approx 9.58$"): the value $9.58$ is correct but the prose then says "$\approx 9.6 \, n$ bits". Choose one precision throughout; the chapter 8 table at line 219 uses $9.59$, so $9.6$ rounds up by one decimal. Standardize.
- **NOTE** §5.5 line 90 ("$\log_2 e \cdot \log_2(1/\fprate) \approx 1.44 \log_2(1/\fprate)$"): the previewing of the chapter 8 result is clean, but the §5.4 footnote at line 130 already gave the $9.6n / 6.64n = 1.44$ ratio explicitly. The repetition reads slightly redundant; one of the two could compress to a forward reference.
- **NOTE** §5.6 line 39 (`bibliographic-notes.tex`): the §5.6 framing of "the Bloom filter as a particular construction of a function $\Universe \to \Bernoulli{\BoolType}$" is well-stated. Consider promoting one sentence into the §5.1 introduction (currently the section opens with a "Why is the construction inevitable?" rhetorical question; the bibliographic-notes contribution claim could move forward).

### Chapter 6: Composition of Sets (~25 pp; target ~24 pp)

**spec-auditor:** all six sections present per spec §4 chapter 6 row.
§6.1 union with FPR derivation; §6.2 intersection, complement,
difference; §6.3 cancellation; §6.4 perfect filter line as algebraic
subalgebra; §6.5 what comes next; §6.6 bibliographic notes. 11
exercises with 3/5/3 distribution. The §6.1 distinction between
predicate-OR (the rate formula) and bit-OR-Bloom (the structural
shortcut with different rates) is the most useful pedagogical
contribution and is well placed.

**quality-auditor (cold read):** §6.1 reads cleanly. The §6.2
multi-operation walkthrough (intersection, complement, difference) is
compact. §6.3's three-class categorization (axis-preserving,
axis-swapping, axis-leaving) is the chapter's organizing observation.
§6.4 closes the algebra cleanly. The §6.6 bibliographic notes are
appropriately concise.

**math-auditor:** verified all numerical claims. Union FPR $0.0298$
from $\fprate_A=0.01, \fprate_B=0.02$ via $1 - (1-0.01)(1-0.02) =
0.0298$ checks. Intersection FPR $0.0002$ from $0.01 \cdot 0.02$
checks. Complement-swap arithmetic checks. The §6.1 bit-OR-Bloom worked
example computation at lines 115-120 ($\fprate \approx 0.137$ for
$m=5000, k=7, n_A=n_B=500$) verifies via $(1 - e^{-7 \cdot 1000 /
5000})^7 = 0.1378$. The §6.3 two-sided B example $\fprate_{\cap} =
0.01 \cdot 0.005 = 5 \times 10^{-5}$ and $\fnrate_{\cap} = 0.02$ both
check.

**cross-ref-auditor:** all DEFINED labels match declarations; no
collisions. All RESOLVED labels exist. The chapter has the most
forward references of Part II (chapters 7, 8, 14, 15), all chapter-level
labels that exist via Plan 0 stubs.

#### Findings (chapter 6)

- **MAJOR** §6.3 lines 182-201 (Proposition 6.3.2 `prop:mixed-intersection-escape`): the proposition's title is "Mixed-axis intersection escapes the line" and the proof concludes "In neither case does the result fall on the FNR-zero or FPR-zero axis of the operands." But the boundary regime gives $\fprate_\cap = 0, \fnrate_\cap = \fnrate_B > 0$, which is a point on the FPR-zero axis (the operand B's axis). It lies on the perfect filter line $\mathcal{L} = \mathcal{L}_\fnrate \cup \mathcal{L}_\fprate$. The §6.3 worked example at lines 155-156 explicitly confirms this: "The composition has landed at $(0, 0.02)$ on the FPR-zero axis in this specific arithmetic". So the proposition's conclusion is wrong (or its scope is wrong). The corrected statement should be: "the composition leaves the FNR-zero axis but lands on the FPR-zero axis in the boundary regime; in the non-boundary regime where $\fprate_B > 0$, the composition leaves the line entirely." The proof's last sentence needs to be rewritten to match.
- **MAJOR** §6.2 intersection FPR worked example (lines 257-277): the §6.2 proof at lines 119-134 explicitly notes "the full intersection FPR mixes this contribution with two boundary regions where $x$ lies in exactly one operand set", but the worked example then computes $\fprate_\cap = 0.01 \cdot 0.02 = 0.0002$ as if no boundary regions exist. The simplification is exact only when the two operand sets coincide on the negatives of the intersection (i.e., when $A = B$). The worked example does not specify this, so a reader could conclude that intersection FPR is always the product when in general it isn't. Either add "assuming $\ASet{A}$ and $\ASet{B}$ approximate the same objective set $A = B$" to the worked example, or write the full mixture formula and specialize. The §6.2 line 132 "the simplified form is exact when the two operand sets coincide on the negatives of the intersection" hint helps but is buried in a paragraph the reader who skips to the worked example will not see.
- **MAJOR** §6.4 Proposition 6.4.1 part (4) `prop:fnr-zero-closure`: the hypothesis is "$\ASet{A}$ and $\ASet{B}$ are FNR-zero". Part (4) then adds "$\ASet{B}$ is in addition FPR-zero (so $\fprate_B = 0$ also)". By `def:one-sided`, an approximate set with both rates zero is excluded. So part (4) as stated has no non-vacuous instances. The proof's last sentence ("$\ASet{A} \setminus \ASet{B}$ reduces to an exact-set test") makes the issue explicit. The substantive part of (4) is the "otherwise" clause: "the difference generically leaves the line". The proposition needs restating so the substantive case is the main statement and the exact-set case is a footnote.
- **MAJOR** §6.1 lines 195-200 (proof of `prop:union-fpr-fnr` FPR): "the two events $\ASet{A}(x) = \top$ (given $x \notin A$) and $\ASet{B}(x) = \top$ (given $x \notin B$) are exactly the per-operand false-positive events at $x$, with conditional probabilities $\fprate_A$ and $\fprate_B$ respectively." This step silently uses the independence assumption stated at line 154 ("the error events of $\ASet{A}$ and $\ASet{B}$ at every query point $x \in \Universe$ are mutually independent") but the proof doesn't cite the assumption back at the multiplication step. One sentence linking the assumption to the multiplication ("By the cross-set independence assumption stated above...") would close the loop. Exercise `ex:ch6-7` explicitly probes this independence; the proof should anchor the same point.
- **MINOR** §6.1 lines 76-145 (`union.tex` predicate-OR vs bit-OR-Bloom): the dual treatment of predicate-OR (the canonical operation) and bit-OR-Bloom (the operational shortcut) is well-motivated, but the section title is "Union of Approximate Sets". The reader who skips ahead to the worked example at line 238 finds it computes the predicate-OR FPR; the bit-OR-Bloom case is mentioned only in the analysis. A clarifying sentence at the start of the worked example ("we compute the predicate-OR FPR; the bit-OR-Bloom result for the same operands appears at line 268") would help.
- **MINOR** §6.4 line 94 (`perfect-filter-line.tex`): the part (4) formula `$(0, \fnrate_B \cdot 0 \,\textrm{terms vanish})$` is awkward LaTeX and reads as a placeholder. The intent appears to be that both terms in the difference FNR formula vanish; the cleaner phrasing is "$(0, 0)$ on the excluded origin" with prose explanation rather than inline math.
- **MINOR** §6.2 line 282 (worked example transition): "The complement of $\ASet{A}$ has rates $(\fprate_\complement, \fnrate_\complement) = (\fnrate_A, \fprate_A) = (0, 0.01)$." The complement has moved $\ASet{A}$ from $(\fprate_A, \fnrate_A) = (0.01, 0)$ to $(0, 0.01)$. The next sentence says "The complement has moved $\ASet{A}$ off the FNR-zero axis and onto the FPR-zero axis." This is correct, but the point $(0, 0.01)$ formally has $\fprate = 0$ AND $\fnrate = 0.01$, i.e., a one-sided approximate set on the FPR-zero axis (per `def:one-sided`, this requires $\fnrate > 0$). The phrasing is fine; the §6.3 follow-up should mention this complement landing is on the line, not "off both axes".
- **MINOR** §6.3 line 142 ("$\complement \ASet{B}$ with rates $(\fnrate_B, \fprate_B) = (0, 0.02)$"): the swap notation is consistent with `prop:complement-swap` but the parenthetical $(\fnrate_B, \fprate_B)$ uses the *operand* labels in the swapped order. A reader looking at this line in isolation could think B itself has these rates. The convention is right; one extra word ("the swapped rates $(\fnrate_B^\complement, \fprate_B^\complement) = ...$") would resolve ambiguity.
- **MINOR** §6.3 line 134-135 ("The mixed intersection $\ASet{A} \cap \complement \ASet{B}$ asks both operands to report $\top$ on points of $A \cap \complement B = A \setminus B$"): "asks both operands to report $\top$ on points of..." reads slightly off. The intersection's predicate is $\ASet{A}(x) \land (\complement \ASet{B})(x)$. The set $A \cap \complement B$ is the objective truth, not a query specification. The reader has to map "report $\top$ on points of" to "is intended to report $\top$ on points of". One word ("intended" or "should") sharpens this.
- **MINOR** §6.1 line 224 ("the union false-negative rate, in contrast, mixes three different per-region rates"): the §6.1 union-FNR derivation at lines 200-220 introduces region weights $w_1, w_2, w_3$ summing to 1 but does not say how the weights are determined operationally. A pointer ("these weights are the query distribution's mass on each region; in chapter 7, the workload prevalence $\pi$ determines them") would link to §7.4.
- **MINOR** §6.2 line 326 ("the chapter notebook explores the discrepancy empirically"): bit-AND of Bloom filters is named as a "different construction" with a worked-example discrepancy, but the discrepancy is not quantified in the text. The Bloom-OR comparison at §6.1 lines 115-120 quantified the gap (predicate-OR $\approx 0.0163$ vs bit-OR-Bloom $\approx 0.137$); the bit-AND case would benefit from the same.
- **NOTE** §6.4 lines 159-172 (geometric structure of $\mathcal{L}$ as a wedge): the algebraic shape paragraph nicely connects the closure properties to the non-convexity of the wedge. The reader who has not internalized "perfect filter line as union of two axes" benefits from the geometric picture. Consider including a small figure (perfect filter line in the rate plane); this would be the chapter's first figure and would anchor §6.4's prose.
- **NOTE** §6.5 (`what-comes-next.tex`): the trajectory preview is appropriately short. Chapter 7 reference is well-motivated (PPV depends on $\fprate, \fnrate, \pi$); chapter 8 reference is also well-motivated (the floor and the gap). No issues.

### Chapter 7: Classification Measures (~25 pp; target ~28 pp)

**spec-auditor:** all six sections present per spec §4 chapter 7 row.
§7.1 setup-revisited names the four items the §1.4 deferral left;
§7.2 retires item (i) with the four propositions (unbiasedness,
variance, MLE, Fisher info and CRLB attainment); §7.3 retires items
(ii) and (iii) with Wald, Wilson, Clopper-Pearson, Jeffreys, and the
sawtooth diagnosis; §7.4 retires item (iv) with PPV, NPV, F1 as
random variables and the delta-method machinery; §7.5 is the deployed
Bloom filter diagnostic with the route A/B fork. 11 exercises with
3/5/3 distribution. Chapter 7 is the longest in Part II (well over
spec target of 28 pp, though within the master spec's 32 pp hard cap).

**quality-auditor (cold read):** the chapter reads cleanly. The
chapter 1 deferred items (named in §7.1) are each retired in a
named subsection of §7.2-§7.5. The §7.2 efficiency / CRLB
chain (four short propositions) is a clean pedagogical structure.
§7.3 diagnoses the Wald failure rigorously (boundary problem, skew
problem, sawtooth) before introducing the three alternatives, which
is the right pedagogical order. §7.4 delivers the prevalence-dependence
caveat well; the workload-A vs workload-B Bloom filter contrast at
the end of §7.4 is the right anchor for §7.5.

**math-auditor:** verified all numerical claims. §7.4 F1 worked
example: $\Recall = 0.9$, $\Precision = 2/3 = 0.667$, $\Fone = 1.2 /
1.5667 = 0.766$ checks. F1 delta-method variance computation
verified symbolically and numerically: $4 \cdot 145^2 \cdot 9 +
4 \cdot 90^2 \cdot 42.75 = 2{,}142{,}000$; $235^4 = 3{,}049{,}800{,}625$;
ratio $= 7.02 \times 10^{-4}$; SE $= 0.0265$; CI $[0.7141, 0.8179]$
matches the text. §7.5 Bloom diagnostic: theoretical FPR $0.0082$ from
$(1 - e^{-0.7})^7$ checks; empirical $\hat{\fprate} = 92/9000 =
0.01022$; Wilson CI center $0.01043$ and half-width $0.00209$ giving
$[0.00834, 0.01252]$ all match. PPV $= 0.1 / 0.10920 = 0.9158$ and
delta-method CI $[0.9001, 0.9314]$ both check. Route A fpr-target $=
(0.05 \cdot 0.1) / (0.95 \cdot 0.9) = 0.00585$ checks. Route B
prevalence-target $\approx 0.163$ checks.

**cross-ref-auditor:** all DEFINED labels match declarations; no
collisions. All RESOLVED labels exist. The cross-chapter retirement
of §1.4 deferrals is comprehensively documented in `\Cref{sec:sampling-rates}`
references across §7.1-§7.4.

#### Findings (chapter 7)

- **MAJOR** §7.4 derived-measures.tex line 232 cites `\cite{casella-berger}` for the delta-method proof but the §7.4 prose does not cite the chapter's reference manuscript `towell-bernoulli-classification-measures` until the bibliographic notes (§7.6 line 34). The §7.4 prose explicitly says "the bivariate delta-method computation that yields \Cref{prop:ppv-variance}" follows the manuscript. A `\cite{towell-bernoulli-classification-measures}` or `(see \Cref{sec:bib-notes-ch7})` at the proposition is the conventional way to credit the source.
- **MAJOR** §7.5 lines 95-101 (Wilson half-width arithmetic): the §7.5 Wilson HW is computed as $0.00209$, and the resulting interval $[0.00834, 0.01252]$ excludes the theoretical $\fprate = 0.0082$. The text concludes "the discrepancy is real and not an artifact of small samples". But the lower endpoint is $0.00834$ vs theoretical $0.0082$, a gap of only $0.00014$, well within typical hashing noise (the §5.2 note at line 195 estimated the bit-check independence approximation could deviate by ~1% of the rate, which at $\fprate = 0.0082$ is ~$8 \times 10^{-5}$, smaller than the gap but in the right ballpark). The diagnostic point ("the deployment $\fprate$ is empirical, not a design parameter to be trusted on faith") is correct, but the framing "the discrepancy is real" understates the closeness. One sentence acknowledging "the deviation is one standard error" or "the theoretical value sits within $0.05 \sigma$ of the Wilson lower endpoint" would calibrate the conclusion. (Note: the Part II spec calls for the diagnostic example to be substantive; the diagnostic itself is fine, the calibration of the deviation is what needs work.)
- **MINOR** §7.4 line 92-94 (PPV definition): the PPV definition writes the denominator as $\pi(1-\fnrate) + (1-\pi)\fprate$ but does not include the column-total normalization explicitly. A reader who has not internalized the column-conditional reading benefits from one sentence: "the denominator is the marginal probability of a $\top$ report, $\Pr[\ASet{A}(X) = \top]$; the numerator is the joint probability $\Pr[\ASet{A}(X) = \top, X = \top]$."
- **MINOR** §7.5 line 188 (Route B prevalence calculation): "$0.95 = \pi / (\pi + (1-\pi) \cdot 0.01022)$" gives $\pi \approx 0.163$ (the §7.5 text says "$\approx 0.163$"). The arithmetic is right but the intermediate step is skipped. One line ("$0.95\pi + 0.95 \cdot 0.01022 - 0.95 \cdot 0.01022 \pi = \pi$, solve to get $\pi = 0.95 \cdot 0.01022 / (0.05 + 0.95 \cdot 0.01022) \approx 0.163$") would help.
- **MINOR** §7.3 line 137-167 (Wilson derivation): the Wilson derivation cleanly arrives at the quadratic inequality and the definition. The text says "this is a downward-closed quadratic in $\fprate$, so its solution set is the interval between the two roots." That is right, but the qualifier "downward-closed" might confuse readers who think of upward-opening parabolas as having interior solution sets. One word substitution ("upward-opening" or "convex") would be clearer; alternatively cite the quadratic formula step explicitly.
- **MINOR** §7.4 line 195-204 (PPV bias discussion): "$\widehat{\PPV}$ is not unbiased for $\PPV$." The discussion is correct but compact. The Jensen inequality reference at line 197 says the bias comes from applying Jensen to the convex function $x \mapsto a/(a+x)$ in the denominator. The numerator of the ratio is also random, so the Jensen argument is more subtle than the prose suggests. A clarifying sentence ("the ratio of two binomial counts has bias O(1/n) under Jensen's inequality applied to the implicit ratio expansion") would suffice.
- **MINOR** §7.5 line 200-201 ("This route trades capital cost for the assumption that the workload mix will shift in the desired direction"): the Route B fork is "wait", and the text correctly notes this is "the right route when prevalence is expected to climb for independent reasons". But the alternative (accepting the lower PPV) is the silent third route. One sentence ("a third route, accepting PPV $= 0.916$ as good enough, is operationally identical to Route B with the assumption removed") would complete the dichotomy.
- **NOTE** §7.6 (`bibliographic-notes.tex`): the bibliographic notes are well-organized and appropriately concise. The Wilson 1927 and Clopper-Pearson 1934 historical anchors are well-placed.
- **NOTE** §7.2 line 219 (MLE = method-of-moments coincidence): "Method-of-moments and maximum-likelihood agree on this problem; in more general settings they need not, as Exercise 9 of this chapter illustrates." Good pedagogical signposting; no action.

### Chapter 8: Information-Theoretic Bounds (~20 pp; target ~22 pp)

**spec-auditor:** all six sections present per spec §4 chapter 8 row.
§8.1 entropy refresher (one page on $H(X)$, $H(p)$, $I(X;Y)$, capacity);
§8.2 BSC capacity (the closed form $C = 1 - H(\fprate)$ derived);
§8.3 the entropy floor theorem with the counting-argument proof sketch;
§8.4 the Bloom filter gap with the $\log_2 e$ overhead proposition;
§8.5 forward-references to chapter 14 and chapter 15; §8.6
bibliographic notes. 11 exercises with 3/5/3 distribution. The "light"
chapter designation in the spec is honored: the proof of the entropy
floor is a sketch (the full proof points to the paper), the source-coding
reading is informal.

**quality-auditor (cold read):** §8.1 is the right length (one page,
no derivation). §8.2 derives BSC capacity in three named steps; the
prose is clean. §8.3 lands the headline theorem and gives an enough
proof sketch for a graduate-level reader; the asymptotic regime is
correctly identified. §8.4 derives the $\log_2 e$ overhead, gives a
table for FPR $= 10^{-2}, 10^{-3}, 10^{-6}, 10^{-9}$, and explicitly
identifies the structural choice (flat shared bit array) as the
source of the overhead. The §8.5 forward references close the chapter
cleanly.

**math-auditor:** verified all numerical claims. $\log_2 e = 1.4427$
(computed as $1/\ln 2$) checks. The Bloom-vs-floor table in §8.4
verifies: at $\fprate = 10^{-2}$, floor $6.64$, Bloom $9.59$, gap
$2.95$; at $\fprate = 10^{-3}$, floor $9.97$, Bloom $14.38$, gap
$4.41$; at $\fprate = 10^{-6}$, floor $19.93$, Bloom $28.76$, gap
$8.82$; at $\fprate = 10^{-9}$, floor $29.90$, Bloom $43.13$, gap
$13.24$. The §8.1 binary entropy values $H(0.01) \approx 0.0808$,
$H(0.1) \approx 0.4690$, $H(0.5) = 1$ all check. The §8.2 BSC capacity
values $C(0.01) = 0.9192$, $C(0.1) = 0.5310$, $C(0.4) = 0.0290$ all
check. The §8.3 entropy-floor numerical table at FPR $= 10^{-k}$ for
$k = 1,2,3,6,9$ matches.

**cross-ref-auditor:** all DEFINED labels match declarations; no
collisions. All RESOLVED labels exist. Forward references to chapters
14 and 15 use chapter-level labels (Plan 0 stubs).

#### Findings (chapter 8)

- **MAJOR** §8.3 lines 258-272 (two-sided floor stated without proof): "Stated as a theorem we do not prove here: a two-sided approximate set with rates $(\fprate, \fnrate)$ can in principle be represented in fewer than $n \log_2(1/\fprate)$ bits ... The exact two-sided bound is the binary-symmetric analog of the present floor: roughly $n (1 - H(\fnrate)) \log_2(1/\fprate)$ bits per element." This formula is stated as "We omit the derivation." It checks at the boundaries (correctly reduces to one-sided at $\fnrate = 0$ and gives $0$ at $\fnrate = 1/2$), but the formula is not in the source paper `towell-bernoulli-entropy` (verified by inspection of `papers/bernoulli_entropy/sections/*.tex`). The textbook is asserting a result with no source citation. Either find a citation (Cover-Thomas chapter on lossy source coding), or weaken to "we conjecture" / "by analogy with...", or remove the formula and keep the qualitative point.
- **MAJOR** §8.4 lines 90-101 (Bloom-vs-floor ratio derivation): the §8.4 derivation reads $m / n = \log_2(1/\fprate) \cdot \log_2 e$ for Bloom, and the floor $m_{\min} / n \geq \log_2(1/\fprate)$, then claims the ratio $m/n \,/\, m_{\min}/n = \log_2 e$. But $m_{\min}/n$ is a lower bound (the floor is an inequality), so the "ratio" is well-defined only if we interpret $m_{\min}/n$ as the tight bound $\log_2(1/\fprate)$. The text needs one sentence clarifying that the floor is achievable (chapter 14's BHF achieves it asymptotically; cited at line 280) so the comparison ratio makes sense.
- **MINOR** §8.1 lines 91-93 ("the dominant term of $H(\fprate)$ as $\fprate \to 0$"): "the quantity that matters in \Cref{sec:entropy-floor} is the related quantity $-\log_2 \fprate$, which is the entropy of an indicator that an event of probability $\fprate$ occurs (the dominant term of $H(\fprate)$ as $\fprate \to 0$)." This is correct (the $-\fprate \log_2 \fprate$ term dominates as $\fprate \to 0$), but the relationship between "the entropy of an indicator" and the floor formula is non-trivial: the floor is $-\log_2 \fprate$, not $-\fprate \log_2 \fprate$. The §8.1 prose is a hint at the source-coding interpretation, but conflates two distinct quantities. A one-sentence calibration ("the floor is $-\log_2 \fprate$ per stored element; the rate $\fprate$ is the per-element probability of a false acceptance, and $-\log_2 \fprate$ is the bit cost of distinguishing accepted elements at that error rate") would clarify.
- **MINOR** §8.3 line 84 (`|A_R| \le n + \fprate (N - n) \approx n + \fprate N`): the approximation step replaces $\fprate(N - n)$ with $\fprate N$ for $N \gg n$. This is correct in the asymptotic regime, but the proof at lines 170-186 then uses the approximation $|A_R| \le n + \fprate N$ throughout. A reader who tracks the approximation will not catch why it is OK to drop the $-n$; one sentence ("the $\fprate \cdot n$ correction is dominated by $\fprate \cdot N$ when $N \gg n$, and the bound holds with the original $\fprate(N - n)$ form throughout") would close the loop.
- **MINOR** §8.3 line 178 ("in the regime $\fprate N \gg n$ simplifies to $n \log_2(\fprate N / n) + O(n)$"): the simplification step replaces $\log_2(1 + \fprate N / n)$ with $\log_2(\fprate N / n)$ in the regime $\fprate N \gg n$. The numerical impact for typical deployments: at $\fprate = 10^{-2}, N = 10^9, n = 10^6$, we have $\fprate N / n = 10$, so $\log_2(11)$ vs $\log_2(10)$ differ by $0.14$, about 4% of the term. The asymptotic regime is correct, but a reader who tries to apply the bound at modest scales will see a slack. One sentence acknowledging the slack at finite scales would be honest.
- **MINOR** §8.4 lines 144-151 (megabyte-per-million comparison): "the gap between Bloom and the floor is about $8.83$ megabits, or $1.10$ megabytes per million items". At $n = 10^6$ and gap $= 8.83$ bits per element, total is $8.83 \cdot 10^6 = 8.83 \times 10^6$ bits, $= 1.104$ megabytes. The text rounds to $1.10$ megabytes. Both are correct; the unit consistency (megabits vs megabytes) is right. No action; this is a verification only.
- **NOTE** §8.6 (`bibliographic-notes.tex`): four paragraphs are appropriately compact. The Mitzenmacher 2002 compressed-Bloom-filter reference is well-motivated. The Cover-Thomas reference is the right depth pointer. No action.

## Cross-chapter coherence findings

These findings only surface when reading across chapters.

- **MAJOR** Predicate-OR / bit-OR / bit-AND distinction across chapters 5 and 6: the §5.5 "what comes next" at line 53 previews "The union of two Bloom filters by bit-OR gives an FPR of $1 - (1 - \fprate_1)(1 - \fprate_2)$", which is the predicate-OR formula, not the bit-OR-Bloom formula. §6.1 then correctly distinguishes the two: predicate-OR gives $0.0298$ but bit-OR-Bloom gives $0.1378$ for the same operands. The §5.5 forward reference uses "bit-OR" as shorthand for what §6.1 then names as predicate-OR. Standardize the terminology: either §5.5 uses "predicate-OR" (matching §6.1) or names "the bit-OR of two Bloom filters' OUTPUTS" rather than "bit-OR of two Bloom filters". The §6.2 caveat-on-bit-AND-of-Bloom-filters paragraph (lines 305-326) has the same issue but in the AND direction.
- **MINOR** Notation drift: $\hat{\PPV}$ vs $\widehat{\PPV}$ in §7. §7.4 lines 183, 187, 192, etc. use `\widehat{\PPV}` (with `\widehat` macro); §7.5 lines 121, 124, 127 use the same. But §7.4 line 142 uses `$\hat\pi$` (with `\hat`). Both are fine LaTeX, but the difference is visible: `\hat` over a single character, `\widehat` over a multi-character symbol. Standardize either to `\widehat` for all hat notations or use `\hat` for single-character only (the latter is more conventional).
- **MINOR** Cross-Chapter PPV story (§7.4 + §8.3): §7.4 PPV depends on workload prevalence. §8.3 floor is for FNR-zero sets at FPR $\fprate$. A reader who wants PPV at the floor (constructive optimum) finds the formula in §7.4 but the floor's PPV implication is not stated until §8.4 line 162-163 ("PPV near $0.99$ on Workload A vs near $0.5$ on Workload B"). One §8.4 cross-reference ("at the floor's FPR, PPV follows §7.4 def:ppv at the workload's prevalence") closes the loop.
- **MINOR** Cross-Chapter Bloom-filter rate consistency: §5.2 line 313 gives $\fprate^* \approx 0.0078$ ($k = 7, m/n = 10$); §6.1 line 116 uses $\fprate = 0.0082$ (same parameters). The two values differ by the $(1/2)^k$ vs $(1 - e^{-kn/m})^k$ approximation gap. Standardize. Either §5.2 says "at the optimum, both formulas give $\fprate \approx 0.008$" or §6.1 uses $0.0078$.
- **NOTE** Bloom-filter thread carry: §5.2 introduces, §5.4 references in bit-budget comparison, §6.1 union worked example, §6.2 intersection worked example, §6.3 cancellation worked example, §7.4 PPV under workload, §7.5 diagnostic application, §8.3 entropy floor table, §8.4 gap proposition. The thread carries cleanly through nine sections. Best Part II demonstration of the running-example device.
- **NOTE** §1.4 deferral retirement: §7.1 names the four items, §7.2 retires item (i) with unbiasedness / variance / MLE / CRLB, §7.3 retires items (ii) and (iii) with Wilson / Clopper-Pearson / Jeffreys / sawtooth diagnosis, §7.4 retires item (iv) with PPV / NPV / F1 / delta-method. All four items are addressed in named subsections. Clean.
- **NOTE** Documented deferred cross-refs unchanged: `ch:composition` x 1 (chapter 4 forward ref), `ch:sketches` x 5 (chapter 9 forward refs to chapter 10's `ch:sketches-estimators`), `sec:noisy-bit` x 2 (chapter 17 forward refs to chapter 1). All are baseline-flagged in the build log and not new findings.
- **NOTE** Page budgets vs spec §6 budget table:

| Chapter | Spec §6 target | Estimated current |
|---|---|---|
| Ch 5 | ~28 pp | ~27 pp (-1) |
| Ch 6 | ~24 pp | ~25 pp (+1) |
| Ch 7 | ~28 pp | ~25 pp (-3) |
| Ch 8 | ~22 pp | ~20 pp (-2) |
| Total | ~102 pp | ~97 pp (-5) |

  All within reasonable tolerance. Chapter 7 at 25 pp is the chapter
  most under spec; the §7.2 / §7.3 / §7.4 / §7.5 sections are each
  3-7 pages and could absorb the additional material the spec budgeted
  for (e.g., the delta-method derivation for $\Fone$ which §7.4 line
  306-309 states as a one-line variance formula without derivation;
  the spec risk-table item 1 explicitly mentioned this might happen).
  No action required.

## Recommended next actions

Ordered by priority.

### BLOCKER

(None.)

### MAJOR (should fix before integration sign-off; may defer to a revise pass)

1. **§6.3 Proposition 6.3.2 (`prop:mixed-intersection-escape`):** rewrite the proposition title and last sentence of the proof so the boundary regime (B is FPR-zero) is correctly characterized as "leaves the FNR-zero axis but lands on the FPR-zero axis" rather than "escapes the line entirely". The non-boundary regime (B is two-sided) is the genuine escape.
2. **§6.4 Proposition 6.4.1 part (4) (`prop:fnr-zero-closure`):** the substantive content is the "otherwise" clause; promote it to the main statement. The exact-set case (B both FPR-zero and FNR-zero) should be a footnote noting that the difference reduces to an exact-set test.
3. **§6.2 intersection FPR worked example:** either assume $A = B$ explicitly in the worked example (lines 257-277), or write the full mixture formula and specialize. The same fix should propagate to §8 ex 11 and §7.4 line 305.
4. **§6.1 proof of `prop:union-fpr-fnr`:** anchor the multiplication step at line 192-193 to the independence assumption stated at line 154. One sentence linking the two ("By the cross-set independence assumption ...") closes the loop.
5. **§7.4 derived-measures: cite `towell-bernoulli-classification-measures`** at the proposition statement (line 232), not only in the bibliographic notes. The §7.4 prose explicitly attributes the manuscript; the citation should appear at the source.
6. **§8.3 two-sided floor:** either find a citation for the formula $n (1 - H(\fnrate)) \log_2(1/\fprate)$ (Cover-Thomas chapter 10 on lossy source coding is the natural reference), weaken the claim to "by analogy", or remove the formula and keep the qualitative point.

### MINOR (polish-pass additions)

Add to the polish-pass list:

- §5.1 header forward-ref list updated to include `sec:one-sided-two-sided`.
- §5.3 header resolved list updated to include `prop:stable-Q`.
- §5.2 line 311 vs line 315: clarify that $0.00819$ (exact formula) and $0.0078$ (half-occupancy asymptotic) refer to different formulas.
- §5.2 line 195: quantify the bit-check independence approximation deviation.
- §5.4 line 130 $9.58$ vs §8.4 table $9.59$ standardize precision.
- §6.1 §6.2 worked examples specify "predicate-OR" / "predicate-AND" at the start.
- §6.4 line 94: rewrite the placeholder $(0, \fnrate_B \cdot 0 \,\textrm{terms vanish})$.
- §6.3 line 142: swapped-rate notation `\fprate_B^\complement` is clearer than $(\fnrate_B, \fprate_B)$.
- §6.3 line 134-135 "asks both operands to report $\top$": insert "is intended to" or "should".
- §6.1 line 224: pointer to chapter 7 for the region-weight interpretation.
- §6.2 line 326: quantify the bit-AND-of-Bloom discrepancy.
- §7.4 PPV definition (line 92-94): one sentence on column-conditional reading.
- §7.5 Route B calculation (line 188): show the intermediate algebraic step.
- §7.3 Wilson derivation: "downward-closed quadratic" wording.
- §7.4 PPV bias discussion: Jensen argument clarification.
- §7.5 Route B "wait": acknowledge the silent third route.
- §8.1 line 91-93: calibrate the relationship between $-\log_2 \fprate$ and the entropy of an indicator.
- §8.3 line 84: prose to justify dropping the $-n$ in the approximation.
- §8.3 line 178: prose to acknowledge finite-scale slack.
- §8.4 Bloom-vs-floor ratio: cite the floor's achievability (chapter 14 BHF).
- §7.5 Wilson interval gap to theoretical $\fprate$: calibrate "the discrepancy is real" against the actual one-standard-error gap.
- $\widehat{\PPV}$ vs $\hat\pi$: standardize hat notation.
- §5.5 / §6.1 standardize bit-OR vs predicate-OR terminology.
- §5.2 / §6.1 standardize Bloom filter FPR at $k=7, m/n=10$ ($0.0078$ or $0.0082$).

### NOTE (defer to a future revision or leave as-is)

- §5.6 "the Bloom filter as a particular construction": promote to §5.1.
- §5.5 line 90 redundant with §5.4 line 130: compress one.
- §6.4 lines 159-172 geometric wedge: consider a figure.
- §6.5 trajectory preview: no issues.
- §7.6 bibliographic notes: no issues.
- §7.2 line 219 MLE / MoM coincidence: good pedagogical signposting.
- §8.6 bibliographic notes: no issues.
- Cross-chapter PPV at the floor: §8.4 cross-reference to §7.4.
- Bloom-filter running thread: cleanest Part II thread carry.
- §1.4 deferral retirement: clean.
- Documented deferred cross-refs unchanged.
- Page budgets within tolerance.

## Specialist verdicts (consolidated)

- **spec-auditor:** Part II PASS. All content checklist items from
  spec §4 chapters 5-8 are realized. The Bloom-filter running thread
  carries (§5.2, §6.1, §6.2, §6.3, §7.4, §7.5, §8.3, §8.4). The §1.4
  deferral is cleanly retired in chapter 7 (§7.1-§7.4 each retire a
  named item). The chapter 8 "light" designation is honored without
  hand-waving the entropy floor proof.
- **quality-auditor:** "minor polish needed" overall, with chapter 6
  carrying the heaviest substantive load (the three MAJOR findings on
  §6.2 intersection, §6.3 escape proposition, and §6.4 difference part
  4 are all related to the perfect-filter-line algebra's edge cases).
  Chapters 5, 7, 8 are nearly publication-ready.
- **math-auditor:** PASS. Every numerical claim checked verifies
  independently. The §5.2 Bloom optimal-$k$ derivation, the §5.4
  $9.6n$ bit budget, the §6.1 union worked example, the §6.2
  intersection worked example, the §7.4 F1 worked example (variance
  $7.02 \times 10^{-4}$, CI $[0.714, 0.818]$), the §7.5 Bloom
  diagnostic (PPV $0.9158$, CI $[0.900, 0.932]$), and the §8.4 Bloom
  gap ($\log_2 e \approx 1.443$) all verify. Known correction baseline
  values (§5.2 0.0117 → 0.0546 and §5.4 14.4n → 9.6n) are correctly
  reflected in the text.
- **cross-ref-auditor:** PASS. All DEFINED labels match declarations
  with no collisions. All RESOLVED labels exist (`prop:stable-Q`,
  `def:bernoulli-bool`, `thm:kronecker`, `ax:element-indep`,
  `ax:block-rates-indep`, and chapter-level stubs). Two header
  comment-block staleness issues (chapter 5 §5.1 and §5.3) are
  documentation issues only, not actual cross-reference failures.
  The three documented deferred items (`ch:composition`, `ch:sketches`
  x 5, `sec:noisy-bit` x 2) match the build log exactly.

## Overall recommendation

Part II is in solid shape. There are no BLOCKERs. The six MAJOR
findings cluster around chapter 6's algebraic edge cases (the perfect
filter line's closure properties under intersection and difference)
and one source-attribution issue in §7.4 plus one citation gap in
§8.3. The 17 MINOR findings are appropriate polish-pass material; the
11 NOTE items are deferrals.

The §6.3 and §6.4 propositions need careful rewriting because the
underlying algebra is subtle and the propositions as stated do not
quite match the geometric story the section's prose tells. The
§6.2 intersection-FPR simplification needs scope-clarification in
the worked example. These three findings together represent the
editorial work most worth doing on Part II before integration sign-off.

The chapters' pedagogical voice is consistent across all four. The
Bloom-filter running thread is the cleanest Part II thread carry and
demonstrates the running-example device working as intended. The §7.1
naming of the §1.4 deferral and the matched retirements in §7.2-§7.4
are the chapter 7 highlight; the §7.5 Bloom diagnostic application is
the pedagogical payoff. The §8.3 / §8.4 floor + gap pair leaves the
reader wanting chapter 14, per the spec's success criterion 4.

Recommend: schedule the six MAJORs for a focused revision pass on
chapter 6 (three findings) plus the §7.4 citation and §8.3 two-sided
formula. Queue the 17 MINORs for a polish pass before Milestone 1.
