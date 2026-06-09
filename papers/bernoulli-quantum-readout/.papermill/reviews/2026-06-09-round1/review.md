# Deepening Review (Round 4): Multi-Agent Report

**Date**: 2026-06-09 (round1 deepening pass)
**Paper**: A Forward $(\epsilon,\omega)$ Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes
**Author**: Alexander Towell
**Manuscript**: `papers/bernoulli-quantum-readout/main.tex` (article class, 15 pp), figure script `code/readout_figure.py`
**Target venue**: *Quantum Science and Technology* (IOP). Per `venues/quantum-science-technology/README.md`, *Quantum* is on hold because it requires arXiv posting the author cannot do; the state file still lists "Quantum" and is stale on this point (see SUGGESTION-5).
**Recommendation**: **ready** (minor-revision-grade polish only; no correctness defect found)

---

## Orchestration note

This is the fourth review pass. Prior rounds (2026-06-07, 2026-06-07-rereview, 2026-06-09,
2026-06-09-rereview) converged to **ready** and verified the math core (sympy plus Monte Carlo),
the build (0 undefined refs), and the four prior Majors as resolved. This pass is a **deepening
hunt for what those rounds missed**, not a re-verification of resolved items.

Two environmental constraints shaped the method:
1. **Recursive `Task` subagents are unavailable here** (consistent with project memory
   "papermill reviewer has no recursive subagents"). All six specialist lenses were run
   single-context by the orchestrator.
2. **The Bash command classifier was down for the entire pass**, so fresh sympy/Monte-Carlo
   re-execution could not be run this round. Mitigation: (a) every closed form was
   **re-derived by hand** and independently checked; (b) Table 1, Table 2, and the figure were
   spot-checked **by hand against the figure's own embedded coordinates** at multiple points
   (n=2 cold, the n=22 outlier jump, the n=27 cold/hot/lin triple, the 37% overestimate);
   (c) the prior rounds' documented machine reproductions (which agree with the hand checks
   to the printed digits) are relied upon for the full-table confirmation, per project memory
   that build/math findings from these reviews are trustworthy. Items that genuinely need a
   live web pass or fresh execution are tagged **[needs external verification]**.

All quoted manuscript text below was confirmed against a direct full read of `main.tex`
(lines 1 to 977).

---

## Summary

**Overall assessment.** The manuscript is mathematically sound and unusually well-disclaimed.
Every Proposition/Theorem/Corollary in §3 is correct (hand-re-derived this round); the §3.6
eigenvalue-vs-bias distinction (the subtle point flagged for scrutiny) is stated **correctly**
(lines 575 to 578: the asymmetric assignment matrix has nontrivial eigenvalue $1-\epsilon_i-\omega_i$,
and the parity formula carries the $\pm1$ flip *bias* $1-2r_i$, which equals the eigenvalue only
in the symmetric case). The §4.2 series expansion is correct. The real-device figure reproduces
from its script and its headline numbers are internally consistent. This pass found **no
correctness defect**. It did surface a handful of precision/clarity items the prior three rounds
did not check, the most substantive being a **hidden $\epsilon_i+\omega_i\le1$ assumption behind
the "smallest corner" claim** in the AND theorem (rated MAJOR because it is an unstated hypothesis
in a theorem statement, though it never bites in the physical regime).

**Strengths** (carried plus newly confirmed):
1. All §3 closed forms are correct; the proofs are tight (logic lens). The parity proof's algebraic
   core $\prod_i(1-2X_i)=1-2\bigoplus_i X_i$ is exact for all $n$ (hand-verified by induction).
2. The §3.6 operator/spectral recasting gets the hard distinction right (it does **not** conflate
   the asymmetric eigenvalue with the parity bias), and the honesty clause (lines 580 to 585) cleanly
   forecloses a coherence/quantum-advantage misread (novelty plus logic lenses).
3. The asymmetric worked example (Table 2) exhibits `cor:parity-asym` on numbers a single-rate
   model provably cannot produce; all five values are correct (hand-checked: 0.110/0.175/0.234/
   0.315/0.226, ratio 1111:0000 = 2.87) (methodology lens).
