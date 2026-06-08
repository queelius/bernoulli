# Salvageability Assessment: "The Abstract Data Type of the Approximate Relation"

**Date**: 2026-06-07
**Paper**: `papers/bernoulli_relations/` — "The abstract data type of the *approximate relation*" (Alexander Towell)
**Reviewer role**: Area chair, calibrating against the mature `bernoulli_sets/` and its complete companions `bernoulli_composition/`, `bernoulli_entropy/`.
**Verdict**: **SALVAGEABLE-WITH-WORK** (substantial — roughly one focused rewrite pass, ~3-5 solid days).
**Prior review**: 2026-05-29 (not-ready; 5 critical, 14 major). This pass re-verifies that review against the current tree, confirms the build is now green, and adds two findings the prior pass under-weighted (a TPR inconsistency in the symmetric-closure theorem; the fact that the two "sibling-owned" sections are now *demonstrably superseded* by finished, correct versions in `bernoulli_composition/` and `bernoulli_maps/`).

---

## 1. Core contribution: what is it trying to establish, and is it sound?

**The intended thesis** (from the abstract and the cross-paper topic table): an *approximate relation* is a Bernoulli random approximate set whose universe is a Cartesian product `X₁ × ⋯ × Xₙ`. From that one move, the paper wants to deliver a relational-algebra layer over the Bernoulli model:

1. the approximate relation as an abstract data type (relation = approximate set of tuples);
2. **error propagation through relational operators — join, project, select, and relational composition** (the declared territory unique to this paper);
3. **invariant preservation** — when a random approximation of a reflexive / symmetric / transitive / functional relation can retain that property, and at what rate;
4. the approximate partial function / dictionary as the single-valued special case;
5. an approximate-set-based implementation, the perfect-hash-map, and a trapdoor-database / encrypted-search application.

**Is the core idea sound and worth finishing?** Yes. The central reduction — "a relation is a set of tuples, so a random approximate relation is a Bernoulli set over the product universe, and the whole foundation transfers" — is correct, natural, and is the right capstone for the family. Two of the five planned contributions are genuinely *this paper's own* and are not covered anywhere else in the collection:

- **(2) error propagation through join/project/select.** No sibling owns this. The relational-operator analysis is the paper's reason to exist. The exact (non-approximate) preliminaries for join, projection, composition, and the worked join-then-project example in `relations.tex` are clear and correct, and give a solid base to build the error analysis on.
- **(3) invariant preservation under approximation.** Also unique, and the most original idea in the paper relative to both the family and the external probabilistic-database literature: the probabilistic-DB world models uncertain *data*, but does not ask "does a space-saving approximation of a *symmetric* relation stay symmetric, and with what probability?"

So the contribution is real. The problem is **execution and scope discipline**, not the idea. As written, the paper spends most of its developed pages (a) re-deriving results that two finished sibling papers now own, and (b) leaving its own unique core (join/project propagation; invariants) as stubs. The salvage is essentially: *delete the borrowed material, cite the siblings, and write the two sections that only this paper can write.*

---

## 2. Current state: concrete inventory (exists vs. missing)

### Does it compile?

**Yes — clean build, 15 pages.** Confirmed today:

```
cd papers/bernoulli_relations
TEXINPUTS=".:./sty:" pdflatex -shell-escape main && bibtex main \
  && TEXINPUTS=".:./sty:" pdflatex -shell-escape main \
  && TEXINPUTS=".:./sty:" pdflatex -shell-escape main
# all four passes exit 0; main.pdf = 15 pages
```

This is a **change from the 2026-05-29 review**, which recorded a doubly-broken build. The 2026-05-29 build-repair pass fixed it: it created `references.bib` (4 keys), lifted `\newcommand{\tsr}{\gamma}` into `main.tex`, fixed the `oblivious_rel_model` subfile path, and **commented out four never-written subfiles** (`intro`, `rel_algebra`, `test`, `unused/optimality`). So "it builds" is true but comes with an asterisk: it builds *because the missing sections are commented out of `main.tex`*, not because they were written. Two notes:

