# Fresh adversarial review: disposition

Reviewed 15 October 2026 at the author's request. **The narrow GBFPlus Comment
survives this review.** Three new independent agents found no counterexample to
the singleton disclosure or disjoint-position certificate, and no contradiction
between their stated premises and the published specification. They did identify
an overbroad ancillary masking sentence, an absolute negative identity claim,
and missing emphasis on the closest predecessor. Those issues are corrected.
The readable five-page draft remains a plausible protocol-specific Comment;
this is not evidence of editorial acceptance or exhaustive novelty.

## Independence and scope

Each reviewer started without conversation history, previous assessments, or
other reviewers' reports. They received the frozen manuscript and relevant
primary source or artifact, and wrote only in separate review directories.
The coordinator independently assessed the findings before editing the shared
manuscript. Each reviewer then checked the relevant corrections. These are
internal AI-assisted reviews, not external peer review.

- [Source and threat-model report](source/report.md), followed by its
  [targeted closure](source/closure.md).
- [Mathematics and methods report](methods/report.md), followed by its
  [targeted closure](methods/closure.md).
- [Readability and layout report](readability/report.md), followed by its
  [all-page final closure](readability/closure.md).

The frozen inputs and hashes remain in `inputs/`. Earlier reports under
`../editorial-review/` retain their original versions and scope.

## Findings and corrections

| Finding | Evidence and consequence | Disposition |
|---|---|---|
| **M1: masking wording claimed too much about the full statistic.** | A mask `M` can be uniform and independent of identifier `N`, while prefix `P=M`. Then `P || (N XOR M)` reveals `N`, despite a uniform suffix. The methods reviewer exhaustively constructed this example; the coordinator independently reproduced its one-bit form. This concerns the optional defense discussion, not either proposition. | **Corrected.** The claim now concerns the recovered suffix for singleton/disjoint cases, and requires the mask vector to be independent of the joint identifiers and prefixes. Padding is explicitly independent of the remaining cells. The full-public-view and reuse limitations remain. |
| **S1: the negative publisher/edge claim was absolute.** | In a permitted registry containing only two domains, knowing the neighbor and public direction can identify the other domain and directed edge. This does not invalidate the two-neighbor comparison, which requires at least three domains. | **Corrected.** The sentence now says the recovery does not *in general* establish publisher identity, a particular data identifier, or a complete named edge/path. Supplement premises record the special case. |
| **S2: the closest GBF warning deserved direct attribution.** | Dong, Chen, and Wen's 2013 paper, Section 4.1, already separates disclosure of a stored value from false-positive membership acceptance. That conceptual distinction is established. | **Corrected.** The text explicitly credits this warning and locates the increment in GBFPlus's occupancy selector and allowed release rule: a complete share set becomes available without a query or support collision. No general secret-sharing novelty is claimed. |
| **S3: “public ledger” could imply unrestricted Internet access.** | The source uses a permissioned/consortium ledger. Its observer can inspect transaction contents, but ledger access is a premise. | **Corrected.** The abstract says “published ledger attestations”; the body defines public visibility relative to a permissioned-ledger reader and states that access is required. |
| **R1: the observer's knowledge of widths and κ was implicit.** | Public parameter set Eq. (3) contains the relevant widths and κ; the Comment's ℓ is the source's `l_DA`. | **Clarified.** The notation paragraph makes this mapping and public knowledge explicit. |
| **R2: the main confidentiality interpretation followed the secondary extension.** | A reader had to traverse the larger-batch proposition before completing the singleton's meaning. | **Reordered.** The confidentiality comparison and limitations now follow the worked singleton example, before the aggregate extension. |
| **R3: the final positive claim split across pages.** | The earlier ending broke its principal concluding sentence between pages 4 and 5. | **Improved.** The operational limitation and final contribution are now distinct intact paragraphs on page 5. |
| **R4: interpreter mechanics interrupted scientific evidence.** | The optimizer-guard sentence was useful artifact documentation but a detour in the paper. | **Moved out of the paper.** The README and tests retain the safeguard details; the paper retains test scope and the reproduction command. |
| **R5: Supplement S1 lacked a concrete entry point.** | Readers needed to identify the associated package and its first instruction. | **Clarified.** The availability statement names the supplement and directs readers to its `README.md`. |
| **C1: the review ZIP's root README used a workspace-relative link.** | The old archive copied a workspace README whose relative path escaped the extracted bundle. The coordinator checked the archive directly. | **Corrected in packaging.** Both archive `README.md` and `START-HERE.md` use the portable review guide, with internal destinations checked. The workspace README is separate. |

All reviewer findings have targeted closure. The source and methods closures
identify body hash `66f0be224c7683c7d8eabfed97dc022e8bbcfca6d5e1b258d2e5d768d6cc414e`.
The subsequent final body hash is
`a9f2748ec68ccb865be5c39b03dc14112e9d73b0e7b7ae8577fca26f8260dd97`:
the scope block was moved unchanged, the source's width notation was mapped
explicitly, the optimizer sentence was removed, and the ending was split into
paragraphs. The coordinator checked that the closed scientific passages and
both propositions were preserved. The readability closure reviews the exact
final body and final venue PDF; it is not relabeled as a new mathematical audit.

## Verification evidence

The methods reviewer independently reproduced the frozen supplement from a
clean ZIP: **17 unit/integration tests**, Ruff, strict mypy, and the standalone
command passed. Normal compilation covers **121 statements and 48 branches**
in the two runtime modules. The compile-time optimization guard is outside that
denominator and was separately tested under optimized execution. All scientific
code, tests, and expected results remain byte-identical in the revised package;
only its premise documentation changed during this review.

An independently derived whole-array oracle checked **771,787 updates** over
all ordered supports, targets, and free-word assignments in the stated small
two-attempt histories, plus a specified three-row overlap. It found no mismatch
and reconstructed all **64** saved full-word arrays. These are finite
implementation checks, not probability estimates, new paper results, or proof
of the unimplemented cryptographic/ledger components. The paper's original
256/1,024/64 table remains unchanged.

Both final manuscripts compile to five pages with no LaTeX warnings or unresolved
citations/references. The coordinator visually inspected all ten pages; the
readability reviewer independently inspected all five final venue pages. No
clipping, overlap, missing glyph, unreadable table, or required layout repair
remains. The final source archive is rebuilt after clean extraction, its PDF
text is compared with the reviewed PDF, and the supplement's deterministic
output is rechecked. Exact results, archive mappings, preservation comparisons,
and hashes are recorded in [verification.json](verification.json).

## Publication judgment and unresolved limits

The potential contribution remains a concrete correction to the written
GBFPlus release protocol: an admitted honest singleton exposes a complete
share set and therefore an adjacent-domain identifier. The source reviewer
refreshed the primary article and Crossref record and searched for corrections
and earlier observations. No indexed prior statement of this exact flaw or
linked correction was found; an unindexed predecessor or update remains possible.
The algebra, disclosure-versus-acceptance distinction, padding, and masking
are established and are now attributed more explicitly.

The review does not measure deployment frequency, implement a complete ledger,
break the separate data-identifier game, prove publisher anonymity, or provide
a full protocol repair. Aggregate disclosure can be uninformative under some
admissible workloads. Those limits are stated in the paper.

Continue with the focused Comment only after the author's scientific/source
review and accurate declarations. The current assessment does not promise
acceptance, a particular fee, or doctoral credit. No external submission,
publication, contact, expense, commit, or push occurred. Prior no-go findings
and unrelated workspace edits are preserved.
