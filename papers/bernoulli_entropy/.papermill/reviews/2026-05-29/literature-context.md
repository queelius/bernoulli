# Literature Context Packet, bernoulli_entropy

**Compiled**: 2026-05-29
**Method**: Synthesized by the area chair from domain knowledge of the approximate-membership-query (AMQ) and information-theory literature (knowledge cutoff Jan 2026). The two literature-scout subagents were unavailable in this environment, so the orchestrator performed the field grounding directly. Citations below are stated from memory and flagged where verification by the citation-verifier is advisable.

---

## A. Field Landscape

The paper combines two well-trodden areas.

1. **Approximate membership / space lower bounds.** The foundational lower bound for approximate set membership (false-negative-free, false-positive rate epsilon) is `n*log2(1/epsilon)` total bits, that is, `-log2(epsilon)` bits per stored element. This is classically attributed to **Carter, Floyd, Gill, Markowsky, Wegman, "Exact and Approximate Membership Testers", STOC 1978** (cited). The modern, tight treatment, establishing the bound as `(1+o(1))*n*log2(1/epsilon)` together with a matching data structure that achieves `(1+o(1))` of it, is **Pagh, Pagh & Rao, "An Optimal Bloom Filter Replacement", SIAM J. Comput. 2005 (SODA 2005)**. This is the canonical reference for "Bloom filters are not space-optimal; here is a structure within o(1) of the bound," which is precisely the gap the present paper highlights (Bloom at ln2 approx 69%). **PPR 2005 is not cited and is a strong must-cite.**

2. **Entropy of the binomial distribution.** The asymptotic `H(Bin(n,p)) = (1/2)*log2(2*pi*e*n*p(1-p)) + O(1/n)` is standard. It follows from a local CLT / Stirling argument and is the discrete analogue of the differential entropy of a Gaussian. It is folklore-level and appears in many places. **Cover & Thomas** (cited) is an acceptable textbook anchor, though it does not state this exact expansion as a numbered result. More precise treatments giving the next-order constant exist (for example, work by **Knessl (1998)**, and asymptotic-combinatorics treatments by **Jacquet & Szpankowski**), but for an O(1/n) statement Cover & Thomas is defensible.

### Modern AMQ structures (context the paper only partially engages)

| Structure | Reference (from memory) | Relevance |
|---|---|---|
| Bloom filter | Bloom 1970 (cited) | Baseline; 69% efficient, the paper's running comparison |
| Optimal Bloom replacement | Pagh, Pagh & Rao, SICOMP 2005 | **Achieves (1+o(1)) of the -log2(epsilon) bound; the tight upper+lower bound pairing the paper's lower bound needs** |
| Cuckoo filter | Fan, Andersen, Kaminsky, Mitzenmacher, CoNEXT 2014 | Practical near-optimal AMQ; deletions |
| Quotient filter | Bender et al., 2012 (VLDB) | Cache-friendly near-optimal AMQ |
| XOR filter | Graf & Lemire, ACM JEA 2020 | approx 1.23*n*log2(1/epsilon); closer to optimal than Bloom |
| Bloomier filter | Chazelle, Kilian, Rubinfeld, Tal, SODA 2004 | Approximate *map* (function), generalizes AMQ; relevant to the family's `bernoulli_maps` |

For a paper whose explicit contribution is the **lower bound** and Bloom's distance from it, the single most important omission is **Pagh-Pagh-Rao**: it is the result that closes the loop (matching upper bound plus tight lower bound). The practical filters (cuckoo/quotient/XOR) are nice-to-cite context but not load-bearing for a lower-bound paper. One sentence acknowledging that near-optimal practical structures exist would suffice.

---

## B. Most Important Works to Engage (priority order)

1. **Pagh, Pagh & Rao (SICOMP 2005), "An Optimal Bloom Filter Replacement."** Must-cite. Provides the matching `(1+o(1))*n*log2(1/epsilon)` upper bound and the tight lower-bound framing. Without it, the paper's claim that Bloom is "69% efficient" relative to "the optimum" is stated against a lower bound whose *achievability* is left implicit. The author's own `bernoulli-hash-function` and `phf`/`shs` papers play the achievability role internally, but the field-standard external reference is PPR.

2. **Yao, "Probabilistic Computations: Toward a Unified Measure of Complexity", FOCS 1977.** Must-cite. The proof of Proposition 3.1 explicitly invokes "Yao's minimax principle" to extend the deterministic bound to randomized data structures, but **no Yao reference appears in the 8-entry bibliography.** This is a concrete, near-certain citation gap (see citation-verifier).

3. **Carter, Floyd, Gill, Markowsky, Wegman (STOC 1978).** Already cited; correct primary source for the -log2(epsilon) bound. Good.

4. **Broder & Mitzenmacher, "Network Applications of Bloom Filters: A Survey", Internet Mathematics 2004.** Optional. Standard entry point for the Bloom-filter optimum `m/n = -log2(epsilon)/ln2` and the ln2 occupancy result; would support the 69%-efficiency claim with a citable source rather than asserting it.

5. **Cover & Thomas, *Elements of Information Theory* 2e.** Already cited; fine as the anchor for entropy and the binomial expansion, with the caveat that the exact O(1/n) expansion is not a numbered theorem there.

---

## C. Pre-emption Check

- **Does anyone pre-empt Result 1 (joint entropy of FP/FN counts)?** No direct pre-emption found. Computing the *Shannon entropy of a Bloom filter's false-positive count* (let alone the joint FP/FN entropy of a general approximate set) is not a standard published result to my knowledge. The result is a near-mechanical consequence of (i) independence implies additivity and (ii) the textbook binomial-entropy expansion, so it is **novel but mathematically elementary**. Its value is framing and completeness within the Bernoulli family, not depth.
- **Does anyone pre-empt Result 2 (the lower bound)?** Yes, by construction. The paper *explicitly restates* Carter et al. 1978 and says so ("We restate it here ... and include a proof for completeness"). PPR 2005 sharpens it. So Result 2 is **acknowledged restatement**, not a novelty claim, and is framed honestly.

## D. Calibration: standard vs. novel

| Claim | Standing |
|---|---|
| H(FP,FN) = H(FP)+H(FN) additivity | Standard (independence). Novel only in application. |
| Closed-form asymptotic via binomial entropy | Standard expansion, novel assembly. Elementary. |
| Extension to random positive count POS | Standard conditioning/chain-rule; routine. |
| -log2(epsilon) bits/element lower bound | **Restatement** of Carter et al. 1978 (so-labeled). Not claimed novel. |
| Bloom at ln2 approx 69% | Well-known folklore (Broder-Mitzenmacher). Correct. |
| General 0<tau<1 case open | Honest open problem; plausible it is genuinely open in this exact framing. |

**Net:** The paper makes modest, honestly-scoped claims. The principal literature-grounding deficiencies are two missing citations (Yao 1977, Pagh-Pagh-Rao 2005) and the absence of any acknowledgment of modern near-optimal AMQ structures.
