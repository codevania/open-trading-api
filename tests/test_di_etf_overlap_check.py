from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_etf_overlap_check.py"
MANIFEST_FILE = REPO_ROOT / "_report/di/candidates/core-satellite-candidates.yaml"
INPUT_EXAMPLE = REPO_ROOT / "_report/di/templates/etf-overlap-inputs.example.yaml"


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


INPUTS = """\
version: 1
portfolio_etf_weights:
  VOO: 50
  QQQ: 10
etf_holdings:
  VOO:
    as_of: "2026-07-09"
    source_url: "https://issuer.example/voo-holdings"
    coverage: candidate_only
    holdings:
      MSFT: 7.2
      NVDA: 6.0
  QQQ:
    as_of: "2026-07-09"
    source_url: "https://issuer.example/qqq-holdings"
    coverage: candidate_only
    holdings:
      MSFT: 8.5
      NVDA: 7.0
"""


class DiEtfOverlapCheckTest(unittest.TestCase):
    def test_calculates_portfolio_overlap_when_inputs_are_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            inputs = root / "overlap.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")
            inputs.write_text(INPUTS, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--input-file",
                    str(inputs),
                    "--run-date",
                    "2026-07-09",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| Candidates checked | 2 |", result.stdout)
            self.assertIn("| Ready for private decision input | 2 |", result.stdout)
            self.assertIn("| `primary_queue` | `MSFT` | Microsoft | `ready_for_private_decision_input` |", result.stdout)
            self.assertIn("`VOO=7.20%`, `QQQ=8.50%`", result.stdout)
            self.assertIn("`4.45pp`", result.stdout)
            self.assertIn("Order intent generated: `false`", result.stdout)

    def test_missing_inputs_keep_candidate_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            inputs = root / "overlap.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")
            inputs.write_text(
                """\
version: 1
portfolio_etf_weights:
  VOO: 50
etf_holdings:
  VOO:
    as_of: "2026-07-09"
    source_url: "https://issuer.example/voo-holdings"
    coverage: candidate_only
    holdings:
      MSFT: 7.2
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--input-file",
                    str(inputs),
                    "--run-date",
                    "2026-07-09",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| Ready for private decision input | 0 |", result.stdout)
            self.assertIn("`needs_overlap_inputs`", result.stdout)
            self.assertIn("`QQQ:source_meta`", result.stdout)
            self.assertIn("`QQQ:portfolio_weight`", result.stdout)
            self.assertIn("`VOO:NVDA_weight`", result.stdout)

    def test_zero_portfolio_weight_counts_as_filled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            inputs = root / "overlap.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")
            inputs.write_text(
                INPUTS.replace("QQQ: 10", "QQQ: 0"),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--input-file",
                    str(inputs),
                    "--run-date",
                    "2026-07-09",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| Ready for private decision input | 2 |", result.stdout)
            self.assertIn("`3.60pp`", result.stdout)

    def test_example_template_covers_current_primary_queue_and_etfs(self) -> None:
        manifest = yaml.safe_load(MANIFEST_FILE.read_text(encoding="utf-8"))
        template = yaml.safe_load(INPUT_EXAMPLE.read_text(encoding="utf-8"))

        primary_symbols = [
            row["symbol"].upper()
            for row in manifest["satellite_equities"]["primary_queue"]
        ]
        expected_etfs = [
            row["symbol"].upper()
            for row in manifest["core_etfs"] + manifest["satellite_etfs_to_verify"]
        ]

        self.assertEqual(expected_etfs, list(template["portfolio_etf_weights"]))
        self.assertEqual(expected_etfs, list(template["etf_holdings"]))
        for etf in expected_etfs:
            self.assertEqual(primary_symbols, list(template["etf_holdings"][etf]["holdings"]))

    def test_rejects_non_numeric_filled_percent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            inputs = root / "overlap.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")
            inputs.write_text(
                """\
portfolio_etf_weights:
  VOO: "large"
etf_holdings:
  VOO:
    as_of: "2026-07-09"
    source_url: "https://issuer.example/voo-holdings"
    coverage: candidate_only
    holdings:
      MSFT: 7.2
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--input-file",
                    str(inputs),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("portfolio_etf_weights.VOO: expected numeric percent", result.stderr)


if __name__ == "__main__":
    unittest.main()
