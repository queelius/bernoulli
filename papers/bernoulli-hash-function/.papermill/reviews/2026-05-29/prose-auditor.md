# Prose Auditor Report

**Paper:** The Bernoulli Hash Function
**Date:** 2026-05-29

## Overall Assessment

The writing is clear, well-structured, and notably cleaner than the 2026-02-26
draft. The two most damaging prose defects from the prior pass are gone: the
"Wait---" self-correction in the appendix is removed, and the "an BHF"
article error no longer appears anywhere in the sources. Notation is consistent
(alex.sty + defs.tex). The exposition flows logically: definitions, predicates,
algorithms, space, entropy, then applications. The comparison table and the
three pgfplots figures carry their weight.

Residual issues are modest: two sections remain thin, a small set of stylistic
nits persists, and one LaTeX typesetting artifact (a `\phantom{x}` empty
denominator) survives in a displayed equation. None are structural.

## Findings

### MINOR-1: Sections 7 (Probabilistic model) and 8 (Set operations) remain thin
- **Location:** `sections/prob_model.tex` (44 lines) and
  `sections/operations.tex` (75 lines as built).
- **Problem:** Section 7 restates FP/FN binomial distributions and the expected-
  cardinality formula, all attributed to the companions, with no BHF-specific
  content. Section 8 proves two short convergence facts that follow directly
  from the Bernoulli set definition (false positives survive intersection with
  prob eps^k; false negatives survive union with prob fnr^k). Both read as brief
  interludes. This is unchanged from the prior pass.
- **Suggestion:** Either (a) add BHF-specific texture (e.g. how the *adaptive*
  threshold's random FPR changes the FP distribution in Sec. 7, or what
  intersecting independent *adaptive* BHF instances does), or (b) fold Sec. 7
  into preliminaries and Sec. 8 into the discussion. Option (a) is preferable
  because it would convert filler into novelty.
- **Severity:** Minor.

### MINOR-2: Stray `\phantom{x}` denominator in the info-interpretation remark
- **Location:** `sections/space.tex`, Remark `rem:info_interp`, the displayed
  `H(Q)` equation (lines 255-261).
- **Quoted text:** `\Entropy(\RV{Q}) = \frac{-\log_2 p + (1-p)\log_2(1-p)/p}
  {\phantom{x}} = ...`
- **Problem:** The `\frac{...}{\phantom{x}}` renders as a fraction bar over empty
  space, a leftover from editing. (The numerator content is also mathematically
  off; see logic-checker MINOR-2, which is the substantive version of this.)
- **Suggestion:** Remove the `\frac{}{\phantom{x}}` wrapper; render the
  expression inline as an ordinary equation.
- **Severity:** Minor (cosmetic; the math error is logged separately).

### MINOR-3: Abstract is dense on the adaptive variant
- **Location:** `main.tex`, abstract, lines 60-66.
- **Quoted text:** "an *adaptive threshold* variant that determines the
  threshold from the data itself, eliminating the salt search entirely for sets
  and achieving vanishing per-element space---at the cost of a random false
  positive rate."
- **Observation:** This is already simplified relative to the prior draft (the
  p-th-order-statistic and O(log N/m) jargon were removed from the abstract).
  Good. The abstract uses an em dash ("space---at the cost"); if the venue or
  house style prefers, replace with a comma or colon. Otherwise no change.
- **Severity:** Minor / optional.

### MINOR-4: "salt" introduced informally before its role is pinned down
- **Location:** `sections/intro.tex` line 19 ("A *salt* is a bit string `b`
  discovered by search...") versus Def. 3.1, which uses `b` without labeling it
  "salt."
- **Problem:** The intro does now italicize and gloss "salt," which is an
  improvement, but the formal Def. `def:acceptance` does not connect the term to
  the symbol `b`. A reader who jumps to Sec. 3 sees `b in B*` with no tie to the
  word "salt."
- **Suggestion:** In Def. 3.1, write "a *salt* `b in B*`" so the term and symbol
  are bound at the formal definition.
- **Severity:** Minor.

### MINOR-5: siunitx "bits per element" styling
- **Location:** `sections/prelim.tex` (x2) and `sections/space.tex` (x4) use
  `\si{bits \per element}`.
- **Observation:** Using siunitx for "bits/element" is unusual in CS theory and
  some readers find it heavy, but it is internally consistent and harmless. Style
  choice; no change required. Flagging only because a copy editor might.
- **Severity:** Minor / optional.

### SUGGESTION-1: Notation table
The paper juggles eps, fnr, mu, m, N, t, p, b, h, h*, h_k, L, Q. A short symbol
table at the end of Sec. 2 would help readers, especially given the set-vs-map
parameter overlap.

### SUGGESTION-2: Running example
A concrete toy (m = 3, eps = 0.25, N = 4) carried from construction through the
space and adaptive sections would make the framework land faster. The deleted
`fig_shs` figure apparently illustrated exactly such an example (`h*(x_i||b)
mod 4`); a refreshed version would be welcome (see format-validator on the
figure's removal).

## Status vs Prior Pass

| Prior prose finding | Status |
|---|---|
| CRITICAL "Wait---" in App. B | RESOLVED (removed) |
| MAJOR "an BHF" article error (x3) | RESOLVED (none in sources) |
| MAJOR Sections 7/8 too thin | OPEN (MINOR-1 here) |
| MINOR Bloom formula wrong in Sec. 9 | RESOLVED (now log2(e)*log2(1/eps)) |
| MINOR abstract density | MOSTLY RESOLVED (simplified) |
| MINOR "salt" used before definition | MOSTLY RESOLVED (intro glosses it) |
| MINOR fig references old SHS naming | RESOLVED (figure removed entirely) |

Overall the prose is at or near submission quality; the remaining items are
polish, not blockers.
