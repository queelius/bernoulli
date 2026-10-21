"""Stored binary fuse baseline using pinned, unmodified FastFilter C source.

Only a C compiler and Python's standard library are needed at runtime. The
first build or load compiles the bridge; compile before starting a timer by
calling ``compile_bridge()``. Every returned filter is queried after a native
serialize/deserialize round trip. See ../vendor/README.md for byte accounting,
construction salt semantics, provenance, and the timing boundary.
"""

from __future__ import annotations

from collections.abc import Sequence
import ctypes
from dataclasses import dataclass, field
from functools import lru_cache
import hashlib
import operator
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import weakref


_ENVELOPE = struct.Struct("<4sBBBBQ")
_MAGIC = b"BFUS"
_VERSION = 1
_BYTEORDER = 1 if sys.byteorder == "little" else 2
_UINT64_MAX = (1 << 64) - 1


def _uint64(value: int, name: str) -> int:
    if isinstance(value, bool):
        raise TypeError(f"{name} must be an integer, not bool")
    result = operator.index(value)
    if not 0 <= result <= _UINT64_MAX:
        raise ValueError(f"{name} must be an unsigned 64-bit integer")
    return result


def compile_bridge() -> Path:
    """Compile a content-addressed shared library, returning its local path.

    This Linux/POSIX research harness invokes cc without a shell. Compilation
    is cached by both source files and the fixed compiler flags. It is separate
    from the serialized filter's storage budget.
    """
    source = Path(__file__).with_name("fuse_bridge.c")
    vendor = source.parent.parent / "vendor"
    flags = ("-O3", "-std=c11", "-fPIC", "-shared")
    identity = hashlib.sha256(
        source.read_bytes() + (vendor / "binaryfusefilter.h").read_bytes()
        + " ".join(flags).encode() + sys.platform.encode()
    ).hexdigest()[:20]
    directory = vendor / ".build"
    directory.mkdir(exist_ok=True)
    library = directory / f"fuse_bridge-{identity}.so"
    if not library.exists():
        with tempfile.TemporaryDirectory(dir=directory) as temporary:
            output = Path(temporary) / "fuse_bridge.so"
            subprocess.run(
                ["cc", *flags, str(source), "-o", str(output), "-lm"],
                check=True, capture_output=True, text=True,
            )
            output.replace(library)
    return library


@lru_cache(maxsize=1)
def _library() -> ctypes.CDLL:
    library = ctypes.CDLL(str(compile_bridge()))
    library.fuse_build.argtypes = (
        ctypes.POINTER(ctypes.c_uint64), ctypes.c_uint32,
        ctypes.c_uint8, ctypes.c_uint64,
    )
    library.fuse_build.restype = ctypes.c_void_p
    library.fuse_free.argtypes = (ctypes.c_void_p,)
    library.fuse_free.restype = None
    library.fuse_payload_size.argtypes = (ctypes.c_void_p,)
    library.fuse_payload_size.restype = ctypes.c_size_t
    library.fuse_serialize.argtypes = (
        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t,
    )
    library.fuse_serialize.restype = ctypes.c_bool
    library.fuse_deserialize.argtypes = (
        ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint8, ctypes.c_uint64,
    )
    library.fuse_deserialize.restype = ctypes.c_void_p
    library.fuse_contains.argtypes = (ctypes.c_void_p, ctypes.c_uint64)
    library.fuse_contains.restype = ctypes.c_bool
    return library


