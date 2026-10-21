# Independent methods and reproducibility review — round 2

**Date:** 2026-10-15. **Final verdict:** M1–M5 are resolved; no remaining methods or reproducibility blocker was found for the stated conditional counterexample. **Scope:** revised portable supplement, shared manuscript body, rendered venue PDF, and standalone source/supplement ZIPs. No prior review from another reviewer was read. The initial tested snapshots and their evidence are preserved below; the completed focused final recheck is recorded at the end.

## Initial round-2 snapshot and verification

| Reviewed object | SHA-256 |
|---|---|
| Supplement ZIP | `1e6ede360cfe120c3ab3acbd8c966034fa2669be654b7a65a843733efc86d556` |
| Source ZIP | `e12017495f6f64780104ef118d0de763c38b1355481121140bdac347fc9a054c` |
| Captured venue PDF | `5ba44973cd90a4e16e33248e89a6934a94ca99d7cb64d6f11911d39f07cd49bf` |
| Shared body at initial capture | `26e7cf8a78e9f6e07802a5bc4d3a70cd9bcf7b34dbb0498f86466fdda2523fb8` |
| `reproduce.py` | `e0f2ab0bbd2fc3c045559a65710ed21df7436cec12adbbe41b818b87d6054fe8` |
| `test_reproduction.py` | `f033600b7474159645a7bbd23f0c55713115a3b1acd88c85e77e04522ec7c37f` |
| `gbfplus_probe.py` (unchanged) | `ffe9e4c05a73787a2b7ffbb2337bcda118d1eaa0a2a4783d99255be216e1100a` |
| `reference-results.json` (unchanged) | `70d6bcd182f2800ac8e5e69f2a99bcfc76c41cf6414868dc660e263b155dd1f5` |

I extracted both archives into `/tmp/gbfplus-methods-review-r2-n53qewnm`, read the actual shared `body.tex`, and inspected rendered PDF pages 2–4 containing the representation, proofs, example, and complete reproduction section. The source archive builds cleanly, and the text of its five-page PDF exactly matches the captured venue PDF. The shared body subsequently changed during the coordinator's ongoing edits; this does not invalidate the captured archive/PDF pair, but final package consistency must be checked against the final files.

Using `/home/spinoza/github/bernoulli/bernoulli-py/.venv/bin` on the clean extraction:

- `python -S reproduce.py` reproduced every deterministic experimental field, including all 256 singleton cases, 1,024 disjoint cases, and 64 stored arrays. I independently reconstructed each full seeded target and array, including prefixes.
- `python -m coverage run --branch --source=gbfplus_probe,reproduce -m pytest -q` passed **16 tests**. Ruff and strict mypy also passed.
- Pytest alone measured **99%** overall coverage: 122/123 statements and 49/50 branches, with the guard's exception path unrecorded because its tests launch subprocesses. An independently executed, expected-failure optimized run under appended coverage exercised that path, producing **123/123 statements and 50/50 branches**. This is separate negative-test execution, not a claim that pytest alone measured 100%.
- A 20-case independent rejection matrix covered `-O`, `-OO`, and `PYTHONOPTIMIZE=1` or `2`, each through script, `-m`, imported result function, imported experiment function, and `runpy`. Every case exited nonzero with the explicit assertion-mode diagnostic and created no results JSON. An existing results sentinel remained untouched.
- The hand-derived full-array oracle passed for the real implementation and failed under an independently injected prefix-only fault, even though the low suffix bits were untouched.
- Experiment ASTs are identical to both round 1 and the original historical driver. The historical driver and unchanged-file hashes match the recorded provenance.

Evidence: [extraction.json](evidence-round-2/extraction.json), [challenge-results.json](evidence-round-2/challenge-results.json), [command-results.json](evidence-round-2/command-results.json), [coverage-commands.json](evidence-round-2/coverage-commands.json), [coverage.json](evidence-round-2/coverage.json), and [tested-file-hashes.json](evidence-round-2/tested-file-hashes.json). The independent challenge is preserved as [challenge_revision.py](evidence-round-2/challenge_revision.py).

## M1–M3 dispositions

**M1 — Resolved for every documented source invocation and ordinary imported use.** The top-level `sys.flags.optimize` guard runs before experiment functions are defined, preventing all previously demonstrated `-O`/environment false-success cases. The new subprocess regression tests check nonzero status, the diagnostic, and absence of output. M5 below records an additional optional hardening case outside the documented source workflow; it does not reopen the original supported-invocation failure.

**M2 — Resolved.** The shared reproduction section explicitly fixes supports and prefixes for the small enumerations, names seeds 0–63, and labels the larger row as `c=1`. Table 1 gives the tested equality and input class, uses “Mismatches,” and explains that the figures are finite implementation checks. The supplement gives `4 × 8² = 256`, `4² × 8² = 1,024`, the actual supports/prefixes, and the seeded drawing protocol. This is sufficient to reconstruct the design without guessing which quantities varied.

**M3 — Resolved.** The new compact oracle checks exact arrays before and after an overlapping insertion, including the entire prefix and a zero occupied word. My independent prefix-only mutation caused it to fail. Coverage is expressly limited to the small implementation and does not claim validation of cryptography, the ledger, or release policy. There is no need to add the round-1 review's exhaustive transition enumeration to the Comment or its released tests.

## Additional findings from the round-2 challenge

### M4 — Minor provenance clarification: specify the AST serialization normalization

**Location:** `supplement/provenance.json`, `unchanged_functions`; README's syntax-tree checksum description.

