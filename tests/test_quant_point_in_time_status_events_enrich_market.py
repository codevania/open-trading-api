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

from scripts.quant_point_in_time_status_events_enrich_market import enrich_event_markets


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


def _event(code: str, market: str = "UNKNOWN") -> dict[str, str]:
    return {
        "event_date": "2026-07-03",
        "code": code,
        "market": market,
        "status_type": "managed_issue",
        "status_value": "designated",
        "source": "kind",
        "source_url": "https://kind.krx.co.kr/investwarn/adminissue.do?method=searchAdminIssueList",
        "raw_path": "_report/raw/2026/2026-07-03/kind/status-source-probe/managed_issue.xls",
        "confidence": "high",
        "notes": "unit-test fixture",
    }


class QuantPointInTimeStatusEventsEnrichMarketTest(unittest.TestCase):
    def test_resolves_unknown_market_from_market_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            market_data = root / "market_data.csv"
            _write_csv(events, EVENT_FIELDS, [_event("005930")])
            _write_csv(market_data, ("date", "code", "market"), [{"date": "2025-01-02", "code": "005930", "market": "KOSPI"}])

            _fields, rows, summary = enrich_event_markets(events, market_data)

        self.assertEqual(rows[0]["market"], "KOSPI")
        self.assertIn("market_enrichment=market_data_join:KOSPI", rows[0]["notes"])
        self.assertEqual(summary["resolved_unknown_market"], 1)

    def test_unmapped_code_stays_unknown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            market_data = root / "market_data.csv"
            _write_csv(events, EVENT_FIELDS, [_event("123456")])
            _write_csv(market_data, ("date", "code", "market"), [{"date": "2025-01-02", "code": "005930", "market": "KOSPI"}])

            _fields, rows, summary = enrich_event_markets(events, market_data)

        self.assertEqual(rows[0]["market"], "UNKNOWN")
        self.assertEqual(summary["unresolved_no_market_mapping"], 1)

    def test_ambiguous_mapping_keeps_unknown_with_note(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            market_data = root / "market_data.csv"
            _write_csv(events, EVENT_FIELDS, [_event("123456")])
            _write_csv(
                market_data,
                ("date", "code", "market"),
                [
                    {"date": "2025-01-02", "code": "123456", "market": "KOSPI"},
                    {"date": "2025-01-03", "code": "123456", "market": "KOSDAQ"},
                ],
            )

            _fields, rows, summary = enrich_event_markets(events, market_data)

        self.assertEqual(rows[0]["market"], "UNKNOWN")
        self.assertIn("market_enrichment=ambiguous_market_mapping:KOSDAQ/KOSPI", rows[0]["notes"])
        self.assertEqual(summary["ambiguous_market_mapping"], 1)

    def test_known_market_is_retained_on_mapping_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            market_data = root / "market_data.csv"
            _write_csv(events, EVENT_FIELDS, [_event("005930", "KOSDAQ")])
            _write_csv(market_data, ("date", "code", "market"), [{"date": "2025-01-02", "code": "005930", "market": "KOSPI"}])

            _fields, rows, summary = enrich_event_markets(events, market_data)

        self.assertEqual(rows[0]["market"], "KOSDAQ")
        self.assertIn("market_enrichment=retained_source_market_conflict:KOSPI", rows[0]["notes"])
        self.assertEqual(summary["retained_source_market_conflict"], 1)


if __name__ == "__main__":
    unittest.main()
