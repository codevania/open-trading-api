from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_sec_filing_document_collect.py"


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


class DiSecFilingDocumentCollectTest(unittest.TestCase):
    def test_dry_run_selects_latest_filings_and_redacts_user_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_dir = Path(tmp) / "raw" / "2026" / "2026-07-08" / "sec" / "MSFT"
            _write_json(
                raw_dir / "submissions.raw.json",
                {
                    "cik": "0000789019",
                    "filings": {
                        "recent": {
                            "form": ["4", "10-Q", "8-K", "10-K", "10-Q", "10-K"],
                            "filingDate": ["2026-07-01", "2026-04-25", "2026-04-20", "2025-07-30", "2025-04-24", "2024-07-30"],
                            "reportDate": ["2026-07-01", "2026-03-31", "2026-04-20", "2025-06-30", "2025-03-31", "2024-06-30"],
                            "accessionNumber": [
                                "0000789019-26-000137",
                                "0000789019-26-000100",
                                "0000789019-26-000099",
                                "0000789019-25-000080",
                                "0000789019-25-000050",
                                "0000789019-24-000090",
                            ],
                            "primaryDocument": [
                                "xslF345X05/doc4.xml",
                                "msft-20260331.htm",
                                "msft-8k.htm",
                                "msft-20250630.htm",
                                "msft-20250331.htm",
                                "msft-20240630.htm",
                            ],
                        }
                    },
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
                    "--form",
                    "10-K",
                    "--form",
                    "10-Q",
                    "--limit-per-form",
                    "1",
                    "--dry-run",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["symbol"], "MSFT")
            self.assertEqual(len(payload["requests"]), 2)
            self.assertEqual(payload["requests"][0]["form"], "10-Q")
            self.assertEqual(payload["requests"][1]["form"], "10-K")
            self.assertIn("https://www.sec.gov/Archives/edgar/data/789019/000078901926000100/msft-20260331.htm", result.stdout)
            self.assertIn("https://www.sec.gov/Archives/edgar/data/789019/000078901925000080/msft-20250630.htm", result.stdout)
            self.assertIn('"User-Agent": "***"', result.stdout)
            self.assertNotIn("SEC_USER_AGENT", result.stdout)

    def test_fails_when_submissions_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--symbol",
                    "MSFT",
                    "--raw-dir",
                    str(Path(tmp) / "missing"),
                    "--dry-run",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("submissions.raw.json", result.stderr)


if __name__ == "__main__":
    unittest.main()
