from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FILTER = REPO_ROOT / "scripts" / "quant_liquidity_filter.py"


def _daily_payload(values: list[int]) -> str:
    rows = []
    for index, value in enumerate(values, start=1):
        rows.append(
            {
                "stck_bsop_date": f"202605{index:02d}",
                "stck_clpr": "10000",
                "stck_oprc": "10000",
                "stck_hgpr": "10000",
                "stck_lwpr": "10000",
                "acml_vol": "1000",
                "acml_tr_pbmn": str(value),
            }
        )
    return json.dumps({"output2": rows}, ensure_ascii=False)


class QuantLiquidityFilterTest(unittest.TestCase):
    def test_applies_liquidity_filter_to_current_universe_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            universe_csv = root / "universe.csv"
            universe_csv.write_text(
                textwrap.dedent(
                    """
                    code,name,market,security_type,listing_date,listing_age_calendar_days,status,reason
                    005930,삼성전자,KOSPI,보통주,2000/01/01,9660,include,eligible_current_snapshot
                    035420,NAVER,KOSPI,보통주,2000/01/01,9660,include,eligible_current_snapshot
                    000660,SK하이닉스,KOSPI,보통주,2000/01/01,9660,include,eligible_current_snapshot
                    121850,코이즈,KOSDAQ,보통주,2020/01/01,2355,exclude,managed_issue_current
                    0004V0,엔비알모션,KOSDAQ,보통주,2026/01/14,150,include,eligible_current_snapshot
                    """
                ).lstrip(),
                encoding="utf-8-sig",
            )
            raw_dir = root / "raw"
            raw_dir.mkdir()
            (raw_dir / "005930.daily.raw.json").write_text(_daily_payload([2_000_000_000] * 20), encoding="utf-8")
            (raw_dir / "035420.daily.raw.json").write_text(_daily_payload([500_000_000] * 20), encoding="utf-8")
            (raw_dir / "0004V0.daily.raw.json").write_text(_daily_payload([2_000_000_000] * 19), encoding="utf-8")

            output = root / "liquidity.md"
            csv_output = root / "liquidity.csv"
            result = subprocess.run(
                [
                    sys.executable,
                    str(FILTER),
                    "--universe-csv",
                    str(universe_csv),
                    "--raw-dir",
                    str(raw_dir),
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
            self.assertIn("- Included rows after Liquidity Filter: `1`", report)
            self.assertIn("| `pass` | 1 |", report)
            self.assertIn("| `fail` | 1 |", report)
            self.assertIn("| `data_missing` | 1 |", report)
            self.assertIn("| `data_insufficient` | 1 |", report)
            self.assertIn("| `not_evaluated_preexisting_exclude` | 1 |", report)

            with csv_output.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = {row["code"]: row for row in csv.DictReader(handle)}

            self.assertEqual(rows["005930"]["status"], "include")
            self.assertEqual(rows["005930"]["avg_trading_value_20d_krw"], "2000000000")
            self.assertEqual(rows["005930"]["liquidity_filter_status"], "pass")
            self.assertEqual(rows["035420"]["status"], "exclude")
            self.assertEqual(rows["035420"]["reason"], "liquidity_value_below_threshold")
            self.assertEqual(rows["035420"]["liquidity_filter_status"], "fail")
            self.assertEqual(rows["000660"]["reason"], "liquidity_raw_missing")
            self.assertEqual(rows["000660"]["liquidity_filter_status"], "data_missing")
            self.assertEqual(rows["0004V0"]["reason"], "liquidity_trading_value_history_insufficient")
            self.assertEqual(rows["0004V0"]["liquidity_filter_status"], "data_insufficient")
            self.assertEqual(rows["121850"]["reason"], "managed_issue_current")
            self.assertEqual(rows["121850"]["liquidity_filter_status"], "not_evaluated_preexisting_exclude")

    def test_fails_when_universe_csv_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw"
            raw_dir.mkdir()

            result = subprocess.run(
                [
                    sys.executable,
                    str(FILTER),
                    "--universe-csv",
                    str(root / "missing.csv"),
                    "--raw-dir",
                    str(raw_dir),
                    "--as-of-date",
                    "2026-06-13",
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("universe CSV not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
