"""Tests for ``bernoulli.maps.codec``.

Covers:

- :class:`DenseCodec` round-trip, codespace fractions, vocabulary errors.
- :class:`PaddedCodec` round-trip, surplus folding onto default.
- :class:`PrefixCodec` round-trip, Kraft inequality, Huffman build.
- :func:`shannon_entropy` on uniform and degenerate distributions.
"""

from __future__ import annotations

import math

import pytest

from bernoulli.maps.codec import (
    DenseCodec,
    PaddedCodec,
    PrefixCodec,
    shannon_entropy,
)

# =====================================================================
# DenseCodec
# =====================================================================


class TestDenseCodec:
    def test_round_trip_full_alphabet(self) -> None:
        # |V| = 2^M = 8, full bijection.
        values = ["a", "b", "c", "d", "e", "f", "g", "h"]
        codec: DenseCodec[str] = DenseCodec(values, m_bits=3)
        assert codec.codespace_size == 8
        for v in values:
            pattern = codec.encode(v)
            assert 0 <= pattern < 8
            assert codec.decode(pattern) == v

    def test_round_trip_distinct_codes(self) -> None:
        # Every value must encode to a distinct slot.
        values = list(range(8))
        codec: DenseCodec[int] = DenseCodec(values, m_bits=3)
        codes = {codec.encode(v) for v in values}
        assert len(codes) == 8

    def test_codespace_fraction_sums_to_one(self) -> None:
        # When |V| = 2^M, every value gets exactly 1/2^M.
        values = list(range(8))
        codec: DenseCodec[int] = DenseCodec(values, m_bits=3)
        total = sum(codec.codespace_fraction(v) for v in values)
        assert total == pytest.approx(1.0, abs=1e-12)
        for v in values:
            assert codec.codespace_fraction(v) == pytest.approx(1.0 / 8.0)

    def test_codespace_surplus_folds_onto_first(self) -> None:
        # |V| = 5, M = 3 (capacity 8) -> 3 surplus patterns fold onto values[0].
        values = ["a", "b", "c", "d", "e"]
        codec: DenseCodec[str] = DenseCodec(values, m_bits=3)
        # First value claims 1 + 3 = 4 of 8 patterns.
        assert codec.codespace_fraction("a") == pytest.approx(4.0 / 8.0)
        for v in values[1:]:
            assert codec.codespace_fraction(v) == pytest.approx(1.0 / 8.0)
        total = sum(codec.codespace_fraction(v) for v in values)
        assert total == pytest.approx(1.0, abs=1e-12)

    def test_decode_surplus_returns_first_value(self) -> None:
        values = ["a", "b", "c"]
        codec: DenseCodec[str] = DenseCodec(values, m_bits=2)
        assert codec.decode(0) == "a"
        assert codec.decode(1) == "b"
        assert codec.decode(2) == "c"
        # Surplus pattern 3 folds onto first.
        assert codec.decode(3) == "a"

    def test_rejects_out_of_vocab(self) -> None:
        codec: DenseCodec[str] = DenseCodec(["a", "b"], m_bits=2)
        with pytest.raises(KeyError):
            codec.encode("z")

    def test_rejects_invalid_pattern(self) -> None:
        codec: DenseCodec[str] = DenseCodec(["a", "b"], m_bits=2)
        with pytest.raises(ValueError):
            codec.decode(-1)
        with pytest.raises(ValueError):
            codec.decode(4)

    def test_rejects_too_many_values(self) -> None:
        with pytest.raises(ValueError):
            DenseCodec(list(range(9)), m_bits=3)  # capacity 8, given 9

    def test_rejects_invalid_m_bits(self) -> None:
        with pytest.raises(ValueError):
            DenseCodec(["a"], m_bits=0)
        with pytest.raises(ValueError):
            DenseCodec(["a"], m_bits=33)

    def test_rejects_empty_vocabulary(self) -> None:
        with pytest.raises(ValueError):
            DenseCodec([], m_bits=3)

    def test_rejects_duplicates(self) -> None:
        with pytest.raises(ValueError):
            DenseCodec(["a", "b", "a"], m_bits=2)

    def test_bits_per_value(self) -> None:
        codec: DenseCodec[str] = DenseCodec(["a", "b", "c", "d"], m_bits=2)
        assert codec.bits_per_value() == 2.0

    def test_expected_codeword_length(self) -> None:
        # Constant m_bits regardless of distribution.
        codec: DenseCodec[str] = DenseCodec(["a", "b", "c", "d"], m_bits=2)
        assert codec.expected_codeword_length({"a": 0.7, "b": 0.1, "c": 0.1, "d": 0.1}) == 2.0

    def test_non_member_distribution_matches_codespace(self) -> None:
        values = list(range(8))
        codec: DenseCodec[int] = DenseCodec(values, m_bits=3)
        nm = codec.non_member_distribution()
        assert sum(nm.values()) == pytest.approx(1.0, abs=1e-12)
        for v in values:
            assert nm[v] == pytest.approx(codec.codespace_fraction(v))


