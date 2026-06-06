"""Natural Bernoulli algorithms.

Each algorithm in this subpackage is a randomized procedure whose answer is
naturally a Bernoulli value: bounded error rates, structurally one-sided
where applicable.

- :mod:`bernoulli.algorithms.miller_rabin`: primality witness check; one-sided
  FPR with worst-case 1/4 per round.
- :mod:`bernoulli.algorithms.noisy_classifier`: configurable two-sided
  Bernoulli<bool> for synthetic experiments and harness validation.
"""
