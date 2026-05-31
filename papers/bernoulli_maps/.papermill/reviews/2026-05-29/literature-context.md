# Literature Context Packet, bernoulli_maps

**Paper**: "The algebra of the random approximate map model" (Alexander Towell)
**Date**: 2026-05-29
**Method note**: This packet merges a broad field-survey lens (competing approaches, benchmarks, the current bar for approximate/probabilistic functions) and a targeted-comparison lens (same-problem prior art and the closely related in-family papers). It is grounded in the manuscript's own 15-entry bibliography plus standard reference knowledge of the probabilistic-data-structures and information-theory literature current to the reviewer's knowledge (Jan 2026). No web retrieval was performed; where a claim depends on an external result the reviewer flags the confidence level.

---

## 1. Field map: where this paper sits

The paper generalizes "approximate set" (Bloom-filter-style) machinery to "approximate map" (key to value retrieval) machinery, framing both as instances of a per-input-independent error channel over a function space `Y^X`. The relevant external literatures are these.

### 1a. Approximate membership and retrieval data structures
- **Bloom filter** (Bloom 1970, cited): one-sided error set membership; FPR `eps`, FNR `0`. The paper correctly positions this as the codomain-`B`, `fnr=0` special case.
- **Bloomier filter** (Chazelle et al. 2004, cited): the canonical function (not just set) generalization. It stores `f: S -> R` for a static key set, returns arbitrary values on members, and returns arbitrary garbage on non-members. This is the most direct prior art for "approximate map," and the paper rightly singles it out in the intro. The novelty-assessor must check that the paper differentiates from Bloomier on more than framing.
- **Cuckoo filter** (Fan et al. 2014, cited): an AMQ with deletion; relevant as another `Y=B` instance.
- **Succinct retrieval / static-function data structures** (Dietzfelbinger and Pagh 2008, cited; also the broader line: Botelho, Pagh, Ziviani perfect-hash retrieval; Bumped Ribbon Retrieval (BuRR, Dillinger and Walzer 2022); binary fuse filters (Graf and Lemire 2022)). These structures solve exactly what the singular hash map (SHM) addresses: storing `r` bits/key of associated data near the `r`-bit information-theoretic floor. They are NOT in the bibliography. The broad-survey lens flags this as the most significant missing comparison class for sections 6 and 7.
- **Minimal perfect hashing** (Fredman, Komlos, Szemeredi 1984, cited; modern line: CHD, RecSplit (Esposito, Graf, Vigna 2020), PTHash (Pibiri and Trani 2021)): underlies retrieval constructions. FKS is cited; the modern MPHF line is not.

### 1b. Information theory and source coding
- **Shannon source coding** (Shannon 1948, cited) and **rate-distortion** (Shannon 1959; Cover and Thomas 2006, cited): correctly invoked for the entropy map's `H(Y)` optimal code length and the `-log2 eps + mu` space law.
- The `-log2 eps` per-element membership lower bound is the classical Carter, Floyd, Gill, Markowsky, Wegman (1978) and Bloom information-theoretic floor; the paper attributes it loosely to Cover and Thomas. That is adequate for a theory paper, but the AMQ-specific lower-bound citation (Carter et al. 1978; Pagh, Pagh, Rao 2005 for the `n log(1/eps)` optimal AMQ) would be more precise. Confidence: high that these are the standard attributions.

### 1c. Per-input channels and Kronecker structure
- The claim "the joint confusion matrix factors as a Kronecker product of per-input channels under independence" is, mathematically, the statement that a product of independent discrete memoryless channels has a tensor-product transition matrix. This is standard information theory (memoryless-channel product). The paper's contribution is not the tensor fact itself but its use as a unifying lens across Boolean, set, map, and relation. The novelty-assessor should weigh it as an organizing and expository contribution rather than a new theorem.

### 1d. Encrypted search and trapdoor (the application thread)
- Song, Wagner, Perrig 2000 and Curtmola et al. 2006 (both cited) anchor the "trapdoor entropy map" subsection. This connects to the author's wider trapdoor-computing program ("Bernoulli maps ARE cipher maps").

---

## 2. Targeted comparisons: closest prior art

| Prior work | Same problem? | Same technique? | Overlapping claim? | Differentiation in paper |
|---|---|---|---|---|
| Bloomier filter (Chazelle 2004) | Yes, approximate `f: S->R` | Hash-based static function store | "approximate map" object | Paper frames Bloomier as an instance of a Bernoulli map; differentiation is the probabilistic model plus composition algebra, not the data structure. Adequate but should be stated more sharply. |
| Static-function / retrieval (Dietzfelbinger and Pagh 2008; BuRR; binary fuse) | Yes, store `r` bits/key | Linear-system / fingerprint retrieval | space approx `r + log(1/eps)` bits/key | Not compared. SHM's `-log2 eps + mu` claim should be situated against this line. |
| Spectral Bloom filter (Cohen and Matias 2003), counting Bloom | Partial (multiplicities) | Counter arrays | values per key | Not cited; lower priority (codomain there is counts). |
| Channel-product / DMC composition (Cover and Thomas 2006) | The composition algebra | Transition-matrix product | composition error rates | Cited; the maps paper's composition theorem is a specialization to the Maybe-type channel. |