- The documented build command in `CLAUDE.md` (`pdflatex main.tex && bibtex …`) still **omits `-shell-escape`** (required by `minted`) and the `TEXINPUTS` prefix. It will fail as written for a fresh checkout. (state.md has the correct invocation; CLAUDE.md does not.)
- 7 residual warnings, all "undefined reference," all pointing at labels inside the commented-out / unfinished material (`thm:subset`, `thm:true_subset_rate`, `sec:powerset`, `sec:bool_search`, `dummyrefs`, `?`, and the `table:`/`tab:` mismatch on `mathrel_vsrelmodel`).

### Section inventory

| Section file | In build? | State | Assessment |
|---|---|---|---|
| `intro.tex` | **No (never written)** | absent from disk | **MISSING.** Commented out in `main.tex`. The paper has no introduction. |
| `relations.tex` | yes | ~complete, correct | **KEEP.** Exact relational-algebra preliminaries (Cartesian product, relation, join, projection, composition) + a correct worked join→project example. Opens with an `integrate:::` scaffolding block (lines 6-10) that must be removed. |
| `approx_rel_model.tex` | yes | partial | **KEEP & REPAIR.** Defines the approximate relation as a Bernoulli set over the product universe; restates two inherited foundation theorems (`thm:fpbinom`, `thm:fpr`) correctly. `def:approx_rel` has the rate-order ambiguity (see §3). No operator error-propagation here yet — this is where the join/project results should land. |
| `rel_algebra.tex` | **No (never written)** | absent from disk | **MISSING.** This is the paper's headline contribution (join/project/select error propagation) and it does not exist. Commented out in `main.tex`. |
| `properties.tex` | yes | partial + mis-scoped | **SPLIT.** Two distinct things welded together: (a) invariant-preservation material (relational, unique, mostly stubs — KEEP & DEVELOP); (b) a long "Random approximate maps" subsection (now owned by `bernoulli_maps/` — CUT/CITE). Contains the symmetric-closure theorem (see §3, new finding) and the unfinished map-composition theorem. |
| `predicates.tex` | yes | **superseded** | **CUT (replace with citation).** Subset/equality predicate rates. `bernoulli_composition/sections/relational.tex` now contains the *finished, correctly-proven* versions of exactly these results. This file is an earlier, partly-wrong draft of sibling-owned material (see §3, C5 and the "superseded" finding). |
| `constrained_ras.tex` | **No (orphaned)** | not subfiled | **CUT/RELOCATE.** Cartesian-product invariant (stated with `?`/`?` rates), power-set FP theorem (Jensen-gap step; belongs to `bernoulli_entropy`/`bernoulli_sets`), disjoint-union theorem. Also has a `\sections{...}` typo that would error if wired in. Not in the build. |
| `oblivious_rel_model.tex` | yes | raw notes | **REWRITE or DEMOTE.** The trapdoor-database / encrypted-search application. Currently a wall of `TODO:`/`NOTE:` notes with a verbatim-duplicated paragraph (lines 5 and 64), an empty `\cite{}`, a stray "[4]", and a `table:`/`tab:` label mismatch. Reads as a notebook, not a section. |

**Definitions / theorems / proofs tally:**
- Correct & proven: `thm:fpbinom`, `thm:fpr` (both inherited restatements of foundation results, fine).
- Stated but unproven / stubbed: symmetric-closure theorem (proof body is a single un-derived probability expression); map-composition theorem (proof ends "…is just the probability that …"); true-subset-rate theorem (proof body is literally `?`); Cartesian-product theorem (rates given as `?`, proof "Prove true positive and false positive rates."); the extended `\tsr` derivation in `predicates.tex` carries a `%%% THIS IS NOT FINISHED` marker and a duplicated display.
- Logically wrong as typeset: `def:approx_pfun` condition (ii) (conditions an event on its own negation); `predicates.tex` equality formula (spurious inclusion-exclusion term).

**Examples:** two good ones (the join→project table example in `relations.tex`; the partial-function table in `properties.tex`). Both correct. No worked *error-propagation* example anywhere — the thing the paper is about has no numerical illustration.

**Figures:** none. No TikZ, no plots. `\graphicspath{img}` points at a non-existent dir (and is mis-braced; should be `{{img/}}`).

