"""Tests for bernoulli.sketches.minhash (MinHash Jaccard estimator)."""

from __future__ import annotations

import math

import pytest

from bernoulli.sketches import MinHash


def items(lo: int, hi: int) -> list[bytes]:
    return [str(i).encode() for i in range(lo, hi)]


class TestMinHash:
    def test_jaccard_estimate(self) -> None:
        a = MinHash.from_items(items(0, 1000), num_hashes=512)
        b = MinHash.from_items(items(500, 1500), num_hashes=512)
        assert abs(a.jaccard(b) - 1 / 3) < 0.05  # true J = 500/1500

    def test_identical_sets_j_is_one(self) -> None:
        a = MinHash.from_items(items(0, 500), num_hashes=128)
        b = MinHash.from_items(items(0, 500), num_hashes=128)
        assert a.jaccard(b) == 1.0
        assert a.jaccard(a) == 1.0

    def test_disjoint_sets_j_near_zero(self) -> None:
        a = MinHash.from_items(items(0, 1000), num_hashes=256)
        b = MinHash.from_items(items(10_000, 11_000), num_hashes=256)
        assert a.jaccard(b) < 0.05

    def test_merge_is_union(self) -> None:
        a = MinHash.from_items(items(0, 1000), num_hashes=256)
        b = MinHash.from_items(items(500, 1500), num_hashes=256)
        union = a.merge(b)
        assert abs(union.jaccard(a) - 2 / 3) < 0.06  # |a| / |a ∪ b| = 1000/1500
        # element-wise min equals hashing the combined set directly
        assert union.signature() == MinHash.from_items(items(0, 1500), num_hashes=256).signature()

    def test_expected_error(self) -> None:
        mh = MinHash(num_hashes=100)
        assert math.isclose(mh.expected_error(), 0.5 / 10.0)  # 0.5 / sqrt(100)
        assert math.isclose(mh.expected_error(0.5), math.sqrt(0.25 / 100))
        assert mh.expected_error(0.0) == 0.0

    def test_memory_bytes(self) -> None:
        assert MinHash(num_hashes=128).memory_bytes() == 128 * 8

    def test_validation(self) -> None:
        with pytest.raises(ValueError):
            MinHash(num_hashes=0)
        a = MinHash.from_items(items(0, 10), num_hashes=64)
        b = MinHash.from_items(items(0, 10), num_hashes=128)
        c = MinHash.from_items(items(0, 10), num_hashes=64, salt=9)
        with pytest.raises(ValueError):
            a.jaccard(b)  # mismatched num_hashes
        with pytest.raises(ValueError):
            a.jaccard(c)  # mismatched salt
        with pytest.raises(ValueError):
            a.merge(b)
        with pytest.raises(ValueError):
            a.expected_error(1.5)
