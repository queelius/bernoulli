# Independent methods and reproducibility review — round 1

**Date:** 2026-10-15. **Recommendation:** minor artifact revision; no scientific methods blocker found for the Comment's stated, conditional counterexample. Fix M1 before releasing the supplement. M2 and M3 are optional and should not expand the brief Comment into a larger experimental paper.

I reviewed the current venue manuscript and a clean extraction of its source and supplement archives. I did not read previous reviews or the other current reviewers' reports. I made no changes to the reviewed artifact, manuscript, prior evidence, or package core. All new material is in this review directory or my temporary extraction directory.

## What an outsider can establish

The representation and experiment are reconstructible. `None` means an unoccupied cell; integer zero remains an occupied payload. The first empty position is reserved, existing words are retained, subsequent empty positions receive supplied free words, and the reserved value satisfies the full target equation. This agrees with the share-processing portion of published Algorithm 4, including atomic failure when every selected cell is occupied. The fresh publisher PDF has SHA-256 `83d28e4460ac017a9117acbd80f06db37a70dffc04536e8ae68904448efc1417`, matching the supplement's recorded source. I inspected the algorithm on its rendered page 11; the source is the [publisher PDF](https://mdpi-res.com/d_attachment/entropy/entropy-28-00947/article_deploy/entropy-28-00947.pdf).

The manuscript correctly distinguishes the proof from enumeration (`main.tex:169–175`). The disjoint-support result is a deterministic identity conditional on an honest insertion history, an authentic count, distinct positions, and the public occupancy selector. The experiments are implementation checks, not estimates of disclosure probability or a proof of cryptographic privacy. Singleton insertion starts empty, so conditioning on successful singleton insertion does not introduce a rejection bias. The individual-share statement explicitly assumes uniform independent free words and at least two shares. No confidence interval or statistical significance test is needed for the reported exhaustive counts.

The larger examples are 64 independently seeded **singleton** constructions. The seeds are exactly 0 through 63. Each seeded run samples a 12-position support in a 64-cell array, a 20-bit domain, a 12-bit prefix, and eleven 32-bit free words. Seeds supply reproducibility, not cryptographic randomness or a claim of deployment representativeness. Repeated reads use the same frozen tuple; the runner does not miscount those reads as independent experiments. Its optional timing scans the final resident tuple 1,000 times and is clearly excluded from any performance contribution.

The limitations are appropriately explicit. Neither the code nor its coverage establishes honest ledger history, authentic counts, successful-count bookkeeping, cryptographic position derivation, signatures, pairings, finalization policy, deployment frequency, or confidentiality of a repaired protocol. Padding and masking tests concern only the indicated statistic. A snapshot with an adversarially supplied count can pass the decoder's shape condition without certifying any history; both manuscript and supplement already say this. More protocol machinery is unnecessary for this conditional algebraic result.

## Findings

### M1 — Required, minor: the reproduction runner can emit success-shaped results without performing any insertions

**Location:** `supplement/reproduce.py:34–35,46–48,52–54,70–76,84–85`; optimization caveat in `supplement/README.md:23–24`.

**Evidence:** Calls with side effects, including `insert(...)`, occur inside `assert`. With Python optimization, those calls disappear along with their checks. In a separate empty working directory I ran the documented `python -S /path/to/reproduce.py` form with `PYTHONOPTIMIZE=1`. It exited **0**, wrote `reproduced-results.json`, and reported `singleton_cases=256`, `singleton_errors=0`, `disjoint_batch_cases=1024`, and `disjoint_batch_errors=0`. All 64 saved arrays were entirely unoccupied, every recovered domain was `null`, and the example array was also empty. The uniformity and joint-support flags were false, so a reader inspecting all fields could detect the inconsistency; the headline zero-error counts nevertheless remain misleading.

The README warns against `-O`, which reduces the severity. It does not make the executable fail safely, and the environment variable activates the same behavior without appearing in the documented command. This is an artifact robustness defect, not a counterexample to either proposition or to the correctly configured run.

**Remedy:** The smallest sufficient fix is an explicit early check that raises a clear exception when assertions are disabled, before any experiment or result writing. Alternatively, move required work outside assertions and use ordinary validation exceptions or calculated failure counts. Do not preserve historical function hashes at the expense of correct execution; record any changes accurately and regenerate the archives and relevant verification hashes.

**Verification criterion:** From fresh extracted archives and empty working directories, normal `python -S reproduce.py` must reproduce all deterministic reference fields. Both `python -O -S reproduce.py` and the `PYTHONOPTIMIZE=1` form must either perform real checked construction successfully or exit nonzero with an explicit diagnostic and no new results file. Add a focused subprocess regression test. Existing normal-mode checks must remain green.

**Evidence file:** [independent-check-results.json](evidence-round-1/independent-check-results.json), `optimization_counterexample`.

