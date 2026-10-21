#!/usr/bin/env python3
"""Restricted functional-row join opportunity test, with full cost accounting.

Run from the repository root: bernoulli-py/.venv/bin/python
.research/query-contract-planner/code/experiment.py --builds 40
"""
from __future__ import annotations

import argparse
from bisect import bisect_left
from collections import defaultdict
from dataclasses import dataclass, replace
from enum import StrEnum
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import random
import statistics
import struct
import subprocess
import sys
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'papers/bernoulli_relations/code'))
from filter_calibration import FrozenBloom  # noqa: E402
from contracts import Budget, error_bound, plan_rate, profile_probability  # noqa: E402
from finite_rows import FrozenRows, collision_rate, select_width  # noqa: E402
from fuse_baseline import FrozenFuse, compile_bridge  # noqa: E402
from value_store import FrozenValues, ValueMode  # noqa: E402


@dataclass(frozen=True)
class Query:
    left: int
    right: int
    profile: str
    repeats: int = 3
    candidates: tuple[int, ...] | None = None


@dataclass(frozen=True, slots=True)
class CandidateSet:
    """Validated query input. Validation cost is recorded separately from probes."""
    values: tuple[int, ...]
    domain_size: int

    def __post_init__(self):
        if self.domain_size < 1 or any(type(v) is not int or not 0 <= v < self.domain_size for v in self.values):
            raise ValueError('candidate outside declared integer domain')
        object.__setattr__(self, 'values', tuple(sorted(set(self.values))))

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __getitem__(self, index):
        return self.values[index]


@dataclass(frozen=True)
class Workload:
    name: str
    keys: tuple[bytes, ...]
    values: tuple[int, ...]
    catalog: tuple[bytes, ...]
    candidates: tuple[int, ...]
    queries: tuple[Query, ...]
    extraction_seconds: float
    provenance: dict

    @property
    def capacity(self):
        return max(len(CandidateSet(q.candidates if q.candidates is not None else self.candidates,
                                    len(self.catalog))) for q in self.queries)

    @property
    def common_payload(self):
        # Actual decodable length-prefixed keys/catalog, plus typed schema.
        schema = json.dumps({'version': 1, 'key': ['snapshot', 'path'],
                             'functional': True, 'total': True,
                             'rows': len(self.keys), 'domain': len(self.catalog)},
                            sort_keys=True, separators=(',', ':')).encode()
        parts = [struct.pack('>I', len(schema)), schema]
        for sequence in (self.keys, self.catalog):
            parts.append(struct.pack('>I', len(sequence)))
            for item in sequence:
                parts.extend((struct.pack('>I', len(item)), item))
        parts.append(struct.pack('>I', len(self.candidates)))
        parts.extend(struct.pack('>I', value) for value in self.candidates)
        return b''.join(parts)


def sample_queries(values, candidates, per_profile, seed):
    rng = random.Random(seed)
    by_value = defaultdict(list)
    for row, value in enumerate(values):
        by_value[value].append(row)
    inside = sorted(set(candidates) & by_value.keys())
    outside = sorted(by_value.keys() - set(candidates))
    queries = []
    for profile in ('two_single', 'one_single', 'zero_single', 'same_outside', 'true'):
        for _ in range(per_profile):
            if profile == 'two_single':
                a, b = rng.sample(inside, 2)
            elif profile == 'one_single':
                a, b = rng.choice(inside), rng.choice(outside)
            elif profile == 'zero_single':
                a, b = rng.sample(outside, 2)
            else:
                pool = inside if profile == 'true' else outside
                a = b = rng.choice([v for v in pool if len(by_value[v]) >= 2])
            if a == b:
                left, right = rng.sample(by_value[a], 2)
            else:
                left, right = rng.choice(by_value[a]), rng.choice(by_value[b])
            queries.append(Query(left, right, profile))
    return tuple(queries)


