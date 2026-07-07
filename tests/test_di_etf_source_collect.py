from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_etf_source_collect.py"


MANIFEST = """\
core_etfs:
  - symbol: VOO
    name: Vanguard S&P 500 ETF
    source_url: https://investor.vanguard.com/investment-products/etfs/profile/voo
  - symbol: VTI
    name: Vanguard Total Stock Market ETF
    source_url: https://investor.vanguard.com/investment-products/etfs/profile/vti
korea_listed_etfs_to_verify:
  - symbol: "360750"
    name: TIGER US S&P500
    source_url: null
satellite_etfs_to_verify:
  - symbol: QQQ
    name: Invesco QQQ Trust
    source_url: https://www.invesco.com/qqq-etf/en/about.html
"""


class DiEtfSourceCollectTest(unittest.TestCase):
    def test_dry_run_lists_only_candidates_with_source_urls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "candidates.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--raw-root",
                    str(Path(tmp) / "raw"),
                    "--run-date",
                    "2026-07-08",
                    "--dry-run",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["dry_run"])
            self.assertEqual(payload["request_count"], 3)
            self.assertEqual([item["symbol"] for item in payload["requests"]], ["VOO", "VTI", "QQQ"])
            self.assertNotIn("360750", json.dumps(payload))
            self.assertIn("2026/2026-07-08/di/etf-sources/VOO", payload["requests"][0]["output_dir"].replace("\\", "/"))

    def test_symbol_filter_limits_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "candidates.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--run-date",
                    "2026-07-08",
                    "--symbol",
                    "voo",
                    "--dry-run",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["request_count"], 1)
            self.assertEqual(payload["requests"][0]["symbol"], "VOO")

    def test_rejects_non_object_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "bad.yaml"
            manifest.write_text("- not\n- object\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--candidate-file", str(manifest), "--dry-run"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("expected YAML object", result.stderr)

    def test_rejects_non_object_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "bad.yaml"
            manifest.write_text(
                """\
core_etfs:
  - not an object
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--candidate-file", str(manifest), "--dry-run"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("core_etfs[0]: expected candidate object", result.stderr)


if __name__ == "__main__":
    unittest.main()
