from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT = REPO_ROOT / "scripts" / "quant_calendar_audit.py"


class QuantCalendarAuditTest(unittest.TestCase):
    def test_symbol_union_mode_reports_reference_only_for_consistent_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw"
            raw_dir.mkdir()
            (raw_dir / "000001.daily.raw.json").write_text(
                textwrap.dedent(
                    """
                    [
                      {"stck_bsop_date": "20260610"},
                      {"stck_bsop_date": "20260611"}
                    ]
                    """
                ).strip(),
                encoding="utf-8",
            )
            (raw_dir / "000002.daily.raw.json").write_text(
                textwrap.dedent(
                    """
                    [
                      {"stck_bsop_date": "20260610"},
                      {"stck_bsop_date": "20260611"}
                    ]
                    """
                ).strip(),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(AUDIT), "--raw-dir", str(raw_dir)],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Overall status: `reference-only`", result.stdout)
            self.assertIn("| `000001` | pass | 2 | 2 | 20260610 | 20260611 |  |  |  |", result.stdout)

    def test_external_calendar_flags_missing_dates_as_hold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw"
            raw_dir.mkdir()
            (raw_dir / "000001.daily.raw.json").write_text(
                '[{"stck_bsop_date": "20260610"}]\n',
                encoding="utf-8",
            )
            calendar = root / "calendar.csv"
            calendar.write_text("date\n20260610\n20260611\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(AUDIT),
                    "--raw-dir",
                    str(raw_dir),
                    "--expected-calendar",
                    str(calendar),
                ],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Overall status: `hold`", result.stdout)
            self.assertIn("20260611", result.stdout)

    def test_duplicate_dates_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw"
            raw_dir.mkdir()
            (raw_dir / "000001.daily.raw.json").write_text(
                textwrap.dedent(
                    """
                    [
                      {"stck_bsop_date": "20260610"},
                      {"stck_bsop_date": "20260610"}
                    ]
                    """
                ).strip(),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(AUDIT), "--raw-dir", str(raw_dir)],
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Overall status: `fail`", result.stdout)
            self.assertIn("20260610", result.stdout)


if __name__ == "__main__":
    unittest.main()
