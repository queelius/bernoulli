# Independent source and threat-model review

Reviewed 15 October 2026. This review was completed independently, without reading prior review, assessment, research-state, or other reviewers' reports. The only submission materials read were the seven frozen files listed below. I read the supplied original Qin et al. article, checked its decisive pages visually, refreshed its PMC full text and Crossref record, and examined primary predecessors. All generated evidence is confined to this review directory.

## Verdict

**Do not reject the Comment on scientific/source/threat-model grounds. Recommend minor clarification of scope and predecessor attribution. No blocking source contradiction or counterexample to either proposition was found.**

The source actually admits the decisive execution: an honest, initially empty directional filter receives one successful insertion and is finalized at the end of its window. The ledger transaction exposes the filter and successful-insertion count. Occupancy identifies precisely its complete share set. XOR decoding then gives the adjacent identifier with certainty, without testing a guessed data identifier or validating a prefix. This directly challenges the source's express controlled-recovery claim for the adjacent identifier. It does not, as formulated, refute the separate data-identifier game or establish deanonymization of an arbitrary uploader.

Confidence is high in the exact singleton identity and its applicability to the written specification; moderate in the absence of a prior published observation of this particular protocol flaw. The bounded search did not establish priority exhaustively. No deployment-frequency or end-to-end implementation conclusion follows from this review.

## Frozen inputs and hashes

SHA-256 values were recomputed from the actual reviewed files. The six submission-content hashes agree with `manifest.json`; the manifest's own hash is also recorded.

| File | SHA-256 |
| --- | --- |
| `main.pdf` | `596500fa15a03357c85284e436d73a5fd3d894bc20d069dfb0bc444c6bb91810` |
| `main.tex` | `d258eec2b1a8a1bdd656a6e06ba9bb5fe44bc2d8d4ed8d4f46bf9dd4cb6dbbce` |
| `abstract.tex` | `eed7f877efc750ea50955db666a767931c6c1591bfb3b52451312761d85164b7` |
| `body.tex` | `f82b746de224af858f5f77087027f17ce2a51b52b6fc50a00060472dfb19bf27` |
| `backmatter.tex` | `660c1a9e68858a306e94da4558d44c6a726895db1df499e2ef65cc536c975045` |
| `references.bib` | `6d1e8e75f0bd202a93ef93ee678627dd68967429ae20aede98e3f71aada704ca` |
| `manifest.json` | `0bda77634b177222ba2dd7f263584f832333ca7b1aabaf07dcda63925e14b64f` |

The source PDF hash is `83d28e4460ac017a9117acbd80f06db37a70dffc04536e8ae68904448efc1417`; adjacent source XML hash is `bb766d99b8364d2c2bc7c6d1eebeb4dfbd8af6cd3a7abf87840195edc5545655`. Paths are `.research/bounded-discovery/frozen-retrieval/evidence/gbfplus-2026.{pdf,xml}`. The Comment PDF has five pages. I inspected all five rendered pages and source pages 11 and 18; the relevant algorithm and claim agree with their extracted text.

## Ranked findings

### 1. Minor scope precision: avoid an absolute negative claim about other disclosures

**Location:** `body.tex:156–158`, Comment PDF p. 3.

**Finding:** The sentence saying the recovered identifier does not identify the publisher or reconstruct a complete edge is a reasonable description of what the proposed scan generally establishes, but reads as an unconditional impossibility claim. The source permits a registry with just two domains (§5.1, p. 9). In a cross-domain singleton with two registered domains, a recovered adjacent identifier determines the other domain as the publisher, and the public direction determines the complete directed domain edge. This does not challenge the preceding comparison, which expressly assumes two eligible neighbors and hence at least three domains. It means that the negative scope sentence should remain attached to that comparison or be qualified.

**Evidence status:** Verified source allowance plus a direct logical inference, not an empirically observed attack. No extra cryptographic capability is required in the two-domain example.

**Decisive fix:** Use “does not in general identify the anonymous publisher, associate the transfer with a particular data identifier, or reconstruct a complete named edge or path.” Alternatively say that the result proves adjacent-identifier recovery without claiming those further capabilities. This is nonblocking and makes the claim more conservative; it does not weaken the singleton disclosure.

### 2. Minor attribution: the closest GBF predecessor already explicitly separates disclosure from acceptance

**Location:** `body.tex:215–224`, Comment PDF p. 4.

**Finding:** Dong, Chen, and Wen's §4.1 expressly warns that a query can reject membership while revealing a stored value, including a warning about other protocols. The Comment cites their padding and OT but omits this closer conceptual precedent. [Author-hosted CCS paper, §4.1, printed pp. 792–793 / PDF pp. 4–5](https://changyudong.site/assets/pdf/ccs13.pdf).

**Evidence status:** Verified primary predecessor. It does **not** expressly give the GBFPlus singleton/time-window/occupancy attack; it is not a novelty-killing disclosure of the whole claimed contribution.

