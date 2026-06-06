# C source for the bernoulli package

This directory holds the C source compiled into ``_bernoulli_c.so`` via cffi
(api mode) when the ``[c]`` extra is installed. Phase 1 ships zero C code;
the directory is reserved.

## What lives here

The sequencing matches ``../PHASING.md``.

### Phase 2 (sets)

- ``bitarray.c``: ``set_bit``, ``test_bit``, ``popcount``, contiguous-block ops.
- ``hash.c``: portable hash primitives (xxhash inlined or 64-bit FNV variants
  with seed parameterization).
- ``bloom.c``: classical k-hash Bloom filter with the bit array and hash
  modules above.

### Phase 3 (maps and codecs)

- ``gf2.c``: GF(2) Gaussian elimination and back-substitution.
- ``ribbon.c``: ribbon-band sparse-system solver, port from
  ``~/github/repos/maph/include/maph/filters/ribbon_filter.hpp`` and
  ``retrieval/ribbon_retrieval.hpp``.
- ``codec.c``: prefix-codec encode / decode, port from
  ``~/github/repos/maph/include/maph/codecs/prefix_codec.hpp``.
- ``phf.c``: minimal-overhead perfect hash evaluation (PHOBIC pilot lookup
  and similar).
- ``fingerprint.c``: packed k-bit fingerprint storage with verify.

### Phase 5 (sketches)

- ``countmin.c``, ``hll.c``, ``minhash.c``: sketch primitives.

## Build strategy

The Python side declares the C ABI in ``../src/bernoulli/_cffi_build.py``
(forthcoming). Each C source file is self-contained, compiles with C99 or
later (``-std=c11``), and depends only on libc. No platform-specific intrinsics
beyond the conditional ``__builtin_popcount`` family.

Pure-Python fallbacks live alongside each Python module that consumes a C
primitive, gated on ``HAS_C = importlib.util.find_spec("bernoulli._c") is not None``.

## Why C, not C++?

The maph research playground at ``~/github/repos/maph/`` is C++23. This
package's C core is intentionally plain C so that PyPI wheels build on
manylinux images and old macOS toolchains without C++23-capable compilers.
Algorithmic ideas port across the boundary; bindings do not.

## Why not bind directly to maph?

For research experiments that want to test maph's exact algorithms, the
right move is a separate ``maph-py`` binding via pybind11 (not in scope
here). This package is the production / pedagogy artifact. The two have
different audience constraints; the C tree above is the one that satisfies
the production constraint.
