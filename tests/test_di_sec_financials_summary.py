from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_sec_financials_summary.py"


def _concept(facts: list[dict[str, object]]) -> dict[str, object]:
    return {"units": {"USD": facts}}


def _annual(val: int, end: str, filed: str, fy: int) -> dict[str, object]:
    return {
        "val": val,
        "start": f"{fy - 1}-01-01",
        "end": end,
        "filed": filed,
        "fy": fy,
        "fp": "FY",
        "form": "10-K",
        "accn": f"annual-{fy}",
    }


def _quarter(val: int, start: str, end: str, filed: str, fy: int, fp: str) -> dict[str, object]:
    return {
        "val": val,
        "start": start,
        "end": end,
        "filed": filed,
        "fy": fy,
        "fp": fp,
        "form": "10-Q",
        "accn": f"quarter-{fy}-{fp}",
    }


def _instant(val: int, end: str, filed: str, fy: int, fp: str = "Q4") -> dict[str, object]:
    return {
        "val": val,
        "end": end,
        "filed": filed,
        "fy": fy,
        "fp": fp,
        "form": "10-Q",
        "accn": f"instant-{fy}-{fp}",
    }


class DiSecFinancialsSummaryTest(unittest.TestCase):
    def test_renders_financials_from_companyfacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw" / "2026" / "2026-07-08" / "sec" / "TST"
            output = root / "research" / "TST" / "financials.md"
            raw_dir.mkdir(parents=True)
            (raw_dir / "submissions.raw.json").write_text(json.dumps({"name": "TEST CO"}), encoding="utf-8")
            (raw_dir / "companyfacts.raw.json").write_text(
                json.dumps(
                    {
                        "entityName": "TEST CO",
                        "facts": {
                            "us-gaap": {
                                "RevenueFromContractWithCustomerExcludingAssessedTax": _concept(
                                    [
                                        _annual(100_000_000_000, "2025-12-31", "2026-02-01", 2025),
                                        _quarter(30_000_000_000, "2026-01-01", "2026-03-31", "2026-04-30", 2026, "Q1"),
                                    ]
                                ),
                                "OperatingIncomeLoss": _concept(
                                    [
                                        _annual(25_000_000_000, "2025-12-31", "2026-02-01", 2025),
                                        _quarter(9_000_000_000, "2026-01-01", "2026-03-31", "2026-04-30", 2026, "Q1"),
                                    ]
                                ),
                                "NetIncomeLoss": _concept(
                                    [
                                        _annual(20_000_000_000, "2025-12-31", "2026-02-01", 2025),
                                        _quarter(7_500_000_000, "2026-01-01", "2026-03-31", "2026-04-30", 2026, "Q1"),
                                    ]
                                ),
                                "NetCashProvidedByUsedInOperatingActivities": _concept(
                                    [
                                        _annual(30_000_000_000, "2025-12-31", "2026-02-01", 2025),
                                        _quarter(8_000_000_000, "2026-01-01", "2026-03-31", "2026-04-30", 2026, "Q1"),
                                    ]
                                ),
                                "PaymentsToAcquirePropertyPlantAndEquipment": _concept(
                                    [
                                        _annual(10_000_000_000, "2025-12-31", "2026-02-01", 2025),
                                        _quarter(3_000_000_000, "2026-01-01", "2026-03-31", "2026-04-30", 2026, "Q1"),
                                    ]
                                ),
                                "CashCashEquivalentsAndShortTermInvestments": _concept([_instant(12_000_000_000, "2026-03-31", "2026-04-30", 2026, "Q1")]),
                                "DebtLongtermAndShorttermCombinedAmount": _concept([_instant(4_000_000_000, "2026-03-31", "2026-04-30", 2026, "Q1")]),
                                "Assets": _concept([_instant(150_000_000_000, "2026-03-31", "2026-04-30", 2026, "Q1")]),
                                "Liabilities": _concept([_instant(50_000_000_000, "2026-03-31", "2026-04-30", 2026, "Q1")]),
                                "StockholdersEquity": _concept([_instant(100_000_000_000, "2026-03-31", "2026-04-30", 2026, "Q1")]),
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--symbol",
                    "TST",
                    "--run-date",
                    "2026-07-08",
                    "--raw-dir",
                    str(raw_dir),
                    "--output",
                    str(output),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("# TST Financials", report)
            self.assertIn("| 2025-12-31 | $100.0B | $25.0B | $20.0B | $30.0B | $10.0B | $20.0B | 25.0% | 20.0% | 20.0% |", report)
            self.assertIn("| 2026-03-31 | $30.0B | $9.0B | $7.5B | $8.0B | $3.0B | $5.0B | 30.0% | 25.0% | 16.7% |", report)
            self.assertIn("| 2026-03-31 | $12.0B | $4.0B | $8.0B | $150.0B | $50.0B | $100.0B |", report)
            self.assertIn("Order intent generated: `false`", report)

    def test_fails_when_companyfacts_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--symbol",
                    "TST",
                    "--raw-dir",
                    str(Path(tmp) / "missing"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("companyfacts.raw.json", result.stderr)


if __name__ == "__main__":
    unittest.main()
