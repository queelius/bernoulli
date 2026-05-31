# Prose Auditor Report, The Perfect Hash Filter

**Date**: 2026-05-29
**Scope**: Writing quality, narrative arc, notation consistency, and presentation. Calibrated to an early (~25%) draft.

## Summary

Where the prose is finished (most of `adt.tex`, the FPR theorem statement, the typed-PHF and fuzzy-IR sections), it is clear, well-structured, and reads like mature technical writing. The problem is unevenness: the introduction is a stub whose forward-references mostly dangle, the central `rd_ph_filter.tex` contains broken sentences and stray symbols at exactly the load-bearing moments, the `cpp_imp.tex` section is half pseudo-code and half TODO, and there are visible authoring scars throughout ("???", "$?$", an empty `\cite{}`, a duplicated theorem, a duplicated figure label). Notation is largely consistent thanks to the shared `sty/` packages, but a few macros are mistyped. The narrative arc the abstract promises (derive PHF, extend to k-perfect, extend to map, apply to IR, implement, discuss ADT) is all present as section skeletons, so the bones are good; the draft needs finishing and de-scarring, not restructuring.

Severity counts: Critical: 0 | Major: 3 | Minor: 5

---

## Major

### P1. The introduction does not function as an introduction
- **Location**: `sections/intro.tex` (whole, 52 lines).
- **Problem**: Two issues. First, the "paper is organized as follows" paragraph (lines 38 to 50) forward-references `sec:phf`, `sec:typed_phf`, `sec:k_perfect`, `sec:pmf`, `sec:apps`, `sec:impl`, `sec:adt`; with the current build several of these resolve only if the corresponding sections compile, and `sec:phf` lives in `rd_ph_filter.tex` whose inclusion currently breaks the build (see format report), so as shipped the roadmap points partly into the void. Second, the intro has no motivation paragraph (why does anyone need another AMQ?), no statement of contributions, and no related work; it jumps from "Bernoulli sets exist" to "we derive the PHF." For an implementation paper this is too thin.
- **Suggestion**: Add (a) a short motivation (immutable, read-many AMQ that beats Bloom at low FPR and realizes the Bernoulli ADT), (b) a numbered contributions list, and (c) a one-paragraph related-work pointer (full section can live later). Verify every `\Cref` in the roadmap resolves once the build is fixed.

### P2. The core derivation section has broken sentences and stray symbols at critical points
- **Location**: `sections/rd_ph_filter.tex`.
- **Quoted text**: line 199 (inside the FPR proof): "no other member of `\Set{S}` hashes ?, and `\matrx{V}[i]` is explicitly set to the hash `h(x)`"; lines 58 to 65 contain a dangling, half-written product-type definition: "$\textrm{PerfectHashFilter} = \textrm{BitMatrix} \times \textrm{PerfectHash}$ and a set of functions \begin{enumerate}\item $\SetContains \colon \BitSet^* \times \textrm{PerfectHashFilter}]$\end{enumerate}" immediately followed by an orphaned fragment "tuple of type $[\textrm{BitMatrix}]$ that implements..." (line 65) that repeats the preceding definition.
- **Problem**: The single most important section reads as a working draft: an unbalanced bracket in the `\SetContains` signature, an orphaned duplicated sentence (lines 52 to 65 say the same thing twice with a broken type signature wedged between), and a "?" inside the membership proof. A reader cannot follow the construction's type at the moment it is introduced.
- **Suggestion**: Rewrite lines 52 to 95 as a single clean definition of the PHF as a product type with a typed `contains` signature; remove the orphaned fragment; fix the "?" in the proof; uncomment and finish `alg:PHF_has` (the membership algorithm is currently entirely inside a `\COMMENT{}` block, lines 134 to 160, so the paper defines construction but not, in displayed form, the membership test it keeps referencing).

### P3. The C++ section is not presentable prose
- **Location**: `sections/cpp_imp.tex`.
- **Quoted text**: line 12 "TODO: break up each function/class/maybe method into separate listings and then talk about each separately."; line 15 "Open set of data types, closed set of operations." (orphan sentence); line 152 "`return rate_distortion(A.hash_fn())*(1-fpr(A)); ???`".
- **Problem**: The section alternates between a TODO note to the author, terse orphan phrases, large commented-out blocks (lines 37 to 90, 174 to 260), and a live code listing that does not compile. There is almost no connecting prose explaining the design.
- **Suggestion**: This section needs to be written, not edited. Once the implementation question (which codebase, see methodology M1) is resolved, write 1 to 2 pages of prose around a small number of clean, compiling listings.

---

## Minor

### p1. "???" and "$?$" placeholders left in displayed math/prose
- **Location**: `adt.tex` line 206 ("$?$"), line 428 ("???"); `rd_ph_filter.tex` line 199 ("?"); `cpp_imp.tex` line 152 ("???").
- **Suggestion**: Resolve or remove all four (each is also flagged by logic/methodology as a substantive gap).

### p2. Duplicated figure caption and label
- **Location**: `adt.tex` line 514 and line 579 both `\label{fig:cor_union_same_fprate}`; the same caption text appears on the commented-out figure (line 487) and the live one (line 554). `fig:efficiency_vs_fprate_union_paset` (line 518) is defined inside the `\COMMENT{}` block and so never produced, though not referenced.
- **Suggestion**: Give the live figure a unique label; remove the dead duplicate.

### p3. Minor typographical errors
- **Location**: `rd_ph_filter.tex` line 366 "mutalbe" (mutable); line 418 "memmbership" and "probality"; line 439/464 "maximumn"; line 199/201 `h{$x$}` mis-typed macro (should be `h(x)`); `adt.tex` line 298 `\BL{X}` missing parentheses (should be `\BL(X)`).
- **Suggestion**: A spell/macro pass.

### p4. Abstract over-promises relative to current content
- **Location**: `main.tex` lines 147 to 149.
- **Quoted text**: "we provide a C++ implementation and compare it to the theoretical analysis."
- **Problem**: No comparison exists (methodology C1). The abstract should describe the paper that exists or the paper that will exist by submission, not a middle state.
- **Suggestion**: Align the abstract with the finished scope.

### p5. Two competing crossover numbers stated as fact
- **Location**: `intro.tex` line 20 ("`\varepsilon < 2^{-3}`") vs `rd_ph_filter.tex` line 531 ("more efficient if `\fprate < 2^{-4}`").
- **Problem**: The reader is told two different break-even thresholds. (The difference is the theoretical-PHF vs CHD-based-PHF distinction, but the prose does not flag that, so it reads as a contradiction.)
- **Suggestion**: State both with their assumptions, or pick the realistic one for the intro and defer the other.

---

## Notes on strengths

- `adt.tex` is genuinely well-written: the type/ADT exposition (lines 6 to 23), the deterministic-vs-probabilistic reconciliation (lines 154 to 229), and the semiring-vs-Boolean-algebra point are clear and mature.
- The typed-PHF section (`typed_phf.tex`) and the fuzzy-set/hedge exposition (`apps_postings_list.tex` lines 53 to 93) are clean and pedagogically effective.
- Notation discipline is good overall: the shared `sty/` packages keep `\ASet`, `\fprate`, `\fnrate`, `\Card`, `\BitSet` consistent across sections, which will pay off as the draft is finished.
