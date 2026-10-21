# Constrained truth and finite hashing: opportunity audit

Date: 2026-10-13. Author identity for subsequent manuscript use: Alexander
Richard Towell. This note records proved statements and checked baselines;
it does not assert research originality.

## Assessment

Integrity constraints genuinely improve a worst-case error contract beyond
canonical source deduplication. For two functional rows and a candidate set of
size `k >= 2`, independent one-sided membership errors of rate `alpha` give the
sharp false-positive envelope

`1 - (1-alpha)^2 (1-alpha^2)^(k-2)`.

The gain comes from restricting exact truth: only two witnesses can have just
one absent input. Every other witness requires two errors. This is a short
product/monotonicity calculation, not a new inference algorithm.

The decisive comparison is **constraint-aware witness union bounds**, rather
than only ordinary zero-certificate bounds. The bound
`2 alpha + (k-2) alpha^2` captures the same first-order gain. At a 5% output
target, the independent product can save at most about 0.03684 continuous
fingerprint bits per row relative to that bound. A finite 4-wise polynomial
fingerprint family proves the union bound with one fingerprint per functional
row and a single 32-byte seed. It does not require independence among witnesses.

For unrestricted row intersection, shared value fingerprints are an even
stronger alternative: they remove the candidate-domain-size dependence. For
queries restricted to an arbitrary supplied candidate set, that simple
alternative can lose the double-error benefit. Row-specific fingerprints then
provide the relevant inexpensive baseline.

The nearby binary-linear exact collision formula is precisely a specialization
of the classical Crapo–Rota Critical Theorem. The constrained-truth formulas
below are elementary consequences of product measures and cardinality
constraints. Neither establishes a new publishable theory by itself. A useful
contribution would need demonstrable compiler/representation benefits over the
explicit baselines here, or a substantially stronger new problem/result.

## 1. Model and two-row sharp theorem

Fix an exact database, two distinct canonical rows `u,v`, and a finite candidate
set `C={1,...,k}` selected independently of construction randomness. Write
`A_i=R(u,i)` and `B_i=R(v,i)`. The query is

`Q_C = OR_{i in C} (A_i AND B_i)`.

Assume each row has at most one exact value. A negative exact answer means the
sets `I={i:A_i=1}` and `J={i:B_i=1}` are disjoint, with `|I|,|J|<=1`. Rows may
have values outside `C`; those are represented by an empty restricted row.

For this section alone, every **distinct canonical** absent membership bit
accepts with probability `alpha`, independently across all such bits. True
membership bits always accept. The construction draws those bits once and all
queries reuse them. Nothing resamples on a repeated query.

For any fixed admissible negative profile, put `t=|I|+|J|`. Since witnesses have
disjoint source supports, their acceptance probabilities are `alpha` at the `t`
active candidates and `alpha^2` elsewhere. Therefore

`P(FP | I,J) = 1-(1-alpha)^t (1-alpha^2)^(k-t)`.

For `0<=alpha<=1`, this is nondecreasing in `t`. The maximum has
`t=min(k,2)`, attained by two different active candidates when `k>=2`. Thus

`worst_FPR = 1-(1-alpha)^min(k,2) (1-alpha^2)^(k-min(k,2))`.

This includes `k=0` (zero), `k=1` (`alpha`), zero error, and unit error. In the
interior `0<alpha<1`, the two-distinct-active case strictly dominates profiles
with fewer active candidates when `k>=2`.

An ordinary unrestricted zero-certificate contract uses `k` absent sources and
gives `1-(1-alpha)^k`, or `min(1,k alpha)` without independence. Its sharpness
profile need not respect functionality. That is why the constrained theorem
can improve it. Exact fixed-profile lineage evaluation already computes the
product above in linear time; the contribution of functionality is the
maximization over admissible unknown truth, not faster weighted model counting.

### Unequal source rates and bounded degrees

Let the absent rates be `a_i` for `A_i` and `b_i` for `B_i`. The exact fixed-profile
formula is

`1 - product_i [1-(1 if i in I else a_i)(1 if i in J else b_i)]`.

