"""Save captured KIS MCP JSON payloads into the Quant raw smoke-test layout.

The script does not call KIS and does not place orders. It accepts an already
captured JSON payload from a file or stdin, validates that it is JSON, writes it
to the canonical raw directory, and rewrites a lightweight manifest.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DAILY_API_TYPE = "inquire_daily_itemchartprice"


def _read_payload(input_path: str) -> Any:
    if input_path == "-":
        text = sys.stdin.read()
    else:
        text = Path(input_path).read_text(encoding="utf-8")
    return json.loads(text)


def _safe_token(value: str) -> str:
    token = re.sub(r"[^A-Za-z0-9_.-]+", "-", value.strip())
    return token.strip("-") or "unknown"


def _file_name(symbol: str, api_type: str) -> str:
    safe_symbol = _safe_token(symbol)
    safe_api = _safe_token(api_type)
    if api_type == DAILY_API_TYPE:
        return f"{safe_symbol}.daily.raw.json"
    return f"{safe_symbol}.{safe_api}.raw.json"


def _yaml_scalar(value: str | None) -> str:
    if value is None or value == "":
        return "null"
    return json.dumps(value, ensure_ascii=False)


def _write_manifest(raw_dir: Path, args: argparse.Namespace, output_path: Path, captured_at: str) -> None:
    files = sorted(raw_dir.glob("*.raw.json"))
    lines = [
        "schema_version: 1",
        "purpose: quant_data_pipeline_smoke_test",
        "source: manual_kis_mcp_capture",
        f"generated_at_utc: {_yaml_scalar(captured_at)}",
        f"raw_dir: {_yaml_scalar(raw_dir.as_posix())}",
        "latest_capture:",
        f"  symbol: {_yaml_scalar(args.symbol)}",
        f"  api_type: {_yaml_scalar(args.api_type)}",
        f"  env_dv: {_yaml_scalar(args.env_dv)}",
        f"  market: {_yaml_scalar(args.market)}",
        f"  start_date: {_yaml_scalar(args.start_date)}",
        f"  end_date: {_yaml_scalar(args.end_date)}",
        f"  period: {_yaml_scalar(args.period)}",
        f"  output_file: {_yaml_scalar(output_path.name)}",
        "files:",
    ]
    for path in files:
        lines.extend(
            [
                f"  - path: {_yaml_scalar(path.name)}",
                f"    bytes: {path.stat().st_size}",
            ]
        )
    (raw_dir / "manifest.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Save captured KIS MCP raw JSON for Quant smoke tests.")
    parser.add_argument("--input", required=True, help="JSON payload file path, or '-' for stdin.")
    parser.add_argument("--raw-dir", required=True, type=Path)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--api-type", default=DAILY_API_TYPE)
    parser.add_argument("--env-dv", default="real")
    parser.add_argument("--market", default="KRX")
    parser.add_argument("--start-date")
    parser.add_argument("--end-date")
    parser.add_argument("--period", default="D")
    args = parser.parse_args()

    payload = _read_payload(args.input)
    raw_dir = args.raw_dir
    raw_dir.mkdir(parents=True, exist_ok=True)

    output_path = raw_dir / _file_name(args.symbol, args.api_type)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    captured_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    _write_manifest(raw_dir, args, output_path, captured_at)
    print(output_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
