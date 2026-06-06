"""Tests for bernoulli.sketches.countmin (Count-Min frequency sketch)."""

from __future__ import annotations

import math
import random

import pytest

from bernoulli.sketches import CountMinSketch


class TestCountMin:
    def test_never_undercounts(self) -> None:
        cms = CountMinSketch(width=500, depth=4)
        truth: dict[bytes, int] = {}
        rng = random.Random(1)
        for _ in range(20_000):
            k = f"k{rng.randint(0, 1000)}".encode()
            cms.add(k)
            truth[k] = truth.get(k, 0) + 1
        assert all(cms.estimate(k) >= truth[k] for k in truth)  # one-sided guarantee
        assert cms.total() == 20_000

    def test_overestimate_mostly_within_bound(self) -> None:
        cms = CountMinSketch.from_error(epsilon=0.002, delta=0.05)
        truth: dict[bytes, int] = {}
        rng = random.Random(2)
        for _ in range(50_000):
            k = f"k{rng.randint(0, 3000)}".encode()
            cms.add(k)
            truth[k] = truth.get(k, 0) + 1
        bound = cms.error_bound()
        within = sum(1 for k in truth if cms.estimate(k) - truth[k] <= bound)
        assert within / len(truth) >= 0.95  # overestimate <= eps*N w.h.p.
        assert all(cms.estimate(k) >= truth[k] for k in truth)

    def test_add_count(self) -> None:
        cms = CountMinSketch(width=100, depth=3)
        cms.add(b"x", count=7)
        assert cms.estimate(b"x") >= 7
        assert cms.total() == 7

    def test_getitem(self) -> None:
        cms = CountMinSketch(width=100, depth=3)
        cms.add(b"x")
        cms.add(b"x")
        assert cms[b"x"] >= 2

    def test_from_error_sizing(self) -> None:
        cms = CountMinSketch.from_error(epsilon=0.01, delta=0.05)
        assert cms.width == math.ceil(math.e / 0.01)
        assert cms.depth == math.ceil(math.log(1.0 / 0.05))

    def test_memory_bytes(self) -> None:
        assert CountMinSketch(width=100, depth=4).memory_bytes() == 100 * 4 * 4

    def test_validation(self) -> None:
        with pytest.raises(ValueError):
            CountMinSketch(width=0, depth=3)
        with pytest.raises(ValueError):
            CountMinSketch(width=10, depth=0)
        with pytest.raises(ValueError):
            CountMinSketch.from_error(epsilon=0.0, delta=0.1)
        with pytest.raises(ValueError):
            CountMinSketch.from_error(epsilon=0.1, delta=1.5)
        with pytest.raises(ValueError):
            CountMinSketch(width=10, depth=2).add(b"x", count=-1)
