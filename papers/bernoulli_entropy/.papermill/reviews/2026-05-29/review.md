# Multi-Agent Review Report

**Date**: 2026-05-29
**Paper**: Entropy and space complexity of random approximate sets (Alexander Towell, SIUE; ORCID 0000-0001-6443-9897)
**Recommendation**: minor-revision

## Summary

**Overall Assessment**: This is a short (6-page), clean, honestly-scoped companion paper in the Bernoulli-sets family. It contributes one genuinely new (if elementary) result, the joint Shannon entropy of false-positive and false-negative error counts, and one carefully re-proved classical result, the Carter et al. (1978) space lower bound of -log2(epsilon) bits/element for false-negative-free approximate sets, with the Bloom filter at ln2 approx 69% efficiency. Both results are mathematically correct (independently re-derived and numerically verified). No critical issues. The defects are addressable in a focused revision: a load-bearing proof step ("Yao's minimax principle") is asserted without citation or justification; two near-certain must-cite references are missing (Yao 1977, Pagh-Pagh-Rao 2005); the objective set and its size carry inconsistent notation across sections; and the two results are never connected nor the novel one motivated.

**Strengths**:
1. Both results are correct. The joint-entropy theorem's algebra is exact and its asymptotic regime is correctly stated; the lower-bound proof's core inequality converges to the claimed bound, confirmed numerically across parameter regimes (logic-checker, methodology-auditor).
2. Intellectual honesty. The paper labels the lower bound as a restatement "for completeness," and the open-problem analysis (Remark 4.2) correctly diagnoses *why* the pigeonhole argument fails for the general false-positive-plus-false-negative case and explicitly disclaims the tempting -tau*log2(epsilon) heuristic as not a valid bound (logic-checker, novelty-assessor).
3. The build is the cleanest in the family: 6 pages, zero overfull/underfull boxes, zero undefined references, no shell-escape or external assets, fully self-contained (format-validator).
4. Bibliography is mechanically clean: all 8 cited keys defined and rendered, no orphans or dangling cites (citation-verifier).

**Weaknesses**:
1. The "Yao's minimax principle" step, which upgrades the lower bound from deterministic to randomized data structures (the generality the proposition claims), is one unsupported sentence with no citation (logic-checker MAJOR-2, citation-verifier MISSING-1).
2. Two must-cite references absent: Yao (FOCS 1977) for the minimax step, and Pagh-Pagh-Rao (SICOMP 2005) for the modern tight bound and matching construction that justify calling -log2(epsilon) "the optimum" (citation-verifier, novelty-assessor, literature context).
3. The objective set is named A, R, and S in different places, and its size is m in Section 3 but p in Section 4, with p also overloaded as the generic binomial parameter and a summation dummy (prose-auditor MAJOR-1, MAJOR-2; methodology-auditor MAJOR-1).
4. The novel result (joint entropy) is unmotivated: the paper computes it but never connects it to coding, to the space bound, or to anything downstream; the two results sit in parallel and in fact use opposite asymptotic regimes (novelty-assessor MAJOR-1, methodology-auditor MAJOR-1, prose-auditor MINOR-1).

**Finding Counts**: Critical: 0 | Major: 6 | Minor: 10 | Suggestions: 7

## Critical Issues

None. Both results are correct; the paper makes no false claim of fact.

## Major Issues

### M1. "Yao's minimax principle" is a load-bearing step asserted without citation or justification (source: logic-checker, corroborated by citation-verifier)
- **Location**: `sections/space_complexity.tex` line 25 (Prop 4.1 proof).
- **Quoted text**: "It suffices to prove the bound for deterministic encodings; the extension to randomized data structures follows from Yao's minimax principle."
- **Problem**: This single sentence is what makes the proposition apply to *randomized* data structures (i.e., justifies "expected bit length"). It cites nothing and does not set up the principle (no hard input distribution, no cost measure, no transfer argument). A referee will scrutinize exactly this step.
- **Suggestion**: Cite Yao (FOCS 1977) and add two sentences instantiating the reduction: hard distribution = uniform over size-m subsets of [n]; a randomized structure is a distribution over deterministic ones; its worst-case expected cost is at least its expected cost under the hard distribution, which is at least the deterministic bound.
- **Cross-verified**: Yes. Citation-verifier independently flagged Yao 1977 as absent from the 8-entry bib (MISSING-1). Both agree.

