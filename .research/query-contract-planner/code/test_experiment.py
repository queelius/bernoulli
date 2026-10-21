import json
from dataclasses import replace
from fractions import Fraction

import pytest

from experiment import CandidateSet, build_representation, execute, interval, make_manifest, make_synthetic, methods_for, run_case, validate_workload, vary_candidates


def test_tiny_complete_experiment_uses_stored_representations(tmp_path):
    workload = make_synthetic(domain=8, rows=48, candidates=4, per_profile=3, seed=28)
    validate_workload(workload)
    result = run_case(workload, builds=2, seed=19, output=tmp_path)
    assert result['builds']
    assert {row['method'] for row in result['summary']} >= {
        'bloom_ordinary_union', 'bloom_constrained_union',
        'bloom_constrained_product', 'finite_rows_constrained_union',
        'finite_rows_ordinary_union', 'exact_values', 'fuse_constrained',
    }
    assert all(row['fn'] == 0 for row in result['summary'])
    assert all(row['repeat_mismatches'] == 0 for row in result['summary'])
    for row in result['builds']:
        assert row['total_bytes'] >= row['representation_bytes']
        if row['contract_kind'] == 'conditional_ideal':
            assert row['certified_bound'] <= 0.05
    saved = json.loads((tmp_path / 'results.json').read_text())
    assert saved['workload']['query_count'] == len(workload.queries)


def test_query_profiles_include_duplicate_operands_and_outside_shared_value():
    workload = make_synthetic(domain=16, rows=80, candidates=8, per_profile=3, seed=11)
    profiles = {query.profile for query in workload.queries}
    assert {'two_single', 'one_single', 'zero_single', 'same_outside', 'true'} <= profiles
    assert all(query.left != query.right and query.repeats == 3 for query in workload.queries)


def test_runtime_rejects_source_alias_before_applying_two_row_contract():
    workload = make_synthetic(domain=8, rows=24, candidates=4, per_profile=1)
    method = next(m for m in methods_for(4, Fraction(1, 20), 8) if m.name == 'finite_rows_constrained_union')
    store = build_representation(method, workload, 18, Fraction(1, 20))[0]
    with pytest.raises(ValueError, match='distinct'):
        execute(method, store, workload.keys, 8, workload.candidates, workload.keys[5], workload.keys[5])


def test_out_of_domain_candidates_cannot_alias_inserted_tuple_codes():
    workload = make_synthetic(domain=8, rows=24, candidates=4, per_profile=1)
    for candidates in ((8,), (-1,)):
        with pytest.raises(ValueError, match='domain'):
            validate_workload(replace(workload, candidates=candidates))


def test_plan_rejects_candidate_sets_larger_than_certified_capacity():
    workload = make_synthetic(domain=8, rows=24, candidates=4, per_profile=1)
    method = next(m for m in methods_for(2, Fraction(1, 20), 8) if m.name == 'finite_rows_constrained_union')
    store = build_representation(method, workload, 18, Fraction(1, 20))[0]
    with pytest.raises(ValueError, match='capacity'):
        execute(method, store, workload.keys, 8, workload.candidates, workload.keys[0], workload.keys[1])


def test_unavailable_fuse_width_does_not_remove_exact_and_finite_choices():
    methods = methods_for(64, Fraction(1, 10**6), 128)
    assert any(m.name == 'exact_values' for m in methods)
    assert any(m.name == 'finite_rows_constrained_union' for m in methods)
    assert not any(m.name == 'fuse_ordinary' for m in methods)


def test_zero_observed_error_has_nonzero_uncertainty():
    estimate = interval([0.0] * 32)
    assert estimate['bounded_mean_95']['hi'] > 0.10
    assert estimate['bounded_mean_95']['lo'] == 0
    estimate = interval([1.0] * 32)
    assert estimate['bounded_mean_95']['lo'] < 0.90
    assert estimate['bounded_mean_95']['hi'] == 1


def test_varying_candidate_workload_keeps_truth_profiles_valid():
    workload = vary_candidates(make_synthetic(32, 96, 16, 5), 8, 12)
    validate_workload(workload)
    assert workload.capacity == 8
    assert len({q.candidates for q in workload.queries}) == 5
    assert all(q.candidates is not None for q in workload.queries)
    assert len(workload.queries) == 25


def test_runtime_checks_actual_domain_even_for_prevalidated_candidates():
    workload = make_synthetic(8, 24, 4, 1)
    method = next(m for m in methods_for(4, Fraction(1,20), 8) if m.name == 'exact_values')
    store = build_representation(method, workload, 5, Fraction(1,20))[0]
    for candidates in ((8,), (-1,), CandidateSet((0,), 9)):
        with pytest.raises(ValueError, match='domain'):
            execute(method, store, workload.keys, 8, candidates, workload.keys[0], workload.keys[1])
    with pytest.raises(KeyError):
        execute(method, store, workload.keys, 8, workload.candidates, b'not-a-key', workload.keys[1])


def test_manifest_extraction_uses_pinned_git_objects():
    workload = make_manifest(('9d38e038d243c3d0f024050d873cda167b6aba77',
                              '61c4a4319ea3e93aae02e0e6b4b54fc3b054e3c7'), per_profile=1)
    validate_workload(workload)
    assert len(workload.keys) == 1840
    assert len(workload.catalog) == 904
    assert len(workload.candidates) == 276


def test_invalid_schema_cannot_reach_planning():
    workload = make_synthetic(8, 24, 4, 1)
    broken = [replace(workload, keys=workload.keys[::-1]),
              replace(workload, values=workload.values[:-1]),
              replace(workload, values=(99,) + workload.values[1:]),
              replace(workload, candidates=(1,0)),
              replace(workload, queries=(replace(workload.queries[0], right=workload.queries[0].left),))]
    for item in broken:
        with pytest.raises(ValueError):
            validate_workload(item)
    with pytest.raises(ValueError):
        make_synthetic(4, 8, 3)
    with pytest.raises(ValueError):
        interval([])
    with pytest.raises(ValueError):
        interval([2])


@pytest.mark.parametrize('target', [Fraction(1,10**12), Fraction(1,10**18)])
def test_all_optional_capabilities_keep_exact_fallback(target):
    methods = methods_for(64, target, 128)
    assert any(m.name == 'exact_values' for m in methods)
    assert all(m.source_rate > 0 for m in methods if m.name.startswith('bloom_'))
    workload = make_synthetic(128, 256, 64, 1)
    for method in methods:
        build_representation(method, workload, 16, target)


def test_duplicate_candidate_parameters_use_canonical_capacity(tmp_path):
    workload = make_synthetic(8, 24, 4, 1)
    duplicate = replace(workload, queries=tuple(replace(q, candidates=workload.candidates*3) for q in workload.queries))
    validate_workload(duplicate)
    assert duplicate.capacity == 4
    assert run_case(duplicate, 2, 19, tmp_path)['workload']['candidate_count'] == 4