def make_synthetic(domain=128, rows=1024, candidates=64, per_profile=64, seed=1):
    start = time.perf_counter()
    if not 2 <= candidates <= domain - 2 or rows < 2 * domain or per_profile < 1:
        raise ValueError('need >=2 inside/outside values and >=2 rows per value')
    keys = tuple(f'row/{row:08d}'.encode() for row in range(rows))
    values = tuple(row % domain for row in range(rows))
    catalog = tuple(struct.pack('>Q', value) for value in range(domain))
    chosen = tuple(range(candidates))
    queries = sample_queries(values, chosen, per_profile, seed)
    return Workload(f'synthetic-d{domain}-k{candidates}', keys, values, catalog, chosen,
                    queries, time.perf_counter() - start, {'type': 'controlled', 'seed': seed})


def make_manifest(refs, per_profile=64, seed=2):
    start = time.perf_counter()
    rows = []
    commits = []
    for ref in refs:
        commit = subprocess.check_output(['git', 'rev-parse', ref], cwd=ROOT).strip()
        commits.append(commit.decode())
        raw = subprocess.check_output([
            'git', 'ls-tree', '-rz', '--full-tree',
            '--format=%(objecttype)%x00%(objectname)%x00%(path)', commit.decode()], cwd=ROOT)
        fields = raw.split(b'\0')[:-1]
        if len(fields) % 3:
            raise ValueError('malformed NUL-delimited git tree')
        for index in range(0, len(fields), 3):
            kind, oid, path = fields[index:index + 3]
            if kind == b'blob':
                rows.append((bytes.fromhex(commit.decode()) + b'/' + path, bytes.fromhex(oid.decode()), path))
    rows.sort()
    catalog = tuple(sorted({oid for _, oid, _ in rows}))
    codes = {oid: index for index, oid in enumerate(catalog)}
    keys = tuple(key for key, _, _ in rows)
    values = tuple(codes[oid] for _, oid, _ in rows)
    candidates = tuple(sorted({codes[oid] for _, oid, path in rows if path.endswith(b'.tex')}))
    queries = sample_queries(values, candidates, per_profile, seed)
    return Workload('git-manifest-tex-catalog', keys, values, catalog, candidates, queries,
                    time.perf_counter() - start,
                    {'type': 'git_manifest', 'commits': commits,
                     'candidate_rule': 'content identifiers of tracked .tex blobs in either snapshot',
                     'documentation': 'https://git-scm.com/docs/git-ls-tree'})


def vary_candidates(workload, size, seed):
    """Fresh query catalog parameters, without storing per-row catalog flags."""
    if not 2 <= size < len(workload.candidates):
        raise ValueError('varying catalog must be a proper subset with >=2 values')
    start = time.perf_counter()
    rng = random.Random(seed)
    repetitions = sum(q.profile == 'true' for q in workload.queries)
    queries = []
    for _ in range(repetitions):
        chosen = tuple(sorted(rng.sample(workload.candidates, size)))
        for query in sample_queries(workload.values, chosen, 1, rng.getrandbits(64)):
            queries.append(replace(query, candidates=chosen))
    return replace(workload, name=f'{workload.name}-varying-k{size}', queries=tuple(queries),
                   extraction_seconds=workload.extraction_seconds + time.perf_counter() - start,
                   provenance={**workload.provenance, 'candidate_parameters': 'independently seeded subsets of public candidate pool',
                               'candidate_seed': seed, 'candidate_capacity': size,
                               'query_class': 'any subset up to capacity, independent of construction seed; not only sampled catalogs'})


def validate_workload(workload):
    if len(set(workload.keys)) != len(workload.keys) or tuple(sorted(workload.keys)) != workload.keys:
        raise ValueError('row keys must be unique and sorted')
    if len(workload.values) != len(workload.keys):
        raise ValueError('functional total schema violated')
    if any(not 0 <= value < len(workload.catalog) for value in workload.values):
        raise ValueError('foreign-key domain violated')
    if tuple(sorted(set(workload.candidates))) != workload.candidates:
        raise ValueError('candidate domain must be canonical')
    CandidateSet(workload.candidates, len(workload.catalog))
    for query in workload.queries:
        candidates = CandidateSet(query.candidates if query.candidates is not None else workload.candidates, len(workload.catalog))
        if query.left == query.right:
            raise ValueError('constrained distinct-row contract cannot serve this self-join')
        a, b = workload.values[query.left], workload.values[query.right]
        exact = a == b and a in candidates
        if exact != (query.profile == 'true'):
            raise ValueError('profile does not match exact query answer')


