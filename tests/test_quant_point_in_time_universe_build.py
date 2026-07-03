from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.quant_point_in_time_universe_build import build_point_in_time_universe


FIELDS = (
    "date",
    "code",
    "stock_name",
    "market",
    "listing_date",
    "security_group",
    "stock_certificate_type",
    "close",
    "volume",
    "trading_value_krw",
    "market_cap_krw",
    "pit_status_replay_status",
    "pit_status_exclude_reasons",
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _row(
    code: str,
    *,
    market: str = "KOSPI",
    security_group: str = "주권",
    stock_certificate_type: str = "보통주",
    status: str = "include_by_status_event",
    status_reasons: str = "",
) -> dict[str, str]:
    return {
        "date": "2025-01-02",
        "code": code,
        "stock_name": "TestCo",
        "market": market,
        "listing_date": "2020-01-01",
        "security_group": security_group,
        "stock_certificate_type": stock_certificate_type,
        "close": "1000",
        "volume": "10",
        "trading_value_krw": "10000",
        "market_cap_krw": "1000000",
        "pit_status_replay_status": status,
        "pit_status_exclude_reasons": status_reasons,
    }


class QuantPointInTimeUniverseBuildTest(unittest.TestCase):
    def test_builds_universe_smoke_with_status_and_instrument_exclusions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "replayed.csv"
            _write_csv(
                path,
                FIELDS,
                [
                    _row("005930"),
                    _row("005935", stock_certificate_type="구형우선주"),
                    _row("000040", security_group="부동산투자회사"),
                    _row("123456", market="KONEX"),
                    _row("269620", status="exclude_by_status_event", status_reasons="managed_issue_active"),
                ],
            )

            rows, summary = build_point_in_time_universe(path)

        by_code = {row["code"]: row for row in rows}
        self.assertEqual(by_code["005930"]["pit_universe_status"], "include")
        self.assertEqual(by_code["005935"]["pit_universe_exclude_reasons"], "stock_certificate_not_common")
        self.assertEqual(by_code["000040"]["pit_universe_exclude_reasons"], "security_group_not_plain_equity")
        self.assertEqual(by_code["123456"]["pit_universe_exclude_reasons"], "market_not_allowed")
        self.assertEqual(by_code["269620"]["pit_universe_exclude_reasons"], "status_event:managed_issue_active")
        self.assertEqual(summary["include_rows"], 1)
        self.assertEqual(summary["exclude_rows"], 4)

    def test_rejects_missing_required_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            _write_csv(path, ("date", "code"), [{"date": "2025-01-02", "code": "005930"}])

            with self.assertRaisesRegex(ValueError, "missing required columns"):
                build_point_in_time_universe(path)


if __name__ == "__main__":
    unittest.main()
