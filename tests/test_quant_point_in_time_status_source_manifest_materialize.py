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

from scripts.quant_point_in_time_status_source_manifest_materialize import (
    materialize_source_manifest,
    main,
)


FILL_PACKET_FIELDS = (
    "batch_id",
    "manifest_draft_row_number",
    "status_type",
    "source",
    "coverage_start",
    "coverage_end",
    "market_labels",
    "lifecycle_target_groups",
    "lifecycle_target_codes",
    "candidate_tables",
    "allowed_url_prefixes",
    "suggested_source",
    "required_evidence",
    "collection_status",
    "evidence_capture_status",
    "source_url_to_fill",
    "raw_path_to_fill",
    "confidence_to_fill",
    "order_intent_generated",
    "manifest_notes",
    "queue_notes",
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _fill_packet_row(**overrides: str) -> dict[str, str]:
    row = {
        "batch_id": "P1-001",
        "manifest_draft_row_number": "2",
        "status_type": "managed_issue",
        "source": "kind",
        "coverage_start": "2025-01-02",
        "coverage_end": "2025-04-18",
        "market_labels": "KOSPI;KOSDAQ",
        "lifecycle_target_groups": "104",
        "lifecycle_target_codes": "104",
        "candidate_tables": "Managed issue event",
        "allowed_url_prefixes": "https://kind.krx.co.kr/",
        "suggested_source": "kind:Managed issue event",
        "required_evidence": "fill source_url, raw_path, and confidence",
        "collection_status": "pending_raw_evidence",
        "evidence_capture_status": "captured_official_raw",
        "source_url_to_fill": "https://kind.krx.co.kr/example",
        "raw_path_to_fill": "_report\\raw\\2026\\2026-07-10\\kind-managed-issues.json",
        "confidence_to_fill": "high",
        "order_intent_generated": "false",
        "manifest_notes": "draft_only",
        "queue_notes": "plan_only_not_source_coverage",
    }
    row.update(overrides)
    return row


class QuantPointInTimeStatusSourceManifestMaterializeTest(unittest.TestCase):
    def test_materializes_filled_packet_to_manifest_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fill_packet = Path(tmp) / "fill-packet.rows.csv"
            _write_csv(fill_packet, FILL_PACKET_FIELDS, [_fill_packet_row()])

            rows, summary = materialize_source_manifest(fill_packet_path=fill_packet)

        self.assertEqual(summary["manifest_rows"], 1)
        self.assertEqual(summary["status_counts"], {"managed_issue": 1})
        self.assertEqual(rows[0]["status_type"], "managed_issue")
        self.assertEqual(rows[0]["source"], "kind")
        self.assertEqual(rows[0]["source_url"], "https://kind.krx.co.kr/example")
        self.assertEqual(rows[0]["raw_path"], "_report/raw/2026/2026-07-10/kind-managed-issues.json")
        self.assertEqual(rows[0]["confidence"], "high")
        self.assertIn("batch_id=P1-001", rows[0]["notes"])

    def test_blank_fill_fields_raise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fill_packet = Path(tmp) / "fill-packet.rows.csv"
            _write_csv(
                fill_packet,
                FILL_PACKET_FIELDS,
                [_fill_packet_row(source_url_to_fill="", raw_path_to_fill="", confidence_to_fill="")],
            )

            with self.assertRaisesRegex(ValueError, "source_url_to_fill is empty"):
                materialize_source_manifest(fill_packet_path=fill_packet)

    def test_pending_capture_status_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fill_packet = Path(tmp) / "fill-packet.rows.csv"
            _write_csv(
                fill_packet,
                FILL_PACKET_FIELDS,
                [_fill_packet_row(evidence_capture_status="pending_official_raw_capture")],
            )

            with self.assertRaisesRegex(ValueError, "evidence_capture_status is still pending"):
                materialize_source_manifest(fill_packet_path=fill_packet)

    def test_cli_writes_lf_manifest_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fill_packet = root / "fill-packet.rows.csv"
            output = root / "manifest.csv"
            report = root / "manifest.md"
            _write_csv(fill_packet, FILL_PACKET_FIELDS, [_fill_packet_row()])

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_source_manifest_materialize.py",
                    "--fill-packet",
                    str(fill_packet),
                    "--output",
                    str(output),
                    "--report-output",
                    str(report),
                ],
            ):
                self.assertEqual(main(), 0)

            output_bytes = output.read_bytes()
            report_bytes = report.read_bytes()
            output_text = output.read_text(encoding="utf-8-sig")
            report_text = report.read_text(encoding="utf-8")

        self.assertNotIn(b"\r\n", output_bytes)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertIn("status_type,coverage_start,coverage_end,source,source_url,raw_path,confidence,notes", output_text)
        self.assertIn("Point-in-Time Status Source Manifest Materialize", report_text)
        self.assertIn("- Backtest readiness impact: `hold`", report_text)


if __name__ == "__main__":
    unittest.main()
