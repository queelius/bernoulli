# Errata: A Forward (epsilon, omega) Calculus for Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes

Date: 2026-10-21. Author: Alexander Towell.

This is the final version of the preprint. It will be deposited on Zenodo as a
new version under concept DOI 10.5281/zenodo.20584894, superseding version
10.5281/zenodo.20618108 (v5). It is superseded by the monograph *Bernoulli
Types: Two-Sided Error in Approximate Membership, Retrieval, and Computation*,
Chapter 19 (The Operator Representation), together with Chapter 3 (Boolean
Algebra Under Noise), the quantum-readout paragraph of Chapter 9, and the
quantum-contextuality section of Chapter 16
(<https://metafunctor.com/latex/bernoulli-monograph/book.html>).
License unchanged: CC BY 4.0.

The manuscript was submitted to Quantum Science and Technology, was rejected,
and is retired from venue submission. The title is unchanged. The base
`main.tex` was edited; `venues/` was not touched and is now stale relative to
this version.

## Corrections

1. **False general propagation claim withdrawn (abstract; Sec. 1, contribution
   paragraph; Sec. 3.5, `prop:tensor`; Sec. 7).** The previous versions said
   the pair (epsilon, omega) is carried "through an entire Boolean tree" and
   that the rate of any Boolean function of the readouts depends on the
   channels "only through the closed forms". That is false: the output of an
   AND gate is not a two-rate bit, because its false-positive rate depends on
   which false latent word occurred (0.0004 at latent word 00 versus 0.018 at
   01 with epsilon = 0.02, omega = 0.10). `prop:tensor` is now "Per-latent-
   assignment propagation": for a fixed latent word, each node's probability of
   reading 1 is propagated by the product, complement, OR, and parity
   recurrences (new eq. `eq:node-recurrence`); a single output FPR/FNR requires
   averaging over latent words. New remark `rem:no-pair` gives the
   counterexample: (b0 AND b1) OR b2 at latent word 010 has exact error
   1 - (0.982)(0.98) = 0.03764, while reusing the AND corner rate and then
   applying the OR rule gives 0.020392. The correctly conditioned product
   formulas (`thm:andor`, `cor:parity-asym`) are kept. Evidence:
   `.research/publication-triage/candidates/quantum-readout/assessment.md`
   (claim Q2), recomputed for this erratum.
2. **Faithfulness scope corrected (Sec. 1, "Why this is sound"; Sec. 2.2;
   Sec. 3.6 honesty clause; Sec. 6 item 3; Sec. 7).** The model was said to be
   faithful "precisely when the density matrix is diagonal". The correct
   condition is on the detector: if the measurement effects are diagonal,
   M_b = sum_t A(b|t) |t><t|, then Tr(M_b rho) = sum_t A(b|t) rho_tt for any
   state rho (new eq. `eq:povm`), so coherent and entangled inputs are
   covered for fixed-basis readout. The Bell / Kochen-Specker remark now says
   the model does not supply a joint distribution across incompatible
   measurement settings. The majority-vote remark no longer appeals to a
   "diagonal readout sector".
3. **Parity identity credited (Sec. 3.4; Sec. 4.4; Sec. 5(c); Sec. 6 item 4).**
   Theorem `thm:parity` is Lemma 1 of Gallager (1962) and Matsui's piling-up
   lemma (1993). Sec. 4.4 previously said it was attributed "to prior art"
   without citing a source.
4. **"No reusable forward calculus exists" withdrawn (Sec. 1; Sec. 5(b),(c),(d);
   Sec. 6 item 4).** Forward propagation of input-pattern-dependent,
   asymmetric error through combinational networks is Parker and McCluskey
   (1975) and probabilistic transfer matrices (Krishnaswamy et al., 2008). The
   paper's calculus is a specialization of those methods to readout. Sec. 5(b)
   no longer calls effectus theory "the most important neighbor".
5. **Asymmetric response matrices credited (Sec. 1; Sec. 5(a); Sec. 6 item 4).**
   Smith et al. (2021) already use general asymmetric response matrices and
   tensors of asymmetric single-qubit matrices before deliberately
   symmetrizing by bit-flip averaging. The sentence saying applied tooling
   "symmetrizes ... losing the very asymmetry" was narrowed.
6. **Crosstalk truncation compared with an established baseline (Sec. 1;
   Sec. 4.6, new paragraph; Sec. 6 item 4; Sec. 7).** Hamilton et al. (2020)
   reconstruct readout distributions from one- and two-qubit cumulants.
   Projected onto parity (all partial matchings of pair covariances, higher
   cumulants zero), that baseline gives 0.0643 at lambda = 0.01 on the chain
   model, against exact 0.0623 and the paper's first-order 0.0735 (at
   lambda = 0.05: 0.110, 0.070, 0.228). The baseline numbers come from the
   October 2026 audit (`results.json`, key `crosstalk`) and are labeled in the
   text as computed for this revision, not reported by Hamilton et al.
