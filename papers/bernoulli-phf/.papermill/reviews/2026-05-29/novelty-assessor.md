# Novelty Assessor Report, The Perfect Hash Filter

**Date**: 2026-05-29
**Calibration**: This paper's declared role (per the family context and `state.md`) is an EARLY-STAGE implementation/application paper: a concrete perfect-hash-filter realization of one optimal Bernoulli-set construction, with a C++ implementation and a ranked-search application. It legitimately builds on the family foundation (`bernoulli_sets`, `bernoulli-hash-function`, `bernoulli_maps`). Shared foundational notation and the Bernoulli axioms are NOT treated as novelty deficits. Novelty is assessed relative to that role.

## Summary

Assessed as an implementation paper, the contribution is real but currently mis-framed and under-differentiated. The PHF data structure itself (perfect hash to a slot plus a `b`-bit fingerprint, membership by fingerprint equality) is well-known prior art: it is the textbook "MPHF + fingerprint" approximate-membership structure that the xor-filter, fuse-filter, cuckoo-filter, and Bloomier-filter literature already covers. The paper does not currently acknowledge any of these, has no related-work section, and states its space result as flat "optimality" in a way that the modern filters beat at practical false-positive rates. The defensible novelty is narrower and should be stated as such: (1) framing the structure as a verified realization of the *positive Bernoulli set* ADT (axiom satisfaction), (2) the unification of set and map (Perfect Map Filter) and the `k`-perfect-hashing false-negative analysis under a single two-rate Bernoulli model, and (3) the fuzzy-set / rank-ordered IR application. Each of these is plausibly publishable as an implementation contribution, but only (2) and (3) are even arguably new mechanisms, and both are presently sketches.

Severity counts: Critical: 1 | Major: 2 | Minor: 2

---

## Critical

### C1. The core data structure is presented as novel but is established prior art, with no related work and no differentiation
- **Location**: Abstract (`main.tex` lines 147 to 149); Introduction (`sections/intro.tex`); the construction and FPR theorem (`sections/rd_ph_filter.tex` lines 52 to 206). There is no related-work section anywhere in `main.tex`.
- **Quoted text**: Abstract: "We derive the \gls*{gls-phf}, an immutable data structure that implements the static \emph{positive Bernoulli set} ... We demonstrate that the \gls*{gls-phf} is a \emph{succinct} data structure that asymptotically achieves the information-theoretic lower bound of `-\log_2 \varepsilon` bits per element." Intro (line 14): "we derive the \emph{Perfect Hash Filter}".
- **Problem**: "Perfect hash to a slot, store a `b`-bit fingerprint of the key, test by fingerprint equality" is the standard static-AMQ construction. It is the explicit baseline behind xor filters (Graf and Lemire, ACM JEA 2020, ~1.23x the lower bound), fuse filters (~1.075x), and is generalized by the cuckoo filter (Fan et al., CoNEXT 2014) and, for the key-value case, the Bloomier filter (Chazelle et al., SODA 2004). All of these appear in the paper's own `references.bib` (`graf2020`, `fan2014`, `bloomier`, `pagh2005`, `dietzfelbinger2008`) yet none is cited in the prose, and there is no related-work section positioning the PHF against them. A reader from the AMQ community will see the central theorem (FPR `= 2^-M`) as a re-derivation of folklore. The word "derive" throughout implies first discovery.
- **Suggestion**: (a) Add a related-work section that names xor/fuse/cuckoo/Bloomier and the Pagh-Pagh-Rao optimal replacement, and states plainly that the PHF is the MPHF-instantiation of the fingerprint-filter family. (b) Reframe the contribution from "we derive a new structure" to "we show that the MPHF+fingerprint structure is a faithful realization of the positive Bernoulli set ADT, analyze its two error rates within the Bernoulli model, and extend it to maps and fuzzy retrieval." (c) The realistic novelty is the *Bernoulli-ADT framing and the cross-structure unification*, not the structure. Say so.
- **Cross-verified**: Yes (prose lens). This is not merely a framing/writing problem that better prose would cure: the absence of related work is structural, and the "asymptotically optimal" phrasing is a substantive claim, not a stylistic one. Both the novelty and prose lenses agree the fix is real content (a related-work section plus a qualified claim), not rewording. See also literature-context section 1 and 2.

---

## Major

