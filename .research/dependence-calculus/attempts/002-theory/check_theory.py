"""Exact small-case checks for the accompanying proofs; no third-party packages."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json


def probability(predicate, rates):
    total = Fraction()
    for assignment in product((0, 1), repeat=len(rates)):
        if predicate(assignment):
            mass = Fraction(1)
            for bit, rate in zip(assignment, rates):
                mass *= rate if bit else 1 - rate
            total += mass
    return total


def path_mass(rates):
    a, b = Fraction(1), Fraction()
    for rate in rates:
        a, b = (a + b) * (1 - rate), a * rate
    return a + b


def cycle_mass(rates):
    total = Fraction()
    for first in (0, 1):
        a, b = (1 - rates[0], Fraction()) if first == 0 else (Fraction(), rates[0])
        for rate in rates[1:]:
            a, b = (a + b) * (1 - rate), a * rate
        total += a + (b if first == 0 else 0)
    return total


def main():
    checks = {"weighted_paths": 0, "weighted_cycles": 0, "projection_covariances": 0}
    for n in range(1, 9):
        rates = [Fraction(i + 1, n + 2) for i in range(n)]
        edges = list(zip(range(n - 1), range(1, n)))
        target = probability(lambda z: all(not (z[u] and z[v]) for u, v in edges), rates)
        assert path_mass(rates) == target
        checks["weighted_paths"] += 1
        if n >= 3:
            edges.append((n - 1, 0))
            target = probability(lambda z: all(not (z[u] and z[v]) for u, v in edges), rates)
            assert cycle_mass(rates) == target
            checks["weighted_cycles"] += 1
    # Include degenerate rates; strict positivity characterization excludes these.
    for rates in product((Fraction(0), Fraction(1, 2), Fraction(1)), repeat=4):
        edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
        target = probability(lambda z: all(not (z[u] and z[v]) for u, v in edges), rates)
        assert cycle_mass(rates) == target
        checks["weighted_cycles"] += 1

    rates = [Fraction(1, 5), Fraction(2, 5), Fraction(3, 5), Fraction(4, 5)]
    subsets = [set(c) for n in range(5) for c in combinations(range(4), n)]

    def q(indices):
        out = Fraction(1)
        for i in indices:
            out *= 1 - rates[i]
        return out

    for a, b in product(subsets, repeat=2):
        pa = probability(lambda z: any(z[i] for i in a), rates)
        pb = probability(lambda z: any(z[i] for i in b), rates)
        joint = probability(lambda z: any(z[i] for i in a) and any(z[i] for i in b), rates)
        assert joint - pa * pb == q(a - b) * q(b - a) * q(a & b) * (1 - q(a & b))
        checks["projection_covariances"] += 1

    # K4 is simple cubic: independent directed occurrences versus canonical edges.
    vertices = list(range(4))
    edges = list(combinations(vertices, 2))
    incidence = [[i for i, edge in enumerate(edges) if v in edge] for v in vertices]
    rates = [Fraction(1, 2)] * len(edges)
    quotient = probability(lambda z: any(all(z[i] for i in row) for row in incidence), rates)
    covers = sum(all(any(z[i] for i in row) for row in incidence) for z in product((0, 1), repeat=6))
    assert quotient == 1 - Fraction(covers, 2 ** len(edges))
    directed = probability(lambda z: any(all(z[3*v+j] for j in range(3)) for v in vertices), [Fraction(1, 2)] * 12)
    assert directed == 1 - (1 - Fraction(1, 8)) ** 4
    assert quotient <= directed
    checks["K4_edge_covers"] = covers
    checks["K4_quotient_FPR"] = str(quotient)
    checks["K4_prequotient_FPR"] = str(directed)
    print(json.dumps(checks, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
