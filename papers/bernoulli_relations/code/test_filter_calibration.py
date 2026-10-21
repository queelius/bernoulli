"""Invariants and integration checks for the stored-filter calibration probe."""

import csv
import json
from dataclasses import FrozenInstanceError
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
from math import prod
from pathlib import Path
from unittest.mock import Mock

import filter_calibration
import pytest
from filter_calibration import (
    ExperimentConfig,
    FrozenBloom,
    Pair,
    Representation,
    SymmetricFilter,
    TruthProfile,
    calibrate_source_rate,
    construction_interval,
    cycle_probability,
    cycle_sensitivity,
    cycle_value,
    extremal_cycle_profile,
    make_workload,
    method_specs,
    run_experiment,
    write_results,
)


def test_calibration_limits_and_inversion():
    assert calibrate_source_rate(0.0, 8) == 0.0
    assert calibrate_source_rate(1.0, 8) == 1.0
    assert calibrate_source_rate(0.0, 0) == 1.0
    assert calibrate_source_rate(0.05, 1) == pytest.approx(0.05)
    rate = calibrate_source_rate(0.05, 8)
    assert 1.0 - (1.0 - rate) ** 8 == pytest.approx(0.05)
    assert calibrate_source_rate(1e-15, 8) == pytest.approx(1.25e-16, rel=1e-12, abs=0.0)


@pytest.mark.parametrize("target", [-0.1, 1.1, float("nan"), float("inf")])
def test_invalid_calibration_rate(target):
    with pytest.raises(ValueError):
        calibrate_source_rate(target, 8)


def test_invalid_sensitivity():
    with pytest.raises(ValueError):
        calibrate_source_rate(0.1, -1)


def test_bloom_uses_frozen_bytes_and_round_trips():
    keys = [f"true-{i}".encode() for i in range(200)]
    bloom = FrozenBloom.build(keys + keys, 0.05, bytes(range(16)))
    assert bloom.inserted_count == len(keys)
    assert isinstance(bloom.bits, bytes)
    assert all(bloom.contains(key) for key in keys)
    unseen = [f"absent-{i}".encode() for i in range(300)]
    answers = [bloom.contains(key) for key in unseen]
    assert [bloom.contains(key) for key in unseen] == answers
    assert bloom.contains(unseen[0]) == bloom.contains(unseen[0])
    recovered = FrozenBloom.deserialize(bloom.serialize())
    assert recovered == bloom
    assert [recovered.contains(key) for key in unseen] == answers
    assert len(bloom.serialize()) == bloom.payload_bytes
    assert bloom.payload_bytes == len(bloom.bits) + 40
    with pytest.raises(FrozenInstanceError):
        bloom.bits = b""
    assert bloom.conditional_fpr == pytest.approx(
        prod(count / bloom.partition_bits for count in bloom.occupancies)
    )
    expected_occupancy = 1.0 - (1.0 - 1.0 / bloom.partition_bits) ** len(keys)
    assert expected_occupancy**bloom.partitions <= 0.05 * (1.0 + 1e-12)


def test_empty_bloom_has_no_false_positives():
    bloom = FrozenBloom.build([], 0.05, b"\0" * 16)
    assert bloom.inserted_count == 0
    assert bloom.conditional_fpr == 0.0
    assert not bloom.contains(b"anything")


@pytest.mark.parametrize("target", [0.0, 1.0, -1.0, float("nan")])
def test_bloom_rejects_unattainable_or_invalid_target(target):
    with pytest.raises(ValueError):
        FrozenBloom.build([b"x"], target, b"\0" * 16)


def test_bloom_sizing_rejects_negative_count():
    with pytest.raises(ValueError):
        filter_calibration.bloom_dimensions(-1, 0.05)


def test_bloom_rejects_invalid_salt_and_payload():
    with pytest.raises(ValueError):
        FrozenBloom.build([b"x"], 0.1, b"bad")
    with pytest.raises(ValueError):
        FrozenBloom.deserialize(b"truncated")
    payload = FrozenBloom.build([b"x"], 0.1, b"\0" * 16).serialize()
    with pytest.raises(ValueError):
        FrozenBloom.deserialize(b"badmagic" + payload[8:])
    with pytest.raises(ValueError):
        FrozenBloom.deserialize(payload[:-1])


