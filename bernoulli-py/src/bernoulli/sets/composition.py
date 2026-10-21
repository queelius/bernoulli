"""Rate propagation for Boolean combinations of approximate sets.

This is the executable form of book chapter 6 (Composition of Sets). When two
approximate sets ``A`` and ``B`` with error profiles ``(fpr, fnr)`` are combined
under union, intersection, complement, or difference, the combined set is again
an approximate set, and its rates follow from the rates of the operands plus the
*geometry of the query population*.

The geometry matters because most of these rates are not a single product. The
universe splits into four cells relative to ``A`` and ``B``::

    both    = A and B          (members of A and of B)
    a_only  = A minus B
    b_only  = B minus A
    neither = complement(A or B)

and a combined rate is a mass-weighted average over the cells where an error can
arise. Two of the four rates collapse to a single cell and are exact products:

- ``union`` FPR: a non-member of ``A or B`` is in ``neither``, so a union false
  positive needs ``A`` or ``B`` to fire wrongly: ``1 - (1 - fpr_A)(1 - fpr_B)``.
- ``intersection`` FNR: a member of ``A and B`` is in ``both``, so an
  intersection miss needs ``A`` or ``B`` to miss: ``1 - (1 - fnr_A)(1 - fnr_B)``.

The other two are genuine three-region weighted sums (book section 6.2):

- ``intersection`` FPR over the non-members of ``A and B`` (the cells
  ``a_only``, ``b_only``, ``neither``)::

      fpr = w1 (1 - fnr_A) fpr_B + w2 fpr_A (1 - fnr_B) + w3 fpr_A fpr_B

  The bare product ``fpr_A fpr_B`` is only the ``w3 -> 1`` *sparse limit*, where
  queries land almost entirely outside ``A or B``. A query known to be in ``A``
  but tested against ``B`` (the ``a_only`` cell) is a false positive at rate
  ``fpr_B`` alone, not ``fpr_A fpr_B``.
- ``union`` FNR over the members of ``A or B`` (the cells ``a_only``,
  ``b_only``, ``both``)::

      fnr = w1 fnr_A (1 - fpr_B) + w2 fnr_B (1 - fpr_A) + w3 fnr_A fnr_B

``complement`` swaps the two axes; ``difference`` is ``A and complement(B)``.

Nesting operations
------------------
Each function is exact for **one** operation, given the partition and
independent operand errors. Its result is a mass-weighted average over cells,
so using it as an operand of a further operation is exact only when the inner
partition describes the queries the outer operation conditions on. A point-mass
partition (one known latent cell per level) is exact; the ``Partition.sparse()``
default and other mixtures discard the information the next level needs. A set
that appears twice in an expression, as in ``(A and B) or (A and C)``, also
breaks the independence of operand errors. For ``(A and B) or C`` with every
operand at ``(0.02, 0.10)`` and a query in ``B`` only, point-mass partitions
give the exact 0.03764 while sparse partitions give 0.020392.
:mod:`bernoulli.formula` evaluates such expressions exactly at any latent word
and gives sound worst-case rates.
"""

from __future__ import annotations

from dataclasses import dataclass

_TOL = 1e-9


def _clamp01(x: float) -> float:
    """Clamp a rate to [0, 1].

    The composed rates are convex combinations of values in [0, 1] and so are
    mathematically in range, but floating-point rounding can overshoot by a few
    ulps (e.g. weights that sum to 1.0000000002). Clamping keeps the result a
    valid :class:`SetRates` without masking any real out-of-range value.
    """
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


