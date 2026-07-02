from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COLLECT = REPO_ROOT / "scripts" / "quant_krx_openapi_collect.py"


class QuantKrxOpenapiCollectTest(unittest.TestCase):
    def test_dry_run_defaults_to_core_services_and_redacts_key(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(COLLECT),
                "--bas-dd",
                "20250102",
                "--capture-date",
                "2026-07-03",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["bas_dd"], "20250102")
        self.assertEqual(payload["capture_date"], "2026-07-03")
        self.assertEqual(len(payload["services"]), 6)
        self.assertIn("kospi_stock_daily_20250102.raw.json", result.stdout)
        self.assertIn('"AUTH_KEY": "***"', result.stdout)
        self.assertNotIn("KRX_AUTH_KEY", result.stdout)

    def test_dry_run_can_select_one_service(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(COLLECT),
                "--bas-dd",
                "20250102",
                "--service",
                "kospi_stock_daily",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual([service["id"] for service in payload["services"]], ["kospi_stock_daily"])

    def test_invalid_bas_dd_fails(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(COLLECT),
                "--bas-dd",
                "2025-01-02",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bas-dd must be YYYYMMDD", result.stderr)


if __name__ == "__main__":
    unittest.main()
