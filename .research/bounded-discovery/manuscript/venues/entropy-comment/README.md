# Entropy Comment: local author-review package

**Current archival edition, 2026-10-20:** the author approved the manuscript on
October 18 and authorized public archiving. The preprint and reproducible packet
are now at https://doi.org/10.5281/zenodo.23497466. See
`../../../archival-publication/README.md`. The PDF/ZIPs in this venue directory
retain their earlier author-review snapshot; draft statements below and inside
those artifacts are historical. Use the archival edition and current declaration
sheet when preparing a later journal submission. The journal submission and
fee waiver remain pending.

Revised 2026-10-15 after two rounds of independent AI-agent assessment of
readability, scientific validity, and reproducibility. No submission or external
contact has occurred. Read `main.pdf` first, then `declarations.md`.

Current submission preparation: the author authorized submission if ready, but
still needs to review the PDF and requires free publication. A methods-level
AI-use disclosure and acknowledgment clarification have been added; the main
result and code are unchanged. The earlier review records identify their exact
versions. Current conditions and checks are in
`../../../submission-preparation/`.

The five-page draft leads with the singleton disclosure, illustrates it with a
worked example, and separates the qualified aggregate extension from the central
result. Its table specifies each equality and input class. The contribution
remains a protocol-specific counterexample; the sharing algebra and standard
padding/masking are established.

The [review response ledger](../../../editorial-review/response-ledger.md)
links all initial reports, revision assessments, and dispositions. These checks
are not external peer review or evidence of journal acceptance or PhD credit.

Entropy's [author instructions](https://www.mdpi.com/journal/Entropy/instructions)
permit free-format initial submissions and code as supplementary information.
This version uses ordinary LaTeX with a Comment title, abstract, keywords,
author metadata, proofs, reproducibility section, implications, references,
and explicit draft declarations. Comment suitability remains editorial.

A subsequent [fresh adversarial review](../../../adversarial-review/assessment.md)
used three new independent agents. It prompted narrower masking language,
qualified inference limits, explicit observer access/parameters, closer prior-art
attribution, and small organizational improvements. The core propositions and
numerical results are unchanged. The new reports accompany the review bundle.

## Contents

- `main.pdf`, `main.tex`: venue draft and wrapper.
- `abstract.tex`, `body.tex`, `backmatter.tex`: shared scientific inputs, linked
  to the canonical manuscript. The source ZIP includes their actual contents.
- `references.bib`, `Makefile`: bibliography and complete build sequence.
- `cover-letter.md`, `declarations.md`: unsent drafts and unresolved author facts.
- `supplement/`: standalone code, data, tests, source premises, and provenance.
- `validation/verification.json`: current checks and exact hashes; older files
  in that directory are historical where superseded by this record.
- `packages/gbfplus-comment-source.zip`: self-contained manuscript sources.
- `packages/gbfplus-comment-supplement.zip`: independently runnable Supplement S1.
- `packages/gbfplus-comment-review.zip`: PDF, both ZIPs, review reports and
  responses, declaration drafts, and verification evidence.
- `packages/manifest.json`: final archive hashes and member lists.

In the extracted review bundle, `README.md` and `START-HERE.md` use the portable
review guide; this working-tree README is not copied there. This avoids links
that resolve only inside the parent repository.

## Rebuild and reproduce

Run `make` here, or in an empty extraction of the source ZIP. The build requires
`pdflatex`, BibTeX, and the packages declared in `main.tex`. From a separate
supplement extraction, run `python3 -S reproduce.py`. No parent repository or
third-party runtime packages are needed.

The supplement has 17 passing tests, including subprocess integration checks.
Coverage reports all 121 statements and 48 branches under normal compilation;
optimized-mode rejection is separately verified because its compile-time guard
is excluded from that coverage total. Ruff and strict mypy pass. The methods
review independently reconstructed the saved arrays and exercised 244,816 tiny
update transitions without a mismatch; those checks are review evidence, not a
new paper result.

The review found that optimized Python could remove insertions inside assertions.
The runner now rejects optimization, including precompiled optimized bytecode,
before computing or writing results. The mathematical module, original ten
tests, and two experiment functions remain unchanged. Previous normal-mode
results remain valid. Canonical and venue scientific text now share inputs.

Archives are snapshots. After future edits, regenerate them and rerun the
recorded verification before describing them as current.

## Remaining author work

Review the mathematics and source premises, finalize accurate declarations,
and decide whether to pursue the Comment route and applicable fee. The last
official fee check found a general APC of CHF 2,600; no Comment exemption was
confirmed. Paid publication is not authorized. The fee-only inquiry has a
separate status in `../../../submission-preparation/state.json`. PhD credit
is secondary under the author's stated preference.
