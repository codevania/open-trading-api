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

from scripts.quant_point_in_time_status_source_manifest_fill_packet import (
    build_source_manifest_fill_packet,
    main,
)


MANIFEST_FIELDS = (
    "status_type",
    "coverage_start",
    "coverage_end",
    "source",
    "source_url",
    "raw_path",
    "confidence",
    "lifecycle_target_groups",
    "lifecycle_target_codes",
    "market_labels",
    "candidate_tables",
    "allowed_url_prefixes",
    "draft_status",
    "notes",
)
QUEUE_FIELDS = (
    "batch_id",
    "priority",
    "blocker_type",
    "status_type",
    "suggested_source",
    "manifest_source",
    "collection_status",
    "market_scope",
    "row_count",
    "code_count",
    "code_sample",
    "required_evidence",
    "source_plan_rows",
    "order_intent_generated",
    "notes",
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _manifest_row(status_type: str = "managed_issue", source: str = "kind") -> dict[str, str]:
    return {
        "status_type": status_type,
        "coverage_start": "2025-01-02",
        "coverage_end": "2025-04-18",
        "source": source,
        "source_url": "",
        "raw_path": "",
        "confidence": "",
        "lifecycle_target_groups": "104",
        "lifecycle_target_codes": "104",
        "market_labels": "KOSPI;KOSDAQ",
        "candidate_tables": "Managed issue event",
        "allowed_url_prefixes": "https://kind.krx.co.kr/",
        "draft_status": "pending_raw_evidence",
        "notes": "draft_only",
    }


def _queue_row(
    batch_id: str = "P1-001",
    status_type: str = "managed_issue",
    manifest_source: str = "kind",
) -> dict[str, str]:
    return {
        "batch_id": batch_id,
        "priority": "1",
        "blocker_type": "source_manifest_evidence",
        "status_type": status_type,
        "suggested_source": f"{manifest_source}:Managed issue event",
        "manifest_source": manifest_source,
        "collection_status": "pending_raw_evidence",
        "market_scope": "KOSPI;KOSDAQ",
        "row_count": "1",
        "code_count": "0",
        "code_sample": "not_applicable",
        "required_evidence": "fill source_url, raw_path, and confidence",
        "source_plan_rows": "1",
        "order_intent_generated": "false",
        "notes": "plan_only_not_source_coverage",
    }


class QuantPointInTimeStatusSourceManifestFillPacketTest(unittest.TestCase):
    def test_builds_p1_fill_packet_from_queue_and_manifest_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.rows.csv"
            queue = root / "queue.rows.csv"
            _write_csv(
                manifest,
                MANIFEST_FIELDS,
                [_manifest_row(), _manifest_row("delisting", "manual_snapshot")],
            )
            _write_csv(
                queue,
                QUEUE_FIELDS,
                [_queue_row(), _queue_row("P1-002", "delisting", "manual_snapshot")],
            )

            rows, summary = build_source_manifest_fill_packet(
                source_manifest_draft_path=manifest,
                evidence_queue_path=queue,
            )

        self.assertEqual(summary["manifest_draft_rows"], 2)
        self.assertEqual(summary["p1_queue_batches"], 2)
        self.assertEqual(summary["packet_rows"], 2)
        self.assertEqual(summary["unmatched_manifest_rows"], [])
        self.assertEqual(rows[0]["batch_id"], "P1-001")
        self.assertEqual(rows[0]["manifest_draft_row_number"], "2")
        self.assertEqual(rows[0]["evidence_capture_status"], "pending_official_raw_capture")
        self.assertEqual(rows[0]["source_url_hint"], "https://kind.krx.co.kr/")
        self.assertEqual(
            rows[0]["raw_path_suggestion"],
            "_report/raw/quant/status-source-manifest/20250102-20250418/p1-001-managed-issue-kind.json",
        )
        self.assertEqual(rows[0]["source_url_to_fill"], "")
        self.assertEqual(rows[0]["raw_path_to_fill"], "")
        self.assertEqual(rows[0]["confidence_to_fill"], "")
        self.assertTrue(all(row["order_intent_generated"] == "false" for row in rows))

    def test_missing_manifest_match_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.rows.csv"
            queue = root / "queue.rows.csv"
            _write_csv(manifest, MANIFEST_FIELDS, [_manifest_row("managed_issue", "kind")])
            _write_csv(queue, QUEUE_FIELDS, [_queue_row("P1-001", "delisting", "manual_snapshot")])

            with self.assertRaisesRegex(ValueError, "no matching manifest draft row: delisting/manual_snapshot"):
                build_source_manifest_fill_packet(
                    source_manifest_draft_path=manifest,
                    evidence_queue_path=queue,
                )

    def test_cli_writes_lf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.rows.csv"
            queue = root / "queue.rows.csv"
            output = root / "fill-packet.rows.csv"
            report = root / "fill-packet.md"
            _write_csv(manifest, MANIFEST_FIELDS, [_manifest_row()])
            _write_csv(queue, QUEUE_FIELDS, [_queue_row()])

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_source_manifest_fill_packet.py",
                    "--source-manifest-draft",
                    str(manifest),
                    "--evidence-queue",
                    str(queue),
                    "--output",
                    str(output),
                    "--report-output",
                    str(report),
                ],
            ):
                self.assertEqual(main(), 0)

            output_bytes = output.read_bytes()
            report_bytes = report.read_bytes()
            report_text = report.read_text(encoding="utf-8")

        self.assertNotIn(b"\r\n", output_bytes)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertIn("Point-in-Time Status Source Manifest Fill Packet", report_text)
        self.assertIn("- Backtest readiness impact: `hold`", report_text)
        self.assertIn("`raw_path_suggestion`", report_text)


if __name__ == "__main__":
    unittest.main()