### M1. The optimality claim is not differentiated from structures that are strictly better at practical FPR
- **Location**: Abstract (lines 147 to 149); intro (`intro.tex` lines 16 to 21).
- **Quoted text**: Intro: "The \gls{gls-phf} achieves an expected space complexity approaching the information-theoretic lower bound of `-\log_2 \varepsilon` bits per element, compared to the Bloom filter's `-1.44 \log_2 \varepsilon` bits per element. For false positive rates `\varepsilon < 2^{-3}`, the \gls{gls-phf} is the more space-efficient structure."
- **Problem**: The comparison is only against the Bloom filter. Against the current state of the art (xor/fuse filters) the PHF is *not* more space-efficient (those sit at 1.075x to 1.23x with cheaper indexing than a full MPHF, whereas the minimal PHF pays ~2.07 extra bits/key). A "more space-efficient structure" claim benchmarked solely against a 1970 baseline overstates the contribution. The intro also contradicts the body on the crossover point (`2^-3` here vs `2^-4` in `rd_ph_filter.tex` line 531).
- **Suggestion**: Compare against xor/fuse/cuckoo, not just Bloom; restrict the "more efficient" claim to the regime where it actually holds; reconcile the crossover threshold.

### M2. Genuinely novel-to-this-paper elements (k-perfect FNR; fuzzy-IR map) are under-developed, so the real contribution is not yet substantiated
- **Location**: `sections/k_perfect_hashing.tex` (whole); `sections/pmf.tex` (whole, two TODO subsections at lines 79 to 83); `sections/apps_postings_list.tex` (rank-ordered search, lines 53 to 93).
- **Quoted text**: `pmf.tex` lines 79 to 83: "% TODO: Derive the information-theoretic lower bound on the space complexity ... % TODO: Derive the upper bound on the entropy of the PMF encoding."
- **Problem**: The strongest novelty case for an implementation paper here is the unification: one Bernoulli model spanning (i) the positive set (FNR 0), (ii) the `k`-perfect two-rate set (FPR and FNR), and (iii) the map (Perfect Map Filter) and its fuzzy-set application. But the map's space and entropy bounds are TODO stubs, the `k`-perfect section is a short derivation with an unresolved indexing issue (see logic m4), and the fuzzy-IR application is a definitional sketch with no worked numeric example and no experiment. The Bloomier filter (the closest prior art for the map) is not cited. As it stands, the parts that would carry the novelty are the least finished.
- **Suggestion**: Prioritize completing the PMF bounds and the `k`-perfect FNR analysis; cite Bloomier for the map; give the fuzzy-IR application one concrete end-to-end example with numbers. This is where the paper can earn its contribution.

---

## Minor

### m1. Contribution list is implicit; no explicit "our contributions" enumeration
- **Location**: `sections/intro.tex` (the intro lists what the paper does in narrative form, lines 30 to 50, but never enumerates claimed contributions).
- **Problem**: For an implementation paper, reviewers look for an explicit, numbered contributions paragraph that separates "we realize the Bernoulli-set ADT as a PHF," "we extend to a two-rate model via k-perfect hashing," "we generalize to maps," "we apply to fuzzy IR," "we provide a C++ implementation." Their absence makes the (narrow but real) novelty hard to locate.
- **Suggestion**: Add a numbered contributions list and tie each item to a section.

### m2. Relationship to the sibling `bernoulli-hash-function` (the "optimal construction") is unstated
- **Location**: Family context says the optimal construction lives in `bernoulli-hash-function`; this paper is "a concrete realization of one optimal Bernoulli-set construction." The manuscript never references that sibling or explains what the PHF adds beyond it.
- **Problem**: Within the family, a reader needs to know whether the PHF *is* the optimal construction, an instance of it, or a practical approximation to it. Currently unclear.
- **Suggestion**: One paragraph situating the PHF relative to `bernoulli-hash-function` and the (theoretical) "singular hash set" `shs`.

---

## Notes on legitimate, family-consistent novelty (not penalized)

- Using the `bernoulli_sets` axioms and notation, and citing `bsets`/`bmaps`, is the paper's intended role and is appropriate; it is not double-counting or a novelty gap.
- The observation that positive/negative approximate sets are semirings (not Boolean algebras) under union/intersection, and that a deterministic generator's image generates a sigma-algebra (`adt.tex` lines 51 to 91), is a thoughtful framing contribution even if it overlaps the family's composition paper; keep it but cross-reference rather than re-derive.
- The maximum-entropy-coder framing of the PHF bit string (`rd_ph_filter.tex` lines 404 to 416) is an interesting angle specific to this paper.
