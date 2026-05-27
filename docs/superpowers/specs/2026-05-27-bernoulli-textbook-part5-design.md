# Design: Part V (The Boundary and Beyond) of the Bernoulli Textbook

**Author:** Alexander Towell
**Date:** 2026-05-27
**Status:** Design (pre-implementation)
**Parent spec:** `docs/superpowers/specs/2026-04-29-bernoulli-textbook-design.md`
**Sibling specs:** Part I (`2026-05-02`), Part II (`2026-05-17`), Part III (`2026-05-23`), Part IV (`2026-05-25`)
**Scope:** Section-level outline for chapters 16-18 (Part V, ~110 pp).

## 1. Purpose

Part V closes the book by stepping outside the Bernoulli framework's strict boundary, then applying the framework to two adjacent paradigms.

- **Chapter 16: Approximate but Not Bernoulli.** Cashes in the "negative-space" forward references seeded throughout chapters 1-13. Systems that look like approximate sets but violate Axiom 1 (independence) or Axiom 2 (block-rate stability): time-varying rates, correlated noise, adaptive adversaries.

- **Chapter 17: Cipher Maps and Trapdoor Computing.** The Bernoulli framework as the error model for trapdoor computing. Cipher maps are random approximate maps with cryptographic properties. The chapter draws on the sibling `~/github/trapdoor-computing/` monorepo.

- **Chapter 18: Encrypted Search as Relaxed Trapdoor.** Encrypted search systems as instances of the Bernoulli framework with privacy constraints. Draws on `~/github/papers/encrypted-search-thesis/`.

By the end of Part V, the reader has seen both the framework's boundary (what it doesn't cover) and two applications outside the standard scope (cryptographic and privacy-preserving).

## 2. Inherited Commitments

Same as Parts II-IV: B+D audience; monograph format; alex.sty notation; learning-outcomes box per chapter; 10-12 exercises with star markers (3/5/3); Path A subagent-driven Plan execution; soul-voice hook discipline.

## 3. Part V-Specific Decisions

### 3.1 Three Chapter Profiles

- Chapter 16 (~35 pp, light notebook): The boundary chapter; mostly counter-examples and analytical alternatives.
- Chapter 17 (~38 pp, no notebook): Theory + sidebar on oblivious computing. The framework's connection to cryptography.
- Chapter 18 (~37 pp, has notebook): Encrypted search application; draws on the thesis material in `papers/encrypted-search-thesis/`.

Total target ~110 pp; expect ~130 pp realistic per Plan 1-15 overshoot pattern.

### 3.2 Honesty Discipline in Chapter 16

Chapter 16 names cases where the Bernoulli framework FAILS. The book has set up many "we'll address this later" deferrals; chapter 16 cashes them. No defensive hedging; if a case is genuinely not Bernoulli, say so.

### 3.3 Source Material per Chapter

