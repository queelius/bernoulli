# Round 1: independent readability and narrative review

Reviewed 2026-10-15. Scope: readability, narrative order, peer-review structure,
notation, claim salience, repetition, title/abstract, and paragraph logic. This is
an adversarial editorial reading, not external peer review or a fresh audit of
the source article's premises. No earlier review or another current reviewer
report was read. No manuscript or implementation file was changed.

Reviewed inputs:

- Venue `manuscript/venues/entropy-comment/main.tex`, lines 1-279, and all five
  pages of the rendered `main.pdf`.
- Canonical `manuscript/main.tex`, for the corresponding prose and structure.
- Venue README and Supplement S1 README, solely for local packaging context and
  the meaning of the table's seeded checks.

Input SHA-256 values:

```text
venue main.tex  0afc54c4b3f506ffbefb83fd90a596ce44b97179e66b8d44ea6ddf0063b9cfc0
venue main.pdf  230f71acbd1cf28c1f7a9a9b0c7504be1f1a5f1ce2e0b4ed277d0a55da4a4177
base main.tex   7678422b618792791fa8998c9b1ba3b3603f97abb7f71332b4d298c1f59f4e89
```

## Assessment

The manuscript has a legible, compact central argument. Its abstract correctly
foregrounds an exact singleton disclosure and distinguishes the multi-insertion
aggregate. The body is less effective: it asks the reader to absorb the general
support-count certificate before giving the simple singleton mechanism, and it
repeatedly answers objections about claims it has not made. This gives a short
Comment the posture of a defense dossier.

The appropriate revision is editorial compression and reordering. It does not
require more science, another experiment, a deployment-frequency study, or a
mechanical Introduction/Methods/Results/Discussion structure. R2 and R3 below are
concrete clarity fixes. R1, R4, and R5 are the highest-value presentation changes;
R6-R8 are preferences that should not become acceptance conditions.

All locations below refer to the reviewed venue `main.tex`.

## Findings

### R1 — Lead the body with the singleton mechanism

**Priority:** high-priority editorial revision, not a validity defect.

**Location:** introduction, lines 46-51; setup, lines 55-91; Proposition 1,
lines 100-119; example, lines 198-200. PDF pages 1-3.

**Problem:** the abstract tells the reader the attack, but the body begins with
an intention (“The purpose of this note is to identify...”), enters notation,
describes the full update, and then presents a more general certificate. The
decisive case appears as “In particular” inside that theorem. A reader should
not have to infer the simple mechanism while carrying the general case.

**Concrete remedy:** immediately after identifying the source's confidentiality
claim, state the result and its reason in plain prose: in a one-insertion
window, occupancy identifies all shares of that insertion; XOR reconstructs
the payload, including its domain suffix. Then establish why that publication
is allowed. After the representation equation, state the singleton identity
first and present the general occupancy-count result as its extension. The
existing theorem can remain, but rename it to reflect the confidentiality
finding or preface it with a short singleton derivation. Move the three-word
example beside the derivation if it earns its space there; its current late
position makes it an illustration of testing rather than of the attack.

**Evaluation criterion:** after the first body paragraph, a reader can answer
who learns what, which permitted execution causes it, and which public operation
reveals it. The generalization must not obscure that the exact individual
identifier recovery is guaranteed for the singleton case.

### R2 — Define the core symbols and remove the two meanings of “support”

**Priority:** must-fix clarity.

**Location:** equation (1) and surrounding text, lines 55-68; Proposition 2,
lines 132-145; “endpoint” terminology, lines 129-130, 229, and 245.

**Problem:** `S_i` and `Z_j` are used without an explicit definition of the
selected-position set and the stored cell payload, and concatenation is denoted
without being named. Their intended meanings are inferable but needlessly cost
attention. More seriously for a general journal reader, “disjoint supports”
means sets of cell positions in Proposition 1 and sets of possible random views
in Proposition 2, only a few paragraphs apart. The later switch from
“adjacent-domain identifier” to “endpoint” also invites a stronger reading than
the result establishes.

**Concrete remedy:** before equation (1), say: “Let `S_i` be the set of positions
selected by successful insertion `i`, and let `Z_j` be the payload stored in
cell `j`.” Name concatenation when defining `T_i=P_i || N_i`. In Proposition 2,
replace the final phrase with “the two complete payload views have disjoint
sets of possible values” or state directly that the recovered suffix identifies
which identifier was encoded. Use “adjacent-domain identifier” consistently in
claim-bearing sentences. One sentence can explain that registered identifiers
identify publicly registered domains; no extra game or model is needed.

**Evaluation criterion:** every symbol in equation (1) is defined locally, a
reader never has to choose between two meanings of “support,” and no sentence
suggests recovery of a complete path, endpoint pair, hidden data identifier, or
signer identity.

### R3 — Make the verification table self-contained about what was checked

**Priority:** must-fix clarity.