def test_range_reduction_rejects_incomplete_residue_block(monkeypatch):
    # A 128-bit maximum falls in the incomplete block for a 24-position range.
    # The next independent domain output is accepted; this is not modulo folding.
    digests = iter([(2**128 - 1).to_bytes(16, "big"), (17).to_bytes(16, "big")])
    fake_hash = Mock(side_effect=lambda *args, **kwargs: Mock(digest=lambda: next(digests)))
    monkeypatch.setattr(filter_calibration.hashlib, "blake2b", fake_hash)
    assert filter_calibration._position(b"key", b"\0" * 16, 3, 24) == 17
    assert fake_hash.call_count == 2
    assert fake_hash.call_args_list[0].args[0] != fake_hash.call_args_list[1].args[0]


@pytest.mark.parametrize("representation", list(Representation))
def test_symmetric_representation_and_reflexive_orbits(representation):
    true_pairs = [Pair(1, 2), Pair(2, 1), Pair(7, 7)]
    relation = SymmetricFilter.build(true_pairs, representation, 0.1, b"\2" * 16)
    assert all(relation.contains(pair) for pair in true_pairs)
    expected = 2 if representation is Representation.CANONICAL else 3
    assert relation.bloom.inserted_count == expected
    for left, right in product(range(10), repeat=2):
        assert relation.contains(Pair(left, right)) == relation.contains(Pair(right, left))
    assert relation.source_probability(Pair(7, 7)) == relation.bloom.conditional_fpr


def test_ordered_or_probability_preserves_tiny_positive_rates():
    # One occupied bit in each of 20 eight-bit partitions gives p = 2^-60.
    bloom = FrozenBloom.build([b"inserted"], 2.0**-20, b"\3" * 16)
    rate = Fraction(1, 2**60)
    assert bloom.conditional_fpr == float(rate)
    relation = SymmetricFilter(Representation.ORDERED_OR, bloom)
    expected = float(1 - (1 - rate) ** 2)
    assert relation.source_probability(Pair(1, 2)) == pytest.approx(
        expected, rel=1e-14, abs=0.0
    )


def test_ordered_or_probability_at_saturation():
    bloom = FrozenBloom(1, 8, 8, b"\4" * 16, b"\xff")
    relation = SymmetricFilter(Representation.ORDERED_OR, bloom)
    assert relation.source_probability(Pair(1, 2)) == 1.0


def test_pair_has_unambiguous_fixed_width_encoding():
    assert Pair(1, 23).encode() != Pair(12, 3).encode()
    assert Pair(2, 1).canonical() == Pair(1, 2)
    with pytest.raises(ValueError):
        Pair(-1, 0)
    with pytest.raises(ValueError):
        Pair(0, 2**64)


@pytest.mark.parametrize("size", range(3, 15))
def test_extremal_cycle_is_maximal_false_with_claimed_sensitivity(size):
    truth = extremal_cycle_profile(size)
    assert not cycle_value(truth)
    zeros = [index for index, bit in enumerate(truth) if not bit]
    assert len(zeros) == cycle_sensitivity(size)
    for index in zeros:
        flipped = list(truth)
        flipped[index] = True
        assert cycle_value(flipped)
    alpha = 0.13
    assert cycle_probability(truth, alpha) == pytest.approx(
        1.0 - (1.0 - alpha) ** len(zeros)
    )


@pytest.mark.parametrize("alpha", [0.0, 0.1, 0.5, 1.0])
def test_cycle_probability_matches_exhaustive_truth_profiles(alpha):
    for size in range(3, 7):
        for truth in product([False, True], repeat=size):
            missing = [index for index, bit in enumerate(truth) if not bit]
            probability = 0.0
            for flips in product([False, True], repeat=len(missing)):
                observed = list(truth)
                for index, flip in zip(missing, flips, strict=True):
                    observed[index] = flip
                weight = alpha ** sum(flips) * (1.0 - alpha) ** (len(flips) - sum(flips))
                probability += weight * cycle_value(observed)
            assert cycle_probability(truth, alpha) == pytest.approx(probability, abs=1e-14)


