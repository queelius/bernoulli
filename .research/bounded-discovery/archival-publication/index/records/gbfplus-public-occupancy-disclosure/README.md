# Adjacent-Domain Disclosure from Public Occupancy in GBFPlus

**Alexander Richard Towell** ([ORCID](https://orcid.org/0000-0001-6443-9897)).
Archival preprint, version 1.0.0, published October 20, 2026.

- [Exact-version DOI](https://doi.org/10.5281/zenodo.23497466)
- [Read the five-page preprint](https://zenodo.org/api/records/23497466/files/gbfplus-occupancy-disclosure-v1.0.0.pdf/content)
- [Canonical source and evidence archive](https://zenodo.org/api/records/23497466/files/gbfplus-occupancy-disclosure-v1.0.0.tar.gz/content)
- [Structured contribution record](record.json), [publication receipt](publication.json),
  [CFF citation](CITATION.cff), and [BibTeX citation](CITATION.bib)

## Contribution

An honest one-insertion GBFPlus attestation exposes its complete share set
through public occupancy. XORing the occupied payloads reconstructs the
unmasked adjacent-domain identifier suffix without a query token. The published
specification permits such a release when a time window expires. A related
occupancy equality certifies disjoint batches and reveals only their aggregate
identifier XOR.

The increment is this protocol-specific combination of an exposed selector
and an allowed release rule. XOR sharing and disclosure without membership
acceptance are established. The note credits Qin et al.'s GBFPlus specification,
Dong, Chen and Wen's earlier disclosure warning, Silva and Kschischang's linear
leakage analysis, and Hao et al.'s masking precedent. No endorsement is implied.

## Evidence and boundaries

Two written proofs establish conditional identities. Release verification
passed 17 unit/integration tests, Ruff, strict mypy, and normal coverage of
121 statements and 48 branches. The excluded optimization guard was separately
tested. A separately derived oracle checked 771,787 finite transitions and
reconstructed all 64 saved full-word arrays. Clean archive extraction reproduces
the deterministic results and rebuilds identical PDF text. All deposited files
were downloaded without authentication and matched their recorded SHA-256 hashes.

The observer needs permissioned-ledger access and the stated honest-history,
public-occupancy and release premises. The result does not generally reveal
publisher identity, complete paths, or individual identifiers in arbitrary
batches. It does not break the separate data-identifier game or prove a complete
repair. Operational prevalence is unmeasured; the literature search was bounded.

The author approved the manuscript on October 18. Substantial OpenAI Codex
assistance and internal AI reviews are disclosed in the archive. There is no
formal verification, external human peer review, or journal acceptance. The
manuscript remains unsubmitted to a journal. This DOI identifies evidence;
it is not a certification of correctness or novelty.

## Source, dates, and license

Development and detailed review remain in the private Bernoulli workspace;
its visibility was not changed. This self-contained archive is the public
canonical source. Its exact bytes are pinned by hashes because the original
research files were uncommitted. The archive includes the primary article's
DOI and audited PDF hash, source-premise table, tests, controls, expected outputs,
licenses, and verification commands.

October 20 is the first verified public release date recorded here. Earlier
local development and review dates are separate events, not backdated public
disclosures. Cite the exact version DOI above. Text and synthetic data are
CC BY 4.0; original software is MIT licensed. Third-party papers are linked and
credited, not redistributed. Future substantive changes use this version family.