**Decisive fix:** Add one sentence noting that Dong et al. already distinguish accidental membership acceptance from recovery of another stored value, then explain that GBFPlus occupancy makes a complete share set deterministically available in the allowed singleton release. Keep novelty tied to that protocol-specific selector and release rule. No additional experiment is needed.

### 3. Optional wording: distinguish ledger visibility from unrestricted public-chain access

**Location:** first sentence of `abstract.tex`; `body.tex:3–4`.

**Finding:** The source describes a permissioned/consortium ledger (§4.1, p. 6), while the Comment repeatedly says “public ledger attestations.” The attacker is within the source's ordinary-ledger-observer class, so the attack is in scope. Nevertheless, the phrase could be read as asserting unrestricted Internet access to an open blockchain.

**Evidence status:** Verified source setting; ambiguity in the Comment's wording, not a substantive threat-model mismatch.

**Decisive fix:** Say “ledger-visible attestations” once, or specify that “public” means visible to ordinary ledger observers in the permissioned setting. This is editorial and nonblocking.

## Source-premise audit

The following facts were checked against the original supplied article, not against the Comment's premise notes. Page numbers refer to the article's printed 24-page pagination. Its [current PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC13605127/) was also retrieved for freshness.

| Premise | Exact source locator | Assessment |
| --- | --- | --- |
| Adjacent-domain metadata is a claimed protected object | Table 1, p. 4; §4.2, p. 7; §6.2, p. 18 | Explicit. Table 1 lists the adjacent domain as protected; §6.2 makes the controlled-recovery claim after prefix and assigned-domain checks. The Comment is not substituting a new protected object for data-identifier privacy. |
| Ordinary observers may inspect transaction contents | §4.3, p. 7 | Explicit adversary capability. The ledger is permissioned, but observers with access are included. |
| Honest administrators obey insertion/submission rules | §4.3, p. 7 | Explicit. This supports the honest-history premise without inferring honesty from signatures. |
| One-insertion release is allowed | §5.2 final paragraph on p. 10 | Finalization occurs at insertion failure, capacity, or time-window end. There is no stated minimum successful-insertion count or mandatory dummy padding before submission. A one-transfer window is a valid trace. This is an existence inference from the rule, not an asserted deployment frequency. |
| Count and full finalized filter are observable | Eq. (5) and immediately following paragraph, p. 11 | `c` is in the authenticated message; the ledger transaction contains those fields and the finalized filter itself. This is not merely a digest-only commitment. |
| Occupied cells remain distinguishable, including a zero payload | §5.2, p. 10; Algorithm 4 lines 7, 11, 15, 21, p. 11; §6.2, p. 18 | Explicit occupancy bit plus occupied-only payload storage. `1 || 0^λ` is distinct from the empty marker. Classical GBF filling is described separately in §3.3, p. 5 and is not a GBFPlus finalization step. |
| The observer knows κ, m, λ, and suffix width ℓ | §5.1, pp. 8–9, especially published public-parameter set Eq. (3), p. 9 | The source publishes `κ`, `η̂` (the Comment's `m`), `λ`, and `l_DA` (the Comment's `ℓ`) in `PP`. Algorithm 4 line 3 specifies that `N_adj` is the final `l_DA` bits. No secret format parameter is assumed. |
| Registered identifiers identify domains | §5.1, p. 9, paragraph following Eq. (3) | Domain/DA/key/identifier associations are public. Reading the suffix therefore yields interpretable metadata, not just an opaque token. |
| Neighbor changes do not change positions or prefix | Algorithm 4 lines 2–4, p. 11 | The paired value uses the publisher key and data identifier; `N_adj` appears only in the target suffix. Same publisher/key/data can therefore share positions and prefix in the two candidate worlds. |
| Exactly κ distinct selected positions | `Idx` definition, §5.1, p. 9; Algorithm 4 line 4 | Explicit duplicate suppression. No uniform-κ-subset assumption is required for the Comment's identities. The double-hash implementation in §6.3 does not defeat them. |
| Later successful insertions preserve prior row equations; failures are atomic | Algorithm 4 lines 7–21; explanatory text §5.2, p. 10 | Occupied payloads are read, never overwritten. `tag = -1` implies no empty selected position and consequently no writes. A successful insertion fills only previously empty positions. |
| The claimed source game is separate | `G_qpriv`, §4.3, p. 8; Theorem 4, pp. 17–18; Eq. (27), p. 17 | The Comment appropriately avoids claiming a formal win in the data-identifier game. Eq. (27) concerns guessed reconstructions passing both tests; exact recovery from the occupancy-selected real support bypasses that task. |

For the challenge-world reachability check, use at least three honestly registered domains, a fixed publisher, and either of two eligible distinct neighbors. Each world has a valid observed transfer, an honest outgoing singleton, and the requisite counterpart behavior. The registration table, publisher key, data identifier, configuration, direction, window, prefix, and selected support can be identical. The row suffix changes. Signatures and digests may change; indistinguishability does not require literally identical authentication bytes. Counterpart records can also differ. Giving the observer additional records cannot undo an exact decoder on the focal snapshot. This is a metadata-confidentiality counterexample, not a purported reduction to `G_qpriv`.

