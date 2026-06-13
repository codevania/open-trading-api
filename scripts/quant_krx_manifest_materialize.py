"""Materialize a KRX manual snapshot manifest after raw CSV files exist.

This script does not download KRX data and does not parse an Investable
Universe. It fills manifest hash and CSV header metadata so the verifier can
check the manual snapshot without hand-editing every field.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

from quant_krx_manifest_verify import _is_placeholder, _load_yaml, _read_csv_header, _sha256


KST = ZoneInfo("Asia/Seoul")


def _now_kst() -> str:
    return datetime.now(KST).replace(microsecond=0).isoformat()


def _fill_dataset(dataset: dict[str, Any], repo_root: Path, downloaded_at_kst: str) -> tuple[dict[str, Any], bool]:
    filled = dict(dataset)
    dataset_id = str(filled.get("id", "")).strip() or "unknown"
    required = bool(filled.get("required", False))
    raw_path = str(filled.get("raw_path", "")).strip()
    raw = repo_root / raw_path if raw_path else repo_root / "__missing_raw_path__"

    if not raw_path:
        filled["status"] = "missing_raw_path"
        return filled, required

    if not raw.exists():
        filled["status"] = "pending_manual_download"
        filled["schema_verified_by_codex"] = False
        return filled, required

    file_format = str(filled.get("file_format", "")).strip().lower()
    if file_format and file_format != "csv":
        raise ValueError(f"{dataset_id}: only csv manifest materialization is supported, got {file_format!r}")

    header, encoding = _read_csv_header(raw)
    filled["downloaded_at_kst"] = downloaded_at_kst
    filled["sha256"] = _sha256(raw)
    filled["columns"] = header
    filled["schema_verified_by_codex"] = True
    filled["status"] = "materialized_from_raw"
    filled["detected_encoding"] = encoding
    return filled, False


def _materialize(manifest: dict[str, Any], repo_root: Path, downloaded_at_kst: str) -> tuple[dict[str, Any], bool]:
    datasets = manifest.get("datasets", [])
    if not isinstance(datasets, list) or not datasets:
        raise ValueError("manifest must contain a non-empty datasets list")

    pending_required = False
    filled = dict(manifest)
    filled_datasets = []
    for dataset in datasets:
        if not isinstance(dataset, dict):
            raise ValueError("each dataset must be a mapping")
        filled_dataset, is_pending_required = _fill_dataset(dataset, repo_root, downloaded_at_kst)
        pending_required = pending_required or is_pending_required
        filled_datasets.append(filled_dataset)

    snapshot = dict(filled.get("snapshot", {}) or {})
    snapshot["download_verified_by_codex"] = bool(snapshot.get("download_verified_by_codex", False))
    snapshot["status"] = "pending_manual_download" if pending_required else "raw_files_materialized"
    notes = list(snapshot.get("notes", []) or [])
    materialize_note = "Manifest hash and CSV header fields were materialized from local raw files by Codex."
    if materialize_note not in notes and not pending_required:
        notes.append(materialize_note)
    if pending_required:
        notes.append("Required raw files are still missing; this output is a pending preview only.")
    snapshot["notes"] = notes

    filled["snapshot"] = snapshot
    filled["datasets"] = filled_datasets
    return filled, pending_required


def _render_yaml(payload: dict[str, Any]) -> str:
    return yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=120)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill KRX manual snapshot manifest metadata from local raw CSV files.")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--downloaded-at-kst", default=_now_kst())
    parser.add_argument("--allow-pending", action="store_true")
    args = parser.parse_args()

    manifest = _load_yaml(args.manifest)
    materialized, pending_required = _materialize(manifest, Path.cwd(), args.downloaded_at_kst)
    output = _render_yaml(materialized)

    if pending_required and not args.allow_pending:
        raise SystemExit("required raw files are missing; use --allow-pending only for a preview")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    if pending_required:
        if args.allow_pending:
            return 0
        return 1

    if any(_is_placeholder(dataset.get("sha256")) for dataset in materialized["datasets"] if dataset.get("required")):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
