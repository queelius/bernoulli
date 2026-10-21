#!/usr/bin/env python3
"""Produce transparent tables/figures from recorded measurements only."""
import csv
from fractions import Fraction
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    results = [json.loads(path.read_text()) for path in sorted((HERE / 'data').glob('*/results.json'))]
    rows = []
    for result in results:
        for row in result['summary']:
            if row['profile'] == 'two_single':
                rows.append({'workload': result['workload']['name'], 'method': row['method'],
                             'payload_bytes': row['representation_bytes'], 'total_bytes': row['total_bytes'],
                             'build_ms': row['mean_build_ms'], 'query_us': row['mean_query_us'],
                             'query_plus_preparation_us': row['mean_query_us_including_preparation'],
                             'empirical_fp': row['positive_interval']['mean'],
                             'bounded_mean_lo': row['positive_interval']['bounded_mean_95']['lo'],
                             'bounded_mean_hi': row['positive_interval']['bounded_mean_95']['hi'],
                             'reported_bound': row['max_reported_bound'],
                             'bound_kind': row['contract_kind']})
    with (HERE / 'summary.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifest = {r['method']: r for r in rows if r['workload'].startswith('git-manifest')}
    ordinary = manifest['bloom_ordinary_union']
    constrained = manifest['bloom_constrained_union']
    product = manifest['bloom_constrained_product']
    finite = manifest['finite_rows_constrained_union']
    exact = manifest['exact_values']
    p, k, repetitions = Fraction(1,64), 64, 3
    actual = 1 - (1-p)**2 * (1-p*p)**(k-2)
    invalid = 1 - (1-p**repetitions)**2 * (1-p**(2*repetitions))**(k-2)
    report = {
        'bloom_constraint_payload_saving': ordinary['payload_bytes'] - constrained['payload_bytes'],
        'bloom_sharp_incremental_bytes': constrained['payload_bytes'] - product['payload_bytes'],
        'bloom_sharp_incremental_total_percent': 100*(constrained['total_bytes'] - product['total_bytes'])/constrained['total_bytes'],
        'finite_vs_exact_bytes': exact['total_bytes'] - finite['total_bytes'],
        'finite_vs_exact_total_percent': 100*(exact['total_bytes'] - finite['total_bytes'])/exact['total_bytes'],
        'finite_vs_exact_payload_percent': 100*(exact['payload_bytes'] - finite['payload_bytes'])/exact['payload_bytes'],
        'finite_vs_exact_latency_ratio_with_preparation': finite['query_plus_preparation_us']/exact['query_plus_preparation_us'],
        'continuous_sharp_vs_union_bit_limit_at_005': math.log2(-math.log1p(-.05)/.05),
        'repeated_operand_example': {'rate': str(p), 'candidates': k, 'copies_of_each_atom': repetitions,
                                    'correct_independent_distinct_source_probability': float(actual),
                                    'incorrect_independent_occurrence_probability': float(invalid),
                                    'scope': 'Exact rational independent-source calculations; not a product theorem for four-wise fingerprints.'},
        'constructions': sum(len(r['builds']) for r in results),
        'primary_queries': sum(q['queries'] for r in results for q in r['queries']),
        'false_negatives': sum(q['fn'] for r in results for q in r['queries']),
        'repeat_mismatches': sum(q['repeat_mismatches'] for r in results for q in r['queries']),
        'cases': len(results),
    }
    (HERE / 'findings.json').write_text(json.dumps(report, indent=2) + '\n')

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    names = ['bloom_ordinary_union','bloom_constrained_union','bloom_constrained_product',
             'finite_rows_constrained_union','fuse_constrained','exact_values']
    labels = ['Bloom\nordinary\nunion','Bloom\nconstrained\nunion','Bloom\nsharp\nproduct',
              'Finite row\nfingerprints','Binary fuse\n(nominal)','Exact\nvalue IDs']
    selected = [manifest[name] for name in names]
    fig, axes = plt.subplots(1,2,figsize=(11,4.8), layout='constrained')
    colors = ['#9aa4ad','#4e79a7','#76a4ce','#59a14f','#af7aa1','#e99b36']
    axes[0].bar(labels, [r['payload_bytes'] for r in selected], color=colors)
    axes[0].set_ylabel('Representation bytes (seed and header included)')
    axes[0].set_title('All methods also require 170,090 common bytes')
    axes[1].bar(labels, [r['query_plus_preparation_us'] for r in selected], color=colors)
    axes[1].set_yscale('log')
    axes[1].set_ylabel('Query + candidate validation (μs, log scale)')
    axes[1].set_title('Two-singleton negative queries; prototype timings')
    for ax in axes:
        ax.tick_params(axis='x', labelsize=8)
        ax.grid(axis='y', alpha=.2)
        ax.set_axisbelow(True)
    fig.suptitle('Manifest workload: 1,840 rows, 32 candidate sets, 64 constructions')
    fig.savefig(HERE/'comparison.png', dpi=170)
    fig.savefig(HERE/'comparison.pdf')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
