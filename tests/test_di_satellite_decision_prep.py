from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_satellite_decision_prep.py"
MANIFEST_FILE = REPO_ROOT / "_report/di/candidates/core-satellite-candidates.yaml"
INPUT_EXAMPLE = REPO_ROOT / "_report/di/templates/satellite-decision-inputs.example.yaml"
REQUIRED_MANUAL_INPUT_FIELDS = {
    "latest_price_checked",
    "valuation_range_checked",
    "reverse_dcf_checked",
    "etf_overlap_checked",
    "tax_account_route",
    "max_position_size",
    "add_trim_rule",
    "source_freshness_checked",
}


MANIFEST = """\
satellite_equities:
  primary_queue:
    - symbol: MSFT
      name: Microsoft
      market: NASDAQ
      status: candidate
      filings_to_read: [10-K, 10-Q, 8-K, XBRL]
  secondary_queue: []
"""


def _write_thesis(path: Path) -> None:
    path.write_text(
        """\
# Thesis

- Symbol: MSFT
- Company: Microsoft
- Source: SEC 10-K and 10-Q evidence
1. Azure is the first operating driver to verify.
2. Enterprise software cash flow funds AI infrastructure.
3. Capex and margin pressure are the main counterweight.
- Invalidation rule: cloud growth or margin quality breaks the written thesis.
""",
        encoding="utf-8",
    )


def _write_financials(path: Path) -> None:
    path.write_text(
        """\
# Financials

- Symbol: MSFT
- Source: SEC companyfacts
- Order intent generated: `false`
- Annual revenue is recorded.
- Annual operating income is recorded.
- Annual net income is recorded.
- Annual operating cash flow is recorded.
- Annual capex is recorded.
- Annual free cash flow proxy is recorded.
- Balance sheet cash and debt proxy are recorded.
- Data quality caveats are recorded.
""",
        encoding="utf-8",
    )


def _write_valuation(path: Path) -> None:
    path.write_text(
        """\
# Valuation

- Symbol: MSFT
- Source: latest market snapshot and SEC filing financials
- Order intent generated: `false`
- Latest price is recorded with timestamp.
- Market cap is recorded.
- Base scenario valuation range is recorded.
- Bear scenario valuation range is recorded.
- Reverse DCF assumption set is recorded.
- ETF overlap is recorded.
- Tax/account route is recorded.
- Maximum position size is recorded.
""",
        encoding="utf-8",
    )


