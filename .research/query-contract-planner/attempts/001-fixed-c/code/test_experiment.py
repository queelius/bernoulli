import json

from experiment import make_synthetic, run_case, validate_workload


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