### M2. Missing must-cite: Yao 1977 (source: citation-verifier)
- **Location**: same sentence as M1.
- **Problem**: A named principle used in a proof with no reference. Confirmed absent.
- **Suggestion**: Add Yao, A. C.-C., "Probabilistic Computations: Toward a Unified Measure of Complexity," Proc. 18th FOCS, 1977, pp 222-227.
- **Cross-verified**: Yes (this is the citation half of M1).

### M3. Missing must-cite: Pagh, Pagh & Rao 2005 (source: citation-verifier, literature context, novelty-assessor)
- **Location**: lower-bound claim and 69%-efficiency framing (`sections/space_complexity.tex` lines 16-23, 72-78).
- **Problem**: The paper asserts -log2(epsilon) is "the optimum" and Bloom reaches only ln2 of it, but never cites the result establishing this bound is achievable to within (1+o(1)): Pagh, Pagh & Rao, "An Optimal Bloom Filter Replacement," SODA 2005 / SIAM J. Comput. This is the standard modern reference pairing a matching upper bound with the lower bound.
- **Suggestion**: Cite PPR 2005 alongside Carter et al. for the bound and when stating Bloom's efficiency. Note that near-optimal constructions exist (the family's own phf/shs are instances).
- **Cross-verified**: Yes. Literature context flags PPR as the single most important omission; novelty-assessor independently notes the differentiation gap.

### M4. Lower-bound proof states an asymptotic bound as if it were exact (source: logic-checker, cross-verified by methodology-auditor)
- **Location**: `sections/space_complexity.tex` lines 51-58, ending "giving $-\log_2 \fprate$ bits per element."
- **Quoted text**: "For fixed $\p$ as $n \to \infty$, $\binom{n}{\p} \sim n^\p / \p!$ and $\binom{\p + \fprate n}{\p} \sim (\fprate n)^\p / \p!$, so $B \geq \log_2 \frac{n^\p}{(\fprate n)^\p} = -\p \log_2 \fprate$".
- **Problem**: The honestly-derived inequality `B >= log2 C(n,p) - log2 C(p+eps(n-p),p)` converges to `-p*log2(eps)` *from below* (verified: p=3, eps=0.1 gives RHS 9.253, 9.889, 9.958, 9.965 at n=1e2..1e5, target 9.96578). So only `B >= -p*log2(eps) - o(1)` holds for finite n; the bound is asymptotic in the universe size. The *result* is correct and standard; the *phrasing* presents it as an exact per-element inequality.
- **Suggestion**: Reword to "Hence B >= -p*log2(eps) - o(1) as n -> infinity, i.e., at least -log2(epsilon) bits per element in the countably-infinite-universe limit."
- **Cross-verified**: Yes. Methodology-auditor confirmed the fixed-p / growing-universe regime is the correct model and the slack is genuinely vanishing; this is a rigor-of-statement issue, not an error of fact. Both agree the result holds.

### M5. The two results use opposite, unreconciled asymptotic regimes and inconsistent symbols for the same quantity (source: methodology-auditor, cross-verified by logic-checker and prose-auditor)
- **Location**: Thm 3.1 (`sections/entropy.tex` lines 29-30) vs. Prop 4.1 (`sections/space_complexity.tex` line 51).
- **Quoted text**: Thm 3.1: "as $u \to \infty$ with $m/u$ bounded away from $0$ and $1$". Prop 4.1: "For fixed $\p$ as $n \to \infty$".
- **Problem**: Section 3 requires constant density (m grows with u); Section 4 requires vanishing density (p fixed, n grows). The quantity is the same (number of true positives) but is written m and p. Verified that the mismatch matters: in the constant-density regime the lower-bound expression falls short of -log2(epsilon) by approx 0.93 bits (eps=0.05). A reader combining the results would silently mix incompatible limits.
- **Suggestion**: Unify the size symbol to m across both sections; add one sentence in Section 4 stating the fixed-size / growing-universe regime and that it differs from Section 3's regime.
- **Cross-verified**: Yes. Logic-checker (MINOR-1) and prose-auditor (MAJOR-2) flag the notation half independently.

