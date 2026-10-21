# Literature audit: finite query contracts and representation planning

Accessed and checked: **2026-10-13**. This is a targeted novelty audit, not an exhaustive review. Bibliographic keys refer to [references.bib](references.bib). Sources are original papers, publisher records, author-hosted copies, and one original formalization. Statements labeled “assessment” or “derived here” are our deductions, not claims made by the cited authors.

## Result

**No new general theorem or data structure has been established.** Constraints already improve probabilistic query evaluation; allocation of Bloom-filter space already has optimization formulations; functional rows admit much stronger retrieval baselines than scanning membership tests; and the proposed rank inclusion–exclusion formula for shared linear fingerprints is precisely an application of the matroid Critical Theorem. A restricted, finite-construction planner remains worth testing as an engineering contribution, provided its benefit survives these comparisons.

Preserve the earlier negative results: [dependence-calculus synthesis](../dependence-calculus/synthesis.md) rejected generic lineage/calculus novelty, and [relations-revision assessment](../relations-revision/assessment.md) reported only **16 bytes, 0.425%** saved by sharp rather than union sizing (3752 versus 3768 bytes). A sharper probability formula is not evidence of a useful representation improvement.

## Closest primary work and applicability

| Area / primary source | Verified result or scope | Consequence for this project |
|---|---|---|
| **SPROUT**, Olteanu–Huang–Koch, ICDE 2009, `olteanu2009sprout`. [Author PDF](https://www.cs.ox.ac.uk/dan.olteanu/papers/ohk-icde09.pdf) | Proposition IV.5 concerns FD reductions to hierarchical queries. Signatures represent one/many join structure; confidence computation can move through plans. | “Integrity constraints simplify probabilistic query planning” is established. Its tuple-independent uncertain-world semantics differs from a fixed exact database with randomized encoding errors. |
| **Bridging the Gap Between Intensional and Extensional Query Evaluation**, Jha–Olteanu–Suciu, EDBT 2010, `jha2010bridging`. [Author PDF](https://www.cs.ox.ac.uk/dan.olteanu/papers/jos-edbt10.pdf) | Proposition 3.2 characterizes data-safe joins of independent relations using at-most-one joining partners for uncertain tuples, with exceptions for certain tuples. Section 3 conditions on offending tuples; Theorem 5.16 treats conditioning sets and partial lineage. | One-to-one structure, explicit dependence, and selective conditioning are direct precedents. Generic “use bounded relational structure to simplify inference” is insufficient novelty. |
| **Consistency Checking and Querying in Probabilistic Databases under Integrity Constraints**, Flesca–Furfaro–Parisi, JCSS 2014, `flesca2014consistency`. [Publisher](https://www.sciencedirect.com/science/article/pii/S0022000014000701), [preprint](https://arxiv.org/abs/1303.3233) | Cautious semantics ranges over joint distributions satisfying tuple marginals and denial constraints. In the preprint, Theorem 2 gives a consistency condition for a γ-hypertree conflict hypergraph; Theorem 7 shows hardness already with two FDs. | Broad constrained probability bounds without a unique joint distribution are established. Do not identify their uncertain true worlds with our encoding randomness. |
| **Monkey**, Dayan–Athanassoulis–Idreos, SIGMOD 2017; expanded TODS 2018, `dayan2017monkey`, `dayan2018optimal`. [2017 paper](https://scholar.harvard.edu/files/stratos/files/monkeykeyvaluestore.pdf), [2018 author record](https://stratos.seas.harvard.edu/publications/optimal-bloom-filters-and-adaptive-merging-lsm-trees) | Optimizes Bloom-filter memory across LSM levels using a sum of false-positive probabilities in negative-lookup I/O cost; expanded work also co-tunes merging. | Error-budget allocation and storage/runtime tradeoffs are known. Here FPs primarily increase I/O, rather than change the final logical answer. |
| **Optimizing Collections of Bloom Filters within a Space Budget**, Mersy–Wang–Sintos–Krishnan, PVLDB 2024, `mersy2024collections`. [Paper](https://vldb.org/pvldb/vol17/p3551-mersy.pdf) | Section 2.1 explicitly adopts the approximate Bloom formula despite its bit-independence limitation. Proposition 3.4 assumes bit independence for truncation; Propositions 4.2–4.3 give convex allocation/relaxation results for utility-weighted FPs. | The strongest direct budget-allocation baseline. A finite certified guarantee would differ from its approximation, but “optimize weighted FP subject to storage” is already covered. |
| **Bitvector-aware Query Optimization**, Ding–Chaudhuri–Narasayya, SIGMOD 2020, `ding2020bitvector`. [Author PDF](https://www.microsoft.com/en-us/research/uploads/prod/2020/05/bqo_sigmod_cr.pdf) | Theorem 5.2 proves optimality among a small candidate family under the stated star/snowflake, PK–FK, right-deep-plan and simplified-cost assumptions. Section 6.3 includes estimated filter FPs/costs. | Do not generalize the theorem to arbitrary joins. It nevertheless strongly precedes using structural constraints to choose filter-aware plans. |
| **Including Bloom Filters in Bottom-up Optimization**, Zeyl et al., SIGMOD Companion 2025, `zeyl2025bottomup`. [Primary preprint](https://arxiv.org/abs/2505.02994) | Incorporates filters into join-order optimization with limited search expansion, rather than only adding them after planning. | A current filter-planning baseline; metadata is the Companion proceedings, not the main research proceedings. |
| **Robust Predicate Transfer with Dynamic Execution**, Qiao–Boncz–Zhang, PVLDB 2026, `qiao2026robust`. [Author PDF](https://people.iiis.tsinghua.edu.cn/~huanchen/publications/rpt%2B-vldb26.pdf) | RPT+ uses asymmetric transfer, equivalence classes of join keys, and dynamic execution to reduce redundant filtering and runtime costs. | Shared join-key structure already informs modern practical filter plans. Final exact joins distinguish this task from approximate-answer contracts. |
| **I Can't Believe It's Not Yannakakis**, Zhao et al., CIDR 2026, `zhao2026yannakakis`. [Paper](https://www.vldb.org/cidrdb/papers/2026/p29-zhao.pdf) | Section 3 describes runtime selection of exact bitvectors versus Bloom filters according to cardinality/range/distribution, inside a bitmap-aware optimizer. | Representation choice itself is not new. Compare exact compact-domain encodings, not only alternative approximate filters. |

## Functional rows: retrieval is the decisive baseline

For an unrestricted equality/intersection query on two nonempty functional rows with values \(u,v\), store a fingerprint \(h(u)\) per row, retrieve two fingerprints, and compare them. A universal \(b\)-bit hash provides zero FN and at most \(2^{-b}\) FP for each fixed unequal pair, independently of the original value-domain size. This is a direct application of universal hashing, not a new algorithm. [Carter–Wegman 1979](https://www.sciencedirect.com/science/article/pii/0022000079900448) (`carter1979universal`).

Static retrieval returns the assigned value exactly on stored keys and may return anything on other keys. Dietzfelbinger–Pagh, ICALP 2008, already gives succinct retrieval and its approximate-membership reduction (`dietzfelbinger2008retrieval`): [author preprint](https://arxiv.org/abs/0803.3693). Dense row IDs can use a packed array directly; sparse or optional rows need an explicit presence mechanism. A retrieval map alone does not certify absence.

The current baseline is not merely a theoretical 2008 construction. Ribbon/BuRR has practical implementations and succinct-space results: SEA 2022 (`dillinger2022ribbon`), [publisher](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SEA.2022.4), and the expanded **JACM 73(1), Article 7, February 2026** paper (`dietzfelbinger2026ribbon`), [institutional full text](https://publikationen.bibliothek.kit.edu/1000191446/177619178). The latter's Theorems 1.1–1.2 and Corollary 1.3 give distinct construction/query/overhead tradeoffs; its guarantees should not be flattened into one universally constant-time implementation claim. A retrieval-based AMQ and a Homogeneous Ribbon Filter also have different stated FP formulas.

**Assessment:** for unrestricted one-hot equality, scanning \(2k\) membership predicates is a weak comparator. Exact packed value IDs can be even smaller when the domain is small. Include dictionary construction/storage, row indexing, hash seeds, and presence metadata consistently. For a content-manifest workload, exact canonical content IDs are especially relevant.

For bounded-degree rows \(A,B\), storing fingerprints of their actual values also gives the elementary union bound

\[
 \Pr[\text{false intersection}]\le |A||B|2^{-b}\le d^2 2^{-b}
\]

for fixed disjoint rows of degree at most \(d\); independence between pair-collision events is unnecessary. Sorted fingerprint lists support merge-based comparison. Compare exact packed adjacency lists as well as this baseline.

Set-intersection filters have dedicated prior algorithms: Eppstein–Goodrich–Mitzenmacher–Torres, **2-3 Cuckoo Filters for Faster Triangle Listing and Set Intersection**, PODS 2017 (`eppstein2017cuckoo`), [author publication record](https://ics.uci.edu/~eppstein/pubs/a-torres.html). Goodrich's [original follow-up manuscript, Section 2](https://ics.uci.edu/~goodrich/pubs/C-206.pdf) describes aligned fingerprint arrays and exact verification of candidates. These schemes target efficient listing with underlying keys, so they are not interchangeable with a final Boolean approximate answer; they are still required runtime comparators for a broad join claim.

Correlation-aware signatures are also not new: **COCA Filters**, Tirdad et al., SPIRE 2011 (`tirdad2011coca`), deliberately exploits co-occurrence in hash/signature construction. Its [author paper](https://cs.uwaterloo.ca/~alopez-o/files/CFCABF_2011.pdf) concerns empirical average FP improvements, not a truth-uniform finite guarantee from FDs. That distinction matters; “exploit correlation in filters” alone is too broad.

## Narrower surviving workload: candidate-restricted functional intersection

The later candidate is

\[
 Q_C(r,s)=\exists z\in C:\ R(r,z)\land S(s,z),\qquad |C|=K,
\]

with at most one exact value in each row. A shared *value-only* fingerprint has a weakness absent from unrestricted equality: if both values equal \(a\notin C\), a collision between \(h(a)\) and \(h(z)\) can satisfy both tests together. Its union bound is \(Kq\), not \(Kq^2\). Therefore the unrestricted-equality dominance argument does not settle this narrower query family.

Store instead a row-specific tuple fingerprint \(f(\text{relation},\text{row},\text{actual value})\), and compare it with the same function on each candidate tuple. This is still retrieval of assigned labels, followed by ordinary fingerprint comparisons. The analysis below is for two present rows; an exact presence guard returns false immediately for an empty row. The finite construction makes a restricted contract possible without assuming full independence across witnesses.

**Derived here; standard ingredients, no novelty claim.** Inject every relevant tuple identity into \(\mathbb F_P\), choose four independent uniform coefficients, and evaluate a polynomial of degree at most three. Its evaluations at any four distinct inputs are independent uniform field elements. This is the classical finite-field polynomial construction associated with Wegman–Carter (`wegman1981hash`): [publisher](https://www.sciencedirect.com/science/article/pii/0022000081900337). The original full-text copy was unavailable during this audit; the polynomial independence property and attribution were checked in [Karayel's original Isabelle/AFP formalization](https://isa-afp.org/browser_info/current/AFP/Distributed_Distinct_Elements/Universal_Hash_Families.Carter_Wegman_Hash_Family.html), specifically `hash_prob`, `k_wise_indep` and `k_universal` (`karayel2022hash`). No unverified theorem number from the 1981 paper is asserted.

After reducing each field output modulo \(M=2^b\), write \(P=tM+r\), \(0\le r<M\). For two distinct inputs the collision probability is exactly

\[
 q=\frac{r(t+1)^2+(M-r)t^2}{P^2}
   =\frac1M+\frac{r(M-r)}{MP^2}.
\]

Four distinct tuple identities give two independent collision events, each of probability \(q\), even after this biased reduction. Thus a witness with two false tuple predicates costs \(q^2\); one with a true predicate costs \(q\). For distinct actual values \(a_1,a_2\), let \(s=|C\cap\{a_1,a_2\}|\). A sound bound is

\[
 \Pr[\mathrm{FP}]\le\min(1,\ s q+(K-s)q^2).
\]

For a truth-uniform bound when \(K\ge2\), maximize at \(s=2\): \(\min(1,2q+(K-2)q^2)\). For \(K=1\), use \(q\); for \(K=0\), use zero. If both actual values coincide outside \(C\), all witnesses have the \(q^2\) bound. Zero FN follows when stored fingerprints are retrieved exactly and true tuple comparisons are preserved. For \(P=2^{61}-1\), four coefficients fit in 32 machine bytes; this does not include tuple encoding/indexing or retrieval storage.

Necessary scope: the two rows must be distinct random-source identities; an alias of the same source cannot be counted twice. Tuple-to-field encoding must be injective on the declared domain, or its collisions must be budgeted. The guarantee is over a fresh random construction for each fixed truth/query, with queries independent of the seed. It is not a guarantee after arbitrary fingerprint disclosure or adaptive query selection. Four-wise independence does **not** justify multiplying all witness-complement probabilities.

Under genuinely independent Bernoulli tuple errors, the earlier unrestricted false-query profile has two singleton and \(k-2\) double exposures, giving \(1-(1-\alpha)^2(1-\alpha^2)^{k-2}\). This product is an elementary consequence of disjoint independent source sets. A finite four-wise hash construction supports the union bound above; it does not generally implement that entire product law. Exact one-hot truth also does not imply one-hot approximate observations.

**Assessment:** this restricted workload can evade the simplest shared-value comparison, but the proof is a short combination of a classical hash construction, the functional constraint, and a union bound. It currently supports an engineering target, not a novel theorem claim. Query runtime still depends on processing \(C\); precomputation and its storage must be charged equally across methods.

## Finite Bloom guarantees and shared-source conditioning are already studied

**Bose et al. 2008**, `bose2008false`, identify the flaw in treating Bloom bits as independent and give corrected analysis. [Publisher](https://www.sciencedirect.com/science/article/pii/S0020019008001579). Standard approximate FP formulas cannot silently become finite contracts.

**Goel–Gupta 2010**, `goel2010subset`, is especially close: it analyzes small subset queries and multiple filters. In the [author paper](https://yuba.stanford.edu/~pankaj/paps/fp109-goel.pdf), Theorem 4.3 bounds an actual finite-filter probability by the approximate expression with \(M-1\) bits and \(E+q/2\) elements, where \(q\) denotes the number of missing query elements. Section 4.2 applies varying missing-subset sizes and a union bound across filters; Appendix C gives an exact-probability dynamic program. A proposal for “finite subset-filter contracts” must explain the difference from this work.

**Kirsch–Mitzenmacher 2008**, `kirsch2008less`, already treats random within-build FP rates and conditioning on the filter. Section 7 of the [author paper](https://www.eecs.harvard.edu/~michaelm/postscripts/rsa2008.pdf) proves concentration and discusses conditional independence under its stated schemes; the double-hashing equivalence is asymptotic. Neither occupancy conditioning nor recognizing reuse of one random filter is new by itself.

For practical AMQ comparison include **Binary Fuse Filters**, Graf–Lemire 2022 (`graf2022binary`), [author preprint](https://arxiv.org/abs/2201.01174), alongside Ribbon. Their performance/space results do not establish independent FP events for arbitrary composed queries. Separate a measured baseline from a proved contract for its actual hash implementation.

## Shared linear fingerprints: the matroid formula is known exactly

Let \(D\subseteq\mathbb F_2^w\setminus\{0\}\) be the set of distinct differences for the unequal pairs whose collisions count as errors, fixed independently of a uniform \(b\times w\) binary matrix \(H\). For \(S\subseteq D\), elementary linear algebra gives

\[
 \Pr[Hd=0\text{ for all }d\in S]=2^{-b\operatorname{rank}(S)}.
\]

Consequently, with \(r=\operatorname{rank}\(D\)\),

\[
 \Pr[\text{no collision on }D]
 =\sum_{S\subseteq D}(-1)^{|S|}2^{-b\operatorname{rank}(S)}
 =2^{-br}\chi_{M\(D\)}(2^b).
\]

This is the **Crapo–Rota Critical Theorem**, not a new rank-sensitive contract theorem. Britz, **Extensions of the Critical Theorem**, Discrete Mathematics 305 (2005), 55–73 (`britz2005critical`), states the characteristic-polynomial subset expansion and restates the Critical Theorem as Theorem 2; see [publisher](https://www.sciencedirect.com/science/article/pii/S0012365X05005145) and [author-uploaded full text](https://www.researchgate.net/profile/Thomas-Britz/publication/222577568_Extensions_of_the_Critical_Theorem/links/5bd8f385299bf1124faf6980/Extensions-of-the-Critical-Theorem.pdf). It attributes the original theorem to Crapo–Rota (1970), Chapter 16, Theorem 1. Each row of \(H\) induces a uniformly random codeword on \(D\); requiring full combined support is exactly its counted event.

**Assessment:** this gives an exact finite guarantee for a specified linear family. It does not give a generally compact or fast computation: the displayed expansion has \(2^{|D|}\) subsets, and total rank alone does not determine the characteristic polynomial. Duplicate differences collapse; zero differences represent genuine equalities, not FP events. Uniform full matrices, matrices conditioned on full rank, and arbitrary practical hashes have different distributions. Include the \(bw\)-bit matrix seed and compilation cost. Probability improvements matter operationally only if they change allocated bits or another measured decision.

## Strongest defensible next claim and rejection tests

The strongest nearby target is **a certified planner for an explicitly restricted query/schema family and actual finite encodings**, selecting among exact packed values, tuple-label retrieval, and modern AMQs while meeting a declared pointwise FP/FN contract. The candidate-restricted functional query above is a better stress test than unrestricted equality. This is a proposed research target; the search has not established that its integration is novel.

Reject or narrow the claim if any of the following occurs:

1. Constraint-aware sizing only improves a weak membership-scan baseline while exact IDs or retrieved fingerprints dominate.
2. Gains disappear after seeds, dictionaries, presence/index metadata, construction, and candidate processing are included.
3. The guarantee requires independent sources that the implemented filter/hash does not provide.
4. The main theorem reduces to safe probabilistic evaluation, classical limited independence, Goel–Gupta finite subset analysis, or the Critical Theorem without a further result.
5. Allocation gives negligible real savings like the prior 0.425% result, or helps only at an engineered integer threshold without a representative workload benefit.

The remaining evidence needed is a measured Pareto improvement and a precise explanation of what the finite contract adds beyond these baselines. No publication-readiness or exhaustive novelty claim follows from this audit.

## Verification record

Publisher/Crossref metadata and the cited primary copies were compared for authors, titles, dates, DOI, venue and pages where available. The 2026 Ribbon author list uses **Lorenz Hübschle**; its 2022 predecessor uses **Lorenz Hübschle-Schneider**. RPT+ is PVLDB 19(6), 1278–1290 (2026). Zeyl et al. is SIGMOD Companion. Bibliography fields not confidently verified were omitted. Access date throughout: 2026-10-13. This audit changes research notes only; it does not change or validate executable implementations.
