# Novelty and Contribution Assessment

**Paper**: A Forward (epsilon, omega) Calculus for Quantum Readout Error
**Date**: 2026-06-07
**Reviewer role**: novelty-assessor

**Caveat (declared)**: I have no live web search in this run. Where a novelty
judgment depends on whether a specific prior artifact exists, I flag it as
requiring external verification rather than asserting it. My structural and
internal-consistency judgments do not depend on web access.

## What the paper claims as new, in its own words

From sec:intro (Contribution) and sec:scope item 4, the paper is unusually
explicit. **Not claimed novel**: the single-bit asymmetric channel (def:atom);
the tensor/Kronecker factorization of independent-qubit readout (eq:kron); the
parity identity (eq:parity). **Claimed novel**: (1) the reusable *forward
asymmetric Boolean calculus* carrying both rates through NOT/AND/OR/parity/chain/
tensor (Section 3); (2) its application to quantum readout and the classical
post-processing of measurement outcomes; (3) the unification of a quantum-
hardware error model with the Bernoulli error model of classical probabilistic
data structures (Bloom filters, cipher maps).

This is a disciplined, honest novelty framing. The paper does not try to sell
the parity formula or the asymmetric channel as its own. That candor is a real
strength and should be preserved.

## Is the claimed contribution actually a contribution?

The honest assessment: **the contribution is real but modest, and its
significance rests almost entirely on the unification framing rather than on the
mathematics.** Each individual closed form is, taken alone, elementary:

- NOT swaps the two rates: one line.
- AND/OR product rules: standard independent-event bookkeeping.
- Parity 1/2(1 - prod(1-2 r_i)): the classical noisy-parity identity, which the
  paper correctly attributes as prior art.
- Chain composition 1 - prod(1 - eta_i): the complement-of-all-correct rule,
  which is also the survival-function/reliability-series-system identity and is
  reused verbatim from the author's own bernoulli_composition.
- Tensor factorization: definitional under independence.

None of these is individually surprising to anyone who has done reliability
theory or noisy-circuit analysis. The novelty claim therefore cannot be "these
formulas are new" (they largely are not, and the paper admits as much). The
novelty has to be the **synthesis**: collecting these into one *asymmetric,
forward, reusable* calculus, observing that real readout is asymmetric and that
the asymmetry survives through the Boolean tree in a way single-rate folklore
discards, and identifying that this is literally the same object as the Bernoulli
set/map error model. That synthesis is genuine and, as far as I can determine,
not assembled in exactly this form elsewhere. **But I cannot rule out a direct
competitor without web access**: the specific question "does a prior forward
closed-form asymmetric Boolean calculus for readout-derived bits already exist?"
needs external verification. If such a thing exists (e.g. in a fault-tolerance
or quantum-architecture paper that propagates two-sided readout rates through
syndrome logic symbolically), the contribution narrows from "the missing piece"
to "a cleaner/unified restatement." This is the single most important
load-bearing novelty risk and it is the one I cannot close here.

## The asymmetry claim: is it under-served, or already standard?

The paper's strongest specific claim is that the *asymmetry* (two rates, omega >
epsilon) is routinely thrown away by "symmetrized device tooling" and single-
rate folklore, and that no reusable forward calculus preserves it. The physics
cites (tannu2019mitigating, hicks2021readout) clearly establish that asymmetric
readout bias is real and exploited. The gap the paper asserts is not "nobody
knows readout is asymmetric" but "nobody has packaged the *forward propagation
of both rates through post-processing* as a reusable symbolic calculus." That is
a plausible and narrow enough claim that I find it credible, with the same
external-verification caveat as above. **Requires external check**: whether
assignment-matrix / tensored-mitigation tooling already effectively propagates
asymmetric rates forward (the local 2x2 channels in eq:kron are asymmetric in
those tools), in which case the "they symmetrize" criticism may be too strong
for some of the cited tooling. The paper should make sure it is not attacking a
straw version of the mitigation tools, which themselves keep per-qubit 2x2
channels.

## The unification claim: strongest and weakest at once

The unification with Bloom filters / cipher maps is the most distinctive and
also the most self-referential part. It is the paper's signature, and it is
honestly flagged ("not new *to us*"). Two observations:

1. For a *quantum-readout* audience (the apparent target, given the title and
   QEC lead example), the Bernoulli/Bloom-filter unification is the part most
   likely to read as orthogonal decoration rather than as load-bearing. A QEC
   architect does not gain predictive power from learning that the same formula
   governs Bloom filters; they gain it from the asymmetric forward rules. The
   unification is intellectually satisfying but its *practical* payload for the
   nominal audience is thin. This is a **positioning** issue, not a novelty
   defect: consider whether the paper is for the quantum-readout community
   (then lead with the budgeting utility, demote the Bernoulli framing) or for
   the Bernoulli-framework community (then the QC instantiation is the news).
   Right now it tries to be both and the unification paragraph sits slightly
   uneasily for either.

2. The unification rests on five self-citations to unpublished framework papers
   (bernoulliSets, bernoulliComposition, bernoulliMaps, bernoulliMeasures,
   bernoulliRelations). A reader cannot currently verify the unification claim
   because the cited works are "Companion paper, Bernoulli type theory,"
   unpublished, no DOI/URL in the bib. This weakens the most novel claim by
   making it uncheckable. (See citation-verifier; from a novelty standpoint, an
   unverifiable unification claim is a soft novelty claim.)

## Significance

For a Zenodo-preprint / perspective venue (the stated publication strategy),
the significance bar is "useful framing + correct math + honest scope," which
the paper clears. For a competitive archival venue it would need either the
asymmetric demonstration that is currently missing (see methodology-auditor) or
a sharper, externally-grounded statement that no forward asymmetric readout
calculus exists. The contribution is a clean **minor-to-moderate** advance whose
main value is conceptual organization and a quotable corrective to the "n times
q" folklore.

## Findings

- **Major (N1)**: The single most load-bearing novelty claim ("there is at
  present no reusable, closed-form, forward calculus" preserving asymmetry, and
  the implicit "no direct competitor") cannot be verified internally and was not
  verifiable in this run. Before publication, run a targeted prior-art search
  for an existing forward asymmetric Boolean readout calculus and for whether
  tensored-mitigation tooling already propagates two-sided rates forward. If a
  competitor exists, soften "the missing piece" to "a unified restatement."
- **Major (N2)**: The unification claim, the paper's most distinctive content,
  is supported only by five unpublished, locator-free self-citations, so it is
  currently uncheckable by a reader. Add DOIs/URLs (Zenodo) or a self-contained
  one-paragraph statement of the Bernoulli error model so the unification stands
  on its own.
- **Minor (N3)**: Audience ambiguity. The Bloom-filter/cipher-map unification is
  decoration for a QEC reader and the news for a Bernoulli reader; pick a primary
  audience and order the contributions accordingly.
- **Suggestion (N4)**: Verify the "they symmetrize / single-rate" criticism is
  not too strong for the cited mitigation tools, which retain asymmetric per-
  qubit 2x2 channels; narrow it to "single-rate folklore and symmetrized
  *summary* reporting" if needed.

The novelty is genuine but rests on the unification and the asymmetric-forward
packaging, not on any single formula. The honest not-claimed/claimed list is a
strength; the two Major findings are about *verifiability* of the novel claims,
not about their falsity.
