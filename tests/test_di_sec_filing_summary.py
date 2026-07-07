from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_sec_filing_summary.py"


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


class DiSecFilingSummaryTest(unittest.TestCase):
    def test_renders_sec_filing_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw" / "2026" / "2026-07-08" / "sec" / "MSFT"
            output = root / "research" / "MSFT" / "sec-filing-summary.md"
            _write_json(raw_dir / "ticker_lookup.json", {"cik_str": 789019, "ticker": "MSFT", "title": "MICROSOFT CORP"})
            _write_json(
                raw_dir / "submissions.raw.json",
                {
                    "cik": "0000789019",
                    "name": "MICROSOFT CORP",
                    "filings": {
                        "recent": {
                            "form": ["4", "10-Q", "8-K", "10-K", "10-Q"],
                            "filingDate": ["2026-07-01", "2026-04-25", "2026-04-24", "2025-07-30", "2025-04-24"],
                            "reportDate": ["2026-07-01", "2026-03-31", "2026-04-24", "2025-06-30", "2025-03-31"],
                            "accessionNumber": [
                                "0000789019-26-000137",
                                "0000789019-26-000100",
                                "0000789019-26-000099",
                                "0000789019-25-000080",
                                "0000789019-25-000050",
                            ],
                            "primaryDocument": ["xslF345X05/doc4.xml", "msft-20260331.htm", "msft-8k.htm", "msft-20250630.htm", "msft-20250331.htm"],
                        }
                    },
                },
            )
            _write_json(raw_dir / "companyfacts.raw.json", {"entityName": "MICROSOFT CORPORATION", "facts": {"dei": {}, "us-gaap": {}}})
            _write_json(
                raw_dir / "concepts" / "us-gaap_Revenues.raw.json",
                {
                    "units": {
                        "USD": [
                            {"val": 100, "end": "2025-06-30", "filed": "2025-07-30", "fy": 2025, "fp": "FY", "form": "10-K"},
                            {"val": 200, "end": "2026-03-31", "filed": "2026-04-25", "fy": 2026, "fp": "Q3", "form": "10-Q"},
                        ]
                    }
                },
            )
            _write_json(
                raw_dir / "concepts" / "us-gaap_OperatingIncomeLoss.raw.json",
                {
                    "units": {
                        "USD": [
                            {"val": 50, "end": "2024-06-30", "filed": "2024-07-30", "fy": 2024, "fp": "FY", "form": "10-K"}
                        ]
                    }
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--symbol",
                    "MSFT",
                    "--run-date",
                    "2026-07-08",
                    "--raw-dir",
                    str(raw_dir),
                    "--output",
                    str(output),
                    "--concept",
                    "Revenues",
                    "--concept",
                    "OperatingIncomeLoss",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("# MSFT SEC Filing Summary", report)
            self.assertIn("| `10-Q` | 2026-04-25 | 2026-03-31 | `0000789019-26-000100` |", report)
            self.assertIn("| `10-K` | 2025-07-30 | 2025-06-30 | `0000789019-25-000080` |", report)
            self.assertIn("https://www.sec.gov/Archives/edgar/data/789019/000078901926000100/msft-20260331.htm", report)
            self.assertIn("| `Revenues` | `ok` | 200 | USD | 2026 | Q3 | 2026-03-31 | 2026-04-25 | 10-Q |", report)
            self.assertIn("| `OperatingIncomeLoss` | `stale` | 50 | USD | 2024 | FY | 2024-06-30 | 2024-07-30 | 10-K |", report)
            self.assertIn("Order intent generated: `false`", report)

    def test_fails_when_raw_files_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--symbol", "MSFT", "--raw-dir", str(Path(tmp) / "missing")],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("submissions.raw.json", result.stderr)


if __name__ == "__main__":
    unittest.main()
