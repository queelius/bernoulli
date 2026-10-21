# Literature and novelty audit

Checked 2026-10-13. This is a bounded primary-source search, not an exhaustive novelty certificate. Read the original papers or author-hosted abstracts; search-engine dates were not treated as publication dates. Bibliographic entries are in `references.bib`.

## Decision

The broad proposal is already covered by several mature literatures. A calculus that records source identities, forms Boolean lineage, conditions on a small separator, and computes exact or interval probabilities is useful engineering, but it is not by itself a new research contribution. Renaming lineage probabilities as representation FP/FN rates changes the application semantics, not the counting problem.

The most useful publication direction in this workspace is a narrower revision of the relations paper: state precisely when canonicalization preserves marginal error rates while changing downstream query error and inference complexity. This should be presented as an application and synthesis of established inference/counting results unless a stronger new algorithm, characterization, or empirical finding survives comparison.

## Claims ruled out or sharply narrowed

| Proposed novelty | Closest established work | Assessment |
|---|---|---|
| Source identity and relational Boolean error algebra | Green–Karvounarakis–Tannen 2007; Dalvi–Suciu 2012 | Known provenance and probabilistic inference |
| Read-once exact evaluation and condition on reused sources | Koch–Olteanu 2008; Gatterbauer–Suciu 2014; scaled dissociation 2019 | Known factorization and Shannon expansion |
| Sound local bounds by replacing dependence with independent copies | Gatterbauer–Suciu 2014; Chou–Gatterbauer–Gogate 2018 | Direct overlap; use as baseline |
| Anytime exact-or-bounded inference | Van den Heuvel et al. 2019 | Direct overlap |
| Low-width joint data/provenance representation | Kanagal–Deshpande 2010; Amarilli–Bourhis–Senellart draft | Known; width must describe the combined object |
| Named uncertainty sources, a type discipline, and interval WMC | Liell-Cock–Staton 2026 | Very recent direct overlap |
| Probabilistic databases do not study integrity constraints | Flesca–Furfaro–Parisi; Koch–Olteanu | False as a broad claim |
| Easy read-once queries become hard after adding dependence | Kanagal–Deshpande 2010 | Explicit established result even for Markov-sequence dependence |
| Pairwise equality aliases plus 3-input constraints cause hardness | Cai–Lu–Xia 2012 Holant dichotomy | Established counting mechanism; relational specialization may be new in exposition |

## Implementable published baseline

For a monotone DNF with distinct variables inside each term, count the number `d_i` of terms in which source `i` appears. Fully dissociate repeated variables across terms. Evaluating the resulting read-once DNF with every copy weighted by `p_i` gives a sound upper bound. A sound symmetric lower bound uses copy weight `q_i = 1 - (1-p_i)^(1/d_i)`. These are disjunctive dissociations under Gatterbauer–Suciu's theorem; do not apply the assignments blindly to arbitrary mixed-polarity circuits.

Thus for term family `T`, evaluate `1 - product_t(1 - product_{i in t} w_i)` at `w_i=p_i` for the upper bound and `w_i=q_i` for the lower bound. This preserves linear work in total DNF occurrences. Deduplicate atoms within a term before counting occurrences. Constants and empty terms require ordinary Boolean simplification. The symmetric lower assignment is merely a baseline: optimized scaled dissociation can improve it substantially, and even a model-based lower bound can outperform it. Comparisons against only the symmetric lower bound must not claim superiority over all dissociation methods.

For a fixed exact database and output tuple, FP is the answer probability when the exact answer is false; FN is one minus that probability when true. Therefore a probability interval `[L,U]` becomes FP interval `[L,U]` or FN interval `[1-U,1-L]`. This translation is elementary. A population-level rate requires an explicit distribution over queried tuples or true databases.

## Nearby alternative: canonicalization and inference cost

