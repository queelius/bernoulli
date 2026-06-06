"""Composition algebra for Bernoulli rate chains.

The composition theorem states that for ``k`` independent identity-with-error
stages, each failing with rate ``eta_i``, the total failure rate is::

    eta_total = 1 - prod(1 - eta_i for i in range(k))

This single formula governs:

- AND chains of one-sided FPR Bernoulli<bool>'s: each round suppresses the
  FPR multiplicatively. Miller-Rabin's ``(1/4)^k`` bound is the ``k``-fold
  composition with ``eta = 1/4``.
- OR chains: dual, suppresses FNR.
- Bloom filter k-hash false-positive analysis: positions are independent
  bits, each "false positive" with rate ``p``, all must fire for the test
  to wrongly succeed (this is the AND form, with the caveat about hash
  independence assumptions).
- Many-witness sketches: each witness is one stage in the chain.

The functions below operate on rate sequences, returning the chained rate.
For atomic-level composition, see :class:`bernoulli.atom.BernoulliBool`.
"""

from __future__ import annotations

import math
from collections.abc import Iterable


def composition_total_error(rates: Iterable[float]) -> float:
    """Composition theorem: ``eta_total = 1 - prod(1 - eta_i)``.

    Each ``eta_i`` is the failure rate of one independent identity-with-error
    stage. The output is the failure rate of the chain.

    Raises ``ValueError`` for any rate outside ``[0, 1]``.
    """
    prod = 1.0
    for eta in rates:
        if not 0.0 <= eta <= 1.0:
            raise ValueError(f"rate must be in [0, 1], got {eta!r}")
        prod *= 1.0 - eta
    return 1.0 - prod


def composition_homogeneous(rate: float, k: int) -> float:
    """Composition of ``k`` identical stages, each with failure rate ``rate``.

    Equivalent to ``composition_total_error([rate] * k)`` but in closed form::

        eta_total = 1 - (1 - rate)^k
    """
    if not 0.0 <= rate <= 1.0:
        raise ValueError(f"rate must be in [0, 1], got {rate!r}")
    if k < 0:
        raise ValueError(f"k must be non-negative, got {k!r}")
    return 1.0 - (1.0 - rate) ** k


def k_for_and_chain_target(per_round_rate: float, target_rate: float) -> int:
    """Smallest ``k`` such that an AND chain of ``k`` rounds has rate at most ``target_rate``.

    The AND chain of one-sided Bernoulli<bool>'s (e.g., Miller-Rabin witness
    rounds) has chained rate ``r^k``. We solve::

        r^k <= target  ==>  k >= log(target) / log(r)

    Returns ``ceil(log(target) / log(per_round_rate))``.

    Examples
    --------
    >>> k_for_and_chain_target(per_round_rate=0.25, target_rate=1e-12)
    20
    """
    if not 0.0 <= per_round_rate < 1.0:
        raise ValueError(f"per_round_rate must be in [0, 1), got {per_round_rate!r}")
    if not 0.0 < target_rate <= 1.0:
        raise ValueError(f"target_rate must be in (0, 1], got {target_rate!r}")
    if per_round_rate == 0.0 or target_rate >= 1.0:
        return 0
    k_real = math.log(target_rate) / math.log(per_round_rate)
    return max(0, math.ceil(k_real))


def max_k_for_or_chain_budget(per_stage_rate: float, error_budget: float) -> int:
    """Largest ``k`` such that an OR chain of ``k`` stages stays within ``error_budget``.

    The OR chain (independent failure points) has chained rate
    ``1 - (1 - r)^k`` (the composition theorem). We solve::

        1 - (1 - r)^k <= budget  ==>  k <= log(1 - budget) / log(1 - r)

    Returns the largest non-negative integer ``k`` satisfying the bound.

    Examples
    --------
    >>> max_k_for_or_chain_budget(per_stage_rate=0.001, error_budget=0.01)
    10
    """
    unbounded = 1 << 30  # sentinel returned when no stage ever fails
    if not 0.0 <= per_stage_rate < 1.0:
        raise ValueError(f"per_stage_rate must be in [0, 1), got {per_stage_rate!r}")
    if not 0.0 <= error_budget <= 1.0:
        raise ValueError(f"error_budget must be in [0, 1], got {error_budget!r}")
    if per_stage_rate == 0.0 or error_budget >= 1.0:
        return unbounded
    if error_budget == 0.0:
        return 0
    k_real = math.log(1.0 - error_budget) / math.log(1.0 - per_stage_rate)
    return max(0, math.floor(k_real))