For `k=1` the worst rate is `max(a_1,b_1)`. For `k>=2` the maximum is attained
at two different active candidates. If some `a_i b_i=1`, it is one. Otherwise
put `c_i=1-a_i b_i`, `r_i=(1-b_i)/c_i`, and `s_i=(1-a_i)/c_i`. The maximum is

`1 - (product_i c_i) min_{i != j} r_i s_j`.

The two smallest entries in each of `r,s` suffice, so this is `O(k)` arithmetic
operations, including all zero/one boundary rates with the preceding branch.

With two degree bounds `|I|<=r`, `|J|<=s` and homogeneous errors, replace `t` by
`min(k,r+s)`. In particular equal degree bounds `Delta` give

`1-(1-alpha)^min(k,2Delta) (1-alpha^2)^(k-min(k,2Delta))`.

The heterogeneous bounded-degree optimum has an exact elementary dynamic
program. Let `D_i[a,b]` be the minimum no-FP product on the first `i` candidates
using exactly `a` left and `b` right true memberships. Initialize `D_0[0,0]=1`
and leave unreachable states explicit. The next candidate has three choices:

* Neither exact membership: multiply by `1-a_i b_i`.
* Left exact membership: multiply by `1-b_i` and increment the left count.
* Right exact membership: multiply by `1-a_i` and increment the right count.

Take minima and enforce the two capacities. The answer is
`1-min_{a<=r,b<=s} D_k[a,b]`. Complexity is `O(k(r+1)(s+1))` arithmetic operations
and `O((r+1)(s+1))` memory. Rational products handle boundaries without logarithms
or divisions. This is a standard capacity dynamic program, not a new optimizer.

## 2. A broader sharp cardinality theorem

For `m>=2` rows, each of exact degree at most `Delta`, consider

`Q = OR_{i=1}^k AND_{j=1}^m A_{ji}`,

with all canonical sources distinct, independent absent-bit rate `alpha`, and
empty exact `m`-way intersection. If candidate `i` has `t_i` true memberships,
then `0<=t_i<=m-1` and `sum_i t_i<=m Delta`. Its witness acceptance probability
is `alpha^(m-t_i)`. Put

`L=min(m Delta,k(m-1))`, `L=n(m-1)+s`, `0<=s<m-1`, `e=1[s>0]`.

The sharp worst-case contract is

`1-(1-alpha)^n (1-alpha^(m-s))^e (1-alpha^m)^(k-n-e)`.

**Proof.** For `0<alpha<1`, the logarithm of the no-FP product is the sum of
`f(t_i)=log(1-alpha^(m-t_i))`. This function is decreasing and strictly concave
on `[0,m-1]`. Increase the total load to `L`; then shifting load between two
interior columns toward an endpoint cannot increase the sum. Consequently the
minimum has `n` columns of load `m-1`, one column of load `s` if nonzero, and all
remaining columns empty.

These column loads can be realized with the row bounds, not merely with a
relaxed aggregate constraint. Assign the memberships of consecutive columns
to consecutive rows in a cyclic sequence `1,...,m,1,...`. Each column uses at
most `m-1` consecutive labels and hence no row twice. Total row loads differ
by at most one, and each is at most `ceil(L/m)<=Delta`. Thus the extremal profile
is feasible. Endpoint rates follow by continuity (and directly from the
probabilities). This proves both the upper bound and attainability.

For `Delta=1`, `k>=2`, this reduces to
`1-(1-alpha)(1-alpha^(m-1))(1-alpha^m)^(k-2)`.
For `k=1` it is `alpha`, and for `Delta=0` it is
`1-(1-alpha^m)^k`. The interpretation is concentrated almost-complete witnesses,
not a new form of model order.

The same extremal profile maximizes the witness union bound, because
`alpha^(m-t)` is increasing and convex in `t`. That bound is

`min(1, n alpha + e alpha^(m-s) + (k-n-e) alpha^m)`.

Thus most of the constrained-truth improvement survives without calculating
the product across witnesses.

## 3. How small is the extra benefit over the constrained union bound?

For the two-row class let
`U(alpha)=t alpha+(k-t)alpha^2`, `t=min(k,2)`, and let `S(alpha)` be the sharp
independent product contract. The inequality `1-x<=exp(-x)` gives

