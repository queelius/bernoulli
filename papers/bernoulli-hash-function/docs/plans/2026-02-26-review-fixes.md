# Review Fixes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix all 3 critical, 8 major, and 10 minor issues from the 2026-02-26 multi-agent review.

**Architecture:** Pure LaTeX edits across the paper's section files, defs.tex, main.tex, references.bib, and Makefile. No new files created (gloss.tex and fig_shs removed). Build verified with `make cleanall && make` after each batch.

**Tech Stack:** pdflatex, bibtex, pgfplots, alex.sty, algorithm2e

---

### Task 1: Fix value hash salting in Algorithms 1 and 2 (C3)

**Files:**
- Modify: `sections/construction.tex:46-48` (Algorithm 1, value hash)
- Modify: `sections/construction.tex:88-90` (Algorithm 2, value hash)

**Step 1: Salt the value hash in Algorithm 1**

In `sections/construction.tex`, line 47, change:
```latex
$\hash(1 \cat x^{(i)}) \bmod 2^{\BL(v^{(i)})}
```
to:
```latex
$\hash(1 \cat x^{(i)} \cat b) \bmod 2^{\BL(v^{(i)})}
```

**Step 2: Salt the value hash in Algorithm 2**

In `sections/construction.tex`, line 89, change:
```latex
$\hash(1 \cat x_i) \bmod 2^{\BL(v_i)}
```
to:
```latex
$\hash(1 \cat x_i \cat b) \bmod 2^{\BL(v_i)}
```

**Step 3: Verify consistency**

Confirm all four algorithms now use `h(1 || x || b)` for value hashing:
- Algorithm 1 (equality): line 47 — just fixed
- Algorithm 2 (threshold): line 89 — just fixed
- Algorithm 3 (adaptive): line 146 — already correct (`h(1 || x_i || b)`)
- Find algorithm: line 225 — already correct (`h(1 || x || b)`)

**Step 4: Build**

Run: `make cleanall && make 2>&1 | tail -3`
Expected: `Output written on main.pdf`

---

### Task 2: Rewrite space complexity proof using exact formula (C1)

**Files:**
- Modify: `sections/space.tex:36-85` (Theorem 5.2 proof)

**Step 1: Replace the Taylor expansion proof**

Replace the entire proof of Theorem 5.2 (lines 36-85) with a rigorous proof that uses the exact formula from Appendix A (`E[N] = sum q^{2^n-1}`) and bounds it via `-log2(p) + O(1)`.

The new proof should:
1. Start from `E[N] = sum_{n>=1} q^{2^n-1}` (Theorem B.3 / Appendix A)
2. Show upper bound: `E[N] <= sum_{n>=0} q^{2^n-1} = (1/(1-q)) * ...` or use `E[N] <= E[floor(log2 Q)] <= E[log2 Q] = -log2(p)/ln(2)` ... Actually use Jensen's inequality: `log2` is concave, so `E[log2 Q] <= log2 E[Q] = -log2 p`, giving an upper bound
3. Show lower bound: `E[N] = E[floor(log2 Q)] >= E[log2 Q] - 1 = -log2 p - 1` (floor drops at most 1)
4. Combine: `E[N] = -log2 p + O(1)`
5. Substitute `p = eps^{m-1}/2^{m*mu}` (equality) or `p = eps^m/2^{m*mu}` (threshold)
6. Divide by m, take limit

**Step 2: Build and verify**

Run: `make cleanall && make 2>&1 | tail -3`

---

### Task 3: Rewrite Appendix B proof — remove "Wait—" (C2)

**Files:**
- Modify: `sections/appendix.tex:133-188` (Theorem B.2 proof)

**Step 1: Restructure the proof**

Replace the entire proof body (lines 133-188) with a clean version that:
1. States upfront: "For `N >> m`, the probability of ties among the m residues is `O(m^2/N)`, which is negligible in the regime of interest. We derive the PMF under the assumption that all m residues are distinct."
2. Presents the combinatorial argument directly (choose p-1 from {0,...,j-1}, 1 matching j, m-p from {j+1,...,N-1})
3. Gives the closed form immediately
4. Derives the continuous Beta limit
5. No "Wait—", no wrong-then-correct structure

**Step 2: Also remove the confusing intermediate formula (m1)**

Remove or simplify eq:os_pmf_detailed (the double-sum formula, lines 116-124). Keep only the closed form. The double-sum is unnecessary since we derive the closed form directly.

**Step 3: Build and verify**

Run: `make cleanall && make 2>&1 | tail -3`

---

### Task 4: Fix Bloom filter formula and add modern filter comparisons (M3, M2)

**Files:**
- Modify: `sections/discussion.tex:27-33` (Bloom filter paragraph)
- Modify: `sections/discussion.tex:60-76` (after adaptive paragraph, before practical considerations)
- Modify: `references.bib` (add 4 new references)

