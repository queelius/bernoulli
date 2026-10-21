# GBFPlus Comment: author review and next steps

Updated 2026-10-18 for Alexander Richard Towell.

**Archival update, 2026-10-20:** the author authorized release under the archival
policy. The preprint and self-contained evidence are now public at
https://doi.org/10.5281/zenodo.23497466. The scientific files are unchanged;
publication metadata and licenses were finalized for this release. See
[the archival record](archival-publication/README.md). Journal declarations
remain to be completed, with this preprint disclosed.

**Fee inquiry sent:** the author authorized the prepared inquiry, which was
sent to entropy@mdpi.com on October 18 and verified in Gmail Sent Mail.
No manuscript was attached or payment authorized. See the
[receipt](submission-preparation/fee-inquiry-sent-2026-10-18.json).

**Current decision:** the author reviewed and approved the PDF on October 18
and asked to submit. He still requires **zero publication charges**. Actual
author declarations and written fee clearance remain pending. The current
draft adds the journal-required AI-use
description in the reproducibility section and clarifies the acknowledgment;
the proofs, results, and code are unchanged. See
[submission preparation](submission-preparation/README.md) for the current
conditions and fee-only inquiry draft.

**Recommendation: prioritize the existing focused Comment.** The author has
clarified that PhD credit is secondary for this result. Doctoral eligibility
therefore no longer gates this route. The narrow contribution and earlier
one-week effort ceiling remain appropriate.

Start with the [five-page manuscript](manuscript/main.pdf). Its editable
[LaTeX source](manuscript/main.tex), [editorial review record](editorial-review/response-ledger.md),
and [portable reproduction instructions](manuscript/venues/entropy-comment/supplement/README.md)
are prepared.

**Editorial revision and packaging, 2026-10-15:** the
[Entropy Comment PDF](manuscript/venues/entropy-comment/main.pdf) and
[complete author-review ZIP](manuscript/venues/entropy-comment/packages/gbfplus-comment-review.zip)
are now the practical review entry points. They include the venue title,
portable supplementary code/data, source ZIP, an unsent cover letter, and
explicit declaration status. Canonical and venue versions now share revised
scientific text: singleton first, worked example, precise assumptions, and an
interpretable verification table. Three independent AI agents assessed both
the initial draft and revision. This is internal review, not journal peer review.
The supplement passes 17 tests; coverage reports 121 statements and 48 branches
under normal compilation, with optimization rejection separately tested.
Clean extraction reproduces every deterministic result. See the
[verification record](manuscript/venues/entropy-comment/validation/verification.json).

**Fresh adversarial review:** three new reviewers independently challenged the
source/threat model, mathematics/artifact, and readability. Their findings and
responses are in [the new assessment](adversarial-review/assessment.md).
The revision narrows the masking statement to suffix uniformity, qualifies
further identity inferences, identifies permissioned-ledger access and public
parameters, and credits Dong et al.'s earlier disclosure warning. Interpretation
now follows the singleton before the aggregate extension. No main-result
counterexample was found; these are internal AI-assisted checks.

## The claim and its source premises

In an honestly generated GBFPlus filter with one successful insertion, public
occupancy identifies all shares of that insertion. XORing those stored words
reveals the adjacent-domain identifier in their suffix, for every construction
realization. No guessed secret prefix or query token is needed.

The source is Qin et al., *Privacy-Preserving On-Chain Attestation for
Cross-Domain Data Flows via GBFPlus*, Entropy 28(9):947,
[DOI 10.3390/e28090947](https://doi.org/10.3390/e28090947).

| Premise to inspect | Source location | Role |
|---|---|---|
| Adjacent-domain metadata is protected; recovery is described as controlled by prefix/domain checks | §4.2, Table 1, and §6.2 | Identifies the precise claim challenged |
| The XOR target ends with the unmasked adjacent-domain identifier | Algorithm 4 | Identifies the recovered payload |
| The filter, count, and genuine occupancy are public | §5.2 after Eq. (5), §6.2 | Gives the complete share set |
| Time-window finalization has no stated minimum insertion count | §5.2 | Permits the singleton execution |

The [saved publisher PDF](frozen-retrieval/evidence/gbfplus-2026.pdf) and XML
match fresh publisher downloads byte-for-byte on 2026-10-15. Crossref lists no
linked correction or update. Focused searches found no matching prior
disclosure; that remains a bounded novelty check. See the
[refresh record](resumption-2026-10-15.json).

The public equality `occupied cells = insertions × shares per insertion`
also certifies disjoint supports and reveals an aggregate XOR. It does not
recover individual identifiers in a general batch; it requires `c*kappa<=m`
and distinguishes histories only when their aggregate XORs differ. XOR sharing and the
marginal/joint distinction are established mathematics; the claimed increment
is the concrete protocol counterexample.

## Limits to preserve

The note does not claim an identifier-game break, signer identification, raw
data recovery, full-path reconstruction, or an end-to-end implementation of
the ledger and cryptography. Deployment prevalence is unmeasured. Padding and
masking comparisons do not constitute a complete secure repair.

A binding rule excluding singleton publication, hiding genuine occupancy or
payloads, or masking the suffix would require reassessing the attack. None was
found in the audited specification.

The historical investigation record reports 19 passing new tests, 92 relevant
package regressions, 100% new-code statement coverage, and 98.89% branch
coverage. Source/result hashes still match that record. These tests were run
in the original investigation, not rerun during the focused editorial revision.
The new 17-test supplement record supersedes the earlier 13-test packaging
record. An optimization-mode bug discovered in review is fixed in the portable
runner; the original experiment driver is retained for provenance and must be
run without optimization.

## Remaining decisions

1. **Author review completed October 18:** the current PDF is approved.
   No further manuscript approval is requested absent a substantive change.
2. **Applicable fee:** indexed official Entropy information lists a general
   APC of CHF 2,600, potentially plus tax. A Comment-specific exemption or
   reduced fee remains unverified. No funding or willingness to pay is assumed.
3. **Declarations and release:** finalize the author contribution, funding,
   conflict, publication-history, and assistance declarations in the
   [prepared sheet](manuscript/venues/entropy-comment/declarations.md).
   Supplementary information is a supported journal release route, so a new
   repository or DOI is not necessary for preparation. Release approval and
   applicable terms remain the author's decision. Packaging is complete;
   the earlier 1–3-day estimate included that now-completed work.

Proposed venue title:

> Comment on Qin et al. Privacy-Preserving On-Chain Attestation for Cross-Domain
> Data Flows via GBFPlus. Entropy 2026, 28, 947

Earlier wording for the fee inquiry (the final version was sent October 18):

> I am preparing a focused Comment on Entropy 2026, 28, 947
> (DOI 10.3390/e28090947). Could you confirm the applicable article processing
> charge for a Comment and whether that article type receives an exemption or
> reduced fee? This inquiry does not submit a manuscript or accept a fee.

The latest user instruction conditionally authorizes submission of this paper,
superseding the earlier no-submission rule. The author has reviewed it,
and publication must be free. The fee-only inquiry has been prepared separately;
its status is recorded in `submission-preparation/state.json`. Local preparation
continues without another permission step. The earlier dependence-calculus,
planner, publication-triage, and deduplication no-go findings remain intact;
this review does not reopen them or add another discovery candidate.
