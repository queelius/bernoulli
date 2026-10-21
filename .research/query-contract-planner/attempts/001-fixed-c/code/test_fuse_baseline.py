"""Behavioral tests for the stored FastFilter baseline; run with pytest."""

from pathlib import Path
import base64
import hashlib
import json
import struct
import subprocess
import sys

import pytest

from fuse_baseline import FrozenFuse


@pytest.mark.parametrize("bits", [8, 16])
def test_stored_filter_has_no_false_negatives_and_round_trips(bits):
    keys = [0, 1, 2, 2**32, 2**63, 2**64 - 1, *range(100, 3000)]
    original = FrozenFuse.build(keys, bits=bits, seed=987654321)
    assert all(original.contains(key) for key in keys)
    payload = original.serialize()
    loaded = FrozenFuse.deserialize(payload)
    assert loaded.bits == bits
    assert loaded.payload_bytes == len(payload)
    assert loaded.serialize() == payload
    queries = [*keys, *range(10_000, 20_000)]
    expected = [original.contains(key) for key in queries]
    assert [loaded.contains(key) for key in queries] == expected
    assert loaded.contains_many(queries) == expected
    # Detect an always-true stub without asserting chance outcomes for one key.
    assert sum(expected[len(keys):]) < 200


@pytest.mark.parametrize("bits", [8, 16])
def test_identical_keys_and_salt_produce_identical_realizations(bits):
    keys = list(range(1000))
    first = FrozenFuse.build(keys, bits=bits, seed=1)
    repeated = FrozenFuse.build(keys[::-1] + keys[:30], bits=bits, seed=1)
    another = FrozenFuse.build(keys, bits=bits, seed=2)
    assert first.serialize() == repeated.serialize()
    assert first.serialize() != another.serialize()
    queries = list(range(2000, 22_000))
    expected = first.contains_many(queries)
    for _ in range(3):
        assert first.contains_many(queries[::-1])[::-1] == expected
    assert first.serialize() == repeated.serialize()
    assert all(another.contains(key) for key in keys)


@pytest.mark.parametrize("keys", [[], [1], [1, 1]])
def test_too_small_sets_are_rejected_clearly(keys):
    with pytest.raises(ValueError, match="two distinct"):
        FrozenFuse.build(keys)


@pytest.mark.parametrize("bad", [-1, 2**64])
def test_unsigned_key_and_salt_range_is_checked(bad):
    with pytest.raises(ValueError):
        FrozenFuse.build([0, bad])
    with pytest.raises(ValueError):
        FrozenFuse.build([0, 1], seed=bad)
    filter_ = FrozenFuse.build([0, 1])
    with pytest.raises(ValueError):
        filter_.contains(bad)


@pytest.mark.parametrize("bad", [True, 1.0, "1", None])
def test_inputs_are_integers_without_lossy_conversion(bad):
    with pytest.raises(TypeError):
        FrozenFuse.build([0, bad])
    with pytest.raises(TypeError):
        FrozenFuse.build([0, 1], seed=bad)
    filter_ = FrozenFuse.build([0, 1])
    with pytest.raises(TypeError):
        filter_.contains(bad)


@pytest.mark.parametrize("bits", [0, 7, 12, 32, True, 8.0])
def test_only_supported_integer_fingerprint_widths_are_accepted(bits):
    with pytest.raises((TypeError, ValueError)):
        FrozenFuse.build([0, 1], bits=bits)


def test_filter_state_is_immutable():
    filter_ = FrozenFuse.build([1, 2, 3])
    with pytest.raises(AttributeError):
        filter_.bits = 16
    with pytest.raises(AttributeError):
        filter_._payload = b"broken"
    assert filter_.contains_many([]) == []


def test_payload_validates_envelope_length_and_native_geometry():
    payload = FrozenFuse.build(range(1000), seed=123).serialize()
    malformed = [b"", payload[:15], payload[:-1], payload + b"x"]
    for offset, value in [(0, 0), (4, 7), (5, 12), (6, 0), (7, 1)]:
        corrupt = bytearray(payload)
        corrupt[offset] = value
        malformed.append(bytes(corrupt))
    # Native header: seed:u64, count:u32, segment_length:u32,
    # segment_count:u32, segment_count_length:u32, array_length:u32.
    for native_offset, value in [(8, 0), (12, 3), (16, 0), (20, 1), (24, 0)]:
        corrupt = bytearray(payload)
        struct.pack_into("=I", corrupt, 16 + native_offset, value)
        malformed.append(bytes(corrupt))
    for corrupt in malformed:
        with pytest.raises(ValueError):
            FrozenFuse.deserialize(corrupt)
    with pytest.raises(TypeError):
        FrozenFuse.deserialize("not bytes")


def test_mutable_input_payload_is_copied():
    source = bytearray(FrozenFuse.build([0, 1, 2], seed=42).serialize())
    restored = FrozenFuse.deserialize(source)
    source[:] = bytes(len(source))
    assert all(restored.contains(key) for key in [0, 1, 2])


@pytest.mark.parametrize("bits", [8, 16])
def test_payload_queries_in_fresh_process_without_original_keys(bits):
    original = FrozenFuse.build(range(500), bits=bits, seed=2**64 - 1)
    queries = [0, 7, 499, *range(900, 5000)]
    request = {"payload": base64.b64encode(original.serialize()).decode(), "queries": queries}
    script = (
        "import base64, json, sys\n"
        "from fuse_baseline import FrozenFuse\n"
        "request = json.load(sys.stdin)\n"
        "f = FrozenFuse.deserialize(base64.b64decode(request['payload']))\n"
        "print(json.dumps([f.contains(q) for q in request['queries']]))\n"
    )
    completed = subprocess.run(
        [sys.executable, "-c", script], input=json.dumps(request), text=True,
        capture_output=True, check=True, cwd=Path(__file__).parent,
    )
    actual = json.loads(completed.stdout)
    assert actual[:3] == [True, True, True]
    assert actual == original.contains_many(queries)


@pytest.mark.parametrize("bits", [8, 16])
def test_serialized_size_counts_fingerprint_array_and_metadata(bits):
    filter_ = FrozenFuse.build(range(1000), bits=bits, seed=99)
    payload = filter_.serialize()
    # ArrayLength is the fifth uint32 following the native uint64 seed.
    array_length = struct.unpack_from("=I", payload, 16 + 24)[0]
    assert filter_.payload_bytes == 44 + array_length * (bits // 8)


def test_vendored_source_and_license_match_pinned_hashes():
    vendor = Path(__file__).parent.parent / "vendor"
    provenance = json.loads((vendor / "SOURCE.json").read_text())
    for entry in provenance["files"]:
        content = (vendor / entry["path"]).read_bytes()
        assert len(content) == entry["bytes"]
        assert hashlib.sha256(content).hexdigest() == entry["sha256"]
        git_blob = b"blob " + str(len(content)).encode() + b"\0" + content
        assert hashlib.sha1(git_blob).hexdigest() == entry["upstream_git_blob_sha1"]
