"""Independent review checks; never modifies the reviewed archive or source tree."""

import argparse
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile


def parity(words, bits):
    """Compute XOR by counting set bits in each column, not using XOR folding."""
    return sum((sum((word >> bit) & 1 for word in words) % 2) << bit
               for bit in range(bits))


def expected_update(before, positions, target, free, bits):
    after = list(before)
    empty = [position for position in positions if before[position] is None]
    if not empty:
        return False, after
    for position, value in zip(empty[1:], free, strict=True):
        after[position] = value
    pivot = empty[0]
    after[pivot] = parity([target] + [after[p] for p in positions if p != pivot], bits)
    return True, after


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    artifact = args.artifact.resolve()
    spec = importlib.util.spec_from_file_location("gbfplus_probe", artifact / "gbfplus_probe.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    reference = json.loads((artifact / "reference-results.json").read_text())
    fresh = json.loads((artifact / "reproduced-results.json").read_text())
    result = {
        "python": sys.version,
        "artifact": str(artifact),
        "reviewed_files_sha256": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(artifact.iterdir()) if path.is_file()
        },
    }

    checked = 0
    for row in reference["gbfplus_stored"]["instances"]:
        rng = random.Random(row["seed"])
        positions = rng.sample(range(64), 12)
        domain = rng.getrandbits(20)
        target = (rng.getrandbits(12) << 20) | domain
        free = [rng.getrandbits(32) for _ in range(11)]
        success, expected = expected_update([None] * 64, positions, target, free, 32)
        assert success
        assert positions == row["positions"]
        assert expected == row["cells"]
        assert domain == row["domain"] == row["recovered_domain"]
        occupied = [index for index, value in enumerate(row["cells"]) if value is not None]
        assert set(occupied) == set(positions)
        assert parity([row["cells"][index] for index in occupied], 32) == target
        checked += 1
    assert checked == 64
    result["saved_arrays_independently_reconstructed"] = checked
    expected_fresh = dict(fresh["gbfplus_stored"])
    expected_reference = dict(reference["gbfplus_stored"])
    expected_fresh.pop("repeated_scan_ns_mean")
    expected_reference.pop("repeated_scan_ns_mean")
    assert expected_fresh == expected_reference
    assert fresh["gbfplus_exact"] == reference["gbfplus_exact"]
    result["fresh_deterministic_results_match_reference"] = True

    singleton_cases = 0
    joint_cases = 0
    for domain in range(4):
        for free in itertools.product(range(8), repeat=2):
            actual = [None] * 7
            success, expected = expected_update(actual, (5, 1, 3), 4 + domain, free, 3)
            assert module.insert(actual, (5, 1, 3), 4 + domain, free, 3) == success
            assert actual == expected
            assert parity([value for value in actual if value is not None], 3) % 4 == domain
            singleton_cases += 1
    for first, second in itertools.product(range(4), repeat=2):
        for free in itertools.product(range(8), repeat=2):
            actual = [None] * 7
            _, expected = expected_update(actual, (0, 4), 4 + first, free[:1], 3)
            _, expected = expected_update(expected, (1, 5), second, free[1:], 3)
            assert module.insert(actual, (0, 4), 4 + first, free[:1], 3)
            assert module.insert(actual, (1, 5), second, free[1:], 3)
            assert actual == expected
            assert parity([value for value in actual if value is not None], 3) % 4 == parity([first, second], 2)
            joint_cases += 1
    result["table_cases_checked_against_independent_cell_oracle"] = {
        "singleton": singleton_cases, "two_disjoint": joint_cases,
    }

    # This supplements line coverage with the complete valid two-bit transition
    # space on four cells, including every support order, overlap, and full-support failure.
    transitions = 0
    failures = 0
    for before in itertools.product((None, 0, 1, 2, 3), repeat=4):
        for size in range(1, 5):
            for positions in itertools.permutations(range(4), size):
                empties = sum(before[p] is None for p in positions)
                for target in range(4):
                    for free in itertools.product(range(4), repeat=max(0, empties - 1)):
                        actual = list(before)
                        expected_success, expected = expected_update(before, positions, target, free, 2)
                        actual_success = module.insert(actual, positions, target, free, 2)
                        assert actual_success == expected_success
                        assert actual == expected
                        if actual_success:
                            assert parity([actual[p] for p in positions], 2) == target
                        else:
                            failures += 1
                            assert actual == list(before)
                        transitions += 1
    result["independent_transition_checks"] = {"transitions": transitions, "atomic_failures": failures, "mismatches": 0}

    # The documented command can inherit optimization from the environment.
    with tempfile.TemporaryDirectory(prefix="gbfplus-optimized-review-") as cwd:
        env = dict(os.environ, PYTHONOPTIMIZE="1")
        completed = subprocess.run([sys.executable, "-S", str(artifact / "reproduce.py")],
                                   cwd=cwd, env=env, capture_output=True, text=True)
        optimized = json.loads((Path(cwd) / "reproduced-results.json").read_text())
        result["optimization_counterexample"] = {
            "command": [sys.executable, "-S", str(artifact / "reproduce.py")],
            "environment_override": {"PYTHONOPTIMIZE": "1"},
            "exit_code": completed.returncode,
            "exact": optimized["gbfplus_exact"],
            "stored_arrays": len(optimized["gbfplus_stored"]["instances"]),
            "stored_arrays_with_no_occupied_cells": sum(all(word is None for word in row["cells"])
                for row in optimized["gbfplus_stored"]["instances"]),
            "stored_arrays_with_null_recovery": sum(row["recovered_domain"] is None
                for row in optimized["gbfplus_stored"]["instances"]),
            "example_cells": optimized["gbfplus_stored"]["example_cells"],
        }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
