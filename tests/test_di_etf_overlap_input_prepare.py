from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_etf_overlap_input_prepare.py"


MANIFEST = """\
core_etfs:
  - symbol: VOO
    name: Vanguard S&P 500 ETF
    source_url: https://investor.vanguard.com/investment-products/etfs/profile/voo
satellite_etfs_to_verify:
  - symbol: QQQ
    name: Invesco QQQ Trust
    source_url: https://www.invesco.com/qqq-etf/en/about.html
satellite_equities:
  primary_queue:
    - symbol: MSFT
      name: Microsoft
    - symbol: GOOGL
      name: Alphabet
    - symbol: AMZN
      name: Amazon
  secondary_queue: []
"""


NORMALIZED_QQQ = {
    "provider": "invesco",
    "as_of": "2026-07-07",
    "coverage": "full",
    "candidate_holdings": {
        "MSFT": 4.631281,
        "GOOGL": 3.427326,
        "AMZN": None,
    },
    "share_class_notes": {
        "GOOGL": "GOOG is reported separately at 3.180934%; decide whether to combine Alphabet classes.",
    },
}


def _write_normalized(root: Path, run_date: str = "2026-07-09") -> None:
    path = root / "raw" / run_date[:4] / run_date / "di" / "etf-holdings" / "QQQ" / "holdings.normalized.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(NORMALIZED_QQQ), encoding="utf-8")


class DiEtfOverlapInputPrepareTest(unittest.TestCase):
    def test_prefills_supported_official_holdings_without_private_weights(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            output = root / "private" / "etf-overlap-inputs.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")
            _write_normalized(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--raw-root",
                    str(root / "raw"),
                    "--run-date",
                    "2026-07-09",
                    "--input-file",
                    str(output),
                    "--output",
                    str(output),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads(result.stdout)
            self.assertFalse(summary["order_intent_generated"])
            self.assertEqual([row["symbol"] for row in summary["autofilled_etfs"]], ["QQQ"])
            self.assertEqual(summary["manual_required_etfs"], ["VOO"])

            payload = yaml.safe_load(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["portfolio_etf_weights"]["VOO"], "TODO - portfolio percent")
            self.assertEqual(payload["portfolio_etf_weights"]["QQQ"], "TODO - portfolio percent")
            self.assertEqual(payload["etf_holdings"]["QQQ"]["as_of"], "2026-07-07")
            self.assertEqual(payload["etf_holdings"]["QQQ"]["coverage"], "full")
            self.assertEqual(payload["etf_holdings"]["QQQ"]["holdings"]["MSFT"], 4.631281)
            self.assertEqual(payload["etf_holdings"]["QQQ"]["holdings"]["GOOGL"], 3.427326)
            self.assertEqual(payload["etf_holdings"]["QQQ"]["holdings"]["AMZN"], "TODO - ETF holding percent")
            self.assertIn("GOOG is reported separately", payload["etf_holdings"]["QQQ"]["notes"][0])
            self.assertEqual(payload["etf_holdings"]["VOO"]["coverage"], "TODO - full, candidate_only, or top_n")

    def test_preserves_existing_private_values_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            existing = root / "private" / "etf-overlap-inputs.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")
            existing.parent.mkdir(parents=True)
            existing.write_text(
                """\
version: 1
portfolio_etf_weights:
  QQQ: 15
etf_holdings:
  QQQ:
    as_of: "2026-06-30"
    source_url: "https://manual.example/qqq"
    coverage: candidate_only
    holdings:
      MSFT: 9.9
""",
                encoding="utf-8",
            )
            _write_normalized(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--raw-root",
                    str(root / "raw"),
                    "--run-date",
                    "2026-07-09",
                    "--input-file",
                    str(existing),
                    "--output",
                    str(existing),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = yaml.safe_load(existing.read_text(encoding="utf-8"))
            self.assertEqual(payload["portfolio_etf_weights"]["QQQ"], 15)
            self.assertEqual(payload["etf_holdings"]["QQQ"]["as_of"], "2026-06-30")
            self.assertEqual(payload["etf_holdings"]["QQQ"]["source_url"], "https://manual.example/qqq")
            self.assertEqual(payload["etf_holdings"]["QQQ"]["holdings"]["MSFT"], 9.9)
            self.assertEqual(payload["etf_holdings"]["QQQ"]["holdings"]["GOOGL"], 3.427326)

    def test_refresh_official_overwrites_existing_official_fields_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            existing = root / "private" / "etf-overlap-inputs.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")
            existing.parent.mkdir(parents=True)
            existing.write_text(
                """\
version: 1
portfolio_etf_weights:
  QQQ: 15
etf_holdings:
  QQQ:
    as_of: "2026-06-30"
    source_url: "https://manual.example/qqq"
    coverage: candidate_only
    holdings:
      MSFT: 9.9
""",
                encoding="utf-8",
            )
            _write_normalized(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--raw-root",
                    str(root / "raw"),
                    "--run-date",
                    "2026-07-09",
                    "--input-file",
                    str(existing),
                    "--output",
                    str(existing),
                    "--refresh-official",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = yaml.safe_load(existing.read_text(encoding="utf-8"))
            self.assertEqual(payload["portfolio_etf_weights"]["QQQ"], 15)
            self.assertEqual(payload["etf_holdings"]["QQQ"]["as_of"], "2026-07-07")
            self.assertEqual(payload["etf_holdings"]["QQQ"]["source_url"], "https://www.invesco.com/qqq-etf/en/about.html")
            self.assertEqual(payload["etf_holdings"]["QQQ"]["holdings"]["MSFT"], 4.631281)

    def test_dry_run_does_not_write_private_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            output = root / "private" / "etf-overlap-inputs.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")
            _write_normalized(root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--raw-root",
                    str(root / "raw"),
                    "--run-date",
                    "2026-07-09",
                    "--input-file",
                    str(output),
                    "--output",
                    str(output),
                    "--dry-run",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(output.exists())
            self.assertTrue(json.loads(result.stdout)["dry_run"])


if __name__ == "__main__":
    unittest.main()
