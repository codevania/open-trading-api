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

from scripts.quant_point_in_time_status_coverage_audit import audit_status_coverage, main


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _market_rows() -> list[dict[str, str]]:
    return [
        {"date": "2025-01-02", "code": "005930", "close": "100"},
        {"date": "2025-01-02", "code": "000660", "close": "200"},
        {"date": "2025-01-03", "code": "005930", "close": "101"},
        {"date": "2025-01-03", "code": "000660", "close": "201"},
    ]


def _event(
    *,
    event_date: str,
    code: str = "005930",
    status_type: str = "managed_issue",
    status_value: str = "designated",
) -> dict[str, str]:
    return {
        "event_date": event_date,
        "code": code,
        "market": "KOSPI",
        "status_type": status_type,
        "status_value": status_value,
        "source": "kind",
        "source_url": "https://kind.krx.co.kr/example",
        "raw_path": "_report/raw/2026/2026-07-03/kind/status-source-probe/managed_issue.xls",
        "confidence": "high",
        "notes": "unit-test fixture",
    }


def _replayed_rows() -> list[dict[str, str]]:
    return [
        {
            "date": "2025-01-02",
            "code": "005930",
            "pit_applied_event_count": "1",
            "pit_status_replay_status": "exclude_by_status_event",
        },
        {
            "date": "2025-01-02",
            "code": "000660",
            "pit_applied_event_count": "0",
            "pit_status_replay_status": "include_by_status_event",
        },
        {
            "date": "2025-01-03",
            "code": "005930",
            "pit_applied_event_count": "2",
            "pit_status_replay_status": "include_by_status_event",
        },
        {
            "date": "2025-01-03",
            "code": "000660",
            "pit_applied_event_count": "0",
            "pit_status_replay_status": "include_by_status_event",
        },
    ]


class QuantPointInTimeStatusCoverageAuditTest(unittest.TestCase):
    def test_current_snapshot_smoke_stays_hold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market = root / "market.csv"
            events = root / "events.csv"
            replayed = root / "replayed.csv"
            _write_csv(market, _market_rows())
            _write_csv(events, [_event(event_date="2025-01-01")])
            _write_csv(replayed, _replayed_rows())

            rows, summary = audit_status_coverage(
                market_data_path=market,
                events_path=events,
                replayed_market_data_path=replayed,
                coverage_mode="current_snapshot_smoke",
                required_status_types=("managed_issue",),
            )

        self.assertEqual(summary["coverage_status"], "hold")
        self.assertEqual(summary["market_rows"], 4)
        self.assertEqual(summary["replay_match_rows"], 4)
        self.assertEqual(summary["rows_with_applied_status_event"], 2)
        self.assertEqual(summary["rows_excluded_by_status_event"], 1)
        self.assertEqual(summary["raw_capture_dates"], ["2026-07-03"])
        self.assertEqual(summary["lifecycle_status_types_without_release"], ["managed_issue"])
        self.assertIn("mode_not_historical_complete", rows[0]["coverage_notes"])
        self.assertIn("no_release_like_events", rows[0]["coverage_notes"])
        self.assertIn("missing_lifecycle_release_events", rows[0]["coverage_notes"])

    def test_historical_complete_can_pass_when_release_events_and_replay_are_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market = root / "market.csv"
            events = root / "events.csv"
            replayed = root / "replayed.csv"
            _write_csv(market, _market_rows())
            _write_csv(
                events,
                [
                    _event(event_date="2025-01-01", status_value="designated"),
                    _event(event_date="2025-01-03", status_value="released"),
                ],
            )
            _write_csv(replayed, _replayed_rows())

            rows, summary = audit_status_coverage(
                market_data_path=market,
                events_path=events,
                replayed_market_data_path=replayed,
                coverage_mode="historical_complete",
                required_status_types=("managed_issue",),
            )

        self.assertEqual(summary["coverage_status"], "pass")
        self.assertEqual(summary["release_like_event_rows"], 1)
        self.assertEqual(summary["lifecycle_status_types_without_release"], [])
        self.assertTrue(all(row["coverage_status"] == "pass" for row in rows))

    def test_cli_writes_lf_report_and_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market = root / "market.csv"
            events = root / "events.csv"
            replayed = root / "replayed.csv"
            output = root / "coverage.rows.csv"
            report = root / "coverage.md"
            _write_csv(market, _market_rows())
            _write_csv(events, [_event(event_date="2025-01-01")])
            _write_csv(replayed, _replayed_rows())

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_coverage_audit.py",
                    "--market-data",
                    str(market),
                    "--events",
                    str(events),
                    "--replayed-market-data",
                    str(replayed),
                    "--required-status-types",
                    "managed_issue",
                    "--output",
                    str(output),
                    "--report-output",
                    str(report),
                ],
            ):
                self.assertEqual(main(), 0)

            report_text = report.read_text(encoding="utf-8")
            report_bytes = report.read_bytes()
            output_bytes = output.read_bytes()

        self.assertIn("- Coverage status: `hold`", report_text)
        self.assertIn("| Rows with applied status event | 2 |", report_text)
        self.assertIn("| Raw status capture dates | 1 |", report_text)
        self.assertIn("| `managed_issue` | 1 | 0 |", report_text)
        self.assertIn("status types with active-like events but no release/resume rows", report_text)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertNotIn(b"\r\n", output_bytes)


if __name__ == "__main__":
    unittest.main()
