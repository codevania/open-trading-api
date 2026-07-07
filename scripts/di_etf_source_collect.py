"""Collect official ETF source pages listed in the DI candidate manifest."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests
import yaml


try:
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = timezone(timedelta(hours=9), "KST")

DEFAULT_CANDIDATE_FILE = Path("_report/di/candidates/core-satellite-candidates.yaml")
DEFAULT_RAW_ROOT = Path("_report/raw")
DEFAULT_SECTIONS = ("core_etfs", "korea_listed_etfs_to_verify", "satellite_etfs_to_verify")
DEFAULT_USER_AGENT = "open-trading-api-di-research/1.0 (personal source snapshot)"
SAFE_SYMBOL_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")
EMPTY_SOURCE_URL_TOKENS = {"", "null", "none", "todo", "verify"}


@dataclass(frozen=True)
class EtfSourceCandidate:
    section: str
    symbol: str
    name: str
    source_url: str


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected YAML object")
    return payload


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _safe_symbol(symbol: str) -> str:
    safe = SAFE_SYMBOL_PATTERN.sub("_", symbol.upper()).strip("._-")
    if not safe:
        raise ValueError("symbol resolves to an empty path segment")
    return safe


def _collection_root(raw_root: Path, run_date: str) -> Path:
    return raw_root / run_date[:4] / run_date / "di" / "etf-sources"


def _source_dir(raw_root: Path, run_date: str, symbol: str) -> Path:
    return _collection_root(raw_root, run_date) / _safe_symbol(symbol)


def iter_source_candidates(
    payload: dict[str, Any],
    *,
    sections: tuple[str, ...],
    symbols: tuple[str, ...],
) -> list[EtfSourceCandidate]:
    filters = {symbol.upper() for symbol in symbols}
    candidates: list[EtfSourceCandidate] = []
    for section in sections:
        for index, row in enumerate(_as_list(payload.get(section))):
            if not isinstance(row, dict):
                raise ValueError(f"{section}[{index}]: expected candidate object")
            symbol = _text(row.get("symbol")).upper()
            if not symbol:
                raise ValueError(f"{section}[{index}]: missing symbol")
            if filters and symbol not in filters:
                continue
            source_url = _text(row.get("source_url"))
            if source_url.lower() in EMPTY_SOURCE_URL_TOKENS:
                continue
            candidates.append(
                EtfSourceCandidate(
                    section=section,
                    symbol=symbol,
                    name=_text(row.get("name")),
                    source_url=source_url,
                )
            )
    return candidates


def build_summary(
    candidates: list[EtfSourceCandidate],
    *,
    candidate_file: Path,
    raw_root: Path,
    run_date: str,
    dry_run: bool,
    results: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "source": "DI ETF official source pages",
        "run_date": run_date,
        "generated_at_kst": _now_kst().isoformat(),
        "candidate_file": candidate_file.as_posix(),
        "raw_root": raw_root.as_posix(),
        "dry_run": dry_run,
        "request_count": len(candidates),
        "requests": [
            {
                **asdict(candidate),
                "output_dir": _source_dir(raw_root, run_date, candidate.symbol).as_posix(),
            }
            for candidate in candidates
        ],
        "results": results or [],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def collect_sources(
    candidates: list[EtfSourceCandidate],
    *,
    candidate_file: Path,
    raw_root: Path,
    run_date: str,
    timeout: float,
    user_agent: str,
) -> dict[str, Any]:
    session = requests.Session()
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    results: list[dict[str, Any]] = []
    fetched_at = _now_kst().isoformat()

    for candidate in candidates:
        output_dir = _source_dir(raw_root, run_date, candidate.symbol)
        output_dir.mkdir(parents=True, exist_ok=True)
        raw_path = output_dir / "source.raw.html"
        meta_path = output_dir / "source.raw.html.meta.json"
        try:
            response = session.get(candidate.source_url, headers=headers, timeout=timeout, allow_redirects=True)
            raw_path.write_bytes(response.content)
            meta = {
                **asdict(candidate),
                "requested_url": candidate.source_url,
                "final_url": response.url,
                "fetched_at_kst": fetched_at,
                "ok": response.ok,
                "status_code": response.status_code,
                "content_type": response.headers.get("content-type", ""),
                "encoding": response.encoding,
                "bytes": len(response.content),
                "raw_path": raw_path.as_posix(),
            }
        except requests.RequestException as exc:
            meta = {
                **asdict(candidate),
                "requested_url": candidate.source_url,
                "fetched_at_kst": fetched_at,
                "ok": False,
                "error_type": exc.__class__.__name__,
                "error": str(exc),
                "raw_path": raw_path.as_posix(),
            }
        _write_json(meta_path, meta)
        results.append(meta)

    summary = build_summary(
        candidates,
        candidate_file=candidate_file,
        raw_root=raw_root,
        run_date=run_date,
        dry_run=False,
        results=results,
    )
    _write_json(_collection_root(raw_root, run_date) / "collection_summary.json", summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect official ETF source pages listed in the DI candidate manifest.")
    parser.add_argument("--candidate-file", type=Path, default=DEFAULT_CANDIDATE_FILE)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--run-date", default=_now_kst().date().isoformat())
    parser.add_argument("--section", choices=DEFAULT_SECTIONS, action="append", dest="sections")
    parser.add_argument("--symbol", action="append", dest="symbols", default=[])
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--user-agent", default=os.environ.get("ETF_USER_AGENT") or os.environ.get("SEC_USER_AGENT") or DEFAULT_USER_AGENT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        payload = _load_yaml(args.candidate_file)
        sections = tuple(args.sections or DEFAULT_SECTIONS)
        symbols = tuple(args.symbols or ())
        candidates = iter_source_candidates(payload, sections=sections, symbols=symbols)
        if args.dry_run:
            summary = build_summary(
                candidates,
                candidate_file=args.candidate_file,
                raw_root=args.raw_root,
                run_date=args.run_date,
                dry_run=True,
            )
        else:
            summary = collect_sources(
                candidates,
                candidate_file=args.candidate_file,
                raw_root=args.raw_root,
                run_date=args.run_date,
                timeout=args.timeout,
                user_agent=args.user_agent,
            )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
