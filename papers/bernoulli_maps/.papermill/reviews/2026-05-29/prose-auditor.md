# Prose Auditor Report, bernoulli_maps

**Specialist**: prose-auditor (writing quality, narrative arc, notation consistency)
**Date**: 2026-05-29

## Verdict summary

Sections 1 to 5 (intro, preliminaries, Bernoulli map model, special cases, composition) are well-written: clear narrative, consistent notation, good use of theorem/proof/remark structure, and a strong "Boolean thread" running through. The quality drops noticeably at section 6 (entropy maps) and section 7 (singular hash map), which read like older draft material with definitions that arrive out of order, undefined-on-first-use symbols, and a notational dialect (`hash`, `BL`, `mod t`) that does not match sections 2 to 5. There is one substantive narrative-arc problem (the abstract over-promises the SHM relative to its actual treatment) and a cluster of notation-consistency defects concentrated in section 7.

## MAJOR findings

### M7. Sections 6 to 7 are a register break from sections 1 to 5 (source: prose-auditor)
- **Location**: `entropy_maps.tex` and `shm.tex` versus the rest.
- **Problem**: The first five sections use precise, modern mathematical prose with carefully staged definitions. Section 6 opens well (the "canonical / least-structured element" framing is elegant) but degrades into terse, under-motivated fragments by section 6.6 ("This result is not the result of computing `E[log2 T]`, nor the expectation of its Taylor approximation. It is simply `log2 E[T]`.") that read like margin notes to oneself rather than exposition. Section 7's proof of `thm:shm-success` is the clearest example: it introduces `y = hash(k_1) mod t`, `hash(1 cat k_1) mod BL(v_1)`, and `N < max BL` with no narration of what these mean relative to Algorithm 1's `trunc(hash(x cat b_n), k)`. A reader who has absorbed sections 1 to 5 will feel they have entered a different paper.
- **Why major**: this is the part of the paper carrying the headline space bound (and the part the abstract advertises). Its roughness undercuts the credibility of an otherwise polished manuscript and (per logic-checker C1/M1/M2) co-occurs with the actual mathematical errors. Prose and correctness fail together here.
- **Suggestion**: rewrite sections 6.4 to 7.2 to the standard of sections 1 to 5: stage each definition, narrate each proof step, and use one consistent reduction operation (`trunc(., k)`) throughout. Cut the self-referential asides.
- **Confidence**: high.

### M8. The abstract and intro Contribution 4 over-promise the singular hash map (source: prose-auditor; relevant to novelty-assessor and methodology M6)
- **Location**: abstract; `intro_new.tex` contribution 4.
- **Quoted text** (abstract): "the \emph{singular hash map}, a concrete algorithm achieving the information-theoretic lower bound of $-\log_2 \fprate + \mu$ bits per element."
- **Problem**: "a concrete algorithm achieving" oversells what section 7 delivers: an exponential-expected-time existence construction whose space bound holds only *asymptotically* and whose lower-bound half is not fully proved (logic M3, methodology M6). "Concrete algorithm" sets an expectation of a runnable, practical method; the body provides a theoretical achievability argument. The narrative arc promises more at the top than it pays off at the bottom.
- **Suggestion**: soften to "a hash-based construction that asymptotically attains the lower bound `-log2 eps + mu` bits per element," and in the body add the feasibility caveat. Foreground the composition theorem in the abstract instead (it is the stronger result; see novelty-assessor).
- **Confidence**: high.

## MINOR findings (notation consistency)

### m10. `Maybe` rendering and the `Nothing` symbol are inconsistent across notations (source: prose-auditor)
- **Location**: throughout; `\Maybe` is defined in `algorithmnotation.sty` as `m(...)`, so `\Maybe{\Set{Y}}` renders as `m(Y)`.
- **Problem**: The Maybe-type is central, but `m(Y)` is an idiosyncratic rendering (most readers expect `Y_perp`, `Y ∪ {⊥}`, or `Maybe Y`). Meanwhile the "special value" is sometimes prose "`Nothing`" (a `\SetKwData`) and the partition uses `Dod(f)`. The lifting `X -> Maybe Y` and the partial-function arrow `pfun` (`X ⇸ Y`) coexist without a single statement reconciling `m(Y) = Y ∪ {nothing}`. Cosmetic but recurring.
- **Suggestion**: state once "`m(Y) := Y ∪ {nothing}`" and use one rendering consistently.
- **Confidence**: high.

