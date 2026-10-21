# Codec/privacy candidate audit

Date: 2026-10-14. Independently reviewed decision: **no-go for a new conventional paper
within one working week**. This is not a claim that all retrieval privacy
questions are settled. The strongest nearby existing manuscript is considered
below as part of this same candidate.

## Precise contribution hypothesis

Choose a finite value codec for a static approximate map to reduce membership
inference across independent releases, with an optimal attacker analysis and a
measured storage cost. The possible increment over DTEs would have to come from
the actual retrieval construction or a useful constrained optimization result,
not from decoding uniform bits into a chosen distribution.

Starting evidence: `bernoulli-py/experiments/{07,11,12,13,14,15,16}_*.py`, their
reports, `SYNTHESIS.md`, and `src/bernoulli/maps/{codec,retrieval}.py`. Companion:
`../trapdoor-computing/papers/codec-controlled-retrieval/`. Its submission ledger
is incorrect according to the author's explicit correction in this session;
submission status is **not** a reason to reject this candidate.

## Exact result and decisive optimal-attacker counterexample

Fix a public codec, membership prior pi, member value law p, and non-member
decoded law q. Assume the member value is unchanged across t releases and
non-member responses are independent across those releases. The observation
laws are P(v,...,v)=p_v and Q(y_1,...,y_t)=product_i q_(y_i).

The equality classifier predicts membership on the diagonal. Its accuracy is

    A_equal = 1 - (1-pi) sum_v q_v^t.

The unrestricted Bayes classifier instead has exact accuracy

    A_Bayes = 1 - sum_v min(pi p_v, (1-pi) q_v^t).

Proof: at each observation choose the larger prior-weighted mass. Member mass
is zero off the diagonal; summing the smaller masses gives the Bayes error.
Equality is optimal exactly when pi p_v >= (1-pi) q_v^t for every v (ties allowed).
This is elementary binary hypothesis testing, not a new theorem for publication.

At pi=1/2, p=(.99,.01), q=(.5,.5), t=2, equality accuracy is .75 while Bayes
accuracy is .87. `test_exact_audit.py` enumerates all 16 classifiers on the four
observations to verify this independently. It also checks the formulas against
complete observation laws for 3,000 finite parameter combinations: alphabets
2/3, probability vectors with denominator 4, t=1..4, and three priors.

For t>1 uniform q minimizes sum q^t and therefore **maximizes** the equality
attacker's accuracy. `RESULTS_14.md` and experiment 14 already correct the sign;
`SYNTHESIS.md` still reverses it. Experiment 14's own AntiHuffman t=2 result
already exhibits a gap from the estimated Bayes accuracy. Do not claim either
repair as new research. Concentrating q is not a universal optimal defense
against the Bayes classifier for arbitrary p.

## Threat model and stored representation

Experiments 14/15 store exact keys and a key-to-slot dictionary, then generate
a fresh uniform raw value on each absent lookup. This implements the stated
ideal value channel for one observation per independent release. It is not a
static keyless representation and does not model repeated calls to one frozen
filter. Exposing that dictionary also reveals membership directly.

Actual `GF2Retrieval` stores a fixed table and public seed. Repeating one query
returns the same result. The audit reproduces this difference with the same
absent key in 32 calls to each implementation. A decoded public-codec attacker
is unaffected by randomizing representatives within a decode class. For a
private codec, an equality-of-raw-patterns statistic is only one restricted
attacker; improved performance against it does not establish optimal privacy.

Even uniform random free variables would give a uniform query output only when
the query coefficient is outside the stored-row span. A row in that span is
forced by the stored values. The real implementation supplies a concrete
conditional example: for seed 2026, member `stored` and non-member `absent-615`
both address slots (5,16,28), so both return 5. The absent key was selected after
observing the seed. This refutes an unqualified adaptive/conditional uniformity
claim; it does **not** measure average FPR for an independently fixed query.
The implementation's deterministic public PRNG initialization is also not a
proof of ideal uniform free randomness.

One further implementation limitation: with PrefixCodec lengths (1,3), M=3,
the default decodes seven raw patterns, but `encode_random` reaches only the
four patterns in its explicit prefix cylinder. With Kraft slack it does not
sample the entire decode fiber. Full-class randomization claims require this
distinction. No package source was modified by this audit.

## Reproduction of the headline storage/privacy example

The heavy-8/M=6 example reproduces exactly for p=(.9,1/70,...,1/70):

| Codec | Expected prefix length | TV(p,q), uniform raw channel | Stored slot width | Packed payload estimate | Actual pickle v5 bytes |
|---|---:|---:|---:|---:|---:|
| Huffman | 9/7 | 2/5 | 6 bits | 671 | 2161 |
| Lengths (1,6,...,6) | 3/2 | 3/320 | 6 bits | 671 | 2161 |

