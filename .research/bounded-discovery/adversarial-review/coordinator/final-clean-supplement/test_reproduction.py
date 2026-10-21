"""Check the portable artifact against the previously audited experiment."""

import hashlib
import json
import os
import py_compile
import runpy
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from gbfplus_probe import insert

HERE = Path(__file__).resolve().parent


def check_result(result: dict[str, Any]) -> None:
    # The artifact contract is JSON, which serializes support tuples as arrays.
    result = json.loads(json.dumps(result))
    reference = json.loads((HERE / "reference-results.json").read_text())
    assert result["gbfplus_exact"] == reference["gbfplus_exact"]
    fresh = dict(result["gbfplus_stored"])
    saved = dict(reference["gbfplus_stored"])
    # Scan timing is descriptive and deliberately excluded from equality.
    assert fresh.pop("repeated_scan_ns_mean") >= 0
    saved.pop("repeated_scan_ns_mean")
    assert fresh == saved
    assert result["schema_version"] == 1
    assert result["source_sha256"] == {
        name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        for name in ("gbfplus_probe.py", "reproduce.py")
    }


def test_imported_results_match_all_deterministic_evidence() -> None:
    from reproduce import reproduce

    check_result(reproduce())


def test_script_writes_results_in_selected_working_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(HERE / "reproduce.py"), run_name="__main__")
    check_result(json.loads((tmp_path / "reproduced-results.json").read_text()))


def test_command_runs_without_site_packages(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "-S", str(HERE / "reproduce.py")],
        cwd=tmp_path, capture_output=True, text=True, check=True,
    )
    assert "reproduced-results.json" in completed.stdout
    check_result(json.loads((tmp_path / "reproduced-results.json").read_text()))


def test_full_stored_array_includes_prefix_and_preserves_occupied_zero() -> None:
    # Expected full words are hand-derived from the row equations, independently
    # of the suffix decoder. Flipping a prefix bit must also fail this check.
    cells: list[int | None] = [None] * 7
    success = insert(cells, (5, 1, 3), 0b101, (0b010, 0b111), 3)
    assert success
    assert cells == [None, 0b010, None, 0b111, None, 0b000, None]
    success = insert(cells, (1, 3, 4), 0b110, (), 3)
    assert success
    assert cells == [None, 0b010, None, 0b111, 0b011, 0b000, None]


@pytest.mark.parametrize("optimization", ["command-line", "environment"])
def test_optimized_execution_fails_before_writing_evidence(
    tmp_path: Path, optimization: str,
) -> None:
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    args = [sys.executable, "-S"]
    if optimization == "command-line":
        args.append("-O")
    else:
        env["PYTHONOPTIMIZE"] = "1"
    completed = subprocess.run(
        [*args, str(HERE / "reproduce.py")], cwd=tmp_path, env=env,
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode != 0
    assert "requires assertions" in completed.stderr
    assert not (tmp_path / "reproduced-results.json").exists()


def test_optimized_bytecode_fails_even_in_unoptimized_interpreter(tmp_path: Path) -> None:
    for name in ("gbfplus_probe.py", "reproduce.py"):
        (tmp_path / name).write_bytes((HERE / name).read_bytes())
    bytecode = tmp_path / "reproduce.pyc"
    py_compile.compile(str(tmp_path / "reproduce.py"), cfile=str(bytecode),
                       doraise=True, optimize=1)
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    env.pop("PYTHONPATH", None)
    completed = subprocess.run(
        [sys.executable, "-S", str(bytecode)], cwd=tmp_path, env=env,
        capture_output=True, text=True, check=False,
    )
    assert completed.returncode != 0
    assert "requires assertions" in completed.stderr
    assert not (tmp_path / "reproduced-results.json").exists()
