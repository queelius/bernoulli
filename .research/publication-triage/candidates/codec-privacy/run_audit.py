"""Reproduce decisive codec findings; no package or manuscript mutations."""

import json
import pickle
import platform
import random
import runpy
import sys
from collections import Counter
from fractions import Fraction as F  # noqa: N817 - conventional exact-arithmetic notation
from hashlib import sha256
from itertools import product
from pathlib import Path

from bernoulli.maps.codec import PrefixCodec
from bernoulli.maps.retrieval import EncodedRetrieval, GF2Retrieval
from exact_audit import binary_span, coincidence_accuracy, diagonal_bayes_accuracy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
COMPANION = ROOT.parent / "trapdoor-computing/papers/codec-controlled-retrieval"


def main() -> None:
    experiment = runpy.run_path(str(ROOT / "bernoulli-py/experiments/13_codec_optimality.py"))
    p = (F(9, 10),) + (F(1, 70),) * 7
    freqs = dict(enumerate(p))
    codecs = {
        "huffman": PrefixCodec.from_frequencies(freqs, m_bits=6),
        "tail_six_bits": PrefixCodec(
            [(0, 1)] + [(v, 6) for v in range(1, 8)], default_value=0, m_bits=6
        ),
    }
    items = {
        f"member-{value}-{index}".encode(): value
        for value, count in enumerate((630,) + (10,) * 7)
        for index in range(count)
    }
    storage = {}
    for label, codec in codecs.items():
        retrieval = EncodedRetrieval(items, codec, seed=2026)
        assert all(retrieval.query(key) == value for key, value in items.items())
        lengths = tuple(codec.codeword_length(value) for value in range(8))
        original_metrics = experiment["assignment_metrics"](lengths, tuple(map(float, p)))
        raw_counts = Counter(codec.decode(raw) for raw in range(64))
        q = tuple(F(raw_counts[v], 64) for v in range(8))
        length = sum(p[v] * lengths[v] for v in range(8))
        tv = sum(abs(p[v] - q[v]) for v in range(8)) / 2
        assert abs(original_metrics.L - float(length)) < 1e-12
        assert abs(original_metrics.TV - float(tv)) < 1e-12
        storage[label] = {
            "codeword_lengths": lengths,
            "expected_prefix_length": str(length),
            "tv_under_uniform_raw_channel": str(tv),
            "q": list(map(str, q)),
            "slot_width_bits": codec.m_bits,
            "slots": len(retrieval._retrieval._z),
            "packed_payload_bytes_estimate": retrieval.memory_bytes(),
            "pickle_protocol_5_bytes_including_codec": len(pickle.dumps(retrieval, protocol=5)),
            "member_correct_count": len(items),
        }
    assert (
        storage["huffman"]["packed_payload_bytes_estimate"]
        == storage["tail_six_bits"]["packed_payload_bytes_estimate"]
    )

    # Exact row alias in the actual frozen implementation. The key is selected
    # after observing the public construction seed: this is not an estimate of
    # average error for a pre-selected, seed-independent query.
    retrieval = GF2Retrieval({b"stored": 5}, value_bits=3, seed=2026)
    target = retrieval._positions(b"stored", retrieval._seg, retrieval._seed_used)
    alias = next(
        f"absent-{i}".encode()
        for i in range(100000)
        if retrieval._positions(f"absent-{i}".encode(), retrieval._seg, retrieval._seed_used)
        == target
    )
    assert retrieval.query(alias) == 5

    # A fresh-response simulator and a real stored retrieval implement different
    # repeated-query experiments even when one-query marginal predictions agree.
    sim = runpy.run_path(str(ROOT / "bernoulli-py/experiments/14_coincidence_oracle.py"))
    codec = codecs["huffman"]
    simulated = sim["CipherMap"].build(list(items), items, codec, 6)
    rng = random.Random(2026)
    fresh_answers = [simulated.lookup(b"absent", rng) for _ in range(32)]
    frozen = EncodedRetrieval(items, codec, seed=2026)
    frozen_answers = [frozen.query(b"absent") for _ in range(32)]
    assert len(set(frozen_answers)) == 1 < len(set(fresh_answers))

    # Enumerate every subspace of GF(2)^4 and reproduce the balanced-codec
    # threshold. This verifies the finite claim, not its novelty or M1 realism.
    spaces = {frozenset({0})}
    for generator in range(16):
        spaces |= {binary_span(tuple(space) + (generator,)) for space in tuple(spaces)}
    assert len(spaces) == 67
    checked = 0
    for space, code_bits in product(spaces, range(1, 5)):
        counts = Counter(value >> (4 - code_bits) for value in space)
        image_size = len(counts)
        assert all(F(count, len(space)) == F(1, image_size) for count in counts.values())
        full_control = all(
            F(counts[v], len(space)) == F(1, 1 << code_bits) for v in range(1 << code_bits)
        )
        assert full_control == (image_size == 1 << code_bits)
        checked += 1

    sparse = PrefixCodec([("a", 1), ("b", 3)], default_value="a", m_bits=3)
    fingerprint_paths = [
        ROOT / "bernoulli-py/src/bernoulli/maps/codec.py",
        ROOT / "bernoulli-py/src/bernoulli/maps/retrieval.py",
        ROOT / "bernoulli-py/experiments/13_codec_optimality.py",
        ROOT / "bernoulli-py/experiments/14_coincidence_oracle.py",
        ROOT / "bernoulli-py/experiments/15_randomized_encoding.py",
        COMPANION / "paper/codec_retrieval.tex",
    ]
    results = {
        "python": sys.version,
        "platform": platform.platform(),
        "seed": 2026,
        "input_sha256": {
            str(path): sha256(path.read_bytes()).hexdigest() for path in fingerprint_paths
        },
        "storage_comparison": storage,
        "coincidence_counterexample": {
            "p": ["99/100", "1/100"],
            "q": ["1/2", "1/2"],
            "releases": 2,
            "coincidence_accuracy": str(coincidence_accuracy((F(1, 2), F(1, 2)), 2, F(1, 2))),
            "bayes_accuracy": str(
                diagonal_bayes_accuracy((F(99, 100), F(1, 100)), (F(1, 2), F(1, 2)), 2, F(1, 2))
            ),
        },
        "actual_stored_row_alias": {
            "member": "stored",
            "nonmember": alias.decode(),
            "positions": target,
            "seed": retrieval._seed_used,
            "output": retrieval.query(alias),
            "predicted_uniform_probability_of_output": "1/8",
            "scope": "deterministic conditional on this seed; adaptively selected alias",
        },
        "repeated_same_query": {"simulated_fresh": fresh_answers, "actual_frozen": frozen_answers},
        "default_decode_fiber": [raw for raw in range(8) if sparse.decode(raw) == "a"],
        "default_random_encoding_support": [
            sparse.encode_random("a", suffix) for suffix in range(4)
        ],
        "threshold_enumeration": {
            "subspaces": len(spaces),
            "projection_cases": checked,
            "assumption": "uniform on stored span (M1)",
        },
        "marginal_transcript_counterexample": {
            "profile_0": {"00": "1/2", "11": "1/2"},
            "profile_1": {"01": "1/2", "10": "1/2"},
            "each_one_query_marginal": ["1/2", "1/2"],
            "two_query_bayes_accuracy": "1",
            "distinguishing_advantage": "1",
            "scope": "logical countermodel to deriving joint privacy from marginal M1 alone",
        },
    }
    (HERE / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(
        json.dumps(
            {
                key: value
                for key, value in results.items()
                if key not in {"input_sha256", "repeated_same_query"}
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
