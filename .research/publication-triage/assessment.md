# Publication decision: no candidate qualifies for the one-week route

Completed 2026-10-14 for Alexander Richard Towell.

**Recommendation: stop this bounded publication search without preparing a new
submission manuscript.** All three selected candidates contain reusable work,
but none has an evidence-backed incremental conventional-research contribution
that can credibly be finished within roughly one author week. This is a
selection judgment for these candidates, not proof that the Bernoulli framework
has no original research potential.

The investigation did not repeat the query-contract planner. Its negative
findings and those of dependence-calculus and relations-revision remain intact.
The user's correction that the companion codec manuscript's submission record
is wrong controls this assessment; no existing submission or venue exclusivity
was assumed.

## Three candidates, judged by the same gates

| Candidate | What survives | Decisive difficulty | Remaining effort and decision |
|---|---|---|---|
| Codec/privacy and multi-instance leakage | Exact ideal-channel classifier, codec TV example, conditional span/prefix laws | DTE/OKVS predecessors; overstated attacker and joint-privacy claims; expected prefix length is not actual stored cost; no demonstrated nontrivial theory increment in the tested refinements | Roughly 1.5–3 days for repairs. Establishing an original contribution is not bounded by the remaining week. **No-go; closest remaining research asset.** |
| Bernoulli hash / PHF construction | Correct finite order statistics and seed-search identities | Claimed adaptive saving changes recall; same-accuracy salvage is ordinary binomial-tail/codebook search; finite formulas need repairs | Roughly 3–6 days for corrected exposition/build, without new research value. **No-go.** |
| Asymmetric quantum readout | Worked probabilities and calibration provenance; scoped channel calculations | Established forward circuit/channel methods; two-rate coarsening fails; pairwise salvage loses to an established cumulant-based comparison and lacks physical validation | Roughly 2–4 days for repaired exposition. New research is not a finishing task. **No-go.** |

These estimates are judgment about remaining author work, not promised review
times or a request to spend those days. The one-week ceiling was a selection
constraint. Draft maturity, passing tests and an available venue did not count
as novelty evidence.

## Evidence that changes the publication decision

**Codec/privacy.** For two independent releases with member law (.99,.01) and
non-member law (.5,.5), the equality attacker has accuracy **75%**, whereas the
exact optimal classifier achieves **87%**. The universal optimal-attacker claim
therefore needs a likelihood-ratio condition. The heavy-tail example's TV
improves from **0.4 to 0.009375**, but both actual 700-key retrievals occupy
**671 packed-payload bytes** and **2161 bytes as Python pickle including the
codec**. Its 16.7% expected-prefix-length increase is not a measured storage
increase. Fresh simulated answers also differ from repeated frozen lookups.

