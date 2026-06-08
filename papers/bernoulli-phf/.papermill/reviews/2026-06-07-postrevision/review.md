# Post-Revision Review: The Perfect Hash Filter

**Date**: 2026-06-07 (post-revision pass)
**Paper**: The Perfect Hash Filter (Alexander Towell, SIUE)
**Root**: `papers/bernoulli-phf/paper/main.tex`
**Reviewer role**: area chair, single-context pass (logic / methodology / novelty / prose /
citation / format lenses applied directly; no live web search, so all prior-art, citation, and
novelty questions are flagged *needs verification* rather than asserted).
**Benchmarks for "par"**: `papers/bernoulli_sets/` (mature primary paper) and
`papers/bernoulli-hash-function/` (the space-optimal sibling this paper is positioned against;
its discussion already cites the PHF).

**Verdict**: **MINOR-REVISIONS**

The salvage + repositioning worked. The new practical-construction thesis is argued
consistently across abstract, intro, related work, body, and conclusion; the load-bearing proofs
introduced or revised this cycle (FPR, inline perfect-hash space bound, `cor:mPHF_size`, the
$k$-perfect $\omega$, the PMF space/entropy bounds, the worked example) are **independently
verified correct to every digit I could check**. What remains are (a) one residual structural
artifact (a stale "C++ implementation" subsection left inside the spine section that contradicts
the repositioning and re-introduces the dropped `oph` dependency), (b) two genuine but
*pre-existing* math errors localized to the mature `adt.tex` section (a wrong corollary factor and
a copy-paste variance estimator), and (c) one non-functional algorithm sketch (`alg:shmap`) plus a
handful of minor notation/prose defects. None of these touches the headline results or the thesis.
The critical/major problems from the 2026-05-29 review (union sign error, duplicated estimator,
empty `\cite{}`, load-bearing `oph`) are all genuinely fixed.

---

## Summary

**Overall Assessment.** This is now a coherent, honestly-framed practical-construction paper whose
core mathematics is sound. The repositioning from "space-optimal / succinct" to "the practical
construction that pays $\log_2 e$ over the optimum for deployability and a cheap tunable FNR" is
carried through every section, and it is *consistent with the sibling paper*: `bernoulli-hash-function`
independently describes the PHF as $\log_2(e/\varepsilon)$ bits/element, "closer to optimal than the
Bloom filter but still exceeds the lower bound" (its `discussion.tex` lines 35-40). The remaining
work is finishing/cleanup, concentrated and low-risk, not research-hard.

**Strengths**
1. **Thesis coherence is achieved.** The practical-vs-optimal positioning is stated identically in
   the abstract, intro, related work, and conclusion; every "instance of" is correctly *negated*
   ("the PHF is **not** an instance of the BHF"); the map-first ($\mu=0$) framing is threaded
   through abstract, intro contribution 1, `pmf.tex`, and `rem:pmf_specializes`. (logic-checker,
   novelty-assessor, prose-auditor)
2. **The load-bearing proofs are correct.** Independently verified: the perfect-hash integral and
   its $\log_2 e$ limit (`thm:mPHF_size`), `cor:mPHF_size`, the binomial-reciprocal identity and
   the $k$-perfect $\omega$ with both limits ($\omega\approx r/2$, $\omega\to e^{-1}$), the entire
   `fig:abs_eff` efficiency table (every digit), and every number in `ex:dictionary`.
   (logic-checker, methodology-auditor)
3. **Honest related work.** The AMQ structure is plainly stated as established prior art; the
   MPHF+fingerprint family (Bloomier/xor/ribbon/cuckoo/Pagh-Pagh-Rao/Dietzfelbinger-Pagh) is cited;
   the contribution is correctly scoped to the Bernoulli-ADT treatment. (novelty-assessor)
4. **The CFGMW lower bound is now a cited theorem, stated once**, no longer a duplicated "postulate";
   the `oph` dependency was removed from the headline space theorem (proved inline). The build is
   clean: 36 pp, 0 undefined refs/cites, 0 multiply-defined labels, 0 bibtex warnings.
   (format-validator, citation-verifier)

**Weaknesses**
1. A **stale "C++ implementation" subsection survives inside `rd_ph_filter.tex`** (the spine),
   re-introducing the `oph` "not tractable" citation and the old CHD `\alpha(1)=2.07` /
   $2^{-4}$-break-even framing that the repositioning was supposed to retire. (Major; structural)
