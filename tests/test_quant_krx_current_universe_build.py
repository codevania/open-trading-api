from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BUILD = REPO_ROOT / "scripts" / "quant_krx_current_universe_build.py"


class QuantKrxCurrentUniverseBuildTest(unittest.TestCase):
    def test_builds_current_universe_with_exclusions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            listed = root / "listed_issues_current.raw.csv"
            listed.write_text(
                textwrap.dedent(
                    """
                    종목코드,종목명,시장구분,주식종류
                    005930,삼성전자,KOSPI,보통주
                    005935,삼성전자우,KOSPI,우선주
                    121850,코이즈,KOSDAQ,보통주
                    464440,한국제13호스팩,KOSDAQ,보통주
                    348950,제이알글로벌리츠,KOSPI,보통주
                    123456,코넥스예시,KONEX,보통주
                    """
                ).lstrip(),
                encoding="utf-8-sig",
            )
            managed = root / "managed_issues_current.raw.csv"
            managed.write_text(
                textwrap.dedent(
                    """
                    종목코드,종목명,지정일자
                    121850,코이즈,2026/06/05
                    """
                ).lstrip(),
                encoding="utf-8-sig",
            )
            output = root / "universe.md"
            csv_output = root / "universe.csv"

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD),
                    "--listed-raw",
                    str(listed),
                    "--managed-raw",
                    str(managed),
                    "--as-of-date",
                    "2026-06-13",
                    "--output",
                    str(output),
                    "--csv-output",
                    str(csv_output),
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("- Included rows: `1`", report)
            self.assertIn("- Excluded rows: `5`", report)
            self.assertIn("| `managed_issue_current` | 1 |", report)
            self.assertIn("| `instrument_type_excluded` | 1 |", report)
            self.assertIn("| `instrument_name_excluded` | 2 |", report)
            self.assertIn("| `market_not_allowed` | 1 |", report)

            with csv_output.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = {row["code"]: row for row in csv.DictReader(handle)}
            self.assertEqual(rows["005930"]["status"], "include")
            self.assertEqual(rows["121850"]["reason"], "managed_issue_current")
            self.assertEqual(rows["005935"]["reason"], "instrument_type_excluded")
            self.assertEqual(rows["464440"]["reason"], "instrument_name_excluded")
            self.assertEqual(rows["348950"]["reason"], "instrument_name_excluded")
            self.assertEqual(rows["123456"]["reason"], "market_not_allowed")

    def test_fails_when_listed_raw_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            managed = root / "managed_issues_current.raw.csv"
            managed.write_text("종목코드,종목명,지정일자\n121850,코이즈,2026/06/05\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(BUILD),
                    "--listed-raw",
                    str(root / "missing.csv"),
                    "--managed-raw",
                    str(managed),
                    "--as-of-date",
                    "2026-06-13",
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("listed raw CSV not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
