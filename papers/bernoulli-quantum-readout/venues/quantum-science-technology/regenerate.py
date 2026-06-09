#!/usr/bin/env python3
"""Regenerate the Quantum Science and Technology (IOP) initial-submission build.

IOP takes an initial submission as a single PDF in any common TeX format; the
iopart class is required only at the revision stage, after peer review. The only
venue-specific need for the initial PDF is IOP's readability request of at least
12 point, so this script reuses the venue-neutral base verbatim and flips the
document class option from 11pt to 12pt. The base ../../main.tex stays the single
source of truth; rerun after any base edit:

    python3 regenerate.py
    pdflatex main && bibtex main && pdflatex main && pdflatex main
"""
import pathlib
import shutil

HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE.parents[1] / "main.tex"

OLD = r"\documentclass[11pt]{article}"
NEW = r"\documentclass[12pt]{article}"


def main():
    src = BASE.read_text()
    if OLD not in src:
        raise SystemExit(f"expected {OLD!r} in base main.tex; did the base change?")
    (HERE / "main.tex").write_text(src.replace(OLD, NEW, 1))
    shutil.copy(BASE.parent / "references.bib", HERE / "references.bib")
    print("regenerated venues/quantum-science-technology/main.tex (12pt) + references.bib")


if __name__ == "__main__":
    main()
