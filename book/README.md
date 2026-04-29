# Bernoulli Types: An Algebra of Approximate Computation

A pedagogical monograph unifying probabilistic data structures, randomized
algorithms, noisy channels, and approximate functions under the Bernoulli
type framework.

> **Status:** scaffolding complete; chapter content in progress.

## Build

```bash
make            # full build (pdflatex + bibtex + pdflatex + pdflatex)
make draft      # single pdflatex pass (fast iteration; bibliography stale)
make watch      # rebuild on file changes (requires inotifywait)
make clean      # remove auxiliary files but keep the PDF
make cleanall   # remove everything including the PDF
```

The output is `book.pdf`.

## Structure

- `book.tex`: document root, inputs preamble and parts.
- `preamble.tex`: `\usepackage` calls and document-wide macros.
- `alex.sty`: unified notation package shared with the source papers.
- `frontmatter/`: title page, copyright, preface.
- `parts/`: five thin wrappers (`\part` plus `\input` chapters).
- `chapters/`: eighteen chapter sources.
- `appendices/`: probability refresher, principles cheat sheet, library walkthrough, selected solutions.
- `figures/`, `code/`: graphics and code listings.
- `references.bib`: bibliography.

## Companion Library

The Python library `bernoulli` lives at `../python/`. See its README for
installation and notebook conventions.

## Source Repositories

- Book sources: `https://github.com/queelius/bernoulli-book` (subtree push planned)
- Underlying papers: `https://github.com/queelius/bernoulli` (this monorepo)

## License

Prose: CC BY-NC-SA 4.0 (see `LICENSE`).
Code samples: MIT.

## Author

Alexander Towell, `lex@metafunctor.com`, ORCID `0000-0001-6443-9897`.
