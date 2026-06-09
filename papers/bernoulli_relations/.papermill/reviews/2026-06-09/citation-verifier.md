# Citation Verifier Report

**Paper**: *The abstract data type of the approximate relation*
**Date**: 2026-06-09
**Scope**: Citation accuracy, missing references, bibliography integrity. No web access; external bibliographic facts tagged `[VERIFY]`.

## Bibliography integrity (mechanical checks, all run)

- **Cite/bib closure**: 11 cite keys used, 11 bib entries defined, **0 cited-but-undefined, 0 defined-but-uncited**. Clean.
  - Used: `aset, bernoulliComposition, bernoulliEntropy, bernoulliMaps, bernoulliSets, bf, codd1970, huang2009maybms, phf, suciu2011, widom2005trio`.
- **bibtex run**: exit 0, **0 warnings, 0 errors** (`main.blg`: "warning$ -- 0").
- **All 11 entries resolve** in the built bibliography (`main.bbl`).

## CV-MAJOR-1: duplicate bibliography entry (`aset` and `bernoulliSets` are the same paper)
- **Location**: references.bib:14-19 (`aset`) and references.bib:39-45 (`bernoulliSets`).
- **Finding**: Both entries have the **identical title** "Bernoulli Sets: A Model for Random Approximate Sets" by Alexander Towell. They are two bib keys for one paper. Both are cited (e.g., intro.tex:33 cites `aset`; intro.tex:81-82 cites both `aset, bernoulliSets`; the abstract and several sections cite `bernoulliSets`). This produces **two distinct entries in the reference list for the same work**, which a copy editor or referee will flag, and which fragments the citation count for the foundation paper.
- **Suggestion**: Merge to a single key (keep `bernoulliSets`, which carries the URL and the cleaner note; redirect all `\cite{aset}` to `\cite{bernoulliSets}`, or vice versa) and delete the redundant entry. Mechanical; verify the merged key is cited everywhere the old one was.

## Citation-appropriateness audit (content-level)

- `codd1970` (Codd, relational model, CACM 1970): correctly cited at intro.tex:6 and oblivious_rel_model.tex:17 for the relational model. Appropriate. `[VERIFY]` the volume/number/pages (13(6):377-387) but this is the standard reference and the .bib matches my recollection.
- `bf` (Bloom 1970, CACM 13(7):422-426): correctly cited for the approximate-membership structure with a known FPR. Appropriate; .bib has the DOI. `[VERIFY]` low-risk.
- `suciu2011`, `widom2005trio`, `huang2009maybms`: cited in the related-work paragraph (intro.tex:64-66) as the probabilistic/uncertain-DB contrast class. **Appropriate and correctly used** (the paper characterizes them as modeling uncertainty in the data, which is accurate). `[VERIFY]` the bibliographic details, but all three are well-formed and standard (Suciu et al. Morgan & Claypool 2011; Widom CIDR 2005; Huang et al. SIGMOD 2009).
- Self-cites `phf, bernoulliComposition, bernoulliMaps, bernoulliEntropy`: all `@unpublished` with real GitHub URLs, consistent with the family's preprint style (matches `bernoulli-phf/paper/references.bib`). Each is cited at an honest deferral point (composition for intersection/subset/equality rates; maps for map composition; entropy for the space bound; phf for the construction). The deferrals are accurate; I verified against the prior-review cross-checks that `bernoulliComposition`'s `cor:equality_prob` and intersection theorems are the correct targets.

## CV-MINOR-1: missing prior-art citations a DB-theory referee will expect
Per the literature-context packet, the following are **absent and should be cited and distinguished** before a database-theory submission (each `[VERIFY]` by the area chair):
- **Bloomjoin / semijoin-filtering** prior art (Mackert & Lohman; runtime-filter literature) `[VERIFY]`. This is the most important gap: the paper's join analysis competes most directly with this literature, and its absence will read as an unsearched neighborhood.
- **Sketch-based AQP / join-size estimation** (AGMS, Count-Min) `[VERIFY]`: cite and distinguish (it estimates aggregates, not membership fidelity).
- **Searchable-encryption** prior art for the application (Goh Z-IDX; Bloom-filter SSE) `[VERIFY]`: the trapdoor-database section currently cites only the author's `phf`; one external SSE anchor would situate it.
These are *missing-citation* findings, not inaccuracies in what is cited.

## Verdict
Bibliography is **mechanically clean** (full closure, 0 bibtex warnings) with **one duplicate-entry defect** (CV-MAJOR-1, `aset`=`bernoulliSets`) and a **set of missing external prior-art anchors** (CV-MINOR-1) that matter specifically for the database-theory venue. All *present* citations are appropriately used; the prob-DB and relational-model citations are correct in role. External bibliographic facts are flagged `[VERIFY]` for the area chair's web check.