Both actual retrievals store 700 keys in 894 fixed-width slots and retrieve
every member correctly. Pickle includes the codec and table; it is a Python
serialization measurement, not an optimized packed format or resident-memory
estimate. The package's `memory_bytes()` is a packed-payload estimate excluding
metadata. Expected prefix length rises 16.7%, but **neither measured stored
representation grows**. Thus the claimed L–TV frontier is not an implemented
storage–privacy frontier. The reduction in TV under the ideal channel is real;
Huffman's source-compression objective simply differs from distribution matching.

A direct DTE-style allocation of the 64 raw patterns gives 57 patterns to the
head and one to each tail, exactly the second codec's law. It is already optimal
in TV among *all* total 6-bit decoders with eight nonempty fibers: each tail
must receive at least 1/64, so the head receives at most 57/64 and its deficit
is at least 3/320. This elementary integer-allocation argument supplies a
competent distribution-shaping baseline without the experiment's truncated
length-tuple search. It does not establish a new prefix-code algorithm.

## Strongest nearby alternative: the existing span manuscript

The companion already separates abstract DTE distribution shaping from its
proposed contribution: zero-filled linear retrieval has solution-row space W
equal to the span of stored codewords. Under **M1, uniform output on W**, the
decoded law is |decode-fiber intersect W|/|W|. For balanced linear codecs it is
uniform on the projection image, and equals the full codec law iff that image
has full rank. The audit reproduces this for all 67 subspaces of GF(2)^4 and
all four prefix projections (268 cases).

The independent reviewer also examined the stronger remaining bundle: skewed
prefix-flag laws, realizability via nested projections, per-rung cogirth, and
full-support randomized-encoding invariance. The last statement has a short
proof for complete codes: every class is hit; its mass under uniform-on-span
M1 is 2^(-rank pi_l(W)) >= 2^-l; both the masses and Kraft-tight shares sum to
one, forcing equality in every coordinate. This holds for every choice of
one representative per class, so additional repetitions cannot spoil it.
The companion's existing finite verification reproduces all 712 representative
choices across eight complete codes and its saturation counterexample (16 of
32 redraws change the law). See `companion-full-support.txt`.

These refinements are useful synthesis. The realizability statement describes
the same subspace image via prefix projections; the cogirth statement transports
its minimum deletion definition through the rank condition. No identical
published bundle was established by this bounded search, but neither a
nontrivial theoretical advance nor a demonstrated application benefit is yet
established. This rejects a quick publication commitment, not the possibility
of a future mathematical contribution or an expository note.

The counting statement is correct under M1 and follows directly from equal
fibers of a linear map. This audit has not found an identical published
retrieval-codec statement; that limited application-specific novelty remains
possible. It does not establish a new practically valid privacy guarantee:

- M1 assumes the distribution the proposed construction needs to justify.
  The manuscript explicitly says that nonzero pinned band vectors do not have
  the equal-fiber property. The real deviation is measured, not bounded.
- At `paper/codec_retrieval.tex:1804`, the related-work comparison nevertheless
  says it proves near-uniformity. That conflicts with the explicit M1 scope.
- M1 as stated specifies one-query marginals. Frozen oracles with transcripts
  (U,U) versus (U,1-U), U uniform, have the same marginals but disjoint two-query
  laws. The audit verifies Bayes accuracy 1. This is a logical countermodel to
  the implication from marginals to adaptive privacy, not a demonstrated attack
  on the particular C++ builder. Defining a joint iid ideal oracle repairs that
  ideal theorem but does not justify the frozen real oracle.
- The manuscript's real single-observation TV triangle bound is valid. Similar
  average cross-profile and same-profile distances do not establish equal
  distributions of complete transcripts or of realized per-build laws.
- The output-support proof still concludes that **non-members** span W after
  exhibiting member witnesses. That implication needs a further condition on
  non-member coefficients. Containment and the solution-row-space identity
  have the stated algebraic proof; the stronger reachable-span claim does not.
- The cogirth robustness statement transports the definition of cogirth through
  the ideal rank criterion. This may be useful exposition; no demonstrated
  application advantage or new nonuniform-band guarantee currently separates it
  from the standard algebra.
- The skewed-prefix theorem needs complete codes or a separate treatment of
  surplus. For lengths (1,3), M=3 and full W, the default's true mass is 7/8,
  not the 1/2 of its prefix cylinder. The randomized-full-support theorem
  explicitly requires completeness and survives this correction.
