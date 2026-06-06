"""Bloom-cascade: a tiered membership pipeline backed by an exact set.

A :class:`BloomCascade` is a sequence of independent Bloom filters in front
of an authoritative ``set[bytes]``. Each filter is built with a different
salt so the layers behave as statistically independent channels (the same
trick used in ``experiments/01_composition_validation.py`` Section A). A
query proceeds layer by layer: any False short-circuits to "definitely not
present"; only when every layer says True do we consult the exact set to
either confirm membership or recognize a cumulative false positive.

Why bother? Cascades pay off when the exact lookup is *expensive* (disk,
RPC, large in-memory hash with poor cache behavior). The first, smallest,
fastest filter rejects the bulk of negatives in a few cycles; later layers
soak up most of what slipped through; the exact set sees only the residual.
The "exact lookup needed" rate is the product of the per-layer FPRs (modulo
the independence assumption that the salt scheme buys us, validated in
experiment 01).

Three rates are interesting per query, all conditioned on the key being a
non-member:

- ``alpha_i``: per-layer FPR.
- ``alpha_filter = prod_i alpha_i``: probability all filters lie. This is
  what :meth:`probably_present` reports; it is the rate at which we *would*
  call into the exact set if the cascade were used as a stand-alone
  approximate set.
- The all-up FPR observed by :meth:`contains` is exactly zero, since the
  exact set has the final word. The cascade is **not** an approximate set
  in the sense of :class:`bernoulli.sets.MembershipOracle`; it is a *cost
  reducer* in front of an exact set.

The algebra is the standard AND chain (``bernoulli.algebra``):
``alpha_total = 1 - prod(1 - alpha_i)`` collapses to
``prod(alpha_i)`` for one-sided FPR Bernoulli<bool>'s with FPRs interpreted
as ``alpha_i``. (Note: this is a slight abuse, since the conventional AND
chain formula in ``algebra.py`` writes the failure rate as ``eta``; here
``alpha_i`` *is* the failure rate of layer ``i`` for a non-member input.)
"""

from __future__ import annotations

import math
from collections.abc import Iterable

from bernoulli.sets.bloom import BloomFilter

# Used to derive a per-layer salt from the layer index. Any non-zero
# constant works; the value just needs to give different bits per index.
_SALT_BASE = 0x9E3779B97F4A7C15  # golden-ratio constant, like splitmix64


def _layer_salt(index: int) -> int:
    """Return a deterministic 64-bit salt for cascade layer ``index``.

    XOR with a high-entropy constant so adjacent layers differ in many
    bits, mirroring the salt convention used in
    ``experiments/01_composition_validation.py``.
    """
    return (_SALT_BASE ^ (index * 0x100000001B3)) & 0xFFFFFFFFFFFFFFFF


class BloomCascade:
    """A tiered Bloom-filter cascade in front of an exact set.

    Parameters
    ----------
    layers : list[tuple[int, float]]
        Per-layer ``(capacity, target_fpr)`` pairs. The list order is the
        query order: the first layer is the cheap front gate; later layers
        refine. Each tuple becomes a :class:`BloomFilter` with an
        independent salt derived from its index.

    Examples
    --------
    >>> cascade = BloomCascade([(100, 0.1), (100, 0.05)])
    >>> cascade.add(b"x")
    >>> cascade.contains(b"x")
    True
    >>> cascade.contains(b"definitely-not-present-zzz")
    False
    """

    def __init__(self, layers: list[tuple[int, float]]) -> None:
        if not layers:
            raise ValueError("cascade must have at least one layer")
        self._filters: list[BloomFilter] = []
        for i, (capacity, target_fpr) in enumerate(layers):
            self._filters.append(
                BloomFilter(
                    capacity=capacity,
                    target_fpr=target_fpr,
                    salt=_layer_salt(i),
                )
            )
        self._exact: set[bytes] = set()

    # ------------------------------------------------------------------ build
    def add(self, key: bytes) -> None:
        """Insert ``key`` into every filter and the authoritative exact set."""
        for bf in self._filters:
            bf.add(key)
        self._exact.add(key)

    def add_all(self, keys: Iterable[bytes]) -> None:
        """Bulk insert."""
        for k in keys:
            self.add(k)

    # ------------------------------------------------------------------ query
    def probably_present(self, key: bytes) -> bool:
        """True iff every filter layer reports True.

        This is the "must consult exact set" event. For a non-member key
        the rate of this returning True is approximately the product of
        per-layer FPRs (validated by experiment 03).
        """
        return all(bf.contains(key) for bf in self._filters)

    def contains(self, key: bytes) -> bool:
        """Authoritative membership: filters first, exact set last.

        Zero false positives, zero false negatives. The cascade cost is the
        sum of one filter probe per layer (until a False) plus, on
        all-pass, one exact-set lookup.
        """
        if not self.probably_present(key):
            return False
        return key in self._exact

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError(f"key must be bytes-like, got {type(key).__name__}")
        return self.contains(bytes(key))

    # ------------------------------------------------------------- diagnostics
    @property
    def num_layers(self) -> int:
        return len(self._filters)

    @property
    def filters(self) -> tuple[BloomFilter, ...]:
        """Read-only view of the underlying filters."""
        return tuple(self._filters)

    def num_keys(self) -> int:
        return len(self._exact)

    def memory_bytes(self) -> int:
        """Memory of the *filters only*; the exact set is not amortizable."""
        return sum(bf.memory_bytes() for bf in self._filters)

    def bits_per_key(self) -> float:
        """Filter bits per stored key. Excludes the exact set on purpose.

        The cascade's value proposition is space against the exact set's
        access cost, not space against the exact set's memory; reporting
        only filter bits keeps the comparison apples-to-apples with a
        single Bloom filter of the same total bit budget.
        """
        n = len(self._exact)
        if n == 0:
            return float("inf") if self.memory_bytes() > 0 else 0.0
        return (self.memory_bytes() * 8) / n

    def predicted_filter_fpr(self) -> float:
        """Closed-form rate at which ``probably_present`` lies on non-members.

        The product of each layer's asymptotic FPR at current load. This is
        the "exact-lookup needed" rate predicted by the algebra.
        """
        product = 1.0
        for bf in self._filters:
            product *= bf.fpr()
        return product

    def predicted_filter_fpr_total_error(self) -> float:
        """Same idea expressed via the composition theorem.

        ``1 - prod(1 - alpha_i)`` interprets ``alpha_i`` as a per-layer
        failure probability where "failure" means the filter rejects.
        For non-members the AND of layers fires only when *every* layer
        produces a false positive, so the relevant quantity is
        ``prod alpha_i``, computed by :meth:`predicted_filter_fpr`. This
        method exists for symmetry with the algebra module's exposed API.
        """
        # By construction, this is the dual: probability that the chain
        # rejects = 1 - prod(alpha_i). We return the complement so the
        # name is self-consistent with "filter false-positive rate".
        return 1.0 - math.prod(1.0 - bf.fpr() for bf in self._filters)

    def __len__(self) -> int:
        return self.num_keys()

    def __repr__(self) -> str:
        spec = ", ".join(
            f"({bf._capacity}, fpr={bf._target_fpr:g})" for bf in self._filters
        )
        return f"BloomCascade(layers=[{spec}], n={self.num_keys()})"
