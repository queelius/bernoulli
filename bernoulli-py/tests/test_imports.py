"""The public API: top-level exports, version metadata, and import hygiene."""

from __future__ import annotations

import importlib
import importlib.metadata
import pkgutil
import subprocess
import sys
import types
from importlib.resources import files

import pytest

import bernoulli

SUBMODULES = sorted(
    info.name for info in pkgutil.walk_packages(bernoulli.__path__, prefix="bernoulli.")
)


def test_version_matches_distribution_metadata() -> None:
    assert bernoulli.__version__ == importlib.metadata.version("bernoulli-types")


def test_all_is_unique_and_resolves() -> None:
    assert len(bernoulli.__all__) == len(set(bernoulli.__all__))
    for name in bernoulli.__all__:
        assert hasattr(bernoulli, name), name


def test_star_import_exports_exactly_all() -> None:
    namespace: dict[str, object] = {}
    exec("from bernoulli import *", namespace)
    exported = {k for k in namespace if k != "__builtins__"}
    assert exported == set(bernoulli.__all__)


@pytest.mark.parametrize("name", [n for n in bernoulli.__all__ if n != "__version__"])
def test_export_is_the_canonical_object(name: str) -> None:
    """Each export is the object its defining module holds, and is documented."""
    obj = getattr(bernoulli, name)
    assert obj.__doc__, f"{name} has no docstring"
    if isinstance(obj, types.ModuleType):
        assert obj.__name__ == f"bernoulli.{name}"
        return
    module = importlib.import_module(obj.__module__)
    assert module.__name__.startswith("bernoulli.")
    assert getattr(module, name) is obj


def test_exported_structures_satisfy_their_protocols() -> None:
    keys = [f"k{i}".encode() for i in range(64)]
    bloom = bernoulli.BloomFilter(capacity=64, target_fpr=0.01)
    perfect = bernoulli.PerfectFilter(keys, target_fpr=0.01)
    mph = bernoulli.MinimalPerfectHash(keys)
    assert isinstance(bloom, bernoulli.MembershipOracle)
    assert isinstance(perfect, bernoulli.MembershipOracle)
    assert isinstance(perfect, bernoulli.ApproximateMap)
    assert isinstance(mph, bernoulli.PerfectHashFunction)


def test_package_ships_type_marker() -> None:
    assert files("bernoulli").joinpath("py.typed").is_file()


def _run(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=False
    )


def test_import_is_cheap_and_dependency_free() -> None:
    """``import bernoulli`` loads no optional dependency or research utility."""
    lazy = ["numpy", "scipy", "cffi", "bernoulli.harness", "bernoulli.bench"]
    proc = _run(
        "import sys, bernoulli; "
        f"print(','.join(m for m in {lazy!r} if m in sys.modules))"
    )
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.strip() == ""


@pytest.mark.parametrize("module", SUBMODULES)
def test_submodule_imports_first_in_fresh_interpreter(module: str) -> None:
    """Importing any submodule first must not trip a circular import."""
    proc = _run(f"import {module}")
    assert proc.returncode == 0, proc.stderr


def test_submodule_discovery_sees_the_whole_package() -> None:
    for expected in ("bernoulli.atom", "bernoulli.formula", "bernoulli.maps.retrieval"):
        assert expected in SUBMODULES