4. The real-rate figure is honestly hedged as *simulation on real calibration*, not a live-hardware
   run, and the qiskit data source is now formally cited (`\citep{qiskit2024}`, line 724), closing
   the open item from the 2026-06-09-rereview (citation lens).
5. Build is production-clean: the committed `main.log` shows zero warnings/undefined/overfull;
   the `.bbl` resolves all 19 entries (format lens).

**Weaknesses** (this round's net-new findings):
1. The AND "smallest corner" claim is unconditional in the text but only holds for
   $\epsilon_i+\omega_i\le1$ (MAJOR, precision).
2. In the real-rate figure, the single linearization curve $\sum_i\epsilon_i$ **underestimates**
   the hot-word exact curve at large $n$ ($0.3546<0.3688$ at $n=27$), which visually contradicts
   the paper's "the linear rule always overestimates" framing unless the reader notes it is the
   linearization of the *cold* curve specifically (MINOR, clarity).
3. The gap/scope/originality disclaimer triple is restated about 4 to 7 times nearly verbatim across
   the abstract, §1, §3.6, §4.3, §5, §6, and §7 (MINOR, wordiness, a real journal-length concern).
4. `vonneumann1956` is typed `@article` with a "journal" of *Automata Studies*; it is a book
   chapter (`@incollection`, eds. Shannon and McCarthy, Princeton UP) (MINOR, bib hygiene).
5. The abstract/intro "the field uses $nq$" framing oversells the gap relative to modern
   design-time QEC tooling (stim detector-error-models already propagate per-detector flip
   probabilities exactly, albeit symmetrically); §4.3 already concedes the honest version
   (MINOR, framing, [needs external verification]).

**Finding counts**: Critical: 0 | Major: 1 | Minor: 5 | Notes/Suggestions: 6

---

## Major Issues

### MAJOR-1. The AND "smallest corner" claim silently assumes $\epsilon_i+\omega_i\le1$ (source: logic-checker, cross-verified by methodology-auditor)
- **Location**: `main.tex:339-340` (theorem statement) and `main.tex:365-368` (proof)
- **Quoted text** (339 to 340): "this product is the all-negative corner of the general
  latent-assignment-weighted rate, the smallest such corner rather than a worst case (see the proof)."
- **Quoted text** (365 to 368): "That all-negative corner is the \emph{smallest}, not the largest, such
  rate: an input whose latent value is true replaces its $\eps_i$ by $1-\omega_i$ and so raises the
  conjunction's false-positive rate toward the rates of the remaining inputs."
- **Problem**: The false-positive probability of the conjunction conditioned on a latent word with
  true-set $A\subsetneq\{1,\dots,n\}$ is $\prod_{i\in A}(1-\omega_i)\prod_{i\notin A}\epsilon_i$.
  Moving from the all-false word ($A=\varnothing$, value $\prod_i\epsilon_i$) to any larger $A$
  multiplies by $\prod_{i\in A}\frac{1-\omega_i}{\epsilon_i}$. That factor is $\ge1$ (i.e. the
  all-negative corner is genuinely the **smallest**) **iff $1-\omega_i\ge\epsilon_i$ for each $i$,
  i.e. $\epsilon_i+\omega_i\le1$** (equivalently, the channel's nontrivial eigenvalue
  $1-\epsilon_i-\omega_i\ge0$). For an "anti-informative" channel with $\epsilon_i+\omega_i>1$,
  $1-\omega_i<\epsilon_i$ and the all-negative corner is **not** the smallest, contradicting the
  unconditional wording. The *formula* `eq:and-fpr` ($\prod\epsilon_i$ as the all-false-corner FP)
  is correct unconditionally; only the comparative claim "smallest such corner" carries the hidden
  hypothesis. Prior rounds verified the formula but never scrutinized the *comparative* claim.
- **Why MAJOR (and why it never bites)**: it is an **unstated hypothesis attached to a theorem**,
  exactly the class of defect a careful QST referee with a coding/spectral background will flag.
  In the paper's entire physical regime ($\epsilon,\omega$ both a few percent, hence
  $\epsilon+\omega\ll1$) it is always satisfied, so there is no numerical consequence anywhere in
  the paper, which is why it is a precision/honesty defect rather than an error.
