# Logic checker (re-review)

Date: 2026-06-07 (re-review of the same-day revision, commit 6f136b7)
Scope: verify the new asymmetric worked example (Table 2 / cor:parity-asym), the
M1 parity sign-rule logic, and check that no prior-verified result regressed.

## New content: the asymmetric worked example (M2 fix)

The new Subsection 4.4 ("The asymmetric case") and Table 2 are mathematically
exact. I recomputed all five claimed values independently from eq:parity-asym,
P(flip | t) = 1/2 (1 - prod_i (1 - 2 r_i)), with r_i = eps_i if t_i = 0 and
r_i = omega_i if t_i = 1, and the deployed channels eps = (0.02, 0.02, 0.04, 0.04),
omega = (0.10, 0.10, 0.12, 0.12):

| latent word | r vector | computed | table |
|-------------|----------|----------|-------|
| 0000 | (.02,.02,.04,.04) | 0.109979 | 0.110 OK |
| 1000 | (.10,.02,.04,.04) | 0.174982 | 0.175 OK |
| 0011 | (.02,.02,.12,.12) | 0.233842 | 0.234 OK |
| 1111 | (.10,.10,.12,.12) | 0.315168 | 0.315 OK |
| sym q=0.07 | (.07,.07,.07,.07) | 0.226496 | 0.226 OK |

All five round correctly to three decimals. The mean of the eight deployed
per-direction rates is exactly 0.07, so the "symmetrized single rate (q = rbar =
0.07)" framing is arithmetically honest.

Prose claims around the table, all verified:
- "1111 misread almost three times as often as 0000": exact ratio
  0.315168 / 0.109979 = 2.866 ("almost three"). CORRECT.
- "the three tau=0 rows span a factor of nearly three": 0.110, 0.234, 0.315;
  span 0.315/0.110 = 2.866. CORRECT.
- "single rate ... wrong on both sides at once": symmetrized 0.226 overstates
  the cold corner (0.226/0.110 = 2.05, "roughly twofold" as claimed) and
  understates the hot corner (0.226 < 0.315). CORRECT on both directions.
- The 1000 row (tau = 1) is the only odd-parity word shown; its value 0.175 sits
  between the cold and hot tau=0 corners, consistent with one relaxation-prone
  bit. CORRECT.

Latent-assignment dependence is real and correctly exhibited: the three tau=0
rows differ, which is the entire point of cor:parity-asym (the flip rate depends
on the assignment, not just the syndrome value tau). This is exactly the content
the prior review (M2) said was asserted-but-never-shown; it is now shown on
numbers.

## M1 parity sign-rule logic

sec:scope item 2 (lines 758-761) claims: positively correlated misreads make
coincident flips more likely and push the parity error BELOW the independent
value, while negatively correlated misreads push it ABOVE. I verified this on the
two-bit parity with fixed marginals r and a tunable joint p11 = P(both flip):

  P(parity flip) = P(odd number of flips) = 2r - 2 p11.

Independent: p11 = r^2 gives 2r(1-r). Positive correlation (p11 > r^2) makes
P(odd) < 2r(1-r), i.e. BELOW independent; negative correlation (p11 < r^2) makes
it ABOVE. The paper's sign assignment is therefore correct, and the underlying
reason it gives ("parity flips only under an odd number of bit flips, coincident
flips are more likely under positive correlation") is the right mechanism. The
"two-sided anchor, not a worst case" characterization follows correctly.

## Regression check on prior-verified results

- Table 1 (the symmetric linearization table) is unchanged and still exact:
  q=0.05, n=8 gives P_exact = 0.284766, rel. overestimate 40.5%; q=0.01, n=8
  gives 0.074618, 7.2%. Re-verified.
- m1 fix: thm:andor (i) now opens "Conditioned on all latent inputs being false
  (t_i = 0 for every i), its false-positive rate is prod eps_i." The FPR clause
  is now explicitly conditioned, matching the FNR clause and removing the
  corner-vs-marginal ambiguity. The corner-is-smallest claim in the proof is
  unchanged and remains correct.
- No theorem, proposition, corollary, or proof was altered in a way that breaks
  the previously verified dependency chain. prop:not, thm:andor, cor:composition,
  thm:parity, cor:parity-asym, prop:tensor all stand as before.

## New logic findings introduced by the revision

None. The new subsection and table are correct, the sign rule is correct, and no
prior result regressed.

## Verdict

All revised mathematical content is exact. M2 (asymmetric demonstration) and the
M1 sign-rule logic are correctly executed. No new logic issues.
