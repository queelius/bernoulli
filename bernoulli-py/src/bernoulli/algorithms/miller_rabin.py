"""Miller-Rabin primality witness check, framed as a Bernoulli<bool>.

A single round with a uniformly chosen base ``a in [2, n-2]`` produces a
:class:`bernoulli.atom.BernoulliBool` with:

- ``value = True`` if ``a`` does not witness compositeness of ``n``
  (i.e., ``n`` passes the witness test for ``a``).
- ``fpr = 1/4`` (worst-case bound: a true composite passes with probability
  at most 1/4 over uniformly chosen ``a``).
- ``fnr = 0`` (a true prime always passes).

A k-round protocol is the AND of k single-round Bernoullis. Because each
round is one-sided FPR, the AND collapses (in the framework) to
``fpr_combined = (1/4)^k``. This is the classical Miller-Rabin error bound,
re-derived as a special case of one-sided AND composition.

For most composites the per-round FPR is far smaller than 1/4. The empirical
distribution of per-composite FPR is interesting in its own right and is the
subject of one of the experiments under ``experiments/``.
"""

from __future__ import annotations

import random

from bernoulli.atom import BernoulliBool

WORST_CASE_PER_ROUND_FPR: float = 0.25


def _decompose(n_minus_1: int) -> tuple[int, int]:
    """Write ``n_minus_1 = d * 2^s`` with ``d`` odd."""
    s = 0
    d = n_minus_1
    while d & 1 == 0:
        d >>= 1
        s += 1
    return d, s


def witness_passes(n: int, a: int) -> bool:
    """Return True iff base ``a`` does NOT witness compositeness of ``n``.

    For ``n`` a true prime, this returns True for every valid ``a``. For
    ``n`` composite, this returns True with probability at most 1/4 over
    uniformly random ``a in [2, n-2]``.

    Special cases:

    - ``n < 2``: not prime, returns False.
    - ``n in {2, 3}``: prime, returns True.
    - ``n`` even and > 2: composite, returns False (every base witnesses).
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    if not 2 <= a <= n - 2:
        raise ValueError(f"base must satisfy 2 <= a <= n-2, got a={a}, n={n}")

    d, s = _decompose(n - 1)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return True
    return False


def witness_query(
    n: int, a: int | None = None, rng: random.Random | None = None
) -> BernoulliBool:
    """One round of Miller-Rabin as a one-sided ``BernoulliBool``.

    If ``a`` is None, a uniformly random base in ``[2, n-2]`` is chosen.

    Returns a ``BernoulliBool.one_sided_fpr`` with ``fpr = 1/4`` (worst case).
    """
    if n < 2:
        return BernoulliBool.one_sided_fpr(False, fpr=0.0)
    if n in (2, 3):
        return BernoulliBool.one_sided_fpr(True, fpr=0.0)
    if n % 2 == 0:
        return BernoulliBool.one_sided_fpr(False, fpr=0.0)

    if a is None:
        rng = rng or random.Random()
        a = rng.randrange(2, n - 1)
    passed = witness_passes(n, a)
    return BernoulliBool.one_sided_fpr(passed, fpr=WORST_CASE_PER_ROUND_FPR)


def is_probably_prime(
    n: int, rounds: int = 20, rng: random.Random | None = None
) -> BernoulliBool:
    """k-round Miller-Rabin as a one-sided ``BernoulliBool``.

    Returns ``BernoulliBool.one_sided_fpr(value, fpr=(1/4)^rounds)`` where
    ``value`` is True iff every round's witness check passed.
    """
    if rounds < 0:
        raise ValueError(f"rounds must be non-negative, got {rounds!r}")

    if n < 2:
        return BernoulliBool.one_sided_fpr(False, fpr=0.0)
    if n in (2, 3):
        return BernoulliBool.one_sided_fpr(True, fpr=0.0)
    if n % 2 == 0:
        return BernoulliBool.one_sided_fpr(False, fpr=0.0)

    rng = rng or random.Random()

    if rounds == 0:
        # No information: every odd n >= 5 "passes" trivially with no test.
        return BernoulliBool.one_sided_fpr(True, fpr=1.0)

    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
        if not witness_passes(n, a):
            # Even one failure proves compositeness.
            return BernoulliBool.one_sided_fpr(False, fpr=0.0)

    return BernoulliBool.one_sided_fpr(True, fpr=WORST_CASE_PER_ROUND_FPR ** rounds)