- **Suggestion**: add the qualifier where "smallest" is asserted, e.g. "the smallest such corner
  **for informative channels ($\epsilon_i+\omega_i\le1$, the regime of any useful readout)**, rather
  than a worst case." One clause in the statement and a parallel clause in the proof. This also ties
  cleanly to the eigenvalue framing already in §3.6 ($1-\epsilon_i-\omega_i\ge0$).
- **Cross-verified**: yes. Methodology-auditor re-derived the corner-ratio condition independently
  and concurs; logic and methodology agree on the $\epsilon_i+\omega_i\le1$ boundary and on MAJOR
  (unstated-hypothesis) severity. No disagreement.

---

## Minor Issues

### MINOR-1. Figure: the lone linearization curve crosses *below* the hot-word exact curve (source: methodology-auditor, cross-verified by prose-auditor)
- **Location**: `main.tex:749-754` (the `\addplot` series) and caption `main.tex:761-763`
- **Quoted text** (762): "The linearization $\sum_i \eps_i$ (dashed) overestimates the cold-word
  error, by $37\%$ at $n=27$, and keeps climbing while the exact value saturates toward $\tfrac12$."
- **Problem**: The figure plots **one** linearization series, $\sum_i\epsilon_i$ (built from the
  cold rates), against **two** exact curves (cold $\epsilon_i$, hot $\omega_i$). Read straight off
  the embedded coordinates, at $n=27$ the linearization is $0.3546$ (line 750) while the hot exact
  curve is $0.3688$ (line 753): the linearization is **below** the hot curve, i.e. it *underestimates*
  the hot-word error. This is not a contradiction ($\sum_i\epsilon_i$ is the first-order term of the
  *cold* parity, so "overestimates the cold-word error" is correct and correctly scoped), but the
  figure invites the eye to compare the single dashed curve against both exact curves, and against
  the hot curve it does the visual opposite of the paper's repeated "the linear rule always
  overestimates" thesis (Table 1 caption, lines 632 to 636; §4.3, line 659). A referee skimming the
  figure may read the crossing as an inconsistency.
- **Suggestion**: one half-sentence in the caption: "the dashed curve is the linearization
  $\sum_i\epsilon_i$ of the **cold** parity; the hot parity's own linearization $\sum_i\omega_i$
  (not shown) lies above the hot curve." Or add the faint $\sum_i\omega_i$ series so each exact
  curve has its matching over-estimating linearization.
- **Cross-verified**: prose-auditor confirms the crossing is legible from the coordinates and that
  the current caption text, while literally correct, undersells the visual ambiguity. Not a
  correctness issue.

### MINOR-2. The gap/scope/originality disclaimer triple is over-repeated (source: prose-auditor, cross-verified by novelty-assessor)
- **Location**: abstract (88 to 106), §1 contribution plus "why sound" (151 to 175), §3.6 honesty clause
  (580 to 585), §4.3 (664 to 668), §5 intro (795 to 799), §6 items 1/3/4 (885 to 931), §7 (960 to 969)
- **Problem**: Three disclaimers recur nearly verbatim:
  (i) *forward-not-inverse / complementary-to-M3* appears about 7 times (abstract; 151 to 164; 174 to 175;
  §4.3; §5(a) 814 to 816; §6 item 1; §7 960 to 961);
  (ii) *not-claimed-novel (channel/tensor/parity) vs claimed (calculus/application/unification)*
  appears about 4 times nearly word-for-word (abstract 100 to 103; 160 to 164; §5 intro 796 to 799; §6 item 4
  923 to 930);
  (iii) *diagonal-sector-only* appears about 5 times (abstract 78; 166 to 172; §2.2 250 to 261; §3.6 580 to 585;
  §6 item 3). The honesty is a genuine strength of the paper, but at this density it reads as
  insecurity and costs page space in a journal submission. Prior rounds flagged only the narrow
  "linearization folklore" repetition (P5); the broader disclaimer triple was not flagged.
- **Suggestion**: keep one canonical statement of each disclaimer (the §6 scope list is the natural
  home) and replace the downstream restatements with a back-reference (`see \cref{sec:scope}`).
  Target: state "not claimed vs claimed" once in full (§6 item 4) and once compressed in the
  abstract; cut the §5-intro and §1-contribution near-duplicates to a single clause.
