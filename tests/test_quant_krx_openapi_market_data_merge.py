from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MERGE = REPO_ROOT / "scripts" / "quant_krx_openapi_market_data_merge.py"
FIELDS = ("date", "code", "stock_name", "market", "close")


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


class QuantKrxOpenapiMarketDataMergeTest(unittest.TestCase):
    def test_merges_inputs_and_sorts_by_date_market_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first.csv"
            second = root / "second.csv"
            output = root / "merged.csv"
            report = root / "merged.md"
            _write_csv(first, [{"date": "2025-01-31", "code": "005930", "stock_name": "Samsung", "market": "KOSPI", "close": "100"}])
            _write_csv(second, [{"date": "2025-02-03", "code": "035420", "stock_name": "NAVER", "market": "KOSPI", "close": "200"}])

            result = subprocess.run(
                [
                    sys.executable,
                    str(MERGE),
                    "--input",
                    str(second),
                    "--input",
                    str(first),
                    "--output",
                    str(output),
                    "--report-output",
                    str(report),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            with output.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual([row["date"] for row in rows], ["2025-01-31", "2025-02-03"])
            self.assertIn("| Merged rows | 2 |", report.read_text(encoding="utf-8"))

    def test_fails_on_duplicate_date_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first.csv"
            second = root / "second.csv"
            _write_csv(first, [{"date": "2025-01-31", "code": "005930", "stock_name": "Samsung", "market": "KOSPI", "close": "100"}])
            _write_csv(second, [{"date": "2025-01-31", "code": "005930", "stock_name": "Samsung", "market": "KOSPI", "close": "100"}])

            result = subprocess.run(
                [
                    sys.executable,
                    str(MERGE),
                    "--input",
                    str(first),
                    "--input",
                    str(second),
                    "--output",
                    str(root / "merged.csv"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("duplicate date/code keys", result.stderr)


if __name__ == "__main__":
    unittest.main()
