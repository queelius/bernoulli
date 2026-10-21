# Frozen retrieval: focused primary-literature audit

Checked 2026-10-14. Scope: candidate 2 only, two investigation rounds. Preserve
the earlier [codec audit](../../publication-triage/candidates/codec-privacy/assessment.md):
neither ideal marginal distribution shaping nor the elementary affine-span law
is a new publication contribution. No external contact or publication occurred.

## Round 1: the generic joint theorem is established

Let `A Z = v` and sample `Z` uniformly from the feasible affine space. For fixed
query rows `B`, `BZ` is uniform on `Bz0 + B ker(A)`. The relevant dimension is
`rank([A; B]) - rank(A)`; under a uniform feasible secret `v`, information
revealed is `rank(A) + rank(B) - rank([A; B])` field symbols. A single row can be
uniform while several rows reveal a linear constraint. These are exact linear
algebra facts, not novel research.

The decisive published predecessor is Silva and Kschischang, **Universal Secure
Network Coding via Rank-Metric Codes**, IEEE TIT 57(2), 2011, Lemma 6 and its
appendix proof. It explicitly gives the rank-deficit upper bound for uniform
coset encoding and the matching lower bound for uniform secret messages. Its
proof constructs matching linear combinations of observed and secret rows.
Theorem 7 supplies a much stronger universal masking design using rank-metric
codes. [Primary preprint](https://arxiv.org/pdf/0809.3546).

Ozarow–Wyner wiretap-II and Wei's generalized Hamming weights are earlier
coordinate-observation precursors. Their metadata/abstracts were checked; this
audit relies on the full Silva–Kschischang proof, rather than asserting that
unread earlier theorems have an identical statement.

Retrieval-specific baselines also predate this audit:

- Bienstock et al. 2023, Definitions 3–4 and Algorithm 1, explicitly assume
  uniformly random stored values for double obliviousness/random decoding.
  Random free-variable filling with those values makes the whole encoding
  uniform. A correlated/nonuniform-value example is not a break of that model.
  [Official PDF](https://www.usenix.org/system/files/usenixsecurity23-bienstock.pdf).
- Ribbon 2026, Section 5.4, Lemma 5.4, already isolates the stored-row-span
  exception to uniform nonmember response for homogeneous filters. This is a
  one-query correctness result, not a joint privacy theorem.
  [Publisher PDF in institutional repository](https://publikationen.bibliothek.kit.edu/1000191446/177619178).
- Hao et al. 2024, Section 4/Figure 5, supports arbitrary values using an OKVS
  on pairs `v_i + F(k,k_i)`, with OPRF outputs and PIR enabling authorized
  demasking. Per-key masking is an established baseline, not a new mitigation.
  [Official PDF](https://www.usenix.org/system/files/usenixsecurity24-hao-meng-unbalanced.pdf).
- Filić et al. 2022, Section 5, analyzes whole interaction/state privacy through
  simulation-based definitions. Its object is AMQ, not arbitrary retrieval,
  but it rules out framing marginal uniformity as a sufficient modern privacy
  definition. [Primary full text](https://arxiv.org/html/2209.06955).

Honey encryption/DTEs remain the inherited predecessor for decoding random
seeds into a desired marginal. They do not by themselves furnish a joint
privacy theorem for a frozen retrieval table. No new DTE optimization is being
claimed in this screen.

## Round 2: a specific 2026 application has a testable content leak

Qin et al., **Privacy-Preserving On-Chain Attestation for Cross-Domain Data Flows
via GBFPlus**, Entropy 28(9):947, published 2026-08-23, uses XOR shares with a
public occupancy bitmap. The actual publisher PDF and XML were downloaded and
preserved, rather than relying only on search excerpts. See
[PDF](evidence/gbfplus-2026.pdf), [XML](evidence/gbfplus-2026.xml),
[layout text](evidence/gbfplus-2026-layout.txt), and
[hash manifest](evidence/source-manifest.json).

The following source premises are explicit:

| Premise | Source locator | Consequence |
|---|---|---|
| Adjacent-domain relationships are intended to remain concealed from ordinary observers. | Section 4.2, printed p. 7; Table 1, p. 4 also calls the adjacent domain protected. | Payload confidentiality is a stated goal, separate from identifier confidentiality. |
| The adversary can inspect committed ledger transactions. | Section 4.3, p. 7. | Full public transaction contents are a legitimate observation. |
| Time-window expiration finalizes the current filter. | Section 5.2, p. 10. | A partially filled filter, including one successful insertion, is admissible. No minimum batch is stated. |
| The signed message includes successful count `c`; the ledger transaction includes the full finalized filter. | Equation (5) and following paragraph, p. 11. | The observer sees `c`, occupancy, and all occupied payload words. |
| Each entry has `kappa` distinct positions. Payload target is `Trunc(H_pay(u)) || N_adj`. | Algorithm 4, lines 2–4 and 11–21, p. 11. | The adjacent ID is an unmasked suffix of the XOR of that entry's shares. |
| Registered adjacent-domain IDs and their associations are public. | Setup, Section 5.1, printed p. 9. | Recovering a suffix identifies its domain; it is not an unlabeled opaque number. |
| The prototype uses `kappa=12`, `lambda=32`, `l_DA=20`. | Section 6.3, p. 19. | The issue is not restricted to the degenerate `kappa=1` case. |

There is no outer encryption of filter payloads in the described ledger
transaction. Paillier encryption appears in registration, not as protection of
the finalized GBFPlus table. The regulator is trusted and controls query
authorization, but neither its secrets nor a query token are needed to read
public cell contents. Each directional filter is finalized and committed by
its domain administrator; the text does not distribute its cells among
noncolluding servers or provide only a hidden subset to the observer.

**Exact application-specific observation.** Let `O` be the occupied set, let
`w=|O|`, and let `c` be the successful insertion count. Every successful row has
`kappa` distinct positions. If `w=c*kappa`, its rows must be pairwise disjoint.
Therefore the XOR of all occupied payload suffixes equals the XOR of the `c`
stored adjacent-domain IDs. In particular, `c=1` reveals the adjacent-domain
ID exactly. For `kappa>=2`, the individual shares in that singleton are uniform
while their complete XOR is fixed by the payload. This uses joint information
and holds for every honest choice of random shares and every legal hidden
index set. It does not depend on approximate uniform-subset modeling.

This is a deterministic claim about the published algorithm. Root's separate
experiment and independent review must establish implementation reproduction
and the final publication decision. The mathematical identity is elementary;
the potential increment is identifying an overlooked confidentiality failure
in a recent concrete protocol under its stated deployment conditions.

### Scope of the security statement

The formal `G_qpriv` game (Section 4.3, p. 8) selects two **identifiers** with
equal public metadata, rather than explicitly selecting two secret payloads or
adjacent-domain histories. Theorem 4 (Section 6.1.4, pp. 17–18) addresses that
game and fresh blinding. Do **not** call the singleton observation a proven
break of the same-recipient identifier game: if both worlds have the same
adjacent ID, recovering that ID does not identify the selected identifier.
Nor does recovery of one adjacent endpoint automatically identify the anonymous
uploader or reconstruct a full path.

A defensible narrow claim is that the specified public view does not hide its
adjacent-domain payload, contrary to the broader design goal and Table 1. A
binary adjacent-payload game with the same public occupancy/configuration/count
and different allowed IDs is distinguished perfectly. That additional game
must be labeled as the audit's formalization of the stated goal, not quoted
as the paper's own game. Public filter digests/signatures are part of the view;
they must not be required to be literally equal when defining equal public
metadata, since they commit to the differing table contents.

Section 6.1.4's Equation (27) uses a random-share argument for arbitrary
occupied `kappa`-tuples passing payload tests. This cannot imply confidentiality
of the suffix: an observer need not validate or guess the hidden random prefix
to recover an unmasked suffix on a publicly identifiable complete row. A
revised argument must separate accidental acceptance of guessed query tokens
from payload leakage. Avoid claiming that merely seeing the target prefix
forges a valid authorization token.

### Competent countermeasures and prior art

Dong, Chen, and Wen's original CCS 2013 GBF construction, Algorithm 1 lines
22–26 (printed p. 792), fills every remaining empty position with fresh random
strings. Its PSI protocol uses OT; it does not give an unauthorized receiver
every server share together with the original occupancy selector. This is the
relevant contrast, not evidence that plain GBFs automatically encrypt arbitrary
values. [Author PDF](https://changyudong.site/assets/pdf/ccs13.pdf).

Filling unused payload cells while continuing to reveal the original occupancy
bits does **not** stop the attack: it selects the original occupied cells.
Hiding occupancy removes this particular selector but is not by itself a full
privacy proof. Independently masking each payload suffix prevents the
single-instance suffix recovery, but is standard cryptographic randomization.
A pad reused for the same key across releases can expose changes through XOR;
a countermeasure needs explicit instance/domain separation and a separate
multi-release argument. No complete repaired GBFPlus protocol is proved here.

The paper's prototype also uses double-hash arithmetic-progression supports
(Equation (28), p. 19). Their enumeration is an established attack technique:
Niedermeyer et al. 2014, Section 4.2, enumerates all pairs of secret hash outputs
to recover candidate supports despite unknown cryptographic keys. It is not a
new algorithm to propose here. The stronger full-batch enumeration route was
identified but deliberately left unimplemented to keep this second round
bounded. [Primary institutional PDF](https://openaccess.city.ac.uk/id/eprint/14304/7/Niedermeyer_2014_Cryptanalysis_Of_Basic_Bloom_Filters_Used_For_Privacy_Preserving_Record_Linkage_2.pdf).

### Correction search and decision boundary

Exact title/DOI/GBFPlus searches with `correction`, `comment`, `critique`, and
`vulnerability` did not identify an existing discussion of this occupancy leak
as of 2026-10-14. The retrieved Crossref record has empty `relation` and no
`update-to`/`updated-by`; the publisher XML has no related correction article.
These are bounded negative search results, not proof that the observation has
never been made. The ordinary publisher HTML endpoint returned 403, while
the official `mdpi-res.com` PDF/XML succeeded; source access is therefore
complete for the audited version, with the saved hashes recording its bytes.

The generic affine theorem is a no-go for novelty. The specific GBFPlus
confidentiality counterexample is a plausible **focused comment** candidate,
conditional on independent scrutiny of claim scope and venue suitability. It
does not warrant a broad new security framework or another parameter sweep.
