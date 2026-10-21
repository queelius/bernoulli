# Paper fleet freeze (October 2026)

Date: 2026-10-21. Author: Alexander Towell.

The ten Bernoulli preprints (eleven manuscripts; `bernoulli_data_type` has two)
are frozen in favor of the monograph *Bernoulli Types: Two-Sided Error in
Approximate Membership, Retrieval, and Computation*
(<https://metafunctor.com/latex/bernoulli-monograph/book.html>; hub
<https://metafunctor.com/research/bernoulli/>). Each manuscript now carries a
"Status and errata (October 2026)" box directly after its abstract, the
minimal corrections and prior-art citations from the October 2026 audit, and an
`ERRATA.md` with the dated list of changes. License unchanged: CC BY 4.0.

Nothing here has been committed, pushed, subtree-pushed, or deposited. The
machine-readable companion is [`freeze-manifest.json`](freeze-manifest.json).

## Manuscripts

"Clean" means the documented build finished with 0 LaTeX errors, 0 undefined
references, 0 undefined citations, and 0 BibTeX warnings, measured from the
final `main.log` and `main.blg`, and that `pdftotext` finds the status box on
page 1 or 2. Chapters are the monograph chapters named in the box.

| Paper | Title | Corrections | Build | Pages | Monograph ch. | Concept DOI | Latest version DOI (to supersede) |
|---|---|---|---|---|---|---|---|
| `bernoulli_sets` | Bernoulli sets: a model for random approximate sets | 6 | clean | 20 | 2, 4, 5, 7 | 10.5281/zenodo.19105381 | 10.5281/zenodo.19105382 |
| `bernoulli_composition` | Composition of Bernoulli sets | 7 | clean | 16 | 6 | 10.5281/zenodo.19105387 | 10.5281/zenodo.19105388 |
| `bernoulli_classification_measures` | Binary classification measures for random approximate sets | 5 | clean | 15 | 7 | 10.5281/zenodo.19104549 | 10.5281/zenodo.19104550 |
| `bernoulli_entropy` | Entropy and space complexity of random approximate sets | 8 | clean | 8 | 8 | 10.5281/zenodo.20602259 | 10.5281/zenodo.20602260 |
| `bernoulli-hash-function` | The Bernoulli Hash Function: Optimal Bernoulli Sets and Bernoulli Maps | 13 | clean | 30 | 14 | 10.5281/zenodo.20602261 | 10.5281/zenodo.20602262 |
| `bernoulli-phf` | The Perfect Hash Filter: An efficient implementation of the positive Bernoulli set and Bernoulli map abstract data types (deposited as: ...Positive Bernoulli Set and Bernoulli Map) | 8 | clean | 37 | 15 | 10.5281/zenodo.20602263 | 10.5281/zenodo.20602264 |
| `bernoulli_maps` | The algebra of the random approximate map model | 8 | clean | 26 | 9 | 10.5281/zenodo.19105389 | 10.5281/zenodo.19105390 |
| `bernoulli_relations` | Error contracts for approximate relations (deposited as: The Abstract Data Type of the Approximate Relation) | 8 | clean | 28 | 12 | 10.5281/zenodo.20602265 | 10.5281/zenodo.20618109 |
| `bernoulli_data_type/bernoulli_model` | The Bernoulli Model: A Probabilistic Framework for Data Structures and Types | 7 | clean | 24 | 1, 2, 3, 4, 13 | 10.5281/zenodo.19105398 | 10.5281/zenodo.19105399 |
| `bernoulli_data_type/algebraic_types` | Random approximate values over algebraic types | 8 | clean | 20 | 13 | 10.5281/zenodo.19105395 | 10.5281/zenodo.19105396 |
| `bernoulli-quantum-readout` | A Forward (epsilon, omega) Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes | 8 | clean | 20 | 19 | 10.5281/zenodo.20584894 | 10.5281/zenodo.20618108 |

Total: 86 corrections across 11 manuscripts. No title was edited during the
freeze. The relations title changed in the October revision (commit 30aa1e2),
and the PHF manuscript title already differed from its deposit before the
freeze. Latest version DOIs were confirmed against the public Zenodo API on
2026-10-21; they match `docs/PROVENANCE.md`.

## What the freeze fixed, by paper

The full lists, with locations and evidence, are in each `ERRATA.md`.

- **Quantum readout.** Withdrew the claim that the (epsilon, omega) pair
  propagates through an entire Boolean tree; propagation is now per latent
  assignment, with the counterexample (b0 AND b1) OR b2 at 010 (0.03764 exact
  versus 0.020392 from pair reuse). The classical assignment model is scoped to
  diagonal detector POVMs (any state), not diagonal density matrices. Credits
  Gallager 1962, Matsui, Parker and McCluskey, PTMs, Smith et al. 2021, and
  Hamilton et al. 2020 (whose cumulant reconstruction beats the paper's
  crosstalk truncation). The box records the QST rejection and retirement.
- **Entropy.** The two-sided space bound is no longer called open: it is
  credited to Pagh and Rodler 2001 (Prop. 1). The lower-bound proof is stated
  asymptotically, and its randomized step is credited to Yao 1977.
- **BHF.** Replaced the wrong discrete order-statistic law with the binomial
  tail; withdrew the "price of FPR certainty" saving, which changed recall
  (at equal recall and FPR cap it is binomial-tail fixed-threshold search); fixed
  the E[log2 Q] and salt-entropy errors; credited RecSplit, ShockHash, ESA 2025,
  and Dietzfelbinger and Pagh 2008.
- **PHF.** Credited the construction to Dietzfelbinger and Pagh 2008 Sec. 1,
  k-perfect hashing to Belazzougui et al. 2009, and the false-negative bound to
  Pagh and Rodler; corrected the k-perfect false-negative analysis (seed
  rejection, fingerprint rescue, dependence), each checked by exact enumeration.
- **Maps.** Replaced the success-probability formula that contradicted Section 7
  and restated the space theorem; scoped composition closure to marginal rates
  (shared intermediate values break element-wise independence); credited
  Bloomier filters, Rely, and channel cascades (Silverman 1955).
- **Sets, composition, classification.** Credited Warner 1965, Bross 1954,
  Hirota 1981, retouched and generalized Bloom filters, Broder and
  Mitzenmacher, Parker and McCluskey, PTMs, Dalvi and Suciu, and Goutte and
  Gaussier; removed every claim that a single (FPR, FNR) pair carries through
  arbitrary set or Boolean expressions; removed novelty claims; fixed several
  smaller errors (a swapped union rate in sets, E[beta] in classification, a
  reversed "positive" label in composition).
- **Relations.** Status box summarizing the October revision relative to v5;
  added Fuhr and Rolleke 1997, Dalvi and Suciu 2007, Benjelloun et al. 2008,
  and Mullin 1990.
- **Data type (both).** Credited Decaf, Rely, `Uncertain<T>`, EnerJ, Chisel,
  the Giry monad, Ramsey and Pfeffer, and signal-probability analysis; removed
  novelty claims; fixed the set-indicator symbol clash and the two-level
  hashing space claim (bernoulli_model) and the bind/closure and C++ rate-field
  errors (algebraic_types).

## Verification performed

- Every build was re-measured from its final log after the edits, independent
  of the per-paper reports (`grep` in this shell is a ugrep wrapper that skips
  gitignored files such as `main.log`, so the check parses logs in Python).
- All 80 new or changed bibliography entries that carry a DOI were checked
  against Crossref (or DataCite for Zenodo, LIPIcs, and arXiv DOIs): title and
  first author match. The single flag is intentional: the quantum paper cites
  the relations preprint under its new title, which Zenodo will show only
  after the relations re-deposit.
- Entries without a Crossref DOI are cited by author-hosted URL and marked in
  the bib files: the Bloomier filter (SODA 2004) and Pagh, Pagh, and Rao
  (SODA 2005).
- Each box was rendered to an image and inspected.
- Added prose contains no em dashes and no "oblivious" outside the retained
  filename `oblivious_rel_model.tex`.

## Re-deposit checklist (not done)

1. Apply the manifest changes below to `docs/zenodo/generate_metadata.py`,
   then run it so each `.zenodo.json` carries the final metadata.
   `mint.py newversion` reads title and description from `.zenodo.json`.
2. For each paper, create a new-version draft under its concept DOI from the
   latest version record id (in `freeze-manifest.json`), for example
   `python3 docs/zenodo/mint.py newversion 20618108 papers/bernoulli-quantum-readout/main.pdf papers/bernoulli-quantum-readout final-2026-10`.
   Check the draft, then publish.
3. Paste the new version DOIs into the manifest, regenerate, and commit.
4. Archive the standalone GitHub repos read-only with a README pointing to the
   monograph, as planned in `.research/program-strategy/README.md`.

## Manifest changes needed (`docs/zenodo/generate_metadata.py`)

Not applied here. Version label: `mint.py newversion` takes it as an argument
(default `v2`); a uniform `final-2026-10` across the fleet is suggested
(current labels: 1.0.0 for sets, composition, classification, maps and both
data_type papers; none for entropy, BHF, PHF; v5 for relations and quantum).

- **All papers:** prefix each description with "Final version (October 2026),
  with errata; superseded by the monograph Bernoulli Types, Chapter N." and
  drop any wording that the errata withdraw.
- **bernoulli_relations:** title "Error contracts for approximate relations".
  Description: separates exact relation truth, construction randomness and
  shared source identity; scoped operator and invariant-preservation formulas,
  one-sided query error contracts, a stored-filter calibration study; credits
  probabilistic relational algebra and probabilistic databases. Drop the
  keyword "trapdoor database".
- **bernoulli-quantum-readout:** the description repeats the withdrawn claim
  ("propagates a false-positive/false-negative rate pair through Boolean
  combinations"). Replace with: applies known forward error-propagation tools
  (signal probability, PTMs, Gallager's parity lemma) to Boolean
  post-processing of asymmetric readout error, computed per latent assignment;
  worked ibm_hanoi syndrome-bit numbers. Title kept. The manifest comment
  saying the quantum paper is "intentionally absent" is stale.
- **bernoulli-hash-function:** replace "optimally implement ... at the
  information-theoretic space bound" with: seed-search constructions whose
  expected salt length matches the known -log2(epsilon)+mu scale in
  exponential expected time; corrected order-statistic law; adaptive-threshold
  saving withdrawn. Title kept ("Optimal" holds only to leading order; an
  optional retitle is "The Bernoulli Hash Function: Seed-Search Bernoulli Sets
  and Maps").
- **bernoulli-phf:** description: restates the minimal perfect hash plus
  fingerprint filter (Dietzfelbinger and Pagh 2008, Sec. 1) as a positive
  Bernoulli set and map, about log2(e) bits per element above the bound, with a
  corrected k-perfect false-negative analysis. Decide which title to deposit:
  the manifest omits the manuscript's "abstract data types" suffix.
- **bernoulli_maps:** drop "the composition theorem" and "space-optimal";
  say closed-form marginal rates under composition (element-wise independence
  only without shared intermediate values) and a seed-search construction
  approaching -log2(epsilon)+mu bits per element.
- **bernoulli_composition:** replace "showing the model is closed under
  set-theoretic composition" with per-region rates; marginal rate pairs do not
  compose through nested expressions.
- **bernoulli_entropy:** credit Carter et al. for the one-sided bound and
  Pagh and Rodler (2001) for the two-sided bound.
- **bernoulli_sets, bernoulli_classification_measures:** add the final-version
  prefix; classification may add "standard delta method; no novelty claimed".
- **bernoulli_data_type:** split into two entries. Keep `papers/bernoulli_data_type`
  (concept 10.5281/zenodo.19105398) for bernoulli_model, drop "Count-Min sketch"
  from its keywords and the "introduces" framing from its description, and add
  an entry for `papers/bernoulli_data_type/algebraic_types` (title "Random
  approximate values over algebraic types", concept 10.5281/zenodo.19105395,
  version 10.5281/zenodo.19105396), so that `mint.py` has a `.zenodo.json` for
  it. Note that `mint.py` names the uploaded file after the paper directory.
- **Book entry:** title "Bernoulli Types: Two-Sided Error in Approximate
  Membership, Retrieval, and Computation" (the manifest still has "An Algebra
  of Approximate Computation").

## Follow-ups outside `papers/` found during the freeze

- Monograph Chapter 8 (`book/chapters/ch08/entropy-floor.tex`,
  `bibliographic-notes.tex`) still calls the two-sided space bound open.
- Monograph Chapters 16 and 19 describe the classical readout sector as the
  diagonal of the density operator; the POVM scope fix applied to the quantum
  preprint likely applies there too.
- `bernoulli-quantum-readout/venues/` still contains the withdrawn claims. It
  was left untouched by instruction; do not publish it as is.
- Build artifacts (`main.aux`, `main.bbl`, `main.blg`, `main.toc`, `main.pdf`)
  are tracked in git for `bernoulli_composition` and `bernoulli_entropy`, so
  they show as modified. New `_minted-main/*.pygtex` caches in
  `bernoulli-phf/paper` and `bernoulli_data_type/algebraic_types` are build
  artifacts and should not be added.
