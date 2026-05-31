# Literature Context Packet

**Paper:** The Bernoulli Hash Function: Optimal Bernoulli Sets and Bernoulli Maps
**Date:** 2026-05-29
**Compiled by:** area chair (merging broad and targeted literature grounding)

This packet merges a broad field survey with a targeted search for the closest
prior art. It updates the 2026-02-26 literature packet, which is largely still
valid. The key change since then is that the manuscript now cites most of the
work the prior packet flagged as missing.

## 1. Field: Approximate Membership / Retrieval Structures

The paper sits in the well-studied area of space-efficient probabilistic
membership structures (approximate sets) and their function-valued
generalization (approximate maps / retrieval structures).

### Lower bounds (the bar the paper claims to hit)
- **Carter, Floyd, Gill, Markowsky & Wegman (1978), "Exact and Approximate
  Membership Testers" (STOC).** Establishes the `n*log2(1/eps)` lower bound for
  approximate membership over an unbounded universe. Now cited in the
  manuscript (`prelim.tex`, both lower-bound theorems, and `discussion.tex`).
- **Pagh, Pagh & Rao (2005), "An Optimal Bloom Filter Replacement" (SODA).**
  Achieves the lower bound up to lower-order terms with *polynomial*
  construction via a dictionary/retrieval reduction. Now cited
  (`discussion.tex`). This is the single most important comparator for a paper
  claiming optimality, because it already achieves the bound efficiently. The
  manuscript now acknowledges this but should sharpen it (see novelty notes).
- **Lovett & Porat (2010); Dietzfelbinger & Pagh (2008) "Succinct Data
  Structures for Retrieval and Approximate Membership."** Retrieval-based
  near-optimal structures. Dietzfelbinger and Pagh is NOT cited and is the most
  defensible remaining omission, because the BHF's value-storage mechanism
  (hash bits encode the value) is exactly a retrieval structure.

### Practical filters (the efficiency frontier)
| Structure | Space (bits/elem) | Construction | In paper? |
|---|---|---|---|
| Bloom (1970) | `log2(e)*log2(1/eps)` approx 1.44*LB | O(n) | yes |
| Cuckoo filter (Fan et al. 2014) | approx LB + small const | O(n) | yes |
| XOR filter (Graf & Lemire 2020) | approx 1.23*LB | O(n) | yes |
| Binary fuse (Graf & Lemire 2022) | approx 1.08 to 1.13*LB | O(n) | mentioned (no cite) |
| Ribbon (Dillinger & Walzer 2021) | approx LB + 1.5 | O(n) | yes |
| Quotient filter (Bender et al. 2012) | approx Bloom | O(n) | no |
| **BHF fixed (this paper)** | **= LB exactly** | **exp(m)** | n/a |
| **BHF adaptive (this paper)** | **O(log N / m) -> 0** | **O(m log m)** | n/a |

The manuscript's comparison subsection (`discussion.tex`) now covers Bloom,
PHF, cuckoo, XOR, ribbon, and Pagh-Pagh-Rao, a major improvement over the
prior draft. Binary fuse is named but not cited; Dietzfelbinger-Pagh and
Bloomier filters are absent.

## 2. Targeted: closest constructions to the BHF mechanism

- **Bloomier filter (Chazelle, Kilian, Rubinfeld & Tal, 2004).** The canonical
  *approximate map* / function-retrieval structure. This is the most direct
  competitor to the BHF's map contribution and is NOT cited. A reviewer at a
  data-structures venue will expect it. The BHF differs in that it stores the
  value *inside the same hash evidence* that certifies membership, rather than
  in a separate retrieval array, but the problem solved (key to value with
  one-sided error) is the same.
- **Perfect-hashing / "find a seed that works" paradigm** (Czech-Havas-Majewski
  1992; Botelho-Pagh-Ziviani 2007; and the author's own PHF/maph line). The BHF
  salt search ("find a hash seed under which all m keys land in the acceptance
  region") is structurally the minimal-perfect-hashing seed search specialized
  to a *single shared* target region. This lineage is acknowledged via the PHF
  self-citations but not via the external MPHF literature.
- **Carter-Wegman universal hashing (1979).** Underlies the random-oracle
  approximation assumption. Cited indirectly through `carter1978` (a different
  Carter paper) but the universal-hashing primitive itself is not cited. Minor.
- **Random oracle model (Bellare & Rogaway, 1993).** The paper leans on the
  random-oracle assumption throughout but does not cite the standard reference.
  Minor but expected at a top venue.

## 3. The adaptive threshold: genuinely novel framing

The adaptive-threshold variant (set the acceptance threshold to the p-th order
statistic of the keys' hash residues, so *every* salt works for sets and the
per-element cost vanishes) does not have a direct prior-art analogue in the
filter literature. The underlying machinery (p-th order statistic of m i.i.d.
uniforms is Beta(p, m-p+1)) is classical (David & Nagaraja 2003, cited). The
*application* of this to trade a deterministic FPR for a random FPR, and thereby
sidestep the `-log2 eps` term, is the paper's strongest original idea. The
"price of FPR certainty" theorem (Delta = m*log2(1/eps)) framing this trade-off
as the information-theoretic content of the lower bound is, to my knowledge, a
new and elegant observation.

The closest conceptual neighbor is the distinction between data-dependent and
data-independent guarantees in the lower-bound literature (the Carter et al.
bound is a worst-case / data-independent guarantee). The manuscript now makes
this distinction precise (Remark `rem:lb_not_violated`, Theorem
`thm:price_certainty`), which is exactly the right move.

## 4. Family context (do NOT penalize as non-novel)

This is an *application* paper in a 9-paper family on random approximate sets.
It legitimately builds on:
- `bernoulli_sets`: the Bernoulli set ADT, axioms, FP/FN distributions.
- `bernoulli_entropy`: the `-log2(eps) + mu` space bound (information-theoretic).
- `bernoulli_maps`, `bernoulli_data_type`: map/type generalizations.

The paper's declared role is the *information-theoretically optimal
construction* that achieves that bound and unifies sets and maps. Novelty must
be assessed relative to that role, not relative to the family foundations.

## 5. Net takeaways for the review

1. The prior pass's central novelty/citation complaint (missing Carter, Pagh,
   modern filters) has been substantially addressed.
2. Two expected citations remain absent: the Bloomier filter (closest map prior
   art) and Dietzfelbinger-Pagh retrieval (closest map/membership theory);
   plus Bellare-Rogaway for the random oracle.
3. The optimality contribution should be framed as "exact bound via a maximum-
   entropy construction" and "the adaptive trade-off," since *achievability*
   per se is Pagh-Pagh-Rao (2005). The current discussion already says this; the
   intro's contribution list does not yet, and should.
