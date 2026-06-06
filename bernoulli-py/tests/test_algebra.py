"""Tests for ``bernoulli.algebra``."""

from __future__ import annotations

import math

import pytest

from bernoulli import algebra


class TestCompositionTotalError:
    def test_empty_chain(self) -> None:
        assert algebra.composition_total_error([]) == 0.0

    def test_single_stage(self) -> None:
        assert math.isclose(algebra.composition_total_error([0.3]), 0.3)

    def test_two_stages(self) -> None:
        # 1 - (1-0.1)(1-0.2) = 1 - 0.72 = 0.28
        assert math.isclose(
            algebra.composition_total_error([0.1, 0.2]), 0.28, abs_tol=1e-12
        )

    def test_invalid_rate_raises(self) -> None:
        with pytest.raises(ValueError):
            algebra.composition_total_error([-0.01])
        with pytest.raises(ValueError):
            algebra.composition_total_error([1.5])


class TestCompositionHomogeneous:
    def test_zero_stages(self) -> None:
        assert algebra.composition_homogeneous(rate=0.5, k=0) == 0.0

    def test_one_stage(self) -> None:
        assert math.isclose(algebra.composition_homogeneous(rate=0.3, k=1), 0.3)

    def test_matches_total_error(self) -> None:
        rate, k = 0.2, 5
        a = algebra.composition_homogeneous(rate=rate, k=k)
        b = algebra.composition_total_error([rate] * k)
        assert math.isclose(a, b, abs_tol=1e-12)

    def test_invalid_k(self) -> None:
        with pytest.raises(ValueError):
            algebra.composition_homogeneous(rate=0.5, k=-1)


class TestKForAndChainTarget:
    def test_miller_rabin_sizing(self) -> None:
        # 0.25^k <= 1e-12 needs k >= 20 (since 4^20 = 2^40 > 10^12).
        k = algebra.k_for_and_chain_target(per_round_rate=0.25, target_rate=1e-12)
        assert k == 20
        assert 0.25 ** k <= 1e-12

    def test_target_above_rate_returns_one(self) -> None:
        # If target >= per_round_rate, one round suffices.
        k = algebra.k_for_and_chain_target(per_round_rate=0.25, target_rate=0.5)
        assert k == 1

    def test_zero_rate_returns_zero_rounds(self) -> None:
        # If rate is zero, no rounds needed.
        k = algebra.k_for_and_chain_target(per_round_rate=0.0, target_rate=0.001)
        assert k == 0


class TestMaxKForOrChainBudget:
    def test_basic(self) -> None:
        # 1 - (1-0.001)^k <= 0.01 -> k <= 10.045 -> 10.
        k = algebra.max_k_for_or_chain_budget(
            per_stage_rate=0.001, error_budget=0.01
        )
        assert k == 10
        rate_at_k = algebra.composition_homogeneous(0.001, k)
        rate_at_k_plus_one = algebra.composition_homogeneous(0.001, k + 1)
        assert rate_at_k <= 0.01
        assert rate_at_k_plus_one > 0.01

    def test_zero_budget_returns_zero(self) -> None:
        k = algebra.max_k_for_or_chain_budget(
            per_stage_rate=0.1, error_budget=0.0
        )
        assert k == 0

    def test_zero_rate_returns_unbounded(self) -> None:
        k = algebra.max_k_for_or_chain_budget(
            per_stage_rate=0.0, error_budget=0.01
        )
        # Sentinel: 2**30. Anything that big counts as "unbounded".
        assert k > 1_000_000


class TestMillerRabin:
    def test_zero_rounds(self) -> None:
        assert algebra.miller_rabin_error(k=0) == 1.0

    def test_one_round(self) -> None:
        assert math.isclose(algebra.miller_rabin_error(k=1), 0.25)

    def test_ten_rounds(self) -> None:
        assert math.isclose(algebra.miller_rabin_error(k=10), 0.25 ** 10)

    def test_custom_witness_rate(self) -> None:
        assert math.isclose(
            algebra.miller_rabin_error(k=5, single_witness_fpr=0.1),
            0.1 ** 5,
        )


class TestBloomFilter:
    def test_empty_filter_zero_fpr(self) -> None:
        assert algebra.bloom_filter_fpr(num_keys=0, num_bits=1024, num_hashes=4) == 0.0

    def test_classical_value(self) -> None:
        # With m/n = 10 and k = 7, Bloom FPR should be ~ 0.00819
        n, m, k = 1000, 10000, 7
        fpr = algebra.bloom_filter_fpr(num_keys=n, num_bits=m, num_hashes=k)
        assert 0.005 < fpr < 0.012

    def test_optimal_k(self) -> None:
        # For m/n = 10, optimal k = 10*ln(2) ~= 6.93.
        k_opt = algebra.bloom_filter_optimal_k(num_keys=1000, num_bits=10000)
        assert math.isclose(k_opt, 10.0 * math.log(2.0), abs_tol=1e-12)


class TestBitsPerKey:
    def test_entropy_lower_bound(self) -> None:
        # FPR = 0.01 -> -log2(0.01) = log2(100) ~= 6.644
        assert math.isclose(
            algebra.bits_per_key_for_fpr(0.01),
            -math.log2(0.01),
            abs_tol=1e-12,
        )

    def test_bloom_overhead(self) -> None:
        # Bloom uses 1/ln(2) more than entropy bound.
        target = 0.001
        entropy = algebra.bits_per_key_for_fpr(target)
        bloom = algebra.bloom_bits_per_key_for_fpr(target)
        assert math.isclose(bloom / entropy, 1.0 / math.log(2.0), abs_tol=1e-12)