@pytest.mark.parametrize("exponent", [30, 60, 120])
def test_cycle_probability_preserves_tiny_success_mass(exponent):
    rate = Fraction(1, 2**exponent)
    boundary = extremal_cycle_profile(12)
    boundary_probability = float(1 - (1 - rate) ** 8)
    # For a three-cycle, a witness exists exactly when at least two bits are true.
    all_false_probability = float(3 * rate**2 * (1 - rate) + rate**3)
    assert cycle_probability(boundary, float(rate)) == pytest.approx(
        boundary_probability, rel=1e-14, abs=0.0
    )
    assert cycle_probability((False, False, False), float(rate)) == pytest.approx(
        all_false_probability, rel=1e-14, abs=0.0
    )


def test_workload_disjoint_sources_and_truths():
    workload = make_workload(cycle_size=12, bundles=5, background=10)
    assert len(workload.true_pairs) == 10 + 5 * (4 + 2)
    queried = [pair for group in workload.groups for bundle in group.bundles for pair in bundle]
    assert len(queried) == len(set(queried))
    for group in workload.groups:
        assert cycle_value(group.truth) == (group.profile is TruthProfile.TRUE_EDGE)
        for bundle in group.bundles:
            assert tuple(pair in workload.true_pairs for pair in bundle) == group.truth


def test_method_calibration_accounts_for_both_ordered_orientations():
    naive, canonical, repaired = method_specs(0.05, 8)
    assert naive.source_target == 0.05
    assert 1.0 - (1.0 - canonical.source_target) ** 8 == pytest.approx(0.05)
    assert 1.0 - (1.0 - repaired.source_target) ** 16 == pytest.approx(0.05)


def test_dependence_budget_sizing_comparison():
    independent, conservative = filter_calibration.canonical_budget_sizing(ExperimentConfig())
    assert independent.source_target == calibrate_source_rate(0.05, 8)
    assert conservative.source_target == 0.05 / 8
    assert independent.inserted_representatives == conservative.inserted_representatives == 2816
    assert independent.payload_bytes == 3752
    assert conservative.payload_bytes == 3768
    assert independent.header_bytes == conservative.header_bytes == 40
    assert independent.payload_bytes == independent.bit_bytes + independent.header_bytes
    saving = 1 - independent.payload_bytes / conservative.payload_bytes
    assert saving == pytest.approx(0.004246284501061571)
    print(
        f"Canonical sizing only: independent={independent.payload_bytes} bytes, "
        f"union={conservative.payload_bytes} bytes, relative saving={saving:.10%}"
    )


def test_interval_uses_builds_as_units():
    estimate = construction_interval([0.0, 0.0, 1.0, 1.0])
    assert estimate.mean == 0.5
    assert estimate.standard_error == pytest.approx((1.0 / 12.0) ** 0.5)
    assert estimate.lower == 0.0
    assert estimate.upper == 1.0
    with pytest.raises(ValueError):
        construction_interval([0.5])


@pytest.mark.parametrize(
    "kwargs",
    [
        {"builds": 1}, {"bundles": 0}, {"background": -1}, {"cycle_size": 2},
        {"query_target": 0.0}, {"query_target": 1.0}, {"query_target": float("nan")},
    ],
)
def test_invalid_experiment_config(kwargs):
    with pytest.raises(ValueError):
        ExperimentConfig(**kwargs)


def test_invalid_probability_and_workload_inputs():
    with pytest.raises(ValueError):
        cycle_probability([False, False], 0.1)
    with pytest.raises(ValueError):
        cycle_probability([False] * 3, float("nan"))
    with pytest.raises(ValueError):
        make_workload(cycle_size=3, bundles=0, background=0)


