# bernoulli

> **The type, not the data structure.**

A teaching-oriented Python implementation of the Bernoulli framework for
random approximate types. Not a Bloom-filter package; a library for
tracking error rates through type composition.

## Status

Alpha. Public API and behavior may change.

## Install

```bash
pip install bernoulli
```

Or, from this repo:

```bash
pip install -e .
pip install -e ".[dev]"          # with development tooling
pip install -e ".[notebooks]"    # with Jupyter and matplotlib
```

## Quick Start

```python
from bernoulli import Bernoulli

# Placeholder API; full implementation coming in Plan 1+.
b = Bernoulli(value=True)
print(b.value)
```

## Notebooks

Notebooks live in `notebooks/`, paired chapter-by-chapter with the textbook
*Bernoulli Types: An Algebra of Approximate Computation* (`../book/`). Not
every chapter has a notebook; some are theory-only by design.

## Development

```bash
pytest                  # run smoke tests
ruff check src tests    # lint
mypy src                # type-check
```

## License

MIT. See `LICENSE`.

## Author

Alexander Towell, `lex@metafunctor.com`.
