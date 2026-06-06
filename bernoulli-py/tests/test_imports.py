"""Smoke tests: package imports and exposes the Phase 1 public API."""

from __future__ import annotations


def test_package_imports() -> None:
    import bernoulli

    assert bernoulli is not None


def test_version_string() -> None:
    import bernoulli

    assert hasattr(bernoulli, "__version__")
    assert isinstance(bernoulli.__version__, str)
    assert bernoulli.__version__ == "0.2.0"


def test_bernoulli_bool_exposed_at_top_level() -> None:
    from bernoulli import BernoulliBool

    b = BernoulliBool(value=True, fpr=0.1, fnr=0.05)
    assert b.value is True
    assert b.fpr == 0.1
    assert b.fnr == 0.05


def test_algebra_module_imports() -> None:
    from bernoulli import algebra

    assert callable(algebra.composition_total_error)
    assert callable(algebra.composition_homogeneous)
    assert callable(algebra.miller_rabin_error)


def test_measures_module_imports() -> None:
    from bernoulli import measures

    assert callable(measures.ppv)
    assert callable(measures.npv)
    assert callable(measures.youden_j)


def test_sets_protocol_imports() -> None:
    from bernoulli.sets import MembershipOracle

    assert MembershipOracle is not None


def test_maps_protocol_imports() -> None:
    from bernoulli.maps import ApproximateMap, PerfectHashFunction

    assert ApproximateMap is not None
    assert PerfectHashFunction is not None
