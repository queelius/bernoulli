"""A small timing harness for Bernoulli structures.

This is the *performance* counterpart to :mod:`bernoulli.harness` (which
measures error rates). It times an operation, normalizes by the number of
logical operations performed, and reports throughput and per-operation
latency. It is dependency-free and reusable from both notebooks and the
``experiments/`` research layer.

Methodology
-----------
- **Best-of-N, not mean.** Wall-clock timing noise is one-sided: scheduling,
  interrupts, and cache effects only ever make a trial slower. The minimum
  over ``repeats`` trials is therefore the cleanest estimate of the true cost;
  the median is reported alongside as a robustness check.
- **Warmup.** A configurable number of untimed runs prime caches and branch
  predictors (and any first-call import cost) before measurement begins.
- **Explicit op count.** The caller states how many logical operations a timed
  batch performs, so throughput is comparable across batch sizes.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class BuildableOracle(Protocol):
    """An approximate set that can be built (``add``) and queried (``contains``).

    A build-and-query superset of :class:`bernoulli.sets.MembershipOracle`,
    which is query-only. ``BloomFilter`` satisfies it.
    """

    def add(self, key: bytes) -> None: ...

    def contains(self, key: bytes) -> bool: ...


@dataclass(frozen=True, slots=True)
class BenchResult:
    """The timing of one benchmarked operation.

    Attributes
    ----------
    label : str
        Human-readable name of what was timed.
    ops : int
        Number of logical operations performed per trial (for normalization).
    repeats : int
        Number of timed trials.
    best_seconds : float
        Minimum wall time over the trials (the headline figure).
    median_seconds : float
        Median wall time over the trials.
    """

    label: str
    ops: int
    repeats: int
    best_seconds: float
    median_seconds: float

    @property
    def ops_per_sec(self) -> float:
        """Throughput at the best trial, in operations per second."""
        return self.ops / self.best_seconds if self.best_seconds > 0 else float("inf")

    @property
    def ns_per_op(self) -> float:
        """Per-operation latency at the best trial, in nanoseconds."""
        return (self.best_seconds / self.ops) * 1e9 if self.ops > 0 else 0.0

    def __str__(self) -> str:
        return (
            f"{self.label:28s}  {self.ops_per_sec:>13,.0f} ops/s  "
            f"{self.ns_per_op:>10.1f} ns/op  "
            f"(best {self.best_seconds * 1e3:.3f} ms over {self.repeats})"
        )


def benchmark(
    batch: Callable[[], object],
    *,
    ops: int,
    repeats: int = 7,
    warmup: int = 1,
    label: str = "",
) -> BenchResult:
    """Time ``batch`` (which performs ``ops`` operations) and report best/median.

    Parameters
    ----------
    batch : Callable[[], object]
        A zero-argument callable performing ``ops`` logical operations. Its
        return value is ignored (but returning a value keeps it from being
        optimized away and lets callers reuse a build closure).
    ops : int
        Number of logical operations one call to ``batch`` performs.
    repeats : int
        Number of timed trials (best and median are taken over these).
    warmup : int
        Number of untimed trials run before timing begins.
    label : str
        Name for the result.

    Examples
    --------
    >>> r = benchmark(lambda: sum(range(1000)), ops=1000, repeats=3, warmup=1)
    >>> r.ops_per_sec > 0
    True
    """
    if ops <= 0:
        raise ValueError(f"ops must be positive, got {ops!r}")
    if repeats <= 0:
        raise ValueError(f"repeats must be positive, got {repeats!r}")
    if warmup < 0:
        raise ValueError(f"warmup must be non-negative, got {warmup!r}")

    for _ in range(warmup):
        batch()

    times: list[float] = []
    for _ in range(repeats):
        start = time.perf_counter()
        batch()
        times.append(time.perf_counter() - start)

    times.sort()
    best = times[0]
    median = times[len(times) // 2]
    return BenchResult(
        label=label or getattr(batch, "__name__", "batch"),
        ops=ops,
        repeats=repeats,
        best_seconds=best,
        median_seconds=median,
    )


def bench_membership(
    make_oracle: Callable[[], BuildableOracle],
    keys: list[bytes],
    queries: list[bytes],
    *,
    repeats: int = 5,
    warmup: int = 1,
    label: str = "",
) -> dict[str, BenchResult]:
    """Benchmark the build and query paths of a membership oracle.

    The ``build`` timing inserts every key into a *fresh* oracle on each trial;
    the ``query`` timing runs every query against a single pre-built oracle.
    Keeping those separate is essential: timing queries against a filter that
    is rebuilt each trial would charge insertion cost to the query path.

    Parameters
    ----------
    make_oracle : Callable[[], MembershipOracle]
        Factory returning a fresh, empty oracle (with ``add`` and ``contains``).
    keys : list[bytes]
        Keys to insert during the build benchmark.
    queries : list[bytes]
        Keys to look up during the query benchmark.
    repeats, warmup : int
        Passed through to :func:`benchmark`.
    label : str
        Prefix for the two result labels.

    Returns
    -------
    dict[str, BenchResult]
        ``{"build": ..., "query": ...}``.
    """
    prefix = f"{label} " if label else ""

    def build() -> BuildableOracle:
        oracle = make_oracle()
        for key in keys:
            oracle.add(key)
        return oracle

    build_result = benchmark(
        build, ops=len(keys), repeats=repeats, warmup=warmup, label=f"{prefix}build"
    )

    oracle = build()

    def run_queries() -> int:
        return sum(1 for q in queries if oracle.contains(q))

    query_result = benchmark(
        run_queries,
        ops=len(queries),
        repeats=repeats,
        warmup=warmup,
        label=f"{prefix}query",
    )
    return {"build": build_result, "query": query_result}


def format_results(results: dict[str, BenchResult]) -> str:
    """Render a dict of benchmark results as aligned lines."""
    return "\n".join(str(r) for r in results.values())
