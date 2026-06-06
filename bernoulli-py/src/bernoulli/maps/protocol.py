"""Protocols for perfect hash functions and approximate maps.

Both protocols mirror maph's C++ concepts directly:

- :class:`PerfectHashFunction` = maph's ``concepts/perfect_hash_function.hpp``.
- :class:`ApproximateMap` = maph's ``concepts/approximate_map.hpp``.

Phase 3 implementations will satisfy these protocols and add the
codec / retrieval / fingerprint layers.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class PerfectHashFunction(Protocol):
    """A perfect hash function from a key set into a slot range.

    For keys in the build set, ``slot_for(key)`` returns a unique slot in
    ``[0, range_size())``. For keys NOT in the build set, ``slot_for(key)``
    returns an arbitrary but valid index. No membership checking is performed
    at this layer.

    When ``range_size() == num_keys()``, the PHF is minimal (MPHF).
    """

    def slot_for(self, key: bytes) -> int: ...

    def num_keys(self) -> int: ...

    def range_size(self) -> int: ...

    def bits_per_key(self) -> float: ...

    def memory_bytes(self) -> int: ...


@runtime_checkable
class ApproximateMap(Protocol):
    """An approximate map: PHF plus membership verification.

    For keys in the build set, ``slot_for(key)`` returns the unique slot
    assigned by the underlying PHF. For keys not in the set, ``slot_for(key)``
    returns ``None`` (modulo a bounded false-positive rate).

    The standard composition is a perfect-hash filter: a PHF for slot
    assignment plus fingerprints (k-bit hashes) for membership verification.
    Space is ``c + log2(1 / epsilon)`` bits/key where ``c`` is the PHF cost.
    """

    def contains(self, key: bytes) -> bool: ...

    def slot_for(self, key: bytes) -> int | None: ...

    def num_keys(self) -> int: ...

    def range_size(self) -> int: ...