**Key targeted finding**: the paper's direct novelty over Bloomier and retrieval is the **compositional algebra of approximate maps** (theorems on `fnr`/`fpr` of `g circ f`, the `rho` overlap parameter, model-order elevation under composition) and the **uniform model** tying Booleans, sets, maps, and relations together. The data structure (SHM) is closer to known retrieval structures and is the weaker novelty axis.

---

## 3. In-family positioning (critical per task instructions)

This is an **extension paper**; shared foundations must NOT be counted against novelty.

- **`bernoulli_sets/` (FOUNDATION)**: supplies the two axioms, the binomial error-count distributions, and the higher-order composition theorem `thm:composition_rates` and `thm:twofold_composition` (full binary-channel product: `tpr = t'*t + fn'*eps`, `fpr = f'*t + tn'*eps`). The maps paper legitimately reuses Axiom 1 (element independence) and the binomial-count machinery, and specializes the composition theorem to the Maybe-type channel. Novelty owned by maps: arbitrary codomain `Y` (not just `B`), the Maybe-type composition theorem with the `rho` parameter, and the entropy-map and SHM construction at `-log2 eps + mu`.
- **`bernoulli_relations/` (companion, cited as `arelation`)**: owns `n`-ary relations, join/project/select. The maps paper's section 5.4 (relations as n-ary predicates) and the conclusion's "relational algebra operators ... merit further investigation" correctly defer to it. Overlap is acknowledged and bounded.
- **`bernoulli_data_type/` (companion, cited only narratively as "a companion paper on random approximate algebraic types")**: owns the constructive type-theoretic account (Bool plus sum/product/exponential). The maps paper's "two perspectives, one theorem" framing (denotational function-space versus constructive type-theory, converging at the exponential type) is the explicit boundary. The data_type paper is NOT in references.bib; it is referenced only in prose. The citation-verifier should flag the missing bib entry.

**Distinguishing maps from relations and data_type (for the novelty-assessor):**
- versus **relations**: maps are single-valued (binary relation with unique first coordinate); relations are general `n`-ary. Maps owns composition `g circ f`; relations owns join/project. Clean separation; the only soft overlap is section 5.4, which is explicitly a teaser.
- versus **data_type**: maps takes the denotational view (a map is a point in `Y^X` approximated per-input); data_type takes the constructive view (types built from Bool). The exponential type `A->B` is the shared object. The maps paper's claimed unique contribution is the Kronecker-factorization-as-organizing-principle stated denotationally plus the composition algebra; data_type's is the sum/product/exponential parameter-count story. The boundary is articulated but rests on a paper not yet citable.

---

## 4. Benchmarks the paper does and does not engage

- For the **space claim** (`-log2 eps + mu` bits/element): the modern bar is retrieval structures within a few percent of the `log2(1/eps)` floor (binary fuse around 1.08x; BuRR around 1.01 to 1.05x). The SHM is presented as an asymptotic, theoretical optimum (a geometric-search construction), not a practical competitor, and there are no experiments (the conclusion lists Monte Carlo validation as future work). For a theory paper this is acceptable, but reviewers from the data-structures community would expect at least a remark situating SHM against these structures.
- For the **composition algebra**: there is no standard competing "algebra of approximate maps" in the literature; this is genuinely the paper's open ground. The closest is the DMC-product view, which the paper subsumes.

---

## 5. Takeaways for the specialists

1. **Novelty-assessor**: Real novelty is (i) arbitrary-codomain generalization with explicit Maybe-type semantics, (ii) the composition theorem with the `rho` overlap parameter and model-order elevation, and (iii) the unifying function-space and Kronecker lens. Differentiate sharply from Bloomier (Chazelle 2004) and from in-family relations and data_type. The SHM is the weakest novelty axis (close to known retrieval structures).
2. **Methodology-auditor**: No experiments at all; every quantitative claim is analytic. The `rho` parameter and the SHM space bound are the claims most in need of the currently absent empirical validation, which the paper itself admits.
3. **Logic-checker**: Verify the Maybe-type composition theorem is the correct specialization of the foundation's full-channel `thm:composition_rates`; verify the `rho`-parametrized FPR; scrutinize the section 6.6 "probability of success" binomial expression and the SHM section 7 success-probability proof (notation `mod t` versus `mod BL`, the `1 cat k` concatenation, the `N < max BL` hypothesis).
4. **Citation-verifier**: the data_type companion paper is cited in prose but absent from `references.bib`; the modern retrieval and MPHF line (BuRR, binary fuse, RecSplit, Botelho et al., Pagh et al., Carter et al. 1978) is uncited (acceptable for a theory paper, but the AMQ lower-bound attribution to Cover and Thomas is imprecise).
5. **Prose-auditor**: the strongest exposition is sections 1 to 5 (intro, model, special cases, composition). Sections 6 (entropy maps) and 7 (SHM) are markedly rougher and read like older draft material imported with less polish.