**References:** `references.bib` exists with 4 keys (`aset`, `bf`, `phf`, `approxrel`). `approxrel` is a self-reference placeholder. No `bernoulliComposition`, `bernoulliMaps`, `bernoulliEntropy` keys (needed once the duplicated sections are replaced by citations). No external prior art at all — Codd, and the probabilistic/uncertain-database literature (Suciu; Trio; MayBMS) are uncited. Compare `bernoulli_sets/` (22 entries, full related-work paragraph).

**Glossary:** `glossaries` is loaded with `[xindy,toc,acronyms,symbols]` and `\printglossary` is called, but no entries are defined — yields an empty glossary and an extra build step. Drop it or populate it.

### Gap to "par" (the `bernoulli_sets` / `bernoulli_composition` benchmark)

A finished paper in this family has: a structured intro (gap → contribution → related work → companion-paper pointers → organization), 1:1 section-to-file correspondence with no orphans, every theorem proven, a related-work paragraph with real external citations, consistent `alex.sty`-style notation, worked examples, and a clean no-warning build. `bernoulli_sets/` is 18 pp / 22 refs; `bernoulli_composition/` is 15 pp and proves every relational predicate it states. This paper is at: no intro, two missing core sections, four orphan/superseded section files, ~5 unproven or wrong theorems, 4 refs (one a self-placeholder), no external citations, no figures, visible scaffolding throughout, and a build that only succeeds because the gaps are commented out. The *content distance* is larger than the 15-vs-18 page count suggests, because a large fraction of the existing 15 pages is borrowed and must be removed.

---

## 3. Correctness: errors, gaps, hand-waving

I re-verified every critical finding from 2026-05-29 against the current text (quotes confirmed verbatim), and add two findings that pass under-weighted. Numerical checks done in Python where useful.

### Confirmed correctness defects

**C3 (confirmed). `def:approx_pfun` conditions an event on its own negation.** `predicates`-adjacent, `properties.tex` line 233:
> `\Prob{\Tuple{\RV{X}} \in \Dom(\APFun{f}) \Given \Tuple{\RV{X}} \notin \Dom(\APFun{f})} = \fprate`

The conditioning event is `∉ Dom(f̃)` — the approximate function's own domain — so this reads `P(X ∈ Dom(f̃) | X ∉ Dom(f̃)) = ε`, which is identically 0, not ε. The prose ("not in the domain of `f`") shows the intended conditioning set is the *objective* `Dom(f)`. **Fix:** condition on `∉ Dom(\PFun{f})` (matching the correct condition (i) directly above). One-character class of fix, but it is a stated definition, so it is critical.

**C4 (confirmed, and the macro makes it worse than cosmetic). Rate-argument order is not defined by the notation.** I inspected the macros: `\ARelation{R}[a][b]` (in `approxrelationnotation.sty`) expands via `\Relation{#1}[#2][\sigma]` — i.e. in the two-optional-argument form it puts `a` in the subscript and **hardcodes `\sigma` in the superscript, silently discarding `b`**. `\ASet{A}[a][b]` (in `approxsetnotation.sty`) is purely positional subscript/superscript with no semantic binding to FPR/FNR/TPR. The manuscript then uses `\ARelation{R}[\fnrate][\fprate]` (FNR-first) in `def:approx_rel` but `\ARelation{R}(\tprate,\fprate)` (TPR-first, parenthesized) in the symmetric theorem. Because `TPR = 1 − FNR`, slot 1 is ambiguous between an error rate and a success rate, and any downstream formula is at risk of being off by a complement. **Fix:** pick one family-standard order (the `alex.sty` papers use `[\fprate][\tprate]`, i.e. FPR-sub/TPR-super) and apply it everywhere; ideally make the macro self-documenting so the slot carries meaning.

**C5 (confirmed wrong, and now provably so against a finished sibling). Equality-predicate formula has a spurious term.** `predicates.tex` lines 50-53:
> `(\tprate_1 \tprate_2 + \fnrate_1 \fnrate_2 - \tprate_1 \tprate_2 \fnrate_1 \fnrate_2)^{|A|} (\fprate_1 \fprate_2 + \tnrate_1 \tnrate_2 - \fprate_1 \fprate_2 \tnrate_1 \tnrate_2)^{|U|-|A|}`

