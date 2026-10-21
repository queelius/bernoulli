"""Exact enumeration of small frozen linear retrieval transcripts."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product


@dataclass(frozen=True)
class System:
    columns: int
    constraints: tuple[int, ...]
    targets: tuple[int, ...]
    queries: tuple[int, ...]
    bits: int = 1

    def __post_init__(self) -> None:
        if self.columns < 0 or self.bits < 1:
            raise ValueError("invalid dimensions")
        if len(self.constraints) != len(self.targets):
            raise ValueError("one target is required for each constraint")
        if any(row < 0 or row >= 1 << self.columns for row in self.constraints + self.queries):
            raise ValueError("row exceeds the declared slot space")
        if any(target < 0 or target >= 1 << self.bits for target in self.targets):
            raise ValueError("target exceeds the declared word width")


def rank(rows: tuple[int, ...]) -> int:
    basis: dict[int, int] = {}
    for row in rows:
        if row < 0:
            raise ValueError("negative binary row")
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return len(basis)


def evaluate(row: int, slots: tuple[int, ...]) -> int:
    result = 0
    for column, value in enumerate(slots):
        if row & (1 << column):
            result ^= value
    return result


def transcript_law(system: System) -> dict[tuple[int, ...], Fraction]:
    if system.columns * system.bits > 16:
        raise ValueError("exhaustive probe limited to 65536 slot arrays")
    counts: dict[tuple[int, ...], int] = {}
    total = 0
    for slots in product(range(1 << system.bits), repeat=system.columns):
        if all(evaluate(row, slots) == value for row, value in
               zip(system.constraints, system.targets, strict=True)):
            word = tuple(evaluate(row, slots) for row in system.queries)
            counts[word] = counts.get(word, 0) + 1
            total += 1
    if not total:
        raise ValueError("inconsistent constraint system")
    return {word: Fraction(count, total) for word, count in counts.items()}


def image_dimension(system: System) -> int:
    return rank(system.constraints + system.queries) - rank(system.constraints)
