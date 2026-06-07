# Citation verifier (re-review)

Date: 2026-06-07 (re-review of revision commit 6f136b7)
Scope: verify the citation fixes from the prior-art follow-up are present and
internally consistent, and that no dangling key or broken bib entry was
introduced.

## Internal integrity (re-verified)

- Build is clean: bibtex ran with zero warnings and zero errors; the final
  pdflatex pass reports zero undefined citations and zero undefined references.
- Every cite key used in main.tex resolves to a bib entry. The 18 keys cited in
  the text:
  adams2015typetheory, bernoulliComposition, bernoulliMaps, bernoulliMeasures,
  bernoulliRelations, bernoulliSets, bloom1970, bravyi2021mitigating,
  cho2015effectus, fowler2012surface, hicks2021readout, koh2024readout,
  krawiec2021certification, nation2021m3, odonnell2014, pippenger1988,
  tannu2019mitigating, vonneumann1956. All 18 are defined in references.bib.
- No uncited entries in the bib (references.bib has exactly these 18 entries).

## Prior-art follow-up fixes: each verified present and consistent

1. Key rename pucha2021certification -> krawiec2021certification. CONFIRMED.
   - The bib entry is now @article{krawiec2021certification, ...} with lead
     author Aleksandra Krawiec, Sci. Rep. 11:21716 (2021), DOI
     10.1038/s41598-021-00444-x.
   - The single in-text use (sec:related (d)) cites krawiec2021certification.
   - Zero occurrences of "pucha" anywhere in main.tex or references.bib: no
     dangling key. CONFIRMED by grep.

2. odonnell2014 added (exact parity identity). CONFIRMED.
   - @book{odonnell2014, Ryan O'Donnell, Analysis of Boolean Functions, CUP 2014,
     DOI 10.1017/CBO9781139814782}. Cited in sec:calculus (after thm:parity) and
     in sec:related (c).

3. koh2024readout added (nearest inverse neighbor). CONFIRMED.
   - @article{koh2024readout, ... arXiv:2406.07611, 2024, DOI
     10.48550/arXiv.2406.07611}. Cited once in sec:related (a). Resolves in the
     .bbl. Author list (Jin Ming Koh, Dax Enshan Koh, Jayne Thompson) and the
     arXiv id 2406.07611 match the prior-art follow-up record.

4. Parity attribution split. CONFIRMED.
   - thm:parity discussion (line ~437): "the pm1/Fourier parity-bias identity is
     standard in the analysis of Boolean functions [odonnell2014], and it
     underlies the noisy-Boolean-formula reliability tradition of [vonneumann1956]
     and [pippenger1988]." The exact identity -> O'Donnell; the reliability
     tradition -> von Neumann / Pippenger.
   - sec:related (c) mirrors this split. This matches the prior-art-followup Q3
     recommendation exactly and resolves prior minor m3.

5. Tannu 84/62 fidelity datapoint added to rem:t1. CONFIRMED.
   - rem:t1 now reads: "tannu2019mitigating report an IBM device reading the
     all-zero state at 84% fidelity but the all-one state at only 62%, precisely
     the relaxation-driven |1> -> |0> bias." This is the verbatim datapoint the
     prior-art follow-up confirmed against the primary source (IBM-Q5, all-zero
     84%, all-one 62%). The "8-30%" figure also remains in sec:related (e),
     consistent with the abstract.

## Framework self-cite DOIs (M4 bibliographic face, prior minor m2)

- bernoulliSets, bernoulliComposition, bernoulliMaps, bernoulliMeasures now carry
  real Zenodo DOIs in both note and doi fields. RESOLVED.
- bernoulliRelations intentionally has no DOI (not yet minted). Per the re-review
  charter this is expected and correct, not a finding. The entry is otherwise
  well-formed and resolves in the build.

## New citation findings introduced by the revision

None. All five fixes are present and internally consistent; no key was orphaned;
the build's citation apparatus is intact.

## Pre-existing item carried forward (not a regression)

- sec:related (c) contains an uncited aside: "the analysis of XOR-PUFs uses the
  same product form." This was present in the original draft (verified in git:
  it predates the revision, commit bafa230) and was not flagged before. It is a
  minor, uncited factual aside, not introduced by the revision and not a
  regression. Optional fix: add a citation or drop the clause. Listed here for
  completeness only.

## Verdict

All five prior-art citation fixes are correctly applied and consistent. The four
framework DOIs are wired. No dangling pucha key. No new citation issues. Internal
integrity perfect.