**Location:** Table 1, lines 184-195; methods paragraph, lines 169-175.

**Problem:** “Separately seeded stored arrays” names a generation method, not
the tested case. The row omits that the 64 arrays are singletons, whereas the
caption allows either exact identifier recovery or aggregate recovery. A
reader cannot tell what assertion those 64 zero failures establish without
opening Supplement S1. The first exhaustive row also leaves `lambda=3`
implicit in “3-bit free shares.” This is a reporting-label defect, not a
request for more tests.

**Concrete remedy:** label the three rows by the assertion and configuration:
singleton suffix recovery (`c=1`, `kappa=3`, `lambda=3`, `ell=2`); two disjoint
insertions, aggregate suffix recovery (`c=2`, existing parameters); seeded
singleton suffix recovery (`c=1`, existing parameters). Retain the enumeration
description needed to interpret the case counts. Define “failure” as mismatch
between recovered and encoded identifier, or encoded aggregate, as applicable.
Keep the existing sentence that proofs establish the result and finite checks
verify the implementation.

**Evaluation criterion:** Table 1 alone identifies the input class and equality
checked for every row. No reader can mistake 64 successful seeded singletons
for evidence about typical mixed or overlapping batches.

### R4 — Put the two distinctions from the source's analysis together

**Priority:** high-priority editorial revision.

**Location:** privacy-game discussion, lines 160-165; conclusion's opening,
lines 238-243.

**Problem:** the text explains the difference from the data-identifier game in
Section 2, but waits until the conclusion to introduce the separate distinction
from guessed-tuple acceptance in source Equation (27). That is new analytical
material in the closing section. It also fragments the answer to the reader's
natural question: why does the published analysis not cover this disclosure?

**Concrete remedy:** place the Equation (27) paragraph immediately after the
privacy-game distinction. State positively that the observer reads an encoded
suffix from an identified complete share set, whereas the source calculation
concerns guessed tuples passing validation. These are two distinct comparisons;
do not conflate Equation (27) with the data-identifier game. Explicitly mark
source-article section, theorem, algorithm, and equation locators where the
reference could be mistaken for this Comment's numbering. Leave the conclusion
to state the consequence and the unmeasured deployment frequency.

**Evaluation criterion:** before the verification section, the reader can
explain both distinctions in one sentence each. The conclusion introduces no
new source result or attack premise.

### R5 — Consolidate scope statements and give the protocol-specific point a positive formulation

**Priority:** high-priority editorial revision.

**Location:** lines 37-38, 83-91, 124-130, 157-165, 170-175, 208-214,
224-234, and 245-252.

**Problem:** several necessary limitations are repeated alongside unrelated
nonclaims: maliciously formed tables, repeated reads, adaptive queries,
download/parsing costs, signer recovery, raw data, full paths, a new leakage
calculus, an OKVS break, repaired-protocol security, and cryptographic primitives.
The accumulation weakens claim salience. In particular, the abstract ends by
disclaiming novelty, and the discussion opens with another such disclaimer.
Terms such as “marginal distribution shaping,” “linear coset-encoding,” “rank
deficits,” and “its increment” introduce a new vocabulary for an argument already
made using elementary XOR.

**Concrete remedy:** keep each necessary boundary once, at its point of use:
honest passive snapshot with the model; singleton versus aggregate with the
result; the separate privacy target with interpretation; unmeasured frequency
with implications; and no complete repair with repair observations. Replace the
novelty-defense paragraph's center of gravity with: “The protocol-specific issue
is that public occupancy identifies a complete set of shares.” An established
linear-observation citation can follow in one sentence. Reduce the list of
unclaimed attacks and move detailed cost accounting or repeated-read remarks
to the supplement if retained. End the abstract with the implication for the
stated claim, not a disclaimer about general XOR theory.

**Evaluation criterion:** the main text still states all assumptions needed for
the claim and all material limits, but each paragraph advances one positive
point. A deletion pass must not remove the honest-history premise, aggregate
qualification, or distinction from the data-identifier game.

### R6 — Give the abstract a single claim-to-implication arc

**Priority:** preference; the current abstract is already serviceable.

**Location:** lines 23-39.

**Problem:** the first ten lines work well, but the final sentences turn into
a contents list (artifact, privacy game, original GBF comparison) followed by a
negative novelty claim. The long verbal description of `w=c*kappa` also costs
space relative to the main singleton finding.

**Concrete remedy:** retain the initial confidentiality target, allowed
singleton, public XOR mechanism, and deterministic success. Describe the
aggregate extension in a shorter sentence; state its aggregate-only nature.
Summarize verification in one clause and close with the construction/claim
implication. A possible replacement appears below.

**Evaluation criterion:** the abstract remains understandable without notation
or the source paper, and a reader can distinguish the primary exact recovery
from the secondary aggregate disclosure.

### R7 — Use a compact Comment hierarchy; keep the venue title if required