2. Two **pre-existing math errors in `adt.tex`**: the same-FPR union corollary uses factor
   $(1-\alpha/2)$ where the correct value is $1/(1+\alpha)$ (up to 12.5% off in the interior), and
   the "population variance" estimator is a verbatim copy of the mean. (Major)
3. **`alg:shmap` (the PMF construction) is a non-functional sketch**: it writes fingerprints as
   `h(k_j) mod k` with `k` a *bit count*, never stores the salt-searched values it computes, and
   collides notation. The PMF *theorems* are fine; the algorithm illustrating them is not. (Major)
4. A dangling cross-reference (`adt.tex:17` promises a "C++ interface" in `sec:impl`, which no
   longer defines one), a mis-resolving figure `\cref`, a notation-abused `\AbsoluteEfficiency`
   macro, and minor prose/notation slips. (Minor)

**Finding Counts**: Critical: 0 | Major: 3 | Minor: 7 | Suggestions: 5

---

## Critical Issues

None. No finding blocks the paper at the "is the contribution sound and correctly argued" level.
The thesis is coherent and the headline proofs are correct.

---

## Major Issues

### MAJ-1. Stale "C++ implementation" subsection inside the spine contradicts the repositioning and resurrects the dropped `oph` dependency (source: logic-checker, novelty-assessor, format-validator)

- **Location**: `sections/rd_ph_filter.tex`, the `\subsection{C++ implementation}` at line 488 through line 564 (end of file).
- **Quoted text** (line 510): *"The theoretical \gls{gls-phf} based off of the random oracle as described by \cite{oph} is not tractable. Its purpose was to demonstrate theoretical properties."* and (line 534): *"For this \emph{practical} construction (using the hash-displace-compress perfect-hash algorithm~\cite{chd}, which does not attain the idealized lower-bound), the point at which the two are equally efficient is $\fprate \approx 2^{-4}$."*
- **Problem**: The repositioning brief states the old C++ section was "cut (now a short Implementation note pointing to maph)". That created the new `implementation.tex`, but a **second, older C++ subsection was left behind inside `rd_ph_filter.tex`**. It does three harmful things: (1) it re-introduces the `\cite{oph}` dependency on an unpublished manuscript that the salvage explicitly removed from the load-bearing path (and `oph` is otherwise cited nowhere else); (2) it presents a parallel "practical construction" framing with a *different* break-even ($2^{-4}$, CHD $\alpha(1)=2.07$) inside the same section whose idealized analysis gives the $2^{-3}$ break-even, so the reader meets both thresholds 200 lines apart in one section; (3) it duplicates the relative-efficiency-vs-Bloom plot (`fig:rel_eff`) that overlaps `fig:rel_eff_bf_PHF`. The CHD/practical break-even content is legitimate but now belongs with `implementation.tex` (which already cites `chd` and `phobic`), not as a "C++ implementation" subsection in the derivation.
- **Suggestion**: Delete the `\subsection{C++ implementation}` from `rd_ph_filter.tex` (lines 488-564). Move the still-wanted practical-overhead content (the $-\tfrac{1}{r}\log_2\fprate+\alpha(r)$ formula, the CHD $2^{-4}$ break-even, `fig:rel_eff`) into `implementation.tex`, and there reconcile the two break-evens explicitly as "idealized random-oracle MPHF ($2^{-3}$) vs CHD ($2^{-4}$)" the way the body already does at `rd_ph_filter.tex:534`. With the subsection gone, `\cite{oph}` disappears and `oph` can be dropped from `references.bib`. This is the single highest-value cleanup: it removes the only residual contradiction with the new thesis.
- **Cross-verified**: yes, by methodology-auditor (the $oph$ removal was the point of salvage Phase C; this subsection re-creates the dependency) and confirmed by build inspection (`oph` is cited at exactly one site, line 510).

### MAJ-2. Two pre-existing math errors in `adt.tex` (same-FPR union corollary; variance estimator) (source: logic-checker, methodology-auditor)

These are in the mature `adt.tex` section, not in the revised core, so they are *latent* rather than
regressions, but they are genuine and should be fixed before submission.

