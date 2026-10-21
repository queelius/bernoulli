# Bernoulli program: situation and strategy

2026-10-21, for Alexander Richard Towell. Synthesizes the five Codex runs in
`.research/` (publication-triage, bounded-discovery, dependence-calculus,
relations-revision, query-contract-planner), the Codex session logs of
2026-10-13 to 2026-10-21, an independent prior-art scan with Crossref-verified
citations ([verified-citations.json](verified-citations.json)), and audits of
the package, monograph, papers, metafunctor site, youtube-channel and
research-records. Nothing outward-facing was done: no submission, withdrawal,
deploy, mint, push or email.

## Verdict

The Bernoulli program is a **synthesis**, not a source of new theorems. Its
central object is a per-element asymmetric binary channel (randomized response
on an indicator), and nearly every headline result has a named predecessor,
several of them closer than the June literature gates or the October Codex
audits found:

| Program claim | Predecessor |
|---|---|
| Syndrome parity `½(1−∏(1−2qᵢ))` | Gallager 1962, *IRE Trans. IT*, Lemma 1; Matsui's piling-up lemma, EUROCRYPT '93 |
| AND/OR/NOT error through Boolean circuits | Parker & McCluskey 1975, *IEEE Trans. Computers*; probabilistic transfer matrices, Krishnaswamy et al. 2008, *ACM TODAES* |
| −log₂ε space bound; false-negative case called "open" | Carter et al. 1978; **Pagh & Rodler 2001, "Lossy Dictionaries," ESA, Prop. 1** |
| Perfect hash filter = MPHF + fingerprints | Dietzfelbinger & Pagh 2008, ICALP, §1 ("the origin of this idea is unknown to us") |
| Seed-search optimal construction (BHF) | RecSplit 2020, ShockHash 2024, ESA 2025 |
| `bernoulli<T>`: values correct w.p. p, composed through programs | Decaf (Boston et al., OOPSLA 2015); Rely 2013; Uncertain&lt;T&gt; 2014 |
| Approximate relational algebra | Fuhr & Rölleke 1997, *TOIS*; probabilistic-database lineage (Suciu et al. 2011) |
| Cipher-map properties | homophonic substitution (1989), honey-encryption DTEs, OKVS (2021, 2023) |
| The Bernoulli set itself | Warner 1965 randomized response; retouched / generalized Bloom filters |

The Codex no-go decisions hold, and the prior art is closer than its audits
found. What is real:

1. **The unification itself**, carried out at book length (19 chapters, ~146k
   words) with an executable companion.
2. **A sharp verification method** (exhaustive finite checks, exact rational
   audits, adversarial review) that has already found one genuine flaw in a
   published system (GBFPlus).
3. **A solid package**: 470 tests pass, 92% coverage, strict mypy clean.

**Earlier "proofs correct / paper ready" verdicts are unreliable**, including
Claude's own June review rounds. Codex later found:

- substantive errors in the relations paper;
- a wrong order-statistic formula in BHF (N=2, m=2, p=1 gives P(T=0)=1;
  enumeration gives 3/4);
- a composition failure in maps (§6.6 vs §7);
- in the quantum paper, the false claim described below.

## Live submission: QST-105566 (quantum readout)

Verified against `papers/bernoulli-quantum-readout/main.tex`:

1. **A false general claim.** Lines 160–161 say the pair (ε, ω) is carried
   "through an entire Boolean tree". Line 510 says any Boolean function's
   rate depends on the channels "only through the closed forms". The AND
   output is not a two-rate bit: its false-positive rate depends on which
   negative latent word occurred.
   - Counterexample: `(b0∧b1)∨b2` at latent word 010 with ε=.02, ω=.10.
   - Exact error: 1−(0.982)(0.98) = **0.03764**.
   - Propagating the pair: **0.020392**, roughly half the true value.
   - The framework's own composition paper gets this right (composition
     raises the model order). The quantum paper compressed it to a pair.
2. **Missing direct prior art for the claimed contribution:**
   - Parker–McCluskey 1975 and PTMs 2008 (forward, asymmetric-capable circuit
     error propagation);
   - Gallager 1962 (line 757 attributes the parity identity to prior art but
     cites no source for it);
   - Smith et al. 2021 (asymmetric response matrices).
3. **Wrong scope statement.** Lines 258 and 1072 say the model is faithful
   "precisely when the density matrix is diagonal". The classical assignment
   model holds for *any* state whenever the detector POVM is diagonal:
   `Tr(M_b ρ) = Σ_t A(b|t) ρ_tt`.

**What survives** once (1) is removed and (2) is credited: known tools applied
to readout, worked ibm_hanoi numbers (the linear rule of thumb overestimates
27-qubit parity error by 37%), and a crosstalk expansion weaker than Hamilton
et al.'s 2020 cumulant reconstruction. That is unlikely to clear QST review,
and an accepted version would print a false statement.

**Recommendation:**