The root/theory branch considers an informative contrast: start with a read-once DNF, then identify occurrences according to equality orbits. Binary witnesses with source multiplicity at most two form a graph of degree at most two and admit path/cycle dynamic programming. Raising multiplicity to three realizes bounded-degree independent-set counting. With three-atom witnesses, size-two orbits already realize cubic edge-cover counting after complementing the Bernoulli bits.

The exact counting barriers are known. Cai–Lu–Xia explicitly introduce separate bits at edge endpoints and then equality gates to obtain shared edge variables. Their Holant framework therefore already contains the essential aliasing operation. Amarilli–Monet 2022, Section 6, confirms edge-cover hardness on simple cubic planar graphs and identifies the primary citations. A graph/symmetry realization in approximate relations remains worth documenting, but should be labeled a corollary of those counting results.

No located source explicitly states the combined compressed-relation claim: canonical orbit evaluation can preserve individual FP/FN rates and reduce stored representatives while making the same downstream query harder to analyze. This absence is not a positive novelty proof. A publishable extension would need something beyond the translation, such as a complete tractability characterization for a practically important constraint/query family, a validated optimizer choosing constraint implementations under storage and error budgets, or calibration guarantees for actual compressed filters.

For projections of independent orbit trials, overlap of orbit supports creates dependence even when tuple fibers are disjoint. This corrects an important interaction in the current relations exposition. Covariance formulas obtained by complement products are useful derived identities, but do not alone establish novelty over lineage-based dependence analysis.

## Current directions worth testing, with risks

1. **Constraint-aware planning:** compare canonical representative tests, independent tuple tests plus repair, and ordinary tuple-independent filters at fixed storage/recall/error budgets. Need a real construction and workload; idealized independent coin tables cannot support a systems performance claim.
2. **Calibration under reused construction randomness:** distinguish per-construction guarantees, over-random-seed guarantees, and observed query frequencies. Repeated false positives and adaptive selection are well studied in AMQ literature; a contribution must go beyond observing that repetition violates fresh-trial independence.
3. **Certified bounded inference in bernoulli-py:** valuable artifact and correctness improvement. Use published techniques transparently; a software contribution requires comparative usability/performance evidence rather than a new-theory claim.

## Source ledger

### green2007provenance

- Todd J. Green, Grigoris Karvounarakis, Val Tannen. *Provenance Semirings*. PODS 2007, pp. 31–40. DOI: 10.1145/1265530.1265535.
- Primary PDF: https://www.cs.ucdavis.edu/~green/papers/pods07.pdf
- Verified abstract: relational algebra over probabilistic, incomplete, bag, and provenance annotations fits a semiring framework. Eliminates novelty of a generic annotation algebra.
- Limit: semiring arithmetic does not permit multiplying repeated-event marginals as though independent; Boolean provenance must retain identities before probability evaluation.

### dalvi2012dichotomy

- Nilesh Dalvi, Dan Suciu. *The Dichotomy of Probabilistic Inference for Unions of Conjunctive Queries*. JACM 59(6), Article 30, 2012. DOI: 10.1145/2395116.2395119.
- Author PDF: https://homes.cs.washington.edu/~suciu/dichotomyUCQ-with-acm-cls.pdf
- Verified conclusion: fixed UCQs over tuple-independent databases have a PTIME/#P-hard data-complexity dichotomy. Safety can depend on inclusion–exclusion/Möbius cancellation; read-once is not the whole tractable class.

### koch2008conditioning

- Christoph Koch, Dan Olteanu. *Conditioning Probabilistic Databases*. 2008.
- https://arxiv.org/abs/0803.2212
- Verified author abstract: conditioning on additional evidence, materialized posterior databases, exact confidence computation, and search/decomposition based on Davis–Putnam. Conditioning and decomposition are not new proposed primitives here.

### re2007views

