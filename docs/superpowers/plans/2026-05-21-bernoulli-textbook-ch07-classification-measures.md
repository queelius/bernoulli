# Bernoulli Textbook Chapter 7: Classification Measures (Plan 7)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 7 of Part II (~28 pp): the proper statistical treatment of approximate-set quality measures (PPV, NPV, recall, F1) as functions of $\fprate, \fnrate$, and workload prevalence, with the binomial estimator and its confidence intervals (Wald, Wilson, Clopper-Pearson, Jeffreys). Chapter 7 retires the chapter 1 §1.4 deferral on "proper CI treatment" and gives the reader the tools to estimate any of these quantities from samples with honest uncertainty.

**Architecture:** Replace `book/chapters/ch07-classification-measures.tex` stub with a fully drafted chapter containing 6 sections, a learning-outcomes opener, 10-12 exercises, supporting bibliographic entries, and a paired Python notebook (`python/notebooks/ch07-classification-measures.ipynb`) that demonstrates PPV/NPV/F1 as random variables, delta-method CIs, and the Wald-vs-Wilson-vs-Clopper-Pearson comparison on the §1.4 sawtooth example.

**Tech Stack:** LaTeX (book class), alex.sty notation, biblatex+biber. Python 3.11+ + numpy + scipy + matplotlib for the notebook (scipy provides exact binomial CIs and Wilson; we may import scipy.stats specifically).

**Scope:** Chapter 7 only. Part II integration check deferred to Plan 8.

**Spec source of truth:** `docs/superpowers/specs/2026-05-17-bernoulli-textbook-part2-design.md` §3.3 (chapter 7 double duty) and §4 (chapter 7 row).

**Base SHA:** `97862d8` (HEAD at end of Plan 6).

**Source material:**
- `papers/bernoulli_classification_measures/sections/preliminaries.tex` (binomial estimator properties)
- `papers/bernoulli_classification_measures/sections/measures.tex` (PPV, NPV, F1 as random variables; delta method)
- `papers/bernoulli_classification_measures/sections/appendix.tex` (variance forms)
- `book/chapters/ch01/sampling-rates.tex` (§1.4; the deferral being retired)
- `book/chapters/ch01/quantifying-noise.tex` (§1.2; the precision/recall cross-walk)

**Lessons inherited from Plans 1-6:**

1. **Page discipline.** Chapter 7 target ~28pp; expect 30-36pp realistic. The chapter has substantial math (estimator theory, three CI methods, delta method). Hold sections to lower-end word counts; the math density justifies tight prose.

2. **Soul-voice hook (BLOCKING):** Respect the full banned-phrase list from `$CLAUDE_PLUGIN_ROOT/hooks/check-banned-phrases.sh`, including (but not limited to) Unicode em-dash U+2014, the lever-age word, the "buzzword spanning two crossroad terms" pattern, and a few other buzzword phrases the hook enforces. The hook does substring matching, so watch for accidental joins like the substring formed by "th." + ".the intersection of" across word boundaries; prefer "intersecting" or rephrase when set intersection appears next to a word ending in "t".

3. **Notation:** alex.sty macros throughout. New macros for this chapter: precision, recall, F1, PPV, NPV. Check alex.sty in Task 0; add `\providecommand` blocks to `preamble.tex` for any missing names.

4. **The §1.4 deferral retirement is the chapter's central pedagogical promise.** §1.4 said "the full treatment of estimation lives in chapter 7"; §7.1 + §7.2 + §7.3 must deliver. Cross-reference §1.4 explicitly so the reader sees the loop close.

5. **Cross-set independence vs Axiom 1:** chapter 6 §6.1's reviewer noted that cross-set independence is logically distinct from Axiom 1 (within-set element independence). Chapter 7 uses the same kind of cross-source independence when PPV/NPV are estimated on a workload with random prevalence; mention it once where it matters and move on.

6. **Numerical accuracy:** chapter 7 has many concrete examples (CI coverage tables, PPV vs prevalence curves, etc.). Reviewers should be prompted to verify arithmetic.

---

## File Structure

After this plan completes:

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch07-classification-measures.tex     # rewritten from stub
│   │   └── ch07/                                # NEW directory
│   │       ├── setup-revisited.tex              # §7.1 (~3 pp)
│   │       ├── binomial-estimator.tex           # §7.2 (~5 pp)
│   │       ├── confidence-intervals.tex         # §7.3 (~5 pp)
│   │       ├── derived-measures.tex             # §7.4 (~7 pp)
│   │       ├── bloom-diagnostics.tex            # §7.5 (~3 pp)
│   │       ├── bibliographic-notes.tex          # §7.6 (~2 pp)
│   │       └── exercises.tex                    # 10-12 exercises (~2 pp)
│   ├── preamble.tex                             # may be extended with PPV/NPV/F1 macros
│   └── references.bib                           # may be extended (Pepe, Wilson, etc.)
└── python/
    └── notebooks/
        └── ch07-classification-measures.ipynb   # PPV/NPV/F1 + CI comparison