**(a) Same-FPR union corollary uses the wrong $\alpha$-factor.**
- **Location**: `sections/adt.tex` lines 478-488 (the corollary `\AbsoluteEfficiency(\fprateob \Given \alpha) = (1 + \log_2(2-\fprateob)/\log_2\fprateob)(1 - \alpha/2)`).
- **Problem**: Deriving from the parent theorem with $\varepsilon_1=\varepsilon_2=\varepsilon$ and
  $\alpha=\Card{S_1\cap S_2}/\Card{S_1\cup S_2}$: the denominator is $(\alpha_1+\alpha_2)\log_2\varepsilon=(1+\alpha)\log_2\varepsilon$,
  so the factor must be $1/(1+\alpha)$, not $(1-\alpha/2)$. The two agree only at the endpoints
  $\alpha\in\{0,1\}$ and differ by up to **12.5%** at $\alpha=0.5$ ($1/1.5=0.667$ vs $0.75$).
  $(1-\alpha/2)$ is just the first-order Taylor approximation of $1/(1+\alpha)$. Relatedly, the
  stated limit $\lim_{\varepsilon\to0}\AbsoluteEfficiency=1$ (line 487) holds only at $\alpha=0$;
  for fixed $\alpha>0$ the limit is $1/(1+\alpha)$.
