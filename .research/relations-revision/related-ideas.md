# Related-manuscript transfers and borrowing hazards

Surveyed 2026-10-13 following the user's invitation to draw from all related papers.
The relations revision incorporates the first three ideas with explicit qualifications.
No other manuscript was edited in this revision.

## Transfers

1. **Condition on construction statistics.** The book's
   `book/chapters/ch16/correlated-noise.tex:118` discusses occupancy conditioning;
   `papers/bernoulli-hash-function/sections/shf.tex:172` supplies a shared random
   threshold/FPR example. For fixed exact false truth x, suppose absent source
   outcomes are conditionally iid Bernoulli(P_x(C)) and members are always one.
   With s=s0(F), conditional application of the boundary contract followed by
   Jensen gives error ≤ E[1−(1−P_x)^s] ≤ 1−(1−E[P_x])^s. A mean bound uniform
   over exact profiles is sufficient. This is elementary conditioning/Jensen,
   not a new arbitrary-dependence calculus. The new paper states it as a corollary.

2. **Physical storage sharing differs from source aliasing.**
   `papers/bernoulli-phf/paper/sections/rd_ph_filter.tex:116` describes the
   standard perfect-hash-plus-fingerprint representation. Conditional on placement
   and member fingerprints, independent ideal fingerprints of distinct absent
   keys match their stored slots independently with constant probability 2^-M,
   even if their slots coincide. Require placement independent of the fingerprint
   oracle and construction not inspecting negative fingerprints. Reusing the
   same canonical key instead reuses an outcome. This is a realization of an
   established AMQ construction, not a novel filter.
   The primary paper [Dietzfelbinger and Pagh (2008)](https://arxiv.org/abs/0803.3693)
   and its [author-hosted text](https://www.rasmuspagh.net/papers/bloomier.pdf)
   were checked; the published retrieval-to-membership connection is cited.

3. **Convert error calibration to an explicit design calculation.**
   `papers/bernoulli_entropy/sections/space_complexity.tex:14` and `:72` give
   membership-space scales and Bloom sizing. For α_s=1−(1−δ)^(1/s), a design
   costing c n log2(1/α) adds c n log2(δ/α_s) bits over tuple-sized δ. Canonical
   representatives also change n. This is neither a query-specific encoding lower
   bound nor an exact prediction of serialized bytes. The experiment reports bytes.

4. **Parameter uncertainty differs from outcome dependence.**
   `papers/bernoulli_composition/sections/uncertain_rates.tex:27` suggests endpoint
   propagation: a justified simultaneous upper bound α≤U gives query bound g_s(U).
   A 1−η confidence statement remains a confidence statement, not deterministic
   certification. Sampling units must be distinct independent constructions where
   within-build query errors are dependent. The current experiment already uses
   construction-level means; no new rate-estimation theorem is asserted.

## Decisive problems to track separately

- **BHF discrete order statistic.**
  `papers/bernoulli-hash-function/sections/shf.tex:264` states a without-replacement
  order-statistic PMF for iid discrete uniform samples. With N=2,m=2,p=1 the
  displayed formula gives P(T=0)=1, but iid enumeration gives P(T=0)=3/4 and
  P(T=1)=1/4. The continuous Beta limit does not repair the finite exact claim.
  Do not import that theorem or the shifted beta-binomial assertion.
- **Map composition closure under collisions.**
  `papers/bernoulli_maps/sections/bernoulli_map.tex:56` requires independent input
  correctness indicators, while `sections/composition_new.tex:74` claims closure.
  If exact f sends x1 and x2 to the same y, a frozen random failure of g(y) is
  shared by both composed outputs. Correct marginals do not imply the original
  independent-input law. A separate correction should scope or generalize closure.
- **Entropy proof scope.** The manuscript's move from fixed-length deterministic
  counting to randomized expected description length is too abbreviated to borrow
  as a general theorem. The relations paper uses an explicitly assumed filter
  cost scale and measurements instead.

`check_borrowed_models.py` checks the discrete-threshold counterexample, a tiny
Bloom shared-rate example (marginal 3/4, AND 5/8 rather than 9/16), and ideal
fingerprint independence across shared/different slots with exact arithmetic.
These are finite checks and examples; the conditioning proofs remain the basis
for the general statements.
