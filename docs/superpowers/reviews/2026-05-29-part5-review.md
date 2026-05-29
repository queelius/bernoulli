# Part V Review (chapters 16-18)

Date: 2026-05-29
Reviewer: bookwright reviewer orchestrator (Part V scope)
Auditors applied: spec, quality, math, cross-ref (per-chapter, inline)

This review evaluates all three chapters of Part V ("The Boundary
and Beyond") of *Bernoulli Types: An Algebra of Approximate
Computation* against the Part V design spec
(`docs/superpowers/specs/2026-05-27-bernoulli-textbook-part5-design.md`)
and the master spec
(`docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`).
The four auditor roles were applied per chapter and the findings
are synthesized below by chapter and by cross-chapter coherence.
The documented deferred items (`ch:composition` x 1, `ch:sketches`
x 5, `sec:noisy-bit` x 2) match `book/book.log` exactly and are
not re-flagged.

## Summary

- **Total findings: 33** (0 BLOCKERs, 7 MAJORs, 19 MINORs, 7 NOTEs).
- **Top high-priority items:**
  1. (MAJOR) §16.6 contains two `Part~VI` references that should be
     `Part~V` (chapters/ch16/whats-next.tex lines 49 and 50). The
     book has five parts; chapters 17-18 sit in Part V, not Part
     VI. The mistake is structural: "Its placement between the
     constructive culmination of Part~IV (the BHF and BPHF) and
     the cryptographic applications of Part~VI is structural.
     Part~IV sat inside the framework's domain of validity;
     Part~VI extends the framework into settings where clean iid
     analysis can no longer be relied on." Both "Part~VI" should
     read "Part~V". A reader sees a chapter pointing forward to a
     non-existent Part VI immediately before chapter 17 begins
     Part V's cryptographic content.
  2. (MAJOR) §17.1 and §17.4 conflate the Bloom filter (chapter 5,
     $1.44 \log_2(1/\fprate) \approx 9.59$ bits per element at
     $\fprate = 0.01$) with the BHF (chapter 14, $-\log_2 \fprate
     + \mu \approx 6.64$ bits per element at the same target).
     §17.1 line 137-139 says "A Bloom-filter-based cipher map for
     set membership uses on the order of $-\log_2 \fprate + \mu$
     bits per inserted element (the optimal formula of chapter
     14)", but the chapter 14 formula is the BHF, not the Bloom
     filter. §17.4 lines 185-187 repeats the mistake more
     concretely: "the optimal Bloom-filter construction of chapter
     5 uses about $-\log_2(0.01) \approx 6.64$ bits per element on
     the underlying filter," which is wrong for Bloom (chapter 5's
     Bloom at $\fprate = 0.01$ uses $9.59$ bits per element). The
     §17.4 worked-example total of "$\approx 830$ kilobytes" at
     $n = 10^6$ comes from BHF arithmetic ($6.64 \cdot 10^6 / 8000
     \approx 830$ KB), not Bloom ($9.59 \cdot 10^6 / 8000 \approx
     1198$ KB $\approx 1.2$ MB). The cipher-map literature
     supports both: a Bloom-based cipher map uses Bloom-rate
     storage, a BHF-based cipher map uses the entropy-floor rate.
     The chapter should either rename the §17.4 construction to a
     BHF-based cipher map (and update the citation to chapter 14)
     or correct the formula and the worked-example total to the
     Bloom rate. As-written, the chapter calls one thing by
     another's name twice in succession.
  3. (MAJOR) §16.2 worked example "Bloom past capacity" has at
     least three internal inconsistencies between stated numbers
     and the underlying Bloom formula. (a) Line 56-58: "The fill
     ratio rises from $30\%$ to nearly $100\%$." At the design
     parameters ($m = 9585, k = 7, n = 1000$), the fill ratio is
     $1 - (1 - 1/m)^{kn} \approx 0.518 = 51.8\%$, not $30\%$. (b)
     Line 59-62: "the false-positive rate climbs from $0.01$ early
     to about $0.5$ late." At $n_{\text{actual}} = 5000$ (the
     scenario's "late" point), $(1 - e^{-7 \cdot 5000/9585})^7
     \approx 0.83$, not $0.5$. The $0.5$ value corresponds to a
     fill of $\approx 3234$ items, not $5000$. (c) Line 205-207:
     "The trajectory expectation $\sum_t \fprate(t)$, computed
     from the Bloom formula at each insertion count, is around
     $230$." With $1000$ queries on the post-fill filter at
     constant $\fprate = 0.83$, the expected total is $830$, not
     $230$. With $1000$ queries during the fill from $n = 1000$
     to $n = 5000$, the expected total is $\approx 420$ (each
     query at fill $1000 + 4t$). With $1000$ queries spread over
     a fill from $1000$ to $\approx 3500$ (where $\fprate$ averages
     to $\approx 0.23$), the trajectory expectation matches $230$,
     but this contradicts the stated $n_{\text{actual}} = 5000$.
     The Azuma-Hoeffding bound itself ($2 \exp(-100^2 / 2000) =
     2e^{-5} \approx 0.0135$) is correct, and the Chernoff
     comparison ($e^{-0.83} \approx 0.43$) is correct, but the
     scenario parameters are not internally consistent with the
     trajectory expectation, the fill ratio, or the rate
     trajectory all simultaneously.

- **Chapters with most findings:** Chapter 17 (11), Chapter 16
  (10), Chapter 18 (7), cross-chapter (4).

Overall the three chapters are pedagogically well-structured and
land Part V's organizational intent: chapter 16 catalogues the
framework's boundary (the iid breakdowns), chapter 17 lifts the
algebra to the cryptographic setting, and chapter 18 demonstrates
the cipher-map framework on a working application. The §18.6
"Closing the Book" section is the book's final word and lands
cleanly: it recaps the five parts in proportion (the atom, the
lift to sets, the lift to maps and types, the constructive
optimum, the boundary and applications) and closes with three
research directions without restating chapter-level minutiae.

Most numerical claims verify exactly: §17.2 cipher-map composition
$Q_1 Q_2$ matrix product (the $0.99 \cdot 0.995 + 0.01 \cdot 0 =
0.98505$ and $0.99 \cdot 0.005 + 0.01 = 0.01495$ entries match),
§17.6 PPV worked examples (PPV(0.05, 0, 0.01) = 0.1681 ≈ 0.168,
PPV(0.05, 0, 0.5) = 0.9524 ≈ 0.952), §18.2 Bloom space (m_d = 478.36
≈ 480 bits, 10000 docs * 480 / (8*1e6) = 0.6 MB), §18.3 worked
examples (PPV(0.01, 0, 0.1) = 0.9174 ≈ 0.917, PPV(0.3, 0, 0.1) =
0.2703 ≈ 0.270), §18.5 trace (PPV at π=0.003, fpr=0.01 = 0.2313 ≈
0.231; retune to C=0.5 at π=0.1 gives fpr* = 0.1111 ≈ 0.111), §18.4
Wilson margin (1.96 * sqrt(0.09 * 0.91 / 6000) = 0.0072), §18.3
intermediate points (PPV at fpr=0.05 = 0.690, at 0.1 = 0.526, at
0.2 = 0.357), and the closed-form solution fpr* = πC / [(1-π)(1-C)]
all verify exactly. Chapter 16's Azuma-Hoeffding application
parameters and Chernoff comparison check arithmetically. Chapter
17's confidentiality formulas C = (1-π)fpr / [π(1-fnr) + (1-π)fpr]
verify at the stated operating points. Chapter 18's §18.5 retuned
filter sizes (45.67 ≈ 46 bits, 95.67 ≈ 96 bits) check.

