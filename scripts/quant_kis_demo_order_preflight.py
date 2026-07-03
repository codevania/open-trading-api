"""Validate KIS demo order intents before any API execution.

This script does not call KIS and cannot place orders. It is a guardrail layer
for future demo trading wrappers.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REQUIRED_COLUMNS = (
    "env_dv",
    "dry_run",
    "order_side",
    "code",
    "quantity",
    "limit_price_krw",
    "order_type",
    "source_strategy",
)
VALIDATION_COLUMNS = REQUIRED_COLUMNS + (
    "order_value_krw",
    "valid",
    "errors",
)
CODE_PATTERN = re.compile(r"^[0-9A-Za-z]{5,12}$")


@dataclass(frozen=True)
class PreflightResult:
    row_number: int
    row: dict[str, str]
    errors: tuple[str, ...]
    order_value_krw: int | None

    @property
    def valid(self) -> bool:
        return not self.errors


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"missing order intent CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    return fieldnames, rows


def _parse_positive_int(value: str, column: str) -> tuple[int | None, str | None]:
    try:
        parsed = int(value)
    except ValueError:
        return None, f"{column} must be an integer"
    if parsed <= 0:
        return None, f"{column} must be positive"
    return parsed, None


def _validate_row(row: dict[str, str], max_order_value_krw: int, max_quantity: int) -> tuple[tuple[str, ...], int | None]:
    errors: list[str] = []
    if row.get("env_dv") != "demo":
        errors.append("env_dv must be demo")
    if row.get("dry_run", "").lower() != "true":
        errors.append("dry_run must be true")
    if row.get("order_side") not in {"buy", "sell"}:
        errors.append("order_side must be buy or sell")
    if row.get("order_type") != "limit":
        errors.append("order_type must be limit")
    if not CODE_PATTERN.fullmatch(row.get("code", "")):
        errors.append("code must preserve a KRX short code")
    if not row.get("source_strategy"):
        errors.append("source_strategy is required")

    quantity, quantity_error = _parse_positive_int(row.get("quantity", ""), "quantity")
    if quantity_error:
        errors.append(quantity_error)
    elif quantity is not None and quantity > max_quantity:
        errors.append(f"quantity must be <= {max_quantity}")

    limit_price, price_error = _parse_positive_int(row.get("limit_price_krw", ""), "limit_price_krw")
    if price_error:
        errors.append(price_error)

    order_value = quantity * limit_price if quantity is not None and limit_price is not None else None
    if order_value is not None and order_value > max_order_value_krw:
        errors.append(f"order_value_krw must be <= {max_order_value_krw}")

    if row.get("order_side") == "sell":
        errors.append("sell intents require a separate demo position check")

    return tuple(errors), order_value


def validate_order_intents(
    intents_path: Path,
    max_order_value_krw: int = 100_000,
    max_quantity: int = 1,
) -> tuple[list[PreflightResult], dict[str, Any]]:
    if max_order_value_krw <= 0:
        raise ValueError("max_order_value_krw must be positive")
    if max_quantity <= 0:
        raise ValueError("max_quantity must be positive")
    fieldnames, rows = _read_csv(intents_path)
    missing = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    if missing:
        raise ValueError(f"order intent CSV missing required columns: {', '.join(missing)}")

    results: list[PreflightResult] = []
    error_counts: Counter[str] = Counter()
    side_counts: Counter[str] = Counter()
    for index, row in enumerate(rows, start=1):
        errors, order_value = _validate_row(row, max_order_value_krw, max_quantity)
        results.append(PreflightResult(index, row, errors, order_value))
        side_counts[row.get("order_side", "") or "missing"] += 1
        error_counts.update(errors)

    valid_rows = sum(1 for result in results if result.valid)
    summary = {
        "intents_path": intents_path,
        "input_rows": len(results),
        "valid_rows": valid_rows,
        "invalid_rows": len(results) - valid_rows,
        "max_order_value_krw": max_order_value_krw,
        "max_quantity": max_quantity,
        "by_order_side": dict(sorted(side_counts.items())),
        "by_error": dict(sorted(error_counts.items())),
    }
    return results, summary


def _write_rows(path: Path, results: list[PreflightResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=VALIDATION_COLUMNS)
        writer.writeheader()
        for result in results:
            row = result.row
            writer.writerow(
                {
                    **{column: row.get(column, "") for column in REQUIRED_COLUMNS},
                    "order_value_krw": "" if result.order_value_krw is None else str(result.order_value_krw),
                    "valid": str(result.valid).lower(),
                    "errors": ";".join(result.errors),
                }
            )


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_report(summary: dict[str, Any], rows_output: Path | None) -> str:
    lines = [
        "# KIS Demo Order Preflight",
        "",
        f"- Order intents: {_wikilink(summary['intents_path'])}",
        "- Mode: `demo_preflight_only`",
        "- KIS API call: `false`",
        "- Backtest readiness: `hold`",
        "- Live trading readiness: `blocked`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Input rows | {summary['input_rows']} |",
        f"| Valid rows | {summary['valid_rows']} |",
        f"| Invalid rows | {summary['invalid_rows']} |",
        f"| Max order value KRW | {summary['max_order_value_krw']} |",
        f"| Max quantity | {summary['max_quantity']} |",
        "",
    ]
    if rows_output:
        lines.extend(["## Row Output", "", f"- {_wikilink(rows_output)}", ""])

    lines.extend(["## Order Side Counts", "", "| Side | Rows |", "| --- | ---: |"])
    for side, count in summary["by_order_side"].items():
        lines.append(f"| `{side}` | {count} |")
    if not summary["by_order_side"]:
        lines.append("| `none` | 0 |")

    lines.extend(["", "## Error Counts", "", "| Error | Rows |", "| --- | ---: |"])
    for error, count in summary["by_error"].items():
        lines.append(f"| `{error}` | {count} |")
    if not summary["by_error"]:
        lines.append("| `none` | 0 |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This script never places orders.",
            "- Only `env_dv=demo`, `dry_run=true`, `order_type=limit`, and `quantity <= 1` pass by default.",
            "- Sell intents stay invalid until a separate demo position check exists.",
            "- A future executor must still perform KIS `find_api_detail`, buying-power checks, position checks, order confirmation, and kill-switch checks before any demo API call.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate KIS demo order intents before any API execution.")
    parser.add_argument("--intents", required=True, type=Path)
    parser.add_argument("--rows-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--max-order-value-krw", default=100_000, type=int)
    parser.add_argument("--max-quantity", default=1, type=int)
    args = parser.parse_args()

    try:
        results, summary = validate_order_intents(args.intents, args.max_order_value_krw, args.max_quantity)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    if args.rows_output:
        _write_rows(args.rows_output, results)
    report = _render_report(summary, args.rows_output)
    if args.report_output:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0 if summary["invalid_rows"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