The disjoint certificate is also exact: every successful support has size κ, occupied positions equal their union, and equality of union size with `cκ` forces pairwise disjointness. XOR then returns the aggregate. The text correctly abstains outside that condition, does not claim all supports are reachable or uniformly sampled, and notes that a fixed aggregate across candidate histories need not leak a distinguishing fact.

## Primary-predecessor and correction checks

The bounded search covered the exact DOI with correction/erratum/corrigendum terms; GBFPlus with attack, singleton, comment, and correction terms; and garbled Bloom filters with occupancy, singleton, leakage, and linear terms. I did not find an indexed primary correction or earlier explicit statement of the deterministic GBFPlus singleton disclosure. This is a negative search result, not a guarantee of novelty.

The refreshed [Crossref DOI record](https://api.crossref.org/works/10.3390/e28090947) has an empty `relation` object, no `update-to` entry, and MDPI's generic update policy. The fresh PMC HTML contains the same decisive release/publication/controlled-recovery premises. MDPI direct retrieval initially returned HTTP 429; indexed MDPI text and PMC were accessible. No correction/erratum/retraction notice was found in the fetched PMC record. A missing notice or database relation does not rule out an unindexed correction.

Dong et al.'s [August 2016 notice](https://faculty.washington.edu/zkwen/articles/dong13psi.pdf) concerns malicious-server selective failure in enhanced PSI, not the semi-honest protocol. The CCS original confirms filling in Algorithm 1 lines 22–26 and OT-based intersection delivery. Neither inspected version reports the occupancy-selected singleton disclosure.

[Silva–Kschischang](https://arxiv.org/abs/0809.3546), §V and Lemma 6, explicitly analyze joint linear observations via rank/row-space conditions. That is appropriate general background; the Comment does not claim new linear-algebra theory. [Hao et al.](https://www.usenix.org/system/files/usenixsecurity24-hao-meng-unbalanced.pdf), §5.1, printed p. 6442 and Figure 5 on p. 6443, encode PRF-masked values and allow authorized de-masking. The Comment's brief precedent claim is supported, and its warning that this does not prove a full GBFPlus repair is warranted.

## Strongest objections tested and rejected

- **Singletons might be forbidden or padded.** No such requirement appears in GBFPlus finalization; importing the original GBF's random-fill step would change the specified construction.
- **Only a commitment is public.** The text following Eq. (5) expressly includes the finalized instance in the transaction.
- **Hidden pairing-derived positions prevent the scan.** For a singleton, occupancy reveals the complete selected support without computing its derivation.
- **The hash prefix masks the suffix.** It is concatenated, not XORed with the identifier. Its secrecy has no effect on extracting the final bits of the recovered word.
- **Marginally uniform shares establish privacy.** Joint observations satisfy the row equation; their XOR is deterministic. This objection contradicts the stored-array structure.
- **The attack requires a successful authenticated query.** It requires only honest generation and ledger access. Prefix checks are validation rules for the authorized API, not barriers to reading public bytes.
- **Permitted occupancy leakage already allows everything claimed.** In the two-neighbor comparison, occupancy and count can be identical while the suffix differs. The extra disclosed identifier is not a function of those metadata alone; it comes from their joint use with public payloads.
- **The claimed neighboring worlds are unreachable.** The neighbor is a separate Algorithm 4 input and does not enter either position or prefix derivation. The honest three-domain transfer traces above are compatible with the source rules.
- **Repeated supports or index collisions invalidate row invariants.** Duplicate positions are suppressed. An all-occupied attempted insertion fails and triggers rotation; it does not erase the existing singleton or invalidate its row equation.
- **The work merely rediscovers secret sharing.** The algebra is elementary and established, as the Comment acknowledges. The source-specific existence of an unauthorized complete-share selector is the substantive corrective observation. Finding #2 improves its positioning without eliminating it.
- **Large experiments or a real ledger are required.** Not to establish the exact conditional counterexample. Operational prevalence and deployed-code behavior are explicitly left unmeasured. The supplement's limited simulation scope is clearly stated.

## Limits and verification

I did not read the supplement archives, run the author's experiments, audit signature security, or reproduce the full pairing/ledger implementation. Their reported test counts remain outside this review's verification scope. No code or manuscript was changed. The exact identities were checked directly from Algorithm 4, and source visibility/finalization premises were checked in the original and refreshed primary text. The title is the neutral journal-Comment form; the abstract and conclusion correctly focus on an allowed release and adjacent metadata, without asserting universal deployment compromise or a formal break of Theorem 4.

Evidence includes `input-hashes.json`, downloaded primary PDFs, a refreshed PMC HTML and Crossref JSON, `evidence/retrieval-manifest.json`, source-premise snippets, and rendered source/Comment pages. The review supports the corrective scientific point; it is not an editorial acceptance decision or a claim of exhaustive novelty.
