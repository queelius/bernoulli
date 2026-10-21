# Independent adversarial validity review, round 2

Reviewed 2026-10-15. This is a review of the actual revised sources and rebuilt PDFs, following my independent round-1 report. I did not read other reviewers' reports. The coordinating agent relayed one occupied-zero wording concern and the provenance of an earlier source hash; those are identified separately below. I changed only this report and notes in my assigned review directory.

## Verdict

**The revision passes this scientific-validity review. V1–V6 are resolved or retain their previously sound treatment. No substantive premise, scope, conditioning, or proof defect remains in the reviewed text.**

One mathematical imprecision in the optional masking discussion was found during this round and corrected: independence alone does not make masks conceal a value. The corrected text now requires fresh uniform masks independent of the identifiers and one another. The occupied-zero wording was also corrected to distinguish its contribution to occupancy from its neutral effect on XOR. I directly rechecked both corrections in the final shared source and both final PDF text extractions, and visually inspected final venue PDF pages 2–4.

The claim remains narrow and valid: an honest, permitted singleton release exposes the registered adjacent-domain identifier. The revision does not convert that into a claim about recovering a data identifier, identifying an anonymous publisher, reconstructing a complete named edge/path, or breaking the source's `G_qpriv` game. The disjoint extension is an exact conditional identity with an explicit feasibility and informativeness boundary.

## Exact reviewed versions

All final hashes below were calculated directly during this review. Paths are relative to `.research/bounded-discovery/manuscript/`.

| File | SHA-256 |
|---|---|
| `abstract.tex` | `eed7f877efc750ea50955db666a767931c6c1591bfb3b52451312761d85164b7` |
| `body.tex` | `f82b746de224af858f5f77087027f17ce2a51b52b6fc50a00060472dfb19bf27` |
| `backmatter.tex` | `660c1a9e68858a306e94da4558d44c6a726895db1df499e2ef65cc536c975045` |
| `references.bib` | `6d1e8e75f0bd202a93ef93ee678627dd68967429ae20aede98e3f71aada704ca` |
| `main.tex` | `39b9ad3708042666a12c958be495bd0abbe95053f58afd08fe96e1ba93230202` |
| `main.pdf` | `2549724465a1df3a803aa89ca27d9549f21de945e782d4a40befbe82661d549a` |
| `venues/entropy-comment/main.tex` | `d258eec2b1a8a1bdd656a6e06ba9bb5fe44bc2d8d4ed8d4f46bf9dd4cb6dbbce` |
| `venues/entropy-comment/main.pdf` | `596500fa15a03357c85284e436d73a5fd3d894bc20d069dfb0bc444c6bb91810` |

I verified that the venue's `abstract.tex`, `body.tex`, and `backmatter.tex` are symlinks to these canonical sources and have identical dereferenced hashes. Its bibliography also has the hash above. Both final PDFs have five pages.

Machine-readable hashes, source snapshots, extracted PDF text, and the inspected venue-page images are preserved under `notes/round-2-*`.

Before the two narrow corrections, I directly read the original round-2 passages and directly hashed the venue PDF as `5ba44973cd90a4e16e33248e89a6934a94ca99d7cb64d6f11911d39f07cd49bf`; its extracted text contained those earlier passages. The corresponding pre-correction `body.tex` hash, `3e5038adfdc354235c0472e53cb87bc8fe7ae51ba61c875bee6babc81499498b`, was relayed by the coordinating agent from the readability review's recorded evidence. It was **not** independently hashed by me before the edit and is included only with that provenance. No source hash was reconstructed or represented as directly observed.

The frozen GBFPlus PDF remains the round-1 primary source, SHA-256 `83d28e4460ac017a9117acbd80f06db37a70dffc04536e8ae68904448efc1417`. In this round I reread the relevant published representation/finalization/transaction passages and Section 6.2. I did not broaden the literature search.

## Per-finding dispositions

Line references below refer to the final shared `body.tex` unless otherwise stated.

### V1 — Disjoint feasibility, informativeness, and minimum count: resolved

Lines 134–141 explicitly state that `cκ<=m` is necessary, the certificate is impossible otherwise, the output is only an aggregate, a reachable history with one differing eligible endpoint changes the aggregate, and identical candidate aggregates disclose nothing through this statistic. They also disclaim a distribution or frequency for disjoint batches.

Lines 236–243 replace the earlier broad minimum-count warning with the precise condition: a policy excludes this certificate only when its accepted batches cannot satisfy `w=cκ`; counts always above `m/κ` are one example. The revision does not imply that `cκ<=m` alone proves reachability under the actual index function. Its example is expressly conditional on a reachable disjoint history. No independence or random-support assumption has been added to Proposition 2.

The choice not to insert my round-1 idealized probability calculations is appropriate. They were diagnostic checks under extra assumptions, not evidence of deployment frequency. The singleton now leads the abstract, argument, and theorem sequence, so the extension no longer carries the core contribution.

### V2 — Eligible worlds and fixed-but-hidden publisher: resolved

Lines 144–154 first fix the public registration table, then explicitly fix the publisher and secret state internally. The observer is expressly not given that identity or secret state. Both endpoint alternatives must be eligible neighboring domains distinct from the publisher. This is an admissibility assumption on the chosen experiment, not a new item of public auxiliary knowledge supplied to perform the attack.

