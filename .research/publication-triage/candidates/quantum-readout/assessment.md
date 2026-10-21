# Quantum-readout candidate: no-go within one working week

Author: Alexander Richard Towell. Audit date: 2026-10-14.

**Decision: do not select this candidate for a conventional research paper under
the one-week ceiling.** The worked probabilities are reproducible, but the
claimed forward asymmetric calculus is a specialization of established
probabilistic circuit analysis. Its advertised two-rate closure also needs a
substantive qualification. The one nearby salvage examined—the pairwise
crosstalk correction—does not establish a sufficiently original or practically
validated result. This judgment does not depend on the historical “ready” ratings
or on selecting a more accommodating venue.

The audit changed only this nested research directory. It did not edit the
canonical manuscript, package, venue versions, or earlier research runs.

## Contribution hypothesis and closest baselines

The manuscript claims a reusable symbolic forward calculus that carries an
asymmetric false-positive/false-negative pair through Boolean post-processing,
with syndrome-parity predictions as its lead application. The precise claims are
at [main.tex:156](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:156),
[main.tex:507](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:507),
and [main.tex:1081](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:1081).

The strongest omitted baseline is Krishnaswamy, Viamontes, Markov, and Hayes,
*Probabilistic transfer matrices in symbolic reliability analysis of logic
circuits*, ACM TODAES 13(1), Article 8, 8:1–8:35 (2008),
[DOI 10.1145/1297666.1297674](https://doi.org/10.1145/1297666.1297674).
The indexed primary manuscript's p. 8:2 expressly treats input-pattern-dependent
errors, error probabilities for individual input words, averaging with joint
input probabilities, and reconvergent fanout. Its abstract gives serial matrix
composition, parallel tensor composition, and polynomial reliability
approximations. Those are forward, asymmetric-capable operations. Applying them
to imperfect input wires followed by ideal Boolean gates reproduces this
candidate's model.

**Access limit:** Crossref independently verified the bibliographic metadata.
The primary author-hosted PDF was readable through indexed excerpts, including
the page locator above, but direct retrieval failed (certificate-chain failure;
a diagnostic unauthenticated retry reached a 404). ACM returned 403; a CiteSeer
mirror returned 404. A complete PDF read is not claimed. The scope conclusion
uses the supported indexed text, not an inferred theorem elsewhere in that paper.
See [references.json](references.json).

For the readout setting, Smith et al.'s *Qubit readout error mitigation with
bit-flip averaging*, Science Advances 7(47), eabi8009 (2021), already uses a
general asymmetric response matrix and tensors of asymmetric single-qubit
matrices before introducing an actual physical randomization that removes the
bias. Its Eqs. (9)–(12) and Sec. IV B give the response-channel/Hadamard spectral
description. Symmetrization there is a deliberate protocol; it is not inability
to represent two rates. The full arXiv PDF was read for those passages.
[Paper](https://arxiv.org/abs/2106.05800),
[published DOI](https://doi.org/10.1126/sciadv.abi8009).

The draft correctly concedes that the parity product is classical
([main.tex:461](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:461)).
Replacing each flip probability by the rate appropriate to its fixed latent bit
is conditional-probability substitution. Neither that substitution nor reversing
the direction of an already known channel supplies a research novelty claim.
The comparisons with a linear union bound and an averaged symmetric channel are
useful explanations, but not competitive baselines for a new method.

## Correctness: fixed-word identities pass; universal two-rate closure does not

The distinction matters even when every input appears once. Give every leaf
epsilon = 0.02 and omega = 0.10. For AND:

| Latent word | True AND | Probability of observed AND = 1 |
|---|---:|---:|
| 00 | 0 | 0.0004 |
| 01 | 0 | 0.018 |

Thus no input-distribution-independent false-positive rate exists for the
coarsened output value alone. The manuscript acknowledges that its AND formula
is only the all-negative corner at
[main.tex:341](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:341)
and [main.tex:368](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:368).
That qualification repairs the corner identity; it does not justify the broader
claim of propagating a fixed pair through an entire tree. The OR false-negative
formula has the dual all-positive-corner limitation.

For the read-once tree `(b0 AND b1) OR b2` at latent word `010`, exact enumeration
gives **0.03764**. Reusing the displayed AND corner as its output false-positive
rate and then applying OR gives **0.020392**. There is no source reuse or physical
crosstalk in this example. This is a counterexample to that pair-reuse reading
of the claimed calculus, not to the correctly conditioned product formula.

The straightforward repair is to retain `P(node = 1 | full latent word)` through
the tree. Independent subtrees then use the familiar product, complement, and
parity recurrences. To report a single output FPR/FNR, one must additionally
specify and average over the latent-word distribution conditioned on the ideal
output. This is already the ordinary forward-channel calculation. The tests
exhaust all **16 two-input Boolean truth tables and all four latent words**
against a directly constructed Kronecker assignment matrix.

Source reuse is separately audited: `b AND b` has error 0.02, while `b XOR b`
has error zero; treating the copies as independent would assign the XOR error
0.0392. The draft already excludes this at
[main.tex:292](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:292).
That caveat should be retained, but it does not fix latent-assignment coarsening.
Likewise the chain complement-of-product identity is exact for an “any stage
failed” event; it is not automatically a final-output error rate when errors
can cancel. Its explicit premise at
[main.tex:408](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:408)
must accompany applications such as feed-forward chains.

An additional scope correction is needed: diagonal **detector effects**, rather
than a diagonal **input density matrix**, justify a classical assignment model
for fixed-basis measurement statistics. If
`M_b = sum_t A(b|t) |t><t|`, then
`Tr(M_b rho) = sum_t A(b|t) rho_tt` for any rho, including coherent or entangled
states. This does not assert a joint hidden-variable model across incompatible
measurement settings. The manuscript's “precisely when the density matrix is
diagonal” language at
[main.tex:258](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:258)
and Bell/Kochen–Specker discussion at
[main.tex:1073](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:1073)
overrestrict the model. Tuziemski et al. (2023), Sec. I.0.2, explicitly formulate
the stochastic transformation of POVMs and the resulting outcome distributions.
[Primary text](https://arxiv.org/html/2311.10661v1).

## Independent reproduction and what it establishes

Both original scripts ran successfully. A separate audit uses exact rational
enumeration for small cases and a two-state recurrence for the 27-bit parity.
It does not call the original parity-product function to generate its answers.

| Quantity | Independent result |
|---|---:|
| Symmetric table, q=.01, n=2 / 4 / 8 | .0198 / .03881592 / .0746184887091072 |
| Symmetric table, q=.05, n=2 / 4 / 8 | .095 / .17195 / .284766395 |
| Asymmetric words 0000 / 1000 / 0011 / 1111 | .10997888 / .1749824 / .23384192 / .315168 |
| Symmetrized q=.07, n=4 | .22649592 |
| 27-qubit cold / hot | .25790697549809266 / .3687556485846237 |
| Cold linear relative overestimate at n=27 | 37.49143438837406% |

These reproduce Tables 1–2 and the headline calibration figure at
[main.tex:712](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:712),
[main.tex:769](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:769),
and [main.tex:840](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:840).
The original seeded Monte Carlo's largest reported deviation is 0.000953.

All **54 per-qubit rates** in `code/readout_figure.py:24` exactly match the
official JSON for IBM Hanoi, timestamp `2025-02-26T15:13:14-05:00`, at immutable
Qiskit commit `7a99d12423c21a34253342db5a3faf63ab0f8b6e`.
[Pinned calibration](https://raw.githubusercontent.com/Qiskit/qiskit-ibm-runtime/7a99d12423c21a34253342db5a3faf63ab0f8b6e/qiskit_ibm_runtime/fake_provider/backends/hanoi/props_hanoi.json).
The source hash and extraction fields are in
[calibration_provenance.json](evidence/calibration_provenance.json).

This establishes numerical correctness under the chosen model. Neither the
calibration snapshot nor sampling independent channels measures actual joint
parity errors, validates channel independence, identifies a code's detector
layout, or establishes an improvement over exact forward-channel methods.
The current artifact's “first n qubits” curve is an illustrative parity family.

## Only nearby salvage examined: pairwise crosstalk sensitivity

The exact central-moment identity at
[main.tex:609](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:609)
is correct: expand a product of centered variables. Its two-bit specialization is
exact, and the sign of its covariance coefficient is correct when the remaining
biases are positive. Calling the truncation “first order” requires a specified
dependence family whose higher central moments are of smaller asymptotic order.
The draft itself recognizes failure for a global shared cause.

Hamilton et al., *Scalable quantum processor noise characterization*, IEEE QCE
2020, pp. 430–440,
[DOI 10.1109/QCE49297.2020.00060](https://doi.org/10.1109/QCE49297.2020.00060),
already develops conditional readout cumulants and reconstruction from one- and
two-qubit data (Sec. II B–C, Eqs. (1)–(4)); it also flags missing higher-order
correlations in Sec. II D. Its full [primary PDF](https://arxiv.org/pdf/2006.01805)
was retrieved and those sections checked. My inference is that projecting this
established moment-cumulant construction onto parity provides the relevant
stronger baseline, rather than comparing only with independence.

The audit implements that baseline by summing **all partial matchings** of
pair covariances, with all cumulants of order greater than two set to zero.
This differs from the manuscript's retained terms, which allow at most one
covariance factor. It is an audit baseline, not a proposed new method or a claim
that every truncated reconstruction is a valid probability distribution.

| Eight-bit chain cause rate | Exact OR-cause model | Paper pair correction | Full pair-cumulant baseline |
|---:|---:|---:|---:|
| .001 | .06265481 | .06278302 | .06267619 |
| .005 | .06237295 | .06540001 | .06289621 |
| .010 | .06226359 | .07353453 | .06430056 |
| .020 | .06283003 | .10187350 | .07053225 |
| .050 | .07033318 | .22831460 | .11042320 |

These independently reproduce the manuscript's values at
[main.tex:935](/home/spinoza/github/bernoulli/papers/bernoulli-quantum-readout/main.tex:935).
The paper correction is 18.10% high already at lambda=.01 and 224.62% high
at .05. The stronger baseline reduces those errors but does not eliminate the
need for higher-order information. For the global-cause model at lambda=.005,
the exact probability is .06243894 and both truncations are negative
(-.13634820 and -.17396227).

A separate finite check shows why pair data cannot certify general parity error.
For three flips let `p_delta(f)` equal the independent Bernoulli(.1) probability
plus `delta * (-1)^parity(f)`. At delta=+/-0.0009 both distributions are valid,
have means (.1,.1,.1), and have every pair covariance exactly zero. Their parity
errors are **.2404 and .2476**. This is a diagnostic counterexample to a generic
pairwise sufficiency claim; the manuscript's exact expansion retains the missing
third moment and is not contradicted.

No physical data in the repository establish the proposed OR-chain mechanism or
the smaller-order remainder assumption. New general remainder bounds, a new
design benefit against known correlated-channel baselines, or empirical
validation would require additional research. None is established by this
salvage check. Contemporary correlated-readout work includes Maciejewski et al.
(Quantum 5, 464, 2021), Tuziemski et al. (arXiv:2311.10661), and Aasen et al.
(PRA 112, 022601, 2025); the reference registry distinguishes full-text from
abstract-only checks. This audit does not claim that any one of them states
the draft's particular scalar covariance formula verbatim.

## Remaining author effort and stop decision

| Work | Estimate | Outcome |
|---|---:|---|
| Correct conditioning, source reuse applications, and detector/state scope | 0.5–1.5 days | A sounder presentation of known calculations |
| Replace novelty claims; integrate direct prior art; update baseline comparisons | 1–1.5 days | Honest positioning, but no new contribution |
| Consolidate reproducibility and rewrite as a short explanatory manuscript | 0.5–1 day | A possible expository note |
| Establish a new result beyond those baselines | Not defensibly bounded by the remaining week | Research risk, not editorial work |

Approximately **2–4 author days** could repair and streamline the exposition.
That does not convert it into an original conventional research publication.
A new contribution would require open-ended work; estimating it as a one-week
finishing task would be misleading. Do not select this candidate, do not spend
time adapting another venue template, and do not initiate a hardware campaign.
No other nearby rescue was opened.

The decision is a bounded evidence judgment, not proof that no future result is
possible. The strongest general baseline has an explicitly recorded full-text
access limitation; the independently reproduced conditioning failure, the
full-text readout/cumulant sources, and the numerical comparison are sufficient
to reject the current contribution and the tested salvage under the effort cap.

## Reproduction files and checks

- [audit.py](audit.py): exact enumerator, independent parity recurrence,
  conditioning checks, structured calibration extraction, shared-cause laws,
  and covariance/cumulant comparisons.
- [test_audit.py](test_audit.py): 17 passing tests, including property tests,
  exhaustive Boolean functions, boundary probabilities, shared source identities,
  arbitrary dependent distributions, and integration with canonical code.
- [results.json](results.json): machine-readable independent results.
- [validation.txt](validation.txt), [coverage.json](coverage.json): pytest and
  coverage evidence. Test coverage is 99%; the uncovered line invokes `main`
  under `__name__ == '__main__'`, which the separate script run exercises.
- [validation.md](validation.md): exact commands, versions, successful checks,
  and checks deliberately not run because canonical files were unchanged.
- [references.json](references.json): verified metadata, URLs, locators, access
  limits, and the claims for which each source was used.
- [search-log.md](search-log.md): bounded search scope and stopping rationale.
