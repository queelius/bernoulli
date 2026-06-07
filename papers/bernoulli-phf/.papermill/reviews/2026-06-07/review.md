# Salvageability Assessment — The Perfect Hash Filter

**Date**: 2026-06-07
**Paper**: The Perfect Hash Filter (Alexander Towell, SIUE)
**Root**: `papers/bernoulli-phf/paper/main.tex`
**Reviewer role**: area chair, single-context pass (all specialist lenses applied directly;
no live web search, so all citation/novelty/prior-art claims are marked *needs verification*)
**Benchmark for "par"**: `papers/bernoulli_sets/` (18 pp, complete, theorem/proof rigor, worked
examples, appendices) and its complete companions `bernoulli_composition/`, `bernoulli_entropy/`

**Verdict**: **SALVAGEABLE-WITH-WORK** (substantial, but the hard part — a correct core idea
plus a real implementation — is already in hand)

---

## 0. Headline

This is a real paper with a sound spine and an unusually strong asset (a ~230k-LOC C++
library, `maph`, sitting in the same repo), trapped inside a draft that reads like a
working scratchpad. The central mathematics that I could check independently is **correct**,
the build **succeeds** (28 pp), and the defensible contribution is clear once reframed. What
stands between it and `bernoulli_sets`-level maturity is finishing work and honesty work, not
a new idea: complete two stub sections, write a related-work section from references the `.bib`
already contains, fix a propagating sign error and a handful of placeholder artifacts, qualify
an over-stated optimality claim, and wire the existing library into an experiments section.
None of these is research-hard. I estimate **~3 to 4.5 focused days** to reach par.

A prior multi-agent review exists at `.papermill/reviews/2026-05-29/review.md` (verdict:
not-ready). I independently re-verified its Critical and Major findings against the current
source: they hold, with two corrections in the paper's favor (the build is no longer broken;
the in-repo library is real and substantial), and one finding I can now *upgrade to a positive*:
the space-efficiency table is numerically correct (verified below), not merely unsourced.

---

## 1. Core contribution: what is it trying to establish, and is it sound?

**The thesis.** The Perfect Hash Filter (PHF) is the concrete, deployable member of the
Bernoulli-set family: a static, immutable data structure that realizes the *positive Bernoulli
set* ADT (false-negative rate zero, tunable false-positive rate `eps`). Construction: build a
(minimal) perfect hash `ph_S` over the objective set `S`; at slot `ph_S(x)` store an `M`-bit
fingerprint `h(x)`; test membership by fingerprint equality. The paper then (a) proves the FPR
is exactly `2^{-M}` with zero false negatives, (b) analyzes space complexity and compares to the
Bloom filter, (c) generalizes the perfect hash to a `k`-perfect hash to admit a tunable
false-*negative* rate (making it a genuine two-rate / second-order Bernoulli set), (d) lifts
set membership to key-value lookup (the Perfect Map Filter, realizing the Bernoulli *map*),
(e) applies the map to fuzzy/rank-ordered retrieval, and (f) provides a C++ implementation.

**Is the idea sound and worth finishing? Yes.** Three reasons:

1. **It fills a declared slot in the program.** Per `papers/CLAUDE.md`, this paper *owns* the
   topics "perfect hash filter, k-perfect hashing, the C++ implementation, ranked-search
   application," and `bernoulli_sets` already cites it as `\cite{phf}`. The family needs its
   one end-to-end "here is the theory made real" paper; this is it. Without it, the collection
   is all model and no artifact.

2. **The core mathematics is correct where I can check it.** The FPR theorem (`thm:fp_rate`)
   is right. The space-complexity theorem (`thm:mPHF_size`) and its efficiency table are
   internally consistent and **numerically verified** (see Section 3): my independent
   minimization of the bits-per-element formula reproduces every digit of the paper's optimal
   load-factor table. The `adt.tex` observation that positive/negative approximate sets form
   **semirings** (not Boolean algebras — they are not closed under complement) is a correct and
   genuinely nice structural point.

