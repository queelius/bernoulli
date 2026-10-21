#!/usr/bin/env python3
"""Inject the book's LaTeX macros into make4ht's MathJax configuration.

make4ht in ``mathjax`` mode leaves math as raw TeX, including this book's own
macros (``\\fprate``, ``\\ASet``, ...), which MathJax does not know. This tool
parses the macro definitions in the given style files with a brace-matching
scanner, converts them to a MathJax v3 ``tex.macros`` table, and rewrites the
page's ``window.MathJax`` configuration line to carry it.

xparse (``\\NewDocumentCommand``) and mathtools paired-delimiter macros cannot be
translated mechanically; ``BARE_FORMS`` gives the bare forms the book uses
(no optional arguments, no star). ``--check`` reports any backslash command
that appears inside math in the page and is neither defined here nor a MathJax
built-in from ``KNOWN_MATHJAX``, so a new macro is caught instead of rendering as
an error.

It also fills the page <title> (tex4ht leaves it empty when \\maketitle is
never called, as with this book's custom title page) via --title.

Usage:
    python3 tools/mathjax_macros.py PAGE.html STYLE.sty [STYLE.tex ...] [--check] [--title=TEXT]
"""

from __future__ import annotations

import html
import json
import sys
from html.parser import HTMLParser
from dataclasses import dataclass
from pathlib import Path

DEFINERS = ("\\newcommand", "\\renewcommand", "\\providecommand", "\\DeclareMathOperator")

# Bare forms of the xparse / paired-delimiter macros as the book uses them.
BARE_FORMS: dict[str, str | list] = {
    "ASet": ["{\\setstyle{#1}}^{\\pm}", 1],
    "Set": ["\\setstyle{#1}", 1],
    "Prob": ["\\ProbFn\\left(#1\\right)", 1],
    "Expect": ["\\mathrm{E}\\left[#1\\right]", 1],
    "Var": ["\\mathrm{Var}\\left(#1\\right)", 1],
    "Card": ["\\left\\lvert #1\\right\\rvert", 1],
    "ket": ["\\left|#1\\right\\rangle", 1],
    "bra": ["\\left\\langle#1\\right|", 1],
    "Fun": ["\\funstyle{#1}", 1],
    "APFun": ["{\\funstyle{#1}}^{\\pm}", 1],
    "FuncSty": ["\\mathrm{#1}", 1],
    "Unit": "\\mathbf{1}",
}
# Fallbacks for macros that come from packages MathJax lacks.
FALLBACKS: dict[str, str | list] = {
    "mathbbm": ["\\mathbb{#1}", 1],
    "funstyle": ["\\mathrm{#1}", 1],
    "funsubstyle": ["\\mathrm{#1}", 1],
    "funsupstyle": ["\\mathrm{#1}", 1],
    # Text commands that LaTeX tolerates in math but MathJax's base TeX lacks.
    "emph": ["\\textit{#1}", 1],
    "textsc": ["\\text{#1}", 1],
    # cleveref inside \tag{...}: MathJax resolves \ref against its own labels.
    "Cref": ["\\text{Eq. }\\ref{#1}", 1],
    "cref": ["\\text{eq. }\\ref{#1}", 1],
}


@dataclass(frozen=True)
class Definition:
    name: str
    body: str
    nargs: int
    operator: bool = False


def _group(text: str, i: int) -> tuple[str, int]:
    """Return the balanced {...} group starting at text[i] == '{' and the index after it.

    A backslash escapes the next character, so \\{ and \\} do not count and \\\\ is
    a single escaped backslash.
    """
    assert text[i] == "{", text[i : i + 20]
    depth = 0
    j = i
    while j < len(text):
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1 : j], j + 1
        j += 1
    raise ValueError(f"unbalanced group at offset {i}: {text[i : i + 60]!r}")


def _read_cs(text: str, i: int) -> tuple[str, int]:
    """Read a control-sequence name \\letters at text[i]; return ('', i) if none."""
    if i >= len(text) or text[i] != "\\":
        return "", i
    j = i + 1
    while j < len(text) and text[j].isalpha():
        j += 1
    return (text[i + 1 : j], j) if j > i + 1 else ("", i)


