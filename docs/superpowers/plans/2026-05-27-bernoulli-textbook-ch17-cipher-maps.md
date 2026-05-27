# Bernoulli Textbook Chapter 17: Cipher Maps and Trapdoor Computing (Plan 17)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Draft Chapter 17 of Part V (~38 pp): the Bernoulli framework as the error model for the trapdoor computing paradigm. Cipher maps are random approximate maps with cryptographic properties; the framework's $\fprate, \fnrate$ govern recovery quality. Theory chapter, no notebook.

**Architecture:** Replace `book/chapters/ch17-cipher-maps-trapdoor.tex` stub with a fully drafted chapter containing 8 sections, learning-outcomes opener, 10-12 exercises, and bibliographic entries.

**Tech Stack:** LaTeX (book class), alex.sty, biblatex+biber. No notebook.

**Scope:** Chapter 17 only. Part V integration check at Plan 18 Task 10.

**Spec source of truth:** `docs/superpowers/specs/2026-05-27-bernoulli-textbook-part5-design.md` §4 chapter 17 row.

**Base SHA:** `855bcc5` (HEAD at end of Plan 16).

**Source material (sibling monorepo `~/github/trapdoor-computing/`):**
- `papers/cipher-maps/` (primary source for §17.1, §17.2, §17.3)
- `papers/boolean-algebra-over-trapdoor-sets/` (§17.5)
- `papers/maximizing-confidentiality/` (§17.6)
- Framework backward refs: chapter 4 §4.4 Kronecker, chapter 6 §6.4 perfect-filter line, chapter 7 §7.4 PPV/NPV, chapter 9 §9.2 channel matrix, chapter 14 BHF.

**Lessons inherited from Plans 1-16:**

1. **Page discipline.** Chapter 17 target ~38pp; expect 40-44pp realistic (theory-only chapters can run longer per Plan 13 pattern: chapter 13 came in at 22pp on 20pp target).

2. **Soul-voice hook (BLOCKING):** Full banned-phrase list. The hook is strict on em-dashes.

3. **Sources are in a sibling monorepo.** The implementer must read from `~/github/trapdoor-computing/papers/...` paths.

4. **No notebook.** Master spec marks this chapter "theory + sidebar on oblivious computing" with no notebook.

5. **Connect to Bernoulli framework throughout.** Cipher maps and trapdoor sets are NEW abstractions here; the framework connection (chapter 4 Kronecker, chapter 6 perfect-filter line, chapter 7 PPV) is what makes this a chapter of THIS book rather than a separate cryptographic monograph.

---

## File Structure

```
bernoulli/
├── book/
│   ├── chapters/
│   │   ├── ch17-cipher-maps-trapdoor.tex      # rewritten from stub
│   │   └── ch17/                                # NEW directory
│   │       ├── what-is-cipher-map.tex           # §17.1 (~4 pp)
│   │       ├── bernoulli-error-model.tex        # §17.2 (~6 pp)
│   │       ├── trapdoor-paradigm.tex            # §17.3 (~7 pp)
│   │       ├── fhe-sidebar.tex                  # §17.4 (~5 pp)
│   │       ├── boolean-trapdoor.tex             # §17.5 (~6 pp)
│   │       ├── maximizing-confidentiality.tex   # §17.6 (~4 pp)
│   │       ├── bridge.tex                       # §17.7 (~2 pp)
│   │       ├── bibliographic-notes.tex          # §17.8 (~2 pp)
│   │       └── exercises.tex                    # 10-12 exercises (~2 pp)
│   └── references.bib                          # extended (cipher-maps paper, FHE refs)
```

No `python/notebooks/ch17-*.ipynb` (theory chapter).

---

## Cross-Reference Map

