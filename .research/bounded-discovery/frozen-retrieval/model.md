# Frozen retrieval: two-round probe

## Round 1 — is there a new joint-transcript result?

The ideal construction samples a fixed slot array Z uniformly from AZ=v over
GF(2), independently for each value bit. A is fixed and consistent; it contains
the public slot-incidence rows of stored keys. Fixed queries give rows B and
observe BZ. The same key is never resampled. Queries chosen after the public
hash seed are conditional queries, not independent fixed-key FPR experiments.

The output lies uniformly in the affine image Bz0+B ker(A). Its dimension is
rank([A;B])-rank(A). The amount of constraint introduced by A, relative to the
public image of B alone, is rank(B)+rank(A)-rank([A;B]). These are different
from an assumption of one independent output per query occurrence.

Probe: enumerate small slot arrays and compare their complete transcript laws
to the rank formula. Use a three-query relation with one slot in each of three
segments; reproduce the XOR relation using absent keys in actual GF2Retrieval.
Separate a general algebraic result from a meaningful security consequence.

The existing implementation initializes free slots deterministically from a
public seed. It does not sample an ideal uniform affine solution. Exact uniform
claims will be proved/tested only for the explicit ideal experiment; the real
implementation supplies a deterministic relation, not a uniformity proof.

## Round 2 — does a useful attack or mitigation remain? (initial selection rule)

An attacker may know hash positions and compare two candidate stored sets, but
must not be granted the hidden stored keys or values merely by the experiment.
A nonmember-only transcript counterexample is a conditional diagnostic, not
automatically a practical attack against an unrestricted API or published OKVS.

Compare (a) uniform free slots, (b) uniform stored words, and (c) standard secret
per-key masking of stored words and query outputs. With independent ideal pads,
the masked stored words are uniform; distinct absent-key pads remain independent
of the whole stored representation. Query reuse reuses the same pad. In the
implementation probe, HMAC-SHA256 is a conventional pseudorandom-function
instantiation, not an information-theoretic proof. The service keeps its mask
key private; exposing that key is outside this mitigation's assumption.

Count payload, public seed/metadata, trusted key bytes, construction and query
costs. Do not count a standard mask wrapper or a rank-nullity identity as new
research. A current application-specific claim must survive its actual threat
model before an attack is attributed to it.

## Artifact and validation plan

- `joint_probe.py`: typed finite system, independent enumeration and GF(2)
  ranks, exact transcript distances, stored-query relation, mask baseline.
- `test_joint_probe.py`: exhaustive finite laws, repeated/dependent rows,
  equal marginals/different joint laws, real retrieval and mask round trips.
- `run_probe.py`: reproducible exact results and descriptive implementation
  cost measurements, with source/seed provenance in `results.json`.
- `literature.md` and `references.json`: independent primary-source audit.

All new code is an isolated experiment. Existing package and manuscript inputs
remain unchanged. A finalist requires an increment beyond these expected
elementary results; failing that gate ends this candidate after round 2.

## Resolved second round and bounded pivot

The generic affine law was located explicitly in Silva–Kschischang (2011),
Lemma 6 and its proof. A general PRF wrapper therefore did not warrant an
implementation/performance project. The standard OKVR mask baseline is cited,
and tiny independent-pad checks test the particular statistic instead.

The same second round found a concrete public-view claim in GBFPlus (2026).
Its public payload format is an identity encoding of a truncated prefix and
registered domain ID; the domain-code association is public. Its positions
and query secrets are private. Unlike a freshly randomized response oracle,
the ledger exposes one frozen stored share array with genuine occupancy bits.
An observer needs no query or token and sees count, configuration, occupancy,
and payload. Construction randomness is conditioned on the chosen legal
support; the XOR identity holds for every remaining random choice. A known
public domain registry is the only auxiliary knowledge needed to name the
recovered endpoint.

Finalist: public occupancy reveals the complete singleton share set, so its
XOR discloses the domain suffix. More generally w=c*kappa certifies disjoint
supports and gives the aggregate suffix XOR. The honest-history and authentic
count assumptions are explicit. The source's timeout finalization permits a
singleton; this is a source premise, not a simulated implementation of its
ledger or scheduler. Repeated reads are identical. Multiple independent
reconstructions, adaptive queries, and full transfer-path recovery are not
needed or claimed.

Actual delivered modules supersede the tentative artifact list above:
`joint_probe.py` gives finite affine laws; `stored_probe.py` records the
conditional three-query relation using existing GF2Retrieval; `gbfplus_probe.py`
implements the share update and public-only statistic; `run_probe.py` writes
the reproducible results. Generic masking performance work was deliberately
not pursued. This is the completion of round 2, not a third investigation.
