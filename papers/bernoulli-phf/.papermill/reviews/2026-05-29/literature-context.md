# Literature Context Packet, The Perfect Hash Filter

**Compiled**: 2026-05-29

**Method note**: The orchestrator's `Task` tool for spawning the dedicated literature-scout subagents was unavailable in this run (the review executed inside a subagent sandbox). The area chair therefore compiled this packet directly from domain knowledge of the AMQ and succinct-data-structure literature and from the paper's own bibliography (`references.bib`, which already contains 16 real references in addition to 9 placeholder self-citations). Citations below give enough detail (authors, year, venue, the one result that matters) to be verified and added to the `.bib`. Where a claim could not be pinned to a specific page from memory, it is flagged "verify."

---

## 1. The core construction is well-known prior art: "MPHF + fingerprint" AMQ

The paper's central data structure is the following. Build a (minimal) perfect hash `ph_S : S -> {1..N}`; store at slot `ph_S(x)` a `b`-bit fingerprint `g(x)`; test membership of `q` by checking `V[ph_S(q)] == g(q)`. Members always match (FNR = 0); a non-member matches with probability `2^-b` (FPR `eps = 2^-b`). Space = (MPHF overhead) + `b` bits/key.

This is a standard, folklore static-AMQ construction, not a new data structure. It is the explicit baseline against which the modern fingerprint filters are compared. The most directly relevant published anchors:

| Work | Citation | Relationship to PHF |
|---|---|---|
| **Xor filters** | Graf and Lemire, "Xor filters: faster and smaller than Bloom and cuckoo filters," *ACM J. Experimental Algorithmics* 25 (2020). *(in bib as `graf2020`)* | Store `b`-bit fingerprints indexed by a peeling/XOR perfect-hash scheme. Zero FNR, static. Achieves about **1.23x** the `n*log2(1/eps)` lower bound. Their related-work explicitly discusses the "perfect hash + fingerprint" design the PHF proposes. The PHF is essentially the MPHF-based instance of this family. |
| **Fuse filters** | Dietzfelbinger and Walzer, "Dense peelable random uniform hypergraphs," 2019 (verify); popularized alongside the xor/ribbon line. | Improve the xor construction to about **1.075x** the lower bound. |
| **MPHF + fingerprint baseline (folklore)** | Stated in Dietzfelbinger and Pagh, "Succinct data structures for retrieval and approximate membership," *ICALP* 2008 *(in bib as `dietzfelbinger2008`)*; and in the BBHash paper: Limasset, Rizk, Salikhov, Chikhi, "Fast and scalable minimal perfect hashing for massive key sets," *SEA* 2017 (verify). | This is the canonical statement that "perfect hash to a slot + `b`-bit fingerprint = AMQ with FPR `2^-b` and space about MPHF-overhead + `b` bits/key." The paper's Theorem (FPR = `2^-M`) and its space formula are a re-derivation of this folklore result. |
| **Cuckoo filter** | Fan, Andersen, Kaminsky, Mitzenmacher, "Cuckoo filter: practically better than Bloom," *CoNEXT* 2014 *(in bib as `fan2014`)*. | Same fingerprint idea, different placement mechanism (partial-key cuckoo hashing instead of perfect hash). About 1.05x at low FPR, supports deletion (the PHF does not). |
| **Bloomier filter** | Chazelle, Kilian, Rubinfeld, Tal, "The Bloomier filter: an efficient data structure for static support lookup tables," *SODA* 2004 *(in bib as `bloomier`)*. | The key-to-value generalization. The paper's "Perfect Map Filter" (`pmf.tex`) is a Bloomier-filter-style construction. The paper does not cite `bloomier` for the map case, a clear gap. |
| **Optimal Bloom replacement** | Pagh, Pagh, Rao, "An optimal Bloom filter replacement," *SODA* 2005 *(in bib as `pagh2005`)*. | A near-optimal static AMQ reaching `(1+o(1))*n*log2(1/eps)` bits. Direct competitor to the PHF's optimality claim. Cited in bib but not yet engaged in the prose. |

