from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "di_sec_filing_section_extract.py"


TEN_K_HTML = """\
<html><body>
<p>Table of contents</p>
<p>Item 1. Business</p>
<p>Item 1A. Risk Factors</p>
<h1>Item 1. Business</h1>
<p>Business body sentence one. Business body sentence two. Business body sentence three.
Business body sentence four. Business body sentence five.</p>
<h1>Item 1A. Risk Factors</h1>
<p>Risk body sentence one. Risk body sentence two. Risk body sentence three.
Risk body sentence four. Risk body sentence five.</p>
<h1>Item 7. Management's Discussion and Analysis</h1>
<p>MD&A body sentence one. MD&A body sentence two. MD&A body sentence three.
MD&A body sentence four. MD&A body sentence five.</p>
<h1>Item 7A. Quantitative and Qualitative Disclosures</h1>
</body></html>
"""


TEN_Q_HTML = """\
<html><body>
<p>Table of contents</p>
<p>Item 1A. Risk Factors</p>
<p>Item 2. Management's Discussion and Analysis</p>
<h1>Item 1A. Risk Factors</h1>
<p>Quarterly risk body sentence one. Quarterly risk body sentence two.
Quarterly risk body sentence three. Quarterly risk body sentence four.</p>
<h1>Item 2. Management's Discussion and Analysis</h1>
<p>Quarterly MD&A sentence one. Quarterly MD&A sentence two.
Quarterly MD&A sentence three. Quarterly MD&A sentence four.</p>
<h1>Item 3. Quantitative and Qualitative Disclosures</h1>
</body></html>
"""


class DiSecFilingSectionExtractTest(unittest.TestCase):
    def test_extracts_narrative_sections_to_ignored_raw_text_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw" / "2026" / "2026-07-08" / "sec" / "TST"
            filings = raw_dir / "filings"
            filings.mkdir(parents=True)
            (filings / "10-K_2026-02-01_0000000001_tst-20251231.htm.raw.html").write_text(TEN_K_HTML, encoding="utf-8")
            (filings / "10-Q_2026-04-30_0000000002_tst-20260331.htm.raw.html").write_text(TEN_Q_HTML, encoding="utf-8")
            output = root / "research" / "TST" / "sec-filing-sections.md"

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
                    "--min-chars",
                    "50",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = output.read_text(encoding="utf-8")
            self.assertIn("| `10-K` | 2026-02-01 | business | `ok` |", report)
            self.assertIn("| `10-K` | 2026-02-01 | risk_factors | `ok` |", report)
            self.assertIn("| `10-K` | 2026-02-01 | mda | `ok` |", report)
            self.assertIn("| `10-Q` | 2026-04-30 | quarterly_mda | `ok` |", report)
            business = raw_dir / "sections" / "10-K_2026-02-01_0000000001_business.raw.txt"
            self.assertTrue(business.exists())
            business_text = business.read_text(encoding="utf-8")
            self.assertIn("Business body sentence one", business_text)
            self.assertNotIn("Table of contents", business_text)
            self.assertIn("Order intent generated: `false`", report)

    def test_fails_when_filing_documents_are_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--symbol",
                    "TST",
                    "--raw-dir",
                    str(Path(tmp) / "raw"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no filing HTML documents found", result.stderr)


if __name__ == "__main__":
    unittest.main()