7. **Chain composition rule scoped (Sec. 3.3; Sec. 4.5 remark on majority and
   feed-forward).** `cor:composition` gives the probability that some stage
   errs. Applied to feed-forward chains, it is an upper bound on final-output
   error when errors can cancel, not the final-output error itself.
8. **Positioning rewritten (abstract; Sec. 1; Sec. 4.3; Sec. 5; Sec. 6 item 4
   "Originality, precisely"; Sec. 7).** The paper now claims no novelty for its
   methods. What it offers: known tools applied to readout-derived bits,
   worked numbers on the ibm_hanoi calibration (the linear rule overestimates
   the 27-qubit cold-word parity error by 37%), and the identification of
   readout error with the Bernoulli error model.

Also changed: the date line now reads "Final version, October 2026"; the
status and errata box (`status_errata.tex`) is input after the abstract; the
`bernoulliRelations` entry now carries that paper's current title ("Error
Contracts for Approximate Relations") and its concept DOI
10.5281/zenodo.20602265.

## Citations added

Each DOI was checked against the Crossref REST API on 2026-10-21 (title and
authors match), unless marked otherwise.

- `gallager1962ldpc`: R. G. Gallager, *Low-Density Parity-Check Codes*, IRE
  Transactions on Information Theory 8(1):21-28 (1962). 10.1109/TIT.1962.1057683.
  (Crossref lists the journal under its later IEEE name.)
- `matsui1993linear`: M. Matsui, *Linear Cryptanalysis Method for DES Cipher*,
  EUROCRYPT '93, LNCS, pp. 386-397 (1994). 10.1007/3-540-48285-7_33.
  (LNCS volume number 765 added from the series; Crossref does not list it.)
- `parker1975probabilistic`: K. P. Parker and E. J. McCluskey, *Probabilistic
  Treatment of General Combinational Networks*, IEEE Trans. Computers
  C-24(6):668-670 (1975). 10.1109/T-C.1975.224279.
- `krishnaswamy2008ptm`: S. Krishnaswamy, G. F. Viamontes, I. L. Markov,
  J. P. Hayes, *Probabilistic Transfer Matrices in Symbolic Reliability
  Analysis of Logic Circuits*, ACM TODAES 13(1), article 8 (2008).
  10.1145/1297666.1297674.
- `smith2021bitflip`: A. W. R. Smith, K. E. Khosla, C. N. Self, M. S. Kim,
  *Qubit Readout Error Mitigation with Bit-Flip Averaging*, Science Advances
  7(47):eabi8009 (2021). 10.1126/sciadv.abi8009.
- `hamilton2020scalable`: K. E. Hamilton et al., *Scalable Quantum Processor
  Noise Characterization*, IEEE QCE 2020, pp. 430-440.
  10.1109/QCE49297.2020.00060.
- `tuziemski2023crosstalk`: J. Tuziemski et al., *Efficient Reconstruction,
  Benchmarking and Validation of Cross-Talk Models in Readout Noise in
  Near-Term Quantum Devices*, arXiv:2311.10661 (2023).
  10.48550/arXiv.2311.10661 (arXiv DOI, verified via DataCite, not Crossref).

## Claims withdrawn or narrowed

- The (epsilon, omega) pair propagates through an entire Boolean tree; any
  Boolean function's rate depends only on the closed forms. Withdrawn.
- The latent-value model is faithful precisely when the density matrix is
  diagonal. Replaced by the diagonal-POVM condition, valid for any state.
- There is no reusable, closed-form, forward calculus preserving the
  asymmetry; the forward asymmetric Boolean calculus is the paper's new
  artifact. Withdrawn.
- Applied tooling symmetrizes and loses the asymmetry. Narrowed.
- The chain composition rule gives the error of a feed-forward chain.
  Narrowed to "some stage errs" (an upper bound).

## Build

`pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
(the paper's documented command). Result: 0 LaTeX errors, 0 undefined
references, 0 undefined citations, 0 BibTeX warnings, 0 overfull boxes,
27 bibliography entries resolved. 20 pages (previous build 17). The status box
renders at the top of page 2, directly after the abstract.

## Known remaining issues (not fixed in the freeze)

- `venues/quantum/` and any other venue ports still contain the withdrawn
  claims; they were deliberately not edited.
- The section title "Introduction: the gap" and the section name "The forward
  (epsilon, omega) calculus" were kept for continuity; the text under them no
  longer claims a gap or a new calculus.
- The PTM predecessor (Krishnaswamy et al., 2008) was credited on the basis of
  the October audit, which read indexed primary text but not the complete PDF.
- Monograph chapters 16 and 19 use "diagonal of the density operator"
  language for the readout sector; they may need the same POVM scope
  correction (outside this paper).
