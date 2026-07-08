from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.quant_point_in_time_status_unknown_market_report import build_unknown_market_rows


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
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _event(code: str, market: str) -> dict[str, str]:
    return {
        "event_date": "2026-07-08",
        "code": code,
        "market": market,
        "status_type": "trading_halt",
        "status_value": "halted",
        "source": "kind",
        "source_url": "https://kind.krx.co.kr/investwarn/haltissue.do?method=searchHaltIssueMain",
        "raw_path": (
            "_report/raw/2026/2026-07-03/kind/status-source-probe/trading_halt.xls;"
            "_report/raw/2026/2026-07-08/kind/status-source-probe/trading_halt.xls"
        ),
        "confidence": "high",
        "notes": "unit-test fixture",
    }


class QuantPointInTimeStatusUnknownMarketReportTest(unittest.TestCase):
    def test_extracts_unknown_market_rows_as_collection_targets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            _write_csv(
                events,
                EVENT_FIELDS,
                [
                    _event("000001", "UNKNOWN"),
                    _event("000002", ""),
                    _event("005930", "KOSPI"),
                ],
            )

            rows, summary = build_unknown_market_rows(events)

        self.assertEqual([row["code"] for row in rows], ["000001", "000002"])
        self.assertEqual(rows[0]["collection_target"], "resolve_market_label")
        self.assertEqual(rows[0]["raw_path_count"], "2")
        self.assertEqual(rows[0]["raw_capture_dates"], "2026-07-03;2026-07-08")
        self.assertEqual(summary["unknown_market_rows"], 2)
        self.assertEqual(summary["unknown_market_codes"], 2)
        self.assertEqual(summary["status_type_counts"], {"trading_halt": 2})
        self.assertEqual(summary["raw_capture_dates"], ["2026-07-03", "2026-07-08"])

    def test_missing_required_column_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            _write_csv(events, tuple(field for field in EVENT_FIELDS if field != "market"), [])

            with self.assertRaisesRegex(ValueError, "has no rows"):
                build_unknown_market_rows(events)

    def test_missing_required_column_with_rows_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            fields = tuple(field for field in EVENT_FIELDS if field != "market")
            row = {key: value for key, value in _event("000001", "UNKNOWN").items() if key in fields}
            _write_csv(events, fields, [row])

            with self.assertRaisesRegex(ValueError, "missing required columns: market"):
                build_unknown_market_rows(events)


if __name__ == "__main__":
    unittest.main()