| Label | Defined in | Referenced from |
|---|---|---|
| `ch:cipher-maps-trapdoor` | `ch17-cipher-maps-trapdoor.tex` (Plan 0 stub) | chapter 16 §16.4, chapter 16 §16.6 |
| `sec:what-is-cipher-map` | `ch17/what-is-cipher-map.tex` (Task 2) | (internal) |
| `sec:bernoulli-error-model` | `ch17/bernoulli-error-model.tex` (Task 3) | (internal) |
| `sec:trapdoor-paradigm` | `ch17/trapdoor-paradigm.tex` (Task 4) | (internal) |
| `sec:fhe-sidebar` | `ch17/fhe-sidebar.tex` (Task 5) | (internal) |
| `sec:boolean-trapdoor` | `ch17/boolean-trapdoor.tex` (Task 6) | (internal) |
| `sec:maximizing-confidentiality` | `ch17/maximizing-confidentiality.tex` (Task 7) | (internal) |
| `sec:ch17-bridge` | `ch17/bridge.tex` (Task 8) | (internal) |

Backward references that should resolve:
- Chapter 4: `\Cref{thm:kronecker}`, `\Cref{sec:kronecker}`
- Chapter 6: `\Cref{def:perfect-filter-line}`, `\Cref{sec:perfect-filter-line}`
- Chapter 7: `\Cref{def:ppv}`, `\Cref{def:npv}`, `\Cref{sec:derived-measures}`
- Chapter 9: `\Cref{def:n-ary-channel}`, `\Cref{sec:n-ary-channels}`, `\Cref{thm:n-ary-kronecker}`
- Chapter 14: `\Cref{def:bhf}`, `\Cref{ch:optimal-bernoulli-sets}`
- Chapter 16: `\Cref{sec:adversarial-inputs}`

Forward references via `\Cref{ch:N}`: chapter 18 (Plan 0 stub).

---

## Tasks

### Task 1: Read sources and write chapter scaffolding

- [ ] Read sources in the sibling monorepo (`~/github/trapdoor-computing/papers/cipher-maps/`, `boolean-algebra-over-trapdoor-sets/`, `maximizing-confidentiality/`) by their text files (skim a few key sections).

- [ ] Replace `book/chapters/ch17-cipher-maps-trapdoor.tex` with the scaffold:

```latex
\chapter{Cipher Maps and Trapdoor Computing}
\label{ch:cipher-maps-trapdoor}

\begin{quote}
\textsc{After this chapter you will be able to:}
\begin{itemize}
  \item State the cipher-map abstraction: a function that computes
    faithfully on encrypted inputs up to bounded $\fprate$ and
    $\fnrate$.
  \item Recognize the Bernoulli framework as the error model for
    cipher maps; identify the chapter~4 Kronecker theorem as the
    composition law for chained cipher-map evaluations.
  \item Apply the chapter~7 PPV / NPV framework to confidentiality
    analysis: every cipher-map output has a posterior over plaintext
    truth, and that posterior is the confidentiality measure.
\end{itemize}
\end{quote}

% Section 17.1
\input{chapters/ch17/what-is-cipher-map}

% Section 17.2
\input{chapters/ch17/bernoulli-error-model}

% Section 17.3
\input{chapters/ch17/trapdoor-paradigm}

% Section 17.4
\input{chapters/ch17/fhe-sidebar}

% Section 17.5
\input{chapters/ch17/boolean-trapdoor}

% Section 17.6
\input{chapters/ch17/maximizing-confidentiality}

% Section 17.7
\input{chapters/ch17/bridge}

% Section 17.8
\input{chapters/ch17/bibliographic-notes}

% Exercises
\input{chapters/ch17/exercises}
```

- [ ] Create `book/chapters/ch17/` + 9 placeholder files. Each: `% Placeholder. Drafted in Plan 17 Task N.` (N = 2-10).

- [ ] Build exit 0. Commit:

