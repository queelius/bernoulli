"""Tests for bernoulli.maps.perfect_hash (BBHash minimal perfect hash)."""

from __future__ import annotations

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from bernoulli.maps.perfect_hash import MinimalPerfectHash


def _keys(n: int, prefix: str = "k") -> list[bytes]:
    return [f"{prefix}-{i}".encode() for i in range(n)]


class TestBijection:
    def test_minimal_perfect_on_build_set(self) -> None:
        keys = _keys(1000)
        mph = MinimalPerfectHash(keys)
        assert sorted(mph.slot_for(k) for k in keys) == list(range(1000))
        assert mph.num_keys() == 1000
        assert mph.range_size() == 1000  # minimal

    def test_deterministic(self) -> None:
        keys = _keys(500)
        a = MinimalPerfectHash(keys, seed=7)
        b = MinimalPerfectHash(keys, seed=7)
        assert [a.slot_for(k) for k in keys] == [b.slot_for(k) for k in keys]

    def test_deduplicates(self) -> None:
        mph = MinimalPerfectHash(_keys(100) + _keys(100))
        assert mph.num_keys() == 100
        assert sorted(mph.slot_for(k) for k in _keys(100)) == list(range(100))

    def test_nonmember_slots_valid(self) -> None:
        mph = MinimalPerfectHash(_keys(2000, "m"))
        assert all(0 <= mph.slot_for(f"x-{i}".encode()) < 2000 for i in range(2000))


class TestSpace:
    def test_bits_per_key_reasonable(self) -> None:
        mph = MinimalPerfectHash(_keys(10000))
        assert 0.0 < mph.bits_per_key() < 8.0  # BBHash at gamma=2 is ~3 bits/key
        assert mph.structure_bits() > 0
        assert mph.memory_bytes() > 0

    def test_smaller_gamma_uses_fewer_bits(self) -> None:
        keys = _keys(5000)
        big = MinimalPerfectHash(keys, gamma=2.0).bits_per_key()
        small = MinimalPerfectHash(keys, gamma=1.3).bits_per_key()
        assert small < big


class TestValidationAndEmpty:
    def test_gamma_must_exceed_one(self) -> None:
        with pytest.raises(ValueError):
            MinimalPerfectHash(_keys(10), gamma=1.0)

    def test_empty(self) -> None:
        mph = MinimalPerfectHash([])
        assert mph.num_keys() == 0
        assert mph.range_size() == 0
        assert mph.bits_per_key() == 0.0


class TestProperties:
    @settings(max_examples=50, deadline=None)
    @given(st.integers(min_value=1, max_value=300))
    def test_bijection_random_sizes(self, n: int) -> None:
        keys = [f"item:{i}:{(i * 7) % 13}".encode() for i in range(n)]
        mph = MinimalPerfectHash(keys)
        assert sorted(mph.slot_for(k) for k in keys) == list(range(n))

    @settings(max_examples=30, deadline=None)
    @given(
        st.lists(
            st.binary(min_size=1, max_size=20), min_size=1, max_size=200, unique=True
        )
    )
    def test_bijection_random_bytes(self, keys: list[bytes]) -> None:
        mph = MinimalPerfectHash(keys)
        assert sorted(mph.slot_for(k) for k in keys) == list(range(len(keys)))
