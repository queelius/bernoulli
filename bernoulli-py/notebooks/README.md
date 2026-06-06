# Notebooks

This directory holds Jupyter notebooks paired with chapters of the textbook
*Bernoulli Types: An Algebra of Approximate Computation* (`../../book/`).

## Conventions

- One notebook per book chapter that has companion code.
- Filename pattern: `chXX-<short-topic>.ipynb` (matching the book's
  chapter source filenames in `book/chapters/`).
- Not every chapter has a notebook. Theory-heavy chapters (4, 13, 16, 17)
  are intentionally notebook-free; this is documented in the book preface.
- Each notebook starts with a markdown cell pointing back to the book
  section it accompanies and ends with cross-references to the next
  notebook in sequence.

## Running

```bash
pip install -e "..[notebooks]"
jupyter lab .
```

## Notebooks (planned)

Notebooks are added in subsequent plans alongside their chapters. The
expected set after all chapter plans complete:

| Chapter | Notebook | Plan |
|---|---|---|
| 1 | `ch01-noisy-bit.ipynb` | Plan 1 |
| 2 | `ch02-binary-channels.ipynb` | Plan 1 |
| 3 | `ch03-boolean-algebra-noise.ipynb` | Plan 1 |
| 5 | `ch05-approximate-sets.ipynb` | Plan 2 |
| 6 | `ch06-set-composition.ipynb` (light) | Plan 2 |
| 7 | `ch07-classification-measures.ipynb` | Plan 2 |
| 8 | `ch08-information-bounds.ipynb` (light) | Plan 2 |
| 9 | `ch09-approximate-functions.ipynb` | Plan 3 |
| 10 | `ch10-sketches-estimators.ipynb` | Plan 3 |
| 11 | `ch11-randomized-algorithms.ipynb` | Plan 3 |
| 12 | `ch12-approximate-relations.ipynb` | Plan 3 |
| 14 | `ch14-optimal-bernoulli-sets.ipynb` | Plan 4 |
| 15 | `ch15-perfect-hash-filters.ipynb` | Plan 4 |
| 16 | `ch16-not-bernoulli.ipynb` (light) | Plan 4 |
| 18 | `ch18-encrypted-search.ipynb` | Plan 4 |

Chapters 4, 13, 17 are theory-only.