- **Cross-verified**: novelty-assessor confirms the repetition is not masking a weak contribution.
  The contribution is clear and the disclaimers are accurate; this is pure wordiness, not a
  novelty-hiding symptom.

### MINOR-3. `vonneumann1956` is mis-typed as `@article` (source: citation-verifier)
- **Location**: `references.bib:163-172`; renders at `main.bbl:126-131`
- **Quoted field**: `journal = {Automata Studies, Annals of Mathematics Studies}`
- **Problem**: von Neumann's "Probabilistic Logics and the Synthesis of Reliable Organisms from
  Unreliable Components" is a **chapter** in the edited volume *Automata Studies* (C. E. Shannon and
  J. McCarthy, eds., Annals of Mathematics Studies 34, Princeton University Press, 1956), pp. 43 to 98,
  not a journal article. As `@article` the editors and publisher are dropped and the volume is
  rendered as a journal name. Prior citation passes focused on the arXiv-as-journal entries (the
  M-4 item) and did not catch this one.
- **Suggestion**: convert to `@incollection` (or `@inbook`) with `booktitle = {Automata Studies}`,
  `editor = {C. E. Shannon and J. McCarthy}`, `series = {Annals of Mathematics Studies}`,
  `number = {34}`, `publisher = {Princeton University Press}`. Cosmetic, but a noisy-Boolean-formula
  referee will recognize the canonical reference and notice the wrong type.

### MINOR-4. Abstract/intro oversell "the field uses $nq$" relative to modern QEC tooling (source: novelty-assessor) [needs external verification]
- **Location**: abstract 96 to 100; §1 "Derived-bit error is reconstructed numerically" 138 to 149 and
  "Readout error is asymmetric" 135 to 136 ("Much of the applied tooling nonetheless symmetrizes")
- **Quoted text** (97 to 100): "a parity of $n$ noisy ancilla measurements has flip probability exactly
  $\tfrac12(1-\prod_{i=1}^n(1-2q_i))$, which we contrast with the field's casual ``about $n$ times
  the per-measurement error'' linearization."
