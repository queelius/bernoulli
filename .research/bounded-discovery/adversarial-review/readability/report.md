# Independent cold-read editorial review

**Verdict:** The frozen Comment is intelligible, visually legible, and sufficiently self-contained for a knowledgeable reader who has not opened the original article. I found **no mandatory readability or layout repair**. One short clarification of the observer's public configuration would improve precision; the other recommendations below reduce navigation and reading effort. They are optional edits, not reasons to reject the argument or impose a different article structure.

This is a readability and presentation verdict. I did not independently verify the original protocol, literature priority, or execution of the implementation. The frozen document explicitly remains an author-review draft with unresolved final declarations; this verdict does not change that status.

## Review conditions and independence

- Reviewed the specified frozen `inputs/main.pdf`, five US Letter pages, dated 15 October 2026.
- Rendered all five pages with Poppler at 150 dpi and inspected them sequentially **before reading any LaTeX source**. The page PNGs and contemporaneous [cold-read notes](cold-read-notes.md) are retained here.
- Then read `main.tex`, `abstract.tex`, `body.tex`, `backmatter.tex`, `references.bib`, and `manifest.json` to identify exact locations. Input hashes matched the supplied manifest.
- For reviewer navigation only, listed the supplement ZIP's members and read its top-level `README.md`. I did not inspect its implementation, recorded results, provenance record, premise ledger, or tests, and did not execute it.
- Did not open prior editorial reports, assessment/state files, response ledgers, or other reviewers' report files. A narrow fact from another reviewer was later relayed by the coordinator; it is disclosed separately below and is not the basis of the cold-read finding.
- No manuscript changes, rebuild, publication, contact, or code tests were performed. All review outputs are confined to this directory.

The PDF has no printed line numbers. Line references below identify the frozen source file, alongside the PDF page and visible passage. The `page-*-text-numbered.txt` files provide additional extraction locators, but their large mathematical operators are imperfectly extracted; the rendered pages are authoritative for visual QA.

## Ranked findings

### 1. Make the observer's configuration knowledge explicit

**Classification: minor clarification; recommended before the next external read, not a blocking defect.**

**Evidence:** p. 2, opening observer paragraph and symbol definitions (`body.tex:26–40`); p. 2, paragraph beginning “The observer therefore needs only” (`body.tex:76–83`); p. 3, Proposition 2 (`body.tex:113–121`). The public successful-insertion count is explicitly supported on p. 1 (`body.tex:16–18`). The suffix width is explicitly listed as needed on p. 2, but its public availability is not stated. Likewise, the reader is introduced to κ without an explicit statement that the observer knows it for the occupancy test.

**Reading task:** List the inputs available to the observer and decide whether the displayed public scan is executable using those inputs alone. This task is only partly answered directly: the reader must infer that κ and ℓ are known configuration parameters. The algebra itself remains clear, and the text does not conceal the need for a suffix width.

**Small remedy:** Add one sentence after the parameter definitions identifying the configuration parameters available to an observer, with the appropriate source location. For example, if supported: “The configured κ, λ, and identifier width ℓ are public.” State the mapping to the source's identifier-width notation if it differs. No new experiment, theorem, or section is warranted.

### 2. The meaning of the singleton disclosure arrives after a secondary result

**Classification: optional organization improvement.**

**Evidence:** the singleton proof and marginal-versus-joint explanation finish on p. 2 (`body.tex:70–110`). On p. 3, the aggregate extension intervenes (`body.tex:112–141`) before “Which confidentiality claim is challenged?” and the explicit account of what the recovered identifier does and does not identify (`body.tex:143–164`).

**Reading task:** Immediately after understanding the proof, determine whose identity is exposed and which original guarantee is challenged. The abstract provides an initial answer, but a reader seeking the precise semantic interpretation must skip the extension or continue through it. The answer is present; it is not missing or contradicted.

**Small remedy:** Consider moving the existing confidentiality-scope block before the larger-batch extension. Alternatively, move just the short existing explanation that the recovered value names the neighboring domain, without identifying the publisher or a complete edge. Prefer moving text to adding another disclaimer. Keeping the current order is defensible if the author wants both algebraic results presented together.

### 3. The final claim loses emphasis at the page break

**Classification: optional visual and structural improvement.**

**Evidence:** the last paragraph begins at the bottom of p. 4 and ends with the fragment “operational workloads”; p. 5 begins “remain unmeasured” and continues to the final conclusion (`body.tex:236–243`). The rest of p. 5 consists of draft declarations and references.

**Reading task:** Skim the ending to identify the paper's final positive claim and its limit. The conclusion is accurate and readable, but the reader must join a split sentence across pages, and the decisive statement is visually grouped with back matter rather than given a clear ending position.

