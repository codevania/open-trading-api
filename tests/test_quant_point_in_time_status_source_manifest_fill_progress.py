from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.quant_point_in_time_status_source_manifest_fill_progress import (
    main,
    summarize_fill_progress,
)


FILL_PACKET_FIELDS = (
    "batch_id",
    "status_type",
    "source",
    "coverage_start",
    "coverage_end",
    "evidence_capture_status",
    "source_url_to_fill",
    "raw_path_to_fill",
    "confidence_to_fill",
    "order_intent_generated",
)


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FILL_PACKET_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _fill_packet_row(**overrides: str) -> dict[str, str]:
    row = {
        "batch_id": "P1-001",
        "status_type": "managed_issue",
        "source": "kind",
        "coverage_start": "2025-01-02",
        "coverage_end": "2025-04-18",
        "evidence_capture_status": "pending_official_raw_capture",
        "source_url_to_fill": "",
        "raw_path_to_fill": "",
        "confidence_to_fill": "",
        "order_intent_generated": "false",
    }
    row.update(overrides)
    return row


class QuantPointInTimeStatusSourceManifestFillProgressTest(unittest.TestCase):
    def test_blank_packet_reports_blocked_rows_without_promoting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fill_packet = Path(tmp) / "fill-packet.rows.csv"
            _write_csv(fill_packet, [_fill_packet_row(), _fill_packet_row(batch_id="P1-002", source="manual_snapshot")])

            rows, summary = summarize_fill_progress(fill_packet_path=fill_packet, repo_root=Path(tmp))

        self.assertEqual(summary["fill_packet_rows"], 2)
        self.assertEqual(summary["materializable_rows"], 0)
        self.assertEqual(summary["blocked_rows"], 2)
        self.assertEqual(summary["missing_counts"]["source_url_to_fill"], 2)
        self.assertEqual(summary["missing_counts"]["raw_path_to_fill"], 2)
        self.assertEqual(summary["missing_counts"]["confidence_to_fill"], 2)
        self.assertEqual(summary["missing_counts"]["evidence_capture_status"], 2)
        self.assertTrue(all(row["materializable_status"] == "blocked" for row in rows))

    def test_filled_packet_reports_materializable_and_raw_path_existence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw = root / "_report" / "raw" / "2026" / "2026-07-10" / "kind.json"
            raw.parent.mkdir(parents=True)
            raw.write_text("{}", encoding="utf-8")
            fill_packet = root / "fill-packet.rows.csv"
            _write_csv(
                fill_packet,
                [
                    _fill_packet_row(
                        evidence_capture_status="captured_official_raw",
                        source_url_to_fill="https://kind.krx.co.kr/example",
                        raw_path_to_fill="_report/raw/2026/2026-07-10/kind.json",
                        confidence_to_fill="high",
                    )
                ],
            )

            rows, summary = summarize_fill_progress(fill_packet_path=fill_packet, repo_root=root)

        self.assertEqual(summary["materializable_rows"], 1)
        self.assertEqual(summary["blocked_rows"], 0)
        self.assertEqual(summary["raw_path_exists_rows"], 1)
        self.assertEqual(summary["missing_counts"], {})
        self.assertEqual(rows[0]["materializable_status"], "ready")
        self.assertEqual(rows[0]["raw_path_exists"], "true")
        self.assertEqual(rows[0]["missing_fields"], "none")

    def test_cli_writes_lf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fill_packet = root / "fill-packet.rows.csv"
            rows_output = root / "fill-progress.rows.csv"
            report_output = root / "fill-progress.md"
            _write_csv(fill_packet, [_fill_packet_row()])

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_source_manifest_fill_progress.py",
                    "--fill-packet",
                    str(fill_packet),
                    "--rows-output",
                    str(rows_output),
                    "--report-output",
                    str(report_output),
                    "--repo-root",
                    str(root),
                ],
            ):
                self.assertEqual(main(), 0)

            rows_bytes = rows_output.read_bytes()
            report_bytes = report_output.read_bytes()
            report_text = report_output.read_text(encoding="utf-8")

        self.assertNotIn(b"\r\n", rows_bytes)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertIn("Point-in-Time Status Source Manifest Fill Progress", report_text)
        self.assertIn("| Materializable rows | 0 |", report_text)
        self.assertIn("- Backtest readiness impact: `hold`", report_text)


if __name__ == "__main__":
    unittest.main()
