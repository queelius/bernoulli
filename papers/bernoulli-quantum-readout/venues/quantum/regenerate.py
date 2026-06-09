#!/usr/bin/env python3
"""Regenerate the Quantum (quantumarticle) version from the venue-neutral base.

The base ../../main.tex is the single source of truth. This script takes the base
verbatim from \\numberwithin onward (the theorem environments, the notation macros,
and the entire body) and prepends the quantumarticle preamble and title block, so
every change to the base math or prose propagates here automatically. Only the
venue package set and the title block below are venue-specific. Run after any
substantive base edit:

    python3 regenerate.py
"""
import pathlib
import shutil

HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE.parents[1] / "main.tex"

VENUE_PREAMBLE = r"""\pdfoutput=1
% nopdfoutputerror + allowtoday: quantumarticle v6.1's pdfoutput/today guards
% mis-fire on the TeX Live 2023 kernel even when set; we compile with real
% pdflatex. Remove these options if the class is updated.
\documentclass[a4paper,onecolumn,unpublished,nopdfoutputerror,allowtoday]{quantumarticle}

% GENERATED from ../../main.tex by regenerate.py; edit the base, not this file.
% quantumarticle supplies geometry, fonts, hyperref, and amsmath.
\usepackage{amssymb}
\usepackage{amsthm}
\usepackage{mathtools}
\usepackage{booktabs}
\usepackage{array}
\usepackage{enumitem}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage[numbers,square]{natbib}
\bibliographystyle{plainnat}
\usepackage{hyperref}   % explicit, so cleveref orders after it
\usepackage{cleveref}

"""

VENUE_TITLE = r"""\title{A Forward \texorpdfstring{$(\eps,\omega)$}{(epsilon, omega)} Calculus for
Quantum Readout Error and the Classical Post-Processing of Measurement Outcomes}

% quantumarticle renders \email as a page-bottom footnote and \orcid only as a
% hyperlink on the author's name (no visible number). To keep the contact block
% visible (parity with the base title page), the affiliation also shows the email
% and ORCID as text; \orcid is kept so the name still links to the ORCID record.
\author{Alexander Towell}
\orcid{0000-0001-6443-9897}
\affiliation{Southern Illinois University Edwardsville \\
  \texttt{atowell@siue.edu} \\ ORCID: 0000-0001-6443-9897}

\date{\today}

"""


def main():
    base = BASE.read_text()
    macros = base[base.index(r"\numberwithin"):base.index(r"\title")]
    body = base[base.index(r"\begin{document}"):]
    (HERE / "main.tex").write_text(VENUE_PREAMBLE + macros + VENUE_TITLE + body)
    shutil.copy(BASE.parent / "references.bib", HERE / "references.bib")
    print("regenerated venues/quantum/main.tex + references.bib from the base")


if __name__ == "__main__":
    main()