```

---

## Cross-Reference Map (Plan 7 closing inventory)

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:classification-measures` | `ch07-classification-measures.tex` (already in Plan 0 stub) | chapter 6 §6.5 forward; chapter 1 §1.4 forward |
| `sec:setup-revisited` | `ch07/setup-revisited.tex` (Task 2) | chapter 1 §1.4 backward |
| `sec:binomial-estimator` | `ch07/binomial-estimator.tex` (Task 3) | (internal) |
| `sec:confidence-intervals` | `ch07/confidence-intervals.tex` (Task 4) | chapter 1 §1.4 notebook backward |
| `sec:derived-measures` | `ch07/derived-measures.tex` (Task 5) | (internal); ch 14/15 backward |
| `sec:bloom-diagnostics` | `ch07/bloom-diagnostics.tex` (Task 6) | (internal) |
| `sec:ch7-what-comes-next` | none separate; closing folded into §7.5 or §7.6 (Plan 7 omits a separate §7.5 What Comes Next; the trajectory preview is in chapter 5 §5.5 and chapter 6 §6.5) |

Backward references (all resolve):
- Chapter 1: `\Cref{sec:sampling-rates}` (the deferral being retired), `\Cref{sec:quantifying-noise}` (FPR/FNR + precision/recall cross-walk)
- Chapter 5: `\Cref{ch:approximate-sets}`, `\Cref{def:bloom-filter}`, `\Cref{sec:bloom-from-scratch}`, `\Cref{thm:bloom-optimal-k}`, `\Cref{def:one-sided}`
- Chapter 6: `\Cref{ch:set-composition}`, `\Cref{prop:union-fpr-fnr}` if needed
- Chapter 3: `\Cref{thm:composition}` if needed

Forward references via `\Cref{ch:N}`: chapters 14, 15 (chapter-level Plan 0 stubs exist).

---

## Per-Task Drafting Discipline

Standard Path A pattern:

1. Read paper source(s) + prior chapter sections.
2. Draft to page-length target + content checklist + notation requirements.
3. Verify cross-references.
4. Build (`cd book && make cleanall && make`, exit 0).
5. Self-review.
6. Commit with HEREDOC message.

Per-task review cycle: spec-compliance reviewer + quality reviewer (or combined for shorter sections), then fix subagent if substantive issues surface.

---

## Tasks

### Task 0: Verify macro coverage