3. **The implementation asset is exceptional and rare for this kind of paper.** The repo's
   `include/maph/` + `tests/v3/` + `benchmarks/` is a mature, tested C++ library (the broader
   tree totals ~230k LOC). Most implementation papers must *write* the artifact; here it
   already exists, with benchmark harnesses (`bench_latency`, `bench_throughput`,
   `bench_perfect_hash`, `bench_ycsb`). The experiments the abstract promises are a
   wiring-up exercise, not a build-from-scratch.

**The honest novelty (needs verification of prior art).** The bare structure — "MPHF to a
slot, store a `b`-bit fingerprint, compare" — is, to an approximate-membership-query (AMQ)
reader, the well-known static construction behind xor filters, fuse filters, cuckoo filters,
and (for the key-value case) the Bloomier filter. All of these appear in the paper's own `.bib`
(`graf2020`, `fan2014`, `bloomier`, `pagh2005`, `dietzfelbinger2008`) but **none is cited in
prose**, and there is no related-work section. So the contribution is *not* "a new data
structure." Reframed honestly, the contribution is: **(i)** exhibiting the MPHF+fingerprint
structure as a faithful realization of the positive Bernoulli-set ADT and inheriting the whole
family's theory automatically; **(ii)** the `k`-perfect two-rate (FPR *and* FNR) analysis in
the Bernoulli channel framework; **(iii)** the map extension and the fuzzy/ranked-IR
application. That is a legitimate implementation-paper contribution, *provided the framing is
corrected*. (I have no web access; the specific "this is folklore / this is what xor filters do"
attributions should be verified against the literature before submission.)

---

## 2. Current state: concrete inventory (exists vs missing) and build

### Does it compile? YES.

```
cd papers/bernoulli-phf/paper
TEXINPUTS=".:./sty:" pdflatex -shell-escape main.tex && makeglossaries main \
  && bibtex main && pdflatex -shell-escape main.tex && pdflatex -shell-escape main.tex
```

- **Result**: builds clean (exit 0 on all passes), **28 pages**, letter size, bibliography
  resolves (16 real refs cited), glossary builds.
- **23 LaTeX warnings**, all content-level, not build blockers:
  - `Label 'pst:approx_l_b' multiply defined` — the lower-bound **postulate is stated twice**,
    in `rd_ph_filter.tex:211` and `adt.tex:281`, **with two different formulas** (`-log2 eps`
    vs `-(1-fnr) log2 eps`).
  - `dummyref` undefined x4 (`adt.tex` lines 99, 362, 411, 456) — literal placeholder, renders `??`.
  - `thm:fpr`, `thm:fnr` undefined (`adt.tex:25`) — should be `thm:fp_rate`; mis-resolves.
  - empty `\ref{}` x2 (`rd_ph_filter.tex` lines 438, 463) — render `(??)`.
  - `asm:ro` undefined (`rd_ph_filter.tex:201`), `def:approx_set` undefined (`:192`) — the proof
    of the central theorem cites an assumption and a definition that **do not exist in this paper**.
  - `lst:asetunion`, `lst:asetcomp`, `sec:set_theory` undefined (`cpp_imp.tex:31`) — point at
    commented-out content.

