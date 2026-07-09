from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_private_input_status.py"


MANIFEST = """\
core_etfs:
  - symbol: VOO
    name: Vanguard S&P 500 ETF
satellite_etfs_to_verify:
  - symbol: QQQ
    name: Invesco QQQ Trust
satellite_equities:
  primary_queue:
    - symbol: MSFT
      name: Microsoft
      market: NASDAQ
    - symbol: NVDA
      name: NVIDIA
      market: NASDAQ
  secondary_queue: []
"""


class DiPrivateInputStatusTest(unittest.TestCase):
    def test_masks_private_values_while_reporting_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            etf_inputs = root / "etf-overlap-inputs.yaml"
            decision_inputs = root / "satellite-decision-inputs.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")
            etf_inputs.write_text(
                """\
version: 1
portfolio_etf_weights:
  VOO: 70
  QQQ: TODO - portfolio percent
etf_holdings:
  VOO:
    as_of: "2026-07-09"
    source_url: "https://issuer.example/voo-holdings"
    coverage: full
    holdings:
      MSFT: 5.4
      NVDA: TODO - ETF holding percent
  QQQ:
    as_of: "2026-07-09"
    source_url: "https://issuer.example/qqq-holdings"
    coverage: candidate_only
    holdings:
      MSFT: 8.1
      NVDA: 7.7
""",
                encoding="utf-8",
            )
            decision_inputs.write_text(
                """\
version: 1
inputs:
  MSFT:
    latest_price_checked: "SENSITIVE_PRICE_MARKER"
    valuation_range_checked: "SENSITIVE_VALUATION_RANGE"
    reverse_dcf_checked: "SENSITIVE_REVERSE_DCF"
    etf_overlap_checked: "SENSITIVE_OVERLAP_NOTE"
    tax_account_route: "SENSITIVE_TAXABLE_ROUTE"
    max_position_size: "SENSITIVE_POSITION_LIMIT"
    add_trim_rule: "SENSITIVE_ADD_TRIM_RULE"
    source_freshness_checked: "SENSITIVE_FRESHNESS_NOTE"
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--etf-input-file",
                    str(etf_inputs),
                    "--decision-input-file",
                    str(decision_inputs),
                    "--run-date",
                    "2026-07-10",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Sensitive values printed: `false`", result.stdout)
            self.assertIn(
                "| ETF portfolio weight | `VOO` | `portfolio_etf_weights.VOO` | `filled` |",
                result.stdout,
            )
            self.assertIn(
                "| ETF portfolio weight | `QQQ` | `portfolio_etf_weights.QQQ` | `missing` |",
                result.stdout,
            )
            self.assertIn(
                "| ETF holding weight | `VOO:NVDA` | `etf_holdings.VOO.holdings.NVDA` | `missing` |",
                result.stdout,
            )
            self.assertIn(
                "| Satellite decision input | `MSFT` | `inputs.MSFT.latest_price_checked` | `filled` |",
                result.stdout,
            )
            self.assertIn(
                "| Satellite decision input | `NVDA` | `inputs.NVDA.latest_price_checked` | `missing` |",
                result.stdout,
            )
            self.assertNotIn("70", result.stdout)
            self.assertNotIn("5.4", result.stdout)
            self.assertNotIn("SENSITIVE_", result.stdout)

    def test_missing_private_files_report_missing_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--etf-input-file",
                    str(root / "missing-etf.yaml"),
                    "--decision-input-file",
                    str(root / "missing-decision.yaml"),
                    "--run-date",
                    "2026-07-10",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| Missing fields | 24 |", result.stdout)
            self.assertIn("`portfolio_etf_weights.VOO` | `missing`", result.stdout)
            self.assertIn("`inputs.MSFT.tax_account_route` | `missing`", result.stdout)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
