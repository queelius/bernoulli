"""bernoulli: random approximate types with principled error propagation.

The package implements the Bernoulli framework for random approximate types,
unifying probabilistic data structures (Bloom filters, perfect-hash filters,
ribbon retrieval, sketches), randomized algorithms (Miller-Rabin, Las Vegas /
Monte Carlo), and noisy classifiers under a single algebra of error rates.

Public API (Phase 1):

- ``BernoulliBool``: the atomic random approximate Boolean (a value plus
  channel rates ``(fpr, fnr)``), closed under AND / OR / NOT.
- ``algebra``: composition theorem helpers for k-fold chains.
- ``measures``: classification measures (PPV, NPV, Youden's J, F1, MCC).

See ``PHASING.md`` for the roadmap of phases 2 to 5 (sets, maps, relations,
sketches), each backed by a small C core.

The framework is described in:

    Towell, A. (2026). *Bernoulli Types: An Algebra of Approximate
    Computation.* Book in progress.

and in the ``bernoulli/papers/`` tree of the parent monorepo.
"""

from bernoulli._version import __version__
from bernoulli.atom import BernoulliBool

__all__ = [
    "__version__",
    "BernoulliBool",
]
