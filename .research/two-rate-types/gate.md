# Novelty gate: two-rate (FPR/FNR) types for approximate programs

Date: 2026-10-21. This was a bounded search: two parallel literature passes (PL/verification; probability, reliability, statistics, and databases) of roughly 60–70 tool calls each, plus my own targeted searches and a full-text read of the closest database prior. DOIs were checked against Crossref (the LIPIcs DOI against DataCite) unless marked UNVERIFIED. Absence from this search is not a proof of novelty.

## Verdict

**PASS, narrowly.** I found no prior that does all of the following at once:

- gives Boolean expressions a pair (ε, ω) indexed by the latent (exact) truth, as a worst case over latent valuations;
- propagates that pair compositionally through AND, OR, NOT, XOR and if/case;
- uses rules sound under arbitrary dependence by default, tightened only where independence is certified;
- has tightness results.

So there is no reason to STOP. Every per-node inequality, however, is classical, and several priors hold large pieces. The defensible contribution is the **packaging plus a few clean theorems**, not new inequalities:

- the latent-indexed semantics, which is what makes the pair compositional;
- the rules as best abstract transformers;
- read-once exactness in this latent-indexed setting;
- strict refinement of single-probability typing;
- the polarity (one-sidedness) theorem.

The paper must say that the arbitrary-dependence rules are derivable in aHL. It must also credit Fréchet/Boole, Berger's intersection-union test, Choudhury–Mohanram, and Shivakumar et al.

## Closest priors and exact overlap

| Prior | What it does | What it does not do | Overlap |
|---|---|---|---|
| **Barthe, Gaboardi, Grégoire, Hsu, Strub, "A Program Logic for Union Bounds" (aHL), ICALP 2016, LIPIcs 55:107, doi:10.4230/LIPIcs.ICALP.2016.107** | Judgments ⊢β c : Φ ⇒ Ψ, meaning Pr[¬Ψ] ≤ β for every initial memory satisfying Φ. [Seq] and [And] add failure probabilities; [Or] is a case rule on preconditions; [Rand] is a per-primitive axiom. The judgment e : Bool[ε, ω] is literally two aHL judgments, ⊢ε (exact=0) ⇒ (r=0) and ⊢ω (exact=1) ⇒ (r=1). The dependent AND rule ε = max(ε1, ε2) follows by [Rand]+[Frame]+[Seq] in each case, then [Weak]+[Or]. ω = ω1+ω2 follows by [And]. | Explicitly excludes independence ("reasoning involving independence of random variables … is not supported"). No two-rate type, no inference, no tightness, nothing on one-sided error. | **Partial, near-direct on the dependence-free rules.** Present those rules as *derived aHL rules*. The new parts relative to aHL are the certified-independence tightening, the tightness/optimality theorems, and the comparison with Decaf. (Derivation sketch is my analysis; aHL never states these rules.) |
| **Choudhury & Mohanram, "Accurate and scalable reliability analysis of logic circuits", DATE 2007, doi:10.1109/date.2007.364503; journal version "Reliability analysis of logic circuits", IEEE TCAD 28(3) 2009, doi:10.1109/TCAD.2009.2012530** | Single-pass analysis propagating, per gate, "a 0 → 1 error probability given that its error-free value is 0 … and a 1 → 0 error probability given that its error-free value is 1". The AND 1→0 term on input 11 is 1−(1−ω1)(1−ω2). Exact "in the absence of reconvergent fanout". | Averages over input vectors with signal-probability weights (a prior), so it is not a worst case over latent truth. Independent gate failures; point estimates rather than certified bounds; no arbitrary-dependence mode; no type system. | **Partial.** Directional, truth-conditional propagation and the independent ω formula are prior art, as is read-once exactness for the averaged quantity. |
| **Shivakumar, Garcia-Molina, Chekuri, "Filtering with approximate predicates", VLDB 1998, pp. 263–274** (no DOI; vldb.org PDF; full text read by me) | Defines n = P(¬A \| I) and p = P(A \| ¬I) for an approximate predicate A of an ideal predicate I. Composes filters of the *same* ideal predicate with NOT, SEQ, AND and OR (their Table 2) under "local independence" or "local conditional independence". | For different ideal predicates (joins) the FP rate is *recomputed from selectivities*, i.e. averaged over a prior (§6). No arbitrary-dependence rules, no worst case over truth, no XOR/if, no soundness theorem. | **Partial.** Our "same-meaning" product rules (AND ε = ε1ε2, OR ω = ω1ω2 for estimates of one fact) are their Table 2 entries under LCI. |
| **Berger, "Multiparameter hypothesis testing and acceptance sampling", Technometrics 24(4) 1982, doi:10.1080/00401706.1982.10487790** (intersection-union test) | Reject a union null only when every component test rejects. Level = max of the component levels, with no dependence assumption and a supremum over the null space. This is the AND-ε rule at one level. The dual union-intersection test with Bonferroni gives OR ε = Σ. | Single level of combination; no ω side (power is not uniformly bounded in testing); no NOT, XOR or if; no recursion. | **Partial; must cite.** Alex's own R package `hypothesize` (rlang/hypothesize, boolean-algebra vignette) already implements this p-value algebra. |
| **Ferson, Nelsen, Hajagos, Berleant, Zhang, Tucker, Ginzburg, Oberkampf, "Dependence in probabilistic modeling, Dempster–Shafer theory, and probability bounds analysis", SAND2004-3072, 2004, doi:10.2172/919189** | Fréchet calculus for fault trees (AND, OR, NOT, XOR). §2.5: pairwise composition "will produce the best possible bounds when there are no repeated parameters". §2.6: optimal bounds for arbitrary functions are NP-hard. | Unconditional event probabilities, not error rates conditional on latent truth; the read-once claim is asserted without proof. | **Partial.** Read-once best-possibility and NP-hardness are stated in the unconditional setting. Our read-once theorem is the latent-indexed analogue and must be framed that way. |
| **Boston, Sampson, Grossman, Ceze, "Probability type inference for flexible approximate programming" (Decaf), OOPSLA 2015, doi:10.1145/2814270.2814301** | `@Approx(p) τ`: correct in at least a fraction p of executions. Operator rule p′ = p1·p2·p_op. The paper states explicitly: "We also assume that these failure events are statistically independent". | One symmetric probability; errors are a single "garbage" value; approximate conditions are not allowed ("only fully reliable types … may appear in conditions"), so `endorse` is needed. Its claim "Pr[y \| x] is at least Pr[y]" fails under negative correlation. | Adjacent. This is the baseline being refined. |

