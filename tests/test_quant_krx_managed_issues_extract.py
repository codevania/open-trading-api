from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTRACT = REPO_ROOT / "scripts" / "quant_krx_managed_issues_extract.py"


class QuantKrxManagedIssuesExtractTest(unittest.TestCase):
    def test_extracts_current_managed_issues_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "managed_issues_current.raw.csv"
            raw.write_text(
                textwrap.dedent(
                    """
                    종목코드,종목명,현재가,지정일자
                    121850,코이즈,"1,715",2026/06/05
                    464440,한국제13호스팩,"2,115",2026/05/06
                    348950,제이알글로벌리츠,"1,182",2026/05/18
                    """
                ).lstrip(),
                encoding="utf-8-sig",
            )
            output = root / "exclusions.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(EXTRACT),
                    "--raw",
                    str(raw),
                    "--as-of-date",
                    "2026-06-13",
                    "--output",
                    str(output),
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("- Row count: `3`", report)
            self.assertIn("| `121850` | 코이즈 | `2026/06/05` | `common-stock-or-unclassified` |", report)
            self.assertIn("| `464440` | 한국제13호스팩 | `2026/05/06` | `SPAC` |", report)
            self.assertIn("| `348950` | 제이알글로벌리츠 | `2026/05/18` | `REIT` |", report)

    def test_fails_when_required_columns_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "managed_issues_current.raw.csv"
            raw.write_text("code,name\n121850,코이즈\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(EXTRACT), "--raw", str(raw), "--as-of-date", "2026-06-13"],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required columns", result.stderr)


if __name__ == "__main__":
    unittest.main()
