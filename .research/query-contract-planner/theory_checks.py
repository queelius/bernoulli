"""Exact finite checks for the query-contract opportunity audit.

Run directly. This checks small models against enumeration; it does not assert
that a concrete hash family has more independence than is proved in theory.md.
"""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction as F
from heapq import nsmallest
from itertools import combinations, product
from pathlib import Path
from random import Random


def subsets(k: int, cap: int) -> list[frozenset[int]]:
    return [frozenset(i for i in range(k) if mask >> i & 1)
            for mask in range(1 << k) if mask.bit_count() <= cap]


def fixed_fp(rows: tuple[frozenset[int], ...], k: int, alpha: F) -> F:
    return 1 - product_fraction(
        1 - alpha ** (len(rows) - sum(i in row for row in rows))
        for i in range(k)
    )


def product_fraction(values) -> F:
    result = F(1)
    for value in values:
        result *= value
    return result


def noise_enumeration(rows: tuple[frozenset[int], ...], k: int, alpha: F) -> F:
    absent = [(j, i) for j, row in enumerate(rows) for i in range(k) if i not in row]
    answer = F(0)
    for bits in product((0, 1), repeat=len(absent)):
        realization = [set(row) for row in rows]
        for (j, i), bit in zip(absent, bits):
            if bit:
                realization[j].add(i)
        if any(all(i in row for row in realization) for i in range(k)):
            ones = sum(bits)
            answer += alpha ** ones * (1 - alpha) ** (len(bits) - ones)
    return answer


def multiway_contract(m: int, k: int, degree: int, alpha: F) -> F:
    load = min(m * degree, k * (m - 1))
    full, residual = divmod(load, m - 1)
    remaining = k - full - bool(residual)
    no_fp = (1 - alpha) ** full * (1 - alpha ** m) ** remaining
    if residual:
        no_fp *= 1 - alpha ** (m - residual)
    return 1 - no_fp


def attaining_rows(m: int, k: int, degree: int) -> tuple[frozenset[int], ...]:
    load = min(m * degree, k * (m - 1))
    full, residual = divmod(load, m - 1)
    counts = [m - 1] * full + ([residual] if residual else [])
    rows: list[set[int]] = [set() for _ in range(m)]
    cursor = 0
    for i, count in enumerate(counts):
        for _ in range(count):
            rows[cursor % m].add(i)
            cursor += 1
    return tuple(frozenset(row) for row in rows)


def heterogeneous_fp(a: tuple[F, ...], b: tuple[F, ...], left, right) -> F:
    return 1 - product_fraction(
        1 - (F(1) if i in left else x) * (F(1) if i in right else y)
        for i, (x, y) in enumerate(zip(a, b))
    )


def heterogeneous_dp(a: tuple[F, ...], b: tuple[F, ...], r: int, s: int) -> F:
    states = {(0, 0): F(1)}
    for x, y in zip(a, b):
        next_states: dict[tuple[int, int], F] = {}
        for (n, p), weight in states.items():
            transitions = [((n, p), weight * (1 - x * y))]
            if n < r:
                transitions.append(((n + 1, p), weight * (1 - y)))
            if p < s:
                transitions.append(((n, p + 1), weight * (1 - x)))
            for state, candidate in transitions:
                next_states[state] = min(next_states.get(state, candidate), candidate)
        states = next_states
    return 1 - min(states.values())


def onehot_heterogeneous(a: tuple[F, ...], b: tuple[F, ...]) -> F:
    if not a:
        return F(0)
    if len(a) == 1:
        return max(a[0], b[0])
    base_terms = tuple(1 - x * y for x, y in zip(a, b))
    if not all(base_terms):
        return F(1)
    first = nsmallest(2, (((1 - y) / z, i) for i, (y, z) in enumerate(zip(b, base_terms))))
    second = nsmallest(2, (((1 - x) / z, i) for i, (x, z) in enumerate(zip(a, base_terms))))
    factor = min(x * y for x, i in first for y, j in second if i != j)
    return 1 - product_fraction(base_terms) * factor


def binary_rank(vectors) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        value = vector
        while value:
            index = value.bit_length() - 1
            if index in pivots:
                value ^= pivots[index]
            else:
                pivots[index] = value
                break
    return len(pivots)


def linear_collision_ie(differences: tuple[int, ...], bits: int) -> F:
    return sum(((-1) ** (len(selected) + 1) * F(1, 2 ** (bits * binary_rank(selected)))
                for count in range(1, len(differences) + 1)
                for selected in combinations(differences, count)), F(0))


def linear_collision_enumeration(differences: tuple[int, ...], width: int, bits: int) -> F:
    matrices = list(product(range(1 << width), repeat=bits))
    bad = sum(any(all((row & d).bit_count() % 2 == 0 for row in matrix)
                  for d in differences) for matrix in matrices)
    return F(bad, len(matrices))


def collision_rate(prime: int, modulus: int) -> F:
    quotient, remainder = divmod(prime, modulus)
    return F(remainder * (quotient + 1) ** 2 + (modulus - remainder) * quotient ** 2, prime ** 2)


def evaluate_polynomial(coefficients: tuple[int, ...], point: int, prime: int) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * point + coefficient) % prime
    return value


