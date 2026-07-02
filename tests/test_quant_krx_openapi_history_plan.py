from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLAN = REPO_ROOT / "scripts" / "quant_krx_openapi_history_plan.py"
CORE_SERVICES = (
    "kospi_stock_daily",
    "kosdaq_stock_daily",
    "kospi_issue_base",
    "kosdaq_issue_base",
    "kospi_index_daily",
    "kosdaq_index_daily",
)


def _touch_raw(raw_root: Path, capture_date: str, service_id: str, bas_dd: str) -> None:
    path = raw_root / capture_date[:4] / capture_date / "krx" / "openapi" / f"{service_id}_{bas_dd}.raw.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"OutBlock_1":[]}\n', encoding="utf-8")


class QuantKrxOpenapiHistoryPlanTest(unittest.TestCase):
    def test_plans_missing_weekday_requests_and_skips_existing_raws(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_root = Path(tmp) / "raw"
            for service_id in CORE_SERVICES:
                _touch_raw(raw_root, "2026-07-03", service_id, "20250102")

            result = subprocess.run(
                [
                    sys.executable,
                    str(PLAN),
                    "--start",
                    "20250102",
                    "--end",
                    "20250106",
                    "--capture-date",
                    "2026-07-03",
                    "--raw-root",
                    str(raw_root),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["totals"]["candidate_dates"], 3)
            self.assertEqual(payload["totals"]["complete_dates"], 1)
            self.assertEqual(payload["totals"]["existing_raw_files"], 6)
            self.assertEqual(payload["totals"]["missing_requests"], 12)
            self.assertEqual([row["bas_dd"] for row in payload["dates"]], ["20250102", "20250103", "20250106"])
            self.assertTrue(payload["dates"][0]["complete"])
            self.assertFalse(payload["dates"][1]["complete"])

    def test_can_plan_one_service_and_write_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / "plan.json"
            report = root / "plan.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(PLAN),
                    "--start",
                    "20250102",
                    "--end",
                    "20250102",
                    "--service",
                    "kospi_stock_daily",
                    "--capture-date",
                    "2026-07-03",
                    "--raw-root",
                    str(root / "raw"),
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
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["services"], ["kospi_stock_daily"])
            self.assertEqual(payload["totals"]["missing_requests"], 1)
            report_text = report.read_text(encoding="utf-8")
            self.assertIn("[[", report_text)
            self.assertIn("kospi_stock_daily", report_text)

    def test_rejects_reversed_range(self) -> None:
        result = subprocess.run(
            [sys.executable, str(PLAN), "--start", "20250106", "--end", "20250102"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("start must be on or before end", result.stderr)


if __name__ == "__main__":
    unittest.main()