For two independent approximations to *agree* on a positive element: P(both in) + P(both out) = `τ₁τ₂ + ω₁ω₂`. "Both in" and "both out" are mutually exclusive — there is no inclusion-exclusion correction. The subtracted `−τ₁τ₂ω₁ω₂` is wrong. **This is no longer a judgment call:** `bernoulli_composition/sections/relational.tex`, `cor:equality_prob`, gives the correct formula `(τ₁τ₂ + ω₁ω₂)^|X| (ε₁ε₂ + η₁η₂)^|U|−|X|`, with a full proof. Numerically the gap is real (per-element positive-block factor: correct 0.820 vs. buggy 0.8119 at τ=0.9, ω=0.1). **Fix:** delete the section; cite `cor:equality_prob`.

### New / upgraded findings (beyond the 2026-05-29 pass)

**NEW-1 (correctness — upgrade). The symmetric-closure theorem is internally inconsistent on the TPR, not merely unproven.** `properties.tex` lines 29-31:
> "A random approximate relation `\ARelation{R}(\tprate,\fprate)` of a symmetric relation `R` induces a random approximate symmetric relation `\ARelation{R}[s](\tprate, 1-(1-\fprate)^2)` if we say that `(x₁,x₂) ∈ R̃_s` if `⟨x₁,x₂⟩ ∈ R̃` or `⟨x₂,x₁⟩ ∈ R̃`."

The closure rule is the symmetric OR-closure. For a *negative* pair `(x,y) ∉ R` (with `R` symmetric, so `(y,x) ∉ R` too), the pair enters `R̃_s` if either `(x,y)` or `(y,x)` false-positives, each independently w.p. ε, giving FPR `= 1 − (1−ε)²`. That part is right. **But the identical doubling applies to true positives:** for a positive pair `(x,y) ∈ R` (so `(y,x) ∈ R`), the pair enters `R̃_s` if either of the two independent trials *fires*, each a true positive w.p. τ, so the closure TPR is `1 − (1−τ)²`, **not the unchanged `τ` the theorem claims.** (Numerically, τ=0.9 → closure TPR 0.99, not 0.9.) The theorem reports the FPR boost from the OR but forgets the symmetric TPR boost. The 2026-05-29 review flagged the *proof* as a stub but characterized the *statement* as "plausible/correct in form"; the statement is in fact wrong on the TPR slot. **Fix:** state the induced relation as `\ARelation{R}[s](1-(1-\tprate)^2,\ 1-(1-\fprate)^2)` and prove both slots; also state explicitly that `R` is assumed symmetric (otherwise the negative-pair argument changes). This is the kind of error a Monte Carlo harness would catch instantly (see §5, item 7).

**NEW-2 (scope — sharpened). The two "duplicated" sections are not just topically misplaced; they are superseded by finished, correct sibling versions.** The 2026-05-29 review said map composition "belongs to `bernoulli_maps`" and subset/equality "belong to `bernoulli_composition`." Stronger: both siblings now *contain completed, superior treatments*:
- `predicates.tex`'s subset derivation is the unfinished (`%%% THIS IS NOT FINISHED`, proof body `?`) ancestor of `bernoulli_composition`'s subset theorem, which has the same three-block `I/J/K` partition argument written out and `\qedhere`'d. The relations draft even references the composition paper's eventual structure (`\cref{thm:subset}`, `thm:true_subset_rate`) by labels that never resolve.
- `properties.tex`'s map-composition theorem (TPR `τ₁τ₂`, FPR a vague `IntervalSpan(ε₁τ₂ ∪ τ₁ε₂ ∪ ε₁ε₂)`, proof trailing off) is a cruder version of `bernoulli_maps`'s composition theorem, which gives `ω_{g∘f} = 1−(1−ω₁)(1−ω₂)` and an FPR governed by an explicit overlap parameter ρ. The relations version is both unfinished and less correct (it never defines `IntervalSpan`, and the FPR of a composition is not generally a simple span of those three products).

  **Consequence for salvage:** these are not "move to the right paper" tasks — the right papers already did them better. They are **delete-and-cite** tasks. This is good news: it removes ~two sections of debt rather than relocating it.

### Hand-waving / gaps specific to this paper's own core

