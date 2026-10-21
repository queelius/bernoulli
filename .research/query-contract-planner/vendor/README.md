# Stored binary fuse baseline

`binaryfusefilter.h` and `LICENSE` are exact, unmodified files from
[FastFilter/xor_singleheader](https://github.com/FastFilter/xor_singleheader),
pinned at commit `5b6b321aa5c0c8ef5b5fb3145206f07f3754a0a1`
(2026-10-09). `SOURCE.json` records the canonical URLs, Git blob identifiers,
byte counts, and SHA-256 hashes. The upstream license is Apache-2.0, copyright
2019 Daniel Lemire. The C bridge and Python wrapper live in `../code/`.

## Build and use

From the repository root, compile the local bridge before timing:

```bash
python .research/query-contract-planner/code/fuse_baseline.py
```

This uses Python's standard library and a C compiler; no Python package is
needed at runtime. Tests use the workspace's existing pytest installation.
The implementation targets the Linux/POSIX research environment. The command
prints the content-addressed `.build/fuse_bridge-<digest>.so` file used by
ctypes. Generated libraries are ignored. The reproducible C compiler command
is:

```bash
cc -O3 -std=c11 -fPIC -shared \
  .research/query-contract-planner/code/fuse_bridge.c \
  -o /tmp/query-contract-fuse-bridge.so -lm
```

The wrapper uses those same arguments, with an atomic temporary output and
the content-addressed path in place of `/tmp/query-contract-fuse-bridge.so`.
The verified environment used GCC 13.3.0 and Python 3.12.3. To rebuild with
a changed compiler, remove the ignored `.build/` cache first; the cache key
tracks source content and fixed flags, not the compiler installation.

With `code/` on the Python import path:

```python
from fuse_baseline import FrozenFuse, compile_bridge

compile_bridge()
stored = FrozenFuse.build([1, 2, 3], bits=8, seed=123)
payload = stored.serialize()
loaded = FrozenFuse.deserialize(payload)
assert loaded.contains(2)
assert loaded.payload_bytes == len(payload)
```

Both 8-bit and 16-bit fingerprint versions use the upstream allocator,
constructor, query function, serializer, and deserializer. Keys and `seed`
must be integers in `[0, 2**64)`. The wrapper accepts integer-index objects
and rejects booleans and lossy floating-point conversions. It sorts and
deduplicates keys and rejects fewer than two distinct keys, following the
upstream allocator's documented minimum. Original exact keys are not retained.
`build` always reloads the serialized bytes and verifies every inserted key
against the reloaded filter. Both `contains` and `contains_many` use the same
per-query ctypes call, with no query-time randomness.

## Construction salt and interpretation

In both upstream `populate` functions, the local SplitMix64 counter is reset
to `0x726b2b9d438b9d4d`. Its first output becomes the native hash seed;
subsequent outputs are deterministic retry seeds. Assigning the filter's
native `Seed` field before calling `populate` cannot control construction.

The wrapper instead transforms every input key as `key XOR seed`, using the
caller-provided 64-bit seed as a salt. The same bijection is applied to queries,
and the salt is saved in the payload. The upstream source and retry sequence
are unchanged. Repeated construction of an equal set with an equal salt is
deterministic, including across input order and duplicate occurrences.

Separately sampled salts provide reproducible varied configurations. They do
not establish an independent-hash theorem, independence between filters, or
independence of repeated queries to a stored realization. Some structured key
sets are invariant under some XOR salts. Experiments must report how salts
were sampled and treat independence assumptions separately from this native
implementation detail. A fixed stored filter returns the same answer to the
same key on every query.

## Serialized byte accounting

The envelope has the Python `struct` format `<4sBBBBQ` (16 bytes): magic
`BFUS`, version 1, fingerprint width, native byte-order tag, reserved zero,
and the XOR salt. The native stream follows: `Seed` (uint64), `Size`,
`SegmentLength`, `SegmentCount`, `SegmentCountLength`, and `ArrayLength`
(five uint32 values), followed by the fingerprint array. `SegmentLengthMask`
is reconstructed as `SegmentLength - 1`.

Thus `payload_bytes = 44 + ArrayLength * (bits / 8)`. This counts all stored
salt, version, sizing, native seed, and fingerprint information. The native
stream retains the upstream byte order; loading a payload with a different
endianness tag is rejected. The bridge validates buffer size and segment
geometry before invoking the upstream deserializer, which otherwise trusts
its input buffer. The format has no checksum and is a local research format.

At this pinned revision, `binary_fuse16_serialization_bytes` incorrectly
counts the derived `SegmentLengthMask`, although its serializer and
deserializer omit it. The bridge counts the actual 28 native header bytes
written, avoiding four unused padding bytes. The 8-bit helper agrees with
the actual stream. Neither upstream file is patched.

Serialized byte count excludes Python objects, native allocation metadata,
the loaded library, and construction workspace. The live wrapper retains
both immutable serialized bytes and a separately allocated native filter,
so live resident memory exceeds the serialized payload size.

## Timing and construction memory

Compile before a timed run. Python `build` timing includes validation,
sorting/deduplication, conversion to a ctypes input array, native construction,
serialization, deserialization, and a per-key false-negative check. It is
not a measurement of native construction alone. Per-query timing includes
Python validation, method dispatch, and the ctypes boundary; it is not native
query throughput. The C implementation is optimized with `-O3`, so comparison
with pure Python baselines needs this qualification. Batch queries intentionally
do not change that execution route.

For `n` distinct keys and a fingerprint array of `m` entries, the upstream
constructor allocates temporary arrays totaling `9*n + 13*m + 4*b + 8` bytes,
where `b` is the smallest power of two at least `SegmentCount`, with minimum
2. The bridge additionally allocates `8*n` bytes for salted keys, and the
native fingerprints use `(bits/8)*m` bytes. These are requested C allocation
sizes from the pinned source, not an observed process peak. The ctypes input
array adds another `8*n`; Python's original inputs, deduplication set, sorted
list, serialization copies, loaded library, and allocator overhead add more.
Use isolated-process RSS for a measured total peak: Python tracemalloc alone
does not account for upstream `malloc`/`calloc` allocations.

## Verification

From the repository root:

```bash
bernoulli-py/.venv/bin/python -m pytest \
  .research/query-contract-planner/code/test_fuse_baseline.py \
  --cov=fuse_baseline --cov-branch --cov-report=term-missing
bernoulli-py/.venv/bin/ruff check \
  .research/query-contract-planner/code/fuse_baseline.py \
  .research/query-contract-planner/code/test_fuse_baseline.py
bernoulli-py/.venv/bin/mypy --strict \
  .research/query-contract-planner/code/fuse_baseline.py
```

Tests cover both widths, boundary keys and salts, duplicates, deterministic
realizations, repeat-query invariance, inserted-key acceptance, reload in a
fresh process, exact stored size, immutable state, malformed envelopes/native
geometry, and invalid scalar inputs. Coverage does not force out-of-memory
conditions, native retry exhaustion, or allocation of billions of keys.
