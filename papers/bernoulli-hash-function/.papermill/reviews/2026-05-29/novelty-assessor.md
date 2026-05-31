# Novelty Assessor Report

**Paper:** The Bernoulli Hash Function
**Date:** 2026-05-29
**Focus (per area chair):** differentiation from classic optimal-Bloom-filter
constructions (Pagh-Pagh-Rao, Bloomier filters, cuckoo/xor filters,
Carter-Wegman). Assess novelty *relative to this paper's declared role* as the
optimal-construction application paper in the Bernoulli family.

## Overall Assessment

The paper makes a real contribution, and its positioning relative to prior art
is much improved since 2026-02-26. The previously decisive weakness (claiming
space-optimality without acknowledging that achievability is a known result of
Pagh-Pagh-Rao 2005 and that the bound is Carter et al. 1978) is now addressed in
the discussion. With those citations in place, the honest novelty of the paper
resolves into three things: (1) a single construction that is optimal for both
sets and maps via the mu = 0 specialization, (2) the threshold / generalized
acceptance predicate that gives a fine FPR lattice and removes subset
enumeration, and (3) the adaptive-threshold variant and its "price of FPR
certainty" interpretation. Item (3) is the genuinely novel and most valuable
piece. Items (1) and (2) are sound but incremental.

This is appropriate novelty for a *family application paper*. The job here is
not to discover the lower bound (that is `bernoulli_entropy` and Carter et al.)
but to exhibit the optimal *construction* and tie the family's `-log2(eps) + mu`
bound to a concrete maximum-entropy encoder. Judged against that role, the
contribution is adequate for a strong venue, contingent on the framing fix
below and on closing the remaining map prior-art gap.

## Findings

### MAJOR-1: Intro contribution list still claims optimality without the
Pagh-Pagh-Rao caveat that the discussion now makes
- **Location:** `sections/intro.tex`, contribution 3 (lines 44-47) versus
  `sections/discussion.tex` (the Pagh-Pagh-Rao paragraph, lines 78-84).
- **Quoted text (intro):** "We prove that the BHF achieves the information-
  theoretic lower bound on space complexity while maximizing the entropy of its
  binary representation, under both predicate forms and for both sets and maps."
- **Problem:** Read in isolation, contribution 3 reads as if achieving the bound
  is the novelty. The discussion correctly states that Pagh-Pagh-Rao (2005)
  already achieves the bound with *polynomial* construction, whereas the BHF's
  fixed-threshold construction is *exponential*. The novelty is therefore the
  *maximum-entropy* character of the encoder and the *adaptive trade-off*, not
  achievability per se. The intro should carry that nuance so a reader does not
  form the wrong impression of the claim before reaching Section 9.
- **Suggestion:** Reword contribution 3 to foreground what is new: "We exhibit a
  maximum-entropy construction that meets the `-log2(eps) + mu` bound exactly
  for both sets and maps, and we introduce an adaptive variant that trades a
  fixed FPR for a random one to sidestep the bound entirely; we show the
  `-log2(eps)` term is precisely the price of FPR certainty (Thm 5.7)." Note up
  front that exact-bound achievability with polynomial time is due to
  Pagh-Pagh-Rao and that the BHF's distinction is the entropy/obliviousness
  property and the adaptive construction.
- **Severity:** Major. This is a framing/credit issue, not a correctness issue,
  but at a top venue it is the difference between "honest incremental" and
  "overclaiming."

### MAJOR-2: Missing the closest map prior art (Bloomier filter) and the closest
membership/retrieval theory (Dietzfelbinger-Pagh)
- **Location:** `sections/discussion.tex`, comparison subsection (lines 25-84).
- **Problem:** The paper claims a *unified set and map* optimal construction, but
  the discussion compares only against membership filters (Bloom, cuckoo, XOR,
  ribbon, Pagh-Pagh-Rao) plus the author's own PHF/PMF. The canonical
  approximate-map structure, the **Bloomier filter** (Chazelle, Kilian,
  Rubinfeld & Tal 2004), is absent, as is the **Dietzfelbinger-Pagh (2008)**
  retrieval framework, which is the closest theoretical relative of the BHF's
  "store the value in the hash evidence" mechanism. For a paper whose
  *unification* with maps is contribution 1, omitting the standard map structure
  is a conspicuous gap.
- **Suggestion:** Add a short paragraph (and two bib entries) comparing the BHF
  *map* with the Bloomier filter and retrieval structures: the Bloomier filter
  stores the value in a separate spine; the BHF folds value bits into the same
  hashed evidence that certifies membership, which is what lets one space-
  optimality proof cover both. This sharpens, rather than dilutes, the novelty.
- **Severity:** Major (for a venue that takes the map claim seriously); see also
  citation-verifier MAJOR-1.

### MINOR-1: "Unified construction" is a clean design choice more than a
standalone contribution
- **Location:** `sections/intro.tex`, contribution 1.
- **Problem:** That a per-element data structure extends to a map by appending
  value bits is natural (it is exactly what retrieval structures do). Presented
  as a co-equal contribution, it slightly inflates the count.
- **Suggestion:** Keep it, but present it as the organizing principle (as the
  remark after `post:map_lb` already does well) rather than as contribution 1 of
  3. Lead with the adaptive threshold.
- **Severity:** Minor.

### MINOR-2: The adaptive threshold, the strongest result, is still under-
weighted structurally
- **Location:** Adaptive material is `sec:adaptive` (a subsection of Sec. 3),
  plus `sec:adaptive_space`, `sec:price_certainty`, and
  `sec:adaptive_entropy`.
- **Observation:** Since the prior pass, the adaptive treatment grew
  substantially (FPR distribution, moments, a dedicated space subsection, the
  price-of-certainty theorem with two figures, and an entropy analysis). This is
  a real improvement and largely answers the prior MINOR. What remains is
  presentational: the title and abstract still lead with "optimal" (the known
  part) rather than with the adaptive trade-off (the new part).
- **Suggestion:** Consider a title/abstract emphasis shift so the order-statistic
  adaptive construction and the price-of-certainty result are the headline.
- **Severity:** Minor.

## Contribution Summary

| Contribution | Novelty | Significance | Notes |
|---|---|---|---|
| Unified set/map construction (mu = 0) | Low | Medium | Clean organizing principle; not a surprise |
| Threshold / generalized acceptance predicate | Medium | Medium | Fine FPR lattice; removes subset enumeration |
| Adaptive threshold (order-statistic) | High | High | No prior-art analogue in filters |
| Price of FPR certainty (Delta = m log2(1/eps)) | High | High | Elegant info-theoretic reframing of the LB |
| Exact-bound achievability | Low | Medium | Known (Pagh-Pagh-Rao); novelty is max-entropy |
| Maximum-entropy / obliviousness property | Medium | Medium | Valuable for the encrypted-search application |

## Recommendation (novelty lens)

Acceptable contribution for a strong theory/data-structures venue *as a family
application paper*, conditional on: (a) reframing contribution 3 and the
title/abstract around the adaptive trade-off and the maximum-entropy property
rather than around achievability (MAJOR-1), and (b) situating the map result
against the Bloomier filter and retrieval structures (MAJOR-2). These are
framing and related-work fixes, not new research. Do not penalize the paper for
building on `bernoulli_sets`/`bernoulli_entropy`; that is its declared role.
