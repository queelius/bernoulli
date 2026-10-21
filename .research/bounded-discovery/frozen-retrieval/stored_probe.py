"""Conditional algebraic witness in the existing stored retrieval implementation."""

from dataclasses import dataclass

from bernoulli.maps.retrieval import GF2Retrieval


@dataclass(frozen=True)
class StoredWitness:
    seed: int
    slot_count: int
    stored_value: int
    stored_positions: tuple[int, ...]
    query_keys: tuple[str, ...]
    query_positions: tuple[tuple[int, ...], ...]
    query_values: tuple[int, ...]
    tested_candidates: int


def stored_witness(seed: int, limit: int = 100_000) -> StoredWitness:
    """Choose queries after the public seed; this is not an FPR experiment.

    Private fields are read solely to instrument the existing implementation.
    Knowledge of the stored row is granted here: no key-recovery attack is
    inferred from this conditional diagnostic.
    """
    retrieval = GF2Retrieval({b"stored": 0x5A}, value_bits=8, seed=seed)
    segment = retrieval._seg
    a, b, c = retrieval._positions(b"stored", segment, retrieval._seed_used)
    aa = (a + 1) % segment
    bb = segment + (b - segment + 1) % segment
    cc = 2 * segment + (c - 2 * segment + 1) % segment
    targets = ((a, bb, cc), (aa, b, cc), (aa, bb, c))
    found: dict[tuple[int, ...], bytes] = {}
    for index in range(limit):
        key = f"absent-{index}".encode()
        positions = retrieval._positions(key, segment, retrieval._seed_used)
        if positions in targets:
            found.setdefault(positions, key)
        if len(found) == 3:
            keys = tuple(found[row] for row in targets)
            return StoredWitness(
                retrieval._seed_used, retrieval._m, 0x5A, (a, b, c),
                tuple(key.decode() for key in keys), targets,
                tuple(retrieval.query(key) for key in keys), index + 1,
            )
    raise RuntimeError("search limit reached before all three rows were found")