No em-dashes (U+2014 or ASCII `---`) anywhere in Part V. One
flagged use of "trivially" in §16.3 line 174 in a math-handwave
position. No "easy to see", "obviously", "clearly" as proof
substitutes (the one "clearly" use is as an adverb of perception,
not a hand-wave). No banned phrases from the soul-voice hook's
list. No label collisions. The 41 section/equation/proposition/
theorem/definition labels in Part V are all unique to those
chapters. All RESOLVED labels referenced from these chapters
resolve correctly in the book tree (`def:ppv`, `def:npv`,
`def:f1`, `def:bloom-filter`, `def:perfect-filter-line`,
`def:bernoulli-bool`, `def:n-ary-channel`, `thm:kronecker`,
`thm:n-ary-kronecker`, `thm:chernoff`, `thm:composition`,
`thm:bloom-optimal-k`, `prop:complement-axis-swap`,
`prop:ppv-variance`, `ax:element-indep`, `ax:block-rates-indep`,
`sec:bloom-from-scratch`, `sec:axiom-1`, `sec:axiom-2`,
`sec:kronecker`, `sec:n-ary-channels`, `sec:n-ary-kronecker`,
`sec:bernoulli-bool-formal`, `sec:perfect-filter-line`,
`sec:cancellation`, `sec:composition-theorem`,
`sec:derived-measures`, `sec:binomial-estimator`,
`sec:confidence-intervals`, `sec:sample-complexity`,
`sec:union-of-sets`, `eq:bloom-fpr`, `ex:ch5-7`, plus chapter
labels `ch:noisy-bit`, `ch:axioms-kronecker`, `ch:approximate-sets`,
`ch:set-composition`, `ch:classification-measures`,
`ch:information-bounds`, `ch:approximate-functions`,
`ch:sketches-estimators`, `ch:randomized-algorithms`,
`ch:approximate-relations`, `ch:algebra-types`,
`ch:optimal-bernoulli-sets`, `ch:perfect-hash-filters`,
`ch:not-bernoulli`, `ch:cipher-maps-trapdoor`,
`ch:encrypted-search`).

The findings below are sorted by severity within each chapter,
then by location.

## Findings by chapter

### Chapter 16: Approximate but Not Bernoulli (~25 pp; target ~31 pp)

**spec-auditor:** all eight sections from spec §4 chapter 16 row
present. §16.1 What This Chapter Is For (lists the five deferrals
from earlier chapters, names three failure modes, states honesty
posture); §16.2 Varying Rates Over Time (Axiom 2 violation, Azuma-
Hoeffding as the right tool, Bloom-past-capacity worked example);
§16.3 Correlated Noise Across Queries (Axiom 1 violation, McDiarmid
as the right tool, two-Bloom-filter worked example); §16.4
Adversarial Inputs (both axioms violated, worst-case bounds and
cryptographic hash families as right tools, Bloom-evasion worked
example); §16.5 Where the Framework Still Helps (perfect-filter
line, channel-matrix view, PPV per-query survive); §16.6 What's
Next (closes negative space, forward-links to chapters 17-18);
§16.7 Bibliographic Notes (4 paragraphs, 7 citations: Azuma 1967,
Hoeffding 1963, McDiarmid 1989, Devroye-Lugosi 2001, Goodfellow
2015, Carlini-Wagner 2017, Goldreich 1996). Learning outcomes box
has three bullets per spec format. 11 exercises with 3/5/3
difficulty distribution. Chapter is at ~25 pp, ~19% under the
spec's 31 pp target, the bibliographic notes and §16.5
(where-framework-helps) are notably under-budget; §16.2
(varying-rates) is also under but justifiably compact.

**quality-auditor (cold read):** §16.1 motivates the chapter
clearly by listing five specific deferrals being closed (chapter
1 §1.4 sampling, chapter 1 ex 10 Miller-Rabin, chapter 5 §5.4
one-sided sets, chapter 10 §10.5 sketch composition, chapter 13
ex 11 boundary algebra) and naming the three failure modes
(varying rates, correlated noise, adversarial inputs) explicitly.
§16.2's structural narrative (phenomenon, Axiom 2 violation,
consequences for iid tools, Azuma-Hoeffding as the right tool,
worked example, pedagogical diagnostic) is the right pedagogical
shape for boundary cataloguing. §16.3 mirrors the structure with
McDiarmid's inequality. §16.4's "the expectation-versus-supremum
gap" framing is the right one-line summary of adversarial
analysis. §16.5's "two-half pragmatic rule" (keep the geometry,
replace the iid tools with non-iid counterparts) is the chapter's
takeaway and lands cleanly. The chapter's overall posture (name
the failure honestly, point to the analytical alternative) is
the right one for a boundary chapter.

**math-auditor:** §16.2 Azuma-Hoeffding bound at $a = 100, c_t = 1,
n = 1000$: $2 \exp(-100^2 / (2 \cdot 1000)) = 2 e^{-5} \approx
0.0135$, text says "$\approx 0.013$" and "probability at least
$0.987$", both check. §16.2 iid Chernoff comparison: $\exp(-250
\cdot 0.01/3) = e^{-0.833} \approx 0.43$, text says "$e^{-0.83}
\approx 0.44$", checks. §16.3 two-Bloom worked example: $\fprate
= (1 - e^{-0.6})^3 = 0.0918$, text says "$\approx 0.097$", within
rounding. $p_A = 1 - (1 - 1/100)^{60} = 0.4528$, text says
"$\approx 0.45$", checks. Joint $(p_A p_B)^3 = (0.205)^3 =
0.00862$, text says "$\approx 0.008$", checks. §16.4 Bloom
evasion: $1 - e^{-7/9.585} = 0.518$ (text matches), $0.518^7 =
0.0100$ (text says "$\approx 0.013$", small discrepancy if
computed at slightly different bit fraction; reasonable within
rounding noise). §16.4 "1/fprate = 100 random tries" matches. The
Azuma martingale derivation (define $Y_t = \sum_{s \le t} (X_s -
\fprate(s))$ with $|Y_t - Y_{t-1}| = |X_t - \fprate(t)| \le 1$)
is correctly set up.

