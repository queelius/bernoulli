"""Independent enumeration and regression checks for the bounded audit."""

from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

import pytest

from audit_hash import Threshold, binomial_tail, geometric_moments, phf_losses, report


@pytest.mark.parametrize("modulus,members", product(range(1, 5), range(1, 5)))
def test_exact_laws_against_full_enumeration(modulus: int, members: int) -> None:
    rows = list(product(range(modulus), repeat=members))
    for rank in range(1, members + 1):
        spec = Threshold(modulus, members, rank)
        assert spec.pmf() == spec.enumerate_pmf()
        recall = sum(Fraction(sum(value <= sorted(row)[rank - 1] for value in row), members)
                     for row in rows) / len(rows)
        fpr = sum(Fraction(sorted(row)[rank - 1] + 1, modulus) for row in rows) / len(rows)
        assert spec.mean_recall() == recall
        assert spec.fpr_moment(1) == fpr
        assert spec.cdf(-2) == 0 and spec.cdf(modulus + 1) == 1


def test_adaptive_cap_and_fixed_threshold_have_same_success_event() -> None:
    for row in product(range(4), repeat=3):
        assert (sorted(row)[1] <= 1) == (sum(value <= 1 for value in row) >= 2)
    rows = list(product(range(2), repeat=2))
    success = sum(min(min(row) for row in codebook) == 0
                  for codebook in product(rows, repeat=3))
    assert Threshold(2, 2, 1).best_of_cdf(0, 3) == Fraction(success, len(rows)**3)


def test_boundaries_and_rejected_parameters() -> None:
    assert binomial_tail(2, 0, Fraction(0)) == 1
    assert binomial_tail(2, 3, Fraction(1)) == 0
    assert Threshold(1, 4, 3).mean_recall() == 1
    for args in ((0, 1, 1), (2, 1, 0), (2, 1, 2)):
        with pytest.raises(ValueError):
            Threshold(*args)


def test_seed_moments_and_phf_counterexamples() -> None:
    moments = geometric_moments(0.5)
    assert 0.73264 < moments["expected_log2_Q_numerical"] < 0.73266
    assert 0.63284 < moments["expected_floor_log2_Q_numerical"] < 0.63285
    assert moments["geometric_entropy_bits"] == 2
    assert moments["paper_entropy_claim"] == 0
    assert phf_losses(2, 2, 1, 2) == (Fraction(0), Fraction(0))
    assert phf_losses(2, 2, 2, 2) == (Fraction(1, 4), Fraction(1, 8))


def test_cli_report_end_to_end() -> None:
    result = subprocess.run([sys.executable, str(Path(__file__).with_name("audit_hash.py"))],
                            check=True, capture_output=True, text=True)
    assert json.loads(result.stdout) == report()
    assert json.loads(result.stdout)["exact_order_statistic_grid_cases"] == 40