- **The signature question is never asked.** Join and project produce tuples that *share components* tested through the same underlying cells, so their membership errors are **not independent** — yet `asm:ber_trial` posits i.i.d. trials and the paper never examines whether element-wise independence (Axiom 1) survives a join or a projection. This is simultaneously the paper's hardest correctness question and its clearest novelty. Right now it is absent. A projection in particular can *merge* distinct tuples down to a shorter tuple, so a projected "false positive" is a union event over the pre-images — the error rate transforms, and that transformation is the result the paper owes the reader.
- **Large-universe tension unresolved.** The subset/equality preservation probabilities carry `|U|` exponents → 0 as `|U| → ∞`, exactly the deployment regime (the manuscript itself notes one such limit). The composition paper resolves this honestly (it states the →0 corollaries as results). This paper raises it and drops it.
- **No validation.** The foundation validates by Monte Carlo (`bernoulli_sets/code/`). Every new propagation claim here is unproven or, in two cases, wrong, with no empirical check. A harness would have caught C5 and NEW-1.

### Prior-art questions (NO web access — flagged for verification)

- **needs verification:** the distinction from *probabilistic / uncertain databases* (Suciu et al.; Trio; MayBMS) — the nearest external neighbor — must be stated and cited. Claimed niche: probabilistic DBs model uncertainty *in the data*; the Bernoulli relation has an *objective* base relation with error injected by a *space-saving representation*, and asks invariant-preservation questions the DB literature does not. Confirm the canonical citations and that no existing work already analyzes FPR/FNR propagation through relational operators in this exact sense.
- **needs verification:** Codd (1970) for the relational-model paragraph in `oblivious_rel_model.tex` (currently an empty `\cite{}` and a stray "[4]").
- **needs verification:** that "perfect-hash-map" and "trapdoor database / rank-ordered encrypted search" are positioned consistently with `bernoulli-phf/` and the trapdoor-computing line, and cite them rather than re-introducing.

---

## 4. Verdict

### SALVAGEABLE-WITH-WORK (substantial)

**Why salvageable, not rewrite-from-scratch:**
- The core reduction is correct and the paper owns real, non-duplicative territory (join/project/select propagation; invariant preservation).
- The reusable assets are non-trivial and *correct*: the exact relational-algebra preliminaries and the join→project worked example (`relations.tex`), the approximate-relation definition and the two inherited theorems (`approx_rel_model.tex`), and the partial-function ADT scaffolding. That is a genuine third of a paper that does not need rewriting.
- It now builds, so iteration is cheap.
- The largest single block of work is *subtractive*: the two most-developed sections are superseded by finished siblings and should be deleted and cited, not rewritten. Deletion is fast and de-risks the paper (it removes the C5 bug and the inconsistent map-composition theorem at a stroke).

**Why not GOOD (near-par):** it is genuinely far from par. No introduction; the two headline sections (`rel_algebra`, and a real invariants section) do not exist; ~5 theorems are unproven or wrong (including the just-found TPR inconsistency); no external citations; no figures; visible scaffolding throughout; the build is green only because the gaps are commented out.

**Why not NOT-SALVAGEABLE:** nothing here is fatally misconceived. There is no wrong central premise, no result that cannot be fixed, no structural dead-end. The defects are "unfinished and over-scoped," which is exactly what a focused pass fixes. The fact that the siblings already proved the hard predicate/composition results *reduces* the remaining work rather than competing with it.

One honest caveat on effort: because so much of the current body is borrowed, the *net new writing* to reach par (intro + a real join/project section + a real invariants section + validation + related work) is close to writing a short paper, even though the scaffolding and preliminaries are in hand. Budget accordingly: this is a multi-day rewrite, not a cleanup.

---

## 5. Concrete, prioritized plan to reach par with `bernoulli_sets`

Ordered so that each step makes the next cheaper. Effort is rough solo-author time. "Lean on composition" notes are called out because relations build on sets and the composition paper already did the set-level relational work.