```
book: scaffold chapter 17 (cipher maps and trapdoor computing) section subfiles

Replace the 4-line stub with the chapter scaffold: learning-outcomes
opener (three bullets: cipher-map abstraction, Bernoulli as error
model + Kronecker composition, PPV-as-confidentiality), eight section
subfile inputs plus exercises, with matching empty placeholders.
Theory chapter; no notebook.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

---

### Task 2: §17.1 What is a Cipher Map? (~4 pp)

**Files:** Modify `book/chapters/ch17/what-is-cipher-map.tex`.

**Content checklist (5 items):**

1. **Setup.** A function $f : X \to Y$ on plaintext data. We want to compute $f$ on encrypted data: given $\mathsf{Enc}(x)$, produce something that decrypts to $f(x)$, without revealing $x$ to whoever computes. Half a page.

2. **The cipher map abstraction.** A cipher map $\tilde f : \mathsf{Enc}(X) \to \mathsf{Enc}(Y)$ approximates $f$ on encrypted inputs: $\mathsf{Dec}(\tilde f(\mathsf{Enc}(x))) \approx f(x)$ with bounded error. Define the error rates: $\fprate$ (extra spurious outputs) and $\fnrate$ (missing real outputs). One page.

3. **Why "approximate."** Exact computation on encrypted data requires FHE (chapter 17 §17.4 covers); FHE is expensive. Allowing bounded error makes cipher maps practical. The trade-off is exactly the Bernoulli framework's: space and runtime vs error rate. One page.

4. **The trapdoor key.** A secret key (the "trapdoor") that ENABLES recovery of plaintext from $\tilde f$'s output. Without the key, the output is "opaque" (information-theoretic or computational). One paragraph.

5. **Three example cipher maps.**
   - Encrypted set membership: $f(x) = \mathbf{1}[x \in A]$ realized via an encrypted Bloom filter.
   - Encrypted equality test: $f(x, y) = \mathbf{1}[x = y]$ via deterministic encryption.
   - Encrypted ordering: $f(x, y) = \mathbf{1}[x \le y]$ via order-preserving encryption (with known leakage).
   Half a page each. Total one page.

**Labels:** `\section{What is a Cipher Map?}` with `\label{sec:what-is-cipher-map}`. Definition `\label{def:cipher-map}`.

**Header cross-reference comment block.**

**Target length:** ~4 pp (900-1200 prose words).

**Workflow:** Standard.

---

### Task 3: §17.2 The Bernoulli Framework as Error Model (~6 pp)

**Files:** Modify `book/chapters/ch17/bernoulli-error-model.tex`.

**Content checklist (6 items):**

1. **The connection.** Cipher-map error rates ARE Bernoulli rates: $\fprate, \fnrate$ as defined in chapter 1 §1.2 and formalized in chapter 4 §4.5. Half a page.

2. **Per-query channel matrix.** Each cipher-map call produces a $2 \times 2$ channel matrix in the simplest case (Boolean predicate cipher maps). General-output cipher maps use chapter 9 §9.2's $K \times L$ matrix. One page.

3. **Chained cipher-map composition.** Computing $f \circ g$ on encrypted inputs: evaluate $g$ first (with its own $\fprate, \fnrate$), then $f$ on the (possibly-noisy) intermediate. Chapter 4 §4.4 Kronecker theorem governs the composed channel matrix. One page.

4. **Theorem: composed cipher-map error.** For two cipher maps $\tilde f, \tilde g$ with channel matrices $Q_f, Q_g$, the composed map $\tilde f \circ \tilde g$ has matrix $Q_g Q_f$ (left-multiplication for sequential composition). State formally with `\label{thm:cipher-composition}`. One page. Cite `\Cref{thm:kronecker}` and `\Cref{thm:n-ary-kronecker}`.

5. **The Bernoulli geometry applies.** Chapter 6 §6.4's perfect-filter line classifies cipher maps too: FNR-zero cipher maps are "safe" (no false negatives but possibly false positives); FPR-zero cipher maps are "exact-when-positive" but may miss some real outputs. Cite `\Cref{def:perfect-filter-line}`. Half a page.

6. **Worked example.** A two-stage encrypted classifier: stage 1 is a Bloom-filter membership test with $\fprate = 0.01, \fnrate = 0$; stage 2 is an exact ranking on stage-1 positives. Compose channel matrices and derive the overall cipher-map error. One page.

**Labels:** `\section{The Bernoulli Framework as Error Model}` with `\label{sec:bernoulli-error-model}`. Theorem `\label{thm:cipher-composition}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 4: §17.3 The Trapdoor Computing Paradigm (~7 pp)

**Files:** Modify `book/chapters/ch17/trapdoor-paradigm.tex`.

