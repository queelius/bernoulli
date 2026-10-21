# Claim–evidence ledger

Audit date: 2026-10-14. Status: complete; no candidate selected.
Assertions of novelty are hypotheses. Exact finite checks verify the indicated
cases; they do not replace general proofs or establish novelty.

| ID | Claim or contribution hypothesis | Evidence | Disposition |
|---|---|---|---|
| C1 | A codec can shape uniform raw outputs into a desired finite law | DTE predecessor; explicit 64-pattern decoder enumeration | Established mechanism; no novelty claimed |
| C2 | Coincidence is always the optimal attacker across releases | p=(.99,.01), q=(.5,.5), t=2: .75 equality vs .87 exact optimal accuracy; all 16 decision rules enumerated | Refuted without the diagonal likelihood-ratio condition |
| C3 | Uniform codecs best resist the coincidence attacker | A=1-(1-pi)sum(q^t); uniform minimizes the collision sum for t>1 | Sign reversed in stale SYNTHESIS.md; experiment 14 already repairs it |
| C4 | Heavy-tail codec example demonstrates a 16.7% storage cost for 42-fold TV reduction | Both actual 700-key retrievals: 894 six-bit slots, 671 packed-payload bytes, 2161 pickle-v5 bytes including codec | TV reduction reproduced; expected prefix length is not the current stored cost |
| C5 | Fresh simulated absent answers describe repeated queries to a stored map | 32 repeated calls: fresh simulator varies, actual frozen retrieval repeats one answer | Different experiments; independence must be assigned to releases or distinct random sources |
| C6 | Random representative encoding samples every full decode fiber | Default length-1 prefix with Kraft slack: 4 reachable encodings vs 7 decoding patterns | False for current PrefixCodec with surplus; limited correctness repair |
| C7 | Actual non-member outputs are always uniform conditional on a public build | Distinct key `absent-615` shares all three positions with `stored` under seed 2026 | Refuted for adaptively chosen aliases; does not refute average fixed-query guarantees |
| C8 | Balanced codec control under uniform-on-span M1 is equivalent to full projected rank | Equal-fiber proof; all 67 subspaces of GF(2)^4, 268 projection cases | Correct conditional result; application-specific novelty not ruled out, usefulness beyond the assumption unestablished |
| C9 | Identical one-query laws imply unbounded adaptive privacy | Frozen transcripts (U,U) and (U,1-U) have identical marginals and disjoint joint supports | Invalid implication; iid ideal oracle is an additional model, not a property established for the real builder |
| C10 | Random-free-slot row-span exception supplies a new finite-construction guarantee | JACM 2026 Ribbon, Section 5.4 Lemma 5.4 | Already published baseline; distinct from zero-filled value-span theorem |
| C11 | Companion codec manuscript is submitted to TOPS | Local ledger claims this, author explicitly says record is incorrect | Author correction controls; no submission/exclusivity premise in the decision |
| C12 | E1's subthreshold TV confirms uniformity on the reachable classes | (.5,.5,0,0) and (.49,.51,0,0) both have TV .5 from uniform | Non-identifying statistic; exact support obstruction survives |
| C13 | Full-support randomized encoding preserves a complete prefix codec's M1 law | Each hit mass >= Kraft share, totals both 1; 712 finite representative choices reproduced | Correct short corollary; no demonstrated nontrivial theory increment |
| C14 | Graded single-prefix formulas cover default codecs with Kraft slack | Default fiber mass 7/8 vs cylinder share 1/2 for lengths (1,3), M=3 | Restrict to complete codes or handle a union of cylinders |
| C15 | Non-input decoding distributions are entirely unstudied in retrieval privacy | Bienstock et al. 2023 Definition 4 explicitly requires random non-input decoding under uniform input values | Broad novelty claim false; different value assumptions prevent a full equivalence claim |

Codec evidence: [assessment](candidates/codec-privacy/assessment.md),
[exact outputs](candidates/codec-privacy/results.json),
[primary references](candidates/codec-privacy/references.json).

| ID | Claim or contribution hypothesis | Evidence | Disposition |
|---|---|---|---|
| Q1 | A new asymmetric symbolic forward Boolean calculus | PTM 2008 scope, asymmetric response-matrix literature and exhaustive truth-table checks | Established method specialized to readout; full PTM PDF access limitation recorded |
| Q2 | Two output-conditioned rates suffice for arbitrary read-once composition | AND truth 00 vs 01 has FP .0004 vs .018; a three-input tree gives .03764 vs .020392 under the corner-pair substitution | Coarsening requires a latent-input distribution; corner formulas do not close |
| Q3 | Hanoi numerical examples reproduce from genuine calibration data | All 54 rates match pinned official JSON; independent recurrence reproduces tables | Verified model calculation, not joint hardware validation |
| Q4 | Pairwise crosstalk term gives a new validated method | At lambda=.01 exact .06226, paper .07353, established cumulant-derived baseline .06430 | Closest salvage lacks incremental evidence; higher moments remain material |

Readout evidence: [assessment](candidates/quantum-readout/assessment.md),
[results](candidates/quantum-readout/results.json),
[primary references](candidates/quantum-readout/references.json).

| ID | Claim or contribution hypothesis | Evidence | Disposition |
|---|---|---|---|
| H1 | Adaptive threshold removes seed storage at equal useful membership accuracy | For m=N=100, rank 1 has mean recall .0158122 and FPR .0157211; rank 100 has recall 1 and FPR .994279 | Comparison changes recall/FPR requirements; saving is not solely a price of certainty |
| H2 | Printed finite threshold law is exact for iid hash residues | N=m=2, rank 1: exact (3/4,1/4), printed (1,0); 40 finite cases enumerated | Without-replacement assumption is incompatible with iid hashes; correction is standard order statistics |
| H3 | Same-recall capped threshold or best-of-budget search supplies a new method | Threshold acceptance and fixed-threshold count are the same event; success probability is a binomial tail | Familiar random-codebook search; ESA 2025 UNI is the direct seed-mechanism baseline |
| H4 | Random realized FPR permits ignoring ordinary randomized-AMQ requirements | A fixed absent key's marginal acceptance is the expectation of the realized FPR; covariance of two absent indicators is Var(FPR) | Random-rate mixtures need correct semantics; no novel lower-bound escape |
| H5 | Printed geometric entropy and log moments establish sharp storage identities | At success 1/2, entropy is 2, E log2 Q≈.732649, E floor(log2 Q)≈.632843 | Exact-moment/sign repairs preserve only the standard leading seed-index scale |
| H6 | PHF occupancy loss formula remains valid after capacity rejection and equals membership FN | m=N=2: cap1 accepted placements have FN0 vs printed1/4; cap2 and one-bit fingerprints give FN1/8 | Conditioning and accidental fingerprint matches require corrections; no new construction advantage |

Hash evidence: [assessment](candidates/hash-construction/assessment.md),
[results](candidates/hash-construction/results.json),
[primary references](candidates/hash-construction/references.json).