# =====================================================================
# PaddedCodec
# =====================================================================


class TestPaddedCodec:
    def test_round_trip_including_default(self) -> None:
        values = ["MISSING", "a", "b", "c"]
        codec: PaddedCodec[str] = PaddedCodec(values, default_value="MISSING", m_bits=3)
        for v in values:
            pattern = codec.encode(v)
            assert 0 <= pattern < 8
            assert codec.decode(pattern) == v

    def test_default_collects_surplus(self) -> None:
        # |V| = 4, M = 3, capacity = 8 -> default gets 5 / 8.
        values = ["MISSING", "a", "b", "c"]
        codec: PaddedCodec[str] = PaddedCodec(values, default_value="MISSING", m_bits=3)
        assert codec.codespace_fraction("MISSING") == pytest.approx(5.0 / 8.0)
        for v in ("a", "b", "c"):
            assert codec.codespace_fraction(v) == pytest.approx(1.0 / 8.0)
        total = sum(codec.codespace_fraction(v) for v in values)
        assert total == pytest.approx(1.0, abs=1e-12)

    def test_decode_surplus_folds_to_default(self) -> None:
        values = ["MISSING", "a", "b", "c"]
        codec: PaddedCodec[str] = PaddedCodec(values, default_value="MISSING", m_bits=3)
        # Patterns 4..7 are surplus and decode to default.
        for pattern in range(4, 8):
            assert codec.decode(pattern) == "MISSING"

    def test_default_first_in_values_property(self) -> None:
        # default_value is reordered to occupy index 0.
        codec: PaddedCodec[str] = PaddedCodec(
            ["a", "b", "MISSING", "c"], default_value="MISSING", m_bits=3
        )
        assert codec.values[0] == "MISSING"

    def test_rejects_default_not_in_values(self) -> None:
        with pytest.raises(ValueError):
            PaddedCodec(["a", "b"], default_value="X", m_bits=2)

    def test_rejects_out_of_vocab(self) -> None:
        codec: PaddedCodec[str] = PaddedCodec(["a", "b"], default_value="a", m_bits=2)
        with pytest.raises(KeyError):
            codec.encode("zzz")

    def test_rejects_invalid_pattern(self) -> None:
        codec: PaddedCodec[str] = PaddedCodec(["a", "b"], default_value="a", m_bits=2)
        with pytest.raises(ValueError):
            codec.decode(8)

    def test_full_alphabet_no_surplus(self) -> None:
        # |V| = 2^M = 4: default gets exactly 1/4 like everyone else.
        values = ["MISSING", "a", "b", "c"]
        codec: PaddedCodec[str] = PaddedCodec(values, default_value="MISSING", m_bits=2)
        for v in values:
            assert codec.codespace_fraction(v) == pytest.approx(0.25)

    def test_non_member_distribution_matches_codespace(self) -> None:
        values = ["MISSING", "a", "b", "c"]
        codec: PaddedCodec[str] = PaddedCodec(values, default_value="MISSING", m_bits=4)
        nm = codec.non_member_distribution()
        assert sum(nm.values()) == pytest.approx(1.0, abs=1e-12)
        # Default gets (16 - 4) + 1 = 13 of the 16 patterns: 13/16.
        assert nm["MISSING"] == pytest.approx(13.0 / 16.0)
        for v in ("a", "b", "c"):
            assert nm[v] == pytest.approx(1.0 / 16.0)


