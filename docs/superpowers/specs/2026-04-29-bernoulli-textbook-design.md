# Design: A Bernoulli Framework Textbook

**Author:** Alexander Towell
**Date:** 2026-04-29
**Status:** SUPERSEDED (2026-06-02) by `2026-06-02-bernoulli-monograph-conversion.md`. This document is the historical design of the drafted text (a pedagogical monograph with textbook affordances) and the record of how the 18-chapter draft was built. The book is being converted to a research monograph; the conversion spec is the current master. Read this for the original structure, threads, and rationale; read the conversion spec for go-forward conventions.
**Working title:** *Bernoulli Types: An Algebra of Approximate Computation*

## 1. Purpose and Thesis

A pedagogical monograph that unifies probabilistic data structures, randomized
algorithms, noisy channels, and approximate functions under a single algebraic
framework: the Bernoulli model of random approximate types. The book makes the
case that Bloom filters, Miller-Rabin primality testing, the binary symmetric
channel, HyperLogLog, and approximate dictionaries are not a parade of clever
tricks but instances of one model with one algebra.

**Single-sentence thesis:** *Approximation is a property of types, not of
gadgets, and Bernoulli types are the algebra that makes approximation
composable.*

The book is not a survey of approximate data structures. It is a theory book
with worked examples, in the tradition of MacKay's *Information Theory,
Inference, and Learning Algorithms*: single voice, opinionated, accessible,
proof-bearing where it counts, with a unifying spine that makes the framework
feel discovered rather than asserted.

## 2. Audience

**Primary (modal reader):** adjacent-field grad students and early-career
researchers in machine learning, statistics, information retrieval, theory of
computation, and cryptography. They want to learn the framework cleanly and
use it to do new work.

**Secondary:** the smart-undergrad-upward self-study reader with undergraduate
probability and willingness to work through proofs.

**Out of scope:**
- Practitioners who want recipes only (they should read the relevant `papers/`
  or third-party Bloom-filter packages)
- Specialists who want full novelty positioning and tightest possible monograph
  density (they should read the underlying papers)

## 3. Format and Tone

**Format:** pedagogical monograph. Single-author voice; opinionated; covers
the framework with intuition first, then statement, then proof. Worked examples
throughout. End-of-chapter exercises (numbered, optional). Selected solutions
in an appendix. Chapter-end Bibliographic Notes pointing to the underlying
papers.

**Tone reference:** MacKay (2003). Less dense than Cover & Thomas; more
mathematical than Mitzenmacher & Upfal; more pedagogical than Pearl's
*Causality* but with the same single-voice authority.

**Density target:** roughly 28 pages per chapter, 18 chapters, total ~500 pp.

## 4. Through-Line: Atom Outward

The book builds the framework from a single noisy bit and unfolds outward.
Each layer adds one new type construction and one new family of concrete
examples:

| Layer | Type | Examples introduced |
|---|---|---|
| Atom | `Bernoulli[bool]` | BSC, biased coin, single Miller-Rabin witness, single classifier verdict |
| Predicates / sets | f: X → `Bernoulli[bool]`, `Bernoulli[Set[X]]` | Bloom filter, full Miller-Rabin protocol |
| General maps | f: X → `Bernoulli[Y]`, any Y | n-ary channels, approximate counter, dictionary, HyperLogLog, MinHash, Reed-Solomon decoder |
| Relations | multi-attribute approximate maps | Approximate joins, projection, selection |
| Algebraic types | sum, product, recursive | Type-theoretic generalization; parametric parsimony shines |

The discipline this imposes: the book never lingers in Set-land long enough
for readers to think Bernoulli is a Bloom-filter framework. Sets are the
*bridge* from atom to general maps, not the destination.

## 5. Structure: 5 Parts, 18 Chapters

| Part | Ch | Topic | Notebook? |
|---|---|---|---|
| **I. The Atom** | 1 | The Noisy Bit | yes (BSC simulation, bit channel demos) |
| | 2 | Binary Channels and Model Order | yes (asymmetric channel, model-order ladder) |
| | 3 | Boolean Algebra Under Noise | yes (AND/OR/NOT under noise, composition theorem) |
| | 4 | Two Axioms and Kronecker Factorization | no (theory) |
| **II. From Bits to Sets** | 5 | Approximate Sets and Predicates | yes (Bloom filter from scratch) |
| | 6 | Composition of Sets | light (set ops simulator) |
| | 7 | Classification Measures | yes (PPV/NPV/F1 as random variables; delta-method CIs) |
| | 8 | Information-Theoretic Bounds | light (entropy calculator, optimal-rate plots) |
| **III. From Sets to Maps** | 9 | Approximate Functions and n-ary Channels | yes (n-ary channels, capacity) |
| | 10 | Sketches and Estimators | yes (CountMin, HyperLogLog, MinHash) |
| | 11 | Randomized Algorithms | yes (Miller-Rabin formal; Las Vegas vs. Monte Carlo) |
| | 12 | Approximate Relations | yes (approximate joins) |
| | 13 | The Algebra of Approximate Types | no (theory) |
| **IV. Optimality and Construction** | 14 | Optimal Bernoulli Sets (BHF) | yes (BHF construction; reaching the bound) |
| | 15 | Perfect Hash Filters | yes (PHF; ranked search) |
| **V. The Boundary and Beyond** | 16 | Approximate but Not Bernoulli | light (correlated-error simulator) |
| | 17 | Cipher Maps and Trapdoor Computing | no (theory + sidebar on oblivious computing) |
| | 18 | Encrypted Search as Relaxed Trapdoor | yes (toy encrypted search demo) |