def test_small_experiment_is_reproducible_and_writes_structured_results(tmp_path):
    config = ExperimentConfig(builds=4, bundles=3, background=200, cycle_size=6, seed=203)
    first = run_experiment(config)
    second = run_experiment(config)
    assert len(first.builds) == 12
    assert len(first.queries) == 36
    assert [row.payload_sha256 for row in first.builds] == [
        row.payload_sha256 for row in second.builds
    ]
    assert [row.positives for row in first.queries] == [row.positives for row in second.queries]
    assert all(row.false_negatives == 0 for row in first.queries)
    assert all(row.repeat_mismatches == row.symmetry_mismatches == 0 for row in first.queries)
    assert len({row.salt_hex for row in first.builds}) == len(first.builds)
    assert all(row.inserted_false_negatives == 0 for row in first.builds)
    assert all(row.conditional_key_fpr <= row.source_target for row in first.builds)
    assert all(row.construction_attempts >= 1 for row in first.builds)
    assert any(row.construction_attempts > 1 for row in first.builds)
    assert all(
        row.conditional_query_envelope <= config.query_target + 1e-14
        for row in first.builds if row.method != "canonical_naive"
    )
    write_results(first, tmp_path)
    assert {path.name for path in tmp_path.iterdir()} == {
        "builds.csv", "queries.csv", "summary.csv", "results.json"
    }


def test_cli_runs_small_experiment(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(
        filter_calibration.sys, "argv",
        [
            "filter_calibration.py", "--builds", "2", "--bundles", "2",
            "--background", "20", "--cycle-size", "3", "--output", str(tmp_path),
        ],
    )
    filter_calibration.main()
    assert "ordered_or_calibrated" in capsys.readouterr().out
    assert (tmp_path / "results.json").exists()


def test_exact_recorded_occupancy_contracts():
    """Audit saved builds exactly, independently of floating acceptance decisions.

    Run with ``pytest -s -k exact_recorded`` to display exact-audit summaries.
    The decimal query target in the manifest is interpreted as an exact rational;
    source targets are also checked against their actual binary float values.
    """
    folder = Path(__file__).resolve().parents[1] / "data" / "calibration"
    metadata = json.loads((folder / "results.json").read_text(), parse_float=Decimal)
    target = Fraction(metadata["config"]["query_target"])
    sensitivity = metadata["cycle_sensitivity"]
    methods = method_specs(float(target), sensitivity)
    with (folder / "builds.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == metadata["config"]["builds"] * len(methods)
    for index, method in enumerate(methods):
        envelopes = []
        method_rows = [row for row in rows if row["method"] == method.name]
        assert len(method_rows) == metadata["config"]["builds"]
        for row in method_rows:
            occupancies = json.loads(row["occupancies"])
            partition_bits = int(row["partition_bits"])
            partitions = int(row["partitions"])
            assert len(occupancies) == partitions
            assert all(0 <= count <= partition_bits for count in occupancies)
            rate = Fraction(prod(occupancies), partition_bits**partitions)
            # No recorded accepted build would fail an exact post-acceptance
            # source check against the implementation's binary float threshold.
            assert rate <= Fraction.from_float(float(row["source_target"]))
            multiplicity = 2 if method.representation is Representation.ORDERED_OR else 1
            envelope = 1 - (1 - rate) ** (sensitivity * multiplicity)
            if index == 0:  # The first structured method is the naive source budget.
                assert rate <= target
                assert envelope <= 1 - (1 - target) ** sensitivity
            else:
                # This compares to the exact decimal query target, not a rounded
                # source root or a stored approximate conditional probability.
                assert envelope <= target
            envelopes.append((envelope, int(row["build"])))
        maximum, build = max(envelopes)
        margin = target - maximum
        with localcontext() as context:
            context.prec = 50
            decimal_maximum = Decimal(maximum.numerator) / Decimal(maximum.denominator)
            decimal_margin = Decimal(margin.numerator) / Decimal(margin.denominator)
        print(
            f"{method.name}: {len(method_rows)} exact audits; "
            f"max envelope={decimal_maximum} (build {build}); "
            f"query-target margin={decimal_margin}"
        )
