"""Smoke tests verifying the bernoulli package imports and exposes a Bernoulli type."""

import importlib


def test_package_imports():
    """The bernoulli package must be importable."""
    bernoulli = importlib.import_module("bernoulli")
    assert bernoulli is not None


def test_version_string():
    """The package must expose a __version__ string."""
    import bernoulli
    assert hasattr(bernoulli, "__version__")
    assert isinstance(bernoulli.__version__, str)
    assert bernoulli.__version__ == "0.1.0"


def test_bernoulli_type_exists():
    """Bernoulli must be importable from the top-level package."""
    from bernoulli import Bernoulli
    assert Bernoulli is not None


def test_bernoulli_constructs_with_value():
    """Bernoulli(value=...) must accept a value and store it on .value."""
    from bernoulli import Bernoulli
    b = Bernoulli(value=True)
    assert b.value is True

    b2 = Bernoulli(value=42)
    assert b2.value == 42


def test_generic_subscription():
    """Bernoulli must support Generic[T] subscription syntax."""
    from bernoulli import Bernoulli
    parameterized = Bernoulli[int]
    assert parameterized is not None


def test_version_synchronized_with_metadata():
    """The __version__ string must match the package metadata version."""
    from importlib.metadata import version
    import bernoulli
    assert bernoulli.__version__ == version("bernoulli")