**Step 1: Fix Bloom filter space formula**

In `sections/discussion.tex`, line 30, change:
```latex
It achieves $\log_2(e) / \fprate$ bits per element, which exceeds the
information-theoretic lower bound of $-\log_2 \fprate$ by a factor of
$\log_2 e \approx 1.44$.
```
to:
```latex
It achieves $\log_2(e) \cdot \log_2(1/\fprate)$ bits per element, which
exceeds the information-theoretic lower bound of $-\log_2 \fprate$ by a
factor of $\log_2 e \approx 1.44$.
```

**Step 2: Add modern filter paragraphs**

After the adaptive threshold paragraph (line 59), add paragraphs for:
- Cuckoo filter (Fan et al. 2014): ~`(2 + eps)*log2(1/eps)` bits, O(n) construction, supports deletion
- XOR filter (Graf & Lemire 2020): `~1.23*log2(1/eps)` bits, O(n) construction, immutable
- Ribbon filter (Dillinger & Walzer 2021): near-optimal `~log2(1/eps) + 1.5` bits, O(n) construction
- Pagh-Pagh-Rao (2005): achieves exact lower bound with polynomial construction

Key differentiator: practical filters achieve near-optimal space with O(n) construction. The BHF (equality/threshold) achieves EXACTLY optimal space with exponential construction. The adaptive variant bridges this with O(m log m) construction but random FPR.

**Step 3: Add references to references.bib**

Add entries for:
- `carter1978` — Carter, Floyd, Gill, Markowsky, Wegman (1978). Exact and Approximate Membership Testers. STOC.
- `pagh2005` — Pagh, Pagh, Rao (2005). An Optimal Bloom Filter Replacement. SODA.
- `cuckoo` — Fan, Andersen, Kaminsky, Mitzenmacher (2014). Cuckoo Filter. CoNEXT.
- `xor_filter` — Graf, Lemire (2020). Xor Filters. ACM JEA.
- `ribbon` — Dillinger, Walzer (2021). Ribbon Filter. SIGMOD.

**Step 4: Build and verify**

Run: `make cleanall && make 2>&1 | tail -3`

---

### Task 5: Change "Postulate" to "Theorem" and cite Carter et al. (M1, m2)

**Files:**
- Modify: `sections/prelim.tex:69-76` (set lower bound)
- Modify: `sections/prelim.tex:99-106` (map lower bound)

**Step 1: Change Postulate to Theorem for set lower bound**

In `sections/prelim.tex`, lines 69-76, change `\begin{postulate}` / `\end{postulate}` to `\begin{theorem}` / `\end{theorem}` and add citation.

Change:
```latex
\begin{postulate}[Space lower bound for sets]
```
to:
```latex
\begin{theorem}[Space lower bound for sets {\cite{carter1978}}]
```
and `\end{postulate}` to `\end{theorem}`.

**Step 2: Same for map lower bound**

Lines 99-106: same change. Cite `carter1978` (the set result implies the map result with the value encoding overhead).

**Step 3: Update cref references**

`post:set_lb` and `post:map_lb` are referenced elsewhere. Check if `postulate` environment is defined differently from `theorem` in alex.sty. If `postulate` is a separate environment, we may need to keep the labels or define the environment. Search for all `\cref{post:set_lb}` and `\cref{post:map_lb}` references.

**Step 4: Build and verify**

---

### Task 6: Formalize Remark 5.5 — lower bound not violated (M4)

**Files:**
- Modify: `sections/space.tex:162-177` (Remark 5.5)

**Step 1: Rewrite Remark 5.5 with formal statement**

Replace the current informal text with a precise argument:
1. State the formal hypothesis of the lower bound: "For every non-member x, the data structure guarantees Pr[x accepted] <= eps."
2. Explain that the adaptive threshold provides only a distributional guarantee: E[Pr[x accepted]] = p/(m+1), but the actual FPR for any particular construction is random.
3. Since no worst-case FPR bound is promised a priori, the hypothesis of the lower bound theorem is not satisfied.
4. The "missing" information is encoded in the randomness of eps itself.

**Step 2: Build and verify**

---

### Task 7: Fix "an BHF" → "a BHF" everywhere (M6)

**Files:**
- Modify: `sections/construction.tex:190` ("an BHF-coded")
- Modify: `sections/construction.tex:214` ("an BHF-coded")
- Modify: `sections/entropy.tex:71` ("an BHF")
- Modify: `sections/appendix.tex:18` ("an BHF")

**Step 1: Replace all "an BHF" with "a BHF"**

Four occurrences in the source files. Use replace_all on each file.

**Step 2: Build and verify**

---

### Task 8: Add independence to random oracle definition (m4)

**Files:**
- Modify: `sections/prelim.tex:31-38` (Definition 2.2)

