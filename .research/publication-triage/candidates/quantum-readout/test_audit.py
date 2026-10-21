"""Boundary, exhaustive, and integration checks for the publication audit."""

import importlib.util
from fractions import Fraction as F
from itertools import product

import numpy as np
import pytest
from hypothesis import given, settings, strategies as st

import audit


@given(st.lists(st.integers(0, 10), max_size=6))
@settings(max_examples=50, derandomize=True)
def test_independent_parity_product_dynamic_and_enumeration_agree(numerators):
    rates = [F(n, 10) for n in numerators]
    oracle = audit.error_probability(audit.independent_law(rates), audit.parity, 0)
    assert audit.parity_dynamic(rates) == oracle == audit.parity_product(rates)


@pytest.mark.parametrize("probability", [F(-1, 100), F(101, 100)])
def test_invalid_channel(probability):
    with pytest.raises(ValueError):
        audit.Channel(probability, F())


def test_invalid_truth_and_width():
    with pytest.raises(ValueError):
        audit.Channel(F(), F()).observed_one(2)
    with pytest.raises(ValueError):
        audit.readout_law([], (0,))


def test_every_two_bit_boolean_function_against_tensor_matrix():
    channels = [audit.Channel(F(2, 100), F(10, 100)), audit.Channel(F(4, 100), F(12, 100))]
    matrix = np.kron(
        np.array([[.98, .02], [.10, .90]]),
        np.array([[.96, .04], [.12, .88]]),
    )
    words = list(product((0, 1), repeat=2))
    for truth_table in product((0, 1), repeat=4):
        def observable(word):
            return truth_table[2 * word[0] + word[1]]
        for i, truth in enumerate(words):
            mask = np.array([observable(word) != observable(truth) for word in words])
            exact = audit.error_probability(audit.readout_law(channels, truth), observable, observable(truth))
            assert float(exact) == pytest.approx(float(matrix[i] @ mask), abs=1e-15)


def test_no_universal_derived_rate_pair_even_without_source_reuse():
    channels = [audit.Channel(F(2, 100), F(10, 100))] * 3
    def derived(word):
        return (word[0] & word[1]) | word[2]
    exact = audit.error_probability(audit.readout_law(channels, (0, 1, 0)), derived, 0)
    assert exact == F(941, 25000)  # .03764
    corner_reuse = 1 - (1 - F(2, 100) ** 2) * (1 - F(2, 100))
    assert corner_reuse == F(2549, 125000)  # .020392
    assert exact != corner_reuse


def test_coarse_rates_depend_on_latent_word_distribution():
    channels = [audit.Channel(F(2, 100), F(10, 100))] * 2
    def conjunction(word):
        return word[0] & word[1]
    cold = audit.conditioned_pair(channels, {(0, 0): F(1, 2), (1, 1): F(1, 2)}, conjunction)
    mixed = audit.conditioned_pair(channels, {(0, 1): F(1, 2), (1, 1): F(1, 2)}, conjunction)
    assert cold.epsilon == F(1, 2500)
    assert mixed.epsilon == F(9, 500)
    assert cold.omega == mixed.omega == F(19, 100)
    with pytest.raises(ValueError):
        audit.conditioned_pair(channels, {(0, 0): F(1)}, conjunction)


def test_reused_source_idempotence_and_parity_cancellation():
    law = audit.readout_law([audit.Channel(F(2, 100), F(10, 100))], (0,))
    assert audit.error_probability(law, lambda b: b[0] & b[0], 0) == F(2, 100)
    assert audit.error_probability(law, lambda b: b[0] ^ b[0], 0) == 0
    assert audit.parity_dynamic([F(2, 100)] * 2) == F(49, 1250)


@pytest.mark.parametrize("n", [2, 3, 4])
def test_exact_central_expansion_for_arbitrary_dependent_laws(n):
    weights = [F(i + 1) for i in range(2 ** n)]
    total = sum(weights)
    law = {word: weight / total for word, weight in zip(product((0, 1), repeat=n), weights)}
    assert audit.central_expansion(law) == audit.error_probability(law, audit.parity, 0)


def test_two_bit_covariance_formula_exact():
    for p in (F(), F(1, 10), F(1, 2), F(1)):
        law = audit.force_cause_law([F(1, 100), F(1, 10)], [(frozenset((0, 1)), p)])
        _, first, cumulant = audit.pairwise_parity_predictions(law)
        assert first == cumulant == audit.error_probability(law, audit.parity, 0)


def test_identical_low_order_data_different_parity():
    independent = audit.independent_law([F(1, 10)] * 3)
    outputs = []
    for delta in (F(-9, 10000), F(9, 10000)):
        law = {word: p + delta * (-1) ** audit.parity(word) for word, p in independent.items()}
        assert min(law.values()) >= 0 and sum(law.values()) == 1
        means, covariance = audit.means_covariances(law)
        assert means == [F(1, 10)] * 3
        assert set(covariance.values()) == {F()}
        outputs.append(audit.error_probability(law, audit.parity, 0))
    assert outputs == [F(619, 2500), F(601, 2500)]  # .2476 and .2404


def test_full_pair_cumulants_capture_two_independent_correlated_pairs():
    causes = audit.independent_law([F(1, 10), F(1, 5)])
    law = {(c, c, d, d): p for (c, d), p in causes.items()}
    _, first, all_pairs = audit.pairwise_parity_predictions(law)
    assert audit.error_probability(law, audit.parity, 0) == 0
    assert all_pairs == 0
    assert first == F(72, 625)  # .1152: it omits the product of both pair covariances.


def test_canonical_tables_and_or_cause_model_integration():
    source = audit.ROOT / "papers/bernoulli-quantum-readout/code/crosstalk_validation.py"
    spec = importlib.util.spec_from_file_location("canonical_crosstalk", source)
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    channels = audit.canonical_rates(audit.ROOT / "papers/bernoulli-quantum-readout/code/readout_figure.py")
    assert channels == audit.snapshot_rates(audit.HERE / "evidence/hanoi.json")
    base = [ch.epsilon for ch in channels[:4]]
    for rate in (F(), F(1, 100), F(1, 2), F(1)):
        law = audit.force_cause_law(base, [(frozenset((i, i + 1)), rate) for i in range(3)])
        exact = audit.error_probability(law, audit.parity, 0)
        assert sum(law.values()) == 1
        assert float(exact) == pytest.approx(original.chain_exact(np.array(list(map(float, base))), float(rate)), abs=1e-14)
        assert audit.central_expansion(law) == exact


def test_report_and_main(monkeypatch, tmp_path):
    report = audit.run_audit()
    assert report["calibration_all_54_rates_match"]
    assert report["asymmetric_table"]["0000"] == pytest.approx(.10997888)
    assert report["asymmetric_table"]["symmetrized_q_0.07"] == pytest.approx(.22649592)
    assert report["device_27"]["cold"] == pytest.approx(.2579, abs=.00005)
    assert report["device_27"]["hot"] == pytest.approx(.3688, abs=.00005)
    # Keep the output-only path branch covered without duplicating the expensive audit.
    monkeypatch.setattr(audit, "run_audit", lambda: report)
    monkeypatch.setattr(audit, "HERE", tmp_path)
    audit.main()
    assert (tmp_path / "results.json").exists()


def test_snapshot_mismatch_is_not_silently_accepted(monkeypatch):
    monkeypatch.setattr(audit, "snapshot_rates", lambda path: [])
    with pytest.raises(ValueError, match="do not match"):
        audit.run_audit()