**Priority:** preference, not an acceptance condition.

**Location:** section titles, lines 44, 53, 93, 167, 206, and 236; title,
lines 13-14.

**Problem:** a single subsection 1.1 adds hierarchy without partitioning its
parent. “Reproduction methods and results” sounds more like an experimental
article than this exact counterexample. “Discussion and established baselines”
plus a separate “Conclusion and limits” creates two successive places for
interpretation. The long venue title is not an editorial defect if it follows
the required Comment convention.

**Concrete remedy:** omit subsection 1.1, shorten the verification heading, and
combine the existing final discussion/conclusion after moving Equation (27)
earlier. A four-section outline appears below. Retain the venue's Comment title;
the canonical descriptive title already communicates the subject effectively.
Do not add IMRAD sections merely to resemble a full research article.

**Evaluation criterion:** headings reveal the argument's sequence, not an
administrative checklist. There are no singleton subsections and no separate
heading whose sole job is to repeat limitations.

### R8 — Keep the first equation with its definitions after reflow

**Priority:** minor layout preference.

**Location:** PDF page 1 bottom/page 2 top, equation (1).

**Problem:** equation (1) ends page 1 while its `N_i` and `P_i` definitions begin
page 2. This reinforces R2's notation burden. All five pages are otherwise
readable: no clipping, overlap, broken mathematical glyphs, or unusable table
was observed at 100-dpi page inspection. The table's close row spacing is
acceptable for this short Comment.

**Concrete remedy:** first perform substantive reordering. Then keep the
definition sentence before the display or keep the display and following
definition paragraph together. Avoid a manual page-break patch before the
text settles.

**Evaluation criterion:** the first equation and definitions are visible
together in the final PDF, with no new large blank space or broken paragraph.

## Suggested outline

1. **The confidentiality claim and allowed public view.** Source target;
   one-paragraph attack sketch; representation and local notation; evidence
   that an authentic singleton snapshot is allowed; passive observer.
2. **Exact disclosure and its scope.** Singleton derivation; general occupancy
   certificate and short proof; aggregate-only qualification; short explanation
   of uniform individual shares versus revealing joint view; two-world comparison;
   distinctions from the identifier game and guessed-tuple acceptance.
3. **Reproducibility checks.** One paragraph distinguishing theorem from checks;
   accurately labeled table; concise artifact pointer. The numerical example
   belongs by the singleton derivation if retained.
4. **Implications.** Explain the relevant original-GBF padding/access contrast;
   state exactly what simple padding or secret masking changes about this
   statistic; retain one sentence that this is not a complete repair. Close with
   the consequence for the metadata-confidentiality claim, the limits of a
   minimum-count rule, and unknown operational frequency.

The marginal-uniformity fact need not remain a separately numbered proposition;
an explanatory paragraph with its short argument would be enough. This is an
optional compression, not a demand to remove the fact or its justification.

## Example opening

> Qin et al. state that GBFPlus conceals adjacent-domain relationships from
> ordinary ledger observers [source Section 4.2 and Table 1]. We show that an
> allowed public snapshot can nevertheless reveal its adjacent-domain identifier
> exactly. When a time window closes after one successful insertion, the
> occupied cells are precisely that insertion's XOR shares. XORing their
> payloads reconstructs the encoded word, whose suffix is the adjacent-domain
> identifier. The attack needs neither a regulator secret nor a query token.
> The relevant publication and representation rules are given below.

This opening should be checked against the final source-premise review; it is a
prose reorganization of the current manuscript's claims, not an independent
verification of those premises.

## Example abstract

> GBFPlus aims to conceal adjacent-domain relationships from ordinary ledger
> observers while supporting authorized tracing. We identify an allowed
> execution that discloses the adjacent-domain identifier exactly. When a time
> window closes after one successful insertion, public occupancy identifies
> every share of the inserted payload; XORing those shares recovers the payload,
> including the identifier stored in its suffix. This holds for every choice of
> construction randomness and requires neither a query token nor a candidate
> data identifier. A public occupancy test extends the attack to disjoint
> insertion supports, where it reveals an aggregate XOR rather than individual
> identifiers. The result concerns adjacent-domain metadata, distinct from the
> source paper's data-identifier privacy game. Finite exhaustive checks and a
> share-level implementation reproduce the disclosure. The stated metadata
> confidentiality claim must therefore account for allowed partial batches and
> the complete public payload view.

## Round-2 reading test

Read the revision once without the supplement. Within the first page, identify
the protected item, observer, allowed execution, and revealing operation. At
the theorem, distinguish exact individual recovery from aggregate recovery.
At the comparison, distinguish the two privacy targets and the acceptance
calculation. At the table, identify each input class and checked equality. The
closing paragraph should follow from that argument without introducing a new
premise. Verify these tasks directly rather than rewarding a change merely
because it follows this proposed outline.
