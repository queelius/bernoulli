# Part IV Review (chapters 14-15)

Date: 2026-05-29
Reviewer: bookwright reviewer orchestrator (Part IV scope)
Auditors applied: spec, quality, math, cross-ref (per-chapter, inline)

This review evaluates both chapters of Part IV ("Optimality and
Construction") of *Bernoulli Types: An Algebra of Approximate
Computation* against the Part IV design spec
(`docs/superpowers/specs/2026-05-25-bernoulli-textbook-part4-design.md`)
and the master spec
(`docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`). The
four auditor roles were applied per chapter and the findings are
synthesized below by chapter and by cross-chapter coherence. The
documented deferred items (`ch:composition` x 1, `ch:sketches` x 5,
`sec:noisy-bit` x 2) match `book/book.log` exactly and are not flagged.

## Summary

- **Total findings: 27** (1 BLOCKER, 6 MAJORs, 12 MINORs, 8 NOTEs).
- **Top high-priority items:**
  1. (BLOCKER) §15.2 FNR derivation is internally inconsistent
     (`chapters/ch15/bphf-construction.tex` lines 218-247). The text
     states that the per-member rank-collision probability is "at most
     $\binom{n}{2} \cdot 2^{-r} \approx n^2 \cdot 2^{-r-1}$ in the
     worst case." This is mathematically wrong as a per-member
     probability bound: $\binom{n}{2} \cdot 2^{-r}$ is the *expected
     number of colliding pairs* across the whole set, not the
     per-member probability. The correct per-member union bound is
     $(n-1) \cdot 2^{-r}$. Worse, at $r = \lceil \log_2 n \rceil$
     (the chapter's standard choice), both forms are $\Theta(1)$ or
     larger, not $2^{-r}$, so the headline bound
     $\fnrate \le 2^{-r}$ at \eqref{eq:bphf-fnr} does *not* follow
     from rank-collision arguments alone. Ex 15-9 (lines 210-240)
     explicitly confirms this: "the exact FNR is approximately $0.5
     \cdot (1 - e^{-1}) \approx 0.32$, much larger than the headline
     upper bound $2^{-r} \approx 1/n$ would suggest, unless a
     second-stage discriminator is added." The chapter's main text
     mentions the second-stage discriminator in one sentence (lines
     229-233) and treats the combined bound as established, but the
     combination is not derived. The pseudocode `alg:bphf-build-query`
     does *not* include the discriminator; the headline bound is not
     supported by the construction as stated.
  2. (MAJOR) §15.2 $\fprate = 0$ argument is hand-waved
     (`chapters/ch15/bphf-construction.tex` lines 184-209). The text
     says "the construction adds a build-time discriminator (a longer
     hash, a residue check, or a stored bit marking ...)
     pre-excluding any colliding non-member at build time and pushing
     the residual non-member acceptance probability to zero." But
     the construction in \Cref{def:bphf} and the pseudocode in
     \Cref{alg:bphf-build-query} only show a rank-equality check
     $R[\phi(x)] = \rho(x)$, which under a uniform $\rho$ gives FPR
     $= 2^{-r}$, exactly like the BHF, not 0. The discriminator that
     converts FPR to 0 is named but never specified. The chapter's
     headline $\fprate = 0$ guarantee is therefore not delivered by
     the construction as presented; a reader who implements
     \Cref{alg:bphf-build-query} verbatim would get the BHF, not the
     BPHF. A proper construction (e.g., storing $\lceil \log_2 n \rceil$
     identifier bits per slot so the rank is checked against an
     independent identifier of the slot's true member, or using a
     full-precision rank that is the slot's true rank by definition)
     needs to be specified, or §15.4's sort-position-based $\rho$
     should be promoted to the canonical construction in §15.2.
  3. (MAJOR) §15.2 / §15.4 inconsistency about what $\rho$ is at
     query time. §15.2 (lines 91-103, 184-200) treats $\rho$ as a
     function the query "can recompute for any candidate $x$, member
     or not, by direct evaluation" (line 99-100), implying $\rho$ is
     a hash. §15.4 (lines 79-92) uses the *sort-position rank* as
     $\rho$, which is only defined on the corpus $A$ (a non-member
     has no sort position). The query algorithm
     \textsc{TopK}$(a) = \textsc{Query}(a) \land R[\phi(a)] < k$
     (line 100) requires evaluating $\rho(a)$, but for an unknown ID
     this is undefined. Either §15.2 needs to admit two rank-source
     regimes (hash-based and application-defined), or §15.4 needs to
     specify how the application restricts queries to known IDs (and
     in that case the FPR = 0 guarantee becomes a trivial consequence
     of input restriction, not the construction).

- **Chapters with most findings:** Chapter 15 (16), Chapter 14 (8),
  cross-chapter (3).

Overall the chapters are in mostly solid shape on the BHF side
(chapter 14), but the BPHF side (chapter 15) has substantive
exposition problems around the $\fprate = 0$ and $\fnrate \le 2^{-r}$
guarantees. Every numerical claim in chapter 14 and most numerical
claims in chapter 15 verified independently with Python checks. The
§14.2 worked example numbers ($n = 1000, \fprate = 0.01$ gives $r = 7$
fingerprint bits, fingerprint table $7000$ bits, BHF total $\approx
9000$ bits at $n = 1000$ with $2-3$ bits perfect-hash overhead, Bloom
at same target $\approx 9586$ bits) all check exactly. The §14.3
comparison table at $n = 10^6$ gives floor $\{6.64, 9.97, 19.93\}$,
Bloom $\{9.59, 14.38, 28.76\}$, BHF $\{7, 10, 20\}$ for $\fprate \in
\{10^{-2}, 10^{-3}, 10^{-6}\}$, all of which check. The §14.4
worked verification at $r = 7$ gives $2^{-7} = 0.0078125$ with
over-achievement $1 - 2^{-0.356} = 0.219$ ($\approx 22\%$ below the
$0.01$ target), all checking. The §14.5 BHF/Bloom space ratio
asymptote $1/\log_2 e \approx 0.693$ checks. The §15.2 worked example
at $n = 1000$ gives $r = 10$, $n \cdot r = 10000$ bits, $\fnrate \le
2^{-10} \approx 0.001$, all checking arithmetically (subject to the
BLOCKER above on whether the bound actually holds). The §15.3
crossover at $\fprate = 1/n$ checks. The §15.4 worked example at $n =
10^6, k = 100, r = 20$ gives $\fnrate \le 2^{-20} \approx 9.5 \times
10^{-7}$, expected misses $\le 100 \cdot 9.5 \times 10^{-7} = 9.5
\times 10^{-5}$, all checking.

No em-dashes (U+2014 or ASCII `---`). No "easy to see", "obviously",
"clearly", "trivially". No banned phrases from the soul-voice
hook's list. No label collisions. The seven section labels and
equation/algorithm/
proposition/theorem labels in each chapter are unique to those
chapters. All RESOLVED labels referenced from these chapters
(`def:bloom-filter`, `alg:bloom-insert-query`, `thm:entropy-floor`,
`sec:entropy-floor`, `prop:bloom-overhead`, `sec:bloom-gap`,
`def:perfect-filter-line`, `sec:perfect-filter-line`,
`prop:fpr-zero-closure`, `def:one-sided`, `def:bhf`,
`sec:bhf-construction`, `alg:bhf-insert-query`, `thm:bhf-optimality`,
`prop:bhf-fpr`, `sec:space-analysis`, `sec:fpr-analysis`,
`sec:construction-time`, plus chapter 16 stub `ch:not-bernoulli`)
resolve correctly in the book tree.

The findings below are sorted by severity within each chapter, then
by location.

## Findings by chapter

### Chapter 14: Optimal Bernoulli Sets (BHF) (~31 pp; target ~30 pp)

**spec-auditor:** all checklist items per spec §4 chapter 14 row are
realized. Seven sections (§14.1 The Optimality Question, §14.2 The
BHF Construction with `def:bhf` and `alg:bhf-insert-query`, §14.3
Space Analysis with `thm:bhf-optimality`, §14.4 False-Positive Rate
Analysis with `prop:bhf-fpr`, §14.5 Construction Time and Trade-offs
with `tab:bhf-bloom-tradeoffs`, §14.6 Bridge, §14.7 Bibliographic
Notes). Learning outcomes box has three bullets per spec format. 11
exercises with 3/5/3 difficulty distribution. Chapter is at ~31 pp,
right on the spec's 30 pp target.

**quality-auditor (cold read):** §14.1 motivates the construction
cleanly by recalling the chapter 8 entropy floor and Bloom gap, then
naming the four properties any constructive answer must deliver
(FNR-zero, FPR $\le \fprate$, near-floor bit budget, fast query) and
sketching the BHF as the answer. §14.2's two-ingredient framing
(perfect hash $\phi$ for addressing, fingerprint $g$ for
discrimination) reads cleanly; the contrast with Bloom (Bloom moves
collisions to query-time conjunction; BHF resolves collisions at
build time so the query is a single $r$-bit comparison) is the right
pedagogical hook. §14.3's space proposition $L_{\text{BHF}}/n =
\lceil -\log_2 \fprate \rceil + o(1)$ is stated clearly and contrasted
with Bloom's $\log_2 e$ multiplicative overhead. §14.4's two-case
analysis ($\phi(x)$ in or out of $\phi(A)$) is short and complete.
§14.5's trade-off table makes the static-vs-streaming distinction
explicit, and §14.6 bridges to chapter 15 without overpromising.

**math-auditor:** verified all numerical claims independently. §14.2
worked example $n = 1000, \fprate = 0.01$: $r = \lceil 6.644 \rceil =
7$, fingerprint table $= 7000$ bits $= 875$ bytes; perfect-hash $2-3$
bits/element gives total $\approx 9000$ bits ($1125$ bytes) as stated.
Bloom at same target: $m = 1000 \cdot 6.644 \cdot 1.4427 = 9585$ bits,
text says "$\approx 9586$" matches. §14.2 second worked example
$\fprate = 10^{-6}$: floor $19.93$, Bloom $28.76$, BHF $20$ at $n =
10^6$, absolute savings $8.76$ bits per element $= 1.095$ megabytes
across the set, all check. §14.3 comparison table: floor $\{6.64,
9.97, 19.93\}$, Bloom $\{9.59, 14.38, 28.76\}$, BHF $\{7, 10, 20\}$
all check. §14.3 additive overhead $\lceil -\log_2 \fprate \rceil -
(-\log_2 \fprate)$ at the three rates: $\{0.36, 0.03, 0.07\}$ all
match the text. §14.4 worked verification at $r = 7$: $2^{-7} =
0.0078125$, over-achievement factor $0.7812$, $1 - 2^{-0.356} =
0.219$ matches the text's $22\%$. §14.5 query cost $k = \ln 2 \cdot
\log_2(1/\fprate)$ at $\fprate = 0.01$ gives $k \approx 4.6$ (text:
"$\approx 4.6$"); at $\fprate = 10^{-6}$ gives $k \approx 13.8$
(text: "$k \approx 14$"); the $0.347$ factor for $(m/n) \ln 2 / 2$
checks ($\ln 2 / 2 = 0.3466$).

Exercise math: ex 14-1 ratios $\{0.781, 0.977, 0.954\}$ match
$\{2^{-7}/0.01, 2^{-10}/0.001, 2^{-20}/10^{-6}\}$ exactly. Ex 14-2:
$n = 10^6, \fprate = 0.001$ gives BHF $10^7$ bits ($1.25$ MB), Bloom
$1.44 \times 10^7$ bits ($1.80$ MB), savings $0.55$ MB ($30\%$), all
check. Ex 14-6: $\fprate = 0.06$ gives $r = 5$, $2^{-5} = 0.03125$,
ratio $0.521$, wasted bits $0.94$ per element, $\approx 115$ KB at
$n = 10^6$. Ex 14-7: BDZ formula at $n = 10^6$ gives $\log_2 \log_2
\log_2 n / \log_2 n = 2.11/19.93 = 0.106$, matching the text's
"approx $0.1$"; at $n = 10^9$ gives $2.29 / 29.9 = 0.077$, matching
"approx $0.076$". Ex 14-10: dynamic BHF $0.1$ threshold, overhead is
$0.1 \cdot 6.644 \cdot 1.443 / 7 = 13.7\%$, matching the text's
"$14\%$ space overhead".

**cross-ref-auditor:** all DEFINED labels match `\label{}`
declarations. All RESOLVED labels exist
(`def:bloom-filter`, `alg:bloom-insert-query`, `thm:entropy-floor`,
`sec:entropy-floor`, `prop:bloom-overhead`, `sec:bloom-gap`,
`def:perfect-filter-line`, `sec:perfect-filter-line`). The forward
ref `\Cref{ch:not-bernoulli}` at §14.4 line 209 resolves to chapter
16's stub label. No label collisions across the book tree.

#### Findings (chapter 14)

- **MINOR** §14.1 line 80 ("structure is one specific design among
  many. \Cref{sec:bloom-gap}"): the sentence claims §8.4 "ended by
  isolating the three Bloom design choices ... and by remarking that
  abandoning at least one of the three is necessary to close the
  gap." The current §8.4 in chapter 8 (lines varying) does cover the
  three choices and mentions the constructive question; the framing
  is accurate but the back-reference is to text that is more of a
  preview than an analytical conclusion. The §14.1 phrasing
  ("isolating ... three choices" and "remarking ... necessary") makes
  the §8.4 content sound more formal than it is. A softer
  back-reference (e.g., "as §8.4 observed in its closing paragraphs")
  would match the chapter 8 content better.
- **MINOR** §14.2 line 320 (worked example "at $n = 10^6$ ... BHF
  runs at approximately $7$ bits per element against the Bloom
  filter's $9.59$"): the comparison is accurate. The transition
  sentence "the perfect-hash overhead per element shrinks well below
  one bit and the BHF runs at approximately $7$ bits per element"
  glosses over that the BHF's total cost at $n = 10^6$ is closer to
  $r + 0.1$-to-$0.5$ bits per element (per ex 14-7's formula and
  practical implementations), not exactly $r$. The "well below one
  bit" is correct but the next phrase could be clearer that the
  comparison is "$r$" (the fingerprint-table dominant term) vs Bloom.
- **MINOR** §14.4 line 200 ("Universal hashing in the sense of
  \textcite{carter-wegman-1979} delivers pairwise independence by
  construction"): the Carter-Wegman 1979 paper introduced
  $2$-universal families with collision probability $\le 1/m$ over
  the family's random selection, but the relationship between
  "$2$-universal" and "pairwise independent" is subtle (the former
  is a weaker condition, sufficient here but not identical). The
  prose treats them as synonymous; a careful reader cross-checking
  with the literature will notice the slight conflation. One
  sentence distinguishing "$2$-universal" from "pairwise independent"
  would help.
- **MINOR** §14.4 line 217 (worked verification at $r = 7$): the
  prose ends with "the construction is correct for the target: every
  non-member query has at most a $0.78\%$ chance of returning a
  false positive, well under the $1\%$ target the designer set."
  This is the per-query non-member FPR. A reader who interprets FPR
  as "expected number of false positives per non-member query" gets
  the right answer; a reader who interprets FPR as "expected number
  of false positives over all queries including members" needs to
  notice that members all return $\top$ correctly (FNR = 0). The
  phrasing is technically correct but could clarify the conditioning.
- **MINOR** §14.5 line 220 ("the Bloom filter's per-element constant
  is much smaller (a few hash evaluations and bit-writes, no
  randomized retries)"): the comparison is fair but the
  characterization "much smaller" hides that the BHF's per-element
  build cost at, say, $n = 10^6$ is dominated by the $O(n)$
  perfect-hash construction, which amortizes to constant time per
  element under expectation. The Bloom filter does $k$ hash
  evaluations per insertion. At $\fprate = 10^{-6}$ where $k \approx
  14$, the Bloom filter does roughly $14$ hash evaluations per
  insertion, the BHF does roughly $1$ (the amortized share of the
  perfect-hash construction) plus the $1$ fingerprint write. The
  BHF's per-element constant is *smaller*, not larger, once
  amortization is accounted for; the "much smaller for Bloom" claim
  is wrong on the per-element axis. The Bloom *insertion* (post-build,
  streaming) cost is smaller; the *build* cost per element is
  comparable or smaller for the BHF.
- **NOTE** §14.5 line 218 "Modern displacement-based implementations
  achieve sustained construction throughputs on the order of $10$ to
  $50$ million elements per second on commodity hardware": the
  citation is to §14.7 bibliographic notes but the specific
  throughput claim is not in any cited paper. The number is
  plausible (BBHash benchmarks run in this range) but the chapter
  could either back the claim with a citation or soften to
  "implementations report throughputs on the order of millions of
  elements per second".
- **NOTE** §14.6 line 88-89 (claim that the BPHF is "the BHF for the
  complement, modulo the practical detail that the complement is
  usually infinite"): this is a useful framing but the §14.6 prose
  presents it as if the duality is exact. The duality between
  FNR-zero and FPR-zero arms of the perfect-filter line *is*
  symmetric at the type level (chapter 6 §6.4), but the specific
  claim that "the BPHF for $A$ is the BHF for $\Universe \setminus
  A$" is precise only when the complement is finite and small; for
  infinite universes the dual construction requires a different
  trick. The §14.6 sentence overstates the cleanness of the
  duality; chapter 15 §15.1 says the same thing more carefully.
- **NOTE** §14.7 bibliographic notes line 105-107 (cuckoo filter
  "approximately $1.05$ to $1.3$ times the entropy floor depending
  on load factor"): the published cuckoo-filter analyses (Fan et al
  2014) give a slightly different range ($1.07$ to $1.23$ in the
  paper's tables); $1.3$ overstates the upper end. Minor
  discrepancy; not load-bearing.

### Chapter 15: Perfect Hash Filters (BPHF) (~25 pp; target ~28 pp)

**spec-auditor:** all six sections present per spec §4 chapter 15
row. §15.1 From BHF to BPHF (recall, opposite axis, construction
sketch, roadmap); §15.2 The BPHF Construction with `def:bphf` and
`alg:bphf-build-query`; §15.3 Space and Time Analysis with
`prop:bphf-space` and the BHF/BPHF comparison table at $n = 10^6$;
§15.4 Ranked Search Application with `prop:bphf-ranked-search` on
expected misses; §15.5 Bridge to Part V; §15.6 Bibliographic Notes.
11 exercises with 3/5/3 distribution. Chapter is at ~25 pp, below
the spec's 28 pp target by ~11%. The under-budget is consistent with
the chapter 15 narrative compression that Plan 15 anticipated
("Chapter 15 narrative will not need to redevelop the machinery; it
will reuse the chapter 14 derivation with the error-mode swap").

**quality-auditor (cold read):** the chapter has structural issues
on its two headline guarantees ($\fprate = 0$ and $\fnrate \le
2^{-r}$). The §15.1 framing is clean (the FPR-zero arm as the dual of
the FNR-zero arm) but §15.2's construction does not actually deliver
either guarantee as stated. The construction shown is a rank-equality
check $R[\phi(x)] = \rho(x)$, which under uniform $\rho$ has FPR =
$2^{-r}$ (same as the BHF), not 0. The text mentions in passing that
"the construction adds a build-time discriminator (a longer hash, a
residue check, or a stored bit ...) pre-excluding any colliding
non-member at build time" (lines 202-205), but the discriminator is
not in the definition, not in the pseudocode, and not in the FNR
analysis. The exercises (especially ex 15-9) explicitly confront this
gap: ex 15-9(c) says "the exact FNR is approximately $0.5 \cdot (1 -
e^{-1}) \approx 0.32$, much larger than the headline upper bound
$2^{-r} \approx 1/n$ would suggest, unless a second-stage
discriminator is added." This exercise should not be discovering a
gap in §15.2's analysis; the gap should be closed in §15.2.

§15.3's space comparison and crossover analysis are clean. §15.4's
ranked-search application introduces a different rank function (sort
position rather than a hash), which changes the construction's
character but is presented as the "canonical application" rather than
an alternative construction.

**math-auditor:** verified all numerical claims (subject to the
caveat about the FNR bound's derivation). §15.2 worked example $n =
1000$: $r = \lceil 9.966 \rceil = 10$, rank table $= 10000$ bits =
$1250$ bytes; total $\approx 12000$ to $13000$ bits with perfect-hash
overhead. $\fnrate \le 2^{-10} = 0.000977$ all checks arithmetically.
§15.3 BPHF $r = \lceil \log_2 10^6 \rceil = 20$, table at $n =
10^6$: BHF/BPHF ratios $\{20/7, 20/10, 20/20\} = \{2.86, 2.00, 1.00\}$
all check. Crossover at $\fprate = 1/n$ is correct (setting $\lceil
-\log_2 \fprate \rceil = \lceil \log_2 n \rceil$ gives $\fprate =
1/n$ up to ceiling effects). §15.4 worked example $n = 10^6, k = 100,
r = 20$: $2^{-20} = 9.537 \times 10^{-7}$, expected misses $9.537
\times 10^{-5}$, "less than one missed top-ranked document per
$10000$ queries" matches ($10000 \cdot 9.537 \times 10^{-5} = 0.95
< 1$). Storage at $n = 10^6, r = 20$: $20 \times 10^6$ bits $= 2.5$
MB (decimal MB) matches the text; $2.384$ MiB (binary MiB) would
also fit "comfortably in L3 cache". §15.4 BPHF vs full sorted index:
BPHF $= 2.5$ MB; sorted index with $32$-bit pointers $= 6.5$ MB;
sorted index with $64$-bit pointers $= 10.5$ MB; ratios $2.6$ to
$4.2$ match the text's "factor of $2$ to $4$".

Exercise math: ex 15-1: $r = 20$, $n \cdot r = 2 \times 10^7$ bits
$= 2.5$ MB matches. Ex 15-2: $r = 10$, $2^{-10} = 0.000977$, "count
per ten thousand member queries" = $10000 \cdot 2^{-10} = 9.77$,
matches if we read "count" as expected count. Ex 15-4: $r =
\lceil \log_2 10000 \rceil = 14$, $2^{-14} = 6.10 \times 10^{-5}$
matches the text's "$\approx 6.1 \times 10^{-5}$". Ex 15-5: $k = 50,
r = 16$, $k \cdot 2^{-16} = 7.63 \times 10^{-4}$, $1/7.63 \times
10^{-4} \approx 1311$ queries per expected miss. Ex 15-9: $n/2^r$ at
$r = \lceil \log_2 n \rceil = 20, n = 10^6$ gives $0.954$, $1 -
e^{-0.954} = 0.615$ (text uses approximation $n \approx 2^r$ giving
$1 - e^{-1} = 0.632$), combined with $1/2$ tie-break gives $0.31$
(text: "$\approx 0.32$"). All checks.

**cross-ref-auditor:** all DEFINED labels match declarations; no
collisions. Two header-block staleness issues: `bridge-to-part5.tex`
line 20 lists `\Cref{ch:bhf}` in its ALREADY DEFINED section, but
`ch:bhf` is not a label in the book tree (chapter 14's label is
`ch:optimal-bernoulli-sets`); the body of `bridge-to-part5.tex` does
not actually reference `\Cref{ch:bhf}`, so this is a stale header
comment, not a real bug. Similarly `exercises.tex` line 21 lists
`\Cref{ch:bhf}` in its RESOLVED section; the body uses prose form
"chapter~14". All RESOLVED labels exist (`def:bloom-filter`,
`def:one-sided`, `def:perfect-filter-line`, `prop:fpr-zero-closure`,
`thm:entropy-floor`, `def:bhf`, `sec:bhf-construction`,
`alg:bhf-insert-query`, `thm:bhf-optimality`, `prop:bhf-fpr`). The
forward `\Cref{sec:bphf-construction}` etc. all resolve in-chapter.

#### Findings (chapter 15)

- **BLOCKER** §15.2 lines 218-247 FNR derivation. The text claims
  "per-member collision probability is at most $\binom{n}{2} \cdot
  2^{-r} \approx n^2 \cdot 2^{-r-1}$ in the worst case", which (a)
  is the wrong quantity ($\binom{n}{2} \cdot 2^{-r}$ is the
  expected number of colliding pairs over the whole set, not the
  per-member probability) and (b) evaluates to $\Theta(n/2)$ at
  $r = \lceil \log_2 n \rceil$, much larger than $2^{-r}$. The
  headline bound $\fnrate \le 2^{-r}$ at \eqref{eq:bphf-fnr} cannot
  be derived by "combining" this rank-collision term with the
  second-stage discriminator's $2^{-r}$ contribution; the
  rank-collision term dominates and is not $2^{-r}$. Ex 15-9
  explicitly catches the gap and quotes the actual exact FNR as
  $\approx 0.32$ "much larger than the headline upper bound ... unless
  a second-stage discriminator is added." Fix: either (a) rewrite
  §15.2's derivation to make the discriminator a first-class object
  in the construction, in which case the per-member miss probability
  is genuinely $\le 2^{-r}$ from the discriminator alone; or (b)
  use an alternative construction where $\rho(a)$ is the slot's
  identifier (full $r = \lceil \log_2 n \rceil$ bits, no collisions
  among members possible by injectivity), in which case the
  "second-stage" is just storing the identifier itself and the FNR
  bound is $0$ for the rank-collision component and the surviving
  $\fnrate$ comes from a separate mechanism the chapter would need
  to identify. The current text falls between the two and gives a
  bound that the construction does not deliver.
- **MAJOR** §15.2 lines 184-209 $\fprate = 0$ argument. The
  construction shown in \Cref{def:bphf} stores $\rho(a)$ at slot
  $\phi(a)$ and the query compares $R[\phi(x)] = \rho(x)$. Under a
  uniform $\rho$, this is the BHF analysis verbatim: $\fprate \le
  2^{-r}$ from \Cref{prop:bhf-fpr}, not $0$. The §15.2 text says
  "the construction adds a build-time discriminator ...
  pre-excluding any colliding non-member at build time and pushing
  the residual non-member acceptance probability to zero" (lines
  202-205), but the discriminator is mentioned in one sentence and
  never made part of the construction. The pseudocode does not show
  it. The query algorithm does not check it. A reader who implements
  \Cref{alg:bphf-build-query} verbatim gets a structure with FPR
  $= 2^{-r}$, identical to the BHF, which is exactly the chapter 14
  construction (the rank table is just a renamed fingerprint table).
  Fix: either specify the discriminator concretely (e.g., as a
  separate stored bit per slot identifying "this rank is genuine vs
  a non-member collision", with build-time check that no
  non-member's $\rho$ collides with the slot's rank), or replace
  \Cref{def:bphf} with the §15.4 construction where $\rho$ is the
  sort-position rank (defined only on $A$), in which case the FPR =
  0 follows from the rank function being undefined on non-members
  (the query restricted to known IDs returns the rank correctly;
  unknown IDs cannot be queried meaningfully). The current §15.2
  reads as both constructions at once and delivers neither cleanly.
- **MAJOR** §15.2 vs §15.4 inconsistency about $\rho$'s domain.
  §15.2 line 99-100 says the rank assignment can be "a secondary
  hash truncated to $r$ bits", which gives a $\rho : \Universe \to
  \{0, \ldots, n-1\}$ defined on the whole universe. §15.4 lines
  82-92 then uses the sort-position rank $\rho : A \to \{0, \ldots,
  n-1\}$, defined only on $A$. The two are different objects with
  different properties; the chapter does not flag the difference.
  The query algorithm $\textsc{Query}(x)$ from \Cref{alg:bphf-build-query}
  reads $R[\phi(x)]$ and compares to $\rho(x)$. For the hash $\rho$,
  $\rho(x)$ is always defined and the comparison is meaningful. For
  the sort-position $\rho$, $\rho(x)$ is undefined for $x \notin A$
  and the comparison is impossible (the application must restrict
  queries to known IDs, but that turns the FPR = 0 guarantee into a
  consequence of input restriction). Resolution: either §15.2 should
  pick one rank-source regime and §15.4 should use it consistently,
  or §15.2 should explicitly admit two regimes and §15.4 should
  state which it uses.
- **MAJOR** §15.2 line 167-173 (the proposition vs the BHF formula
  comparison): the proposition `prop:bphf-space` says BPHF uses
  $\lceil \log_2 n \rceil + o(1)$ bits per element. The chapter
  earlier said "the BPHF spends $\lceil \log_2 n \rceil$ bits per
  slot enough to distinguish the $n$ possible ranks" (§15.2 line 80,
  127-128). But "enough to distinguish $n$ ranks" is the rank
  table's *job*; it is not the *bit-cost minimum* for the BPHF as a
  data structure. The actual minimum is determined by what the
  filter needs to do to maintain its guarantees. The text presents
  $\lceil \log_2 n \rceil$ as both "what's needed for ranks" and
  "the optimal cost", but the optimality claim should be derived
  from the entropy floor (chapter 8) for FPR-zero structures, not
  from a per-slot accounting. The chapter 8 §8.3 floor applies to
  the FNR-zero case; chapter 6 §6.4 §15.1 mention that the FPR-zero
  arm has its own floor, but no theorem in chapter 8 states a
  matching floor for FPR-zero. The §15.2 prose treats $\lceil \log_2
  n \rceil$ as the analogue of $\lceil -\log_2 \fprate \rceil$
  without naming the underlying lower bound. Either the chapter 8
  floor needs to be extended (or referenced more carefully) or §15.2
  / §15.3 should explicitly acknowledge that the $\lceil \log_2 n
  \rceil$ formula is the construction's cost, not necessarily the
  optimum for FPR-zero filters.
- **MAJOR** §15.3 line 180-182 (small-$n$ claim): "At small $n$ the
  BPHF is cheaper per element than a BHF at any nontrivial $\fprate$;
  at large $n$ the BPHF becomes more expensive than a BHF at any but
  the strictest $\fprate$ targets." The first half is wrong for any
  "nontrivial" $\fprate$ a reader would naturally consider. At $n =
  1000$ (small by any sensible measure), BPHF $= 10$ bits and BHF at
  $\fprate = 0.01$ (the standard "nontrivial" target) $= 7$ bits;
  the BHF is *cheaper*, not the BPHF. The claim holds only for $n$
  small enough that $\log_2 n <$ the reader's "nontrivial" $\log_2
  (1/\fprate)$. The crossover analysis (eq. $\fprate = 1/n$) is
  correct in §15.3 line 294 but the narrative summary contradicts
  it for typical "nontrivial" parameters. Fix: rewrite the
  small-vs-large $n$ claim as "the BPHF is cheaper when $n$ is small
  enough that $\log_2 n$ is smaller than the BHF's $-\log_2 \fprate$
  budget" or refer directly to the crossover formula.
- **MAJOR** §15.4 lines 89-101 (the TopK query algorithm): the
  algorithm $\textsc{TopK}(a) = \textsc{Query}(a) \land R[\phi(a)] <
  k$ requires evaluating $\rho(a)$ inside $\textsc{Query}(a)$
  (per \Cref{alg:bphf-build-query}). For a candidate $a$ that may
  not be in the corpus, $\rho(a)$ (the sort-position rank) is
  undefined. The algorithm therefore only works when $a \in A$, in
  which case the rank is trivially recoverable from the table. The
  text says "the membership check returns $\top$ when $a$ is a known
  corpus document", which is true under input restriction, but the
  filter does not detect "is $a$ a known corpus document" without
  an additional mechanism (a separate hash check, a salted
  identifier, a membership filter prior). The chapter should make
  the input restriction explicit (and consequently the FPR = 0
  becomes trivial) or specify how the BPHF detects non-members
  without a sort-position to compare against.
- **MINOR** §15.1 lines 86-92 ("The dual is exact: the BPHF for a
  designated set is the BHF for the complement, modulo the
  practical detail that the complement is usually infinite"): this
  is a useful framing but the cleanest version of the duality
  requires the complement to be finite. For a universe of size $|
  \Universe| = N$ and $|A| = n$, the "BHF for the complement" would
  have $N - n$ elements; for typical $N \gg n$ this is a different
  construction with different cost. The §15.1 sentence elides this;
  one half-sentence acknowledging the asymmetry would tighten the
  exposition.
- **MINOR** §15.2 line 100-105 (rank assignment options): "The
  assignment may come from any source the application supplies: a
  secondary hash truncated to $r$ bits, a position in a sorted
  ordering of $A$, a relevance score discretized to $n$ buckets, or
  an external rank derived from metadata." This is correct that
  multiple rank sources work, but the analysis that follows assumes
  a specific source (uniform across $\{0, \ldots, n-1\}$, which the
  hash source delivers but the sort-position source does not give
  the same probability structure). The text mixes the options
  without acknowledging that the FNR analysis depends on which one
  is chosen.
- **MINOR** §15.2 line 287-293 worked example final paragraph: "a
  BHF on the same set at $\fprate = 0.01$ would use $r = 7$ bits per
  element ($7000$ bits total) and provide $\fnrate = 0$ at $\fprate
  \le 0.0078$." The "$3$ extra bits per element" comparison is fair
  ($10 - 7 = 3$). But the chapter then says BPHF "spends $3$ extra
  bits per element to push the FPR to zero exactly while accepting
  a $0.001$ FNR" — given the BLOCKER above on whether the BPHF
  actually delivers FPR = 0 with the construction as stated, this
  paragraph requires verification of what trade is actually made.
- **MINOR** §15.3 line 259-260 worked example: "$\lceil \log_2 10^6
  \rceil = \lceil 19.93 \rceil = 20$" — correct. The table caption
  says "Both columns omit the sublinear perfect-hash overhead" which
  is the right disclaimer.
- **MINOR** §15.4 line 192-198 expected miss derivation: the
  derivation uses linearity of expectation correctly: $\mathbb{E}[
  \text{misses}] = \sum_i \Prob{i \text{ missed}} \le k \cdot 2^{-r}$,
  assuming per-member miss events are individually bounded by $2^{-r}$.
  The hypothesis is conditional on the BLOCKER finding above being
  resolved: if the FNR upper bound is actually $\le 2^{-r}$ per
  member, then the expected misses bound is correct.
- **MINOR** §15.5 line 80-84 (closing Part IV claim): "the two
  constructions together cover the perfect-filter line at the
  asymptotic bit-budget optimum on each side; the part closes with
  both arms supplied with their constructive realization." The
  "asymptotic bit-budget optimum" for the BPHF side is the $\lceil
  \log_2 n \rceil$ rate, which is presented as analogous to the
  $\lceil -\log_2 \fprate \rceil$ rate of the BHF. The chapter does
  not state a corresponding entropy-floor theorem for FPR-zero
  filters; the claim of optimality on the FPR-zero side rests on a
  result that is not in chapter 8.
- **MINOR** §15 ex 15-6 (lines 122-141): the BPHF vs sorted-index
  comparison is sound but the "associative-structure overhead, on
  the order of a factor of $2$ to $4$ at $n = 10^6$" matches the
  Python computation: BPHF $2.5$ MB, sorted with $32$-bit pointer
  $6.5$ MB (factor $2.6$), sorted with $64$-bit pointer $10.5$ MB
  (factor $4.2$). The "factor of $2$ to $4$" is the right ballpark.
- **NOTE** §15.6 bibliographic notes (paragraph 1 "the manuscript
  treats the BPHF in greater generality"): the manuscript
  description is sparse but consistent with the BPHF source paper
  in `papers/bernoulli-phf/`. A reader looking for the discriminator
  mechanism mentioned in §15.2 would naturally turn to the
  manuscript; a sentence pointing them there would close the loop.
- **NOTE** §15 ex 15-9 part (c): the exercise's conclusion
  ($\approx 0.32$ exact FNR without discriminator) is the
  diagnostic that flags the BLOCKER finding above. The exercise is
  pedagogically valuable but should not be the only place the
  reader sees the gap. Once the BLOCKER is fixed in §15.2, ex 15-9
  should be re-evaluated for whether it still teaches the right
  intuition.

## Cross-chapter coherence findings

These findings only surface when reading across chapters.

- **MINOR** Notation consistency. Chapter 14 uses $g$ for the
  fingerprint hash and $F$ for the fingerprint table; chapter 15
  uses $\rho$ for the rank assignment and $R$ for the rank table.
  The parallel is clean and signals the dual structure. The choice
  to use Greek letters for the chapter 15 objects ($\rho$ rather
  than, say, $h$) emphasizes that the BPHF's $\rho$ is *not* a hash
  in the same sense as $g$ — it carries semantic information about
  the application's ordering. This is good pedagogically. One small
  notational drift: chapter 14 §14.7 introduces $\sigma$ as a
  notation for the fingerprint (plan-spec list at top of plan 14
  bullet 3), but the chapter's body uses $g(a)$ rather than
  $\sigma(a)$ for the fingerprint value. The plan's notation
  intention is dropped without explanation.
- **NOTE** Page budgets vs spec §6 budget table:

| Chapter | Spec §6 target | Estimated current |
|---|---|---|
| Ch 14  | ~30 pp | ~31 pp (+1) |
| Ch 15  | ~28 pp | ~25 pp (-3) |
| Total  | ~58 pp | ~56 pp (-2) |

  Chapter 15 is under spec by ~11%, consistent with the chapter's
  compression strategy (Plan 15 anticipated: "the chapter 15
  narrative will not need to redevelop the machinery; it will
  reuse the chapter 14 derivation with the error-mode swap"). Total
  Part IV at ~56 pp is within tolerance of the spec's ~58 pp
  target. The under-budget on chapter 15 is partly explained by
  the BLOCKER finding above: the missing detail on the
  discriminator and the rank-source clarification would add
  approximately 1-2 pp, bringing chapter 15 closer to spec.

- **NOTE** The BHF/BPHF pairing is the central structural promise of
  Part IV. The chapters do deliver this pairing at the high level:
  chapter 14 covers the FNR-zero arm, chapter 15 covers the FPR-zero
  arm, both reach (claimed) optimal bit budgets, both share the
  perfect-hash + per-slot-value architectural template. The pairing
  reads cleanly at the chapter-level synthesis; the issues identified
  above are at the section level of chapter 15's analysis. The Part
  IV success criteria from spec §10 (reader can describe both
  constructions; recognizes chapter 14 closes the chapter 8 floor;
  sees chapter 14 and chapter 15 as the two halves of the perfect-
  filter line) are mostly met for chapter 14 and partially met for
  chapter 15 pending the BLOCKER fix.

- **NOTE** Documented deferred cross-refs unchanged: `ch:composition`
  x 1 (chapter 4 forward ref), `ch:sketches` x 5 (chapter 9 forward
  refs to chapter 10's `ch:sketches-estimators`), `sec:noisy-bit` x
  2 (chapter 17 forward refs to chapter 1). All are baseline-flagged
  in `book/book.log` and not new findings. Part IV adds no new
  documented-deferred items.

## Recommended next actions

Ordered by priority.

### BLOCKER

1. **§15.2 FNR derivation:** rework the §15.2 "false-negative rate
   trade-off" subsection to make the discriminator first-class. The
   current rank-collision argument cannot support the headline bound
   $\fnrate \le 2^{-r}$. Either (a) replace the rank-equality check
   with a construction that genuinely has FNR $\le 2^{-r}$ from a
   single source (e.g., store $r$-bit identifier of the rank's
   owner, so a member's miss requires the identifier check to fail
   independently, with the only source of FNR being a separate
   mechanism), or (b) make the discriminator visible in the
   definition and pseudocode so the analysis can flow through it.
   Update ex 15-9 to be consistent with the fixed derivation. Update
   the worked example accordingly.

### MAJOR (should fix before integration sign-off; may defer to a revise pass)

2. **§15.2 $\fprate = 0$ specification:** make the FPR = 0 derivable
   from the construction. The hand-wave "the construction adds a
   build-time discriminator" needs to be replaced with a concrete
   mechanism. The most pedagogically clean version is probably to
   replace the abstract $\rho$ with the sort-position rank (defined
   only on $A$) used in §15.4, making the FPR = 0 a consequence of
   the rank function being undefined on non-members and the query
   being restricted to candidate IDs the application provides. This
   removes the hand-wave at the cost of a small framing shift in
   §15.2.
3. **§15.2 / §15.4 rank-source consistency:** pick one rank-source
   regime (hash-based with discriminator, or sort-position-based
   with input restriction) and use it consistently between §15.2's
   construction and §15.4's application. Currently §15.2 lists both
   as options and §15.4 silently switches to one, which leaves the
   reader confused about which is canonical.
4. **§15.2 / §15.3 BPHF optimality framing:** acknowledge that the
   $\lceil \log_2 n \rceil$ rate is the construction's cost, not
   necessarily a proven lower bound for FPR-zero filters. Either
   add a brief discussion of why $\lceil \log_2 n \rceil$ is optimal
   for FPR-zero structures (a one-paragraph adaptation of the
   chapter 8 floor argument) or soften "asymptotic bit-budget
   optimum" claims throughout the chapter to "the bit budget the
   construction delivers".
5. **§15.3 small-$n$ claim:** rewrite "At small $n$ the BPHF is
   cheaper per element than a BHF at any nontrivial $\fprate$" to
   refer to the crossover formula $\fprate = 1/n$ directly, or
   qualify "small $n$" to mean $\log_2 n <$ the $\fprate$-budget the
   reader is comparing against.
6. **§15.4 TopK algorithm clarification:** make explicit that the
   algorithm only works when the application restricts queries to
   known corpus IDs (or specify the membership-detection mechanism
   that handles unknown IDs). The current text glosses over the
   issue.
7. **§14.5 line 220 build-cost comparison:** correct the "Bloom
   filter's per-element constant is much smaller" claim. The Bloom
   filter's *insertion* (post-build) cost per element is smaller;
   the *build* cost per element is comparable or larger when $k$ is
   large. The current phrasing reverses the relationship.

### MINOR (polish-pass additions)

Add to the polish-pass list:

- §14.1 line 80 (soften the §8.4 back-reference about "isolating
  three design choices and remarking").
- §14.2 line 320 (clarify that the BHF total at $n = 10^6$ is the
  fingerprint $r$ bits plus the sublinear perfect-hash term, not
  exactly $r$).
- §14.4 line 200 (distinguish "$2$-universal" from "pairwise
  independent" in the Carter-Wegman discussion).
- §14.4 line 217 (clarify the conditioning of the $0.78\%$ figure).
- §14.5 line 218 (cite or soften the "$10$ to $50$ million elements
  per second" throughput claim).
- §14.6 line 88-89 (acknowledge the asymmetry in the
  BPHF-as-BHF-of-complement duality).
- §14.7 bibliographic notes (correct the cuckoo-filter range from
  "$1.05$ to $1.3$" to "$1.07$ to $1.23$").
- §15.1 line 86-92 (acknowledge the complement-finiteness assumption
  in the duality framing).
- §15.2 line 100-105 (clarify which rank source the FNR analysis
  assumes).
- §15.2 line 287-293 worked example (pending BLOCKER resolution).
- §15.2 line 167 (the $\lceil \log_2 n \rceil$ "enough to distinguish"
  vs "optimal" distinction).
- §15.5 line 80-84 (clarify the optimality claim on the FPR-zero
  side).
- §15.6 (add pointer to manuscript for discriminator details).
- §15 ex 15-9 (re-evaluate after BLOCKER fix).
- Headers: `ch15/bridge-to-part5.tex` and `ch15/exercises.tex` list
  `ch:bhf` as a label in their comment blocks but the actual label
  is `ch:optimal-bernoulli-sets`. Clean up header comments.
- Chapter 14 notation: align with plan-spec intent (`\sigma` for
  fingerprint values vs body's `g(a)`); either update notation or
  document why `g` was chosen.

### NOTE (defer to a future revision or leave as-is)

- §14.6 bridge is appropriately compact.
- §14.7 bibliographic notes are well-organized and concise.
- §15.6 bibliographic notes appropriately concise.
- §14.5 trade-off table is the right summary for the
  static-vs-streaming decision.
- §15.4 worked example bit accounting is clean.
- Documented deferred cross-refs unchanged.

## Specialist verdicts (consolidated)

- **spec-auditor:** Part IV PASS. All content checklist items from
  spec §4 chapters 14-15 are realized. Chapter 14 hits its 30 pp
  target exactly; chapter 15 is under spec by ~11% but consistent
  with the planned narrative compression. The BHF/BPHF pairing
  delivers the perfect-filter-line architecture the spec called for
  at the part-level synthesis. Spec §10 success criteria 1 and 3 are
  met (reader can describe both constructions; chapter 14 closes the
  chapter 8 floor); criterion 2 (BHF as the FNR-zero, BPHF as the
  FPR-zero realization at the asymptotic optimum) is partially met
  pending the BLOCKER fix.
- **quality-auditor:** "substantive revision needed" for chapter 15;
  "ships as is" for chapter 14. Chapter 14 is publication-ready
  modulo MINOR polish. Chapter 15 carries the BLOCKER (FNR
  derivation gap) and three MAJORs ($\fprate = 0$ specification,
  $\rho$ source consistency, small-$n$ claim) that require focused
  revision before the chapter is ready for an integration pass. The
  pedagogical voice is consistent across both chapters; the issues
  are content-level, not voice-level.
- **math-auditor:** PASS with corrections. Every numerical claim
  checked verifies independently. The exception is the §15.2
  derivation of $\fnrate \le 2^{-r}$ which is mathematically
  unsupported by the rank-collision argument the text gives (the
  $\binom{n}{2} \cdot 2^{-r}$ form is the wrong quantity; the
  correct per-member bound is $(n-1) \cdot 2^{-r}$ which evaluates
  to $\Theta(1)$ at $r = \lceil \log_2 n \rceil$, not $2^{-r}$). The
  §14.2, §14.3, §14.4, §14.5 worked examples (including the BHF/Bloom
  comparison table at $n = 10^6$, the $r = 7$ verification with
  $2^{-7} = 0.0078$, the $1/\log_2 e \approx 0.693$ asymptote, the
  query-cost ratios) all check exactly. The §15.3 crossover at
  $\fprate = 1/n$ and §15.4 ranked-search expected misses ($k \cdot
  2^{-r} = 9.5 \times 10^{-5}$ at $n = 10^6, k = 100, r = 20$) check
  arithmetically.
- **cross-ref-auditor:** PASS with two minor header-comment
  staleness items. All DEFINED labels match declarations; no
  collisions. All RESOLVED labels exist (`def:bloom-filter`,
  `alg:bloom-insert-query`, `thm:entropy-floor`, `sec:entropy-floor`,
  `prop:bloom-overhead`, `sec:bloom-gap`, `def:perfect-filter-line`,
  `sec:perfect-filter-line`, `prop:fpr-zero-closure`, `def:one-sided`,
  `def:bhf`, `sec:bhf-construction`, `alg:bhf-insert-query`,
  `thm:bhf-optimality`, `prop:bhf-fpr`, `sec:space-analysis`,
  `sec:fpr-analysis`, `sec:construction-time`, plus chapter 16 stub
  `ch:not-bernoulli`). Two header-block staleness issues
  (`ch15/bridge-to-part5.tex` and `ch15/exercises.tex` list `ch:bhf`
  in their comment blocks but `ch:bhf` is not a real label; the
  actual chapter 14 label is `ch:optimal-bernoulli-sets`; the body
  does not reference `ch:bhf`, so this is documentation only). The
  documented deferred items (`ch:composition`, `ch:sketches` x 5,
  `sec:noisy-bit` x 2) match the build log exactly.

## Overall recommendation

Chapter 14 is in good shape. The chapter delivers the BHF
construction cleanly, the optimality theorem matches the chapter 8
floor up to integer rounding, the FPR analysis is short and complete,
the trade-off discussion is well-organized, and every numerical claim
verifies. The five MINOR findings and three NOTE items are
appropriate polish-pass material.

Chapter 15 has substantive issues that should be addressed before
integration sign-off. The BLOCKER is the §15.2 FNR derivation, which
cannot support the headline bound $\fnrate \le 2^{-r}$ as written.
The six MAJOR findings cluster around the $\fprate = 0$ specification
(the discriminator is named but not specified), the rank-source
consistency between §15.2 and §15.4 (hash vs sort-position), the
optimality framing (the $\lceil \log_2 n \rceil$ rate is presented as
optimal without a matching floor theorem), and exposition issues in
§15.3 and §15.4. The chapter's pedagogical structure is sound (the
parallel with chapter 14 is clear, the ranked-search application is
the right canonical use case, the BHF/BPHF comparison table makes
the trade visible), but the analysis needs to be tightened so the
guarantees it claims are the ones the constructions actually deliver.

The 12 MINOR findings include items that surface only on careful
cross-chapter reading (notation drift, header staleness, comparison
claims). The 8 NOTE items are deferrals or items that work as is.

Recommend: schedule a focused revision pass on chapter 15 §15.2 to
fix the FNR derivation and the FPR specification, and to align
§15.4's rank-source with §15.2's construction. The chapter 14
MINORs and the cross-chapter notation alignment can be queued for a
polish pass before Milestone 2.