def run() -> dict:
    counts = Counter()
    rates = (F(0), F(1, 10), F(1, 2), F(1))
    for m in range(2, 5):
        for k in range(0, 5 if m < 4 else 4):
            for degree in range(k + 2):
                profiles = [rows for rows in product(subsets(k, degree), repeat=m)
                            if not set.intersection(*(set(row) for row in rows))]
                for alpha in rates:
                    expected = multiway_contract(m, k, degree, alpha)
                    assert max(fixed_fp(rows, k, alpha) for rows in profiles) == expected
                    attained = attaining_rows(m, k, degree)
                    assert max(map(len, attained)) <= degree
                    assert not set.intersection(*(set(row) for row in attained))
                    assert fixed_fp(attained, k, alpha) == expected
                    counts['multiway_parameter_cases'] += 1
                counts['false_profiles_enumerated'] += len(profiles)
    for m, k in ((2, 0), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2)):
        for rows in product(subsets(k, k), repeat=m):
            if set.intersection(*(set(row) for row in rows)):
                continue
            for alpha in rates:
                assert fixed_fp(rows, k, alpha) == noise_enumeration(rows, k, alpha)
                counts['independent_noise_oracle_cases'] += 1
    rng = Random(631792)
    palette = (F(0), F(1, 7), F(2, 5), F(4, 5), F(1))
    for k in range(5):
        for _ in range(20):
            a = tuple(rng.choice(palette) for _ in range(k))
            b = tuple(rng.choice(palette) for _ in range(k))
            for r in range(k + 1):
                for s in range(k + 1):
                    expected = max(heterogeneous_fp(a, b, left, right)
                                   for left in subsets(k, r) for right in subsets(k, s)
                                   if not left & right)
                    assert heterogeneous_dp(a, b, r, s) == expected
                    counts['heterogeneous_dp_cases'] += 1
            assert onehot_heterogeneous(a, b) == heterogeneous_dp(a, b, 1, 1)
            counts['onehot_heterogeneous_cases'] += 1
    for width in range(1, 4):
        vectors = range(1, 1 << width)
        for size in range(min(4, len(vectors)) + 1):
            for differences in combinations(vectors, size):
                for bits in range(1, 4):
                    exact = linear_collision_ie(differences, bits)
                    assert exact == linear_collision_enumeration(differences, width, bits)
                    assert exact <= min(F(1), F(len(differences), 1 << bits))
                    counts['linear_hash_cases'] += 1
    # A within-witness alias can make the unaliased one-hot formula unsound.
    alias_actual = 1 - (1 - F(1, 2)) ** 3
    alias_unaliased = multiway_contract(2, 3, 1, F(1, 2))
    assert alias_actual == F(7, 8) > alias_unaliased == F(13, 16)
    # Three distinct collision differences are pairwise but not mutually independent.
    triangle_actual = linear_collision_ie((1, 2, 3), 1)
    triangle_independent = 1 - (1 - F(1, 2)) ** 3
    assert triangle_actual == 1 > triangle_independent == F(7, 8)
    # Conditioning a one-bit linear hash on successful injectivity of two rows.
    accepted = [row for row in range(4) if (row & 1).bit_count() % 2 and (row & 2).bit_count() % 2]
    conditional_collision = F(sum((row & 3).bit_count() % 2 == 0 for row in accepted), len(accepted))
    assert conditional_collision == 1
    # Every four-point image of cubic polynomials over F_5 occurs exactly once.
    prime = 5
    images = Counter(tuple(evaluate_polynomial(cs, x, prime) for x in range(4))
                     for cs in product(range(prime), repeat=4))
    assert len(images) == prime ** 4 and set(images.values()) == {1}
    counts['polynomial_four_point_images'] = len(images)
    # Exhaust all 2,401 F_7 cubics and all false two-row queries on a 3-value domain.
    prime = 7
    for modulus in (1, 2, 4, 8):
        q = collision_rate(prime, modulus)
        all_images = [tuple(evaluate_polynomial(cs, x, prime) % modulus for x in range(6))
                      for cs in product(range(prime), repeat=4)]
        for left, right in product(range(3), repeat=2):
            for candidates in subsets(3, 3):
                if left == right and left in candidates:
                    continue
                bad = sum(any(values[c] == values[left] and values[3 + c] == values[3 + right]
                              for c in candidates) for values in all_images)
                observed = F(bad, prime ** 4)
                singles = sum(int(c == left) + int(c == right) for c in candidates)
                fixed_bound = min(F(1), singles * q + (len(candidates) - singles) * q * q)
                cap = min(len(candidates), 2)
                uniform_bound = min(F(1), cap * q + (len(candidates) - cap) * q * q)
                assert observed <= fixed_bound <= uniform_bound
                counts['finite_polynomial_query_cases'] += 1
    prime = 2 ** 61 - 1
    concrete_rates = []
    for bits in (1, 4, 8, 16, 32, 61):
        modulus = 1 << bits
        q = collision_rate(prime, modulus)
        assert q == F(1, modulus) + F(modulus - 1, modulus * prime * prime)
        concrete_rates.append({'bits': bits, 'collision_rate': str(q), 'float': float(q)})
    return {
        'status': 'passed',
        'counts': dict(counts),
        'counterexamples': {
            'source_alias': {'actual': str(alias_actual), 'invalid_unaliased_formula': str(alias_unaliased)},
            'linear_triangle': {'actual': str(triangle_actual), 'invalid_independence_formula': str(triangle_independent)},
            'postselected_linear_collision': str(conditional_collision),
        },
        'mersenne_prime_modulo_collision_rates': concrete_rates,
        'scope': 'Exact rational finite enumeration; no manuscript or package changes; no empirical independence inference.',
    }


if __name__ == '__main__':
    result = run()
    destination = Path(__file__).with_name('theory_checks_results.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