**Small remedy:** Give the final claim its own short paragraph, beginning with the existing “The exact singleton counterexample…” sentence, or recover a few lines earlier so the final paragraph stays together. Do not add a full conclusion section merely to satisfy a template. This is a presentation cost, not an illegible or missing conclusion.

### 4. Runtime safeguard detail interrupts the scientific evidence summary

**Classification: optional concision improvement.**

**Evidence:** p. 4, final paragraph of Section 3 (`body.tex:207–211`), especially the sentence explaining that the runner rejects optimized execution because its experiments require assertions. The supplement README already gives this operational information under its first “Reproduce” heading.

**Reading task:** Determine what the checks establish and how they relate to the exact proof. That task is already completed by the preceding prose, input classes, and table. The interpreter's assertion behavior makes the reader switch from scientific interpretation to execution mechanics immediately before the implications section.

**Small remedy:** Move the optimized-execution sentence to the README alone. The command, tested Python version, and availability statement can remain if desired. Preserve the substantive distinctions between fixed-configuration enumeration, independently seeded arrays, and operational attack prevalence; those caveats perform useful work.

### 5. The PDF does not identify the supplement's concrete entry point

**Classification: optional navigation improvement; the supplied package passes this task.**

**Evidence:** p. 4, Section 3 and Table 1 caption (`body.tex:168–172, 200–211`); p. 5, “Data and code availability” (`backmatter.tex:1–4`). These name “Supplement S1” but give neither its descriptive title nor archive filename or README entry point.

**Reading task:** Starting from the PDF, find the promised stored arrays and the reproduction instructions. With the supplied package this succeeds: the ZIP has a top-level `README.md` headed “Supplement S1: GBFPlus public-occupancy disclosure,” and its first substantive section gives the command. An isolated PDF gives less help locating the accompanying file.

**Small remedy:** In the availability paragraph, identify S1 by its descriptive title and indicate that its README is the starting point. A stable journal supplement link can replace package-specific navigation later. No public deposit is necessary for this local review, and I do not count the absence of a public URL as a defect in the frozen author-review draft.

## Reading-task results

| Task for an unfamiliar knowledgeable reader | Result and evidence |
|---|---|
| State the concern and contribution from the abstract alone | **Pass.** p. 1 explains the allowed single insertion, occupancy-selected share set, exact XOR recovery, and distinct metadata target (`abstract.tex:1–14`). |
| Understand the relevant construction without the original paper | **Pass for the claimed mathematical model.** p. 2 defines the words, positions, prefix/suffix, insertion update, failure behavior, and occupied set (`body.tex:35–57`). Determining whether these premises faithfully match the source is a different review task. |
| Enumerate the observer's known inputs | **Pass with an inference.** Occupancy, public cells, and successful count are stated; public parameter knowledge should be consolidated as in finding 1. |
| Reconstruct the singleton attack and understand an occupied zero | **Pass.** Proposition 1 and its short proof on p. 2, then the concrete three-share array on p. 3 (`body.tex:59–100`). The occupied `000` is visibly distinct from an empty cell. |
| Distinguish exact identities from empirical success rates | **Pass.** Exact quantification appears in Proposition 1; Section 3 explains fixed enumerations and separate seeds; Table 1 explicitly denies a disclosure-probability interpretation (`body.tex:61–67, 168–203`). |
| Tell whether larger batches disclose each individual identifier | **Pass.** p. 3 states aggregate-only recovery, the sufficient condition, possible lack of informational value, and abstention outside the condition (`body.tex:118–141`). |
| Identify the affected privacy claim and avoid overreading the result | **Pass, with delayed detail.** p. 3 separates neighbor metadata from publisher identity, data identifiers, and complete paths (`body.tex:143–164`); finding 2 concerns the route to this answer. |
| Interpret the table without consulting code | **Pass.** p. 4 states each tested equality, parameter class, counts, and mismatches. The caption identifies where fixed positions and prefixes are supplied. |
| Locate and start the supplement from the review package | **Pass.** The README is at archive root and immediately supplies the standalone command. Execution correctness was outside this review. |
| Find the take-home message quickly at the end | **Partial presentation pass.** The message is explicit, but its paragraph straddles pp. 4–5; see finding 3. |

No central reading task failed outright. The partial results above are concrete inference or navigation costs; they should not be inflated into mandatory stylistic rules.

## Per-page visual QA