**Appendices:**
- A. Probability Refresher
- B. The Five Core Principles (cheat sheet)
- C. Library Walkthrough
- D. Selected Exercise Solutions

**Notebook discipline:** "lockstep where natural." Of 18 chapters, ~11 carry
substantive notebooks, ~4 carry light notebooks (small simulations or
visualizations), and 3 are theory-only with no notebook. This is named
explicitly in the preface so readers do not feel something is missing in the
theory chapters.

## 6. Code Companion: Python Library + Notebooks

**Repository:** `bernoulli/python/` (subtree, pushes to `queelius/bernoulli-py`
on GitHub).

**Library identity:** the library is teaching-oriented, not
performance-oriented. Tagline: *"the type, not the data structure."*

**Public API:** `Bernoulli[T]` is the only primary abstraction. Everything
else (Bloom filter, BHF, PHF, Miller-Rabin protocol, n-ary channel, sketches)
is a constructor that returns a `Bernoulli[T]` instance for the appropriate
T. Composition operators (union, intersection, complement, AND, OR, NOT,
sequential and parallel composition) are methods on `Bernoulli[T]` that
return new `Bernoulli[T']`.

**Two operating modes:**
- *Numerical*: numpy-backed simulation; sample, estimate empirical rates,
  validate theory.
- *Symbolic*: sympy-backed; closed-form error rate propagation; matches the
  paper formulas exactly. Useful for the algebra-of-types chapter.

**Notebook convention:** one `.ipynb` per chapter that has a notebook,
filename `chXX-<short-topic>.ipynb`, living in `bernoulli/python/notebooks/`.
Book references notebooks by URL pointing to the GitHub repo; readers can
also `git clone` and run locally.

**Position relative to `bernoulli-cpp/`:** the existing C++ library remains
as the high-performance reference implementation. The Python library is the
*book companion*, optimized for clarity. Both are valid artifacts; they serve
different audiences.

**PyPI name action item:** check whether `bernoulli` is available on PyPI
before committing. Fallback: `bernoulli-types`. (See section 12.)

## 7. Tooling

**Book source:** LaTeX (book class). Matches the 9 existing papers in
`bernoulli/papers/`, allowing direct reformulation of paper material into
chapters. Mathematical typography is the highest-quality option for a
monograph with this much algebra.

**Build:**
```
cd bernoulli/book && pdflatex book.tex && bibtex book && pdflatex book.tex && pdflatex book.tex
```
Or via a `Makefile` (preferred, like `bernoulli-hash-function/`).

**Notebooks:** Jupyter `.ipynb`, run against the Python library. Notebooks
are not built into the book; they are referenced by URL.

**Future option (not committed):** Quarto-based HTML build for free
online-readable version. Decided after the LaTeX is mature.

## 8. Citation Policy

**Cite, do not subsume.** The 9 existing papers in `bernoulli/papers/`
remain the canonical citable sources for specific results. The book does
not reproduce paper proofs verbatim (self-plagiarism territory and
pedagogically dull). It reformulates, condenses, and chooses which proofs
make it into the main text.