**Phase A — Stop the bleeding (subtract debt, fix what's wrong). ~0.5 day.**

1. **Delete `predicates.tex` from the paper; replace with a one-paragraph citation** to `bernoulli_composition` (subset theorem + `cor:equality_prob`). This removes C5 entirely and clears the `thm:subset`/`thm:true_subset_rate`/`dummyrefs`/`?` dangling refs. *Lean on composition:* state the subset/equality rates as imported results and move on. (~1 h)
2. **Cut the "Random approximate maps" subsection** from `properties.tex` (the map-composition theorem, currying/composition stubs, the `Dom`/`Range`/augmented-codomain machinery); **replace with a citation** to `bernoulli_maps` (composition theorem with the ρ overlap parameter, `ω_{g∘f}=1−(1−ω₁)(1−ω₂)`). Keep only a single sentence noting that a partial function is the single-valued special case of a relation and that its composition is `bernoulli_maps`'s `join + project`. This removes the unfinished map-composition proof and the `IntervalSpan` hand-wave. (~1 h)
3. **Fix `def:approx_pfun` (C3)** — condition on `∉ Dom(\PFun{f})`. (~5 min)
4. **Fix the symmetric-closure theorem (NEW-1)** — TPR slot to `1−(1−τ)²`, assume `R` symmetric, or defer the theorem to Phase C with the other invariant results. (~15 min if deferred; ~1 h if proven now)
5. **Decommission orphans:** delete `constrained_ras.tex` (or move the genuinely-relational Cartesian-product invariant into the invariants section, Phase C; the power-set/Jensen material belongs to `bernoulli_entropy`, the disjoint-union material to `bernoulli_composition`/`bernoulli_data_type` — cite, don't host). Remove the `\sections{}` typo with the file. (~30 min)
6. **Strip scaffolding** repo-wide: `integrate:::` block (relations.tex 6-10), `TODO:`/`NOTE:` blocks and the duplicated paragraph in `oblivious_rel_model.tex`, stub subsubsections. (~30 min)

**Phase B — Fix the foundation of the build & notation. ~0.5 day.**

7. **Adopt one rate-order convention (C4)** and apply it everywhere. Strongly recommend migrating this paper to **`alex.sty`** (the convention used by all four mature papers: `\ASet`, `\fprate/\fnrate/\tprate/\tnrate`, `\APFun{f}[\fprate][\tprate]`). This single change buys notation parity with the benchmark, kills the ambiguous-slot macro, and makes cross-citation to the siblings frictionless. If a full migration is too invasive now, at minimum redefine `\ARelation` so both slots carry fixed meaning and stop hardcoding `\sigma`. (~2-3 h either way)
8. **Bibliography to par:** add `bernoulliComposition`, `bernoulliMaps`, `bernoulliEntropy`, `bernoulliSets` keys (copy from `bernoulli_sets/references.bib`), `codd1970`, and the probabilistic-DB anchors (Suciu/Trio/MayBMS — *verify*). Resolve `approxrel` self-reference. Fix empty `\cite{}` and stray "[4]" in the oblivious section. (~1 h, +verification)
9. **Build hygiene:** drop the empty `glossaries` machinery (or populate it); fix `\graphicspath{{img/}}`; update `CLAUDE.md`'s build command to the `-shell-escape` + `TEXINPUTS` form already in `state.md`; fix the `table:`/`tab:` label. Target a zero-warning build. (~30 min)

**Phase C — Write the paper's actual contribution. ~2-3 days. This is the center of gravity.**

10. **Write `rel_algebra.tex` — error propagation through join, project, select.** This is the headline and it currently does not exist. *Lean on composition heavily:* a join is an AND-like combination of membership events (cite `bernoulli_composition`'s intersection rates as the per-tuple building block); a projection is an OR/union over pre-image tuples (cite the union rates). Then do the part *only this paper can do*: derive how FPR/FNR transform under each operator and, critically, **address whether Axiom 1 independence survives** (the shared-component problem — likely it does *not* in general for projection, and the honest result is the conditional under which it does). State each as a theorem with a proof and at least one **worked numerical example** mirroring the join→project table already in `relations.tex` but now carrying rates. Target ~4-6 pp. (~1.5 days)
11. **Develop the invariants section** (rename `properties.tex` from "Approximate relations with invariants" to a focused invariants section). Prove reflexive / symmetric / transitive / functional preservation rates. Symmetric closure (fixed per NEW-1) is the model worked result; transitivity is the hard one (state the rate and be honest about the large-`|U|` →0 behavior, as composition does for subset/equality). This is the most original material in the paper. Target ~3-4 pp. (~1 day)
12. **Write `intro.tex`** in the family template (mirror `bernoulli_sets/sections/intro.tex`): gap → contribution (lead with join/project + invariants, *not* with entropy/perfect-hash-map, which belong to siblings) → related work (probabilistic DBs contrast paragraph — the framing the whole paper needs) → companion-paper pointers → organization. (~3 h)
13. **Rewrite the abstract** to claim only this paper's territory: relation-as-Bernoulli-set ADT; join/project/select propagation; invariant preservation; trapdoor-database application. **Drop the over-claims** (bits-per-relation entropy bound → `bernoulli_entropy`; perfect-hash-map construction → `bernoulli-phf`; partial-function composition → `bernoulli_maps`), replacing each with a one-line "see companion." (~30 min)

**Phase D — Validation, application, polish. ~1 day.**

14. **Add a Monte Carlo validation harness** for the new propagation and invariant results, mirroring `bernoulli_sets/code/`: sample a base relation, inject errors at known rates, apply join/project/closure, compare empirical to formula. This both validates and is the safety net that catches sign errors like C5/NEW-1. A short validation table in the paper brings it to par on rigor. (~0.5 day)
15. **Rehabilitate or demote the trapdoor-database application** (`oblivious_rel_model.tex`): either write it as a real section with a stated leakage/threat model and citations to the trapdoor-computing line and `bernoulli-phf`, or downgrade it to an explicitly-labeled short "application sketch." Per repo terminology, prefer "trapdoor/cipher" over "oblivious" in the prose (the filename can stay historical). (~0.5 day)
16. **Add a figure** (even one): e.g., propagated FPR vs. number of joined relations, or invariant-preservation probability vs. `|U|`. The benchmark papers have figures; this has none. (~1-2 h)
17. **Final consistency pass:** fill the empty thesis/prior-art YAML in `state.md`, set a target venue (the relational-algebra angle suits a database/theory venue), typo sweep ("multipicity", "similiar", "umambiguously", double commas, "ake care", "no such such"), confirm 1:1 section-to-file and zero warnings.

### Rough total

| Phase | Work | Effort |
|---|---|---|
| A | Subtract superseded/orphaned content; fix C3, C5, NEW-1 | ~0.5 day |
| B | Notation convention (→`alex.sty`), bib, build hygiene | ~0.5 day |
| C | Write the real contribution: rel_algebra, invariants, intro, abstract | ~2-3 days |
| D | Monte Carlo validation, application, figure, polish | ~1 day |
| **Total** | | **~4-5 focused days** |

### One-line strategic summary

The paper is salvageable and worth salvaging because its unique core (relational-operator error propagation + invariant preservation) is real and unclaimed; the fastest path to par is to **delete the two superseded sections and cite the finished siblings, then spend the freed time writing the join/project and invariants sections the collection still lacks** — leaning on `bernoulli_composition` for the per-tuple set-level rates and confronting head-on the one question no sibling answers: whether element-wise independence survives a join or a projection.

---

## Appendix: verification log

- **Build:** reproduced clean (4 passes exit 0, 15 pp) with `TEXINPUTS=".:./sty:" pdflatex -shell-escape`. 7 undefined-reference warnings, all into commented-out/unfinished material.
- **Quotes:** C3 (`properties.tex` L233), C5 (`predicates.tex` L50-53), NEW-1 (`properties.tex` L29-36) re-read verbatim. C4 confirmed at the macro level by reading `approxrelationnotation.sty` (slot 2 hardcodes `\sigma`) and `approxsetnotation.sty` (positional, no rate binding).
- **Sibling cross-checks:** `bernoulli_composition/sections/relational.tex` confirmed to contain the correct equality formula (`cor:equality_prob`) and the completed subset theorem (the `I/J/K` partition the relations draft leaves unfinished). `bernoulli_maps/sections/{intro_new,composition_new,conclusion}.tex` confirmed to own the map-composition theorem (ρ overlap parameter; `ω_{g∘f}=1−(1−ω₁)(1−ω₂)`).
- **Numerics (Python):** equality formula gap (0.820 correct vs 0.8119 buggy at τ=0.9,ω=0.1); symmetric-closure TPR should be 0.99 = 1−(1−0.9)², not the claimed 0.9.
- **Prior review:** `.papermill/reviews/2026-05-29/` (unified + 7 specialist reports) read in full; this assessment confirms its 5 criticals against the current tree, notes the build is now repaired, and adds NEW-1 (TPR inconsistency) and NEW-2 (sections superseded, not merely misplaced).