**Purpose:** Confirm alex.sty has (or doesn't have) macros for PPV, NPV, F1, precision, recall, prevalence. If missing, extend `book/preamble.tex` with `\providecommand` blocks.

- [ ] Grep alex.sty:
```bash
grep -nE "PPV|NPV|precision|recall|F[ _]?1|prevalence" book/alex.sty
```

- [ ] If any are missing, extend `book/preamble.tex` with names like:
```latex
% Classification-measure macros for Part II chapter 7.
\providecommand{\PPV}{\mathrm{PPV}}
\providecommand{\NPV}{\mathrm{NPV}}
\providecommand{\Precision}{\mathrm{precision}}
\providecommand{\Recall}{\mathrm{recall}}
\providecommand{\Fone}{F_1}
\providecommand{\Prevalence}{\pi}
```

(Use whatever names match what alex.sty provides where possible. The Greek symbol $\pi$ for prevalence is conventional in epidemiology; check it doesn't clash with $\pi$ for the mathematical constant in chapter 7's prose.)

- [ ] Build to verify (`cd book && make cleanall && make`, exit 0).

- [ ] Commit IF preamble was modified; otherwise skip:

```
book: extend preamble with classification-measure macros for chapter 7

Add \providecommand blocks for PPV, NPV, precision, recall, F1,
prevalence as chapter 7 will use them. alex.sty is shared with the
papers and not modified.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 1: Read sources and write chapter scaffolding

**Files:** Modify `book/chapters/ch07-classification-measures.tex`; create `book/chapters/ch07/` + 7 placeholders.

**Source reading:**
- `papers/bernoulli_classification_measures/sections/preliminaries.tex` and `measures.tex` and `appendix.tex`
- `book/chapters/ch01/sampling-rates.tex` (the deferral being retired)
- `book/chapters/ch01/quantifying-noise.tex` (the precision/recall cross-walk)
- Part II spec §3.3 and §4 chapter 7 row.

- [ ] Read sources end-to-end.

- [ ] Replace `book/chapters/ch07-classification-measures.tex` with the scaffold:

```latex
\chapter{Classification Measures}
\label{ch:classification-measures}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Define PPV, NPV, recall, and F1 as functions of $\fprate$,
    $\fnrate$, and workload prevalence; recognize the
    prevalence-dependence of precision and the
    prevalence-independence of $\fprate, \fnrate$.
  \item Estimate any of these quantities from samples with
    proper confidence intervals (Wald, Wilson, Clopper-Pearson,
    Jeffreys); apply the delta method to derived measures.
  \item Apply the framework to Bloom filter diagnostics: given an
    observed false-positive count on a workload, recover a CI for
    the underlying $\fprate$ and use it to bound PPV at the
    workload's prevalence.
\end{itemize}
\end{quote}

% Section 7.1
\input{chapters/ch07/setup-revisited}

% Section 7.2
\input{chapters/ch07/binomial-estimator}

% Section 7.3
\input{chapters/ch07/confidence-intervals}

% Section 7.4
\input{chapters/ch07/derived-measures}

% Section 7.5
\input{chapters/ch07/bloom-diagnostics}

% Section 7.6
\input{chapters/ch07/bibliographic-notes}

% Exercises
\input{chapters/ch07/exercises}
```

- [ ] Create `book/chapters/ch07/` and 7 placeholder files: `setup-revisited.tex`, `binomial-estimator.tex`, `confidence-intervals.tex`, `derived-measures.tex`, `bloom-diagnostics.tex`, `bibliographic-notes.tex`, `exercises.tex`. Each contains `% Placeholder. Drafted in Plan 7 Task N.` with N substituted (2, 3, 4, 5, 6, 7, 8).

- [ ] Build (exit 0).

- [ ] Commit:

```
book: scaffold chapter 7 (classification measures) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener (three bullets: define PPV/NPV/recall/F1, estimate with proper
CIs, apply to Bloom diagnostics), six section subfile inputs plus
exercises, with matching empty placeholders. Section drafts land in
subsequent Plan 7 tasks.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §7.1 The §1.4 Setup Revisited (~3 pp)

**Files:** Modify `book/chapters/ch07/setup-revisited.tex`.

**Source reading:**
- `book/chapters/ch01/sampling-rates.tex` (the §1.4 setup)
- `book/chapters/ch01/quantifying-noise.tex` (the precision/recall cross-walk)
- `papers/bernoulli_classification_measures/sections/preliminaries.tex` (binomial setup)

**Purpose:** Short recap of §1.4 that opens the chapter. Brings the §1.4 setup into Part II's cleaner notation (after chapter 5's predicate framing). The reader is told explicitly: this is where the §1.4 deferral starts getting retired.

**Content checklist (4 items):**

1. **Recall the §1.4 setup.** Cross-reference `\Cref{sec:sampling-rates}` explicitly. The setup: an approximate set $\tilde A$ with unknown rates $\fprate, \fnrate$; observe $n$ samples (workload of queries); estimate from data. One paragraph.

2. **What §1.4 left deferred.** State the four open items: (i) prove the binomial estimator is unbiased and derive its variance; (ii) derive proper confidence intervals (not just Wald); (iii) handle the known sawtooth under-coverage near boundaries; (iv) extend to derived measures (PPV, NPV, F1). One paragraph each item; half a page total.

3. **The chapter's roadmap.** §7.2 retires (i). §7.3 retires (ii) and (iii). §7.4 retires (iv). §7.5 applies the toolkit to Bloom filters. One paragraph.

4. **Notation refresh.** Recap the alex.sty macros for $\fprate, \fnrate, \hat{\fprate}, \hat{\fnrate}, n_0, n_1, z_{\alpha/2}$. Light; one paragraph.

**Labels:** `\section{The Setup Revisited}` with `\label{sec:setup-revisited}`.

**Header cross-reference block** matching chapter 5/6 style:
- DEFINED: `\label{sec:setup-revisited}`
- RESOLVED (ch1): `\Cref{sec:sampling-rates}`, `\Cref{sec:quantifying-noise}`
- FORWARD within ch7: `\Cref{sec:binomial-estimator}`, `\Cref{sec:confidence-intervals}`, `\Cref{sec:derived-measures}`, `\Cref{sec:bloom-diagnostics}`

**Target length:** ~3 pp (700-900 prose words).

**Workflow:** Standard task pattern. Commit:

```
book: draft chapter 7.1 The Setup Revisited (~3 pp)

Recap chapter 1 §1.4's binomial-estimator and CI setup in Part II's
cleaner notation, naming the four items §1.4 deferred (estimator
properties, proper CIs, sawtooth under-coverage, derived measures)
and which chapter-7 section retires each. Short notation refresh.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 3: §7.2 The Binomial Estimator: Properties (~5 pp)

**Files:** Modify `book/chapters/ch07/binomial-estimator.tex`.

**Source reading:**
- `papers/bernoulli_classification_measures/sections/preliminaries.tex`
- `book/chapters/ch01/sampling-rates.tex`

**Purpose:** Retire item (i) of the §1.4 deferral: prove the binomial estimator is unbiased, derive its variance, identify it as MLE.

**Content checklist (5 items):**

1. **Setup.** $n_0$ samples with truth $\bot$, $\mathrm{FP}$ count is $\mathrm{Binomial}(n_0, \fprate)$. Estimator $\hat{\fprate} = \mathrm{FP}/n_0$. One paragraph.

2. **Unbiasedness.** $E[\hat{\fprate}] = \fprate$. One-line proof via linearity of expectation. Proposition with `\label{prop:binomial-unbiased}`. One paragraph.

3. **Variance.** $\Var[\hat{\fprate}] = \fprate(1 - \fprate)/n_0$. Proof via $\Var[\mathrm{Binomial}(n, p)] = np(1-p)$. State as proposition `\label{prop:binomial-variance}`. One paragraph + proof.

4. **MLE.** The likelihood is $\binom{n_0}{\mathrm{FP}} \fprate^{\mathrm{FP}}(1-\fprate)^{n_0 - \mathrm{FP}}$. Taking $\partial \log L / \partial \fprate = 0$ gives $\hat{\fprate}_{\mathrm{MLE}} = \mathrm{FP}/n_0$, same as the moment estimator. State as proposition `\label{prop:binomial-mle}`. One paragraph + derivation.

5. **CRLB and efficiency.** The Cramer-Rao lower bound for this estimator is $\fprate(1-\fprate)/n_0$, the same as the variance. So $\hat{\fprate}$ achieves the CRLB and is efficient. State as proposition with `\label{prop:binomial-efficiency}`. One paragraph. Note: the CRLB derivation needs the Fisher information $I(\fprate) = n_0 / (\fprate(1-\fprate))$; show this briefly (one paragraph).

6. **Closing.** The estimator is unbiased, MLE, and efficient. The deferral from §1.4 on these properties is now retired. §7.3 takes up the CI question. One paragraph.

**Labels:** `\section{The Binomial Estimator: Properties}` with `\label{sec:binomial-estimator}`. Propositions: `\label{prop:binomial-unbiased}`, `\label{prop:binomial-variance}`, `\label{prop:binomial-mle}`, `\label{prop:binomial-efficiency}`.

**Header cross-reference block.**

**Target length:** ~5 pp (1100-1400 prose words). Math-dense; allow up to ~1700 if proofs are tight but complete.

**Workflow:** Standard. Commit:

```
book: draft chapter 7.2 The Binomial Estimator: Properties (~5 pp)

Retire item (i) of the chapter 1 §1.4 deferral: prove the binomial
estimator hat_eps = FP/n_0 is unbiased, derive its variance
eps(1-eps)/n_0, show it equals the MLE, and confirm it achieves the
Cramer-Rao lower bound (Fisher information = n_0 / [eps(1-eps)]).
Four propositions with proofs.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 4: §7.3 Confidence Intervals Properly (~5 pp)

**Files:** Modify `book/chapters/ch07/confidence-intervals.tex`.

**Source reading:**
- `papers/bernoulli_classification_measures/sections/appendix.tex` (variance forms)
- `book/chapters/ch01/sampling-rates.tex` (Wald CI from §1.4)
- The chapter 1 notebook ran the Wald sawtooth experiment; reference for context but do not depend on.

**Purpose:** Retire items (ii) and (iii) of the §1.4 deferral. Present Wald, Wilson, Clopper-Pearson, Jeffreys CIs; explain the sawtooth coverage failure at small $n_0$ near the boundary; recommend Wilson or Jeffreys as default replacements for Wald.

**Content checklist (5 items):**

1. **The Wald CI recap.** $\hat{\fprate} \pm z_{\alpha/2}\sqrt{\hat{\fprate}(1-\hat{\fprate})/n_0}$. From §1.4. One paragraph + the formula.

2. **The under-coverage problem.** For small $n_0$ or $\fprate$ near 0 or 1, the Wald CI under-covers (coverage drops below $1 - \alpha$). Specifically: at $\fprate$ near 0, the CI can extend below 0 (impossible) AND the Normal approximation breaks down (the binomial is right-skewed). The chapter 1 notebook empirically showed this with $\sim 0.92$ coverage at $n_0 = 100, \fprate = 0.05$. Half a page.