1. Log in to check the status.
2. If it is still under review, withdraw it, or at minimum send the editor a
   correction.
3. If a decision has already arrived, record it in `~/github/pubs` and don't
   resubmit the paper as research.
4. Reuse the material as a monograph section, a blog post and a video.

## What is publishable

| Item | Status | Action |
|---|---|---|
| GBFPlus adjacent-domain disclosure | The only verified new result. Zenodo 10.5281/zenodo.23497466. Entropy Comment awaiting a fee reply (APC CHF 2,600; budget 0) | If no waiver, fold into idea A. Notify Qin et al. directly either way |
| Quantum readout | Above | Withdraw or correct |
| Relations ("Error contracts…") | Corrected scoped synthesis (Codex revision, uncommitted). Novelty unestablished | Becomes monograph ch12. No standalone submission |
| Sets, composition, classification, entropy | KNOWN (Warner, Carter, Pagh–Rodler). Entropy states a solved problem as open | Freeze with erratum |
| BHF, PHF | KNOWN (seed search, Dietzfelbinger–Pagh). BHF formula error | Freeze with erratum |
| Maps | PARTIAL. Critical §6.6 error | Freeze with erratum |
| Data type (`bernoulli<T>`) | PARTIAL against Decaf (not cited anywhere). Rough | Only research seed; see idea C |
| Dependence calculus, query planner | Negative results | Done |

## New publishable work, ranked

Ranked under the stated constraints: a conventional peer-reviewed article
(which counts for the PhD), no fees, no arXiv, side-project effort.

**A. An attack-pattern paper grown from the GBFPlus finding.** This has the
best value per unit of effort.

- **The pattern.** The GBFPlus flaw looks like an instance of a general one.
  XOR-share and filter-cell constructions look uniform cell by cell. But
  publishing occupancy, insertion counts or several releases lets an observer
  recombine the shares.
- **Screening.** Check recent (2023–2026) papers that rest confidentiality
  claims on garbled Bloom filters, Bloom-encoded record linkage, OKVS, or
  cuckoo/xor filters in ledger, IoT and health systems. Each screen takes about
  one agent-day with the existing exhaustive-check harness.
