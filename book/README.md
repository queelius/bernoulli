# Bernoulli Types: Two-Sided Error in Approximate Membership, Retrieval, and Computation

A research monograph on one object: a query that returns a bit, observed
through a binary channel with a false-positive rate and a false-negative rate.
Bloom filters, retrieval structures and perfect hash filters, randomized
algorithms, approximate relational queries, encrypted indexes, and quantum
readout are all read through that channel.

The contribution is a unification, not a set of new theorems. Most individual
results have named predecessors (randomized response, Carter et al. on
approximate membership, Pagh and Rodler on lossy dictionaries, Parker and
McCluskey on gate-level error propagation, Gallager's parity lemma,
Dietzfelbinger and Pagh on retrieval, Decaf on probability types, Fuhr and
Rölleke on probabilistic relational algebra, and others). Every chapter ends
with a *Notes and Lineage* section that credits them, says what the chapter
adds, and says what it leaves out. The book also maps the model's limits: a
rate pair does not propagate through a Boolean formula (exact propagation is
per latent input assignment), and dependence, adaptivity, and shared
intermediate values each break the independence the model needs.

> **Status:** complete draft, 19 chapters in five parts, three appendices,
> bibliography and index. Apparatus pass of October 2026: lineage notes,
> corrections of earlier claims (listed in Appendix B), figures, index.

## Build

```bash
make            # full build: pdflatex, biber, makeindex, pdflatex, makeindex, pdflatex
make draft      # single pdflatex pass (fast iteration; bibliography and index stale)
make watch      # rebuild on file changes (requires inotifywait)
make clean      # remove auxiliary files but keep the PDF
make cleanall   # remove everything including the PDF
```

Requires a TeX Live installation with `biber`, `biblatex`, `imakeidx`,
`makeindex`, `tikz`, and `pgfplots`. The output is `book.pdf`.

## Structure

- `book.tex`: document root; inputs the preamble, front matter, parts,
  appendices, bibliography, and index.
- `preamble.tex`: packages, PDF metadata, bibliography and index setup, and
  book-specific macros.
- `alex.sty`: notation package shared with the source papers.
- `book.ist`: makeindex style.
- `frontmatter/`: title page, copyright and license page, preface.
- `parts/`: five thin wrappers (`\part` plus `\input` of chapters).
- `chapters/`: nineteen chapter wrappers, each inputting its section files
  from `chapters/chNN/`.
- `appendices/`: A, notation and conventions; B, principles and their scope
  (with the table of corrected statements); C, companion code and notebooks.
- `references.bib`: biblatex bibliography.

## Companion package

The Python package `bernoulli-types` (import name `bernoulli`) lives at
`../bernoulli-py/`, with chapter notebooks in `../bernoulli-py/notebooks/`.
Appendix C indexes the modules and notebooks by chapter.

## Source manuscripts

The book supersedes the program's paper manuscripts in `../papers/` where they
differ; Appendix B lists the corrected statements.

## Tooling

The project is managed with the
[bookwright](https://github.com/queelius/alex-claude-plugins) Claude Code
plugin; its settings are in `../docs/superpowers/bookwright.config.yaml`
(`/bookwright:check`, `/bookwright:review`, `/bookwright:integrate`).

## License

Text: CC BY 4.0 (see `LICENSE`).
Embedded code and the companion package: MIT.

Drafting and verification were assisted by AI tools (Anthropic Claude and
OpenAI Codex); the author is responsible for all content.

## Author

Alexander Towell, `lex@metafunctor.com`, ORCID `0000-0001-6443-9897`.
