# Logic and Proof-Correctness Report

**Paper**: A Forward (epsilon, omega) Calculus for Quantum Readout Error
**Date**: 2026-06-07
**Reviewer role**: logic-checker (proof correctness, claim support, logical chain integrity)

All claims below were checked analytically and, where possible, confirmed by
independent Monte Carlo simulation and symbolic algebra (sympy). Every printed
numeral in Table 1 was recomputed.

## Verdict

The mathematical core is **sound**. Every theorem, proposition, and corollary
in Section 3 (sec:calculus) is correct as stated, and the Section 4 worked
example (Table 1, the Taylor expansion) is numerically and symbolically exact.
I found no incorrect proof. I did find a small number of places where the prose
of a proof is terser than the result deserves, and one statement-level
imprecision (the FPR conditioning in Theorem 3.3) that is correct but invites
misreading. These are Minor.

## Checked results

### Proposition 3.1 (NOT), prop:not  -  CORRECT
Swapping (epsilon, omega) -> (omega, epsilon) under negation is immediate from
the definitions. A false positive for not-b is (not-b = 1, not-t = 0) = (b = 0,
t = 1), which is the omega event. The proof is complete and correct.

### Theorem 3.3 (AND/OR), thm:andor  -  CORRECT (statement slightly loose)
- **FNR of conjunction**, eq:and-fnr, omega_and = 1 - prod(1 - omega_i):
  verified by Monte Carlo. Conditioned on all t_i = 1, the conjunction reads 0
  iff at least one bit is independently missed; complement of prod(1 - omega_i).
  Correct.
- **FPR of conjunction**, eq:and-fpr, epsilon_and = prod(epsilon_i): verified by
  Monte Carlo at the all-false corner (empirical 0.00077 vs predicted 0.00075
  for params (0.10,0.20),(0.05,0.30),(0.15,0.08)). Correct.
- **The "all-negative corner is the smallest, not the largest" claim**: verified.
  Across all latent assignments with conjunction-latent 0, the (0,0,0) corner
  gave the minimum false-positive rate (0.00077), and turning any latent input
  true raised the rate (e.g. (1,1,0) gave 0.084). The proof's sentence "an input
  whose latent value is true replaces its epsilon_i by 1 - omega_i and so raises
  the conjunction's false-positive rate" is exactly right.
- **OR dual**, eq:or: verified by Monte Carlo (omega_or = prod(omega_i) emp
  0.00486 vs 0.00480; epsilon_or = 1 - prod(1 - epsilon_i) emp 0.27366 vs
  0.27325). The "(ii) follows from (i) by Prop 3.1 and De Morgan" step is valid.

**Minor imprecision worth fixing.** The theorem statement says the conjunction's
false-positive rate "is" prod(epsilon_i), then the body and remark clarify this
is the all-negative *corner* of a latent-assignment-weighted quantity, not the
single unconditional FPR. The statement and proof are mutually consistent and
ultimately correct, but a reader who stops at eq:and-fpr could mistake a corner
for the marginal rate. The fix is one clause in the theorem statement: write
"conditioned on all latent inputs false, its false-positive rate is
prod(epsilon_i)" symmetrically to how the FNR clause already conditions on "all
t_i = 1." The FNR clause is conditioned cleanly; the FPR clause should match.

### Corollary 3.4 (Composition theorem), cor:composition  -  CORRECT
eta_total = 1 - prod(1 - eta_i). One-line proof (chain correct iff every stage
correct) is valid. The identification with eq:and-fnr (set eta_i = omega_i) is
exact: confirmed numerically (both 0.48480 on the test vector). The remark that
it linearizes to sum(eta_i) (the union bound, an overestimate) is correct.

### Theorem 3.5 (Parity), thm:parity  -  CORRECT
P(XOR X_i = 1) = 1/2(1 - prod(1 - 2 q_i)). The +-1 encoding proof is valid:
S_i = 1 - 2 X_i gives E[S_i] = 1 - 2 q_i, S = prod S_i = 1 - 2 (XOR X_i), and
P(XOR = 1) = P(S = -1) = 1/2(1 - E[S]). I confirmed the n=2 case symbolically
against direct enumeration: 1/2(1 - (1-2q)^2) = 2q(1-q), exactly the
"exactly-one-of-two" probability. Correct.

