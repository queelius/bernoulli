# Round 2: independent readability and reviewer-usability review

Reviewed 2026-10-15. I read the revised scientific text before any response
ledger or other review report, then inspected all five rendered pages. The
assessment below is based on that revision, not on whether it followed my
proposed outline. No manuscript or implementation file was changed.

## Reviewed inputs

Files are under `manuscript/venues/entropy-comment/`; `abstract.tex`, `body.tex`,
and `backmatter.tex` are the shared scientific inputs referenced by the wrapper.
Line numbers below refer to those input files, not to the old monolithic source.

```text
SHA-256
main.tex       d258eec2b1a8a1bdd656a6e06ba9bb5fe44bc2d8d4ed8d4f46bf9dd4cb6dbbce
abstract.tex   eed7f877efc750ea50955db666a767931c6c1591bfb3b52451312761d85164b7
body.tex       3e5038adfdc354235c0472e53cb87bc8fe7ae51ba61c875bee6babc81499498b
backmatter.tex 660c1a9e68858a306e94da4558d44c6a726895db1df499e2ef65cc536c975045
main.pdf       5ba44973cd90a4e16e33248e89a6934a94ca99d7cb64d6f11911d39f07cd49bf
```

The PDF contains five pages, with creation time 2026-10-15 02:18:59 CDT.
Rendered review copies are in `rendered-round-2/` beside this report.

## Assessment

The revision now reads as a compact protocol Comment. Its first body paragraph
provides the confidentiality target, allowed execution, public operation, and
recovered object. The theorem order matches the importance of the claims; the
general extension is clearly secondary and qualified. The table can be read
without consulting the supplement to determine what was checked. The conclusion
draws together material already established rather than introducing the source's
acceptance analysis for the first time.

R1-R8 are resolved at their intended level. One new sentence about the zero-word
example needs a narrow correction (R9). This is an explanatory error, not a
problem with the figure's arithmetic or the singleton theorem. I find no
remaining structural readability blocker and request no additional science.
The final source-premise and mathematical judgments remain outside this
editorial review's remit.

## R1-R8 disposition

| ID | Disposition | Evidence and reading test |
|---|---|---|
| R1: singleton-first narrative | Resolved | `body.tex` 3-12 states the mechanism before notation. Proposition 1, lines 59-74, is now the singleton result; the example follows it and Proposition 2 is introduced as a limited extension. A reader can explain the attack from the first paragraph. |
| R2: notation and terminology | Resolved | Lines 35-48 define `Z_j`, `S_i`, `N_i`, `P_i`, widths, and concatenation locally; lines 55-57 define `O`, `c`, and the suffix operation. “Disjoint sets of possible complete views” avoids overloading insertion-position support. Lines 155-163 explicitly distinguish the neighbor identifier from a named edge, path, signer, and data identifier. |
| R3: verification table | Resolved | Lines 173-202 state the fixed small-case inputs, explicit equalities, counts, and all parameter widths. The larger row says “Seeded singleton” and `c=1`. “Mismatch” is defined before the table. Each row now has a clear input class and assertion. |
| R4: interpretation order | Resolved | Lines 142-163 put the two-world comparison, data-identifier-game distinction, and source Equation (27) distinction together. The two analyses are not conflated. Section 4 no longer introduces either distinction as new evidence. |
| R5: repeated scope defenses | Resolved at the substantive level | The opening has one honest-history/observer paragraph; the aggregate limitation follows its result; the privacy-target boundary follows the comparison; and repair/workload limits are in the implications. The discussion opens with the positive protocol-specific issue. A few harmless verification cautions could still be trimmed, but they no longer dominate the argument. |
| R6: abstract arc | Resolved | `abstract.tex` 1-14 follows target, allowed singleton, mechanism, deterministic result, qualified extension, verification, scope, and implication. It ends on the confidentiality claim rather than on a disclaimer about novelty. |
| R7: compact hierarchy | Resolved | Four sections expose the argument's sequence; there is no isolated numbered subsection. The marginal-uniformity point is an explanatory paragraph. The venue title is retained. The three-feature source-premise paragraph is readable as prose; a premise table is unnecessary. |
| R8: equation and definitions | Resolved | PDF page 2 contains the first equation and all its definitions together. Neither display equations nor their immediate explanations are clipped or separated awkwardly. |

## New findings, ranked

### R9 — Correct what the occupied-zero example demonstrates

**Priority:** small required explanatory correction. This is not a validity
challenge to either proposition.