**Verdict for the area chair (positioning):** The PHF's data structure is not novel. It is the textbook MPHF+fingerprint AMQ. What can be legitimately novel, given the paper's declared role as an implementation/application paper inside the Bernoulli-set family, is: (a) the framing of this structure as a concrete realization of the *positive Bernoulli set* ADT and verification that it satisfies the two Bernoulli axioms; (b) the `k`-perfect-hashing FNR analysis (the coupon-collector placement model), if it is more than a standard occupancy argument; and (c) the fuzzy-set / rank-ordered IR application of the map variant. The paper must therefore (i) cite xor/fuse/cuckoo/Bloomier as the structures it coincides with, (ii) reframe its contribution as "Bernoulli-ADT realization plus analysis," not "a new succinct structure," and (iii) soften or qualify the optimality claim (see section 2).

---

## 2. The "asymptotically optimal `-log2 eps` bits/element" claim, overclaim risk

The CFGMW lower bound (Carter, Floyd, Gill, Markowsky, Wegman, "Exact and approximate membership testers," *STOC* 1978, in bib as `carter1978`) establishes that an approximate membership tester for `n` keys with false-positive rate `eps` needs at least about `n*log2(1/eps)` bits.

Two points the reviewers must hold the paper to:

1. **The lower bound is on the fingerprint payload only.** Any indexing mechanism (perfect hash, xor peeling, cuckoo) adds overhead on top of `n*log2(1/eps)`. The MPHF information-theoretic minimum is `log2(e)` (about 1.4427) bits/key (Mehlhorn 1982, in bib as `mehlhorn1982`; see also Fredman, Komlos, Szemeredi, `fks`). Practical MPHFs (CHD: Belazzougui, Botelho, Dietzfelbinger, "Hash, displace, and compress," *ESA* 2009, in bib as `chd`; "simple": Botelho, Pagh, Ziviani, *WADS* 2007, in bib as `simple`) sit around 1.5 to 3 bits/key.

2. The honest statement is therefore: total space `= n*log2(1/eps) + Theta(n)` overhead bits, i.e. absolute efficiency tends to 1 only in the limit `eps -> 0`, where the fixed `Theta(1)` bits/key overhead becomes negligible relative to the growing `log2(1/eps)` payload. The paper's own `rd_ph_filter.tex` actually contains this nuance (its `log2 e - (1/r -1)log2(1/(1-r))` term and the explicit "not asymptotically optimal w.r.t. `m`; tends to 1 as `eps -> 0`" remark). But the abstract and intro state the optimality flatly ("asymptotically achieves the information-theoretic lower bound") without the `eps -> 0` qualifier, and the body contains two contradictory crossover thresholds (`eps < 2^-3` in the intro vs `eps < 2^-4` in `rd_ph_filter.tex`). The modern filters (xor 1.23x, fuse 1.075x) achieve the same "tends to 1" asymptote with less overhead, so a flat "optimal" claim is not defensible against the state of the art.

**This is the single most important substantive issue.** The claim is correct in the `eps -> 0` limit but is overclaimed as written, and is not differentiated from xor/fuse filters that do better at practical `eps`.

---

## 3. Minimal-perfect-hashing space facts (the numbers the paper rides on)

