"""Bounded research probe; no new policy or security theorem is claimed.

Construction uses stored bytearrays and SHAKE256-derived locations. Seeds are
independent PRNG samples in experiments; an ideal random oracle is NOT assumed
in empirical results. SQLite is the authoritative processed-ID log.
"""

from __future__ import annotations

import hashlib
import heapq
import json
import math
import random
import sqlite3
import sys
import tempfile
import time
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any


class Policy(str, Enum):
    ARRIVAL = "uniform_arrival"
    ARRIVAL_CACHE = "uniform_arrival_with_verified_positive_cache"
    UNIFORM_DISTINCT = "uniform_distinct"
    HIGH_FREQUENCY = "high_frequency"
    LOW_FREQUENCY = "low_frequency"


def key_bytes(key: int) -> bytes:
    return key.to_bytes(16, "big")


class KeyedBloom:
    """Small actual filter; extra RAM baseline caps hashing at 16 locations."""

    def __init__(
        self, capacity: int, target_fpr: float, seed: int, extra_bytes: int = 0
    ) -> None:
        if capacity <= 0 or not 0 < target_fpr < 1 or extra_bytes < 0:
            raise ValueError("invalid filter dimensions")
        count = max(1, math.ceil(-capacity * math.log(target_fpr) / math.log(2) ** 2 / 8))
        self.bits = bytearray(count + extra_bytes)
        self.hashes = min(16, max(1, round(8 * len(self.bits) / capacity * math.log(2))))
        self.seed = seed.to_bytes(16, "big")

    def positions(self, key: int) -> list[int]:
        raw = hashlib.shake_256(self.seed + key_bytes(key)).digest(8 * self.hashes)
        return [
            int.from_bytes(raw[i : i + 8], "big") % (8 * len(self.bits))
            for i in range(0, len(raw), 8)
        ]

    def add(self, key: int) -> None:
        for position in self.positions(key):
            self.bits[position >> 3] |= 1 << (position & 7)

    def contains(self, key: int) -> bool:
        return all(self.bits[p >> 3] & (1 << (p & 7)) for p in self.positions(key))

    def bitmap(self) -> bytes:
        return bytes(self.bits)

    def payload_bytes(self) -> int:
        return len(self.bits)


def deep_size(value: Any, seen: set[int] | None = None) -> int:
    """Reachable Python object bytes, counting aliases once; not allocator RSS."""
    visited = set() if seen is None else seen
    if id(value) in visited:
        return 0
    visited.add(id(value))
    size = sys.getsizeof(value)
    if isinstance(value, dict):
        size += sum(deep_size(k, visited) + deep_size(v, visited) for k, v in value.items())
    elif isinstance(value, (tuple, list, set)):
        size += sum(deep_size(item, visited) for item in value)
    return size