**Content checklist (5 items):**

1. **The paradigm.** Trapdoor computing: the data is encrypted; computation happens on the encrypted form; only the trapdoor key holder can decrypt. The cipher map is the computation; the trapdoor is the key. Reformulate from `~/github/trapdoor-computing/papers/cipher-maps/` (skim the README and intro). One page.

2. **Two-party setup.** A "server" holds encrypted data; a "client" holds the trapdoor key. The server runs the cipher map; the client decrypts. The Bernoulli error rates govern what the client can recover. One page.

3. **Confidentiality vs correctness trade-off.** A cipher map with tighter error rates often reveals more about the plaintext (less confidential); looser error rates preserve more privacy. The $(\fprate, \fnrate)$ point on the perfect-filter line of `\Cref{def:perfect-filter-line}` is also a confidentiality-vs-correctness point. One page.

4. **Multiple-query setting.** A server that answers many queries leaks more about the plaintext than one that answers few. Chapter 4 §4.4 Kronecker theorem governs how leakage accumulates across queries: the joint over $m$ queries factors, and each factor's contribution to confidentiality is independent under Axiom 1. Cite `\Cref{ax:element-indep}`. One page.

5. **Adaptive-adversary setting.** Chapter 16 §16.4's adversarial-query analysis applies: a server facing an adaptive adversary cannot rely on iid Bernoulli accounting and needs worst-case bounds. Cite `\Cref{sec:adversarial-inputs}`. Worked example: an adaptive query strategy that extracts $O(\log n)$ bits of plaintext per query under a leaky cipher map. Two pages.

**Labels:** `\section{The Trapdoor Computing Paradigm}` with `\label{sec:trapdoor-paradigm}`.

**Target length:** ~7 pp (1600-1900 prose words).

**Workflow:** Standard.

---

### Task 5: §17.4 Sidebar: Fully Homomorphic Encryption (~5 pp)

**Files:** Modify `book/chapters/ch17/fhe-sidebar.tex`.

**Content checklist (4 items):**

1. **What FHE is.** Fully homomorphic encryption: a scheme where any function $f$ can be computed on encrypted data with zero error. Gentry (2009) gave the first construction. Half a page.

2. **Cipher maps as a weaker abstraction.** Cipher maps are NOT zero-error; they accept the Bernoulli framework's $\fprate, \fnrate$ as a cost. In exchange they are practical (fast, small ciphertexts). Half a page.

3. **FHE cost.** FHE ciphertexts are huge (megabytes per bit in early schemes) and slow (seconds per bit operation). Modern schemes (BFV, BGV, CKKS) improve but remain orders of magnitude slower than cipher maps. One page.

4. **When to use which.** Use FHE when correctness matters absolutely (e.g., contract evaluation, medical-record exact lookup). Use cipher maps when error is tolerable and performance matters (e.g., approximate search, ranked retrieval, anonymity-preserving analytics). One page.

5. **A concrete comparison.** A Bloom-filter cipher map at $\fprate = 0.01$ uses bits per inserted element from chapter 5 §5.2's optimal formula. The FHE equivalent (encrypted exact set) uses kilobytes per element. The factor is $\sim 10^4$ at typical parameters. Half a page.

**Labels:** `\section{Sidebar: Fully Homomorphic Encryption}` with `\label{sec:fhe-sidebar}`.

**Target length:** ~5 pp (1100-1400 prose words).

**Workflow:** Standard.

---

### Task 6: §17.5 Boolean Algebra Over Trapdoor Sets (~6 pp)

**Files:** Modify `book/chapters/ch17/boolean-trapdoor.tex`.

**Source reading:** `~/github/trapdoor-computing/papers/boolean-algebra-over-trapdoor-sets/`.

**Content checklist (5 items):**

1. **Trapdoor sets.** A trapdoor set is an encrypted representation of an underlying plaintext set $A$. Membership queries use the trapdoor key; without the key, the set is opaque. The chapter 5 §5.2 Bloom filter is one example (a server can store an encrypted Bloom-filter representation, decryption happens client-side). One page.

