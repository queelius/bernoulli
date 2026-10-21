# Dependence after constraint-preserving quotienting

Date: 2026-10-13. This is a research note, not a claim of original counting-complexity results.

## 1. Semantics and the candidate contribution

Fix an exact relation and a finite collection of ground tuple tests. An equivalence relation on tuple tests gives **canonical source IDs**. Every equivalence class must be homogeneous in exact membership. For source `i`, draw one bit `Z_i` at construction and reuse it at every occurrence. Distinct source bits are mutually independent in the model studied here. For exact membership `x_i`, the source acceptance probability is `p_i = alpha_i` when `x_i=0`, and `p_i = 1-beta_i` when `x_i=1`. Here alpha and beta are FPR and FNR, respectively.

This model describes a frozen random realization. It does not resample a tuple upon every query, assert that different bits in an actual Bloom filter are independent, or condition on adaptive observations of the construction. Those are different models requiring additional evidence or analysis.

A positive relational query at a fixed output tuple has monotone Boolean lineage

`F(Z) = OR_{j=1}^k AND_{i in S_j} Z_i`.

Deduplicate sources **inside** each witness, eliminate duplicate witnesses, and absorb every witness that contains another. The resulting `S_j` are sets. A tuple's exact answer is `F(x)`. Conditional on that fixed exact relation, its FPR is `P(F(Z)=1)` if `F(x)=0`; its FNR is `1-P(F(Z)=1)` if `F(x)=1`. An average over unknown exact relations is a further modeling choice, not implied by a probability calculation for a fixed `x`.

Define witness width `w = max_j |S_j|` and source occurrence `d = max_i |{j:i in S_j}|`. These are properties of the normalized lineage. An orbit-size bound implies an occurrence bound only when the **prequotient lineage is read once**. A size-one orbit can occur arbitrarily many times in a self-join or reused subquery.

The promising narrow statement is a precise interface between constraint-preserving storage and inference: canonical quotienting preserves per-tuple error rates while changing the lineage graph, sometimes from read-once exact evaluation to #P-hard exact evaluation. The positive contract class `(w,d) <= (2,2)` is linear in arithmetic operations. This is an applied synthesis of classical counting results, not a new general-purpose probability calculus. Whether its relational packaging supports publication requires scrutiny beyond the proof.

## 2. Projection: an exact correction to independence reasoning

Let `A_s` be the set of canonical sources appearing in the fiber of projected tuple `s`. Its output bit is `Y_s = OR_{i in A_s} Z_i`. Write `q_C = product_{i in C}(1-p_i)`, with `q_empty=1`. Then

`P(Y_s=1) = 1-q_{A_s}`,

and, for two projected tuples,

`Cov(Y_s,Y_t) = q_{A_s\A_t} q_{A_t\A_s} q_{A_s intersect A_t} (1-q_{A_s intersect A_t})`.

**Proof.** The covariance of the two indicators equals the covariance of their complements. Both complements equal one precisely when all sources in `A_s union A_t` equal zero, so covariance is `q_{A_s union A_t}-q_{A_s}q_{A_t}`. Factor the three disjoint source sets to obtain the formula.

If every participating source has `0<p_i<1`, two nonconstant projected bits are independent exactly when their canonical supports are disjoint. Consequently a family of projected bits is mutually independent exactly when its nonempty source supports are pairwise disjoint. The forward implication follows from the strictly positive pairwise covariance for any overlap; the reverse follows from independence of disjoint collections of independent sources. Degenerate source probabilities need separate treatment.

Example: project a symmetric two-tuple orbit `{(a,b),(b,a)}` onto the first coordinate. The two tuple fibers are disjoint as sets of tuples, but their source supports are identical. Both output bits equal one `Bernoulli(p)` variable and have covariance `p(1-p)`. No join is needed to create dependence at the projected tuple level.

**Relationship to current manuscript.** `papers/bernoulli_relations/sections/rel_algebra.tex` explicitly assumes independent per-tuple trials at the start. Its projection theorem is correct under that stated assumption. It is inapplicable after the canonical test of `sections/properties.tex`, which introduces within-orbit dependence. A compositional account must carry that distinction. This is an assumption-boundary correction, not a counterexample to the properly scoped theorem.

## 3. A complete easy corner for positive witness queries

