# Two-Rate Types: Worst-Case False-Positive and False-Negative Bounds for Approximate Boolean Programs

*Draft paper outline, about 8 pages, ready to convert to LaTeX. Author: Alexander Towell. Status: internal draft; not submitted.*

**Evidence labels used throughout**

| Label | Meaning |
|---|---|
| **[P]** | Proved on paper here |
| **[L]** | Machine-checked in Lean 4 (`lean/TwoRate.lean`; core only, no `sorry`; axioms `propext` and `Quot.sound`) |
| **[E]** | Exactly checked on finite instances in rational arithmetic (`test_tworate.py`). This is evidence for the finite claim, not a proof of the general one |
| **[K]** | Known; cited |
| **[C]** | Conjecture or open problem |

---

## Abstract

Approximate data structures and randomized tests answer Boolean questions with *asymmetric* errors. A Bloom filter never misses a member but sometimes accepts a non-member. A Miller–Rabin round never rejects a prime. Programs combine such answers with AND, OR, NOT and conditionals. Type systems for approximate computing track one symmetric "correct with probability ≥ p" per value (Decaf, Rely), so they cannot state "no false negatives", and they lose a factor of about 2 on simple conjunctions.

Tracking two rates looks easy but has a trap. A pair of false-positive and false-negative rates averaged over a prior, or read off the all-negative corner, does not compose; the corner rule is even unsound. We give a type system whose judgment e : Bool[ε, ω] bounds the false-positive rate ε and the false-negative rate ω *for every latent truth assignment*. Under that reading the pair composes.

- The rules are sound under arbitrary dependence and tightened only where disjoint random provenance certifies independence.
- Each rule is the best abstract transformer for its connective.
- The rules are exact on read-once programs.
- The analysis strictly refines single-probability typing.
- "No false negatives" becomes a static polarity property.

We mechanize soundness of the dependence-free fragment in Lean, and validate exactness and soundness against an exact oracle over all admissible joint error laws.

## 1. Introduction

**The setting.** Many programs consult structures whose Boolean answers err in a known, one-sided way:

- Bloom, cuckoo and xor filters: false positives only;
- retrieval maps with b-bit fingerprints: rate 2⁻ᵇ on non-keys;
- Miller–Rabin: composites pass a round with probability at most 1/4; primes always pass;
- learned and approximate predicates.

Programs then compute with the answers:

- an LSM-tree read path is `bloom(x) && disk(x)`;
- a sharded set is `bloom(S1,x) || … || bloom(Sk,x)`;
- a blocklist gate is `!bloom(Block,x) && auth(x)`.

**The gap.** Single-probability type systems annotate each value with p, the probability that it is correct, and compose p multiplicatively (Decaf, OOPSLA 2015: p′ = p₁·p₂·p_op, assuming independent failures). Three consequences follow:

1. They cannot express one-sidedness.
2. They charge an AND of two Bloom answers about 2ε, although its false-positive rate is at most ε.
3. Repetition looks like degradation, so they cannot derive amplification: 10 Miller–Rabin rounds get δ = 1 − 0.75¹⁰ ≈ 0.944 instead of 4⁻¹⁰.

**The trap.** The obvious fix tracks (FPR, FNR) per value. Textbook formulas for AND (FPR ε₁ε₂, FNR 1 − (1−ω₁)(1−ω₂)) hold only when both operands are truly negative (the "all-negative corner"), or are averages over a prior. Neither composes (§2).

**Contributions**

1. A latent-indexed semantics for two-rate Boolean types (§3). Under it, composition is pointwise in the latent valuation, hence compositional.
2. Typing rules for AND/OR/NOT/XOR/if/case/let/pairs (§4).
   - They are sound under arbitrary dependence (the Fréchet/union side).
   - Product tightenings apply only under certified independence (disjoint random provenance).
   - An equal-meaning refinement yields amplification.
   - Soundness: Theorem 1 [P][L][E].
3. Optimality (§5):
   - every rule is the best transformer (Theorem 2 [P][E]);
   - the rules are exact on read-once programs (Theorem 3 [P][E]);
   - exactness fails with sharing, and deciding whether the exact worst-case rate is 0 is coNP-complete (Proposition 4 [P][E]).
4. One-sidedness as a static guarantee (Theorem 5, polarity [P][E]).
5. Strict refinement of single-probability typing, and an amplification separation (Theorem 6, Proposition 7 [P][E]), with case studies (§8).

**What is not new (stated up front).** Each per-connective inequality is a Fréchet/Boole bound or a product formula [K]:

- The dependence-free rules are derivable in the union-bound logic aHL (Barthe et al., ICALP 2016) by its case rule.
- Directional, truth-conditional error propagation through gates exists in average-case circuit reliability (Choudhury–Mohanram 2007/2009).
- Same-predicate filter composition under conditional independence is in Shivakumar–Garcia-Molina–Chekuri (VLDB 1998).
- The AND-ε rule at a single level is Berger's intersection-union test (1982).

Our contribution is the latent-indexed packaging as a type discipline, the dependence/independence split via provenance, and the optimality, exactness, polarity and refinement theorems.

## 2. The pitfall, precisely

Take three independent leaves b₀, b₁, b₂, each with FPR 0.02 and FNR 0.10, and the program (b₀ ∧ b₁) ∨ b₂. Consider the latent word 010, i.e. x₀=0, x₁=1, x₂=0. The exact value is 0.

- **Exact error at 010** (rates exactly 0.02/0.10): P((b₀∧b₁) ∨ b₂) = 0.018 + 0.02 − 0.018·0.02 = **0.03764**.
- **Naive corner summary** (ε∧ = ε₀ε₁ = 0.0004, then OR): **0.020392**. This under-reports by a factor of 1.85, so it is **unsound**.
- **Rule of this paper** (ε∧ = max(ε₀, ε₁) = 0.02, then independent OR): **0.0396**. This is sound, and it is attained when b₁'s actual FNR is 0. That is admissible because declared rates are upper bounds. [E]
- **If rates are known exactly**, the worst case over latent words is 0.03764. An interval-rate refinement (Remark 4.3) recovers it. [E]

The naive summary is wrong because the error of a composite at a valuation depends on its operands' errors *at that valuation*. The AND's worst false positive occurs at the *mixed* valuation (0,1), not at (0,0). There, the truly positive operand reports 1, and only one operand needs to err.

A prior-averaged summary avoids the corner error only by carrying the prevalence of each subterm and assuming a product prior over latent facts. This is the signal-probability scheme of circuit reliability analysis, and it fails under latent correlation (reconvergent fanout). The latent supremum needs no prior and tolerates arbitrary latent correlation.

## 3. Calculus

### 3.1 Syntax

$$e ::= q \mid c \mid x \mid \neg e \mid e \wedge e \mid e \vee e \mid e \oplus e \mid \mathsf{if}\ e\ \mathsf{then}\ e\ \mathsf{else}\ e \mid \mathsf{let}\ x = e\ \mathsf{in}\ e \mid (e,e) \mid \mathsf{fst}\ e \mid \mathsf{snd}\ e \mid \mathsf{tag}(e; e, e) \mid \mathsf{case}\ e\ \mathsf{of}\ \mathsf{inl}\,x \Rightarrow e \mid \mathsf{inr}\,y \Rightarrow e$$

**Primitives.** A primitive q = ⟨a_q, s_q, ε_q, ω_q⟩ is one frozen random bit:

- **atom** a_q: its exact meaning, the latent fact it estimates, e.g. `x ∈ S`;
- **source** s_q: the random seed it draws on;
- **rates** (ε_q, ω_q): its declared rates.

Re-reading the same primitive yields the same bit. `tag(c; l, r)` is `inl l` when c reads 1 and `inr r` otherwise. Both payload slots are always present, so `case` is a total multiplexer.

### 3.2 Semantics

**Valuations and observations.**

- A **latent valuation** is v : Atoms → 2.
- The **exact semantics** ⟦e⟧*(v) evaluates every primitive at v(a_q).
- An **observation** is o ∈ 2^Prims. The **observed semantics** ⟦e⟧(o) evaluates q at o_q.
- The **error indicator** of q is I_q = o_q ⊕ v(a_q).

**Definition 1 (admissible error model).** A family (M_v)_v of laws on 2^Prims is admissible when, for every v:

- **(A1) marginals:** M_v(I_q = 1) ≤ b_q(v), where b_q(v) = ε_q if v(a_q) = 0 and ω_q otherwise;
- **(A2) independence:** M_v = ⊗_s M_v^s, a product across sources, with arbitrary dependence within a source.

**Definition 2 (semantic judgment).** ⊨ e : Bool[ε, ω] iff for every admissible M and every v:

- ⟦e⟧*(v) = 0 implies M_v(⟦e⟧ = 1) ≤ ε;
- ⟦e⟧*(v) = 1 implies M_v(⟦e⟧ = 0) ≤ ω.

The least such pair is the **tight pair** (ε*(e), ω*(e)).

Both quantifiers are supremums. The supremum over v is taken *without* a prior over truths; that is the point. The supremum over M covers adversarial dependence within a source.