2. **Boolean operations on trapdoor sets.** Union $\tilde A \cup \tilde B$, intersection $\tilde A \cap \tilde B$, complement $\complement \tilde A$. Each operation can be computed on the encrypted representations and decrypted to recover an approximate result of the plaintext set operation. One page.

3. **The composition theorem applies.** Chapter 3 §3.3's composition theorem $\eta_{\text{total}} = 1 - \prod(1 - \eta_i)$ governs how Boolean composition propagates trapdoor-set error rates. Cite `\Cref{thm:composition}`. One page.

4. **Cancellation phenomena.** Chapter 6 §6.3's cancellation analysis applies: composing trapdoor sets can ESCAPE the perfect-filter line, just as composing approximate sets in chapter 6 could. Cite `\Cref{sec:cancellation}`. One page.

5. **Worked example.** A query "is $x$ in $A$ AND $x$ in $B$?" computed on two trapdoor sets. Server returns the intersection's membership result; client decrypts. Derive the overall $\fprate$. One page.

**Labels:** `\section{Boolean Algebra Over Trapdoor Sets}` with `\label{sec:boolean-trapdoor}`.

**Target length:** ~6 pp (1400-1700 prose words).

**Workflow:** Standard.

---

### Task 7: §17.6 Maximizing Confidentiality (~4 pp)

**Files:** Modify `book/chapters/ch17/maximizing-confidentiality.tex`.

**Source reading:** `~/github/trapdoor-computing/papers/maximizing-confidentiality/`.

**Content checklist (4 items):**

1. **Confidentiality as a posterior.** Given a cipher map's output, the adversary's posterior over the plaintext is the confidentiality measure. PPV-style: $\Pr[\text{plaintext}=A \mid \text{observation}=B]$. One page.

2. **The chapter 7 §7.4 PPV framework applies.** For a cipher map at $\fprate, \fnrate$ on a workload with prevalence $\pi$ (background distribution over the plaintext space), the PPV is the chapter 7 §7.4 formula. Confidentiality is bounded by $1 - \PPV$. Cite `\Cref{def:ppv}`. One page.

3. **Maximizing confidentiality at fixed cost.** Given a target rate budget on the perfect-filter line, what point maximizes confidentiality? Generally: more error = more confidentiality. The trade-off curve is one-dimensional on the perfect-filter line. One page.

4. **Worked example.** A trapdoor set on a workload with $\pi = 0.01$ (1% of queries are real positives). At $\fprate = 0.05, \fnrate = 0$: PPV $\approx 0.168$ (chapter 7 §7.4 formula); confidentiality $\approx 0.832$. Compare to FHE (PPV = 1, confidentiality = 0). The Bernoulli framework gives a quantitative confidentiality metric. One page.

**Labels:** `\section{Maximizing Confidentiality}` with `\label{sec:maximizing-confidentiality}`.

**Target length:** ~4 pp (900-1200 prose words).

**Workflow:** Standard.

---

### Task 8: §17.7 Bridge (~2 pp)

**Files:** Modify `book/chapters/ch17/bridge.tex`.

**Content (3 items):**

1. Recap: cipher maps are Bernoulli-framework instances; their error rates serve a dual purpose (correctness AND confidentiality).
2. Chapter 18 applies these ideas to one specific cipher-map family: encrypted search. The encrypted-search problem is the canonical application.
3. §17.8 names the antecedents.

**Labels:** `\section{Bridge}` with `\label{sec:ch17-bridge}`.

**Target length:** ~2 pp (400-600 prose words).

**Workflow:** Standard.

---

### Task 9: §17.8 Bibliographic Notes (~2 pp)

**Files:** Modify `book/chapters/ch17/bibliographic-notes.tex`; extend `book/references.bib`.

**Content (4 paragraphs):**

1. **Cipher-maps paper.** Add bib entry pointing to `~/github/trapdoor-computing/papers/cipher-maps/`.

2. **Trapdoor-computing series.** Boolean algebra over trapdoor sets; maximizing confidentiality; algebraic cipher types. Add bib entries for the sibling papers.

3. **FHE literature.** Gentry (2009) "Fully Homomorphic Encryption Using Ideal Lattices"; BFV/BGV/CKKS papers. Add Gentry bib entry; others if cited.

