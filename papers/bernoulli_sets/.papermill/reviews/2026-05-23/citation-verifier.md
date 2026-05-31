# Citation Verifier Report

## Inventory

The `references.bib` file contains 22 entries. All 22 are cited at least once from a compiled section (intro, algebra_of_sets, bernoulli_model, distributions, conclusion, or appendix). No unused entries.

Cited keys by section:
- `intro.tex` (10 cites): bf, phf, cuckoo, quotient, xor, ribbon, broderMitzenmacher, boseBloom, kirschMitzenmacher, carterWegman, countMinSketch, mitzenmacherUpfal, bernoulliComposition, bernoulliMeasures, bernoulliEntropy
- `algebra_of_sets.tex` (1 cite): feller
- `bernoulli_model.tex` (8 cites): shannonBSC, warner1965, bernoulliComposition, bernoulliEntropy, coverThomas, bf, phf, bernoulliMaps
- `distributions.tex` (3 cites): coverThomas, feller2, bernoulliComposition
- `conclusion.tex` (6 cites): bernoulliComposition, bernoulliMeasures, bernoulliEntropy, shannonBSC, warner1965, bernoulliMaps
- `appendix.tex` (1 cite): hoeffding

## Per-Citation Verification

### Books and classical journal articles (verified accurate)
- `feller` (1968), `feller2` (1971): Volume numbers and editions correct.
- `coverThomas` (2006): Elements of Information Theory, 2nd edition, Wiley-Interscience. Correct.
- `mitzenmacherUpfal` (2005): Probability and Computing, Cambridge University Press. Correct.
- `bf` (Bloom 1970): CACM 13(7) pp. 422-426. Correct.
- `hoeffding` (1963): JASA 58(301) pp. 13-30. Correct.
- `shannonBSC` (Shannon 1948): BSTJ 27(3) pp. 379-423. Correct.
- `warner1965`: JASA 60(309) pp. 63-69. Correct.
- `carterWegman` (1979): JCSS 18(2) pp. 143-154. Correct.

### Probabilistic data structures (verified accurate)
- `broderMitzenmacher` (2004): Internet Mathematics 1(4) pp. 485-509. Correct.
- `cuckooFilter` (Fan et al. 2014): CoNEXT proceedings. Correct.
- `quotientFilter` (Bender et al. 2012): VLDB Endowment 5(11). Correct.
- `xorFilter` (Graf and Lemire 2020): JEA 25 pp. 1-16. Correct.
- `kirschMitzenmacher` (2006): ESA proceedings. Correct.
- `boseBloom` (2008): IPL 108(4) pp. 210-213. Correct.
- `countMinSketch` (Cormode and Muthukrishnan 2005): Journal of Algorithms 55(1). Correct.

### Issues

#### C1 (Minor): Ribbon filter citation is the preprint
- **Location**: `references.bib` lines 99-104.
- **Quoted text**: `journal={arXiv preprint arXiv:2103.02515}, year={2021}`
- **Problem**: The Ribbon filter paper by Dillinger and Walzer was presented at the ICDE 2022 PDS workshop and a related production-focused paper appears in the ALENEX 2023 proceedings. The arXiv preprint is technically valid but ideally citations should use the published venue when one exists.
- **Suggestion**: Update to either the ICDE 2022 workshop or the most appropriate published venue. If unsure, retain the arXiv form but add `note={Preprint}` for transparency.
- **Confidence**: High. This was noted in the 2026-03-19 review and remains unaddressed.

#### C2 (Minor): Four `@Unpublished` entries (companion papers and phf)
- **Location**: `references.bib` lines 29-33, 164-189.
- **Quoted text**: phf "Working paper. Available from the author upon request"; bernoulliComposition, bernoulliMeasures, bernoulliEntropy, bernoulliMaps "Companion paper".
- **Problem**: For final submission, these five entries depend on the companion papers being in a citable state. Submitting to a journal that expects all references to be available will require either (a) all five being uploaded to arXiv with a citable identifier, or (b) softening or removing the explicit dependencies.
- **Suggestion**: Before submission, decide a publication strategy for the companion papers. The minimum acceptable is arXiv preprints with stable identifiers. The phf citation in particular blocks easy verification of Section 3 examples and the Bloom filter / PHF comparison.

#### C3 (Suggestion): Naming consistency with downstream papers
- **Problem**: The cipher-maps paper cites this work as `@misc{bernoulli-types, title={Bernoulli Sets and Maps: A Probabilistic Framework for Approximate Data Structures}, year={2026}, note={Manuscript in preparation. See https://github.com/queelius/bernoulli_sets}}`. The title in the misc citation does not match this paper's actual title. The note URL points to the bernoulli_sets repository but suggests the citation covers the entire Bernoulli framework.
- **Suggestion**: When this paper goes to arXiv, update the cipher-maps `bernoulli-types` entry to point to the specific arXiv ID for `bernoulli_sets` (foundational paper). If the cipher-maps citation needs the full framework, it should cite multiple bernoulli papers (`bernoulli_sets`, `bernoulli_maps`, `bernoulli_data_type` as appropriate to which results it draws on). This is a coordination issue, not a fault of this paper, but worth tracking.

## Missing References Check

The introduction's related-work paragraph covers Bloom, cuckoo, quotient, xor, ribbon filters, count-min sketch, universal hashing (Carter-Wegman), and probabilistic methods generally (Mitzenmacher-Upfal). The omitted but adjacent literature:

- **Tarkoma, Rothenberg, Lagerspetz (2012)** "Theory and Practice of Bloom Filters for Distributed Systems" (IEEE Communications Surveys and Tutorials) is the most cited survey besides Broder-Mitzenmacher. Adding it would strengthen the related-work paragraph by one solid reference.
- **Pagh, Pagh, Rao (2005)** "An Optimal Bloom Filter Replacement" introduced the dictionary-style Bloom filter alternatives and is methodologically close to the kind of "implementation that satisfies the axioms" the paper discusses.
- **Goodrich and Mitzenmacher (2011)** "Invertible Bloom Lookup Tables" extends approximate set membership with deletion and listing. Mentioning IBLTs as one of the "any implementation satisfying the axioms" would broaden the ADT claim's apparent scope.

These are not blocking. The current related work is adequate.

## Bibliography Integrity

- Field formatting consistent across entries.
- No duplicate entries.
- All keys are referenced; no orphans.
- BibTeX builds without warnings.

## Recommendation

Address C1 before submission. C2 requires planning around the companion papers' publication. Other items are optional improvements.
