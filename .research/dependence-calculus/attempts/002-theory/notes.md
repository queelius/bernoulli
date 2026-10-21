# Mathematical alternatives

Owned files: this directory only. No core package or manuscript edits.

The initial generic source-aware Boolean-calculus direction overlaps provenance,
weighted model counting, dissociation, and recent named-uncertainty languages.
Root requested a pivot to the interaction between canonical constraints and
query inference. `theory.md` records proofs and an explicit relational reduction.

Established mathematically:

- Projection covariance after quotienting; distinct tuple fibers need not have
  distinct canonical source supports.
- Exact `O(L)`-arithmetic inference for normalized witness DNF with width and
  source occurrence at most two, via weighted path/cycle independent sets.
- Classical counting reductions give hard examples at `(width,occurrence)`
  `(2,3)` and `(3,2)`.
- The latter reduction has a fixed relational query and **ordinary symmetry**
  on tuple pairs; a deterministic relation specifies cubic neighbor triples.
- A construction preserving every tuple rate and every individual witness rate
  can nevertheless change exact inference from read-once to #P-hard.

Novelty assessment: these are useful relation-specific consequences of known
counting machinery, not yet a distinct methods contribution. Kanagal–Deshpande
2010 already reports hardness for read-once lineage under correlations; Holant
uses equality constraints directly. Treat an extension/correction to the existing
relations manuscript as more defensible than a new standalone theory paper.

`check_theory.py` independently enumerates rational small cases for path/cycle
probability, projection covariance, and the K4 symmetric edge-cover reduction.
Its output is written to `checks.json` after a successful run.

## Second alternative: exact one-sided worst-case contracts

At root's request, pursued a more contract-specific alternative beyond fixed
truth-profile model counting. `theory.md` Section 8 and `technical-note.tex`
prove:

- Independent homogeneous source noise: worst FPR is
  `1-(1-alpha)^s0`, and worst FNR is `1-(1-beta)^s1` in the corresponding
  one-sided models.
- Heterogeneous rates: exact boundary-certificate product formulas.
- Arbitrary dependence with marginal bounds: sharp homogeneous envelope
  `min(1,alpha*s0)`, and the dual FN expression.
- Binary witness max-occurrence-two graphs: `s0` is the sum of
  `n-ceil(n/3)` over path/cycle components, plus singleton count.

The one-sided sensitivities are standard monotone certificate complexities.
The exact channel formula was not found verbatim in the targeted search, but
the result is an elementary certificate consequence; no independent novelty
claim is justified. Related pointwise noise/sensitivity results are identified
by the literature branch.

Validation on 2026-10-13:

```text
python .research/dependence-calculus/attempts/002-theory/check_theory.py
python .research/dependence-calculus/attempts/002-theory/check_contracts.py
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=.research/dependence-calculus/attempts/002-theory .research/dependence-calculus/attempts/002-theory/technical-note.tex
```

Both programs passed. `contract-checks.json` records all 1,970 exact rational
identity checks on 197 monotone functions with one through four variables and
305 graph invariant checks. PDF built in two passes, with no unresolved
citations/references, overfull boxes, underfull boxes, or remaining warnings
in the final log. All six rendered pages were visually inspected; no clipping,
overlap, or unreadable mathematical notation was observed. The PDF is labeled
an internal research note, and no submission was made.

Final metadata correction: aligned Cai--Lu--Xia with the verified literature
ledger: *Holographic Reduction, Interpolation and Hardness*, Computational
Complexity 21(4):573--604 (2012). Clarified that the note's zero convention for
empty truth classes differs from the prototype's `None` for undefined
conditioning. Theorem semantics are unchanged.
