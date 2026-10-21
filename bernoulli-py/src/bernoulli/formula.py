"""Exact error rates of Boolean formulas over independent noisy bits.

Why this module exists
----------------------
A single gate over two noisy bits has closed-form rates (book chapter 3, and
:class:`bernoulli.atom.BernoulliBool`). A *pair* ``(fpr, fnr)`` does not,
however, carry through an arbitrary Boolean tree. The output of ``x0 AND x1``
over two different latent bits is not a two-rate bit: its false-positive rate
is ``fpr0 * (1 - fnr1)`` when the latent word is ``(False, True)`` and
``fpr0 * fpr1`` when it is ``(False, False)``. A later gate that receives only
one summary number cannot tell which case occurred.

Counterexample. For ``(x0 AND x1) OR x2`` with every channel at
``fpr = 0.02``, ``fnr = 0.10`` and latent word ``(False, True, False)``, the
exact error is ``1 - (1 - 0.02 * 0.90)(1 - 0.02) = 0.03764``. Reusing the pair
(``fpr0 * fpr1`` for the AND, then the OR rule) gives ``0.020392``, about half
the true value. The pair-reuse number is the exact error at the all-negative
word ``(False, False, False)`` only.

Model
-----
There are ``n`` latent bits ``w = (w_0, ..., w_{n-1})``. Bit ``i`` is observed
once, through its own binary channel with rates ``(fpr_i, fnr_i)``, and the
observations are independent given ``w`` (the framework's Axiom 1). A formula
``f`` is evaluated on the observed word ``o``; the correct answer is ``f(w)``.
For a fixed latent word,

    P(observed f is True | w) = sum over o of prod_i P(o_i | w_i) * [f(o)].

Evaluation
----------
For a *read-once* formula (each variable occurs at most once) the sum collapses
to one linear pass with the signal-probability rules of Parker and McCluskey
(1975): ``p(NOT g) = 1 - p(g)``, ``p(g AND h) = p(g) p(h)`` and
``p(g OR h) = 1 - (1 - p(g))(1 - p(h))``. They hold because the operands depend
on disjoint, independent observations. A variable that occurs more than once
is still one observation feeding several places, so its occurrences are
perfectly correlated; the evaluator conditions on the observed values of the
repeated variables (a Shannon expansion), which costs ``2**r`` passes for ``r``
repeated variables.

What to use
-----------
- :func:`error_probability`: the exact error at one latent word.
- :func:`error_profile`: the error at every latent word. The number of distinct
  values is the formula's model order; a two-rate summary is exact only when
  it is at most one value per output class.
- :func:`worst_case_rates`: a sound pair. Its ``fpr`` is the largest
  false-positive probability over the negative latent words and its ``fnr``
  the largest false-negative probability over the positive ones, so every
  latent word's error is bounded by the pair. It bounds this formula only: it
  is not a channel to feed into further gates (see the function).
- :func:`marginal_rates`: the prior-weighted average rates when the latent bits
  are independent Bernoulli variables. It is the exact marginal for this
  formula, and like any average it is not itself composable.

Cost and limits
---------------
Evaluating one latent word costs ``2**r`` passes over the formula for ``r``
repeated variables, and the profile functions repeat that for all ``2**n``
latent words. Calls whose exponent (``r`` for one word, ``n + r`` for the
profile functions) exceeds :data:`MAX_ENUMERATION_VARIABLES` raise
``ValueError``. The tree is walked recursively, so nesting depth is bounded by
Python's recursion limit (about 1000 levels); build long conjunctions or
disjunctions as balanced trees rather than as a left-leaning chain.

Examples
--------
>>> from bernoulli.sets.composition import SetRates
>>> x = variables(3)
>>> f = (x[0] & x[1]) | x[2]
>>> str(f)
'(x0 & x1) | x2'
>>> channels = [SetRates(fpr=0.02, fnr=0.10)] * 3
>>> round(error_probability(f, channels, (False, True, False)), 6)
0.03764
>>> round(error_probability(f, channels, (False, False, False)), 6)
0.020392
>>> worst = worst_case_rates(f, channels)
>>> round(worst.fpr, 6), round(worst.fnr, 6)
(0.03764, 0.1862)

The pair-reuse value is exact only at the all-negative word, which is why it
cannot stand in for the formula's false-positive rate.
"""

from __future__ import annotations