- **Suggestion**: Replace $(1-\alpha/2)$ with $\dfrac{1}{1+\alpha}$ and qualify the
  $\varepsilon\to0$ limit as "for fixed $\alpha$, $\to 1/(1+\alpha)$" (or "$\to 1$ when the operands
  are disjoint, $\alpha=0$").

**(b) "Population variance" estimator is a copy of the mean.**
- **Location**: `sections/adt.tex` lines 248-252.
- **Quoted text**: `s^2_\fprate = \frac{1}{\Card{\Set{U}_p}} \sum_{\Set{X} \in \Set{U}_p} \fprateob(\Set{X})` followed by *"is an unbiased estimator of $\Var{\FPR_\n} = \fprate(1-\fprate)/\n$."*
- **Problem**: The displayed formula is character-for-character the mean estimator $\overline{\fprate}$
  from the equation immediately above it; it has no squared-deviation term, so it equals
  $\overline{\fprate}\approx\fprate$, not the variance $\fprate(1-\fprate)/\n$. The accompanying
  proof (lines 253-266) only proves the *mean* is unbiased and never addresses the variance.
- **Suggestion**: Write $s^2_\fprate=\frac{1}{\Card{\Set{U}_p}}\sum_{\Set{X}}(\fprateob(\Set{X})-\overline{\fprate})^2$
  (or the unbiased $1/(\Card{\Set{U}_p}-1)$ form), and either extend the proof to the variance or
  drop the variance claim. Note also the estimand $\fprate(1-\fprate)/\n$ is the variance of the
  *mean* $\FPR_\n$ across an $\n$-element complement, not of a single observation, so the target and
  the estimator must be matched carefully.
- **Cross-verified**: yes, both verified numerically (corollary factor) and by direct read (variance).

### MAJ-3. `alg:shmap` (the PMF construction algorithm) is non-functional as written (source: logic-checker, methodology-auditor)

- **Location**: `sections/pmf.tex` lines 22-75 (Algorithm "Theoretical implementation of MakeApproxMap").
- **Problem**: The algorithm is an incoherent sketch, even read as a "theoretical implementation":
  (1) the fingerprint write `\matrx{V}[\ph_K(x_j)] \gets \operatorname{h}(k_j) \bmod k` uses
  `k = \lceil\log_2(1/\fprate)\rceil` (a *bit count*) as a modulus, so it stores a value in
  $\{0,\dots,k-1\}$ rather than a $k$-bit fingerprint; (2) the subsequent salt-search loop tests
  `h(k_j \cat b_n) \bmod \operatorname{BL}(v_j^*) = v_j^*` (again `mod` a bit length, and `\bmod` of
  a self-delimiting codeword is undefined), and **never writes the salt-conditioned values back into
  `\matrx{V}`**: the returned `(\matrx{V}, b_n)` carries a `\matrx{V}` populated only by the first,
  unrelated `mod k` loop; (3) the loop variable confusion: the inner check indexes `v_j^*` while
  iterating `i`. The PMF *theorems* (`thm:pmf_lower_bound`, `thm:pmf_entropy`) are correct and
  self-contained, so this is an exposition defect, not a results defect, but the algorithm as printed
  would not produce a valid PMF.
- **Suggestion**: Rewrite `alg:shmap` to mirror the working `alg:PHF`/`alg:k_PHF` structure: build the
  MPHF over the keys; for each key store the self-delimiting value codeword $v_j^*$ at slot
  $\ph_K(k_j)$ in an $M$-bit (or variable-width) slot; the false-positive behavior on out-of-domain
  keys comes from the fingerprint/codeword width, matching `thm:pmf_lower_bound`. If a salt-search
  presentation is wanted (paralleling the BHF), make the search actually constrain the stored bits and
  write them. Alternatively, demote it to prose pointing at the set-case algorithms plus the value
  codeword, since the theorems do not depend on it.
- **Cross-verified**: yes (methodology-auditor confirms the algorithm cannot be executed to produce the
  object the theorems describe; the theorems stand on their own).

---

## Minor Issues

### MIN-1. Dangling "C++ interface" cross-reference (source: prose-auditor, format-validator)
- **Location**: `sections/adt.tex` line 17: *"See \cref{sec:impl} to see how a C++ interface for the Bernoulli set data type may be defined."*
- **Problem**: `sec:impl` is now `implementation.tex`, a prose note about maph/PHOBIC/CHD; it defines
  no C++ interface. The promise is unmet. (A second "C++" mention is the MAJ-1 subsection.)
- **Suggestion**: Reword to "See \cref{sec:impl} for the off-the-shelf perfect-hash libraries that
  realize the construction," or drop the sentence.

### MIN-2. `thm:fp_rate` domain statement vs proof are slightly inconsistent (source: logic-checker)
- **Location**: `sections/rd_ph_filter.tex` `\cref{eq:fp_rate}` (line 198) states
  $\varepsilon\in\{2^{-k}:k\in\mathbb{Z}^+\}\subset(0,1]$; the proof (line 215) says "$M$ is any
  non-negative integer."
- **Problem**: With the usual convention $\mathbb{Z}^+=\{1,2,\dots\}$, the set excludes
  $2^0=1$, yet the interval is written $(0,1]$ (closed at 1) and the proof admits $M=0$
  (giving $\varepsilon=1$). Pick one convention.
- **Suggestion**: Use $k\in\mathbb{Z}_{\ge 0}$ (non-negative integers) to match the proof and the
  closed interval, or change the interval to $(0,1/2]$ and the proof to "positive integer."

### MIN-3. FPR-proof assumption block conflates the perfect hash with a cryptographic hash (source: logic-checker, methodology-auditor)
- **Location**: `sections/rd_ph_filter.tex` lines 177-189 (assumptions enumerate + `asm:ro`).
- **Problem**: Assumption 2, "the rate-distorted perfect hash function $\ph_A$ is a cryptographic
  hash function," is imprecise: $\ph_A$ is a *constructed injection* on $\Set{S}$, not a random oracle
  on the universe; the FPR derivation actually relies on the *fingerprint* hash $h$ (Assumption 3 /
  `asm:ro`), not on $\ph_A$. The enumerate list also overlaps `asm:ro` (two assumption systems for the
  hash), and the block silently switches the set name from $\Set{S}$ (theorem) to $A$ (assumptions).
- **Suggestion**: State that $\ph_{\Set{S}}$ is injective on $\Set{S}$ (definitional, no crypto needed),
  and that the *fingerprint* hash $h$ is the random oracle (`asm:ro`); drop or merge the redundant
  enumerate item; use $\Set{S}$ throughout.

### MIN-4. Conditional independence (Axiom 2) is asserted, not connected to `asm:ro` (source: logic-checker)
- **Location**: `sections/intro.tex` lines 87-89: "The construction of the PHF satisfies both axioms
  under standard cryptographic hash assumptions."
- **Problem**: Element-wise independence (Axiom 1) follows cleanly from `asm:ro`; conditional
  independence of rates (Axiom 2: FPR independent of the objective set given its cardinality) is the
  less obvious one and is not argued anywhere. For the PHF it holds because $\varepsilon=2^{-M}$ is
  set by the fixed fingerprint width $M$ regardless of which keys are stored, but that sentence is
  missing.
- **Suggestion**: Add one clause: "Axiom 2 holds because the false positive rate $2^{-M}$ is fixed by
  the fingerprint width, independent of the stored key set."

### MIN-5. Two cardinality estimators with an under-explained transition (source: prose-auditor)
- **Location**: `sections/rd_ph_filter.tex` `thm:phf_mom_estimator` (line 453) vs the
  "trade space for entropy" estimator $\hat{\Card{\Set{S}}}=-t/\log_2\fprate$ (line 480).
- **Problem**: The first divides by $(-\log_2\fprate+\log_2 e)$ (includes the MPHF floor); the second
  drops the $\log_2 e$ term. They are not contradictory (the second is for a code *deliberately
  inflated* to length $t\gg -m\log_2\fprate$), but the text does not flag why the $\log_2 e$ term
  disappears, and the sentence "We made trade space complexity for entropy" (line 478) is
  ungrammatical.
- **Suggestion**: Fix the sentence ("We can trade space complexity for cardinality entropy") and add a
  half-sentence noting the inflated-code estimator neglects the (now-negligible relative to $t$) MPHF
  term.

### MIN-6. `\AbsoluteEfficiency` notation abuse and inconsistent efficiency macros (source: prose-auditor)
- **Location**: `sty/algorithmnotation.sty:38` defines `\SetKwFunction{AbsoluteEfficiency}{E}` (an
  algorithm2e *keyword*), but `adt.tex` uses `\AbsoluteEfficiency` ~10x as a *math operator* (e.g.
  lines 304, 319, 378, 481). Meanwhile `rd_ph_filter.tex` and the abstract use `\AE` and `\RE`
  (`main.tex:65-66`) for the same two concepts.
- **Problem**: Renders (as "E") but is a notation abuse, and the paper uses two macro families
  (`\AE`/`\RE` vs `\AbsoluteEfficiency`/`\RE`) for absolute/relative efficiency.
- **Suggestion**: Standardize on `\AE`/`\RE` throughout (replace `\AbsoluteEfficiency` in `adt.tex`),
  or define a proper `\DeclareMathOperator`.

### MIN-7. Duplicate figure label and a mis-resolving `\cref` in `adt.tex` (source: format-validator)
- **Location**: `sections/adt.tex`: `\label{fig:cor_union_same_fprate}` appears at line 521 (inside a
  `\COMMENT{}` block) and line 586 (live); `\cref{fig:cor_union_same_fprate}` at lines 463 and 489.
- **Problem**: No "multiply defined" warning fires only because the first label is inside `\COMMENT{}`.
  But the `\cref` at line 463 describes the *two-rate* figure ("as $\fprateob_1\to0$ or
  $\fprateob_2\to0$"), whose figure is the commented-out one, so it silently resolves to the *same-FPR*
  figure (line 586), the wrong figure for that sentence.
- **Suggestion**: Either restore the two-rate figure (it sits ready in the `\COMMENT{}` block, lines
  491-557, but reads absent CSVs `data/*.csv`) with its own label, or reword line 463 to point at the
  same-FPR figure. Also fix the dangling `\BL{X}` (missing parens) at `adt.tex:293` -> `\BL(X)`.

---

## Suggestions (optional improvements)

1. **Precision on the FNR-vs-BHF claim.** The intro/abstract/related-work say the optimal salt-search
   construction "would need combinatorial subset enumeration to admit false negatives." Verified
   against `bernoulli-hash-function`: this is exactly true for the BHF's **equality** predicate
   ($O(\binom{m}{p}p)$ per salt, its `construction.tex` remark line 107), but the BHF's **threshold**
   predicate explicitly *eliminates* the $\binom{m}{p}$ enumeration when $\fnrate>0$ (its intro
   contribution 2, line 39). Consider tightening to "the equality-predicate salt search needs
   combinatorial subset enumeration" or noting the threshold variant trades it for a random/finer FPR,
   so the PHF's $k$-perfect route is still the cheaper *fixed-FPR* path to a tunable FNR. As written the
   claim slightly understates the sibling's threshold result. *(needs verification against the final
   BHF draft, but both papers are the same author's and currently consistent on the equality case.)*

2. **Drop `oph` and uncited self-cites.** Once MAJ-1 lands, `oph` is uncited and should be removed from
   `references.bib`. `aset` and `pmf` are also defined-but-uncited (confirmed via `.aux`); either cite
   them where relevant (the `pmf` paper is the natural forward-reference for the Perfect Map Filter) or
   remove them. `phf` self-cites the paper itself in `adt.tex:332`; consider replacing with a `\cref`.

3. **Wire in the maph experiments (Phase D).** The abstract no longer over-promises experiments (good),
   but the paper's distinguishing asset over its purely-theoretical siblings is the measurable `maph`
   library. A short experiments section (measured FPR vs $2^{-M}$; measured bits/key vs the
   $-\tfrac1r\log_2\fprate+\alpha(r)$ formula; $k$-perfect $\omega$ vs `thm:k_omega` by Monte Carlo;
   throughput vs a real Bloom filter) would lift this from "correct and honest" to "the empirical
   anchor of the family." This is the state file's open Phase D.

4. **`pmf.tex` notation collisions.** Line 6 introduces the partial function $f\colon X\rightharpoonup Y$;
   line 8 then reuses $f$ as "proportion $f$ of the bit patterns" and references "$d$ bits" with $d$
   undefined (should be $M$ or the codeword width). Rename the proportion (it is $\fprate$) and define
   the width.

5. **One end-to-end retrieval example in `apps`.** The applications section is clean but instantiates no
   PHF/PMF numbers (it reads as a generic fuzzy-IR primer). A single worked ranked query over a small
   PMF with concrete fingerprint widths would tie it to the rest of the paper. (Carried over from the
   prior review; not a blocker.)

---

## Focus-Area Findings (as requested)

### 1. Thesis coherence: PASS, with one residual contradiction (MAJ-1)

The practical-construction thesis is argued **consistently** across abstract (`main.tex:146`), intro
(`intro.tex`, esp. the "Relation to the Bernoulli framework" paragraph lines 91-125), related work
(`related_work.tex`, esp. `sec:related_contribution`), and conclusion (`adt.tex:335-342`). Specifically:

- **No residual optimality over-claim in the framing.** Every optimality statement is correctly
  attributed to the BHF; the PHF is "suboptimal by $\log_2 e$." The retained succinctness claim is
  explicitly the *relative* one ("succinct in the relative sense ... we concede the absolute optimum to
  the Bernoulli hash function"), stated identically in abstract, `intro.tex:40-52`/`76-81`, and
  `related_work.tex:35`. This is defensible and self-consistent.
- **No leftover "PHF is an instance of BHF" language.** All four occurrences of "instance of" are
  negations ("not an instance of it," `related_work.tex:16`; "not one as an instance of the other,"
  `intro.tex:117`, `adt.tex:342`) or the *correct* positive use ("the perfect-hash instance of this
  **AMQ family**," `related_work.tex:19`). Cross-verified against the sibling: `bernoulli-hash-function`
  treats them as two distinct constructions (its `discussion.tex:35-44`), matching.
- **Map-first framing is carried through.** The set-as-$\mu=0$-special-case is in the abstract,
  intro contribution 1, `related_work.tex:32`, `pmf.tex` (whole section), and `rem:pmf_specializes`
  ("Setting $\mu=0$ ... recovers `thm:mPHF_size`"). Consistent.
- **The two break-even thresholds are reconciled** ($2^{-3}$ idealized vs $2^{-4}$ CHD, explicitly at
  `rd_ph_filter.tex:534`), resolving a prior-review contradiction.

The **one** place the old framing still contradicts the new positioning is **MAJ-1**: the leftover
"C++ implementation" subsection in `rd_ph_filter.tex`, which re-introduces `oph` and a parallel
practical-construction narrative inside the spine. Removing it completes the repositioning.

### 2. Proof correctness: all load-bearing results VERIFIED

Independently checked (numerically and/or by derivation); all correct:

| Result | Location | Verification |
|---|---|---|
| FPR $=2^{-M}$, zero FN | `thm:fp_rate` | Sound (one domain nit, MIN-2). |
| Perfect-hash integral $\to \log_2 e - (\tfrac1r-1)\log_2\tfrac{1}{1-r}$ | `thm:mPHF_size` | Integral, antiderivative $\int_0^r\ln(1-u)du=-(1-r)\ln(1-r)-r$, and $r\to1$ limit $=\log_2 e$ all verified to $<10^{-15}$. |
| Minimal bound $\log_2(e/\fprate)$ | `cor:mPHF_size` | Correct ($r=1$ specialization and direct derivation agree). |
| $\binom{n}{j}^{-1}$-style identity $\Expect{1/(1+B)}=\frac{1-(1-p)^{n+1}}{(n+1)p}$ | `eq:binom_recip` | Verified vs direct summation, exact. |
| $\omega=1-\frac{N}{m}(1-(1-\tfrac1N)^m)=1-\Expect{\RV O}/m$ | `thm:k_omega` | $\omega$ via $1-\Expect{1/L}$ equals the occupied-slots form, exact. |
| $\omega\to 1-(1-e^{-r})/r$; $\omega\approx r/2$ ($r\to0$); $\omega\to e^{-1}$ ($r=1$) | `eq:k_omega_asym`, `rem:omega_limits` | All verified ($r/2$ ratio $\to1$ as $r\to0$; $\omega_{\rm asym}(1)=0.367879=1/e$). |
| PMF space $\log_2 e-(\tfrac1r-1)\log_2\tfrac1{1-r}+\tfrac1r(-\log_2\fprate+\mu)$; minimal $=\log_2 e-\log_2\fprate+\mu$ | `thm:pmf_lower_bound` | Decomposition correct; minimal $=$ BHF floor $(-\log_2\fprate+\mu)+\log_2 e$, consistent with "PHF pays $\log_2 e$ over the optimum." $\mu=0$ recovers `thm:mPHF_size`. |
| PMF entropy upper bound $=$ lower bound | `thm:pmf_entropy` | Sound given the max-entropy seed + codeword argument (parallels `thm:max_entropy_coder`). |
| `fig:abs_eff` table ($r^*$, $e^*(X)$, $e(X,Y)$) | `rd_ph_filter.tex:325-343` | Every published digit reproduced by independent ternary-search minimization. |
| `ex:dictionary` ($m=10^6$, $\fprate=2^{-16}$): 17.4427 vs 23.0831 bits/elem, 75.6%, $\RE=1.32$, $\AE=0.917$, $M^*\approx3.26$, 2.18 vs 2.89 MB | `rd_ph_filter.tex:293-318` | Every number verified exactly. |
| Union induced FPR $=\varepsilon_1+\varepsilon_2-\varepsilon_1\varepsilon_2=1-(1-\varepsilon_1)(1-\varepsilon_2)$ | `thm:union_space_complexity` | **Sign now correct** (the prior-review C1 fix holds); the AE ratio is positive and in $(0,1)$ as it should be. |

**Errors found** are confined to `adt.tex` (MAJ-2: the same-FPR *corollary* factor $1/(1+\alpha)$ vs
$(1-\alpha/2)$, and the variance estimator) and to the `alg:shmap` *algorithm* (MAJ-3); the
corresponding *theorems* are correct. Unstated-assumption nits: MIN-3 (perfect hash vs crypto hash),
MIN-4 (Axiom 2 connection).

Cross-verification of the BHF claims (read `bernoulli-hash-function` intro/construction/space/discussion):
the PHF's characterization of the BHF as (i) salt search, (ii) reaching $-\log_2\fprate+\mu$ exactly,
(iii) needing combinatorial subset enumeration for FNR>0, and (iv) building by a different mechanism is
**accurate** for the equality predicate; the only refinement is that the BHF's *threshold* predicate
also avoids the enumeration (Suggestion 1).

### 3. General review: clean and submittable after the above

Beyond the grouped findings: build is clean (36 pp, 0 undefined, 0 multiply-defined, 0 bibtex
warnings; only cosmetic overfull-hbox messages). House style respected (no em-dashes in the sources; no
banned promotional adjectives detected). No `dummyref`/`???`/`$?$`/empty-cite/empty-ref artifacts
remain (all fixed since 2026-05-29). The figure `img/phfilter.tex` is now a real TikZ schematic, not a
stub. Structural gaps are the three Majors plus the commented-out two-rate figure in `adt.tex`
(reads absent CSVs).

---

## Detailed Notes by Domain

### Logic and Proofs
Headline results correct (table above). Three localized defects: the leftover `oph`-citing C++
subsection (MAJ-1, also a logic/consistency issue since it asserts a different break-even in the same
section), the `adt.tex` corollary/variance errors (MAJ-2), and the non-executable `alg:shmap` (MAJ-3).
Minor: `thm:fp_rate` domain (MIN-2), FPR-proof assumption conflation (MIN-3), Axiom-2 assertion (MIN-4).
The 2026-05-29 logic-checker's C1/M1/M2/M3/M4 are all genuinely resolved.

### Novelty and Contribution
Honestly scoped and well-differentiated. The base AMQ structure is correctly disclaimed; the
contribution (Bernoulli-ADT realization + $k$-perfect two-rate analysis + map/fuzzy-IR application +
tie to the CFGMW bound) is legitimate for an implementation paper and does not overlap the BHF paper
(which owns the optimal construction). *Needs verification* (no web): the specific prior-art
attributions (xor/ribbon/cuckoo/Bloomier as the established MPHF+fingerprint family; CFGMW as the
$-\log_2\fprate$ source), but these are standard and the `.bib` entries look correct.

### Methodology
The probabilistic model (random oracle for the fingerprint; balls-into-bins for $k$-perfect occupancy)
is appropriate and the derivations follow from it. `asm:uniform_slots` + `def:loss` make $\omega$
derivable rather than posited (good). Gaps: the perfect-hash *injective-placement* assumption vs the
crypto-hash wording (MIN-3); no empirical validation yet (Suggestion 3, the maph experiments). The
`alg:shmap` defect (MAJ-3) is methodological in that the printed construction does not realize the
analyzed object.

### Writing and Presentation
Generally clear and well-threaded. Defects: the dangling "C++ interface" pointer (MIN-1), the
ungrammatical "We made trade..." (MIN-5), the `\AbsoluteEfficiency` macro abuse and `\AE`/`\RE`
inconsistency (MIN-6), the `\BL{X}` parens and mis-resolving figure `\cref` (MIN-7), and the
`pmf.tex` notation collisions $f$/$\fprate$/$d$ (Suggestion 4). The abstract is long (one dense
paragraph, ~290 words) but accurate; optional to tighten.

### Citations and References
Bibliography is clean and resolves (0 bibtex warnings). 16 real external entries + dated self-cites
with real GitHub URLs. Issues: `oph` is load-bearing only for the to-be-deleted C++ subsection (drop
with MAJ-1); `aset` and `pmf` are defined-but-uncited (confirmed in `.aux`); `phf` self-cites the
paper in `adt.tex:332` (use `\cref`). *Needs verification*: `dillinger2021` carries `year={2022}` with
a 2021 key (cosmetic); `graf2020` is typed `@article` (correct, JEA). No invented DOIs detected.

### Formatting and Production
Build clean: 36 pp, exit 0 on all passes, 0 undefined refs/cites, 0 multiply-defined labels (the
prior `pst:approx_l_b` collision is gone; the lower bound is stated once as a cited theorem). Only
cosmetic overfull `\hbox` warnings (algorithm boxes, two paragraphs) and pgfplots backward-compat
notices. The commented-out two-rate figure in `adt.tex` and the duplicate-but-shielded
`fig:cor_union_same_fprate` label (MIN-7) are the only production loose ends.

---

## Literature Context Summary (no web; cross-paper only)

Calibrated against the two in-repo benchmarks:
- **`bernoulli_sets/`** (mature primary): supplies the model, the two axioms, the composition theorem
  $\eta_{\rm total}=1-\prod(1-\eta_i)$, and the binomial error counts the PHF inherits. The PHF's
  framework-relation paragraph correctly defers to it.
- **`bernoulli-hash-function/`** (the optimal sibling): independently confirms every PHF claim about
  the BHF (salt search, exact $-\log_2\fprate+\mu$ floor, $\binom{m}{p}$ enumeration for FNR>0)
  (equality predicate), and it already cites the PHF as $\log_2(e/\fprate)$, "closer to optimal than
  the Bloom filter but still exceeds the lower bound." The two papers are mutually consistent in their
  positioning. The single refinement (Suggestion 1): the BHF's *threshold* predicate also avoids the
  combinatorial enumeration, which the PHF's blanket "salt search needs subset enumeration" slightly
  understates.

*External prior-art / novelty / citation-accuracy questions are flagged needs-verification throughout;
none is decisive for the verdict.*

---

## Review Metadata
- Agents used: area chair (single-context), applying logic-checker, methodology-auditor,
  novelty-assessor, prose-auditor, citation-verifier, and format-validator lenses directly.
- Independent verifications performed: full build chain (36 pp, 0 undefined); numerical verification of
  the perfect-hash integral + antiderivative + limit, the binomial-reciprocal identity, the $k$-perfect
  $\omega$ and its three limits, the entire `fig:abs_eff` table, the `ex:dictionary` worked example, the
  union induced-FPR sign, the same-FPR corollary factor (error confirmed), and the variance-estimator
  formula (error confirmed); cross-read of `bernoulli-hash-function` (intro/construction/space/discussion)
  to verify all BHF claims; cross-read of `bernoulli_sets` CLAUDE/topic placement.
- Cross-verifications: MAJ-1 (logic + methodology + format), MAJ-2 (logic + methodology, numeric),
  MAJ-3 (logic + methodology).
- Disagreements noted: 0 (correctness vs clarity separated where relevant; e.g. PMF *theorems* sound
  while the PMF *algorithm* is defective, both stand).
- Items flagged needs-verification (no web): external prior-art attributions; `carter1978` as the
  $-\log_2\fprate$ source; modern-filter overhead figures; the BHF threshold-predicate refinement
  against the final BHF draft.
