"""Validate saved KIS daily raw files for Quant smoke tests.

This script does not fetch market data and does not run a performance Backtest.
It reads already-saved raw JSON, validates the daily OHLCV shape, and emits a
Signal Candidate summary for Data Pipeline Smoke Test use only.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = ("stck_bsop_date", "stck_clpr", "stck_oprc", "stck_hgpr", "stck_lwpr", "acml_vol")


@dataclass
class SmokeResult:
    symbol: str
    raw_path: Path
    status: str
    rows: int
    latest_date: str | None
    latest_close: float | None
    roc_pct: float | None
    avg_trading_value_20d_krw: float | None
    message: str


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _unwrap_payload(payload: Any) -> Any:
    if isinstance(payload, dict) and isinstance(payload.get("data"), str):
        return json.loads(payload["data"])
    if isinstance(payload, dict) and isinstance(payload.get("data"), dict):
        return payload["data"]
    return payload


def _extract_rows(payload: Any) -> list[dict[str, Any]]:
    payload = _unwrap_payload(payload)
    if isinstance(payload, dict) and isinstance(payload.get("output2"), list):
        return payload["output2"]
    if isinstance(payload, dict) and isinstance(payload.get("latest_rows"), list):
        return payload["latest_rows"]
    if isinstance(payload, list):
        return payload
    return []


def _as_float(value: Any) -> float:
    if value is None:
        raise ValueError("missing numeric value")
    return float(str(value).replace(",", "").strip())


def _symbol_from_path(path: Path) -> str:
    name = path.name
    for suffix in (".daily.raw.json", ".raw.json", ".json"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    if name == "inquire_daily_itemchartprice":
        return path.parent.name
    return name


def validate_file(path: Path, lookback: int, threshold: float) -> SmokeResult:
    symbol = _symbol_from_path(path)
    payload = _load_json(path)
    rows = _extract_rows(payload)
    if not rows:
        return SmokeResult(symbol, path, "data-insufficient", 0, None, None, None, None, "no daily rows found")

    missing = sorted({field for row in rows for field in REQUIRED_FIELDS if field not in row})
    if missing:
        return SmokeResult(
            symbol,
            path,
            "data-insufficient",
            len(rows),
            None,
            None,
            None,
            None,
            f"missing required fields: {', '.join(missing)}",
        )

    try:
        ordered = sorted(rows, key=lambda row: str(row["stck_bsop_date"]))
        closes = [_as_float(row["stck_clpr"]) for row in ordered]
        volumes = [_as_float(row["acml_vol"]) for row in ordered]
        trading_values = [
            _as_float(row["acml_tr_pbmn"]) if row.get("acml_tr_pbmn") not in (None, "") else None
            for row in ordered
        ]
    except ValueError as exc:
        return SmokeResult(symbol, path, "data-insufficient", len(rows), None, None, None, None, str(exc))

    latest = ordered[-1]
    latest_date = str(latest["stck_bsop_date"])
    latest_close = closes[-1]

    if len(ordered) <= lookback:
        return SmokeResult(
            symbol,
            path,
            "data-insufficient",
            len(ordered),
            latest_date,
            latest_close,
            None,
            None,
            f"need at least {lookback + 1} rows for {lookback}-day ROC",
        )

    base_close = closes[-lookback - 1]
    if base_close <= 0:
        return SmokeResult(
            symbol,
            path,
            "data-insufficient",
            len(ordered),
            latest_date,
            latest_close,
            None,
            None,
            "base close is non-positive",
        )

    roc_pct = (latest_close / base_close - 1.0) * 100.0
    if roc_pct > threshold:
        status = "BUY candidate"
    elif roc_pct < 0:
        status = "SELL candidate"
    else:
        status = "HOLD"

    avg_trading_value = None
    recent_values = [value for value in trading_values[-20:] if value is not None]
    if recent_values:
        avg_trading_value = sum(recent_values) / len(recent_values)

    return SmokeResult(
        symbol,
        path,
        status,
        len(ordered),
        latest_date,
        latest_close,
        roc_pct,
        avg_trading_value,
        "ok",
    )


def _find_raw_files(raw_dir: Path) -> list[Path]:
    candidates = sorted(raw_dir.glob("*.daily.raw.json"))
    if candidates:
        return candidates
    return sorted(raw_dir.glob("**/inquire_daily_itemchartprice.json"))


def _render_markdown(results: list[SmokeResult], lookback: int, threshold: float, raw_dir: Path) -> str:
    lines = [
        "# Data Pipeline Smoke Test Result",
        "",
        f"- Source raw directory: `{raw_dir.as_posix()}`",
        "- Validator: `scripts/quant_smoke_validate.py`",
        "- Universe definition mode: `manual_smoke_test`",
        "- Interpretation: `Data Pipeline Smoke Test - Not Quant Validation`",
        "- Bias Control judgment: `hold`",
        f"- Lookback: `{lookback}`",
        f"- Threshold: `{threshold}`",
        "- Cost model reference: `_report/quant/research/2026-06-08-transaction-cost-slippage-assumptions.md`",
        "",
        "| Symbol | Status | Rows | Latest Date | Latest Close | ROC % | Avg Trading Value 20D KRW | Message |",
        "| --- | --- | ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for result in results:
        roc = "" if result.roc_pct is None else f"{result.roc_pct:.4f}"
        avg_value = "" if result.avg_trading_value_20d_krw is None else f"{result.avg_trading_value_20d_krw:.0f}"
        latest_close = "" if result.latest_close is None else f"{result.latest_close:.0f}"
        latest_date = result.latest_date or ""
        lines.append(
            f"| `{result.symbol}` | {result.status} | {result.rows} | {latest_date} | "
            f"{latest_close} | {roc} | {avg_value} | {result.message} |"
        )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- Manual symbol files are not a Quant Universe.",
            "- This output must not be used as Strategy performance evidence.",
            "- Point-in-Time Investable Universe remains required before Backtest interpretation.",
            f"- Files with fewer than {lookback + 1} daily rows only prove the parser and `data-insufficient` path.",
            "- Full smoke test acceptance remains blocked until raw files with enough daily rows are saved under `_report/raw/YYYY/YYYY-MM-DD/quant/smoke-test/`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Quant smoke test raw KIS daily files.")
    parser.add_argument("--raw-dir", required=True, type=Path)
    parser.add_argument("--lookback", default=20, type=int)
    parser.add_argument("--threshold", default=0.0, type=float)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    raw_dir = args.raw_dir
    if not raw_dir.exists():
        raise SystemExit(f"raw dir not found: {raw_dir}")

    raw_files = _find_raw_files(raw_dir)
    if not raw_files:
        raise SystemExit(f"no raw daily files found under: {raw_dir}")

    results = [validate_file(path, args.lookback, args.threshold) for path in raw_files]
    report = _render_markdown(results, args.lookback, args.threshold, raw_dir)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