| Page | Observed result |
|---|---|
| [1](page-1.png) | The long title fits in two lines; author information, draft status, abstract, keywords, and Section 1 are legible. The title block is spacious but does not obstruct reading. Section 1 ends mid-sentence before p. 2; this is routine continuity, not a serious break. |
| [2](page-2.png) | Equations (1) and (2), subscripts, XOR operators, concatenation symbols, proof, and complexity terms are legible and unclipped. The exact-object and observed-cell notation is consistent locally. The forward Figure 1 reference resolves at the top of the next page. No figure relocation is required. |
| [3](page-3.png) | The seven-cell toy array, empty-cell marks, occupied zero, three-word XOR, and 2-bit suffix are interpretable at the inspected scale. Caption and figure are together. Equation (3) and its proof are readable. The aggregate result and confidentiality discussion are dense but not visually crowded. |
| [4](page-4.png) | Table 1's first two input descriptions wrap cleanly; numeric columns remain aligned under clear headings. No collision or clipped mathematics was observed. The table follows its introduction and caption. The final paragraph begins too near the page foot to retain its ending; see finding 3. |
| [5](page-5.png) | The continuation of the conclusion, declarations, and four references are legible. DOI line breaks do not clip text. The page is dominated by back matter, which weakens the visual emphasis of the conclusion but causes no loss of content. |

Across all pages I observed no overlapping text, missing mathematical glyphs, black replacement boxes, unresolved citation markers, or visibly broken cross-references. The table's smaller type remains readable. The all-zero/empty distinction is not dependent on color.

## Title, abstract, tone, scope, and provenance

The title is long because it identifies the article being discussed. I would not replace it with a generic attack headline: its form follows MDPI's recommended Comment-title pattern. [MDPI Layout Style Guide, Section 2.2](https://www.mdpi.com/authors/layout)

The abstract contains the problem, mechanism, exact scope, extension, evidence, and implication. It does not promise full data recovery, anonymity failure, or measured deployment prevalence. The opening restates the attack, but then adds the concrete source premises; this repetition is productive. The conclusion makes the narrow correction needed to the claimed guarantee and does not declare the protocol wholly insecure.

The tone criticizes a claim and a public-view assumption, not the authors. The singleton argument and limited extension address one protocol issue rather than becoming an unrelated theory paper. These are the relevant Comment considerations in MDPI's policy; they do not justify imposing a full research-article IMRAD sequence here. [MDPI Comments and Replies policy](https://www.mdpi.com/ethics)

The provenance distinctions are mostly well judged: proofs versus implementation checks, public-premise verification versus simulation, and AI-assisted checking versus external peer review are all explicit. The draft status and pending human declarations should remain accurate until the author resolves them. The operational optimizer sentence is expendable; the scientific scope limitations are not. Entropy's instructions allow supplementary code and request description of supplementary elements, supporting the small navigation improvement rather than demanding a new external deposit for this review. [Entropy Instructions for Authors](https://www.mdpi.com/journal/Entropy/instructions)

## Separately supplied fact after the cold read

After all five PDF pages and the listed manuscript sources had been read, the coordinator relayed that another reviewer found κ, λ, and the source's identifier-width parameter in public parameters in source Section 5.1, Equation (3), and the suffix assignment in Algorithm 4. I did not inspect that review or independently verify the source in this editorial task. The coordinator proposed a clarifying sentence.

This supports an easy remedy to finding 1 if confirmed; it does not alter my original classification. The cold-read issue was the need to infer known configuration, not evidence that the parameter was secret or that the mathematical result failed. No changed manuscript was reviewed here.

## Exact reviewed hashes

SHA-256 values are also available in [reviewed-hashes.json](reviewed-hashes.json). The supplement was read only to the navigation extent specified above.

| Frozen input | SHA-256 |
|---|---|
| `main.pdf` | `596500fa15a03357c85284e436d73a5fd3d894bc20d069dfb0bc444c6bb91810` |
| `main.tex` | `d258eec2b1a8a1bdd656a6e06ba9bb5fe44bc2d8d4ed8d4f46bf9dd4cb6dbbce` |
| `abstract.tex` | `eed7f877efc750ea50955db666a767931c6c1591bfb3b52451312761d85164b7` |
| `body.tex` | `f82b746de224af858f5f77087027f17ce2a51b52b6fc50a00060472dfb19bf27` |
| `backmatter.tex` | `660c1a9e68858a306e94da4558d44c6a726895db1df499e2ef65cc536c975045` |
| `references.bib` | `6d1e8e75f0bd202a93ef93ee678627dd68967429ae20aede98e3f71aada704ca` |
| `manifest.json` | `0bda77634b177222ba2dd7f263584f832333ca7b1aabaf07dcda63925e14b64f` |
| `gbfplus-comment-supplement.zip` | `b53663fc475519a669af2f0c8831dc6a91e73333dc05114ef4263a232fc2727b` |

The supplement's inspected `README.md` member hashes to `dcfa62a7c8ad1510dc124eaef492bf2a5ffbd5552845d70a37af775f0121c8a8`.
