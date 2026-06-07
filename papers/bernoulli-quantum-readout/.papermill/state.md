---
title: "A Forward (ε, ω) Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes"
stage: review
format: latex
authors:
  - name: "Alexander Towell"
    email: "lex@metafunctor.com"
    orcid: "0000-0001-6443-9897"

thesis:
  claim: ""
  novelty: ""
  refined: null

prior_art:
  last_survey: null
  key_references: []
  gaps: ""

experiments: []

venue:
  target: null
  candidates: []

review_history:
  - date: "2026-06-07"
    type: "multi-agent-review"
    findings_major: 4
    findings_minor: 7
    recommendation: "minor-revision"
    notes: "Math core fully verified (all of sec:calculus + Table 1 reproduced by sympy/Monte Carlo); build production-clean (11pp, 0 undefined refs). 4 Majors are demonstrate/verify gaps not correctness: M1 independence failure never bounded, M2 worked example is symmetric so asymmetric machinery never shows a number, M3 no-prior-forward-calculus novelty unverified offline, M4 unification rests on 5 locator-free @unpublished self-cites (add Zenodo DOIs). Citation/novelty findings tagged [needs external verification]; reviewer ran single-context (no recursive Task / live web search)."
    report_path: ".papermill/reviews/2026-06-07/review.md"
  - date: "2026-06-07-rereview"
    type: "multi-agent-re-review"
    findings_major: 0
    findings_minor: 0
    recommendation: "ready"
    notes: "Re-review of same-day revision (commit 6f136b7). All 4 Majors RESOLVED, verified not just present: M1 independence framed as correlation-free reference + parity sign rule (sign independently verified) + CTMP cite discharged; M2 new Subsection 4.4 + Table 2 (asymmetric T1-biased syndrome, all 5 values recomputed exact: 0.110/0.175/0.234/0.315/sym 0.226, ratio 1111/0000=2.866, sym wrong on both sides); M3 koh2024readout named as nearest inverse neighbor, prior-art pass confirms no competitor; M4 four framework Zenodo DOIs wired + self-contained Bernoulli-model paragraph. Blocking minors resolved: m1 (FPR clause now conditioned), m3 (parity attribution split O'Donnell vs vonNeumann/Pippenger), m7 (0 hyperref PDF-string warnings). Build production-clean (13pp, 0 undefined refs/cites, 0 bad boxes, 0 bibtex warnings). NO regressions; 0 new findings (1 pre-existing uncited XOR-PUF aside noted, predates revision). Remaining open items all optional stylistic (m4/m5 notation bridges, m6/P5/P6, S1/S2). Recommendation: ready."
    report_path: ".papermill/reviews/2026-06-07-rereview/review.md"

related_papers:
  - path: ~/github/bernoulli/papers/bernoulli_sets
    rel: extends
    label: "Foundation: the asymmetric (ε,ω) Bernoulli channel and two-axiom error model this paper applies to quantum readout"
  - path: ~/github/bernoulli/papers/bernoulli_composition
    rel: extends
    label: "Composition theory: the forward Boolean (ε,ω) calculus specializes the set-operation error-propagation and composition theorem (eta_total = 1 - prod(1-eta_i)) to readout-derived bits"
  - path: ~/github/bernoulli/papers/bernoulli_maps
    rel: companion
    label: "Bernoulli maps ARE cipher maps; readout-derived bits are Bernoulli-map outputs, same calculus over a different domain"
  - path: ~/github/bernoulli/book
    rel: companion
    label: "Monograph (bookwright): ch9 frames the channel matrix as the classical shadow of quantum readout; ch11 covers amplitude amplification as the coherent upgrade of composition"
---

## Notes

Initialized by papermill on 2026-06-07.

