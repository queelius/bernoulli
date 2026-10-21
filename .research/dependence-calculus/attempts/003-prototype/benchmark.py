"""Reproduce synthetic inference comparisons; no physical filter performance claim."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import random
import statistics
import time
import tracemalloc
from collections import Counter
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass
from functools import partial
from itertools import combinations
from pathlib import Path

from contracts import (
    DNF,
    Bounds,
    condition_bounds,
    degree_two_exact,
    dissociation_bounds,
    exact_probability,
    frechet_bounds,
    packing_bounds,
)


@dataclass
class Case:
    name: str
    raw_terms: tuple[tuple[int, ...], ...]
    probabilities: dict[int, float]
    exact_truth: bool

    @property
    def query(self) -> DNF:
        return DNF.from_terms(self.raw_terms)


def make_case(name: str, terms: Iterable[Iterable[int]], p: float, truth: bool) -> Case:
    raw = tuple(tuple(t) for t in terms)
    return Case(name, raw, {i: p for term in raw for i in term}, truth)


def cases() -> Iterable[Case]:
    for p, truth in [(0.05, False), (0.8, True)]:
        label = "false" if not truth else "true"
        yield make_case(f"repeated_and_{label}", [(0,) * 8], p, truth)
        yield make_case(f"repeated_or_{label}", [(0,)] * 8, p, truth)
        for n in [8, 12, 16, 128, 1024]:
            yield make_case(f"cycle_{n}_{label}", [(i, (i + 1) % n) for i in range(n)], p, truth)
        for n in [8, 16, 128]:
            yield make_case(f"shared_hub_{n}_{label}", [(0, i) for i in range(1, n)], p, truth)
        edges = list(combinations(range(4), 2))
        yield make_case(
            f"symmetric_K4_{label}",
            [[i for i, e in enumerate(edges) if v in e] for v in range(4)],
            p,
            truth,
        )
    rng = random.Random(413)
    for n in [8, 12, 16]:
        yield make_case(
            f"random_width3_{n}", [rng.sample(range(n), 3) for _ in range(n)], 0.2, False
        )


def timed(function: Callable[[], Bounds], repeats: int) -> tuple[Bounds, float, int]:
    values = []
    result = (0.0, 0.0)
    for _ in range(repeats):
        start = time.perf_counter_ns()
        result = function()
        values.append((time.perf_counter_ns() - start) / 1e6)
    # Measure allocation separately so tracing does not contaminate timing.
    tracemalloc.start()
    function()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, statistics.median(values), peak


def point(value: float) -> Bounds:
    return value, value


def point_method(
    method: Callable[[DNF, dict[int, float]], float], q: DNF, p: dict[int, float]
) -> Bounds:
    return point(method(q, p))


def occurrence_product(case: Case) -> Bounds:
    return point(
        1 - math.prod(1 - math.prod(case.probabilities[i] for i in t) for t in case.raw_terms)
    )


def run(repeats: int) -> dict[str, object]:
    rows = []
    for case in cases():
        q, p = case.query, case.probabilities
        reference = exact_probability(q, p) if len(q.support) <= 16 else None
        try:
            dp = degree_two_exact(q, p)
        except ValueError:
            dp = None
        if reference is None:
            reference = dp
        if case.name.startswith("shared_hub"):
            reference = p[0] * (1 - math.prod(1 - p[i] for i in q.support if i != 0))
        occurrences = Counter(i for t in q.terms for i in t)
        selected = [i for i, _ in sorted(occurrences.items(), key=lambda pair: (-pair[1], pair[0]))]
        methods: list[tuple[str, str, Callable[[], Bounds]]] = [
            ("occurrence_product", "estimate", partial(occurrence_product, case)),
            ("frechet", "arbitrary_dependence_bound", partial(frechet_bounds, q, p)),
            (
                "published_symmetric_dissociation",
                "independent_source_bound",
                partial(dissociation_bounds, q, p),
            ),
            ("witness_packing", "independent_source_bound", partial(packing_bounds, q, p)),
        ]
        if len(q.support) <= 16:
            methods.append(
                (
                    "exhaustive",
                    "exact_independent_sources",
                    partial(point_method, exact_probability, q, p),
                )
            )
        if dp is not None:
            methods.append(
                (
                    "path_cycle_dp",
                    "exact_independent_sources",
                    partial(point_method, degree_two_exact, q, p),
                )
            )
        if len(q.support) <= 16 or case.name.startswith("shared_hub"):
            for k in [1, 3]:
                methods.append(
                    (
                        f"condition_{k}",
                        "independent_source_bound",
                        partial(condition_bounds, q, p, selected[:k]),
                    )
                )
        for method, kind, function in methods:
            bounds, elapsed, peak = timed(function, repeats)
            error = (1 - bounds[1], 1 - bounds[0]) if case.exact_truth else bounds
            row = {
                "case": case.name,
                "sources": len(q.support),
                "witnesses": len(q.terms),
                "method": method,
                "kind": kind,
                "acceptance_lower": bounds[0],
                "acceptance_upper": bounds[1],
                "width": bounds[1] - bounds[0],
                "reference_acceptance": reference,
                "error_type": "FN" if case.exact_truth else "FP",
                "error_lower": error[0],
                "error_upper": error[1],
                "median_ms": elapsed,
                "peak_traced_bytes": peak,
                "covers_reference": None
                if reference is None
                else bounds[0] - 1e-12 <= reference <= bounds[1] + 1e-12,
            }
            if kind != "estimate" and row["covers_reference"] is False:
                raise AssertionError(row)
            rows.append(row)
    return {
        "metadata": {
            "python": platform.python_version(),
            "source_sha256": {
                name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                for name in ("benchmark.py", "contracts.py")
            },
            "platform": platform.platform(),
            "repeats": repeats,
            "timing": "median; lineage construction excluded",
            "memory": "peak tracemalloc allocation during inference, excluding input",
            "seed": 413,
            "scope": "synthetic independent sources; not compressed filters",
            "numerics": "float tolerance 1e-12, not outward-rounded certification",
            "baseline_limit": "symmetric dissociation, not optimized scaled dissociation",
        },
        "cases": [asdict(case) for case in cases()],
        "results": rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output", type=Path, default=Path("benchmark.json"))
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    data = run(args.repeats)
    args.output.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    print(f"Wrote {len(data['results'])} comparisons to {args.output}")
