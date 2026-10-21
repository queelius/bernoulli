# Published premises used by the Comment

Qin, S.; Zhou, Y.; Dai, W.; Sun, Y.; Qiang, W. *Privacy-Preserving On-Chain
Attestation for Cross-Domain Data Flows via GBFPlus*. Entropy **2026**, 28, 947.
[DOI 10.3390/e28090947](https://doi.org/10.3390/e28090947).

| Location | Premise | Why needed |
|---|---|---|
| Table 1, Section 4.2, and Section 6.2 (p. 18) | Adjacent domains are protected metadata; Section 6.2 describes recovery of the adjacent-domain identifier after prefix and assigned-domain checks. | Identifies the specific controlled-recovery claim challenged. |
| Sections 4.1–4.3 | The ledger is permissioned; ordinary observers with ledger access can inspect transactions. | Defines visibility and the observer's access, without assuming an unrestricted public blockchain. |
| Section 5.1, Equation (3) | Public parameters include the number of cells, share count, word width, and domain-identifier width. | The observer knows kappa and suffix width; these are not secret decoding inputs. |
| Section 5.1 | Registered domain IDs and their associations are public. | Turns the recovered suffix into a domain identity. |
| Algorithm 4 | Each successful insertion enforces an XOR target comprising a secret-derived prefix and an unmasked adjacent-domain suffix at distinct positions. | Establishes the algebraic invariant. |
| Section 5.2, including the transaction after Eq. (5) | The finalized filter and successful count are public; timeout finalization has no specified positive minimum batch size. | Admits a public singleton. |
| Section 6.2 | Occupancy is represented publicly, with sparse payload storage. | Identifies the complete singleton share set, including any zero word. |

The original publisher PDF and XML were audited and retained in the parent
research workspace. Fresh downloads on 2026-10-15 matched those copies.
`provenance.json` records the PDF link and SHA-256. The paper was published online
2026-08-23. A bounded title/DOI search and Crossref update check found no matching
correction; this does not prove absence of a prior disclosure.

The experiment models the share operation. It does not independently establish
the publication policy, ledger visibility, authentic count, or honest history.
Those are premises from the specification. A binding rule excluding singleton
release, encrypting the public payload, or hiding genuine occupancy would require
reassessing the counterexample. No such rule was found in the audited version.

This challenges adjacent-payload confidentiality, not the identifier-only
privacy game, anonymous signer identity, or authorization-token secrecy.
This scope is not a guarantee against additional inferences: in a registry
with only two domains, the recovered neighbor determines the other endpoint.
The two-choice comparison fixes the publisher and secret state internally;
it does not give them to the observer. Both alternative neighbors must be
eligible and distinct from the publisher. The comparison concerns a snapshot,
not identical complete bilateral ledger histories.

For larger batches, the certificate `w=c*kappa` requires `c*kappa<=m` and
returns only an aggregate XOR. It distinguishes histories only when their
aggregate XORs differ. A minimum accepted count above `m/kappa` excludes this
certificate. No deployment frequency is inferred from combinatorial feasibility.