class Family(StrEnum):
    BLOOM = 'bloom'
    ROWS = 'rows'
    FUSE = 'fuse'
    EXACT = 'exact'


@dataclass(frozen=True)
class Method:
    name: str
    family: Family
    budget: Budget | None
    source_rate: Fraction
    width: int
    contract_kind: str
    max_candidates: int = 0
    domain_size: int = 0


def methods_for(k, target, domain_size):
    if not 1 <= k <= domain_size or not 0 < target < 1:
        raise ValueError('candidate capacity must fit declared domain; target must be in (0,1)')
    methods = []
    for budget in Budget:
        rate = plan_rate(budget, k, target)
        if rate > 0:
            methods.append(Method(f'bloom_{budget.value}', Family.BLOOM, budget,
                                  rate, 0, 'conditional_ideal'))
    for budget in (Budget.ORDINARY_UNION, Budget.CONSTRAINED_UNION):
        try:
            width = select_width(k, target, budget)
        except ValueError:
            # Valid target/capacity checked above: this family lacks a width.
            continue
        methods.append(Method(f'finite_rows_{budget.value}', Family.ROWS, budget,
                              collision_rate(width), width, 'finite_unconditional'))
    for name, budget in (('ordinary', Budget.ORDINARY_UNION), ('constrained', Budget.CONSTRAINED_UNION)):
        for width in (8, 16):
            p = Fraction(1, 2**width)
            if error_bound(budget, k, p) <= target:
                methods.append(Method(f'fuse_{name}', Family.FUSE, budget, p, width, 'nominal_hash_model'))
                break
    methods.append(Method('exact_values', Family.EXACT, None, Fraction(0), 0, 'exact'))
    return tuple(replace(method, max_candidates=k, domain_size=domain_size) for method in methods)


def tuple_key(row, value, domain):
    return struct.pack('>Q', row * domain + value)


def build_representation(method, workload, seed, target):
    domain, k = len(workload.catalog), method.max_candidates
    if domain != method.domain_size:
        raise ValueError('construction domain does not match plan')
    rng = random.Random(seed)
    attempts = 1
    if method.family is Family.BLOOM:
        keys = [tuple_key(row, value, domain) for row, value in enumerate(workload.values)]
        while True:
            bloom = FrozenBloom.build(keys, float(method.source_rate), rng.getrandbits(128).to_bytes(16, 'big'))
            p = Fraction(1)
            for occupancy in bloom.occupancies:
                p *= Fraction(occupancy, bloom.partition_bits)
            bound = error_bound(method.budget, k, p)
            if bound <= target:
                break
            attempts += 1
            if attempts > 10000:
                raise RuntimeError('construction acceptance did not terminate')
        payload = bloom.serialize()
        restored = FrozenBloom.deserialize(payload)
        assert all(restored.contains(key) for key in keys)
        return restored, payload, p, bound, attempts
    if method.family is Family.ROWS:
        store = FrozenRows.build(workload.values, domain, method.width, seed)
        payload = store.serialize()
        restored = FrozenRows.deserialize(payload)
        assert all(restored.contains(row, value) for row, value in enumerate(workload.values))
        return restored, payload, method.source_rate, error_bound(method.budget, k, method.source_rate), attempts
    if method.family is Family.FUSE:
        store = FrozenFuse.build([row * domain + value for row, value in enumerate(workload.values)], bits=method.width, seed=seed)
        payload = store.serialize()
        return FrozenFuse.deserialize(payload), payload, method.source_rate, error_bound(method.budget, k, method.source_rate), attempts
    if method.family is Family.EXACT:
        store = FrozenValues.build(workload.values, domain, ValueMode.EXACT, 1, seed)
        payload = store.serialize()
        return FrozenValues.deserialize(payload), payload, Fraction(0), Fraction(0), attempts
    raise ValueError('unknown representation')


