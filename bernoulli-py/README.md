# bernoulli

> Random approximate types as a *type theory*, not a parade of clever tricks.
> Bloom filters, perfect-hash filters, ribbon retrieval, and noisy classifiers
> are instances of one model, with one composition algebra.

`bernoulli` is a Python package, backed by a small C core for hot paths,
that implements the **Bernoulli framework** for random approximate types.
The package serves two audiences:

1. A **research artifact** for running experiments on approximate-data-structure
   algorithms (Bloom, BHF, perfect-hash filters, ribbon retrieval, codecs,
   classification measures) with a unified error model.
2. A **PyPI package** for working scientists and practitioners who want
   principled error propagation rather than ad-hoc per-data-structure folklore.

The framework is the subject of nine papers and a book in progress
(`../book/`); this package is the executable companion.

## Status

**Alpha (0.2.0).** Phase 1 (the atom, Boolean algebra, classification measures)
is implemented in pure Python. Phases 2 through 5 (sets, maps, relations,
sketches) are scaffolded with protocols and will land incrementally with
optional C acceleration. See [`PHASING.md`](PHASING.md).

## Install

```bash
pip install -e .
pip install -e ".[dev]"          # tests + lint + type-check
pip install -e ".[c]"            # cffi for C-backed primitives (Phase 2+)
pip install -e ".[notebooks]"    # Jupyter + matplotlib + numpy
```

## Quick taste

```python
from bernoulli import BernoulliBool

# A noisy classifier output: claims true with FPR alpha=0.10 and FNR beta=0.05
b1 = BernoulliBool(value=True, fpr=0.10, fnr=0.05)
b2 = BernoulliBool(value=True, fpr=0.08, fnr=0.12)

# AND / OR propagate rates per book ch.3
both = b1 & b2          # distribution-free FNR; min-bound FPR
either = b1 | b2        # distribution-free FPR; min-bound FNR

# When you know the prior, get the exact rate
both_exact = b1.and_with_prior(b2, prior=0.5)
print(both_exact.fpr, both_exact.fnr)

# k-fold AND chain (Miller-Rabin pattern)
from bernoulli.algebra import composition_homogeneous
fpr_after_k = composition_homogeneous(rate=0.25, k=10)  # ~ 5.6e-7

# Classification measures
from bernoulli.measures import ppv, npv, youden_j
print(ppv(fpr=0.05, fnr=0.10, prevalence=0.01))   # PPV at low prevalence
print(youden_j(fpr=0.05, fnr=0.10))                # informedness
```

## Why a separate package from `python/bernoulli`?

The `bernoulli/python/` tree is a teaching skeleton tied chapter-by-chapter
to the textbook notebooks. This `src/bernoulli/` tree is the production
implementation: complete model coverage, C-backed where it matters, suitable
for paper experiments and PyPI release. The two will reconcile (the teaching
notebooks will eventually import from this package); for now they coexist.

## Relationship to `maph`

The C++ research playground at `~/github/repos/maph/` is the algorithm sandbox.
Empirical findings that prove out there get ported here, with the
maph-equivalent referenced for traceability:

| `bernoulli` | `maph` reference |
|---|---|
| `bernoulli.sets.MembershipOracle` | `concepts/membership_oracle.hpp` |
| `bernoulli.maps.ApproximateMap` | `concepts/approximate_map.hpp` |
| `bernoulli.maps.PerfectHashFunction` | `concepts/perfect_hash_function.hpp` |
| `bernoulli.sets.bloom` (Phase 2) | conventional Bloom filter |
| `bernoulli.maps.perfect_filter` (Phase 3) | `composition/perfect_filter.hpp` |
| `bernoulli.maps.codec` (Phase 3) | `codecs/prefix_codec.hpp` |
| `bernoulli.maps.ribbon_retrieval` (Phase 3) | `retrieval/ribbon_retrieval.hpp` |

## Layout

```
src/bernoulli/
|-- pyproject.toml
|-- README.md         (you are here)
|-- PHASING.md        (roadmap)
|-- LICENSE           (MIT)
|-- src/
|   `-- bernoulli/
|       |-- atom.py        (BernoulliBool: the noisy bit)
|       |-- algebra.py     (composition theorem, k-fold chains)
|       |-- measures.py    (PPV, NPV, J, F1, MCC)
|       |-- sets/          (MembershipOracle protocol; Bloom, etc.)
|       `-- maps/          (PerfectHashFunction, ApproximateMap protocols)
|-- c/                (C source for Phase 2+ acceleration)
`-- tests/
```

## License

MIT. See [`LICENSE`](LICENSE).

## Author

Alexander Towell, `lex@metafunctor.com`.
ORCID: [0000-0001-6443-9897](https://orcid.org/0000-0001-6443-9897).
