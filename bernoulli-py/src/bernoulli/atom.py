"""The atomic Bernoulli type: a noisy Boolean with channel rates ``(fpr, fnr)``.

The class :class:`BernoulliBool` represents a single observation drawn through
a binary channel parameterized by:

- ``fpr`` (alpha): false-positive rate, ``P(observe true | true value false)``
- ``fnr`` (beta):  false-negative rate, ``P(observe false | true value true)``

The operators ``~``, ``&`` and ``|`` return another :class:`BernoulliBool`, and
book chapter 3 derives their rates. Which formula is exact depends on what the
operands observe, so the semantics are stated per method:

1. ``~b`` swaps the two rates. Exact for any single observation.
2. ``a & b`` and ``a | b`` use the **shared-truth** reading: both operands are
   independent noisy observations of the *same* latent truth value (``k``
   Miller-Rabin rounds on one ``n``, two classifiers on one input). The rates
   are then prior-free products, and a read-once AND/OR tree of independent
   observations of one latent bit composes exactly node by node.
3. ``and_with_prior`` and ``or_with_prior`` use the **independent-truths**
   reading: each operand observes its own latent bit, true with probability
   ``prior``. The returned prior-dependent rate is the exact marginal for that
   one gate, averaged over the input words.

What does *not* hold is exact composition through an arbitrary Boolean formula.
Over different latent bits, a gate's output is not a two-rate bit: the AND's
false-positive rate is ``fpr_1 * (1 - fnr_2)`` when the true inputs are
``(False, True)`` and ``fpr_1 * fpr_2`` when they are ``(False, False)``. A
later gate that receives one summary number cannot tell these apart. For
``(b0 & b1) | b2`` with every channel at ``(0.02, 0.10)`` and true inputs
``(False, True, False)``, the exact error is 0.03764 while chaining the
operators reports 0.020392. The operators also cannot detect a reused operand:
``b & b`` treats one observation as two independent ones, and ``a & ~b`` of two
observations of one bit violates the shared-truth premise. Use
:mod:`bernoulli.formula` for exact per-word rates, a sound worst-case pair, or
prior-weighted marginals through a whole formula.

Two structurally important specializations:

- ``one_sided_fpr(value, fpr)``: a Bernoulli with ``fnr == 0``. The Bloom
  filter family, Miller-Rabin's witness AND, and any "membership-checked then
  ..." structure live here. There is no false negative; the structure is
  conservative on the positive side.
- ``one_sided_fnr(value, fnr)``: dual; ``fpr == 0``. Las Vegas algorithms and
  any "answer is always correct, but might fail to answer" structure.

Under the shared-truth reading, the AND of two ``one_sided_fpr`` instances is
again ``one_sided_fpr`` with ``fpr_1 * fpr_2``, independent of any prior, which
is why Miller-Rabin's ``alpha^k`` bound holds in closed form: its rounds all
test the same ``n``.
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
        boolean facts about a query), use :meth:`and_with_prior`. Neither
        reading makes the result exact as an input to further gates over other
        latent bits; see the module docstring and :mod:`bernoulli.formula`.
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

        For independent-truths semantics, use :meth:`or_with_prior`; for exact
        rates through a larger formula, use :mod:`bernoulli.formula`.
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
        exact FPR for the given prior. That FPR is an average over the three
        negative input words, so it is the right rate for this one gate and
        the wrong one to feed into another gate; :func:`bernoulli.formula.marginal_rates`
        computes the marginal for a whole formula.
        """
        if not 0.0 <= prior <= 1.0:
            raise ValueError(f"prior must be in [0, 1], got {prior!r}")

        v = self.value and other.value
        fnr = self.fnr + other.fnr - self.fnr * other.fnr

        # P[true AND = False] = 1 - prior^2 = (1 - prior)(1 + prior). The three
        # negative words carry weights prior(1-prior), (1-prior)prior and
        # (1-prior)^2, so the common factor (1 - prior) cancels analytically.
        # Cancelling it in code avoids the precision lost to 1 - prior^2 near
        # prior = 1, and mirrors or_with_prior, where the uncancelled form
        # rounds to 0 for tiny priors.
        if prior >= 1.0:
            fpr = 0.0  # the negative class is empty
        else:
            num = (
                prior * (1.0 - self.fnr) * other.fpr
                + prior * self.fpr * (1.0 - other.fnr)
                + (1.0 - prior) * self.fpr * other.fpr
            )
            fpr = min(1.0, num / (1.0 + prior))
        return BernoulliBool(value=v, fpr=fpr, fnr=fnr)

    def or_with_prior(self, other: BernoulliBool, prior: float) -> BernoulliBool:
        """OR using the closed-form prior-dependent FNR (dual of AND's FPR).

        ``prior`` is ``P(true value of either input == True)``.

        Returns the same FPR as ``__or__`` (prior-free) plus the exact FNR
        for the given prior, averaged over the three positive input words (the
        same caveat as :meth:`and_with_prior` applies to further composition).
        """
        if not 0.0 <= prior <= 1.0:
            raise ValueError(f"prior must be in [0, 1], got {prior!r}")

        v = self.value or other.value
        fpr = self.fpr + other.fpr - self.fpr * other.fpr

        # P[true OR = True] = 1 - (1 - prior)^2 = prior(2 - prior). The three
        # positive words carry weights prior^2, prior(1-prior) and
        # (1-prior)prior, so the common factor prior cancels analytically,
        # which keeps tiny priors from cancelling or underflowing to 0.
        if prior <= 0.0:
            fnr = 0.0  # the positive class is empty
        else:
            num = (
                prior * self.fnr * other.fnr
                + (1.0 - prior) * self.fnr * (1.0 - other.fpr)
                + (1.0 - prior) * (1.0 - self.fpr) * other.fnr
            )
            fnr = min(1.0, num / (2.0 - prior))
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