- 2026-06-07 (multi-agent review): Recommendation **minor-revision** (0 Critical, 4 Major, 7 Minor, 7 Suggestions). Report at `.papermill/reviews/2026-06-07/review.md`. Math + build verified clean; the 4 Majors are contribution-demonstration/verification gaps (see review_history notes).
- 2026-06-07 (revision pass, commit 6f136b7): Addressed the majors and the prior-art pass. **M2**: added an asymmetric, inhomogeneous worked example (Table 2) exercising `cor:parity-asym`; values independently re-verified (0.110/0.175/0.234/0.315 vs a symmetrized 0.226; all-excited word misread ~2.9x the all-ground word). **M1**: framed the independent rate as the correlation-free reference and gave the parity sign rule; discharged the CTMP `% TODO` by citing `bravyi2021mitigating` (live-verified: CTMP is defined in its Sec IV). **M4**: wired the four already-minted framework concept DOIs into `references.bib` (sets 19105381, composition 19105387, maps 19105389, measures 19104549) and added a self-contained one-paragraph Bernoulli-model statement. **Prior-art pass** (live web search, `.papermill/reviews/2026-06-07/prior-art-followup.md`): novelty **stands**; renamed `pucha2021certification`->`krawiec2021certification`; added O'Donnell (exact parity identity) and `koh2024readout` (arXiv:2406.07611, nearest inverse neighbor); added Tannu's 84/62 fidelity datapoint. Build clean (13pp, 0 undefined refs, 0 hyperref PDF-string warnings, 0 bad boxes).
- 2026-06-07 (multi-agent **re-review**): Recommendation **ready** (0 Critical, 0 Major, 0 Minor, 1 optional pre-existing suggestion). Report at `.papermill/reviews/2026-06-07-rereview/review.md`. Verified each prior finding is actually resolved (not just present) and ran a fresh regression pass. All 4 Majors RESOLVED; blocking minors m1/m3/m7 RESOLVED. Table 2's five values recomputed exact; the M1 parity sign rule verified correct independently; build production-clean (13pp, 0 hyperref PDF-string warnings). No regressions, 0 new findings. The one item noted (uncited XOR-PUF aside in sec:related (c)) predates the revision (in commit bafa230) and is not a regression. Remaining open items are all optional stylistic (m4/m5 notation bridges, m6/P5/P6 sentence length and folklore repetition, S1 Table generator, S2 audience framing, S7 title).
- 2026-06-07 (Zenodo reconcile, commit fa3cc42): Discovered the framework papers were already minted; the monorepo ledger was stale. Wired real concept+version DOIs into the generator manifest. Added `docs/zenodo/audit.py` + `resolve_dois.py`. Mints go to the GitHub-login Zenodo account (owner 1003873).

**Open minting items:**
- `bernoulli_relations` (cited as `bernoulliRelations`) is the only cited framework paper still without a DOI. It is **not mint-ready**: build exits non-zero with 8 undefined cross-references (incl. a literal `\ref{?}`, and `sec:powerset`/`sec:bool_search`/`thm:subset`). Needs a cross-ref cleanup pass before minting; cited without a DOI for now.
- This paper (`bernoulli-quantum-readout`) **minted v1** on 2026-06-07 (via `docs/zenodo/mint.py`, direct Zenodo API, GitHub-login account): concept DOI **10.5281/zenodo.20584894**, version DOI **10.5281/zenodo.20584895**, record <https://zenodo.org/record/20584895>. To revise: edit, rebuild, and push a v2 under the same concept DOI.

Fresh init of a complete first draft (committed 2026-06-06, `bafa230`). The
paper is self-contained: standard `article` class, `amsmath`/`amsthm`,
`natbib` + bibtex (`plainnat`), `cleveref`. No `sections/`, `research/`,
`code/`, or `img/` subdirectories. All prose and math live in `main.tex`.

### Build

