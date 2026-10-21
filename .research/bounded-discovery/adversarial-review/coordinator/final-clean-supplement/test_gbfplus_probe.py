"""Breaks concealed-endpoint claim, not an identifier-only security game."""

from collections import Counter
from functools import reduce
from itertools import permutations, product
from operator import xor

import pytest

from gbfplus_probe import Snapshot, insert, recover_domain_xor


def test_singleton_recipient_recovery_for_every_share_choice() -> None:
    for domain in range(4):
        for words in product(range(8), repeat=2):
            cells: list[int | None] = [None] * 7
            assert insert(cells, (5, 1, 3), 4 | domain, words, word_bits=3)
            snapshot = Snapshot(tuple(cells), count=1, k=3, word_bits=3)
            assert recover_domain_xor(snapshot, domain_bits=2) == domain


def test_every_share_uniform_but_full_view_separates_recipients() -> None:
    views: list[set[tuple[int | None, ...]]] = []
    for domain in (1, 2):
        distributions: list[Counter[int | None]] = [Counter() for _ in range(3)]
        support = set()
        for words in product(range(8), repeat=2):
            cells: list[int | None] = [None] * 5
            insert(cells, (0, 2, 4), 4 | domain, words, 3)
            support.add(tuple(cells))
            for j, index in enumerate((0, 2, 4)):
                distributions[j][cells[index]] += 1
        assert all(counts == Counter({word: 8 for word in range(8)})
                   for counts in distributions)
        views.append(support)
    assert len(views[0]) == len(views[1]) == 64
    assert views[0].isdisjoint(views[1])


def test_disjoint_batch_exposes_aggregate_without_row_labels() -> None:
    for n1, n2 in product(range(4), repeat=2):
        for words in product(range(8), repeat=2):
            cells: list[int | None] = [None] * 7
            assert insert(cells, (0, 4), 4 | n1, words[:1], 3)
            assert insert(cells, (1, 5), n2, words[1:], 3)
            assert recover_domain_xor(Snapshot(tuple(cells), 2, 2, 3), 2) == n1 ^ n2


def test_recovery_does_not_depend_on_support_order() -> None:
    for positions in permutations(range(4), 3):
        cells: list[int | None] = [None] * 4
        insert(cells, positions, 7, (1, 2), 3)
        assert recover_domain_xor(Snapshot(tuple(cells), 1, 3, 3), 2) == 3


def test_overlapping_insertion_preserves_rows_and_attack_abstains() -> None:
    cells: list[int | None] = [None] * 5
    assert insert(cells, (0, 1, 2), 5, (2, 3), 3)
    old = tuple(cells[:3])
    assert insert(cells, (1, 2, 4), 6, (), 3)
    assert tuple(cells[:3]) == old
    assert reduce(xor, (cells[i] for i in (0, 1, 2))) == 5
    assert reduce(xor, (cells[i] for i in (1, 2, 4))) == 6
    assert recover_domain_xor(Snapshot(tuple(cells), 2, 3, 3), 2) is None


def test_full_support_failure_is_atomic() -> None:
    cells: list[int | None] = [1, 2, 3, None]
    before = list(cells)
    assert not insert(cells, (0, 1, 2), 7, (), 3)
    assert cells == before


def test_padding_with_public_support_does_not_help_but_unlabelled_xor_is_uniform() -> None:
    # One random unused word suffices to mask the all-cells XOR statistic.
    cells: list[int | None] = [None] * 4
    insert(cells, (0, 1, 2), 5, (2, 7), 3)
    occupied = tuple(value is not None for value in cells)
    all_xors: Counter[int] = Counter()
    for padding in range(8):
        padded = tuple(padding if value is None else value for value in cells)
        retained_mask = tuple(value if flag else None
                              for value, flag in zip(padded, occupied, strict=True))
        assert recover_domain_xor(Snapshot(retained_mask, 1, 3, 3), 2) == 1
        all_xors[reduce(xor, padded)] += 1
    assert all_xors == Counter({word: 1 for word in range(8)})


def test_independent_recipient_mask_removes_endpoint_from_this_statistic() -> None:
    # This tests the statistic only; it is not a proof for an entire protocol.
    for domain in range(4):
        observed: Counter[int] = Counter()
        for pad in range(4):
            cells: list[int | None] = [None] * 5
            insert(cells, (0, 1, 4), 4 | (domain ^ pad), (3, 6), 3)
            result = recover_domain_xor(Snapshot(tuple(cells), 1, 3, 3), 2)
            assert result is not None
            observed[result] += 1
        assert observed == Counter({word: 1 for word in range(4)})


def test_empty_and_k_one_boundaries() -> None:
    assert recover_domain_xor(Snapshot((None,) * 5, 0, 3, 3), 2) is None
    cells: list[int | None] = [None] * 3
    assert insert(cells, (1,), 7, (), 3)
    assert recover_domain_xor(Snapshot(tuple(cells), 1, 1, 3), 2) == 3


def test_invalid_input_rejected_before_mutation() -> None:
    for positions, target, words, bits in [((0, 0), 1, (), 3), ((5,), 1, (), 3),
                                         ((0, 1), 8, (0,), 3), ((0, 1), 1, (), 3),
                                         ((0, 1), 1, (8,), 3), ((), 1, (), 3)]:
        cells: list[int | None] = [None] * 4
        with pytest.raises(ValueError):
            insert(cells, positions, target, words, bits)
        assert cells == [None] * 4
    with pytest.raises(ValueError):
        insert([9, None], (0, 1), 1, (), 3)
    for snapshot_cells, count, k, bits in [((None,), -1, 1, 3), ((None,), 0, 0, 3),
                                 ((None,), 0, 1, 0), ((8,), 1, 1, 3)]:
        with pytest.raises(ValueError):
            Snapshot(snapshot_cells, count, k, bits)
    with pytest.raises(ValueError):
        recover_domain_xor(Snapshot((None,), 0, 1, 3), 3)
