from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CAPTURE = REPO_ROOT / "scripts" / "quant_kis_ohlcv_capture.py"


def _queue_row(code: str, name: str = "테스트") -> dict[str, object]:
    return {
        "sequence": 1,
        "code": code,
        "name": name,
        "market": "KOSPI",
        "tool": "domestic_stock",
        "api_type": "inquire_daily_itemchartprice",
        "params": {
            "env_dv": "real",
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": code,
            "fid_input_date_1": "20260301",
            "fid_input_date_2": "20260615",
            "fid_period_div_code": "D",
            "fid_org_adj_prc": "0",
        },
        "raw_dir": "_report/raw/2026/2026-06-15/quant/universe-ohlcv",
        "output_file": f"{code}.daily.raw.json",
    }


class QuantKisOhlcvCaptureTest(unittest.TestCase):
    def test_dry_run_validates_queue_and_writes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue = root / "requests.jsonl"
            rows = [_queue_row("000020", "동화약품"), _queue_row("000040", "KR모터스")]
            queue.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
            raw_dir = root / "raw"
            output = root / "result.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(CAPTURE),
                    "--queue",
                    str(queue),
                    "--raw-dir",
                    str(raw_dir),
                    "--dry-run",
                    "--output",
                    str(output),
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("| `dry_run` | 2 |", report)
            self.assertIn("| `000020` | 동화약품 | `dry_run` | `000020.daily.raw.json` |", report)
            self.assertIn("- Execution path: `direct_kis_openapi_sample_auth` / read-only quotation endpoint", report)
            manifest = (raw_dir / "manifest.yaml").read_text(encoding="utf-8")
            self.assertIn("dry_run: true", manifest)
            self.assertIn("dry_run: 2", manifest)

    def test_skip_existing_does_not_overwrite_raw(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue = root / "requests.jsonl"
            queue.write_text(json.dumps(_queue_row("000020"), ensure_ascii=False) + "\n", encoding="utf-8")
            raw_dir = root / "raw"
            raw_dir.mkdir()
            existing = raw_dir / "000020.daily.raw.json"
            existing.write_text('{"kept": true}\n', encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(CAPTURE),
                    "--queue",
                    str(queue),
                    "--raw-dir",
                    str(raw_dir),
                    "--dry-run",
                    "--skip-existing",
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(existing.read_text(encoding="utf-8"), '{"kept": true}\n')
            self.assertIn("| `skipped_existing` | 1 |", result.stdout)

    def test_rejects_missing_required_param(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad = _queue_row("000020")
            del bad["params"]["fid_input_iscd"]  # type: ignore[index]
            queue = root / "requests.jsonl"
            queue.write_text(json.dumps(bad, ensure_ascii=False) + "\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(CAPTURE),
                    "--queue",
                    str(queue),
                    "--raw-dir",
                    str(root / "raw"),
                    "--dry-run",
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required params", result.stderr)


if __name__ == "__main__":
    unittest.main()
