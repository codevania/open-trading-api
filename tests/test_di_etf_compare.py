from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_etf_compare.py"


VALID_MANIFEST = """\
version: 1
portfolio_frame:
  name: test core-satellite
  horizon: 5-10 years
  priority_order:
    - build core first
  guardrails:
    core_first: true
    exclude_from_long_term_core:
      - leveraged ETF
core_etfs:
  - symbol: VOO
    name: Vanguard S&P 500 ETF
    listing: US
    benchmark: S&P 500 Index
    status: candidate
korea_listed_etfs_to_verify:
  - symbol: "360750"
    name: TIGER US S&P500
    listing: Korea
    benchmark: S&P 500 Index
    status: needs_issuer_and_tax_verification
satellite_etfs_to_verify:
  - symbol: QQQ
    name: Invesco QQQ Trust
    listing: US
    benchmark: Nasdaq-100 Index
    status: satellite_candidate
satellite_equities:
  primary_queue:
    - symbol: MSFT
      name: Microsoft
      market: NASDAQ
      status: candidate
  secondary_queue:
    - symbol: AMD
      name: Advanced Micro Devices
      market: NASDAQ
      status: secondary_candidate
manual_checks_before_buy:
  etf:
    - total expense
  stock:
    - latest 10-K
"""


class DiEtfCompareTest(unittest.TestCase):
    def test_renders_candidate_report_to_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "candidates.yaml"
            manifest.write_text(VALID_MANIFEST, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--run-date",
                    "2026-07-05",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("# DI Core ETF and Satellite Candidate Comparison", result.stdout)
            self.assertIn("| VOO | Vanguard S&P 500 ETF | US |", result.stdout)
            self.assertIn("| 360750 | TIGER US S&P500 |", result.stdout)
            self.assertIn("| QQQ | Invesco QQQ Trust | US |", result.stdout)
            self.assertIn("| MSFT | Microsoft | NASDAQ |", result.stdout)
            self.assertIn("Move only approved candidates into `_report/di/watchlist.yaml`", result.stdout)

    def test_writes_report_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            output = root / "report.md"
            manifest.write_text(VALID_MANIFEST, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--output",
                    str(output),
                    "--run-date",
                    "2026-07-05",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("Run date: `2026-07-05`", report)
            self.assertIn("Manual Checks Before Buy", report)
            self.assertEqual(result.stdout, "")

    def test_rejects_missing_required_candidate_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "bad.yaml"
            manifest.write_text(
                """\
version: 1
core_etfs:
  - name: Missing symbol
    listing: US
    benchmark: S&P 500 Index
    status: candidate
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--candidate-file", str(manifest)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("core_etfs[0]: missing symbol", result.stderr)


if __name__ == "__main__":
    unittest.main()
