from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE = REPO_ROOT / "scripts" / "quant_point_in_time_status_events_validate.py"


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


def _write_events(path: Path, rows: list[dict[str, str]], fields: tuple[str, ...] = FIELDS) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


class QuantPointInTimeStatusEventsValidateTest(unittest.TestCase):
    def test_accepts_valid_status_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            rows_output = root / "rows.csv"
            report = root / "report.md"
            _write_events(
                events,
                [
                    {
                        "event_date": "2025-01-08",
                        "code": "005930",
                        "market": "KOSPI",
                        "status_type": "managed_issue",
                        "status_value": "designated",
                        "source": "krx_data_marketplace",
                        "source_url": "https://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd",
                        "raw_path": "_report/raw/2026/2026-07-03/krx/status/managed.raw.csv",
                        "confidence": "high",
                        "notes": "unit-test fixture",
                    },
                    {
                        "event_date": "2025-01-09",
                        "code": "005930",
                        "market": "KOSPI",
                        "status_type": "managed_issue",
                        "status_value": "released",
                        "source": "manual_snapshot",
                        "source_url": "",
                        "raw_path": "_report/raw/2026/2026-07-03/krx/status/managed.raw.csv",
                        "confidence": "medium",
                        "notes": "manual source-url can be blank until raw manifest is available",
                    },
                ],
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATE),
                    "--events",
                    str(events),
                    "--rows-output",
                    str(rows_output),
                    "--report-output",
                    str(report),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            with rows_output.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["valid"], "true")
            self.assertEqual(rows[1]["valid"], "true")
            report_text = report.read_text(encoding="utf-8")
            self.assertIn("Valid rows | 2", report_text)
            self.assertIn("Backtest readiness: `hold`", report_text)

    def test_rejects_invalid_values_and_duplicate_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / "events.csv"
            rows_output = root / "rows.csv"
            duplicate = {
                "event_date": "20250108",
                "code": "005930",
                "market": "KOSPI",
                "status_type": "trading_halt",
                "status_value": "resumed",
                "source": "kind",
                "source_url": "https://data.krx.co.kr/not-kind",
                "raw_path": "raw/status.raw.csv",
                "confidence": "certain",
                "notes": "bad fixture",
            }
            _write_events(events, [duplicate, duplicate.copy()])

            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATE),
                    "--events",
                    str(events),
                    "--rows-output",
                    str(rows_output),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            with rows_output.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            errors = rows[0]["errors"]
            self.assertIn("event_date must be YYYY-MM-DD", errors)
            self.assertIn("status_value resumed is not valid for status_type trading_halt", errors)
            self.assertIn("source_url does not match source policy for kind", errors)
            self.assertIn("raw_path must be under _report/raw/", errors)
            self.assertIn("confidence has unsupported value: certain", errors)
            self.assertIn("duplicate event key", errors)

    def test_rejects_missing_required_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events.csv"
            rows_output = Path(tmp) / "rows.csv"
            _write_events(
                events,
                [{"event_date": "2025-01-08", "code": "005930"}],
                fields=("event_date", "code"),
            )

            result = subprocess.run(
                [sys.executable, str(VALIDATE), "--events", str(events), "--rows-output", str(rows_output)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            with rows_output.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(rows[0]["row_number"], "0")
            self.assertIn("missing required columns", rows[0]["errors"])


if __name__ == "__main__":
    unittest.main()