### Corollary 3.6 (Asymmetric parity), cor:parity-asym  -  CORRECT
Applying Theorem 3.5 to the flip indicators F_i = 1[b_i != t_i] with
P(F_i = 1) = r_i (= epsilon_i if t_i = 0, omega_i if t_i = 1) gives the per-
latent-assignment disagreement probability 1/2(1 - prod(1 - 2 r_i)). I verified
all 8 latent assignments by Monte Carlo for an asymmetric inhomogeneous channel;
every empirical rate matched the predicted value to within sampling error
(e.g. latent (0,1,0): emp 0.389 vs pred 0.388). Correct. The remark that the two
"sides" (true parity 0 vs 1) generally carry different error is the genuinely
novel asymmetric content and it is sound.

### Proposition 3.7 (Tensor factorization), prop:tensor  -  CORRECT
Under independence the joint readout law is the product of marginals, so
A = tensor Q_i, and every derived rate in Section 3 was computed from marginal
flip probabilities; hence no entry of the 2^n x 2^n matrix need be formed. The
proof is correct, if almost definitional. The marginal-on-a-subset claim is also
correct under independence.

### Section 4 worked example  -  CORRECT
- Table 1: every one of the six (q, n) rows reproduced to all printed digits.
  P_exact = 1/2(1 - (1-2q)^n), P_lin = nq, rel. overestimate
  (P_lin - P_exact)/P_exact. My values: 1.0101, 3.0505, 7.2120, 5.2632,
  16.3129, 40.4660 percent, matching the printed 1.0, 3.1, 7.2, 5.3, 16.3, 40.5.
- The Taylor claim "P_exact = nq - C(n,2)(2q)^2/2 + ... = nq - n(n-1)q^2 + O(q^3)"
  is symbolically exact: the q-coefficient is n, the q^2 coefficient is -n(n-1),
  and the intermediate -C(n,2)(2q)^2/2 equals -n(n-1)q^2. The "overestimate"
  conclusion follows because the q^2 term is negative. Correct.
- The bound "P_exact <= 1/2" holds because (1-2q)^n in [-1, 1]. Correct.
- "For nq >~ 1/2 the linear rule can exceed 1": correct (nq is unbounded).

## Logical-chain integrity

The dependency graph is clean and acyclic: Def 3 (atom) -> Prop NOT -> Thm
AND/OR (uses NOT + De Morgan) -> Cor composition (special case of AND-FNR) and
Thm parity -> Cor asymmetric parity (applies parity to flip indicators) ->
Prop tensor -> Section 4 (instantiates asymmetric parity). No result is used
before it is proved. The independence hypothesis is stated once at the head of
Section 3 and is genuinely required by every step that follows; I found no place
where independence is silently dropped or silently assumed beyond what is
stated.

## Findings

- **Minor (L1)**: Theorem 3.3 statement, eq:and-fpr. The FPR clause is stated as
  an unconditional rate but is actually the all-negative latent corner; the
  proof and remark say so, but the statement should condition explicitly to
  match the (correctly conditioned) FNR clause. Suggested fix: add "conditioned
  on all latent inputs false" to the FPR sentence.
- **Suggestion (L2)**: Proposition 3.7's proof is essentially definitional ("of
  which there is none under independence"). Consider a one-line forward pointer
  to where non-independence would break it (the crosstalk discussion in
  sec:scope), so the proposition reads as the boundary of validity rather than a
  triviality.
- **Suggestion (L3)**: The majority-vote remark (Remark 4.1) gives the binomial
  tail sum but does not label it as conditioned on one side (flip rate r in
  {epsilon, omega}); it does say "on the conditioned side," which is enough, but
  a half-sentence noting the two sides differ would mirror the parity treatment.

No Critical or Major logic findings. The calculus is correct.