### M2 — Optional: state the enumeration conditioning and singleton seed design beside the counts

**Location:** `main.tex:184–194`; `supplement/reproduce.py:29–48,64–78`; supplement README expected-results table.

**Evidence:** The first count is `4 × 8² = 256`: four suffixes, fixed one-bit prefix 1, fixed support `(5,1,3)` in seven cells, and every pair of 3-bit free words. The second is `4² × 8² = 1,024`: fixed disjoint supports `(0,4)` and `(1,5)`, fixed prefixes 1 and 0, all suffix pairs, and one free word for each insertion. The last row contains 64 singleton constructions, not a batch-size sweep. The code makes all of this unambiguous, and the existing table is not false, but the conditioning is less visible in the paper itself.

**Remedy:** Add `c=1` to the 64-array row. One short caption or methods clause can say that the exact enumerations fix supports and prefixes; put the two count factorizations and seeds 0–63 in the supplement README. Do not add another table or a synthetic prevalence experiment.

**Verification criterion:** A reader can derive 256 and 1,024 and identify the 64 runs as singletons without reverse-engineering the Python loops. The reported counts and conclusions remain unchanged.

### M3 — Optional: retain one compact full-array oracle check; do not overinterpret 100% coverage

**Location:** `supplement/test_gbfplus_probe.py:13–46`; `supplement/test_reproduction.py:16–37`; supplement README tests-and-coverage section.

**Evidence:** The packaged tests pass with 100% measured statements and branches in the 120-statement probe/runner. This establishes execution coverage, not independence from the implementation or coverage of the original protocol. The exact recovery loops primarily test suffixes through the same decoder, and the saved-output comparisons intentionally test regression against outputs of the same implementation. There are useful independent full-row XOR checks for the overlap example, so this is not an absence of all external invariants.

For this review, an independently written bit-column parity oracle reconstructed every saved array, checked the full target including its prefix, and agreed on all 244,816 valid two-bit insertion transitions on four cells. These include every support order, empty/occupied state, valid target and required free-word assignment; 82,496 were atomic full-support failures. I found **zero mismatches**. This is supplemental review evidence, not a new manuscript result or a reason to enlarge Table 1.

**Remedy:** If strengthening the distributed tests, keep a small direct check of the entire stored array or full target using an independently computed expected value, including an occupied zero and an overlapping insertion. Retaining the full review enumeration in the release is unnecessary. Preserve the present limitations around coverage and avoid presenting the percentage as protocol validation.

**Verification criterion:** A deliberate corruption of a target prefix or of an existing occupied word must be caught even when the suffix decoder still returns the expected domain. Any added test should remain concise and mathematically motivated.

## Fresh verification performed

Extraction root: `/tmp/gbfplus-methods-review-osxxcyi4`. The archive members match the current venue source and supplement byte for byte. Archive hashes and file lists are recorded in [extraction.json](evidence-round-1/extraction.json); current-tree comparisons are in [package-comparison.json](evidence-round-1/package-comparison.json).

The Python/tool executables were reused from `/home/spinoza/github/bernoulli/bernoulli-py/.venv/bin`. Coverage data was isolated under this review's `evidence-round-1/.coverage`.

| Check in clean extraction | Fresh result |
|---|---|
| `python -S reproduce.py` | Exit 0; every deterministic experimental field matches the reference, excluding only the explicitly variable timing |
| `python -m coverage run --branch --source=gbfplus_probe,reproduce -m pytest -q` | 13 passed |
| `python -m coverage report -m` | 120/120 statements; 48/48 branches; no missing lines or partial branches |
| `ruff check .` | Passed |
| `mypy --strict gbfplus_probe.py reproduce.py test_gbfplus_probe.py test_reproduction.py` | Passed, four files |
| Independent array reconstruction | All 64 seeded arrays, supports, domains, recovered values, and full targets agree |
| Independent table checks | 256 singleton and 1,024 disjoint cases agree with the full-cell oracle |
| Independent transition enumeration | 244,816 transitions, including 82,496 atomic failures; zero mismatches |
| `make` in clean source archive | Exit 0; five-page PDF; final log has no undefined references/citations, warnings, or overfull/underfull boxes |
| Optimized reproduction | Reproduces M1: exit 0 with omitted insertions and misleading zero-error counts |

The independent verifier and its results are [independent_check.py](evidence-round-1/independent_check.py) and [independent-check-results.json](evidence-round-1/independent-check-results.json). Exact command results, coverage JSON, final build logs, and a fresh reproduced JSON are also retained in `evidence-round-1/`.

No package-core code changed, so the unrelated whole-project pytest suite was not rerun. I did not assess the other literature comparisons, journal eligibility, author declarations, novelty, or publication decisions. The initial web-reader requests could not retrieve the publisher page/PDF; a direct read-only publisher PDF download succeeded and matched the stated hash. No external communication or publication occurred.