3. **The Wilson interval.** Define: $\hat{\fprate}_{\mathrm{Wilson}} = (\hat{\fprate} + z^2/(2n_0)) / (1 + z^2/n_0)$ with half-width derivation. State the formula and justify it intuitively (it's the CI for the score statistic, not the moment estimator). Half a page.

4. **The Clopper-Pearson interval.** "Exact" interval via inverting the binomial CDF. Lower endpoint $L$ s.t. $\Pr[\mathrm{Binomial}(n_0, L) \ge \mathrm{FP}] = \alpha/2$. Numerically conservative (guarantees coverage $\ge 1 - \alpha$ but often over-covers). Half a page.

5. **The Jeffreys interval.** Bayesian credible interval under the Jeffreys prior $\mathrm{Beta}(1/2, 1/2)$. Posterior is $\mathrm{Beta}(\mathrm{FP} + 1/2, n_0 - \mathrm{FP} + 1/2)$; the interval is the quantile interval of this posterior. Half a page.

6. **Comparison table.** A small table comparing Wald, Wilson, Clopper-Pearson, Jeffreys on: (i) coverage at $n_0 = 100, \fprate = 0.05$; (ii) coverage at $n_0 = 1000, \fprate = 0.05$; (iii) symmetry about $\hat{\fprate}$; (iv) computation cost. Half a page.

7. **Recommendation.** Wilson is the default for most applications (good balance of coverage and width); Jeffreys is a Bayesian alternative; Clopper-Pearson is the conservative-safe option; Wald is acceptable only at large $n_0$ and $\fprate$ away from boundaries. One paragraph.

**Labels:** `\section{Confidence Intervals Properly}` with `\label{sec:confidence-intervals}`. Definitions and propositions for each interval (`\label{def:wald-ci}`, `\label{def:wilson-ci}`, `\label{def:clopper-pearson-ci}`, `\label{def:jeffreys-ci}`).

**Header cross-reference block.**

**Target length:** ~5 pp (1100-1500 prose words; the four intervals + table justify slight overshoot).

**Workflow:** Standard. Commit:

```
book: draft chapter 7.3 Confidence Intervals Properly (~5 pp)

Retire items (ii) and (iii) of the chapter 1 §1.4 deferral. Wald
recap, the sawtooth under-coverage at small n_0 near boundaries
(empirically observed in the §1.4 notebook), then Wilson,
Clopper-Pearson, and Jeffreys intervals with derivations and a small
coverage comparison table. Recommendation: Wilson as default,
Jeffreys for Bayesian users, Clopper-Pearson for safety-conservative
applications, Wald only at large n_0 away from boundaries.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 5: §7.4 Derived Measures: PPV, NPV, F1 (~7 pp)

**Files:** Modify `book/chapters/ch07/derived-measures.tex`.

**Source reading:**
- `papers/bernoulli_classification_measures/sections/measures.tex`
- `papers/bernoulli_classification_measures/sections/appendix.tex`
- `book/chapters/ch01/quantifying-noise.tex` (precision/recall cross-walk from §1.2)

**Purpose:** Define PPV, NPV, recall, F1 as functions of $\fprate, \fnrate, \pi$ (prevalence). Derive each as a random variable when estimated from samples. Apply the delta method for variance and CIs. Land the prevalence-dependence of precision/PPV as the central caveat.

**Content checklist (7 items):**

1. **Definitions in terms of $\fprate, \fnrate, \pi$.** $\pi = \Pr[X = \top]$ is the prevalence. Then:
   - $\Recall = \tprate = 1 - \fnrate$ (recall is prevalence-independent).
   - $\PPV = \Precision = \pi(1-\fnrate) / [\pi(1-\fnrate) + (1-\pi)\fprate]$ (prevalence-dependent).
   - $\NPV = (1-\pi)(1-\fprate) / [(1-\pi)(1-\fprate) + \pi \fnrate]$ (prevalence-dependent).
   - $\Fone = 2 \Precision \cdot \Recall / (\Precision + \Recall)$. One page.

2. **Prevalence dependence.** Plot or describe PPV as a function of $\pi$ for fixed $\fprate, \fnrate$: at $\pi \to 0$, PPV $\to 0$ (all positives are false); at $\pi \to 1$, PPV $\to 1$ (almost no negatives to be false-positive about). This is the central caveat: $(\fprate, \fnrate)$ is intrinsic to the classifier; precision is intrinsic to the classifier + workload. Half a page.

3. **PPV from samples.** $\widehat{\PPV} = \mathrm{TP}/(\mathrm{TP} + \mathrm{FP})$. Derive as a ratio of two binomial counts; not unbiased in general. Half a page.

4. **Delta method for derived-measure variance.** Stated theorem: if $\hat\theta$ is asymptotically Normal with variance $\sigma^2(\theta)/n$, and $g$ is differentiable, then $g(\hat\theta)$ is asymptotically Normal with variance $[g'(\theta)]^2 \sigma^2(\theta)/n$. State the theorem (no proof; cite Casella-Berger or DasGupta) and apply to PPV: derive $\Var[\widehat{\PPV}]$ as a function of $\fprate, \fnrate, \pi, n$. One page.

5. **Delta-method CI for PPV.** Wald-style CI: $\widehat{\PPV} \pm z_{\alpha/2} \sqrt{\widehat{\Var[\widehat{\PPV}]}}$. Half a page.

6. **F1 derivation.** Apply delta method to $\Fone$ similarly. Worked example with $\fprate = 0.05, \fnrate = 0.10, \pi = 0.1, n = 1000$: compute $\Fone$, its variance, and a 95% CI. One page.

7. **Bloom filter PPV under workload.** Tie back to §5.2: a Bloom filter with $\fprate = 0.01, \fnrate = 0$ on a workload with $\pi = 0.01$ has $\PPV = 0.01 \cdot 1 / [0.01 + 0.99 \cdot 0.01] = 0.01 / 0.0199 \approx 0.503$. About HALF of all positive reports are false positives! At $\pi = 0.5$, PPV = 0.99. Same classifier, different workload, vastly different PPV. Forward-reference §7.5 for the full Bloom filter diagnostics. Half a page.

**Labels:** `\section{Derived Measures}` with `\label{sec:derived-measures}`. Definitions and propositions (`\label{def:ppv}`, `\label{def:npv}`, `\label{thm:delta-method}`, `\label{prop:ppv-variance}`).

**Header cross-reference block.**

**Target length:** ~7 pp (1500-1900 prose words; this is the chapter's longest section).

**Workflow:** Standard. Commit:

```
book: draft chapter 7.4 Derived Measures: PPV, NPV, F1 (~7 pp)

Retire item (iv) of the chapter 1 §1.4 deferral. Definitions of PPV,
NPV, recall, F1 as functions of fpr, fnr, and prevalence pi.
Prevalence-dependence as central caveat: at the SAME classifier,
PPV varies from 0 to 1 as pi varies from 0 to 1, while fpr/fnr stay
fixed. Delta method for derived-measure variance. CI for PPV and F1.
Worked Bloom filter PPV example: at fpr = 0.01, pi = 0.01, PPV ≈ 0.50,
showing that half of all positive reports are false positives.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 6: §7.5 Worked Application: Bloom Filter Diagnostics (~3 pp)

**Files:** Modify `book/chapters/ch07/bloom-diagnostics.tex`.

**Source reading:**
- `book/chapters/ch05/bloom-from-scratch.tex` (Bloom filter context)
- Just-drafted §7.4 (the PPV / prevalence framework)

**Purpose:** Apply the full chapter-7 toolkit to a single concrete scenario: given a deployed Bloom filter with measured rates AND a workload with measured prevalence, compute PPV and a CI; identify whether the false-positive rate is the limiting factor or whether prevalence is.

**Content checklist (4 items):**

1. **Scenario.** A spam filter deployed as a Bloom filter at $m = 50000, n = 5000, k = 7$. Theoretical $\fprate \approx (1 - e^{-0.7})^7 \approx 0.0082$. Workload of $N = 10000$ messages.

2. **Empirical observation.** $\mathrm{FP} = 92$ over $n_{\bot} = 9000$ true-negative messages (the rest are true positives). Compute $\hat{\fprate} = 92/9000 \approx 0.01022$, Wilson 95% CI $\approx [0.00834, 0.01253]$.

3. **PPV computation.** Prevalence $\hat\pi = 1000/10000 = 0.1$. PPV at the point estimates: $0.1 \cdot 1 / [0.1 + 0.9 \cdot 0.01022] \approx 0.1 / 0.10920 \approx 0.916$. So ~92% of $\top$-flagged messages are actually spam. Wilson CI for PPV via delta method.

4. **Diagnostic question.** If we want PPV > 0.95, do we need to (a) reduce $\fprate$ (re-tune Bloom filter) or (b) wait for higher-prevalence regime? Compute: at $\fprate = 0.005$, PPV $\approx 0.956$. At $\pi = 0.2$, PPV $\approx 0.961$. Either fix works; choice depends on cost. Half a page.

**Labels:** `\section{Worked Application: Bloom Filter Diagnostics}` with `\label{sec:bloom-diagnostics}`.

**Header cross-reference block.**

**Target length:** ~3 pp (700-900 prose words). Concrete and concise.

**Workflow:** Standard. Commit:

```
book: draft chapter 7.5 Worked Application: Bloom Filter Diagnostics (~3 pp)

Apply the chapter 7 toolkit end-to-end on a spam-filter scenario:
m=50000, n=5000, k=7 Bloom filter, workload of 10000 messages with
prevalence 0.1. Empirical FPR with Wilson CI; PPV at the point
estimate (~0.916) with delta-method CI; diagnostic question of
whether to reduce fpr or hope for higher prevalence to reach a target
PPV.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 7: §7.6 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch07/bibliographic-notes.tex`; possibly extend `book/references.bib`.

**Content (4-5 paragraphs):**

1. **The `towell-bernoulli-classification-measures` paper** (the chapter's primary source). Add bib entry.

2. **Wilson (1927) and the Wilson interval.** Cite. Add bib entry.

3. **Clopper-Pearson (1934) "exact" interval.** Cite. Add bib entry.

4. **Pepe (2003) for medical diagnostic testing tradition** (already mentioned in chapter 1 §1.6 prose). May or may not cite here.

5. **The delta method:** standard statistical-asymptotics result. Cite Casella-Berger or DasGupta (asymptotic theory). Add bib entry if not present.

**Possible new bib entries:**

```bibtex
@misc{towell-bernoulli-classification-measures,
  author = {Alexander Towell},
  title  = {Binary classification measures for random approximate sets},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/bernoulli_classification_measures}}
}

@article{wilson-1927,
  author  = {Edwin B. Wilson},
  title   = {Probable Inference, the Law of Succession, and Statistical Inference},
  journal = {Journal of the American Statistical Association},
  volume  = {22},
  number  = {158},
  pages   = {209--212},
  year    = {1927}
}

@article{clopper-pearson-1934,
  author  = {C. J. Clopper and E. S. Pearson},
  title   = {The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial},
  journal = {Biometrika},
  volume  = {26},
  number  = {4},
  pages   = {404--413},
  year    = {1934}
}

@book{casella-berger,
  author    = {George Casella and Roger L. Berger},
  title     = {Statistical Inference},
  publisher = {Duxbury},
  edition   = {2nd},
  year      = {2002}
}
```

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline{toc}{section}{Bibliographic Notes}` + `\label{sec:bib-notes-ch7}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard. Commit:

```
book: draft chapter 7.6 Bibliographic Notes (~2 pp); extend bib

Attribute the classification-measure framework to the
towell-bernoulli-classification-measures paper (new bib entry).
Cite Wilson (1927) and Clopper-Pearson (1934) for the eponymous
intervals (new bib entries). Cite Casella-Berger for the delta
method (new bib entry).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 8: Chapter 7 Exercises (11)

**Files:** Modify `book/chapters/ch07/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Compute PPV.** Classifier with $\fprate = 0.05, \fnrate = 0.10$; workloads with $\pi \in \{0.01, 0.1, 0.5\}$. Compute PPV in each.

2. **Compute F1.** Same classifier, workload $\pi = 0.5$. Compute F1.

3. **Wilson interval evaluation.** For $\mathrm{FP} = 10$ at $n_0 = 100$, compute the Wilson 95% CI.

**Medium (★★ × 5):**

4. **Notebook-tied CI comparison.** Use `python/notebooks/ch07-classification-measures.ipynb` to compute the empirical coverage of Wald, Wilson, Clopper-Pearson, Jeffreys at $n_0 \in \{20, 100, 500\}$ and $\fprate \in \{0.01, 0.05, 0.5\}$. Identify the regime where Wald under-covers most.

5. **Delta method for log-odds.** Apply the delta method to $g(\fprate) = \log[\fprate/(1-\fprate)]$. Derive $\Var[g(\hat{\fprate})]$.

6. **Prevalence-dependence visualization.** For $\fprate = 0.01, \fnrate = 0.01$, sketch PPV and NPV as functions of $\pi \in [0, 1]$. Identify where each is minimized/maximized.

7. **Sample-size formula for PPV CI.** Given target half-width $h$ on PPV's 95% CI, derive a formula for required $n$ (assume $\pi$ known).

8. **Bloom filter PPV with uncertain prevalence.** A Bloom filter with $\fprate = 0.005, \fnrate = 0$ deployed on a workload with estimated $\hat\pi = 0.05$ from a sample of $1000$. The Wilson 95% CI for $\pi$ is approximately $[0.038, 0.066]$. Propagate this uncertainty to a CI for PPV. (Hint: PPV is a function of two random quantities now.)

**Challenging (★★★ × 3):**

9. **MLE vs method-of-moments.** Compare $\hat{\fprate}_{\mathrm{MLE}}$ to a hypothetical method-of-moments estimator based on $E[\mathrm{FP}^2]$. Show they coincide for the Bernoulli/Binomial case but differ in general (small example).

10. **Coverage of the delta-method CI.** Derive (or sketch) why the delta-method CI for $\widehat{\PPV}$ can under-cover when the prevalence $\pi$ is small. Connect to the §7.3 Wald sawtooth.

11. **F1 vs precision-recall tradeoff.** Given a target F1 = 0.9, derive the set of $(\Precision, \Recall)$ pairs achieving it. Sketch the curve in the $(\Precision, \Recall)$ plane. Argue that F1 weights precision and recall equally (the harmonic mean property).

**Workflow:** Standard. Commit:

```
book: draft chapter 7 exercises (11 with star difficulty markers)

3 warm-ups (PPV/F1/Wilson computations), 5 medium (notebook CI
comparison, delta method on log-odds, prevalence-dependence
visualization, sample-size formula, Bloom PPV with uncertain
prevalence), 3 challenging (MLE vs MOM, delta-method coverage,
F1 tradeoff curve).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 9: Chapter 7 Notebook (`ch07-classification-measures.ipynb`)

**Files:** Create `python/notebooks/ch07-classification-measures.ipynb`.

**Source reading:**
- `python/notebooks/ch01-noisy-bit.ipynb` (the Wald sawtooth experiment; chapter 7 builds on it)
- `python/notebooks/ch05-approximate-sets.ipynb` (Bloom filter context)

**Purpose:** Substantive notebook (per master spec): demonstrate PPV/NPV/F1 as random variables; compare Wald/Wilson/Clopper-Pearson/Jeffreys intervals; revisit the §1.4 sawtooth with the new intervals.

**Content checklist (~14-16 cells):**

1. **Title** (markdown).
2. **Setup** (code): imports including scipy.stats; seeded RNG.
3. **The Wald sawtooth, revisited** (code): compute exact coverage of Wald, Wilson, Clopper-Pearson, Jeffreys at $\fprate = 0.05$, varying $n_0$. Plot the four coverage curves on one axes.
4. **Discussion** (markdown): Wald oscillates and undercovers; Wilson and Jeffreys converge cleanly to 0.95; Clopper-Pearson over-covers slightly.
5. **PPV as random variable** (code): simulate 1000 datasets at $\fprate = 0.05, \fnrate = 0.1, \pi = 0.2, n = 500$. Compute empirical distribution of $\widehat{\PPV}$.
6. **Delta-method CI vs empirical** (code): for the same scenario, compute the delta-method 95% CI; empirically check coverage over 1000 simulations.
7. **Prevalence sweep** (code): plot PPV and NPV as functions of $\pi$ for fixed $\fprate = 0.01, \fnrate = 0.01$.
8. **F1 ridge** (code): plot F1 contours in the $(\Precision, \Recall)$ plane.
9. **Bloom filter diagnostic example** (code): replicate §7.5's scenario empirically. Compute PPV CI from synthetic data.
10. **Discussion / open question** (markdown): the prevalence-dependence is the diagnostic-testing community's central tension. Mention chapter 16's "negative-space" framing if applicable.

**Numerical sanity targets:**
- Wald coverage at $n_0 = 100, \fprate = 0.05$: approximately 0.92 (under-covers).
- Wilson coverage at same params: approximately 0.94-0.95.
- Clopper-Pearson coverage: ≥ 0.95 by construction.
- PPV at $\fprate = 0.01, \fnrate = 0, \pi = 0.1$: $\approx 0.92$.

**Run-to-completion:** notebook MUST execute end-to-end.

**Workflow:**

1. Read precedent notebooks.
2. Draft as valid nbformat-4 JSON.
3. Execute:
```bash
cd python && uv run jupyter nbconvert --to notebook --execute notebooks/ch07-classification-measures.ipynb --output ch07-classification-measures.ipynb 2>&1 | tail -20
```
4. Verify outputs.
5. Commit:

```
python: add chapter 7 notebook (classification measures)

Substantive notebook: Wald sawtooth revisited with Wilson,
Clopper-Pearson, Jeffreys (one plot comparing four coverage curves).
PPV as random variable: 1000-trial empirical distribution vs
delta-method CI. Prevalence sweep showing PPV/NPV variation. F1
contour plot. Bloom filter diagnostic example replicating §7.5.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

## Self-Review

Spec coverage:
- Part II spec §3.3 (chapter 7 double duty): retires the §1.4 deferral (Tasks 2, 3) AND develops PPV/NPV/F1 (Task 5). Both covered.
- Part II spec §4 chapter 7 row: each section has its own task.
- Master spec exercise discipline: Task 8.
- Master spec substantive notebook: Task 9.

Placeholder scan: none.

Type and label consistency: Labels match across this plan; chapter 1's `sec:sampling-rates` is the deferral-retiring backward reference; chapter 5's Bloom filter labels are the worked-example targets.