@dataclass
class Sampler:
    policy: Policy
    budget: int
    seed: int
    arrivals: int = 0
    reservoir: list[tuple[int, int]] = field(default_factory=list)
    heap: list[tuple[int, int, int]] = field(default_factory=list)
    retained: set[int] = field(default_factory=set)
    counts: dict[int, tuple[int, int]] = field(default_factory=dict)
    rng: random.Random | None = field(init=False)

    def __post_init__(self) -> None:
        if self.budget < 0:
            raise ValueError("negative budget")
        self.rng = (
            random.Random(self.seed)
            if self.policy in (Policy.ARRIVAL, Policy.ARRIVAL_CACHE) else None
        )

    def observe(self, key: int, offset: int) -> None:
        if self.budget == 0:
            return
        self.arrivals += 1
        if self.policy in (Policy.ARRIVAL, Policy.ARRIVAL_CACHE):
            if len(self.reservoir) < self.budget:
                self.reservoir.append((key, offset))
            else:
                assert self.rng is not None
                index = self.rng.randrange(self.arrivals)
                if index < self.budget:
                    self.reservoir[index] = (key, offset)
        elif self.policy is Policy.UNIFORM_DISTINCT:
            if key in self.retained:
                return
            priority = self.priority(key)
            item = (-priority, key, offset)
            if len(self.heap) < self.budget:
                heapq.heappush(self.heap, item)
                self.retained.add(key)
            elif item > self.heap[0]:
                removed = heapq.heapreplace(self.heap, item)
                self.retained.remove(removed[1])
                self.retained.add(key)
        else:
            count, first = self.counts.get(key, (0, offset))
            self.counts[key] = (count + 1, first)

    def priority(self, key: int) -> int:
        return int.from_bytes(
            hashlib.blake2b(
                key_bytes(key), key=self.seed.to_bytes(16, "big"), digest_size=16
            ).digest(),
            "big",
        )

    def selected(self) -> list[tuple[int, int]]:
        if self.policy in (Policy.ARRIVAL, Policy.ARRIVAL_CACHE):
            return list(self.reservoir)
        if self.policy is Policy.UNIFORM_DISTINCT:
            return [(key, offset) for _, key, offset in self.heap]
        sign = -1 if self.policy is Policy.HIGH_FREQUENCY else 1
        items = heapq.nsmallest(
            self.budget, self.counts.items(),
            key=lambda item: (sign * item[1][0], self.priority(item[0])),
        )
        return [(key, value[1]) for key, value in items]

    def memory_bytes(self, selected: list[tuple[int, int]], cache: set[int]) -> int:
        structures = (self.reservoir, self.heap, self.retained, self.counts, selected, cache)
        # CPython Random.__sizeof__ includes its fixed C generator state.
        return deep_size((structures, self.rng))

    def packed_metadata_bytes(self, cache_count: int) -> int:
        # 128-bit document ID; 64-bit input offset/count; 128-bit bottom-k priority.
        if self.policy in (Policy.ARRIVAL, Policy.ARRIVAL_CACHE):
            return len(self.reservoir) * 24 + cache_count * 16
        if self.policy is Policy.UNIFORM_DISTINCT:
            return len(self.heap) * 40
        return len(self.counts) * 32


def omitted_probability(repetitions: int, check_probability: Fraction) -> Fraction:
    if repetitions < 1 or not 0 <= check_probability <= 1:
        raise ValueError("invalid omission-law parameters")
    return (1 - check_probability) ** repetitions


def exhaustive_bitmap_invariance() -> dict[str, int]:
    """All four-key streams through length four, 2-bit one-location filters."""
    cases = 0
    for initial_bitmap in range(4):
        for length in range(5):
            for stream in product(range(4), repeat=length):
                for coins in product([False, True], repeat=length):
                    baseline = initial_bitmap
                    audited = initial_bitmap
                    for key, check in zip(stream, coins, strict=True):
                        mask = 1 << (key % 2)
                        if not baseline & mask:
                            baseline |= mask
                        if not audited & mask or check:
                            audited |= mask
                        if baseline != audited:
                            raise AssertionError("bitmap induction failed")
                    cases += 1
    return {"policy_stream_pairs": cases, "counterexamples": 0}


def sequential_history(
    initial: list[int], stream: list[int], checks: list[bool], seed: int
) -> dict[str, Any]:
    bloom = KeyedBloom(100, 0.2, seed)
    processed = set(initial)
    for key in initial:
        bloom.add(key)
    snapshots: list[str] = []
    novel_suppressed = 0
    duplicate_suppressed = 0
    for key, check in zip(stream, checks, strict=True):
        positive = bloom.contains(key)
        if not positive or (check and key not in processed):
            processed.add(key)
            bloom.add(key)
        elif key not in processed:
            novel_suppressed += 1
        else:
            duplicate_suppressed += 1
        snapshots.append(bloom.bitmap().hex())
    return {
        "processed": sorted(processed),
        "bitmaps": snapshots,
        "novel_suppressed": novel_suppressed,
        "true_duplicate_suppressed": duplicate_suppressed,
    }


