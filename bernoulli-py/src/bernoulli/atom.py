"""The atomic Bernoulli type: a noisy Boolean with channel rates ``(fpr, fnr)``.

The class :class:`BernoulliBool` represents a single observation drawn through
a binary channel parameterized by:

- ``fpr`` (alpha): false-positive rate, ``P(observe true | true value false)``
- ``fnr`` (beta):  false-negative rate, ``P(observe false | true value true)``

The framework treats ``BernoulliBool`` as a single algebraic type closed under
AND, OR, and NOT, with closed-form rate composition derived in book chapter 3.

Two flavors of binary composition are exposed:

1. ``__and__`` / ``__or__``: distribution-free formulas for one rate, with the
   conservative ``min`` bound for the other. Cheap; never wrong; not always
   tight.
2. ``and_with_prior`` / ``or_with_prior``: the closed-form prior-dependent
   formulas. Tight when the prior is known.

Two structurally important specializations:

- ``one_sided_fpr(value, fpr)``: a Bernoulli with ``fnr == 0``. The Bloom
  filter family, Miller-Rabin's witness AND, and any "membership-checked then
  ..." structure live here. There is no false negative; the structure is
  conservative on the positive side.
- ``one_sided_fnr(value, fnr)``: dual; ``fpr == 0``. Las Vegas algorithms and
  any "answer is always correct, but might fail to answer" structure.

Both one-sided forms compose cleanly: AND of two ``one_sided_fpr`` instances
is again ``one_sided_fpr`` with ``fpr_combined`` independent of any input
prior, which is why Miller-Rabin's ``alpha^k`` bound holds in closed form.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class BernoulliBool:
    """A random approximate Boolean: observed value plus channel rates.

    Attributes
    ----------
    value : bool
        The observed (potentially noisy) Boolean.
    fpr : float
        False-positive rate alpha in [0, 1]: ``P(observe True | truth False)``.
        Defaults to 0 (no false positives).
    fnr : float
        False-negative rate beta in [0, 1]: ``P(observe False | truth True)``.
        Defaults to 0 (no false negatives).

    Examples
    --------
    >>> b = BernoulliBool(value=True, fpr=0.1, fnr=0.05)
    >>> b.value
    True
    >>> b.rates
    (0.1, 0.05)
    >>> nb = ~b
    >>> nb.value, nb.rates
    (False, (0.05, 0.1))
    """

    value: bool
    fpr: float = 0.0
    fnr: float = 0.0

    EPS: ClassVar[float] = 1e-12

    def __post_init__(self) -> None:
        if not 0.0 <= self.fpr <= 1.0:
            raise ValueError(f"fpr must be in [0, 1], got {self.fpr!r}")
        if not 0.0 <= self.fnr <= 1.0:
            raise ValueError(f"fnr must be in [0, 1], got {self.fnr!r}")

    @property
    def rates(self) -> tuple[float, float]:
        """``(fpr, fnr)`` as a pair."""
        return (self.fpr, self.fnr)

    @property
    def is_certain(self) -> bool:
        """True iff both rates are (numerically) zero."""
        return self.fpr <= self.EPS and self.fnr <= self.EPS

    @property
    def is_one_sided_fpr(self) -> bool:
        """True iff ``fnr == 0`` (conservative on positive answers).

        Bloom filters, Miller-Rabin witness AND chains, and any
        ``check then ...`` structure satisfy this. Composition under AND
        preserves it.
        """
        return self.fnr <= self.EPS

    @property
    def is_one_sided_fnr(self) -> bool:
        """True iff ``fpr == 0`` (conservative on negative answers).

        Las Vegas algorithms ("answer is always correct, but may fail to
        answer") satisfy this. Composition under OR preserves it.
        """
        return self.fpr <= self.EPS

    def __invert__(self) -> BernoulliBool:
        """NOT: swaps ``fpr`` and ``fnr`` (book section 3.2).

        ``not`` is involutive on the rate pair: applying it twice restores
        the original channel matrix.
        """
        return BernoulliBool(value=not self.value, fpr=self.fnr, fnr=self.fpr)

    def __and__(self, other: BernoulliBool) -> BernoulliBool:
        """AND under the **shared-truth** interpretation.

        Both inputs are interpreted as independent noisy observations of the
        *same* underlying truth (e.g., k Miller-Rabin witnesses on the same
        n, or two classifiers querying the same input). Under this assumption
        and Axiom 1 (cross-instance independence of error events), both
        rates are prior-free closed forms::

            fpr_AND = alpha_1 * alpha_2
            fnr_AND = beta_1 + beta_2 - beta_1 * beta_2  =  1 - (1-beta_1)(1-beta_2)

        For the alternative scenario in which the two inputs are independent
        truths drawn from a shared prior pi (e.g., AND-ing two distinct
        boolean facts about a query), use :meth:`and_with_prior`.
        """
        v = self.value and other.value
        fpr = self.fpr * other.fpr
        fnr = self.fnr + other.fnr - self.fnr * other.fnr
        return BernoulliBool(value=v, fpr=fpr, fnr=fnr)

    def __or__(self, other: BernoulliBool) -> BernoulliBool:
        """OR under the **shared-truth** interpretation.

        Dual of :meth:`__and__`. Both rates are prior-free closed forms::

            fpr_OR = alpha_1 + alpha_2 - alpha_1 * alpha_2  =  1 - (1-alpha_1)(1-alpha_2)
            fnr_OR = beta_1 * beta_2

        The duality with AND is exact: OR's FNR mirrors AND's FPR, and
        vice versa, as expected from De Morgan's law.

        For independent-truths semantics, use :meth:`or_with_prior`.
        """
        v = self.value or other.value
        fpr = self.fpr + other.fpr - self.fpr * other.fpr
        fnr = self.fnr * other.fnr
        return BernoulliBool(value=v, fpr=fpr, fnr=fnr)

    def and_with_prior(self, other: BernoulliBool, prior: float) -> BernoulliBool:
        """AND using the closed-form prior-dependent FPR (book eq. 3.3).

        ``prior`` is ``P(true value of either input == True)``, assumed
        identical across the two inputs and independent.

        Returns the same FNR as ``__and__`` (which is prior-free) plus the
        exact FPR for the given prior.
        """
        if not 0.0 <= prior <= 1.0:
            raise ValueError(f"prior must be in [0, 1], got {prior!r}")

        v = self.value and other.value
        fnr = self.fnr + other.fnr - self.fnr * other.fnr

        # P[true AND = False] = 1 - prior^2
        # The three contributing patterns are weighted equally by prior(1-prior),
        # prior(1-prior), and (1-prior)^2.
        denom = 1.0 - prior * prior
        if denom <= 0.0:
            fpr = 0.0
        else:
            num = (
                prior * (1.0 - prior) * (1.0 - self.fnr) * other.fpr
                + (1.0 - prior) * prior * self.fpr * (1.0 - other.fnr)
                + (1.0 - prior) * (1.0 - prior) * self.fpr * other.fpr
            )
            fpr = num / denom
        return BernoulliBool(value=v, fpr=fpr, fnr=fnr)

    def or_with_prior(self, other: BernoulliBool, prior: float) -> BernoulliBool:
        """OR using the closed-form prior-dependent FNR (dual of AND's FPR).

        ``prior`` is ``P(true value of either input == True)``.

        Returns the same FPR as ``__or__`` (prior-free) plus the exact FNR
        for the given prior.
        """
        if not 0.0 <= prior <= 1.0:
            raise ValueError(f"prior must be in [0, 1], got {prior!r}")

        v = self.value or other.value
        fpr = self.fpr + other.fpr - self.fpr * other.fpr

        # P[true OR = True] = 1 - (1 - prior)^2
        denom = 1.0 - (1.0 - prior) * (1.0 - prior)
        if denom <= 0.0:
            fnr = 0.0
        else:
            num = (
                prior * prior * self.fnr * other.fnr
                + prior * (1.0 - prior) * self.fnr * (1.0 - other.fpr)
                + (1.0 - prior) * prior * (1.0 - self.fpr) * other.fnr
            )
            fnr = num / denom
        return BernoulliBool(value=v, fpr=fpr, fnr=fnr)

    NOT = __invert__
    AND = __and__
    OR = __or__

    @classmethod
    def certain(cls, value: bool) -> BernoulliBool:
        """A noiseless observation, ``(fpr, fnr) == (0, 0)``."""
        return cls(value=value, fpr=0.0, fnr=0.0)

    @classmethod
    def from_bsc(cls, value: bool, crossover: float) -> BernoulliBool:
        """An observation through a binary symmetric channel.

        ``fpr == fnr == crossover``.
        """
        return cls(value=value, fpr=crossover, fnr=crossover)

    @classmethod
    def one_sided_fpr(cls, value: bool, fpr: float) -> BernoulliBool:
        """A one-sided Bernoulli with ``fnr == 0``.

        Examples: Bloom filter membership test, Miller-Rabin's "is composite?"
        witness, any structure that always answers correctly on positives.
        """
        return cls(value=value, fpr=fpr, fnr=0.0)

    @classmethod
    def one_sided_fnr(cls, value: bool, fnr: float) -> BernoulliBool:
        """A one-sided Bernoulli with ``fpr == 0``.

        Examples: Las Vegas algorithms (correct when they answer; may fail
        to answer at all).
        """
        return cls(value=value, fpr=0.0, fnr=fnr)

    @classmethod
    def observe(
        cls,
        true_value: bool,
        fpr: float = 0.0,
        fnr: float = 0.0,
        rng: random.Random | None = None,
    ) -> BernoulliBool:
        """Sample one observation of ``true_value`` through a ``(fpr, fnr)`` channel.

        Useful for simulations and notebooks. The returned ``BernoulliBool``
        carries the realized output as ``.value`` and the channel rates.
        """
        rng = rng or random.Random()
        observed = (rng.random() >= fnr) if true_value else (rng.random() < fpr)
        return cls(value=observed, fpr=fpr, fnr=fnr)

    def __str__(self) -> str:
        return f"Bernoulli<bool>({self.value}, fpr={self.fpr:.4g}, fnr={self.fnr:.4g})"
