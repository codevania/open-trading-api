from __future__ import annotations

import ast
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from quant_io import write_json_lf, write_text_lf


def _quant_scripts() -> list[Path]:
    return sorted(SCRIPTS_DIR.glob("quant_*.py"))


class QuantIoTest(unittest.TestCase):
    def test_write_text_lf_uses_lf_newlines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "report.md"
            write_text_lf(output, "a\nb\n")

            raw = output.read_bytes()
            self.assertEqual(raw, b"a\nb\n")
            self.assertNotIn(b"\r\n", raw)

    def test_write_json_lf_uses_lf_newlines(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "payload.json"
            write_json_lf(output, {"name": "KRX", "rows": [1, 2]}, sort_keys=True)

            raw = output.read_bytes()
            self.assertNotIn(b"\r\n", raw)
            self.assertEqual(json.loads(raw.decode("utf-8"))["rows"], [1, 2])

    def test_quant_generators_use_lf_text_helper(self) -> None:
        failures: list[str] = []
        for path in _quant_scripts():
            if path.name == "quant_io.py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "write_text"
                ):
                    failures.append(f"{path.relative_to(REPO_ROOT)}:{node.lineno}")

        self.assertEqual([], failures)

    def test_quant_write_handles_set_explicit_newlines(self) -> None:
        failures: list[str] = []
        for path in _quant_scripts():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "open"
                ):
                    continue

                mode = _constant_string_arg(node, 0) or _constant_string_kwarg(node, "mode")
                if mode and mode.startswith("w") and _constant_string_kwarg(node, "newline") is None:
                    failures.append(f"{path.relative_to(REPO_ROOT)}:{node.lineno}")

        self.assertEqual([], failures)

    def test_quant_csv_writers_set_lf_lineterminator(self) -> None:
        failures: list[str] = []
        for path in _quant_scripts():
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "csv"
                    and node.func.attr == "DictWriter"
                ):
                    continue

                if _constant_string_kwarg(node, "lineterminator") != "\n":
                    failures.append(f"{path.relative_to(REPO_ROOT)}:{node.lineno}")

        self.assertEqual([], failures)


def _constant_string_arg(node: ast.Call, index: int) -> str | None:
    if len(node.args) <= index:
        return None
    value = node.args[index]
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return value.value
    return None


def _constant_string_kwarg(node: ast.Call, name: str) -> str | None:
    for keyword in node.keywords:
        if (
            keyword.arg == name
            and isinstance(keyword.value, ast.Constant)
            and isinstance(keyword.value.value, str)
        ):
            return keyword.value.value
    return None


if __name__ == "__main__":
    unittest.main()
