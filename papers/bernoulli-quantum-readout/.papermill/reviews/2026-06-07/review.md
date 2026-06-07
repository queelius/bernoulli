# Multi-Agent Review Report

**Date**: 2026-06-07
**Paper**: A Forward (epsilon, omega) Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes
**Author**: Alexander Towell
**Recommendation**: minor-revision

## Severity counts

| Severity   | Count |
|------------|-------|
| Critical   | 0     |
| Major      | 4     |
| Minor      | 7     |
| Suggestion | 7     |

The four Major findings are about *demonstrating and verifying* the
contribution (an unquantified independence assumption, a symmetric-only worked
example, and two unverifiable-as-written novelty/unification claims). None is a
correctness defect. The mathematics is sound and the build is clean, which is
why the recommendation is minor-revision rather than major-revision.

## Summary

**Overall assessment**: This is a well-written, scope-honest theory/perspective
paper whose mathematical core is entirely correct (every theorem, proposition,
corollary, and every digit of Table 1 was independently verified by symbolic
algebra and Monte Carlo) and whose build is production-clean (11 pages, zero
undefined references/citations, zero bad boxes). The contribution is genuine but
modest: its value is conceptual organization (a reusable, forward, asymmetric
Boolean calculus) and a quotable corrective to the "n times q" syndrome-error
folklore, rather than any individually novel formula. The work needed before
publication is to *demonstrate* the asymmetric machinery on a genuinely
asymmetric example, to *bound or frame* the independence assumption it leans on,
and to make its most distinctive claims (the no-prior-forward-calculus novelty
and the Bernoulli/Bloom unification) externally checkable.

**Strengths**:
1. The mathematics is correct throughout. Every result in Section 3 and every
   number in Table 1 was independently reproduced (logic-checker; confirmed by
   the orchestrator via sympy and Monte Carlo). (logic-checker)
2. Exemplary scope discipline. Diagonal-sector faithfulness and the independence
   assumption are each stated before use and re-stated consistently in four
   places, with Bell / Kochen-Specker / Fine correctly named as the
   out-of-scope obstructions. (methodology-auditor)
3. Honest novelty framing. The explicit not-claimed/claimed list (sec:scope item
   4) disclaims the asymmetric channel, the tensor factorization, and the parity
   formula, and claims only the forward asymmetric calculus, the readout
   application, and the unification. This candor is rare and valuable.
   (novelty-assessor)
4. Strong, confident prose with a clear narrative arc and a fully resolved
   cross-reference apparatus. (prose-auditor, format-validator)
5. The "n times q" overestimate is a real, quotable, correct corrective: Table 1
   shows the linear rule overstates the true syndrome-flip rate by up to 40.5%
   at q = 0.05, n = 8, and the saturation-at-1/2 argument is exact.
   (logic-checker)

**Weaknesses**:
1. The independence assumption is load-bearing and the paper criticizes the
   linear rule for inaccuracy, yet never bounds or frames its own inaccuracy when
   independence fails (crosstalk). (methodology-auditor)
2. The single worked example is symmetric (q_i = q), so the headline asymmetric
   two-rate machinery never produces a concrete asymmetric number anywhere in the
   paper. (methodology-auditor)