4. **Oblivious-computing tradition.** Goldreich (1996) on software protection (already in bib from chapter 16); Naor-Yung; older line of work on secure multiparty computation.

**New bib entries (add only if cited):**

```bibtex
@misc{towell-cipher-maps,
  author = {Alexander Towell},
  title  = {Cipher maps: a unified framework for oblivious function evaluation},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/trapdoor-computing/tree/main/papers/cipher-maps}}
}

@inproceedings{gentry-2009,
  author    = {Craig Gentry},
  title     = {Fully Homomorphic Encryption Using Ideal Lattices},
  booktitle = {STOC},
  pages     = {169--178},
  year      = {2009}
}

@misc{towell-boolean-trapdoor,
  author = {Alexander Towell},
  title  = {Boolean algebra over trapdoor sets},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/trapdoor-computing/tree/main/papers/boolean-algebra-over-trapdoor-sets}}
}

@misc{towell-maximizing-confidentiality,
  author = {Alexander Towell},
  title  = {Maximizing confidentiality in encrypted search},
  year   = {2026},
  note   = {Manuscript},
  howpublished = {\url{https://github.com/queelius/trapdoor-computing/tree/main/papers/maximizing-confidentiality}}
}
```

**Section style:** `\section*{Bibliographic Notes}` + `\addcontentsline` + `\label{sec:bib-notes-ch17}`.

**Target length:** ~2 pp (400-600 prose words). Zero undefined citations.

**Workflow:** Standard.

---

### Task 10: Chapter 17 Exercises (11)

**Files:** Modify `book/chapters/ch17/exercises.tex`.

**Exercise set (11, 3 ★ / 5 ★★ / 3 ★★★):**

**Warm-up (★ × 3):**

1. **Cipher-map FPR computation.** A trapdoor set at $\fprate = 0.05, \fnrate = 0$ on a workload with prevalence $\pi = 0.1$. Compute PPV and confidentiality.

2. **Cipher-map composition.** Two cipher maps with channel matrices $Q_1, Q_2$ ($2 \times 2$, both FNR-zero). Write $Q_1 Q_2$ for the composed map.

3. **FHE vs cipher map.** State in two sentences when to use FHE vs cipher map.

**Medium (★★ × 5):**

4. **Multiple-query leakage.** A trapdoor set answers 10 queries at $\fprate = 0.05$. Bound the leakage using chapter 4 Axiom 1 (iid queries) and Kronecker factorization.

5. **Adaptive attack.** Construct an adaptive query strategy that recovers all of $A$ in $O(|A|/(1 - \fprate))$ queries.

6. **Confidentiality vs space.** A trapdoor Bloom filter at $\fprate = 0.01$ vs $\fprate = 0.001$; which gives more confidentiality? Quantify the gap at fixed prevalence $\pi = 0.05$.

7. **Boolean algebra leakage.** A query "$x \in A \cap B$" on two trapdoor sets at $\fprate = 0.05$ each. Compute the overall $\fprate$ and the confidentiality.

8. **Cancellation in trapdoor sets.** Apply chapter 6 §6.3's cancellation analysis to a complement of a trapdoor set union. Compute the resulting $(\fprate, \fnrate)$ point.

**Challenging (★★★ × 3):**

9. **PPV-based confidentiality bound.** Derive a tight lower bound on confidentiality given $\fprate, \fnrate, \pi$.

10. **Trapdoor set as a $\Bernoulli{T}$ instance.** Cast a trapdoor set as a $\Bernoulli{T}$ from chapter 13's algebra. Identify $T$ and the channel matrix structure.

11. **Information-theoretic confidentiality.** Apply Shannon entropy (chapter 8 §8.1) to compute the leakage of a cipher map in bits per query.

**Target length:** ~2 pp (700-900 prose words).

**Workflow:** Standard.

---

## Self-Review

Spec coverage: chapter 17 row → each section has its own task; theory-only (no notebook) per master spec.

Type and label consistency: chapter 4/6/7/9/14/16 labels referenced; sibling-monorepo paper bib entries added.
