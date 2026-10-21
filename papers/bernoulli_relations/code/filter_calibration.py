#!/usr/bin/env python3
"""Query calibration on frozen, serialized partitioned Bloom filters.

Run from the workspace root with::

    bernoulli-py/.venv/bin/python papers/bernoulli_relations/code/filter_calibration.py

No runtime dependency outside Python 3.11+ is needed. Exact relation keys exist
only during construction and validation: ``contains`` reads a frozen bit array,
never an exact-membership oracle. Candidate constructions use fresh salts from
a reproducibly seeded PRNG. Candidates are accepted using ONLY inserted-key
occupancies, until the conditional ideal key rate meets the source target.
Repeated queries never sample randomness.

The analytical comparator uses an IDEAL random function for each partition.
Conditional on the inserted-key hashes, distinct absent-key hashes are then
independent, with membership probability equal to the product of the occupied
fractions. BLAKE2b with domain separation is the concrete implementation, not a
proof of that idealization. Shared occupancy makes unconditional errors dependent
even in the ideal model. We average conditional query probabilities over builds,
and use builds, rather than within-build queries, as the uncertainty units.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import random
import statistics
import struct
import sys
import time
from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass, fields
from enum import StrEnum
from pathlib import Path


def calibrate_source_rate(query_target: float, sensitivity: int) -> float:
    """Invert the independent one-sided contract, including its limits.

    Zero sensitivity permits every source rate. A zero target at positive
    sensitivity needs exact storage; a finite Bloom filter cannot supply it.
    """
    if not math.isfinite(query_target) or not 0.0 <= query_target <= 1.0:
        raise ValueError("query target must be finite and in [0, 1]")
    if sensitivity < 0:
        raise ValueError("sensitivity must be nonnegative")
    if sensitivity == 0 or query_target == 1.0:
        return 1.0
    return -math.expm1(math.log1p(-query_target) / sensitivity)


@dataclass(frozen=True, order=True, slots=True)
class Pair:
    """An ordered pair of unsigned 64-bit identifiers; no string parsing."""

    left: int
    right: int

    def __post_init__(self) -> None:
        if not 0 <= self.left < 2**64 or not 0 <= self.right < 2**64:
            raise ValueError("pair identifiers must be unsigned 64-bit integers")

    def encode(self) -> bytes:
        return struct.pack(">QQ", self.left, self.right)

    def reverse(self) -> Pair:
        return Pair(self.right, self.left)

    def canonical(self) -> Pair:
        return self if self.left <= self.right else self.reverse()


_HEADER = struct.Struct(">8sIIQ16s")
_MAGIC = b"BRELCAL1"
_HASH_SPACE = 2**128


def _position(key: bytes, salt: bytes, partition: int, partition_bits: int) -> int:
    """Uniform range reduction under the ideal-hash model, with domain tags.

    Rejection avoids a modulo-bias qualification. It is vanishingly unlikely at
    these sizes but matters to the stated ideal comparator. The salt is public
    construction randomness; this experiment makes no cryptographic claim.
    """
    limit = _HASH_SPACE - _HASH_SPACE % partition_bits
    retry = 0
    while True:
        digest = hashlib.blake2b(
            struct.pack(">II", partition, retry) + key,
            key=salt,
            digest_size=16,
            person=b"brel-filter-v1",
        ).digest()
        value = int.from_bytes(digest, "big")
        if value < limit:
            return value % partition_bits
        retry += 1


def bloom_dimensions(count: int, target_rate: float) -> tuple[int, int]:
    """Choose partition count and bits per partition without building a filter."""
    if count < 0:
        raise ValueError("inserted count must be nonnegative")
    if not math.isfinite(target_rate) or not 0.0 < target_rate < 1.0:
        raise ValueError("finite Bloom target must be in (0, 1); zero requires exact storage")
    if count == 0:
        return 1, 8
    partitions = max(1, math.ceil(-math.log2(target_rate)))
    occupancy_target = target_rate ** (1.0 / partitions)
    inverse_bits = -math.expm1(math.log1p(-occupancy_target) / count)
    partition_bits = 8 * math.ceil((1.0 / inverse_bits) / 8)
    return partitions, partition_bits


@dataclass(frozen=True, slots=True)
class FrozenBloom:
    """Immutable partitioned Bloom filter, with its actual portable payload.

    The payload contains a 40-byte version/dimensions/count/salt header followed
    by byte-aligned partitions. Python object overhead is not included.
    """

    partitions: int
    partition_bits: int
    inserted_count: int
    salt: bytes
    bits: bytes

    @classmethod
    def build(cls, keys: Iterable[bytes], target_rate: float, salt: bytes) -> FrozenBloom:
        if len(salt) != 16:
            raise ValueError("construction salt must be exactly 16 bytes")
        distinct = sorted(set(keys))
        count = len(distinct)
        partitions, partition_bits = bloom_dimensions(count, target_rate)
        bits = bytearray(partitions * partition_bits // 8)
        for key in distinct:
            for partition in range(partitions):
                position = partition * partition_bits + _position(
                    key, salt, partition, partition_bits
                )
                bits[position // 8] |= 1 << (position % 8)
        return cls(partitions, partition_bits, count, salt, bytes(bits))

    def contains(self, key: bytes) -> bool:
        for partition in range(self.partitions):
            position = partition * self.partition_bits + _position(
                key, self.salt, partition, self.partition_bits
            )
            if not self.bits[position // 8] & (1 << (position % 8)):
                return False
        return True

    @property
    def occupancies(self) -> tuple[int, ...]:
        width = self.partition_bits // 8
        return tuple(
            sum(byte.bit_count() for byte in self.bits[start : start + width])
            for start in range(0, len(self.bits), width)
        )

    @property
    def conditional_fpr(self) -> float:
        """Conditional ideal-random-function rate, not a measured BLAKE2 rate."""
        return math.prod(count / self.partition_bits for count in self.occupancies)

    @property
    def payload_bytes(self) -> int:
        return _HEADER.size + len(self.bits)

    def serialize(self) -> bytes:
        return _HEADER.pack(
            _MAGIC, self.partitions, self.partition_bits, self.inserted_count, self.salt
        ) + self.bits

    @classmethod
    def deserialize(cls, payload: bytes) -> FrozenBloom:
        if len(payload) < _HEADER.size:
            raise ValueError("truncated Bloom header")
        magic, partitions, partition_bits, count, salt = _HEADER.unpack_from(payload)
        if magic != _MAGIC or partitions == 0 or partition_bits == 0 or partition_bits % 8:
            raise ValueError("invalid Bloom format or dimensions")
        if len(payload) != _HEADER.size + partitions * partition_bits // 8:
            raise ValueError("Bloom payload length disagrees with its dimensions")
        return cls(partitions, partition_bits, count, salt, payload[_HEADER.size :])


class Representation(StrEnum):
    CANONICAL = "canonical"
    ORDERED_OR = "ordered_or"


@dataclass(frozen=True, slots=True)
class SymmetricFilter:
    representation: Representation
    bloom: FrozenBloom

    @classmethod
    def build(
        cls,
        true_pairs: Iterable[Pair],
        representation: Representation,
        target_rate: float,
        salt: bytes,
    ) -> SymmetricFilter:
        canonical = {pair.canonical() for pair in true_pairs}
        keys = {pair.encode() for pair in canonical}
        if representation is Representation.ORDERED_OR:
            keys.update(pair.reverse().encode() for pair in canonical)
        return cls(representation, FrozenBloom.build(keys, target_rate, salt))

    def contains(self, pair: Pair) -> bool:
        if self.representation is Representation.CANONICAL:
            return self.bloom.contains(pair.canonical().encode())
        return self.bloom.contains(pair.encode()) or self.bloom.contains(pair.reverse().encode())

    def source_probability(self, pair: Pair) -> float:
        """Conditional ideal rate of an absent symmetry orbit, including diagonals."""
        rate = self.bloom.conditional_fpr
        if self.representation is Representation.CANONICAL or pair.left == pair.right:
            return rate
        if rate == 1.0:
            return 1.0
        return -math.expm1(2 * math.log1p(-rate))


def cycle_value(values: Sequence[bool]) -> bool:
    return any(value and values[(index + 1) % len(values)] for index, value in enumerate(values))


def cycle_sensitivity(size: int) -> int:
    if size < 3:
        raise ValueError("a simple cycle needs at least three sources")
    return size - math.ceil(size / 3)


def extremal_cycle_profile(size: int) -> tuple[bool, ...]:
    """A smallest maximal independent set, by cyclic gaps of two or three."""
    cycle_sensitivity(size)
    selected = math.ceil(size / 3)
    extra = size - 2 * selected
    truth = [False] * size
    position = 0
    for index in range(selected):
        truth[position] = True
        position += 2 + (index < extra)
    return tuple(truth)


def cycle_probability(truth: Sequence[bool], absent_rate: float) -> float:
    """Evaluate independent-source probability using direct success mass.

    The two transient states record the last bit with no witnessed edge yet.
    Each transition from a last-one state to another one contributes disjoint
    first-witness mass. Accumulating that mass avoids subtracting a near-one
    no-witness probability, which loses tiny positive query probabilities.
    """
    if len(truth) < 3 or not 0.0 <= absent_rate <= 1.0:
        raise ValueError("need a cycle of size >= 3 and a rate in [0, 1]")
    rates = [1.0 if bit else absent_rate for bit in truth]
    witness_mass = 0.0
    for first in (False, True):
        last_zero = 0.0 if first else 1.0 - rates[0]
        last_one = rates[0] if first else 0.0
        for rate in rates[1:]:
            witness_mass += last_one * rate
            last_zero, last_one = (last_zero + last_one) * (1.0 - rate), last_zero * rate
        if first:
            witness_mass += last_one
    return min(1.0, max(0.0, witness_mass))


class TruthProfile(StrEnum):
    ALL_FALSE = "all_false"
    BOUNDARY_FALSE = "boundary_false"
    TRUE_EDGE = "true_edge"


@dataclass(frozen=True, slots=True)
class QueryGroup:
    profile: TruthProfile
    truth: tuple[bool, ...]
    bundles: tuple[tuple[Pair, ...], ...]


@dataclass(frozen=True, slots=True)
class Workload:
    true_pairs: frozenset[Pair]
    groups: tuple[QueryGroup, ...]


def make_workload(cycle_size: int, bundles: int, background: int) -> Workload:
    cycle_sensitivity(cycle_size)
    if bundles < 1 or background < 0:
        raise ValueError("need positive bundle count and nonnegative background count")
    true_pairs = {Pair(2 * index, 2 * index + 1) for index in range(background)}
    groups = []
    next_source = background
    profiles = (
        (TruthProfile.ALL_FALSE, (False,) * cycle_size),
        (TruthProfile.BOUNDARY_FALSE, extremal_cycle_profile(cycle_size)),
        (TruthProfile.TRUE_EDGE, (True, True) + (False,) * (cycle_size - 2)),
    )
    for profile, truth in profiles:
        queries = []
        for _ in range(bundles):
            pairs = tuple(
                Pair(2 * index, 2 * index + 1)
                for index in range(next_source, next_source + cycle_size)
            )
            true_pairs.update(pair for pair, bit in zip(pairs, truth, strict=True) if bit)
            queries.append(pairs)
            next_source += cycle_size
        groups.append(QueryGroup(profile, truth, tuple(queries)))
    return Workload(frozenset(true_pairs), tuple(groups))


@dataclass(frozen=True, slots=True)
class Method:
    name: str
    representation: Representation
    source_target: float


def method_specs(query_target: float, sensitivity: int) -> tuple[Method, ...]:
    return (
        Method("canonical_naive", Representation.CANONICAL, query_target),
        Method(
            "canonical_calibrated", Representation.CANONICAL,
            calibrate_source_rate(query_target, sensitivity),
        ),
        Method(
            "ordered_or_calibrated", Representation.ORDERED_OR,
            calibrate_source_rate(query_target, 2 * sensitivity),
        ),
    )


@dataclass(frozen=True, slots=True)
class Interval:
    mean: float
    standard_error: float
    lower: float
    upper: float


def construction_interval(values: Sequence[float]) -> Interval:
    """Approximate 95% normal interval, using construction averages as units."""
    if len(values) < 2:
        raise ValueError("uncertainty estimation needs at least two independent builds")
    mean = statistics.mean(values)
    standard_error = statistics.stdev(values) / math.sqrt(len(values))
    radius = statistics.NormalDist().inv_cdf(0.975) * standard_error
    return Interval(mean, standard_error, max(0.0, mean - radius), min(1.0, mean + radius))


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    builds: int = 160
    bundles: int = 128
    background: int = 2048
    cycle_size: int = 12
    query_target: float = 0.05
    seed: int = 20261013

    def __post_init__(self) -> None:
        if self.builds < 2:
            raise ValueError("need at least two independent builds")
        if self.bundles < 1 or self.background < 0:
            raise ValueError("invalid workload counts")
        cycle_sensitivity(self.cycle_size)
        if not 0.0 < self.query_target < 1.0:
            raise ValueError("finite-filter experiment requires target in (0, 1)")


@dataclass(frozen=True, slots=True)
class BudgetSizing:
    assumption: str
    source_target: float
    inserted_representatives: int
    partitions: int
    partition_bits: int
    bit_bytes: int
    header_bytes: int
    payload_bytes: int


def canonical_budget_sizing(config: ExperimentConfig) -> tuple[BudgetSizing, ...]:
    """Compare independent and union-bound budgets by dimensions only.

    This is not another Monte Carlo method. It isolates the source-budget effect
    while holding canonical representation, inserted keys, and sizing policy fixed.
    """
    sensitivity = cycle_sensitivity(config.cycle_size)
    count = len(make_workload(config.cycle_size, config.bundles, config.background).true_pairs)
    budgets = (
        ("independent_sources", calibrate_source_rate(config.query_target, sensitivity)),
        ("arbitrary_dependence_union_bound", config.query_target / sensitivity),
    )
    comparison = []
    for assumption, target in budgets:
        partitions, partition_bits = bloom_dimensions(count, target)
        bit_bytes = partitions * partition_bits // 8
        comparison.append(BudgetSizing(
            assumption, target, count, partitions, partition_bits,
            bit_bytes, _HEADER.size, bit_bytes + _HEADER.size,
        ))
    return tuple(comparison)


@dataclass(frozen=True, slots=True)
class BuildRow:
    method: str
    build: int
    salt_hex: str
    source_target: float
    inserted_representatives: int
    partitions: int
    partition_bits: int
    bit_bytes: int
    payload_bytes: int
    payload_sha256: str
    occupancies: tuple[int, ...]
    conditional_key_fpr: float
    conditional_query_envelope: float
    construction_attempts: int
    build_seconds: float
    inserted_false_negatives: int


@dataclass(frozen=True, slots=True)
class QueryRow:
    method: str
    build: int
    profile: TruthProfile
    exact_answer: bool
    bundles: int
    positives: int
    false_positives: int
    false_negatives: int
    conditional_model_positive_rate: float
    query_seconds: float
    repeat_mismatches: int
    symmetry_mismatches: int


@dataclass(frozen=True, slots=True)
class SummaryRow:
    method: str
    profile: TruthProfile
    source_target: float
    builds: int
    bundles_per_build: int
    inserted_representatives: int
    payload_bytes: int
    empirical_positive_rate: float
    construction_standard_error: float
    ci95_lower: float
    ci95_upper: float
    mean_conditional_model_positive_rate: float
    max_conditional_query_envelope: float
    mean_construction_attempts: float
    mean_build_ms: float
    mean_query_us: float
    total_false_negatives: int


@dataclass(frozen=True, slots=True)
class ExperimentResult:
    config: ExperimentConfig
    builds: tuple[BuildRow, ...]
    queries: tuple[QueryRow, ...]
    summary: tuple[SummaryRow, ...]


def query_cycle(relation: SymmetricFilter, pairs: Sequence[Pair]) -> bool:
    """Read each orbit once, then reuse it in its two neighboring witnesses."""
    return cycle_value(tuple(relation.contains(pair) for pair in pairs))


def run_experiment(config: ExperimentConfig) -> ExperimentResult:
    workload = make_workload(config.cycle_size, config.bundles, config.background)
    methods = method_specs(config.query_target, cycle_sensitivity(config.cycle_size))
    rng = random.Random(config.seed)
    build_rows = []
    query_rows = []
    for build in range(config.builds):
        # Rotate timing order to reduce a fixed-order warmup/load confound.
        offset = build % len(methods)
        for method in methods[offset:] + methods[:offset]:
            started = time.perf_counter()
            attempts = 0
            while True:
                attempts += 1
                salt = rng.getrandbits(128).to_bytes(16, "big")
                relation = SymmetricFilter.build(
                    workload.true_pairs, method.representation, method.source_target, salt
                )
                # Only inserted hashes decide acceptance. In the ideal model,
                # conditioning on this stopping rule leaves fixed absent-key
                # hash outputs independent and uniform in the accepted build.
                if relation.bloom.conditional_fpr <= method.source_target:
                    break
            build_seconds = time.perf_counter() - started
            payload = relation.bloom.serialize()
            # All measured queries use the serialized-and-reloaded bit payload.
            relation = SymmetricFilter(method.representation, FrozenBloom.deserialize(payload))
            inserted_false_negatives = sum(
                not relation.bloom.contains(pair.encode())
                for pair in workload.true_pairs
            )
            if method.representation is Representation.ORDERED_OR:
                inserted_false_negatives += sum(
                    not relation.bloom.contains(pair.reverse().encode())
                    for pair in workload.true_pairs
                )
            bloom = relation.bloom
            source_rate = relation.source_probability(workload.groups[0].bundles[0][0])
            envelope = -math.expm1(
                cycle_sensitivity(config.cycle_size) * math.log1p(-source_rate)
            )
            build_rows.append(BuildRow(
                method.name, build, salt.hex(), method.source_target,
                bloom.inserted_count, bloom.partitions, bloom.partition_bits,
                len(bloom.bits), len(payload), hashlib.sha256(payload).hexdigest(),
                bloom.occupancies, bloom.conditional_fpr, envelope, attempts, build_seconds,
                inserted_false_negatives,
            ))
            for group in workload.groups:
                started = time.perf_counter()
                answers = [query_cycle(relation, pairs) for pairs in group.bundles]
                query_seconds = time.perf_counter() - started
                # Validation is deliberately outside the timed query loop.
                repeated = [query_cycle(relation, pairs) for pairs in group.bundles]
                reversed_answers = [
                    query_cycle(relation, tuple(pair.reverse() for pair in pairs))
                    for pairs in group.bundles
                ]
                exact = cycle_value(group.truth)
                positives = sum(answers)
                rate = relation.source_probability(group.bundles[0][0])
                query_rows.append(QueryRow(
                    method.name, build, group.profile, exact, config.bundles,
                    positives, 0 if exact else positives,
                    config.bundles - positives if exact else 0,
                    cycle_probability(group.truth, rate), query_seconds,
                    sum(left != right for left, right in zip(answers, repeated, strict=True)),
                    sum(
                        left != right
                        for left, right in zip(answers, reversed_answers, strict=True)
                    ),
                ))
    summaries = []
    for method in methods:
        builds = [row for row in build_rows if row.method == method.name]
        for group in workload.groups:
            queries = [
                row for row in query_rows
                if row.method == method.name and row.profile is group.profile
            ]
            estimate = construction_interval([row.positives / row.bundles for row in queries])
            summaries.append(SummaryRow(
                method.name, group.profile, method.source_target, config.builds,
                config.bundles, builds[0].inserted_representatives, builds[0].payload_bytes,
                estimate.mean, estimate.standard_error, estimate.lower, estimate.upper,
                statistics.mean(row.conditional_model_positive_rate for row in queries),
                max(row.conditional_query_envelope for row in builds),
                statistics.mean(row.construction_attempts for row in builds),
                1000.0 * statistics.mean(row.build_seconds for row in builds),
                1e6 * statistics.mean(row.query_seconds / row.bundles for row in queries),
                sum(row.false_negatives for row in queries),
            ))
    return ExperimentResult(config, tuple(build_rows), tuple(query_rows), tuple(summaries))


def _write_csv(
    rows: Sequence[BuildRow] | Sequence[QueryRow] | Sequence[SummaryRow], path: Path
) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=[field.name for field in fields(rows[0])])
        writer.writeheader()
        for row in rows:
            record = asdict(row)
            if "occupancies" in record:
                record["occupancies"] = json.dumps(record["occupancies"])
            writer.writerow(record)


def write_results(result: ExperimentResult, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    _write_csv(result.builds, destination / "builds.csv")
    _write_csv(result.queries, destination / "queries.csv")
    _write_csv(result.summary, destination / "summary.csv")
    metadata = {
        "config": asdict(result.config),
        "cycle_sensitivity": cycle_sensitivity(result.config.cycle_size),
        "python": sys.version,
        "platform": platform.platform(),
        "hash": "BLAKE2b-128, 16-byte keyed salt, partition/rejection domain separation",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "uncertainty": (
            "Approximate 95% normal intervals over independent construction means; "
            "no independence of within-build query outcomes is assumed."
        ),
        "payload": (
            "Serialized bit array plus 40-byte metadata/salt header; excludes Python overhead."
        ),
        "construction_acceptance": (
            "Retry independent candidate salts until the product of occupied partition fractions "
            "does not exceed the source target. This uses only inserted-key hashes, "
            "never absent-query answers; build time includes retries."
        ),
        "comparator": (
            "Ideal independent random functions conditional on inserted-key hashes. "
            "Concrete hash and PRNG draws are empirical approximations, not independence proofs."
        ),
        "canonical_budget_sizing": [
            asdict(row) for row in canonical_budget_sizing(result.config)
        ],
        "canonical_budget_sizing_scope": (
            "Dimensions only, holding the canonical representation fixed; "
            "no fourth filter method or Monte Carlo measurement was run."
        ),
        "summary": [asdict(row) for row in result.summary],
    }
    (destination / "results.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    defaults = ExperimentConfig()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--builds", type=int, default=defaults.builds)
    parser.add_argument("--bundles", type=int, default=defaults.bundles)
    parser.add_argument("--background", type=int, default=defaults.background)
    parser.add_argument("--cycle-size", type=int, default=defaults.cycle_size)
    parser.add_argument("--query-target", type=float, default=defaults.query_target)
    parser.add_argument("--seed", type=int, default=defaults.seed)
    parser.add_argument(
        "--output", type=Path, default=Path(__file__).resolve().parents[1] / "data" / "calibration"
    )
    args = parser.parse_args()
    config = ExperimentConfig(
        args.builds, args.bundles, args.background, args.cycle_size, args.query_target, args.seed
    )
    result = run_experiment(config)
    write_results(result, args.output)
    for row in result.summary:
        print(
            f"{row.method:24} {row.profile:15} "
            f"observed={row.empirical_positive_rate:.6f} "
            f"CI=[{row.ci95_lower:.6f},{row.ci95_upper:.6f}] "
            f"ideal={row.mean_conditional_model_positive_rate:.6f} "
            f"bytes={row.payload_bytes}"
        )
    print(f"Wrote results to {args.output}")


if __name__ == "__main__":
    main()