**Proposition.** A normalized monotone DNF with `w<=2` and `d<=2` has exactly computable acceptance probability in `O(L)` arithmetic operations and `O(L)` representation space, where `L` is its number of literal occurrences. Rational probabilities give polynomial bit complexity; the claim is not linear bit complexity.

**Proof.** An empty witness makes the formula identically true. Otherwise separate singleton witnesses `U`. To have `F=0`, every `Z_i` for `i in U` must be zero. This contributes `product_{i in U}(1-p_i)`. Absorption removes all other witnesses containing such a variable.

Each remaining binary witness `{u,v}` is an edge of a simple graph `G`. The event `F=0` is exactly that the set of sources whose bits equal one is an independent vertex set. Source occurrence at most two gives maximum graph degree at most two. Each component is a path, cycle, or isolated vertex. Components involve disjoint sources, so their probabilities multiply.

For a path `1,...,r`, let `a_i` and `b_i` be the probabilities that the first `i` positions contain no adjacent ones and the last bit is zero or one. Initialize `a_1=1-p_1`, `b_1=p_1`. Then

`a_i=(a_{i-1}+b_{i-1})(1-p_i)`,

`b_i=a_{i-1}p_i`.

The path contribution is `a_r+b_r`. For a cycle of length at least three, condition on the first bit, run the same recurrence with initial values `(1-p_1,0)` and `(0,p_1)`, and in the second case retain only the final zero state. This excludes the last–first adjacent-one case. Each edge and source is processed a constant number of times. Subtract the resulting no-witness probability from one.

### Interval source probabilities

For any monotone lineage, independent source rates in the Cartesian box `p_i in [l_i,u_i]` have the **sharp** acceptance envelope

`[P_l(F=1), P_u(F=1)]`.

Couple source bits through independent uniforms `V_i` and put `Z_i(p)=1[V_i<=p_i]`. The output is pointwise monotone in every `p_i`, proving the inequalities; both endpoints are feasible and attained. Thus the easy-corner algorithm yields exact sharp interval contracts with two evaluations. This result presumes a fixed exact-membership profile, independent sources, and a full Cartesian uncertainty set. It does not justify separate optimization over rates constrained by a shared parameter, or quantification over unknown exact truth profiles. Monotone endpoint optimization is classical, not novel here.

## 4. Binary witnesses: occurrence three already reaches #P hardness

**Proposition.** Exact acceptance probability for positive binary-witness lineage with `d<=3` is #P-hard, even when all source probabilities are `1/2`.

**Proof.** For a simple graph `G` of maximum degree three, set

`F_G = OR_{uv in E(G)} (Z_u AND Z_v)`.

The assignments with `F_G=0` are exactly the independent sets of `G`, so

`P(F_G=1) = 1 - #IndependentSets(G)/2^{|V(G)|}`.

Every witness has width two and every source occurs at most three times. Exact probability evaluation recovers the independent-set count by one arithmetic transformation. Counting independent sets in three-regular graphs is #P-complete (Greenhill 2000, Theorem 3.1). The numerator counts satisfying assignments, so this is ordinary finite counting rather than a numerical-precision obstacle.

To obtain the lineage by quotienting, initially assign a fresh source to every edge endpoint occurrence. The prequotient DNF is read once. Identify all occurrences belonging to a common vertex; each class has size at most three. For nondegenerate homogeneous rates, all single tuple marginals are unchanged. This is a reformulation of known bounded-degree independent-set hardness.

## 5. Strict symmetry: size-two orbits suffice with width-three witnesses

**Proposition.** There is a fixed positive relational query whose prequotient instances have read-once lineage, but whose exact false-positive probability under canonical symmetry is #P-hard to compute. All symmetry orbits have size two on the queried tuples, the source FPR is uniformly `1/2`, and the source FNR can be zero.

**Construction.** Let `G=(V,E)` be a simple three-regular graph. For each vertex `v`, choose one ordering `(a_v,b_v,c_v)` of its three distinct neighbors and put exactly one tuple `(v,a_v,b_v,c_v)` into an exact deterministic relation `D`. Use the fixed Boolean conjunctive query

`Q = exists v,a,b,c. D(v,a,b,c) AND R(v,a) AND R(v,b) AND R(v,c)`.

The exact relation `R` contains no tuple on `V x V`, so `Q` is false. To avoid depending on whether a formalism permits nonzero FPR for an empty relation, let `R` also contain an unqueried symmetric sentinel pair on two fresh vertices not present in `D`; the exact relation is then nonempty and symmetric.