The §16.2 "Bloom past capacity" parameters are internally
inconsistent: fill ratio at design is 51.8% (not "30%"), FPR at
$n_{\text{actual}} = 5000$ is 0.83 (not "0.5 late"), and the
trajectory expectation $\sum_t \fprate(t) \approx 230$ does not
match the scenario as described (it requires either a different
fill range or different $k$). See MAJOR finding 3 above.

**cross-ref-auditor:** all DEFINED labels match `\label{}`
declarations (`sec:what-this-chapter-is-for`, `sec:varying-rates`,
`prop:azuma-hoeffding`, `sec:correlated-noise`, `prop:mcdiarmid`,
`sec:adversarial-inputs`, `sec:where-framework-helps`,
`sec:ch16-whats-next`, `sec:bib-notes-ch16`, `ex:ch16-1`-
`ex:ch16-11`). All RESOLVED labels exist (`ax:element-indep`,
`ax:block-rates-indep`, `sec:axiom-1`, `sec:axiom-2`,
`thm:chernoff`, `sec:bloom-from-scratch`, `thm:composition`,
`sec:composition-theorem`, `eq:bloom-fpr`, `ex:ch5-7`,
`def:bloom-filter`, `def:ppv`, `def:perfect-filter-line`,
`sec:perfect-filter-line`, `sec:n-ary-channels`,
`def:n-ary-channel`, `sec:n-ary-kronecker`,
`thm:n-ary-kronecker`). Two FORWARD refs (`ch:cipher-maps-trapdoor`,
`ch:encrypted-search`) now resolve to the actual chapter labels in
Part V (no longer Plan 0 stubs). No label collisions across the
book tree.

#### Findings (chapter 16)