# =====================================================================
# PrefixCodec
# =====================================================================


class TestPrefixCodec:
    def test_round_trip_explicit_codes(self) -> None:
        # Lengths satisfy Kraft: 1/2 + 1/4 + 1/4 = 1.
        codes = [("a", 1), ("b", 2), ("c", 2)]
        codec: PrefixCodec[str] = PrefixCodec(codes, default_value="a", m_bits=4)
        for v, _ in codes:
            pattern = codec.encode(v)
            assert codec.decode(pattern) == v

    def test_kraft_inequality_satisfied(self) -> None:
        codes = [("a", 1), ("b", 2), ("c", 2)]
        codec: PrefixCodec[str] = PrefixCodec(codes, default_value="a", m_bits=4)
        # Sum of 2^(-l_v) <= 1.
        kraft = codec.kraft_sum()
        assert kraft <= 1.0 + 1e-9
        assert kraft == pytest.approx(0.5 + 0.25 + 0.25)

    def test_kraft_violation_raises(self) -> None:
        # 2^(-1) + 2^(-1) + 2^(-1) = 1.5 > 1.
        with pytest.raises(ValueError):
            PrefixCodec(
                [("a", 1), ("b", 1), ("c", 1)], default_value="a", m_bits=4
            )

    def test_kraft_strict_inequality_surplus_to_default(self) -> None:
        # 2^(-1) + 2^(-2) = 0.75 < 1; default ("a") absorbs surplus 0.25.
        codes = [("a", 1), ("b", 2)]
        codec: PrefixCodec[str] = PrefixCodec(codes, default_value="a", m_bits=4)
        # a's codespace: 2^(-1) = 0.5, plus surplus 0.25 = 0.75.
        assert codec.codespace_fraction("a") == pytest.approx(0.75)
        assert codec.codespace_fraction("b") == pytest.approx(0.25)

    def test_codespace_fractions_sum_to_one(self) -> None:
        codes = [("a", 1), ("b", 2), ("c", 3), ("d", 3)]
        codec: PrefixCodec[str] = PrefixCodec(codes, default_value="a", m_bits=4)
        total = sum(codec.codespace_fraction(v) for v, _ in codes)
        assert total == pytest.approx(1.0, abs=1e-12)

    def test_canonical_prefixes_are_disjoint(self) -> None:
        # Verify decoding is unambiguous over the codespace.
        codes = [("a", 1), ("b", 2), ("c", 3), ("d", 3)]
        codec: PrefixCodec[str] = PrefixCodec(codes, default_value="a", m_bits=4)
        # Every M-bit pattern decodes to exactly one value.
        decoded_counts: dict[str, int] = {v: 0 for v, _ in codes}
        for pattern in range(1 << 4):
            v = codec.decode(pattern)
            decoded_counts[v] += 1
        # Counts should match codespace shares (codec * 2^M).
        codespace = 1 << 4
        assert decoded_counts["a"] == int(codespace * 0.5)
        assert decoded_counts["b"] == int(codespace * 0.25)
        assert decoded_counts["c"] == int(codespace * 0.125)
        assert decoded_counts["d"] == int(codespace * 0.125)

    def test_codeword_length_lookup(self) -> None:
        codes = [("a", 1), ("b", 2), ("c", 3), ("d", 3)]
        codec: PrefixCodec[str] = PrefixCodec(codes, default_value="a", m_bits=4)
        assert codec.codeword_length("a") == 1
        assert codec.codeword_length("b") == 2
        assert codec.codeword_length("c") == 3
        assert codec.codeword_length("d") == 3

    def test_encode_random_within_class(self) -> None:
        codes = [("a", 1), ("b", 2), ("c", 2)]
        codec: PrefixCodec[str] = PrefixCodec(codes, default_value="a", m_bits=4)
        # b has length 2, suffix is 4 - 2 = 2 bits -> 4 random patterns
        # all decode back to b.
        for r in range(4):
            pattern = codec.encode_random("b", rng_uniform=r)
            assert codec.decode(pattern) == "b"

    def test_encode_random_rejects_out_of_range(self) -> None:
        codes = [("a", 1), ("b", 2)]
        codec: PrefixCodec[str] = PrefixCodec(codes, default_value="a", m_bits=4)
        # b suffix is 4 - 2 = 2 bits -> max rng_uniform = 3.
        with pytest.raises(ValueError):
            codec.encode_random("b", rng_uniform=4)

    def test_encode_unknown_value_raises(self) -> None:
        codec: PrefixCodec[str] = PrefixCodec(
            [("a", 1), ("b", 1)], default_value="a", m_bits=2
        )
        with pytest.raises(KeyError):
            codec.encode("zzz")

    def test_invalid_code_length_raises(self) -> None:
        with pytest.raises(ValueError):
            PrefixCodec([("a", 0), ("b", 1)], default_value="a", m_bits=4)
        with pytest.raises(ValueError):
            PrefixCodec([("a", 5), ("b", 5)], default_value="a", m_bits=4)

    def test_default_must_be_in_codes(self) -> None:
        with pytest.raises(ValueError):
            PrefixCodec(
                [("a", 1), ("b", 2), ("c", 2)], default_value="X", m_bits=4
            )


