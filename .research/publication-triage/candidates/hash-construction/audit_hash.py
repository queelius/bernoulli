"""Finite ideal-hash audit; exact fractions except labeled numerical seed moments.

Run with Python 3.11+; no third-party dependencies. This is an audit, not a filter.
"""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
from math import comb, log2


def binomial_tail(n: int, rank: int, probability: Fraction) -> Fraction:
    """P[Binomial(n, probability) >= rank], including boundary ranks."""
    return sum(
        (Fraction(comb(n, k)) * probability**k * (1 - probability)**(n - k)
         for k in range(max(0, rank), n + 1)),
        Fraction(),
    )


@dataclass(frozen=True)
class Threshold:
    modulus: int
    members: int
    rank: int

    def __post_init__(self) -> None:
        if self.modulus < 1 or not 1 <= self.rank <= self.members:
            raise ValueError("Require modulus >= 1 and 1 <= rank <= members")

    def cdf(self, value: int) -> Fraction:
        probability = Fraction(min(self.modulus, max(0, value + 1)), self.modulus)
        return binomial_tail(self.members, self.rank, probability)

    def pmf(self) -> tuple[Fraction, ...]:
        return tuple(self.cdf(j) - self.cdf(j - 1) for j in range(self.modulus))

    def enumerate_pmf(self) -> tuple[Fraction, ...]:
        counts = Counter(sorted(row)[self.rank - 1]
                         for row in product(range(self.modulus), repeat=self.members))
        return tuple(Fraction(counts[j], self.modulus**self.members)
                     for j in range(self.modulus))

    def mean_recall(self) -> Fraction:
        # A named member with residue j is accepted iff fewer than rank of
        # the OTHER members have residue strictly below j. Ties are accepted.
        return sum((1 - binomial_tail(self.members - 1, self.rank,
                                     Fraction(j, self.modulus))
                    for j in range(self.modulus)), Fraction()) / self.modulus

    def fpr_moment(self, power: int) -> Fraction:
        return sum((prob * Fraction(j + 1, self.modulus)**power
                    for j, prob in enumerate(self.pmf())), Fraction())

    def best_of_cdf(self, value: int, trials: int) -> Fraction:
        """Minimum threshold across independent, distinct salt trials."""
        return 1 - (1 - self.cdf(value))**trials


def phf_losses(members: int, slots: int, cap: int,
               fingerprint_values: int) -> tuple[Fraction, Fraction]:
    """Enumerate conditional overwrite count and true fingerprint-test FNR.

    Placement and fingerprints are independent uniform ideal hashes. The last
    member in a slot wins. Averaging over uniformly named keys equals averaging
    a random write order for this aggregate loss calculation.
    """
    placements = [row for row in product(range(slots), repeat=members)
                  if max(Counter(row).values()) <= cap]
    displaced_count = sum(members - len(set(row)) for row in placements)
    displacement = Fraction(displaced_count, len(placements) * members)
    false_negatives = 0
    for row in placements:
        for fingerprints in product(range(fingerprint_values), repeat=members):
            stored = dict(zip(row, fingerprints))
            false_negatives += sum(stored[slot] != mark
                                   for slot, mark in zip(row, fingerprints))
    count = len(placements) * fingerprint_values**members * members
    return displacement, Fraction(false_negatives, count)


def geometric_moments(probability: float) -> dict[str, float]:
    """Numerical sums for Q on {1,2,...}; used only at p=1/2.

    200 terms leave < 2^-192 error in E log2 Q at p=1/2; floor-log sum
    through level 9 has omitted tail less than 2^-1022.
    """
    q = 1 - probability
    expected_log = sum(probability * q**(j - 1) * log2(j) for j in range(1, 201))
    expected_length = sum(q**(2**level - 1) for level in range(1, 10))
    entropy = -log2(probability) - q / probability * log2(q)
    return {
        "success_probability": probability,
        "expected_log2_Q_numerical": expected_log,
        "expected_floor_log2_Q_numerical": expected_length,
        "geometric_entropy_bits": entropy,
        "paper_expected_log2_Q_claim": -log2(probability) - q / probability * log2(q),
        "paper_entropy_claim": -log2(probability) + q / probability * log2(q),
    }


def fraction_value(value: Fraction) -> dict[str, int | float]:
    return {"numerator": value.numerator, "denominator": value.denominator,
            "decimal": float(value)}


def report() -> dict[str, object]:
    checked = 0
    for modulus in range(1, 5):
        for members in range(1, 5):
            for rank in range(1, members + 1):
                spec = Threshold(modulus, members, rank)
                assert spec.pmf() == spec.enumerate_pmf()
                checked += 1

    tiny = Threshold(2, 2, 1)
    adaptive = []
    for spec in (tiny, Threshold(100, 100, 1), Threshold(100, 100, 100)):
        fpr = spec.fpr_moment(1)
        recall = spec.mean_recall()
        adaptive.append({
            "modulus": spec.modulus, "members": spec.members, "rank": spec.rank,
            "mean_fpr": float(fpr), "mean_recall": float(recall),
            "youden_J": float(recall - fpr),
            "nonmember_covariance": float(spec.fpr_moment(2) - fpr**2),
        })

    # One nearby salvage: fixed FPR and at least rank accepted members.
    # The success event is identical for a fixed threshold and adaptive
    # threshold constrained afterward to be <= that fixed threshold.
    spec = Threshold(10, 4, 3)
    success = spec.cdf(1)
    assert success == Fraction(17, 625)
    phf = []
    for cap in (1, 2):
        lost, rejected = phf_losses(2, 2, cap, 2)
        phf.append({"members": 2, "slots": 2, "cap": cap,
                    "fingerprint_values": 2,
                    "conditional_displacement": fraction_value(lost),
                    "actual_fnr": fraction_value(rejected),
                    "paper_unconditional_loss_formula": 0.25})

    return {
        "exact_order_statistic_grid_cases": checked,
        "tiny_pmf": [fraction_value(x) for x in tiny.pmf()],
        "paper_tiny_pmf": [1, 0],
        "tiny_best_of_3_probability_threshold_zero": fraction_value(tiny.best_of_cdf(0, 3)),
        "adaptive_tradeoff": adaptive,
        "nearby_salvage": {
            "members": 4, "rank": 3, "fpr": 0.2,
            "success_probability": fraction_value(success),
            "expected_trials": fraction_value(1 / success),
            "success_within_8_trials": fraction_value(spec.best_of_cdf(1, 8)),
            "zero_false_negatives_success_at_m100_fpr001": "10^-200",
            "zero_false_negatives_expected_trials_at_m100_fpr001": "10^200",
        },
        "geometric_moments": geometric_moments(0.5),
        "phf_counterexamples": phf,
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
