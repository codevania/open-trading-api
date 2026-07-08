from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_etf_holdings_collect.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("di_etf_holdings_collect", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


MANIFEST = """\
core_etfs:
  - symbol: VOO
    name: Vanguard S&P 500 ETF
    source_url: https://investor.vanguard.com/investment-products/etfs/profile/voo
  - symbol: VTI
    name: Vanguard Total Stock Market ETF
    source_url: https://investor.vanguard.com/investment-products/etfs/profile/vti
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
    - symbol: NVDA
      name: NVIDIA
  secondary_queue:
    - symbol: AAPL
      name: Apple
"""


INVESCO_SAMPLE = {
    "cusip": "QQQ",
    "effectiveDate": "2026-07-07",
    "effectiveBusinessDate": "2026-07-07",
    "totalNumberOfHoldings": 4,
    "holdings": [
        {
            "ticker": "NVDA",
            "issuerName": "NVIDIA Corp",
            "percentageOfTotalNetAssets": 7.641168,
            "securityTypeName": "Common Stock",
            "currency": "USD",
            "cusip": "67066G104",
        },
        {
            "ticker": "MSFT",
            "issuerName": "Microsoft Corp",
            "percentageOfTotalNetAssets": 4.631281,
            "securityTypeName": "Common Stock",
            "currency": "USD",
            "cusip": "594918104",
        },
        {
            "ticker": "GOOGL",
            "issuerName": "Alphabet Inc Class A",
            "percentageOfTotalNetAssets": 3.427326,
            "securityTypeName": "Common Stock",
            "currency": "USD",
            "cusip": "02079K305",
        },
        {
            "ticker": "GOOG",
            "issuerName": "Alphabet Inc Class C",
            "percentageOfTotalNetAssets": 3.180934,
            "securityTypeName": "Common Stock",
            "currency": "USD",
            "cusip": "02079K107",
        },
    ],
}


class DiEtfHoldingsCollectTest(unittest.TestCase):
    def test_dry_run_marks_qqq_fetchable_and_vanguard_manual(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "candidates.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--raw-root",
                    str(Path(tmp) / "raw"),
                    "--run-date",
                    "2026-07-09",
                    "--dry-run",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            by_symbol = {row["symbol"]: row for row in payload["sources"]}
            self.assertEqual(by_symbol["QQQ"]["source_state"], "confirmed_api")
            self.assertTrue(by_symbol["QQQ"]["live_fetch_supported"])
            self.assertIn("dng-api.invesco.com", by_symbol["QQQ"]["holdings_url"])
            self.assertEqual(by_symbol["VOO"]["source_state"], "manual_official_source_required")
            self.assertFalse(by_symbol["VOO"]["live_fetch_supported"])
            self.assertEqual(payload["candidate_symbols"], ["MSFT", "GOOGL", "NVDA"])
            self.assertFalse(payload["order_intent_generated"])

    def test_symbol_filter_limits_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "candidates.yaml"
            manifest.write_text(MANIFEST, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--symbol",
                    "qqq",
                    "--dry-run",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual([row["symbol"] for row in payload["sources"]], ["QQQ"])

    def test_normalizes_invesco_candidate_weights_and_share_class_note(self) -> None:
        module = _load_module()

        normalized = module.normalize_invesco_holdings(INVESCO_SAMPLE, ("MSFT", "GOOGL", "NVDA", "AMZN"))

        self.assertEqual(normalized["as_of"], "2026-07-07")
        self.assertEqual(normalized["coverage"], "full")
        self.assertEqual(normalized["candidate_holdings"]["MSFT"], 4.631281)
        self.assertEqual(normalized["candidate_holdings"]["GOOGL"], 3.427326)
        self.assertEqual(normalized["candidate_holdings"]["NVDA"], 7.641168)
        self.assertIsNone(normalized["candidate_holdings"]["AMZN"])
        self.assertIn("GOOG is reported separately", normalized["share_class_notes"]["GOOGL"])

    def test_rendered_status_report_keeps_private_portfolio_weights_out(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "candidates.yaml"
            output = Path(tmp) / "status.md"
            manifest.write_text(MANIFEST, encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--run-date",
                    "2026-07-09",
                    "--dry-run",
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
            self.assertIn("# DI ETF Holdings Source Status", report)
            self.assertIn(
                "Private portfolio ETF weights stay only in [[_report/private/di/etf-overlap-inputs.yaml|etf-overlap-inputs.yaml]].",
                report,
            )
            self.assertIn("| `QQQ` | `invesco` | `confirmed_api` | `yes` |", report)
            self.assertIn("| `VOO` | `vanguard` | `manual_official_source_required` | `no` |", report)

    def test_rejects_non_object_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "bad.yaml"
            manifest.write_text("- not\n- object\n", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--candidate-file", str(manifest), "--dry-run"],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("expected YAML object", result.stderr)


if __name__ == "__main__":
    unittest.main()
