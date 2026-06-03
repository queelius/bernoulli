# Design: Convert the Bernoulli Book to a Research Monograph

**Author:** Alexander Towell
**Date:** 2026-06-02
**Status:** Design (pre-implementation of the conversion)
**Working title:** *Bernoulli Types: An Algebra of Approximate Computation*
**Supersedes:** `2026-04-29-bernoulli-textbook-design.md` for all go-forward
work. That document is the historical design of the drafted text and remains
the record of how the 18-chapter draft was built; this document governs the
conversion of that draft into a research monograph and is the new master spec.

## 1. Purpose

The book was drafted as a *pedagogical monograph* with strong textbook
affordances: graded end-of-chapter exercises, a selected-solutions appendix, a
probability refresher, a gentle intuition-first ramp, and a stated goal of
course adoption and undergraduate self-study. The decision now is to convert it
into a **research monograph**: a single-author scholarly treatise that presents
the Bernoulli framework as a unified contribution, addressed to peers who
already hold the background, denser and more authoritative, with the
pedagogical apparatus removed.

The thesis is unchanged: *approximation is a property of types, not of gadgets,
and Bernoulli types are the algebra that makes approximation composable.* What
changes is the stance toward the reader (peer, not student) and the apparatus
that stance implies.

This is the right genre for the work. The book synthesizes a nine-paper
research program into one unified algebra; that is natively monograph territory.
A textbook packages settled material for a course, whereas this draws a
nine-paper research program into a single algebra. The cost we accept: a monograph sheds some of the reach and
accessibility the textbook draft built, in exchange for depth, density, and
scholarly authority.

## 2. What carries over (do not rebuild)

The hard synthesis work is done and is kept intact:

- **The unified five-Part, eighteen-chapter arc** (atom outward: atom, sets,
  maps, optimality, boundary). This *is* the monograph's spine; a monograph is a
  unified treatment, and this structure already provides it.
- **The unified notation.** The book uses one `alex.sty`-derived notation across
  all chapters, reconciling the two notation systems the source papers use
  (unified `alex.sty` vs. modular `sty/`). This unification is a primary asset
  and is preserved.
- **Cross-references, running threads, theorem/definition/proof environments.**
  A monograph keeps and benefits from these.
- **The bookwright project infrastructure**: specs, per-chapter plans, the
  reviewer/auditor agents, the paired notebooks, the build, the hooks.
- **The paired Python notebooks**, reframed (see section 6) as reproducibility
  artifacts rather than reader labs.

## 3. What is removed or transformed

| Element | Textbook draft | Monograph |
|---|---|---|
| End-of-chapter exercises | Graded star problem sets | Removed as an apparatus; substantive content salvaged into prose (section 5) |
| Selected-solutions appendix (App. D) | Half the exercises worked | Removed |
| Probability refresher (App. A) | Full refresher | Removed, or compressed to a terse notation-and-conventions appendix; the reader is assumed to hold undergraduate probability |
| Voice | "we will learn," instructing a student | "we establish," addressing a peer; authorial, may take positions |
| Scaffolding | Learning-objective framing, heavy recap, hand-holding signposts | Scholarly signposting; state once, move on; trim repetition |
| Worked examples | Drill ("verify all four probabilities") | Illustrative ("to fix ideas, consider"); fewer, each demonstrating a result |
| Front matter | "who this is for, how to use, course adoption" | The thesis, what is new in this synthesis, relation to the source papers |
| Bibliographic notes | Light per-chapter pointers | Lean into related-work and attribution; which results are this program's and which are prior work |
| "Five Core Principles cheat sheet" (App. B) | Student cheat sheet | Either a closing synthesis section or a concise principles appendix in scholarly register |
| Library walkthrough (App. C) | Tutorial appendix | Brief reproducibility/companion note, or folded into the notebooks' reproducibility framing |

## 4. Audience and success criteria (revised)

**Audience.** Researchers and specialists: the modal reader is a researcher in
machine learning, statistics, information retrieval, theory of computation,
randomized algorithms, or cryptography who wants the authoritative,
unified treatment of the framework and its proofs. The textbook's secondary
undergraduate self-study reader and its course-adoption goal are dropped.