class TestPrefixCodecFromFrequencies:
    def test_uniform_freqs_produce_balanced_codes(self) -> None:
        # 4 equal-mass values -> all length 2.
        freqs = {"a": 1.0, "b": 1.0, "c": 1.0, "d": 1.0}
        codec: PrefixCodec[str] = PrefixCodec.from_frequencies(freqs, m_bits=4)
        for v in freqs:
            assert codec.codeword_length(v) == 2
        # Kraft = 4 * 2^(-2) = 1.
        assert codec.kraft_sum() == pytest.approx(1.0)

    def test_skewed_freqs_produce_shorter_codes_for_heavy_value(self) -> None:
        # 90/10 split between two values -> Huffman gives length 1 each.
        freqs = {"common": 90.0, "rare": 10.0}
        codec: PrefixCodec[str] = PrefixCodec.from_frequencies(freqs, m_bits=4)
        # For 2 values, Huffman always produces equal length 1.
        assert codec.codeword_length("common") == 1
        assert codec.codeword_length("rare") == 1

    def test_huffman_3_values_skewed(self) -> None:
        # Heavy "a" should get length 1; light pair gets length 2.
        freqs = {"a": 80.0, "b": 10.0, "c": 10.0}
        codec: PrefixCodec[str] = PrefixCodec.from_frequencies(freqs, m_bits=4)
        assert codec.codeword_length("a") == 1
        assert codec.codeword_length("b") == 2
        assert codec.codeword_length("c") == 2

    def test_round_trip_after_huffman_build(self) -> None:
        freqs = {"a": 50.0, "b": 25.0, "c": 12.5, "d": 12.5}
        codec: PrefixCodec[str] = PrefixCodec.from_frequencies(freqs, m_bits=4)
        for v in freqs:
            pattern = codec.encode(v)
            assert codec.decode(pattern) == v

    def test_default_defaults_to_max_freq(self) -> None:
        freqs = {"a": 10.0, "b": 90.0, "c": 5.0}
        codec: PrefixCodec[str] = PrefixCodec.from_frequencies(freqs, m_bits=4)
        assert codec.default_value == "b"

    def test_explicit_default_used(self) -> None:
        freqs = {"a": 10.0, "b": 90.0, "c": 5.0}
        codec: PrefixCodec[str] = PrefixCodec.from_frequencies(
            freqs, m_bits=4, default_value="a"
        )
        assert codec.default_value == "a"

    def test_zero_weight_values_dropped(self) -> None:
        freqs = {"a": 50.0, "b": 50.0, "c": 0.0}
        codec: PrefixCodec[str] = PrefixCodec.from_frequencies(freqs, m_bits=4)
        # c was dropped, so encoding it is an error.
        with pytest.raises(KeyError):
            codec.encode("c")

    def test_no_positive_weights_raises(self) -> None:
        with pytest.raises(ValueError):
            PrefixCodec.from_frequencies({"a": 0.0, "b": 0.0}, m_bits=4)

    def test_singleton_value(self) -> None:
        # One value: assigned length 1.
        codec: PrefixCodec[str] = PrefixCodec.from_frequencies({"only": 1.0}, m_bits=4)
        assert codec.codeword_length("only") == 1

    def test_huffman_expected_length_at_most_entropy_plus_1(self) -> None:
        # Shannon's source coding theorem: H(Y) <= L < H(Y) + 1.
        freqs = {"a": 50.0, "b": 30.0, "c": 15.0, "d": 5.0}
        codec: PrefixCodec[str] = PrefixCodec.from_frequencies(freqs, m_bits=4)
        h = shannon_entropy(freqs)
        l_avg = codec.expected_codeword_length(freqs)
        assert h <= l_avg + 1e-9
        assert l_avg < h + 1.0


