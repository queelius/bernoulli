"""Sketches: probabilistic data structures as Bernoulli estimators.

- :class:`HyperLogLog`: cardinality, a ``Bernoulli<int>`` estimator.
- :class:`CountMinSketch`: frequency, a one-sided ``Bernoulli<int>`` estimator
  (never undercounts).
- :class:`MinHash`: Jaccard similarity, a ``Bernoulli<float>`` estimator.
"""

from bernoulli.sketches.countmin import CountMinSketch
from bernoulli.sketches.hyperloglog import HyperLogLog
from bernoulli.sketches.minhash import MinHash

__all__ = ["CountMinSketch", "HyperLogLog", "MinHash"]
