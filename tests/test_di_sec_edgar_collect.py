from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COLLECT = REPO_ROOT / "scripts" / "di_sec_edgar_collect.py"


def _load_collect_module():
    spec = importlib.util.spec_from_file_location("di_sec_edgar_collect", COLLECT)
    if spec is None or spec.loader is None:
        raise RuntimeError("failed to load di_sec_edgar_collect.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DiSecEdgarCollectTest(unittest.TestCase):
    def test_meta_path_keeps_raw_json_name(self) -> None:
        module = _load_collect_module()

        self.assertEqual(module._meta_path(Path("submissions.raw.json")).name, "submissions.raw.json.meta.json")

    def test_dry_run_redacts_user_agent_and_plans_default_outputs(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(COLLECT),
                "--ticker",
                "MSFT",
                "--run-date",
                "2026-07-05",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["source"], "SEC EDGAR")
        self.assertEqual(payload["symbol"], "MSFT")
        self.assertIn("_report/raw/2026/2026-07-05/sec/MSFT", payload["raw_dir"])
        self.assertIn("submissions/CIK<resolved>.json", result.stdout)
        self.assertIn("companyfacts/CIK<resolved>.json", result.stdout)
        self.assertIn('"User-Agent": "***"', result.stdout)
        self.assertNotIn("SEC_USER_AGENT", result.stdout)

    def test_dry_run_can_use_cik_and_skip_concepts(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(COLLECT),
                "--cik",
                "789019",
                "--run-date",
                "2026-07-05",
                "--skip-concepts",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["symbol"], "CIK0000789019")
        self.assertIn("submissions/CIK0000789019.json", result.stdout)
        self.assertNotIn("concepts", result.stdout)

    def test_invalid_ticker_fails(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(COLLECT),
                "--ticker",
                "1234",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ticker must start with a letter", result.stderr)


if __name__ == "__main__":
    unittest.main()
