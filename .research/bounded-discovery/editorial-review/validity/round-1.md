# Independent adversarial validity review, round 1

Reviewed 2026-10-15. Scope: scientific validity of the current Entropy Comment, especially publication admissibility, the observer's view, conditioning, the disjoint extension, and the predecessor contrast. No earlier assessment, positive review, or concurrent reviewer report was read. The component README was read for local instructions; its links to earlier reviews were not followed. No manuscript, implementation, or package file was changed.

Reviewed manuscript: `.research/bounded-discovery/manuscript/venues/entropy-comment/main.tex`, SHA-256 `0afc54c4b3f506ffbefb83fd90a596ce44b97179e66b8d44ea6ddf0063b9cfc0`. A copy fixing these line references is in `notes/reviewed-main.tex`. The five-page PDF was checked against its extracted text.

Primary target: Qin et al., *Entropy* **2026**, *28*, 947, DOI [10.3390/e28090947](https://doi.org/10.3390/e28090947). I inspected the frozen PDF, XML, and layout extraction, including direct rendered inspection of physical PDF pages 10 and 11. The PDF hash is `83d28e4460ac017a9117acbd80f06db37a70dffc04536e8ae68904448efc1417`, matching the supplied source manifest. Live publisher access failed through the web tool; this review establishes what the frozen published source says and does not certify the absence of a later correction.

## Verdict

**No fatal premise or proof error found. The singleton confidentiality counterexample is valid against the frozen published specification.** The strongest attempted rejection was that the Comment treats an internal, incompletely filled filter as a public attestation. That rejection fails: the source explicitly finalizes on time-window expiry, explicitly transmits the finalized instance, explicitly exposes occupancy, and explicitly transmits the successful-insertion count. No stated rule excludes a singleton. The result is not contingent on observing a lucky share realization, guessing a data identifier, or learning the uploader's identity.

The revision should make the singleton the primary result and sharpen the disjoint extension and comparison experiment. V1 is the main wording issue. V2 and V3 prevent foreseeable but avoidable objections. They do not require weakening the singleton theorem or changing the protocol. The remaining entries record objections I tested and found already answered or mathematically unsupported; they should not be turned into invented defects.

## V1 — Bound the minimum-count conclusion and show when the aggregate is informative

**Severity: moderate, scope/interpretation issue; not a defect in Proposition 1.**

**Manuscript locations:** lines 30–32, 100–130, and especially 245–249.

The implication `w=cκ => suffix(XOR occupied cells)=XOR endpoints` is correct. The conclusion that a minimum count would not by itself invalidate the disjoint case needs an explicit feasibility boundary. Any snapshot satisfying the certificate must have `cκ <= m`. A policy admitting only counts above `m/κ` excludes this certificate altogether. In the source's tabulated configurations, `m=2216` at capacity `η=128` and `κ=12`, so `ηκ<m`; an ordinary threshold at or below capacity does not eliminate combinatorial feasibility in that configuration. This source-specific observation does not license an unqualified statement across arbitrary configurations or a claim that the event is operationally common.

Also, revealing an aggregate is not automatically a nonzero information disclosure under every workload. For example, two equal endpoints have XOR zero; a workload already known to have that form gives this statistic no endpoint entropy to reveal. The current text correctly disclaims individual recovery, but a small distinguishing example would establish the extension's confidentiality meaning rather than relying on the word “reveals.”

**Source evidence:** Section 5.1, physical pp. 8–9, defines `κ`, `η`, and position count `η̂`; Algorithm 4 on p. 11 limits successful counts to capacity. Section 6.3, Table 3, p. 19, reports the configurations. Frozen layout lines 460–465, 621–649, 1124–1146. The Comment uses `m` for the source's `η̂`.

**Exact remedy:** replace the minimum-count sentence with wording equivalent to:

> A minimum count above one excludes singleton publication. The disjoint-support identity remains applicable only to accepted snapshots satisfying `w=cκ`, which requires `cκ<=m`; it yields a confidentiality distinction when the candidate endpoint sequences have different aggregate XORs. No occurrence frequency for this event in deployment is established here.

Then give the following example, explicitly conditional on a reachable disjoint history: keep the publisher, data identifiers, supports, release metadata, and the first `c−1` endpoints fixed; let the last endpoint be either of two eligible neighboring identifiers `B` and `C`. Position derivation does not use this endpoint. The two aggregate XORs differ by `B XOR C != 0`, so the certificate distinguishes the two candidate histories exactly. No individual-recovery claim for an arbitrary unknown batch follows.

This example does not require disclosure of the publisher's identity or of actual other endpoints during the attack. It is a chosen pair of admissible confidentiality worlds. Distinguish that proof device from an operational attack assuming `c−1` known endpoints.

**Why workload evidence matters only to the extension's practical significance:** under the explicitly additional model of independent uniform `κ`-subsets for a predetermined sequence of `c` attempted records,

`Pr[all disjoint] = product(j=0,...,c−1) binom(m−jκ,κ)/binom(m,κ)`.

For `m=2216, κ=12`, the base-10 log probability is approximately `−0.0284` at `c=2`, `−0.803` at `c=8`, and `−316.28` at `c=128`. These are my independent analytic checks, recorded in `notes/checks.json`, not measurements or claims about the prototype's double hashing. They are unconditional over the predetermined attempts, not probabilities conditioned on a published successful-only batch or rotation. The large-batch extension can be negligible even when feasible. The singleton identity is unaffected.

**Unresolved:** actual counts and support distributions in deployments, and the occurrence probability under the implemented deterministic index construction. The Comment does not need to resolve these to refute a universal singleton confidentiality claim.

## V2 — Make the two-world experiment explicitly admissible without giving away the publisher

**Severity: minor formalization gap.**

**Manuscript locations:** lines 134–158.

The sentence fixing the “public registration table, publishing administrator, data identifier” does not say which fixed quantities are public and which are fixed internally by the experiment. A hostile reader could incorrectly interpret it as giving the observer the uploader's identity, undermining the claimed ordinary-observer relevance. It also says only “two different registered adjacent-domain identifiers.” For a cross-domain transfer with the same publisher, both alternatives must identify eligible domains distinct from that publisher. A two-choice comparison therefore requires an admissible system with two such alternatives, rather than merely two registered domains total.

**Source evidence:** Section 5.1 p. 9 makes the registration association `(DA_i,KPK_i,N_i,D_i)` public, but Section 4.2 p. 7 separately promises anonymous uploading. Section 5.2 p. 10 defines sender/receiver roles for a cross-domain event. Algorithm 4 p. 11 derives `u` and the indices from the publishing DA's query key and the data identifier, while `N_adj` enters only the payload target. Frozen layout lines 354–365, 476–490, 566–580, 621–629.

**Exact remedy:** begin the experiment as follows:

> In a system with a fixed publishing DA and two eligible neighboring DAs distinct from it, fix the public registration table and choose the same publishing DA, its secret state, data identifier, direction, time window, and configuration internally in both worlds. The observer is not given the publishing DA's identity or secret state. The challenge bit changes only the adjacent-domain identifier among those two eligible alternatives.

Continue by observing that the support and prefix are therefore identical for the source-side target snapshot, because the endpoint is not an input to their derivation. Let the free shares be freshly sampled in either world. Clarify that the public view being compared is that snapshot and its authenticating transaction fields; the claim does not require the entire bilateral ledger histories to have identical metadata.

For Proposition 2, “condition on any support and prefix reached by honest derivation” is slightly more precise than “fix a singleton support, prefix,” which could otherwise include an unattainable support under the actual deterministic index procedure. No uniformity assumption on the distribution of supports is needed.

**Unresolved:** none for the singleton proof after this clarification. A complete new global-ledger security game is unnecessary and would enlarge the claim.

## V3 — Anchor the target to adjacent-identifier confidentiality, not recovery of a complete relationship

**Severity: minor scope precision; the present manuscript already has a sufficient substantive defense.**

**Manuscript locations:** lines 25–29, 46–51, 160–165, 245–252.

The strongest semantic defense of the original paper is that recovering an endpoint without recovering the anonymous publisher does not identify a whole edge or path. That defense is valid against any inflated full-path or signer-deanonymization claim. It does not answer the Comment's actual endpoint claim, because the source separately promises to protect the adjacent-domain identifier itself.

The most useful exact source locations are:

- Section 2, p. 3, final comparison paragraph: the paper separately lists the data identifier, adjacent domain, and signer's public identity as concealed properties (layout lines 160–168).
- Table 1, p. 4, GBFPlus row: lists dimensions/occupancy/direction/rotation as visible and the target, adjacent domain, and uploader identity as protected (layout lines 199–206).
- Section 4.2, p. 7: “Privacy of Flow Metadata” includes adjacent-domain relationships; “Accountable Anonymity” separately concerns the uploader's identity (layout lines 354–365).
- **Section 6.2, p. 18:** the claimed privacy advantage includes “controlled recovery of an adjacent-domain identifier only after the consistency-prefix and assigned-domain checks” (layout lines 1085–1090). This is the sharpest direct contrast with the attack, which performs neither check.

**Exact remedy:** add the Section 6.2 reference to the Introduction and state that the recovered registered identifier identifies the neighbor attached to an anonymous directional attestation; the counterexample need not identify the publishing DA, a particular data item, a complete edge between two named domains, or a path. The existing disclaimer at lines 160–165 should remain.

Do not claim that the Comment breaks `G_qpriv` or Theorem 4 merely because it recovers the same endpoint in both identifier worlds. The current explicit refusal to make that claim is correct. The broader metadata goal and narrower identifier game are a mismatch exposed by this example, not a license to conflate their experiments.

**Unresolved:** editorial judgment about whether a correction to the stated design goal and its interpretation warrants a Comment. This is not a mathematical flaw.

## V4 — Singleton publication and the observable count/occupancy survive the primary-source audit

**Severity: informational; attempted fatal objection rejected.**

**Manuscript locations:** lines 55–91 and 95–119.

The following premises are explicit rather than inferred from a storage diagram:

1. Section 5.2 p. 10 invokes finalization when capacity is reached **or** the time window ends, in addition to failure-triggered rotation. There is no stated lower count guard (layout 581–589).
2. The paragraph following Equation (5), p. 11, names `c` as the successful-insertion count and says the ledger transaction includes the message fields and the finalized GBFPlus instance (layout 600–612).
3. Section 5.2 p. 10 attaches an occupancy bit to each payload, and Algorithm 4 p. 11 writes `1 || word`. Hence an occupied zero payload is distinguishable from an empty cell (layout 575–580, 632–647).
4. Section 6.2 p. 18 specifies occupied-only payload storage in addition to the occupancy bits (layout 1085–1097). Sparse encoding does not conceal the selector.

A concrete admissible history is: initialize a directional instance; process one ordinary cross-domain transfer with an eligible neighbor; perform the first insertion; receive no further records in that direction before the configured window ends; finalize, sign, and submit the instance. The first insertion necessarily succeeds because every selected position is empty, assuming the normal valid configuration `κ<=m`. The normal bilateral acknowledgement and off-chain signatures do not create a lower bound on the source-side filter's record count.

Authenticity is not itself a proof of faithful construction, but Section 4.3 assumes registered DAs follow insertion/submission protocols, and the Comment expressly assumes honest generation. The count is neither the number of attempted records nor a secret implementation counter. These objections are already sufficiently answered; a succinct execution example would make the source-to-counterexample chain easier to audit.

## V5 — Proofs and conditioning are sound within their stated domains

**Severity: informational; no proof error found.**

**Manuscript locations:** lines 70–75, 95–119, and 132–146.

The union equality follows from the published update. If an insertion succeeds, every chosen cell is occupied afterward and no nonselected cell is touched. If all selected cells were occupied, the loop only reads those words, `tag` stays unset, and failure causes no mutation. Existing occupied cells are not overwritten. Duplicate suppression in Section 5.1 ensures exactly `κ` distinct positions, so cancellation from repeated indices is excluded.

The support-cardinality proof needs no independence of insertion supports, endpoints, or prefixes. It is an exact identity under honest history. Independence is used only in Proposition 2, where the source independently samples the `κ−1` free words of a singleton; the residual contains at least one uniform summand when `κ>=2`. The entire view is nevertheless constrained by its XOR. Neither a pseudorandom-prefix assumption nor a random-support model is needed to distinguish endpoint suffixes.

The probability-one statement is over share randomness for an honest singleton, not over how often a workload releases one. The present text already distinguishes those quantifiers. Keep that distinction prominent in the revision.

## V6 — The predecessor contrast is supportable; do not turn it into a security claim about padding

**Severity: informational; no incorrect contrast found.**

**Manuscript locations:** lines 216–234.

[Dong, Chen, and Wen's primary paper](https://changyudong.site/assets/pdf/ccs13.pdf), Algorithm 1 lines 22–26 (PDF p. 4), fills residual empty cells with random words. Section 4.3 (PDF p. 6) transfers an intersection structure using OT, rather than transmitting the full server filter plus genuine insertion occupancy. Its Theorem 2 distinguishes reconstruction of a stored value from acceptance of a nonmember. These support the Comment's limited contrast. They do not establish that public release of an arbitrarily filled full GBF is secure, and the current Comment does not claim that.

The all-cell-XOR padding statement is correct as a statement about that statistic: one fresh uniform pad independent of the secret and remaining shares makes its XOR uniform. It is not a statement about the observer's entire vector, and eliminating the occupancy bit alone does not establish secrecy. Preserve the existing qualification at lines 227–228. A padding word might also be removable through other side information; the statement should not be read as asserting that genuine occupancy is the only possible selector.

[Hao et al., Section 4.2](https://www.usenix.org/system/files/usenixsecurity24-hao-meng-unbalanced.pdf), p. 6442, explicitly masks values with PRF outputs before encoding and supports the brief established-technique comparison. [Silva and Kschischang, Lemma 6](https://arxiv.org/pdf/0809.3546), p. 7, supports the rank-based precedent under its stated distribution assumptions. Neither reference is needed to rescue the elementary singleton proof.

## Revision acceptance criteria

The next revision should establish, in a short continuous argument:

1. An ordinary honest singleton is permitted by the published finalization rule and its complete occupancy-selected shares are public together with a reliable count under the source's honest-DA model.
2. XORing those shares returns a registered adjacent-domain identifier for every share realization, without revealing or needing the publishing administrator's identity.
3. This contradicts a separately stated adjacent-identifier confidentiality claim; it is not presented as a break of the identifier challenge game, signer anonymity, or full-path secrecy.
4. The disjoint extension remains an exact conditional identity, with the `cκ<=m` feasibility boundary, an example of distinct aggregate worlds, and no implied deployment frequency or universal individual recovery.

A full protocol implementation, empirical singleton-rate estimate, or new cryptographic assumption is not necessary to establish those four statements. None should be invented to make the Comment seem stronger. No code changes were made, so the repository unit/integration suite was not run for this review. The independent combinatorial calculation was executed and its assumptions and results are preserved in `notes/checks.json`.