- Christopher Ré, Dan Suciu. *Materialized Views in Probabilistic Databases: For Information Exchange and Query Optimization (Full Version)*. University of Washington Technical Report TR2007-03-02, 2007; title page verified.
- Primary PDF: https://cs.stanford.edu/people/chrismre/papers/prob_materialized_views_TR.pdf
- Verified Sections 2 and 4, Appendix 10: independent blocks and partial representability let users consume views without full lineage when a query does not depend on omitted correlations. Theorem 10.1 characterizes independence for all probability assignments by absence of a shared influential variable. Strong precedent for compact source/dependence contracts. This is not the same as pointwise independence at a single parameter assignment.

### kanagal2010lineage

- Bhargav Kanagal, Amol Deshpande. *Lineage Processing on Correlated Probabilistic Databases*. SIGMOD 2010, pp. 675–686.
- Author-hosted record: https://research.google/pubs/lineage-processing-on-correlated-probabilistic-databases/
- Verified abstract: even read-once lineage evaluation becomes #P-complete for Markov-sequence correlations. The lwidth parameter controls exact inference and message passing. This explicitly anticipates the easy-query/hard-dependence contrast.
- Limit: the page title says “on”; other bibliography records use “over”. Resolve publication-title spelling from final publisher PDF if included in a submitted paper.

### gatterbauer2014bounds

- Wolfgang Gatterbauer, Dan Suciu. *Oblivious Bounds on the Probability of Boolean Functions*. ACM TODS 39(1), 2014.
- https://arxiv.org/abs/1409.6052 ; author PDF https://gatterbauer.name/download/tods2014_Dissociation.pdf
- Read theorem discussion and PDF formulas. Splits repeated variables into independent copies with locally assigned probabilities to obtain sound bounds. For positive disjunctive splitting, identical original probabilities upper-bound; lower assignments have product of complements equal to the original complement. “Oblivious” here is the paper's technical established term.

### gatterbauer2017propagation

- Wolfgang Gatterbauer, Dan Suciu. *Dissociation and Propagation for Approximate Lifted Inference with Standard Relational Database Management Systems*. VLDB Journal 2017; author preprint v4 June 2016.
- https://arxiv.org/abs/1310.6257
- Verified abstract: evaluate a bounded set of safe relational plans and minimize their upper bounds. Enumerating minimal plans accounts for schema information. The one-plan case recovers PTIME self-join-free CQs.
- Caveat: author project page has inconsistent page/issue metadata; bibliography intentionally omits those fields.

### chou2018dissociation

- Li Chou, Wolfgang Gatterbauer, Vibhav Gogate. *Dissociation-Based Oblivious Bounds for Weighted Model Counting*. UAI 2018, pp. 866–875.
- Proceedings PDF: https://www.auai.org/uai2018/proceedings/papers/312.pdf
- Verified theorem snippets and Algorithm 1: extends dissociation beyond monotone formulas, using logical structure of weighted 2CNF. Any claim that handling negation alone supplies novelty must compare here.

### vandenheuvel2019scaled

- Maarten Van den Heuvel, Peter Ivanov, Wolfgang Gatterbauer, Floris Geerts, Martin Theobald. *Anytime Approximation in Probabilistic Databases via Scaled Dissociations*. SIGMOD 2019. DOI: 10.1145/3299869.3319900.
- Author PDF: https://gatterbauer.name/download/sigmod2019_anytime_approximations_scaled_dissociations.pdf
- Metadata verified at author institutional repository: https://orbilu.uni.lu/handle/10993/41785?locale=en
- Read indexed primary PDF passages describing constrained lower-bound optimization, independent subformula decomposition, and repeated Shannon expansion. Direct PDF fetch intermittently timed out; indexed text was accessible. It shows why symmetric lower assignments are not a strong best-of-literature baseline. A numeric optimizer only finds candidate local optima; do not infer guaranteed global optimization from the theoretical optimal envelope.

### amarilli2015treedecomp

