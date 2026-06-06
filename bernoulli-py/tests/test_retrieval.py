"""Tests for bernoulli.maps.retrieval (GF(2) retrieval + codec-controlled output)."""

from __future__ import annotations

from collections import Counter

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from bernoulli.maps.codec import DenseCodec, PaddedCodec
from bernoulli.maps.retrieval import EncodedRetrieval, GF2Retrieval


def _keys(n: int, prefix: str = "k") -> list[bytes]:
    return [f"{prefix}-{i}".encode() for i in range(n)]


class TestGF2Retrieval:
    def test_round_trip(self) -> None:
        items = {k: i % 16 for i, k in enumerate(_keys(1000))}
        ret = GF2Retrieval(items, value_bits=4)
        assert all(ret.query(k) == v for k, v in items.items())
        assert ret.num_keys() == 1000
        assert ret.value_bits() == 4
        assert ret.bits_per_key() > 4.0  # overhead * r
        assert ret.memory_bytes() > 0

    def test_values_masked_to_width(self) -> None:
        ret = GF2Retrieval({b"a": 0b1111_0101}, value_bits=4)
        assert ret.query(b"a") == 0b0101

    @settings(max_examples=25, deadline=None)
    @given(
        st.lists(
            st.binary(min_size=1, max_size=20), min_size=1, max_size=250, unique=True
        )
    )
    def test_round_trip_random(self, keys: list[bytes]) -> None:
        items = {k: (i * 7) % 256 for i, k in enumerate(keys)}
        ret = GF2Retrieval(items, value_bits=8)
        assert all(ret.query(k) == v for k, v in items.items())

    def test_non_member_output_is_uniform(self) -> None:
        ret = GF2Retrieval({k: 0 for k in _keys(2000)}, value_bits=3)  # all store 0
        counts = Counter(ret.query(f"x-{i}".encode()) for i in range(16000))
        mean = 16000 / 8
        assert len(counts) == 8  # every bucket hit despite all stored values being 0
        assert all(0.7 * mean < c < 1.3 * mean for c in counts.values())

    def test_validation(self) -> None:
        with pytest.raises(ValueError):
            GF2Retrieval({b"a": 1}, value_bits=0)
        with pytest.raises(ValueError):
            GF2Retrieval({b"a": 1}, value_bits=4, overhead=1.0)

    def test_empty(self) -> None:
        ret = GF2Retrieval({}, value_bits=4)
        assert ret.num_keys() == 0
        assert ret.query(b"x") == 0
        assert ret.bits_per_key() == 0.0
        assert ret.memory_bytes() == 0


class TestEncodedRetrieval:
    def test_members_exact(self) -> None:
        codec = DenseCodec(["a", "b", "c", "d"], m_bits=2)
        data = {k: "abcd"[i % 4] for i, k in enumerate(_keys(400))}
        er = EncodedRetrieval(data, codec)
        assert all(er.query(k) == v for k, v in data.items())
        assert er.num_keys() == 400
        assert er.bits_per_key() > 2.0
        assert er.memory_bytes() > 0

    def test_codec_controls_non_member_distribution(self) -> None:
        # The headline: storage is skewed, non-member output follows the CODEC.
        codec = PaddedCodec(values=["d", "a", "b"], default_value="d", m_bits=2)
        # codespace: d = 0.5, a = 0.25, b = 0.25
        data = {k: ("a" if i % 10 else "b") for i, k in enumerate(_keys(2000))}
        # storage: 90% a, 10% b, zero d
        er = EncodedRetrieval(data, codec, seed=3)
        nm = Counter(er.query(f"y-{i}".encode()) for i in range(40000))
        total = sum(nm.values())
        expected = codec.non_member_distribution()
        for v in ("d", "a", "b"):
            assert abs(nm[v] / total - expected[v]) < 0.03
        # 'd' was never stored, yet the codec gives it ~half the non-members.
        assert nm["d"] / total > 0.4

    def test_non_member_distribution_method(self) -> None:
        codec = DenseCodec(["a", "b"], m_bits=1)
        er = EncodedRetrieval({b"k": "a"}, codec)
        assert er.non_member_distribution() == codec.non_member_distribution()