@dataclass(frozen=True, slots=True)
class SetRates:
    """The error profile ``(fpr, fnr)`` of an approximate set.

    Unlike :class:`bernoulli.atom.BernoulliBool` this carries no query value; it
    is the set's rate pair, the object that composition propagates.

    Examples
    --------
    >>> SetRates(fpr=0.01, fnr=0.0).rates
    (0.01, 0.0)
    """

    fpr: float = 0.0
    fnr: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.fpr <= 1.0:
            raise ValueError(f"fpr must be in [0, 1], got {self.fpr!r}")
        if not 0.0 <= self.fnr <= 1.0:
            raise ValueError(f"fnr must be in [0, 1], got {self.fnr!r}")

    @property
    def rates(self) -> tuple[float, float]:
        """``(fpr, fnr)`` as a pair."""
        return (self.fpr, self.fnr)

    @classmethod
    def one_sided_fpr(cls, fpr: float) -> SetRates:
        """An ``fnr == 0`` set (the Bloom-style contract)."""
        return cls(fpr=fpr, fnr=0.0)

    @classmethod
    def one_sided_fnr(cls, fnr: float) -> SetRates:
        """An ``fpr == 0`` set (the perfect-filter / coRP contract)."""
        return cls(fpr=0.0, fnr=fnr)


@dataclass(frozen=True, slots=True)
class Partition:
    """Masses of the four cells of the universe relative to two sets ``A``, ``B``.

    The four masses are normalized to sum to 1 and are read as the probability
    that a query drawn from the working population lands in each cell.

    Attributes
    ----------
    both : float
        Mass of ``A and B``.
    a_only : float
        Mass of ``A minus B``.
    b_only : float
        Mass of ``B minus A``.
    neither : float
        Mass of ``complement(A or B)``.
    """

    both: float
    a_only: float
    b_only: float
    neither: float

    def __post_init__(self) -> None:
        for name in ("both", "a_only", "b_only", "neither"):
            v = getattr(self, name)
            if not 0.0 <= v <= 1.0:
                raise ValueError(f"{name} must be in [0, 1], got {v!r}")
        total = self.both + self.a_only + self.b_only + self.neither
        if abs(total - 1.0) > _TOL:
            raise ValueError(f"cell masses must sum to 1, got {total!r}")

    @classmethod
    def from_masses(
        cls, both: float, a_only: float, b_only: float, neither: float
    ) -> Partition:
        """Build a partition from non-negative cell masses, normalizing the sum."""
        for name, v in (
            ("both", both),
            ("a_only", a_only),
            ("b_only", b_only),
            ("neither", neither),
        ):
            if v < 0.0:
                raise ValueError(f"{name} must be non-negative, got {v!r}")
        total = both + a_only + b_only + neither
        if total <= 0.0:
            raise ValueError("at least one cell mass must be positive")
        return cls(
            both=both / total,
            a_only=a_only / total,
            b_only=b_only / total,
            neither=neither / total,
        )

    @classmethod
    def from_counts(
        cls, n_both: int, n_a_only: int, n_b_only: int, n_neither: int
    ) -> Partition:
        """Build a partition from integer cell counts (e.g. measured set sizes)."""
        return cls.from_masses(
            float(n_both), float(n_a_only), float(n_b_only), float(n_neither)
        )

    @classmethod
    def sparse(cls) -> Partition:
        """The both-negative limit: every query is outside ``A or B``.

        This is the regime in which the intersection FPR collapses to the bare
        product ``fpr_A * fpr_B`` and the union FNR to ``fnr_A * fnr_B``. It is
        the best case for conjunctive precision, and the wrong default when
        queries commonly hit one set but not the other.
        """
        return cls(both=0.0, a_only=0.0, b_only=0.0, neither=1.0)

    @classmethod
    def disjoint(cls, mass_a: float, mass_b: float) -> Partition:
        """Two disjoint sets covering masses ``mass_a`` and ``mass_b`` of the universe."""
        return cls.from_masses(0.0, mass_a, mass_b, 1.0 - mass_a - mass_b)


def complement(a: SetRates) -> SetRates:
    """The complement set ``complement(A)``: swap the error axes (book prop. 6.x).

    A non-member of ``complement(A)`` is a member of ``A``, so the complement's
    false-positive rate is ``A``'s false-negative rate, and vice versa. The
    operation is involutive.

    Examples
    --------
    >>> complement(SetRates(fpr=0.01, fnr=0.0)).rates
    (0.0, 0.01)
    """
    return SetRates(fpr=a.fnr, fnr=a.fpr)


