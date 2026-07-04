from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COLLECT = REPO_ROOT / "scripts" / "di_opendart_collect.py"


def _load_collect_module():
    spec = importlib.util.spec_from_file_location("di_opendart_collect", COLLECT)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load di_opendart_collect.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DiOpenDartCollectTest(unittest.TestCase):
    def test_meta_path_keeps_raw_json_name(self) -> None:
        module = _load_collect_module()

        self.assertEqual(module._meta_path(Path("company.raw.json")).name, "company.raw.json.meta.json")

    def test_dry_run_redacts_key_and_plans_default_outputs(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(COLLECT),
                "--stock-code",
                "005930",
                "--run-date",
                "2026-07-05",
                "--business-year",
                "2025",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["source"], "OpenDART")
        self.assertEqual(payload["symbol"], "005930")
        self.assertIn("_report/raw/2026/2026-07-05/dart/005930", payload["raw_dir"])
        financial_requests = [request for request in payload["requests"] if request["id"].startswith("financials_")]
        self.assertEqual(len(financial_requests), 1)
        self.assertIn("corpCode.raw.zip", result.stdout)
        self.assertIn("financials_2025_11011_CFS.raw.json", result.stdout)
        self.assertIn('"crtfc_key": "***"', result.stdout)
        self.assertNotIn("OPENDART_API_KEY", result.stdout)

    def test_invalid_stock_code_fails(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(COLLECT),
                "--stock-code",
                "MSFT",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stock-code must be a 6 digit KRX code", result.stderr)


if __name__ == "__main__":
    unittest.main()
