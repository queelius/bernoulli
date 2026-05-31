# Citation Verification Report

## Summary

Citation hygiene is clean: every `\cite` key resolves to a bibliography entry,
there are no phantom citations and no orphan keys, and the two cited external
works (Moore 1966; Hickey, Ju, Van Emden 2001; plus Cover and Thomas 2006) are
real, correctly attributed, and used appropriately. The substantive issue is
omission: the paper motivates itself with Bloom filters and approximate sets but
cites none of the standard AMQ prior art (Bloom 1970, the Broder and Mitzenmacher
survey) that the foundation paper does cite. The small bibliography (6 entries) is
appropriate for a companion paper, but the missing AMQ anchors are a fairness and
positioning gap rather than a size complaint.

[Total citations checked: 6 keys / 6 bibliography entries. Phantom citations: 0.
Orphan entries: 0. Web verification: not available this pass; external entries
checked against known publication metadata.]

## Critical Issues

None. No phantom citations, no misrepresented sources.

## Major Issues

### M1. Bloom filters and the AMQ survey are invoked rhetorically but never cited
- **Citing text**: Introduction: "Encrypted search indexes, database query planners, and distributed systems routinely compose approximate sets through union, intersection, complement, and difference." Conclusion: "A practitioner building a system on Bloom filters need not re-derive the error analysis for each new combination of filters."
- **Reference**: missing. The natural citations are Bloom (1970), "Space/Time Trade-offs in Hash Coding with Allowable Errors," and Broder and Mitzenmacher (2004), "Network Applications of Bloom Filters: A Survey." Both are present in the foundation paper's `references.bib` (keys `bf` and `broderMitzenmacher`), so the entries already exist in the family.
- **Problem**: missing attribution. The paper names Bloom filters as its motivating application and its union FPR formula `1-(1-e1)(1-e2)` is the standard independent-filter OR behavior documented in that survey. Stating these without citation leaves the union result looking like a fresh derivation of folklore and gives the reader no entry point to the literature the paper claims to serve. For a top-venue submission a reviewer will flag the absence immediately.
- **Evidence**: The foundation paper `bernoulli_sets/references.bib` cites both works; the survey explicitly discusses union and intersection of Bloom filters. (External re-verification by web search was not available this pass, but both are canonical, high-confidence references.)
- **Severity**: major
- **Confidence**: high

### M2. The intersection result's relationship to the known "AND-of-filters introduces false positives" fact is uncited, weakening the novelty contrast
- **Citing text**: Section 3 (Intersection), `thm:intersect_fprate`: "The intersection $\tilde{A}_1 \cap \tilde{A}_2$ has false positive rate [weighted formula]".
- **Reference**: missing; Broder and Mitzenmacher (2004) (or any AMQ text) for the qualitative fact that intersecting filters by AND is not exact.
- **Problem**: The paper's quantified intersection FPR is one of its genuine contributions, but without citing the known qualitative fact it generalizes, the reader cannot see the delta. A single citation establishing "it is known that filter intersection introduces false positives; we quantify the rate as a function of overlap" would both credit prior work and sharpen the novelty claim.
- **Severity**: major
- **Confidence**: medium-high

## Minor Issues

