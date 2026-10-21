"""Independent finite oracle and masking-side-information counterexample.

Run from any directory with the supplement path as argv[1]. Uses no pytest,
assert statements, random sampling, or bundled experiment functions.
"""

import importlib.util
import json
import sys
from collections import Counter
from functools import reduce
from itertools import permutations, product
from operator import xor
from pathlib import Path


supplement = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("probe_under_test", supplement / "gbfplus_probe.py")
probe = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = probe
spec.loader.exec_module(probe)


def require(condition, context):
    if not condition:
        raise RuntimeError(context)


def functional_oracle(before, positions, target, free):
    """Construct the unique residual solution without a mutable share loop."""
    vacancies = tuple(p for p in positions if before[p] is None)
    if not vacancies:
        return False, before
    assigned = dict(zip(vacancies[1:], free, strict=True))
    pivot = vacancies[0]
    others = tuple(before[p] if before[p] is not None else assigned[p]
                   for p in positions if p != pivot)
    assigned[pivot] = reduce(xor, others, target)
    return True, tuple(assigned.get(p, value) for p, value in enumerate(before))


counts = Counter()


def check_transition(before, rows, positions, target, free, bits):
    success, expected = functional_oracle(before, positions, target, free)
    actual = list(before)
    observed = probe.insert(actual, positions, target, free, bits)
    require((observed, tuple(actual)) == (success, expected),
            ("update mismatch", before, positions, target, free, actual, expected))
    counts["updates"] += 1
    if not success:
        counts["atomic_failures"] += 1
        return None
    counts["successful_updates"] += 1
    new_rows = rows + ((positions, target),)
    require(all(old is None or expected[p] == old for p, old in enumerate(before)),
            "overwritten occupied word")
    require(all(reduce(xor, (expected[p] for p in support), 0) == word
                for support, word in new_rows), "full-word row lost")
    occupied = tuple(p for p, v in enumerate(expected) if v is not None)
    union = set().union(*(set(support) for support, _ in new_rows))
    require(set(occupied) == union, "occupancy union mismatch")
    snap = probe.Snapshot(expected, len(new_rows), len(positions), bits)
    got = probe.recover_domain_xor(snap, bits - 1)
    certificate = len(occupied) == len(new_rows) * len(positions)
    want = (reduce(xor, (word for _, word in new_rows), 0) & ((1 << (bits - 1)) - 1)
            if certificate else None)
    require(got == want, ("scan mismatch", new_rows, expected, got, want))
    require(all(probe.recover_domain_xor(snap, bits - 1) == got for _ in range(3)),
            "frozen reads changed")
    if certificate:
        counts["certificate_successes"] += 1
    else:
        counts["overlap_abstentions"] += 1
    return expected, new_rows


# All ordered supports, all two-bit targets, and every free-word assignment
# for every two-attempt history in m=1..4, k=1..m. Failed attempts do not count.
for m in range(1, 5):
    for k in range(1, m + 1):
        supports = tuple(permutations(range(m), k))
        for first in supports:
            for target1 in range(4):
                for free1 in product(range(4), repeat=k - 1):
                    first_state = check_transition((None,) * m, (), first, target1, free1, 2)
                    before, rows = first_state
                    for second in supports:
                        vacancies = sum(before[p] is None for p in second)
                        for target2 in range(4):
                            for free2 in product(range(4), repeat=max(0, vacancies - 1)):
                                check_transition(before, rows, second, target2, free2, 2)

# Arbitrary-length successful histories need not have fresh cells in old rows:
# the new support's zero/one/two overlaps are exercised above. A third row
# tests accumulation across two old constraints with an occupied-zero payload.
state = ((None,) * 5, ())
for support, target, free in (((3, 0), 3, (3,)), ((0, 2), 1, ()), ((2, 4), 2, ())):
    state = check_transition(*state, support, target, free, 2)

# Independent validation of the 64 recorded full words, including prefixes.
# Regenerate target directly from the stated PRNG draw order, never calling
# stored_constructions() or the bundled decoder to calculate the expectation.
import random

saved = json.loads((supplement / "reference-results.json").read_text())
for row in saved["gbfplus_stored"]["instances"]:
    rng = random.Random(row["seed"])
    positions = rng.sample(range(64), 12)
    domain = rng.getrandbits(20)
    prefix = rng.getrandbits(12)
    words = tuple(rng.getrandbits(32) for _ in range(11))
    _, expected = functional_oracle((None,) * 64, tuple(positions), (prefix << 20) | domain, words)
    require(tuple(row["cells"]) == expected, ("stored full-word mismatch", row["seed"]))
    require(row["positions"] == positions and row["domain"] == domain, "PRNG order mismatch")
    require(reduce(xor, (v for v in expected if v is not None), 0) == (prefix << 20) | domain,
            "saved prefix is wrong")
    counts["saved_full_word_arrays"] += 1

# Caution: masks independent of N and each other do not suffice to hide the
# FULL word P||(N xor M) if M is correlated with P. Let P=M for c=1.
mask_views = {}
for domain in range(4):
    views = [(mask << 2) | (domain ^ mask) for mask in range(4)]
    require(Counter(v & 3 for v in views) == Counter(range(4)), "suffix not uniform")
    require(all((v >> 2) ^ (v & 3) == domain for v in views), "counterexample failed")
    mask_views[str(domain)] = views

# Unsupported histories are accepted structurally, as the README warns.
# This is recorded as a rejected theorem objection, not an implementation bug.
unreachable = probe.Snapshot((1, 2, None), 2, 2, 2)
require(probe.recover_domain_xor(unreachable, 1) is None, "unreachable scan result")

print(json.dumps({"counts": dict(counts), "mask_prefix_correlation_views": mask_views,
                  "malformed_history_is_not_validated": True}, indent=2))
