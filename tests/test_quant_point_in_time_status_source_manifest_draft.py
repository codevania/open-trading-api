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

from scripts.quant_point_in_time_status_source_manifest_draft import build_source_manifest_draft, main


LIFECYCLE_FIELDS = (
    "code",
    "market",
    "status_type",
    "lifecycle_gap_status",
    "active_like_rows",
    "release_like_rows",
    "first_active_event_date",
    "latest_active_event_date",
    "first_release_like_event_date",
    "latest_release_like_event_date",
    "market_rows",
    "market_start",
    "market_end",
    "event_sources",
    "raw_paths",
    "notes",
)


def _write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _write_policy(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                'version: "1.0"',
                "sources:",
                "  krx_data_marketplace:",
                "    display_name: KRX Data Marketplace",
                "    allowed_url_prefixes:",
                '      - "https://data.krx.co.kr/"',
                "    candidate_tables:",
                "      - Designated details of all issues",
                "      - Market alert issue",
                "      - Delisting",
                "  kind:",
                "    display_name: KIND",
                "    allowed_url_prefixes:",
                '      - "https://kind.krx.co.kr/"',
                "    candidate_tables:",
                "      - Managed issue event",
                "      - Trading halt or resumption disclosure",
                "      - Delisting disclosure",
                "  manual_snapshot:",
                "    display_name: Manual official snapshot",
                "    allowed_url_prefixes:",
                '      - "https://data.krx.co.kr/"',
                '      - "https://kind.krx.co.kr/"',
                "    candidate_tables:",
                "      - Manual official download",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _lifecycle_row(code: str, status_type: str, market: str = "KOSPI") -> dict[str, str]:
    return {
        "code": code,
        "market": market,
        "status_type": status_type,
        "lifecycle_gap_status": "missing_release_resume_evidence",
        "active_like_rows": "2",
        "release_like_rows": "0",
        "first_active_event_date": "2026-07-03",
        "latest_active_event_date": "2026-07-08",
        "first_release_like_event_date": "",
        "latest_release_like_event_date": "",
        "market_rows": "72",
        "market_start": "2025-01-02",
        "market_end": "2025-04-18",
        "event_sources": "kind",
        "raw_paths": "_report/raw/2026/2026-07-08/kind/status-source-probe/status.xls",
        "notes": "release_resume_collection_target",
    }


class QuantPointInTimeStatusSourceManifestDraftTest(unittest.TestCase):
    def test_builds_pending_rows_without_evidence_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.yaml"
            lifecycle = root / "lifecycle.csv"
            _write_policy(policy)
            _write_csv(
                lifecycle,
                LIFECYCLE_FIELDS,
                [
                    _lifecycle_row("000001", "managed_issue"),
                    _lifecycle_row("000002", "trading_halt", "KOSDAQ"),
                ],
            )

            rows, summary = build_source_manifest_draft(
                lifecycle_gaps_path=lifecycle,
                policy_path=policy,
                required_status_types=("managed_issue", "trading_halt", "delisting"),
            )

        self.assertEqual(summary["coverage_start"], "2025-01-02")
        self.assertEqual(summary["coverage_end"], "2025-04-18")
        self.assertEqual(summary["target_counts"]["managed_issue"], 1)
        self.assertEqual(summary["target_counts"]["delisting"], 0)
        self.assertTrue(all(row["draft_status"] == "pending_raw_evidence" for row in rows))
        self.assertTrue(all(row["source_url"] == "" for row in rows))
        self.assertTrue(all(row["raw_path"] == "" for row in rows))
        self.assertTrue(all(row["confidence"] == "" for row in rows))
        self.assertIn("kind", {row["source"] for row in rows if row["status_type"] == "trading_halt"})
        delisting_rows = [row for row in rows if row["status_type"] == "delisting"]
        self.assertTrue(delisting_rows)
        self.assertIn("required_manifest_coverage_no_lifecycle_gap_rows", delisting_rows[0]["notes"])

    def test_missing_required_lifecycle_column_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.yaml"
            lifecycle = root / "lifecycle.csv"
            _write_policy(policy)
            fields = tuple(field for field in LIFECYCLE_FIELDS if field != "market")
            row = {key: value for key, value in _lifecycle_row("000001", "managed_issue").items() if key in fields}
            _write_csv(lifecycle, fields, [row])

            with self.assertRaisesRegex(ValueError, "missing required columns: market"):
                build_source_manifest_draft(lifecycle_gaps_path=lifecycle, policy_path=policy)

    def test_cli_writes_lf_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            policy = root / "policy.yaml"
            lifecycle = root / "lifecycle.csv"
            output = root / "draft.rows.csv"
            report = root / "draft.md"
            _write_policy(policy)
            _write_csv(lifecycle, LIFECYCLE_FIELDS, [_lifecycle_row("000001", "managed_issue")])

            with patch(
                "sys.argv",
                [
                    "quant_point_in_time_status_source_manifest_draft.py",
                    "--lifecycle-gaps",
                    str(lifecycle),
                    "--policy",
                    str(policy),
                    "--required-status-types",
                    "managed_issue,delisting",
                    "--output",
                    str(output),
                    "--report-output",
                    str(report),
                ],
            ):
                self.assertEqual(main(), 0)

            report_text = report.read_text(encoding="utf-8")
            report_bytes = report.read_bytes()
            output_bytes = output.read_bytes()

        self.assertIn("- Draft status: `pending_raw_evidence`", report_text)
        self.assertNotIn(b"\r\n", report_bytes)
        self.assertNotIn(b"\r\n", output_bytes)


if __name__ == "__main__":
    unittest.main()