import itertools
import math
from abc import ABC, abstractmethod
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from bernoulli.sets.composition import SetRates

#: Largest enumeration exponent a call may use. One latent word costs ``2**r``
#: formula passes for ``r`` repeated variables; the profile functions
#: (:func:`error_profile`, :func:`worst_case_rates`, :func:`marginal_rates`)
#: cost ``2**(n + r)``. A call over the limit raises ``ValueError``, which
#: keeps every call below about a million formula passes.
MAX_ENUMERATION_VARIABLES: int = 20

Word = tuple[bool, ...]


class RatePair(Protocol):
    """Anything with a false-positive and a false-negative rate.

    :class:`bernoulli.sets.composition.SetRates` and
    :class:`bernoulli.atom.BernoulliBool` both qualify.
    """

    @property
    def fpr(self) -> float: ...

    @property
    def fnr(self) -> float: ...


class Formula(ABC):
    """A Boolean formula over indexed variables.

    Build formulas from :func:`variables` with ``&``, ``|`` and ``~``. Nodes are
    immutable and compare structurally.
    """

    __slots__ = ()

    def __and__(self, other: Formula) -> Formula:
        return And(self, other)

    def __or__(self, other: Formula) -> Formula:
        return Or(self, other)

    def __invert__(self) -> Formula:
        return Not(self)

    @abstractmethod
    def evaluate(self, word: Sequence[bool]) -> bool:
        """The formula's value on a word of variable values."""

    @abstractmethod
    def occurrences(self) -> Counter[int]:
        """How many times each variable index occurs in the formula."""

    def is_read_once(self) -> bool:
        """True iff every variable occurs at most once."""
        return all(count == 1 for count in self.occurrences().values())

    @abstractmethod
    def _signal_probability(self, p_true: Sequence[float]) -> float:
        """``P(formula is True)`` by the read-once rules.

        ``p_true[i]`` is the probability that variable ``i`` is True. The
        result is exact when the variables that occur more than once have
        ``p_true`` equal to 0 or 1, which is how :func:`output_probability`
        calls it.
        """


@dataclass(frozen=True, slots=True)
class Var(Formula):
    """The variable with index ``index``."""

    index: int

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError(f"variable index must be non-negative, got {self.index!r}")

    def evaluate(self, word: Sequence[bool]) -> bool:
        return bool(word[self.index])

    def occurrences(self) -> Counter[int]:
        return Counter({self.index: 1})

    def _signal_probability(self, p_true: Sequence[float]) -> float:
        return p_true[self.index]

    def __str__(self) -> str:
        return f"x{self.index}"


@dataclass(frozen=True, slots=True)
class Not(Formula):
    """Negation of ``operand``."""

    operand: Formula

    def evaluate(self, word: Sequence[bool]) -> bool:
        return not self.operand.evaluate(word)

    def occurrences(self) -> Counter[int]:
        return self.operand.occurrences()

    def _signal_probability(self, p_true: Sequence[float]) -> float:
        return 1.0 - self.operand._signal_probability(p_true)

    def __str__(self) -> str:
        return f"~{_parenthesize(self.operand)}"


@dataclass(frozen=True, slots=True)
class And(Formula):
    """Conjunction of ``left`` and ``right``."""

    left: Formula
    right: Formula

    def evaluate(self, word: Sequence[bool]) -> bool:
        return self.left.evaluate(word) and self.right.evaluate(word)

    def occurrences(self) -> Counter[int]:
        return self.left.occurrences() + self.right.occurrences()

    def _signal_probability(self, p_true: Sequence[float]) -> float:
        return self.left._signal_probability(p_true) * self.right._signal_probability(
            p_true
        )

    def __str__(self) -> str:
        return f"{_parenthesize(self.left)} & {_parenthesize(self.right)}"


@dataclass(frozen=True, slots=True)
class Or(Formula):
    """Disjunction of ``left`` and ``right``."""

    left: Formula
    right: Formula

    def evaluate(self, word: Sequence[bool]) -> bool:
        return self.left.evaluate(word) or self.right.evaluate(word)

    def occurrences(self) -> Counter[int]:
        return self.left.occurrences() + self.right.occurrences()

    def _signal_probability(self, p_true: Sequence[float]) -> float:
        p_left = self.left._signal_probability(p_true)
        p_right = self.right._signal_probability(p_true)
        return 1.0 - (1.0 - p_left) * (1.0 - p_right)

    def __str__(self) -> str:
        return f"{_parenthesize(self.left)} | {_parenthesize(self.right)}"