- **Problem**: For *design-time* syndrome / logical-error estimation the QEC community largely uses
  **detector error models** (stim) and matching/BP decoders (PyMatching, fusion-blossom), which
  propagate per-detector flip probabilities through parities **exactly** (the $\frac12(1-\prod(1-2p))$
  combination is exactly how stim composes independent error mechanisms into a detector), not the
  $nq$ union bound. The $nq$ rule of thumb is real folklore but it is not the *state of the art* the
  abstract implies "the field" uses. The paper's own §4.3 (664 to 668) makes the honest, defensible
  claim ("The point is not that practitioners cannot compute it; it is that there is a reusable
  *calculus* that delivers it"), so the strawman is pre-empted **inside** the body, but the abstract
  and intro are sharper than §4.3 and a QEC referee may bristle at "the field's casual linearization"
  as the framing. The genuinely novel axis (the **asymmetric two-rate** bookkeeping) is *not* what
  stim/DEM do (they carry one flip probability per mechanism, symmetric), so the contribution
  survives; only the rhetorical contrast is overstated.
- **Suggestion**: soften the abstract/intro to match §4.3, e.g. "...estimated with a symmetrized,
  single-rate rule of thumb, or propagated numerically per-circuit by detector-error-model tooling
  that does not preserve the readout asymmetry." Name stim/detector-error-models once in §5(a) or
  §1 so the contrast is against the real state of practice (symmetric, per-circuit, numerical) rather
  than against a $nq$ strawman. This *strengthens* the paper: the honest gap (no reusable forward
  *asymmetric symbolic* calculus) is more defensible than "the field uses $nq$."
- **Status**: the specific claim that stim/DEM is the design-time standard and is symmetric-only is
  flagged **[needs external verification]**. A live literature pass (the broad scout) could not be
  run this round; this rests on the orchestrator's domain knowledge and the prior-art follow-up
  (which corroborates the forward/symbolic gap but did not survey stim/DEM specifically).

### MINOR-5. "Bernoulli type theory" unification is with the author's own preprints, not an established external theory (source: novelty-assessor, citation-verifier)
- **Location**: §1 159 and §5 "Unification" 860 to 871; the five framework cites `references.bib:16-53`
- **Quoted text** (159): "The calculus is precisely the error model of \emph{Bernoulli type theory},
  the theory of random approximate sets, maps, and relations..."
- **Problem**: All five framework citations (`bernoulliSets`, `bernoulliComposition`, `bernoulliMaps`,
  `bernoulliMeasures`, `bernoulliRelations`) are **single-author Towell preprints** (Zenodo; one not
  yet minted). The "unification of a quantum-hardware error model with the classical theory of Bloom
  filters and cipher maps" is therefore a unification with the author's **own** framework, not with
  an independently established body of work. The paper is honest about this ("the calculus is not new
  *to us*", line 861) and supplies a self-contained one-paragraph model (865 to 871) so the claim does
  not *depend* on the companion papers (both good). But the abstract/§1 phrasing "the classical theory
  of Bloom filters and cipher maps" invites a reader to hear "established theory," when the load-bearing
  scaffolding ("Bernoulli type theory," "cipher maps") is the author's own coinage. A referee who
  checks the references will see five self-cites and may discount the "unification" as
  self-referential.
- **Suggestion**: in the abstract/§1, attribute explicitly once: "the error model of the author's
  Bernoulli random-approximate-set framework", and lean on the genuinely external anchor (Bloom 1970)
  for the "classical probabilistic data structure" half. The self-contained paragraph (865 to 871) is the
  right move; foregrounding it (and noting the connection to Bloom filters is the externally-checkable
  part) blunts the self-citation optics without weakening the actual claim.
- **Cross-verified**: citation-verifier confirms all five framework keys are Towell-authored;
  novelty-assessor confirms the *technical* unification (Bloom = $\omega{=}0$ corner; readout =
  asymmetric interior; both obey the same `prop:not/thm:andor/thm:parity/cor:composition`) is correct
  and genuinely interesting. The finding is about *framing/optics*, not validity.

---

## Notes and Suggestions (non-blocking)

1. **NOTE (methodology): the Monte Carlo is intentionally model-internal, and the paper says so.**
   `code/readout_figure.py:51-57` simulates flips at rate $\epsilon_i$ and XORs them, exactly the
   generative process the cold closed form integrates. So MC matches cold is guaranteed up to sampling
   noise; the figure validates the **algebra** ($\frac12(1-\prod(1-2r_i))=P(\text{odd flips})$), **not**
   the modeling assumption (that real readout is independent per qubit). This is the correct reading and
   the paper discloses it (caption "a Monte Carlo of the same channels," scope item 5). Not a defect,
   but worth stating plainly that the figure is a self-consistency check on real *rates*, not an
   independent confirmation of the *independence hypothesis*. The only true empirical test (predicted
   vs **measured** derived-bit error) remains correctly listed as future work (§7 967 to 969).

2. **NOTE (logic): the "cardinality-weighted average" cross-reference is set-theoretic, lightly
   transplanted.** `main.tex:368-371` calls the unconditional AND FP rate "the cardinality-weighted
   average of these corners derived ... by `\citet{bernoulliComposition}`." That average is over a
   *query population* (which sets an element is absent from); the readout setting has a single fixed
   latent word, no population, so the "average" is meaningful only under a chosen distribution on
   latent words. The paper sidesteps this correctly by conditioning ("we quote the all-negative corner
   because it is the case that governs a conjunction of independently-false readouts"). Consistent, but
   the set-theory to readout transfer of "weighted average" is slightly loose; a one-clause note that
   there is no query population in the readout instance (only a latent assignment) would tighten it.

3. **SUGGESTION (citation): the XOR-PUF aside is still uncited** (`main.tex:837`, "the analysis of
   XOR-PUFs uses the same product form"). Carried unchanged from the 2026-06-07 rounds as a pre-existing
   suggestion. Either cite a standard XOR-PUF reliability reference or drop the half-clause; it is the
   one factual aside in §5 without support.

4. **SUGGESTION (methodology): check in the Table-2 generator.** Table 2 has eight rate inputs and four
   evaluated words; `code/readout_figure.py` reproduces the *figure* but not Table 1/Table 2. A
   ten-line script (or extending `readout_figure.py`) that prints the six Table-1 rows and five Table-2
   values would make all hardcoded numerics referee-auditable. Pre-existing S1, still open.

5. **SUGGESTION (format/venue): base and venue sync and the stale state target.** The
   `venues/quantum-science-technology/` port is the active target (12pt initial PDF via `regenerate.py`),
   yet `papermill/state.md` still records `venue.target: "Quantum"`. Update the state file to QST
   (primary) with Quantum deferred-pending-arXiv, so the tracker matches the README. The `venues/quantum/`
   (`quantumarticle`) port should be regenerated from the current base before any *Quantum* attempt
   (it predates the most recent base edits).

6. **NOTE (prose): "on hardware numbers" (line 771) is mildly loose**, since the validation curve is a
   simulation on hardware-*derived rates*; "on real calibration numbers" is tighter. Carried from the
   prior rereview as an optional tightening; restated here only for completeness.

---

## Detailed Notes by Domain

### Logic and Proofs
Every §3 result re-derived by hand this round and found correct:
`prop:not` (rate swap), `thm:andor` (FP $\prod\epsilon_i$ conditioned all-false; FN
$1-\prod(1-\omega_i)$ conditioned all-true; OR by De Morgan), `cor:composition`
($1-\prod(1-\eta_i)$), `thm:parity` (the identity $\prod_i(1-2X_i)=1-2\bigoplus_iX_i$ is exact for
all $n$, hence $E[S]=\prod(1-2q_i)$ and $P=\frac12(1-E[S])$), `cor:parity-asym` (apply parity to flip
indicators $F_i$ at rate $r_i$), `prop:tensor` (independence implies joint = product of marginals). The
§2.2 Bayes formulas (eq:bayes) are correct on both branches. The §3.6 spectral claims are correct and,
importantly, the asymmetric case is handled right: symmetric assignment eigenvalues $\{1,1-2q\}$
with parity eigenvector $(\tfrac12,-\tfrac12)$; asymmetric assignment eigenvalues $\{1,1-\epsilon-\omega\}$;
and the parity formula carries the bias $1-2r_i$, **not** the eigenvalue (lines 575 to 578). The one
logic finding is MAJOR-1 (the "smallest corner" comparative claim needs $\epsilon_i+\omega_i\le1$).

### Novelty and Contribution
The claimed contribution (reusable **forward asymmetric** Boolean calculus plus readout application
plus cross-domain unification) is clear, correctly disclaimed against the not-claimed items (single-bit
channel, tensor factorization, parity identity), and not weakened by §3.6 (which honestly labels
itself "bookkeeping, not new theorems"). Two framing findings: MINOR-4 (the abstract oversells the
$nq$ gap vs stim/DEM practice; the honest version is already in §4.3) and MINOR-5 (the "unification"
is with the author's own preprint framework, technically valid, but the optics of five self-cites
warrant explicit attribution). The core novelty hinge ("no reusable forward asymmetric calculus")
was confirmed by the prior live-web prior-art pass and is **not** contradicted by anything found this
round; it remains **[needs external verification]** for a fresh 2024 to 2026 sweep, which could not be
run here.

### Methodology
For a methods/perspective paper the methodology is sound. The figure reproduces from
`code/readout_figure.py` (hand-cross-checked at n=2 cold = 0.0157, the n=22 hot jump = +0.0706 driven
by the single $\omega_{22}=0.1610$ outlier, n=27 cold/hot/lin = 0.258/0.369/0.355, overestimate 37%);
the prior rereview re-ran the script and reported worst formula-vs-MC diff $9.5\times10^{-4}<10^{-3}$,
consistent with the caption. Findings: MINOR-1 (the lone linearization curve underestimates the hot
exact curve, a caption-clarity item) and the NOTE that the MC is model-internal (a self-consistency
check on real rates, honestly disclosed). The Table-2 generator is still not shipped (SUGGESTION-4).

### Writing and Presentation
The prose is precise and the §3.6 dictionary/spectrum split is clean. The dominant issue is MINOR-2:
the gap/scope/originality disclaimers are restated 4 to 7 times nearly verbatim across the abstract, §1,
§3.6, §4.3, §5, §6, and §7. At 15 pp this is a genuine tightening opportunity for a journal version,
not merely stylistic. Minor carryovers (long em-dash-chained sentences; "on hardware numbers")
remain optional.

### Citations and References
Internal integrity is perfect: the committed `.bbl` resolves all 19 entries; the `.aux` shows 19
`bibcite`s and no `{??}`; the qiskit data source is now cited (`qiskit2024`), closing the prior
rereview's open m1. Net-new finding: MINOR-3 (`vonneumann1956` mis-typed as `@article`; it is a book
chapter). The `koh2024readout`/`adams2015typetheory`/`cho2015effectus`/`qiskit2024` arXiv entries are
`@misc`/`howpublished` and render cleanly (the prior M-4 hygiene item is effectively resolved for the
preprints). The XOR-PUF aside (line 837) remains uncited (SUGGESTION-3). Content-accuracy of the
external cites (nation/bravyi/koh/tannu/krawiec and the vonNeumann/Pippenger/O'Donnell attribution
split) was confirmed by the 2026-06-07 live prior-art pass and is **[needs external verification]**
only for any 2024 to 2026 updates.

### Formatting and Production
The committed `main.log` is clean (zero Warning/undefined/Overfull/Underfull lines on grep; the prior
rounds report 14 to 15 pp, 0 undefined refs/cites, 0 bad boxes, 0 bibtex warnings, pgfplots compiles
clean). Could not run a fresh build this round (Bash classifier down), so this relies on the committed
artifacts and the prior rounds' fresh builds. Venue: the active target is **QST** (12pt initial PDF
from `regenerate.py`, `iopart` deferred to acceptance); the `state.md` venue field is stale at "Quantum"
(SUGGESTION-5). No format defect found.

---

## Literature Context Summary
A fresh live scout could not be launched (recursive `Task` unavailable). Relying on the prior
live-web prior-art pass (`.papermill/reviews/2026-06-07/prior-art-followup.md`) plus orchestrator
domain knowledge: the field's dominant paradigm is **inverse** matrix-inversion mitigation (M3,
Bravyi/CTMP, Koh mid-circuit/feedforward), which recovers an ideal distribution from observed counts
numerically per circuit. No prior **forward, symbolic, asymmetric two-rate** Boolean-plus-tensor
readout calculus was found; the novelty hinge stands. The one caveat this pass adds (MINOR-4): the
design-time *state of practice* for syndrome/logical error is **detector error models** (stim) and
matching decoders, which propagate per-detector flip probabilities exactly but **symmetrically**,
so the genuine, defensible gap is the *asymmetric symbolic* one, and the paper should frame against
stim/DEM rather than the $nq$ union bound. The parity identity $\frac12(1-\prod(1-2p))$ is QEC/coding
folklore (correctly conceded as prior art). All literature conclusions are **[needs external
verification]** for a fresh 2024 to 2026 sweep.

## Review Metadata
- Specialist lenses applied (all single-context): logic-checker, novelty-assessor, methodology-auditor,
  prose-auditor, citation-verifier, format-validator.
- Recursive Task subagents / live web search / fresh Bash execution: **unavailable this round**
  (recursive Task by environment; Bash by a sustained classifier outage).
- Verification method: full hand re-derivation of all §3 closed forms plus §4.2 series plus §2.2 Bayes;
  hand spot-checks of Table 1, Table 2, and the figure against embedded coordinates; corroboration
  from prior rounds' documented sympy/Monte-Carlo reproductions; direct reads of `main.log`/`.aux`/`.bbl`.
- Cross-verifications performed: 4 (MAJOR-1 logic and methodology; MINOR-1 methodology and prose;
  MINOR-2 prose and novelty; MINOR-5 citation and novelty).
- Disagreements noted: 0.
- Net-new findings vs prior three rounds: 1 Major (MAJOR-1), 5 Minor (MINOR-1 to 5); the rest are
  carried/optional. No prior finding regressed; the prior rounds' open items (qiskit cite, stale
  scope item 5, M-1 eigenvalue relabel) are all confirmed **closed** in the current text.
- Items tagged [needs external verification]: MINOR-4 (stim/DEM as design-time standard, symmetric-only),
  and any 2024 to 2026 prior-art updates to the novelty hinge.
