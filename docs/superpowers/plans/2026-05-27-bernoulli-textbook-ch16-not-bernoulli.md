# Bernoulli Textbook Chapter 16: Approximate but Not Bernoulli (Plan 16)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 16 of Part V (~35 pp): the "negative-space" chapter. Catalog systems that look like approximate sets but violate the Bernoulli axioms. Cash in the "we'll address this later" deferrals seeded in chapters 1, 3, 5, 10, 13.

**Architecture:** Replace `book/chapters/ch16-not-bernoulli.tex` stub with a fully drafted chapter containing 7 sections, learning-outcomes opener, 10-12 exercises, bibliographic entries, and a paired light Python notebook simulating correlated-error scenarios.

**Tech Stack:** LaTeX (book class), alex.sty, biblatex+biber. Python 3.11+ + numpy + matplotlib for the notebook.

**Scope:** Chapter 16 only. Part V integration check deferred to Plan 18.

**Spec source of truth:** `docs/superpowers/specs/2026-05-27-bernoulli-textbook-part5-design.md` §4 chapter 16 row.

**Base SHA:** `daf7766` (HEAD at end of Plan 15).

**Source material:**
- Mostly fresh writing.
- Reference points: chapter 4 axioms (the ones being violated); chapter 6 §6.4 perfect-filter line (still useful outside strict Bernoulli); chapter 9 §9.2 channel matrix (still useful).
- External literature: martingale concentration (Azuma-Hoeffding, McDiarmid; cite Devroye-Lugosi-Lugosi or similar); adversarial-ML literature.

**Lessons inherited from Plans 1-15:**

1. **Page discipline.** Chapter 16 target ~35pp; expect 38-44pp realistic.

2. **Soul-voice hook (BLOCKING):** Full banned-phrase list at `$CLAUDE_PLUGIN_ROOT/hooks/check-banned-phrases.sh`.

3. **Notation:** Mostly inherited; chapter 16 introduces no new symbols. References chapter 4 Axiom 1 / Axiom 2; chapter 6 perfect-filter line; chapter 9 channel matrix.

4. **Honesty discipline.** If a case is genuinely not Bernoulli, say so. No defensive hedging.

5. **The chapter cashes deferrals.** §16.1 must list each deferral being closed, with cross-references to the chapter where it was raised.

---

## File Structure

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch16-not-bernoulli.tex             # rewritten from stub
│   │   └── ch16/                               # NEW directory
│   │       ├── what-this-chapter-is-for.tex    # §16.1 (~3 pp)
│   │       ├── varying-rates.tex               # §16.2 (~6 pp)
│   │       ├── correlated-noise.tex            # §16.3 (~6 pp)
│   │       ├── adversarial-inputs.tex          # §16.4 (~6 pp)
│   │       ├── where-framework-helps.tex       # §16.5 (~4 pp)
│   │       ├── whats-next.tex                  # §16.6 (~2 pp)
│   │       ├── bibliographic-notes.tex         # §16.7 (~2 pp)
│   │       └── exercises.tex                   # 10-12 exercises (~2 pp)
│   └── references.bib                          # extended (martingale + adversarial-ML refs)
└── python/
    └── notebooks/
        └── ch16-not-bernoulli.ipynb            # correlated-error simulator (light)
```

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:not-bernoulli` | `ch16-not-bernoulli.tex` (Plan 0 stub) | (forward refs already exist in chapters 1/3/5/10/13 prose) |
| `sec:what-this-chapter-is-for` | `ch16/what-this-chapter-is-for.tex` (Task 2) | (internal) |
| `sec:varying-rates` | `ch16/varying-rates.tex` (Task 3) | (internal) |
| `sec:correlated-noise` | `ch16/correlated-noise.tex` (Task 4) | (internal) |
| `sec:adversarial-inputs` | `ch16/adversarial-inputs.tex` (Task 5) | (internal) |
| `sec:where-framework-helps` | `ch16/where-framework-helps.tex` (Task 6) | (internal) |

Backward references that should resolve:
- Chapter 4: `\Cref{ax:element-indep}` (Axiom 1), `\Cref{ax:block-rates-indep}` (Axiom 2), `\Cref{sec:axiom-1}`, `\Cref{sec:axiom-2}`
- Chapter 6: `\Cref{def:perfect-filter-line}`, `\Cref{sec:perfect-filter-line}`
- Chapter 9: `\Cref{def:n-ary-channel}`, `\Cref{sec:n-ary-channels}`
- Chapter 7: `\Cref{prop:binomial-variance}` (the Chebyshev/Chernoff connection for §16.2 martingale tools)
- Chapter 11: `\Cref{thm:chernoff}` (the iid Chernoff bound; §16.2 contrasts with Azuma-Hoeffding for the non-iid case)

