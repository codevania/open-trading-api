"""Probe a KRX OpenAPI endpoint and save the raw response.

This script is intentionally generic because KRX OpenAPI service URLs are
issued per API service/spec page. It keeps the authentication key out of
tracked files and passes it only through the required AUTH_KEY request header.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests


KST = ZoneInfo("Asia/Seoul")


def _now_kst() -> str:
    return datetime.now(KST).replace(microsecond=0).isoformat()


def _load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"{path}:{line_no}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"{path}:{line_no}: empty key")
        values[key] = value.strip().strip('"').strip("'")
    return values


def _resolve_auth_key(env_file: Path) -> str:
    file_values = _load_env_file(env_file)
    auth_key = os.environ.get("KRX_AUTH_KEY") or os.environ.get("AUTH_KEY") or file_values.get("KRX_AUTH_KEY") or file_values.get("AUTH_KEY")
    if not auth_key:
        raise ValueError(
            "KRX OpenAPI key is missing. Set KRX_AUTH_KEY in .env.krx or the process environment."
        )
    return auth_key


def _parse_param(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise ValueError(f"parameter must be KEY=VALUE, got {value!r}")
    key, param_value = value.split("=", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"parameter key is empty in {value!r}")
    return key, param_value.strip()


def _parse_params(values: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    for value in values:
        key, param_value = _parse_param(value)
        params[key] = param_value
    return params


def _redacted_request(url: str, params: dict[str, str]) -> dict[str, Any]:
    return {
        "method": "GET",
        "url": url,
        "headers": {"AUTH_KEY": "***"},
        "params": params,
    }


def _write_metadata(path: Path, metadata: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _save_response(output: Path, content: bytes) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Call one KRX OpenAPI endpoint with AUTH_KEY and save the raw response.")
    parser.add_argument("--url", required=True, help="Full KRX OpenAPI service URL from the KRX spec/sample page.")
    parser.add_argument("--param", action="append", default=[], help="Query parameter as KEY=VALUE. May be repeated.")
    parser.add_argument("--env-file", type=Path, default=Path(".env.krx"))
    parser.add_argument("--output", type=Path, help="Raw response output path. Required unless --dry-run is set.")
    parser.add_argument("--metadata-output", type=Path, help="Optional metadata JSON output path.")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--dry-run", action="store_true", help="Print the redacted request and exit without network access.")
    args = parser.parse_args()

    params = _parse_params(args.param)
    redacted = _redacted_request(args.url, params)

    if args.dry_run:
        print(json.dumps(redacted, ensure_ascii=False, indent=2))
        return 0

    if args.output is None:
        raise SystemExit("--output is required unless --dry-run is set")

    auth_key = _resolve_auth_key(args.env_file)
    response = requests.get(
        args.url,
        params=params,
        headers={"AUTH_KEY": auth_key},
        timeout=args.timeout,
    )

    _save_response(args.output, response.content)
    metadata_output = args.metadata_output or args.output.with_name(f"{args.output.name}.meta.json")
    _write_metadata(
        metadata_output,
        {
            "captured_at_kst": _now_kst(),
            "request": redacted,
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "raw_output": args.output.as_posix(),
        },
    )
    response.raise_for_status()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
