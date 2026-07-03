from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.quant_kind_status_events_extract import (
    extract_events_from_snapshot,
    extract_kind_status_events,
    parse_html_table,
)


def _write_html_table(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    body = ["<html><body><table><tr>"]
    for header in headers:
        body.append(f"<th>{header}</th>")
    body.append("</tr>")
    for row in rows:
        body.append("<tr>")
        for value in row:
            body.append(f"<td>{value}</td>")
        body.append("</tr>")
    body.append("</table></body></html>")
    path.write_bytes("".join(body).encode("euc-kr"))


class QuantKindStatusEventsExtractTest(unittest.TestCase):
    def test_parse_html_table_reads_euc_kr_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "managed_issue.xls"
            _write_html_table(
                path,
                ["\uc885\ubaa9\uba85", "\uc885\ubaa9\ucf54\ub4dc", "\uc9c0\uc815\uc77c"],
                [["ABC", "005930", "2026-07-03"]],
            )

            rows = parse_html_table(path)

        self.assertEqual(rows, [{"\uc885\ubaa9\uba85": "ABC", "\uc885\ubaa9\ucf54\ub4dc": "005930", "\uc9c0\uc815\uc77c": "2026-07-03"}])

    def test_extract_managed_issue_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_dir = Path(tmp)
            raw_path = raw_dir / "managed_issue.xls"
            _write_html_table(
                raw_path,
                ["\uc885\ubaa9\uba85", "\uc885\ubaa9\ucf54\ub4dc", "\uc9c0\uc815\uc77c", "\uc9c0\uc815\uc0ac\uc720"],
                [["TestCo", "5930", "2026-07-03", "reason"]],
            )

            rows, summary = extract_kind_status_events(raw_dir, "2026-07-03")

        self.assertEqual(summary["by_snapshot"]["managed_issue"], 1)
        managed = [row for row in rows if row["status_type"] == "managed_issue"]
        self.assertEqual(len(managed), 1)
        self.assertEqual(managed[0]["code"], "005930")
        self.assertEqual(managed[0]["status_value"], "designated")
        self.assertEqual(managed[0]["source"], "kind")

    def test_trading_halt_uses_capture_date_when_source_has_no_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_path = Path(tmp) / "trading_halt.xls"
            _write_html_table(
                raw_path,
                ["\ubc88\ud638", "\uc885\ubaa9\uba85", "\uc885\ubaa9\ucf54\ub4dc", "\uc0ac\uc720"],
                [["1", "HaltCo", "123450", "halt reason"]],
            )
            from scripts.quant_kind_status_events_extract import DEFAULT_SPECS

            spec = next(item for item in DEFAULT_SPECS if item.slug == "trading_halt")
            events = extract_events_from_snapshot(spec, raw_path, "2026-07-03")

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_date"], "2026-07-03")
        self.assertEqual(events[0]["confidence"], "medium")
        self.assertEqual(events[0]["status_value"], "halted")

    def test_market_alert_release_rows_are_added_when_release_date_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_path = Path(tmp) / "market_alert_warning.xls"
            _write_html_table(
                raw_path,
                [
                    "\ubc88\ud638",
                    "\uc885\ubaa9\uba85",
                    "\uc885\ubaa9\ucf54\ub4dc",
                    "\uacf5\uc2dc\uc77c",
                    "\uc9c0\uc815\uc77c",
                    "\ud574\uc81c\uc77c",
                ],
                [["1", "WarnCo", "777770", "2026-07-01", "2026-07-02", "2026-07-03"]],
            )
            from scripts.quant_kind_status_events_extract import DEFAULT_SPECS

            spec = next(item for item in DEFAULT_SPECS if item.slug == "market_alert_warning")
            events = extract_events_from_snapshot(spec, raw_path, "2026-07-03")

        self.assertEqual([row["status_value"] for row in events], ["warning", "released"])
        self.assertEqual(events[1]["event_date"], "2026-07-03")

    def test_duplicate_schema_keys_are_merged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_dir = Path(tmp)
            raw_path = raw_dir / "market_alert_caution.xls"
            _write_html_table(
                raw_path,
                [
                    "\ubc88\ud638",
                    "\uc885\ubaa9\uba85",
                    "\uc885\ubaa9\ucf54\ub4dc",
                    "\uc720\ud615",
                    "\uacf5\uc2dc\uc77c",
                    "\uc9c0\uc815\uc77c",
                ],
                [
                    ["1", "CautionCo", "044480", "type-a", "2026-07-02", "2026-07-03"],
                    ["2", "CautionCo", "044480", "type-b", "2026-07-02", "2026-07-03"],
                ],
            )

            rows, summary = extract_kind_status_events(raw_dir, "2026-07-03")

        caution = [row for row in rows if row["status_type"] == "market_alert"]
        self.assertEqual(len(caution), 1)
        self.assertEqual(summary["deduped_rows"], 1)
        self.assertIn("duplicate_source_row", caution[0]["notes"])


if __name__ == "__main__":
    unittest.main()