Before canonical symmetry, draw independent bits for directed tuple tests `R(v,u)`. Every directed arc appears in exactly one witness, so the lineage is read once and

`P(Q=1) = 1 - (1-p^3)^{|V|}`.

After canonical symmetry, `R(u,v)` and `R(v,u)` read the same independent undirected-edge bit `Z_{uv}`. This imposes precisely the standard tuple-swapping symmetry, not an arbitrary equivalence relation. Each edge source appears in the two endpoint witnesses; each witness has three distinct sources. Every tuple marginal is still `p`, and every individual witness marginal is still `p^3`.

The output is false exactly when every vertex has at least one incident edge with bit zero. Thus the zero edges form an edge cover of `G`. At `p=1/2`,

`FPR(Q) = 1 - #EdgeCovers(G)/2^{|E|}`.

Counting edge covers is #P-hard even on simple planar three-regular graphs; the literature branch verified the primary-source chain through Cai–Lu–Xia (2012), plus the explicit statement in Amarilli–Monet (2022), Section 6. Therefore exact FPR computation is #P-hard for this fixed query family. Arbitrarily assign TPR one on the unqueried true sentinel orbit, obtaining zero source FNR without changing the reduction.

**Consequences and limits.** Marginal error preservation and small local orbits do not imply tractable exact query contracts. Under the read-once-before-quotient promise, `(w,d)=(2,2)` is easy, while `(2,3)` and `(3,2)` already permit hard instances. These are tractability boundaries between restricted classes, not claims that every instance outside the easy corner is hard. A symmetry orbit bound does not control `d` when tuple occurrences were already reused before quotienting.

The counting core is classical Holant/equality-constraint structure. Kanagal–Deshpande (2010) already shows that correlations can make read-once or hierarchical lineage difficult. The strict symmetric-relation realization is a precise application, with **novelty not established**. It should not be presented as a new general #P-hardness theorem without a more exhaustive targeted comparison.

## 6. Safe baselines and counterexamples

Under independent canonical bits, let `w_j=product_{i in S_j}p_i`. Positive association of monotone Boolean events gives

`max_j w_j <= P(F=1) <= 1-product_j(1-w_j) <= min(1,sum_j w_j)`.

The upper bound follows because all complementary witness events are decreasing, hence positively associated under a product measure. Any subset `J` of pairwise source-disjoint witnesses improves the lower bound to `1-product_{j in J}(1-w_j)`. Published dissociation methods give stronger general bounds and are required comparison baselines; none of this is a new bounding method.

This implies that treating **deduplicated monotone witnesses** as independent overestimates their union probability. It yields a sound FPR upper bound for a false exact answer, but a FNR **lower** bound for a true exact answer. It does not certify an FNR upper bound. Treating repeated sources inside a witness as independent is unsound: `Z AND Z=Z` has probability `p`, whereas multiplication returns `p^2`. The two issues must not be conflated.

If distinct canonical sources are not independent, the positive-association bound need not hold. For example, two mutually exclusive events of probability `1/2` have union probability one, exceeding the independent expression `3/4`. A real approximate-filter implementation needs an independent-source guarantee, an explicit correlated model, or dependence-robust bounds.

## 7. Evidence standard and next-step recommendation

The proofs establish a coherent result but not an independent original algorithm. A publication based only on named sources, Boolean lineage, product probability evaluation, endpoint interval propagation, or read-once-to-correlated hardness would overlap substantial prior work.

The strongest honest package currently available is an extension of the relations paper: scope its independence assumptions, add the projection covariance and symmetry-hardness application, implement source-aware compilation with recognized probability backends, and demonstrate that physically meaningful constraint-aware storage/query workloads benefit. A separate methods paper needs an additional new theorem, new inference algorithm, or convincing empirical result unavailable from existing lineage/dissociation tooling.

For implementation validation use exact rational enumeration on small cases, check the reduction against independently counted edge covers, check the path/cycle recurrence against enumeration, and check interval endpoints and degenerate probabilities. Experimental agreement is evidence for the implementation; it is not a proof of the complexity reductions.

## 8. Nearby alternative: exact truth-prior-free one-sided contracts

This alternative answers a different question from fixed-profile weighted model counting. Instead of receiving an exact truth profile `x`, it asks for a uniform error guarantee over **all** exact profiles that give the specified exact output. All source assignments must be admissible after the equality quotient; further constraints such as functionality or transitivity can invalidate sharpness, although the resulting inequalities remain upper bounds.

