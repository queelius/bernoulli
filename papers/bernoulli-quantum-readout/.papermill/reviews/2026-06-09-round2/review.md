# Multi-Agent Review Report (Round 2)

**Date**: 2026-06-09 (round 2)
**Paper**: A Forward $(\epsilon,\omega)$ Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes
**Author**: Alexander Towell
**Manuscript**: `papers/bernoulli-quantum-readout/main.tex` (article class, 17 pp); scripts `code/crosstalk_validation.py`, `code/readout_figure.py`
**Recommendation**: **ready** (no correctness defect; residual items are NOTE/MINOR polish)

---

## Orchestration note

This round followed a round-1 pass (`.papermill/reviews/2026-06-09-round1/review.md`) whose
findings were all addressed, plus two substantial new pieces of content (§3.7 the dependence
expansion; §4.6 crosstalk sensitivity plus Table 3). Per project memory ("papermill reviewer has
no recursive subagents here"), the `Task` tool is unavailable in this environment, so all six
specialist lenses were run single-context by the orchestrator. Unlike the round-1 pass (which
could not run Bash), this round executed everything:

- Both validation scripts were **run fresh** (`python3 code/crosstalk_validation.py`,
  `python3 code/readout_figure.py`) and their output checked cell-by-cell against the manuscript.
- The paper was **rebuilt** (`pdflatex; bibtex; pdflatex; pdflatex`), all four stages exit 0;
  17 pp, **0 undefined refs/cites, 0 LaTeX warnings, 0 overfull/underfull boxes, 0 bibtex warnings**,
  20/20 bibcites resolved, no `{??}`.
- The new propositions were **re-derived from scratch independently** (brute-force enumeration
  over random dependent joints; small-$\lambda$ asymptotic exponent fits) rather than trusting
  the paper's own scripts.

All quoted manuscript text below was confirmed against a direct full read of `main.tex`
(lines 1 to 1136).

---

## Summary

**Overall assessment.** The two new mathematical artifacts are **correct**. Proposition 3.9
(`prop:corrparity`) and its first-order reading (`cor:crosstalk-sign`) were independently
re-derived and hold exactly: the $\pm1$ expansion, the $|T|=1$ vanishing argument, the
$\operatorname{Cov}(S_i,S_j)=4c_{ij}$ identity, the $n=2$ exactness, and the $-2$ first-order
coefficient all check to machine precision. Every one of the 30 cells of Table 3 matches the
fresh script output to the printed digit, and all six §4.6 prose numbers (2.8x, 5.8x, the 0.0628
baseline, the $O(\lambda^2)$ residual, the $[0,1]$ escape, the $n{=}9$ $\lambda{=}\tfrac12$ sign
reversal 0.535 vs 0.500) reproduce. The build is production-clean. The exact-vs-first-order-vs-
future-work story is consistent across abstract, intro, scope, and conclusion, with **no stale
sentence** left framing crosstalk as wholly future work. This pass found **no correctness defect**
and **no blocking issue**. The residual items are two small analytic-precision NOTEs (a loose
$2^{|T|}$ prefactor; a rounding nuance on the 0.0628 baseline) and the carried-over disclaimer-
density observation, now reduced to acceptable levels by the round-1 dedup except for the
diagonal-sector theme.

**Strengths**
1. **The new §3.7 math is exactly right** (logic lens). Independent brute-force verification over
   random dependent joints confirms `eq:corrparity` for $n=2,3,4,5$; the remainder $R$ is exactly
   $0$ at $n=2$ (machine epsilon) and genuinely nonzero ($=$ the 3rd+ central moments) for $n\ge3$.
   The $-2$ first-order coefficient, $\operatorname{Cov}(S_i,S_j)=4c_{ij}$, and the $n=2$ closed
   form all verified to $10^{-16}$.
2. **Table 3 and all §4.6 numbers reproduce from a fresh run** (methodology lens). 30/30 table
   cells match; the chain first-order error is confirmed $O(\lambda^2)$ (fitted exponent 1.994)
   and the global central cross-moments confirmed linear in $\lambda$ at every order (fitted
   exponent 0.9999 for $|T|=2,3,4$), which is exactly *why* the first-order truncation must fail
   for the global model, as the paper argues.
3. **The two dependence models are legitimate ground truths** (methodology lens). `chain_exact`
   (conditioning over $2^{n-1}$ edge configs) and `global_exact` $=(1-\lambda)P_{\mathrm{indep}}
   +\lambda(n\bmod 2)$ both match brute-force enumeration exactly; the $2\times10^6$-trial Monte
   Carlo is a genuine independent confirmation gated by a 5-$\sigma$ assert.
4. **§3.7 and §4.6 are well-placed** (prose lens). §3.7 sits last in the calculus section, after
   the §3.6 operator view it explicitly leans on ("the same $\pm1$ algebra that proved
   `thm:parity`"; the closing spectral back-reference at L666 to 668). §4.6 caps the worked example
   after the majority/feed-forward remark, delivering empirically the sensitivity §3.7 set up
   theoretically. The narrative arc is coherent.
5. **The exact/first-order/future-work story is consistent** (novelty plus prose lenses). Abstract
   L104, intro L162 to 164, scope item 2 L1058 to 1067, and conclusion L1118 to 1125 all say the same
   thing: exact under independence, first-order beyond it, beyond-first-order CTMP lift is future
   work. No contradiction; no leftover "blind to crosstalk" / "wholly future work" sentence.
6. **Build plus bibliography integrity perfect** (format plus citation lenses). 17 pp, clean log;
   20 cited keys $=$ 20 defined keys (no orphans, no undefined); the round-1 `gidney2021stim`
   addition is cited 3x and resolves; `vonneumann1956` is now correctly `@incollection`.

**Weaknesses** (all NOTE/MINOR; none blocking)
1. The $|m_T|\sim\lambda\,2^{|T|}$ prefactor (L903) is loose: the true growth is faster than
   $2^{|T|}$ (NOTE, analytic precision).
2. The 0.0628 "crosstalk-free value" (L893) is the figure's $n{=}8$ cold parity, while Table 3's
   chain-exact column reads 0.0623 to 0.0703; "barely moves from 0.0628" is fair but the baseline and
   the table column differ in the third digit (NOTE, rounding nuance).
3. The diagonal-sector disclaimer recurs in ~7 passages; the other two disclaimer themes are now
   at acceptable density after the round-1 dedup (MINOR, residual wordiness).

**Finding counts**: Critical: 0 | Major: 0 | Minor: 1 | Notes/Suggestions: 5

---

## Critical Issues

None.

## Major Issues

None. (The round-1 Major, the AND "smallest corner" claim needing $\epsilon_i+\omega_i\le1$,
is **confirmed fixed**: the qualifier "for informative channels ($\epsilon_i+\omega_i\le1$,
equivalently a nonnegative channel eigenvalue $1-\epsilon_i-\omega_i$...)" now appears in **both**
the theorem statement (L349 to 351) and the proof (L376 to 380, including the anti-informative
$\epsilon_i+\omega_i>1$ reversal note). The comparative claim is now correctly conditioned.)

## Minor Issues

### MINOR-1. The diagonal-sector disclaimer remains dense (~7 passages) (source: prose-auditor, cross-verified by novelty-assessor)
- **Location**: abstract L78; intro L177 to 178; §2.2 L263 to 269; §3.6 honesty clause L595 to 600;
  §4.5 majority caveat L869; scope item 3 L1072 to 1074; conclusion L1120.
- **Status vs round 1**: the round-1 report flagged a 4 to 7x disclaimer *triple*. The dedup
  (back-reference to `sec:scope` at L948 to 949; the canonical claimed/not-claimed list now collected
  once in scope item 4) brought **theme 1 (forward-not-inverse)** to 4 well-separated, structurally
  expected locations and **theme 2 (not-claimed-vs-claimed)** to 4 differentiated ones (intro brief;
  §3.6 "bookkeeping not new theorems"; §5 "not new to us"; scope item 4 canonical). Those two are
  now **acceptable** and need no further cutting. The diagonal-sector theme is the lone residual.
- **Problem**: It is the paper's most important honesty boundary (it forecloses a coherence /
  quantum-advantage misread), and most occurrences are substantive (the §2.2 faithfulness paragraph,
  the §3.6 honesty clause, the L869 majority-vote caveat that genuinely needs the "resampleable
  latent value" point). So this is the most defensible of the three themes; but at journal length a
  referee may still read 7 restatements as over-insurance.
- **Suggestion**: optional. Keep §2.2, §3.6, and scope item 3 (the three load-bearing statements);
  trim the abstract mention to a half-clause and let the intro L177 to 178 point forward to §2.2 rather
  than restate. Not required for correctness or acceptance.
- **Cross-verified**: novelty-assessor confirms the density is honesty, not a contribution-hiding
  symptom; the contribution is clear and the disclaimers are accurate.

## Notes and Suggestions (non-blocking)

1. **NOTE (methodology/logic): the $|m_T|\sim\lambda\,2^{|T|}$ prefactor is loose.** At L903 the
   global-model central cross-moments are written $|m_T|\sim\lambda\,2^{|T|}$. The **load-bearing**
   content, that every $m_T$ ($|T|\ge2$) is *linear in $\lambda$* (so a pairwise truncation cannot
   capture it and the first-order rate must fail), is **exactly correct** (independently fitted
   exponent $0.9999$ for $|T|=2,3,4$ as $\lambda\to0$). But the *constant* $2^{|T|}$ understates the
   true small-$\lambda$ prefactor, which grows faster than $2^{|T|}$ (measured $|m_T|/(\lambda
   2^{|T|})\to$ roughly $3.9, 7.8, 15.5$ for $|T|=2,3,4$). The "$\sim$" is doing order-of-magnitude /
   "every order enters at $O(\lambda)$" work, which is the point being made, so the claim is not
   wrong as a scaling statement; only the specific power-of-two constant is not tight. Optional fix:
   write "$|m_T|=\Theta(\lambda)$ at every order $|T|$" (the actually-load-bearing fact) and drop the
   specific $2^{|T|}$, or soften to "$|m_T|\gtrsim\lambda\,2^{|T|}$". Cosmetic.

2. **NOTE (methodology): the 0.0628 baseline vs the Table-3 chain-exact column.** L893 says the
   chain-exact error "barely moves from its crosstalk-free value of $0.0628$." That $0.0628$ is the
   figure script's $n{=}8$ cold parity (direct value $0.06275$, rounds to $0.0628$). Table 3's
   chain-exact column reads $0.0626/0.0624/0.0623/0.0628/0.0703$, i.e. it agrees at $\lambda=0.02$
   and stays within a few $10^{-4}$ elsewhere, fully supporting "barely moves," but the quoted
   baseline ($0.0628$) and the smallest-$\lambda$ table entry ($0.0626$) differ in the third digit
   because the chain model inflates the marginals slightly even at $\lambda=0.001$. Honest and
   correct; a half-clause ("$\approx0.063$") would avoid a reader cross-checking $0.0628$ against the
   $0.0626$ table cell. Cosmetic.

3. **NOTE (logic): the §3.7 proof could name the constant pull-out explicitly.** The proof (L640 to 642)
   says "the terms with exactly two [$\delta$ factors] carry $\mathbb{E}[\delta_i\delta_j]=4c_{ij}$."
   Strictly, such a term is $\delta_i\delta_j\prod_{k\notin\{i,j\}}\mu_k$, and the $\mu_k$ (constants)
   pull out of the expectation before $\mathbb{E}[\delta_i\delta_j]=4c_{ij}$ applies, which is why
   `eq:corrparity` carries the $\prod_{k\notin\{i,j\}}\mu_k$ weight. `eq:corrparity` displays the
   weight, so the reader can reconstruct it, and the result is unambiguously correct (verified by
   brute force). A one-clause "(the remaining $\mu_k$ factor out)" would make the proof airtight on
   its face. Optional.

4. **NOTE (consistency): the conclusion's "the field's '$n$ times the per-measurement error' rule"
   (L1113).** The abstract and intro were softened in round 1 to name "detector-error-model tooling"
   and a "symmetrized, single-rate rule of thumb" rather than baldly asserting the field uses $nq$;
   the §4.3 subsection heading ("The linearization the field uses", L692) and the conclusion L1113
   still use the sharper folklore framing. This is internally defensible (the $nq$ union bound *is*
   real folklore, and the surrounding sentences scope it correctly), so it is not an inconsistency;
   noted only because a QEC referee who reads the (correctly hedged) abstract and then the (sharper)
   conclusion may notice the tonal step. No change required.

5. **SUGGESTION (methodology): EPS8 / RATES coupling is correct but implicit.** `crosstalk_validation.py`
   hardcodes `EPS8` (line 40) and `readout_figure.py` hardcodes the full `RATES` (lines 24 to 32); the
   first 8 cold rates are **identical** across the two files (verified element-by-element), which is
   what makes the cross-script "0.0628 crosstalk-free value" claim coherent. Since both are manual
   copies of the same `ibm_hanoi` snapshot, a one-line comment in `crosstalk_validation.py` noting
   "EPS8 == first 8 of readout_figure.RATES eps column" (or importing it) would prevent future drift.
   Both scripts already cross-cite each other in comments, so this is minor.

---

## Detailed Notes by Domain

### Logic and Proofs
The two new results are correct, re-derived from scratch this round (not merely re-read):
- **`prop:corrparity` (eq:corrparity).** Expanding $\prod_i(\mu_i+\delta_i)$ and taking
  expectations: single-$\delta$ terms vanish because $\mathbb{E}[\delta_i]=0$ and the accompanying
  $\mu_k$ are constants that factor out (verified: every one-$\delta$ term is $0$); two-$\delta$
  terms give $4c_{ij}\prod_{k\notin\{i,j\}}\mu_k$; the rest is $R$ over $|T|\ge3$ central moments.
  Brute-force enumeration over random dependent joints confirms $\mathbb{E}[\prod S_i]=\prod\mu_i
  +4\sum c_{ij}\prod\mu_k+R$ for $n=2,3,4,5$; at $n=2$ the remainder is exactly $0$ (machine
  epsilon), confirming "for $n=2$ the remainder is empty."
- **$\operatorname{Cov}(S_i,S_j)=4c_{ij}$.** $\operatorname{Cov}(1-2F_i,1-2F_j)=4\operatorname{Cov}
  (F_i,F_j)$; verified to $2\times10^{-16}$. And $\mathbb{E}[\delta_i\delta_j]=\operatorname{Cov}
  (S_i,S_j)$ holds because $\delta_i=S_i-\mathbb{E}[S_i]$.
- **$n=2$ exact $P=\tfrac12(1-\mu_1\mu_2)-2c_{12}$.** Matches brute-force $P(F_1\oplus F_2{=}1)$ to
  $10^{-16}$ over 20 random joints.
- **First-order coefficient $-2$.** $P=\tfrac12(1-\mathbb{E}[\prod S])$, so the $c$-term in $P$ is
  $-\tfrac12\cdot4\sum c_{ij}\prod\mu_k=-2\sum c_{ij}\prod\mu_k$; the script's `first_order()`
  (lines 48 to 59) implements exactly this $-2$. Confirmed.
- **`cor:crosstalk-sign`.** If $r_k<\tfrac12$ then $\mu_k>0$, so each weight $\prod_{k\notin\{i,j\}}
  \mu_k>0$ and the slope $-2\prod\mu_k<0$: positive covariance lowers parity error to first order.
  Correct. The "to first order" qualifier is honest, not papering: the global model exhibits a
  genuine sign reversal (positive covariance, induced cov$(0,1)=0.246$ at $\lambda=\tfrac12$, yet
  exact error $0.535 > 0.500$ independent anchor) precisely because the linear-in-$\lambda$ higher
  cumulants overwhelm the pairwise term. The empty-product $n=2$ convention (weight $=1$) is handled
  correctly.
- **Independence recovery.** $c_{ij}=0,R=0\Rightarrow$ `eq:parity-asym` (L651): correct.
- **Round-1 AND fix.** The "smallest corner" comparative claim is now correctly gated by
  $\epsilon_i+\omega_i\le1$ in both statement and proof.

### Methodology
Every number in §4.6 / Table 3 reproduces from a **fresh run** of `crosstalk_validation.py`:
- Table 3: all 30 cells match (chain indep/first/exact and global indep/first/exact at
  $\lambda=0.001/0.005/0.010/0.020/0.050$).
- 2.8x and 5.8x (L895): chain indep/exact $=0.17168/0.06226=2.76\approx2.8$ at $\lambda=0.01$ and
  $0.40496/0.07033=5.76\approx5.8$ at $\lambda=0.05$. PASS.
- $O(\lambda^2)$ chain residual (L899): fitted exponent 1.994. PASS.
- First-order leaves $[0,1]$ for the global model (L904): $P_{\text{first}}$ goes
  $0.0206\to-0.9370$. PASS.
- $n{=}9$, $\lambda=\tfrac12$ reversal (L910 to 912): script gives exact $0.5354$, indep $0.5000$;
  rounds to 0.535 > 0.500. PASS.
- Ground-truth legitimacy: `chain_exact` and `global_exact` both match brute-force enumeration
  exactly; the $2\times10^6$ MC is gated by a 5-$\sigma$ assert (script line 162); caption's "agrees
  to within $10^{-3}$" (L920) is consistent with the run.
- Table 1 (`tab:syndrome`) and Table 2 (`tab:syndrome-asym`) still reproduce via
  `readout_figure.py::print_tables()` (1.0/3.1/7.2/5.3/16.3/40.5%; 0.110/0.175/0.234/0.315/0.226).
- The figure (`fig:realcalib`) coordinates match the script's emitted pgfplots blocks; formula-vs-MC
  worst diff $9.53\times10^{-4}<10^{-3}$, matching the caption.
Findings: NOTE-1 (loose $2^{|T|}$ prefactor), NOTE-2 (0.0628 baseline rounding), SUGGESTION-5
(implicit EPS8/RATES coupling).

### Novelty and Contribution
The contribution is unchanged in kind from the rounds that converged to "ready"; §3.7/§4.6 *extend*
it cleanly (the calculus now quantifies the leading correction beyond independence rather than only
signing it), and the abstract/intro/scope/conclusion tell one consistent story about what is exact
(independent/tensor regime), first-order (weak crosstalk), and future work (beyond-first-order CTMP
lift, live-hardware study). The new material does not overclaim: §3.7 is framed as the exact
expansion with an honestly-bounded first-order reading, and §4.6 deliberately exhibits a regime
where first-order *fails*. No novelty-framing regression.

### Writing and Presentation
§3.7 and §4.6 are well-integrated and well-placed (see Strength 4). Prose is precise. The dominant
residual is MINOR-1 (diagonal-sector disclaimer density); the round-1 disclaimer-triple is otherwise
adequately deduped. NOTE-4 (a tonal step between the hedged abstract and the sharper conclusion on
the $nq$ folklore) is optional. No new long-sentence or notation-consistency problems introduced by
the new content.

### Citations and References
Perfect internal integrity: 20 cited keys $=$ 20 defined keys; no orphan, no undefined, no `{??}`;
fresh `bibtex` run emits 0 warnings. Round-1 bib fixes confirmed: `vonneumann1956` is now
`@incollection` (booktitle *Automata Studies*, eds. Shannon and McCarthy, Annals of Mathematics
Studies 34, Princeton UP, pp. 43 to 98), the round-1 MINOR-3 fix; `gidney2021stim` (Quantum 5, 497,
2021) is added and cited 3x (abstract L99/L153, §1 L153, §5 L963). The remaining arXiv-as-`@misc`
entries (`koh2024readout`, `adams2015typetheory`, `cho2015effectus`, `qiskit2024`) render cleanly.
No new citation issues from §3.7/§4.6 (both cite only already-present keys).

### Formatting and Production
Fresh full rebuild this round: `pdflatex; bibtex; pdflatex; pdflatex` all exit 0. 17 pp; log shows
**0** undefined refs/cites, **0** LaTeX warnings, **0** overfull/underfull boxes; `bibtex` 0
warnings. New labels all resolve: `sec:crosstalk` to 3.7, `prop:corrparity` to 3.9, `eq:corrparity`
to 3.9, `eq:corrparity-fo` to 3.10, `cor:crosstalk-sign` to 3.10, `sec:worked-crosstalk` to 4.6,
`tab:crosstalk` to Table 3. No format defect.

## Literature Context Summary
No fresh live scout could be launched (recursive `Task` unavailable). The novelty hinge (no prior
reusable *forward, symbolic, asymmetric two-rate* Boolean+tensor readout calculus) is carried from
the prior live prior-art pass and is not contradicted by the new content; §3.7/§4.6 only deepen the
existing contribution. The detector-error-model framing (stim, `gidney2021stim`) added in round 1
correctly positions the design-time state of practice as exact-but-numerical-and-symmetric, against
which the asymmetric symbolic calculus is the genuine gap. All literature conclusions remain
**[needs external verification]** for a fresh 2024 to 2026 sweep.

## Review Metadata
- Specialist lenses applied (all single-context): logic-checker, novelty-assessor,
  methodology-auditor, prose-auditor, citation-verifier, format-validator.
- Recursive `Task` subagents / live web search: **unavailable** (environment).
- Bash execution: **available and used** this round (both scripts run fresh; paper rebuilt;
  new propositions independently re-derived by brute-force enumeration and asymptotic exponent fits).
- Verification method: fresh `python3` runs of both scripts; independent from-scratch re-derivation
  of `prop:corrparity`/`cor:crosstalk-sign` (random-joint brute force plus small-$\lambda$ exponent
  fits: global $m_T$ exponent 0.9999, chain first-order error exponent 1.994); full rebuild plus log
  scan; 20/20 bibcite check; cross-script EPS8/RATES equality check; full read of `main.tex`
  (1 to 1136).
- Cross-verifications performed: 2 (MINOR-1 prose / novelty; NOTE-1 methodology / logic on the
  $2^{|T|}$ prefactor).
- Disagreements noted: 0.
- Net-new findings vs round 1: 0 Major, 1 Minor (residual diagonal-sector density), 5 Notes/
  Suggestions (all cosmetic). The round-1 Major and all round-1 Minors are confirmed **resolved**.
  No regression. The new §3.7/§4.6 math, Table 3, and all §4.6 prose numbers are **verified correct**.