- Antoine Amarilli, Pierre Bourhis, Pierre Senellart. *Probabilities and Provenance via Tree Decompositions*. Author draft (PDF footer generated 2014; filename 2015); not a verified publication under this exact title.
- https://a3nm.net/publications/amarilli2015probabilities.pdf
- Verified full introduction: circuit-annotated instances and a joint width of data and annotations yield linear-time data complexity for fixed expressive queries under bounded width and unit-cost arithmetic. Use the later published descendants when preparing submission; do not falsely cite this draft as a conference paper.

### flesca2013constraints

- Sergio Flesca, Filippo Furfaro, Francesco Parisi. *Consistency Checking and Querying in Probabilistic Databases under Integrity Constraints*. Author preprint 2013; later JCSS publication.
- https://arxiv.org/abs/1303.3233
- Verified author abstract: respect both tuple marginals and denial constraints; quantify cautiously over all consistent interpretations, with tractable cases. Directly refutes the local introduction's blanket claim that PDB research does not ask constraint questions. Different from canonical orbit construction, but the distinction must be stated specifically.

### barthe2016union

- Gilles Barthe, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, Pierre-Yves Strub. *A Program Logic for Union Bounds*. ICALP 2016. DOI: 10.4230/LIPIcs.ICALP.2016.107.
- https://arxiv.org/abs/1602.05681
- Verified abstract and author PDF excerpt: aHL supports compositional failure-probability accounting, including interactive/adaptive examples. Independence-free union bounds are established, though often loose.

### li2023lilac

- John M. Li, Amal Ahmed, Steven Holtzen. *Lilac: A Modal Separation Logic for Conditional Probability*. PACMPL 7(PLDI), Article 112, 2023. DOI: 10.1145/3591226.
- https://arxiv.org/abs/2304.01339
- Verified abstract and publisher metadata: separating conjunction models independence and a modality supports conditional probability. A typed dependence-aware calculus must explain its narrower added value, not claim first compositional independence logic.

### liellcock2026imprecise

- Jack Liell-Cock, Sam Staton. *Imprecise Probabilistic Programming, Precisely: Credal Sets via Graded Monads, BDDs, and Semiring-Parametric Inference (Functional Pearl)*. PACMPL 10(ICFP), Article 300, 2026. DOI: 10.1145/3828698.
- https://arxiv.org/abs/2607.20801 ; full text https://arxiv.org/html/2607.20801v1
- Verified full-text introduction and contents: named epistemic uncertainty, a graded monad, BDD compilation, exact/gradient/interval inference. Distinguish an uncertain probability parameter from a shared random outcome: this paper does not erase that semantic distinction, but strongly preempts broad claims for named uncertainty plus interval WMC.

### ho2025basl

- Shing Hin Ho, Nicolas Wu, Azalea Raad. *Bayesian Separation Logic*. arXiv 2025; publisher title expands with “A Logical Foundation and Axiomatic Semantics for Probabilistic Programming”.
- https://arxiv.org/abs/2507.15530 ; related publisher DOI 10.1145/3776696.
- Verified abstract: Bayesian updating, unnormalized/conditional distributions and independence reasoning. Modern comparison point if conditional contracts enter the proposed scope; not itself a database implementation.

### greenhill2000complexity

- Catherine Greenhill. *The Complexity of Counting Colourings and Independent Sets in Sparse Graphs and Hypergraphs*. Computational Complexity 9(1), 52–72, 2000.
- Author PDF: https://web.maths.unsw.edu.au/~csg/papers/complexity.pdf
- Verified Theorem 3.1: independent-set counting is #P-complete for cubic graphs. Supports the binary-witness/three-alias hardness corollary.

### cai2012holographic

- Jin-Yi Cai, Pinyan Lu, Mingji Xia. *Holographic Reduction, Interpolation and Hardness*. Computational Complexity 21(4), 573–604, 2012.
- Author PDF: https://pages.cs.wisc.edu/~jyc/880/HRIH.pdf
- Verified introduction and Theorem 6.2 table (PDF page 14): equality signature `[1,0,1]` with OR signature `[0,1,1,1]` is marked #P-complete even for planar graphs. Holant assigns separate endpoint bits and uses equality gates to join them. This is the established framework for the size-two-alias/three-atom threshold.