The abstract distribution-shaping mechanism is already present in
[Honey Encryption's DTE construction](https://pages.cs.wisc.edu/~rist/papers/HoneyEncryptionpre.pdf).
[Random-band OKVS](https://www.usenix.org/system/files/usenixsecurity23-bienstock.pdf)
explicitly studies non-input decoding under uniform stored values. That
qualification matters: it does not subsume the companion's arbitrary-value,
zero-filled span statement. The distinction leaves possible narrow novelty,
but not a validated new security guarantee.

The strongest nearby alternative was examined: balanced rank, skewed prefix
projections, realizability, cogirth and randomized full-support invariance.
The balanced result reproduces in **268** finite subspace/projection cases.
The complete-prefix/full-support result has a short proof by lower-bounding
each class mass by its Kraft share and summing; **712** representative choices
also reproduce. These are useful algebraic assets. The independent reviewer
found no established nontrivial theory increment or application advantage in
this bundle. Marginal uniformity still does not imply adaptive transcript
privacy, and the experiments used to bridge that gap do not identify it.

**Hash construction.** The advertised adaptive method becomes almost a random
membership coin at small false-positive rates. At m=N=100, its rank-1 setting
has mean recall **1.5812%** and mean FPR **1.5721%**. Its zero-FN rank-100
setting has FPR **99.4279%**. Enforcing the same recall and FPR cap turns the
construction back into the same binomial-tail acceptance event as fixed
threshold search. The existing shared-seed mechanism and exponential work are
explicit in [ESA 2025, Section 1.1](https://drops.dagstuhl.de/storage/00lipics/lipics-vol351-esa2025/html/LIPIcs.ESA.2025.109/LIPIcs.ESA.2025.109.html).
The audit reproduces 40 exact finite order-statistic cases and isolates the
PHF conditioning/fingerprint corrections. Repairing these results does not
produce a new useful construction.

**Quantum readout.** The central tables and all **54** marginal calibration
rates reproduce from the pinned official source. They validate calculations
under the model, not joint readout behavior on hardware. Even a read-once tree
can produce error **0.03764** while reusing corner-specific two-rate summaries
predicts **0.020392**. The proper fix is ordinary conditional channel
propagation. The only nearby salvage, pairwise crosstalk, is weaker than an
established cumulant reconstruction projected onto parity: in the examined
lambda=.01 case, exact error is **.06226**, the draft gives **.07353**, and
the stronger baseline gives **.06430**. That comparison draws on
[Hamilton et al.'s conditional readout cumulants](https://arxiv.org/abs/2006.01805).

The readout audit records a full-text access limitation for the 2008 PTM
predecessor; its scope claim uses indexed primary text and verified metadata.
It does not pretend to have read an unavailable proof. Independent
counterexamples and accessible readout-channel/cumulant sources provide
additional reasons for the no-go decision.

## Reproducibility and independent review

There are **44 passing new audit tests** (7 codec, 20 hash, 17 readout) and
**62 passing existing codec/retrieval tests**. New audit coverage is 98–100%
depending on module; documented gaps are entry-point/subprocess paths.
Existing codec/retrieval combined statement/branch coverage is **88%**; its
remaining error-handling and boundary gaps are documented rather than hidden.
Ruff checks pass for the new audits; strict mypy passes for the hash and readout
audits. The standalone codec driver and both original readout scripts ran
successfully. A full unchanged-package suite or a LaTeX build is not claimed.

The independent reviewer reran the codec tests, reproduced its JSON output,
checked the strongest theory-note alternative, and found additional scope and
prior-art issues. [Review and resolutions](review.md) distinguish this internal
critical review from external peer review. The hash investigator's turn ended
while finishing documentation; the root completed its registry, corrected a
Fraction typing issue, and reran its checks before relying on the report.

Detailed evidence:

- [Claim–evidence ledger](claim-evidence-ledger.md).
- [Codec assessment and reproduction](candidates/codec-privacy/assessment.md).
- [Hash assessment and reproduction](candidates/hash-construction/assessment.md).
- [Readout assessment and reproduction](candidates/quantum-readout/assessment.md).
- [Verified bibliography](verified-bibliography.json): 23 candidate-tagged
  records, including a shared Ribbon entry and a primary calibration dataset;
  entries state the passages examined and access limitations.

## Best remaining direction and stopping rule

Retain the codec/span material as the strongest research asset. A future
conventional-paper candidate would need **one substantive new theoretical
result or an application benefit under explicit frozen, joint-observation
semantics**, differentiated from DTE/OKVS and random-free-slot baselines. The
present audit supplies neither a promise nor authorization to start another
research program. Given this project's side-project status, the recommendation
is to stop publication-directed expansion here and use the findings to avoid
unsupported claims in future work.

No new LaTeX manuscript or venue-specific version was warranted, so no venue
or fee recommendation is made. Venue eligibility would not establish PhD
credit. Canonical manuscripts and package source were left unchanged; prior
research, archive moves and unrelated edits were preserved. Nothing was
submitted, published, sent to an editor, or purchased.
