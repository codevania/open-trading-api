from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN = REPO_ROOT / "scripts" / "quant_kis_ohlcv_batch_plan.py"
API_CONFIG = REPO_ROOT / "MCP" / "Kis Trading MCP" / "configs" / "domestic_stock.json"


class QuantKisOhlcvBatchPlanTest(unittest.TestCase):
    def test_builds_request_plan_from_included_universe_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            universe_csv = root / "universe.csv"
            universe_csv.write_text(
                textwrap.dedent(
                    """
                    code,name,market,security_type,listing_date,listing_age_calendar_days,status,reason
                    000020,동화약품,KOSPI,보통주,1976/03/24,18343,include,eligible_current_snapshot
                    000040,KR모터스,KOSPI,보통주,1976/05/25,18281,include,eligible_current_snapshot
                    0004V0,엔비알모션,KOSDAQ,보통주,2026/01/14,150,include,eligible_current_snapshot
                    121850,코이즈,KOSDAQ,보통주,2020/01/01,2355,exclude,managed_issue_current
                    """
                ).lstrip(),
                encoding="utf-8-sig",
            )
            raw_dir = root / "raw"
            raw_dir.mkdir()
            (raw_dir / "000020.daily.raw.json").write_text("{}", encoding="utf-8")

            output = root / "plan.md"
            jsonl_output = root / "requests.jsonl"
            result = subprocess.run(
                [
                    sys.executable,
                    str(PLAN),
                    "--universe-csv",
                    str(universe_csv),
                    "--api-config",
                    str(API_CONFIG),
                    "--raw-dir",
                    str(raw_dir),
                    "--as-of-date",
                    "2026-06-15",
                    "--start-date",
                    "20260301",
                    "--end-date",
                    "20260615",
                    "--limit",
                    "2",
                    "--skip-existing",
                    "--output",
                    str(output),
                    "--jsonl-output",
                    str(jsonl_output),
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("- Base included rows: `3`", report)
            self.assertIn("- Existing raw skipped: `1`", report)
            self.assertIn("- Selected requests: `2`", report)
            self.assertIn("| `fid_input_iscd` |", report)

            requests = [json.loads(line) for line in jsonl_output.read_text(encoding="utf-8").splitlines()]
            self.assertEqual([row["code"] for row in requests], ["000040", "0004V0"])
            self.assertEqual(requests[0]["tool"], "domestic_stock")
            self.assertEqual(requests[0]["api_type"], "inquire_daily_itemchartprice")
            self.assertEqual(requests[0]["params"]["env_dv"], "real")
            self.assertEqual(requests[0]["params"]["fid_cond_mrkt_div_code"], "J")
            self.assertEqual(requests[0]["params"]["fid_input_date_1"], "20260301")
            self.assertEqual(requests[0]["params"]["fid_input_date_2"], "20260615")
            self.assertEqual(requests[0]["params"]["fid_period_div_code"], "D")
            self.assertEqual(requests[0]["params"]["fid_org_adj_prc"], "0")

    def test_fails_when_universe_csv_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = subprocess.run(
                [
                    sys.executable,
                    str(PLAN),
                    "--universe-csv",
                    str(root / "missing.csv"),
                    "--api-config",
                    str(API_CONFIG),
                    "--raw-dir",
                    str(root / "raw"),
                    "--as-of-date",
                    "2026-06-15",
                    "--start-date",
                    "20260301",
                    "--end-date",
                    "20260615",
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
