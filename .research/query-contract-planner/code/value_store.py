"""Packed exact values and a specified finite shared linear fingerprint family."""
from dataclasses import dataclass
from enum import IntEnum
import random
import struct


class ValueMode(IntEnum):
    EXACT = 0
    LINEAR = 1


HEADER = struct.Struct('>8sIHHB')
MAGIC = b'QCVALUE1'


def pack_values(values, width):
    if width < 1 or any(not 0 <= v < 2**width for v in values):
        raise ValueError('invalid packed value')
    output = bytearray((len(values) * width + 7) // 8)
    for index, value in enumerate(values):
        start = index * width
        for bit in range(width):
            if value >> bit & 1:
                output[(start + bit) // 8] |= 1 << ((start + bit) % 8)
    return bytes(output)


def read_value(payload, index, width):
    start = index * width
    begin, end = start // 8, (start + width + 7) // 8
    return (int.from_bytes(payload[begin:end], 'little') >> (start % 8)) & ((1 << width) - 1)


@dataclass(frozen=True, slots=True)
class FrozenValues:
    count: int
    input_width: int
    width: int
    mode: ValueMode
    masks: tuple[int, ...]
    payload: bytes

    @classmethod
    def build(cls, values, domain_size, mode, width, seed):
        if domain_size < 1 or any(not 0 <= value < domain_size for value in values):
            raise ValueError('value outside declared domain')
        input_width = max(1, (domain_size - 1).bit_length())
        if mode is ValueMode.EXACT:
            return cls(len(values), input_width, input_width, mode, (), pack_values(values, input_width))
        if mode is not ValueMode.LINEAR or width < 1 or width > 64:
            raise ValueError('invalid fingerprint width or mode')
        rng = random.Random(seed)
        return cls.from_masks(values, domain_size, tuple(rng.getrandbits(input_width) for _ in range(width)))

    @classmethod
    def from_masks(cls, values, domain_size, masks):
        input_width = max(1, (domain_size - 1).bit_length())
        if domain_size < 1 or not masks or len(masks) > 64 or any(not 0 <= m < 2**input_width for m in masks):
            raise ValueError('invalid finite hash matrix')
        if any(not 0 <= value < domain_size for value in values):
            raise ValueError('value outside declared domain')
        fingerprints = [sum(((value & mask).bit_count() % 2) << bit for bit, mask in enumerate(masks)) for value in values]
        return cls(len(values), input_width, len(masks), ValueMode.LINEAR, tuple(masks), pack_values(fingerprints, len(masks)))

    def value(self, index):
        if not 0 <= index < self.count:
            raise IndexError(index)
        return read_value(self.payload, index, self.width)

    def equal(self, left, right):
        return self.value(left) == self.value(right)

    def serialize(self):
        seed_width = (self.input_width + 7) // 8
        seed = b''.join(mask.to_bytes(seed_width, 'big') for mask in self.masks)
        return HEADER.pack(MAGIC, self.count, self.input_width, self.width, self.mode) + seed + self.payload

    @classmethod
    def deserialize(cls, data):
        if len(data) < HEADER.size:
            raise ValueError('truncated value header')
        magic, count, input_width, width, mode = HEADER.unpack_from(data)
        if magic != MAGIC or input_width < 1 or not 1 <= width <= 64:
            raise ValueError('invalid value header')
        mode = ValueMode(mode)
        if mode is ValueMode.EXACT and width != input_width:
            raise ValueError('inconsistent exact value width')
        seed_width = (input_width + 7) // 8
        seed_length = width * seed_width if mode is ValueMode.LINEAR else 0
        if len(data) != HEADER.size + seed_length + (count * width + 7) // 8:
            raise ValueError('value payload length mismatch')
        masks = tuple(int.from_bytes(data[pos:pos + seed_width], 'big') for pos in range(HEADER.size, HEADER.size + seed_length, seed_width))
        if any(mask >= 2**input_width for mask in masks):
            raise ValueError('matrix exceeds input width')
        return cls(count, input_width, width, mode, masks, data[HEADER.size + seed_length:])

    @property
    def payload_bytes(self):
        return len(self.serialize())
