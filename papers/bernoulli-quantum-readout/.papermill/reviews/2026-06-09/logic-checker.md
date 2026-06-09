# Logic Checker, Section 3.6 focus plus regression

**Date**: 2026-06-09
**Scope**: New Subsection 3.6 (`sec:operator`, main.tex 514 to 579) for correctness; regression check on the rest of Section 3.

## Independently re-verified (exact arithmetic plus Monte Carlo)

- **eq:assignment is the transpose of eq:channel** (goal 1a): `A_i = [[1-eps,om],[eps,1-om]]` (eq:assignment, line 530 to 532) is exactly `Q^T` of eq:channel `[[1-eps,eps],[om,1-om]]`. Confirmed `A == Q^T` and `A` column-stochastic (columns sum to 1). CORRECT.
- **Eigenvalue/parity-mode claim** (line 547 to 551): for the symmetric flip channel (`eps_i=om_i=q_i`) the matrix has eigenvalues `{1, 1-2q_i}`; eigenvector `(1/2,1/2)` for eigenvalue 1 (stationary), eigenvector `(1/2,-1/2)` for `1-2q_i` (parity/difference mode). Reproduced exactly for q in {0.05,0.1,0.3}. CORRECT.
- **parity-spectral identity eq:parity-spectral** (line 558 to 562): `(1/2)(1-prod(1-2q_i))` matches a 2M-trial Monte Carlo (0.26470 formula vs 0.26460 MC). CORRECT.
- **Triple-identity (i)/(ii)/(iii)** (line 551 to 555): for the symmetric channel, `1-2q_i` simultaneously is the nontrivial eigenvalue, the plus/minus-1 bias `E[(-1)^{F_i}]=E[S_i]` with `S_i=1-2F_i`, and the Walsh-Hadamard coefficient on the parity character. All three coincide in the symmetric case. CORRECT as scoped.
- **Regression on Section 3 core**: Table 1 (symmetric, six rows) and Table 2 (asymmetric T1-biased: 0.110/0.175/0.234/0.315, symmetrized 0.226, ratio 1111/0000 = 2.866) reproduce exactly. The addition introduced no regression in the calculus or tables.

## Finding L1 (minor), asymmetric extension conflates "eigenvalue" with "flip bias"

**Location**: main.tex 569 to 571, closing sentence of the spectral paragraph.
**Quoted text**: "the asymmetric \cref{cor:parity-asym} is the same coefficient with the per-bit eigenvalue $1-2q_i$ replaced by the latent-conditioned $1-2r_i$, $r_i\in\{\eps_i,\omega_i\}$."
**Problem**: The eigenvalue/parity-mode statement is correctly scoped to the *symmetric* channel (line 547: "For the symmetric per-bit flip channel ($\eps_i=\omega_i=q_i$)"). But the closing sentence extends it to the asymmetric corollary by calling `1-2r_i` "the per-bit eigenvalue ... replaced by the latent-conditioned `1-2r_i`." That is imprecise: for the *asymmetric* assignment matrix `A_i=[[1-eps_i,om_i],[eps_i,1-om_i]]` the nontrivial eigenvalue is `1-eps_i-om_i`, NOT `1-2r_i`. Verified: (eps,om)=(0.02,0.10) gives eigenvalue 0.88, while 1-2eps=0.96 and 1-2om=0.80; (0.04,0.12) gives eigenvalue 0.84, neither side. The object `1-2r_i` is genuinely the *bias of the latent-conditioned flip indicator* `F_i` (the (ii)/(iii) reading the proof of cor:parity-asym actually rides on), which is correct, but it is not the eigenvalue of the asymmetric channel matrix. So the proof and the corollary are *correct*; only the label "the per-bit eigenvalue" applied to `1-2r_i` in the asymmetric case is wrong.
**Suggestion**: Change "the per-bit eigenvalue $1-2q_i$ replaced by the latent-conditioned $1-2r_i$" to "the per-bit **flip-channel bias** $1-2q_i$ replaced by the latent-conditioned $1-2r_i$" (or "the (ii)/(iii) bias/Walsh reading, with the eigenvalue reading exact only in the symmetric case"). The (i) eigenvalue identity holds exactly only when `eps_i=om_i`; the (ii)/(iii) bias/Walsh reading holds in the asymmetric conditioned case and is the right object for cor:parity-asym.
**Confidence**: high (arithmetic).

## Finding L2 (suggestion), "relaxation rate" loose in honesty clause

**Location**: main.tex 577 to 578.
**Quoted text**: "The eigenvalue $1-2q_i$ is a relaxation rate of a stochastic matrix, not a quantum phase."
**Problem**: `1-2q_i` is the (sub-unit) eigenvalue/contraction factor governing relaxation toward the stationary mode; a literal "rate" would be its log. Harmless in context (the clause's job, deny quantum phase, is done) but "relaxation **eigenvalue**" or "contraction factor" is more precise.
**Confidence**: high; severity cosmetic.

## Verdict
The new subsection's three load-bearing claims (transpose, eigenvalue triple-identity, parity-spectral) are all correct as scoped. One minor wording fix (L1) is warranted to avoid mislabeling the asymmetric `1-2r_i` as an eigenvalue. No correctness regression elsewhere. No critical or major logic issues.