def synthetic_workload(name: str, initial_count: int = 2000) -> tuple[list[int], list[int]]:
    initial = list(range(initial_count))
    hot_count = max(5, initial_count // 40)
    cold_count = initial_count // 2
    if name == "hot_novel":
        hot = range(initial_count, initial_count + hot_count)
        cold = range(cold_count)
    elif name == "cold_novel":
        hot = range(hot_count)
        cold = range(initial_count, initial_count + cold_count)
    elif name == "mixed":
        hot = range(initial_count - hot_count // 2, initial_count + hot_count // 2)
        cold = range(initial_count // 2, initial_count // 2 + cold_count * 2)
    else:
        raise ValueError("unknown workload")
    stream = list(cold) + [key for key in hot for _ in range(20)]
    random.Random(314159).shuffle(stream)
    return initial, stream


def audit_run(
    initial: list[int],
    stream: list[int],
    policy: Policy | None,
    budget: int,
    seed: int,
    directory: Path,
    extra_filter_bytes: int = 0,
    audit_seed: int = 0,
) -> dict[str, Any]:
    """Batch pass plus pre-output audits; ground-truth sets are evaluator-only."""
    start = time.perf_counter()
    bloom = KeyedBloom(len(set(initial) | set(stream)), 0.05, seed, extra_filter_bytes)
    sampler = None if policy is None else Sampler(policy, budget, audit_seed)
    exact = set(initial)  # Evaluator state, never consulted by the policy.
    source_keys = set(stream)  # Evaluator state, not an algorithm data structure.
    with tempfile.TemporaryDirectory(dir=directory) as temporary:
        connection = sqlite3.connect(Path(temporary) / "processed.sqlite")
        connection.execute("PRAGMA cache_size=-64")
        connection.execute("CREATE TABLE processed (id BLOB PRIMARY KEY) WITHOUT ROWID")
        connection.executemany("INSERT INTO processed VALUES (?)", [(key_bytes(k),) for k in initial])
        connection.commit()
        for key in initial:
            bloom.add(key)
        build_seconds = time.perf_counter() - start
        candidate_keys: set[int] = set()  # Evaluator-only baseline denominator.
        positive_arrivals = 0
        first_pass_start = time.perf_counter()
        for offset, key in enumerate(stream):
            if bloom.contains(key):
                positive_arrivals += 1
                candidate_keys.add(key)
                if sampler is not None:
                    sampler.observe(key, offset)
            else:
                # No exact membership lookup. Successful processing precedes insertion.
                connection.execute("INSERT INTO processed VALUES (?)", (key_bytes(key),))
                exact.add(key)
                bloom.add(key)
        connection.commit()
        first_pass_seconds = time.perf_counter() - first_pass_start
        base_bitmap = bloom.bitmap()
        omitted_before = source_keys - exact
        plan_start = time.perf_counter()
        selected = [] if sampler is None else sampler.selected()
        plan_seconds = time.perf_counter() - plan_start
        audit_start = time.perf_counter()
        checked: set[int] = set()
        exact_checks = 0
        for key, _ in selected:
            if policy is Policy.ARRIVAL_CACHE and key in checked:
                continue
            present = connection.execute(
                "SELECT 1 FROM processed WHERE id=?", (key_bytes(key),)
            ).fetchone()
            exact_checks += 1
            if present is None:
                connection.execute("INSERT INTO processed VALUES (?)", (key_bytes(key),))
                exact.add(key)
                bloom.add(key)
            if policy is Policy.ARRIVAL_CACHE:
                checked.add(key)
        connection.commit()
        audit_seconds = time.perf_counter() - audit_start
        pages = connection.execute("PRAGMA page_count").fetchone()[0]
        page_size = connection.execute("PRAGMA page_size").fetchone()[0]
        stored_count = connection.execute("SELECT COUNT(*) FROM processed").fetchone()[0]
        connection.close()
    omitted = source_keys - exact
    assert bloom.bitmap() == base_bitmap
    assert stored_count == len(exact)
    counts = Counter(stream)
    return {
        "policy": "no_audit" if policy is None else policy.value,
        "seed": seed,
        "audit_seed": audit_seed,
        "budget": budget,
        "exact_checks": exact_checks,
        "exact_lookup_wire_payload_lower_bound": 17 * exact_checks,
        "initial_distinct": len(initial),
        "source_arrivals": len(stream),
        "source_identifier_bytes": 16 * len(stream),
        "input_novel_distinct": len(source_keys - set(initial)),
        "candidate_positive_arrivals": positive_arrivals,
        "candidate_distinct": len(candidate_keys),
        "omitted_before_audits": len(omitted_before),
        "omitted_distinct": len(omitted),
        "omitted_source_occurrences": sum(counts[key] for key in omitted),
        "rescued_distinct": len(omitted_before - omitted),
        "oracle_rescue_upper_bound": min(budget, len(omitted_before)),
        "uniform_distinct_expected_rescues": (
            min(budget, len(candidate_keys)) * len(omitted_before) / len(candidate_keys)
            if candidate_keys else 0.0
        ),
        "processed_total": len(exact),
        "authoritative_bytes": pages * page_size,
        "authoritative_key_payload_bytes": len(exact) * 16,
        "sqlite_configured_page_cache_bytes": 65536,
        "filter_payload_bytes": bloom.payload_bytes(),
        "filter_hash_locations": bloom.hashes,
        "filter_python_state_bytes": deep_size(bloom.__dict__),
        "policy_packed_metadata_bytes": (
            0 if sampler is None else sampler.packed_metadata_bytes(len(checked))
        ),
        "policy_python_state_bytes": (
            0 if sampler is None else sampler.memory_bytes(selected, checked)
        ),
        "build_seconds": build_seconds,
        "first_pass_and_sampler_seconds": first_pass_seconds,
        "final_selection_seconds": plan_seconds,
        "audit_seconds": audit_seconds,
        "total_seconds": time.perf_counter() - start,
        "bitmap_unchanged_by_auditing": True,
    }


def run() -> dict[str, Any]:
    directory = Path(__file__).resolve().parent
    seeds = [random.Random(20261014 + i).getrandbits(64) for i in range(8)]
    audit_seeds = [random.Random(20271014 + i).getrandbits(64) for i in range(8)]
    rows: list[dict[str, Any]] = []
    for workload in ("hot_novel", "cold_novel", "mixed"):
        initial, stream = synthetic_workload(workload)
        for seed, audit_seed in zip(seeds, audit_seeds, strict=True):
            baseline = audit_run(initial, stream, None, 0, seed, directory)
            baseline["workload"] = workload
            rows.append(baseline)
            for policy in Policy:
                result = audit_run(
                    initial, stream, policy, 64, seed, directory, audit_seed=audit_seed
                )
                result["workload"] = workload
                rows.append(result)
            # One conservative comparison uses only packed bottom-k records,
            # excluding Python overhead and the PRNG. It fits within its RAM.
            extra = 64 * 40
            larger = audit_run(initial, stream, None, 0, seed, directory, extra)
            larger["policy"] = "larger_filter_with_bottom_k_packed_RAM"
            larger["workload"] = workload
            larger["extra_filter_bytes"] = extra
            rows.append(larger)
    summary: list[dict[str, Any]] = []
    for workload in ("hot_novel", "cold_novel", "mixed"):
        policies = sorted({str(row["policy"]) for row in rows})
        for policy_name in policies:
            group = [
                row for row in rows
                if row["workload"] == workload and row["policy"] == policy_name
            ]
            fields = (
                "omitted_distinct", "omitted_source_occurrences", "exact_checks",
                "rescued_distinct", "uniform_distinct_expected_rescues", "authoritative_bytes",
                "filter_payload_bytes", "policy_packed_metadata_bytes", "policy_python_state_bytes",
                "first_pass_and_sampler_seconds", "final_selection_seconds", "audit_seconds",
                "total_seconds", "candidate_distinct", "omitted_before_audits",
            )
            summary.append({
                "workload": workload,
                "policy": policy_name,
                "builds": len(group),
                **{f"mean_{field}": sum(row[field] for row in group) / len(group) for field in fields},
            })
    output = {
        "scope": "Controlled synthetic corpus-ingestion model, not a Dolma benchmark",
        "construction_seeds": seeds,
        "audit_seeds": audit_seeds,
        "round_1_bitmap_exhaustive": exhaustive_bitmap_invariance(),
        "singleton_vs_repeated_omission_at_q_point_one": {
            str(frequency): float(omitted_probability(frequency, Fraction(1, 10)))
            for frequency in (1, 10, 100)
        },
        "round_2_rows": rows,
        "round_2_summary": summary,
    }
    (directory / "results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"round_1": output["round_1_bitmap_exhaustive"], "summary": summary}, indent=2))
    return output


if __name__ == "__main__":
    run()
