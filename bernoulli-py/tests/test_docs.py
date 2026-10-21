"""Documentation examples are tests: the README and every module docstring.

Modules are discovered by walking the package, so a new module's examples are
checked without editing this file.
"""

from __future__ import annotations

import doctest
import importlib
import pkgutil
from pathlib import Path

import pytest

import bernoulli

README = Path(__file__).resolve().parents[1] / "README.md"
MODULES = ["bernoulli"] + sorted(
    info.name for info in pkgutil.walk_packages(bernoulli.__path__, prefix="bernoulli.")
)


def test_readme_examples() -> None:
    result = doctest.testfile(str(README), module_relative=False)
    assert result.attempted > 20, "README examples were not found"
    assert result.failed == 0


@pytest.mark.parametrize("name", MODULES)
def test_module_doctests(name: str) -> None:
    result = doctest.testmod(importlib.import_module(name))
    assert result.failed == 0