```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

- **Engine:** pdflatex
- **Bibliography:** bibtex + `plainnat` (natbib, `[numbers,square]`)
- **Notation:** inline macros in the `main.tex` preamble. `\fpr`/`\eps`=`\epsilon`
  (false-positive rate), `\fnr`=`\omega` (false-negative rate), plus `\ket`/`\bra`,
  `\tensor`, `\bxor`. This is **not** `alex.sty` and **not** the modular `sty/`
  packages the other Bernoulli papers use; the paper is deliberately standalone
  so it reads outside the framework.
- Last committed build: `main.pdf`, ~13 pp, 2026-06-07 (post-revision).

### Structure (single file, `main.tex`)

| § | Label | Content |
|---|-------|---------|
| 1 | `sec:intro` | The gap: readout error is asymmetric and derived-bit error is reconstructed numerically; contribution is a reusable forward asymmetric calculus |
| 2 | `sec:channel` | The Bernoulli readout channel (Def 2.1, asymmetric 2×2 row-stochastic Q); Bayesian recovery; diagonal-sector faithfulness; Kronecker assignment matrix |
| 3 | `sec:calculus` | The forward (ε,ω) calculus: NOT (swap), AND/OR (Thm), composition theorem (Cor), parity (Thm + asymmetric Cor), tensor factorization (Prop) |
| 4 | `sec:worked` | Worked example: reliability of a QEC syndrome bit; symmetric Table 1 (linearization overestimate) + asymmetric Subsection 4.4 / Table 2 (T1-biased latent-assignment dependence) |
| 5 | `sec:related` | Positioning against five neighbors (a through e) plus self-contained unification with classical probabilistic data structures |
| 6 | `sec:scope` | Five explicit limitations: forward-not-inverse, independence-as-reference (with parity sign rule), diagonal sector only, precise originality, no empirical validation |
| 7 | `sec:conclusion` | Synthesis plus next steps (correlated/CTMP lift, empirical calibration) |

Environments: ~2 theorems, ~3 propositions, ~2 corollaries, 1 definition, plus
remarks. Two tables (Table 1 symmetric linearization error; Table 2 asymmetric
T1-biased syndrome).

### Bibliography

`references.bib` holds **18 entries, all cited, zero placeholders**. Citation
policy stated in the file header: every entry is either a vetted work from the
concept note or a framework self-citation. No invented citations; uncertain
fields are omitted.

- **Framework self-cites (5):** `bernoulliSets`, `bernoulliComposition`,
  `bernoulliMaps`, `bernoulliMeasures` (each now with a Zenodo DOI),
  `bernoulliRelations` (no DOI yet, not mint-ready).
- **External (13):** `bloom1970`; mitigation `nation2021m3` (M3),
  `bravyi2021mitigating`, `koh2024readout`; relaxation/asymmetry
  `tannu2019mitigating`, `hicks2021readout`; effectus/type-theory
  `adams2015typetheory`, `cho2015effectus`; noisy-formula `vonneumann1956`,
  `pippenger1988`, `odonnell2014`; hypothesis testing `krawiec2021certification`;
  QEC background `fowler2012surface`.

No `% TODO` markers remain in `main.tex` (both prior TODOs discharged in the
revision: CTMP cite resolved to `bravyi2021mitigating`; the empirical-study note
is folded into sec:scope item 5 as explicit scope).

### Thesis (for context; formalize via `/papermill:thesis`)

Quantum readout error, restricted to the diagonal sector of the density matrix,
is exactly a classical asymmetric bit-flip channel with distinct false-positive
rate ε and false-negative rate ω (with ω > ε from T₁ relaxation). The paper
supplies the missing **forward, asymmetric, closed-form calculus** that
propagates the pair (ε, ω) through Boolean post-processing (NOT, AND, OR, parity)
and independent-qubit Kronecker composition, which is precisely the Bernoulli
random-approximate-set/map error model, thereby unifying a quantum-hardware
error model with the classical theory of Bloom filters and cipher maps.
Explicitly **not** claimed as novel: the single-bit asymmetric channel, the
tensor factorization, the parity identity. **Claimed:** the reusable forward
asymmetric Boolean calculus, its readout application, and the unification.

## Related Work and Software

This paper is part of the **Bernoulli type theory** program (monorepo at
`~/github/bernoulli/`). Per the Acknowledgments, the readout connection was
developed in a concept note dated 2026-06-06.

- **Extends** the core framework: the asymmetric channel and two-axiom error
  model of `bernoulli_sets`, and the composition/error-propagation theory of
  `bernoulli_composition` (the chain rule eta_total = 1 - prod(1-eta_i) is
  reused verbatim as the conjunction false-negative and disjunction
  false-positive rule).
- **Companion** to `bernoulli_maps` (Bernoulli maps = cipher maps at the
  mathematical level) and to the **monograph** in `book/`, whose recent QC
  chapters (ch9 channel matrix as the classical shadow of quantum readout; ch11
  amplitude amplification) develop the same bridge pedagogically. It also cites
  `bernoulli_classification_measures` (Bayesian PPV/NPV recovery, §2.2) and
  `bernoulli_relations` (unification paragraph, §5).
- **Reference implementation:** the framework's Python package is
  `bernoulli-py/` (PyPI `bernoulli-types`); the readout calculus corresponds to
  the `atom`/`algebra` Boolean layer (Bernoulli Boolean AND/OR/NOT/parity).

**Publication strategy** (see global memory `bernoulli-publication-strategy`):
the monograph is the primary publication; the focused Bernoulli papers are
**Zenodo preprints** (no arXiv; mint Zenodo concept + version DOIs via the
GitHub integration). This paper already carries `CITATION.cff` and `.zenodo.json`
and is provenance-ready. Note one strategy tension worth revisiting: that memory
records "QC connections live in the monograph, not the focused papers," yet this
is itself a focused QC-connection paper, a deliberate standalone bridge whose
notation is kept independent of `alex.sty` so it reads outside the framework.

A standalone GitHub remote (`queelius/bernoulli-quantum-readout`, per
`CITATION.cff`) is referenced but **not yet wired** as a monorepo subtree (no
`bernoulli-quantum-readout` remote on `origin` yet). Adding it follows the
subtree workflow in `~/github/bernoulli/CLAUDE.md` when ready to publish.