def miller_rabin_error(k: int, single_witness_fpr: float = 0.25) -> float:
    """Miller-Rabin: composite-witness FPR after ``k`` AND'd rounds.

    Each round of Miller-Rabin's witness check is a one-sided Bernoulli<bool>
    with ``fnr = 0`` (true primes always pass) and ``fpr <= 1/4`` (a true
    composite passes with probability at most 1/4 over a uniformly chosen
    witness). The protocol AND's ``k`` rounds together, suppressing FPR
    multiplicatively to ``(1/4)^k``.

    The ``1/4`` bound is the classical worst-case for strong-pseudoprime
    witnesses. For most composites the per-round FPR is far smaller.
    """
    if k < 0:
        raise ValueError(f"k must be non-negative, got {k!r}")
    if not 0.0 <= single_witness_fpr <= 1.0:
        raise ValueError(
            f"single_witness_fpr must be in [0, 1], got {single_witness_fpr!r}"
        )
    return single_witness_fpr ** k


def bloom_filter_fpr(num_keys: int, num_bits: int, num_hashes: int) -> float:
    """The classical Bloom-filter FPR formula.

    ``alpha = (1 - exp(-k * n / m))^k``

    where ``n = num_keys``, ``m = num_bits``, ``k = num_hashes``. This is
    the asymptotic formula assuming hash-bit independence. It is a special
    case of an AND-chain: each of the ``k`` hash positions must be 1 for
    the membership test to (incorrectly) report present.

    Returns 0 for ``num_keys == 0`` and 1 for ``num_bits == 0`` (degenerate).
    """
    if num_keys < 0 or num_bits < 0 or num_hashes < 0:
        raise ValueError("counts must be non-negative")
    if num_bits == 0:
        return 1.0
    if num_keys == 0 or num_hashes == 0:
        return 0.0
    p_bit_set = 1.0 - math.exp(-num_hashes * num_keys / num_bits)
    return p_bit_set ** num_hashes


def bloom_filter_optimal_k(num_keys: int, num_bits: int) -> float:
    """The number of hash functions that minimizes Bloom FPR.

    ``k_opt = (m / n) * ln(2)``

    Returns the real-valued optimum; round to nearest integer for use.
    """
    if num_keys <= 0 or num_bits <= 0:
        raise ValueError("counts must be positive")
    return (num_bits / num_keys) * math.log(2.0)


def bits_per_key_for_fpr(target_fpr: float) -> float:
    """The information-theoretic lower bound on bits per key for a target FPR.

    For an approximate set with false-positive rate ``alpha`` and zero
    false-negative rate, the entropy lower bound is ``-log2(alpha)`` bits
    per key (this is the ``bernoulli_entropy`` paper's content).

    Bloom filters reach ``log2(e) * -log2(alpha) approx 1.44 * -log2(alpha)``
    bits per key, which is a constant factor above the lower bound. The
    bernoulli-hash-function paper gives a construction reaching the bound.

    Raises ``ValueError`` if ``target_fpr`` not in ``(0, 1]``.
    """
    if not 0.0 < target_fpr <= 1.0:
        raise ValueError(f"target_fpr must be in (0, 1], got {target_fpr!r}")
    return -math.log2(target_fpr)


def bloom_bits_per_key_for_fpr(target_fpr: float) -> float:
    """Bloom filter bits per key to reach ``target_fpr`` (asymptotic, optimal k).

    ``bpk_bloom = -log2(alpha) / ln(2) = -log2(alpha) * log2(e) approx 1.44 * -log2(alpha)``
    """
    if not 0.0 < target_fpr <= 1.0:
        raise ValueError(f"target_fpr must be in (0, 1], got {target_fpr!r}")
    return -math.log2(target_fpr) / math.log(2.0)