- **Stopping rule.** Stop after about 10 screens with no hits.
- **Outlets.**
  - One confirmed flaw: a Comment in the target journal. IEEE Transactions
    regularly publish "Comments on …" papers and are free on the traditional
    route.
  - Three or more instances: a standalone paper for a free security venue, such
    as IEEE TDSC/TIFS (traditional route), *Computers & Security* (subscription
    route), or ACM TOPS ($0 if SIUE's ACM Open participation is confirmed).
- **Fit.** It sits in cybersecurity, the stated research focus.
- **Etiquette.** Contact the original authors before publishing.

**B. A survey, "Two-sided error in approximate membership and retrieval," for
ACM Computing Surveys.**

- **Why.** This is the honest form of the program's real contribution: one
  channel model organizing Bloom filters, retrieval and PHF, approximate
  queries, readout and encrypted indexes, with lineage credited and limits
  stated (dependence, adaptivity, two-rate non-closure).
- **Cost.** Free if SIUE's ACM Open listing is verified; otherwise $1,450
  ($950 for members).
- **Effort.** Weeks, not days. Most of it can be drawn from the monograph and
  the verified bibliography. Expect a long review cycle.

**C. Research long shot: confusion-matrix type qualifiers.**

- **The gap.** Decaf types carry one correctness probability. A sound two-rate
  qualifier system over sum, product and function types, with inference and an
  evaluation, would be new.
- **Venue.** OOPSLA or ECOOP (ACM Open).
- **Effort.** Months. Not low-hanging.

**Not recommended:** further per-result papers from the existing nine, a
standalone relations calibration note, or the query planner.

## Representing the body of work

Present it as what it is: a unification with credited lineage, an executable
companion, and an honest boundary map. Candor about predecessors builds
credibility; it is not a concession.

1. **The monograph is the canonical artifact.** It needs:
   - per-chapter lineage notes crediting the predecessors above;
   - a fuller bibliography (69 entries; Carter, Pagh–Rodler, Bloomier, xor and
     ribbon filters, BBHash and probabilistic databases are missing);
   - a real preface, appendices A–C written or cut, figures (currently none)
     and an index;
   - ch12 resynced to the corrected relations paper;
   - an audit for any "two rates through a tree" statements (ch3, ch6, ch9);
   - a license decision: the README says CC BY-NC-SA, `docs/PROVENANCE.md`
     says all rights reserved with KDP intent.

   Then mint a Zenodo DOI, keep the free HTML on metafunctor, and optionally
   print via KDP (AI disclosure required). Self-publishing is the realistic
   route: Now Publishers / Foundations and Trends forbids AI-drafted text, and
   MIT Press Direct to Open is highly selective.
   - **Title.** Lead with field terms ("approximate membership", "two-sided
     error") and keep "Bernoulli types" as the framework's name. "Bernoulli
     filter" (target tracking) and "Bernoulli map" (dynamical systems) are
     established terms that capture search results.
2. **Freeze the paper fleet.**
   - Publish one final round of Zenodo versions, each with an erratum and a
     "superseded by monograph ch. X" note. Quantum v5, relations v5, entropy,
     BHF and maps currently state known-wrong things in public.
   - Archive the ten standalone GitHub repos (read-only, README pointing to the
     monograph) and retire the subtree-push workflow.
3. **Package.**
   - Refresh the README, `__init__` and `SYNTHESIS.md` (all stale). Fix the
     Exp 14 generator, which regenerates the inverted May conclusion.
   - Release `bernoulli-types` 0.3.0 on PyPI.
   - JOSS later: it needs 6 months of public history and evidence of research
     impact. It gives peer review and a DOI but does not count for the PhD.
   - **One real-system demo:** error-budgeted approximate semi-joins on DuckDB
     over TPC-H, wrapping real filter libraries (pyxorfilter, rbloom) as
     membership oracles. The demo predicts query-level false-match rates and
     compares them with exact answers. The punchline is the relations
     calibration finding: sizing each filter at a 5% FPR gives a 0.329 query
     error on a valid worst-case profile, and calibrated sizing restores about
     0.05. It also works as a blog post, a notebook and a video.
4. **metafunctor: make the hub the single front door.**
   - **Links.** The hub links to the private `queelius/bernoulli` and an
     unpublished PyPI name, both 404. Either make the monorepo public after the
     errata, or link the public per-paper repos and Zenodo.
   - **Tags.** Normalize them. The "notes and posts" list shows one post
     because tags are split across `bernoulli-model`, `bernoulli model`,
     `bernoulli-types`, `bloom-filters` and others.
   - **Series page.** Create `content/series/bernoulli-types/_index.md`.
   - **Stale pages.** Retire or redirect the Jan-2026 `/papers/` pages that the
     trapdoor triage disowned, and the empty project stubs.
   - **Lineage.** Add a lineage section to the hub.
   - **Trapdoor hub.** It still says TOPS is "under review"; pubs records a
     rejection and a PeerJ submission.
5. **YouTube: an 8–10 episode playlist drawn from the monograph.** Pedagogy is
   the program's strength. Hook: one equation explains Bloom filters,
   randomized response and QEC syndrome bits.
   - Restore `_archive/probabilistic-approximate-data-structures`.
   - Add `_books/bernoulli-types/book.yaml`.
   - Embed `{{< youtube-series "bernoulli-types" >}}` on the hub.
   - Fix the stale `source_posts` paths.
6. **research-records:** add one record for the monograph with
   `novelty: synthesis` and a `predecessor_credit` list, so the honest framing
   sits next to GBFPlus in machine-readable form.

## Archive and start a fresh monorepo?

No. A fresh monorepo would move the same known results to a new location; the
problem is the claims, not the layout. Restructure in place:

- `book/` and `bernoulli-py/` stay living.
- `papers/` becomes a frozen archive.
- `.research/` is the audit trail; commit it.

New research lines live where they belong: idea A in a security-focused repo
(or trapdoor-computing), idea C in its own repo if pursued.

## Housekeeping (local, reversible)

- `.research/` is entirely untracked, yet the GBFPlus Zenodo record names it as
  the owning evidence. Commit it, checking first for large binaries
  (`qa/*.png`, coverage files).
- Commit the Codex relations revision. It is complete: the build gives 27
  pages, 540 tests pass, and there are no unresolved references. Its tests need
  numpy, which the `bernoulli-py/.venv` lacks.
- Fix the Exp 14 generator and SYNTHESIS Thread A, claim 6.
- The clerk mail cache has been stale since 2026-06-12. Re-authenticate
  (`clerk accounts auth`) to track QST and Entropy correspondence.
- In `CLAUDE.md`: there are 10 papers, not 9; maph now lives at
  `~/github/bijou/lapidary`.

## Sequence

1. **Week 1 (low effort):**
   - housekeeping;
   - the QST decision;
   - the Entropy reply;
   - notifying Qin et al.;
   - the site front-door fixes.
2. **Weeks 2–3:** attack screening for idea A, about a day per candidate, with
   the stopping rule.
3. **In parallel, slower:**
   - monograph apparatus, then a v1.0 DOI;
   - package 0.3.0 and the DuckDB demo, then a blog post and the first videos.
4. **Optional:** the CSUR survey (idea B) once monograph v1 exists, as a
   compressed derivative of it.

## Decisions only Alex can make

1. QST: withdraw, correct, or wait.
2. Whether Comments and surveys count toward the PhD (ask the advisor). This
   decides whether ideas A and B are worth the time.
3. The monograph's license, and whether to print via KDP.
4. Whether to make the bernoulli monorepo public.
5. Whether to start the attack screening (idea A).
