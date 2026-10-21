"""Protocol-specific finite probe; no pairing or cryptographic implementation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Snapshot:
    cells: tuple[int | None, ...]
    count: int
    k: int
    word_bits: int

    def __post_init__(self) -> None:
        if self.count < 0 or not 1 <= self.k <= len(self.cells) or self.word_bits < 1:
            raise ValueError("invalid public configuration")
        if any(value is not None and not 0 <= value < (1 << self.word_bits)
               for value in self.cells):
            raise ValueError("invalid payload word")


def insert(cells: list[int | None], positions: tuple[int, ...], target: int,
           random_words: tuple[int, ...], word_bits: int) -> bool:
    """Algorithm 4's share update; cryptographic position derivation is external.

    random_words supplies independent uniform words in the ideal experiment.
    Injection makes exhaustive testing possible without mocking randomness.
    No occupied word is overwritten. Full-support failure leaves cells intact.
    """
    if word_bits < 1 or not 0 <= target < 1 << word_bits:
        raise ValueError("invalid target width")
    if not positions or len(set(positions)) != len(positions):
        raise ValueError("positions must be nonempty and distinct")
    if any(not 0 <= index < len(cells) for index in positions):
        raise ValueError("position out of range")
    if any(value is not None and not 0 <= value < 1 << word_bits for value in cells):
        raise ValueError("invalid existing word")
    empty = [index for index in positions if cells[index] is None]
    if len(random_words) != max(0, len(empty) - 1):
        raise ValueError("wrong number of free words")
    if any(not 0 <= word < 1 << word_bits for word in random_words):
        raise ValueError("invalid free word")
    if not empty:
        return False
    pivot = empty[0]
    residual = target
    words = iter(random_words)
    for index in positions:
        if index == pivot:
            continue
        value = cells[index]
        if value is None:
            value = next(words)
            cells[index] = value
        residual ^= value
    cells[pivot] = residual
    return True


def recover_domain_xor(snapshot: Snapshot, domain_bits: int) -> int | None:
    """Public-only attack; abstain unless occupancy certifies disjoint supports."""
    if not 0 < domain_bits < snapshot.word_bits:
        raise ValueError("domain width must leave a nonempty prefix")
    occupied = 0
    aggregate = 0
    for word in snapshot.cells:
        if word is not None:
            occupied += 1
            aggregate ^= word
    if snapshot.count == 0 or occupied != snapshot.count * snapshot.k:
        return None
    return aggregate & ((1 << domain_bits) - 1)
