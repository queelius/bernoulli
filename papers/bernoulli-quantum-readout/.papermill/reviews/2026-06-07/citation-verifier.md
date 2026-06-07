# Citation and Bibliography Verification

**Paper**: A Forward (epsilon, omega) Calculus for Quantum Readout Error
**Date**: 2026-06-07
**Reviewer role**: citation-verifier

**Caveat (declared)**: no live web/DOI resolution in this run. I verified
*internal* citation integrity exhaustively (every key, every direction, the
bibtex build) and I sanity-check external entries against my own knowledge,
flagging anything I cannot independently confirm as "needs external check"
rather than asserting correctness.

## Internal integrity  -  CLEAN

- **16 bib entries, 16 cited, 0 uncited, 0 undefined.** I enumerated the keys in
  references.bib, the \cite[pt] keys in main.tex, and the rendered \bibitem keys
  in main.bbl. All three sets are identical. There is no cited-but-missing key
  and no defined-but-uncited entry.
- **bibtex build**: zero real warnings (no `Warning--` lines), zero errors.
  Every entry carries a location field (journal / booktitle / note). The
  "missing$/empty$" tokens in main.blg are plainnat.bst internal function names,
  not warnings about this bibliography.
- **plainnat + numbers,square** renders all 16 references; the final pass has no
  undefined-citation warnings.

So the **state file's claim of "16 entries, all cited, zero placeholders" is
correct** (an earlier line in the same state file says "16 entries"; the bib has
16; consistent).

## External entries  -  plausibility and attribution

For each, I report: plausible/real (to my knowledge), attribution as used in the
paper, and whether external verification is still advisable.

- **bloom1970** -- Bloom, "Space/Time Trade-offs in Hash Coding with Allowable
  Errors," CACM 13(7):422-426, 1970. Real, canonical, correctly attributed. The
  paper uses it only as the "one-sided (omega=0) corner" exemplar. Fine.
- **nation2021m3** -- Nation, Kang, Sundaresan, Gambetta, "Scalable Mitigation of
  Measurement Errors on Quantum Computers," PRX Quantum 2(4):040326, 2021. This
  matches my knowledge of M3. Correctly used as the scalable inverse mitigator.
  M3 is matrix-free/iterative rather than literal dense matrix inversion, so the
  umbrella label "matrix-inversion paradigm" is roughly fair but slightly loose;
  the paper does hedge ("approximately invert it," "scalable realizations"),
  which is adequate. No finding.