The same paragraph correctly explains why endpoints do not change the source-side positions or prefix: in Algorithm 4, the endpoint enters the suffix, whereas the secret-derived input controls the prefix and indices. It confines the comparison to one snapshot and its authenticating transaction and does not require distinct bilateral ledger histories or signatures to be identical.

Lines 104–110 now condition the individual-share statement on an honestly reached support and prefix. This avoids silently treating every arbitrary position set as attainable by the actual deterministic index procedure. The proof still needs uniformity only for the free shares, not for support selection.

### V3 — Adjacent-identifier claim versus signer/path/game claims: resolved

Lines 5–12 directly identify the source's Table 1, Section 4.2, and especially Section 6.2 claim that recovering the adjacent identifier is controlled by prefix and assigned-domain checks. The last claim was rechecked against source PDF p. 18, frozen layout lines 1085–1090. This is a faithful target for an attack that reads the suffix without either check.

Lines 156–164 explicitly limit the recovered value to the neighbor encoded in the attestation and separate this result from data-identifier association, named-edge/path reconstruction, signer identification, `G_qpriv`, Theorem 4, and guessed-tuple acceptance. These statements set the result's demonstrated scope; they should not be read as a separate proof that auxiliary information can never identify a publisher. No such universal anonymity preservation result is needed here.

### V4 — Honest singleton publication and public inputs: retained and strengthened

Lines 14–24 give the complete source-to-counterexample chain and a concrete allowed history: initialize a directional filter, insert one transfer, observe no further transfer in that direction, and finalize on window expiry. Lines 26–31 distinguish authentic commitment from honest construction.

I rechecked source Section 5.2 on pp. 10–11: time-window expiry invokes finalization; `c` is explicitly the successful-insertion count; the transaction contains the finalized instance and message fields. Source Sections 5.2 and 6.2 expose occupancy. No minimum-count rule, secret count, digest-only release, or payload masking was found in those passages. The revision introduces none as an assumption.

### V5 — Identities and conditioning: retained correctly

Lines 50–57 correctly preserve the source update invariant. The singleton proof, lines 59–74, uses `O=S_1` and the row equation; it holds for every admitted position set, prefix, and share realization. The larger-batch proof, lines 116–132, uses equality in the union-cardinality bound to certify disjointness and then XORs the row equations. Both are exact identities under honest construction.

The revision does not turn deterministic exact checks into estimated probabilities. Its probability-one distinguishing statement concerns construction coins in an allowed singleton experiment, while release frequency remains expressly unmeasured. The occupied-zero clarification described below now avoids confusing occupancy counting with arithmetic contribution.

### V6 — Predecessor contrast and limited protection statements: retained, with masking precision fixed

Lines 215–224 preserve the supported contrast with the original GBF construction: random filling of unused cells and an OT-mediated intersection structure are different from releasing the full filter plus genuine insertion occupancy. The revision makes no claim that arbitrary public GBF release is secure.

Lines 226–234 confine padding and masking observations to the statistic, retain the occupancy-selector objection, and expressly decline to claim a complete repaired protocol. The PRF precedent remains an attribution to an existing technique, not a proof of a new instantiation. The uniform-mask correction below makes the sufficient condition mathematically explicit.

## Issues identified or checked during round 2

### V7 — Independence alone does not conceal a masked identifier: found and resolved

**Initial severity: minor mathematical imprecision in an optional protection statement; no effect on the attack or proofs.**

The initially read passage said:

> Secret masks on the adjacent identifiers also hide this statistic when the masks are independent; PRF masking of arbitrary values is already used in oblivious key-value retrieval.

Independent deterministic-zero masks are an immediate counterexample; independent biased masks can also leave information. I reported this to the coordinator before the edit.

The final source, lines 229–232, requires fresh uniform masks independent of the identifiers and one another and gives PRF masking as a separate established-technique statement. An XOR containing a fresh independent uniform mask is uniform, so this condition is sufficient for the narrow statistic claim. I verified the corrected wording in both final PDF extractions and visually on final venue p. 4. **Closed.**

### Occupied-zero wording: externally flagged, directly rechecked, resolved

The coordinator relayed this concern before my second review. My initial source and PDF read confirmed the sentence:

> Figure 1 illustrates why a zero-valued occupied cell must still be included.

Without specifying occupancy counting, this can suggest that omitting a zero changes the XOR. It does not. The final lines 78–80 state that the occupied zero counts toward occupancy but does not change XOR. The figure's arithmetic remains `010 XOR 111 XOR 000 = 101`; its occupancy interpretation is correct. The correction appears in both final PDFs and was visually checked on venue p. 2. **Closed.**

## Remaining limits and review scope

No further scientific revision is required by this review. Deployment frequency and impact, a complete protocol repair, and editorial suitability remain unestablished; the manuscript now states the relevant scientific limits accurately. Final human review is still needed as the draft itself records.

I did not rerun the supplement or the repository's unit/integration tests: no code was changed in my task, and implementation reproduction is a separate review scope. My checks were source comparison, proof and experiment audit, direct hashing, PDF text verification, and targeted PDF rendering. This verdict is not external peer review or a claim about material outside the pinned versions above.