**Location:** `body.tex` lines 78-79, referring to Figure 1 at lines 84-101;
PDF page 2 near the bottom and page 3 at the top.

**Problem:** “Figure 1 illustrates why a zero-valued occupied cell must still
be included” suggests that including the zero word is necessary for the XOR
recovery shown in the figure. The displayed calculation itself shows the
opposite: `010 XOR 111` already equals `101`, because `000` is the XOR identity.
An occupied zero word must be treated as occupied when forming/counting the
selected set and applying an occupancy certificate; its arithmetic contribution
to the XOR is zero. The current sentence blurs those two roles.

**Concrete remedy:** replace the sentence with “Figure 1 distinguishes an
occupied zero word from an empty cell.” If the counting point should be
emphasized, add “The zero word counts toward occupancy even though it does not
change the XOR.” No change to the example or any test is needed.

**Evaluation criterion:** a reader can say which quantity changes if `000` is
misclassified as empty: the occupied set and its count, but not the XOR value
in this example. The example must not imply that XORing with zero changes the
reconstructed word.

### R10 — Optional final trim of redundant verification cautions

**Priority:** optional preference; not a blocker.

**Location:** `body.tex` lines 173-179, Table 1 caption at 199, and line 211.

**Problem:** the text already explains that the seeds provide reproducibility,
not a cryptographic or workload model, and the caption says the table is not an
estimate of disclosure probability. “No statistical confidence interval is
inferred from these checks” adds little after those statements and revives some
of the earlier defensive tone.

**Concrete remedy:** delete line 211 if a final compression pass is desired.
Keep the proof-versus-check distinction and the seeded-input description.

**Evaluation criterion:** readers still understand that the identity is exact
and the enumerations check the implementation. Leaving the sentence unchanged
does not impair comprehension or justify another revision round.

## Concrete reading tasks after the revision

- **First-page orientation — passes.** The observer is an ordinary ledger
  reader; the protected item is the adjacent-domain identifier; a permitted
  singleton window supplies the complete share set; XOR exposes the suffix.
- **Reconstruct the formal claim — passes.** The symbols are defined as they
  enter, and the singleton proof is short enough to follow directly from the
  displayed insertion invariant.
- **Separate singleton from general result — passes.** Proposition 2 and its
  following paragraph state aggregate-only recovery and the condition under
  which the certificate applies.
- **Understand the relationship to the source's analysis — passes.** The two
  privacy targets and the guessed-tuple acceptance calculation are distinguished
  locally. The observer is not implicitly handed the anonymous publisher's
  identity.
- **Interpret the verification counts — passes.** The table identifies the
  equalities, configurations, and input classes. The reader need not infer
  whether the 64 cases are arbitrary batches.
- **Explain the zero cell's role — currently misleading.** R9 is the only
  concrete local reading task that remains impaired by the revised wording.

## Rendered-page inspection

All five pages were rendered and visually inspected at 100 dpi. The figure is
legible and its cell labels and arithmetic are clear. It floats to the top of
page 3, after its page-2 mention and before the aggregate extension; that is a
normal and usable placement, not a new blocker. Table 1's longer descriptions
remain readable and the numeric columns are distinct. No overlap, clipped text,
broken mathematical glyph, or unreadable reference was observed.

The last implications paragraph crosses from page 4 to page 5. This does not
impair the argument and does not warrant forced page breaks. The revised
backmatter is concise and separate from the scientific conclusion. Its pending
author declarations remain visible without repeatedly interrupting the argument.

After R9's one-sentence correction, another broad restructuring pass would have
little editorial value. A targeted verification of that sentence and any
resulting pagination is sufficient from this review's perspective.

## Targeted source closure — 2026-10-15

Checked the current shared `body.tex` without reopening the broad review.
Its SHA-256 is:

```text
f82b746de224af858f5f77087027f17ce2a51b52b6fc50a00060472dfb19bf27
```

**R9 is closed.** Lines 78-79 now explicitly distinguish an occupied zero word
from an empty cell and state that it counts toward occupancy without changing
the XOR. This directly satisfies the reading criterion above. **R10 is closed:**
the redundant confidence-interval sentence has been removed.

The mask observation at lines 229-232 now specifies fresh uniform secret masks
independent of the identifiers and one another, and separately mentions PRF
masking as related practice. This remains readable and does not reopen an
editorial issue.

The original reviewed-source and PDF hashes above are preserved. This closure
verifies source wording only; the coordinating agent will rebuild and inspect
final pagination. No readability issue remains open from this review.