**Step 1: Add independence clause**

In the random oracle definition, after "uniformly distributed over its range for every unique input", add: "with outputs independent across distinct inputs".

**Step 2: Build and verify**

---

### Task 9: Rename salt bit length RV to avoid overloading N (m5)

**Files:**
- Modify: `sections/space.tex` (all occurrences of `\RV{N}` for salt bit length)
- Modify: `sections/entropy.tex` (same)
- Modify: `sections/appendix.tex` (same)

**Step 1: Rename `\RV{N}` to `\RV{L}` for salt bit length**

Search for all `\RV{N}` in space.tex, entropy.tex, and appendix.tex. Replace with `\RV{L}`. Also update the surrounding text that says "bit length $\RV{N}$" or "length $N$" when it refers to the salt length.

Do NOT change `N` when it refers to the modulus (used in shf.tex, construction.tex, etc.).

**Step 2: Build and verify all cross-references still resolve**

---

### Task 10: Remove dead code — gloss.tex and unused figure (M7, m10)

**Files:**
- Delete: `gloss.tex`
- Delete: `img/fig_shs.tex`, `img/fig_shs.pdf`
- Modify: `Makefile` (remove `gloss.tex` from SOURCES)

**Step 1: Remove gloss.tex from Makefile SOURCES**

In Makefile, line 6, remove `gloss.tex` from the SOURCES variable.

**Step 2: Delete the files**

```bash
rm gloss.tex img/fig_shs.tex img/fig_shs.pdf
```

**Step 3: Build and verify**

---

### Task 11: Fix cardinality estimator sign and entropy-space tradeoff (m8, m9)

**Files:**
- Modify: `sections/entropy.tex:71-77` (cardinality estimator)
- Modify: `sections/entropy.tex:79-91` (entropy-space tradeoff)

**Step 1: Fix sign in map case**

Line 76: "replacing $\log_2 \fprate$ with $\log_2 \fprate - \mu$" is wrong because `log2(eps)` is negative. The denominator should be `log2(eps) - mu` which makes it more negative. Fix to:
```latex
For maps, replace $\log_2 \fprate$ with $\log_2 \fprate - \mu$ in the
denominator (both terms are negative, so $\hat{m}$ remains positive).
```

Or more clearly: the formula should be `hat{m} = -BL(S~) / (log2(eps) - mu)`.

**Step 2: Add concrete mechanism for entropy-space tradeoff**

In the tradeoff subsection, add a sentence: "This is achieved by skipping all salts shorter than $\ell$ bits and searching only among salts of length exactly $\ell$."

**Step 3: Build and verify**

---

### Task 12: Define "salt" at first use in intro (m7)

**Files:**
- Modify: `sections/intro.tex:16-18`

**Step 1: Add brief parenthetical**

After "acceptance predicate over hash outputs", add a brief definition of salt. Change:
```latex
constructions parameterized by an \emph{acceptance predicate} over hash
outputs.
```
to:
```latex
constructions parameterized by an \emph{acceptance predicate} over hash
outputs. A \emph{salt} is a bit string discovered by search that, when
concatenated with each key before hashing, yields the desired acceptance
behavior.
```

**Step 2: Build and verify**

---

### Task 13: Simplify abstract (m6 from review)

**Files:**
- Modify: `main.tex:49-68` (abstract)

**Step 1: Trim adaptive threshold details from abstract**

Replace the overly technical adaptive threshold sentence with a simpler version that avoids "p-th order statistic" and "O(log N/m)" notation. Keep it to one sentence about the adaptive variant.

**Step 2: Build and verify**

---

### Task 14: Add note about FNR search complexity (m3)

**Files:**
- Modify: `sections/shf.tex:139-152` (Theorem 3.4 proof, after line 151)

**Step 1: Add remark after the proof**

After the proof of Theorem 3.4, add a brief remark:
```latex
\begin{remark}
The $\binom{m}{p}$ bound for the equality predicate applies to the naive
subset-enumeration algorithm (\cref{alg:make_shf_eq}).
A hash-and-count approach---hashing all $m$ elements, grouping by hash value,
and checking if any group has $\geq p$ members---achieves $\mathcal{O}(m)$
per candidate salt, matching the threshold predicate.
However, the equality predicate must still search over possible $h_0$ values
implicitly, so the constant factor is larger.
\end{remark}
```

**Step 2: Build and verify**

---

### Task 15: Final build, cross-ref check, and commit

**Step 1: Full clean build**

```bash
make cleanall && make
```

**Step 2: Check for warnings**

```bash
grep -c "undefined" main.log
grep -c "multiply defined" main.log
grep "pdfTeX warning" main.log
```

Expected: 0 undefined, 0 multiply-defined.

**Step 3: Commit**

```bash
git add -A
git commit -m "Address all review findings: fix proofs, algorithms, citations, and prose"
```
