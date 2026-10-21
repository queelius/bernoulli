# Targeted readability and layout closure

**Disposition: closed.** The current Entropy Comment PDF remains **five pages**. All five pages were rendered at 150 dpi and visually inspected before checking the revised shared sources. The five earlier optional recommendations have been addressed. I found no introduced reading failure, illegible element, overflow, or awkward break requiring another edit.

This closure concerns the exact hashes below. It is not a new source-fidelity, mathematical, or implementation audit. No other review reports were read, no manuscript files were changed, and no tests or build were run in this closure.

## Earlier recommendations

| Earlier finding and reading task | Current evidence | Disposition |
|---|---|---|
| Identify the configuration known to the observer | p. 2, `body.tex:36–43`, explicitly identifies the widths and κ as public configuration parameters and maps ℓ to the source's `l_DA`. The later suffix-width requirement is now grounded without an inference. | **Closed.** The added sentence is compact and legible. |
| Understand the singleton's confidentiality consequence before the aggregate extension | p. 3, `body.tex:116–137`, now follows the singleton example and precedes the extension at `body.tex:139–168`. | **Closed.** The reader can complete the main claim before taking up the secondary result. |
| Find a distinct, intact final positive claim | p. 5, `body.tex:244–253`, contains an intact minimum-batch/operational-limit paragraph followed by a separate three-line concluding paragraph. | **Closed.** The earlier split sentence across pp. 4–5 is gone. The ending remains on p. 5, but now has a clear visual boundary before the back matter. |
| Read the scientific evidence without an interpreter-safeguard detour | p. 4, `body.tex:211–214`, retains the test classes, standalone command, and tested Python version; the optimizer-mechanics sentence is absent. | **Closed.** The transition to implications is cleaner without losing the reproduction pointer. |
| Identify Supplement S1 and its entry point | p. 5, `backmatter.tex:1–5`, names *GBFPlus public-occupancy disclosure* and directs the reader to `README.md`. | **Closed.** The package-level navigation task is answered in the PDF. The supplement itself was not re-audited. |

## Other changed passages

- **Permissioned-ledger access:** p. 2, `body.tex:26–32`, defines the intended meaning of “public” and states the observer's access requirement. This resolves the possible Internet-public reading without adding a new model or a long qualification. The abstract's “published ledger attestations” on p. 1 is consistent with that definition (`abstract.tex:1–2`).
- **Publisher scope:** p. 3, `body.tex:129–137`, uses “does not in general” and remains easy to parse. The disclosure's positive target is still stated first, followed by limits; the qualifying phrase does not obscure the central result.
- **Dong precursor:** p. 4, `body.tex:218–231`, explains the value-disclosure versus false-positive-acceptance distinction and then states what public occupancy supplies here. The paragraph is longer than before but has a concrete logical progression. No new notation is needed to follow the contrast.
- **Padding and masking scope:** p. 4, `body.tex:233–242`, distinguishes the all-cell statistic, the retained occupancy selector, and the uniform recovered suffix for singleton/disjoint cases. Independence is stated in the same paragraph as the claim, and the paragraph still ends with the limit that this is not a complete protocol repair. The new wording is denser but remains readable.

These observations assess the wording and placement, not whether the source citations or probability statements are independently correct.

## All-page visual QA

| Page | Result |
|---|---|
| [1](closure-page-1.png) | Title, author block, abstract, keywords, and opening argument remain legible. The opening discussion continues mid-sentence onto p. 2, with no orphaned heading or missing content. This routine break does not need repair. |
| [2](closure-page-2.png) | The access and public-parameter clarifications add density, but the definitions, source-notation mapping, equations, proposition, proof, and final marginal-versus-joint paragraph fit without collision or clipping. Equation (1)'s lead-in remains understandable. |
| [3](closure-page-3.png) | Figure 1 remains readable and together with its caption. The scope discussion now has the intended priority; the aggregate proposition, proof, and limitations all remain on this page. No crowded math or broken transition was introduced. |
| [4](closure-page-4.png) | Table 1 is unchanged in interpretability: wrapped descriptions and numeric columns are aligned, and the caption is adjacent. The longer implications section fits as two intact paragraphs. It is text-dense but uses the same readable type and spacing. |
| [5](closure-page-5.png) | The final two argument paragraphs are intact and clearly separated from availability and declarations. The named supplement and `README.md` are legible. All four references remain on this page; no extra page or clipped DOI was introduced. |

There are no new mandatory fixes and no need for a further editorial rewrite on the evidence of this closure. The draft's stated pending human review and declarations remain unchanged.

## Exact reviewed hashes

All paths are relative to `.research/bounded-discovery/manuscript/`. SHA-256 values are also saved in [closure-hashes.json](closure-hashes.json).

| File | SHA-256 |
|---|---|
| `venues/entropy-comment/main.pdf` | `6abdc1c0b9613699bc4aabc8d6a872ba2785e9c27585452f743347d061859e46` |
| `venues/entropy-comment/main.tex` | `d258eec2b1a8a1bdd656a6e06ba9bb5fe44bc2d8d4ed8d4f46bf9dd4cb6dbbce` |
| `venues/entropy-comment/references.bib` | `6d1e8e75f0bd202a93ef93ee678627dd68967429ae20aede98e3f71aada704ca` |
| `abstract.tex` | `ed9594b82370715761474e26b04a7219a781dbcbca9475444d636e6e77a81e70` |
| `body.tex` | `a9f2748ec68ccb865be5c39b03dc14112e9d73b0e7b7ae8577fca26f8260dd97` |
| `backmatter.tex` | `86d67d8e14f1f1eb5269cf66b2c95193844c7b332ce0dc0201692d18518cc7a0` |
| `references.bib` | `6d1e8e75f0bd202a93ef93ee678627dd68967429ae20aede98e3f71aada704ca` |

The PDF metadata records creation and modification at 03:33:09 CDT on 15 October 2026. Hashes, not that timestamp, identify the reviewed version.
