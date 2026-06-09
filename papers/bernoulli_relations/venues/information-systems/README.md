# venues/information-systems

Target venue: *Information Systems* (Elsevier).

## Submission format: the base is ready as-is

Elsevier operates a "Your Paper Your Way" policy: the **initial** submission may be
in any reasonable format and document class. The venue-neutral base
(`../../main.tex`, `article` class, builds clean at 22 pages) is therefore
submission-ready without modification. The Elsevier `elsarticle` formatting is only
required **after acceptance**, at the revision stage.

So, for the initial submission, use the base PDF plus `cover-letter.md` here. Do not
spend effort on the `elsarticle` port until the paper is accepted in principle.

## The elsarticle port (deferred to acceptance)

The base is a modular-sty paper (`../../sty/` notation packages, `\subfile`d
sections, `minted`), so the `elsarticle` port is a non-trivial preamble-and-package
reconciliation, best done once when it is actually required. When that time comes,
follow the same pattern as `bernoulli-quantum-readout/venues/quantum/` (a
`regenerate.py` that prepends the venue preamble and reuses the base body), loading
the `../../sty/` packages via `TEXINPUTS` and resolving the conflicts `elsarticle`
raises with `geometry`, `microtype`, `caption`, and `subcaption`.

## Files

- `cover-letter.md`: the submission cover letter (venue-neutral content; reusable).