### m11. `BL` is an algorithm keyword (`$\ell$`) used in math mode as a function (source: prose-auditor)
- **Location**: `shm.tex`, `entropy_maps.tex` (`\BL(b)`, `\BL(z)`, `\BL(v_j)`); defined in `algorithmnotation.sty` as `\SetKwFunction{BL}{$\ell$}`.
- **Problem**: `\BL` is meant for algorithm pseudocode but is used inside displayed math, rendering as `ℓ(...)` via the algorithm2e keyword styling. It compiles, but mixing a `SetKwFunction` into math mode is fragile and semantically odd (the "bit length" operator should be a `\DeclareMathOperator{\bl}{bl}` or similar). Also `\ell` (the symbol) is separately used in `entropy_maps.tex` for expected code length (`ell = H(Y)`), so `BL` rendering as `ℓ(b)` collides visually with the scalar `ell`.
- **Suggestion**: define a dedicated math operator for bit length (e.g., `\operatorname{len}` or `\lvert\cdot\rvert_{bits}`) distinct from the scalar `ell`.
- **Confidence**: high.

### m12. `prelim.tex` defines `set` as "unordered" but `gloss.tex` defines it as "ordered" (source: prose-auditor)
- **Location**: `prelim.tex` Definition 1 ("A set is an unordered collection of distinct elements") vs `gloss.tex` entry `gls-set` ("An ordered collection of distinct elements").
- **Problem**: direct contradiction. (Mitigating: `gloss.tex` is not loaded into the build, see format-validator, so the contradiction is latent, but it is a defect in the source and would surface if the glossary were ever enabled.)
- **Suggestion**: fix `gloss.tex` to "unordered," or remove the orphaned glossary file.
- **Confidence**: high.

### m13. `Dod` vs `Dom` distinction is introduced then used interchangeably (source: prose-auditor)
- **Location**: `prelim.tex` ("`Dod(f) = Dom(f)`; the notation `Dod` is preferred in later sections to emphasize partiality").
- **Problem**: The paper sets up `Dod` (domain of definition) as the preferred symbol, but `Dom` still appears (e.g., in `prelim.tex`'s own table example and the function-as-set-of-pairs equation uses `Dom(f)`). The "preferred in later sections" promise is only loosely kept. Minor, but the careful reader notices the two symbols for one concept.
- **Suggestion**: use `Dod` consistently after the definition, or drop the distinction.
- **Confidence**: medium.

### m14. Several remarks do real work but are unnumbered and easy to miss (source: prose-auditor; overlaps logic m2)
- **Location**: `composition_new.tex`, the remark after `prop:higher-order` (the uniform-FP first-order condition); `bernoulli_map.tex`, the remark on `P` being known a priori.
- **Problem**: Content that qualifies a theorem (e.g., the condition under which composition stays first-order) is placed in unnumbered remarks. Narratively this buries load-bearing caveats. (Logic-checker m2 flags the same remark as a logical-scope issue.)
- **Suggestion**: promote theorem-qualifying remarks into the relevant theorem hypotheses or numbered remarks.
- **Confidence**: high.

### m15. Minor typographic/wording nits (source: prose-auditor)
- `entropy_maps.tex` sec:optimal-code: "the optimally space-efficient code" reads awkwardly; prefer "the space-optimal code."
- `shm.tex` sec:shm-prob: "The \emph{singular hash set} proves that the keys in `f*` are an approximate set ...". A *construction* does not "prove"; reword to "establishes" or "witnesses."
- `gloss.tex`: "poular" (typo for "popular") and "a a" (doubled article) in `gls-blf` and `gls-geo` (latent, file not loaded, but present).
- `def:randomoracle` codomain is `B^infty` while `def:entropy-map` uses `hash: X x B^* -> B^*`; the oracle's infinite output vs the finite hash output is not reconciled in prose (relates to logic M1's `N < max BL`).
- **Confidence**: high.

## Narrative arc assessment
- **Strong**: the intro's "every probabilistic approximation is per-input-independent error over a function space" hook, carried through the Boolean thread and paid off in the special-cases hierarchy and composition algebra. Sections 1 to 5 build cleanly.
- **Weak**: the arc loses tension at section 6 to 7, where the entropy-map/SHM material reads as a separate, older manuscript stapled on, and the abstract's SHM promise is not matched by the body's rigor. The conclusion's "two perspectives, one theorem" paragraph is genuinely good and almost rescues the arc, but it points to a paper (data_type) the reader cannot consult.
- **Recommendation**: restructure so the composition algebra is the climax (it is the best material), and present entropy-map/SHM as a shorter, tightened "construction" coda with honest scope.