The recorded hashes are reproducible after omitting the empty `FunctionDef.type_params` field that Python 3.12 added to the AST. With unnormalized `ast.dump(node, include_attributes=False)` under the stated Python 3.12.3 environment, the hashes are instead:

- `exact_gbf_checks`: `a03fa3e0a69de3bc70c683332d7406b7050059a40130401131d82f69fba38f73`
- `stored_constructions`: `3b2f06d4d96f1da1bd25d8b2d5aee7f02b760847772803cf8a644d2f4f42e5a5`

Removing that empty field yields exactly the historical `2c311fc...` and `2c4b710...` values. This is serialization-version ambiguity, not evidence of changed functions. Document the exact normalization and UTF-8 SHA-256 procedure, or use new explicitly versioned hashes. Verification should reconstruct both recorded function hashes using the declared procedure from the released source. The coordinator has accepted this clarification.

### M5 — Optional hardening: guard the module's compilation mode directly

**Location:** `supplement/reproduce.py:24–27` in the initial round-2 snapshot.

An external caller can precompile the source using `py_compile.compile(..., optimize=1)` and then run that bytecode with an unoptimized interpreter. In this deliberately nonstandard case, `sys.flags.optimize` is zero although the experiment assertions were removed. The initial round-2 guard therefore permits exit 0 and a JSON containing 64 empty arrays and zero reported singleton errors. The archive ships source, not such precompiled bytecode, and all documented source paths are already protected; this is optional hardening rather than a new scientific or release blocker.

Using `if not __debug__:` checks the actual compilation mode of the module and handles this edge while preserving the audited experiment function ASTs. The coordinator has accepted that change and a focused regression test. Verification should run externally precompiled optimized code under unoptimized Python and observe the same explicit nonzero/no-output rejection as the ordinary optimized modes.

## Focused final recheck

I extracted the final archives afresh into `/tmp/gbfplus-methods-final-vxxeikdm`. Every extracted source and supplement member matches the corresponding live file byte for byte. These are the final reviewed versions:

| Object | SHA-256 |
|---|---|
| Supplement ZIP | `b53663fc475519a669af2f0c8831dc6a91e73333dc05114ef4263a232fc2727b` |
| Source ZIP | `054a7028902acaaf8a250158d6b365ef639f91374a2ed10c614ce7d1f32ddd09` |
| Venue PDF | `596500fa15a03357c85284e436d73a5fd3d894bc20d069dfb0bc444c6bb91810` |
| Shared/packaged `body.tex` | `f82b746de224af858f5f77087027f17ce2a51b52b6fc50a00060472dfb19bf27` |
| `reproduce.py` | `b6a3ccc1a021f7340ddf924f86178d8409c24a38676c2eaf612441e093b4fc1f` |
| `test_reproduction.py` | `474f8340aedcd765af768d2ef71e0efecfa987f9e80ff7c51d65658e5fc1e80a` |
| `provenance.json` | `2e917455f0dac52fef67445eee261964f6998600c10e8e17175f75fa86ff4a32` |

**M1 and M5 are fully closed.** The final `if not __debug__:` guard rejects all 20 optimized source/import entry-point cases already described, and the additional externally precompiled optimized bytecode case now exits 1 and creates no result file. Existing output remains untouched. The new distributed bytecode regression checks the diagnostic as well as the exit status and absence of JSON.

**M4 is closed.** `function_hash_method` now specifies `ast.dump` arguments, omission of only an empty `FunctionDef.type_params`, UTF-8, no trailing newline, SHA-256, CPython 3.12.3, and the deliberately narrow purpose of this historical normalization. Applying that procedure independently reproduces both recorded function hashes. The evidence retains the unnormalized hashes and their expected mismatch to distinguish the two serializations; `matches_recorded_without_python312_empty_type_params=true` is the check of the now-declared method. Both functions still have identical ASTs to the historical driver and round 1.

**M2 and M3 remain closed.** The final body and README preserve the clarified experimental design. The hand-derived full-array oracle passes normally and still rejects my prefix-only injected error. The revised prose also makes explicit that an occupied zero contributes to the occupancy count without changing the XOR, and that the masking comparison assumes fresh uniform masks independent of the identifiers and one another.

Final fresh verification:

- **17 pytest cases pass**, including the new precompiled-bytecode regression; Ruff and strict mypy pass.
- Normal `python -S reproduce.py` reproduces all deterministic reference fields and current source hashes. The independent checker reconstructs all **64 complete arrays and targets**. Counts remain **256/0** and **1,024/0** cases/mismatches, with the stated uniformity and disjoint-view checks true.
- Normal-compilation coverage is **121/121 statements and 48/48 branches**. The `__debug__` rejection code is removed at normal compilation and is not part of those totals. Its behavior is verified separately by subprocess rejection tests and the independent 21-case challenge; the README accurately explains that distinction.
- The final source ZIP builds a five-page PDF with no final-log warnings, undefined references/citations, or overfull/underfull boxes. Its extracted text equals the final venue PDF text exactly. I inspected the final rendered methods/table page and read the final body changes; the reproduction claims and counts agree.

Final evidence is separate from the initial round-2 record: [final extraction and member hashes](evidence-round-2/final/extraction.json), [final challenge results](evidence-round-2/final/challenge-results.json), [final commands](evidence-round-2/final/command-results.json), [final coverage](evidence-round-2/final/coverage.json), and [source/PDF consistency](evidence-round-2/final/final-consistency.json).

No further experiment is required for this methods review. The result remains conditional on the specification's public representation and honest-history premises; these finite checks do not assess operational prevalence or a repaired protocol. Final author declarations and the complete review ZIP remain outside this methods sign-off. No external communication or publication has occurred.