- Chapter 16: mostly fresh writing, with references to bias-variance/concentration literature (Devroye-Lugosi-Lugosi) and the standard non-iid concentration tools (martingale Azuma-Hoeffding, McDiarmid).
- Chapter 17: `~/github/trapdoor-computing/papers/cipher-maps/` and adjacent papers in the sibling monorepo.
- Chapter 18: `~/github/papers/encrypted-search-thesis/` (the master's thesis); `~/github/papers/encrypted_search_a_robust_approach/` if relevant.

### 3.4 Notebook Discipline

Per master spec:
- Ch 16: light notebook (correlated-error simulator showing how composition theorem breaks).
- Ch 17: no notebook (theory + cryptographic sidebar).
- Ch 18: substantive notebook (toy encrypted search demo).

## 4. Chapter Outlines

### Chapter 16: Approximate but Not Bernoulli (~35 pp, light notebook)

**Learning outcomes:** identify three failure modes (varying rates, correlated noise, adversarial), state why each violates Axiom 1 or Axiom 2, apply the appropriate analytical tool (martingale concentration, conditional bounds, adversary models) when Bernoulli machinery does not apply.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 16.1 | What Chapter 16 Is For | ~3 | fresh | Recall the deferrals from chapters 1, 3, 5, 10, 13; this chapter cashes them. |
| 16.2 | Varying Rates Over Time | ~6 | fresh | Time-non-stationary FPR/FNR; e.g., a classifier that degrades as data drifts. Violates Axiom 2 (block rates not stable). Analytical tool: martingale Azuma-Hoeffding. |
| 16.3 | Correlated Noise Across Queries | ~6 | fresh | Two queries on the same Bloom filter share hash collisions; same query repeated is deterministic. Violates Axiom 1 (element-wise independence). |
| 16.4 | Adversarial Inputs | ~6 | fresh | A query distribution chosen to maximize FPR (or to evade detection); not iid; gradient-descent attackers. |
| 16.5 | Where the Framework Still Helps | ~4 | fresh | Even outside strict Bernoulli, the rate-plane geometry (chapter 6 §6.4 perfect-filter line) and the channel-matrix view (chapter 2 §2.4 / chapter 9 §9.2) often still give useful approximations. |
| 16.6 | What's Next | ~2 | fresh | Forward to chapters 17-18 for applications. |
| 16.7 | Bibliographic Notes | ~2 | fresh | Devroye et al, McDiarmid, adversarial ML literature, adaptive-adversary results. |
| Exercises | ~2 | fresh | 11 with star markers. |

### Chapter 17: Cipher Maps and Trapdoor Computing (~38 pp, no notebook)

**Learning outcomes:** state the cipher-map abstraction; recognize the Bernoulli framework as its error model; relate the trapdoor computing paradigm to the noisy-bit atom; identify privacy-vs-correctness trade-offs.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 17.1 | What is a Cipher Map? | ~4 | reformulate `trapdoor-computing/papers/cipher-maps/` | A function that computes faithfully on encrypted inputs, up to bounded error. |
| 17.2 | The Bernoulli Framework as Error Model | ~6 | reformulate paper | Cipher-map error rates ARE Bernoulli rates; chapter 4 Kronecker theorem governs their composition. |
| 17.3 | Trapdoor Computing Paradigm | ~7 | reformulate trapdoor-computing monorepo | The trapdoor key enables computation on encrypted data; the framework's $\fprate, \fnrate$ govern recovery quality. |
| 17.4 | Sidebar: Fully Homomorphic Encryption | ~5 | fresh | Brief comparison to FHE; cipher maps are weaker but practical. |
| 17.5 | Boolean Algebra Over Trapdoor Sets | ~6 | reformulate sibling paper `boolean-algebra-over-trapdoor-sets/` | Chapter 3 §3.3 composition theorem applied to trapdoor sets. |
| 17.6 | Maximizing Confidentiality | ~4 | reformulate sibling paper `maximizing-confidentiality/` | The chapter 7 §7.4 PPV framework applied to confidentiality measures. |
| 17.7 | Bridge | ~2 | fresh | Chapter 18 applies these ideas to search specifically. |
| 17.8 | Bibliographic Notes | ~2 | fresh | Trapdoor-computing monorepo papers; Gentry's FHE; related work. |
| Exercises | ~2 | fresh | 11 with star markers. |

### Chapter 18: Encrypted Search as Relaxed Trapdoor (~37 pp, substantive notebook)

**Learning outcomes:** state the encrypted-search problem; recognize Bloom-filter-based encrypted-search constructions as Bernoulli instances; apply chapter 7 PPV/NPV to confidentiality analysis; build a toy encrypted-search system.

| § | Title | Pages | Source | Purpose |
|---|---|---|---|---|
| 18.1 | The Encrypted Search Problem | ~4 | reformulate thesis | Search over encrypted data without revealing query or document content. |
| 18.2 | Bloom-Filter-Based Constructions | ~7 | reformulate thesis | Encrypted bit array as a "permitted positive" filter. |
| 18.3 | Confidentiality Measures | ~6 | reformulate thesis + chapter 7 §7.4 | PPV / NPV / F1 applied to leakage. |
| 18.4 | Estimation under Adversarial Queries | ~5 | reformulate `estimating-es-conf-mab/` paper | Multi-armed bandit confidence intervals for confidentiality. |
| 18.5 | A Toy Encrypted Search System | ~6 | fresh (notebook demo) | Walk through a minimal end-to-end encrypted-search construction. |
| 18.6 | Closing the Book | ~3 | fresh | Recap the full arc: noisy bit (Part I) → sets (Part II) → maps and types (Part III) → optimal constructions (Part IV) → boundary and applications (Part V). |
| 18.7 | Bibliographic Notes | ~2 | fresh | Encrypted-search thesis; related papers in the encrypted-search-thesis monorepo. |
| Exercises | ~2 | fresh | 11 with star markers. |

## 5. Forward and Backward Reference Map

| From | To | Form |
|---|---|---|
| §16.1 | ch 1 §1.5, ch 3 §3.4, ch 5 §5.4, ch 10 §10.5, ch 13 §13.4 | backward (cashes deferrals) |
| §16.2 | ch 4 §4.3 (Axiom 2) | backward |
| §16.3 | ch 4 §4.2 (Axiom 1), ch 6 §6.1 (composition under independence) | backward |
| §16.5 | ch 6 §6.4 (perfect-filter line), ch 9 §9.2 (channel matrix) | backward |
| §17.2 | ch 4 §4.4 (Kronecker), ch 9 §9.3 (n-ary Kronecker) | backward |
| §17.5 | ch 3 §3.3 (composition theorem) | backward |
| §17.6 | ch 7 §7.4 (PPV/NPV) | backward |
| §18.2 | ch 5 §5.2 (Bloom filter) | backward |
| §18.3 | ch 7 §7.4, ch 14 (BHF for compact representation) | backward |
| §18.6 | all chapters | closing recap |

## 6. Page Budget

| Chapter | Target | Notes |
|---|---|---|
| Ch 16 | ~35 pp | Boundary catalog + analytical alternatives |
| Ch 17 | ~38 pp | Cipher maps + trapdoor computing |
| Ch 18 | ~37 pp | Encrypted search application + book closing |
| **Total** | **~110** | Expect ~125-135 pp actual |

Adding to running total: Parts I-IV = 434pp; Part V target adds ~110pp → 544pp total book body. Master spec target ~500pp; we are tracking at +8.8% over.

## 7. Sequencing for Plans 16-18

- Plan 16: chapter 16 first (boundary; cashes deferrals).
- Plan 17: chapter 17 (cipher maps; depends on broader framework but not on chapter 16).
- Plan 18: chapter 18 + book closing + full-book integration check.

## 8. Open Action Items

1. **Chapter 17 sources are external.** The trapdoor-computing monorepo lives in `~/github/trapdoor-computing/`. Plan 17 must read the relevant papers from that sibling repository.
2. **Chapter 18 thesis source.** The master's thesis lives in `~/github/papers/encrypted-search-thesis/`.
3. **Decision on Appendix B (Five Core Principles cheat sheet).** Currently a Plan 0 stub; the polish plan should populate it. Out of scope for Plans 16-18.

## 9. Out of Scope

- Full FHE treatment (chapter 17 §17.4 is a brief sidebar; cite Gentry).
- Information-theoretic encrypted-search lower bounds (advanced; cite the thesis but do not subsume).
- Performance benchmarks for production encrypted-search systems.

## 10. Success Criteria for Part V

Part V succeeds if:

1. A reader who has finished Parts I-IV can finish Part V in three focused weeks.
2. Chapter 16 cashes every "we'll address this later" deferral seeded in earlier chapters; no forward-reference debts remain.
3. Chapter 17 connects the Bernoulli framework to cryptographic ideas via a clean cipher-map definition.
4. Chapter 18 demonstrates a working encrypted-search construction at the end of the book.
5. §18.6 closes the book with a satisfying recap of the full arc.