### M6. The novel result (joint entropy) is unmotivated and disconnected (source: novelty-assessor, corroborated by prose-auditor)
- **Location**: `sections/entropy.tex` (whole) and intro "Contribution"/"Motivation".
- **Problem**: Result 1 is obtained by additivity-from-independence plus the textbook binomial-entropy expansion, a small and elementary delta. The paper never says what the entropy is *for*: the intro promises a coding interpretation ("any lossless representation ... requires at least this many bits") but the body never connects the entropy to a coding scheme, to the Section 4 space bound, or to the mutual information it defers to future work. The entropy and space results never interact.
- **Suggestion**: Add a paragraph linking Result 1 to a consequence: a source-coding statement for transmitting the error pattern, or the mutual information I(tilde A; A) (cheap to land here rather than defer), or a redundancy bound relative to Section 4.
- **Cross-verified**: Yes. Prose-auditor (MINOR-1) independently flags the missing narrative bridge between the two sections.

## Minor Issues

1. **Objective set named A, R, and S** across the paper (prose-auditor MAJOR-1). `A` in Axiom 1, `R` in Axiom 2, `S` in the lower-bound proof, with `A` also serving as the model's set symbol. Pick one. *(Quoted text verified: preliminaries lines 17, 23; space_complexity line 28.)*
2. **Size symbol m vs p, and p overloaded** (prose-auditor MAJOR-2): p is simultaneously the generic binomial parameter, the objective-set size, the positive-count summation dummy, and the pmf name p_POS(p|u). Standardize size to m; rename the pmf.
3. **Theorem 3.1 conditioning is implicit** (logic-checker MINOR-1, methodology-auditor MINOR-2): H(FP_m,FN_m) is conditional on m and on fixed rates eps, omega, but written as an unconditional entropy; risk of conflation with the random block rates of Axiom 2. Add "for fixed rates eps, omega; m given."
4. **Orphan "dense set" paragraph** opening Section 4 (methodology-auditor MINOR-1, prose-auditor MINOR-2): the O(u) claim is uncited, "dense" undefined, switches universe symbol to u (vs n in the proof), and is never reused. Integrate as a one-line remark or cut.
5. **"binary channels" mis-scopes Shannon** (prose-auditor MINOR-3, citation-verifier): "Shannon introduced the entropy of binary channels" narrows the 1948 general theory; the paper uses entropy of a *distribution*, not a channel. Reword.
6. **Bib key `shannonBSC` misleading** (citation-verifier): suggests "binary symmetric channel"; rename to `shannon1948`.
7. **`coverThomas` for the binomial expansion is imprecise** (citation-verifier MISSING-3, literature context): the O(1/n) expansion is folklore, not a numbered result there; add a page anchor or a precise source.
8. **No citable source for the Bloom optimum / 69% folklore** (citation-verifier MISSING-3): cite Broder-Mitzenmacher 2004 or Mitzenmacher-Upfal for m/n = -log2(eps)/ln2.
9. **cleveref `axiom` name has stray spaces** (format-validator MINOR-1, prose-auditor MINOR-4): `\crefname{axiom}{ axiom }{ axioms }` in the shared alex.sty renders irregular spacing. Fix in the style file (family-wide).
10. **Label prefix `pst:` for a Proposition** (format-validator MINOR-2): `\label{pst:approx_l_b}` on a `proposition` environment; rename to `prop:` for hygiene.

## Suggestions

1. Add a numerical sanity-check figure/table for the joint-entropy result (exact vs. asymptotic over u), giving Section 3 visual parity with Section 4 and supplying a reproducibility aid (methodology-auditor SUGGESTION-1).
2. State explicitly that all results are analytical and no experiments are required (methodology-auditor SUGGESTION-2).
3. Promote the general-case open problem (Remark 4.2) from a single remark to a fuller treatment, with a formal conjecture and the strongest available partial argument; it is the paper's freshest contribution but currently three sentences (novelty-assessor MINOR-1).
4. Add one sentence clarifying scope: the matching construction is in [bernoulli-hash-function]; this paper establishes only the bound, pre-empting the salami-slicing concern (novelty-assessor MINOR-2).
5. Name the chain-rule step in the random-POS decomposition (eq:joint_entropy_pos) rather than presenting it as a bare equation (logic-checker SUGGESTION-1).
6. Add one sentence of modern-AMQ context (cuckoo/quotient/XOR filters) for readers outside the family (citation-verifier MISSING-4).
7. Add stable references (URL/arXiv) for the four author working papers currently marked "available upon request" (citation-verifier).