Forward references via `\Cref{ch:N}`: chapter 17, chapter 18 (Plan 0 stubs exist).

---

## Tasks

### Task 1: Read sources and write chapter scaffolding

- [ ] Read sources: `book/chapters/ch04/axiom-1.tex`, `axiom-2.tex`; `book/chapters/ch06/perfect-filter-line.tex`; `book/chapters/ch11/sample-complexity.tex`; chapter notebooks for deferral context (ch1, ch3); Part V spec §4 chapter 16.

- [ ] Replace `book/chapters/ch16-not-bernoulli.tex` with the scaffold:

```latex
\chapter{Approximate but Not Bernoulli}
\label{ch:not-bernoulli}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item Identify three failure modes of the Bernoulli framework:
    varying rates over time, correlated noise across queries, and
    adversarial inputs.
  \item State which axiom each failure violates (Axiom 1 or Axiom 2)
    and recognize the consequences for chapter 3's composition
    theorem and chapter 7's confidence intervals.
  \item Apply the appropriate analytical tool when the Bernoulli
    machinery does not apply: martingale concentration inequalities,
    conditional bounds, or adversary models.
\end{itemize}
\end{quote}

% Section 16.1
\input{chapters/ch16/what-this-chapter-is-for}

% Section 16.2
\input{chapters/ch16/varying-rates}

% Section 16.3
\input{chapters/ch16/correlated-noise}

% Section 16.4
\input{chapters/ch16/adversarial-inputs}

% Section 16.5
\input{chapters/ch16/where-framework-helps}

% Section 16.6
\input{chapters/ch16/whats-next}

% Section 16.7
\input{chapters/ch16/bibliographic-notes}

% Exercises
\input{chapters/ch16/exercises}
```

- [ ] Create `book/chapters/ch16/` + 8 placeholder files. Each: `% Placeholder. Drafted in Plan 16 Task N.` (N = 2-9).

- [ ] Build exit 0. Commit:

```
book: scaffold chapter 16 (approximate but not Bernoulli) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener, seven section subfile inputs plus exercises, with matching
empty placeholders. Chapter 16 is the "negative-space" chapter that
cashes deferrals from chapters 1, 3, 5, 10, 13.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §16.1 What Chapter 16 Is For (~3 pp)

**Files:** Modify `book/chapters/ch16/what-this-chapter-is-for.tex`.

**Content checklist (4 items):**

1. **The chapter's role.** Throughout the book, several "what if?" questions were deferred to this chapter. §16.1 lists each one and the section that addresses it. Half a page.

2. **Deferral list.** Cross-reference each:
   - Chapter 1 §1.4 (sampling): "what if rates vary across samples?" → §16.2.
   - Chapter 1 exercise 10 / chapter 3 notebook open question: "what if witnesses are not independent?" → §16.3.
   - Chapter 5 §5.4 (one-sided sets): "what if the input distribution adapts?" → §16.4.
   - Chapter 10 §10.5 (sketch composition): "what if the data stream is adversarial?" → §16.4.
   - Chapter 13 exercise 11 (boundary algebra): "structures not fitting the type algebra?" → §16.4 and §16.5.
   One page.

3. **Three failure modes.** State explicitly: varying rates (§16.2), correlated noise (§16.3), adversarial inputs (§16.4). Each one violates either Axiom 1 (`\Cref{ax:element-indep}`) or Axiom 2 (`\Cref{ax:block-rates-indep}`) or both. Half a page.

4. **The chapter's posture.** Honesty: where the Bernoulli framework genuinely doesn't apply, we say so. §16.5 then catalogues partial cases where the framework still gives useful structure.

**Labels:** `\section{What This Chapter Is For}` with `\label{sec:what-this-chapter-is-for}`.

**Header cross-reference comment block.**

**Target length:** ~3 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 3: §16.2 Varying Rates Over Time (~6 pp)

**Files:** Modify `book/chapters/ch16/varying-rates.tex`.

**Content checklist (5 items):**

1. **The phenomenon.** $\fprate(t)$ varies with the query index $t$ rather than being a fixed property of the channel. Concrete examples: a classifier whose training distribution drifts from the deployment distribution; a Bloom filter being filled past its design capacity; a hardware fault rate that drifts with temperature. One page.

2. **Which axiom is violated.** Axiom 2 (`\Cref{ax:block-rates-indep}`): per-block rates are no longer stable across queries. Recap what Axiom 2 said and exactly why the time-varying case breaks it. One page.

3. **Consequences.** The chapter 3 §3.3 composition theorem $\eta_{\text{total}} = 1 - \prod(1 - \eta_i)$ breaks: the product no longer gives the chained error rate. The chapter 7 §7.4 PPV formulas break: prevalence + rates are no longer a fixed function. The chapter 11 §11.4 Chernoff bound also breaks for iid sums; we need martingale tools. One page.

4. **The right tool: martingale concentration.** Azuma-Hoeffding inequality for sums of bounded-difference martingales: for $X = \sum X_t$ with $|X_t - X_{t-1}| \le c_t$ (a "bounded difference" sequence), $\Pr[|X - \mathbb{E}[X]| \ge a] \le 2 \exp(-a^2 / (2 \sum c_t^2))$. Cite Azuma (1967) and Hoeffding (1963). One paragraph statement, no proof. Half a page.

5. **Worked example.** A Bloom filter being filled past its design capacity: $\fprate$ grows from $0.01$ early to $0.5$ late. Apply Azuma-Hoeffding to bound the total false-positive count under the time-varying $\fprate(t)$. One page.

6. **Pedagogical note.** When you suspect varying rates, the diagnostic is: does $\hat{\fprate}$ shift as you sweep through time-ordered samples? If yes, drop the iid assumption and use Azuma. Half a page.

**Labels:** `\section{Varying Rates Over Time}` with `\label{sec:varying-rates}`. Proposition `\label{prop:azuma-hoeffding}` on the Azuma-Hoeffding bound.

**Header cross-reference comment block.**

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 4: §16.3 Correlated Noise Across Queries (~6 pp)

**Files:** Modify `book/chapters/ch16/correlated-noise.tex`.

**Content checklist (5 items):**

1. **The phenomenon.** Two queries on the same data structure may share noise sources. The same query repeated is deterministic. Sequential dependent draws. One page.

2. **Which axiom is violated.** Axiom 1 (`\Cref{ax:element-indep}`): error events at distinct queries are no longer mutually independent. Recap Axiom 1 and the failure case. One page.

3. **Concrete examples.**
   - **Same Bloom filter, repeated query**: $\Pr[\text{2nd query says } \top \mid \text{1st query said } \top] = 1$ for identical $x$. Deterministic, fully correlated.
   - **Two Bloom filters sharing a hash family**: query the union; the bit-OR collision events are correlated.
   - **Online learning**: a classifier updates between queries; the noise at query $t$ depends on queries $1, \ldots, t - 1$.
   One page.

4. **Consequences.** Chapter 3 §3.3 composition theorem $\eta_{\text{total}} = 1 - \prod(1 - \eta_i)$ assumed independence; it breaks when error events are correlated. Chapter 5 §5.2 Bloom filter's $\fprate$ derivation assumed independent bit-checks; the $k$-bit-position correlation case (chapter 5 §5.2 exercise 7 acknowledged this) is real. One page.

5. **Right tools.**
   - Conditional bounds via the law of total probability.
   - McDiarmid's inequality for bounded-difference functions of dependent variables.
   - Negative correlation can sometimes be ignored (gives tighter bounds, not looser).
   Half a page.

6. **Worked example.** Two Bloom filters with shared hash family, both representing related but different sets. Their joint false-positive rate at a query $x \notin A \cup B$ is greater than the product (positive correlation through shared hashes). Quantify with a small numerical example. One page.

**Labels:** `\section{Correlated Noise Across Queries}` with `\label{sec:correlated-noise}`. Optional proposition on McDiarmid's inequality.

**Header cross-reference comment block.**

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 5: §16.4 Adversarial Inputs (~6 pp)

**Files:** Modify `book/chapters/ch16/adversarial-inputs.tex`.

**Content checklist (5 items):**

1. **The phenomenon.** Queries are not iid; they are chosen by an adversary (or by an adaptive learning system) to expose failures. A gradient-descent attacker can find inputs that maximize $\fprate$ for a specific filter or classifier. One page.

2. **What's violated.** Axiom 1 (independence) breaks because the adversary's $t$-th query depends on the responses to queries $1, \ldots, t - 1$. The whole probabilistic setup assumes a query distribution; an adversary chooses the worst-case query. One page.

3. **Concrete examples.**
   - **Bloom-filter evasion**: an attacker chooses inputs whose hashes collide with the false-positive set.
   - **Side-channel timing**: the time taken to respond reveals which bits are set; the attacker queries based on response timings.
   - **Adversarial ML inputs**: classifier inputs crafted at decision boundaries.
   - **Cryptographic chosen-plaintext attacks**: the encrypted-search context (chapter 18 §18.3) faces this.
   One page.

4. **Right tools.**
   - Worst-case analysis (drop the average and bound the maximum).
   - Cryptographic hash families (forces the attacker to guess the secret salt).
   - Privacy-preserving primitives (oblivious computing; chapter 17 §17.3 covers).
   One page.

5. **Worked example.** A Bloom filter at $\fprate = 0.01$ under iid queries. An attacker with knowledge of the hash family can find a colliding input in expected $O(1/\fprate) = O(100)$ queries. Quantify the gap between iid analysis and worst-case adversarial analysis. One page.

**Labels:** `\section{Adversarial Inputs}` with `\label{sec:adversarial-inputs}`.

**Header cross-reference comment block.**

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 6: §16.5 Where the Framework Still Helps (~4 pp)

**Files:** Modify `book/chapters/ch16/where-framework-helps.tex`.

**Content checklist (4 items):**

1. **The framework's reach extends beyond strict iid.** Even outside Axiom 1 / Axiom 2, the framework's geometric and structural intuitions often still help.

2. **Geometric reach.** The chapter 6 §6.4 perfect-filter line still classifies systems by their $\fprate, \fnrate$ point in $[0, 1]^2$, even when those rates are time-varying or correlated. One page.

3. **Channel-matrix reach.** The chapter 9 §9.2 channel matrix $Q$ still captures the per-query behavior even if the matrix is not stable across queries; you replace a single $Q$ with a sequence $(Q_t)_{t = 1, \ldots, m}$ and the chapter 9 §9.3 Kronecker theorem still applies CONDITIONALLY on the query sequence. One page.

4. **PPV/NPV reach.** The chapter 7 §7.4 PPV formula still holds at any single query; what changes is that the prevalence $\pi$ may itself be time-varying. The downstream uncertainty propagation requires care, but the formula is intact. Half a page.

5. **A pragmatic rule.** When Axiom 1 or Axiom 2 fails, use the framework's geometry and channel-matrix view; replace the iid analytical tools (Chernoff, binomial CI) with their non-iid counterparts (Azuma, McDiarmid, worst-case bounds). Half a page.

**Labels:** `\section{Where the Framework Still Helps}` with `\label{sec:where-framework-helps}`.

**Header cross-reference comment block.**

**Target length:** ~4 pp (900-1200 prose words).

**Workflow:** Standard.

---

### Task 7: §16.6 What's Next (~2 pp)

**Files:** Modify `book/chapters/ch16/whats-next.tex`.

**Content (3 items):**

1. **Closing the negative space.** This chapter completed the framework's boundary cataloguing.

2. **Forward to chapters 17-18.** Two applications: cipher maps and trapdoor computing (chapter 17); encrypted search (chapter 18). Both are Bernoulli-framework applications with cryptographic constraints.

3. **§16.7 names the analytical alternatives.**

**Labels:** `\section{What's Next}` with `\label{sec:ch16-whats-next}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 8: §16.7 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch16/bibliographic-notes.tex`; extend `book/references.bib`.

**Content (4 paragraphs):**

1. **Martingale concentration:** Azuma (1967), Hoeffding (1963), McDiarmid (1989). Add bib entries.

2. **Devroye-Lugosi-Lugosi:** standard reference for non-iid concentration in learning theory.

3. **Adversarial ML:** Goodfellow et al on adversarial examples; Carlini-Wagner on attack methods. Add bib entries if cited.

4. **Oblivious computing literature** as the bridge to chapter 17.

**New bib entries:**

```bibtex
@article{azuma-1967,
  author  = {Kazuoki Azuma},
  title   = {Weighted Sums of Certain Dependent Random Variables},
  journal = {Tohoku Mathematical Journal},
  volume  = {19},
  number  = {3},
  pages   = {357--367},
  year    = {1967}
}

@article{hoeffding-1963,
  author  = {Wassily Hoeffding},
  title   = {Probability Inequalities for Sums of Bounded Random Variables},
  journal = {Journal of the American Statistical Association},
  volume  = {58},
  number  = {301},
  pages   = {13--30},
  year    = {1963}
}

@incollection{mcdiarmid-1989,
  author    = {Colin McDiarmid},
  title     = {On the Method of Bounded Differences},
  booktitle = {Surveys in Combinatorics},
  pages     = {148--188},
  year      = {1989},
  publisher = {Cambridge University Press}
}
```

(Add only if cited; add others only if cited.)

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline` + `\label{sec:bib-notes-ch16}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 9: Chapter 16 Exercises (11)

**Files:** Modify `book/chapters/ch16/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Identify the violation.** For each of three example systems (time-varying classifier, two-Bloom-filter union with shared hashes, online learning), state which axiom is violated.

2. **Azuma-Hoeffding application.** For a martingale with $|X_t - X_{t-1}| \le 1$ and $n = 100$, compute the bound on $\Pr[|X_n - \mathbb{E}[X_n]| \ge 10]$.

3. **Bloom filter at capacity.** A Bloom filter sized for $n = 1000$ items at $\fprate = 0.01$ is filled with $n = 5000$ items instead. What is the resulting $\fprate$? (Recall §5.2 formula.)

**Medium (★★ × 5):**

4. **Notebook-tied correlated noise simulation.** Use the chapter 16 notebook to simulate two Bloom filters with shared hash family; measure the joint FPR and compare to the iid prediction.

5. **Composition theorem under varying rates.** Suppose $\fprate(t)$ for $t = 1, \ldots, k$ are independent but with different means. Adapt chapter 3 §3.3's composition formula and bound the expected combined FPR.

6. **Bloom adversary lower bound.** For a Bloom filter at $\fprate = 0.001$, derive the expected number of queries an adversary needs to find a false positive (assuming hash family is known).

7. **Chernoff vs Azuma at iid.** Show that when the dependence vanishes, Azuma-Hoeffding recovers the Chernoff bound up to constants.

8. **PPV under varying prevalence.** Apply chapter 7 §7.4 PPV with a time-varying prevalence $\pi(t)$; derive the time-average PPV and identify when it equals the single-instance PPV.

**Challenging (★★★ × 3):**

9. **McDiarmid for Bloom filter FPR.** Apply McDiarmid's inequality to derive a concentration bound for the empirical FPR of a Bloom filter under a single fixed query stream (avoiding the iid assumption).

10. **Adaptive adversary.** Design an adaptive query strategy that exploits feedback from earlier query responses to maximize a Bloom filter's empirical FPR. Quantify the gain over a non-adaptive baseline.

11. **Bounds on Bernoulli framework's domain of validity.** State a sufficient condition under which the chapter 3 composition theorem's $\eta_{\text{total}} = 1 - \prod(1 - \eta_i)$ formula gives an upper bound (rather than equality) on the true error rate.

**Target length:** ~2 pp (700-900 prose words).

**Workflow:** Standard.

---

### Task 10: Chapter 16 Notebook (`ch16-not-bernoulli.ipynb`)

**Files:** Create `python/notebooks/ch16-not-bernoulli.ipynb`. Light notebook per master spec.

**Content (~10-12 cells):**

1. **Title + setup** (markdown + code): numpy, matplotlib, hashlib; seeded RNG.

2. **Independent Bloom filters baseline** (code): build two Bloom filters with INDEPENDENT hash families; measure the joint FPR on a query stream; verify it matches the iid product prediction.

3. **Shared-hash-family Bloom filters** (code): build two Bloom filters with the SAME hash family; measure the joint FPR; compare to iid prediction. Show the discrepancy.

4. **Varying-rate simulation** (code): a Bloom filter that fills past capacity; plot $\fprate$ over time as items are inserted; compare to the §5.2 stationary formula.

5. **Adversarial query simulation** (code): with knowledge of the hash family, run an attack that finds a false positive in expected $1/\fprate$ queries. Plot the running count of attacks until first FP.

6. **Azuma-Hoeffding vs iid Chernoff** (code): for the varying-rate scenario, compute and compare the Azuma-Hoeffding and Chernoff bounds on the empirical FPR.

7. **Discussion** (markdown): each scenario as a violation of a specific axiom; the framework's geometric reach still helps (§16.5).

**Numerical sanity targets:**
- Independent Bloom filters: joint empirical FPR within $\pm 0.005$ of $\fprate^2$ at large sample.
- Shared-hash-family Bloom filters: joint empirical FPR > $\fprate^2$ (positive correlation).
- Adversary finds first FP within $O(1/\fprate)$ expected queries.

**Workflow:** Standard. Execute end-to-end. Commit.

---

## Self-Review

Spec coverage: chapter 16 row → each section has its own task. Light notebook in Task 10.

Type and label consistency: chapter 4 axioms referenced; chapter 6 §6.4 referenced; chapter 9 §9.2 referenced; chapter 7 §7.4 referenced; chapter 11 §11.4 referenced.

The chapter cashes 5 explicit deferrals from prior chapters (§16.1 lists them).