### Other priors checked (adjacent, cite as appropriate)

- **Approximate-computing type systems and logics.**
  - Rely (OOPSLA 2013, doi:10.1145/2509136.2509546) and Chisel (OOPSLA 2014, doi:10.1145/2660193.2660231) use symmetric reliability, i.e. a joint correctness probability.
  - EnerJ (PLDI 2011, doi:10.1145/1993498.1993518) has no probabilities and prohibits approximate conditions.
  - Uncertain⟨T⟩ (ASPLOS 2014, doi:10.1145/2541940.2541958) and probabilistic assertions (PLDI 2014, doi:10.1145/2594291.2594294) report FP/FN of a *statistical test's verdict*, not error rates of values relative to latent truth.
  - Probabilistic Boolean Logic (Chakrapani & Palem, ASP-DAC 2010, doi:10.1109/aspdac.2010.5419810) attaches one symmetric correctness probability to each operator.
- **Error-bound program logics.**
  - Eris (ICFP 2024, doi:10.1145/3674635) and Coneris (ICFP 2025, doi:10.1145/3747514) use error credits. Coneris gives a truth-conditional single-query Bloom FP spec, but nothing about Boolean combination. By my analysis, Eris's expectation-preserving split could derive the independent ω product for fresh samples.
  - HO-UBL (ICFP 2021, doi:10.1145/3473598) is another union-bound logic.
  - Kura–Unno refinement types (ICFP 2024, doi:10.1145/3674662) cover weakest pre-expectations.
  - All of these track one failure index, with no truth indexing.
- **Independence certification.** PSL (POPL 2020, doi:10.1145/3371123), Lilac (PLDI 2023, doi:10.1145/3591226), DIBI (LICS 2021, doi:10.1109/LICS52264.2021.9470712) and Bluebell (POPL 2025, doi:10.1145/3704894) certify independence by disjoint randomness. Our provenance-disjointness side condition is the type-level shadow of this; cite it, do not claim it.
- **Imprecise probabilistic programming.** Liell-Cock & Staton, ICFP 2026, doi:10.1145/3828698, use credal sets with named Knightian choices and BDD/WMC inference. This is whole-program inference, not closed-form rules, and has no FP/FN indexing.
- **Probabilistic abstract interpretation.** Monniaux (SAS 2000, doi:10.1007/978-3-540-45099-3_17) and Cousot & Monerau (ESOP 2012, doi:10.1007/978-3-642-28869-2_9) give upper probabilities under nondeterminism. Our semantics is an instance; no per-truth-value error domain was found.
- **Verified approximate-membership structures.** Ceramist (CAV 2020, doi:10.1007/978-3-030-53291-8_16) proves per-structure no-false-negative and FP bounds. Its "compositional" refers to implementation structure, not to Boolean combinations of answers.
- **Circuit and noisy-computation reliability.**
  - Probabilistic transfer matrices (TODAES 2008, doi:10.1145/1297666.1297674) are exact and per-input, with the reported metric averaged.
  - Signal-probability reliability (Microelectron. Reliab. 2008, doi:10.1016/j.microrel.2008.07.002) is averaged and assumes independence.
  - The Alekhina line (Discrete Math. Appl. 2001, doi:10.1515/dma.2001.11.5.493) considers worst case over inputs with one-type faults, but a single scalar and independent faults.
  - von Neumann, Pippenger, Evans–Schulman, and Feige–Raghavan–Peleg–Upfal (SIAM J. Comput. 1994, doi:10.1137/S0097539791195877) assume symmetric independent noise.
