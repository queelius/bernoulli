# Citation Verifier Report

## Overall Assessment

The bibliography is thin (11 entries) and heavily self-referential (7 of 11 are the author's own unpublished works). Only 4 external references exist. Critical prior work on space-optimal filters and information-theoretic lower bounds is missing.

## Findings

### MAJOR-1: Missing foundational citation for space lower bound
- **Location**: Section 2, Postulate 2.1 and 2.2
- **Problem**: The space lower bounds for approximate set membership are stated as "postulates" with no citation. The original result is due to Carter, Floyd, Gill, Markowsky & Wegman (1978), "Exact and Approximate Membership Testers". This is the most important missing citation in the paper.
- **Suggestion**: Add: Carter, L., Floyd, R., Gill, J., Markowsky, G., & Wegman, M. (1978). Exact and Approximate Membership Testers. STOC.

### MAJOR-2: Missing citations for space-optimal filter constructions
- **Location**: Section 9 (Discussion)
- **Problem**: The paper compares only with Bloom filters and the author's PHF, ignoring significant related work:
  - Pagh, Pagh & Rao (2005): "An Optimal Bloom Filter Replacement" -- achieved the space lower bound with polynomial construction.
  - Fan, Andersen, Kaminsky & Mitzenmacher (2014): "Cuckoo Filter" -- practical near-optimal filter.
  - Graf & Lemire (2020): "Xor Filters: Faster and Smaller Than Bloom and Cuckoo Filters" -- practical near-optimal.
  - Dillinger & Walzer (2021): "Ribbon Filter" -- practical, near-optimal, based on Gaussian elimination.
  - Dietzfelbinger & Pagh (2008): "Succinct Data Structures for Retrieval and Approximate Membership" -- theoretical near-optimal.
- **Suggestion**: Add these references and discuss the BHF's position relative to them.
- **Severity**: Major -- the paper appears unaware of significant related work.

### MAJOR-3: All companion papers lack stable identifiers
- **Location**: references.bib, entries bernoulli_sets, bernoulli_maps, bernoulli_data_type, phf, pmf, oph, es
- **Problem**: Seven of eleven bibliography entries are the author's own unpublished works with no journal, conference, arxiv ID, DOI, or URL. A reader cannot access or verify these references.
- **Suggestion**: Upload companion papers to arxiv or a preprint server and add the identifiers. At minimum, add URLs to a personal website or repository.
- **Severity**: Major -- references are unverifiable.

### MINOR-1: Missing citation for random oracle model
- **Location**: Section 2.2, Definition 2.2
- **Problem**: The random oracle model is used throughout but not cited. The standard reference is Bellare & Rogaway (1993), "Random Oracles are Practical: A Paradigm for Designing Efficient Protocols".
- **Suggestion**: Add the Bellare & Rogaway citation.

### MINOR-2: Missing citation for Beta distribution of order statistics
- **Location**: Section 3.5, Theorem 3.6 (thm:fpr_distribution)
- **Problem**: The paper cites David & Nagaraja (2003) for the continuous limit, which is correct. However, the exact discrete PMF (eq. 15) is presented without a specific citation. For discrete uniform order statistics, the standard reference would be Arnold, Balakrishnan & Nagaraja (2008).
- **Suggestion**: Consider adding Arnold et al. (2008) or a specific theorem/page reference in David & Nagaraja (2003).

### MINOR-3: Bloom filter space formula citation
- **Location**: Section 9.2, discussion.tex line 31
- **Problem**: The claim about Bloom filter space (stated incorrectly as "log2(e) / eps") should cite a specific result. The optimal Bloom filter uses k = (m/n) * ln(2) hash functions and achieves -(m/n) * ln(2) * log2(eps) bits per element. Broder & Mitzenmacher (2004) is cited but the specific formula should be attributed.
- **Suggestion**: Cite the specific result from Bloom (1970) or the survey, and correct the formula.

### MINOR-4: Manning (2008) reference seems unnecessary
- **Location**: references.bib
- **Problem**: Manning's "Introduction to Information Retrieval" is in the bibliography but I cannot find any \cite{manning} in the manuscript sections. This appears to be an unused reference.
- **Suggestion**: Either cite it somewhere relevant (e.g., in the information retrieval context of encrypted search) or remove it.

## Citation Statistics

| Category | Count | Entries |
|---|---|---|
| Author's unpublished work | 7 | bernoulli_sets, bernoulli_maps, bernoulli_data_type, phf, pmf, oph, es |
| External references | 4 | bloom1970, bf_survey, manning, order_statistics |
| Total | 11 | |
| Cited in text | 10 | (manning appears unused) |
| Missing critical citations | 2+ | Carter et al. 1978, Pagh et al. 2005 |
| Missing relevant citations | 5+ | Cuckoo filter, XOR filter, Ribbon filter, Bellare-Rogaway, Dietzfelbinger-Pagh |

## Bibliography Integrity

- All cited keys exist in references.bib: YES
- All bib entries are cited: NO (manning appears unused)
- Bibliography entries have complete metadata: NO (7 entries lack venue/pages/DOI)
- External references have complete metadata: YES (bloom1970, bf_survey, manning, order_statistics all have publisher/journal/pages)
