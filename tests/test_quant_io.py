from __future__ import annotations

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


if __name__ == "__main__":
    unittest.main()