Let `F:{0,1}^n->{0,1}` be monotone. Its 0-sensitivity `s_0(F)` is the maximum, over `F(x)=0`, of the number of coordinates whose change from zero to one makes `F=1`. Define 1-sensitivity dually. For a constant function take both relevant worst-case errors and sensitivities to be zero. Let `B_0` denote the inclusion-maximal false assignments and `B_1` the inclusion-minimal true assignments.

Assigning zero to an extremum over an empty truth class is a mathematical convention for these formulas. The companion prototype instead returns `None` when the conditioning class is empty, to distinguish an undefined conditional error rate from a measured or proved zero error on a nonempty class.

### Exact homogeneous theorem

Under one-sided FP noise, each exact true source stays one, and each exact false source becomes one independently with probability `alpha`. Then

`max_{x:F(x)=0} P(F(Y)=1 | x) = 1-(1-alpha)^{s_0(F)}`.

Under one-sided FN noise, each exact false source stays zero, and each exact true source becomes zero independently with probability `beta`. Then

`max_{x:F(x)=1} P(F(Y)=0 | x) = 1-(1-beta)^{s_1(F)}`.

**Proof, FP case.** Couple all profiles by one independent uniform per source, setting `Y_i(x)=x_i OR 1[V_i<=alpha]`. If `x<=x'`, then `Y(x)<=Y(x')` pointwise, hence the acceptance probability is monotone in the exact profile. Extend any false profile to a maximal false profile `b`; its acceptance probability is no smaller. At `b`, changing any remaining zero to one makes the function true. Since true bits never disappear, `F(Y)=0` precisely when **every** zero of `b` stays zero. If there are `k` such coordinates, FPR is `1-(1-alpha)^k`.

The maximum zero count on `B_0` is exactly `s_0(F)`. Every zero at a maximal false profile is pivotal, giving one inequality. Conversely, extend any false `x` to a maximal false `b`. A pivotal zero of `x` cannot have been changed to one in `b`, because monotonicity would then force `F(b)=1`. It remains pivotal at `b`, again by monotonicity. Thus the extension has at least as many pivotal zeros. Maximizing gives equality. The FN theorem follows either by the dual function `1-F(1-x)` or by shrinking a true profile to a minimal true profile. There every remaining one is pivotal, so the first deletion destroys the answer.

These sensitivities are the standard one-sided certificate complexities for monotone functions. For positive witness DNF, `s_1` is the maximum size of a minimal witness; `s_0` is the maximum size of an inclusion-minimal hitting set of the witness family. This is an exact contract and an algorithmic reduction to existing combinatorial invariants, **not presently an originality claim**.

### Heterogeneous extension

With independent, potentially different false-positive rates `alpha_i`,

`worst_FPR = max_{b in B_0} [1-product_{i:b_i=0}(1-alpha_i)]`.

With independent false-negative rates `beta_i`,

`worst_FNR = max_{b in B_1} [1-product_{i:b_i=1}(1-beta_i)]`.

The same coupling and boundary proof applies. If the rates are upper bounds rather than equalities, these formulas are sharp worst-case upper envelopes because the upper rates themselves are feasible. No prior over exact relations is needed.

For two-sided noise, the expressions remain sound upper bounds: suppressing false negatives can only increase the output and suppressing false positives can only decrease it. They are generally not sharp when both noise rates are specified and nonzero. Example: for `F=X_1 AND X_2`, uniform `alpha<=1-beta`, the exact worst FPR is `alpha(1-beta)`, whereas the certificate bound is `alpha`. Do not present the one-sided identity as a sharp two-sided formula.

### Sharp distribution-free counterpart

If false-positive bit errors may have arbitrary dependence but each has marginal at most `alpha`, the sharp uniform FP envelope is

`sup_{x:F(x)=0, admissible couplings} P(F(Y)=1|x) = min(1,alpha*s_0(F))`.

For a fixed profile, select a zero certificate of size at most `s_0(F)`. The output cannot become true unless at least one certified zero flips; the union bound proves the upper inequality without needing independence or a coupling monotone across profiles. At a maximal false profile with exactly `s_0(F)` zeros, every such flip suffices. The maximum union probability of `k` events each of probability `alpha` is `min(1,k*alpha)`: disjoint intervals attain it when `k*alpha<=1`, and equal-length cyclic intervals covering the unit circle attain it otherwise. This proves sharpness. The heterogeneous envelope is `max_{b in B_0} min(1,sum_{i:b_i=0}alpha_i)` by the same certificate argument and construction. The FN version is dual.