def _skip_space(text: str, i: int) -> int:
    while i < len(text) and text[i] in " \t\n":
        i += 1
    return i


def _strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        k = 0
        while True:
            k = line.find("%", k)
            if k == -1 or k == 0 or line[k - 1] != "\\":
                break
            k += 1
        out.append(line if k == -1 else line[:k])
    return "\n".join(out)


def parse_definitions(text: str) -> list[Definition]:
    """Scan for \\newcommand-family and \\DeclareMathOperator definitions."""
    text = _strip_comments(text)
    defs: list[Definition] = []
    i = 0
    while True:
        hits = [(text.find(d, i), d) for d in DEFINERS]
        hits = [(k, d) for k, d in hits if k != -1]
        if not hits:
            return defs
        k, definer = min(hits)
        j = k + len(definer)
        if j < len(text) and text[j].isalpha():  # e.g. \newcommandx: not ours
            i = j
            continue
        operator = definer == "\\DeclareMathOperator"
        star = j < len(text) and text[j] == "*"
        if star:
            j += 1
        j = _skip_space(text, j)
        if j < len(text) and text[j] == "{":
            name, j = _group(text, j)
        else:  # \newcommand\foo form
            name, j = _read_cs(text, j)
            if not name:
                i = j
                continue
        name = name.strip().lstrip("\\")
        j = _skip_space(text, j)
        nargs = 0
        if not operator and j < len(text) and text[j] == "[":
            close = text.index("]", j)
            nargs = int(text[j + 1 : close])
            j = _skip_space(text, close + 1)
            if j < len(text) and text[j] == "[":  # optional-argument default: unsupported
                i = j
                continue
        if j >= len(text) or text[j] != "{":
            i = j
            continue
        body, j = _group(text, j)
        if operator:
            body = ("\\operatorname*{%s}" if star else "\\operatorname{%s}") % body
        defs.append(Definition(name, body.strip(), nargs, operator))
        i = j


def macro_table(paths: list[Path]) -> dict[str, str | list]:
    table: dict[str, str | list] = {}
    for p in paths:
        for d in parse_definitions(p.read_text(encoding="utf-8")):
            table[d.name] = [d.body, d.nargs] if d.nargs else d.body
    table.update(BARE_FORMS)
    for k, v in FALLBACKS.items():
        table.setdefault(k, v)
    return table


def inject(page: Path, table: dict[str, str | list]) -> None:
    """Rewrite the line holding make4ht's window.MathJax config (idempotent)."""
    lines = page.read_text(encoding="utf-8").split("\n")
    config = 'window.MathJax = { tex: { tags: "ams", macros: %s }, };' % json.dumps(table)
    for n, line in enumerate(lines):
        if "window.MathJax" in line and "tex:" in line:
            indent = line[: len(line) - len(line.lstrip())]
            lines[n] = indent + config
            break
    else:
        raise SystemExit(f"no window.MathJax config line in {page}")
    # tex4ht marks \mathrm inside section titles with '@@'; MathJax shows it literally.
    page.write_text("\n".join(lines).replace("@@", ""), encoding="utf-8")


def set_title(page: Path, title: str) -> None:
    """Replace the contents of the page's single <title> element."""
    text = page.read_text(encoding="utf-8")
    start, end = text.find("<title>"), text.find("</title>")
    if start == -1 or end < start:
        raise SystemExit(f"no <title> element in {page}")
    start += len("<title>")
    page.write_text(text[:start] + html.escape(title, quote=False) + text[end:], encoding="utf-8")


