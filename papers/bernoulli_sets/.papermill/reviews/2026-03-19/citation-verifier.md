# Citation Verifier Report

**Date**: 2026-03-19
**Paper**: Bernoulli sets: a model for random approximate sets

## Summary

Citations are clean and well-aligned. All 22 bib entries are cited, all citations resolve to bib entries, and no undefined references exist. The 7 unused bib entries mentioned in the state file have already been removed. No critical or major issues.

## Citation Inventory

### Active Citations (22 cited, 22 in bib)

| Key | Used in | Context |
|-----|---------|---------|
| bf | intro, bernoulli_model | Bloom filter (foundational) |
| phf | intro, bernoulli_model | Perfect hash filter (author's companion) |
| feller | algebra_of_sets | Probability theory background |
| feller2 | distributions | CLT reference |
| coverThomas | bernoulli_model, distributions | Channel matrices, max entropy |
| hoeffding | appendix | Concentration inequality |
| broderMitzenmacher | intro | Bloom filter survey |
| cuckooFilter | intro | Cuckoo filter |
| mitzenmacherUpfal | intro | Probability and computing |
| quotientFilter | intro | Quotient filter |
| xorFilter | intro | Xor filters |
| ribbonFilter | intro | Ribbon filter |
| kirschMitzenmacher | intro | Less hashing |
| carterWegman | intro | Universal hash families |
| countMinSketch | intro | Count-min sketch |
| boseBloom | intro | Bloom filter FPR bounds |
| shannonBSC | bernoulli_model, conclusion | Binary channel |
| warner1965 | bernoulli_model, conclusion | Randomized response |
| bernoulliComposition | intro, bernoulli_model, distributions, conclusion | Companion paper |
| bernoulliMeasures | intro, conclusion | Companion paper |
| bernoulliEntropy | intro, bernoulli_model, conclusion | Companion paper |
| bernoulliMaps | bernoulli_model, conclusion | Companion paper |

### Unused Bib Entries: None

The state file mentioned 7 unused entries (basicinterval, shs, fawcettROC, mooreInterval, powersEval, carterExact, casellaBerger) as candidates for removal. These have already been removed from references.bib. Clean.

### Missing Citations: None critical

All referenced works are properly cited. No dangling \cite commands.

## Bibliography Formatting

### Issues

**m1: Unpublished companion papers lack URLs or preprint identifiers** (severity: minor)
- The four companion papers (bernoulliComposition, bernoulliMeasures, bernoulliEntropy, bernoulliMaps) are listed as @Unpublished with only "Companion paper" as the note. This is fine for a working draft but should be updated with DOIs, arXiv identifiers, or URLs before venue submission.
- **Location**: references.bib, lines 164-190

**m2: ribbonFilter cites arXiv preprint** (severity: minor)
- The Ribbon filter paper was published at VLDB 2021 but the bib entry still cites the arXiv preprint (arXiv:2103.02515). Should be updated to the published venue.
- **Location**: references.bib, lines 99-104

### Suggestions

**s1: bernoulliMaps lacks year**
- The bernoulliMaps entry has `year={2026}` which is correct for the current draft state. No action needed now.

## Cross-Reference Integrity

All \cref and \Cref references resolve correctly. No undefined labels in the build log. The cleveref package handles all cross-references consistently.
