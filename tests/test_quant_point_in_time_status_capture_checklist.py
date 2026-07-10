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

from scripts.quant_point_in_time_status_capture_checklist import (
    build_capture_checklist,
    main,
    render_report,
)


FILL_PACKET_FIELDS = (
    "batch_id",
    "status_type",
    "source",
    "coverage_start",
    "coverage_end",
    "candidate_tables",
    "source_url_hint",
    "raw_path_suggestion",
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
        "candidate_tables": "Managed issue event",
        "source_url_hint": "https://kind.krx.co.kr/",
        "raw_path_suggestion": "_report/raw/quant/status-source-manifest/20250102-20250418/p1-001-managed-issue-kind.json",
        "evidence_capture_status": "pending_official_raw_capture",
        "source_url_to_fill": "",
        "raw_path_to_fill": "",
        "confidence_to_fill": "",
        "order_intent_generated": "false",
    }
    row.update(overrides)
    return row


class QuantPointInTimeStatusCaptureChecklistTest(unittest.TestCase):
    def test_blank_packet_renders_pending_operator_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fill_packet = Path(tmp) / "fill-packet.rows.csv"
            _write_csv(fill_packet, [_fill_packet_row()])

            rows, summary = build_capture_checklist(fill_packet)
            report = render_report(rows=rows, summary=summary)

        self.assertEqual(summary["checklist_rows"], 1)
        self.assertEqual(summary["pending_rows"], 1)
        self.assertEqual(summary["ready_rows"], 0)
        self.assertEqual(rows[0]["capture_state"], "pending_official_capture")
        self.assertIn("Point-in-Time Status P1 Official Capture Checklist", report)
        self.assertIn("not source coverage evidence", report)
        self.assertIn("raw_path_suggestion", report)
        self.assertIn("- Backtest readiness impact: `hold`", report)

    def test_filled_packet_renders_ready_row_without_promoting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fill_packet = Path(tmp) / "fill-packet.rows.csv"
            _write_csv(
                fill_packet,
                [
                    _fill_packet_row(
                        evidence_capture_status="captured_official_raw",
                        source_url_to_fill="https://kind.krx.co.kr/example",
                        raw_path_to_fill="_report/raw/quant/status-source-manifest/20250102-20250418/p1-001.json",
                        confidence_to_fill="high",
                    )
                ],
            )

            rows, summary = build_capture_checklist(fill_packet)

        self.assertEqual(summary["pending_rows"], 0)
        self.assertEqual(summary["ready_rows"], 1)
        self.assertEqual(rows[0]["capture_state"], "ready_for_materialization")

    def test_order_intent_rows_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fill_packet = Path(tmp) / "fill-packet.rows.csv"
            _write_csv(fill_packet, [_fill_packet_row(order_intent_generated="true")])

            with self.assertRaisesRegex(ValueError, "order intent"):
                build_capture_checklist(fill_packet)

    def test_cli_writes_lf_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fill_packet = root / "fill-packet.rows.csv"
            report_output = root / "capture-checklist.md"
            _write_csv(fill_packet, [_fill_packet_row()])

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_capture_checklist.py",
                    "--fill-packet",
                    str(fill_packet),
                    "--report-output",
                    str(report_output),
                ],
            ):
                self.assertEqual(main(), 0)

            report_bytes = report_output.read_bytes()
            report_text = report_output.read_text(encoding="utf-8")

        self.assertNotIn(b"\r\n", report_bytes)
        self.assertIn("| Pending rows | 1 |", report_text)


if __name__ == "__main__":
    unittest.main()
