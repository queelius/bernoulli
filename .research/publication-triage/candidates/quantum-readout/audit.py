"""Exact, independent checks for the bounded quantum-readout publication audit.

Author: Alexander Richard Towell. Research audit, 2026-10-14.
All model probabilities use fractions; no sampled data establish the claims.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import prod
from pathlib import Path
from typing import Callable, Mapping, Sequence

Word = tuple[int, ...]
Law = dict[Word, Fraction]
Observable = Callable[[Word], int]
ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Channel:
    epsilon: Fraction
    omega: Fraction

    def __post_init__(self) -> None:
        if not all(0 <= p <= 1 for p in (self.epsilon, self.omega)):
            raise ValueError("Channel probabilities must lie in [0, 1]")

    def observed_one(self, truth: int) -> Fraction:
        if truth not in (0, 1):
            raise ValueError("Truth must be a bit")
        return 1 - self.omega if truth else self.epsilon


def independent_law(probabilities: Sequence[Fraction]) -> Law:
    """Enumerate the product distribution, including its zero-mass atoms."""
    return {
        word: Fraction(prod(p if bit else 1 - p for bit, p in zip(word, probabilities)))
        for word in product((0, 1), repeat=len(probabilities))
    }


def readout_law(channels: Sequence[Channel], truth: Word) -> Law:
    if len(channels) != len(truth):
        raise ValueError("One channel is required per latent bit")
    return independent_law([ch.observed_one(t) for ch, t in zip(channels, truth)])


def parity(word: Word) -> int:
    return sum(word) % 2


def error_probability(law: Mapping[Word, Fraction], observable: Observable, truth: int) -> Fraction:
    return sum((p for word, p in law.items() if observable(word) != truth), Fraction())


def parity_dynamic(rates: Sequence[Fraction]) -> Fraction:
    """Two-state forward recurrence, independent of the manuscript's product."""
    odd = Fraction()
    for rate in rates:
        odd = odd * (1 - rate) + (1 - odd) * rate
    return odd


def parity_product(rates: Sequence[Fraction]) -> Fraction:
    return Fraction(1 - prod(1 - 2 * rate for rate in rates), 2)


def conditioned_pair(
    channels: Sequence[Channel], ideal_law: Mapping[Word, Fraction], observable: Observable
) -> Channel:
    """Coarse output FPR/FNR require an ideal-word distribution, not just Q_i."""
    mass = [Fraction(), Fraction()]
    errors = [Fraction(), Fraction()]
    for truth, weight in ideal_law.items():
        output = observable(truth)
        mass[output] += weight
        errors[output] += weight * error_probability(readout_law(channels, truth), observable, output)
    if any(p == 0 for p in mass):
        raise ValueError("Both conditioning events need positive probability")
    return Channel(errors[0] / mass[0], errors[1] / mass[1])


def force_cause_law(
    base_rates: Sequence[Fraction], causes: Sequence[tuple[frozenset[int], Fraction]]
) -> Law:
    """Exact OR-cause model; condition on shared causes, then enumerate free bits."""
    n = len(base_rates)
    output = {word: Fraction() for word in product((0, 1), repeat=n)}
    for active, weight in independent_law([rate for _, rate in causes]).items():
        forced = frozenset().union(*(sites for (sites, _), on in zip(causes, active) if on))
        conditional_rates = [Fraction(1) if i in forced else p for i, p in enumerate(base_rates)]
        for word, conditional_weight in independent_law(conditional_rates).items():
            output[word] += weight * conditional_weight
    return output


def means_covariances(law: Mapping[Word, Fraction]) -> tuple[list[Fraction], dict[tuple[int, int], Fraction]]:
    n = len(next(iter(law)))
    means = [sum((p * word[i] for word, p in law.items()), Fraction()) for i in range(n)]
    covariances = {
        (i, j): sum((p * word[i] * word[j] for word, p in law.items()), Fraction()) - means[i] * means[j]
        for i, j in combinations(range(n), 2)
    }
    return means, covariances


def pairwise_parity_predictions(law: Mapping[Word, Fraction]) -> tuple[Fraction, Fraction, Fraction]:
    """Independent, paper's one-pair term, and full pair-cumulant baseline.

    The final entry sums all partial matchings (all cumulants of order >2 set
    to zero). This is the moment-cumulant construction, not a new method.
    Neither truncation is guaranteed to define a nonnegative joint law.
    """
    rates, covariance = means_covariances(law)
    mu = [1 - 2 * p for p in rates]
    anchor = parity_dynamic(rates)
    first = anchor - 2 * sum(
        (c * prod(mu[k] for k in range(len(mu)) if k not in pair) for pair, c in covariance.items()),
        Fraction(),
    )

    @lru_cache(maxsize=None)
    def pair_moment(sites: tuple[int, ...]) -> Fraction:
        if not sites:
            return Fraction(1)
        i, *rest = sites
        unpaired = mu[i] * pair_moment(tuple(rest))
        paired = sum(
            (4 * covariance[i, j] * pair_moment(tuple(k for k in rest if k != j)) for j in rest),
            Fraction(),
        )
        return unpaired + paired

    return anchor, first, (1 - pair_moment(tuple(range(len(mu))))) / 2


