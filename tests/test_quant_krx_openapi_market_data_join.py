from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
JOIN = REPO_ROOT / "scripts" / "quant_krx_openapi_market_data_join.py"


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


class QuantKrxOpenapiMarketDataJoinTest(unittest.TestCase):
    def test_joins_stock_and_issue_rows_by_date_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            normalized_dir = root / "normalized"
            output = root / "market_data.csv"
            report = root / "market_data.md"
            _write_csv(
                normalized_dir / "stock_daily.csv",
                (
                    "date",
                    "code",
                    "name",
                    "market",
                    "section",
                    "close",
                    "volume",
                    "trading_value_krw",
                    "market_cap_krw",
                    "listed_shares",
                    "source_service",
                    "source_path",
                ),
                [
                    {
                        "date": "2025-01-02",
                        "code": "005930",
                        "name": "Samsung Electronics",
                        "market": "KOSPI",
                        "section": "",
                        "close": "53400",
                        "volume": "123",
                        "trading_value_krw": "456",
                        "market_cap_krw": "789",
                        "listed_shares": "10",
                        "source_service": "kospi_stock_daily",
                        "source_path": "stock.raw.json",
                    }
                ],
            )
            _write_csv(
                normalized_dir / "issue_base.csv",
                (
                    "date",
                    "standard_code",
                    "code",
                    "name",
                    "short_name",
                    "english_name",
                    "listing_date",
                    "market",
                    "security_group",
                    "section",
                    "stock_certificate_type",
                    "par_value_krw",
                    "listed_shares",
                    "source_service",
                    "source_path",
                ),
                [
                    {
                        "date": "2025-01-02",
                        "standard_code": "KR7005930003",
                        "code": "005930",
                        "name": "Samsung Electronics Common",
                        "short_name": "Samsung Electronics",
                        "english_name": "Samsung Electronics Co., Ltd.",
                        "listing_date": "1975-06-11",
                        "market": "KOSPI",
                        "security_group": "Stock",
                        "section": "",
                        "stock_certificate_type": "Common",
                        "par_value_krw": "100",
                        "listed_shares": "10",
                        "source_service": "kospi_issue_base",
                        "source_path": "issue.raw.json",
                    }
                ],
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(JOIN),
                    "--normalized-dir",
                    str(normalized_dir),
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
                joined_rows = list(csv.DictReader(handle))
            self.assertEqual(joined_rows[0]["standard_code"], "KR7005930003")
            self.assertEqual(joined_rows[0]["stock_name"], "Samsung Electronics")
            self.assertEqual(joined_rows[0]["issue_name"], "Samsung Electronics Common")
            self.assertIn("Joined rows", report.read_text(encoding="utf-8"))

    def test_fails_when_stock_has_no_issue_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            normalized_dir = Path(tmp) / "normalized"
            _write_csv(
                normalized_dir / "stock_daily.csv",
                ("date", "code", "name", "market"),
                [{"date": "2025-01-02", "code": "005930", "name": "Samsung Electronics", "market": "KOSPI"}],
            )
            _write_csv(normalized_dir / "issue_base.csv", ("date", "code", "name", "market"), [])

            result = subprocess.run(
                [
                    sys.executable,
                    str(JOIN),
                    "--normalized-dir",
                    str(normalized_dir),
                    "--output",
                    str(Path(tmp) / "out.csv"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("stock rows without issue rows", result.stderr)


if __name__ == "__main__":
    unittest.main()