def execute(method, store, keys, domain, candidates, left_key, right_key):
    # Resolve public keys within timed query; no access to exact values.
    if not isinstance(candidates, CandidateSet):
        candidates = CandidateSet(tuple(candidates), domain)
    if candidates.domain_size != domain or domain != method.domain_size:
        raise ValueError('candidate domain does not match the tuple encoding')
    if len(candidates) > method.max_candidates:
        raise ValueError('query exceeds certified candidate capacity')
    left, right = bisect_left(keys, left_key), bisect_left(keys, right_key)
    if left >= len(keys) or right >= len(keys) or keys[left] != left_key or keys[right] != right_key:
        raise KeyError('unknown exact row key')
    if left == right:
        raise ValueError('this contract requires distinct canonical rows')
    if method.family is Family.EXACT:
        a, b = store.value(left), store.value(right)
        index = bisect_left(candidates, a)
        return a == b and index < len(candidates) and candidates[index] == a, 0
    probes = 0
    for value in candidates:
        probes += 1
        if method.family is Family.BLOOM:
            a = store.contains(tuple_key(left, value, domain))
        elif method.family is Family.ROWS:
            a = store.contains(left, value)
        else:
            a = store.contains(left * domain + value)
        if not a:
            continue
        probes += 1
        if method.family is Family.BLOOM:
            b = store.contains(tuple_key(right, value, domain))
        elif method.family is Family.ROWS:
            b = store.contains(right, value)
        else:
            b = store.contains(right * domain + value)
        if b:
            return True, probes
    return False, probes


def interval(values):
    """Diagnostic SE band plus a valid bounded-mean Chernoff interval.

    For independent construction means Xi in [0,1] with common mean mu,
    Chernoff's bounded-variable mgf gives exp(-n*kl(xbar,mu)) per tail.
    Invert with alpha/2=.025. No within-build query independence is used.
    """
    if not values or any(not 0 <= value <= 1 for value in values):
        raise ValueError('nonempty bounded construction means required')
    mean = statistics.mean(values)
    se = statistics.stdev(values) / len(values)**0.5 if len(values) > 1 else 0.0
    threshold = math.log(40) / len(values)

    def divergence(p):
        if p == 0:
            return 0.0 if mean == 0 else math.inf
        if p == 1:
            return 0.0 if mean == 1 else math.inf
        return ((mean * math.log(mean / p) if mean else 0.0)
                + ((1 - mean) * math.log((1 - mean) / (1 - p)) if mean < 1 else 0.0))

    low, high = 0.0, mean
    for _ in range(60):
        middle = (low + high) / 2
        if divergence(middle) > threshold:
            low = middle
        else:
            high = middle
    lower = low
    low, high = mean, 1.0
    for _ in range(60):
        middle = (low + high) / 2
        if divergence(middle) > threshold:
            high = middle
        else:
            low = middle
    return {'mean': mean, 'se': se,
            'normal_diagnostic_band': {'lo': max(0, mean - 1.96 * se), 'hi': min(1, mean + 1.96 * se)},
            'bounded_mean_95': {'lo': lower, 'hi': high}}


