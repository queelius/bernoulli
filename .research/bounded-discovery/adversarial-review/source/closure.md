# Targeted source-review closure

Date: 15 October 2026.

This is a targeted check of the **current** `.research/bounded-discovery/manuscript/abstract.tex` and `body.tex`, following my independent frozen-input report. I read both current files directly. I did not read other reviewers' reports, search for new literature, inspect implementation changes, or change manuscript files. This closure does not replace the original report or its frozen-input hashes.

**Verdict: all three findings from my source review are closed. The requested public-parameter clarification is also correct and complete. No source-review blocker remains in the checked wording.**

## Exact reviewed versions

SHA-256:

| Current manuscript file | Hash |
| --- | --- |
| `abstract.tex` | `ed9594b82370715761474e26b04a7219a781dbcbca9475444d636e6e77a81e70` |
| `body.tex` | `66f0be224c7683c7d8eabfed97dc022e8bbcfca6d5e1b258d2e5d768d6cc414e` |

The hashes were recomputed after writing this closure to verify that the files had not changed during the check.

## Finding-by-finding disposition

| Item | Current location | Disposition and reason |
| --- | --- | --- |
| Original finding 1: absolute negative statement about identifying the publisher/edge | `body.tex:159–161` | **Closed.** “Does not in general identify” states the limited capability established by the result without excluding special registries or auxiliary information. It accommodates the two-domain counterexample noted in my report. |
| Original finding 2: closer Dong et al. predecessor | `body.tex:222–231` | **Closed.** The text explicitly attributes disclosure despite a negative membership result to Dong et al. §4.1, then distinguishes the GBFPlus occupancy selector that exposes a complete share set without a query or support collision. The subsequent padding/OT contrast remains accurate. This appropriately locates the contribution in the protocol-specific release and selector, rather than the established fact that complete shares reconstruct their value. |
| Original finding 3: unrestricted-public-ledger implication | `abstract.tex:1–2`; `body.tex:3–4,26–32` | **Closed.** The opening now says “published ledger attestations”; the body defines public visibility relative to a permissioned-ledger reader and explicitly requires ledger access. This matches source §§4.1–4.3 and preserves the ordinary-observer attack. |
| Additional request: public knowledge of widths and κ | `body.tex:38–43` | **Closed.** The manuscript explicitly cites source §5.1, Eq. (3). That published `PP` includes `l_DA`, `λ`, and `κ`; the prefix width follows as `λ − l_DA`. Algorithm 4 line 3 fixes the identifier as the suffix. The Comment's `ℓ` is its renaming of `l_DA`. No unavailable parsing parameter is assumed. |

## Narrow masking-language check

At `body.tex:233–242`, padding is now independent of the remaining cells, and identifier masking is expressly limited to the singleton/disjoint-batch statistic. The masks are fresh, mutually independent, uniform, secret, and their joint vector is independent of the identifiers and prefixes. Under the stated construction, the recovered suffix in those cases is respectively `N_1 XOR R_1` or the XOR of all `N_i XOR R_i`; a nonempty collection of independent uniform masks has a uniform XOR. The retained warning that this is not a complete repair prevents interpreting the statement as a proof of confidentiality for all payload information, overlapping supports, or multiple releases. This wording introduces no source-review objection. I did not independently audit a proposed masking implementation or its key lifecycle.

## Limits

This is a source-text closure, not a fresh PDF/layout or build certification. No new build was requested for this remit. The original report's bounded novelty-search limits and lack of a deployment-frequency claim still apply. Its substantive verdict remains: the exact singleton disclosure is supported by the published specification, with no blocking source or threat-model contradiction found.
