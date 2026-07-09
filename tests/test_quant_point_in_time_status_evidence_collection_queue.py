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

from scripts.quant_point_in_time_status_evidence_collection_queue import build_evidence_collection_queue, main


PLAN_FIELDS = (
    "priority",
    "blocker_type",
    "status_type",
    "code",
    "market",
    "lifecycle_gap_status",
    "target_groups",
    "active_like_rows",
    "release_like_rows",
    "manifest_source",
    "manifest_status",
    "unknown_market_target",
    "suggested_source",
    "required_evidence",
    "collection_status",
    "order_intent_generated",
    "notes",
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _plan_row(
    *,
    priority: str,
    blocker_type: str,
    status_type: str = "managed_issue",
    code: str = "",
    market: str = "",
    suggested_source: str = "kind",
    manifest_source: str = "kind",
    collection_status: str,
    unknown_market_target: str = "false",
) -> dict[str, str]:
    return {
        "priority": priority,
        "blocker_type": blocker_type,
        "status_type": status_type,
        "code": code,
        "market": market,
        "lifecycle_gap_status": "missing_release_resume_evidence" if priority == "2" else "",
        "target_groups": "1",
        "active_like_rows": "2" if priority == "2" else "",
        "release_like_rows": "0" if priority == "2" else "",
        "manifest_source": manifest_source,
        "manifest_status": "requires_filled_manifest",
        "unknown_market_target": unknown_market_target,
        "suggested_source": suggested_source,
        "required_evidence": "official evidence",
        "collection_status": collection_status,
        "order_intent_generated": "false",
        "notes": "unit-test",
    }


class QuantPointInTimeStatusEvidenceCollectionQueueTest(unittest.TestCase):
    def test_builds_chunked_batch_queue_without_order_intents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.rows.csv"
            _write_csv(
                plan,
                PLAN_FIELDS,
                [
                    _plan_row(
                        priority="1",
                        blocker_type="source_manifest_evidence",
                        suggested_source="kind:Managed issue event",
                        collection_status="pending_raw_evidence",
                    ),
                    _plan_row(
                        priority="1",
                        blocker_type="source_manifest_evidence",
                        suggested_source="krx_data_marketplace:Designated details",
                        manifest_source="krx_data_marketplace",
                        collection_status="pending_raw_evidence",
                    ),
                    _plan_row(
                        priority="2",
                        blocker_type="release_resume_evidence",
                        code="000001",
                        market="KOSPI",
                        collection_status="pending_release_resume_evidence",
                    ),
                    _plan_row(
                        priority="2",
                        blocker_type="release_resume_evidence",
                        code="000002",
                        market="KOSPI",
                        collection_status="pending_release_resume_evidence",
                    ),
                    _plan_row(
                        priority="2",
                        blocker_type="release_resume_evidence",
                        code="000003",
                        market="KOSPI",
                        collection_status="pending_release_resume_evidence",
                    ),
                    _plan_row(
                        priority="3",
                        blocker_type="market_label_resolution",
                        status_type="trading_halt",
                        code="0099X0",
                        market="UNKNOWN",
                        collection_status="pending_market_label_evidence",
                        unknown_market_target="true",
                    ),
                ],
            )

            rows, summary = build_evidence_collection_queue(evidence_plan_path=plan, batch_size=2)

        self.assertEqual(summary["input_rows"], 6)
        self.assertEqual(summary["queued_rows"], 6)
        self.assertEqual(summary["queue_batches"], 5)
        self.assertEqual([row["priority"] for row in rows], ["1", "1", "2", "2", "3"])
        self.assertEqual([row["row_count"] for row in rows if row["priority"] == "2"], ["2", "1"])
        self.assertTrue(all(row["order_intent_generated"] == "false" for row in rows))
        release_batch = next(row for row in rows if row["priority"] == "2" and row["row_count"] == "2")
        self.assertEqual(release_batch["code_count"], "2")
        self.assertEqual(release_batch["code_sample"], "000001;000002")
        manifest_batch = next(row for row in rows if row["batch_id"] == "P1-001")
        self.assertEqual(manifest_batch["code_sample"], "not_applicable")
        self.assertIn("plan_only_not_source_coverage", manifest_batch["notes"])

    def test_missing_plan_column_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "plan.rows.csv"
            fields = tuple(field for field in PLAN_FIELDS if field != "order_intent_generated")
            row = {key: value for key, value in _plan_row(
                priority="1",
                blocker_type="source_manifest_evidence",
                collection_status="pending_raw_evidence",
            ).items() if key in fields}
            _write_csv(plan, fields, [row])

            with self.assertRaisesRegex(ValueError, "missing required columns: order_intent_generated"):
                build_evidence_collection_queue(evidence_plan_path=plan)

    def test_cli_writes_lf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = root / "plan.rows.csv"
            output = root / "queue.rows.csv"
            report = root / "queue.md"
            _write_csv(
                plan,
                PLAN_FIELDS,
                [
                    _plan_row(
                        priority="1",
                        blocker_type="source_manifest_evidence",
                        collection_status="pending_raw_evidence",
                    )
                ],
            )

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_evidence_collection_queue.py",
                    "--evidence-plan",
                    str(plan),
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
        self.assertIn("Point-in-Time Status Evidence Collection Queue", report_text)
        self.assertIn("- Backtest readiness impact: `hold`", report_text)


if __name__ == "__main__":
    unittest.main()