**Success criteria (replace the textbook's):**

1. The monograph reads as the canonical, self-contained synthesis of the
   Bernoulli framework: a researcher cites *it* (not the scattered papers) for
   the unified algebra, the Kronecker factorization theorem, the
   space-accuracy duality, and the perfect-filter-line constructions.
2. Parts IV and V present material that is genuinely new relative to the
   underlying papers (the unification, the relaxed-trapdoor framing, the
   algebraic-types treatment) at monograph density.
3. The proofs in the main text are complete and rigorous; deferrals to the
   papers are deliberate and few.
4. The notebooks reproduce every quantitative claim, and the monograph says so.

## 5. Salvage policy for exercise content

Removing the exercise apparatus is not deletion of all exercise content. Each
exercise has one of three fates:

1. **Pure drill** ("compute D(1/2 || 1/3)", "verify the row sums"): cut.
2. **Substantive result dressed as a problem**: promote to prose, as a remark, a
   worked illustration, or a short proposition with proof. Examples already
   identified: the chapter 15 point that rank collisions do not cause false
   negatives under a perfect hash; the BPHF-composed-with-BHF rate algebra; the
   adversarial rank-assignment analysis; the hybrid filter on the
   (fpr, fnr) plane. These are content, not homework, and several state results
   the body should carry directly.
3. **Open-ended or research-flavored**: fold into a "notes and open directions"
   remark at the end of the relevant chapter. Open problems suit a monograph.

When converting a chapter, read its exercises first and classify each before
deleting the block, so nothing substantive is lost.

## 6. Notebooks as reproducibility artifacts

The paired notebooks stay, reframed. In the textbook they were reader labs; in
the monograph they are reproducibility artifacts that compute and verify every
quantitative claim in the corresponding chapter. The preface (or a short
"reproducibility" note) states that each chapter's numerical claims are
reproduced in a companion notebook, and the chapter prose references the
notebook as the source of its empirical values. Self-verifying assertions in
the notebooks (as in the chapter 15 notebook) are the preferred style: a
notebook that executes to completion certifies its chapter's numbers.

## 7. Conversion methodology

**Convert in place, consulting the paper sources per chapter as the density and
rigor anchor.** For each chapter:

1. Read the chapter's section files and its exercises.
2. Read the source paper(s) that anchor the chapter (the source map, section 8).
   The papers are already in scholarly register and are tighter than the
   textbook prose; use them as the model for density and as the authority for
   proofs the textbook deferred or softened.
3. Tighten the prose toward the paper's density: cut pedagogical scaffolding,
   heavy recap, and motivational throat-clearing; keep the connective tissue
   that makes the chapter part of the unified arc (this is the monograph's
   value-add over the separate papers).
4. Convert worked examples from drill to illustration.
5. Remove the exercise block, salvaging per section 5.
6. Shift tone (peer, not student).
7. Reconcile any result the paper states more sharply (fold in the sharper
   statement or proof where it belongs in the main text).
8. Rebuild; keep cross-references and the unified notation intact.

**Methodology considered and rejected: re-derive the monograph from the papers
from scratch.** The user raised this, since the papers are tighter. Rejected
because it would discard the two assets the draft already provides and the
papers do not: the unified five-Part arc across all nine papers, and the single
reconciled notation. The papers are also uneven in maturity (the perfect-hash
filter paper is roughly 25 percent complete; the maps, relations, and
data-type papers are early). Re-deriving would re-do the synthesis and the
notation unification and risk a less coherent result. Consulting the papers as
the per-chapter anchor captures their density without discarding the synthesis.

## 8. Paper source map

Which source materials anchor each chapter (consult these during conversion).
Papers live in `papers/`; trapdoor-computing references are in the sibling
`~/github/trapdoor-computing/` repo.

| Ch | Topic | Primary source(s) |
|---|---|---|
| 1 | The Noisy Bit | `bernoulli_sets` (atom, Boolean example); `bernoulli_data_type/bernoulli_model` (order and channels) |
| 2 | Binary Channels and Model Order | `bernoulli_data_type/bernoulli_model` (order_and_channels); `bernoulli_sets` |
| 3 | Boolean Algebra Under Noise | `bernoulli_sets`; `bernoulli_composition` (gate composition) |
| 4 | Two Axioms and Kronecker Factorization | `bernoulli_sets` (axioms, Kronecker theorem, parametric parsimony) |
| 5 | Approximate Sets and Predicates | `bernoulli_sets` (ADT, FPR/FNR); Bloom filter standard refs |
| 6 | Composition of Sets | `bernoulli_composition` (union/intersection/complement/difference, monoid, relational predicates) |
| 7 | Classification Measures | `bernoulli_classification_measures` (PPV, NPV, Youden's J, delta method) |
| 8 | Information-Theoretic Bounds | `bernoulli_entropy` (joint entropy, space lower bound, Bloom efficiency) |
| 9 | Approximate Functions and n-ary Channels | `bernoulli_maps` (function spaces, map composition); `bernoulli_data_type` |
| 10 | Sketches and Estimators | `bernoulli_sets` (error-count distributions, CLT); CountMin/HyperLogLog/MinHash standard refs |
| 11 | Randomized Algorithms | `bernoulli_sets` (Miller-Rabin example); Rabin (1980), standard RP/BPP refs |
| 12 | Approximate Relations | `bernoulli_relations` (relational algebra, join/project/select) |
| 13 | The Algebra of Approximate Types | `bernoulli_data_type/algebraic_types` (sum/product/recursive, computational basis) |
| 14 | Optimal Bernoulli Sets (BHF) | `bernoulli-hash-function` (threshold predicate, space-optimal construction) |
| 15 | Perfect Hash Filters (BPHF) | `bernoulli-phf` (perfect hash filter, k-perfect hashing, ranked search) |
| 16 | Approximate but Not Bernoulli | synthesis/negative-space; correlated-error and adversarial-input literature |
| 17 | Cipher Maps and Trapdoor Computing | `~/github/trapdoor-computing/` (cipher-maps, boolean-algebra-over-trapdoor-sets) |
| 18 | Encrypted Search as Relaxed Trapdoor | `~/github/trapdoor-computing/` (maximizing-confidentiality); `papers/encrypted-search-thesis` |

Chapters 10 and 16 are the least paper-backed (they are synthesis chapters);
their conversion is prose-tightening and apparatus-removal rather than
paper-reanchoring.

## 9. Density and length

Expect the body to shrink. Removing exercises and the selected-solutions
appendix, cutting or compressing the probability-refresher appendix, and
trimming pedagogical scaffolding should reduce the draft from its current 548
pages toward roughly 400 pages. This is an outcome of tightening, not a quota:
the target is monograph density (state once, prove cleanly, do not pad), not a
page count. The textbook spec's "~28 pages per chapter" guidance is retired.

## 10. Sequencing

1. **This spec lands first** (the user's instruction). It becomes the master
   spec; `bookwright.config.yaml` is repointed to it; the textbook spec is
   marked superseded.
2. **Per-Part conversion passes**, in chapter order, Part I through Part V. Each
   chapter goes through the section 7 methodology. Convert a whole Part, build,
   run a scoped `/bookwright:review` against the monograph conventions, then
   move on. Part-by-Part keeps the unified arc coherent as the tone shifts.
3. **Resume the open correctness work in the monograph frame.** The pending ch6
   mixed-axis proposition fix (the two-sided difference correction) and the
   remaining MAJORs from the 2026-05-29 book-level review are genre-independent
   for the propositions themselves; fold them into the relevant chapter's
   conversion pass rather than treating them separately. Exercise-level review
   findings (for example the ch11 KL and BPP exercise fixes already made, and
   the ch15 exercise rewrites) are moot once exercises are removed, though their
   substantive math is salvaged per section 5.
4. **Front matter and bibliography pass**: rewrite the preface to monograph
   register; expand bibliographic notes toward scholarly attribution.
5. **Final integration and reproducibility pass**: confirm every quantitative
   claim is reproduced by a notebook; full-book `/bookwright:integrate`.

## 11. Bookwright and review implications

- `bookwright.config.yaml`: update `master_spec` to this file; record the genre
  as `monograph`.
- The `spec-auditor` and `quality-auditor` now check against monograph
  conventions: no exercise apparatus, scholarly tone, density, complete proofs.
  The reviewer prompts should be told the genre is monograph so they do not flag
  the absence of exercises or the denser tone as regressions.
- The soul-voice and macro-leak hooks are unaffected and continue to apply.

## 12. Out of scope (unchanged in spirit, sharpened)

The monograph is not, and should not become: a survey of probabilistic data
structures; a tutorial on the Python library; a course textbook; a development
of information theory, coding theory, or cryptography from scratch (it uses
results and cites them); or a replacement for the underlying papers (it
synthesizes and cites them, and is the canonical unified treatment, but the
papers remain the citable sources for specific sharpest-form results).

## 13. Open items

1. **Title.** The working title still fits a monograph. Revisit at publication.
2. **Publication target.** Academic press vs. self-published vs. free online
   plus print. A monograph leans toward an academic press or a series; does not
   affect conversion drafting.
3. **Probability-refresher appendix.** Decide during the Part I pass: cut
   entirely, or compress to a one-to-two-page notation-and-conventions
   appendix. Recommendation: compress, since a single notation reference serves
   a monograph reader well.
4. **Preface length.** A monograph preface stating the thesis, the synthesis,
   and the relation to the papers is short. Draft it in the front-matter pass,
   not now.
