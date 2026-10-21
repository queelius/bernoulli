"""Exhaustively check one-sided contracts for every monotone function on <=4 bits."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json


def value(table: int, assignment: int) -> int:
    return (table >> assignment) & 1


def monotone_tables(n: int):
    for table in range(1 << (1 << n)):
        if all(
            value(table, x) <= value(table, x | (1 << i))
            for x in range(1 << n)
            for i in range(n)
        ):
            yield table


def error_at(table, x, rates, fp):
    out = Fraction()
    for y in range(1 << len(rates)):
        if (x & y) != (x if fp else y):
            continue
        mass = Fraction(1)
        for i, rate in enumerate(rates):
            bx, by = (x >> i) & 1, (y >> i) & 1
            if bx == (0 if fp else 1):
                mass *= rate if bx != by else 1 - rate
        if value(table, y) == int(fp):
            out += mass
    return out


def worst_error(table, n, rates, fp):
    return max(
        (error_at(table, x, rates, fp) for x in range(1 << n) if value(table, x) != int(fp)),
        default=Fraction(),
    )


def sensitivity(table, n, output):
    return max(
        (
            sum(value(table, x ^ (1 << i)) != output for i in range(n))
            for x in range(1 << n)
            if value(table, x) == output
        ),
        default=0,
    )


def boundary_formula(table, n, rates, fp):
    boundary_errors = []
    for x in range(1 << n):
        if value(table, x) == int(fp):
            continue
        changeable = [i for i in range(n) if ((x >> i) & 1) != int(fp)]
        if not all(value(table, x ^ (1 << i)) == int(fp) for i in changeable):
            continue
        survival = Fraction(1)
        for i in changeable:
            survival *= 1 - rates[i]
        boundary_errors.append(1 - survival)
    return max(boundary_errors, default=Fraction())


def graph_checks():
    checked = 0
    for n in range(1, 6):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            adjacency = [set() for _ in range(n)]
            edges = []
            for j, (u, v) in enumerate(possible):
                if (mask >> j) & 1:
                    edges.append((u, v))
                    adjacency[u].add(v)
                    adjacency[v].add(u)
            if any(len(row) > 2 for row in adjacency):
                continue
            unseen = set(range(n))
            expected_s0 = 0
            while unseen:
                todo = [unseen.pop()]
                size = 0
                while todo:
                    u = todo.pop()
                    size += 1
                    for v in adjacency[u] & unseen:
                        unseen.remove(v)
                        todo.append(v)
                expected_s0 += size - (size + 2) // 3
            table = sum(
                1 << x for x in range(1 << n)
                if any(((x >> u) & 1) and ((x >> v) & 1) for u, v in edges)
            )
            assert sensitivity(table, n, 0) == expected_s0
            assert sensitivity(table, n, 1) == (2 if edges else 0)
            checked += 1
    return checked


def main():
    counts = {}
    cases = 0
    uniform_rates = [Fraction(0), Fraction(1, 5), Fraction(1, 2), Fraction(1)]
    for n in range(1, 5):
        count = 0
        for table in monotone_tables(n):
            for fp in (False, True):
                s = sensitivity(table, n, 0 if fp else 1)
                for rate in uniform_rates:
                    actual = worst_error(table, n, [rate] * n, fp)
                    assert actual == 1 - (1 - rate) ** s, (n, table, fp, rate, s, actual)
                    cases += 1
                rates = [Fraction(i + 1, n + 2) for i in range(n)]
                actual = worst_error(table, n, rates, fp)
                assert actual == boundary_formula(table, n, rates, fp), (n, table, fp, actual)
                cases += 1
            count += 1
        counts[str(n)] = count
    assert counts == {"1": 3, "2": 6, "3": 20, "4": 168}
    print(json.dumps({
        "monotone_function_counts": counts,
        "exact_contract_checks": cases,
        "degree_at_most_two_graphs": graph_checks(),
        "maximum_variables": 4,
        "arithmetic": "exact rational",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
