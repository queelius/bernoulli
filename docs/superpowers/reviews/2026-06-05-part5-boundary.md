# Review: Part V (The Boundary and Beyond), ch16-18

**Date:** 2026-06-05
**Scope:** `part5-boundary`: ch16 (Approximate but Not Bernoulli), ch17 (Cipher Maps and Trapdoor Computing), ch18 (Encrypted Search)
**Build state at review:** clean, 248 pages, zero undefined references.
**Auditors:** spec, quality (cold-read), math, cross-ref, dispatched in parallel.

## Verdict

**NEEDS CORRECTION (one HIGH, one MEDIUM); otherwise strong.** All ten of the conversion's flagged correctness fixes were independently re-verified and confirmed; cross-references and chapter structure are clean. The review surfaced one genuine HIGH math error introduced during the conversion (`rem:composition-jensen`) and one MEDIUM expository error inherited from the textbook draft (§17.3 leakage rate), plus minor LOW polish.

## HIGH

**H1. `rem:composition-jensen` (ch16 §16.2, `varying-rates.tex:69-82`) is mathematically false.**
The remark claims that for *independent* stage rates $\eta_i$ with means $\mu_i$, plugging the means into the serial composition formula *under*-estimates the expected combined error, by Jensen on $-\log(1-x)$, with a nonzero gap ("a fraction of a percentage point" at five stages, $\mu=0.1$, $\sigma=0.02$). This is wrong. For **independent** $\eta_i$, $\mathbb{E}[\prod(1-\eta_i)] = \prod\mathbb{E}[1-\eta_i] = \prod(1-\mu_i)$ *exactly*, so $\mathbb{E}[1-\prod(1-\eta_i)] = 1-\prod(1-\mu_i)$ exactly: the gap is *identically zero* (math-auditor's Monte-Carlo: simulated 0.409512 vs deterministic 0.409510, gap $2\times10^{-6}$, i.e. sampling noise). The Jensen step is misapplied, since convexity of $-\log(1-x)$ bounds $\mathbb{E}[\log\prod(1-\eta_i)]$, which does not transfer to $\mathbb{E}[\prod(1-\eta_i)]$. A genuine directional bias requires *correlated* stages, exactly what `rem:composition-correlation-bracket` (§16.3) already handles, with the opposite sign for positive correlation. **Disposition: rewrite to the correct statement** (independent random rates leave composition unbiased in expectation; bias requires correlation).

## MEDIUM

**M1. §17.3 adaptive-adversary leakage rate (`trapdoor-paradigm.tex:124-131`) does not follow.**
"Either way the adversary extracts $O(\log N)$ bits of plaintext per query" is not supported by either mechanism described: seed-probing extracts about 1 bit/query ($O(1)$), and record-localization takes $\log N$ queries to localize one record ($O(1)$/query, or $O(\log N)$ *total*). The $\log N$ factor is the *number of queries to localize*, mis-promoted to *bits per query*. This is the section's security punchline (worst-case vs average-case gap), so a peer will try and fail to reproduce the rate. **Disposition: correct the rate.** Per-query extraction is $O(1)$; the real gap is that a bounded budget of $O(\log N)$ crafted queries breaks the scheme outright, where the iid attacker gains only $O(\varepsilon)$ bits/query and never recovers the seed. (Inherited from the textbook draft; the conversion preserved it while fixing the adjacent $n$/$N$ notation collision.)

## LOW

| # | Location | Finding | Disposition |
|---|----------|---------|-------------|
| L1 | §18.4 `adversarial-estimation.tex:97-99` | Displayed formula $0.09\pm1.96\sqrt{\cdots}$ is the **Wald** interval, labelled "Wilson." Number is fine to rounding. | Relabel to normal-approximation (Wald). |
| L2 | §18.4 `adversarial-estimation.tex:104-107` | Clopper-Pearson upper limit for $(n{=}6,x{=}3)$ at $\delta{=}5{\times}10^{-5}$ is about 0.986, not "roughly 0.95." Unused downstream ($C\approx0.001$ holds either way). | Tighten to about 0.99. |
| L3 | §17.2 `bernoulli-error-model.tex:8` (header comment) | Stale slug `sec:noisy-bit` lingers in the `% Cross-refs` comment (prose body correctly uses `sec:quantifying-noise`). Inert; no compiled-output effect. | Update comment for consistency. |
| L4 | §16.2 `varying-rates.tex:124-135` | Chernoff uses mean 250, Azuma uses 230, without a clause reconciling them. | Add a half-sentence (the 250 is the misspecified mean). |
| L5 | §17.4 `fhe-sidebar.tex:96`; misc | "exploits" (resource-use sense) borderline against the soul-voice use/exploit rule; a couple of >40-word sentences at the edge of parseability. | Optional; left as register-consistent. |

## Confirmations (no action)

- **Math:** all ten flagged fixes re-derived and confirmed exact (the $k^\*$/Bloom numbers, $0.518^7\approx0.010$, $(1-e^{-0.6})^3\approx0.092$, the three-region intersection rate and its cancellation-into-the-interior corollary, the conjunction $\le\varepsilon$ bound, every PPV/$C$ worked example, the $\sqrt{2\ln(K/\delta)}\approx5.4$ widening, the toy-trace numbers). Regression check PASS: none of the known-wrong ch5 values reappear, and the serial-vs-matrix composition identity holds for all rates.
- **Cross-ref:** PASS. Zero undefined refs, zero label collisions (309 distinct labels, each defined once), all 75 distinct Part V reference targets resolve. The three ch6 cross-refs added to §17.5/§18.2 (`prop:intersection-fpr-fnr`, `eq:intersection-fpr`, `prop:complement-axis-swap`/`sec:union-of-sets`) all exist. The `sec:noisy-bit` to `sec:quantifying-noise` repoint is complete and semantically correct; the two residual occurrences are inert header comments.
- **Spec:** PASS. All three wrappers strip the objectives box and the exercises input cleanly; all 22 sections present and ordered; every substantive environment (defs, theorems, propositions, the four salvaged remarks) survives and is well-formed; all `exercises.tex` deleted; DEFINED header blocks match actual labels (except the L3 comment nit).
- **Quality:** the three trickiest reframes, §16.3 (shared randomness is not correlation), §17.5 (three-region intersection plus cancellation-into-the-interior), and §18.2 (conjunction $\le\varepsilon$), all "land cleanly," and §18.6 "Closing the Book" reads as a satisfying close to the monograph with accurate chapter attributions.
