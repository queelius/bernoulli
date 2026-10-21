"""Finite counterexamples and stored-filter integration tests for the audit."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

import pytest

from probe import (
    KeyedBloom,
    Policy,
    Sampler,
    audit_run,
    exhaustive_bitmap_invariance,
    key_bytes,
    omitted_probability,
    sequential_history,
    synthetic_workload,
)


def test_bitmap_invariance_exhaustive() -> None:
    result = exhaustive_bitmap_invariance()
    assert result["counterexamples"] == 0
    assert result["policy_stream_pairs"] > 10000


@pytest.mark.parametrize("seed", range(4))
def test_stored_bitmap_invariance_and_truth_transition(seed: int) -> None:
    initial = list(range(80))
    base = KeyedBloom(capacity=100, target_fpr=0.2, seed=seed)
    for key in initial:
        base.add(key)
    collision = next(key for key in range(80, 100000) if base.contains(key))
    skipped = sequential_history(initial, [collision] * 4, [False] * 4, seed=seed)
    rescued = sequential_history(initial, [collision] * 4, [False, True, False, False], seed=seed)
    assert skipped["bitmaps"] == rescued["bitmaps"]
    assert skipped["processed"] == initial
    assert collision in rescued["processed"]
    assert skipped["novel_suppressed"] == 4
    assert rescued["novel_suppressed"] == 1
    assert rescued["true_duplicate_suppressed"] == 2


def test_no_insert_for_suppressed_document() -> None:
    initial = list(range(80))
    base = KeyedBloom(100, 0.2, 0)
    for key in initial:
        base.add(key)
    collision = next(key for key in range(80, 10000) if base.contains(key))
    result = sequential_history(initial, [collision], [False], seed=0)
    assert collision not in result["processed"]


def test_sequential_negative_is_processed_without_audit() -> None:
    result = sequential_history([], [7, 7], [False, False], seed=0)
    assert result["processed"] == [7]
    assert result["true_duplicate_suppressed"] == 1
    assert result["novel_suppressed"] == 0


def test_omission_law_by_enumerating_audit_coins() -> None:
    for repetitions in range(1, 8):
        for q in [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)]:
            total = Fraction(0)
            for coins in product([False, True], repeat=repetitions):
                mass = Fraction(1)
                for coin in coins:
                    mass *= q if coin else 1 - q
                if not any(coins):
                    total += mass
            assert omitted_probability(repetitions, q) == total


def test_uniform_distinct_finite_population_identity() -> None:
    for count in range(1, 8):
        for novel_count in range(count + 1):
            # By exchangeability the first novel_count items suffice; enumerate
            # every possible sample, not Monte Carlo/hash outputs.
            novel = set(range(novel_count))
            for budget in range(count + 1):
                samples = list(combinations(range(count), budget))
                recovered = sum(len(novel.intersection(sample)) for sample in samples)
                assert Fraction(recovered, len(samples)) == Fraction(budget * novel_count, count)


def test_frequency_is_not_a_novelty_probability() -> None:
    # One check, independent labels: enumerate the four label profiles.
    priors = (Fraction(1, 1000), Fraction(99, 100))
    rewards = [Fraction(0), Fraction(0)]
    for first, second in product([False, True], repeat=2):
        labels = (first, second)
        mass = Fraction(1)
        for label, prior in zip(labels, priors, strict=True):
            mass *= prior if label else 1 - prior
        for index, label in enumerate(labels):
            rewards[index] += mass * label
    assert rewards == list(priors)
    assert rewards[1] == 990 * rewards[0]


def test_uniform_distinct_is_repeat_invariant() -> None:
    one = Sampler(Policy.UNIFORM_DISTINCT, budget=3, seed=17)
    repeated = Sampler(Policy.UNIFORM_DISTINCT, budget=3, seed=17)
    for key in range(20):
        one.observe(key, key)
        for _ in range(key + 1):
            repeated.observe(key, key)
    assert {key for key, _ in one.selected()} == {key for key, _ in repeated.selected()}
    assert len(one.selected()) == 3


@pytest.mark.parametrize("policy", list(Policy))
def test_sampler_zero_budget_and_empty_stream(policy: Policy) -> None:
    sampler = Sampler(policy, budget=0, seed=0)
    sampler.observe(1, 0)
    assert sampler.selected() == []
    assert Sampler(policy, budget=2, seed=0).selected() == []


def test_frequency_policies_are_opposites() -> None:
    high = Sampler(Policy.HIGH_FREQUENCY, 1, 0)
    low = Sampler(Policy.LOW_FREQUENCY, 1, 0)
    for offset, key in enumerate([1, 2, 1, 1]):
        high.observe(key, offset)
        low.observe(key, offset)
    assert high.selected()[0][0] == 1
    assert low.selected()[0][0] == 2


def test_positive_cache_preserves_results_and_saves_checks(tmp_path) -> None:
    initial = list(range(100))
    stream = [1] * 100
    plain = audit_run(initial, stream, Policy.ARRIVAL, budget=10, seed=3, directory=tmp_path)
    cached = audit_run(
        initial, stream, Policy.ARRIVAL_CACHE, budget=10, seed=3, directory=tmp_path
    )
    assert plain["exact_checks"] == 10
    assert cached["exact_checks"] == 1
    assert plain["omitted_distinct"] == cached["omitted_distinct"] == 0


@pytest.mark.parametrize("policy", list(Policy))
def test_sqlite_filter_pipeline_budget_and_exact_reference(tmp_path, policy: Policy) -> None:
    initial, stream = synthetic_workload("mixed", initial_count=200)
    result = audit_run(initial, stream, policy, budget=10000, seed=4, directory=tmp_path)
    assert result["omitted_distinct"] == 0
    assert result["exact_checks"] <= 10000
    assert result["processed_total"] == len(set(initial) | set(stream))
    assert result["authoritative_bytes"] >= result["processed_total"] * 16
    assert result["source_identifier_bytes"] == len(stream) * 16
    assert result["filter_payload_bytes"] > 0


def test_serialization_and_no_false_negative() -> None:
    bloom = KeyedBloom(200, 0.05, 12)
    keys = list(range(200))
    for key in keys:
        bloom.add(key)
    assert all(bloom.contains(key) for key in keys)
    assert key_bytes(257) == b"\x00" * 14 + b"\x01\x01"
    assert len(bloom.bitmap()) == bloom.payload_bytes()


def test_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        KeyedBloom(0, 0.05, 0)
    with pytest.raises(ValueError):
        Sampler(Policy.ARRIVAL, -1, 0)
    with pytest.raises(ValueError):
        omitted_probability(0, Fraction(1, 2))
    with pytest.raises(ValueError):
        omitted_probability(2, Fraction(3, 2))
    with pytest.raises(ValueError):
        synthetic_workload("unknown")
