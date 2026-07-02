"""Replay Point-in-Time status events onto date/code market-data rows.

The replay consumes already-normalized status-event rows. It does not fetch raw
KRX/KIND data and it does not prove historical status coverage.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from quant_point_in_time_status_events_validate import (
    DEFAULT_SCHEMA,
    DEFAULT_SOURCE_POLICY,
    validate_events,
)


REPLAY_FIELDS = (
    "pit_status_replay_status",
    "pit_status_exclude_reasons",
    "pit_managed_issue_active",
    "pit_trading_halt_active",
    "pit_market_alert_active",
    "pit_delisting_active",
    "pit_latest_event_date",
    "pit_applied_event_count",
    "pit_source_paths",
)


@dataclass
class StatusState:
    managed_issue_active: bool = False
    trading_halt_active: bool = False
    market_alert_active: bool = False
    delisting_active: bool = False
    latest_event_date: str = ""
    applied_event_count: int = 0
    source_paths: set[str] = field(default_factory=set)

    def exclude_reasons(self) -> list[str]:
        reasons = []
        if self.managed_issue_active:
            reasons.append("managed_issue_active")
        if self.trading_halt_active:
            reasons.append("trading_halt_active")
        if self.market_alert_active:
            reasons.append("market_alert_active")
        if self.delisting_active:
            reasons.append("delisting_active")
        return reasons


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"missing CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    return fieldnames, rows


def _iso_date(value: str, field_name: str) -> str:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{field_name} must be YYYY-MM-DD: {value}") from exc
    return value


def _validate_market_rows(rows: list[dict[str, str]], date_column: str, code_column: str) -> None:
    for index, row in enumerate(rows, start=1):
        if not row.get(date_column):
            raise ValueError(f"market-data row {index} missing {date_column}")
        if not row.get(code_column):
            raise ValueError(f"market-data row {index} missing {code_column}")
        _iso_date(row[date_column], date_column)


def _events_by_code(events: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    by_code: dict[str, list[dict[str, str]]] = defaultdict(list)
    for event in events:
        by_code[event["code"]].append(event)
    for code, code_events in by_code.items():
        by_code[code] = sorted(code_events, key=lambda event: (event["event_date"], event["status_type"], event["status_value"]))
    return dict(by_code)


def _apply_event(state: StatusState, event: dict[str, str]) -> None:
    status_type = event["status_type"]
    status_value = event["status_value"]
    if status_type == "managed_issue":
        state.managed_issue_active = status_value == "designated"
    elif status_type == "trading_halt":
        state.trading_halt_active = status_value == "halted"
    elif status_type == "trading_resume":
        state.trading_halt_active = False
    elif status_type == "market_alert":
        state.market_alert_active = status_value in {"caution", "warning", "risk"}
    elif status_type == "delisting":
        state.delisting_active = status_value in {"delisting_notice", "delisted"}
    elif status_type in {"listing", "listing_change"}:
        pass
    else:  # pragma: no cover - validator should reject this first
        raise ValueError(f"unsupported status_type: {status_type}")

    state.latest_event_date = event["event_date"]
    state.applied_event_count += 1
    if event.get("raw_path"):
        state.source_paths.add(event["raw_path"])


def _state_for_date(events: list[dict[str, str]], as_of_date: str) -> StatusState:
    state = StatusState()
    for event in events:
        if event["event_date"] > as_of_date:
            break
        _apply_event(state, event)
    return state


def _annotate_row(row: dict[str, str], state: StatusState) -> dict[str, str]:
    reasons = state.exclude_reasons()
    replay_status = "exclude_by_status_event" if reasons else "include_by_status_event"
    annotated = dict(row)
    annotated.update(
        {
            "pit_status_replay_status": replay_status,
            "pit_status_exclude_reasons": ";".join(reasons),
            "pit_managed_issue_active": str(state.managed_issue_active).lower(),
            "pit_trading_halt_active": str(state.trading_halt_active).lower(),
            "pit_market_alert_active": str(state.market_alert_active).lower(),
            "pit_delisting_active": str(state.delisting_active).lower(),
            "pit_latest_event_date": state.latest_event_date,
            "pit_applied_event_count": str(state.applied_event_count),
            "pit_source_paths": ";".join(sorted(state.source_paths)),
        }
    )
    return annotated


def replay_status_events(
    market_data_path: Path,
    events_path: Path,
    schema_path: Path,
    source_policy_path: Path,
    date_column: str = "date",
    code_column: str = "code",
) -> tuple[list[dict[str, str]], list[str], dict[str, Any]]:
    event_results, event_summary = validate_events(events_path, schema_path, source_policy_path)
    if event_summary["invalid_rows"]:
        raise ValueError(f"status events failed validation: {event_summary['invalid_rows']} invalid rows")

    market_fields, market_rows = _read_csv(market_data_path)
    if date_column not in market_fields:
        raise ValueError(f"market-data CSV missing date column: {date_column}")
    if code_column not in market_fields:
        raise ValueError(f"market-data CSV missing code column: {code_column}")
    _validate_market_rows(market_rows, date_column, code_column)

    _event_fields, event_rows = _read_csv(events_path)
    events_by_code = _events_by_code(event_rows)
    output_rows: list[dict[str, str]] = []
    for row in market_rows:
        as_of_date = row[date_column]
        code = row[code_column]
        state = _state_for_date(events_by_code.get(code, []), as_of_date)
        output_rows.append(_annotate_row(row, state))

    exclude_rows = sum(1 for row in output_rows if row["pit_status_replay_status"] == "exclude_by_status_event")
    summary = {
        "market_data_path": market_data_path,
        "events_path": events_path,
        "schema_path": schema_path,
        "source_policy_path": source_policy_path,
        "input_rows": len(market_rows),
        "status_event_rows": event_summary["input_rows"],
        "include_rows": len(output_rows) - exclude_rows,
        "exclude_rows": exclude_rows,
        "codes_with_events": len(events_by_code),
        "date_count": len({row[date_column] for row in market_rows}),
    }
    output_fields = tuple(market_fields) + tuple(field for field in REPLAY_FIELDS if field not in market_fields)
    return output_rows, list(output_fields), summary


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_report(summary: dict[str, Any], output: Path) -> str:
    lines = [
        "# Point-in-Time Status Replay Scaffold",
        "",
        f"- Market data: {_wikilink(summary['market_data_path'])}",
        f"- Status events: {_wikilink(summary['events_path'])}",
        f"- Output: {_wikilink(output)}",
        "- Interpretation: event-row replay scaffold only, not full historical status coverage",
        "- Backtest readiness: `hold`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Input market rows | {summary['input_rows']} |",
        f"| Status event rows | {summary['status_event_rows']} |",
        f"| Dates | {summary['date_count']} |",
        f"| Codes with events | {summary['codes_with_events']} |",
        f"| Include rows by event state | {summary['include_rows']} |",
        f"| Exclude rows by event state | {summary['exclude_rows']} |",
        "",
        "## Guardrails",
        "",
        "- `include_by_status_event` means no active exclusion in the provided event rows; it does not prove complete official status coverage.",
        "- Use this only after event rows pass [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]].",
        "- `Backtest` remains `hold` until historical status coverage is validated for the selected scope.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay normalized Point-in-Time status events onto market-data rows.")
    parser.add_argument("--market-data", required=True, type=Path)
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--schema", default=DEFAULT_SCHEMA, type=Path)
    parser.add_argument("--source-policy", default=DEFAULT_SOURCE_POLICY, type=Path)
    parser.add_argument("--date-column", default="date")
    parser.add_argument("--code-column", default="code")
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    try:
        rows, fields, summary = replay_status_events(
            args.market_data,
            args.events,
            args.schema,
            args.source_policy,
            args.date_column,
            args.code_column,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    _write_csv(args.output, fields, rows)
    report = _render_report(summary, args.output)
    if args.report_output:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