**Scope assumption (non-adaptivity).** Queries are determined by v (the program's exact inputs). No query key is computed from an observed answer of the same source. Approximate keys are handled by a coercion rule (Remark 4.2).

### 3.3 Types

τ ::= Bool[ε, ω] | τ × τ | τ +_{Bool[ε,ω]} τ. Here the tag of a sum carries its own two-rate type, with the convention that tag 1 is inl.

A Boolean judgment carries:

- **provenance** R ⊆ Sources: the sources its observed value can depend on (∅ for exact primitives and constants);
- **erasure** ⌊e⌋: its exact meaning, a Boolean term over atoms, normalized by double negation, negation of constants, and idempotence: AND/OR of equal erasures keeps the erasure, XOR of equal erasures becomes the constant 0, and an if with equal branch erasures takes the branch erasure.

Variables carry the type, provenance and erasure of their binding. Pairs and projections are componentwise. A sum's payload types hold at valuations where the exact tag selects that slot. This is the latent-indexed reading of "the payload is meaningful only when the tag is right."

## 4. Typing rules

**Combinators.** Let ρ ∈ {D, I} be the dependence regime: I iff the operands' provenances are disjoint. The rules use:

| Name | D (arbitrary dependence) | I (certified independence) |
|---|---|---|
| union u | min(1, a+b) | a + b − ab |
| meet m | min(a, b) | ab |
| xor x | min(1, a+b) | max(a, b, a+b−2ab) |

All are nondecreasing in each argument on [0,1].

**Figure 1 (Boolean rules).** In every binary rule the operands are e₁ : Bool[ε₁, ω₁] ! R₁ and e₂ : Bool[ε₂, ω₂] ! R₂. Output provenance is the union of the operands' provenance.

| Rule | ε | ω | Side condition |
|---|---|---|---|
| PRIM | ε_q | ω_q | R = {s_q}, or ∅ if q is exact |
| NOT | ω | ε | |
| AND | max(ε₁, ε₂) | u_ρ(ω₁, ω₂) | |
| AND≡ | m_ρ(ε₁, ε₂) | u_ρ(ω₁, ω₂) | ⌊e₁⌋ = ⌊e₂⌋ |
| OR | u_ρ(ε₁, ε₂) | max(ω₁, ω₂) | |
| OR≡ | u_ρ(ε₁, ε₂) | m_ρ(ω₁, ω₂) | ⌊e₁⌋ = ⌊e₂⌋ |
| XOR | max(x_ρ(ε₁,ε₂), x_ρ(ω₁,ω₂)) | max(x_ρ(ε₁,ω₂), x_ρ(ω₁,ε₂)) | |
| XOR≡ | as XOR | 0 (vacuous) | ⌊e₁⌋ = ⌊e₂⌋ |
| IF c e₁ e₂ | max(u_{ρ₁}(ε₁, ω_c), u_{ρ₂}(ε₂, ε_c)) | max(u_{ρ₁}(ω₁, ω_c), u_{ρ₂}(ω₂, ε_c)) | ρ_k = I iff R_c ∩ R_k = ∅ |
| IF≡ c e₁ e₂ | min(IF, max(g(ε₁, ε₂, ω_c), g(ε₂, ε₁, ε_c))) | same with ω₁, ω₂ | ⌊e₁⌋ = ⌊e₂⌋; g(r, r′, f) = r + f·(r′ − r)⁺ if c is independent of both branches, else min(1, r + min(f, r′)) |
| CASE | IF (or IF≡), with the tag's type as c | | payload variables typed by the slot types |

LET, PAIR, FST, SND and TAG are structural.

**Reading the rules.**

- **AND's false-positive rate is a maximum, not a product.** If some operand is truly 0, the conjunction fires only if that operand falsely fires. Independence never helps this side across different facts; it helps only the ω side, or ε when meanings coincide (AND≡).
- **XOR's false-positive rate is driven by the operands' false-negative rates** at the latent pair (1,1).
- **IF's condition matters only through its flips into a disagreeing branch.** IF needs independence of c from the branch it is paired with, not between the branches.

**Remark 4.1 (encoding if loses precision).** Encoding if as (c ∧ e₁) ∨ (¬c ∧ e₂) is sound but strictly looser, because c is shared. Example: ε_c = ω_c = 0.01 and independent branches at 0.1 give 0.109 by IF versus 0.2 via the encoding [E]. IF is therefore primitive.

**Remark 4.2 (approximate arguments).** If a primitive predicate with spec (ε, ω) on exact arguments receives an argument whose value is wrong with probability at most δ, the result is typed Bool[ε+δ, ω+δ] under arbitrary dependence. The error event is contained in {argument wrong} ∪ {query at the exact argument wrong}. [P; not implemented]

**Remark 4.3 (exact-rate refinement).** Track intervals [lo, hi] for each rate and take node-wise min/max over the rate box. At the independent AND this gives ε∧ ∈ [ε₁ˡᵒε₂ˡᵒ, max(ε₁ε₂, ε₁(1−ω₂ˡᵒ), ε₂(1−ω₁ˡᵒ))]. The bernoulli_data_type manuscript states the interval without the ε₁ε₂ term, which is correct only when ε_k + ω_k ≤ 1 for both operands: with all rates 0.9 the true worst case is 0.81, against 0.09. With that term, the refinement recovers 0.03764 in §2. [P for that example, computed by hand and cross-checked by the oracle's exact-rate mode; general rules C]

## 5. Soundness

**Lemma 1 (pointwise connective lemma) [P][L: default D rules without caps; AND/OR product case in regime I].** Fix v. Let B₁, B₂ (and B_c) be observed bits on one probability space, with exact values t_k and error probabilities r_k ≤ b_k(t_k). Then, for each connective, P(op(B) ≠ op(t)) is at most the corresponding Figure 1 entry for the class op(t). This holds always for ρ = D, and when the relevant error indicators are independent for ρ = I.

*Proof.* At fixed t, op(t ⊕ I) depends only on t and the error indicators I. So the error is the probability of a fixed event E_op(t) in the indicators:

| Connective | Exact values t | Error event | Bound (D) |
|---|---|---|---|
| AND | (0, ·) | {I₁ = 1, B₂ = 1} ⊆ {I₁ = 1} | r₁ ≤ ε₁ |
| AND | (1, 1) | I₁ ∪ I₂ | union |
| AND≡ | (0, 0) | I₁ ∩ I₂ | Fréchet upper bound min(r₁, r₂) |
| XOR | (t, t) | I₁ ⊕ I₂ ⊆ I₁ ∪ I₂ | union |
| IF | t_c = 1, t₁ = 0 | (¬I_c ∩ I₁) ∪ (I_c ∩ ·) ⊆ I₁ ∪ I_c | union |

Under independence:

- the AND/OR unions become 1 − (1−r₁)(1−r₂);
- the XOR error is r₁ + r₂ − 2r₁r₂, bilinear, so its supremum over the rate box is at a corner, giving x_I;
- the IF error is at most (1−r_c)r₁ + r_c = u_I(r₁, r_c). The other branch's term is bounded by P(I_c) with no assumption, which is why only c ⊥ e₁ is needed.

Monotonicity of the combinators replaces r_k by the declared bounds. ∎

**Lemma 2 (provenance certifies independence) [P].** The observed value of e is a function of the observations of primitives whose sources lie in R(e) (exact primitives are almost surely constant). By (A2), disjoint provenance implies that the observed values, and hence the error indicators, are independent under every M_v.

**Theorem 1 (soundness) [P][L: the default (non-≡) dependence-free rules without the min(1, ·) cap, over the Boolean core with sharing and constants][E].** If ⊢ e : Bool[ε, ω] ! R then ⊨ e : Bool[ε, ω].

*Proof.* Induct on the derivation. For `let`, the observed value of e₂[e₁/x] equals that of the let, because primitives are frozen bits, so typing x by e₁'s judgment is sound. Products and projections are structural. A case over a tag is the multiplexer of Lemma 1 at the tag's bit; payload judgments are used only at valuations where the exact tag selects that slot, which is exactly where they hold.

At every connective, fix v and apply Lemma 1 with r_k bounded by the induction hypothesis *at the same v*. Use Lemma 2 for ρ = I. Because the quantifier over v is outermost and every step is pointwise in v, the supremum composes. ∎

**Mechanization.** `lean/TwoRate.lean` defines laws as finite weighted outcome lists with natural-number weights (any common denominator), arbitrary joint dependence, and expressions with shared primitive indices and constants. It proves `sound`: for every latent valuation and every law, every expression meets `ty`. `lean/TwoRateIndep.lean` adds the pointwise independence lemma for the AND false-negative rule (and, by duality, the OR false-positive rule) over product laws: err + ab ≤ aT₂ + bT₁, i.e. err/(T₁T₂) ≤ 1 − (1−α)(1−β). The other independent-regime rules, and their integration with provenance into the inductive theorem, are proved on paper and exhaustively checked [E], not mechanized.

## 6. Optimality

**Theorem 2 (each rule is the best transformer) [P][E].** For each connective, regime ρ and feasibility class (default, or equal meaning), and for all operand types, the Figure 1 output is the least pair that is sound for every operand semantics with those types (in the uniform regimes D and I; mixed regimes are only checked for soundness). In particular, fresh primitives with exactly the operand types attain it: distinct atoms (equal atoms for ≡), one shared source for D, distinct sources for I.

*Witnesses.*

| Rule | Witness | Value attained |
|---|---|---|
| AND ε | valuation (0,1); operand 1 errs at rate ε₁; operand 2 exact | ε₁ |
| AND ω, D | valuation (1,1); disjoint error events | min(1, ω₁+ω₂) |
| AND ω, I | full rates, independent | the product formula |
| AND≡ ε, D | nested error events | min |
| XOR ε, D | disjoint errors at (0,0) or (1,1) | min(1, ε₁+ε₂) or min(1, ω₁+ω₂) |
| XOR ε, I | a corner of the rate box | x_I |
| IF ε, D | t_c=1, t₁=0, t₂=1, else-branch exact, the condition flip disjoint from the then-branch error | min(1, ε₁+ω_c) |
| IF ε, I | independent | ε₁ + ω_c − ε₁ω_c |

The supremum computation is the Fréchet LP (D) or the bilinear corner enumeration (I) over the operand error indicators. The test `test_each_rule_is_best_transformer` checks equality against the exact oracle for each of the five connectives in each regime (60 random rate vectors per cell from the grid {0, 1/100, …, 1/2, 3/5, 9/10, 1}; 600 instances). `test_same_meaning_rules_are_best_transformers` checks AND≡/OR≡/XOR≡ (150 instances), and `test_if_equal_rule_is_best_transformer` checks IF≡ in both regimes (200 instances). Caps at 1 are exercised. An independent review additionally checked exhaustive grids: 28,812 binary instances (AND/OR/XOR × D/I × default/≡ × 7⁴ rates) and 31,250 IF instances, all exact.

**Theorem 3 (read-once exactness) [P][E].** Let e be constant-free and read-once: distinct atoms, each primitive used once. If all primitives share one source (D), or all have distinct sources (I), the rules derive exactly (ε*(e), ω*(e)).

*Proof sketch.* Induct with three invariants:

- **(a) feasibility:** both exact values occur at some valuation. Children have disjoint atoms, so every tuple of children's exact values is feasible.
- **(b) rate filling:** at a valuation where a child attains its bound b(τ), the child can realize every error probability in [0, b(τ)]. In D, mix with the exact law. In I, scale every primitive rate by λ and apply continuity; only the corners {0, b} are needed in I anyway, since node errors are multilinear.
- **(c) gluing:** in D, any coupling π of children's error indicators is realizable. Draw (i₁, i₂) ~ π, then each child's observations from its witness law conditioned on I_k = i_k; marginals are preserved and a single source admits any joint law. In I, the product is forced and realized by distinct sources.

The node's error depends only on the exact values and the joint law of the children's indicators, so its supremum equals the best transformer of Theorem 2. ∎

*Checks.* Rules equal the exact oracle on 150 random read-once programs with 2–5 leaves in regime I, 150 with 2–3 leaves and 60 with 2–4 leaves in regime D, and 4 fixed 4-leaf D shapes. An independent review added 150 programs with 4–6 leaves in each regime. Both maximizing witnesses are re-verified (total mass, marginal admissibility, product structure across sources, error value). The witness checker shares the core evaluator with the oracle; desugaring plus core evaluation is cross-checked against an independent big-step evaluator on 300 random structured programs, and the reviewer's independent oracle agreed on 2,400 programs.

This is the latent-indexed analogue of Moore's single-use-expression theorem for interval arithmetic [K]. Ferson et al. (2004, §2.5) assert the unconditional Fréchet version [K]; Choudhury–Mohanram state the averaged circuit version [K]. A corollary is an exact worst-case analysis for read-once programs in linear time (with hash-consed erasures; naive erasure comparison is quadratic in the worst case).

**Proposition 4 (sharing; hardness).**

- **(a) Sharing costs exactness [E].**
  - b ∧ b: rule (ε, 2ω), exact (ε, ω).
  - b ∧ ¬b: rule (max(ε, ω), min(1, ε+ω)), exact (0, 0).
  - if versus its encoding: Remark 4.1.
  - Partially shared sources in a read-once program, (a ∧ b) ∧ c with a and c in source s₁ and b in source s₂, all ω = 0.2: rule ω = 0.56, exact 0.52. The top node sees overlapping provenance, but b cannot be anti-correlated with c.
- **(b) Deciding ε* = 0 is coNP-complete [P].** Let every declared rate lie in (0, 1). Then ε*(e) = 0 iff the exact function is constantly 1 or the observed function is constantly 0, because every observation vector has positive probability under the product law. Hence deciding ε*(e) = 0 is coNP-complete: UNSAT(φ) reduces to ε*(φ ∧ z) = 0 with z fresh, and membership is witnessed by (v, o). Computing ε* exactly with sharing is therefore NP-hard (the threshold problem ε* ≤ θ is shown hard, not shown to be in coNP; fixed-law evaluation is already #P-hard), while the rules run in linear time. For comparison [K]: NP-hardness of optimal bounds (Ferson §2.6), probabilistic satisfiability (Georgakopoulos–Kavvadias–Papadimitriou 1988), and #P-hardness of fixed-valuation probabilities (Valiant 1979).
- **[C] Open: a source-indexed refinement.** Track, per source, the error mass charged to it; combine with union within a source and product across sources. We conjecture such a refinement is exact for read-once programs under arbitrary source structure. In the 0.52 example it gives the exact value.

## 7. One-sidedness as a static guarantee

**Theorem 5 (polarity) [P][E].** With the ≡ rules disabled, for a constant-free expression, the derived ω(e) = 0 iff:

- every primitive occurrence under an even number of negations has ω_q = 0;
- every one under an odd number has ε_q = 0;
- every primitive under an XOR or inside an if/case condition is exact.

If-branches inherit the polarity of the if. The dual statement holds for ε(e) = 0. On read-once programs (either uniform regime) the condition is also necessary for ω*(e) = 0. Completeness follows from Theorem 3. (300 random read-once programs with many zero rates, in both regimes.) Constant-freeness is needed for necessity: And(false, a) with ω_a > 0 has ω* = 0 but derived ω > 0.

The ≡ rules relax the condition soundly (AND≡ gives ε = min(ε₁, ε₂)).

**Reading.** "No false negatives" is preserved by AND/OR and by monotone contexts. NOT turns it into "no false positives". XOR and approximate conditions destroy it. This is the type-level analogue of RP being closed under union and intersection but not, as far as is known, under complement [K, folklore].

The brief's claim that "XOR loses asymmetry" is refined, not confirmed. The tight XOR pair stays class-specific: leaves (0.01, 0.1) give (0.18, 0.108), against the symmetric collapse ½(1 − ∏(1 − 2q_i)) = 0.18 for both. What XOR destroys is one-sidedness: one-sided leaves (0.01, 0) give ω = 0.01 [E].

## 8. Relation to single-probability typing

Define the like-for-like single-probability system S:

- δ(q) = max(ε_q, ω_q);
- δ(e₁ op e₂) = u_ρ(δ₁, δ₂);
- δ(¬e) = δ(e);
- δ(if) = max(u_{ρ₁}(δ_c, δ₁), u_{ρ₂}(δ_c, δ₂)).

Decaf's rule is u_I applied unconditionally; Decaf additionally forbids approximate conditions.

**Theorem 6 (refinement) [P][E].** For every e, max(ε(e), ω(e)) ≤ δ(e) under the same provenance regimes.

*Proof.* Induct. Every Figure 1 output is a max of combinators applied to operand rates each bounded by the corresponding δ, and max ≤ u, m ≤ u, x_I ≤ u_I and x_D = u_D pointwise. ∎ (400 random programs.)

The inequality is strict when the ε side of an AND dominates (dually the ω side of an OR) and no cap absorbs the difference, e.g. two one-sided operands: ε versus 2ε − ε². It is an equality when the maximum is attained on the side where both systems use the same union (e.g. symmetric noise, or a = b = (0.1, 0.5): two-rate (0.1, 0.75), δ = 0.75).

**Proposition 7 (amplification needs two rates) [P][E].** Consider tests of one fact with symmetric error δ. No sound *single-probability* rule for a binary AND or OR can type the result below δ: the exact worst case of AND≡ under independence is the pair (δ², 2δ − δ²), whose maximum 2δ − δ² ≥ δ (a two-rate type keeps ε = δ² < δ). In two-rate types, one-sided tests amplify:

- k Miller–Rabin rounds with independent witnesses on the same n are typed (4⁻ᵏ, 0), tight [E for k ≤ 4];
- the single-probability product gives 1 − (3/4)ᵏ, which grows with k.

Amplifying symmetric error requires majority voting (BPP-style) or a hand annotation.

**On Decaf's soundness model.** Decaf's product rule is justified by its model of independent operator faults; its paper says so explicitly. Approximate data structures share seeds: two answers from one filter can have negatively correlated, even disjoint, error events. There the product is unsound. Two answers with ω = 0.2 each give an exact worst-case ω = 0.4, against the product's 0.36 [E: `test_forced_independence_is_unsound_for_shared_source`]. Provenance tracking is what licenses the product.

## 9. Case studies

All values come from `casestudies.py` (also in `casestudies.json`).

- **"exact"** is the oracle's worst case over all latent valuations and admissible joint laws, where enumeration is feasible.
- **"Decaf derived"** applies the product rule with leaf annotations p = 1 − max(ε, ω).
- **"Decaf annotated"** uses a hand-written annotation of the subcomputation as a whole.

The test suite asserts that the rules match every enumerated "exact" entry and refine the sound single-probability column.

| Case | Two-rate (ε, ω) | Exact (ε*, ω*) | Decaf derived δ | Decaf annotated | Single-prob sound δ |
|---|---|---|---|---|---|
| Bloom pre-filter + exact check of the same fact (LSM read path) | (0, 0) | (0, 0) | 0.01 | – | 0.01 |
| Bloom answer AND exact predicate of a different fact | (0.01, 0) | (0.01, 0) | 0.01 | – | 0.01 |
| AND of two Bloom answers (different sets) | (0.01, 0) | (0.01, 0) | 0.0199 | – | 0.0199 |
| Cascade of 3 independent filters on one set | (1.0e−6, 0) | (1.0e−6, 0) | 0.0297 | – | 0.0297 |
| Same cascade, shared hash seed | (0.01, 0) | (0.01, 0) | 0.0297 (product not licensed; not violated here) | – | 0.03 |
| Miller–Rabin alone, 10 rounds | (9.54e−7, 0) | – (attained: composite n, each witness lies independently with rate exactly 1/4) | 0.9437 | 9.54e−7 | 0.9437 |
| Miller–Rabin alone, 4 rounds | (0.003906, 0) | (0.003906, 0) | 0.6836 | 0.003906 | 0.6836 |
| Miller–Rabin (10 rounds) AND set query | (0.01, 0) | – | 0.9442 | 0.01 | 0.9442 |
| Miller–Rabin (4 rounds) AND set query | (0.01, 0) | (0.01, 0) | 0.6868 | 0.01387 | 0.6868 |
| OR over 8 sharded filters (ε = 0.001 each) | (0.007972, 0) | – | 0.007972 | – | 0.007972 |
| OR over 3 sharded filters | (0.002997, 0) | (0.002997, 0) | 0.002997 | – | 0.002997 |
| Blocklist gate !bloom(Block,x) && auth(x) | (0, 0.01) | (0, 0.01) | 0.01 | – | 0.01 |
| Blocklist gate, approximate auth (0.02, 0.05) | (0.02, 0.0595) | (0.02, 0.0595) | 0.0595 | – | 0.0595 |
| AND of symmetric-noise bits (0.01, 0.01) | (0.01, 0.0199) | (0.01, 0.0199) | 0.0199 | – | 0.0199 |
| XOR of two Bloom answers | (0.0198, 0.01) | (0.0198, 0.01) | 0.0199 | – | 0.0199 |

**Where two rates are strictly better.**

- **Equal-meaning compositions.** The pre-filter + exact check is typed exact, against δ = ε. A cascade of three independent filters gives ε³ against about 3ε.
- **One-sided amplification.** Miller–Rabin is derived as 4⁻ᵏ rather than 1 − 0.75ᵏ.
- **Conjunctions across facts.** ε rather than about 2ε.
- **Safety statements.** The blocklist gate's ε = 0 says that a blocked item is never admitted, a property Decaf cannot express. "No false negatives" is carried through every monotone case.

**Where they add only one-sidedness.**

- OR over shards: same FPR as Decaf, plus ω = 0.
- AND with an exact predicate of a different fact: same FPR, plus ω = 0.

**Where they add nothing.**

- Symmetric-noise hardware bits: the collapse max(ε, ω) equals Decaf's δ.
- XOR: comparable to Decaf, and one-sidedness is lost.

**Where neither helps: learned filters.** A trained model's errors are deterministic per key, so the per-valuation worst case is 1. Learned-filter guarantees are distributional over the query stream (Mitzenmacher 2018), outside this semantics.

## 10. Related work and novelty

**Approximate-computing types.** Decaf (OOPSLA 2015), Rely (OOPSLA 2013), Chisel (OOPSLA 2014), EnerJ (PLDI 2011) and Uncertain⟨T⟩ (ASPLOS 2014) carry a single correctness probability, or none, with independent faults. Several forbid approximate conditions. We refine their Boolean fragment (Theorem 6) and handle approximate conditionals.

**Error-bound logics.** aHL (ICALP 2016) can *derive* our dependence-free rules: each rate is an aHL judgment with a precondition on the exact value, and its [Or] case rule yields the maximum. We present them as derived rules. aHL excludes independence; Eris and Coneris (ICFP 2024/2025) add expectation-based error credits. Independence certification by disjoint randomness is the province of probabilistic separation logics: PSL (POPL 2020), Lilac (PLDI 2023), DIBI (LICS 2021) and Bluebell (POPL 2025). Our provenance side condition is their syntactic shadow.

**Reliability and probability bounds.**

- Fréchet (1935), Boole and Hailperin (1965) supply the per-node bounds.
- Probability bounds analysis (Ferson et al. 2004) composes Fréchet bounds through fault trees and asserts best-possibility without repeated parameters.
- Circuit reliability (Choudhury–Mohanram 2007/2009) propagates 0→1 and 1→0 rates conditional on the error-free value, averaged over inputs and assuming independent gates.
- Our setting differs in quantity (error rates conditional on latent truth, worst case over truth, no prior), in the dependence regime (arbitrary by default), and in form (a type discipline with optimality theorems).

**Databases and statistics.**

- Shivakumar et al. (VLDB 1998) define FP/FN of approximate predicates conditional on the ideal predicate. They compose filters of one ideal predicate under conditional independence (our ≡ rules in regime I) and average across different predicates.
- Probabilistic predicates (SIGMOD 2018) preserve one-sidedness under independence.
- Berger's intersection-union test (1982) is the AND-ε rule at one level. It has no ω side, since power is not uniformly bounded in testing.

**Novelty paragraph (honest).** We found no prior that types Boolean expressions with a pair (ε, ω) indexed by latent truth and propagates it compositionally through AND/OR/NOT/XOR/if with dependence-free defaults and certified-independence tightening. We also found no prior that proves the rules are best transformers and exact on read-once programs. However:

- the inequalities are classical;
- the dependence-free rules are derivable in aHL;
- read-once best-possibility is known in unconditional form;
- the polarity theorem is an elementary analogue of RP closure.

The contribution is a clean, checkable discipline and its precise optimality boundary. It is not a new probabilistic inequality. A reviewer may reasonably call parts of it folklore; the paper should pre-empt this by crediting the sources above in the introduction (§1, "What is not new").

## 11. Limitations

- **Non-adaptive queries.** Adaptively chosen keys against the same source void per-query rates (cf. adaptive Bloom-filter attacks); Remark 4.2 covers approximate keys whose error is fixed independently of the queried structure's answers (its union bound needs no independence); keys chosen adaptively from the same source's answers are excluded.
- **Declared rates are upper bounds** that must hold conditionally on every latent valuation. This is true for idealized hashing and fixed sets, but must be justified per structure.
- **Equal-meaning detection is syntactic** and misses semantic equalities.
- **Mixed source structures are sound but not exact** (Proposition 4a); the source-indexed refinement is open [C].
- **First-order only.** Higher-order functions would need a logical-relations semantics indexed by latent valuations [C].
- **Partial mechanization.** Only the independent AND/OR product lemma is mechanized among the independent rules; provenance-based independence and Theorems 2–7 are not mechanized.

## 12. Artifact

- `tworate.py`: the checker.
- `oracle.py`: exact semantics, with block-polytope vertex enumeration in exact rational arithmetic.
- `test_tworate.py`: 52 tests (after parametrization), including about 4,250 hypothesis-generated instances, among them 400 random programs using Let/Pair/Case; statement and branch coverage is reported in README.md. Mutation testing by the independent review (22 mutants of the rules) found two unsound mutants that the earlier suite missed (IF provenance, equal-branch IF erasure); targeted tests now kill them.
- `casestudies.py`: the case-study table.
- `lean/TwoRate.lean`: the Lean soundness proof (dependence-free fragment).
- `lean/TwoRateIndep.lean`: the independent AND-ω / OR-ε product lemma.

## 13. Candidate venues (free to author)

| Venue | Fit | Cost to author | Status |
|---|---|---|---|
| **Information Processing Letters** (Elsevier) | Short theorem-centred notes; best fit for an 8-page version | $0 on the subscription route (no APC unless OA chosen) | Policy as commonly stated; current APC route UNVERIFIED |
| **J. Logical and Algebraic Methods in Programming** (Elsevier) | Quantitative correctness, specification | $0 subscription route | Scope verified in the earlier dependence-calculus note; APC route UNVERIFIED |
| **LAFI workshop** (POPL-affiliated, extended abstracts, non-archival) | PL audience for a 2–4 page version | No publication fee | 2027 call UNVERIFIED |
| **QAPL** (ETAPS workshop, EPTCS proceedings, diamond OA) | Ideal topical fit | Free | No 2026 edition found; UNVERIFIED that it continues |
| **PACMPL (OOPSLA/ICFP) / TOPLAS** (ACM) | Only for a full version with inference over a real language and an evaluation | $0 only if SIUE participates in ACM Open, otherwise an APC | SIUE ACM Open participation UNVERIFIED (participants page returned HTTP 403) |
| **Logical Methods in Computer Science** (diamond OA) | Full mechanized version | Free | Expects a substantial paper |

**Recommendation.** An IPL-style short note, or a LAFI abstract, then fold the material into the monograph's types chapter.
