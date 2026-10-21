# bernoulli-types

[![bernoulli-py CI](https://github.com/queelius/bernoulli/actions/workflows/bernoulli-py.yml/badge.svg)](https://github.com/queelius/bernoulli/actions/workflows/bernoulli-py.yml)

`bernoulli-types` (import name `bernoulli`) is the reference implementation of
a single error model for approximate answers. Every structure in it answers
through a binary channel with two rates, the false-positive rate `fpr` and the
false-negative rate `fnr`, and the package carries those rates through
composition. Bloom filters, perfect-hash filters, retrieval structures,
sketches, Miller-Rabin and noisy classifiers are all instances.

The structures are not new, and neither is most of the rate algebra. The
package is a unification, written so that its claims can be executed and
checked:

- Warner (1965), randomized response: a bit reported through known flip rates
  ([doi:10.1080/01621459.1965.10480775](https://doi.org/10.1080/01621459.1965.10480775)).
- Bloom (1970), the Bloom filter
  ([doi:10.1145/362686.362692](https://doi.org/10.1145/362686.362692)).
- Carter, Floyd, Gill, Markowsky and Wegman (1978), approximate membership
  testers and the `-log2(fpr)` bits-per-key bound
  ([doi:10.1145/800133.804332](https://doi.org/10.1145/800133.804332)).
- Dietzfelbinger and Pagh (2008), a minimal perfect hash plus fingerprints as
  an approximate membership structure, and retrieval
  ([doi:10.1007/978-3-540-70575-8_32](https://doi.org/10.1007/978-3-540-70575-8_32)).
  `PerfectFilter` is this construction.
- Limasset, Rizk, Chikhi and Peterlongo (2017), BBHash
  ([doi:10.4230/LIPIcs.SEA.2017.25](https://doi.org/10.4230/LIPIcs.SEA.2017.25)).
  `MinimalPerfectHash` is this construction.

Other components follow Parker and McCluskey (1975) for signal probabilities
through Boolean networks
([doi:10.1109/T-C.1975.224279](https://doi.org/10.1109/T-C.1975.224279)),
Kirsch and Mitzenmacher (2006) for double hashing
([doi:10.1007/11841036_42](https://doi.org/10.1007/11841036_42)), Graf and
Lemire (2020) for peeling-based retrieval
([doi:10.1145/3376122](https://doi.org/10.1145/3376122)), Cormode and
Muthukrishnan (2005) for Count-Min
([doi:10.1016/j.jalgor.2003.12.001](https://doi.org/10.1016/j.jalgor.2003.12.001)),
Flajolet, Fusy, Gandouet and Meunier (2007) for HyperLogLog, Broder (1997)
for MinHash ([doi:10.1109/SEQUEN.1997.666900](https://doi.org/10.1109/SEQUEN.1997.666900)),
and Miller (1976) and Rabin (1980) for primality testing.

The theory is developed in the monograph
[*Bernoulli Types*](https://metafunctor.com/latex/bernoulli-monograph/book.html);
the [project hub](https://metafunctor.com/research/bernoulli/) collects the
papers, notes and this package.

## Install

```bash
pip install bernoulli-types
```

The distribution is `bernoulli-types` because the name `bernoulli` is taken on
PyPI; the import name is `bernoulli`. Python 3.11 or later; there are no
runtime dependencies.

From source:

```bash
pip install "git+https://github.com/queelius/bernoulli.git#subdirectory=bernoulli-py"

# or, for development
git clone https://github.com/queelius/bernoulli.git
cd bernoulli/bernoulli-py
pip install -e ".[dev]"          # pytest, pytest-cov, hypothesis, ruff, mypy
pip install -e ".[notebooks]"    # Jupyter, numpy, scipy, matplotlib, sympy
```

## Examples

The examples below are doctests: `python -m doctest README.md` runs them, and
the test suite runs them too.

### A noisy bit

`BernoulliBool` is an observed Boolean plus its channel rates. `&` and `|`
treat both operands as independent observations of the *same* truth (two
classifiers on one input, Miller-Rabin rounds on one `n`), where the rates are
prior-free. `and_with_prior` covers two independent truths.

```pycon
>>> from bernoulli import BernoulliBool, algebra, measures
>>> b1 = BernoulliBool(value=True, fpr=0.10, fnr=0.05)
>>> b2 = BernoulliBool(value=True, fpr=0.08, fnr=0.12)
>>> both = b1 & b2                      # shared truth: fpr1 * fpr2, 1 - (1-fnr1)(1-fnr2)
>>> round(both.fpr, 6), round(both.fnr, 6)
(0.008, 0.164)
>>> round(b1.and_with_prior(b2, prior=0.5).fpr, 4)   # independent truths, prior 1/2
0.0573
>>> algebra.miller_rabin_error(k=10)    # ten one-sided rounds: (1/4)**10
9.5367431640625e-07
>>> round(measures.ppv(fpr=0.05, fnr=0.10, prevalence=0.01), 4)   # base-rate effect
0.1538

```

### Approximate sets

A Bloom filter and a perfect-hash filter both have `fnr = 0`. The perfect
filter (a BBHash minimal perfect hash plus a 10-bit fingerprint per key) needs
the key set up front and pays an additive overhead over the `-log2(fpr)`
floor, where the Bloom filter pays a factor of about 1.44.

```pycon
>>> from bernoulli import BloomFilter, PerfectFilter
>>> from bernoulli.sets.entropy_bound import entropy_floor_bits_per_key
>>> keys = [f"user-{i}".encode() for i in range(5000)]
>>> bloom = BloomFilter(capacity=len(keys), target_fpr=2**-10)
>>> for k in keys:
...     bloom.add(k)
>>> perfect = PerfectFilter(keys, target_fpr=2**-10)
>>> all(bloom.contains(k) and perfect.contains(k) for k in keys)   # no false negatives
True
>>> perfect.fpr()                       # 2**-10, by construction
0.0009765625
>>> others = [f"other-{i}".encode() for i in range(50_000)]
>>> sum(map(perfect.contains, others)) / len(others)   # measured on non-members
0.00094
>>> sum(map(bloom.contains, others)) / len(others)     # the Bloom formula assumes ideal hashes
0.00128
>>> entropy_floor_bits_per_key(2**-10), round(perfect.bits_per_key(), 2), round(bloom.bits_per_key(), 2)
(10.0, 13.35, 14.43)

```

### Composition, and where a rate pair stops being enough

Set operations propagate rates, and the result depends on where the queries
fall (book chapter 6). An intersection's false-positive rate is the product
only for queries outside both sets.

```pycon
>>> from bernoulli import BernoulliBool, Partition, SetRates, formula
>>> from bernoulli.sets.composition import intersection
>>> a = b = SetRates(fpr=0.01, fnr=0.0)
>>> round(intersection(a, b, Partition.sparse()).fpr, 6)   # queries outside A and B
0.0001
>>> in_a = Partition(both=0.0, a_only=1.0, b_only=0.0, neither=0.0)
>>> round(intersection(a, b, in_a).fpr, 6)                 # queries known to be in A
0.01

```

A pair of rates is exact for one operation. It does not compose exactly
through a Boolean tree over different latent bits, because a gate's error
depends on which latent word occurred. `bernoulli.formula` computes the exact
error at any latent word and a worst-case pair that bounds every word:

```pycon
>>> x = formula.variables(3)
>>> f = (x[0] & x[1]) | x[2]
>>> channels = [SetRates(fpr=0.02, fnr=0.10)] * 3
>>> bit = BernoulliBool(value=False, fpr=0.02, fnr=0.10)
>>> round(((bit & bit) | bit).fpr, 6)   # one pair reused at every gate
0.020392
>>> round(formula.error_probability(f, channels, (False, True, False)), 6)   # exact at 010
0.03764
>>> worst = formula.worst_case_rates(f, channels)
>>> round(worst.fpr, 6), round(worst.fnr, 6)
(0.03764, 0.1862)

```

### A codec decides what non-members see

A retrieval structure stores `key -> value` in about `r` bits per key without
storing keys, so a non-member still gets an answer. Through a codec, that
answer follows the codec's codespace shares rather than the stored values:
below, `c` and `d` are never stored but still come back for non-members.

```pycon
>>> from collections import Counter
>>> from bernoulli import EncodedRetrieval, PrefixCodec
>>> codec = PrefixCodec.from_frequencies({"a": 4, "b": 2, "c": 1, "d": 1}, m_bits=4)
>>> sorted(codec.non_member_distribution().items())
[('a', 0.5), ('b', 0.25), ('c', 0.125), ('d', 0.125)]
>>> data = {f"key-{i}".encode(): "ab"[i % 2] for i in range(2000)}
>>> retrieval = EncodedRetrieval(data, codec)
>>> all(retrieval.query(k) == v for k, v in data.items())   # exact on the build set
True
>>> seen = Counter(retrieval.query(f"probe-{i}".encode()) for i in range(20_000))
>>> {v: round(seen[v] / 20_000, 2) for v in "abcd"}
{'a': 0.5, 'b': 0.25, 'c': 0.12, 'd': 0.13}

```

## What is implemented

Everything below is pure Python with no runtime dependencies. The phases
follow the monograph; [PHASING.md](https://github.com/queelius/bernoulli/blob/main/bernoulli-py/PHASING.md)
has the roadmap.

| Phase | Module | Contents |
|---|---|---|
| 1 Atom | `bernoulli.atom` | `BernoulliBool`: noisy bit, `~ & \|`, prior-dependent AND / OR |
| | `bernoulli.algebra` | composition theorem `1 - prod(1 - eta_i)`, k-fold chains, Bloom sizing |
| | `bernoulli.measures` | PPV, NPV, TPR, TNR, Youden's J, F1, MCC, balanced accuracy |
| | `bernoulli.formula` | exact error of Boolean formulas over independent noisy bits: per latent word, worst case, prior-weighted marginal |
| 2 Sets | `bernoulli.sets` | `MembershipOracle` protocol, `BloomFilter` |
| | `bernoulli.sets.composition` | `SetRates`, `Partition`; union, intersection, complement, difference |
| | `bernoulli.sets.entropy_bound` | `-log2(fpr)` floor, Bloom 1.44x overhead, perfect-filter space model |
| | `bernoulli.sets.cascade`, `.correlated_bloom` | research helpers: Bloom cascades, filters with shared hash salts |
| 3 Maps | `bernoulli.maps` | `PerfectHashFunction`, `ApproximateMap` protocols; `MinimalPerfectHash` (BBHash); `PerfectFilter` |
| | `bernoulli.maps.codec` | `DenseCodec`, `PaddedCodec`, `PrefixCodec` (Huffman), `shannon_entropy` |
| | `bernoulli.maps.retrieval` | `GF2Retrieval` (peeling), `EncodedRetrieval` (retrieval plus codec) |
| 4 Relations | `bernoulli.relations` | `BernoulliRelation`: exact tuples carrying membership rates through select, project, join |
| 5 Sketches | `bernoulli.sketches` | `CountMinSketch`, `HyperLogLog`, `MinHash` |
| | `bernoulli.algorithms` | Miller-Rabin as a one-sided Bernoulli bit; a configurable noisy classifier |
| Tools | `bernoulli.harness`, `bernoulli.bench` | measured rates with Wilson intervals; best-of-N timing |

Not implemented yet:

- **C acceleration.** There is no C code. `c/` holds a design note for a
  planned optional cffi core with pure-Python fallbacks, and no `[c]` extra is
  offered until it exists.
- The banded ribbon solver (the peeling construction is the reference), Las
  Vegas and Monte Carlo adapters, and an approximate relation store.

The repository also holds 16 validation experiments
([experiments/](https://github.com/queelius/bernoulli/tree/main/bernoulli-py/experiments),
summarized in `SYNTHESIS.md`) and 15 notebooks that accompany the monograph
([notebooks/](https://github.com/queelius/bernoulli/tree/main/bernoulli-py/notebooks)).
Neither ships in the wheel.

## Limits

- **No security claims.** The hashes are FNV-1a and splitmix64, chosen for
  speed and reproducibility. They are not cryptographic, and nothing in this
  package supports a claim about adversaries, privacy or secrecy.
- **Rate pairs are summaries.** A single `(fpr, fnr)` is exact for one gate or
  one set operation, and `&` / `|` are exact for read-once AND / OR trees of
  independent observations of one bit. Through a general Boolean formula over
  different latent bits, reusing pairs can understate the error (0.020392
  against 0.03764 in the example above). Use `bernoulli.formula` for exact
  per-word values or a sound worst-case pair.
- **Independence is assumed, not checked.** The composition rules assume
  independent error events across operands. Filters that share hash
  randomness, or an operand used twice, violate it; experiment 01 measures a
  19x error when two Bloom filters share salt and keys.
- **Composition works on rates, not on live structures.** `SetRates` and
  `Partition` propagate numbers. There is no `bloom_a & bloom_b` that returns
  a queryable filter.
- **`BernoulliRelation` is not an approximate store.** It keeps exact tuples;
  its `rates` describe what an approximate representation would do.
- **No save or load.** Nothing is serializable yet.
- **Static structures.** `MinimalPerfectHash`, `PerfectFilter` and
  `GF2Retrieval` are built once from a known key set. Keys are `bytes`.
- **Speed.** Pure Python suits experiments, teaching and moderate key counts,
  not production throughput.
- **Reported rates are models.** `BloomFilter.fpr()` is the asymptotic formula
  at the current load and `PerfectFilter.fpr()` is `2**-r`; measured rates on
  real keys differ (see the Bloom example). `bernoulli.harness` measures them.

## Development

From `bernoulli-py/`:

```bash
uv venv && VIRTUAL_ENV="$PWD/.venv" uv pip install -e ".[dev]"
.venv/bin/python -m pytest --cov=bernoulli --cov-branch --cov-report=term-missing
.venv/bin/ruff check src tests
.venv/bin/mypy
```

The changelog is
[CHANGELOG.md](https://github.com/queelius/bernoulli/blob/main/bernoulli-py/CHANGELOG.md).

## Citing

See [CITATION.cff](https://github.com/queelius/bernoulli/blob/main/bernoulli-py/CITATION.cff).
For the theory, cite the monograph.

## License

MIT; see [LICENSE](https://github.com/queelius/bernoulli/blob/main/bernoulli-py/LICENSE).

## Author

Alexander Towell (`lex@metafunctor.com`,
ORCID [0000-0001-6443-9897](https://orcid.org/0000-0001-6443-9897)),
Southern Illinois University Edwardsville.
