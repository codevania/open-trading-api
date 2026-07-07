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

from scripts.quant_point_in_time_status_events_merge import merge_status_event_files, main


FIELDS = (
    "event_date",
    "code",
    "market",
    "status_type",
    "status_value",
    "source",
    "source_url",
    "raw_path",
    "confidence",
    "notes",
)


def _write_events(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _event(*, raw_path: str, market: str = "UNKNOWN", notes: str = "fixture") -> dict[str, str]:
    return {
        "event_date": "2025-01-02",
        "code": "005930",
        "market": market,
        "status_type": "managed_issue",
        "status_value": "designated",
        "source": "kind",
        "source_url": "https://kind.krx.co.kr/investwarn/adminissue.do?method=searchAdminIssueList",
        "raw_path": raw_path,
        "confidence": "high",
        "notes": notes,
    }


class QuantPointInTimeStatusEventsMergeTest(unittest.TestCase):
    def test_merges_duplicate_logical_events_and_preserves_raw_capture_dates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first.csv"
            second = root / "second.csv"
            _write_events(
                first,
                [_event(raw_path="_report/raw/2026/2026-07-03/kind/status-source-probe/managed_issue.xls")],
            )
            _write_events(
                second,
                [
                    _event(
                        raw_path="_report/raw/2026/2026-07-08/kind/status-source-probe/managed_issue.xls",
                        market="KOSPI",
                        notes="second fixture",
                    )
                ],
            )

            rows, summary = merge_status_event_files([first, second])

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["market"], "KOSPI")
        self.assertIn("2026-07-03", rows[0]["notes"])
        self.assertIn("2026-07-08", rows[0]["notes"])
        self.assertIn("_report/raw/2026/2026-07-03", rows[0]["raw_path"])
        self.assertIn("_report/raw/2026/2026-07-08", rows[0]["raw_path"])
        self.assertEqual(summary["input_rows"], 2)
        self.assertEqual(summary["output_rows"], 1)
        self.assertEqual(summary["merged_duplicate_rows"], 1)
        self.assertEqual(summary["raw_capture_dates"], ["2026-07-03", "2026-07-08"])

    def test_cli_writes_lf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first.csv"
            second = root / "second.csv"
            output = root / "merged.csv"
            report = root / "merge.md"
            _write_events(
                first,
                [_event(raw_path="_report/raw/2026/2026-07-03/kind/status-source-probe/managed_issue.xls")],
            )
            _write_events(
                second,
                [_event(raw_path="_report/raw/2026/2026-07-08/kind/status-source-probe/managed_issue.xls")],
            )

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_events_merge.py",
                    "--events",
                    str(first),
                    "--events",
                    str(second),
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
        self.assertIn("| Raw capture dates | 2 |", report_text)


if __name__ == "__main__":
    unittest.main()
