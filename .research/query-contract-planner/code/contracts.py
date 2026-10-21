"""Small typed contracts for functional-row intersection; no novelty claim."""
from dataclasses import dataclass
from enum import StrEnum
from fractions import Fraction


class Budget(StrEnum):
    ORDINARY_UNION = 'ordinary_union'
    ORDINARY_PRODUCT = 'ordinary_product'
    CONSTRAINED_UNION = 'constrained_union'
    CONSTRAINED_PRODUCT = 'constrained_product'


def error_bound(budget: Budget, k: int, p: Fraction) -> Fraction:
    """Distinct rows, <=1 true value each, fixed false query; FN is zero.

    Product cases require independent distinct tuple FP events. Constrained
    union needs only the two-negative-atom witness bound <=p^2. Ordinary union
    needs only marginal FP<=p. With aliases use deduplicated lineage instead.
    """
    if k < 0 or not 0 <= p <= 1:
        raise ValueError('invalid domain or source probability')
    if k == 0:
        return Fraction(0)
    if budget is Budget.ORDINARY_UNION:
        return min(Fraction(1), k * p)
    if budget is Budget.ORDINARY_PRODUCT:
        return 1 - (1 - p) ** k
    if k == 1:
        return p
    if budget is Budget.CONSTRAINED_UNION:
        return min(Fraction(1), 2 * p + (k - 2) * p * p)
    if budget is Budget.CONSTRAINED_PRODUCT:
        return 1 - (1 - p) ** 2 * (1 - p * p) ** (k - 2)
    raise ValueError('unknown budget')


def plan_rate(budget: Budget, k: int, target: Fraction) -> Fraction:
    """Monotone dyadic search, rounding DOWN; exact certification of budget."""
    if k < 1 or not 0 < target < 1:
        raise ValueError('positive candidate count and target in (0,1) required')
    scale = 2**40
    low, high = 0, scale
    while high - low > 1:
        middle = (low + high) // 2
        if error_bound(budget, k, Fraction(middle, scale)) <= target:
            low = middle
        else:
            high = middle
    return Fraction(low, scale)


@dataclass(frozen=True, slots=True)
class FunctionalSchema:
    domain_size: int
    total: bool = True

    def __post_init__(self):
        if self.domain_size < 1:
            raise ValueError('nonempty declared value domain required')


@dataclass(frozen=True, order=True, slots=True)
class Source:
    row: int
    value: int


@dataclass(frozen=True, slots=True)
class IntersectionQuery:
    left: int
    right: int
    repeats: int = 1

    def __post_init__(self):
        if self.left < 0 or self.right < 0 or self.repeats < 1:
            raise ValueError('invalid row or repetition count')

    def lineage(self, schema: FunctionalSchema, candidates=None):
        domain = range(schema.domain_size) if candidates is None else sorted(set(candidates))
        # Repeated syntactic atoms denote the same frozen source, by identity.
        return tuple(frozenset((Source(self.left, z), Source(self.right, z))) for z in domain)

    def exact_from_schema(self, schema: FunctionalSchema):
        return True if self.left == self.right and schema.total else None


def profile_probability(k: int, singles: int, p: Fraction) -> Fraction:
    """Read-once lineage/WMC product for a fixed false profile, not a solver."""
    if not 0 <= singles <= min(k, 2):
        raise ValueError('invalid false profile')
    return 1 - (1 - p) ** singles * (1 - p * p) ** (k - singles)
