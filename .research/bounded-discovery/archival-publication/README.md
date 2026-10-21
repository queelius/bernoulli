# GBFPlus archival publication

Published 2026-10-20 with the author's explicit authorization to carry out the
archival policy. This is a preprint and reproducible evidence packet, separate
from a journal submission or acceptance. No expenditure was made.

- Version DOI: https://doi.org/10.5281/zenodo.23497466
- Concept DOI: https://doi.org/10.5281/zenodo.23497465
- Record: https://zenodo.org/records/23497466
- Central contribution ID: `gbfplus-public-occupancy-disclosure`
- Index: https://github.com/queelius/research-records/tree/main/records/gbfplus-public-occupancy-disclosure

## Source and artifact identity

The owning Bernoulli repository remains private. The public archive is the
canonical source for this version. The research files were uncommitted; the
packet does not claim they were present in a public Git commit. Exact bytes
are pinned by its manifest and `artifact-manifest.json`.

The archival edition is under `stage/gbfplus-occupancy-disclosure-v1.0.0/` and
the four published files under `artifacts/`. The approved abstract, body,
bibliography, scientific implementation, tests and expected data are unchanged.
The wrapper, availability, review-status and licensing text were updated for
release. The original author-reviewed PDFs remain preserved as historical
drafts; their old declaration text is not current publication metadata.

Original prose and synthetic data are CC BY 4.0; original software is MIT.
The source paper and other third-party publications are linked and credited,
not redistributed. Private correspondence, raw account responses and unrelated
research are excluded. No source repository visibility was changed.

## Evidence and publication receipts

- `duplicate-search.json`: all 113 authenticated depositions paginated over
  pages of 100 and 13; no matching contribution family found.
- `stage/.../verification/`: 17 passing unit/integration tests, Ruff, strict
  mypy, coverage, standalone reproduction and independent finite oracle.
- `clean-extraction-check.json`: safe members, exact hashes, runtime replay,
  forced clean LaTeX rebuild and matching PDF text; deterministic archive rebuild.
- `draft-verified.json`: correct draft metadata and four uploaded file checksums.
- `publication.json`: successful publication, public metadata, and four
  unauthenticated file downloads with matching SHA-256 hashes.
- `index-publication.json`: public index files, catalog registration, README
  entry, and DOI resolver verification.

All five final PDF pages were visually inspected. No unresolved references,
citations, or layout warnings remain. Normal runtime coverage is 121 statements
and 48 branches; the compile-time optimizer guard is separately tested.
The independent oracle checks 771,787 finite transitions and all 64 saved arrays.
These checks are not formal verification, external human peer review or a
measurement of deployment prevalence.

The first clean-build check exposed a packaging detail: deterministic archive
timestamps make an included PDF appear current to Make. The reproduction command
now uses `make -B` to force a rebuild; the clean extracted build passed. No
mathematical, algorithmic, or data correction was needed.

## Journal continuation

MDPI's current preprint policy, checked 2026-10-20 at
https://www.mdpi.com/ethics, permits unreviewed preprints and requires disclosure
of their DOI and license at submission. It also says not to update a preprint
with revisions while the manuscript is undergoing confidential peer review.
The ordinary article-class template used here is not an MDPI submission template.

The manuscript is still unsubmitted to Entropy. The existing zero-charge
condition and unresolved actual author declarations remain. The cover-letter
draft now identifies this preprint. The earlier fee-only inquiry remains the
only message sent to the journal. No archival publication notice or other
follow-up was sent. Update `../submission-preparation/state.json` when that
process advances.

For a substantive scientific correction, use the same Zenodo concept record
and identify the corrected version. Do not silently replace this archive or
mint a new DOI family for a minor metadata/index edit.
