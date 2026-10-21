#!/usr/bin/env python3
"""Rebuild all recorded payloads and exact contracts; recheck build-zero queries."""
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'code'))
from experiment import (  # noqa: E402
    CandidateSet, Family, Query, Workload, build_representation,
    execute, methods_for, validate_workload)


def verify():
    start = time.perf_counter()
    audits = []
    checked_queries = 0
    for path in sorted((HERE / 'data').glob('*/results.json')):
        result = json.loads(path.read_text())
        inputs = json.loads(path.with_name('input.json').read_text())
        info = result['workload']
        workload = Workload(info['name'], tuple(bytes.fromhex(k) for k in inputs['keys_hex']),
                            tuple(inputs['construction_values']),
                            tuple(bytes.fromhex(k) for k in inputs['catalog_hex']),
                            tuple(inputs['candidate_pool']),
                            tuple(Query(q['left'], q['right'], q['profile'], q['repeats'],
                                        tuple(q['candidates'])) for q in inputs['queries']),
                            info['extraction_seconds'], info['provenance'])
        validate_workload(workload)
        assert workload.common_payload == path.with_name('common.bin').read_bytes()
        target = Fraction(result['config']['query_target'])
        methods = {m.name: m for m in methods_for(workload.capacity, target, len(workload.catalog))}
        for saved in result['methods']:
            method = methods[saved['name']]
            assert str(method.source_rate) == saved['rate'] and method.width == saved['width']
        for saved in result['builds']:
            method = methods[saved['method']]
            store, payload, rate, bound, attempts = build_representation(method, workload, saved['seed'], target)
            assert hashlib.sha256(payload).hexdigest() == saved['payload_sha256']
            assert len(payload) == saved['representation_bytes']
            assert attempts == saved['attempts']
            assert bound <= target
            audits.append({'case': info['name'], 'method': method.name, 'build': saved['build'],
                           'rate_exact': str(rate), 'bound_exact': str(bound),
                           'guarantee_kind': method.contract_kind,
                           'finite_or_ideal_certificate': method.family is not Family.FUSE})
            if saved['build'] == 0:
                assert payload == path.with_name(f'{method.name}.bin').read_bytes()
                by_profile = defaultdict(int)
                for query in workload.queries:
                    candidates = CandidateSet(query.candidates, len(workload.catalog))
                    answer, _ = execute(method, store, workload.keys, len(workload.catalog), candidates,
                                        workload.keys[query.left], workload.keys[query.right])
                    by_profile[query.profile] += answer
                    checked_queries += 1
                for row in result['queries']:
                    if row['build'] == 0 and row['method'] == method.name:
                        assert by_profile[row['profile']] == row['positives']
        print('Verified', info['name'], len(result['builds']), 'payloads', flush=True)
    report = {'status': 'passed', 'payloads_rebuilt': len(audits), 'queries_rechecked': checked_queries,
              'seconds': time.perf_counter() - start, 'audits': audits,
              'current_source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                        for p in (HERE / 'code').glob('*.py')},
              'scope': 'All recorded payload hashes, dimensions, attempts, and exact rational bounds reproduced. Build-zero queries reproduced. Fuse bound is nominal only, not a certificate.'}
    (HERE / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    output = verify()
    print(output['status'], output['payloads_rebuilt'], output['queries_rechecked'])
