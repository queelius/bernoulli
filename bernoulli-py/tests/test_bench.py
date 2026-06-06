"""Tests for bernoulli.bench: timing-harness mechanics, not absolute speeds.

Asserting concrete throughput would be flaky across machines and CI load, so
these tests check structure and invariants (positive throughput, best <=
median, correct op counts and labels), not wall-clock numbers.
"""

from __future__ import annotations

import pytest

from bernoulli.bench import BenchResult, bench_membership, benchmark, format_results
from bernoulli.sets import BloomFilter


class TestBenchmark:
    def test_returns_sane_result(self) -> None:
        r = benchmark(lambda: sum(range(1000)), ops=1000, repeats=5, warmup=1, label="sum")
        assert isinstance(r, BenchResult)
        assert r.ops == 1000
        assert r.repeats == 5
        assert r.label == "sum"
        assert r.best_seconds > 0.0
        assert r.best_seconds <= r.median_seconds  # best is the minimum trial
        assert r.ops_per_sec > 0.0
        assert r.ns_per_op > 0.0

    def test_label_defaults_to_callable_name(self) -> None:
        def my_batch() -> int:
            return sum(range(10))

        assert benchmark(my_batch, ops=10).label == "my_batch"

    def test_ops_per_sec_matches_best(self) -> None:
        r = benchmark(lambda: sum(range(100)), ops=100, repeats=3)
        assert r.ops_per_sec == pytest.approx(100 / r.best_seconds)
        assert r.ns_per_op == pytest.approx(r.best_seconds / 100 * 1e9)

    def test_validation(self) -> None:
        with pytest.raises(ValueError):
            benchmark(lambda: None, ops=0)
        with pytest.raises(ValueError):
            benchmark(lambda: None, ops=1, repeats=0)
        with pytest.raises(ValueError):
            benchmark(lambda: None, ops=1, warmup=-1)


class TestBenchMembership:
    def test_build_and_query(self) -> None:
        keys = [f"k{i}".encode() for i in range(200)]
        queries = [f"q{i}".encode() for i in range(200)]
        res = bench_membership(
            lambda: BloomFilter(capacity=200, target_fpr=0.01),
            keys,
            queries,
            repeats=3,
            warmup=1,
            label="bloom",
        )
        assert set(res) == {"build", "query"}
        assert res["build"].ops == len(keys)
        assert res["query"].ops == len(queries)
        assert res["build"].label == "bloom build"
        assert res["query"].label == "bloom query"
        assert res["build"].ops_per_sec > 0.0
        assert res["query"].ops_per_sec > 0.0

    def test_format_results_is_str(self) -> None:
        res = bench_membership(
            lambda: BloomFilter(capacity=16, target_fpr=0.01),
            [b"a", b"b"],
            [b"c"],
            repeats=2,
        )
        out = format_results(res)
        assert isinstance(out, str)
        assert "build" in out and "query" in out
