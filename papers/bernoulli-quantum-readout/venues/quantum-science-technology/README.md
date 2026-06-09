# venues/quantum-science-technology

Target venue: *Quantum Science and Technology* (IOP Publishing). Active submission
target for the quantum-readout paper.

## Why this venue

*Quantum* (quantum-journal.org) was the first choice on audience fit, but it makes
arXiv posting (quant-ph) a necessary condition of submission, which the author's
no-arXiv-endorser situation blocks. The `venues/quantum/` port (quantumarticle) is
therefore on hold pending arXiv access, not deleted. *Quantum Science and
Technology* is the chosen no-arXiv home: a strong scope match for a forward
error-budgeting calculus, with a free subscription-access publication route (gold
open access optional), and no preprint requirement.

## Submission format: the base is ready, at 12pt

IOP takes an **initial** submission as a single PDF in any common TeX format; the
`iopart` class is required only at the **revision** stage, through ScholarOne. The
one venue-specific need for the initial PDF is IOP's readability request of at least
12 point. `regenerate.py` produces that build by reusing the venue-neutral base
(`../../main.tex`) verbatim and flipping the document class option from 11pt to
12pt; the base stays the single source of truth.

```bash
python3 regenerate.py
pdflatex main && bibtex main && pdflatex main && pdflatex main   # 17 pp, 0 undefined refs
```

So the initial submission is `main.pdf` here plus `cover-letter.md`. Regenerate
after any substantive base edit.

## The iopart port (deferred to acceptance)

Defer the full `iopart` formatting until the paper is accepted in principle, the
same policy we follow for the Elsevier (`bernoulli_relations`) target. When that
time comes, port the preamble to `iopart`, move the bibliography to the IOP
`iopart-num` style, and reconcile `pgfplots`, `natbib`, and `cleveref` against the
class.

## Files

- `regenerate.py`: builds the 12pt initial-submission `.tex` from the base.
- `main.pdf`: the 12pt initial-submission PDF (gitignored build artifact; regenerate).
- `cover-letter.md`: the QST submission cover letter.
