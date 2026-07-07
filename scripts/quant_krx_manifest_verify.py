"""Verify KRX manual snapshot manifests for Quant Universe work.

This script does not download KRX data. It checks a manifest, verifies raw file
presence, SHA-256 hashes, and CSV headers when the manual files exist, then
emits a compact markdown status report.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from quant_io import write_text_lf


PLACEHOLDERS = ("TO_BE_FILLED", "TO_BE_VERIFIED", "YYYY", "pending")
CSV_ENCODINGS = ("utf-8-sig", "utf-8", "cp949", "euc-kr")


@dataclass
class DatasetCheck:
    dataset_id: str
    required: bool
    raw_path: str
    raw_exists: bool
    hash_status: str
    schema_status: str
    status: str
    message: str


def _is_placeholder(value: Any) -> bool:
    text = str(value or "").strip()
    if not text:
        return True
    return any(token in text for token in PLACEHOLDERS)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("manifest root must be a mapping")
    return payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv_header(path: Path) -> tuple[list[str], str]:
    last_error: Exception | None = None
    for encoding in CSV_ENCODINGS:
        try:
            with path.open("r", encoding=encoding, newline="") as handle:
                sample = handle.read(4096)
                handle.seek(0)
                try:
                    dialect = csv.Sniffer().sniff(sample)
                except csv.Error:
                    dialect = csv.excel
                reader = csv.reader(handle, dialect)
                header = next(reader)
                return [cell.strip() for cell in header], encoding
        except Exception as exc:  # pragma: no cover - used for fallback diagnostics
            last_error = exc
    raise ValueError(f"could not read CSV header: {last_error}")


def _check_dataset(dataset: dict[str, Any], repo_root: Path) -> DatasetCheck:
    dataset_id = str(dataset.get("id", "")).strip() or "unknown"
    required = bool(dataset.get("required", False))
    raw_path = str(dataset.get("raw_path", "")).strip()
    raw = repo_root / raw_path if raw_path else repo_root / "__missing_raw_path__"

    if not raw_path:
        return DatasetCheck(dataset_id, required, "", False, "missing", "missing", "fail", "raw_path is missing")

    if not raw.exists():
        status = "pending" if required else "optional-missing"
        message = "required raw file is missing" if required else "optional raw file is missing"
        return DatasetCheck(dataset_id, required, raw_path, False, "pending", "pending", status, message)

    expected_hash = str(dataset.get("sha256", "")).strip()
    actual_hash = _sha256(raw)
    if _is_placeholder(expected_hash):
        hash_status = "pending"
        hash_ok = False
    elif expected_hash.lower() == actual_hash.lower():
        hash_status = "ok"
        hash_ok = True
    else:
        hash_status = "mismatch"
        hash_ok = False

    expected_columns = [str(col).strip() for col in dataset.get("columns", []) or []]
    expected_columns = [col for col in expected_columns if col]
    if not expected_columns or any(_is_placeholder(col) for col in expected_columns):
        schema_status = "pending"
        schema_ok = False
    else:
        try:
            header, encoding = _read_csv_header(raw)
            schema_ok = header == expected_columns
            schema_status = "ok" if schema_ok else "mismatch"
            if not schema_ok:
                return DatasetCheck(
                    dataset_id,
                    required,
                    raw_path,
                    True,
                    hash_status,
                    schema_status,
                    "fail",
                    f"CSV header mismatch; detected encoding {encoding}",
                )
        except ValueError as exc:
            schema_status = "unreadable"
            schema_ok = False
            return DatasetCheck(dataset_id, required, raw_path, True, hash_status, schema_status, "fail", str(exc))

    if hash_ok and schema_ok:
        return DatasetCheck(dataset_id, required, raw_path, True, hash_status, schema_status, "pass", "ok")

    pending_bits = []
    if not hash_ok:
        pending_bits.append("sha256")
    if not schema_ok:
        pending_bits.append("schema")
    return DatasetCheck(
        dataset_id,
        required,
        raw_path,
        True,
        hash_status,
        schema_status,
        "pending",
        f"needs {' and '.join(pending_bits)} verification",
    )


def _overall_status(results: list[DatasetCheck]) -> str:
    if any(result.status == "fail" for result in results):
        return "fail"
    if any(result.required and result.status != "pass" for result in results):
        return "pending"
    return "pass"


def _render_report(manifest_path: Path, manifest: dict[str, Any], results: list[DatasetCheck]) -> str:
    snapshot = manifest.get("snapshot", {}) or {}
    status = _overall_status(results)
    lines = [
        "# KRX Manual Snapshot Verify Result",
        "",
        f"- Manifest: `{manifest_path.as_posix()}`",
        f"- As-of date: `{snapshot.get('as_of_date', '')}`",
        f"- Source mode: `{snapshot.get('source_mode', '')}`",
        f"- Overall status: `{status}`",
        "- Interpretation: `manual snapshot verification only`, `not Backtest ready`",
        "- Bias Control judgment: `hold`",
        "",
        "| Dataset | Required | Raw Exists | Hash | Schema | Status | Message |",
        "| --- | ---: | ---: | --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            f"| `{result.dataset_id}` | {str(result.required).lower()} | {str(result.raw_exists).lower()} | "
            f"{result.hash_status} | {result.schema_status} | {result.status} | {result.message} |"
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This verifier does not download KRX files.",
            "- `pass` only means the manual snapshot files match the manifest hash and schema.",
            "- A single manual snapshot does not create a reproducible `Point-in-Time` Universe.",
            "- Keep Strategy interpretation at `hold` until historical Point-in-Time snapshots and calendar audits exist.",
            "",
            "## Next Checks",
            "",
            "1. Download the required KRX files manually if status is `pending`.",
            "2. Fill `downloaded_at_kst`, `sha256`, and `columns` in the final raw-directory manifest.",
            "3. Re-run this verifier against `_report/raw/YYYY/YYYY-MM-DD/krx/universe/manifest.yaml`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a KRX manual snapshot manifest.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-pending", action="store_true")
    args = parser.parse_args()

    repo_root = Path.cwd()
    manifest_path = args.manifest
    manifest = _load_yaml(manifest_path)
    datasets = manifest.get("datasets", [])
    if not isinstance(datasets, list) or not datasets:
        raise SystemExit("manifest must contain a non-empty datasets list")

    results = [_check_dataset(dataset, repo_root) for dataset in datasets]
    report = _render_report(manifest_path, manifest, results)
    if args.output:
        write_text_lf(args.output, report)
    else:
        print(report, end="")

    status = _overall_status(results)
    if status == "pass" or (status == "pending" and args.allow_pending):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
