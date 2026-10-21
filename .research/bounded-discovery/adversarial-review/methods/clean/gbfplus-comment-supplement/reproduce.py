"""Portable reproduction of Table 1; no repository or third-party runtime imports.

The two experiment functions are copied unchanged from the audited driver.
See provenance.json for the original file hash and syntax-tree checksums.
"""

from __future__ import annotations

import hashlib
import json
import platform
import random
from collections import Counter
from functools import reduce
from itertools import product
from operator import xor
from pathlib import Path
from time import perf_counter_ns

from gbfplus_probe import Snapshot, insert, recover_domain_xor


if not __debug__:
    raise RuntimeError(
        "This reproduction requires assertions: run without -O/-OO and unset PYTHONOPTIMIZE."
    )



def exact_gbf_checks() -> dict[str, object]:
    singleton_cases = 0
    disjoint_cases = 0
    view_supports: dict[int, set[tuple[int | None, ...]]] = {}
    marginals_uniform = True
    for domain in range(4):
        views: set[tuple[int | None, ...]] = set()
        marginals: list[Counter[int | None]] = [Counter() for _ in range(3)]
        for words in product(range(8), repeat=2):
            cells: list[int | None] = [None] * 7
            assert insert(cells, (5, 1, 3), 4 | domain, words, 3)
            assert recover_domain_xor(Snapshot(tuple(cells), 1, 3, 3), 2) == domain
            views.add(tuple(cells))
            for marginal, index in zip(marginals, (5, 1, 3), strict=True):
                marginal[cells[index]] += 1
            singleton_cases += 1
        marginals_uniform &= all(counter == Counter({word: 8 for word in range(8)})
                                 for counter in marginals)
        view_supports[domain] = views
    for first, second in product(range(4), repeat=2):
        for words in product(range(8), repeat=2):
            cells = [None] * 7
            assert insert(cells, (0, 4), 4 | first, words[:1], 3)
            assert insert(cells, (1, 5), second, words[1:], 3)
            assert recover_domain_xor(Snapshot(tuple(cells), 2, 2, 3), 2) == first ^ second
            disjoint_cases += 1
    return {
        "singleton_cases": singleton_cases,
        "singleton_errors": 0,
        "disjoint_batch_cases": disjoint_cases,
        "disjoint_batch_errors": 0,
        "all_individual_share_marginals_uniform": marginals_uniform,
        "two_recipient_view_support_sizes": [len(view_supports[i]) for i in (1, 2)],
        "two_recipient_view_supports_disjoint": view_supports[1].isdisjoint(view_supports[2]),
        "interpretation": "Finite verification of proved identities, not a sampled privacy proof.",
    }


def stored_constructions() -> dict[str, object]:
    instances: list[dict[str, object]] = []
    for seed in range(64):
        rng = random.Random(seed)
        positions = tuple(rng.sample(range(64), 12))
        domain = rng.getrandbits(20)
        target = (rng.getrandbits(12) << 20) | domain
        cells: list[int | None] = [None] * 64
        assert insert(cells, positions, target,
                      tuple(rng.getrandbits(32) for _ in range(11)), 32)
        # Count is one only after the successful insertion above.
        snapshot = Snapshot(tuple(cells), 1, 12, 32)
        recovered = recover_domain_xor(snapshot, 20)
        assert recovered == domain
        assert recover_domain_xor(snapshot, 20) == recovered  # frozen reuse
        instances.append({"seed": seed, "positions": positions, "cells": cells,
                          "domain": domain, "recovered_domain": recovered})
    started = perf_counter_ns()
    for _ in range(1000):
        recover_domain_xor(snapshot, 20)
    elapsed = perf_counter_ns() - started
    reference_cells: list[int | None] = [None] * 7
    assert insert(reference_cells, (5, 1, 3), 5, (2, 7), 3)
    assert reduce(xor, (v for v in reference_cells if v is not None), 0) == 5
    return {
        "lambda": 32, "domain_bits": 20, "kappa": 12, "m": 64,
        "parameter_provenance": "Word/domain widths and kappa from paper Sec. 6.3; m=64 is this probe's example, not its benchmark configuration.",
        "instances": instances,
        "example_cells": reference_cells,
        "example_target_binary": "101", "example_domain_binary": "01",
        "repeated_scan_ns_mean": elapsed / 1000,
        "timing_scope": "Descriptive CPython scan of one already resident 64-cell tuple; excludes ledger access, parsing and verification. No performance contribution claimed.",
        "randomness": "64 separate seeded Python PRNG constructions; exact theorem does not require a computational randomness assumption.",
        "implementation_scope": "Actual stored share arrays and Algorithm 4 update only, not pairings, signatures, ledger or finalization implementation.",
    }

def reproduce() -> dict[str, object]:
    here = Path(__file__).resolve().parent
    return {
        "schema_version": 1,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "source_sha256": {
            name: hashlib.sha256((here / name).read_bytes()).hexdigest()
            for name in ("gbfplus_probe.py", "reproduce.py")
        },
        "gbfplus_exact": exact_gbf_checks(),
        "gbfplus_stored": stored_constructions(),
    }


if __name__ == "__main__":
    output = Path.cwd() / "reproduced-results.json"
    output.write_text(json.dumps(reproduce(), indent=2) + "\n")
    print(output)
