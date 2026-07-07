from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.quant_krx_openapi_history_collect import collect_from_plan, main


def _plan() -> dict[str, object]:
    return {
        "plan_type": "krx_openapi_history_missing_raw",
        "capture_date": "2026-07-06",
        "start": "20250210",
        "end": "20250210",
        "dates": [
            {
                "bas_dd": "20250210",
                "requests": [
                    {"service_id": "kospi_stock_daily", "raw_output": "_report/raw/path-a.json"},
                    {"service_id": "kosdaq_stock_daily", "raw_output": "_report/raw/path-b.json"},
                ],
            }
        ],
    }


class QuantKrxOpenApiHistoryCollectTest(unittest.TestCase):
    def test_collect_from_plan_summarizes_successes_without_auth_key(self) -> None:
        def collector(bas_dd: str, service_id: str) -> dict[str, object]:
            return {
                "status_code": 200,
                "row_count": 10 if service_id == "kospi_stock_daily" else 20,
                "raw_output": f"_report/raw/{service_id}_{bas_dd}.raw.json",
            }

        summary = collect_from_plan(plan=_plan(), collector=collector)

        self.assertEqual(summary["planned_requests"], 2)
        self.assertEqual(summary["successful_requests"], 2)
        self.assertEqual(summary["failed_requests"], 0)
        self.assertTrue(summary["guardrails"]["auth_key_redacted"])
        self.assertNotIn("AUTH_KEY", json.dumps(summary, ensure_ascii=False))

    def test_collect_from_plan_keeps_partial_failure_evidence(self) -> None:
        def collector(bas_dd: str, service_id: str) -> dict[str, object]:
            if service_id == "kosdaq_stock_daily":
                raise RuntimeError("temporary network failure")
            return {"status_code": 200, "row_count": 10, "raw_output": "_report/raw/path.raw.json"}

        summary = collect_from_plan(plan=_plan(), collector=collector)

        self.assertEqual(summary["successful_requests"], 1)
        self.assertEqual(summary["failed_requests"], 1)
        self.assertIn("temporary network failure", summary["failures"][0]["error"])

    def test_limit_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ValueError, "limit must be positive"):
            collect_from_plan(plan=_plan(), collector=lambda _date, _service: {}, limit=0)

    def test_cli_writes_lf_report_and_json_with_mocked_collection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan_path = root / "plan.json"
            output = root / "result.json"
            report = root / "result.md"
            plan_path.write_text(json.dumps(_plan(), ensure_ascii=False), encoding="utf-8")

            def fake_collect_one(*_args: object, **_kwargs: object) -> dict[str, object]:
                return {"status_code": 200, "row_count": 1, "raw_output": "_report/raw/mock.raw.json"}

            with patch("scripts.quant_krx_openapi_history_collect._resolve_auth_key", return_value="secret"):
                with patch("scripts.quant_krx_openapi_history_collect._collect_one", side_effect=fake_collect_one):
                    with patch(
                        "sys.argv",
                        [
                            "quant_krx_openapi_history_collect.py",
                            "--plan",
                            str(plan_path),
                            "--output",
                            str(output),
                            "--report-output",
                            str(report),
                        ],
                    ):
                        self.assertEqual(main(), 0)

            result_text = output.read_text(encoding="utf-8")
            report_text = report.read_text(encoding="utf-8")
            result_bytes = output.read_bytes()
            report_bytes = report.read_bytes()

        self.assertIn('"successful_requests": 2', result_text)
        self.assertIn("AUTH_KEY stored in report: `false`", report_text)
        self.assertNotIn("secret", result_text)
        self.assertNotIn("secret", report_text)
        self.assertNotIn(b"\r\n", result_bytes)
        self.assertNotIn(b"\r\n", report_bytes)


if __name__ == "__main__":
    unittest.main()
