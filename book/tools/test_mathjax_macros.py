"""Tests for the MathJax macro injector (run: python3 -m pytest book/tools)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))
import mathjax_macros as M  # noqa: E402

BOOK = Path(__file__).resolve().parent.parent


def test_parses_newcommand_with_and_without_arguments():
    defs = M.parse_definitions(r"\newcommand{\fprate}{\varepsilon}" "\n" r"\newcommand{\pair}[2]{(#1,#2)}")
    assert [(d.name, d.body, d.nargs) for d in defs] == [("fprate", r"\varepsilon", 0), ("pair", "(#1,#2)", 2)]


def test_bare_control_sequence_name_and_renewcommand():
    defs = M.parse_definitions(r"\renewcommand\Given{\mid}")
    assert defs[0].name == "Given" and defs[0].body == r"\mid"


def test_escaped_braces_and_linebreak_do_not_unbalance():
    defs = M.parse_definitions(r"\newcommand{\lb}{\{\,x\\}" "\n" r"\newcommand{\nxt}{y}")
    assert [d.name for d in defs] == ["lb", "nxt"]
    assert defs[0].body == r"\{\,x\\"


def test_declare_math_operator_plain_and_starred():
    defs = M.parse_definitions(r"\DeclareMathOperator{\rank}{rank}" "\n" r"\DeclareMathOperator*{\argmax}{arg\,max}")
    assert defs[0].body == r"\operatorname{rank}"
    assert defs[1].body == r"\operatorname*{arg\,max}"


def test_comments_are_ignored_but_escaped_percent_is_kept():
    defs = M.parse_definitions("% \\newcommand{\\no}{x}\n\\newcommand{\\pct}{50\\%} % trailing")
    assert [(d.name, d.body) for d in defs] == [("pct", r"50\%")]


def test_optional_default_argument_is_skipped_not_mistranslated():
    defs = M.parse_definitions(r"\newcommand{\opt}[2][a]{#1#2}" "\n" r"\newcommand{\ok}{z}")
    assert [d.name for d in defs] == ["ok"]


def test_unbalanced_definition_raises():
    with pytest.raises(ValueError):
        M.parse_definitions(r"\newcommand{\bad}{\left( x")


def test_bare_forms_override_and_fallbacks_fill_gaps(tmp_path):
    sty = tmp_path / "a.sty"
    sty.write_text(r"\newcommand{\Card}{WRONG}" "\n" r"\newcommand{\funstyle}[1]{\mathsf{#1}}", encoding="utf-8")
    table = M.macro_table([sty])
    assert table["Card"] == M.BARE_FORMS["Card"]
    assert table["funstyle"] == [r"\mathsf{#1}", 1]  # defined: fallback does not override
    assert table["mathbbm"] == M.FALLBACKS["mathbbm"]


def _page(tmp_path, body: str) -> Path:
    page = tmp_path / "p.html"
    page.write_text(
        '<html><head><script>\nwindow.MathJax = { tex: { tags: "ams" }, };\n</script></head>'
        f"<body>{body}</body></html>",
        encoding="utf-8",
    )
    return page


def test_inject_is_idempotent_and_strips_tex4ht_markers(tmp_path):
    page = _page(tmp_path, r"<h2>\(\mathrm{@@Bernoulli}\)</h2>")
    M.inject(page, {"fprate": r"\varepsilon"})
    once = page.read_text(encoding="utf-8")
    M.inject(page, {"fprate": r"\varepsilon"})
    assert page.read_text(encoding="utf-8") == once
    assert "@@" not in once
    config = next(line for line in once.split("\n") if "window.MathJax" in line)
    assert json.loads(config.split("macros: ", 1)[1].rsplit(" }, };", 1)[0]) == {"fprate": r"\varepsilon"}


def test_inject_requires_a_mathjax_config_line(tmp_path):
    page = tmp_path / "p.html"
    page.write_text("<html></html>", encoding="utf-8")
    with pytest.raises(SystemExit):
        M.inject(page, {})


def test_unknown_macros_scans_math_only_outside_scripts(tmp_path):
    page = _page(tmp_path, r"<p>\notmath outside \(\fprate + \mystery x\) and \[\frac{1}{2}\mystery\]</p>")
    assert M.unknown_macros(page, {"fprate": r"\varepsilon"}) == {"mystery": 2}


def test_real_book_styles_parse_and_cover_the_core_notation():
    table = M.macro_table([BOOK / "alex.sty", BOOK / "preamble.tex"])
    for name in ("fprate", "fnrate", "ASet", "Prob", "Card"):
        assert name in table


def test_set_title_fills_empty_title_and_escapes(tmp_path):
    page = tmp_path / "p.html"
    page.write_text("<html><head><title></title></head></html>", encoding="utf-8")
    M.set_title(page, "Sets & Maps")
    assert "<title>Sets &amp; Maps</title>" in page.read_text(encoding="utf-8")
    M.set_title(page, "Again")
    assert page.read_text(encoding="utf-8").count("<title>") == 1 and "<title>Again</title>" in page.read_text(encoding="utf-8")
