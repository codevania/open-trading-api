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

from scripts.quant_point_in_time_status_evidence_collection_plan import build_evidence_collection_plan, main


LIFECYCLE_FIELDS = (
    "code",
    "market",
    "status_type",
    "lifecycle_gap_status",
    "active_like_rows",
    "release_like_rows",
    "first_active_event_date",
    "latest_active_event_date",
    "first_release_like_event_date",
    "latest_release_like_event_date",
    "market_rows",
    "market_start",
    "market_end",
    "event_sources",
    "raw_paths",
    "notes",
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
UNKNOWN_FIELDS = (
    "code",
    "status_type",
    "status_value",
    "event_date",
    "source",
    "confidence",
    "source_url",
    "current_market",
    "raw_path_count",
    "raw_capture_dates",
    "raw_paths",
    "collection_target",
    "notes",
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _lifecycle_row(code: str = "000001", status_type: str = "managed_issue") -> dict[str, str]:
    return {
        "code": code,
        "market": "KOSPI",
        "status_type": status_type,
        "lifecycle_gap_status": "missing_release_resume_evidence",
        "active_like_rows": "2",
        "release_like_rows": "0",
        "first_active_event_date": "2026-07-03",
        "latest_active_event_date": "2026-07-08",
        "first_release_like_event_date": "",
        "latest_release_like_event_date": "",
        "market_rows": "72",
        "market_start": "2025-01-02",
        "market_end": "2025-04-18",
        "event_sources": "kind",
        "raw_paths": "_report/raw/2026/2026-07-08/kind/status-source-probe/managed.xls",
        "notes": "release_resume_collection_target",
    }


def _manifest_row(status_type: str = "managed_issue", source: str = "kind") -> dict[str, str]:
    return {
        "status_type": status_type,
        "coverage_start": "2025-01-02",
        "coverage_end": "2025-04-18",
        "source": source,
        "source_url": "",
        "raw_path": "",
        "confidence": "",
        "lifecycle_target_groups": "1",
        "lifecycle_target_codes": "1",
        "market_labels": "KOSPI",
        "candidate_tables": "Managed issue event",
        "allowed_url_prefixes": "https://kind.krx.co.kr/",
        "draft_status": "pending_raw_evidence",
        "notes": "draft_only",
    }


def _unknown_row() -> dict[str, str]:
    return {
        "code": "0099X0",
        "status_type": "trading_halt",
        "status_value": "halted",
        "event_date": "2026-07-08",
        "source": "kind",
        "confidence": "medium",
        "source_url": "https://kind.krx.co.kr/example",
        "current_market": "UNKNOWN",
        "raw_path_count": "1",
        "raw_capture_dates": "2026-07-08",
        "raw_paths": "_report/raw/2026/2026-07-08/kind/status-source-probe/trading_halt.xls",
        "collection_target": "resolve_market_label",
        "notes": "unit-test fixture",
    }


class QuantPointInTimeStatusEvidenceCollectionPlanTest(unittest.TestCase):
    def test_builds_prioritized_collection_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lifecycle = root / "lifecycle.csv"
            manifest = root / "manifest.csv"
            unknown = root / "unknown.csv"
            _write_csv(lifecycle, LIFECYCLE_FIELDS, [_lifecycle_row(), _lifecycle_row("000002", "trading_halt")])
            _write_csv(manifest, MANIFEST_FIELDS, [_manifest_row(), _manifest_row("trading_halt", "kind")])
            _write_csv(unknown, UNKNOWN_FIELDS, [_unknown_row()])

            rows, summary = build_evidence_collection_plan(
                lifecycle_gaps_path=lifecycle,
                source_manifest_draft_path=manifest,
                unknown_market_targets_path=unknown,
            )

        self.assertEqual(summary["plan_rows"], 5)
        self.assertEqual(summary["blocker_counts"]["source_manifest_evidence"], 2)
        self.assertEqual(summary["blocker_counts"]["release_resume_evidence"], 2)
        self.assertEqual(summary["blocker_counts"]["market_label_resolution"], 1)
        self.assertEqual([row["priority"] for row in rows[:2]], ["1", "1"])
        self.assertTrue(all(row["order_intent_generated"] == "false" for row in rows))
        self.assertIn("pending_release_resume_evidence", {row["collection_status"] for row in rows})

    def test_missing_manifest_column_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lifecycle = root / "lifecycle.csv"
            manifest = root / "manifest.csv"
            _write_csv(lifecycle, LIFECYCLE_FIELDS, [_lifecycle_row()])
            fields = tuple(field for field in MANIFEST_FIELDS if field != "draft_status")
            row = {key: value for key, value in _manifest_row().items() if key in fields}
            _write_csv(manifest, fields, [row])

            with self.assertRaisesRegex(ValueError, "missing required columns: draft_status"):
                build_evidence_collection_plan(
                    lifecycle_gaps_path=lifecycle,
                    source_manifest_draft_path=manifest,
                )

    def test_cli_writes_lf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            lifecycle = root / "lifecycle.csv"
            manifest = root / "manifest.csv"
            output = root / "plan.rows.csv"
            report = root / "plan.md"
            _write_csv(lifecycle, LIFECYCLE_FIELDS, [_lifecycle_row()])
            _write_csv(manifest, MANIFEST_FIELDS, [_manifest_row()])

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_evidence_collection_plan.py",
                    "--lifecycle-gaps",
                    str(lifecycle),
                    "--source-manifest-draft",
                    str(manifest),
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
        self.assertIn("Point-in-Time Status Evidence Collection Plan", report_text)
        self.assertIn("- Order intent generated: `false`", report_text)


if __name__ == "__main__":
    unittest.main()
