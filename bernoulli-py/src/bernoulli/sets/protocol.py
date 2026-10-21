"""Protocol for approximate-set membership oracles.

Mirrors maph's ``concepts/membership_oracle.hpp``. A type satisfying this
protocol answers ``contains(x)`` with bounded false-positive rate (and, by
convention, zero false-negative rate, which is the standard "Bloom-style"
contract).

Implementations include :class:`bernoulli.sets.BloomFilter` and
:class:`bernoulli.maps.PerfectFilter`.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class MembershipOracle(Protocol):
    """An approximate set: ``contains(x)`` with bounded FPR and zero FNR.

    Required methods:

    - ``contains(x: bytes) -> bool``: membership test.
    - ``bits_per_key() -> float``: amortized space cost.
    - ``memory_bytes() -> int``: total memory in bytes.
    - ``num_keys() -> int``: build-set cardinality.
    - ``fpr() -> float``: configured or empirical false-positive rate.

    Implementations should preserve the contract: for ``x`` in the build set,
    ``contains(x)`` always returns True (zero FNR). For ``x`` not in the
    build set, ``contains(x)`` returns True with probability at most
    ``fpr()``.
    """

    def contains(self, x: bytes) -> bool: ...

    def bits_per_key(self) -> float: ...

    def memory_bytes(self) -> int: ...

    def num_keys(self) -> int: ...

    def fpr(self) -> float: ...