def _parenthesize(node: Formula) -> str:
    return str(node) if isinstance(node, (Var, Not)) else f"({node})"


def variables(n: int) -> tuple[Var, ...]:
    """The variables ``x0, ..., x{n-1}``.

    >>> x0, x1 = variables(2)
    >>> str(~(x0 | x1))
    '~(x0 | x1)'
    """
    if n < 0:
        raise ValueError(f"n must be non-negative, got {n!r}")
    return tuple(Var(i) for i in range(n))


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def _repeated_variables(formula: Formula, channels: Sequence[RatePair]) -> list[int]:
    """Validate the inputs; return the variables that occur more than once."""
    for i, ch in enumerate(channels):
        if not (0.0 <= ch.fpr <= 1.0 and 0.0 <= ch.fnr <= 1.0):
            raise ValueError(f"channel {i} has rates outside [0, 1]: {ch!r}")
    counts = formula.occurrences()
    if counts and max(counts) >= len(channels):
        raise ValueError(
            f"formula uses variable x{max(counts)} but only {len(channels)} "
            "channels were given"
        )
    return sorted(i for i, c in counts.items() if c > 1)


def _check_budget(exponent: int, what: str) -> None:
    if exponent > MAX_ENUMERATION_VARIABLES:
        raise ValueError(
            f"{what} needs 2**{exponent} formula passes; the limit is "
            f"2**{MAX_ENUMERATION_VARIABLES} (MAX_ENUMERATION_VARIABLES)"
        )


def _check_word(word: Sequence[bool], n: int) -> None:
    if len(word) != n:
        raise ValueError(f"latent word has length {len(word)}, expected {n}")


def _output_probability(
    formula: Formula,
    channels: Sequence[RatePair],
    word: Sequence[bool],
    repeated: Sequence[int],
) -> float:
    # P(observed bit i is True | latent bit w_i).
    p_obs = [
        1.0 - ch.fnr if w else ch.fpr for ch, w in zip(channels, word, strict=True)
    ]
    total = 0.0
    for observed in itertools.product((False, True), repeat=len(repeated)):
        weight = 1.0
        p_true = list(p_obs)
        for i, bit in zip(repeated, observed, strict=True):
            weight *= p_obs[i] if bit else 1.0 - p_obs[i]
            p_true[i] = 1.0 if bit else 0.0
        if weight > 0.0:
            total += weight * formula._signal_probability(p_true)
    return _clamp01(total)


def output_probability(
    formula: Formula, channels: Sequence[RatePair], word: Sequence[bool]
) -> float:
    """``P(observed formula is True | latent word)``, exactly.

    ``channels[i]`` gives the rates of variable ``i``; ``word[i]`` is its latent
    (true) value.

    >>> from bernoulli.sets.composition import SetRates
    >>> x0, x1 = variables(2)
    >>> ch = [SetRates(fpr=0.1, fnr=0.2), SetRates(fpr=0.3, fnr=0.4)]
    >>> round(output_probability(x0 & x1, ch, (True, False)), 6)   # 0.8 * 0.3
    0.24
    """
    repeated = _repeated_variables(formula, channels)
    _check_word(word, len(channels))
    _check_budget(len(repeated), f"{len(repeated)} repeated variables")
    return _output_probability(formula, channels, word, repeated)


def error_probability(
    formula: Formula, channels: Sequence[RatePair], word: Sequence[bool]
) -> float:
    """``P(observed formula != formula(word))`` at one latent word, exactly.

    >>> from bernoulli.sets.composition import SetRates
    >>> x = variables(3)
    >>> ch = [SetRates(fpr=0.02, fnr=0.10)] * 3
    >>> round(error_probability((x[0] & x[1]) | x[2], ch, (False, True, False)), 6)
    0.03764
    """
    p = output_probability(formula, channels, word)
    return 1.0 - p if formula.evaluate(word) else p


