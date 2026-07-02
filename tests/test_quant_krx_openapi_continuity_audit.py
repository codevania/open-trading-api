from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = REPO_ROOT / "scripts" / "quant_krx_openapi_continuity_audit.py"


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


class QuantKrxOpenapiContinuityAuditTest(unittest.TestCase):
    def test_audits_counts_duplicates_and_pair_mismatches(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            normalized_dir = root / "normalized"
            rows_output = root / "audit.rows.csv"
            report_output = root / "audit.md"
            _write_csv(
                normalized_dir / "stock_daily.csv",
                ("date", "code", "market"),
                [
                    {"date": "2025-01-02", "code": "005930", "market": "KOSPI"},
                    {"date": "2025-01-02", "code": "000660", "market": "KOSPI"},
                    {"date": "2025-01-03", "code": "005930", "market": "KOSPI"},
                    {"date": "2025-01-06", "code": "005930", "market": "KOSPI"},
                ],
            )
            _write_csv(
                normalized_dir / "issue_base.csv",
                ("date", "code", "market"),
                [
                    {"date": "2025-01-02", "code": "005930", "market": "KOSPI"},
                    {"date": "2025-01-02", "code": "005930", "market": "KOSPI"},
                    {"date": "2025-01-03", "code": "005930", "market": "KOSPI"},
                    {"date": "2025-01-06", "code": "005930", "market": "KOSPI"},
                ],
            )
            _write_csv(
                normalized_dir / "index_daily.csv",
                ("date", "index_class", "index_name"),
                [
                    {"date": "2025-01-02", "index_class": "KOSPI", "index_name": "KOSPI"},
                    {"date": "2025-01-03", "index_class": "KOSPI", "index_name": "KOSPI"},
                    {"date": "2025-01-06", "index_class": "KOSPI", "index_name": "KOSPI"},
                ],
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(AUDIT),
                    "--normalized-dir",
                    str(normalized_dir),
                    "--max-row-delta",
                    "0",
                    "--rows-output",
                    str(rows_output),
                    "--report-output",
                    str(report_output),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            with rows_output.open("r", encoding="utf-8-sig", newline="") as handle:
                audit_rows = list(csv.DictReader(handle))
            self.assertEqual(audit_rows[0]["stock_daily_rows"], "2")
            self.assertEqual(audit_rows[0]["duplicate_issue_keys"], "1")
            self.assertEqual(audit_rows[0]["missing_issue_for_stock"], "1")
            self.assertEqual(audit_rows[1]["row_count_alert"], "true")
            report = report_output.read_text(encoding="utf-8")
            self.assertIn("Stock/issue code mismatches", report)
            self.assertIn("| `2025-01-06` | 1 | 1 | 1 | 0 | 0 | `false` | 0 |", report)
            self.assertIn("[[", report)

    def test_fails_when_required_table_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            normalized_dir = Path(tmp)

            result = subprocess.run(
                [sys.executable, str(AUDIT), "--normalized-dir", str(normalized_dir)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing normalized table", result.stderr)


if __name__ == "__main__":
    unittest.main()
