"""Exact finite counterexamples and construction checks for borrowed ideas."""

from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def check_partitioned_bloom() -> dict[str, str]:
    # One two-cell partition, two distinct inserted and two distinct absent keys.
    outcomes = Counter()
    for h1, h2, q1, q2 in product(range(2), repeat=4):
        occupied = {h1, h2}
        outcomes[(q1 in occupied, q2 in occupied)] += 1
    p = Fraction(sum(n for (a, _), n in outcomes.items() if a), 16)
    both = Fraction(outcomes[(True, True)], 16)
    either = 1 - Fraction(outcomes[(False, False)], 16)
    assert p == Fraction(3, 4)
    assert both == Fraction(5, 8) > p * p
    assert either == Fraction(7, 8) <= 1 - (1 - p) ** 2
    return {"marginal": str(p), "conjunction": str(both),
            "independent_conjunction": str(p * p), "disjunction": str(either),
            "jensen_contract": str(1 - (1 - p) ** 2)}


def check_fingerprint_slots() -> int:
    cases = 0
    # Include equal placement slots; independent fingerprints still factor.
    for slots in product(range(2), repeat=2):
        for stored in product(range(2), repeat=2):
            counts = Counter(
                (q1 == stored[slots[0]], q2 == stored[slots[1]])
                for q1, q2 in product(range(2), repeat=2)
            )
            assert all(counts[outcome] == 1 for outcome in product([False, True], repeat=2))
            cases += 1
    return cases


def check_discrete_threshold() -> dict[str, str]:
    minima = Counter(min(values) for values in product(range(2), repeat=2))
    assert minima == {0: 3, 1: 1}
    # The BHF manuscript's displayed without-replacement formula gives 1,0.
    return {"iid_P_T_0": str(Fraction(minima[0], 4)),
            "iid_P_T_1": str(Fraction(minima[1], 4)),
            "draft_P_T_0": "1", "draft_P_T_1": "0"}


if __name__ == "__main__":
    report = {"partitioned_bloom": check_partitioned_bloom(),
              "fingerprint_conditional_cases": check_fingerprint_slots(),
              "bhf_counterexample": check_discrete_threshold()}
    Path(__file__).with_name("borrowed-model-checks.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    print(json.dumps(report, indent=2))
