# Citation Verifier Report, bernoulli_relations

**Agent**: citation-verifier (citation accuracy, missing references, bibliography integrity)
**Date**: 2026-05-29
**Verdict**: Bibliography is absent. Every citation is unresolved. Two citations have empty keys.

## State of the bibliography

There is **no `references.bib` file** in the paper tree (confirmed: `find ... -name '*.bib'` returns nothing), yet `main.tex` declares `\bibliography{references}` with `\bibliographystyle{plainnat}` and `natbib`. Result: the bibliography is empty and every `\cite` resolves to `[?]`. This is a known, pre-existing gap also captured by the format-validator (C-F2); it is the root cause of all findings below.

## Citation inventory (every `\cite` in the manuscript)

| Key | Count | Where | Intended referent | Resolvable today? |
|---|---|---|---|---|
| `aset` | 2 | approx_rel_model.tex (2x) | The foundation paper, "Bernoulli sets" | No (no bib) |
| `bf` | 1 | approx_rel_model.tex | Bloom (1970) / Bloom filter | No |
| `phf` | 1 | approx_rel_model.tex | Perfect hash filter (author, `bernoulli-phf`) | No |
| `approxrel` | 1 | constrained_ras.tex (orphaned file) | This paper or a companion on approximate relations (self-reference) | No |
| (empty) | 2 | oblivious_rel_model.tex lines 5, 64 | Codd / relational model | No: `\cite{}` has no key at all |

### CV-1 (CRITICAL). No `references.bib`; all four named keys dangle
The keys `aset`, `bf`, `phf`, `approxrel` are used but undefined. Three of them (`aset` as the foundation, `bf`, `phf`) correspond to entries that already exist in `bernoulli_sets/references.bib` (`bf`, `phf` verbatim; the foundation paper is the referent of `aset`). The fix is mechanical: create `references.bib`, copy `bf` and `phf` from the foundation paper, add an `aset` entry pointing at "Bernoulli sets," and add `approxrel` (a self/companion reference). Until then the paper has zero working citations.

### CV-2 (MAJOR). Two empty `\cite{}` calls
`oblivious_rel_model.tex` lines 5 and 64 contain literally `\cite{}` (no key) after "first-order predicate logic." Even with a populated bibliography these emit a warning and print an empty bracket. The intended citation is almost certainly **Codd (1970)**, "A relational model of data for large shared data banks," CACM 13(6). Add a `codd1970` entry and fill both keys. (The same file also contains a bare "[4]" in prose on line 68, evidently pasted from a Wikipedia-style source with the citation marker left in as literal text; remove it.)

### CV-3 (MAJOR). Missing external references for claims that require attribution
The manuscript makes several attributable claims with no citation. A credible bibliography for this paper should add, at minimum:
- **Codd (1970)** for the relational model (currently empty `\cite{}`). Mandatory.
- **Probabilistic databases** (Suciu, Olteanu, Re, Koch, 2011). The paper's entire premise (a relation whose tuples carry membership uncertainty) sits adjacent to this field and currently cites nothing from it. Without it, the relational-algebra contribution looks unaware of its nearest neighbor. See novelty-assessor N-2 and the literature context.
- **Approximate-set substrate**: Bloom (1970) is implied by key `bf`; a modern AMQ (cuckoo/xor/ribbon filter) would substantiate the claim in approx_rel_model.tex that "it is common for implementations of approximate sets to exhibit this assumed behavior."
- **Encrypted search / oblivious databases** (Curtmola et al. 2006; Popa et al. CryptDB 2011) for the oblivious-relational application promised in the abstract.

### CV-4 (MINOR). Self-citation consistency across the family
Sibling papers are referenced informally in prose (for example properties.tex re-derives map composition that belongs to `bernoulli_maps`; predicates.tex re-derives subset/equality rates that belong to `bernoulli_composition`) but there is no citation to those companion papers. Once `references.bib` exists, add `bernoulliMaps`, `bernoulliComposition` keys (these exist in the foundation paper's bib as `@Unpublished`) and cite them at the overlapping passages. This both fixes scholarship and resolves the novelty-differentiation problem (see N-1).

## Bibliography integrity checks not yet possible
Author-year accuracy, page numbers, venue names, DOI correctness, and duplicate-key detection cannot be assessed because there are no entries to check. Re-run citation verification after `references.bib` is created.

## Summary for synthesis
- Critical: 1 (CV-1, no bibliography; shared root with format-validator C-F2)
- Major: 2 (CV-2 empty `\cite{}`; CV-3 missing external anchors including probabilistic-DB and Codd)
- Minor: 1 (CV-4 uncited sibling papers)
The headline remains: create `references.bib`. Seed it from `bernoulli_sets/references.bib` (keys `bf`, `phf`, and add `aset`, `bernoulliMaps`, `bernoulliComposition`), add `codd1970` and a probabilistic-databases entry, and fill the two empty `\cite{}` calls.