### amarilli2022matchings

- Antoine Amarilli, Mikaël Monet. *Weighted Counting of Matchings in Unbounded-Treewidth Graph Families*. MFCS 2022; full version revised 2023.
- https://arxiv.org/abs/2205.00851 ; full PDF https://arxiv.org/pdf/2205.00851
- Verified Section 6: edge-cover weighted-counting hardness for subgraph-closed treewidth-constructible families under ZPP reductions; cites cubic planar hardness and simple-graph refinement. Its topology-sensitive result is stronger than merely saying large orbit sharing can make inference difficult. Preserve restrictions when citing.

### amarilli2025approximating

- Antoine Amarilli, Timothy van Bremen, Octave Gaspard, Kuldeep S. Meel. *Approximating Queries on Probabilistic Graphs*. LMCS 21(4), 2025. DOI: 10.46298/lmcs-21(4:30)2025.
- Author record and abstract: https://www.cs.utoronto.ca/~meel/publications/b2hd-ABGM25.html
- Verified abstract: combined FPRAS and inapproximability landscape for graph queries; warns that self-join-freeness and bounded hypertree width hypotheses cannot simply be dropped. Exact #P-hardness alone does not imply no useful approximation scheme.

### bender2017adaptivity

- Michael A. Bender, Martin Farach-Colton, Mayank Goswami, Rob Johnson, Samuel McCauley, Shikha Singh. *Bloom Filters, Adaptivity, and the Dictionary Problem*. Author preprint 2017, revised 2018.
- https://arxiv.org/abs/1711.01616
- Verified abstract: one-query guarantees differ from guarantees conditional on previous answers; reusing discovered false positives defeats ordinary AMQ rates. Essential operational caveat for real filter instantiations. Do not claim adaptive safety from a fixed-query construction-randomness model.

## Search limitations

The closest major collisions are established directly. There was no exhaustive citation-graph traversal, formal equivalence proof to every prior system, or attempt to certify that a particular relational corollary has never appeared. No new method should be called novel solely because this search found no identical title. Venue fit and comparative implementation remain root-branch decisions.

## Follow-up: worst-input one-sided error and certificates

Audited 2026-10-13 at the root branch's request. This is a different target from fixed-truth-profile WMC: the exact truth profile is arbitrary, not sampled from a prior, and the contract takes a maximum over all profiles on which the query's exact answer is false (dually, true).

### Candidate and assessment

For a nonconstant monotone Boolean function \(F\), let \(s_0(F)\) be maximum sensitivity at a false input. Generate \(Y_i=x_i\lor E_i\), where the \(E_i\) are independent Bernoulli variables of fixed parameters \(\alpha_i\). Each source is sampled once, including when its identity occurs repeatedly in the query. Then the candidate exact formula is

\[
\max_{x:F(x)=0}\Pr(F(Y)=1)
 =\max_{C\in\mathcal C_0(F)}
       \left[1-\prod_{i\in C}(1-\alpha_i)\right],
\]

where \(\mathcal C_0(F)\) is the family of inclusion-minimal sets of coordinates whose being zero forces \(F=0\). Equivalently, for positive DNF, these are inclusion-minimal transversals of its witness hypergraph. For common rate \(\alpha\), this reduces to \(1-(1-\alpha)^{s_0(F)}\), since \(\max_{C\in\mathcal C_0}|C|=C_0(F)=s_0(F)\). The distinction between **maximum size of an inclusion-minimal transversal** and a minimum transversal is essential.

The dual statement uses minimal true certificates and one-sided deletions. Without source independence, but allowing every coupling having marginal error at most \(\alpha\), the worst-case value over couplings and truth profiles is \(\min(1,\alpha s_0(F))\). That is the sharp union bound after the same boundary-state reduction, not a new general dependence inequality.