@dataclass(frozen=True)
class FrozenFuse:
    """Immutable 8/16-bit membership filter reconstructed from stored bytes.

    ``seed`` is an unsigned 64-bit XOR salt, not the upstream internal seed.
    Equal sets and equal salts give equal payloads. Distinct salts give varied
    hash configurations; statistical independence is an experimental model
    assumption, not a guarantee of this salt family.

    Empty and singleton sets are rejected because the upstream allocator's
    documented input contract requires at least two keys. Duplicates are
    removed and keys sorted before construction; no exact keys are retained.
    """

    _payload: bytes = field(repr=False)
    _bits: int = field(init=False)
    _handle: int = field(init=False, repr=False, compare=False)
    _finalizer: weakref.finalize[[int], FrozenFuse] = field(
        init=False, repr=False, compare=False,
    )

    def __post_init__(self) -> None:
        if not isinstance(self._payload, (bytes, bytearray, memoryview)):
            raise TypeError("payload must be bytes-like")
        payload = bytes(self._payload)
        if len(payload) < _ENVELOPE.size:
            raise ValueError("truncated binary fuse envelope")
        magic, version, bits, byteorder, reserved, salt = _ENVELOPE.unpack_from(payload)
        if (magic != _MAGIC or version != _VERSION or bits not in (8, 16)
                or byteorder != _BYTEORDER or reserved != 0):
            raise ValueError("unsupported binary fuse payload envelope or byte order")
        native = payload[_ENVELOPE.size:]
        library = _library()
        handle = library.fuse_deserialize(native, len(native), bits, salt)
        if not handle:
            raise ValueError("invalid binary fuse payload or native allocation failed")
        object.__setattr__(self, "_payload", payload)
        object.__setattr__(self, "_bits", bits)
        object.__setattr__(self, "_handle", handle)
        object.__setattr__(self, "_finalizer", weakref.finalize(self, library.fuse_free, handle))

    @classmethod
    def build(cls, keys: Sequence[int], bits: int = 8, seed: int = 0) -> FrozenFuse:
        """Build, serialize, reload, and verify every inserted key is accepted."""
        bits = _uint64(bits, "bits")
        if bits not in (8, 16):
            raise ValueError("bits must be 8 or 16")
        salt = _uint64(seed, "seed")
        unique = sorted({_uint64(key, "key") for key in keys})
        if len(unique) < 2:
            raise ValueError("binary fuse requires at least two distinct keys")
        if len(unique) >= 1 << 32:
            raise ValueError("binary fuse requires fewer than 2**32 distinct keys")
        library = _library()
        native_keys = (ctypes.c_uint64 * len(unique))(*unique)
        handle = library.fuse_build(native_keys, len(unique), bits, salt)
        if not handle:
            raise RuntimeError("binary fuse construction failed (allocation or retry limit)")
        try:
            length = library.fuse_payload_size(handle)
            buffer = ctypes.create_string_buffer(length)
            if not library.fuse_serialize(handle, buffer, length):
                raise RuntimeError("binary fuse serialization failed")
            payload = _ENVELOPE.pack(_MAGIC, _VERSION, bits, _BYTEORDER, 0, salt) + buffer.raw
        finally:
            library.fuse_free(handle)
        result = cls.deserialize(payload)
        if not all(result.contains(key) for key in unique):
            raise RuntimeError("binary fuse round trip introduced a false negative")
        return result

    def contains(self, key: int) -> bool:
        """Query a fixed native realization with no query-time randomness."""
        return bool(_library().fuse_contains(self._handle, _uint64(key, "key")))

    def contains_many(self, keys: Sequence[int]) -> list[bool]:
        """Use the same per-key ctypes route as ``contains``."""
        return [self.contains(key) for key in keys]

    def serialize(self) -> bytes:
        return self._payload

    @classmethod
    def deserialize(cls, payload: bytes | bytearray | memoryview) -> FrozenFuse:
        if not isinstance(payload, (bytes, bytearray, memoryview)):
            raise TypeError("payload must be bytes-like")
        return cls(bytes(payload))

    @property
    def payload_bytes(self) -> int:
        """Bytes on disk including the 16-byte envelope and native metadata."""
        return len(self._payload)

    @property
    def bits(self) -> int:
        return self._bits


if __name__ == "__main__":
    print(compile_bridge())