### m1. Companion-paper entries are `@Unpublished` with no locator, stable identifier, or arXiv link
- **Citing text**: e.g., Abstract: "These results build on the Bernoulli set model introduced in a companion paper~\cite{bernoulliSets}".
- **Reference**: `bernoulliSets`, `bernoulliMeasures`, `bernoulliEntropy`, all `@Unpublished{... note={Companion paper}, year={2026}}`.
- **Problem**: Three of the six references are unpublished self-citations with no way for a reader to obtain them (no URL, no arXiv id, no "available from author"). The foundation paper at least annotates its own unpublished entries with "Working paper. Available from the author upon request." For submission, the companion papers need stable identifiers (arXiv) or the venue's preferred unpublished-citation form, or the reviewer cannot check the inherited results the paper depends on (axioms, distributions, CLT).
- **Severity**: minor (becomes major at submission time if the companions remain unreachable, since the paper's correctness rests on them).
- **Confidence**: high

### m2. `coverThomas` is cited only for the Kronecker-product claim; the citation is correct but could be pinned to a section
- **Citing text**: Section 3, `rem:parametric_parsimony`: "element-wise independence forces the joint transition matrix to factor as a Kronecker product of per-set $2 \times 2$ channels~\cite{coverThomas}".
- **Reference**: Cover and Thomas (2006), *Elements of Information Theory*, 2nd ed., Wiley-Interscience. Verified correct metadata.
- **Problem**: The book is 700+ pages; citing it for "Kronecker product of channels" without a chapter or section pin is loose. The product-of-channels idea is in the channel-capacity chapters. A page or section pin would help.
- **Severity**: minor
- **Confidence**: high

### m3. Self-citation ratio is high (3 of 6) but justified by the companion structure
- **Observation**: Three of six references are the author's own companion papers. In isolation this ratio would be a flag, but here it is structurally appropriate: the paper is explicitly a companion that inherits axioms and distributions from `bernoulliSets` and defers classification measures and entropy to the siblings. No padding self-citation was found; each self-cite carries a specific inherited result. Noted for completeness, not as a defect.
- **Severity**: minor (informational).
- **Confidence**: high

## Missing References

From the literature context (and the foundation paper's own bibliography),
the following are relevant and should be considered:

1. **Bloom (1970)** , `bf` , foundational AMQ structure and the union-by-OR
   behavior; motivated by the paper's own examples. (High priority.)
2. **Broder and Mitzenmacher (2004)** , `broderMitzenmacher` , the survey that
   states union and intersection behavior of Bloom filters; the qualitative
   baseline the paper quantifies. (High priority.)
3. **A cardinality-estimation-from-filters reference** when the open problem
   (estimating `|A1 ∩ A2|`) is named , for example HyperLogLog intersection via
   inclusion-exclusion or a filter count estimator. (Medium priority; only needed
   where the open problem is discussed.)
4. **A probabilistic-database or mergeable-sketch reference** if the paper
   targets PODS or VLDB , to connect the monoidal-fold observation to
   sketch mergeability. (Medium priority; venue-dependent.)

All four exist or have close analogues in the foundation paper's bibliography,
so importing them is low-effort.

## Bibliography Issues

- **Three `@Unpublished` self-citations lack locators** (see m1). At submission,
  add arXiv ids or the venue-preferred form.
- **`basicinterval` entry**: the author field "T. Hickey and Q. Ju and M. H. Van
  Emden" uses initials only, while `mooreInterval` and `coverThomas` use full
  given names. Minor inconsistency in name formatting across entries.
- No duplicate entries. No syntax errors (BibTeX ran clean during the build).
- All entries have year, title, author. The two books have publisher; the two
  articles have journal and (for `basicinterval`) volume, number, pages. Fields
  are complete for the entry types used.

## Verified Accurate

- **`mooreInterval`** , Ramon E. Moore, *Interval Analysis*, Prentice-Hall, 1966.
  Correct; this is the founding monograph of interval arithmetic. Used correctly
  as the foundational interval-arithmetic citation.
- **`basicinterval`** , Hickey, Ju, Van Emden, "Interval Arithmetic: From
  Principles to Implementation," *Journal of the ACM* 48(5):1038-1068, 2001.
  Metadata correct (JACM vol 48, 2001). Used correctly for the modern algebraic
  treatment and the dependency-problem reference.
- **`coverThomas`** , Cover and Thomas, *Elements of Information Theory*, 2nd ed.,
  Wiley-Interscience, 2006. Correct. Used correctly for the channel-matrix
  Kronecker-product claim (pin recommended; see m2).
- **`bernoulliSets`, `bernoulliMeasures`, `bernoulliEntropy`** , author's
  companion papers. Internally consistent with the family; the inherited results
  cited (axioms, error-count distributions, CLT, confidence intervals;
  classification measures; entropy) match the stated scope of each companion per
  the collection state file. Cannot externally verify (unpublished); see m1.