def union(a: SetRates, b: SetRates, partition: Partition) -> SetRates:
    """Rates of ``A or B``.

    The FPR is the single-region exact product form; the FNR is the three-region
    weighted sum over the members of ``A or B``.

    Examples
    --------
    >>> a = b = SetRates.one_sided_fpr(0.01)
    >>> u = union(a, b, Partition.sparse())
    >>> round(u.fpr, 6), u.fnr
    (0.0199, 0.0)
    """
    fpr = 1.0 - (1.0 - a.fpr) * (1.0 - b.fpr)

    members = partition.a_only + partition.b_only + partition.both
    if members <= 0.0:
        fnr = 0.0
    else:
        w1 = partition.a_only / members
        w2 = partition.b_only / members
        w3 = partition.both / members
        fnr = (
            w1 * a.fnr * (1.0 - b.fpr)
            + w2 * b.fnr * (1.0 - a.fpr)
            + w3 * a.fnr * b.fnr
        )
    return SetRates(fpr=_clamp01(fpr), fnr=_clamp01(fnr))


def intersection(a: SetRates, b: SetRates, partition: Partition) -> SetRates:
    """Rates of ``A and B``.

    The FNR is the single-region exact product form; the FPR is the three-region
    weighted sum over the non-members of ``A and B`` (book section 6.2). The bare
    product ``fpr_A * fpr_B`` is only the sparse limit.

    Examples
    --------
    >>> a = b = SetRates.one_sided_fpr(0.01)
    >>> # Sparse limit: the optimistic conjunctive precision, fpr_A * fpr_B.
    >>> round(intersection(a, b, Partition.sparse()).fpr, 6)
    0.0001
    >>> # Query known to be in A, tested against B: rate is fpr_B alone.
    >>> p = Partition(both=0.0, a_only=1.0, b_only=0.0, neither=0.0)
    >>> round(intersection(a, b, p).fpr, 6)
    0.01
    """
    fnr = 1.0 - (1.0 - a.fnr) * (1.0 - b.fnr)

    nonmembers = partition.a_only + partition.b_only + partition.neither
    if nonmembers <= 0.0:
        fpr = 0.0
    else:
        w1 = partition.a_only / nonmembers
        w2 = partition.b_only / nonmembers
        w3 = partition.neither / nonmembers
        fpr = (
            w1 * (1.0 - a.fnr) * b.fpr
            + w2 * a.fpr * (1.0 - b.fnr)
            + w3 * a.fpr * b.fpr
        )
    return SetRates(fpr=_clamp01(fpr), fnr=_clamp01(fnr))


def difference(a: SetRates, b: SetRates, partition: Partition) -> SetRates:
    """Rates of ``A minus B`` (``A and complement(B)``).

    Implemented as the intersection of ``A`` with ``complement(B)``, with the
    partition cells relabeled for ``complement(B)``: an element of ``A minus B``
    is in ``A`` and in ``complement(B)``, so ``a_only`` becomes the ``both`` cell
    of ``(A, complement(B))``, ``both`` becomes ``a_only``, ``neither`` becomes
    ``b_only``, and ``b_only`` becomes ``neither``.

    A consequence worth noting (book section 6.2): the difference of two FNR-zero
    sets is two-sided, because ``complement(B)`` carries ``B``'s false-positive
    rate as a false-negative rate.

    Examples
    --------
    >>> a = b = SetRates.one_sided_fpr(0.01)            # both FNR-zero
    >>> d = difference(a, b, Partition.from_masses(1, 1, 1, 1))
    >>> d.fnr > 0.0                                     # two-sided result
    True
    """
    relabeled = Partition(
        both=partition.a_only,
        a_only=partition.both,
        b_only=partition.neither,
        neither=partition.b_only,
    )
    return intersection(a, complement(b), relabeled)