def central_expansion(law: Mapping[Word, Fraction]) -> Fraction:
    """Evaluate every central cross-moment; compare with direct odd mass."""
    rates, _ = means_covariances(law)
    mu = [1 - 2 * p for p in rates]
    sites = tuple(range(len(mu)))
    bias = Fraction()
    for size in range(len(mu) + 1):
        for subset in combinations(sites, size):
            moment = sum(
                (p * prod((1 - 2 * word[i]) - mu[i] for i in subset) for word, p in law.items()),
                Fraction(),
            )
            bias += moment * prod(mu[i] for i in sites if i not in subset)
    return (1 - bias) / 2


def canonical_rates(path: Path) -> list[Channel]:
    """Read the literal RATES assignment with Python's parser, without execution."""
    tree = ast.parse(path.read_text())
    assignment = next(
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "RATES" for target in node.targets)
    )
    return [Channel(Fraction(str(e)), Fraction(str(w))) for e, w in ast.literal_eval(assignment.value)]


def snapshot_rates(path: Path) -> list[Channel]:
    snapshot = json.loads(path.read_text())
    channels = []
    for qubit in snapshot["qubits"]:
        values = {entry["name"]: Fraction(str(entry["value"])) for entry in qubit}
        channels.append(Channel(values["prob_meas1_prep0"], values["prob_meas0_prep1"]))
    return channels


def run_audit() -> dict[str, object]:
    channels = canonical_rates(ROOT / "papers/bernoulli-quantum-readout/code/readout_figure.py")
    fetched_channels = snapshot_rates(HERE / "evidence/hanoi.json")
    if channels != fetched_channels:
        raise ValueError("Canonical hardcoded rates do not match the retrieved calibration")
    symmetric = []
    for q in (Fraction(1, 100), Fraction(5, 100)):
        for n in (2, 4, 8):
            exact = error_probability(independent_law([q] * n), parity, 0)
            symmetric.append({"q": float(q), "n": n, "exact": float(exact),
                              "relative_linear_overestimate": float(n * q / exact - 1)})
    asymmetric_channels = [Channel(Fraction(2, 100), Fraction(10, 100))] * 2 + [Channel(Fraction(4, 100), Fraction(12, 100))] * 2
    asymmetric = {
        "".join(map(str, word)): float(error_probability(readout_law(asymmetric_channels, word), parity, parity(word)))
        for word in ((0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 1, 1), (1, 1, 1, 1))
    }
    asymmetric["symmetrized_q_0.07"] = float(parity_dynamic([Fraction(7, 100)] * 4))
    cold = parity_dynamic([ch.epsilon for ch in channels])
    hot = parity_dynamic([ch.omega for ch in channels])
    e, w = Fraction(2, 100), Fraction(10, 100)
    def and_gate(bits: Word) -> int:
        return bits[0] & bits[1]

    def tree(bits: Word) -> int:
        return (bits[0] & bits[1]) | bits[2]
    and_00 = error_probability(readout_law([Channel(e, w)] * 2, (0, 0)), and_gate, 0)
    and_01 = error_probability(readout_law([Channel(e, w)] * 2, (0, 1)), and_gate, 0)
    tree_exact = error_probability(readout_law([Channel(e, w)] * 3, (0, 1, 0)), tree, 0)
    tree_corner = 1 - (1 - e * e) * (1 - e)
    crosstalk = []
    base = [ch.epsilon for ch in channels[:8]]
    for rate in (Fraction(1, 1000), Fraction(5, 1000), Fraction(1, 100), Fraction(2, 100), Fraction(5, 100)):
        for name, sites in (
            ("chain", [frozenset((i, i + 1)) for i in range(7)]),
            ("global", [frozenset(range(8))]),
        ):
            law = force_cause_law(base, [(subset, rate) for subset in sites])
            exact = error_probability(law, parity, 0)
            anchor, first, cumulant = pairwise_parity_predictions(law)
            crosstalk.append({"model": name, "lambda": float(rate), "exact": float(exact),
                             "independent": float(anchor), "first_pair": float(first),
                             "all_pair_cumulants": float(cumulant),
                             "first_pair_relative_error": float((first - exact) / exact)})
    no_covariance = []
    independent = independent_law([Fraction(1, 10)] * 3)
    for delta in (Fraction(-9, 10000), Fraction(9, 10000)):
        law = {word: p + delta * (-1) ** parity(word) for word, p in independent.items()}
        means, covariance = means_covariances(law)
        no_covariance.append({"delta": float(delta), "means": list(map(float, means)),
                              "max_abs_covariance": float(max(map(abs, covariance.values()))),
                              "parity_error": float(error_probability(law, parity, 0))})
    return {
        "author": "Alexander Richard Towell", "audit_date": "2026-10-14",
        "calibration_all_54_rates_match": True, "symmetric_table": symmetric,
        "asymmetric_table": asymmetric,
        "device_27": {"cold": float(cold), "hot": float(hot), "gap": float(hot - cold),
                      "cold_linear_relative_overestimate": float(sum(ch.epsilon for ch in channels) / cold - 1)},
        "conditioning_counterexample": {"and_truth_00": str(and_00), "and_truth_01": str(and_01),
                                         "read_once_tree_exact": str(tree_exact), "read_once_tree_corner_reuse": str(tree_corner)},
        "crosstalk": crosstalk, "same_marginals_zero_pair_covariances": no_covariance,
    }


def main() -> None:
    report = run_audit()
    (HERE / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
