# Two-rate (FPR/FNR) types for approximate programs: quick-shot investigation

Date: 2026-10-21. Time-boxed to roughly one working day of agent effort. Nothing was submitted, published or committed.

## Verdict: GO for a short paper (letters journal or workshop); NO-GO for a full PL-conference paper as-is

**The novelty gate passes, narrowly.** No prior was found that types Boolean expressions with a pair (ε, ω) indexed by latent truth and propagates it compositionally, under either dependence regime: dependence-free rules by default, tightened only where independence is certified. See [gate.md](gate.md).

But the per-connective inequalities are classical, and several priors hold pieces:

| Prior | What it already covers |
|---|---|
| aHL (Barthe et al., ICALP 2016) | Can derive the dependence-free rules through its case rule |
| Choudhury–Mohanram (DATE 2007 / TCAD 2009) | Propagates 0→1 and 1→0 rates conditional on the error-free value, averaged over inputs, independent gates |
| Shivakumar–Garcia-Molina–Chekuri (VLDB 1998) | Composes FP/FN of filters for the *same* ideal predicate under conditional independence |
| Berger's intersection-union test (1982) | Is the AND-ε rule at a single level |
| Ferson et al. (2004) | Assert unconditional read-once best-possibility |

The contribution is therefore a discipline plus optimality theorems, not new inequalities.

## The hypothesis, tested

| Claim in the brief | Outcome |
|---|---|
| AND: ε = max(ε₁, ε₂) under arbitrary dependence | **Confirmed**, and tight. Independence does *not* improve it across different facts; it only improves ω, or ε when the two operands estimate the same fact. |
| AND: ω = ω₁+ω₂ (dependent), 1−(1−ω₁)(1−ω₂) (independent) | **Confirmed**, with a cap min(1, ·). The independent form is valid only under disjoint provenance; forcing it on a shared source is unsound (exact 0.4 vs 0.36). |
| OR dual, NOT swaps | **Confirmed.** |
| XOR "loses asymmetry", bound ½(1−∏(1−2q_i)) | **Refined.** That bound is sound but loose. The tight XOR pair stays class-specific: leaves (0.01, 0.1) give (0.18, 0.108). What XOR loses is *one-sidedness*. |
| ω = 0 preserved by AND/OR, destroyed by NOT/XOR | **Confirmed** as a polarity theorem, complete on read-once programs. NOT turns ω = 0 into ε = 0. |
| Tighter than Decaf (AND of two Bloom answers: ε vs about 2ε) | **Confirmed** (0.01 vs 0.0199). In general max(ε, ω) ≤ Decaf-style δ, strictly on one-sided operands. |
| b ∧ b sound on the Fréchet side | **Confirmed**: sound, not tight ((ε, 2ω) vs (ε, ω)). |
| Pitfall (b₀∧b₁)∨b₂ at 010 | **Reproduced exactly.** Exact error 0.03764, naive 0.020392 (unsound), rule 0.0396 (sound; attained under upper-bound semantics). |

**Additions beyond the brief:**

- an if/case rule: max(u(ε₁, ω_c), u(ε₂, ε_c)), tighter than encoding if with AND/OR, plus an equal-branch refinement (IF≡) that removes the condition's cost when both branches estimate the same fact;
- an equal-meaning refinement that derives amplification (Miller–Rabin gives 4⁻ᵏ; Decaf-style composition gives 1 − 0.75ᵏ);
- a best-transformer theorem;
- read-once exactness in both uniform regimes;
- coNP-completeness of deciding whether the exact rate is 0 once primitives are shared;
- a counterexample showing that mixed source structures break exactness (0.56 vs 0.52).

## Main results (labels: [P] paper proof, [L] Lean, [E] exact finite checks)

- **Theorem 1, soundness** [P][L][E]. The default (non-≡) dependence-free rules without the min(1, ·) cap, over the Boolean core with sharing and constants, are machine-checked in `lean/TwoRate.lean`. The independence tightening of AND-ω (dually OR-ε) over product laws is a pointwise lemma in `lean/TwoRateIndep.lean`. Both use Lean 4 core only, have no `sorry`, and depend on the axioms `propext` and `Quot.sound` only.
- **Theorem 2, each rule is the best abstract transformer** for its connective in the uniform regimes [P][E].
- **Theorem 3, read-once exactness**: the rules compute the true worst case exactly [P][E]. This is the latent-indexed analogue of Moore's single-use theorem.
- **Proposition 4, sharing loses exactness; exact analysis is hard** [P][E]. With every rate in (0, 1), deciding whether ε* = 0 is coNP-complete.
- **Theorem 5, polarity: a static "no false negatives" guarantee** [P][E].
- **Theorem 6, two-rate refines single-probability typing; Proposition 7, amplification needs two rates** [P][E].
- **Conjecture**: a source-indexed refinement is exact for read-once programs under arbitrary source structure [C].

## Test results

`test_tworate.py` has 52 tests (after parametrization), all passing (about 4–5 min). They include about 4,250 hypothesis-generated instances, checked against an exact rational oracle over all latent valuations and all admissible joint error laws, which are enumerated as polytope vertices per source. The instances are:

- 1,000 + 400 random programs with sharing, aliases, constants and mixed sources, plus 400 using Let/Pair/Case (soundness);
- 150 (regime I, 2–5 leaves) + 150 + 60 (regime D, 2–4 leaves) random read-once programs (exactness);
- 600 best-transformer instances (each connective × regime), plus 150 for AND≡/OR≡/XOR≡ and 200 for IF≡;
- 300 structured programs cross-checking desugaring against an independent evaluator;
- 400 programs for the refinement theorem;
- 300 programs for the polarity theorem (both regimes).

Coverage is 100% statement and branch for `oracle.py`, 99% for `tworate.py` and 95% for `casestudies.py`.

**Independent adversarial review.** A separate reviewer agent rechecked the rules, oracle and theorems.

- **Confirmed:** soundness (exhaustive grids of 28,812 binary and 31,250 IF instances, plus 7,756 random and adversarial programs); oracle exactness (agreement with an independent rational simplex and with an independent oracle); Theorem 3 on read-once programs with 4–6 leaves in both regimes; all table numbers.
- **Fixed:** a false strictness claim in Theorem 6; overstated Lean labels; a missing constant-free hypothesis in Theorem 5; Remark 4.3's interval (the same formula in the `bernoulli_data_type` manuscript is wrong when ε + ω > 1); several wording slips.
- **Mutation testing:** two unsound mutants (IF provenance, equal-branch IF erasure) and one loose mutant initially survived. Targeted tests now kill all three.
- **Added:** the IF≡ rule, which the review identified as missing.

The case studies are tabulated in `note.md` §9 and stored in `casestudies.json`.

- **Strictly better than Decaf:**
  - an exact check behind a pre-filter is typed exact, against ε;
  - a cascade of three independent filters on one set gives ε³ against about 3ε;
  - Miller–Rabin is derived as 4⁻ᵏ;
  - AND across facts gives ε against about 2ε;
  - a blocklist gate gets ε = 0 ("never admits a blocked item").
- **One-sidedness only:** OR over shards.
- **Nothing:** symmetric hardware noise; XOR.
- **Out of scope:** learned filters, whose guarantees are distributional.

## Remaining effort to a short submission

| Item | Effort | Why it matters |
|---|---|---|
| LaTeX write-up from `note.md` (8 pages) | 2–3 days | The draft is complete in structure; proofs need full detail for Theorem 3 |
| Read the not-yet-read primaries: Choudhury–Mohanram TCAD 2009, Hailperin 1965, Ferson §2.5, multiple-testing closed-testing/gatekeeping | 1 day | The most likely remaining collisions are on the ε side |
| Mechanize the remaining independent rules (XOR/IF products, provenance → independence) and Theorem 3 in Lean | 3–5 days (optional) | Strengthens a letters-journal or workshop submission; not required |
| Verify venue policies (IPL/JLAMP APC routes, LAFI 2027, SIUE ACM Open) | 1 hour | Several statuses are UNVERIFIED |
| For a full OOPSLA/ECOOP paper: inference for a real language, higher-order functions, an implementation and an evaluation on real programs | Months | Matches idea C in `../program-strategy/README.md` |

**Recommended route.** An Information Processing Letters-style note (free on the subscription route), or a LAFI extended abstract. Then fold the rules into the monograph's types chapter, which currently propagates prior-dependent rates (ch03 "Closure under Boolean operations"). Also flag that `bernoulli-py`'s `BernoulliBool.__and__` multiplies FPRs (shared-truth semantics), which under-reports for operands with different truths. A test here demonstrates the issue; nothing outside this directory was changed.

## Files

| File | Contents |
|---|---|
| [gate.md](gate.md) | Prior-art gate: verdict, overlap table, self-overlap, limitations |
| [note.md](note.md) | Draft paper outline: calculus, rules, theorems with proofs, case studies, related work, novelty, venues |
| `tworate.py` | Closed-form type checker, plus a Decaf-style single-probability baseline |
| `oracle.py` | Exact semantics and exact worst case (vertex enumeration, Fractions) with witness checking |
| `test_tworate.py` | The test suite |
| `casestudies.py`, `casestudies.json` | Case-study comparison |
| `lean/TwoRate.lean` | Lean 4 soundness proof of the dependence-free Boolean fragment |
| `lean/TwoRateIndep.lean` | Lean 4 lemma: independent AND false-negative (dually OR false-positive) bound over product laws |

## Reproduce

```bash
cd .research/two-rate-types
../../bernoulli-py/.venv/bin/python -m pytest -q test_tworate.py
../../bernoulli-py/.venv/bin/python -m pytest -q --cov=tworate --cov=oracle --cov=casestudies --cov-branch test_tworate.py
../../bernoulli-py/.venv/bin/python casestudies.py
(cd lean && ~/.elan/bin/lean TwoRate.lean && ~/.elan/bin/lean TwoRateIndep.lean)   # silent = success
```
