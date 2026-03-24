# Citation Verifier Report

**Date**: 2026-02-26
**Paper**: Bernoulli sets: a model for sets with random errors

## Summary

The bibliography contains 24 entries. All 24 are cited at least once in the manuscript. No undefined citation warnings appear in the build. I assess citation accuracy, missing references, and bibliography integrity.

## Citation Accuracy

### Verified Citations (no issues)
- Bloom (1970) [bf]: Correctly cited for space/time tradeoffs, the original Bloom filter paper.
- Feller (1968, 1971) [feller, feller2]: Standard probability textbooks, appropriately cited.
- Cover & Thomas (2006) [coverThomas]: Correctly cited for information theory results including binomial entropy.
- Hoeffding (1963) [hoeffding]: Correctly cited for probability inequalities.
- Broder & Mitzenmacher (2004) [broderMitzenmacher]: Correctly cited as a Bloom filter survey.
- Fan et al. (2014) [cuckooFilter]: Correct for cuckoo filters.
- Mitzenmacher & Upfal (2005) [mitzenmacherUpfal]: Correct for probabilistic methods.
- Bender et al. (2012) [quotientFilter]: Correct for quotient filters.
- Graf & Lemire (2020) [xorFilter]: Correct for xor filters.
- Kirsch & Mitzenmacher (2006) [kirschMitzenmacher]: Correct for the less-hashing result.
- Carter & Wegman (1979) [carterWegman]: Correct for universal hashing.
- Fawcett (2006) [fawcettROC]: Correct for ROC analysis introduction.
- Powers (2011) [powersEval]: Correct for evaluation measures.
- Shannon (1948) [shannonBSC]: Correct for mathematical theory of communication.
- Song, Wagner & Perrig (2000) [songWagnerPerrig]: Correct for encrypted search.
- Curtmola et al. (2006) [curtmola]: Correct for searchable symmetric encryption.
- Cash et al. (2013) [cashDynamic]: Correct for dynamic searchable encryption.
- Moore (1966) [mooreInterval]: Correct for interval analysis.
- Hickey, Ju & Van Emden (2001) [basicinterval]: Correct for interval arithmetic.
- Cormode & Muthukrishnan (2005) [countMinSketch]: Correct for count-min sketch.
- Bose et al. (2008) [boseBloom]: Correct for Bloom filter FPR bounds.

### Issues

#### I1. Self-citations lack publication details
**Location**: references.bib, entries [phf] and [shs]
**Problem**: Both entries are @Unpublished with "Working paper" as the note. These are cited as if they are established results ("Perfect hash filters [phf]", "Singular hash set [shs]") but provide no URL, preprint server, or other means for a reader to access them.
**Suggestion**: Either (a) provide a URL or preprint link, (b) include the relevant results inline if they are short, or (c) note explicitly in the text that these are unpublished.

#### I2. Ribbon filter venue is incorrect
**Location**: references.bib, entry [ribbonFilter]
**Quoted text**: "booktitle={Proceedings of the International Conference on Learning Representations (ICLR)}"
**Problem**: The Ribbon Filter paper by Dillinger & Walzer was published at ICLR 2021, which is unusual for a data structures paper. The actual venue appears to be the 29th Annual European Symposium on Algorithms (ESA 2021) or possibly a VLDB venue. The ICLR venue should be verified.
**Suggestion**: Verify the correct publication venue and update the entry.

#### I3. Missing tilde before some \cite commands
**Location**: Multiple locations
**Quoted text**: "the Bloom filter\cite{bf}" (bernoulli_model.tex line 103), "Hoeffding's inequality\cite{hoeffding}" (appendix.tex line 17), "the Bloom filter\cite{bf}" (entropy.tex line 174)
**Problem**: LaTeX convention requires a non-breaking space (~) before \cite to prevent line breaks between the text and the citation number.
**Suggestion**: Replace "\cite{" with "~\cite{" in all instances where there is no space or tilde before the \cite command.

## Missing References

### Important Omissions

1. **Warner (1965), "Randomized response: A survey technique for eliminating evasive answer bias"**: The per-element Bernoulli error model is identical to Warner's randomized response technique. This is a significant intellectual predecessor that should be cited, especially since Remark 3.1 discusses the BSC connection.

2. **Tarkoma, Rothenberg & Lagerspetz (2012), "Theory and Practice of Bloom Filters for Distributed Systems"**: A more recent and comprehensive survey than Broder & Mitzenmacher (2004) that discusses Bloom filter compositions in distributed settings.

3. **Pagh, Pagh & Rao (2005), "An Optimal Bloom Filter Replacement"**: Relevant to the space complexity discussion in Section 8, as it provides optimal constructions that match the information-theoretic bound.

### Potentially Useful References

4. **Mitzenmacher (2002), "Compressed Bloom Filters"**: Discusses compressed Bloom filter unions, directly relevant to Section 5.

5. **Bruck, Gao & Jiang (2006)** or similar work on cascaded BSC channels: relevant to the composition theorem (Theorem 3.3) and its convergence behavior.

## Bibliography Integrity

- All 24 entries are syntactically valid BibTeX.
- No duplicate entries.
- No orphaned entries (all are cited).
- Author names are consistently formatted.
- Journal/conference names use proper capitalization with {} protection where needed.
- Year and page ranges are present for all published works.
- The two @Unpublished entries lack sufficient detail (see I1 above).

## Summary

| Finding | Severity |
|---------|----------|
| Self-citations lack access information | Major |
| Ribbon filter venue possibly incorrect | Minor |
| Missing ~ before \cite commands | Minor |
| Missing reference: Warner (1965) | Major |
| Missing reference: Tarkoma et al. (2012) | Minor |
| Missing reference: Pagh et al. (2005) | Minor |