def error_profile(
    formula: Formula, channels: Sequence[RatePair]
) -> dict[Word, float]:
    """The exact error probability at every latent word.

    The keys are all ``2**n`` words for ``n = len(channels)``.

    >>> from bernoulli.sets.composition import SetRates
    >>> x0, x1 = variables(2)
    >>> ch = [SetRates(fpr=0.1, fnr=0.0)] * 2
    >>> {w: round(e, 4) for w, e in error_profile(x0 & x1, ch).items()}
    {(False, False): 0.01, (False, True): 0.1, (True, False): 0.1, (True, True): 0.0}
    """
    repeated = _repeated_variables(formula, channels)
    n = len(channels)
    _check_budget(
        n + len(repeated),
        f"{2**n} latent words with {len(repeated)} repeated variables "
        "(error_probability evaluates single words)",
    )
    profile: dict[Word, float] = {}
    for word in itertools.product((False, True), repeat=n):
        p = _output_probability(formula, channels, word, repeated)
        profile[word] = 1.0 - p if formula.evaluate(word) else p
    return profile


def worst_case_rates(formula: Formula, channels: Sequence[RatePair]) -> SetRates:
    """A sound two-rate summary: the worst error in each output class.

    ``fpr`` is the maximum false-positive probability over latent words where
    the formula is False, and ``fnr`` the maximum false-negative probability
    over words where it is True (0 when the class is empty). Every latent
    word's error is at most the matching rate, whatever the input distribution.

    The pair bounds this formula's own error. It is not a channel to feed into
    a larger formula: a gate's error can fall as an input's rate rises (``g & y``
    with ``g`` true and ``y`` false errs with probability ``(1 - fnr_g) fpr_y``),
    so substituting the maximum can understate the larger formula's error.
    Enumerate the larger formula instead.
    """
    fpr = 0.0
    fnr = 0.0
    for word, err in error_profile(formula, channels).items():
        if formula.evaluate(word):
            fnr = max(fnr, err)
        else:
            fpr = max(fpr, err)
    return SetRates(fpr=fpr, fnr=fnr)


def marginal_rates(
    formula: Formula,
    channels: Sequence[RatePair],
    priors: float | Sequence[float],
) -> SetRates:
    """The prior-weighted rates under independent Bernoulli latent bits.

    ``priors`` is ``P(w_i is True)``, either one value for every variable or one
    per variable. The ``fpr`` is ``P(observed True | formula False)`` and the
    ``fnr`` is ``P(observed False | formula True)``; a rate is 0 when its
    conditioning event has probability 0.

    For a single gate this reproduces
    :meth:`bernoulli.atom.BernoulliBool.and_with_prior` and
    :meth:`~bernoulli.atom.BernoulliBool.or_with_prior`.

    >>> from bernoulli.sets.composition import SetRates
    >>> x0, x1 = variables(2)
    >>> ch = [SetRates(fpr=0.10, fnr=0.05), SetRates(fpr=0.08, fnr=0.12)]
    >>> r = marginal_rates(x0 & x1, ch, priors=0.5)
    >>> round(r.fpr, 4), round(r.fnr, 4)
    (0.0573, 0.164)
    """
    n = len(channels)
    prior_list = [float(priors)] * n if isinstance(priors, (int, float)) else list(priors)
    if len(prior_list) != n:
        raise ValueError(f"got {len(prior_list)} priors for {n} channels")
    for i, pi in enumerate(prior_list):
        if not 0.0 <= pi <= 1.0:
            raise ValueError(f"prior {i} must be in [0, 1], got {pi!r}")

    # Word weights are products of priors, which underflow for extreme priors
    # (1e-200 squared is 0.0 in floating point) although the conditional rates
    # stay well defined. Work with log weights and normalize within each output
    # class by its largest weight before exponentiating.
    log_odds = [
        (math.log(pi) if pi > 0.0 else -math.inf, math.log1p(-pi) if pi < 1.0 else -math.inf)
        for pi in prior_list
    ]
    by_class: dict[bool, list[tuple[float, float]]] = {False: [], True: []}
    for word, err in error_profile(formula, channels).items():
        log_weight = sum(lt if w else lf for w, (lt, lf) in zip(word, log_odds, strict=True))
        if log_weight > -math.inf:
            by_class[formula.evaluate(word)].append((log_weight, err))

    def _ratio(cls: bool) -> float:
        terms = by_class[cls]
        if not terms:
            return 0.0
        top = max(lw for lw, _ in terms)
        mass = sum(math.exp(lw - top) for lw, _ in terms)
        weighted = sum(math.exp(lw - top) * err for lw, err in terms)
        return _clamp01(weighted / mass)

    return SetRates(fpr=_ratio(False), fnr=_ratio(True))
