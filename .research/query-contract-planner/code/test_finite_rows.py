from fractions import Fraction
from itertools import product

import pytest

from finite_rows import FrozenRows, collision_rate, select_width
from contracts import Budget, error_bound


def test_actual_finite_four_wise_joint_collision_law():
    # Over all 7^4 degree<=3 polynomials, the four distinct inputs 0,1,2,3
    # are uniform independent. Reducing field outputs modulo2 is not uniform.
    q = collision_rate(1, 7)
    assert q == Fraction(25, 49)
    count = 0
    for coefficients in product(range(7), repeat=4):
        rows = FrozenRows.from_coefficients([0, 0], 2, 1, coefficients, prime=7)
        count += rows.contains(0, 1) and rows.contains(1, 1)
    assert Fraction(count, 7**4) == q * q


def test_finite_payload_reloads_and_never_forgets_insertions():
    values = [1, 0, 3, 1, 2]
    rows = FrozenRows.build(values, 4, 7, seed=209)
    restored = FrozenRows.deserialize(rows.serialize())
    assert restored == rows
    assert restored.payload_bytes == len(rows.serialize())
    assert all(restored.contains(i, value) for i, value in enumerate(values))
    assert [rows.contains(0, v) for v in range(4)] == [restored.contains(0, v) for v in range(4)]
    for data in (b'', rows.serialize()[:-1], b'broken!!' + rows.serialize()[8:]):
        with pytest.raises(ValueError):
            FrozenRows.deserialize(data)
    for row, value in ((-1, 0), (5, 0), (0, -1), (0, 4)):
        with pytest.raises(ValueError):
            rows.contains(row, value)


@pytest.mark.parametrize('k', [1, 8, 64, 1024])
def test_width_selection_is_smallest_certified_integer(k):
    target = Fraction(1, 20)
    for budget in (Budget.ORDINARY_UNION, Budget.CONSTRAINED_UNION):
        width = select_width(k, target, budget)
        assert error_bound(budget, k, collision_rate(width)) <= target
        if width > 1:
            assert error_bound(budget, k, collision_rate(width - 1)) > target


def test_requires_injective_valid_field_encoding():
    with pytest.raises(ValueError):
        FrozenRows.from_coefficients([0, 0, 0], 3, 1, (1, 1, 1, 1), prime=7)
    with pytest.raises(ValueError):
        FrozenRows.from_coefficients([2], 2, 1, (1, 1, 1, 1))
    with pytest.raises(ValueError):
        select_width(5, Fraction(1, 20), Budget.CONSTRAINED_PRODUCT)