- Information-theoretic MPHF lower bound: `log2 e` (about 1.4427) bits/key (the paper's "1.44" figure is correct: this is the lower bound, not an achievable practical cost).
- The paper also uses `alpha(1) = 2.07` bits/key as a practical minimal-perfect-hash cost. This is in the right ballpark for CHD-class constructions (verify the exact source; CHD reports roughly 2.07 bits/key at certain parameters, in bib as `chd`). The paper attributes its space theorems to an unpublished manuscript `oph` ("Random oracles that perfectly hash..."), invoking "Theorem 3 of `oph`." That is a load-bearing dependency on an uncitable source (see section 5).
- Modern lower-overhead MPHF (RecSplit: Esposito, Graf, Vigna, *ALENEX* 2020, about 1.56 bits/key; verify) would strengthen the paper's "MPHF overhead is small" argument and should be cited.

---

## 4. Evaluation norms in this subfield (scopes the "zero experiments" gap)

A credible AMQ paper in 2020s venues reports, at minimum:
- bits/key vs target FPR curves, measured, for the proposed structure against Bloom, cuckoo, xor, ribbon/fuse filters;
- construction time vs `n`;
- query throughput (lookups/sec, often with SIMD/batch) and false-positive rate empirically measured vs the `2^-b` prediction;
- a table at several `eps` (e.g. `2^-8, 2^-12, 2^-16`) of measured bits/key and the absolute/relative efficiency.

The paper currently has zero experiments, while a substantial C++ library (`maph`, about 12.8k LOC, with tests and benchmark harnesses) exists in the same repository but is never referenced by the paper. Closing the experiments gap is largely a matter of wiring the existing `benchmarks/` to the paper's claims (measured FPR vs `2^-b`; measured bits/key vs the predicted `-(1/r)log2 eps + alpha(r)`; throughput vs Bloom).

---

## 5. Load-bearing claims that rest on unpublished, uncitable self-references

The following are cited as authorities for quantitative results but are `@unpublished` placeholders (notes read "Manuscript in preparation"):

- `oph`, invoked for the perfect-hash space lower bound ("Theorem 3 of `oph`") that underlies Theorem `thm:mPHF_size` and its corollary. The paper's headline space result currently has no citable basis.
- `bsets`, the Bernoulli-set foundation (this is the family's primary paper; it exists at `papers/bernoulli_sets/`, so this can be made a real citation immediately).
- `bmaps`, the Bernoulli-map paper (exists in the family).
- `shs`, `obset`, `emaps`, `aset`, `pmf`, referenced in `adt.tex` and `intro.tex`. `shs` ("singular hash set") is claimed to "optimally implement the Bernoulli set and oblivious set," a strong claim resting on a non-existent manuscript.

**For the area chair:** at least the foundation references (`bsets`, `bmaps`) can be upgraded to real in-family citations now; the space-bound dependency on `oph` must either be (a) proved inline in this paper or (b) deferred, with the claim weakened until `oph` exists.

---

## 6. Fuzzy sets in IR (applications section)

- Zadeh, "Fuzzy sets," *Information and Control* 8(3), 1965 (in bib as `zadeh1965`), is the correct canonical anchor for degree-of-membership and the min/max/`1-x` connectives the paper uses.
- The "fuzzy AMQ map for rank-ordered postings-list search" is a plausible but non-standard application. It is not a recognized named technique. The IR plumbing (postings lists, Boolean retrieval) is well covered by the already-present `manning` (Manning, Raghavan, Schutze, *Intro to IR*, 2008) and `zobel2006` (Zobel and Moffat, "Inverted files," *ACM CSUR* 2006). The novelty here, if any, is the combination, and it needs at least a worked example with numbers to be more than a sketch.

---

## Key takeaways for the review

1. **Core structure = known prior art** (MPHF+fingerprint AMQ; xor/fuse/cuckoo/Bloomier lineage). Realistic novelty is the Bernoulli-ADT framing, the `k`-perfect FNR analysis, and the fuzzy-IR app, and these must be stated as the contribution.
2. **Optimality claim is overclaimed** as flatly written; correct only in `eps -> 0`; not differentiated from xor (1.23x) / fuse (1.075x). Must qualify and compare.
3. **No related-work section** despite a strong (real) bibliography already present. The references exist but are not deployed in prose. This is the cheapest high-value fix.
4. **Space theorems depend on unpublished `oph`.** Must prove inline or weaken.
5. **Zero experiments**, but a 12.8k-LOC benchmarkable C++ library sits unused in the repo.
6. **Bloomier filter must be cited** for the Perfect Map Filter.
