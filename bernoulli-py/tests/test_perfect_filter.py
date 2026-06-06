"""Tests for bernoulli.maps.perfect_filter (the chapter 14 BHF)."""

from __future__ import annotations

import math

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from bernoulli.atom import BernoulliBool
from bernoulli.maps.perfect_filter import PerfectFilter
from bernoulli.sets import entropy_bound as eb


def _keys(n: int, prefix: str = "k") -> list[bytes]:
    return [f"{prefix}-{i}".encode() for i in range(n)]


class TestNoFalseNegatives:
    def test_all_members_present(self) -> None:
        keys = _keys(3000)
        pf = PerfectFilter(keys, target_fpr=0.01)
        assert all(pf.contains(k) for k in keys)
        assert pf.fnr() == 0.0

    @settings(max_examples=30, deadline=None)
    @given(
        st.lists(
            st.binary(min_size=1, max_size=24), min_size=1, max_size=300, unique=True
        )
    )
    def test_no_false_negatives_random(self, keys: list[bytes]) -> None:
        pf = PerfectFilter(keys, fingerprint_bits=8)
        assert all(pf.contains(k) for k in keys)  # structural fnr = 0


class TestFalsePositiveRate:
    def test_fpr_value(self) -> None:
        pf = PerfectFilter(_keys(100), fingerprint_bits=7)
        assert pf.fpr() == 2.0 ** -7
        assert pf.fingerprint_bits() == 7

    def test_target_fpr_sets_width(self) -> None:
        pf = PerfectFilter(_keys(100), target_fpr=0.01)
        assert pf.fingerprint_bits() == math.ceil(-math.log2(0.01))  # 7
        assert pf.fpr() <= 0.01

    def test_empirical_fpr_near_2_to_minus_r(self) -> None:
        # Deterministic: keys, filter, and queries are all fixed (no RNG).
        pf = PerfectFilter(_keys(2000, "m"), fingerprint_bits=4)  # fpr = 1/16
        nq = 10000
        fp = sum(1 for i in range(nq) if pf.contains(f"x-{i}".encode()))
        assert abs(fp / nq - 0.0625) < 0.012  # within ~1 bin of 2^-4


class TestQueryAndContainer:
    def test_query_returns_bernoulli_bool(self) -> None:
        pf = PerfectFilter(_keys(500), fingerprint_bits=8)
        q = pf.query(b"k-0")
        assert isinstance(q, BernoulliBool)
        assert q.value is True
        assert q.fnr == 0.0
        assert q.fpr == 2.0 ** -8

    def test_contains_dunder_and_len(self) -> None:
        pf = PerfectFilter(_keys(50), fingerprint_bits=10)
        assert b"k-0" in pf
        assert len(pf) == 50
        with pytest.raises(TypeError):
            _ = "k-0" in pf  # str, not bytes

    def test_slot_for(self) -> None:
        pf = PerfectFilter(_keys(200), fingerprint_bits=12)
        assert isinstance(pf.slot_for(b"k-0"), int)  # a member maps to its slot
        nonmembers = [f"absent-{i}".encode() for i in range(1000)]
        rejected = sum(1 for x in nonmembers if pf.slot_for(x) is None)
        assert rejected >= 990  # ~99.98% expected at 12-bit fingerprints


class TestSpace:
    def test_bits_per_key_matches_bhf_model(self) -> None:
        r = 10
        pf = PerfectFilter(_keys(8000), fingerprint_bits=r)
        assert pf._phf is not None
        mu = pf._phf.bits_per_key()
        assert math.isclose(pf.bits_per_key(), mu + r)
        assert math.isclose(
            pf.bits_per_key(), eb.bhf_bits_per_key(2.0 ** -r, perfect_hash_overhead=mu)
        )
        assert pf.memory_bytes() > 0

    def test_beats_bloom_at_tight_fpr(self) -> None:
        r = 12
        pf = PerfectFilter(_keys(8000), fingerprint_bits=r)
        assert pf.bits_per_key() < eb.bloom_bits_per_key(2.0 ** -r)


class TestValidationAndEmpty:
    def test_requires_a_width(self) -> None:
        with pytest.raises(ValueError):
            PerfectFilter(_keys(10))

    def test_bad_target(self) -> None:
        with pytest.raises(ValueError):
            PerfectFilter(_keys(10), target_fpr=1.5)

    def test_bad_fingerprint_bits(self) -> None:
        with pytest.raises(ValueError):
            PerfectFilter(_keys(10), fingerprint_bits=0)

    def test_empty(self) -> None:
        pf = PerfectFilter([], fingerprint_bits=8)
        assert len(pf) == 0
        assert pf.contains(b"anything") is False
        assert pf.slot_for(b"anything") is None
        assert pf.bits_per_key() == 0.0
        assert pf.memory_bytes() == 0