`1-exp(-U(alpha)) <= S(alpha) <= min(1,U(alpha))`.

Fix `0<epsilon<1` and `k>=1`. Let `alpha_U` solve `U(alpha_U)=epsilon` and
`alpha_S` solve `S(alpha_S)=epsilon`. These equations have unique relevant
solutions, and

`U(alpha_S)<=-log(1-epsilon)`.

For `r>=1`, `U(r alpha_U)>=r U(alpha_U)`. Hence

`alpha_S/alpha_U <= -log(1-epsilon)/epsilon`.

With the usual continuous fingerprint cost `-log2(alpha)`, the extra saving is
at most

`log2[-log(1-epsilon)/epsilon]` bits.

This is about 0.03684 bits at a 5% target, and tends to zero with the target.
Discrete fingerprint widths can still change by one bit near a boundary; this
does not contradict the continuous bound. The comparison assumes a common
rate and the stated cost proxy; it is not a general theorem about every
heterogeneous allocation or serialized format. The same argument applies to
the multiway union polynomial since it has nonnegative coefficients and no
constant term.

## 4. Finite 4-wise row fingerprints for restricted candidate queries

This is the strongest compact baseline identified in this audit. It is an
application of classical limited-independent hashing, not a new hash family.
See [Wegman and Carter, 1981](https://www.sciencedirect.com/science/article/pii/0022000081900337)
for the established hashing framework; the finite proof is included here.

Let `P=2^61-1`. Assign every possible queried `(row,value)` pair an injective
integer code in `[0,P)`. Codes must be fixed independently of the seed. Sample
four coefficients `c_0,c_1,c_2,c_3` independently and uniformly in `F_P`,
including zero, and set

`g(x)=c_0+c_1 x+c_2 x^2+c_3 x^3 mod P`,
`f(x)=g(x) mod M`, where `M=2^b` and `0<=b<=61`.

For every nonempty functional row with exact value `a`, store the fingerprint
`f(code(row,a))`. A theoretical partial-row extension stores presence separately,
so empty rows are exactly empty. The executable `FrozenRows` and workload below
implement total rows only; they do not implement that presence extension.
To test a tuple `(row,c)`, compare its computed fingerprint with the stored
one. This has no false negatives. A restricted query scans `c in C` and accepts
when both row tests accept. The row IDs must be distinct canonical rows.

### Exact collision rate after modulo reduction

Any four distinct field inputs have independent uniform `g` values. For exactly
four inputs this follows from invertibility of the Vandermonde evaluation
matrix; for fewer inputs each prescribed image has `P^(4-t)` preimages among
the coefficient vectors. Requiring a nonzero leading coefficient would spoil
this exact property.

Write `P=a M+r`, `0<=r<M`. The modulo buckets have sizes `a+1` at `r` outputs
and `a` at the other `M-r`. Therefore the exact collision probability of two
distinct inputs is

`q=[r(a+1)^2+(M-r)a^2]/P^2 = 1/M+r(M-r)/(M P^2)`.

Here `P mod M=M-1`, so

`q=1/M+(M-1)/(M P^2)`.

The rate is extremely close to `2^-b`, but the exact rational correction
matters in a mathematical certificate. For `b=61` it is `1/P`; for `b=0` it is
one. Uniform sampling of coefficients must use a sampler for `[0,P)`, not a
biased reduction of a fixed-length random word. The all-zero coefficient
vector is permitted and already accounted for.

### Restricted-query guarantee

Fix the exact rows and `C` before sampling the polynomial. In a negative query,
each candidate has one or two absent row tests. A single absent test collides
with probability exactly `q`. If both are absent, the relevant input codes are

`(u,a), (u,c), (v,d), (v,c)`.

All four are distinct because `u!=v`, `a!=c`, and `d!=c`. Four-wise independence
therefore makes the two collision events independent, so that witness has
probability exactly `q^2`, even when `a=d` outside `C`.

At most `t=min(k,2)` candidates can have only one absent test. The union bound
now proves the uniform contract

`P(FP) <= min(1, t q+(k-t)q^2)`.

If either row is empty, the proposed presence-aware extension has error zero. For
`k=0` the bound is zero; for `k=1` it is `q`. A fixed negative profile with `s`
singly absent witnesses has the tighter bound `min(1,s q+(k-s)q^2)`.

This probability is **unconditional over the uniform construction seed**, for
fixed data and a fixed query. It is not an assertion of mutual source
independence, an independent-witness product formula, a conditional guarantee
after inspecting the whole stored structure, or an adaptive-query guarantee.
Four-wise independence is used only within one witness; the union bound handles
all cross-witness dependence.

### Space, scope, and competing representations

Four canonical field coefficients serialized in eight bytes each cost exactly
32 bytes. Count this once for the shared seed. Fingerprints can use `b` bits per
nonempty row, plus presence/indexing, framing, alignment, and any dictionaries.
Integer dictionary IDs and an injective tuple packing can be supplied, but
their metadata and any exact dictionary storage must be counted. An encoding
modulo `P` that aliases distinct tuples invalidates the theorem.

For unrestricted pair intersection, store a shared **value** fingerprint of the
single exact value in each row. Unequal values collide with probability about
`2^-b`, independently of the domain size. For bounded-degree rows, storing
hashed value sets gives the union bound `|A||B| 2^-b` for a negative intersection.
No pairwise independence among these collision events is required.

For restricted `C`, simple shared-value equality is insufficient: if two rows
have the same exact value `a` outside `C`, their equality test always succeeds
and a match between `h(a)` and `h(C)` costs roughly `|C| 2^-b`, not
`|C| 2^-2b`. Row-specific fingerprints retain the double-error effect. For one
fixed candidate set, a stored exact `a in C` flag is another strong baseline;
it does not serve arbitrary candidate subsets without additional metadata.

An exact packed dictionary remains a required comparison: one functional value
from a domain of size `D`, plus absence, needs about `log2(D+1)` bits per row
before framing. The approximate fingerprint plan is most plausible when its
needed fingerprint width is materially smaller than that exact code and the
shared metadata can be amortized over many rows.

## 5. Binary-linear finite hashes and construction conditioning

Let `H` be a uniformly random `b` by `w` binary matrix. For fixed disjoint value
sets `A,B` in `F_2^w`, use shared value fingerprints and let
`D={a XOR b : a in A,b in B}` be the set of distinct nonzero differences. A
false intersection occurs precisely when `H(d)=0` for some `d in D`.

For each nonempty subset `S` of differences,

`P(H(d)=0 for all d in S)=2^(-b rank(S))`.

Each row of `H` must annihilate the rank-dimensional span, and the rows are
independent. Inclusion–exclusion gives the exact answer

`P(FP)=sum_{nonempty S subset D} (-1)^(|S|+1) 2^(-b rank(S))`.

Equivalently, if `r=rank(D)` and `chi_M` is the represented matroid's
characteristic polynomial,

`P(FP)=1-chi_M(2^b)/2^(br)`.

This is the Crapo–Rota Critical Theorem specialized to binary linear hashing.
Its established status is explicit in the introduction of the primary research
article [Alfarano and Byrne, 2025 version](https://arxiv.org/html/2305.07567v3).
The elementary rank proof above is sufficient for this application; there is
no reason to build a new matroid solver for the proposed planner.

The safe simple bound is `min(1,|D|2^-b)`, with a `bw`-bit matrix seed that must
be counted. Distinct differences need not yield mutually independent collision
events. For `D={u,v,u+v}` with independent `u,v`, each pair is independent but

`P(FP)=3p-2p^2`, `p=2^-b`,

whereas the invalid independent estimate is `3p-3p^2+p^3`. The former is larger.
At `b=1` the true rate is one and the independent estimate is `7/8`. This is
realized by the disjoint rows `A={0}`, `B={u,v,u+v}`.

More generally, conditioning on observed `H|_W=T` changes the collision law.
For `V=span(S)`, the event that `H` vanishes on `S` has conditional probability
zero if `T` does not vanish on `W intersect V`; otherwise it is

`2^[-b(dim(W+V)-dim(W))]`.

This follows by counting linear extensions of `T`; it is not a new conditioning
theorem. It shows exactly why newly chosen differences in the observed span
can have deterministic collision outcomes.

A concrete seed-selection failure is especially relevant. For one-bit hashes,
accept a construction only if `H(u)!=0` and `H(v)!=0`. Then `H(u+v)=0` with
conditional probability one, although its unconditional collision probability
is `1/2`. This acceptance rule is realized by demanding injective fingerprints
within two stored rows `{0,u}` and `{0,v}`. A later fixed pair `{0}` and `{u+v}`
then always falsely intersects. Universal-hash collision guarantees cannot be
silently carried through this construction conditioning.

If a seed is accepted exactly when no difference in a set `C` collides, the
conditional query probability, when acceptance has positive probability, is

`1-P(avoid(C union D))/P(avoid(C))`.

Each avoidance probability has the characteristic-polynomial expression above.
The accepted law generally is not the original uniform-seed law.

## 6. Aliases, repeated operands, and adaptive requests

Source identity must be resolved before using any theorem. An exact membership
constraint does not prohibit a false positive, so exact functional rows do not
make their approximate membership outputs mutually exclusive.

* If every `A_i` aliases `B_i`, a negative exact query forces all canonical bits
  to be false. At `k=3`, `alpha=1/2`, its error is `7/8`, larger than the unaliased
  functional formula `13/16`. Deduplicating only repeated witnesses misses this
  within-witness problem.
* Repeating the same row in the finite-fingerprint query reduces two tests to
  one collision event. Its per-candidate rate is `q`, not `q^2`. Canonical row
  identity must therefore be part of the type/precondition, not a comment.
* Repeating an already answered query reads the same frozen realization. If a
  query was observed to be a false positive, its next conditional false-positive
  probability is one. Repetition supplies no new independent trial.
* When `b<w`, every public binary-linear hash has a nonzero kernel vector. If
  data or queried values may be selected after observing `H`, choosing a
  difference in that kernel gives a certain collision. Fixed-query construction
  averages do not survive arbitrary adaptivity.
* A fixed finite workload admits a workload union bound over its fixed negative
  queries. This can cover an adaptive choice among those predefined queries via
  the event that any one is wrong. It is a workload-wide guarantee, not a fresh
  per-query error bound after arbitrary observations.

## 7. Verification and remaining limits

`theory_checks.py` uses independent exact-rational enumeration, including actual
source-noise assignments for small cases. The recorded successful run checked:

* 216 homogeneous multiway parameter cases across 19,502 negative profiles;
* 384 comparisons with an independent source-noise enumeration;
* 1,100 heterogeneous dynamic-program cases and 100 linear-time one-hot cases;
* 327 binary-linear rank/inclusion–exclusion cases against all finite matrices;
* all 625 four-point images of cubic polynomials over `F_5`;
* 240 fixed negative restricted queries by exhausting all 2,401 cubics over
  `F_7`, with four modulo output widths;
* the alias, linear-triangle, and post-selection counterexamples, and the exact
  `P=2^61-1` modulo-collision identity at six output widths.

Results are in `theory_checks_results.json`. These finite checks support the
implementation of the formulas; the proofs establish the general statements.
They do not establish an original contribution, an adaptive guarantee, or
performance on a realistic workload. No manuscript or package code was changed
by this theory audit.

Commands actually run from the repository root:

```bash
python .research/query-contract-planner/theory_checks.py
bernoulli-py/.venv/bin/ruff check .research/query-contract-planner/theory_checks.py
bernoulli-py/.venv/bin/python -m coverage run --data-file=/tmp/bernoulli-query-theory.coverage --branch --include='*/query-contract-planner/theory_checks.py' .research/query-contract-planner/theory_checks.py
bernoulli-py/.venv/bin/python -m coverage json --data-file=/tmp/bernoulli-query-theory.coverage -o .research/query-contract-planner/theory_coverage.json
bernoulli-py/.venv/bin/python -m coverage report --data-file=/tmp/bernoulli-query-theory.coverage --show-missing
```

All 188 executable statements were covered. The sole missing branch is the
false arm of the script's `if __name__ == '__main__'` guard; no mathematical
branch was left uncovered. The coverage report has 84 branches and reports 99%
combined coverage. Lint passed. This audit did not rerun the unrelated Python
package suite, since it changed no package or manuscript source.
