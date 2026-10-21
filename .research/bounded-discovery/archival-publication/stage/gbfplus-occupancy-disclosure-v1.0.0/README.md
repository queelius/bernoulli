# Adjacent-Domain Disclosure from Public Occupancy in GBFPlus

Alexander Richard Towell, Southern Illinois University Edwardsville  
ORCID: https://orcid.org/0000-0001-6443-9897  
Archival preprint and reproducible evidence, version 1.0.0, 2026-10-20  
Exact-version DOI: https://doi.org/10.5281/zenodo.23497466

Start with `manuscript/main.pdf`. This is a narrow counterexample to a published
protocol specification, with written proofs and executable checks. It is not
a peer-reviewed or formally verified result.

## Exact contribution

Qin et al., *Privacy-Preserving On-Chain Attestation for Cross-Domain Data Flows
via GBFPlus*, Entropy 2026, 28:947, doi:10.3390/e28090947, permits publication
when a time window closes without specifying a minimum successful batch count.
Under the stated honest-history and ledger-visibility assumptions, a snapshot
with one successful insertion exposes its complete share set through occupancy.
XORing the occupied words reconstructs the stored word. Its unmasked suffix is
the adjacent-domain identifier, without a query token or candidate data identifier.

More generally, for `c` successful insertions with `kappa` distinct positions
per insertion, public occupied count `w = c*kappa` certifies disjoint supports.
The same scan returns the aggregate XOR of their identifier suffixes. It does
not generally recover the individual identifiers in a batch. If the certificate
fails, this particular scan abstains.

The increment is the protocol-specific occupancy selector and allowed release
rule. XOR sharing, joint versus marginal leakage, and disclosure without
membership acceptance are established ideas. The manuscript credits Dong,
Chen and Wen (2013), Silva and Kschischang (2011), and Hao et al. (2024).
The bounded novelty search is not an exhaustive priority determination.

## Assumptions and scope

- One authentically committed, honestly generated snapshot, starting empty;
  occupied words are never overwritten, and failed insertions do not change it.
- Occupancy distinguishes an occupied zero word from an empty cell. The count,
  share count, and relevant word/suffix widths are public and correct.
- The observer has permissioned-ledger read access. This does not assume an
  unrestricted public blockchain, regulator secrets, or an authorization token.
- The proof holds for every admissible share realization. Uniform independent
  free shares are used only for the marginal-distribution discussion. Repeated
  reads of one frozen snapshot repeat the same view; they are not new samples.
- The software models share insertion and scanning, not cryptographic position
  derivation, authentication, signatures, pairings, time-window finalization,
  or a deployed ledger. Structurally valid input is not proof of an honest history.

This is not a break of the separate data-identifier game, a general publisher
deanonymization method, full-path recovery, a measured operational exploit rate,
or a complete protocol repair. The aggregate can carry no new information when
all admissible histories already have the same XOR. Padding/masking controls
concern the stated statistic and do not establish full-protocol security.

## Reproduce from an empty directory

Extract the archive, change into its root, and run:

```sh
cd supplement
python3 -S reproduce.py
```

No installed packages, network access, or parent repository are needed at
runtime. The output is `reproduced-results.json`. Python 3.12 was used for the
release checks. `supplement/README.md` explains all fields and fixed configurations.
The deterministic results are 256 singleton choices, 1,024 disjoint-pair choices,
and 64 independently seeded stored arrays, with no recovery mismatch. These
are finite implementation checks, distinct from the written proofs. Timing is
descriptive and deliberately excluded from deterministic comparisons.

For the optional validation environment, from the packet root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r supplement/requirements-validation.txt
cd supplement
../.venv/bin/python -m coverage run --branch --source=gbfplus_probe,reproduce -m pytest -q
../.venv/bin/python -m coverage report -m
../.venv/bin/python -m ruff check .
../.venv/bin/python -m mypy --strict gbfplus_probe.py reproduce.py test_gbfplus_probe.py test_reproduction.py
cd ..
python3 -S review/independent_checks.py supplement
make -B -C manuscript
```

The last build requires `pdflatex`, BibTeX, and the ordinary LaTeX packages
listed in `manuscript/main.tex`. No publisher template is used. The independent
oracle checks every stated tiny two-attempt history plus a three-row overlap,
the saved full-word arrays, and a masking-side-information counterexample.
Its 771,787 transitions are additional finite review evidence, not an expansion
of the manuscript's experimental table or a security-probability estimate.

## Evidence, controls, and navigation

- `manuscript/`: self-contained LaTeX sources, bibliography, and readable preprint.
- `supplement/`: unchanged scientific implementation, tests, recorded arrays,
  source-premise table and provenance. The original paper is linked, not bundled.
- `review/independent_checks.py`: a separately derived whole-array oracle.
- `REVIEW.md`: review history, corrections and limits, separating AI and human review.
- `SOURCE-PINS.json`: exact source hashes and the scope of repository context.
- `verification/`: release commands, outputs, coverage and reproduction evidence.
- `MANIFEST.json`: SHA-256 and byte size for every other archived file.
- `CITATION.cff`, `CITATION.bib`, `LICENSE.md`: citation and reuse terms.

Meaningful controls cover overlap abstention, occupied zero values, preservation
of earlier row equations, atomic failure, support permutations, frozen repeated
reads, and misleading padding or masking interpretations. Subprocess tests
reject optimization that removes required assertions, including precompiled
optimized bytecode. The coverage denominator excludes the compile-time guard;
its rejection behavior is separately exercised by the tests.

## Publication and attribution

This release is a preprint and evidence packet. No journal acceptance or human
peer review is claimed. The manuscript was approved by the author on October
18; he authorized archival publication on October 20. Local research and AI
review dates on October 14-15 are not public disclosure dates. The public
archive and index record establish the release event separately.

The owning Bernoulli workspace remains private. This packet is the canonical
public source for this exact version; its hashes identify the actual evidence.
The curated public index is https://github.com/queelius/research-records .
No unrelated research, private correspondence, or account data is included.

OpenAI Codex substantially assisted research, proofs, coding, tests, writing,
AI review, and release preparation. AI assessments are not human peer review.
The historical model-version record is incomplete. The author reviewed the
scientific manuscript and authorized public release. See `REVIEW.md`.

The preprint, explanatory text and synthetic data are CC BY 4.0; software is
MIT licensed. Cite this exact version DOI for its evidence. A DOI does not
establish correctness, novelty, peer review, or legal priority.
