# Bernoulli types

A unified error model for approximate computation, by
[Alexander Towell](https://metafunctor.com) (ORCID
[0000-0001-6443-9897](https://orcid.org/0000-0001-6443-9897)).

An approximate structure answers each query through a noisy binary channel:
a false-positive rate (truth 0, reported 1) and a false-negative rate (truth 1,
reported 0). This repository develops that single model across Booleans, sets,
maps, relations and algebraic types. It gives Bloom filters, retrieval tables,
perfect hash filters, randomized algorithms, approximate relational queries and
quantum readout post-processing one vocabulary. It also states where the model
breaks: dependence, adaptive queries, and the fact that two-rate summaries do
not compose exactly.

**What this is and is not.** The contribution is the unification, an honest map
of its limits, and an executable companion. Most of the individual results have
named predecessors, and the monograph credits them. Examples:

- randomized response (Warner 1965);
- the parity lemma (Gallager 1962);
- probabilistic circuit analysis (Parker and McCluskey 1975);
- approximate-membership space bounds (Carter et al. 1978; Pagh and Rodler
  2001);
- MPHF-plus-fingerprint filters (Dietzfelbinger and Pagh 2008);
- probability types (Decaf, 2015);
- probabilistic relational algebra (Fuhr and Rölleke 1997).

The prior-art audits are in [`.research/`](.research/), starting with
[`.research/program-strategy/`](.research/program-strategy/README.md).

## Contents

| Path | What it is |
|---|---|
| [`book/`](book/) | The monograph *Bernoulli Types: An Algebra of Approximate Computation*. Read it [online](https://metafunctor.com/latex/bernoulli-monograph/book.html) or as a [PDF](https://metafunctor.com/latex/bernoulli-monograph/bernoulli-monograph.pdf). |
| [`bernoulli-py/`](bernoulli-py/) | The Python reference implementation (`import bernoulli`; distribution name `bernoulli-types`). Pure Python, zero runtime dependencies, with property-based tests, experiments and book-companion notebooks. |
| [`papers/`](papers/) | The ten focused preprints that preceded the monograph, each archived on Zenodo; DOIs in [`docs/PROVENANCE.md`](docs/PROVENANCE.md). |
| [`.research/`](.research/) | Audit trail: prior-art reviews, counterexamples, exhaustive finite checks and negative results, kept so that claims stay checkable. |
| [`archived/`](archived/) | The retired C++ reference implementation (design reference only). |

The research hub, with papers, posts and status, is
[metafunctor.com/research/bernoulli](https://metafunctor.com/research/bernoulli/).

## Quick start

```bash
cd bernoulli-py
uv venv && VIRTUAL_ENV="$PWD/.venv" uv pip install -e ".[dev]"
.venv/bin/python -m pytest
```

The book builds with `make -C book` (pdflatex and biber). For paper builds, see
[`papers/CLAUDE.md`](papers/CLAUDE.md).

## License

Monograph and papers: CC BY 4.0. Code: MIT. See each component's `LICENSE`.

## Related

- [trapdoor-computing](https://github.com/queelius/trapdoor-computing): the
  security program that uses this error model (cipher maps).
- [lapidary](https://github.com/queelius/lapidary): C++ constructions
  (perfect hashing, xor and ribbon retrieval).
