# Hash construction candidate: no-go for a one-week research paper

Audited 2026-10-14. Scope: Bernoulli hash-function paper and its PHF context as
one candidate, one main claim and one nearby salvage. No canonical manuscript
or package was edited. The prior “95% complete” and “minor revision” ratings
measure draft maturity; they are not evidence of correctness or novelty.

**Decision:** useful corrected mathematics survives, but no defensible
incremental conventional-paper contribution is established within the
one-working-week ceiling. The strongest advertised adaptive saving compares
different recall guarantees. Its same-guarantee salvage is ordinary finite
random-codebook search. PHF does not supply a ready alternative contribution.

## Exact contribution hypothesis and source locations

The best existing hypothesis is that choosing the acceptance threshold from
the data creates a finite storage–accuracy–construction tradeoff beyond
standard retrieval/AMQ and seed search. The centerpiece is
`papers/bernoulli-hash-function/sections/space.tex:195`, “Price of FPR certainty”:
an adaptive encoding stores only `(N,t)` whereas a fixed-threshold seed costs
`m log2(1/epsilon) + O(1)` extra bits. The interpretation at line 266 attributes
the entire difference to certainty rather than membership information.

Supporting claims are at `sections/shf.tex:172` (rank threshold), `:205`
(every salt succeeds), `:264` (purported exact discrete law), `:295`
(continuous Beta moments), and `:121` (subset-search speedup). The introduction
at `sections/intro.tex:33` advertises the threshold generalization. The sole
nearby salvage considered here is to keep the same recall and impose an FPR
cap, or examine a finite budget of salts and select its best threshold.

All formulas below assume independently uniform residues for distinct
key/salt pairs, an injective encoding of those pairs, a fresh nonmember hash
uninspected during construction, and independent trials from distinct salts.
A real fixed-width digest reduced modulo a non-power-of-two N is not exactly
uniform without rejection sampling. No real-hash runtime claim is made.

## Positive result reproduced, and the decisive comparison

Let `m` members have iid residues in `{0,...,N-1}`, `1 <= r <= m`, and let
`T` be their r-th smallest residue. The correct exact law is

```
P(T <= j) = sum_{a=r}^m C(m,a) ((j+1)/N)^a (1-(j+1)/N)^(m-a)
P(T = j)  = P(T <= j) - P(T <= j-1).
```

**Proof:** `T <= j` iff at least r of the m independent residues are at most j.
Thus this is a binomial tail, not a sampling-without-replacement law.
`audit_hash.py` compares this law with full enumeration in all 40 cases
`N,m in {1,2,3,4}`, `r in {1,...,m}`. All agree exactly using rational numbers.
The paper's finite PMF fails already at `N=m=2,r=1`: it gives `(1,0)`;
enumeration gives `(3/4,1/4)`. The appendix at `:110` explicitly switches to
distinct residues, but the main theorem calls the result exact. Even for an
approximation the birthday scale is `m^2/N`, not merely `m/N`.

The positive continuous-limit claim is correct: with iid continuous uniform
scores, `T ~ Beta(r,m-r+1)`, recall is exactly `r/m`, and mean FPR is
`r/(m+1)`. Therefore

```
mean recall - mean FPR = r / (m(m+1)) <= 1/(m+1).
```

This is an almost nondiscriminating membership rule. At zero false negatives,
`r=m`, the mean FPR is `m/(m+1)`. At finite N it is at least that large:
couple discrete residues with `floor(N U_i)` and observe
`(max_i floor(N U_i)+1)/N >= max_i U_i`.
Conversely, targeting small mean FPR makes recall approximately that small.
The following values are exact rational sums rounded for display, not Monte
Carlo estimates:

| N | m | r | Mean recall | Mean FPR | Difference |
|---|---|---|---|---|---|
| 2 | 2 | 1 | 0.750000 | 0.625000 | 0.125000 |
| 100 | 100 | 1 | 0.015812207 | 0.015721141 | 0.000091066 |
| 100 | 100 | 100 | 1 | 0.994278859 | 0.005721141 |