def run_case(workload, builds, seed, output):
    if builds < 2:
        raise ValueError('need >=2 builds for construction-level uncertainty')
    validate_workload(workload)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'common.bin').write_bytes(workload.common_payload)
    target = Fraction(1, 20)
    k, domain = workload.capacity, len(workload.catalog)
    start = time.perf_counter()
    methods = methods_for(k, target, domain)
    planning_seconds = time.perf_counter() - start
    start = time.perf_counter()
    prepared = tuple((q, CandidateSet(q.candidates if q.candidates is not None else workload.candidates, domain))
                     for q in workload.queries)
    preparation_seconds = time.perf_counter() - start
    query_input_bytes = sum(16 + len(workload.keys[q.left]) + len(workload.keys[q.right]) + 4 * len(c)
                            for q, c in prepared)
    compile_bridge()
    build_rows, query_rows = [], []
    generator = random.Random(seed)
    profiles = sorted({query.profile for query in workload.queries})
    by_profile = {profile: tuple((q,c) for q,c in prepared if q.profile == profile) for profile in profiles}
    for build in range(builds):
        offset = build % len(methods)
        for method in methods[offset:] + methods[:offset]:
            construction_seed = generator.getrandbits(64)
            start = time.perf_counter()
            store, payload, p, bound, attempts = build_representation(method, workload, construction_seed, target)
            build_seconds = time.perf_counter() - start
            if build == 0:
                (output / f'{method.name}.bin').write_bytes(payload)
            build_rows.append({
                'build': build, 'method': method.name, 'seed': construction_seed,
                'representation_bytes': len(payload), 'common_bytes': len(workload.common_payload),
                'total_bytes': len(payload) + len(workload.common_payload),
                'width': method.width, 'construction_seconds': build_seconds,
                'attempts': attempts, 'source_rate': float(p),
                'certified_bound': None if method.family is Family.FUSE else float(bound),
                'reported_bound': float(bound), 'contract_kind': method.contract_kind,
                'payload_sha256': hashlib.sha256(payload).hexdigest()})
            for profile, queries in by_profile.items():
                start = time.perf_counter()
                observed = [execute(method, store, workload.keys, domain, candidates,
                                    workload.keys[q.left], workload.keys[q.right]) for q,candidates in queries]
                query_seconds = time.perf_counter() - start
                repeated = [execute(method, store, workload.keys, domain, candidates,
                                    workload.keys[q.left], workload.keys[q.right])[0] for q,candidates in queries]
                exact = profile == 'true'
                positives = sum(answer for answer, _ in observed)
                singles = 2 if profile == 'two_single' else 1 if profile == 'one_single' else 0
                if exact:
                    model = 1.0
                else:
                    by_size = {size: float(profile_probability(size, singles, p)) for size in {len(c) for _,c in queries}}
                    model = statistics.mean(by_size[len(c)] for _,c in queries)
                query_rows.append({
                    'build': build, 'method': method.name, 'profile': profile,
                    'queries': len(queries), 'positives': positives,
                    'fp': 0 if exact else positives, 'fn': len(queries) - positives if exact else 0,
                    'query_seconds': query_seconds, 'probes': sum(n for _, n in observed),
                    'repeat_mismatches': sum(a != b for (a, _), b in zip(observed, repeated, strict=True)),
                    'independent_lineage_reference': model,
                    'reference_is_identity': method.family in (Family.BLOOM, Family.EXACT)})
    summary = []
    for method in methods:
        records = [row for row in build_rows if row['method'] == method.name]
        for profile in profiles:
            records_q = [row for row in query_rows if row['method'] == method.name and row['profile'] == profile]
            estimate = interval([row['positives'] / row['queries'] for row in records_q])
            summary.append({
                'method': method.name, 'profile': profile, 'positive_interval': estimate,
                'fp': sum(row['fp'] for row in records_q), 'fn': sum(row['fn'] for row in records_q),
                'repeat_mismatches': sum(row['repeat_mismatches'] for row in records_q),
                'mean_query_us': statistics.mean(1e6 * row['query_seconds'] / row['queries'] for row in records_q),
                'mean_query_us_including_preparation': statistics.mean(1e6 * row['query_seconds'] / row['queries'] for row in records_q)
                    + 1e6 * preparation_seconds / len(prepared),
                'mean_probes': statistics.mean(row['probes'] / row['queries'] for row in records_q),
                'mean_build_ms': 1000 * statistics.mean(row['construction_seconds'] for row in records),
                'representation_bytes': records[0]['representation_bytes'], 'total_bytes': records[0]['total_bytes'],
                'max_reported_bound': max(row['reported_bound'] for row in records),
                'contract_kind': method.contract_kind,
                'mean_lineage_reference': statistics.mean(row['independent_lineage_reference'] for row in records_q),
                'reference_is_identity': records_q[0]['reference_is_identity']})
    # Separate memory pass avoids contaminating construction/query timing.
    memory = []
    for method in methods:
        tracemalloc.start()
        store = build_representation(method, workload, seed + 88, target)[0]
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory.append({'method': method.name, 'python_retained_bytes': current, 'python_peak_bytes': peak,
                       'scope': 'tracemalloc excludes native C allocations and preexisting workload/directory'})
    start = time.perf_counter()
    count = sum(sum(1 for _ in candidates) for _,candidates in prepared)
    candidate_seconds = time.perf_counter() - start
    result = {
        'workload': {'name': workload.name, 'rows': len(workload.keys), 'domain_size': domain,
                     'candidate_count': k, 'query_count': len(workload.queries),
                     'candidate_pool_count': len(workload.candidates),
                     'distinct_candidate_sets': len({c.values for _,c in prepared}),
                     'query_input_bytes_total': query_input_bytes,
                     'candidate_validation_seconds': preparation_seconds,
                     'common_bytes': len(workload.common_payload), 'provenance': workload.provenance,
                     'extraction_seconds': workload.extraction_seconds,
                     'planning_seconds': planning_seconds,
                     'candidate_enumeration_control_seconds': candidate_seconds,
                     'candidate_enumeration_control_count': count},
        'config': {'builds': builds, 'seed': seed, 'query_target': str(target)},
        'methods': [{'name': method.name, 'width': method.width, 'rate': str(method.source_rate),
                     'contract_kind': method.contract_kind} for method in methods],
        'builds': build_rows, 'queries': query_rows, 'summary': summary, 'memory': memory,
        'caveats': [
            'Finite_rows: proved only for uniform independent coefficients, fixed data/query, unconditional construction.',
            'Bloom: exact rational acceptance certifies conditional ideal random-function contract, not BLAKE2 independence.',
            'Fuse: nominal 2^-b collision model is a baseline assumption, not a finite-family guarantee.',
            'Lineage reference is an identity only in Bloom ideal conditional model or exact storage; not for four-wise rows/fuse.',
            'Bounded-mean 95% Chernoff intervals assume independent construction means; normal SE bands are diagnostics only. No within-build query independence.',
            'Query costs include directory lookup and candidate enumeration. Python/ctypes overhead limits throughput comparison.',
            'Packed serialized bytes include seed/headers and common key directory/catalog/schema/candidate catalog; Python object memory is separate.',
        ],
        'sources': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in Path(__file__).parent.glob('*.py')}
    }
    (output / 'input.json').write_text(json.dumps({
        'keys_hex': [key.hex() for key in workload.keys], 'catalog_hex': [value.hex() for value in workload.catalog],
        'construction_values': workload.values, 'candidate_pool': workload.candidates,
        'queries': [{'left': q.left, 'right': q.right, 'profile': q.profile, 'repeats': q.repeats,
                     'candidates': c.values} for q,c in prepared],
        'scope': 'Reproduction inputs. Exact construction_values are never passed to execute and are not part of approximate storage.'
    }, indent=2) + '\n')
    (output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--builds', type=int, default=40)
    parser.add_argument('--per-profile', type=int, default=64)
    parser.add_argument('--manifest-only', action='store_true')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'data')
    args = parser.parse_args()
    workloads = [make_manifest(('9d38e038d243c3d0f024050d873cda167b6aba77', '61c4a4319ea3e93aae02e0e6b4b54fc3b054e3c7'), args.per_profile)]
    if not args.manifest_only:
        for domain, candidates in ((32, 8), (128, 64), (1024, 512)):
            workloads.append(make_synthetic(domain, 2 * domain + 256, candidates, args.per_profile, domain))
    workloads = [vary_candidates(workload, min(64, len(workload.candidates)//2), 903 + i) for i,workload in enumerate(workloads)]
    for index, workload in enumerate(workloads):
        result = run_case(workload, args.builds, 20261013 + index, args.output / workload.name)
        print(workload.name, result['workload'], flush=True)
        for row in result['summary']:
            if row['profile'] == 'two_single':
                print(row['method'], row['representation_bytes'], row['total_bytes'],
                      round(row['mean_query_us'], 2), row['positive_interval'], flush=True)


if __name__ == '__main__':
    main()
