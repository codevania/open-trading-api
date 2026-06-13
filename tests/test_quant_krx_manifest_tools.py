from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
MATERIALIZE = REPO_ROOT / "scripts" / "quant_krx_manifest_materialize.py"
VERIFY = REPO_ROOT / "scripts" / "quant_krx_manifest_verify.py"


class QuantKrxManifestToolsTest(unittest.TestCase):
    def test_materialize_then_verify_passes_for_local_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "_report" / "raw" / "2026" / "2026-06-13" / "krx" / "universe"
            raw_dir.mkdir(parents=True)
            raw_path = raw_dir / "managed_issues_current.raw.csv"
            raw_path.write_text("row_no,symbol,name\n1,000001,Fixture Corp\n", encoding="utf-8")

            manifest = root / "pending.yaml"
            manifest.write_text(
                textwrap.dedent(
                    """
                    version: "1.0"
                    snapshot:
                      as_of_date: "2026-06-13"
                      market: "KRX"
                      source_mode: "manual_snapshot"
                      downloaded_by: "manual"
                      download_verified_by_codex: false
                      status: "pending_manual_download"
                      notes: []
                    datasets:
                      - id: "managed_issues_current"
                        required: true
                        source_name: "fixture"
                        source_url: "https://example.invalid"
                        downloaded_at_kst: "TO_BE_FILLED"
                        raw_path: "_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv"
                        file_format: "csv"
                        sha256: "TO_BE_FILLED"
                        columns:
                          - "TO_BE_VERIFIED_AFTER_DOWNLOAD"
                        schema_verified_by_codex: false
                    bias_judgment:
                      current_status: "hold"
                      reason: []
                    next_step_after_manifest: []
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )
            output = raw_dir / "manifest.yaml"

            materialize = subprocess.run(
                [
                    sys.executable,
                    str(MATERIALIZE),
                    "--manifest",
                    str(manifest),
                    "--output",
                    str(output),
                    "--downloaded-at-kst",
                    "2026-06-13T12:00:00+09:00",
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(materialize.returncode, 0, materialize.stderr)
            payload = yaml.safe_load(output.read_text(encoding="utf-8"))
            dataset = payload["datasets"][0]
            self.assertEqual(payload["snapshot"]["status"], "raw_files_materialized")
            self.assertEqual(dataset["columns"], ["row_no", "symbol", "name"])
            self.assertEqual(dataset["downloaded_at_kst"], "2026-06-13T12:00:00+09:00")
            self.assertEqual(dataset["status"], "materialized_from_raw")
            self.assertTrue(dataset["schema_verified_by_codex"])
            self.assertEqual(len(dataset["sha256"]), 64)

            verify = subprocess.run(
                [sys.executable, str(VERIFY), "--manifest", str(output)],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)
            self.assertIn("Overall status: `pass`", verify.stdout)

    def test_materialize_fails_when_required_raw_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "pending.yaml"
            manifest.write_text(
                textwrap.dedent(
                    """
                    version: "1.0"
                    snapshot:
                      as_of_date: "2026-06-13"
                      market: "KRX"
                      source_mode: "manual_snapshot"
                    datasets:
                      - id: "managed_issues_current"
                        required: true
                        raw_path: "_report/raw/2026/2026-06-13/krx/universe/managed_issues_current.raw.csv"
                        file_format: "csv"
                        sha256: "TO_BE_FILLED"
                        columns:
                          - "TO_BE_VERIFIED_AFTER_DOWNLOAD"
                    """
                ).strip()
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(MATERIALIZE), "--manifest", str(manifest)],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("required raw files are missing", result.stderr)


if __name__ == "__main__":
    unittest.main()
