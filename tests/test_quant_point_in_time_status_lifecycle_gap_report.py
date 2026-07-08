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

from scripts.quant_point_in_time_status_lifecycle_gap_report import build_lifecycle_gap_rows, main


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [{key: value or "" for key, value in row.items()} for row in csv.DictReader(handle)]


def _event(
    *,
    event_date: str,
    code: str = "005930",
    market: str = "KOSPI",
    status_type: str = "managed_issue",
    status_value: str = "designated",
) -> dict[str, str]:
    return {
        "event_date": event_date,
        "code": code,
        "market": market,
        "status_type": status_type,
        "status_value": status_value,
        "source": "kind",
        "source_url": "https://kind.krx.co.kr/example",
        "raw_path": f"_report/raw/2026/2026-07-03/kind/status-source-probe/{status_type}.xls",
        "confidence": "high",
        "notes": "unit-test fixture",
    }


def _market_rows() -> list[dict[str, str]]:
    return [
        {"date": "2025-01-02", "code": "005930", "market": "KOSPI", "close": "100"},
        {"date": "2025-01-03", "code": "005930", "market": "KOSPI", "close": "101"},
        {"date": "2025-01-02", "code": "000660", "market": "KOSPI", "close": "200"},
        {"date": "2025-01-03", "code": "000660", "market": "KOSPI", "close": "201"},
    ]


class QuantPointInTimeStatusLifecycleGapReportTest(unittest.TestCase):
    def test_reports_missing_release_resume_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            market = root / "market.csv"
            _write_csv(
                events,
                [
                    _event(event_date="2025-01-01", code="005930", status_type="managed_issue"),
                    _event(
                        event_date="2025-01-01",
                        code="000660",
                        status_type="trading_halt",
                        status_value="halted",
                    ),
                ],
            )
            _write_csv(market, _market_rows())

            rows, summary = build_lifecycle_gap_rows(events_path=events, market_data_path=market)

        self.assertEqual(summary["lifecycle_groups"], 2)
        self.assertEqual(summary["gap_status_counts"], {"missing_release_resume_evidence": 2})
        self.assertEqual({row["lifecycle_gap_status"] for row in rows}, {"missing_release_resume_evidence"})
        self.assertEqual({row["market_rows"] for row in rows}, {"2"})

    def test_maps_trading_resume_to_trading_halt_release_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            _write_csv(
                events,
                [
                    _event(
                        event_date="2025-01-01",
                        code="005930",
                        status_type="trading_halt",
                        status_value="halted",
                    ),
                    _event(
                        event_date="2025-01-02",
                        code="005930",
                        status_type="trading_resume",
                        status_value="resumed",
                    ),
                ],
            )

            rows, summary = build_lifecycle_gap_rows(events_path=events)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status_type"], "trading_halt")
        self.assertEqual(rows[0]["lifecycle_gap_status"], "has_release_resume_evidence")
        self.assertEqual(rows[0]["release_like_rows"], "1")
        self.assertIn("trading_resume_mapped_to_trading_halt_release", rows[0]["notes"])
        self.assertEqual(summary["gap_status_counts"], {"has_release_resume_evidence": 1})

    def test_reports_active_after_latest_release(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            _write_csv(
                events,
                [
                    _event(event_date="2025-01-01", status_type="managed_issue", status_value="designated"),
                    _event(event_date="2025-01-02", status_type="managed_issue", status_value="released"),
                    _event(event_date="2025-01-03", status_type="managed_issue", status_value="designated"),
                ],
            )

            rows, summary = build_lifecycle_gap_rows(events_path=events)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["lifecycle_gap_status"], "active_after_latest_release")
        self.assertEqual(rows[0]["active_like_rows"], "2")
        self.assertEqual(rows[0]["release_like_rows"], "1")
        self.assertEqual(summary["gap_status_counts"], {"active_after_latest_release": 1})

    def test_cli_writes_lf_csv_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            market = root / "market.csv"
            output = root / "rows.csv"
            report = root / "report.md"
            _write_csv(events, [_event(event_date="2025-01-01")])
            _write_csv(market, _market_rows())

            with patch.object(
                sys,
                "argv",
                [
                    "quant_point_in_time_status_lifecycle_gap_report.py",
                    "--events",
                    str(events),
                    "--market-data",
                    str(market),
                    "--output",
                    str(output),
                    "--report-output",
                    str(report),
                ],
            ):
                result = main()

            rows = _read_csv(output)
            output_bytes = output.read_bytes()
            report_bytes = report.read_bytes()
            report_text = report.read_text(encoding="utf-8")

        self.assertEqual(result, 0)
        self.assertEqual(rows[0]["lifecycle_gap_status"], "missing_release_resume_evidence")
        self.assertNotIn(b"\r\n", output_bytes)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertIn("Point-in-Time Status Lifecycle Gap Report", report_text)


if __name__ == "__main__":
    unittest.main()