- **MAJOR** §16.2 line 56-62 worked example "Bloom past capacity":
  three internal inconsistencies in the numerical setup (see Top
  priority item 3 above). At design parameters $m = 9585, k = 7,
  n = 1000$ the fill ratio is 51.8% (not the stated 30%) and at
  $n_{\text{actual}} = 5000$ the rate is 0.83 (not "about 0.5
  late"). The trajectory expectation $\sum_t \fprate(t) \approx
  230$ does not match either reading. The Azuma-Hoeffding bound
  arithmetic itself is correct, but the scenario as presented
  cannot simultaneously yield the stated rate trajectory, fill
  ratio, and trajectory expectation. Fix: pick a self-consistent
  scenario. For example, if $n_{\text{actual}} = 3000$ and 1000
  queries happen at fills uniformly spaced over the post-design
  fill from 1000 to 3000, the average $\fprate \approx 0.23$ and
  the trajectory expectation $\approx 230$; the rate "0.5 late"
  matches fill $\approx 3234$. Alternatively keep $n_{\text{actual}}
  = 5000$ and update the trajectory expectation and "rate late"
  to the corresponding values.
- **MAJOR** §16.6 lines 49-50 (two `Part~VI` references): the
  book has five parts; chapters 17 and 18 are in Part V, not Part
  VI. The two instances of "Part~VI" should both read "Part~V".
  See Top priority item 1.
- **MINOR** §16.1 line 49-50 (citation of chapter 1 §1.4): the
  text says "Chapter 1 \S1.4 (the sampling diagnostic) ended with
  an open question." Need to verify chapter 1's actual §1.4 ends
  with this question, if §1.4's content is different in the
  current draft, the reference would be wrong. (This is a check
  item; given the documented deferred `sec:noisy-bit` referent
  drift, it's worth verifying the chapter 1 §1.4 referent is
  what §16.1 claims.)
- **MINOR** §16.2 line 88 (after the "30%/100%" statement): the
  rate formula $(1 - e^{-k t / m})^k$ is given with $t$ the
  number of inserted items at the moment of the query. This is
  the standard Bloom formula, but using $t$ for "fill count"
  conflicts with the next section §16.2's use of $t$ for "query
  index" in the martingale $Y_t$. The variable overload could
  confuse a reader.
- **MINOR** §16.2 line 138-140 ("The standard MGF-plus-Markov
  argument from chapter 11 §11.4 carries over"): the proof
  sketch is fine but does not cite a specific result number from
  chapter 11. A `\Cref{prop:something}` or naming the specific
  result would tighten the back-reference.
- **MINOR** §16.3 line 174 ("hence trivially 'independent' given
  the conditioning"): the "trivially" is in a math-handwave
  position. Even with the scare-quoted "independent", the
  qualifier slides over a real conditional-independence
  argument. The sentence would read better with the argument
  stated: "the responses are deterministic functions of the bit
  patterns, hence (conditionally) independent given the bit
  patterns and the hash positions."
- **MINOR** §16.3 line 220-230 (negative correlation salvage):
  the paragraph is well-positioned but slightly under-developed.
  A one-sentence example (Bloom-filter bit-set events as
  negatively correlated; cite chapter 5 ex 7) would make the
  point concrete.
- **MINOR** §16.4 line 213-218 (Bloom evasion worked example
  rate): the text says "$0.518^7 \approx 0.013$, which matches
  the design target within rounding." With exact arithmetic
  $0.518^7 = 0.0100$, the "0.013" is approximate but the
  design target is 0.01. The "within rounding" phrasing is fine
  if the reader understands the small discrepancy.
- **NOTE** §16.4 lines 246-248 (targeted attacker O(1) work
  claim): "the attacker finds false positives in O(1) work per
  attempt" is correct asymptotically but skips over the
  constraint-satisfaction step (solving a small system to
  construct $y$ given target positions). A pointer to a specific
  attack construction or a citation to the adversarial-Bloom
  literature would tighten the claim.
- **NOTE** §16.5 lines 117-125 (Kronecker geometry for time-
  varying or correlated rates): the "applies sliced or
  conditioned rather than unconditionally" framing is the right
  framing but the supporting machinery (the chapter 4 Kronecker
  theorem's exact hypotheses on rate matrices) is not re-derived
  here. A back-reference to chapter 4 §4.4 with a one-line
  justification of why the per-query factorization survives
  would help.

### Chapter 17: Cipher Maps and Trapdoor Computing (~31 pp; target ~38 pp)

**spec-auditor:** all nine sections from spec §4 chapter 17 row
present. §17.1 What is a Cipher Map? (`def:cipher-map`; three
example cipher maps); §17.2 The Bernoulli Framework as Error Model
(`thm:cipher-composition`; channel matrix; two-stage encrypted
classifier worked example); §17.3 The Trapdoor Computing Paradigm
(client-server setup; multi-query leakage; adaptive adversaries
with $O(\log n)$ bit extraction worked example); §17.4 Sidebar:
Fully Homomorphic Encryption (Gentry 2009; FHE vs cipher-map
trade-off; concrete comparison at $n = 10^6$); §17.5 Boolean
Algebra Over Trapdoor Sets (`def:trapdoor-set`; union, intersection,
complement; cancellation phenomenon; conjunctive query worked
example); §17.6 Maximizing Confidentiality (confidentiality $C = 1
- \PPV$; FHE comparison at $C = 0$); §17.7 Bridge; §17.8
Bibliographic Notes (6 citations: Towell cipher maps, Towell
Boolean trapdoor, Towell max confidentiality, Gentry 2009,
Naor-Yung 1989, plus Goldreich 1996 from chapter 16). Learning
outcomes box has three bullets. 11 exercises with 3/5/3
distribution. Chapter is at ~31 pp, ~18% under the spec's 38 pp
target, all sections are uniformly somewhat compressed.

**quality-auditor (cold read):** §17.1's three-example introduction
(encrypted set membership, equality test, ordering) lands the
abstraction in concrete cases that span the rate landscape
(Bloom on the perfect-filter line; deterministic encryption at
zero error with structural leakage; order-preserving encryption
at zero error with even larger structural leakage). The
distinction between Bernoulli-error and structural-leakage
confidentiality is well-flagged. §17.2's chained-composition
machinery (channel matrix, matrix product, thm:cipher-composition)
is the right algebraic backbone and the worked example exhibits
$Q_g Q_f$ in the simplest two-cipher-map case. §17.3 introduces
the operational setting (client-server, honest-but-curious
threat model) cleanly and then takes the adaptive adversary case
seriously by giving a concrete attack (extract $O(\log n)$ bits
per query). §17.4's three-dimensional FHE cost analysis
(ciphertext size, operation latency, bootstrapping) is the right
summary for readers wondering about the FHE-vs-cipher-map gap.
§17.5's Boolean-algebra section makes the chapter 3 composition
theorem and the chapter 6 cancellation analysis carry over to
trapdoor sets without modification, and the worked conjunctive
query gives the multiplicative-precision result cleanly. §17.6
makes the dual reading of $(\fprate, \fnrate)$ as both correctness
and confidentiality formal via the chapter 7 PPV; this is the
chapter's central result and lands cleanly. §17.7 bridges
forward to chapter 18 and signposts the chapter's three "lifts"
(geometric, predictive, cryptographic).

The chapter has a structural Bloom/BHF confusion (see MAJOR
findings) that mars the §17.1 motivating example and the §17.4
worked example; otherwise the pedagogical structure is solid.

**math-auditor:** §17.2 cipher-map composition $Q_g Q_f$ in the
two-stage encrypted classifier worked example: $Q_g = [[0.99,
0.01], [0, 1]]$, $Q_f = I$ gives $Q_g Q_f = Q_g$, checks. With
$Q_f = [[0.995, 0.005], [0, 1]]$ instead, $Q_g Q_f$ entries
$(0.985, 0.015, 0, 1)$ check (text says "$\approx 0.015$").
Chapter 3 composition $1 - (1 - 0.01)(1 - 0.005) = 0.01495$
matches.

§17.5 trapdoor union/intersection arithmetic: $\fprate_{A \cup
B} = 1 - (1 - 0.01)(1 - 0.01) = 0.0199$ (text doesn't compute
this directly), $\fprate_{A \cap B} = 0.01 \times 0.01 = 10^{-4}$
(text matches; this is the headline result). The conjunctive
query worked example arithmetic is exact.

§17.5 cancellation example: $\fprate_{A \cup B} = 1 - (1 -
0.05)(1 - 0.05) = 0.0975$. Complement on the FNR-zero axis maps
to $(0, 0.0975)$ on the FPR-zero axis (per
`prop:complement-axis-swap`). Intersection with $(\fprate_C, 0)
= (0.05, 0)$: $\fprate = 0$ (since one operand has $\fprate = 0$
under independence) and $\fnrate = 1 - (1 - \fpr_{A \cup B})(1 -
0) = 0.0975$. The resulting cipher map sits at $(0, 0.0975)$ on
the FPR-zero axis, having traversed from the FNR-zero axis
through the complement and back through the cross-axis
intersection. All arithmetic checks.

§17.6 PPV worked examples: PPV$(0.05, 0, 0.01) = 0.01 / 0.0595
= 0.168$ (text matches, $C \approx 0.832$). PPV$(0.05, 0, 0.5)
= 0.5 / 0.525 = 0.952$ (text matches, $C \approx 0.048$). The
confidentiality formula $C = (1-\pi)\fprate / [\pi(1-\fnrate) +
(1-\pi)\fprate]$ at $\fnrate = 0$ verifies at both operating
points.

The §17.1 / §17.4 Bloom-vs-BHF storage formula confusion is a
substantive math finding (MAJOR; see Top priority item 2).

The §17.3 worked example "extracting $O(\log n)$ plaintext bits
per query" mixes two distinct attack scenarios with different
scalings (k queries to recover seed of length H gives H/k
bits/query; log|A| queries to localize a record gives 1
bit/query). Neither sub-claim matches the stated $O(\log n)$
rate. SUBSTANTIVE.

§17.4 line 207-208: "The space ratio is on the order of $10^4$,
with the cipher map four orders of magnitude smaller. The
runtime ratio is roughly the same: nanoseconds for the cipher
map, seconds for FHE, giving about $10^9$ in favor of the
cipher map." Then §17.6 line 207: "the FHE operator pays a
$10{,}000\times$ space and time overhead." The "$10,000\times$
space AND time" elides the §17.4 $10^9$ runtime ratio. Minor
inconsistency between §17.4 and §17.6 framings.

**cross-ref-auditor:** all DEFINED labels match `\label{}`
declarations (`sec:what-is-cipher-map`, `def:cipher-map`,
`sec:bernoulli-error-model`, `thm:cipher-composition`,
`sec:trapdoor-paradigm`, `sec:fhe-sidebar`, `sec:boolean-trapdoor`,
`def:trapdoor-set`, `sec:maximizing-confidentiality`,
`sec:ch17-bridge`, `sec:bib-notes-ch17`, `ex:ch17-1`-`ex:ch17-11`).
All RESOLVED labels exist (`sec:noisy-bit` x 2 is in the
documented deferred baseline; all other refs resolve). Two
forward refs to chapter 18 (`ch:encrypted-search` from §16.4 and
§18 references) resolve correctly. No label collisions.

#### Findings (chapter 17)

- **MAJOR** §17.1 line 137-139 and §17.4 lines 185-187 conflate
  Bloom (chapter 5, 9.59 bits/element at $\fprate = 0.01$) with
  BHF (chapter 14, 6.64 bits/element at the same target). The
  §17.4 storage estimate "$\approx 830$ kilobytes" at $n = 10^6$
  comes from BHF arithmetic; the actual Bloom storage is
  $\approx 1.2$ MB. Either rename the construction to "BHF-based
  cipher map" and update the chapter reference, or use Bloom's
  actual 9.59 bits/element rate and update the storage total.
  See Top priority item 2.
- **MAJOR** §17.3 lines 245-256 ("extracting $O(\log n)$
  plaintext bits per query"): the worked example mixes two
  distinct attack scenarios. Sub-claim (a) "After $k$ such
  queries the adversary has recovered the seed" implies a rate
  of $|\text{seed}|/k$ bits per query, independent of $n$.
  Sub-claim (b) "after $\log |A|$ queries the adversary has
  localized the membership status of a specific record" implies
  a rate of $\log_2(|A|) / \log_2(|A|) = 1$ bit per query.
  Neither matches the stated "$O(\log n)$ bits of plaintext per
  query, where $n = |A|$." A reader following the arithmetic
  cannot derive the rate from either sub-claim. Fix: pick one
  attack and derive its rate; or clarify that the rates are for
  different threat models and state each rate separately.
- **MAJOR** §17.5 line 105-109 ("union ... computed by a
  bitwise OR of the encrypted bit arrays, provided the
  encryption scheme is additively homomorphic over the bits"):
  bitwise OR is not "additively homomorphic over the bits".
  Additive homomorphism over $\mathbb{Z}/2$ gives XOR ($a + b
  \mod 2 = a \oplus b$), not OR. Computing encrypted OR
  requires either a multiplicative gate (somewhat-homomorphic
  with at least one multiplication, since $a \lor b = a + b -
  ab$ over reals) or a specialized homomorphic-OR scheme. The
  sentence as written is technically imprecise. Fix: either
  drop the "additively homomorphic" qualifier (and say "for
  schemes that support encrypted bitwise OR") or rewrite to
  say the underlying Bloom-filter array OR uses a scheme with
  the appropriate homomorphism.
- **MINOR** §17.1 line 36-42 (Bloom-filter motivation): the
  motivating paragraph correctly references Bloom filters, but
  the link to chapter 5 §5.2 versus chapter 14 (BHF) is not
  made explicit. A one-clause clarification ("Bloom filters,
  chapter 5; BHF, chapter 14") would prevent the §17.4
  confusion downstream.
- **MINOR** §17.2 line 178-185 (chained cipher-map theorem
  proof sketch): the theorem statement is clear but the proof
  is "the chapter 4 argument" with no derivation. A two-line
  derivation showing the matrix entry $(Q_g Q_f)_{x,z} =
  \sum_y (Q_g)_{x,y} (Q_f)_{y,z}$ explicitly would be cleaner
  than the current "the chapter 4 argument" wave.
- **MINOR** §17.2 lines 198-201 (n-ary generalization): "For
  n-ary cipher maps the theorem reads against
  \Cref{thm:n-ary-kronecker} with $m = 2$ stages instead of
  $m$ independent queries; the algebra is identical." The
  cross-reference to `thm:n-ary-kronecker` is to the multi-
  query (parallel) Kronecker theorem, but chained composition
  is sequential (matrix product), not Kronecker (tensor
  product). The two are different operations; the §17.2
  reference is structurally imprecise. Fix: clarify that
  chained composition uses matrix multiplication; the
  Kronecker product is the multi-query setting.
- **MINOR** §17.3 lines 180-183 ("$m^{1/2}$" sharpening of
  confidence intervals): standard concentration says CI width
  shrinks as $m^{-1/2}$, not "$m^{1/2}$". The text says CIs
  "sharpen as $m^{1/2}$" which could be read as precision
  (inverse-width) growing as $\sqrt{m}$, a defensible reading,
  but the notational convention in the rest of the book is to
  say "$O(m^{-1/2})$" for the width. Aligning with the
  convention would tighten the exposition.
- **MINOR** §17.4 lines 95-97 ("a cipher map with $\fprate =
  \epsilon$ uses about $-\log_2 \epsilon$ bits per element of
  useful information capacity"): the "useful information
  capacity" framing is unusual; the standard reading is that
  $-\log_2 \epsilon$ is the entropy floor for FNR-zero
  approximate sets (chapter 8). A pointer to chapter 8 §8.3
  would tighten the framing.
- **MINOR** §17.6 lines 200-207 (FHE comparison "$10,000\times$
  space and time"): contradicts §17.4's clearer "$10^4$ space
  / $10^9$ time" comparison. The §17.6 line should be
  rewritten to match §17.4's separate space and time ratios,
  or rephrased as "many orders of magnitude" rather than
  collapsing the two ratios.
- **NOTE** §17.3 line 162-176 (multi-query subsection): the
  Kronecker-product framing is correct but compact. A worked
  numerical example (the $m = 10$ query budget already
  appears in ex 17-4; an in-text version would help) would
  ground the abstract claim.
- **NOTE** §17.5 line 90-92 (counting trapdoor set with
  deletions costing $\fnrate > 0$): the brief mention is fine,
  but the trade-off (deletions vs FNR positivity) is not
  derived. The cipher-map paper presumably has the derivation;
  a citation pointer would help.
- **NOTE** §17.6 line 150-159 (storage and confidentiality
  inversely coupled): the surprising claim "lower-storage
  cipher maps are more confidential, not less" is correctly
  derived from PPV + chapter 8 entropy floor, but the
  exposition could be sharper. A small numerical comparison
  (e.g., a cipher map at $\fprate = 0.01$ vs at $\fprate =
  0.1$ in the same column) would make the surprise concrete.

### Chapter 18: Encrypted Search as Relaxed Trapdoor (~27 pp; target ~37 pp)

**spec-auditor:** all eight sections from spec §4 chapter 18 row
present. §18.1 The Encrypted Search Problem (`def:encrypted-search`;
three naive resolutions and why they fail; cipher-map framing as
the fourth resolution); §18.2 Bloom-Filter-Based Constructions
(`def:per-document-bloom`, `def:inverted-index-bloom`; cipher-map
identification; FNR-zero structural property; space and query
cost analysis; worked example at $|D| = 10^4$); §18.3 Confidentiality
Measures (PPV as confidentiality; NPV and F1 round out the picture;
`prop:multi-query-leakage`; worked example at two operating points);
§18.4 Estimation under Adversarial Queries (why iid Chernoff
fails; MAB UCB framing; CI construction; worked comparison at 100
queries/minute for 1 hour); §18.5 A Toy Encrypted Search System
(HMAC tokens; AES-encrypted bit arrays; trace through a single
query; production-tuned retuning; notebook hook); §18.6 Closing
the Book (recaps the five parts and the framework's arc); §18.7
Bibliographic Notes (4 citations: Towell encrypted-search thesis,
Towell ES conf MAB, Song-Wagner-Perrig 2000, Curtmola et al
2006; plus Towell max confidentiality from chapter 17). Learning
outcomes box has three bullets. 11 exercises with 3/5/3
distribution. Chapter is at ~27 pp, ~27% under the spec's 37 pp
target, the §18.1 and §18.6 sections are notably under-budget;
§18.2 and §18.5 are also under but compactly written. The
under-budget reflects the chapter's strategy of building on
chapter 17's machinery without re-deriving it.

**quality-auditor (cold read):** §18.1's three-naive-resolutions
framing (download all, plaintext queries, FHE, and why each
fails) lands the chapter's motivation cleanly and sets up the
cipher-map framing as the fourth resolution. §18.2's two-
construction discussion (per-document vs inverted-index) gives
the right operational alternatives with their respective
trade-offs. The cipher-map identification (both constructions
have $(\fprate, 0)$ error profiles) makes the chapter 17
machinery applicable directly. §18.3's lifting of chapter 7 PPV
into the confidentiality role is clean, and the two operating
points ($\fprate = 0.01$ at PPV = 0.917 vs $\fprate = 0.3$ at
PPV = 0.270) span the trade-off curve concretely. §18.4's MAB
UCB vs iid Chernoff comparison ends with a two-orders-of-
magnitude gap on the same dataset that makes the right rhetorical
impact. §18.5's toy-system trace through a single query exhibits
every framework parameter ($\fprate, \fnrate, \pi, \PPV, C$) at
a concrete operating point, and the production-tuned retuning
section shows the design problem in operational form.

§18.6 "Closing the Book" is the book's final word and deserves
special editorial attention. The structure (atom → sets → maps
and types → constructive optimum → boundary and applications) is
the right organizational summary, hits all five parts in
proportion, and closes with three research directions
(approximate query languages, federated computation, relation to
differential privacy). The section avoids the trap of restating
every chapter's content (which would inflate to many pages); it
hits the headline result of each part in one or two sentences
and lets the reader's accumulated context do the rest. The
"What comes next" subsection is appropriately compact, three
research threads, one sentence each, no overpromising. This is
exactly the closing the book needs.

**math-auditor:** §18.2 Bloom space worked example: $m_d = 1.44
\cdot 50 \cdot \log_2(100) = 1.44 \cdot 50 \cdot 6.6439 = 478.36
\approx 480$ bits per filter (text matches). Total storage:
$10^4 \cdot 480 / (8 \cdot 10^6) = 0.6$ MB (text matches). Exact
word-set storage at $10^4 \cdot 50 \cdot 8 = 4 \times 10^6$
bytes = 4 MB (text matches). §18.2 inverted-index check:
$\sum_d W_d = |W| \cdot |D_w|$ identity holds; storage cost
formula equivalence at leading order checks.

§18.3 PPV worked examples: PPV$(0.01, 0, 0.1) = 0.1 / 0.109 =
0.9174$ (text matches $\approx 0.917$, $C \approx 0.083$).
PPV$(0.3, 0, 0.1) = 0.1 / 0.37 = 0.2703$ (text matches $\approx
0.270$, $C \approx 0.730$). Intermediate points: PPV$(0.05, 0,
0.1) = 0.690$, PPV$(0.1, 0, 0.1) = 0.526$, PPV$(0.2, 0, 0.1) =
0.357$ (text matches all three). Closed-form $\fprate^* = \pi C
/ [(1 - \pi)(1 - C)]$ at $\pi = 0.1, C = 0.9$ gives $1.0$
(degenerate, text matches); at $\pi = 0.01, C = 0.9$ gives
$0.0909$ (text matches $\approx 0.091$).

§18.4 defender stats: Wilson margin $1.96 \sqrt{0.09 \cdot 0.91
/ 6000} = 0.0072$ (text matches). PPV at $\pi_{\max}^{\text{iid}}
= 0.097$ gives 0.915 (text matches), $C \approx 0.085$. MAB UCB
arithmetic: at vocabulary $K = 1000$, joint $\delta = 0.05$
gives per-arm $\delta = 5 \times 10^{-5}$. Clopper-Pearson upper
at $n_w = 6, k_{\text{obs}} = 3, \delta = 5 \times 10^{-5}$ is
$\approx 0.986$, not the stated "$\approx 0.95$", the text
under-states the bound. This is MINOR (the qualitative point
that the bound is "near 1" holds). PPV at $\pi_{\max}^{\text{MAB}}
= 0.95$ gives 0.9995, $C \approx 0.0005$ (text matches
"$\approx 0.001$"). The "log(2 × 10^6) ≈ 14.5" claim checks
($\log_e(2 \cdot 10^6) = 14.51$).

§18.5 single query trace: PPV at $\pi = 0.003, \fpr = 0.01$ is
$0.003 / 0.01297 = 0.2313$ (text matches $\approx 0.231$, $C
\approx 0.769$). Expected FPs: $997 \cdot 0.01 = 9.97$ (text
matches "$\approx 9.97$"). §18.5 retune: $\fpr^* = 0.05 / 0.45 =
0.1111$ (text matches $\approx 0.111$). Filter sizes at $\fpr =
0.111$: $m = 1.44 \cdot 10 \cdot \log_2(9.009) = 45.67$ bits
(text matches $\approx 46$); at $\fpr = 0.01$: $m = 1.44 \cdot
10 \cdot \log_2(100) = 95.67$ bits (text matches $\approx 96$).

**cross-ref-auditor:** all DEFINED labels match `\label{}`
declarations (`sec:encrypted-search-problem`, `def:encrypted-search`,
`sec:bloom-based`, `def:per-document-bloom`,
`def:inverted-index-bloom`, `sec:confidentiality-measures`,
`prop:multi-query-leakage`, `sec:adversarial-estimation`,
`sec:toy-system`, `sec:closing-the-book`, `sec:bib-notes-ch18`,
`ex:ch18-1`-`ex:ch18-11`). All RESOLVED labels exist
(`def:cipher-map`, `def:bloom-filter`, `def:ppv`, `def:npv`,
`def:f1`, `def:perfect-filter-line`, `thm:bloom-optimal-k`,
`thm:composition`, `thm:kronecker`, `thm:chernoff`,
`ax:element-indep`, `sec:bloom-from-scratch`, `sec:union-of-sets`,
`sec:kronecker`, `sec:fhe-sidebar`, `sec:maximizing-confidentiality`,
`sec:trapdoor-paradigm`, `sec:derived-measures`,
`sec:binomial-estimator`, `sec:confidence-intervals`,
`sec:sample-complexity`, `sec:bernoulli-error-model`,
`sec:adversarial-inputs`, all 13 chapter labels from §18.6, plus
chapter 17 §17.6 confidentiality references). No label
collisions. The chapter's status as the book's final chapter
means there are no FORWARD refs to chapters outside the book.

#### Findings (chapter 18)

- **MAJOR** §18.4 MAB UCB Clopper-Pearson interval text: at $n_w
  = 6, k_{\text{obs}} = 3, \delta_{\text{arm}} = 5 \times
  10^{-5}$, the Clopper-Pearson upper bound is $\approx 0.986$,
  not the stated "$\approx 0.95$". This is a real arithmetic
  understatement (text low by ~3.5%). The qualitative point
  (the bound is near 1) holds, but the specific "0.95" is wrong.
  Also: some arms see only $n_w = 1$ query, for which the
  upper bound is even closer to 1. Taking the maximum over arms
  gives $\pi^{\text{MAB}}_{\max}$ close to 1, not 0.95. Fix:
  recompute the Clopper-Pearson upper bound at the stated
  parameters and report the right value, or restate the example
  with parameters that yield the claimed 0.95.
- **MINOR** §18.1 line 116-118 (chapter 4 Kronecker reference
  for multi-query aggregation): "the chapter~4 Kronecker
  composition law (chapter~17 §\ref{sec:bernoulli-error-model})
  tells the client how the per-test error rates aggregate into a
  corpus-wide result." §17.2 covers chained composition (matrix
  product), not multi-query aggregation (Kronecker tensor
  product); §17.3's multi-query subsection is the right
  cross-reference. The §18.1 cite is slightly imprecise.
- **MINOR** §18.2 line 287-289 ("expected number of spurious
  documents returned per query is 0.01 · |D| = 100"): correct
  to within the $\pi$ correction. At $|D| = 10000$ and $\pi =
  0.001$, the non-member count is 9990 and expected FPs are
  9990 · 0.01 = 99.9 ≈ 100. The approximation is fine but the
  $|D|$ vs $|D| - \text{true matches}$ distinction is elided.
- **MINOR** §18.3 lines 184-193 (`prop:multi-query-leakage`):
  "the confidentiality of the worst plaintext bit, measured as
  the number of bits of uncertainty about a single $(w, d_i)$
  pair after $m$ queries, shrinks as $C_m = \Theta(m^{-1/2})$
  in bits." Standard CLT gives posterior gap $\sim m^{-1/2}$ in
  probability units; in bits of entropy this is $\sim m^{-1/2}
  \log m$, not strictly $\Theta(m^{-1/2})$. The statement is
  qualitatively right but the rate "in bits" is imprecise. Fix:
  state the gap in probability units, or use $O(m^{-1/2} \log
  m)$ for the bits.
- **MINOR** §18.4 line 116-119 ("Thompson sampling is the
  Bayesian counterpart"): the comparison to UCB is mentioned but
  not developed; the section then drops back to UCB. A reader
  who comes from the bandit literature would expect either a
  derivation of Thompson's analogous bound or a pointer; the
  one-line mention is too brief to be useful.
- **MINOR** §18.5 line 39 (notebook reference):
  `python/notebooks/ch18-encrypted-search.ipynb` is the
  expected path; verify the notebook actually exists at this
  path with the described content (per the parent's note that
  chapter 18 has a substantive notebook).
- **NOTE** §18.4 line 144-156 (`towell-es-conf-mab` bootstrap
  construction): the construction is introduced as a tighter
  alternative to the union bound but is not derived. The text
  appropriately points to the paper for the derivation; this
  is a deliberate citation rather than a gap.

## Cross-chapter findings

- **MAJOR** Bloom/BHF terminology consistency across §17.1,
  §17.4, §18.2. §17.1 and §17.4 conflate Bloom and BHF (see
  MAJOR finding 2). §18.2 correctly uses the Bloom rate ($1.44
  \log_2(1/\fpr)$ for the per-document filters); the worked
  example arithmetic is the actual Bloom storage. The
  inconsistency is between chapters: §17.4's "Bloom-filter
  cipher map" uses BHF arithmetic; §18.2's Bloom-filter
  constructions use Bloom arithmetic. A reader following §17.4
  into §18.2 sees the bits-per-element jump from 6.64 to 9.59
  with no explanation. Fix: align the §17 terminology with
  §18's actual Bloom use, or rename §17's "Bloom-filter cipher
  map" to "BHF-based cipher map" with corrected chapter
  citations.
- **MINOR** Notation drift: §17.6's confidentiality is $C$;
  §18.3 uses the same $C$. Both use $\pi$ for workload
  prevalence consistently. §16.5 uses $\bar\pi$ for
  time-averaged prevalence, a useful convention but not
  carried into §18.3, where multi-window prevalence is
  discussed without the bar notation.
- **MINOR** Chapter 16's "where the framework still helps"
  rule (§16.5) is good as a synthesis but is not explicitly
  invoked in chapters 17 and 18 even though the trapdoor-
  paradigm setting (§17.3) and the encrypted-search adversarial
  estimation (§18.4) are both natural applications of the
  rule. A one-clause back-reference from §17.3 or §18.4 to
  §16.5 would tighten the part's internal coherence.
- **NOTE** Part V is overall ~83 pp at the chapter counts
  (Ch 16 ~25, Ch 17 ~31, Ch 18 ~27) against the design
  spec's ~110 pp target, about 25% under. The under-budget is
  consistent across all three chapters and across all
  sections within each, reflecting compact prose rather than
  missing content. The §16.7, §17.8, §18.7 bibliographic notes
  are uniformly under target (the section style is one
  paragraph per citation cluster, which is the right style at
  the right length). Total book body: Parts I-IV (~434 pp) +
  Part V (~83 pp) = ~517 pp, against master spec's ~500 pp
  target (+3.4% over).

## Documented deferred items (not flagged)

- `ch:composition` (chapter 4 → chapter 6 slug mismatch).
- `ch:sketches` x 5 in chapter 9 (chapter 10's label is
  `ch:sketches-estimators`).
- `sec:noisy-bit` x 2 in chapter 17 (ch1's labels are
  `sec:quantifying-noise` / `sec:sampling-rates`).

## Triage (suggested action by severity)

### MAJOR (should be addressed before integration sign-off)

1. §16.6 lines 49-50 "Part~VI" → "Part~V" (two occurrences;
   trivial typo fix but visible at chapter-close).
2. §17.1 and §17.4 Bloom vs BHF conflation (rename and/or
   correct formula and storage arithmetic).
3. §16.2 worked example "Bloom past capacity" numerical
   parameters (fill ratio 30% vs 51.8%, rate "0.5 late" vs
   0.83, trajectory expectation 230 vs computed values).
4. §17.3 worked example "$O(\log n)$ bits per query" two
   sub-claims with different scalings (clarify which attack
   model is meant or state both rates separately).
5. §17.5 line 105-109 "additively homomorphic" qualifier for
   bitwise OR (technically imprecise).
6. §18.4 Clopper-Pearson "0.95" understatement (recompute to
   0.986 or restate with parameters yielding 0.95).
7. Cross-chapter §17 vs §18.2 Bloom rate inconsistency (depends
   on resolution of MAJOR 2).

### MINOR (polish-pass material)

- §16.1 line 49-50 (cite-target check vs chapter 1 §1.4).
- §16.2 line 88 (variable overload $t$ for fill count vs query
  index).
- §16.2 line 138-140 (chapter 11 MGF citation; name the result).
- §16.3 line 174 ("trivially" in math-handwave position).
- §16.3 line 220-230 (negative correlation salvage, example
  needed).
- §16.4 line 213-218 ("0.013 within rounding" should be "0.01
  within rounding").
- §17.1 line 36-42 (clarify Bloom = ch 5 vs BHF = ch 14
  citation; will fix MAJOR 2 with a pointer).
- §17.2 line 178-185 (proof sketch derivation more explicit).
- §17.2 lines 198-201 (n-ary generalization cross-reference
  precision: chained vs multi-query is different operations).
- §17.3 lines 180-183 ($m^{1/2}$ vs $m^{-1/2}$ convention).
- §17.4 lines 95-97 (cite chapter 8 §8.3 entropy floor).
- §17.6 lines 200-207 (FHE space and time ratio inconsistency
  with §17.4).
- §18.1 line 116-118 (§17.2 vs §17.3 cross-reference precision).
- §18.2 line 287-289 (FP count $|D|$ vs $|D| - \text{true}$).
- §18.3 lines 184-193 ($\Theta(m^{-1/2})$ in bits imprecise).
- §18.4 line 116-119 (Thompson sampling brief mention).
- §18.5 line 39 (verify notebook exists at stated path).
- Cross-chapter notation drift on $\bar\pi$ (§16.5).

### NOTE (defer to a future revision or leave as-is)

- §16.4 lines 246-248 (targeted attacker $O(1)$ work claim).
- §16.5 lines 117-125 (Kronecker geometry for time-varying
  rates).
- §17.3 line 162-176 (multi-query subsection, worked example
  in body would help).
- §17.5 line 90-92 (counting trapdoor set with deletions).
- §17.6 line 150-159 (storage-confidentiality coupling
  surprise).
- §18.4 line 144-156 (`towell-es-conf-mab` bootstrap
  construction).
- Cross-chapter back-reference from §17.3 or §18.4 to §16.5.

## Specialist verdicts (consolidated)

- **spec-auditor:** Part V PASS. All content checklist items
  from spec §4 chapters 16-18 rows are realized. The three
  chapters land the design spec's organizational intent
  (boundary → cryptographic algebra → encrypted-search
  application) and §18.6 closes the book per success criterion
  5. Chapter 16 hits 8/8 checklist items at ~81% of budget;
  chapter 17 hits 9/9 at ~82% of budget; chapter 18 hits 8/8
  at ~73% of budget. The total ~83 pp against ~110 pp target
  is consistent with the chapters' strategy of building on
  prior parts' machinery without re-deriving it. Spec §10
  success criteria 1, 2, 3, 4, 5 all met (reader can finish
  Part V in three focused weeks; chapter 16 cashes the
  deferrals; chapter 17 connects to cryptography via clean
  cipher-map definition; chapter 18 demonstrates a working
  encrypted-search construction; §18.6 closes the book with
  a satisfying recap).
- **quality-auditor:** "minor polish" for chapter 18; "minor
  polish" for chapter 17; "minor polish" for chapter 16. No
  BLOCKING findings in any chapter. Chapter 18's §18.6
  Closing the Book is publication-ready and lands the book's
  final word cleanly. Chapter 17's pedagogical structure is
  solid but the Bloom/BHF conflation (MAJOR 2) and the
  $O(\log n)$ worked example (MAJOR 4) require focused
  revision. Chapter 16's worked-example arithmetic (MAJOR 3)
  and Part V/VI typo (MAJOR 1) are the highest-priority
  fixes. The pedagogical voice is consistent across all
  three chapters; the issues are content-level, not
  voice-level.
- **math-auditor:** PASS with corrections. Every numerical
  claim in chapters 17 and 18 checked verifies independently
  (§17.2 matrix product, §17.5 cancellation, §17.6 PPV
  worked examples, §18.2 storage, §18.3 PPV at five fpr
  values, §18.4 Wilson margin, §18.5 single-query trace,
  §18.5 retune). Two substantive arithmetic issues: §16.2's
  worked example parameters are internally inconsistent
  (MAJOR 3) and §18.4's Clopper-Pearson "0.95" is wrong
  (MAJOR 6). The §17.3 $O(\log n)$ claim is hand-waved
  rather than mathematically wrong (MAJOR 4). The §17.4
  Bloom-vs-BHF conflation (MAJOR 2) means the §17.4 worked
  example arithmetic is right (it's BHF), but the labeling
  is wrong.
- **cross-ref-auditor:** PASS. All DEFINED labels match
  declarations; no collisions in Part V or against the rest
  of the book tree. All RESOLVED labels exist. The
  forward refs in §16.4 to chapters 17-18 now resolve
  correctly. The book.log undefined references
  (`ch:composition` x 1, `ch:sketches` x 5, `sec:noisy-bit`
  x 2) are entirely in the documented deferred baseline.
  No new undefined references introduced by Part V.

## Overall recommendation

Part V is publication-ready in structure, scope, and overall
prose quality. The three chapters land Part V's organizational
intent cleanly: chapter 16 catalogues the framework's boundary,
chapter 17 lifts the algebra to the cryptographic setting via
cipher maps, and chapter 18 demonstrates the framework on a
working application. §18.6 Closing the Book lands the book's
final word with the right balance between recap and brevity.

The seven MAJOR findings cluster around two themes:
(1) Bloom-vs-BHF terminology confusion in §17.1 and §17.4 that
propagates a 30% error in the §17.4 storage worked example,
and (2) miscellaneous arithmetic and typographic issues in
specific worked examples (§16.2 Bloom past capacity, §17.3
adaptive adversary, §18.4 MAB UCB Clopper-Pearson). The Part~VI
→ Part~V typo in §16.6 is the most visible single fix and the
cleanest to apply.

The 16 MINOR findings include cross-reference precision items,
notation drift, and polish-pass material that would benefit
from a final read but does not affect integration sign-off.
The 8 NOTE items are deferrals to future revisions or items
that work as-is for the chapter's pedagogical purpose.

Chapter 18's §18.6 deserves the editorial care it received:
the section avoids the trap of restating every chapter while
hitting all five parts in proportion, the "what comes next"
research-directions paragraph is appropriately compact, and
the final sentence ("the book closes with the framework in a
state that admits the extensions but does not require them")
lands the closing tone correctly. No BLOCKING or MAJOR
findings in §18.6.

Part V meets all five spec §10 success criteria. The book is
ready for an integration pass once the MAJOR findings are
addressed; the MINOR findings are appropriate polish-pass
material for the final pre-submission review.
