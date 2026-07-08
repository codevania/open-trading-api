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


def _write_sec_documents(path: Path) -> None:
    path.write_text(
        """\
# SEC Filing Documents

- Source: SEC EDGAR primary filing documents
- Order intent generated: `false`
- Latest 10-K document: available
- Latest 10-Q document: available
- Local raw paths: recorded
- Reading checklist: recorded
""",
        encoding="utf-8",
    )


def _write_sec_sections(path: Path) -> None:
    path.write_text(
        """\
# SEC Filing Section Map

- Source: SEC filing HTML converted to ignored raw text snippets
- Order intent generated: `false`
- Business section: available
- Risk Factors section: available
- MD&A section: available
- Quarterly MD&A section: available
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
- Annual revenue, operating income, net income, operating cash flow, capex, and FCF are recorded.
- Quarterly revenue, operating income, net income, operating cash flow, capex, and FCF are recorded.
- Balance sheet assets, liabilities, equity, cash, and debt proxy are recorded.
- Concept selection notes are recorded.
- Data quality caveats are recorded.
- FCF calculation caveat is recorded.
- No buy or order intent is generated.
""",
        encoding="utf-8",
    )


def _write_valuation(path: Path) -> None:
    path.write_text(
        """\
# Valuation

- Symbol: MSFT
- Source: latest market data and filing-based financials
- Order intent generated: `false`
- Latest price and currency are recorded.
- Base scenario multiple range is recorded.
- Bull scenario assumptions are recorded.
- Bear scenario assumptions are recorded.
- Reverse DCF assumptions are recorded.
- ETF overlap is recorded.
- Tax/account route is recorded.
""",
        encoding="utf-8",
    )


