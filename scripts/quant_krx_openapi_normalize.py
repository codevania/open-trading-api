"""Normalize saved KRX OpenAPI raw JSON into stable CSV schemas.

This script reads already-saved KRX OpenAPI raw files. It does not call KRX and
does not create a complete Point-in-Time Universe. The output is normalized
market-data input for parser development and future Backtest plumbing.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


BAS_DD_RE = re.compile(r"^\d{8}$")

STOCK_DAILY_SERVICES = {"kospi_stock_daily", "kosdaq_stock_daily"}
ISSUE_BASE_SERVICES = {"kospi_issue_base", "kosdaq_issue_base"}
INDEX_DAILY_SERVICES = {"kospi_index_daily", "kosdaq_index_daily"}

STOCK_DAILY_FIELDS = (
    "date",
    "code",
    "name",
    "market",
    "section",
    "close",
    "change",
    "return_pct",
    "open",
    "high",
    "low",
    "volume",
    "trading_value_krw",
    "market_cap_krw",
    "listed_shares",
    "source_service",
    "source_path",
)
ISSUE_BASE_FIELDS = (
    "date",
    "standard_code",
    "code",
    "name",
    "short_name",
    "english_name",
    "listing_date",
    "market",
    "security_group",
    "section",
    "stock_certificate_type",
    "par_value_krw",
    "listed_shares",
    "source_service",
    "source_path",
)
INDEX_DAILY_FIELDS = (
    "date",
    "index_class",
    "index_name",
    "close",
    "change",
    "return_pct",
    "open",
    "high",
    "low",
    "volume",
    "trading_value_krw",
    "market_cap_krw",
    "source_service",
    "source_path",
)


@dataclass(frozen=True)
class NormalizedTable:
    name: str
    rows: list[dict[str, str]]
    fieldnames: tuple[str, ...]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _extract_rows(path: Path) -> list[dict[str, Any]]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    rows = payload.get("OutBlock_1")
    if not isinstance(rows, list):
        raise ValueError(f"{path}: missing list field OutBlock_1")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"{path}: OutBlock_1[{index}] is not an object")
    return rows


def _service_id_from_path(path: Path) -> str:
    name = path.name
    if not name.endswith(".raw.json"):
        raise ValueError(f"{path}: expected file name ending in .raw.json")
    stem = name[: -len(".raw.json")]
    for suffix in re.findall(r"_\d{8}$", stem):
        return stem[: -len(suffix)]
    raise ValueError(f"{path}: expected service_id_YYYYMMDD.raw.json")


def _source_bas_dd_from_path(path: Path) -> str:
    match = re.search(r"_(\d{8})\.raw\.json$", path.name)
    if not match:
        raise ValueError(f"{path}: expected YYYYMMDD in file name")
    return match.group(1)


def _compact(value: Any) -> str:
    if value is None:
        return ""
    return str(value).replace(",", "").strip()


def _date_yyyy_mm_dd(value: Any) -> str:
    text = _compact(value)
    if not BAS_DD_RE.match(text):
        return text
    return f"{text[:4]}-{text[4:6]}-{text[6:]}"


def _normalize_code(value: Any) -> str:
    return _compact(value).upper()


def _normalize_stock_daily_row(row: dict[str, Any], source_service: str, source_path: Path) -> dict[str, str]:
    return {
        "date": _date_yyyy_mm_dd(row.get("BAS_DD")),
        "code": _normalize_code(row.get("ISU_CD")),
        "name": _compact(row.get("ISU_NM")),
        "market": _compact(row.get("MKT_NM")),
        "section": _compact(row.get("SECT_TP_NM")),
        "close": _compact(row.get("TDD_CLSPRC")),
        "change": _compact(row.get("CMPPREVDD_PRC")),
        "return_pct": _compact(row.get("FLUC_RT")),
        "open": _compact(row.get("TDD_OPNPRC")),
        "high": _compact(row.get("TDD_HGPRC")),
        "low": _compact(row.get("TDD_LWPRC")),
        "volume": _compact(row.get("ACC_TRDVOL")),
        "trading_value_krw": _compact(row.get("ACC_TRDVAL")),
        "market_cap_krw": _compact(row.get("MKTCAP")),
        "listed_shares": _compact(row.get("LIST_SHRS")),
        "source_service": source_service,
        "source_path": source_path.as_posix(),
    }


def _normalize_issue_base_row(row: dict[str, Any], source_service: str, source_path: Path, bas_dd: str) -> dict[str, str]:
    return {
        "date": _date_yyyy_mm_dd(bas_dd),
        "standard_code": _normalize_code(row.get("ISU_CD")),
        "code": _normalize_code(row.get("ISU_SRT_CD")),
        "name": _compact(row.get("ISU_NM")),
        "short_name": _compact(row.get("ISU_ABBRV")),
        "english_name": _compact(row.get("ISU_ENG_NM")),
        "listing_date": _date_yyyy_mm_dd(row.get("LIST_DD")),
        "market": _compact(row.get("MKT_TP_NM")),
        "security_group": _compact(row.get("SECUGRP_NM")),
        "section": _compact(row.get("SECT_TP_NM")),
        "stock_certificate_type": _compact(row.get("KIND_STKCERT_TP_NM")),
        "par_value_krw": _compact(row.get("PARVAL")),
        "listed_shares": _compact(row.get("LIST_SHRS")),
        "source_service": source_service,
        "source_path": source_path.as_posix(),
    }


def _normalize_index_daily_row(row: dict[str, Any], source_service: str, source_path: Path) -> dict[str, str]:
    return {
        "date": _date_yyyy_mm_dd(row.get("BAS_DD")),
        "index_class": _compact(row.get("IDX_CLSS")),
        "index_name": _compact(row.get("IDX_NM")),
        "close": _compact(row.get("CLSPRC_IDX")),
        "change": _compact(row.get("CMPPREVDD_IDX")),
        "return_pct": _compact(row.get("FLUC_RT")),
        "open": _compact(row.get("OPNPRC_IDX")),
        "high": _compact(row.get("HGPRC_IDX")),
        "low": _compact(row.get("LWPRC_IDX")),
        "volume": _compact(row.get("ACC_TRDVOL")),
        "trading_value_krw": _compact(row.get("ACC_TRDVAL")),
        "market_cap_krw": _compact(row.get("MKTCAP")),
        "source_service": source_service,
        "source_path": source_path.as_posix(),
    }


def _validate_required(row: dict[str, str], required: tuple[str, ...], source_path: Path) -> None:
    missing = [field for field in required if not row.get(field)]
    if missing:
        raise ValueError(f"{source_path}: normalized row missing required fields: {', '.join(missing)}")


def _sort_rows(rows: list[dict[str, str]], key: Callable[[dict[str, str]], tuple[str, ...]]) -> list[dict[str, str]]:
    return sorted(rows, key=key)


def normalize_raw_files(raw_files: list[Path]) -> dict[str, NormalizedTable]:
    stock_rows: list[dict[str, str]] = []
    issue_rows: list[dict[str, str]] = []
    index_rows: list[dict[str, str]] = []

    for raw_file in sorted(raw_files):
        service_id = _service_id_from_path(raw_file)
        bas_dd = _source_bas_dd_from_path(raw_file)
        rows = _extract_rows(raw_file)
        if service_id in STOCK_DAILY_SERVICES:
            for raw_row in rows:
                row = _normalize_stock_daily_row(raw_row, service_id, raw_file)
                _validate_required(row, ("date", "code", "name", "market"), raw_file)
                stock_rows.append(row)
        elif service_id in ISSUE_BASE_SERVICES:
            for raw_row in rows:
                row = _normalize_issue_base_row(raw_row, service_id, raw_file, bas_dd)
                _validate_required(row, ("date", "standard_code", "code", "name", "market", "listing_date"), raw_file)
                issue_rows.append(row)
        elif service_id in INDEX_DAILY_SERVICES:
            for raw_row in rows:
                row = _normalize_index_daily_row(raw_row, service_id, raw_file)
                _validate_required(row, ("date", "index_class", "index_name"), raw_file)
                index_rows.append(row)
        else:
            raise ValueError(f"{raw_file}: unsupported service id: {service_id}")

    return {
        "stock_daily": NormalizedTable(
            "stock_daily",
            _sort_rows(stock_rows, lambda row: (row["date"], row["market"], row["code"])),
            STOCK_DAILY_FIELDS,
        ),
        "issue_base": NormalizedTable(
            "issue_base",
            _sort_rows(issue_rows, lambda row: (row["date"], row["market"], row["code"])),
            ISSUE_BASE_FIELDS,
        ),
        "index_daily": NormalizedTable(
            "index_daily",
            _sort_rows(index_rows, lambda row: (row["date"], row["index_class"], row["index_name"])),
            INDEX_DAILY_FIELDS,
        ),
    }


def _discover_raw_files(raw_dir: Path, bas_dd: str | None, start_bas_dd: str | None, end_bas_dd: str | None) -> list[Path]:
    if not raw_dir.exists():
        raise ValueError(f"raw dir not found: {raw_dir}")
    candidates = sorted(raw_dir.glob("*.raw.json"))
    if bas_dd:
        candidates = [path for path in candidates if path.name.endswith(f"_{bas_dd}.raw.json")]
    if start_bas_dd:
        candidates = [path for path in candidates if _source_bas_dd_from_path(path) >= start_bas_dd]
    if end_bas_dd:
        candidates = [path for path in candidates if _source_bas_dd_from_path(path) <= end_bas_dd]
    return [path for path in candidates if not path.name.endswith(".meta.json")]


def _write_csv(table: NormalizedTable, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=table.fieldnames)
        writer.writeheader()
        for row in table.rows:
            writer.writerow(row)


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_markdown(tables: dict[str, NormalizedTable], raw_files: list[Path], output_dir: Path | None) -> str:
    lines = [
        "# KRX OpenAPI Normalize Result",
        "",
        "- Source: saved KRX OpenAPI raw JSON",
        "- Interpretation: `parser_normalization_smoke`, not a `Point-in-Time Universe` or `Backtest` result",
        "- Bias Control judgment: `hold`",
        "",
        "## Inputs",
        "",
    ]
    for raw_file in raw_files:
        lines.append(f"- {_wikilink(raw_file)}")

    lines.extend(
        [
            "",
            "## Output Tables",
            "",
            "| Table | Rows | Output |",
            "| --- | ---: | --- |",
        ]
    )
    for table_name in ("stock_daily", "issue_base", "index_daily"):
        table = tables[table_name]
        output = "" if output_dir is None else _wikilink(output_dir / f"{table_name}.csv")
        lines.append(f"| `{table_name}` | {len(table.rows)} | {output} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- KRX raw fields are normalized into stable local column names but not yet joined into a historical Universe.",
            "- Stock and issue rows preserve KRX short codes exactly, including leading zeros and any future alphanumeric short codes.",
            "- Management designation, trading halt, market alert, and delisting event replay are not covered by these six core APIs.",
            "- Backtest readiness remains `hold` until `Point-in-Time` status replay and historical coverage are validated.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize saved KRX OpenAPI raw JSON into CSV tables.")
    parser.add_argument("--raw-dir", required=True, type=Path)
    parser.add_argument("--bas-dd", help="Optional YYYYMMDD filter.")
    parser.add_argument("--start-bas-dd", help="Optional inclusive YYYYMMDD start filter.")
    parser.add_argument("--end-bas-dd", help="Optional inclusive YYYYMMDD end filter.")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    if args.bas_dd and not BAS_DD_RE.match(args.bas_dd):
        raise SystemExit("--bas-dd must be YYYYMMDD")
    if args.start_bas_dd and not BAS_DD_RE.match(args.start_bas_dd):
        raise SystemExit("--start-bas-dd must be YYYYMMDD")
    if args.end_bas_dd and not BAS_DD_RE.match(args.end_bas_dd):
        raise SystemExit("--end-bas-dd must be YYYYMMDD")
    if args.start_bas_dd and args.end_bas_dd and args.start_bas_dd > args.end_bas_dd:
        raise SystemExit("--start-bas-dd must be on or before --end-bas-dd")

    try:
        raw_files = _discover_raw_files(args.raw_dir, args.bas_dd, args.start_bas_dd, args.end_bas_dd)
        if not raw_files:
            raise ValueError(f"no KRX OpenAPI raw files found under: {args.raw_dir}")
        tables = normalize_raw_files(raw_files)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.output_dir:
        for table in tables.values():
            _write_csv(table, args.output_dir / f"{table.name}.csv")

    report = _render_markdown(tables, raw_files, args.output_dir)
    if args.report_output:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