# =====================================================================
# shannon_entropy
# =====================================================================


class TestShannonEntropy:
    def test_uniform_returns_log2_k(self) -> None:
        for k in (2, 4, 8, 16):
            freqs = {i: 1.0 for i in range(k)}
            assert shannon_entropy(freqs) == pytest.approx(math.log2(k))

    def test_delta_distribution_returns_zero(self) -> None:
        # All mass on one value.
        freqs = {"a": 1.0, "b": 0.0, "c": 0.0}
        assert shannon_entropy(freqs) == pytest.approx(0.0)

    def test_singleton_returns_zero(self) -> None:
        assert shannon_entropy({"a": 7.0}) == pytest.approx(0.0)

    def test_normalization_independent_of_scale(self) -> None:
        # Doubling all weights doesn't change entropy.
        freqs1 = {"a": 1.0, "b": 1.0}
        freqs2 = {"a": 100.0, "b": 100.0}
        assert shannon_entropy(freqs1) == pytest.approx(shannon_entropy(freqs2))

    def test_hand_computed_two_value(self) -> None:
        # H(0.25, 0.75) = -0.25*log2(0.25) - 0.75*log2(0.75)
        #               = 0.25 * 2 + 0.75 * log2(4/3)
        #               = 0.5 + 0.75 * (2 - log2(3))
        freqs = {"a": 1.0, "b": 3.0}  # 0.25 / 0.75
        expected = -0.25 * math.log2(0.25) - 0.75 * math.log2(0.75)
        assert shannon_entropy(freqs) == pytest.approx(expected)

    def test_hand_computed_three_value(self) -> None:
        # H(1/2, 1/4, 1/4) = 1/2 * 1 + 1/4 * 2 + 1/4 * 2 = 1.5 bits.
        freqs = {"a": 2.0, "b": 1.0, "c": 1.0}
        assert shannon_entropy(freqs) == pytest.approx(1.5)

    def test_negative_weight_raises(self) -> None:
        with pytest.raises(ValueError):
            shannon_entropy({"a": 1.0, "b": -0.5})

    def test_empty_or_zero_total_raises(self) -> None:
        with pytest.raises(ValueError):
            shannon_entropy({})
        with pytest.raises(ValueError):
            shannon_entropy({"a": 0.0, "b": 0.0})
