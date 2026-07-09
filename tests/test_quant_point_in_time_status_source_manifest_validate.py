from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from scripts.quant_point_in_time_status_source_manifest_validate import main, validate_manifest


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_policy(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                'version: "1.0"',
                "sources:",
                "  kind:",
                "    allowed_url_prefixes:",
                '      - "https://kind.krx.co.kr/"',
                "  krx_data_marketplace:",
                "    allowed_url_prefixes:",
                '      - "https://data.krx.co.kr/"',
                "",
            ]
        ),
        encoding="utf-8",
    )


def _market_rows() -> list[dict[str, str]]:
    return [
        {"date": "2025-01-02", "code": "005930"},
        {"date": "2025-01-03", "code": "005930"},
    ]


def _manifest_row(
    *,
    status_type: str = "managed_issue",
    coverage_start: str = "2025-01-02",
    coverage_end: str = "2025-01-03",
    source: str = "kind",
    source_url: str = "https://kind.krx.co.kr/example",
    raw_path: str = "_report/raw/2026/2026-07-08/kind/status-source-probe/managed_issue.xls",
    confidence: str = "high",
) -> dict[str, str]:
    return {
        "status_type": status_type,
        "coverage_start": coverage_start,
        "coverage_end": coverage_end,
        "source": source,
        "source_url": source_url,
        "raw_path": raw_path,
        "confidence": confidence,
        "notes": "fixture",
    }


class QuantPointInTimeStatusSourceManifestValidateTest(unittest.TestCase):
    def test_passes_when_each_required_status_type_covers_market_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.yaml"
            manifest = root / "manifest.csv"
            market = root / "market.csv"
            _write_policy(policy)
            _write_csv(market, _market_rows())
            rows = []
            for status_type in ("managed_issue", "trading_halt"):
                raw = root / "_report" / "raw" / "2026" / "2026-07-08" / "kind" / f"{status_type}.xls"
                raw.parent.mkdir(parents=True, exist_ok=True)
                raw.write_text("fixture\n", encoding="utf-8")
                rows.append(
                    _manifest_row(
                        status_type=status_type,
                        raw_path=f"_report/raw/2026/2026-07-08/kind/{status_type}.xls",
                    )
                )
            extra_raw = root / "_report" / "raw" / "2026" / "2026-07-08" / "kind" / "other_status.xls"
            extra_raw.write_text("fixture\n", encoding="utf-8")
            rows.append(
                _manifest_row(
                    status_type="other_status",
                    raw_path="_report/raw/2026/2026-07-08/kind/other_status.xls",
                )
            )
            _write_csv(manifest, rows)

            checks, summary = validate_manifest(
                manifest_path=manifest,
                policy_path=policy,
                market_data_path=market,
                required_status_types=("managed_issue", "trading_halt"),
                repo_root=root,
            )

        self.assertEqual(summary["overall_status"], "pass")
        self.assertEqual(summary["missing_coverage_status_types"], [])
        self.assertTrue(all(check.status == "pass" for check in checks))
        self.assertIn("outside required coverage scope", checks[-1].message)

    def test_fails_when_raw_path_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.yaml"
            manifest = root / "manifest.csv"
            _write_policy(policy)
            _write_csv(manifest, [_manifest_row()])

            checks, summary = validate_manifest(
                manifest_path=manifest,
                policy_path=policy,
                market_start="2025-01-02",
                market_end="2025-01-03",
                required_status_types=("managed_issue",),
                repo_root=root,
            )

        self.assertEqual(summary["overall_status"], "fail")
        self.assertEqual(summary["row_failures"], 1)
        self.assertIn("raw_path does not exist", checks[0].message)

    def test_fails_when_source_url_does_not_match_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.yaml"
            manifest = root / "manifest.csv"
            raw = (
                root
                / "_report"
                / "raw"
                / "2026"
                / "2026-07-08"
                / "kind"
                / "status-source-probe"
                / "managed_issue.xls"
            )
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_text("fixture\n", encoding="utf-8")
            _write_policy(policy)
            _write_csv(manifest, [_manifest_row(source_url="https://example.invalid/managed")])

            checks, summary = validate_manifest(
                manifest_path=manifest,
                policy_path=policy,
                market_start="2025-01-02",
                market_end="2025-01-03",
                required_status_types=("managed_issue",),
                repo_root=root,
            )

        self.assertEqual(summary["overall_status"], "fail")
        self.assertIn("source_url does not match allowed source prefixes", checks[0].message)

    def test_fails_when_required_type_does_not_cover_market_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.yaml"
            manifest = root / "manifest.csv"
            raw = (
                root
                / "_report"
                / "raw"
                / "2026"
                / "2026-07-08"
                / "kind"
                / "status-source-probe"
                / "managed_issue.xls"
            )
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_text("fixture\n", encoding="utf-8")
            _write_policy(policy)
            _write_csv(manifest, [_manifest_row(coverage_start="2025-01-03", coverage_end="2025-01-03")])

            _checks, summary = validate_manifest(
                manifest_path=manifest,
                policy_path=policy,
                market_start="2025-01-02",
                market_end="2025-01-03",
                required_status_types=("managed_issue",),
                repo_root=root,
            )

        self.assertEqual(summary["overall_status"], "fail")
        self.assertEqual(summary["missing_coverage_status_types"], ["managed_issue"])

    def test_cli_writes_lf_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.yaml"
            manifest = root / "manifest.csv"
            report = root / "manifest-validate.md"
            rows_output = root / "manifest-validate.rows.csv"
            raw = (
                root
                / "_report"
                / "raw"
                / "2026"
                / "2026-07-08"
                / "kind"
                / "status-source-probe"
                / "managed_issue.xls"
            )
            raw.parent.mkdir(parents=True, exist_ok=True)
            raw.write_text("fixture\n", encoding="utf-8")
            _write_policy(policy)
            _write_csv(manifest, [_manifest_row()])

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_source_manifest_validate.py",
                    "--manifest",
                    str(manifest),
                    "--policy",
                    str(policy),
                    "--market-start",
                    "2025-01-02",
                    "--market-end",
                    "2025-01-03",
                    "--required-status-types",
                    "managed_issue",
                    "--repo-root",
                    str(root),
                    "--rows-output",
                    str(rows_output),
                    "--report-output",
                    str(report),
                ],
            ):
                self.assertEqual(main(), 0)

            report_text = report.read_text(encoding="utf-8")
            report_bytes = report.read_bytes()
            rows_bytes = rows_output.read_bytes()
            with rows_output.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))

        self.assertIn("- Overall status: `pass`", report_text)
        self.assertIn("| Manifest rows | 1 |", report_text)
        self.assertIn("- " + f"[[{rows_output.as_posix()}|{rows_output.as_posix()}]]", report_text)
        self.assertEqual(rows[0]["status"], "pass")
        self.assertEqual(rows[0]["source_url"], "https://kind.krx.co.kr/example")
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertNotIn(b"\r\n", rows_bytes)


if __name__ == "__main__":
    unittest.main()
