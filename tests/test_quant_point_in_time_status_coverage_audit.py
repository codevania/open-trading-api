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


def _source_manifest_row(
    *,
    status_type: str = "managed_issue",
    coverage_start: str = "2025-01-02",
    coverage_end: str = "2025-01-03",
) -> dict[str, str]:
    return {
        "status_type": status_type,
        "coverage_start": coverage_start,
        "coverage_end": coverage_end,
        "source": "kind",
        "source_url": "https://kind.krx.co.kr/example",
        "raw_path": f"_report/raw/2026/2026-07-03/kind/status-source-probe/{status_type}.xls",
        "confidence": "high",
        "notes": "unit-test fixture",
    }


def _write_source_raw(root: Path, status_type: str = "managed_issue") -> None:
    raw = root / "_report" / "raw" / "2026" / "2026-07-03" / "kind" / "status-source-probe" / f"{status_type}.xls"
    raw.parent.mkdir(parents=True, exist_ok=True)
    raw.write_text("fixture\n", encoding="utf-8")


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

    def test_counts_multiple_raw_capture_dates_in_merged_raw_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market = root / "market.csv"
            events = root / "events.csv"
            replayed = root / "replayed.csv"
            merged_event = _event(event_date="2025-01-01")
            merged_event["raw_path"] = (
                "_report/raw/2026/2026-07-03/kind/status-source-probe/managed_issue.xls;"
                "_report/raw/2026/2026-07-08/kind/status-source-probe/managed_issue.xls"
            )
            _write_csv(market, _market_rows())
            _write_csv(events, [merged_event])
            _write_csv(replayed, _replayed_rows())

            _rows, summary = audit_status_coverage(
                market_data_path=market,
                events_path=events,
                replayed_market_data_path=replayed,
                coverage_mode="current_snapshot_smoke",
                required_status_types=("managed_issue",),
            )

        self.assertEqual(summary["raw_capture_dates"], ["2026-07-03", "2026-07-08"])

    def test_historical_complete_can_pass_when_release_events_and_replay_are_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market = root / "market.csv"
            events = root / "events.csv"
            replayed = root / "replayed.csv"
            manifest = root / "source_manifest.csv"
            _write_csv(market, _market_rows())
            _write_csv(
                events,
                [
                    _event(event_date="2025-01-01", status_value="designated"),
                    _event(event_date="2025-01-03", status_value="released"),
                ],
            )
            _write_csv(replayed, _replayed_rows())
            _write_source_raw(root)
            _write_csv(manifest, [_source_manifest_row()])

            rows, summary = audit_status_coverage(
                market_data_path=market,
                events_path=events,
                replayed_market_data_path=replayed,
                source_coverage_manifest_path=manifest,
                repo_root=root,
                coverage_mode="historical_complete",
                required_status_types=("managed_issue",),
            )

        self.assertEqual(summary["coverage_status"], "pass")
        self.assertEqual(summary["release_like_event_rows"], 1)
        self.assertEqual(summary["lifecycle_status_types_without_release"], [])
        self.assertEqual(summary["source_coverage_manifest_row_failures"], 0)
        self.assertEqual(summary["source_coverage_manifest_missing_status_types"], [])
        self.assertTrue(all(row["coverage_status"] == "pass" for row in rows))

    def test_historical_complete_holds_when_source_manifest_raw_path_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market = root / "market.csv"
            events = root / "events.csv"
            replayed = root / "replayed.csv"
            manifest = root / "source_manifest.csv"
            _write_csv(market, _market_rows())
            _write_csv(
                events,
                [
                    _event(event_date="2025-01-01", status_value="designated"),
                    _event(event_date="2025-01-03", status_value="released"),
                ],
            )
            _write_csv(replayed, _replayed_rows())
            _write_csv(manifest, [_source_manifest_row()])

            rows, summary = audit_status_coverage(
                market_data_path=market,
                events_path=events,
                replayed_market_data_path=replayed,
                source_coverage_manifest_path=manifest,
                repo_root=root,
                coverage_mode="historical_complete",
                required_status_types=("managed_issue",),
            )

        self.assertEqual(summary["coverage_status"], "hold")
        self.assertEqual(summary["source_coverage_manifest_row_failures"], 1)
        self.assertEqual(summary["source_coverage_manifest_validation_status"], "fail")
        self.assertIn("source_coverage_manifest_row_failures", rows[0]["coverage_notes"])

    def test_historical_complete_holds_without_source_coverage_manifest(self) -> None:
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

        self.assertEqual(summary["coverage_status"], "hold")
        self.assertEqual(summary["source_coverage_manifest_missing_status_types"], ["managed_issue"])
        self.assertTrue(all(row["coverage_status"] == "hold" for row in rows))
        self.assertIn("source_coverage_manifest_not_supplied", rows[0]["coverage_notes"])

    def test_historical_complete_holds_when_source_manifest_misses_market_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market = root / "market.csv"
            events = root / "events.csv"
            replayed = root / "replayed.csv"
            manifest = root / "source_manifest.csv"
            _write_csv(market, _market_rows())
            _write_csv(
                events,
                [
                    _event(event_date="2025-01-01", status_value="designated"),
                    _event(event_date="2025-01-03", status_value="released"),
                ],
            )
            _write_csv(replayed, _replayed_rows())
            _write_source_raw(root)
            _write_csv(manifest, [_source_manifest_row(coverage_start="2025-01-03", coverage_end="2025-01-03")])

            rows, summary = audit_status_coverage(
                market_data_path=market,
                events_path=events,
                replayed_market_data_path=replayed,
                source_coverage_manifest_path=manifest,
                repo_root=root,
                coverage_mode="historical_complete",
                required_status_types=("managed_issue",),
            )

        self.assertEqual(summary["coverage_status"], "hold")
        self.assertEqual(summary["source_coverage_manifest_missing_status_types"], ["managed_issue"])
        self.assertIn("source_coverage_manifest_missing_status_types", rows[0]["coverage_notes"])

    def test_historical_complete_holds_when_any_lifecycle_type_lacks_release(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market = root / "market.csv"
            events = root / "events.csv"
            replayed = root / "replayed.csv"
            manifest = root / "source_manifest.csv"
            _write_csv(market, _market_rows())
            _write_csv(
                events,
                [
                    _event(event_date="2025-01-01", status_type="managed_issue", status_value="designated"),
                    _event(event_date="2025-01-03", status_type="managed_issue", status_value="released"),
                    _event(event_date="2025-01-01", status_type="trading_halt", status_value="halted"),
                ],
            )
            _write_csv(replayed, _replayed_rows())
            _write_source_raw(root, "managed_issue")
            _write_source_raw(root, "trading_halt")
            _write_csv(
                manifest,
                [
                    _source_manifest_row(status_type="managed_issue"),
                    _source_manifest_row(status_type="trading_halt"),
                ],
            )

            rows, summary = audit_status_coverage(
                market_data_path=market,
                events_path=events,
                replayed_market_data_path=replayed,
                source_coverage_manifest_path=manifest,
                repo_root=root,
                coverage_mode="historical_complete",
                required_status_types=("managed_issue", "trading_halt"),
            )

        self.assertEqual(summary["coverage_status"], "hold")
        self.assertEqual(summary["release_like_event_rows"], 1)
        self.assertEqual(summary["lifecycle_status_types_without_release"], ["trading_halt"])
        self.assertTrue(all(row["coverage_status"] == "hold" for row in rows))
        self.assertIn("missing_lifecycle_release_events", rows[0]["coverage_notes"])

    def test_historical_complete_holds_without_raw_capture_dates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market = root / "market.csv"
            events = root / "events.csv"
            replayed = root / "replayed.csv"
            manifest = root / "source_manifest.csv"
            designated = _event(event_date="2025-01-01", status_value="designated")
            released = _event(event_date="2025-01-03", status_value="released")
            designated["raw_path"] = "_report/raw/kind/status-source-probe/managed_issue.xls"
            released["raw_path"] = "_report/raw/kind/status-source-probe/managed_issue.xls"
            _write_csv(market, _market_rows())
            _write_csv(events, [designated, released])
            _write_csv(replayed, _replayed_rows())
            _write_source_raw(root)
            _write_csv(manifest, [_source_manifest_row()])

            rows, summary = audit_status_coverage(
                market_data_path=market,
                events_path=events,
                replayed_market_data_path=replayed,
                source_coverage_manifest_path=manifest,
                repo_root=root,
                coverage_mode="historical_complete",
                required_status_types=("managed_issue",),
            )

        self.assertEqual(summary["coverage_status"], "hold")
        self.assertEqual(summary["raw_capture_dates"], [])
        self.assertTrue(all(row["coverage_status"] == "hold" for row in rows))
        self.assertIn("raw_capture_date_unknown", rows[0]["coverage_notes"])

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
