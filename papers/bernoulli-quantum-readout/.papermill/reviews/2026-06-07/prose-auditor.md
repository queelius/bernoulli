# Prose and Presentation Audit

**Paper**: A Forward (epsilon, omega) Calculus for Quantum Readout Error
**Date**: 2026-06-07
**Reviewer role**: prose-auditor (writing quality, narrative arc, notation consistency)

## Overall

The writing is strong: confident, precise, and unusually disciplined about
scope. The narrative arc (gap -> atom -> calculus -> worked example ->
positioning -> limits -> synthesis) is clean and well-signposted; sec:intro ends
with an explicit roadmap and every section delivers what the roadmap promises.
The author has a recognizable, vigorous voice ("never worse than a coin," "they
mitigate; we propagate," "asymmetry intact, without ever forming the exponential
assignment matrix"). For a perspective paper this voice is an asset.

The issues are about *density* and a few notational/consistency snags, not about
clarity of argument.

## Sentence-length and density

Several sentences are very long and carry three or four clauses of technical
load. They are parseable but tax the reader. Examples:

- **Abstract**, the sentence beginning "Yet the bits a circuit reports are
  rarely raw measurements; they are Boolean functions of measured ancillas,
  parities for syndrome and stabilizer extraction, majority votes, and feed-
  forward conditionals, and the error on those derived bits is today
  reconstructed numerically per circuit, or estimated with a symmetrized,
  single-rate rule of thumb." This is one sentence doing the work of three. Split
  it.
- **sec:worked**, the closing sentence of "Reading the table" beginning "The
  point is not that practitioners cannot compute..." runs ~70 words across
  several em-dash-joined clauses. Split after "directly from the per-qubit
  rates."
- **thm:andor proof**: the false-positive paragraph packs the conditioning
  argument, the corner claim, and the cardinality-weighted-average aside into one
  block. Breaking the "all-negative corner is the smallest" aside into its own
  sentence (it already nearly is) would help.

**Minor (P1)**: tighten the longest sentences in the abstract and sec:worked.
None is wrong; several are denser than they need to be.

## Em-dash usage (house-style note)

The manuscript uses the em-dash ("---") liberally (abstract, intro, several
proofs, sec:related). That is fine for the *paper itself* (the soul hook
constrains report files, not the LaTeX source). I flag it only because the dense
em-dash chaining is part of what makes the longest sentences hard: a few of
those dashes are doing the job a period should. This is stylistic, not required.

## Notation consistency  -  mostly clean, a few snags

- The (epsilon, omega) convention is defined once (def:atom) and used uniformly.
  Good.
- **Subscript collision (worth a glance)**: the subscript on rates is overloaded
  across the paper between *qubit index* (epsilon_i, omega_i for qubit i) and
  *operation* (epsilon_and, omega_and, epsilon_or, omega_or). Both are standard
  and context disambiguates, but the reader meets epsilon_i and epsilon_{wedge}
  in the same theorem. Consider a one-line note at the head of sec:calculus that
  subscripts are indices and the connective symbols (wedge, vee) tag derived
  rates. **Minor (P2)**.
- **r_i overloading**: in cor:parity-asym, r_i is the conditioned per-bit flip
  rate; in Remark 4.1 (majority) r is reused for the same notion. Consistent,
  good, but r is introduced mid-corollary without fanfare; a half-clause "the
  conditioned flip rate r_i" at first use (the intro to sec:calculus already
  promises "conditional flip probabilities") would tie it back.
- **q vs r**: thm:parity uses q_i for generic bit-one probabilities; the
  syndrome example uses q for the per-measurement *error*; cor:parity-asym uses
  r_i for flip rates. These are three different roles for two letters within two
  pages. They are individually correct but a reader tracking "what is q here" has
  to re-anchor. **Minor (P3)**: add a one-line bridge in sec:worked noting that
  the example's q is the symmetric per-measurement error, i.e. r_i = q for all i
  in cor:parity-asym.

## Specific local issues

- **Abstract last sentence** lists the five neighbors ("matrix-inversion
  mitigation paradigm, effectus theory, the classical noisy-Boolean-formula
  identities, and asymmetric quantum hypothesis testing") but names only four;
  the fifth (asymmetry-from-relaxation physics) is folded into the body of the
  abstract earlier. Not wrong, but the abstract under-counts what sec:related
  delivers. **Suggestion (P4)**.
- **sec:channel**, "Bayesian recovery" subsection: eq:bayes is correct and well
  motivated, but the subsection's payload ("this is the inverse reading; our
  concern is forward") is a single idea wrapped in a full Bayes derivation. For a
  forward-calculus paper this is a slight detour. Keep it (it earns the
  pucha2021certification distinction later), but consider compressing.
- **cleveref usage** is consistent and correct (verified all targets resolve).
  Mixed \Cref at sentence start vs \cref mid-sentence follows the standard
  convention. Good.
- **"about n times the per-measurement error"** appears in quotes in three
  places (abstract, intro, sec:worked, conclusion) as the folklore foil. It is
  effective once or twice; by the conclusion it is the fourth airing. Trim one.
  **Suggestion (P5)**.

## Title

The title is long ("A Forward (epsilon, omega) Calculus for Quantum Readout
Error and the Classical Post-Processing of Measurement Outcomes"). It is
accurate but the "and the Classical Post-Processing of Measurement Outcomes" tail
restates "Boolean post-processing," which the first half implies. A shorter
title would read better, but this is purely optional. **Suggestion (P6)**.

## Findings

- **Minor (P1)**: A handful of very long, em-dash-chained sentences (abstract,
  sec:worked closing, thm:andor proof) should be split.
- **Minor (P2)**: Note at the head of sec:calculus that rate subscripts are
  either qubit indices (i) or connective tags (wedge, vee).
- **Minor (P3)**: Add a one-line bridge in sec:worked relating the example's q
  to r_i = q in cor:parity-asym, to settle the q/r/q_i role-switching.
- **Suggestions (P4-P6)**: abstract neighbor count (4 named vs 5 delivered);
  trim one airing of the "n times" folklore; consider shortening the title.

No Critical or Major prose findings. The exposition is well above the bar for a
draft; the work is in tightening density and pinning down the q/r/index notation
bridges.
