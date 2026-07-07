"""Enrich Point-in-Time status-event rows with market labels.

The enrichment uses an already-collected market-data CSV as deterministic local
evidence. It does not fetch KRX/KIND data and does not expand historical status
coverage by itself.
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from quant_io import write_text_lf


VALID_MARKETS = {"KOSPI", "KOSDAQ", "KONEX"}


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise ValueError(f"missing CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    return fieldnames, rows


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _append_note(existing: str, note: str) -> str:
    if not existing:
        return note
    if note in existing:
        return existing
    return f"{existing}; {note}"


def _build_market_map(
    market_rows: list[dict[str, str]],
    code_column: str,
    market_column: str,
) -> dict[str, set[str]]:
    mapping: dict[str, set[str]] = defaultdict(set)
    for row in market_rows:
        code = row.get(code_column, "").strip()
        market = row.get(market_column, "").strip()
        if code and market in VALID_MARKETS:
            mapping[code].add(market)
    return dict(mapping)


def _require_columns(fieldnames: list[str], required: tuple[str, ...], label: str) -> None:
    missing = [column for column in required if column not in fieldnames]
    if missing:
        raise ValueError(f"{label} CSV missing required columns: {', '.join(missing)}")


def enrich_event_markets(
    events_path: Path,
    market_data_path: Path,
    event_code_column: str = "code",
    event_market_column: str = "market",
    market_code_column: str = "code",
    market_market_column: str = "market",
) -> tuple[list[str], list[dict[str, str]], dict[str, Any]]:
    event_fields, event_rows = _read_csv(events_path)
    market_fields, market_rows = _read_csv(market_data_path)
    _require_columns(event_fields, (event_code_column, event_market_column, "notes"), "events")
    _require_columns(market_fields, (market_code_column, market_market_column), "market-data")

    market_map = _build_market_map(market_rows, market_code_column, market_market_column)
    counts: Counter[str] = Counter()
    output_rows: list[dict[str, str]] = []

    for row in event_rows:
        enriched = dict(row)
        code = enriched.get(event_code_column, "")
        current_market = enriched.get(event_market_column, "") or "UNKNOWN"
        mapped_markets = market_map.get(code, set())

        if len(mapped_markets) == 1:
            mapped_market = next(iter(mapped_markets))
            if current_market == "UNKNOWN":
                enriched[event_market_column] = mapped_market
                enriched["notes"] = _append_note(enriched.get("notes", ""), f"market_enrichment=market_data_join:{mapped_market}")
                counts["resolved_unknown_market"] += 1
            elif current_market == mapped_market:
                counts["retained_matching_market"] += 1
            else:
                enriched["notes"] = _append_note(
                    enriched.get("notes", ""),
                    f"market_enrichment=retained_source_market_conflict:{mapped_market}",
                )
                counts["retained_source_market_conflict"] += 1
        elif len(mapped_markets) > 1:
            enriched["notes"] = _append_note(
                enriched.get("notes", ""),
                f"market_enrichment=ambiguous_market_mapping:{'/'.join(sorted(mapped_markets))}",
            )
            counts["ambiguous_market_mapping"] += 1
        else:
            counts["unresolved_no_market_mapping"] += 1

        output_rows.append(enriched)

    summary = {
        "events_path": events_path,
        "market_data_path": market_data_path,
        "input_rows": len(event_rows),
        "output_rows": len(output_rows),
        "market_data_rows": len(market_rows),
        "mapped_codes": len(market_map),
        "resolved_unknown_market": counts["resolved_unknown_market"],
        "retained_matching_market": counts["retained_matching_market"],
        "retained_source_market_conflict": counts["retained_source_market_conflict"],
        "ambiguous_market_mapping": counts["ambiguous_market_mapping"],
        "unresolved_no_market_mapping": counts["unresolved_no_market_mapping"],
    }
    return event_fields, output_rows, summary


def _wikilink(path: Path) -> str:
    rendered = path.as_posix()
    return f"[[{rendered}|{rendered}]]"


def _render_report(summary: dict[str, Any], output_path: Path) -> str:
    lines = [
        "# Point-in-Time Status Events Market Enrichment",
        "",
        f"- Events input: {_wikilink(summary['events_path'])}",
        f"- Market-data input: {_wikilink(summary['market_data_path'])}",
        f"- Output: {_wikilink(output_path)}",
        "- Interpretation: local market-label enrichment only, not additional status coverage",
        "- Backtest readiness: `hold`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Input event rows | {summary['input_rows']} |",
        f"| Output event rows | {summary['output_rows']} |",
        f"| Market-data rows | {summary['market_data_rows']} |",
        f"| Mapped codes | {summary['mapped_codes']} |",
        f"| Resolved UNKNOWN market rows | {summary['resolved_unknown_market']} |",
        f"| Retained matching market rows | {summary['retained_matching_market']} |",
        f"| Retained source-market conflicts | {summary['retained_source_market_conflict']} |",
        f"| Ambiguous market mappings | {summary['ambiguous_market_mapping']} |",
        f"| Unresolved no market mapping | {summary['unresolved_no_market_mapping']} |",
        "",
        "## Guardrails",
        "",
        "- This only fills market labels when the provided market-data join has deterministic code-to-market evidence.",
        "- Unresolved rows remain `UNKNOWN` and must not be interpreted as excluded or included by market.",
        "- `Backtest` remains `hold` until historical status coverage is validated for the selected scope.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Enrich status-event market labels from a local market-data CSV.")
    parser.add_argument("--events", required=True, type=Path)
    parser.add_argument("--market-data", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--event-code-column", default="code")
    parser.add_argument("--event-market-column", default="market")
    parser.add_argument("--market-code-column", default="code")
    parser.add_argument("--market-market-column", default="market")
    args = parser.parse_args()

    try:
        fields, rows, summary = enrich_event_markets(
            args.events,
            args.market_data,
            args.event_code_column,
            args.event_market_column,
            args.market_code_column,
            args.market_market_column,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    _write_csv(args.output, fields, rows)
    report = _render_report(summary, args.output)
    if args.report_output:
        write_text_lf(args.report_output, report)
    else:
        print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
