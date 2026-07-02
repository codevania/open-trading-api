from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REPLAY = REPO_ROOT / "scripts" / "quant_point_in_time_status_replay.py"


EVENT_FIELDS = (
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


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _event(event_date: str, status_type: str, status_value: str) -> dict[str, str]:
    return {
        "event_date": event_date,
        "code": "005930",
        "market": "KOSPI",
        "status_type": status_type,
        "status_value": status_value,
        "source": "manual_snapshot",
        "source_url": "",
        "raw_path": "_report/raw/2026/2026-07-03/krx/status/status.raw.csv",
        "confidence": "medium",
        "notes": "unit-test fixture",
    }


class QuantPointInTimeStatusReplayTest(unittest.TestCase):
    def test_replays_active_and_released_status_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market_data = root / "market_data.csv"
            events = root / "events.csv"
            output = root / "replayed.csv"
            report = root / "replayed.md"
            _write_csv(
                market_data,
                ("date", "code", "market", "close"),
                [
                    {"date": "2025-01-07", "code": "005930", "market": "KOSPI", "close": "100"},
                    {"date": "2025-01-08", "code": "005930", "market": "KOSPI", "close": "101"},
                    {"date": "2025-01-09", "code": "005930", "market": "KOSPI", "close": "102"},
                    {"date": "2025-01-08", "code": "000660", "market": "KOSPI", "close": "200"},
                ],
            )
            _write_csv(
                events,
                EVENT_FIELDS,
                [
                    _event("2025-01-08", "managed_issue", "designated"),
                    _event("2025-01-09", "managed_issue", "released"),
                ],
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(REPLAY),
                    "--market-data",
                    str(market_data),
                    "--events",
                    str(events),
                    "--output",
                    str(output),
                    "--report-output",
                    str(report),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            with output.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["pit_status_replay_status"], "include_by_status_event")
            self.assertEqual(rows[1]["pit_status_replay_status"], "exclude_by_status_event")
            self.assertEqual(rows[1]["pit_status_exclude_reasons"], "managed_issue_active")
            self.assertEqual(rows[2]["pit_status_replay_status"], "include_by_status_event")
            self.assertEqual(rows[3]["pit_applied_event_count"], "0")
            self.assertIn("Exclude rows by event state | 1", report.read_text(encoding="utf-8"))

    def test_rejects_invalid_status_events_before_replay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market_data = root / "market_data.csv"
            events = root / "events.csv"
            _write_csv(market_data, ("date", "code"), [{"date": "2025-01-08", "code": "005930"}])
            bad_event = _event("20250108", "managed_issue", "designated")
            _write_csv(events, EVENT_FIELDS, [bad_event])

            result = subprocess.run(
                [
                    sys.executable,
                    str(REPLAY),
                    "--market-data",
                    str(market_data),
                    "--events",
                    str(events),
                    "--output",
                    str(root / "out.csv"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("status events failed validation", result.stderr)

    def test_rejects_market_data_without_date_code_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            market_data = root / "market_data.csv"
            events = root / "events.csv"
            _write_csv(market_data, ("as_of_date", "symbol"), [{"as_of_date": "2025-01-08", "symbol": "005930"}])
            _write_csv(events, EVENT_FIELDS, [_event("2025-01-08", "managed_issue", "designated")])

            result = subprocess.run(
                [
                    sys.executable,
                    str(REPLAY),
                    "--market-data",
                    str(market_data),
                    "--events",
                    str(events),
                    "--output",
                    str(root / "out.csv"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("market-data CSV missing date column", result.stderr)


if __name__ == "__main__":
    unittest.main()