- **bravyi2021mitigating** -- Bravyi, Sheldon, Kandala, McKay, Gambetta,
  "Mitigating Measurement Errors in Multiqubit Experiments," PRA 103(4):042605,
  2021. Matches my knowledge. Correctly used. **Relevant to the open TODO**: this
  is the paper that introduces the continuous-time Markov process (CTMP)
  correlated-readout model the sec:scope TODO wants to cite. If that recollection
  is correct, the paper *already has in its bib* the citation its CTMP TODO is
  looking for, and could resolve the first TODO by pointing to bravyi2021mitigating
  for CTMP. **Recommend external confirmation** that CTMP originates in (or is
  presented in) bravyi2021mitigating before naming it; the TODO comment itself
  says as much ("Bravyi et al. discuss a continuous-time Markov process model;
  verify before citing by name").
- **tannu2019mitigating** -- Tannu, Qureshi, "Mitigating Measurement Errors in
  Quantum Computers by Exploiting State-Dependent Bias," MICRO-52, 2019. Matches
  my knowledge. Correctly attributed as the state-dependent (asymmetric) bias
  source. The "roughly 8-30%" figure attributed to it in sec:related (e) is a
  specific empirical quantitative claim; **needs external check** that this range
  is what the paper reports.
- **hicks2021readout** -- Hicks, Bauer, Nachman, "Readout Rebalancing for Near-
  Term Quantum Computers," PRA 103(2):022407, 2021. Matches my knowledge.
  Correctly attributed (readout rebalancing exploiting asymmetry).
- **adams2015typetheory** -- Adams, Jacobs, "A Type Theory for Probabilistic and
  Bayesian Reasoning," TYPES 2015 (arXiv:1511.09230). Plausible and matches my
  knowledge of the Adams-Jacobs line. Correctly used as foundational, not a rate
  calculus.
- **cho2015effectus** -- Cho, Jacobs, Westerbaan, Westerbaan, "An Introduction to
  Effectus Theory," arXiv:1512.05813, 2015. Plausible and matches my knowledge.
  Correctly characterized (algebra of predicates, effect algebras; not a device
  readout-rate model). The "no (epsilon,omega) rate-propagation rules"
  distinction is fair: effectus is structural.
- **vonneumann1956** -- von Neumann, "Probabilistic Logics and the Synthesis of
  Reliable Organisms from Unreliable Components," Automata Studies, 1956. Real,
  canonical. **Attribution caveat**: the paper cites it (with pippenger1988) as
  owning the *parity identity* eq:parity. von Neumann 1956 is about reliable
  computation from unreliable components broadly (majority/restoring organs); the
  specific +-1-encoding parity bias identity 1/2(1 - prod(1-2q_i)) is more
  precisely a folklore/coding-theory result (it is the standard "probability that
  a sum of independent bits is odd," and appears in the Fourier-analysis-of-
  Boolean-functions tradition). Citing von Neumann and Pippenger as the lineage
  of "noisy Boolean formula reliability" is defensible, but the *exact* parity
  formula is not original to either and a reader may want a more precise pointer
  (O'Donnell's Analysis of Boolean Functions, or a coding-theory text). **Minor
  attribution looseness**, flagged for the author's judgment.
- **pippenger1988** -- Pippenger, "Reliable Computation by Formulas in the
  Presence of Noise," IEEE Trans. IT 34(2):194-197, 1988. Real, correctly
  attributed to the noisy-formula reliability line. Same caveat as above about
  the *exact* parity identity vs the general noisy-formula theory.
- **pucha2021certification** -- the bib entry's authors are **Krawiec, Pawela,
  Puchala** with title "Excluding False Negative Error in Certification of
  Quantum Channels," Sci Rep 11:21716, 2021. **Cite-key/attribution mismatch
  worth noting**: the key is `pucha2021certification` (suggesting Puchala as
  lead) but Puchala is the *third* author; the in-text \citet renders as the full
  numbered ref under plainnat so this does not surface in the PDF, but the key is
  mildly misleading for anyone reading the bib. The paper/title/journal are
  plausible and match the asymmetric (false-negative-free) certification idea the
  paper invokes. **Needs external check** that the title, author order, volume,
  and DOI (10.1038/s41598-021-00444-x) are exactly right; this is a specific
  factual claim I cannot confirm offline.
- **fowler2012surface** -- Fowler, Mariantoni, Martinis, Cleland, "Surface Codes:
  Towards Practical Large-Scale Quantum Computation," PRA 86(3):032324, 2012.
  Real, canonical, correctly used as QEC/syndrome background.

## Framework self-citations  -  uncheckable as written

The five Bernoulli citations (bernoulliSets, bernoulliComposition, bernoulliMaps,
bernoulliMeasures, bernoulliRelations) are all `@unpublished` with note
"Companion paper, Bernoulli type theory," **no DOI, no URL, no arXiv/Zenodo
locator**. They build cleanly but a reader cannot locate them. Per the
publication strategy these are Zenodo preprints; the bib should carry the Zenodo
DOIs once minted. As written, the paper's most distinctive claim (the
unification) leans on five locator-free references. **Minor (C-self)**, with
novelty implications noted by the novelty-assessor.

## Missing-citation check (things a reader expects)

- The parity identity could use a precise canonical pointer beyond von
  Neumann/Pippenger (see above).
- The CTMP correlated-readout citation is an open TODO; bravyi2021mitigating may
  already cover it (see above). This is a *known* gap, not a new finding.
- No other obviously-expected citation is missing for a perspective paper of this
  scope. The five-neighbor positioning is well covered bibliographically.

## Findings

- **Minor (C1)**: The five framework self-citations are `@unpublished` with no
  DOI/URL. Add Zenodo locators (or a stable URL) so the unification claim is
  followable. Build is unaffected; readability and verifiability are.
- **Minor (C2)**: Parity-identity attribution to von Neumann 1956 / Pippenger
  1988 is defensible for the noisy-formula *lineage* but loose for the *exact*
  formula, which is folklore/coding-theory. Consider an additional precise
  pointer, or rephrase to "in the tradition of."
- **Suggestion (C3)**: Rename the cite-key `pucha2021certification` to reflect the
  lead author (Krawiec) to avoid a misleading key; cosmetic, key-only.
- **Needs external verification (not findings, flagged honestly)**: the exact
  bibliographic fields of pucha2021certification (title/authors/volume/DOI); the
  "8-30%" empirical figure attributed to tannu2019mitigating; whether CTMP is in
  bravyi2021mitigating. These are factual claims I could not confirm offline.

Internal citation integrity is perfect. The only substantive citation finding is
the locator-less self-cites (C1); the rest are minor attribution polish and items
requiring an external pass.
