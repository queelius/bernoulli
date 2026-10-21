"""Adversarial release checks for the round-2 extracted supplement."""

import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import py_compile
import random
import subprocess
import sys
import tempfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ast_hashes(path, omit_empty_type_params=False):
    nodes = ast.parse(path.read_text()).body
    if omit_empty_type_params:
        for node in nodes:
            if isinstance(node, ast.FunctionDef) and not node.type_params:
                node._fields = tuple(name for name in node._fields if name != 'type_params')
    return {node.name: hashlib.sha256(ast.dump(node, include_attributes=False).encode()).hexdigest()
            for node in nodes if isinstance(node, ast.FunctionDef)
            and node.name in ("exact_gbf_checks", "stored_constructions")}


def parity(words, bits):
    return sum((sum((word >> bit) & 1 for word in words) % 2) << bit
               for bit in range(bits))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    artifact = args.artifact.resolve()
    root = Path('/home/spinoza/github/bernoulli')
    old = Path('/tmp/gbfplus-methods-review-osxxcyi4/supplement')
    provenance = json.loads((artifact / 'provenance.json').read_text())
    result = {"python": sys.version, "artifact": str(artifact)}
    result['files_sha256'] = {name: digest(artifact / name) for name in
        ('reproduce.py', 'gbfplus_probe.py', 'test_reproduction.py', 'test_gbfplus_probe.py',
         'README.md', 'provenance.json', 'reference-results.json')}
    current_ast = ast_hashes(artifact / 'reproduce.py')
    prior_ast = ast_hashes(old / 'reproduce.py')
    original = root / '.research/bounded-discovery' / provenance['original_driver']
    original_ast = ast_hashes(original)
    result['provenance_checks'] = {
        'experiment_ast_hashes': current_ast,
        'equal_to_round_1': current_ast == prior_ast,
        'equal_to_original_driver': current_ast == original_ast,
        'equal_to_recorded_hashes': current_ast == provenance['unchanged_functions'],
        'matches_recorded_without_python312_empty_type_params':
            ast_hashes(artifact / 'reproduce.py', omit_empty_type_params=True)
            == provenance['unchanged_functions'],
        'original_driver_hash_matches': digest(original) == provenance['original_driver_sha256'],
        'unchanged_files_match': all(digest(artifact / name) == value
             for name, value in provenance['unchanged_files'].items()),
    }
    assert all(value for key, value in result['provenance_checks'].items()
               if key not in ('experiment_ast_hashes', 'equal_to_recorded_hashes'))

    fresh = json.loads((artifact / 'reproduced-results.json').read_text())
    reference = json.loads((artifact / 'reference-results.json').read_text())
    stored = dict(fresh['gbfplus_stored'])
    saved = dict(reference['gbfplus_stored'])
    stored.pop('repeated_scan_ns_mean')
    saved.pop('repeated_scan_ns_mean')
    assert stored == saved
    assert fresh['gbfplus_exact'] == reference['gbfplus_exact']
    for name, value in fresh['source_sha256'].items():
        assert digest(artifact / name) == value
    for row in stored['instances']:
        rng = random.Random(row['seed'])
        positions = rng.sample(range(64), 12)
        domain = rng.getrandbits(20)
        target = (rng.getrandbits(12) << 20) | domain
        free = [rng.getrandbits(32) for _ in range(11)]
        expected = [None] * 64
        for position, value in zip(positions[1:], free, strict=True):
            expected[position] = value
        expected[positions[0]] = parity([target, *free], 32)
        assert expected == row['cells']
        assert positions == row['positions']
        assert domain == row['domain'] == row['recovered_domain']
        assert parity([word for word in row['cells'] if word is not None], 32) == target
    result['normal_results'] = {'deterministic_fields_match': True,
        'source_hashes_match': True, 'arrays_reconstructed': len(stored['instances']),
        'exact': fresh['gbfplus_exact']}

    cases = []
    options = [('flag_O', ['-O'], None), ('flag_OO', ['-OO'], None),
               ('environment_1', [], '1'), ('environment_2', [], '2')]
    actions = {
        'script': [str(artifact / 'reproduce.py')],
        'module': ['-m', 'reproduce'],
        'import_result_function': ['-c', 'from reproduce import reproduce; print(reproduce())'],
        'import_experiment_function': ['-c', 'from reproduce import exact_gbf_checks; print(exact_gbf_checks())'],
        'runpy': ['-c', "import runpy; runpy.run_path(" + repr(str(artifact / 'reproduce.py')) + ", run_name='__main__')"],
    }
    for name, flags, optimization in options:
        for action, suffix in actions.items():
            with tempfile.TemporaryDirectory(prefix='gbfplus-r2-guard-') as cwd:
                env = dict(os.environ)
                env.pop('PYTHONOPTIMIZE', None)
                env['PYTHONPATH'] = str(artifact)
                if optimization is not None:
                    env['PYTHONOPTIMIZE'] = optimization
                cmd = [sys.executable, '-S', *flags, *suffix]
                run = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
                created = (Path(cwd) / 'reproduced-results.json').exists()
                assert run.returncode != 0
                assert 'requires assertions' in run.stderr
                assert not created
                cases.append({'mode': name, 'entry': action, 'command': cmd,
                    'exit_code': run.returncode, 'diagnostic': run.stderr.splitlines()[-1],
                    'output_json_created': created})
    result['optimization_rejections'] = cases

    with tempfile.TemporaryDirectory(prefix='gbfplus-r2-sentinel-') as cwd:
        path = Path(cwd) / 'reproduced-results.json'
        path.write_text('existing-results-sentinel\n')
        run = subprocess.run([sys.executable, '-O', '-S', str(artifact / 'reproduce.py')],
            cwd=cwd, capture_output=True, text=True)
        assert run.returncode != 0
        assert path.read_text() == 'existing-results-sentinel\n'
        result['optimized_existing_output_untouched'] = True

    # Additional edge case outside the published source invocation: a caller can
    # explicitly compile an optimized code object in an unoptimized interpreter.
    compiled = artifact / 'review_optimized.pyc'
    py_compile.compile(str(artifact / 'reproduce.py'), cfile=str(compiled), optimize=1, doraise=True)
    with tempfile.TemporaryDirectory(prefix='gbfplus-r2-bytecode-') as cwd:
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        run = subprocess.run([sys.executable, '-S', str(compiled)], cwd=cwd,
            env=env, capture_output=True, text=True)
        out = Path(cwd) / 'reproduced-results.json'
        record = {'exit_code': run.returncode, 'output_json_created': out.exists()}
        if out.exists():
            data = json.loads(out.read_text())
            record['empty_stored_arrays'] = sum(all(word is None for word in row['cells'])
                for row in data['gbfplus_stored']['instances'])
            record['singleton_errors'] = data['gbfplus_exact']['singleton_errors']
        result['externally_precompiled_optimized_bytecode_edge_case'] = record
    compiled.unlink()

    # Independently challenge the new oracle using an in-memory prefix-only fault.
    sys.path.insert(0, str(artifact))
    spec = importlib.util.spec_from_file_location('review_artifact_tests', artifact / 'test_reproduction.py')
    tests = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tests)
    tests.test_full_stored_array_includes_prefix_and_preserves_occupied_zero()
    original_insert = tests.insert
    def prefix_fault(cells, positions, target, random_words, word_bits):
        empty = [position for position in positions if cells[position] is None]
        success = original_insert(cells, positions, target, random_words, word_bits)
        if success:
            cells[empty[0]] ^= 1 << (word_bits - 1)
        return success
    tests.insert = prefix_fault
    try:
        tests.test_full_stored_array_includes_prefix_and_preserves_occupied_zero()
    except AssertionError:
        result['new_full_array_oracle_rejects_prefix_only_corruption'] = True
    else:
        raise AssertionError('new full-array oracle failed to detect prefix corruption')
    finally:
        tests.insert = original_insert
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key != 'optimization_rejections'}, indent=2))
    print('Optimization entry-point rejection cases:', len(cases))


if __name__ == '__main__':
    main()
