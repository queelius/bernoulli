# Notebooks

This directory holds the Jupyter notebooks that accompany the monograph
*Bernoulli Types: Two-Sided Error in Approximate Membership, Retrieval, and
Computation* (`../../book/`).

## Conventions

- One notebook per book chapter that has companion code, named
  `chXX-<short-topic>.ipynb`.
- Chapters 4, 13, 17, and 19 are theoretical and have no notebook, as the
  book's preface states; the book's appendix "Companion Code and Notebooks"
  indexes the fifteen notebooks below.
- Each notebook opens with a pointer to the chapter it accompanies and, where
  practical, asserts the chapter's numbers, so a notebook that runs to the end
  has checked them. Notebooks are committed with their outputs.

## Running

```bash
pip install -e "..[notebooks]"
jupyter lab .
```

To execute a notebook non-interactively and keep its outputs:

```bash
jupyter nbconvert --to notebook --execute --inplace ch14-bhf.ipynb
```

## Notebooks

| Chapter | Notebook |
|---|---|
| 1 | `ch01-noisy-bit.ipynb` |
| 2 | `ch02-binary-channels.ipynb` |
| 3 | `ch03-boolean-algebra-noise.ipynb` |
| 5 | `ch05-approximate-sets.ipynb` |
| 6 | `ch06-set-composition.ipynb` |
| 7 | `ch07-classification-measures.ipynb` |
| 8 | `ch08-information-bounds.ipynb` |
| 9 | `ch09-approximate-functions.ipynb` |
| 10 | `ch10-sketches-estimators.ipynb` |
| 11 | `ch11-randomized-algorithms.ipynb` |
| 12 | `ch12-approximate-relations.ipynb` |
| 14 | `ch14-bhf.ipynb` |
| 15 | `ch15-bphf.ipynb` |
| 16 | `ch16-not-bernoulli.ipynb` |
| 18 | `ch18-encrypted-search.ipynb` |
