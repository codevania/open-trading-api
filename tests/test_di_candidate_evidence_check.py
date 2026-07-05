from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_candidate_evidence_check.py"


MANIFEST = """\
core_etfs:
  - symbol: VOO
    name: Vanguard S&P 500 ETF
    benchmark: S&P 500 Index
    source_url: https://example.com/voo
    currency_hedge: unhedged
    distribution_policy: quarterly
    tax_account_fit: taxable account note recorded
    expense_ratio: "0.03%"
korea_listed_etfs_to_verify:
  - symbol: "360750"
    name: TIGER US S&P500
    benchmark: S&P 500 Index
    source_url: null
    currency_hedge: verify
    distribution_policy: verify
    tax_account_fit: check account wrapper
    expense_ratio: null
satellite_etfs_to_verify: []
satellite_equities:
  primary_queue:
    - symbol: MSFT
      name: Microsoft
      market: NASDAQ
      filings_to_read: [10-K, 10-Q, 8-K, XBRL]
  secondary_queue: []
"""


class DiCandidateEvidenceCheckTest(unittest.TestCase):
    def test_reports_ready_and_hold_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            (msft / "thesis.md").write_text("# Thesis\n", encoding="utf-8")
            (msft / "decision.md").write_text("# Decision\n", encoding="utf-8")
            manifest.write_text(MANIFEST, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--research-root",
                    str(research_root),
                    "--run-date",
                    "2026-07-06",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| Candidates checked | 3 |", result.stdout)
            self.assertIn("| Ready for next review | 2 |", result.stdout)
            self.assertIn("| `core_etfs` | `VOO` | Vanguard S&P 500 ETF | `ready_for_decision_note` | - |", result.stdout)
            self.assertIn("| `korea_listed_etfs_to_verify` | `360750` | TIGER US S&P500 | `hold` |", result.stdout)
            self.assertIn("`source_url`, `currency_hedge`, `distribution_policy`, `tax_account_fit`, `expense_ratio`", result.stdout)
            self.assertIn("| `satellite_equities.primary_queue` | `MSFT` | Microsoft | `ready_for_watchlist_review` | - |", result.stdout)
            self.assertIn("Order intent generated: `false`", result.stdout)

    def test_current_repo_candidates_are_not_ready_for_promotion(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--candidate-file",
                "_report/di/candidates/core-satellite-candidates.yaml",
                "--run-date",
                "2026-07-06",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Candidates checked | 17 |", result.stdout)
        self.assertIn("| Ready for next review | 0 |", result.stdout)
        self.assertIn("| Hold | 17 |", result.stdout)

    def test_rejects_non_object_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "bad.yaml"
            manifest.write_text("- not\n- object\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--candidate-file", str(manifest)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("expected YAML object", result.stderr)


if __name__ == "__main__":
    unittest.main()
