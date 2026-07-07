"""Check local KIS demo account configuration without exposing secrets.

This script is intentionally local and read-only. It does not call KIS, does not
request tokens, and does not print credential or account values.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from quant_io import write_text_lf


DEFAULT_ENV_CONFIG = Path("MCP/Kis Trading MCP/.env.kis")
DEFAULT_YAML_CONFIG = Path("kis_devlp.yaml")
DEFAULT_DOMESTIC_STOCK_CONFIG = Path("MCP/Kis Trading MCP/configs/domestic_stock.json")

REQUIRED_API_METHODS = (
    "inquire_psbl_order",
    "inquire_psbl_sell",
    "inquire_balance",
    "order_cash",
    "order_rvsecncl",
)

FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "demo_app_key": ("KIS_PAPER_APP_KEY", "paper_app"),
    "demo_app_secret": ("KIS_PAPER_APP_SECRET", "paper_sec"),
    "demo_stock_account": ("KIS_PAPER_STOCK", "my_paper_stock"),
    "account_product_code": ("KIS_PROD_TYPE", "my_prod"),
    "demo_rest_url": ("KIS_URL_REST_PAPER", "vps"),
}

REQUIRED_FIELDS = ("demo_app_key", "demo_app_secret", "demo_stock_account", "demo_rest_url")
PLACEHOLDER_RE = re.compile(
    r"(your_|example|sample|placeholder|todo|change_me|replace|발급받은|실제_|계좌번호)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class CheckResult:
    check: str
    status: str
    detail: str
    source_key: str | None = None


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return line[:index]
    return line


def _parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = _strip_comment(raw_line).strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def _flatten_yaml(value: Any, prefix: str = "") -> dict[str, str]:
    flattened: dict[str, str] = {}
    if isinstance(value, dict):
        for key, child in value.items():
            child_key = f"{prefix}.{key}" if prefix else str(key)
            flattened.update(_flatten_yaml(child, child_key))
    elif value is not None:
        flattened[prefix] = str(value)
        flattened[prefix.rsplit(".", 1)[-1]] = str(value)
    return flattened


def _read_config(path: Path) -> dict[str, str]:
    if not path.exists():
        raise ValueError(f"missing KIS config file: {path}")
    if path.name.startswith(".env") or path.suffix.lower() in {".env", ".kis"}:
        return _parse_env(path)
    parsed = yaml.safe_load(path.read_text(encoding="utf-8-sig")) or {}
    return _flatten_yaml(parsed)


def _selected_config_path(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit
    if DEFAULT_ENV_CONFIG.exists():
        return DEFAULT_ENV_CONFIG
    return DEFAULT_YAML_CONFIG


def _value_for(values: dict[str, str], logical_field: str) -> tuple[str | None, str | None]:
    for key in FIELD_ALIASES[logical_field]:
        value = values.get(key)
        if value is not None:
            return value.strip(), key
    return None, None


def _value_state(value: str) -> str:
    if not value.strip():
        return "empty"
    if PLACEHOLDER_RE.search(value):
        return "placeholder"
    return "configured"


def _validate_field(logical_field: str, value: str | None, source_key: str | None) -> CheckResult:
    if value is None:
        if logical_field == "account_product_code":
            return CheckResult(logical_field, "warn", "not configured; MCP default product code 01 would apply", None)
        return CheckResult(logical_field, "fail", "missing required demo field", None)

    value_state = _value_state(value)
    if value_state in {"empty", "placeholder"}:
        if logical_field == "demo_rest_url" and value_state == "empty":
            return CheckResult(logical_field, "warn", "not configured; KIS template default demo REST URL may apply", source_key)
        return CheckResult(logical_field, "fail", f"configured value is {value_state}", source_key)

    if logical_field in {"demo_app_key", "demo_app_secret"}:
        if len(value) < 10:
            return CheckResult(logical_field, "fail", "configured value is unexpectedly short", source_key)
        return CheckResult(logical_field, "pass", "present and non-placeholder", source_key)

    if logical_field == "demo_stock_account":
        if not re.fullmatch(r"\d{8}", value):
            return CheckResult(logical_field, "fail", "must be an 8-digit account number", source_key)
        return CheckResult(logical_field, "pass", "8-digit demo stock account present", source_key)

    if logical_field == "account_product_code":
        if not re.fullmatch(r"\d{2}", value):
            return CheckResult(logical_field, "fail", "must be a 2-digit account product code", source_key)
        if value != "01":
            return CheckResult(logical_field, "warn", "configured product code is not the domestic stock default 01", source_key)
        return CheckResult(logical_field, "pass", "domestic stock product code present", source_key)

    if logical_field == "demo_rest_url":
        if not value.startswith("https://"):
            return CheckResult(logical_field, "fail", "demo REST URL must start with https://", source_key)
        return CheckResult(logical_field, "pass", "demo REST URL present", source_key)

    raise ValueError(f"unknown logical field: {logical_field}")


def _validate_api_methods(domestic_stock_config: Path) -> list[CheckResult]:
    if not domestic_stock_config.exists():
        return [CheckResult("domestic_stock_config", "fail", "missing domestic stock MCP config", None)]
    try:
        payload = json.loads(domestic_stock_config.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [CheckResult("domestic_stock_config", "fail", f"invalid JSON: {exc}", None)]

    api_section = payload.get("apis")
    if not isinstance(api_section, dict):
        return [CheckResult("domestic_stock_config", "fail", "missing apis object", None)]

    results: list[CheckResult] = []
    for method in REQUIRED_API_METHODS:
        if method in api_section:
            results.append(CheckResult(f"api_method:{method}", "pass", "configured in domestic_stock.json", method))
        else:
            results.append(CheckResult(f"api_method:{method}", "fail", "missing from domestic_stock.json", method))
    return results


def run_preflight(config_path: Path | None = None, domestic_stock_config: Path = DEFAULT_DOMESTIC_STOCK_CONFIG) -> dict[str, Any]:
    selected_path = _selected_config_path(config_path)
    values = _read_config(selected_path)

    checks: list[CheckResult] = []
    for logical_field in FIELD_ALIASES:
        value, source_key = _value_for(values, logical_field)
        checks.append(_validate_field(logical_field, value, source_key))
    checks.extend(_validate_api_methods(domestic_stock_config))

    required_failures = [check for check in checks if check.status == "fail" and check.check in REQUIRED_FIELDS]
    api_failures = [check for check in checks if check.status == "fail" and check.check.startswith("api_method:")]
    status_counts = Counter(check.status for check in checks)
    return {
        "config_path": selected_path,
        "domestic_stock_config": domestic_stock_config,
        "checks": checks,
        "status_counts": dict(sorted(status_counts.items())),
        "ready_for_read_only_demo_account_calls": not required_failures and not api_failures,
        "required_failures": len(required_failures),
        "api_failures": len(api_failures),
    }


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def render_report(summary: dict[str, Any]) -> str:
    lines = [
        "# KIS Demo Account Preflight",
        "",
        f"- Config source: {_wikilink(summary['config_path'])}",
        f"- Domestic stock API config: {_wikilink(summary['domestic_stock_config'])}",
        "- Mode: `local_config_preflight_only`",
        "- KIS API call: `false`",
        "- Secrets printed: `false`",
        f"- Ready for read-only demo account calls: `{str(summary['ready_for_read_only_demo_account_calls']).lower()}`",
        "- Backtest readiness: `hold`",
        "- Live trading readiness: `blocked`",
        "",
        "## Status Counts",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status, count in summary["status_counts"].items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Checks", "", "| Check | Status | Source key | Detail |", "| --- | --- | --- | --- |"])
    for check in summary["checks"]:
        source_key = check.source_key or ""
        lines.append(f"| `{check.check}` | `{check.status}` | `{source_key}` | {check.detail} |")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- This report contains no credential or account values.",
            "- Passing this preflight does not authorize order execution.",
            "- The next safe API step is read-only demo `inquire_psbl_order`, `inquire_psbl_sell`, and balance/status checks.",
            "- A future order executor must still require explicit confirmation, kill switch, order status/cancel handling, and `env_dv=demo` hard gating.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local KIS demo account config without exposing secrets.")
    parser.add_argument("--config", type=Path, help="KIS config path. Defaults to MCP .env.kis, then kis_devlp.yaml.")
    parser.add_argument("--domestic-stock-config", default=DEFAULT_DOMESTIC_STOCK_CONFIG, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        summary = run_preflight(args.config, args.domestic_stock_config)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    report = render_report(summary)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0 if summary["ready_for_read_only_demo_account_calls"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