**Citation locations:**
- *Inline*: when stating a result that has a sharper or more general form in
  a paper, cite at the point of statement. ("This is a special case of the
  composition theorem in Towell (2026a).")
- *Chapter-end Bibliographic Notes*: a paragraph or two per chapter pointing
  to the underlying papers, related work, and natural deeper reading. Knuth
  / CLRS pattern.

**Stable citations:** lock paper versions (DOI / arXiv ID) before book
print run. Several papers are still under revision; this is a downstream
gate, not a now-decision.

## 9. Repository Layout

Two new git subtrees in this monorepo, consistent with the existing pattern.

| Path | Subtree remote | Purpose |
|---|---|---|
| `bernoulli/book/` | `queelius/bernoulli-book` (new) | Book LaTeX sources |
| `bernoulli/python/` | `queelius/bernoulli-py` (new) | Python library + notebooks |
| `bernoulli/papers/` | (existing remotes) | Paper sources, untouched |
| `bernoulli/bernoulli-cpp/` | `queelius/bernoulli-cpp` (existing) | C++ reference library, untouched |

**Top-level `CLAUDE.md`** updates once the new subtrees are created, adding
two rows to the routing table and two entries to the subtree workflow table.

## 10. Prerequisites (declared in preface)

**Required:**
- Undergraduate probability: random variables, expectation, variance,
  Bernoulli, binomial, normal, Poisson distributions
- Basic discrete math: sets, functions, relations
- Comfort with proof and mathematical notation
- Working Python (read code, run cells) for notebook companion

**Helpful but not required:**
- Linear algebra (Kronecker factorization in chapter 4)
- Information theory basics (entropy in chapter 8)
- Type theory exposure (chapter 13 algebraic types)
- Cryptography basics (chapters 17 and 18 on trapdoor computing)

The preface should be honest about which chapters are easier and which
demand more. Readers who want a soft landing can stop after Part III.

## 11. Exercises

End-of-chapter, numbered, optional. Mix of:
- *Pencil-and-paper proofs* (extend a result in the chapter, prove a corollary)
- *Computational* ("compute X using the library; compare to the formula")
- *Conceptual* ("give an example of a process that violates Axiom 2")

Selected solutions in Appendix D, roughly half the exercises worked. The
unworked half are reader practice.

## 12. Open Action Items (pre-implementation)

Items the design doesn't lock but flags for resolution before or during
implementation:

1. **PyPI name availability:** check `bernoulli` on PyPI; fall back to
   `bernoulli-types` if taken. (Pre-implementation; affects library naming
   throughout the book.)
2. **Title finalization:** working title is *Bernoulli Types: An Algebra of
   Approximate Computation*. Final title can revisit closer to publication.
3. **Publication target:** self-published / academic press / free online +
   paid print. Affects nothing in early drafting; revisit after Part III is
   drafted.
4. **DOI freeze for cited papers:** several papers in `papers/` are still
   under revision. Lock DOIs before final book typesetting. Tracked
   downstream of paper revision cycles.
5. **Notebook framework:** plain Jupyter vs. Quarto-rendered. Default to
   plain Jupyter (`.ipynb`) for now; reassess once Part I is drafted.

## 13. Sequencing and Build Plan (high-level)

Three milestones, roughly equal in effort, ordered to deliver a publishable
artifact incrementally:

**Milestone 1: Parts I-III drafted (~330 pp).** Atom, Sets, Maps. The
unification thesis is fully expressed. Algebraic types chapter (13) closes
the theoretical arc. If energy or time runs out here, the book is already
publishable as *An Introduction to Bernoulli Types*.

**Milestone 2: Parts IV-V drafted (~170 pp).** Optimal constructions (BHF,
PHF) and the Boundary (negative space, trapdoor computing, encrypted
search). Adds the constructive and the application climaxes. The full
~500 pp book.

**Milestone 3: polishing.** Exercises and solutions. Bibliographic notes.
Index. Final figures. PyPI release. Subtree push to `bernoulli-book` and
`bernoulli-py` GitHub repos.

This is the brainstorming-stage build plan. The detailed implementation plan
will be written by `superpowers:writing-plans` immediately after this design
is approved.

## 14. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Encyclopedic books don't get finished. | Part structure: Parts I-III alone are publishable. Milestone 1 is a graceful exit. |
| Lockstep notebooks rot as Python deps change. | Pin a `requirements.txt` per major book version; CI tests notebooks against pinned deps. |
| Citations to papers under revision become stale. | Freeze DOIs only at typesetting time. During drafting, cite by working title; refactor at the end. |
| Library competes poorly against established Python Bloom-filter packages. | Defensive niche: lead with `Bernoulli[T]` as the *concept*, not Bloom filters. Tagline "the type, not the data structure." |
| Book voice drifts toward survey under the breadth aside (algorithms, channels, processes). | Atom-outward spine forces every chapter to derive its examples from the framework, not survey them. Negative-space chapter (16) explicitly bounds scope. |
| Some chapters (4, 13) are theory-only and may feel dry. | Honest preface; partial-solution exercises; insight callouts; do not force notebooks where unnatural. |

## 15. Out of Scope

The book is not, and should not become:
- A survey of probabilistic data structures
- A tutorial on the Python library (the library has its own docs)
- A graduate textbook on information theory or coding theory (uses results,
  doesn't develop them)
- A replacement for the underlying papers (cites them, doesn't subsume them)
- A treatise on cryptography (chapters 17 and 18 use crypto, do not develop it)

If a chapter starts to drift into any of the above, that is a signal to
trim or refactor rather than expand.

## 16. Success Criteria

The book is successful if:
1. A motivated B+D reader can finish Parts I-III in a focused term and emerge
   able to apply `Bernoulli[T]` to their own work.
2. A specialist can pick up Parts IV and V and find non-trivial new material
   relative to the underlying papers (the unification framing, the
   relaxed-trapdoor framing, the algebraic-types treatment).
3. The Python library has organic adoption traceable to the book.
4. At least one course adopts the book as primary or supplementary text.
5. The negative-space chapter (16) gets cited as a useful map of where the
   framework does and does not apply.
