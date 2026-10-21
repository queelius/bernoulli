"""Integration with the existing stored GF2Retrieval, without modifying it."""

from functools import reduce
from operator import xor

import pytest

from joint_probe import rank
from stored_probe import stored_witness


@pytest.mark.parametrize("seed", [1, 2026, 3027])
def test_three_absent_queries_recover_stored_linear_combination(seed: int) -> None:
    witness = stored_witness(seed)
    assert len(set(witness.query_keys)) == 3
    assert all(key.startswith("absent-") for key in witness.query_keys)
    rows = tuple(sum(1 << position for position in row)
                 for row in witness.query_positions)
    stored_row = sum(1 << position for position in witness.stored_positions)
    assert rank(rows) == 3
    assert stored_row not in rows
    assert reduce(xor, rows) == stored_row
    assert reduce(xor, witness.query_values) == witness.stored_value
    assert 0 < witness.tested_candidates <= 100_000


def test_search_limit_is_explicit() -> None:
    with pytest.raises(RuntimeError, match="search limit"):
        stored_witness(1, limit=0)