**Novelty status: unresolved exact precedent; no standalone contribution established.** The search found primary predecessors for pointwise noise stability, the monotone certificate/sensitivity identity, and the graph optimization problem. It did not locate an explicit published statement identical to the displayed one-sided maximum. It would be equally unjustified to claim that the exact formula has already been published and to claim that it is novel merely because it was not located.

The strongest reason for modest positioning is the short derivation. Monotone coupling lets a false input be extended to a maximal false input without decreasing its acceptance probability. At such a boundary input, flipping any remaining zero changes the answer; hence the answer remains false exactly when all those bits survive unchanged. Their zero set is a minimal zero certificate. Taking the maximum yields the formula. This is an elementary consequence of established Boolean boundary structure and the independent OR probability identity. It can be useful even if not sufficient as the sole theoretical novelty of a paper.

### What the related results do and do not cover

- **Pointwise noise stability:** Gopalan et al. 2016, Lemma 15, bounds the error under independent *two-sided* flips at every fixed input by \(2\delta s(F)\), for \(0<\delta\le 1/2\). This is substantially closer than average-case noise sensitivity, but is not the proposed exact *one-sided* extremal identity. Their definition also explicitly distinguishes a fixed input from averaging over a uniform input.
- **Certificates:** Blanc et al. 2022, published Fact 4.2 (arXiv Fact 4.1), credits \(C(F)=s(F)\) for monotone functions to Nisan 1989. The boundary argument specializes this standard relationship to the two output classes. The original Nisan full text was not accessible in this audit; publisher metadata and this explicit attribution were verified.
- **Reliability and fault trees:** searches for maximal false vectors, minimal cut sets, and worst-case reliability located the standard boundary/cut-set framework and product evaluation. They did not establish a direct prior statement of this worst-exact-input noise contract. Ordinary system reliability fixes a component-status probability law; minimizing over starting states is an additional quantifier. Do not cite a generic reliability formula as proof that the exact candidate was previously stated.
- **Noisy circuits:** gate-failure tolerance and depth lower bounds solve a different problem from passing a fixed exact source vector through independent one-sided channels and then evaluating a noiseless Boolean query. No direct collision was verified in that branch.

### Consequences for a useful restricted query class

For graph DNF \(F_G=\bigvee_{uv\in E}x_ux_v\), the zero certificates are minimal vertex covers. Their complements are maximal independent sets, so

\[
s_0(F_G)=|V|-i(G),
\]

where \(i(G)\) is the minimum cardinality of a maximal independent set, equivalently the independent domination number. This is an elementary complement identity, not a new graph parameter. It means that a compact scalar contract need not be cheap to *compute*: independent domination is NP-complete even on cubic bipartite graphs (Liu, Poon, Lin 2015, Theorem 1). For \(0<\alpha<1\), computing the exact scalar rate can recover that integer parameter.

For heterogeneous rates below one, write \(w_i=-\log(1-\alpha_i)\). The logarithm of the certificate's survival probability turns maximum certificate weight into total vertex weight minus minimum **weighted** independent domination. Existing graph algorithms are therefore the appropriate starting point, not enumeration renamed as a new calculus. Paths and cycles give a natural easy corner; their \(\lceil n/3\rceil\) independent domination formula follows by elementary covering and explicit construction. Trees and width-bounded graphs suggest standard dynamic programs, but this audit does not claim a newly discovered algorithm for them.

The resulting calibration condition, \(\alpha\le 1-(1-\varepsilon)^{1/s_0(F)}\), is a useful interpretation: a filter's tuple budget can be selected from a query-level target without inventing a truth prior. A defensible added contribution would need to show how this changes a real constraint-preserving filter's design, query planning, or storage/runtime tradeoff beyond simply evaluating existing certificate algorithms.

### Assumptions that must remain visible