class DiCandidateEvidenceCheckTest(unittest.TestCase):
    def test_reports_ready_and_hold_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            (msft / "sec-filing-summary.md").write_text(
                """\
# MSFT SEC Filing Summary

- Source: SEC EDGAR raw JSON collected for DI research
- Order intent generated: `false`
- Latest 10-K: available
- Latest 10-Q: available
- Latest 8-K: available
- XBRL facts: available
""",
                encoding="utf-8",
            )
            _write_sec_documents(msft / "sec-filing-documents.md")
            _write_sec_sections(msft / "sec-filing-sections.md")
            _write_financials(msft / "financials.md")
            _write_valuation(msft / "valuation.md")
            (msft / "thesis.md").write_text(
                """\
# Thesis

- Symbol: MSFT
- Company: Microsoft
- 주요 원천: SEC 10-K, SEC 10-Q
- 한 줄 결론: cloud and enterprise software remain the first thesis to test.
1. Azure growth is the first operating driver to verify.
2. Office and Windows cash flow fund AI infrastructure.
3. Capex and margin pressure are the main counterweight.
- 무효화 조건: cloud growth or margin quality breaks the written thesis.
""",
                encoding="utf-8",
            )
            (msft / "decision.md").write_text(
                """\
# Decision

- Symbol: MSFT
- Company/ETF: Microsoft
- [x] 관심
- 결정: research watch candidate only
1. Filing evidence exists in the research folder.
2. Position size is not approved yet.
- 무효화 조건: thesis evidence becomes stale.
""",
                encoding="utf-8",
            )
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

    def test_placeholder_stock_notes_do_not_pass_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            (msft / "sec-filing-summary.md").write_text(
                "# MSFT SEC Filing Summary\n\n- Source: SEC\n- 10-K available\n- 10-Q available\n- 8-K available\n- Facts available\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            _write_sec_documents(msft / "sec-filing-documents.md")
            _write_sec_sections(msft / "sec-filing-sections.md")
            _write_financials(msft / "financials.md")
            (msft / "thesis.md").write_text("# Thesis\n\n- Symbol:\n-\n1.\n", encoding="utf-8")
            (msft / "decision.md").write_text("# Decision\n\n- [ ] 관심\n-\n", encoding="utf-8")
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
                    "2026-07-08",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| Ready for next review | 1 |", result.stdout)
            self.assertIn("| `satellite_equities.primary_queue` | `MSFT` | Microsoft | `hold` |", result.stdout)
            self.assertIn("`research thesis.md content`", result.stdout)
            self.assertIn("`research valuation.md`", result.stdout)
            self.assertIn("`research decision.md content`", result.stdout)

    def test_decision_note_requires_checked_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            (msft / "sec-filing-summary.md").write_text(
                "# MSFT SEC Filing Summary\n\n- Source: SEC\n- 10-K available\n- 10-Q available\n- 8-K available\n- Facts available\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            _write_sec_documents(msft / "sec-filing-documents.md")
            _write_sec_sections(msft / "sec-filing-sections.md")
            _write_financials(msft / "financials.md")
            _write_valuation(msft / "valuation.md")
            (msft / "thesis.md").write_text(
                """\
# Thesis

- Symbol: MSFT
- Company: Microsoft
- 주요 원천: SEC 10-K
1. First thesis point with evidence.
2. Second thesis point with evidence.
3. Third thesis point with evidence.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
            (msft / "decision.md").write_text(
                """\
# Decision

- Symbol: MSFT
- Company/ETF: Microsoft
- [ ] 관심
- [ ] 보류
- 결정: no checked box yet.
1. Evidence was reviewed.
2. Risk budget remains pending.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
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
                    "2026-07-08",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("`research decision.md checked decision`", result.stdout)

    def test_stock_requires_valuation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            (msft / "sec-filing-summary.md").write_text(
                "# MSFT SEC Filing Summary\n\n- Source: SEC\n- 10-K available\n- 10-Q available\n- 8-K available\n- Facts available\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            _write_sec_documents(msft / "sec-filing-documents.md")
            _write_sec_sections(msft / "sec-filing-sections.md")
            _write_financials(msft / "financials.md")
            (msft / "thesis.md").write_text(
                """\
# Thesis

- Symbol: MSFT
- Company: Microsoft
- 二쇱슂 ?먯쿇: SEC 10-K
1. First thesis point with evidence.
2. Second thesis point with evidence.
3. Third thesis point with evidence.
- 臾댄슚??議곌굔: evidence changes.
""",
                encoding="utf-8",
            )
            (msft / "decision.md").write_text(
                """\
# Decision

- Symbol: MSFT
- Company/ETF: Microsoft
- [x] 愿??- 寃곗젙: valuation missing test.
1. Evidence was reviewed.
2. Risk budget remains pending.
- 臾댄슚??議곌굔: evidence changes.
""",
                encoding="utf-8",
            )
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
                    "2026-07-08",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("`research valuation.md`", result.stdout)

    def test_us_stock_requires_sec_filing_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            (msft / "thesis.md").write_text(
                """\
# Thesis

- Symbol: MSFT
- Company: Microsoft
- 주요 원천: SEC 10-K
1. First thesis point with evidence.
2. Second thesis point with evidence.
3. Third thesis point with evidence.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
            (msft / "decision.md").write_text(
                """\
# Decision

- Symbol: MSFT
- Company/ETF: Microsoft
- [x] 관심
- 결정: source summary missing test.
1. Evidence was reviewed.
2. Risk budget remains pending.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
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
                    "2026-07-08",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("`research sec-filing-summary.md`", result.stdout)

    def test_us_stock_requires_sec_filing_documents(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            (msft / "sec-filing-summary.md").write_text(
                "# MSFT SEC Filing Summary\n\n- Source: SEC\n- 10-K available\n- 10-Q available\n- 8-K available\n- Facts available\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            _write_sec_sections(msft / "sec-filing-sections.md")
            _write_financials(msft / "financials.md")
            (msft / "thesis.md").write_text(
                """\
# Thesis

- Symbol: MSFT
- Company: Microsoft
- 주요 원천: SEC 10-K
1. First thesis point with evidence.
2. Second thesis point with evidence.
3. Third thesis point with evidence.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
            (msft / "decision.md").write_text(
                """\
# Decision

- Symbol: MSFT
- Company/ETF: Microsoft
- [x] 관심
- 결정: source documents missing test.
1. Evidence was reviewed.
2. Risk budget remains pending.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
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
                    "2026-07-08",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("`research sec-filing-documents.md`", result.stdout)

    def test_us_stock_requires_sec_filing_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            (msft / "sec-filing-summary.md").write_text(
                "# MSFT SEC Filing Summary\n\n- Source: SEC\n- 10-K available\n- 10-Q available\n- 8-K available\n- Facts available\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            _write_sec_documents(msft / "sec-filing-documents.md")
            _write_financials(msft / "financials.md")
            (msft / "thesis.md").write_text(
                """\
# Thesis

- Symbol: MSFT
- Company: Microsoft
- 주요 원천: SEC 10-K
1. First thesis point with evidence.
2. Second thesis point with evidence.
3. Third thesis point with evidence.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
            (msft / "decision.md").write_text(
                """\
# Decision

- Symbol: MSFT
- Company/ETF: Microsoft
- [x] 관심
- 결정: source sections missing test.
1. Evidence was reviewed.
2. Risk budget remains pending.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
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
                    "2026-07-08",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("`research sec-filing-sections.md`", result.stdout)

    def test_stock_requires_financials(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "candidates.yaml"
            research_root = root / "research"
            msft = research_root / "MSFT"
            msft.mkdir(parents=True)
            (msft / "sec-filing-summary.md").write_text(
                "# MSFT SEC Filing Summary\n\n- Source: SEC\n- 10-K available\n- 10-Q available\n- 8-K available\n- Facts available\n- Order intent generated: `false`\n",
                encoding="utf-8",
            )
            _write_sec_documents(msft / "sec-filing-documents.md")
            _write_sec_sections(msft / "sec-filing-sections.md")
            (msft / "thesis.md").write_text(
                """\
# Thesis

- Symbol: MSFT
- Company: Microsoft
- 주요 원천: SEC 10-K
1. First thesis point with evidence.
2. Second thesis point with evidence.
3. Third thesis point with evidence.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
            (msft / "decision.md").write_text(
                """\
# Decision

- Symbol: MSFT
- Company/ETF: Microsoft
- [x] 관심
- 결정: financials missing test.
1. Evidence was reviewed.
2. Risk budget remains pending.
- 무효화 조건: evidence changes.
""",
                encoding="utf-8",
            )
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
                    "2026-07-08",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("`research financials.md`", result.stdout)

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