Thus source identity and an actual independence guarantee have different roles: identity removes duplicate coordinates and changes the certificate invariant; independence sharpens the union bound from `min(1,k*alpha)` to `1-(1-alpha)^k`.

### Closed forms on the easy graph class

For `F_G=OR_{uv in E}(Z_u AND Z_v)`, the maximal false profiles are maximal independent sets. Therefore

`s_0(F_G) = |V|-i(G)`,

where `i(G)` is the minimum cardinality of a maximal independent set, equivalently the independent domination number. Also `s_1(F_G)=2` when at least one edge exists.

For a path `P_n` and a cycle `C_n` (cycle `n>=3`), `i(G)=ceil(n/3)`. To prove the lower bound, an independent dominating set's selected vertex covers at most itself and its two neighbors. For a path the upper bound is attained by vertices `2,5,...` when `n` is zero or two modulo three, with the appropriate final term, and by `1,4,...,n` when `n` is one modulo three. For a cycle, put `r=ceil(n/3)` selected vertices at cyclic gaps two or three: such gaps sum to `n` because `2r<=n<=3r`. They are independent and dominate the cycle. Independent domination numbers add across disconnected components.

Consequently, normalized binary witness lineage of source occurrence at most two, with singleton source set `U` and path/cycle components `G_c`, has

`s_0 = |U| + sum_c (|V(G_c)|-ceil(|V(G_c)|/3))`,

`s_1 = max witness size`,

with constant cases handled separately. The associated homogeneous one-sided worst-case contracts are computable in linear time without enumerating truth profiles or computing any model count.

For heterogeneous rates, weighted minimal-transversal optimization is needed. On paths this too has a constant-state dynamic program: let `q_i=1-alpha_i`; choose an independent dominating set `S` minimizing `product_{i notin S}q_i`. Track whether the current vertex is selected (`A`), unselected but dominated from the left (`B`), or unselected and awaiting domination from the right (`C`). Initialize `(A,B,C)=(1,unreachable,q_1)` and use `A'=min(B,C)`, `B'=q_i*A`, `C'=q_i*B`, accepting only `A,B` at the end. Unreachable states must be represented explicitly, especially when `q_i=0`. Closing a cycle requires a constant number of boundary cases. This is a standard weighted independent-domination dynamic program with multiplicative costs, not a new general algorithm.

### Publication assessment of this alternative

This formula is potentially a better fit for Bernoulli **error contracts** than the generic provenance implementation: it quantifies uniformly over unknown exact truth, distinguishes alias identity from independence, and has sharp distribution-free and independent cases. It is elementary once expressed in certificate language. A targeted literature search must determine whether this exact channel interpretation is already stated, and whether a useful new restricted-query algorithm or storage/error optimization follows. Lack of an exact keyword match is not evidence of novelty.

## Primary sources used or directly identified

- Catherine Greenhill, “The complexity of counting colourings and independent sets in sparse graphs and hypergraphs,” 2000, Theorem 3.1: https://web.maths.unsw.edu.au/~csg/papers/complexity.pdf
- Jin-Yi Cai, Pinyan Lu, Mingji Xia, “Holographic Reduction, Interpolation and Hardness,” *Computational Complexity* 21(4):573–604, 2012, preprint with Theorem 6.2: https://pages.cs.wisc.edu/~jyc/880/HRIH.pdf
- Antoine Amarilli and Mikaël Monet, “Weighted Counting of Matchings in Unbounded-Treewidth Graph Families,” arXiv:2205.00851, Section 6 supplies the explicit cubic planar edge-cover hardness reference chain: https://arxiv.org/abs/2205.00851
- Bhargav Kanagal and Amol Deshpande, “Lineage Processing over Correlated Probabilistic Databases,” SIGMOD 2010: https://research.google/pubs/lineage-processing-on-correlated-probabilistic-databases/
- Wolfgang Gatterbauer and Dan Suciu, “Oblivious Bounds on the Probability of Boolean Functions,” ACM TODS 2014: https://arxiv.org/abs/1409.6052

Source-title and identifier verification is recorded by the literature branch. Check bibliography metadata before reuse in a manuscript; this note does not certify originality.