# MathJax v3 built-ins the book uses (ams, base, mathtools-free subset).
KNOWN_MATHJAX = set(
    """alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi pi
    rho sigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda Xi Pi Sigma Phi Psi Omega
    frac dfrac tfrac binom sqrt sum prod int lim log ln exp min max sup inf arg det Pr left right big Big
    bigg Bigg middle cdot cdots ldots dots vdots ddots times div pm mp le leq ge geq ne neq approx sim
    simeq equiv propto in notin subset subseteq supset supseteq cup cap setminus emptyset varnothing
    forall exists neg lnot land lor wedge vee oplus otimes odot circ to mapsto rightarrow leftarrow
    Rightarrow Leftarrow iff implies infty partial nabla mathbb mathbf mathrm mathit mathcal mathsf
    mathtt mathfrak boldsymbol text textbf textit textrm textsf texttt operatorname quad qquad hat
    bar tilde vec dot ddot overline underline overbrace underbrace widehat widetilde lvert rvert lVert
    rVert vert Vert langle rangle lceil rceil lfloor rfloor mid nmid parallel top bot perp ell hbar
    begin end label ref eqref tag nonumber notag displaystyle textstyle scriptstyle limits nolimits
    stackrel overset underset xrightarrow xleftarrow mathop mathrel mathbin mathord mathopen mathclose
    colon prime backslash lbrace rbrace star ast bullet triangle triangleq coloneqq phantom hphantom
    vphantom mathstrut smash hspace kern mkern mskip enspace thinspace negthinspace quad bmod pmod mod
    gcd deg dim ker hom sin cos tan sec csc cot sinh cosh tanh arcsin arccos arctan liminf limsup
    choose atop over cfrac substack aligned align gathered cases matrix pmatrix bmatrix vmatrix
    Bmatrix smallmatrix array hline cline ensuremath lnot uparrow downarrow updownarrow Uparrow
    Downarrow leftrightarrow Leftrightarrow longrightarrow longleftarrow longmapsto hookrightarrow
    ll gg lll ggg prec succ preceq succeq cong asymp doteq models vdash dashv square blacksquare
    checkmark dagger ddagger S P aleph beth complement Re Im wp mathring acute grave breve check
    color textcolor boxed fbox mbox hbox raisebox not unicode tfrac genfrac above underleftarrow
    bigl bigr Bigl Bigr biggl biggr Biggl Biggr bigm Bigm lt gt amp nobreakspace space
    nonscript delimsize gets bigotimes bigoplus bigodot bigvee bigwedge bigcup bigcap bigsqcup
    sqcup sqcap bowtie gtrless lessgtr Longleftrightarrow Longrightarrow Longleftarrow
    leftrightarrows rightleftharpoons""".split()
)

class _TextCollector(HTMLParser):
    """Collect page text outside <script> and <style> (where MathJax config lives)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in ("script", "style"):
            self._skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style") and self._skip:
            self._skip -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self.parts.append(data)


def _math_segments(text: str):
    """Yield the contents of \\( ... \\) and \\[ ... \\] segments (make4ht's math)."""
    i = 0
    while True:
        k = min((p for p in (text.find("\\(", i), text.find("\\[", i)) if p != -1), default=-1)
        if k == -1:
            return
        close = "\\)" if text[k + 1] == "(" else "\\]"
        e = text.find(close, k + 2)
        if e == -1:
            return
        yield text[k + 2 : e]
        i = e + 2


def _commands(tex: str):
    i = 0
    while i < len(tex):
        name, j = _read_cs(tex, i)
        if name:
            yield name
            i = j
        else:
            i += 2 if tex[i] == "\\" else 1


def unknown_macros(page: Path, table: dict[str, str | list]) -> dict[str, int]:
    collector = _TextCollector()
    collector.feed(page.read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    for seg in _math_segments("".join(collector.parts)):
        for c in _commands(seg):
            if c not in table and c not in KNOWN_MATHJAX:
                counts[c] = counts.get(c, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: -kv[1]))


def main(argv: list[str]) -> int:
    check = "--check" in argv
    titles = [a.split("=", 1)[1] for a in argv if a.startswith("--title=")]
    args = [a for a in argv if a != "--check" and not a.startswith("--title=")]
    if len(args) < 2:
        print(__doc__)
        return 2
    page, styles = Path(args[0]), [Path(a) for a in args[1:]]
    table = macro_table(styles)
    inject(page, table)
    print(f"injected {len(table)} macros into {page}")
    if titles:
        set_title(page, titles[-1])
    if check:
        missing = unknown_macros(page, table)
        if missing:
            print("macros in math with no definition:", missing)
            return 1
        print("no undefined macros found in math")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
