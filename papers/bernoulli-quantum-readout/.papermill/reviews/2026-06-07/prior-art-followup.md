# Prior-art and citation-verification pass (live web search)

Paper: A Forward $(\epsilon,\omega)$ Calculus for Quantum Readout Error
Date: 2026-06-07
Method: live WebSearch / WebFetch against primary sources (publisher pages, arXiv, ar5iv, PMC, ACM, GitHub). Every claim below carries a URL. "Uncertain" is used where a primary source could not be opened.

---

## Q1. The core novelty hinge (M3 positioning)

**Claim under test (intro):** "There is at present no reusable, closed-form, forward calculus that answers this question while preserving the asymmetry."

### Verdict: novelty stands (no direct competitor found). One nearby paper warrants a one-line citation to harden the claim.

### Evidence

**(a) Is there a prior reusable, forward, closed-form, asymmetric Boolean-plus-tensor readout calculus?**

- The closest neighbors split cleanly into three non-overlapping buckets, none of which is the paper's object:
  1. **Inverse mitigation** (assignment-matrix inversion). See Q1(b).
  2. **Single-symmetric-rate noisy-Boolean-formula reliability**: the von Neumann / Pippenger tradition and its modern statistical-physics treatment (Mozeika and Saad, "On reliable computation by noisy random Boolean formulas", and "Noisy Random Boolean Formulae"). These propagate error through gates but use a single symmetric flip rate and study noise thresholds, not a two-rate $(\epsilon,\omega)$ bookkeeping. https://arxiv.org/pdf/1206.4851 , https://arxiv.org/pdf/1003.3806
  3. **Forward circuit success-rate predictors**: e.g. "Quantum Vulnerability Analysis" (https://arxiv.org/pdf/2207.14446) and Pauli-error-propagation reschedulers (https://arxiv.org/pdf/2201.12946). These predict an aggregate circuit success probability from gate-level Pauli/depolarizing error, not a symbolic asymmetric two-rate calculus over Boolean post-processing of measured bits, and they do not unify with classical probabilistic data structures.
- A general search for "asymmetric two-rate error propagation AND/OR/NOT closed form Bloom filter quantum readout unification" returned no source that unifies these; the search tool itself reported "The search results don't contain specific literature that directly unifies all these concepts ... into a single unified framework." https://arxiv.org/pdf/1206.4851
- "Quantum Bloom filter" work (e.g. IEEE TQE 2021, https://ieeexplore.ieee.org/document/9336250/) is a quantum data structure, not an error-model unification, and is unrelated to the paper's classical-shadow framing. It is not a competitor, but the title proximity means a reviewer may raise it; the paper need not cite it.

**(b) Is tensored/local readout mitigation (M3, Bravyi CTMP, IBM tooling) forward+symbolic+asymmetric, or inverse+numerical+per-circuit?**

- **M3 (mthree) is strictly inverse, numerical, and per-circuit.** The official repo describes it as solving "for corrected measurement probabilities using a dimensionality reduction step followed by either direct LU factorization or a preconditioned iterative method," i.e. it takes raw observed counts and recovers a corrected distribution. It does not symbolically propagate rates forward through derived bits (parities, syndromes, Boolean functions). https://github.com/Qiskit/qiskit-addon-mthree
- M3 is explicitly **matrix-free**: it "need not explicitly form the assignment matrix, or its inverse" and works in the reduced subspace of observed bitstrings, per the M3 paper (Nation et al., arXiv:2108.12518) and Qiskit docs. This reinforces that it is an inverse solver on measured data, not a forward predictor. https://arxiv.org/pdf/2108.12518 , https://qiskit.github.io/qiskit-addon-mthree/
- Per-qubit calibration in M3 is numerical (1Q calibration matrices on physical qubits); the tensored/Kronecker assignment matrix the paper writes as Eq. (kron) is exactly the LocalReadoutMitigator object, and it too is used **inverse-wise** (applied/inverted against observed counts), confirmed in Qiskit Experiments docs. https://qiskit-community.github.io/qiskit-experiments/dev/manuals/measurement/readout_mitigation.html
- The one paper a reviewer is most likely to wave at as a competitor is **"Readout Error Mitigation for Mid-Circuit Measurements and Feedforward"** (arXiv:2406.07611). It addresses derived/feedforward measurement outcomes, which overlaps the paper's motivating examples. UNCERTAIN on its internal method: the arXiv PDF would not render as text. From its title and venue it is a mitigation (inverse) paper for mid-circuit/feedforward readout, not a forward closed-form asymmetric Boolean calculus, but this should be confirmed by reading the actual PDF before relying on the distinction in print. https://arxiv.org/pdf/2406.07611

### Recommended action
- **Keep the novelty sentence**, it survives. The forward/inverse, symbolic/numerical, reusable/per-circuit, two-rate/single-rate distinctions are all corroborated by primary sources for M3 and the tensored mitigators.
- **Harden it** by reading arXiv:2406.07611 (mid-circuit measurement / feedforward mitigation) and adding one sentence in sec:related (a) that names it as the nearest derived-bit mitigation work and notes it is still inverse/numerical (assuming the read confirms this). This pre-empts the most likely reviewer objection. Until the PDF is read, treat the "it is inverse" attribution for that specific paper as UNCERTAIN.
- Optionally add Mozeika and Saad (noisy random Boolean formulas) to the (c) paragraph as the modern continuation of the von Neumann / Pippenger single-symmetric-rate tradition, sharpening the "single symmetric rate" contrast.

---

## Q2a. pucha2021certification fields and lead author

### Verdict: CONFIRMED. All fields correct. Lead author is Aleksandra Krawiec.

### Evidence
- Author order as published: **Aleksandra Krawiec, Łukasz Pawela, Zbigniew Puchała** (Krawiec first and corresponding). Confirmed on the publisher page and on PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC8571408/ , https://www.nature.com/articles/s41598-021-00444-x
- Title: "Excluding false negative error in certification of quantum channels" (the bib capitalizes per-word; the published title is sentence case, harmless for plainnat). CONFIRMED.
- Journal Scientific Reports, **volume 11, article number 21716, 2021, DOI 10.1038/s41598-021-00444-x**. All CONFIRMED. https://www.nature.com/articles/s41598-021-00444-x
- Note: there is an **Author Correction** (2022) to this article (PMID 35414653 / PMC9005725). It is an erratum, not a retraction; no need to cite it, but it confirms the record is stable. https://pubmed.ncbi.nlm.nih.gov/35414653/
- arXiv preprint is 2106.02375 (consistent). https://arxiv.org/abs/2106.02375

### Recommended action
- **Rename the cite key** from `pucha2021certification` to `krawiec2021certification` (lead author is Krawiec, not Puchała). All in-text uses (currently one, in sec:related (d)) update with it.
- No field edits needed. Optionally normalize the title to sentence case to match the published form, though plainnat will not care.

---

## Q2b. tannu2019mitigating: the "8 to 30%" range and the asymmetry/T1 attribution

### Verdict: CONFIRMED. The "8% to 30%" figure is verbatim from the abstract, and the paper does establish and exploit state-dependent (asymmetric) bias attributable to energy relaxation.

### Evidence
- Abstract, verbatim: "qubit measurement is typically the most error-prone operation on a quantum computer, **with measurement errors ranging from 8% to 30%** reported on current machines." So the paper's sec:related "roughly 8 to 30%" is accurate. https://www.semanticscholar.org/paper/Mitigating-Measurement-Errors-in-Quantum-Computers-Tannu-Qureshi/f54130052a99f2cbc4609afa3fafe0c81a184e65 , https://dl.acm.org/doi/10.1145/3352460.3358265
- State-dependent (asymmetric) bias, with explicit relaxation mechanism: on IBM-Q5 the all-zero state reads at fidelity 84%, dropping to 62% for the all-one state, an asymmetry the paper attributes to "qubits' natural tendency to relax to the lower energy state." This is exactly the $\omega > \epsilon$ ($1 \to 0$ biased) regime the paper's rem:t1 invokes. https://memlab.ece.gatech.edu/papers/MICRO_2019_1.pdf
- The title itself, "Exploiting State-Dependent Bias," confirms the paper builds on the asymmetry rather than merely noting it. https://dl.acm.org/doi/10.1145/3352460.3358265

### Recommended action
- **No change required.** The "8 to 30%" attribution is exact. The paper may optionally add the concrete 84% vs 62% all-zero/all-one fidelity datapoint to rem:t1 as a vivid, citable instance of the $T_1$-driven asymmetry; this strengthens the physics motivation with a real number. Verbatim source figure: IBM-Q5, all-zero 84%, all-one 62%.
- Minor: the bib lists pages 279 to 290; this matches the MICRO-52 proceedings record (not separately re-verified against the page range, but consistent with the ACM entry). Treat page range as CONFIRMED-by-consistency.

---

## Q2c. bravyi2021mitigating and the CTMP citation

### Verdict: CONFIRMED. The continuous-time Markov process (CTMP) model for correlated readout error IS in bravyi2021mitigating. This is the correct primary citation for the paper's CTMP "% TODO".

### Evidence
- The paper (Bravyi, Sheldon, Kandala, McKay, Gambetta; arXiv:2006.14044; PRA 103, 042605, 2021) presents "two error mitigation schemes based on **tensor product and correlated Markovian noise models**." https://arxiv.org/abs/2006.14044
- It defines CTMP (Continuous Time Markov Process) as the noise model $A = e^{G}$ with generator $G = \sum_i r_i G_i$, where the $G_i$ include single-qubit ($0 \to 1$, $1 \to 0$) and **two-qubit correlated** generators ($01 \leftrightarrow 10$, $00 \leftrightarrow 11$), explicitly to "account for correlated (cross-talk) errors" from qubit-qubit coupling and readout-resonator spectral overlap. https://ar5iv.labs.arxiv.org/html/2006.14044
- The paper compares exactly three noise models: full A-matrix ($2^n \times 2^n$), tensor product (independent single-qubit), and CTMP (adds two-qubit correlations); CTMP gives roughly 2x lower total-variation distance than tensor product at n = 6,7. https://ar5iv.labs.arxiv.org/html/2006.14044

### Recommended action
- **Resolve the "% TODO" in sec:scope item 2 by citing `bravyi2021mitigating` directly for CTMP.** The model is named, defined, and used there; the TODO's caution ("verify before citing by name") is now discharged. Suggested text: "correlated models (e.g. the CTMP model of Bravyi et al. [bravyi2021mitigating])". Remove the TODO comment.
- The same citation already appears in sec:related (a) and sec:scope item 1, so no new bib entry is needed, the entry is correct as-is (volume 103, article 042605, DOI 10.1103/PhysRevA.103.042605). CONFIRMED.

---

## Q3. Parity-bias identity attribution (von Neumann / Pippenger vs Boolean-function folklore)

### Verdict: The attribution should be SPLIT. von Neumann (1956) and Pippenger (1988) own the noisy-Boolean-formula RELIABILITY tradition (the right citation for "this lineage of analysis"), but the exact $\pm 1$ (Fourier) parity-bias identity $\Pr[\bigoplus X_i = 1] = \tfrac12(1 - \prod_i(1-2q_i))$ is standard Boolean-function-analysis material, not a result original to either of those two papers. Cite O'Donnell for the exact identity.

### Evidence
- The identity is the elementary consequence of the $\pm 1$ encoding $S_i = 1 - 2X_i$, $\mathbb{E}[S_i] = 1 - 2q_i$, and independence, exactly the Fourier/$\pm 1$ machinery that is the foundation of analysis of Boolean functions. O'Donnell's "Analysis of Boolean Functions" establishes that for parity the noise stability is $(1-2\epsilon)^n$ and that parities $\chi_S$ form the Fourier basis; the $(1-2q)$ factor per coordinate is the standard object there. https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf
- von Neumann (1956) and Pippenger (1988) are about reliable computation / formula reliability under noise (thresholds, restoring organs, fault-tolerant formula depth), the RELIABILITY tradition. They are the correct lineage citation for "noisy Boolean formula analysis," but the clean closed-form parity-bias product identity is not a headline theorem unique to them; it is folklore that long predates and surrounds them and is presented as routine in modern Boolean-function-analysis texts. von Neumann: foundational restoring-organ / multiplexing reliability; Pippenger (IEEE Trans. IT 34(2):194-197, 1988, DOI 10.1109/18.2628): formula reliability bounds. Both CONFIRMED as reliability-tradition works, not as the origin of this specific identity.

### Recommended action
- In sec:calculus (the line after thm:parity) and in sec:related (c), **keep von Neumann and Pippenger as the citation for the noisy-Boolean-formula reliability tradition**, but **re-phrase so they are not credited with the exact identity**. Concretely, change wording like "the ... parity identity used by von Neumann and Pippenger" to something like: "Theorem (Parity) is classical, the $\pm 1$/Fourier parity-bias identity standard in analysis of Boolean functions [odonnell2014]; it underlies the noisy-Boolean-formula reliability tradition [vonneumann1956, pippenger1988]."
- **Add a bib entry for O'Donnell** as the citable modern source for the exact identity:
  ```
  @book{odonnell2014,
    author    = {Ryan O'Donnell},
    title     = {Analysis of Boolean Functions},
    publisher = {Cambridge University Press},
    year      = {2014},
  }
  ```
- This is a precision improvement, not a correction of an error; the current text is defensible but slightly over-credits two reliability papers with a folklore identity. The split phrasing is more accurate and more robust to a Boolean-function-analysis reviewer.

---

## Bottom line

**CONFIRMED**
- Q1(b): M3/mthree is inverse, numerical, per-circuit, matrix-free; the tensored assignment matrix is used inverse-wise. The paper's forward/inverse positioning is sound.
- Q1 overall: no direct competitor (reusable + forward + closed-form + asymmetric two-rate + Boolean/tensor + Bloom-filter unification) was found. Novelty claim stands.
- Q2a: krawiec2021certification, all fields correct; lead author Aleksandra Krawiec (rename the key from pucha...).
- Q2b: "8% to 30%" is verbatim from the Tannu-Qureshi abstract; state-dependent/T1-relaxation asymmetry confirmed (84% all-zero vs 62% all-one fidelity).
- Q2c: CTMP is defined and used in bravyi2021mitigating (Section IV, $A = e^G$, two-qubit correlated generators). The "% TODO" can be resolved by citing it. Three-model comparison (full / tensor / CTMP) confirmed.
- Q3: von Neumann and Pippenger own the reliability tradition; the exact parity-bias identity is standard analysis-of-Boolean-functions material (O'Donnell). Split the attribution.

**UNCERTAIN**
- The internal method of arXiv:2406.07611 ("Readout Error Mitigation for Mid-Circuit Measurements and Feedforward"). It is the nearest derived-bit work and is presumed inverse/mitigation from title and venue, but its PDF would not render as text; read it before citing it as inverse-only in print.
- The exact page range 279-290 for Tannu-Qureshi was taken as consistent with the ACM/proceedings record rather than independently line-verified; treat as CONFIRMED-by-consistency, not primary-verified.