> Note: the `state.md` Meta table ("Pages: 10", "only 4 of 8 sections compiled", "rd_ph_filter
> excluded", "tests/ empty") is **stale**. `main.tex` now subfiles **all 8 sections**, the build
> is 28 pp, and `tests/` is **not** empty (it holds the `maph` v3 suite). The most recent
> `state.md` history entries (2026-05-29) already record the build repair; the tables above them
> were not updated. Recommend syncing.

### Section-by-section inventory

| # | Section | Lines | State | What's there | What's missing |
|---|---------|-------|-------|--------------|----------------|
| 1 | `intro.tex` | 52 | **Rewritten, decent** | Motivation, the model's two axioms, both extensions previewed, a roadmap whose cross-refs now resolve | No numbered contributions list; no related-work pointer; repeats the over-stated `eps<2^-3` claim |
| 2 | `rd_ph_filter.tex` | 562 | **Core; ~60%, bimodal** | Definitions (hash, perfect hash, load factor, minimal), **correct FPR theorem**, space theorem + **verified** efficiency table + two efficiency plots, Bloom comparison | Sign-clean but has: broken sentence w/ `?` (l.199), construction-type passage half-rewritten (ll.57-65, orphan dup at 65), membership algorithm entirely inside `\COMMENT{}` (ll.134-160), **duplicated estimator theorem** (ll.426-447 == 451-472), **spurious leading `-`** in both estimators, **empty `\cite{}`** for a pmf (l.387), space theorem leans on unpublished `oph` (l.230), max-entropy-coder "proof" trails off (ll.404-416) |
| 3 | `typed_phf.tex` | 60 | **Clean, near-done** | Typed PHF via injection `X -> B*`, two well-formed algorithms, good footnotes on serialization vs hash-code | Could use one concrete worked instance; otherwise solid |
| 4 | `k_perfect_hashing.tex` | 88 | **Promising; ~50%** | The FNR story, second-order/binary-asymmetric-channel framing, placement-probability model, two algorithms | Placement probability has an **index/off-by-one concern** (geometric "from top" vs product "from bottom" don't visibly match, `j=1` terms disagree); "coupon collector" is a loose label; **no derivation of the FNR `omega` itself** (the section's whole reason for existing); no simulation |
| 5 | `pmf.tex` | 86 | **Stub; ~30%** | PMF definition, a (dense) construction algorithm with self-delimiting codes | Two subsections are literally `% TODO` (space lower bound, entropy upper bound); no FPR/FNR statement for the map; `bloomier` not cited though it is exactly this object |
| 6 | `apps_postings_list.tex` | 95 | **Decent but unconnected; ~55%** | Boolean-search reduction + BNF grammar, fuzzy-set operators, hedges, defuzzification — clean exposition | **No PHF/PMF numbers anywhere** — reads as a generic fuzzy-IR tutorial, not an application *of this structure*; Example (ll.38-51) has a copy-paste bug: `A` and `B` are defined identically (both `Has(Z,x)`); no end-to-end worked retrieval |
| 7 | `cpp_imp.tex` | 274 | **Broken; ~25%** | Prose on ADT/generic-programming framing; intent of union-by-composition and complement operators | Points at a **nonexistent** `random_approximate_sets_adt/` tree; the **real `maph` library is never mentioned**; the one live listing is **not valid C++** (`template PerfectHashFn` l.99, mismatched braces ll.110/118), trailing `???` (l.152); `TODO` note to self (l.12); orphan sentence (l.15); most content commented out |
| 8 | `adt.tex` | 581 | **Most mature; ~75%** | The strongest section: ADT/data-structure exposition, deterministic-vs-probabilistic reconciliation, sigma-algebra/**semiring** structure, space-complexity bounds, union/difference efficiency | **Propagating sign error** in the union proof (theorem says `eps1+eps2-eps1 eps2`, proof body uses `+`, ll.413/421/431); `???` mid-proof (l.428); `$?$` where a number is needed (l.206); sigma-algebra definition left as "closed under..." (ll.51-53); **duplicate figure label** `fig:cor_union_same_fprate` (ll.514, 579); 4x `dummyref`; figure reads absent CSVs (in a `\COMMENT{}`, ll.484-550) |

### Cross-cutting inventory

- **Definitions**: present and mostly clean (hash, perfect hash, minimal PH, load factor, PHF,
  PMF, relative/absolute efficiency, fuzzy operators). One unfinished (sigma-algebra).
- **Theorems/proofs**: FPR (sound); space `thm:mPHF_size` (sound modulo `oph` dependency,
  table verified); union space complexity (right statement, **broken proof**); two cardinality
  estimators (**duplicated**, **sign-flipped**, the "MLE" one is actually method-of-moments);
  max-entropy coder (incomplete). The lower bound is called a **"postulate"** at two sites — it
  is a published result (CFGMW 1978, `carter1978` in the `.bib`) and should be a cited theorem.
- **Worked examples**: thin. One 3-element PHF example (figure is a stub I/we added to restore
  the build — `img/phfilter.tex` is a placeholder, not the real 3-slot diagram). The fuzzy-set
  examples are toy. **No numeric end-to-end example** of construct -> query -> measure.
- **Figures**: 4 live (two efficiency plots in `rd_ph_filter`, two in `adt`), plus the **stub**
  `img/phfilter.tex` and a `\COMMENT{}`-shielded contour/CSV figure in `adt`. `img/` and `data/`
  are otherwise sparse; the real PHF schematic does not exist.
- **Experiments**: **zero**, despite the abstract's "we provide a C++ implementation and compare
  it to the theoretical analysis." This is the single biggest gap relative to the asset available.
- **References**: `references.bib` has **25 entries** — 16 real (Bloom, CFGMW/`carter1978`, FKS,
  Mehlhorn, CHD, BPZ `simple`, cuckoo, xor, ribbon, Bloomier, Pagh-Pagh-Rao, Dietzfelbinger-Pagh,
  Zadeh, Zobel-Moffat, Manning, Broder-Mitzenmacher survey) and **9 unpublished self-cites**
  (`aset`, `obset`, `oph`, `pmf`, `phf`, `bsets`, `bmaps`, `emaps`, `shs`). Of the real refs,
  almost none is cited in prose. Of the self-cites, `oph` and `shs` are **load-bearing** for the
  space theorem and an optimality claim, respectively, and neither manuscript exists.

---

## 3. Correctness: errors, gaps, hand-waving

### Verified correct (bright spots)

- **FPR theorem `thm:fp_rate`** (`rd_ph_filter.tex:183`): `eps = 2^{-M}`, zero false negatives.
  Sound. (Condition-1 prose has a typo `?`, but the logic is right.)
- **Space-efficiency table `fig:abs_eff`** (`rd_ph_filter.tex:277-296`): I independently
  minimized the `thm:mPHF_size` bits-per-element formula
  `log2(e) - (1/r)log2(eps) - (1/r - 1)log2(1/(1-r))` over `r in (0,1)` by ternary search and
  **reproduced every published digit** of `r*`, `e*(X)`, and `e(X,Y)` vs Bloom (Bloom taken at
  `-log2(eps)/ln2`). Example: at `eps=2^-3`, paper `(r*, e*, e(X,Y)) = (0.951741, 0.686016,
  0.989713)`; computed `(0.951741, 0.686016, 0.989713)`. So the table is *correct*, just
  *unsourced in the text* — upgrade from the prior review's "no provenance" to "provenance
  missing but numbers are right." The conditional `thm:mPHF_size` (its perfect-hash term cites
  `oph`) is the only caveat; the *combination* and the curve are verifiably consistent.
- **Semiring structure** (`adt.tex:69`): positive/negative approximate sets are not closed under
  complement, hence semirings under union/intersection rather than Boolean algebras. Correct.
- **Relative/absolute efficiency framework, Bloom `ln 2 ~= 0.69`** — standard and correct.

### Errors and gaps (ranked)

**Critical (block "submittable", not "builds"):**

- **C1 — Sign error propagates through the union space-complexity proof** (`adt.tex`). Theorem
  statement uses inclusion-exclusion `eps1 + eps2 - eps1 eps2` (ll.363, 373, 380); the proof
  body switches to `+ eps1 eps2` (ll.413, 421, 431, in `eq:proof_union_ae`), then silently
  reverts to `-` at the "(revisited)" line 440. The `+` form is wrong and contradicts the
  family's own composition theorem (`eta_total = 1 - prod(1-eta_i)`). A `???` sits mid-proof
  (l.428). The corollary (ll.459-468) compounds it by dividing by `log2(eps1 eps2)`, dropping
  the `alpha` weights the theorem carries. **Fix**: use `-` throughout; re-derive
  `eq:proof_union_ae`; reconcile the corollary.
- **C2 — Core construction presented as novel; no related work** (Abstract, `intro`,
  `rd_ph_filter`). The MPHF+fingerprint AMQ is established prior art (*needs verification*:
  xor/fuse/cuckoo/Bloomier). No related-work section; the right refs are in the `.bib`, uncited.
  **Fix**: add related work; reframe contribution (see Section 1, "honest novelty").
- **C3 — Abstract promises an empirical comparison that does not exist.** Zero experiments;
  the C++ section points at a phantom codebase while the real `maph` library goes undocumented.
  **Fix**: add an experiments section from `maph`'s benchmarks, or drop the promise.

**Major:**

- **M1 — Optimality claim overstated.** "Asymptotically achieves `-log2 eps`" is true only as
  `eps -> 0` (the body says so; the abstract/intro omit it). "For `eps < 2^-3` the PHF is more
  space-efficient" is stated flatly but (a) is benchmarked only against 1970 Bloom, not against
  xor/fuse which reach the same asymptote more cheaply (*needs verification*), and (b)
  **contradicts the paper's own other threshold**: `intro.tex:20` says `2^-3`,
  `rd_ph_filter.tex:531` says `2^-4` (the CHD `alpha(1)=2.07` case). **Fix**: qualify to
  `eps -> 0`; reconcile the two thresholds (they are theoretical-MPHF vs CHD — say so); compare
  honestly with the modern filters.
- **M2 — Load-bearing dependence on unpublished `oph`.** `thm:mPHF_size`'s perfect-hash term is
  "Theorem 3 in `oph`" (`@unpublished, Manuscript in preparation`). Everything downstream
  (corollary, entropy, estimators) inherits the dependency. **Fix**: prove the load-factor
  occupancy/entropy bound inline (it is standard), or mark the result explicitly conditional and
  weaken the abstract.
- **M3 — Duplicated estimator theorem; spurious sign; mislabeled "MLE."**
  `rd_ph_filter.tex` ll.426-447 and 451-472 are the *same* theorem and proof; the second
  relabels it "maximum likelihood estimator" but the proof is a method-of-moments plug-in. Both
  statements carry a leading `-` (`hat m = -BL/(...)`) that makes cardinality negative; the
  proofs' unsigned form is correct. **Fix**: delete one; remove the sign; fix or drop "MLE."
- **M4 — `k`-perfect placement probability indexing.** `k_perfect_hashing.tex` ll.13-27: the
  geometric `K_j ~ Geo((N-j+1)/N)` (occupied-from-top) and the product `prod (1-(j/N)^{k+1})`
  (from-bottom) conventions don't visibly correspond; `j=1` terms disagree. And the section
  never actually **derives the FNR `omega`**, which is its raison d'etre. **Fix**: state the
  placement model precisely; derive `omega`; validate by Monte Carlo (the C++ is right there).
- **M5 — Empty `\cite{}` and `\ref{}`.** `rd_ph_filter.tex:387` asserts a specific pmf on an
  empty citation; ll.438/463 have empty `\ref{}`. Render `[?]`/`(??)`. **Fix**: supply source
  (likely `oph`) or derive; fill the refs.
- **M6 — Lower bound called a "postulate," stated twice, two formulas, duplicate label.**
  `rd_ph_filter.tex:210` (`-log2 eps`) and `adt.tex:280` (`-(1-fnr)log2 eps`), both labeled
  `pst:approx_l_b` (-> multiply-defined warning). It is the published CFGMW result
  (`carter1978`, in the `.bib`). **Fix**: cite `carter1978`, call it a theorem, state it once
  (the general two-rate form), and specialize to `fnr=0` for the PHF.
- **M7 — C++ section disconnected from reality.** Phantom `random_approximate_sets_adt/`
  listings; non-compiling live listing (`template PerfectHashFn`, mismatched braces, `???`); the
  real `maph` (with `include/maph/maph.hpp`, `hashers_perfect.hpp`, v3 tests, benchmarks) is
  never named. **Fix**: rewrite around `maph`'s actual API with a few short *compiling* listings.
- **M8 — Hand-waving at crucial numbers / assumptions.** Independence axiom is *asserted* to
  follow from "cryptographic hash function," never checked; reconciliation lands on `$?$` exactly
  where a probability is needed (`adt.tex:206`, the `|U|=2` case). The central FPR proof cites
  `asm:ro` and `def:approx_set` that **don't exist in this paper**. **Fix**: import/restate the
  needed assumption and definition; fill the `|U|=2` number; add a small empirical independence
  check.
- **M9 — Applications carry no numbers and a copy-paste bug.** `apps_postings_list.tex` Example
  ll.38-51 defines `A` and `B` identically (both `Has(Z,x)`; `B` should be `Has(Z,y)`). The
  whole section never instantiates a PHF/PMF. **Fix**: fix the bug; add one end-to-end ranked
  query with real fingerprint widths and measured behavior.
- **M10 — `pmf.tex` core results are TODO.** Space lower bound and entropy upper bound are empty
  `% TODO`s; no FPR/FNR statement for the map; `bloomier` uncited. **Fix**: state the map's two
  rates; derive (or cite) the bounds; cite `bloomier`.

**Minor (sample; full list mirrors the 2026-05-29 review, all re-confirmed):** typos
("mutalbe", "memmbership", "probality", "maximumn", "cardality"); `h{$x$}` mis-typed macro
(ll.199, 201); `\BL{X}` missing parens (`adt.tex:298`); `\AbsoluteEfficiency` is defined as an
`algorithm2e` keyword (`\SetKwFunction{AbsoluteEfficiency}{E}`) yet used 20x as a math operator
in `adt.tex` (renders, but is a notation abuse); fragile `\COMMENT{}`-gobbling disables whole
algorithms/figures (prefer VCS or `%`); `graf2020` typed `@inproceedings` but has
journal/volume fields (it is `@article`, JEA); `dillinger2021` key-year vs `year={2022}`;
`bloom1970` present but unused while the survey `bf` carries the Bloom cites — cite the primary
source for the `1.44` figure.

### Notation / framework conformance

- Uses the **modular `sty/`** system (not `alex.sty`) — consistent with its declared family
  membership (`bernoulli_maps`, `bernoulli_relations`, `bernoulli_data_type` also use modular).
  Core macros (`\ASet`, `\fprate`, `\fnrate`, `\Set`, `\RV`) match the family. **No notation
  migration needed.** One stray local stub, `obliviousnotation.sty`, is loaded but unused
  (harmless; and per the project's terminology rule, "oblivious" is retired in favor of
  trapdoor/cipher — the file and any residual usage should be renamed/removed during cleanup).
- The Five Core Principles are *implicitly* satisfied (the PHF is exactly Principle 3,
  space-accuracy duality, made concrete, and Principle 5, the Boolean thread, via membership)
  but are **never named or cross-referenced** to `bernoulli_sets`. Par-level papers in this
  family thread these explicitly.

---

## 4. Verdict: SALVAGEABLE-WITH-WORK

**Reasoning.** Rewrite is *not* warranted — that would discard a correct core, a strong
`adt.tex`, a clean `typed_phf.tex`, a verified efficiency analysis, a complete and well-chosen
bibliography, and (decisively) a mature C++ library purpose-built for the experiments the paper
needs. The defects are concentrated and mechanical: one propagating sign error, a duplicated
theorem, placeholder artifacts (`dummyref`, empty `\cite{}/\ref{}`, mismatched theorem labels),
two stub sections, a missing related-work section sourced from refs already in hand, an
over-stated claim that the body itself already knows how to qualify, and a C++ section pointed at
the wrong codebase. Every one of these is finishing/honesty work.

It is also not GOOD/near-par yet: it has zero experiments against an abstract that promises them,
a core section that reads as a draft at the moment it introduces the construction's type, a
load-bearing dependence on a manuscript that does not exist, and a contribution that is mis-framed
as a new structure. Calibrated against `bernoulli_sets` (complete sections, clean cross-refs,
worked examples, explicit framework threading, an honest contribution statement), this paper is
roughly **40-45% of the way** there — but the remaining 55% is unusually low-risk because the
hard assets already exist.

---

## 5. Prioritized plan to reach par with `bernoulli_sets`

Phased so each step leaves the paper in a better, still-building state. Efforts are for one
person familiar with the codebase.

### Phase A — De-risk and de-embarrass (make every page defensible). ~0.5 day
Cheap, high-value, removes all the "draft scars" a reader sees first.

1. **Kill placeholder artifacts.** Replace 4x `\cref{dummyref}` with the real composition-theorem
   citation (`bernoulli_composition` / the family's `eta_total` result); fill the 2 empty
   `\ref{}` (ll.438, 463); fix `thm:fpr,thm:fnr` -> `thm:fp_rate` (`adt.tex:25`); de-duplicate
   the `pst:approx_l_b` label. **~1 h.**
2. **Fix the sign error (C1) and the estimator mess (M3).** `-eps1 eps2` throughout the union
   proof; re-derive `eq:proof_union_ae`; reconcile the corollary; delete the duplicated estimator
   theorem; drop the spurious leading `-`; either justify "MLE" or rename to method-of-moments.
   **~2 h.**
3. **Resolve the missing assumption/definition in the FPR proof (M8 partial).** Restate inline
   the random-oracle assumption (currently `asm:ro`) and the approximate-set definition
   (`def:approx_set`) the proof needs, or import them explicitly from `bernoulli_sets`. **~1 h.**
4. **Sweep the small stuff.** Typos; `h{$x$}` macro; `\BL` parens; the `$?$` at `adt.tex:206`
   (fill the `|U|=2` probability — it is computable); fix the `A`/`B` copy-paste bug in the
   applications example; finish the sigma-algebra definition. **~1 h.**

### Phase B — Honesty: related work + claim calibration (the cheapest credibility win). ~0.5 day

5. **Write a Related Work section (C2).** Deploy refs already in the `.bib`: Bloom + survey;
   CFGMW `carter1978` for the lower bound; FKS/Mehlhorn/BPZ/CHD for perfect hashing and the
   `1.44`/`2.07` bits-per-key figures; cuckoo/xor/ribbon/Bloomier/Pagh-Pagh-Rao/Dietzfelbinger-Pagh
   for the AMQ landscape. One page. State the realistic novelty explicitly (ADT realization +
   k-perfect two-rate analysis + map/fuzzy-IR application). *Verify the prior-art attributions
   against the literature before submission.* **~3 h.**
6. **Reframe abstract + intro (C2/M1).** Drop "we derive a new structure" framing; qualify
   "optimal" to `eps -> 0`; reconcile the `2^-3` vs `2^-4` thresholds (label them theoretical-MPHF
   vs CHD); add a **numbered contributions list**; add a related-work pointer. Reclassify the
   lower bound from "postulate" to cited theorem (M6). **~2 h.**

### Phase C — Finish the core and the stubs (turn 25-50% sections into 90%). ~1.5 days

7. **Complete `rd_ph_filter.tex` (the spine).** Rewrite the construction-type passage (ll.57-65)
   as one clean typed definition; fix the `?` in the FPR proof; **uncomment and finish the
   membership algorithm** (ll.134-160); finish the max-entropy-coder proof or demote it to a
   remark. Resolve the `oph` dependence (M2): prove the perfect-hash load-factor bound inline
   (standard occupancy/entropy argument) — this also lets you *delete* one self-cite. **~5 h.**
8. **Finish `k_perfect_hashing.tex` (the real new analysis).** Fix the placement-probability
   indexing (M4); **derive the FNR `omega`** explicitly as a function of `(m, N, k)`; connect to
   the binary-asymmetric-channel / second-order Bernoulli framing already gestured at. **~3 h.**
9. **Finish `pmf.tex` (M10).** State the map's FPR/FNR; derive (or cite `bloomier` for) the space
   lower bound and entropy upper bound now sitting as `% TODO`. **~2 h.**
10. **Author the real PHF figure.** Replace the stub `img/phfilter.tex` with the actual 3-element,
    5-slot diagram its caption describes (perfect-hash arrows + fingerprint rows). **~1 h.**

### Phase D — The differentiator: experiments from `maph` (C3). ~1 day

11. **Add an Experiments section** driven by the in-repo library (`include/maph/`,
    `benchmarks/bench_*`, `tests/v3/`):
    - **Measured FPR vs predicted `2^{-M}`** across fingerprint widths and seeds (also validates
      the binomial error-count prediction the "Bernoulli set" label promises).
    - **Measured bits/key vs the `-log2 eps + alpha(r)` formula**, with CHD's real `alpha(r)`.
    - **Throughput / construction time vs a real Bloom filter** (and, if feasible, vs a cuckoo or
      xor filter for an honest modern comparison).
    Report hardware/protocol. This is wiring existing harnesses to the paper's predictions, not
    new code. **~5 h.**
12. **Rewrite `cpp_imp.tex` around `maph` (M7).** Delete phantom listings; show a few short
    *compiling* excerpts of the actual API (`maph.hpp`, `hashers_perfect.hpp`); state the
    space/time it actually achieves. **~2 h.**

### Phase E — Polish to family standard. ~0.5 day

13. **Thread the framework explicitly.** One paragraph each: situate the PHF against
    `bernoulli-hash-function` (the *optimal* construction; PHF is the *practical* one) and name
    where it instantiates the Five Core Principles (esp. space-accuracy duality) with cross-refs
    to `bernoulli_sets`. **~2 h.**
14. **Tie off applications (M9).** Give the fuzzy/ranked-search app one end-to-end numeric example
    using a real PMF. **~1 h.**
15. **Bib + notation hygiene.** Fix `graf2020` entry type and `dillinger2021` year; cite
    `bloom1970` for `1.44`; remove/rename the unused `obliviousnotation.sty` and any residual
    "oblivious" usage (terminology rule); upgrade `bsets`/`bmaps`/`pmf` self-cites to real family
    drafts; ensure the only surviving self-cites are ones that exist. Sync `state.md`. **~1 h.**

**Total: ~3 to 4.5 focused days.** Phases A+B alone (~1 day) move it from "not-ready" to a
credible, honest, building draft; A-C (~3 days) make it genuinely solid; the full A-E (~4.5
days) bring it to `bernoulli_sets` par including the experiments that distinguish it.

### Implementation-to-theory story (how to tell it, given the C++ is present)
The asset is the argument: this is the *one* paper in the family with a real, tested, benchmarked
artifact. Lead with that. Structure the narrative as **theory -> ADT realization -> measurement**:
the Bernoulli-set ADT (from `bernoulli_sets`) specifies the contract; the PHF (MPHF+fingerprint)
is shown to satisfy it; `maph` is shown to *be* a PHF; and the experiments confirm the model's
predictions (`2^{-M}` FPR, the bits/key curve, the binomial error counts) on real data. That arc
converts the two current liabilities (a hand-wavy C++ section, zero experiments) into the paper's
strongest section and its headline differentiator versus the purely theoretical companions.

---

## Appendix: verification performed (not inferred)
- **Build**: ran the full chain; 28 pp, exit 0; cataloged all 23 warnings from `main.log`.
- **Math**: independently reproduced the entire `fig:abs_eff` efficiency table by numerical
  minimization of `thm:mPHF_size` (every digit matched).
- **Source**: read all 8 section files end to end; confirmed every Critical/Major finding's
  quoted location by direct read/grep (sign error, duplicated theorem, estimator signs,
  `dummyref`x4, empty `\cite{}/\ref{}`, label collisions, the two-formula postulate, the
  phantom-codebase listings and the non-compiling live listing).
- **Repo**: inventoried the C++ tree; confirmed `include/maph/` + `tests/v3/` + `benchmarks/`
  are real and substantial and that `cpp_imp.tex` references a different, nonexistent tree.
- **Not verifiable here (no web)**: all prior-art / novelty / "this is what xor-fuse-cuckoo-
  Bloomier do" claims, and the published status of `carter1978` as the lower-bound source —
  flagged throughout as *needs verification*.
- **Prior review** at `.papermill/reviews/2026-05-29/review.md` cross-checked; findings hold,
  with build now passing, the in-repo library confirmed real, and the efficiency table upgraded
  from "unsourced" to "verified correct."