## Detailed Notes by Domain

### Logic and Proofs
Both proofs were independently re-derived and numerically verified. The binomial entropy expansion, the joint-entropy algebra (the error-term combination 1/(u-m)+1/m = u/(m(u-m)) is an exact identity), the lower-bound asymptotic, and the Bloom efficiency are all correct. Two rigor issues: the Yao step is unsupported (M1), and the lower-bound conclusion is asymptotic-from-below but phrased as exact (M4). The open-problem reasoning in Remark 4.2 is a model of honest analysis. Confidence: high.

### Novelty and Contribution
Assessed relative to the declared companion role; shared foundations not counted against. Result 1 (joint entropy) is novel but elementary and, critically, unmotivated (M6). Result 2 is an acknowledged restatement of Carter et al. 1978; its Bernoulli-notation value-add is asserted, not demonstrated, and it should be positioned against the modern tight bound (PPR 2005, M3). The general-case open problem is the most original content and is underdeveloped. Standalone significance: low-to-moderate; as a family companion: appropriate.

### Methodology
Pure theory, no experiments. Every analytical claim reproduced numerically. Principal finding: Sections 3 and 4 live in opposite density regimes with the same quantity written m vs p, unreconciled (M5); verified that the mismatch is load-bearing (the bound fails in the constant-density regime). The "dense set" preamble is an orphan. A numerical sanity-check figure would strengthen the entropy result.

### Writing and Presentation
Clean, terse, professional. Two notation problems dominate: three symbols for the objective set (A/R/S) and m-vs-overloaded-p for its size. The two results lack a narrative bridge, and the Section 4 opening clashes with its own notation. All macros resolve; the issues are choices, not errors.

### Citations and References
Bibliography mechanically clean (8/8 cited, defined, rendered; no orphans/dangling). Existing external metadata accurate. Two near-certain must-cites missing: Yao 1977 (M2) and Pagh-Pagh-Rao 2005 (M3). Folklore claims (binomial expansion, Bloom 69%) want precise sources. Self/external citation ratio is high (4 of 8 are the author's); adding Yao, PPR, Broder-Mitzenmacher fixes both the gaps and the balance.

### Formatting and Production
Cleanest build in the family: 6 pages, zero bad boxes, zero undefined refs, fully self-contained, no shell-escape. All labels resolve, TOC correct, figure is inline pgfplots matching the formulas exactly. Two cosmetic naming issues (cleveref axiom spacing inherited from alex.sty; `pst:` prefix on a proposition). No venue style applied (none selected).

## Literature Context Summary
The paper combines two well-trodden areas: approximate-membership space lower bounds (Carter et al. 1978, sharpened by Pagh-Pagh-Rao 2005 to a tight (1+o(1)) bound with matching construction) and the entropy of the binomial distribution (folklore; Cover-Thomas is an acceptable anchor). The single most important missing reference is PPR 2005, which is the canonical "Bloom is not optimal; here is the tight bound and a near-optimal structure" result, exactly the gap this paper highlights. Yao 1977 is the missing citation for the minimax step. No work pre-empts Result 1 (joint FP/FN entropy appears unpublished elsewhere); Result 2 is an acknowledged restatement. Modern practical AMQ structures (cuckoo, quotient, XOR filters) go unmentioned; one sentence of acknowledgment is recommended. Full details in `literature-context.md`.

## Review Metadata
- Agents used: literature-scout-broad, literature-scout-targeted (both synthesized by the orchestrator, as the Task subagent tool was unavailable in this environment), logic-checker, novelty-assessor, methodology-auditor, prose-auditor, citation-verifier, format-validator.
- Cross-verifications performed: 4 (M1 logic<->citation; M4 logic<->methodology; M5 methodology<->logic<->prose; M3 citation<->novelty<->literature). All concurred; no disagreements.
- Disagreements noted: 0.
- Independent verification by orchestrator: clean LaTeX build reproduced (6 pp, no warnings); both proofs re-derived and numerically checked (binomial entropy expansion, joint-entropy algebra, lower-bound asymptotic and its from-below convergence, Bloom efficiency); all quoted manuscript text confirmed verbatim against the source files; bibliography integrity cross-checked against main.bbl and main.aux.