1. Equal aliases must first be identified. Independence concerns distinct source bits, not syntactic occurrences. A filter's shared seed does not automatically instantiate independent bits.
2. The result takes the maximum over all quotient truth profiles. Extra constraints such as transitivity may forbid the extremizing profile. The unrestricted value remains an upper bound, but equality then requires a feasibility argument.
3. The displayed formula is a construction-randomness guarantee for a query fixed independently of that randomness. Repeated queries return the same frozen source bits. It is not a conditional guarantee after observing previous outcomes.
4. One-sided channels and monotonicity are material. Simultaneous false negatives remove the product identity at a maximal false input, and nonmonotone formulas do not admit this boundary reduction.
5. Constant functions require a convention for maxima over empty truth classes. Rates zero/one should be handled directly rather than only via logarithms.

### Follow-up source ledger

#### gopalan2016smooth

- Parikshit Gopalan, Noam Nisan, Rocco A. Servedio, Kunal Talwar, Avi Wigderson. *Smooth Boolean Functions are Easy: Efficient Algorithms for Low-Sensitivity Functions*. ITCS 2016, 59–70. DOI: 10.1145/2840728.2840738.
- Author-hosted publication PDF: https://www.cs.columbia.edu/~rocco/Public/GNSTW.pdf ; full preprint https://arxiv.org/abs/1508.02420
- Verified publication title page, §2.2 definition and Lemma 15 with its random-walk proof. Use the non-strict bound at \(\delta=0\); the printed strict inequality includes zero in its displayed domain but the endpoint is trivially equality.

#### blanc2022counterfactuals

- Guy Blanc, Caleb Koch, Jane Lange, Li-Yang Tan. *A query-optimal algorithm for finding counterfactuals*. ICML 2022, PMLR 162, 2075–2090.
- Publisher record: https://proceedings.mlr.press/v162/blanc22a.html ; PDF https://proceedings.mlr.press/v162/blanc22a/blanc22a.pdf
- Verified publisher metadata and published Fact 4.2: monotone certificate complexity equals sensitivity, attributed to Nisan 1989. This paper's main algorithm concerns optimal counterfactual search, not the proposed stochastic error contract.

#### nisan1991crew

- Noam Nisan. *CREW PRAMs and Decision Trees*. SIAM Journal on Computing 20(6), 999–1007, 1991. DOI: 10.1137/0220062. Conference version STOC 1989, 327–335.
- Publisher record: https://epubs.siam.org/doi/10.1137/0220062
- Metadata and abstract verified; theorem-specific attribution checked through Blanc et al., not independently against the original full paper. Avoid implying otherwise.

#### liu2015independent

- Ching-Hao Liu, Sheung-Hung Poon, Jin-Yong Lin. *Independent dominating set problem revisited*. Theoretical Computer Science 562, 1–22, 2015. DOI: 10.1016/j.tcs.2014.09.001.
- Publisher: https://www.sciencedirect.com/science/article/pii/S0304397514006537 ; author publication list https://www.cs.nthu.edu.tw/~spoon/pubs/pubs.htm
- Verified indexed primary full-text abstract, §2.1, and conclusion. Cubic bipartite NP-completeness, subcubic grid hardness, FPT algorithms, and weighted variants are existing results. Publisher direct fetching intermittently returned 403; search extraction included the actual theorem/proof section. Author list corroborated by the author-hosted list and author-uploaded article title page. A preliminary message accidentally said “Liu/Song”; it was corrected before this ledger was written.

### Publication decision for this alternative

Retain the theorem as a clear, self-contained contract corollary and connect it to the existing relations manuscript. The truth-prior-free interpretation is more useful for its stated approximate-data model than treating tuple truths as a new probability distribution. Still, the search has not established enough independent algorithmic or mathematical novelty to recommend a standalone submission or a specific theory venue for this scalar theorem. The warranted next test is a concrete calibration or design advantage on a restricted query family with a justified independence model. Official venue screening should follow evidence of that contribution; no external submission is implied.
