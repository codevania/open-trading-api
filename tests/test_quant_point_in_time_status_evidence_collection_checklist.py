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

from scripts.quant_point_in_time_status_evidence_collection_checklist import (
    build_evidence_collection_checklist,
    main,
    render_report,
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


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: tuple[str, ...] = QUEUE_FIELDS) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _queue_row(**overrides: str) -> dict[str, str]:
    row = {
        "batch_id": "P2-001",
        "priority": "2",
        "blocker_type": "release_resume_evidence",
        "status_type": "managed_issue",
        "suggested_source": "krx_data_marketplace;kind;manual_snapshot",
        "manifest_source": "krx_data_marketplace;kind;manual_snapshot",
        "collection_status": "pending_release_resume_evidence",
        "market_scope": "KOSDAQ",
        "row_count": "25",
        "code_count": "25",
        "code_sample": "001840;008290;016790",
        "required_evidence": "official release/resume evidence",
        "source_plan_rows": "14;19;25",
        "order_intent_generated": "false",
        "notes": "release_resume_collection_target;plan_only_not_source_coverage",
    }
    row.update(overrides)
    return row


class QuantPointInTimeStatusEvidenceCollectionChecklistTest(unittest.TestCase):
    def test_builds_checklist_for_all_priorities_without_promoting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            queue = Path(tmp) / "queue.rows.csv"
            _write_csv(
                queue,
                [
                    _queue_row(
                        batch_id="P1-001",
                        priority="1",
                        blocker_type="source_manifest_evidence",
                        status_type="delisting",
                        collection_status="pending_raw_evidence",
                        market_scope="required_manifest_scope",
                        row_count="1",
                        code_count="0",
                        code_sample="not_applicable",
                    ),
                    _queue_row(),
                    _queue_row(
                        batch_id="P3-001",
                        priority="3",
                        blocker_type="market_label_resolution",
                        status_type="delisting",
                        suggested_source="kind",
                        collection_status="pending_market_label_evidence",
                        market_scope="UNKNOWN",
                        row_count="9",
                        code_count="9",
                    ),
                ],
            )

            rows, summary = build_evidence_collection_checklist(queue)
            report = render_report(rows=rows, summary=summary)

        self.assertEqual(summary["checklist_batches"], 3)
        self.assertEqual(summary["queued_source_rows"], 35)
        self.assertEqual(summary["pending_batches"], 3)
        self.assertEqual([row["batch_id"] for row in rows], ["P1-001", "P2-001", "P3-001"])
        self.assertEqual(rows[1]["raw_path_suggestion"], "_report/raw/quant/status-evidence/p2-001/")
        self.assertIn("P1 Source Manifest Evidence", report)
        self.assertIn("P2 Release/Resume Evidence", report)
        self.assertIn("P3 Market Label Evidence", report)
        self.assertIn("not source coverage evidence", report)
        self.assertIn("- Backtest readiness impact: `hold`", report)

    def test_missing_queue_column_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            queue = Path(tmp) / "queue.rows.csv"
            fields = tuple(field for field in QUEUE_FIELDS if field != "order_intent_generated")
            row = {key: value for key, value in _queue_row().items() if key in fields}
            _write_csv(queue, [row], fieldnames=fields)

            with self.assertRaisesRegex(ValueError, "missing required columns: order_intent_generated"):
                build_evidence_collection_checklist(queue)

    def test_order_intent_rows_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            queue = Path(tmp) / "queue.rows.csv"
            _write_csv(queue, [_queue_row(order_intent_generated="true")])

            with self.assertRaisesRegex(ValueError, "order intent"):
                build_evidence_collection_checklist(queue)

    def test_cli_writes_lf_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue = root / "queue.rows.csv"
            report_output = root / "evidence-checklist.md"
            _write_csv(queue, [_queue_row()])

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_evidence_collection_checklist.py",
                    "--queue",
                    str(queue),
                    "--report-output",
                    str(report_output),
                ],
            ):
                self.assertEqual(main(), 0)

            report_bytes = report_output.read_bytes()
            report_text = report_output.read_text(encoding="utf-8")

        self.assertNotIn(b"\r\n", report_bytes)
        self.assertIn("| Checklist batches | 1 |", report_text)


if __name__ == "__main__":
    unittest.main()