3. The most load-bearing novelty claim ("no reusable forward asymmetric
   calculus exists") could not be verified in this run and rests on an
   unestablished absence of a direct competitor. (novelty-assessor)
4. The signature unification claim is supported only by five unpublished,
   locator-free self-citations, making it uncheckable by a reader.
   (novelty-assessor, citation-verifier)

**Finding counts**: Critical: 0 | Major: 4 | Minor: 7 | Suggestions: 7

---

## Critical Issues

None.

---

## Major Issues

### M1. Independence is assumed but its failure is never quantified or framed (source: methodology-auditor)
- **Location**: sec:scope item 2 (lines ~677-687); the assumption is declared at
  the head of sec:calculus (line ~277).
- **Quoted text**: "Every closed form above holds under per-bit channel
  independence ... Real devices exhibit measurement crosstalk ... A
  correlated-channel extension ... is future work; the present calculus is the
  independent/tensor regime."
- **Problem**: The paper's Table 1 thesis is that the field's linear rule
  *overestimates by tens of percent*. A reader will symmetrically ask how far the
  paper's own independent rule is off when the independence it assumes fails.
  That question is currently unanswered: there is no sensitivity statement, not
  even a directional one (e.g. whether the independent prediction bounds the
  correlated rate from one side).
- **Suggestion**: Add a one-paragraph worst-case or directional statement, or
  frame the independent prediction as the named reference point against which
  crosstalk corrections are measured. Even a single inequality would close this.
- **Cross-verified**: yes, routed to logic-checker. The independent calculus is
  logically sound exactly under its stated hypothesis; this is a
  demonstration/positioning gap, not a logic error. The two specialists agree:
  correctness stands, the framing gap stands. No disagreement.

### M2. The worked example is symmetric, so the asymmetric contribution is never demonstrated numerically (source: methodology-auditor)
- **Location**: sec:worked, setup (line ~508) and Table 1 (lines ~537-560).
- **Quoted text**: "consider the symmetric per-measurement rate $q_i=q$ for
  clarity (\cref{cor:parity-asym} handles the asymmetric and inhomogeneous case
  verbatim)."
- **Problem**: The headline novelty is the *asymmetric* two-rate calculus, but
  every number in the paper is reproducible from the *symmetric* single-rate
  identity that the paper itself attributes to prior art. The asymmetry the paper
  is built to preserve never appears in a computed value.
- **Suggestion**: Add an asymmetric, inhomogeneous instance (a syndrome bit with
  T1-biased ancillas at distinct epsilon_i, omega_i), showing the two latent-
  parity sides carrying different error. This makes the novel content visible
  rather than asserted, and exercises cor:parity-asym (the paper's most original
  result) on numbers.
- **Cross-verified**: yes. cor:parity-asym was verified correct for all 8 latent
  assignments of an asymmetric inhomogeneous channel by the orchestrator's Monte
  Carlo, so the machinery to produce such a table already works; only the
  exhibition is missing. logic-checker concurs the result is sound.

### M3. The central novelty claim rests on an unverified absence of a competitor (source: novelty-assessor)
- **Location**: sec:intro (lines ~138-141).
- **Quoted text**: "There is at present no reusable, closed-form, forward
  calculus that answers this question while preserving the asymmetry."
- **Problem**: This absence-of-prior-art claim is the hinge of the paper's
  novelty. It could not be verified in this run (no live literature search). Each
  individual formula is elementary and admitted as prior art; the novelty is
  entirely the synthesis, so a single existing forward asymmetric readout
  calculus, or QEC tooling that already propagates two-sided rates symbolically
  through syndrome logic, would reduce "the missing piece" to "a unified
  restatement."
- **Suggestion**: Before publication, run a targeted prior-art search for (a) a
  prior forward asymmetric Boolean readout calculus and (b) whether tensored-
  mitigation tooling already propagates asymmetric rates forward. If a competitor
  exists, soften the framing; if not, cite the search to harden the claim.
- **Cross-verified**: yes, routed to prose-auditor. prose-auditor independently
  flagged audience ambiguity (the unification is decoration for a QEC reader,
  news for a Bernoulli reader), which is the framing half of the same issue. The
  two findings are complementary, not contradictory: M3 is the novelty-
  verifiability axis, the prose finding is the audience-framing axis.

### M4. The signature unification claim is supported only by locator-free unpublished self-citations (source: novelty-assessor, citation-verifier)
- **Location**: sec:intro (line ~151), sec:related unification paragraph
  (lines ~653-662), and the five `@unpublished` entries in references.bib.
- **Quoted text**: "it is the error model of Bernoulli type theory ... whose
  special cases include Bloom filters, perfect hash filters, and cipher maps
  \citep{bernoulliSets,bernoulliComposition,bernoulliMaps,bernoulliRelations}."
- **Problem**: The unification is the paper's most distinctive contribution, yet
  all five supporting references are `@unpublished` with note "Companion paper,
  Bernoulli type theory" and no DOI, URL, or arXiv/Zenodo locator. A reader
  cannot follow the claim to its source, so the most novel assertion is currently
  uncheckable.
- **Suggestion**: Add Zenodo DOIs (concept + version, per the stated publication
  strategy) to the five framework entries, and/or include a self-contained one-
  paragraph statement of the Bernoulli error model so the unification stands on
  its own without the companion papers.
- **Cross-verified**: concordant across novelty-assessor and citation-verifier
  (same finding from two angles: novelty-verifiability and bibliographic
  locatability). No disagreement.

---

## Minor Issues

### m1. AND theorem FPR clause is stated unconditionally but is a latent corner (source: logic-checker)
- **Location**: thm:andor, eq:and-fpr (lines ~316-319).
- **Problem**: The FNR clause conditions cleanly ("conditions on the only latent
  assignment making the conjunction true, all $t_i=1$"), but the FPR clause reads
  as an unconditional rate, then the proof and remark clarify it is the all-
  negative *corner*. Correct, but a reader who stops at the equation could
  mistake a corner for the marginal FPR.
- **Suggestion**: Add "conditioned on all latent inputs false" to the FPR
  sentence, mirroring the FNR clause. (Verified: the corner-is-smallest claim is
  itself correct, confirmed by Monte Carlo.)

### m2. Five framework self-citations carry no DOI/URL (source: citation-verifier)
- **Location**: references.bib, the five `bernoulli*` entries.
- **Problem**: `@unpublished`, locator-free; unfollowable. (This is the
  bibliographic face of M4; kept here as the concrete bib fix.)
- **Suggestion**: Add Zenodo locators once minted.

### m3. Parity-identity attribution is loose for the exact formula (source: citation-verifier)
- **Location**: thm:parity discussion (line ~428) and sec:related (c).
- **Problem**: von Neumann 1956 / Pippenger 1988 own the noisy-formula
  *reliability tradition*, but the exact +-1-encoding parity-bias identity is
  folklore / coding-theory / Boolean-function analysis. Attributing the lineage
  to them is defensible; attributing the precise formula is loose.
- **Suggestion**: Rephrase to "in the tradition of," or add a precise pointer
  (e.g. Boolean-function-analysis text). Note: this needs an external pass.

### m4. Rate subscripts overload index vs connective (source: prose-auditor)
- **Location**: sec:calculus, throughout (epsilon_i vs epsilon_wedge).
- **Suggestion**: One line at the head of sec:calculus noting subscripts are
  either qubit indices or connective tags.

### m5. q / r / q_i play three roles across two pages (source: prose-auditor)
- **Location**: thm:parity (q_i), cor:parity-asym (r_i), sec:worked (q).
- **Suggestion**: A one-line bridge in sec:worked: the example's q is the
  symmetric per-measurement error, i.e. r_i = q for all i in cor:parity-asym.

### m6. Long, em-dash-chained sentences tax the reader (source: prose-auditor)
- **Location**: abstract; sec:worked "Reading the table" closing; thm:andor
  proof.
- **Suggestion**: Split the longest sentences. (Stylistic; em-dashes in the paper
  source itself are fine.)

### m7. Four cosmetic hyperref PDF-string warnings (source: format-validator)
- **Location**: build log; from math in the title and section headings.
- **Problem**: hyperref "Token not allowed in a PDF string (Unicode)" x4. Affects
  only PDF outline/metadata, not the rendered document.
- **Suggestion**: Add \texorpdfstring or \hypersetup{pdftitle=...} to silence.

---

## Suggestions

1. (S-meth-1) Ship the 5-line Table 1 generator or a bernoulli-py notebook cell
   as an ancillary artifact, so the "costs nothing, it is one product" claim is
   literally executable. (methodology-auditor)
2. (N3) Resolve audience ambiguity: the Bloom-filter/cipher-map unification is
   decoration for a QEC reader and the news for a Bernoulli reader; pick a primary
   audience and order the contributions accordingly. (novelty-assessor)
3. (N4) Verify the "they symmetrize / single-rate" criticism is not too strong
   for the cited mitigation tools, which retain asymmetric per-qubit 2x2 channels;
   narrow it to single-rate folklore and symmetrized summary reporting if needed.
   (novelty-assessor)
4. (C3) Rename cite-key `pucha2021certification` to the lead author (Krawiec) to
   avoid a misleading key. Cosmetic. (citation-verifier)
5. (P4) The abstract names four neighbors but sec:related delivers five; reconcile.
   (prose-auditor)
6. (P5) The "n times the per-measurement error" folklore is aired four times
   (abstract, intro, sec:worked, conclusion); trim one. (prose-auditor)
7. (P6) Consider shortening the long title. (prose-auditor)

---

## Detailed Notes by Domain

### Logic and Proofs
All seven results in Section 3 are correct. Verified independently: NOT swaps
rates (prop:not); AND FPR = prod(epsilon_i) at the all-negative corner and AND
FNR = 1 - prod(1-omega_i) (thm:andor), with the "corner is smallest not largest"
claim confirmed by Monte Carlo; the OR dual; the composition theorem
eta_total = 1 - prod(1-eta_i) and its exact identity with the AND-FNR rule; the
parity identity 1/2(1 - prod(1-2q_i)) (checked against direct enumeration at
n=2); and the asymmetric parity corollary across all 8 latent assignments of an
asymmetric inhomogeneous channel. Table 1 reproduces to every printed digit, and
the Taylor expansion P_exact = nq - n(n-1)q^2 + O(q^3) is symbolically exact (the
q-coefficient is n, the q^2 coefficient is -n(n-1)). One minor statement-level
imprecision (m1). The dependency graph is acyclic and independence is used
consistently. No Critical or Major logic finding.

### Novelty and Contribution
Genuine but modest. The individual formulas are elementary and honestly
disclaimed; the contribution is the synthesis (forward + asymmetric + reusable +
unified). Two Major findings: the no-prior-forward-calculus claim is unverifiable
in this run (M3), and the unification rests on locator-free unpublished self-
cites (M4). For the stated Zenodo-preprint venue the contribution clears the bar;
for a competitive archival venue it needs the asymmetric demonstration (M2) and a
grounded novelty statement (M3).

### Methodology
Appropriate for a theory paper: assumptions stated before use, honest scope,
single reproducible computation. Two Major gaps are about demonstrating the
contribution: the unquantified independence assumption (M1) and the symmetric-
only worked example (M2). No correctness or reproducibility defect.

### Writing and Presentation
Strong, confident, well-signposted. Issues are density (long em-dash-chained
sentences, m6) and notation bridges (q/r/index roles, m4/m5). cleveref usage is
clean and all targets resolve. No Critical or Major prose finding.

### Citations and References
Internal integrity is perfect: 16 entries, all 16 cited, zero uncited, zero
undefined, zero real bibtex warnings. (The state file's "16 entries, all cited,
zero placeholders" is accurate.) External entries are plausible and broadly
correctly attributed; the parity attribution is loose (m3) and the cite-key for
pucha2021certification is mildly misleading (S4). The five framework self-cites
are locator-free (m2/M4). Several specific external facts (pucha2021certification
fields, the "8-30%" figure from tannu2019mitigating, whether CTMP is in
bravyi2021mitigating) need an external verification pass.

### Formatting and Production
Production-clean. 11 pages, zero undefined references/citations, zero
overfull/underfull boxes, zero multiply-defined labels, all 27 labels resolve.
Only four cosmetic hyperref PDF-string warnings (m7). Generic article class,
appropriate for a Zenodo preprint; venue restyling is trivial when targeted.

## Literature Context Summary
The forward / symbolic / design-time niche is plausibly under-occupied: the
mitigation literature (M3, Bravyi et al., tensored mitigators) is inverse,
numerical, and per-circuit. Asymmetry from T1 is well established (Tannu/Qureshi,
Hicks et al.), so the novelty is the forward propagation of both rates through
connectives, not the observation of asymmetry. The effectus and hypothesis-
testing neighbors are correctly distinguished (structure vs rates; one decision
vs composition). The CTMP citation the TODO seeks is likely already in the bib
(bravyi2021mitigating). The one load-bearing risk that could not be closed
without live search is the existence of a direct forward-asymmetric-readout-
calculus competitor (M3). Full caveats and the [needs external verification]
markers are in literature-context.md.

## Review Metadata
- Specialist reports written: logic-checker, methodology-auditor, novelty-
  assessor, prose-auditor, citation-verifier, format-validator, plus the merged
  literature-context.
- Agents dispatched as subagents: 0. The Task tool was unavailable in this
  execution context (no recursive subagents), so the orchestrator performed all
  specialist analyses single-context, with independent symbolic-algebra and
  Monte Carlo verification of every mathematical claim and a full build pass.
  Citation and novelty findings that would normally be scout-verified against the
  live literature are explicitly marked as needing an external pass.
- Cross-verifications performed: 2 (M1 routed to logic-checker; M3 routed to
  prose-auditor). Both concordant.
- Disagreements noted: 0.
- Independent computational checks by the orchestrator: Table 1 (all 6 rows),
  the Taylor expansion (sympy), and Monte Carlo confirmation of thm:andor (FPR
  corner + FNR), the OR dual, cor:parity-asym (all 8 latent assignments), and the
  composition/AND-FNR identity. Full LaTeX build (pdflatex + bibtex + 2 passes):
  clean, 11 pages, zero undefined refs/citations.
```
