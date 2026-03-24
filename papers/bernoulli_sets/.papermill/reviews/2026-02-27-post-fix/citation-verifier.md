# Citation Verifier Report

## Summary
The bibliography contains 25 entries. 22 are actively cited in the compiled manuscript. 3 are orphaned from the removed Boolean search section. All citations are correctly formatted and referenced. The two major attribution issues from the previous review (Carter et al. for space bound, Cover & Thomas for composition theorem) have been resolved.

## Active Citations (22)
All 22 actively cited entries are present in references.bib and correctly referenced in the text:
- bf (Bloom 1970), phf (Towell), shs (Towell), feller (1968), feller2 (1971), coverThomas (2006), hoeffding (1963), basicinterval (2001), broderMitzenmacher (2004), cuckooFilter (2014), mitzenmacherUpfal (2005), quotientFilter (2012), xorFilter (2020), ribbonFilter (2021), kirschMitzenmacher (2006), carterWegman (1979), fawcettROC (2006), mooreInterval (1966), countMinSketch (2005), powersEval (2011), boseBloom (2008), warner1965, shannonBSC (1948), carterExact (1978)

## Orphaned Entries (3)
The following entries are defined in references.bib but not cited in any compiled section:
- `songWagnerPerrig` (Song, Wagner & Perrig, 2000)
- `curtmola` (Curtmola et al., 2006)
- `cashDynamic` (Cash et al., 2013)

These were previously cited in `sections/unused/bool_search.tex`, which has been removed from main.tex.

**Fix**: Remove these 3 entries from references.bib.

## Attribution Verification
- **Space lower bound (Proposition 8.1)**: Now correctly attributed to Carter et al. (1978) with `\cite{carterExact}`. FIXED.
- **Composition theorem (Theorem 3.1)**: Now correctly attributed to Cover & Thomas (2006) with cite{coverThomas}. FIXED.

## Remaining Issues

### Minor

**m1. Orphaned bibliography entries (references.bib)**
3 entries (songWagnerPerrig, curtmola, cashDynamic) are not cited in the compiled document.

**m2. Ribbon filter citation may need updating**
The ribbonFilter entry (Dillinger & Walzer, 2021) is cited as "arXiv preprint arXiv:2103.02515". If it has since been published in a conference or journal, the citation should be updated.

**m3. Self-citations are working papers**
The phf and shs entries are cited as "Working paper. Available from the author upon request." Making these available as preprints (e.g., on arXiv) would strengthen the citations.

**m4. Delta method not cited**
The second-order Taylor expansion technique used for expected PPV (Theorem 4.5, Appendix B) is the standard delta method. No statistics reference is provided for this technique.

## Statistics
- Total bib entries: 25
- Actively cited: 22
- Orphaned: 3
- Missing citations for techniques used: 1 (delta method)
