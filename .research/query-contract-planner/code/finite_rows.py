"""Finite four-wise polynomial fingerprints, stored once per functional row.

The theorem is over four UNIFORM independent field coefficients. Reproducible
experiments use Python's seeded PRNG; no cryptographic or adaptive claim follows.
Only unconditional fixed-query bounds are asserted. Conditioning on all stored
fingerprints can destroy the four-wise law.
"""
from dataclasses import dataclass
from fractions import Fraction
import random
import struct

from contracts import Budget, error_bound
from value_store import pack_values, read_value

PRIME = 2**61 - 1
HEADER = struct.Struct('>8sIIBQ4Q')
MAGIC = b'QCROWS01'


def collision_rate(width, prime=PRIME):
    if not 1 <= width <= 60 or prime not in (7, PRIME):
        raise ValueError('unsupported width or verified prime')
    bins = 2**width
    low, high_count = divmod(prime, bins)
    return Fraction(high_count * (low + 1)**2 + (bins - high_count) * low**2, prime**2)


def select_width(k, target, budget):
    if budget not in (Budget.ORDINARY_UNION, Budget.CONSTRAINED_UNION):
        raise ValueError('finite four-wise family does not license product contracts')
    if k < 1 or not 0 < target < 1:
        raise ValueError('invalid planning input')
    for width in range(1, 61):
        if error_bound(budget, k, collision_rate(width)) <= target:
            return width
    raise ValueError('target below supported finite-family resolution')


@dataclass(frozen=True, slots=True)
class FrozenRows:
    count: int
    domain_size: int
    width: int
    prime: int
    coefficients: tuple[int, int, int, int]
    payload: bytes

    @classmethod
    def build(cls, values, domain_size, width, seed):
        rng = random.Random(seed)
        coefficients = tuple(rng.randrange(PRIME) for _ in range(4))
        return cls.from_coefficients(values, domain_size, width, coefficients)

    @classmethod
    def from_coefficients(cls, values, domain_size, width, coefficients, prime=PRIME):
        collision_rate(width, prime)
        if domain_size < 1 or len(values) * domain_size > prime:
            raise ValueError('tuple encoding is not injective in field')
        if len(coefficients) != 4 or any(not 0 <= c < prime for c in coefficients):
            raise ValueError('four field coefficients required')
        if any(not 0 <= value < domain_size for value in values):
            raise ValueError('value outside declared domain')
        empty = cls(len(values), domain_size, width, prime, tuple(coefficients), b'')
        fingerprints = [empty.fingerprint(row, value) for row, value in enumerate(values)]
        return cls(len(values), domain_size, width, prime, tuple(coefficients), pack_values(fingerprints, width))

    def fingerprint(self, row, value):
        if not 0 <= row < self.count or not 0 <= value < self.domain_size:
            raise ValueError('row or value outside declared domain')
        x = row * self.domain_size + value
        result = 0
        for coefficient in reversed(self.coefficients):
            result = (result * x + coefficient) % self.prime
        return result % (1 << self.width)

    def contains(self, row, value):
        return self.fingerprint(row, value) == read_value(self.payload, row, self.width)

    def serialize(self):
        return HEADER.pack(MAGIC, self.count, self.domain_size, self.width, self.prime, *self.coefficients) + self.payload

    @classmethod
    def deserialize(cls, data):
        if len(data) < HEADER.size:
            raise ValueError('truncated row header')
        magic, count, domain_size, width, prime, *coefficients = HEADER.unpack_from(data)
        collision_rate(width, prime)
        if magic != MAGIC or domain_size < 1 or count * domain_size > prime:
            raise ValueError('invalid row header or field encoding')
        if any(c >= prime for c in coefficients) or len(data) != HEADER.size + (count * width + 7) // 8:
            raise ValueError('invalid row payload')
        return cls(count, domain_size, width, prime, tuple(coefficients), data[HEADER.size:])

    @property
    def payload_bytes(self):
        return len(self.serialize())