Thus the plot at `space.tex:355`, labeled target FPR 0.01, does not compare
the same accuracy contract. It also relies on the continuous approximation
in a plotted regime with N=100 and m as large as 200. A data-independent hash
coin with the same mean FPR has recall equal to that FPR, illustrating the
small amount of discrimination bought by the adaptive construction. This is
a diagnostic baseline, not a claim that it matches exact finite recall.

The lower-bound explanation at `space.tex:168` is also unsound: a per-build
random FPR does not itself evade the usual randomized AMQ requirement. For
each fixed nonmember, its acceptance probability is the expectation of the
conditional FPR. The standard formulation explicitly allows a random
superset, as in [Pagh, Pagh and Rao, introduction](https://www.rasmuspagh.net/papers/bloom.pdf).
The relevant changes here are recall, attained mean FPR, and dependence.

The adaptive model also fails the paper's independent-element definition at
`prelim.tex:58`. Distinct nonmembers are independent conditional on T, but
their unconditional covariance is `Var((T+1)/N)`. In the two-key example it
is `3/64 > 0`. This is a mixture of iid laws, not the claimed iid law.

## Only nearby salvage: keep both accuracy requirements fixed

Fix an FPR cap `epsilon=(t*+1)/N` and require at least r accepted members.
Then adaptive threshold acceptance `T <= t*` is **the very same event** as
the fixed-threshold count being at least r. Its probability is

```
s = P(Binomial(m,epsilon) >= r).
E[trials to success] = 1/s.
P(success within B independent salts) = 1-(1-s)^B.
P(min_b T_b <= j) = 1-(1-P(T <= j))^B.
```

These are proved directly by the event equivalence and independent trials.
At `m=4,r=3,epsilon=1/5`, exact enumeration gives `s=17/625`, expected trials
`625/17`, and success within eight trials approximately `0.1979739114`.
At zero false negatives, `s=epsilon^m`; m=100 and epsilon=0.01 require
`10^200` expected trials. The fixed budget limits construction work by accepting
construction failures; it does not remove this tradeoff.

If Q is the first successful trial and salt length is `floor(log2 Q)`, the
paper's valid exact positive result is
`E[L]=sum_{n>=1}(1-s)^(2^n-1)`. Its leading term is `-log2(s)+O(1)`.
The general lower bound can be obtained directly from
`P(Q <= a) <= a s`, giving an O(1) bound on
`E[(log2(1/s)-log2 Q)_+]`; Jensen gives the matching upper bound.
Thus fixing the incorrect printed log moment preserves only the familiar
seed-index scale.

For `s=1/2`, the numerical sums give `E[log2 Q]=0.7326494821` and
`E[floor(log2 Q)]=0.6328430180`. `space.tex:66` instead claims 2 for the first
quantity. At the same s, the geometric entropy is exactly 2 bits, while
`space.tex:257` gives 0 because of a sign error. The numerical sum truncation
errors are below `2^-192` and `2^-1022`, respectively, before floating-point
roundoff; these are not identities inferred from decimal agreement.

**Novelty conclusion for the salvage:** this is binomial order statistics
plus geometric/random-codebook search. [Lehmann et al., ESA 2025, §1.1,
UNI and Lemma 3](https://drops.dagstuhl.de/storage/00lipics/lipics-vol351-esa2025/html/LIPIcs.ESA.2025.109/LIPIcs.ESA.2025.109.html)
explicitly analyzes one seed successful for all independent Bernoulli
constraints: near-optimal storage and exponential construction. The BHF's
zero-FN threshold case is that mechanism with per-key probability epsilon
(or epsilon times the value-matching probability). Their improved algorithm
concerns jointly encoded sequences of seeds; its improvement is not being
misapplied as a direct contradiction to a single seed's entropy. It does
show that a publishable modern construction contribution must go beyond
the baseline BHF repeats.

## Other nearest primary literature and readiness costs

The verified source ledger is `references.json`, including versions and
access limits. The main comparisons are:

| Prior work | What it already supplies; implication |
|---|---|
| [Chazelle, Kilian, Rubinfeld and Tal, SODA 2004](https://www.cs.princeton.edu/~chazelle/pubs/soda04.pdf), §3 and §3.3 | Static support maps and a validity/interval decoder for uniformly random decoded outputs, with acceptance probability determined by the valid range size. Threshold/acceptance-set decoding and the map-to-membership connection are established ideas. This is not asserted to be the identical seed-only data structure. |
| [Dietzfelbinger and Pagh, 2008](https://www.rasmuspagh.net/papers/bloomier.pdf), Observation 1 and Theorem 1 | General retrieval-to-AMQ reduction, arbitrarily near-optimal space with efficient construction/evaluation. A proof that a seed achieves the information scale does not establish a new optimal filter. |
| [Dietzfelbinger et al., JACM 2026](https://publikationen.bibliothek.kit.edu/1000191446/177619178), introduction and §5.4 | Current succinct retrieval/AMQ baseline. Homogeneous Ribbon's exact FPR is `p+(1-p)2^-r`, where p is a query row-span event; it must not be treated as ideal independent fingerprints without this exception. No speed measurements were reproduced here. |
| [Graf and Lemire, JEA 2020](https://arxiv.org/abs/1912.08258) and [JEA 2022](https://arxiv.org/abs/2201.01174) | Xor and binary fuse filters are practical comparison points beyond Bloom. Their reported results are external empirical evidence, not measurements of BHF. Abstracts and primary metadata verified; full empirical replication is outside this audit. |

The “subset enumeration eliminated” improvement is also against a needlessly
slow baseline. `shf.tex:154` already concedes equality hash-and-count uses O(m)
hash evaluations per salt; the introduction still presents an exponential
improvement. A fixed acceptance set's probability depends only on its
cardinality under uniform hashing; naming the set is not a further algorithm.
The threshold itself is deterministic when fixed in advance, so the
maximum-entropy proof's claim that t is uniform (`entropy.tex:19`) is false.
Randomly ordering equal-length seed candidates can make their labels uniform
by symmetry; that fact neither creates a new compression bound nor a privacy
theorem.

The PHF fallback requires correctness repairs before evaluating novelty.
`papers/bernoulli-phf/paper/sections/k_perfect_hashing.tex:31` conditions on
rejecting overfull bins, while `:54` applies the unconditional occupancy law.
For m=N=2,k=1, every accepted placement is injective, so loss is zero, whereas
the displayed formula gives 1/4. For k=2 and one-bit independent fingerprints,
the same 1/4 is a displacement probability, but actual membership FNR is 1/8
because equal fingerprints rescue half the displaced keys. Both results are
exhaustively enumerated in the audit. Neither repair makes standard
occupancy/fingerprinting a new research contribution. This is context for the
same candidate, not a second salvage investigated.

The adaptive-map path has additional readiness debt: `construction.tex:156`
omits the salt required at `:225`; accepted members with incorrect value
hashes can lie below the rank threshold formed only from matching keys; and
unequal value lengths produce a Poisson-binomial count, not the theorem's
binomial with success probability `2^-mean_length`. These observations do not
support a new contribution and were not expanded into a separate project.

## Evidence, remaining effort, and stopping decision

`audit_hash.py` uses exact fractions and exhaustive enumeration, with labeled
numerical geometric moments. `test_audit_hash.py` independently checks laws,
recall, event equivalence, edge cases, counterexamples, and CLI-to-JSON output.
`results.json` contains the reproducible numbers. Commands and output are in
`commands.md`, `test-output.txt`, `lint-output.txt`, and `type-output.txt`.
Final verification: 20 tests passed, branch-aware coverage 98%, Ruff clean,
strict mypy clean. The uncovered line is CLI printing, exercised by the
subprocess integration test but outside pytest's child coverage collection.
No package or manuscript changes were made, so the package suite and LaTeX
build were not run. No runtime or practical filter performance is claimed.

Effort estimate, not a guaranteed schedule: 2–4 working days could correct
and simplify the mathematical exposition and regenerate honest plots; 1–2
more could reconcile definitions, metadata, bibliography, and build. That
would yield a defensible technical/expository note. Establishing a new useful
construction or a genuine improvement over retrieval/modern seed encoders
would require new research and substantive comparative implementation, with
no supported one-week completion estimate.

**Gate result:** correctness fails for the current central presentation;
the repaired result passes elementary mathematical checks; incremental
novelty remains unestablished; the conventional-paper goal fails the effort
gate. Stop this candidate. Do not turn these repairs into a novelty claim or
start another construction under the triage budget.