class DiSatelliteDecisionPrepTest(unittest.TestCase):
    def test_input_example_covers_current_primary_queue(self) -> None:
        manifest = yaml.safe_load(MANIFEST_FILE.read_text(encoding="utf-8"))
        template = yaml.safe_load(INPUT_EXAMPLE.read_text(encoding="utf-8"))

        primary_symbols = [
            row["symbol"].upper()
            for row in manifest["satellite_equities"]["primary_queue"]
        ]
        template_inputs = template["inputs"]

        self.assertEqual(primary_symbols, list(template_inputs))
        for symbol in primary_symbols:
            self.assertEqual(REQUIRED_MANUAL_INPUT_FIELDS, set(template_inputs[symbol]))

    def test_reports_pre_decision_inputs_without_creating_order_intent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            manifest.write_text(MANIFEST, encoding="utf-8")
            _write_thesis(msft / "thesis.md")
            _write_financials(msft / "financials.md")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--research-root",
                    str(research_root),
                    "--run-date",
                    "2026-07-08",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| Candidates checked | 1 |", result.stdout)
            self.assertIn("| Ready for checked decision | 0 |", result.stdout)
            self.assertIn("| `primary_queue` | `MSFT` | Microsoft | `needs_decision_inputs` |", result.stdout)
            self.assertIn("`valuation.md`", result.stdout)
            self.assertIn("`latest_price`", result.stdout)
            self.assertIn("`etf_overlap`", result.stdout)
            self.assertIn("Order intent generated: `false`", result.stdout)

    def test_current_repo_primary_queue_stays_pre_decision(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--candidate-file",
                "_report/di/candidates/core-satellite-candidates.yaml",
                "--run-date",
                "2026-07-08",
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Candidates checked | 6 |", result.stdout)
        self.assertIn("| Ready for checked decision | 0 |", result.stdout)
        self.assertIn("| Needs prep | 6 |", result.stdout)
        self.assertIn("| `primary_queue` | `MSFT` | Microsoft | `needs_decision_inputs` |", result.stdout)
        self.assertIn("| `primary_queue` | `AVGO` | Broadcom | `needs_decision_inputs` |", result.stdout)
        self.assertIn(
            "| `primary_queue` | `AVGO` | Broadcom | `needs_decision_inputs` | present: financials.md+thesis.md+valuation.md; pending: decision.md |",
            result.stdout,
        )
        self.assertIn("`tax_account_route`", result.stdout)
        self.assertIn("[[_report/di/candidates/core-satellite-candidates.yaml|core-satellite-candidates.yaml]]", result.stdout)
        self.assertIn("[[_report/private/di/satellite-decision-inputs.yaml|satellite-decision-inputs.yaml]]", result.stdout)

    def test_placeholder_valuation_stays_pending(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            manifest.write_text(MANIFEST, encoding="utf-8")
            _write_thesis(msft / "thesis.md")
            _write_financials(msft / "financials.md")
            (msft / "valuation.md").write_text(
                """\
# Valuation

- Symbol: TODO
- Latest price: TODO
- Market cap: TODO
- Base scenario: TODO
- Bear scenario: TODO
- ETF overlap: TODO
- Tax/account route: TODO
- Maximum position size: TODO
""",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--research-root",
                    str(research_root),
                    "--run-date",
                    "2026-07-08",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("pending: valuation.md+decision.md", result.stdout)
            self.assertIn("`valuation.md`", result.stdout)

    def test_private_input_file_can_clear_manual_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            input_file = root / "inputs.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            manifest.write_text(MANIFEST, encoding="utf-8")
            input_file.write_text(
                """\
version: 1
inputs:
  MSFT:
    latest_price_checked: "2026-07-08 source recorded"
    valuation_range_checked: "base bear bull range recorded"
    reverse_dcf_checked: "scenario assumptions recorded"
    etf_overlap_checked: "core and satellite overlap recorded"
    tax_account_route: "taxable account route recorded"
    max_position_size: "single-name cap recorded"
    add_trim_rule: "add and trim rule recorded"
    source_freshness_checked: "source dates recorded"
""",
                encoding="utf-8",
            )
            _write_thesis(msft / "thesis.md")
            _write_financials(msft / "financials.md")
            _write_valuation(msft / "valuation.md")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--research-root",
                    str(research_root),
                    "--input-file",
                    str(input_file),
                    "--run-date",
                    "2026-07-08",
                    "--fail-on-blocked",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| Ready for checked decision | 1 |", result.stdout)
            self.assertIn("| `primary_queue` | `MSFT` | Microsoft | `ready_for_checked_decision` |", result.stdout)
            self.assertIn("write checked decision.md with no order intent", result.stdout)

    def test_fail_on_blocked_returns_2_and_only_blocked_filters_ready_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            input_file = root / "inputs.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            nvda = research_root / "NVDA"
            msft.mkdir(parents=True)
            nvda.mkdir(parents=True)
            manifest.write_text(
                """\
satellite_equities:
  primary_queue:
    - symbol: MSFT
      name: Microsoft
      market: NASDAQ
      status: candidate
    - symbol: NVDA
      name: NVIDIA
      market: NASDAQ
      status: candidate
  secondary_queue: []
""",
                encoding="utf-8",
            )
            input_file.write_text(
                """\
version: 1
inputs:
  MSFT:
    latest_price_checked: "recorded"
    valuation_range_checked: "recorded"
    reverse_dcf_checked: "recorded"
    etf_overlap_checked: "recorded"
    tax_account_route: "recorded"
    max_position_size: "recorded"
    add_trim_rule: "recorded"
    source_freshness_checked: "recorded"
""",
                encoding="utf-8",
            )
            _write_thesis(msft / "thesis.md")
            _write_financials(msft / "financials.md")
            _write_valuation(msft / "valuation.md")
            _write_thesis(nvda / "thesis.md")
            _write_financials(nvda / "financials.md")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--candidate-file",
                    str(manifest),
                    "--research-root",
                    str(research_root),
                    "--input-file",
                    str(input_file),
                    "--run-date",
                    "2026-07-08",
                    "--only-blocked",
                    "--fail-on-blocked",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("Row filter: `blocked_only`", result.stdout)
            self.assertIn("| Candidates checked | 1 |", result.stdout)
            self.assertIn("| Ready for checked decision | 0 |", result.stdout)
            self.assertNotIn("| `primary_queue` | `MSFT` | Microsoft |", result.stdout)
            self.assertIn("| `primary_queue` | `NVDA` | NVIDIA | `needs_decision_inputs` |", result.stdout)
            self.assertIn("Order intent generated: `false`", result.stdout)

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
