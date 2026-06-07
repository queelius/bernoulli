# Novelty assessor (re-review)

Date: 2026-06-07 (re-review of revision commit 6f136b7)
Scope: did the revision close M3 (no-prior-forward-calculus novelty unverified)
and M4 (unification rests on locator-free self-cites)?

## M3: the no-prior-forward-calculus novelty claim

RESOLVED (via the live-web prior-art follow-up, now treated as confirmed per the
re-review charter, plus a hardening citation in the text).

The prior-art-followup.md pass (live WebSearch / WebFetch against primary
sources) found no direct competitor for the paper's object: a reusable, forward,
closed-form, asymmetric two-rate Boolean-plus-tensor readout calculus that also
unifies with classical probabilistic data structures. The three nearest buckets
(inverse mitigation; single-symmetric-rate noisy-Boolean-formula reliability;
forward circuit-success-rate predictors) are each distinct on a verifiable axis.
The novelty sentence in the intro ("There is at present no reusable, closed-form,
forward calculus that answers this question while preserving the asymmetry")
therefore stands.

The revision also hardened the claim in the text: sec:related (a) now names
koh2024readout (arXiv:2406.07611, "Readout Error Mitigation for Mid-Circuit
Measurements and Feedforward") as the work nearest the motivating examples and
explains it is "still inverse mitigation of measured outcomes, not a forward
symbolic rate calculus." This pre-empts the most likely reviewer objection (that
mid-circuit/feedforward mitigation already covers derived bits) by naming it and
distinguishing it. That is exactly the M3 remedy the prior review specified:
"cite the search to harden the claim." The contribution is correctly positioned
as a synthesis (forward + asymmetric + reusable + unified), with every component
formula honestly disclaimed as prior art in sec:scope item 4.

## M4: the unification claim's support

RESOLVED.

Two complementary fixes, both present:

1. The four framework self-cites that carry the unification (bernoulliSets,
   bernoulliComposition, bernoulliMaps, bernoulliMeasures) now have real Zenodo
   DOIs in both the note and doi fields (19105381, 19105387, 19105389, 19104549),
   so a reader can follow the claim to a locatable source. (bernoulliRelations
   intentionally still lacks a DOI; per the charter this is expected and not a
   finding.)

2. More importantly for novelty: sec:related's unification paragraph now contains
   a self-contained one-paragraph statement of the Bernoulli error model (lines
   722-728): "a random approximate set is the membership indicator of a set A,
   reported through an independent per-element asymmetric channel (eq:channel)
   with false-positive rate eps on nonmembers and false-negative rate omega on
   members, and set operations compose those two rates by the closed forms of
   sec:calculus." This lets the unification claim stand WITHOUT the companion
   papers: the Bloom-filter corner (omega = 0) and the T1-biased interior point
   are both grounded against the in-paper theorems (prop:not, thm:andor,
   thm:parity, cor:composition). The companion papers now "develop the
   consequences" rather than being load-bearing for the core claim.

The prior M4 complaint was that "the most novel assertion is currently
uncheckable" because the only support was five @unpublished, locator-free
self-cites. Both halves are now addressed: locatable (DOIs) and self-contained
(the one-paragraph model). The unification claim is now checkable by a reader
with no access to the companion papers.

## Audience-framing (prior suggestion N3 / cross-verified with prose)

Still a soft point but not a finding: the Bloom-filter/cipher-map unification is
"news" for a Bernoulli reader and "decoration" for a QEC reader. The revision
does not pick a single primary audience and reorder contributions. This is a
stylistic positioning choice, optional, and does not undermine any claim. Carry
forward as a suggestion.

## New novelty findings introduced by the revision

None. The added asymmetric example (M2) actually strengthens novelty: it is the
one place where the asymmetric two-rate machinery produces a number a single-rate
model provably cannot, which is the concrete face of the claimed contribution.

## Verdict

Both novelty Majors (M3, M4) are resolved: M3 by the confirmed prior-art pass
plus the koh2024readout hardening citation; M4 by real DOIs plus a self-contained
model paragraph that makes the unification claim stand alone. No new novelty
issues.
