# Independent review and resolution

Reviewer: separate `planner_review` agent, read-only mathematical, code, and
experimental audit. Reviews completed 2026-10-14. Root implemented fixes only
after reproducing findings with failing regressions.

| Finding | Evidence | Resolution |
|---|---|---|
| Runtime aliases invalidate two-row guarantees | Same-row query gave 2630/4096 FPs against a nominal 4.64% bound | execute rejects equal resolved canonical rows; regression test |
| Out-of-domain candidates alias inserted tuples | With domain size 2, candidate 2 converts a row 0 tuple into a row 1 true tuple; FP=1 | Validated CandidateSet checks integer domain before encoding; runtime checks declared plan domain |
| Larger C bypassed allocated capacity | Original Method did not retain K | Method carries max_candidates and domain_size; runtime checks both |
| Normal intervals collapse at zero observations | n=32 zero samples gave [0,0] | Bounded-mean Chernoff/KL 95% interval plus explicitly diagnostic SE band; 32 zero samples give upper endpoint 0.108881 |
| Optional unavailable filter removes valid plans | Fuse width greater than 16 bits; later zero dyadic Bloom rate/finite-width exhaustion | Capability filtering retains exact fallback; tests at targets 10^-6, 10^-12, 10^-18 |
| Partial-row implementation overclaim | FrozenRows has no presence field | Total-row implementation scope stated; presence-aware extension remains theoretical |
| Fixed-C benchmark omitted a simple cached flag baseline | One exact membership-in-C bit per row can enable cheaper query | Pilot retained as failed approach; final workload varies candidate parameters |
| Duplicate candidate capacity counted raw length | Three copies of four candidates incorrectly planned capacity 12 | Capacity derived from the same canonical CandidateSet used at execution |

The reviewer independently repeated all theorem checks, all 67 then 70 unit tests,
and Bernoulli outcome checks of the new interval for seven sample sizes and 999
probability values (maximum observed noncoverage 0.02780). This finite interval
check supplements, rather than proves, the Chernoff argument.

The final review found no remaining material issue in the scoped benchmark.
It checked saved workload counts, byte arithmetic, build-zero payload hashes,
and measured-source provenance. It confirmed the 880-byte / 0.5104% manifest
saving against exact IDs, 97.06 versus 12.17 μs including preparation, and the
6-byte sharp-over-union saving. It warned against claiming all empirical
rates meet 5%, treating nominal Fuse assumptions as finite certificates, or
presenting prototype timing ratios as optimized throughput.

## Validation record

- New artifact tests: 70 passed.
- New tests plus borrowed filter/mathematical regression tests: 610 passed.
- Theory: 19502 negative profiles, 384 independent noise-oracle cases,
  1100 heterogeneous cases, 100 one-hot cases, 327 linear hash cases,
  625 four-point images over F5, 240 queries over all 2401 cubics over F7.
- All 2304 saved payloads rebuilt; exact bounds and retry counts reproduced;
  5760 build-zero query outcomes reproduced by current code.
- Ruff passes for all current research code and scripts. Strict mypy and
  `cc -Wall -Wextra -Werror` pass for the fuse bridge/wrapper (the exploratory
  Python harness is not claimed to pass strict mypy).
- Current new-code statement coverage 672/723 = 92.95%; branch coverage
  220/262 = 83.97%; combined 90.56%. Uncovered lines include CLI orchestration (exercised
  by the measured run outside coverage), malformed-input guards, and native
  allocation/retry failures. No attempt is made to force OOM or enormous arrays.
- Charts rendered and inspected; no paper/PDF manuscript was regenerated.

The final driver differs from the measured source only in the subsequently
reviewed tiny-target capability handling and duplicate-candidate capacity.
Neither condition occurs in saved workloads. The exact original source hashes
are preserved in measured-source/, and full artifact rebuilding checks that
the current implementation produces the same payloads and representative
answers. Recorded timings are from the archived measured driver.