- E1's subthreshold TV value does not verify uniformity on the hit classes.
  With K=4, both (.5,.5,0,0) and (.49,.51,0,0) have TV .5 from global uniform.
  Zero-width TV bars therefore cannot establish a deterministic per-class
  law. The support obstruction survives; the proposed empirical confirmation
  of the stronger law is non-identifying.

The natural competent baseline is random free-slot filling with a row-span
exception, already analyzed for homogeneous ribbon filters. It must not be
presented as a newly discovered finite-construction theorem. The existing
Python implementation already uses a version of that engineering choice.

## Closest primary literature (checked 2026-10-14)

- Juels and Ristenpart, **Honey Encryption: Security Beyond the Brute-Force
  Bound**, EUROCRYPT 2014, Section 4. Randomized encoding and deterministic
  decoding shape the law of uniform seeds. This subsumes the abstract
  distribution-shaping mechanism, not the whole retrieval security problem.
  [Author PDF](https://pages.cs.wisc.edu/~rist/papers/HoneyEncryptionpre.pdf).
- Cheng et al., **Probability Model Transforming Encoders Against Encoding
  Attacks**, USENIX Security 2019. Encoding artifacts can distinguish decoys
  even without message-distribution statistics; addresses limitations of a
  marginal-only attack evaluation.
  [Official paper page](https://www.usenix.org/conference/usenixsecurity19/presentation/cheng).
- Filić et al., **Adversarial Correctness and Privacy for Probabilistic Data
  Structures**, CCS 2022. Simulation-based AMQ privacy models distinguish API
  access and internal-state exposure. It studies membership structures, not
  the identical retrieval-value problem; a necessary threat-model comparison.
  [Author preprint](https://arxiv.org/abs/2209.06955).
- Bienstock, Patel, Seo and Yeo, **Near-Optimal Oblivious Key-Value Stores for
  Efficient PSI, PSU and Volume-Hiding Multi-Maps**, USENIX Security 2023,
  Section 2.1 Definition 4. Random decoding of non-input keys is an explicit
  studied property. Its uniformly random input-value assumption means it does
  not subsume this manuscript's nonuniform zero-filled value-span problem.
  It nevertheless refutes the broad claim that such off-set laws are entirely
  absent from prior retrieval/privacy research.
  [Official paper](https://www.usenix.org/system/files/usenixsecurity23-bienstock.pdf).
- Dietzfelbinger et al., **Ribbon: Fast Succinct Static Retrieval and Approximate
  Membership**, JACM 73(1), Article 7, 2026, DOI 10.1145/3785417. Section 5.4,
  Lemma 5.4 gives p+(1-p)2^-r with p the stored-row-span event, using uniform
  free variables. This is a construction-specific prior for the natural
  baseline, not the companion's zero-filled value-span identity. Section 1.7
  also describes prefix coding into one-bit retrieval for actual compression.
  [Institution-hosted publisher PDF](https://publikationen.bibliothek.kit.edu/1000191446/177619178).
- Böcherer and Mathar, **Matching Dyadic Distributions to Channels**, DCC 2011
  preprint. Optimizes a KL objective over dyadic laws using geometric Huffman
  coding. Related distribution-matching precedent, **not** proof that the
  project's TV-constrained optimization has an identical published solution.
  [Author preprint](https://arxiv.org/abs/1009.3751).
- Cheng et al., **Practically Secure Honey Password Vaults: New Design and New
  Evaluation against Online Guessing**, USENIX Security 2025. A recent adjacent
  example where operational attack success changes conclusions from
  distinguishability evaluation; different application, not a direct theorem
  predecessor. [Official page](https://www.usenix.org/conference/usenixsecurity25/presentation/cheng-haibo).

## Effort and decision

Correct the stale experiment synthesis and state the exact ideal classifier:
roughly 0.5–1 author day. Align storage and threat-model claims, separate the
companion's ideal and real claims: another 1–2 days. These are repairs and
repositioning, not an established original paper.

A new defensible contribution would additionally need a nontrivial theoretical
advance, a real-construction guarantee, or a validated practical application beyond distribution shaping,
with a credible comparison to random free-slot filling and an explicit joint
security model. Its feasibility is unproven; **there is no evidence that this
can be completed within the one-week ceiling**. An empirical-only route would
need a concrete workload and operational attacker evaluation, not another
codec sweep. Do not start that new program for this side-project goal.

Result: retain the exact counterexamples and the conditional span identity as
research assets, but do not prepare another submission draft from these claims.
Independent review specifically challenged the theory-note route and examined
the graded and full-support results as well as the headline balanced case.
Its conclusion agrees with this bounded no-go; it does not establish that all
these statements have already been published or that no paper is possible.