- **Probability logic.**
  - Hailperin, Amer. Math. Monthly 72 (1965), doi:10.1080/00029890.1965.11970533, gives best-possible LP bounds, unconditional.
  - Fréchet 1935 (doi:10.4064/fm-25-1-379-387) supplies the per-node bounds.
  - Nilsson 1986 (doi:10.1016/0004-3702(86)90031-7) is unconditional probabilistic entailment.
  - Georgakopoulos–Kavvadias–Papadimitriou 1988 (doi:10.1016/0885-064X(88)90006-4) shows probabilistic satisfiability is NP-complete, an analogue for our hardness remark.
  - Credal networks (Cozman 2000, doi:10.1016/S0004-3702(00)00029-1) could express the quantity, but give no closed-form rules.
- **Databases and ML.**
  - Lu, Chowdhery, Kandula, Chaudhuri, probabilistic predicates, SIGMOD 2018, doi:10.1145/3183713.3183751: one-sided predicates, with AND/OR preserving one-sidedness under independence; accuracy is an averaged output fraction.
  - Learned Bloom filters and sandwiching (Kraska et al. SIGMOD 2018, doi:10.1145/3183713.3196909; Mitzenmacher NeurIPS 2018) derive composite rates by hand, and the rates are tied to the query distribution.
  - Gatterbauer–Suciu dissociation bounds (TODS 2014, doi:10.1145/2532641) treat repeated variables as the source of looseness.
- **Diagnostic testing.** Vacek 1985 (doi:10.2307/2530967), Gardner et al. 2000 (doi:10.1016/s0167-5877(00)00119-7) and Marshall 1989 (doi:10.2307/2531772) cover serial/parallel combination of tests for the *same* condition, under independence or modelled covariance. No Boolean combination of tests for different conditions with a worst case over truth was found.
- **Complexity folklore.** RP is closed under ∪ and ∩ (Arora–Barak 2009; textbook location UNVERIFIED). This is the complexity analogue of our polarity theorem.

### Alex's own prior material (self-overlap, not external prior art)

- **Algebraic-types manuscript.** `papers/bernoulli_data_type/algebraic_types/sections/error_propagation.tex` (remark "Interval arithmetic for composed outputs") already states ε_out ∈ [ε1ε2, max{(1−ω1)ε2, ε1(1−ω2)}] for the independent AND with exact rates. It asserts the approach "is composable", without proof.
- **The book.** `book/chapters/ch03/and-under-noise.tex` mentions the max(ε1, ε2) extreme. `ch03/or-not.tex` Prop. "Closure under Boolean operations" propagates prior-dependent rates, which is the non-compositional reading this work corrects.
- **The package.** `bernoulli-py/src/bernoulli/atom.py` `BernoulliBool.__and__` multiplies FPRs (shared-truth semantics). Used on operands with different truths, it under-reports; a regression test demonstrates this.
- **Internal research notes.** `.research/dependence-calculus/` (2026-10-13) has truth-uniform one-sided contracts for monotone query lineage (certificate/sensitivity formulas). These are the same worst-case-over-truth idea, applied to database lineage rather than as typing rules.
- **Program strategy.** `.research/program-strategy/README.md` idea C is this research line.

## What survives, stated so a reviewer cannot say "this is X"

1. **Latent-indexed two-rate types with dependence-free defaults and provenance-certified independence tightening, for AND/OR/NOT/XOR/if/case/let/pairs.** aHL can derive the dependence-free half. The packaging, inference and tightening are new as far as this search found.
2. **Best-transformer theorem.** Each rule is the least sound output pair for its connective, given only the operand types and the dependence information. Unconditional Fréchet best-possibility is classical; the latent-indexed version, including if/XOR and both dependence regimes, was not found.
3. **Read-once exactness.** Single-use expressions get exactly the true worst case. Ferson et al. assert the unconditional analogue, and Choudhury–Mohanram state the averaged one. Present this as the latent-indexed analogue of a known principle, with a proof.
4. **Strict refinement of single-probability typing, and one-sided amplification.** The collapse max(ε, ω) is never worse than the Decaf-style δ and is strictly better on one-sided operands. Amplification by repetition is derivable only with two rates. Not found as a theorem.
5. **Polarity theorem.** A static "no false negatives" guarantee comes from a polarity condition, and it is complete on read-once programs. This is an analogue of RP closure. It is elementary.

## Search limitations

- **Full texts not read:**
  - Hailperin 1965; Cozman 2000; Williamson–Downs 1990.
  - The TCAD 2009 journal version (the DATE 2007 version was read).
  - Gardner 2000; the QIF book; pRHL, apRHL and EpRHL; Lilac and Bluebell bodies; Monniaux's body.
  - The Russian reliability-theory literature (abstracts only).
- **Not searched in depth:** multiple-testing closed-testing and gatekeeping procedures, which compose intersection-union and union-intersection tests hierarchically and are the most likely remaining place for an ε-side collision (they have no ω side).
- **Tool limits:** Semantic Scholar rate-limited the searches; Google Scholar and ACM full-text search were unavailable. A workshop paper or thesis chapter could have been missed.
- **ACM Open status of SIUE: UNVERIFIED.** The participants page returned HTTP 403.
