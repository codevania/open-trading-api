from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.quant_kis_demo_account_preflight import render_report, run_preflight


REQUIRED_METHODS = (
    "inquire_psbl_order",
    "inquire_psbl_sell",
    "inquire_balance",
    "order_cash",
    "order_rvsecncl",
)


def _write_api_config(path: Path, missing: str | None = None) -> None:
    apis = {method: {"method": method} for method in REQUIRED_METHODS if method != missing}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"apis": apis}), encoding="utf-8")


class QuantKisDemoAccountPreflightTest(unittest.TestCase):
    def test_accepts_complete_mcp_env_config_without_exposing_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / ".env.kis"
            config.write_text(
                "\n".join(
                    [
                        "KIS_PAPER_APP_KEY=paper_app_key_12345",
                        "KIS_PAPER_APP_SECRET=paper_secret_12345",
                        "KIS_PAPER_STOCK=12345678",
                        "KIS_PROD_TYPE=01",
                        "KIS_URL_REST_PAPER=https://openapivts.koreainvestment.com:29443",
                    ]
                ),
                encoding="utf-8",
            )
            api_config = root / "domestic_stock.json"
            _write_api_config(api_config)

            summary = run_preflight(config, api_config)
            report = render_report(summary)

        self.assertTrue(summary["ready_for_read_only_demo_account_calls"])
        self.assertEqual(summary["required_failures"], 0)
        self.assertNotIn("paper_secret_12345", report)
        self.assertNotIn("12345678", report)

    def test_rejects_placeholder_or_malformed_demo_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / ".env.kis"
            config.write_text(
                "\n".join(
                    [
                        "KIS_PAPER_APP_KEY=your_paper_app_key",
                        "KIS_PAPER_APP_SECRET=short",
                        "KIS_PAPER_STOCK=1234",
                        "KIS_URL_REST_PAPER=http://example.test",
                    ]
                ),
                encoding="utf-8",
            )
            api_config = root / "domestic_stock.json"
            _write_api_config(api_config)

            summary = run_preflight(config, api_config)

        self.assertFalse(summary["ready_for_read_only_demo_account_calls"])
        failures = {check.check: check.detail for check in summary["checks"] if check.status == "fail"}
        self.assertIn("demo_app_key", failures)
        self.assertIn("demo_app_secret", failures)
        self.assertIn("demo_stock_account", failures)
        self.assertIn("demo_rest_url", failures)

    def test_empty_demo_rest_url_is_warning_because_template_default_may_apply(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / ".env.kis"
            config.write_text(
                "\n".join(
                    [
                        "KIS_PAPER_APP_KEY=paper_app_key_12345",
                        "KIS_PAPER_APP_SECRET=paper_secret_12345",
                        "KIS_PAPER_STOCK=12345678",
                        "KIS_PROD_TYPE=01",
                        "KIS_URL_REST_PAPER=",
                    ]
                ),
                encoding="utf-8",
            )
            api_config = root / "domestic_stock.json"
            _write_api_config(api_config)

            summary = run_preflight(config, api_config)

        self.assertTrue(summary["ready_for_read_only_demo_account_calls"])
        warnings = {check.check: check.detail for check in summary["checks"] if check.status == "warn"}
        self.assertIn("demo_rest_url", warnings)

    def test_accepts_yaml_aliases_from_examples_config_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "kis_devlp.yaml"
            config.write_text(
                "\n".join(
                    [
                        "paper_app: paper_app_key_12345",
                        "paper_sec: paper_secret_12345",
                        "my_paper_stock: '12345678'",
                        "my_prod: '01'",
                        "vps: https://openapivts.koreainvestment.com:29443",
                    ]
                ),
                encoding="utf-8",
            )
            api_config = root / "domestic_stock.json"
            _write_api_config(api_config)

            summary = run_preflight(config, api_config)

        self.assertTrue(summary["ready_for_read_only_demo_account_calls"])
        self.assertEqual(summary["status_counts"].get("fail", 0), 0)

    def test_missing_required_api_method_blocks_read_only_account_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / ".env.kis"
            config.write_text(
                "\n".join(
                    [
                        "KIS_PAPER_APP_KEY=paper_app_key_12345",
                        "KIS_PAPER_APP_SECRET=paper_secret_12345",
                        "KIS_PAPER_STOCK=12345678",
                        "KIS_PROD_TYPE=01",
                        "KIS_URL_REST_PAPER=https://openapivts.koreainvestment.com:29443",
                    ]
                ),
                encoding="utf-8",
            )
            api_config = root / "domestic_stock.json"
            _write_api_config(api_config, missing="inquire_psbl_sell")

            summary = run_preflight(config, api_config)

        self.assertFalse(summary["ready_for_read_only_demo_account_calls"])
        self.assertEqual(summary["api_failures"], 1)


if __name__ == "__main__":
    unittest.main()
