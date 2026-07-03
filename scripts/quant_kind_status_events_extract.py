"""Extract normalized status-event rows from KIND status snapshot downloads.

The input is a local raw directory produced by quant_kind_status_source_probe.py.
This script does not download data. It converts verified KIND Excel-HTML
snapshots into the local Point-in-Time status-event CSV schema.
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


KST = ZoneInfo("Asia/Seoul")
KIND_BASE_URL = "https://kind.krx.co.kr"
CAPTURE_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CODE_RE = re.compile(r"^[0-9A-Za-z]{5,12}$")

COL_COMPANY = "\ud68c\uc0ac\uba85"
COL_NAME = "\uc885\ubaa9\uba85"
COL_CODE = "\uc885\ubaa9\ucf54\ub4dc"
COL_DESIGNATION_DATE = "\uc9c0\uc815\uc77c"
COL_DESIGNATION_REASON = "\uc9c0\uc815\uc0ac\uc720"
COL_REASON = "\uc0ac\uc720"
COL_DELIST_DATE = "\ud3d0\uc9c0\uc77c\uc790"
COL_DELIST_REASON = "\ud3d0\uc9c0\uc0ac\uc720"
COL_DISCLOSURE_DATE = "\uacf5\uc2dc\uc77c"
COL_ALERT_TYPE = "\uc720\ud615"
COL_RELEASE_DATE = "\ud574\uc81c\uc77c"

EVENT_FIELDS = (
    "event_date",
    "code",
    "market",
    "status_type",
    "status_value",
    "source",
    "source_url",
    "raw_path",
    "confidence",
    "notes",
)


@dataclass(frozen=True)
class KindSnapshotSpec:
    slug: str
    filename: str
    source_url: str
    status_type: str
    status_value: str
    event_date_column: str | None
    confidence: str
    note_columns: tuple[str, ...] = ()
    release_status_value: str | None = None
    release_date_column: str | None = None


DEFAULT_SPECS = (
    KindSnapshotSpec(
        slug="managed_issue",
        filename="managed_issue.xls",
        source_url=f"{KIND_BASE_URL}/investwarn/adminissue.do?method=searchAdminIssueList",
        status_type="managed_issue",
        status_value="designated",
        event_date_column=COL_DESIGNATION_DATE,
        confidence="high",
        note_columns=(COL_NAME, COL_DESIGNATION_REASON),
    ),
    KindSnapshotSpec(
        slug="trading_halt",
        filename="trading_halt.xls",
        source_url=f"{KIND_BASE_URL}/investwarn/tradinghaltissue.do?method=searchTradingHaltIssueMain",
        status_type="trading_halt",
        status_value="halted",
        event_date_column=None,
        confidence="medium",
        note_columns=(COL_NAME, COL_REASON),
    ),
    KindSnapshotSpec(
        slug="delisted_company",
        filename="delisted_company.xls",
        source_url=f"{KIND_BASE_URL}/investwarn/delcompany.do?method=searchDelCompanyMain",
        status_type="delisting",
        status_value="delisted",
        event_date_column=COL_DELIST_DATE,
        confidence="high",
        note_columns=(COL_COMPANY, COL_DELIST_REASON),
    ),
    KindSnapshotSpec(
        slug="market_alert_caution",
        filename="market_alert_caution.xls",
        source_url=f"{KIND_BASE_URL}/investwarn/investattentwarnrisky.do?method=investattentwarnriskyMain",
        status_type="market_alert",
        status_value="caution",
        event_date_column=COL_DESIGNATION_DATE,
        confidence="high",
        note_columns=(COL_NAME, COL_ALERT_TYPE, COL_DISCLOSURE_DATE),
    ),
    KindSnapshotSpec(
        slug="market_alert_warning",
        filename="market_alert_warning.xls",
        source_url=f"{KIND_BASE_URL}/investwarn/investattentwarnrisky.do?method=investattentwarnriskyMain",
        status_type="market_alert",
        status_value="warning",
        event_date_column=COL_DESIGNATION_DATE,
        confidence="high",
        note_columns=(COL_NAME, COL_DISCLOSURE_DATE),
        release_status_value="released",
        release_date_column=COL_RELEASE_DATE,
    ),
    KindSnapshotSpec(
        slug="market_alert_risk",
        filename="market_alert_risk.xls",
        source_url=f"{KIND_BASE_URL}/investwarn/investattentwarnrisky.do?method=investattentwarnriskyMain",
        status_type="market_alert",
        status_value="risk",
        event_date_column=COL_DESIGNATION_DATE,
        confidence="high",
        note_columns=(COL_NAME, COL_DISCLOSURE_DATE),
        release_status_value="released",
        release_date_column=COL_RELEASE_DATE,
    ),
)


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._in_row = False
        self._in_cell = False
        self._row: list[str] = []
        self._cell: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lowered = tag.lower()
        if lowered == "tr":
            self._in_row = True
            self._row = []
        elif lowered in {"td", "th"} and self._in_row:
            self._in_cell = True
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        if lowered in {"td", "th"} and self._in_cell:
            self._row.append(" ".join("".join(self._cell).split()))
            self._in_cell = False
        elif lowered == "tr" and self._in_row:
            if self._row:
                self.rows.append(self._row)
            self._in_row = False


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _validate_capture_date(value: str) -> str:
    if not CAPTURE_DATE_RE.match(value):
        raise argparse.ArgumentTypeError("capture-date must be YYYY-MM-DD")
    return value


def _decode_html(path: Path) -> str:
    content = path.read_bytes()
    for encoding in ("euc-kr", "cp949", "utf-8"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("utf-8", errors="replace")


def parse_html_table(path: Path) -> list[dict[str, str]]:
    parser = _TableParser()
    parser.feed(_decode_html(path))
    if not parser.rows:
        return []
    headers = [header.strip() for header in parser.rows[0]]
    rows: list[dict[str, str]] = []
    for raw_row in parser.rows[1:]:
        if not any(raw_row):
            continue
        row = {headers[index]: value.strip() for index, value in enumerate(raw_row[: len(headers)])}
        rows.append(row)
    return rows


def _normalize_code(value: Any) -> str:
    code = str(value or "").strip().strip('"').upper()
    if code.endswith(".0") and code[:-2].isdigit():
        code = code[:-2]
    if code.isdigit() and len(code) < 6:
        code = code.zfill(6)
    return code


def _valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def _repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _notes(spec: KindSnapshotSpec, row: dict[str, str]) -> str:
    parts = [f"snapshot={spec.slug}"]
    for column in spec.note_columns:
        value = row.get(column, "")
        if value:
            parts.append(f"{column}={value}")
    return "; ".join(parts)


def _event_row(
    *,
    event_date: str,
    code: str,
    status_type: str,
    status_value: str,
    source_url: str,
    raw_path: str,
    confidence: str,
    notes: str,
) -> dict[str, str]:
    return {
        "event_date": event_date,
        "code": code,
        "market": "UNKNOWN",
        "status_type": status_type,
        "status_value": status_value,
        "source": "kind",
        "source_url": source_url,
        "raw_path": raw_path,
        "confidence": confidence,
        "notes": notes,
    }


def extract_events_from_snapshot(
    spec: KindSnapshotSpec,
    raw_path: Path,
    capture_date: str,
) -> list[dict[str, str]]:
    rows = parse_html_table(raw_path)
    raw_path_text = _repo_relative(raw_path)
    events: list[dict[str, str]] = []
    for row in rows:
        code = _normalize_code(row.get(COL_CODE, ""))
        if not code or not CODE_RE.fullmatch(code):
            continue
        event_date = capture_date if spec.event_date_column is None else row.get(spec.event_date_column, "")
        if not _valid_date(event_date):
            continue
        notes = _notes(spec, row)
        events.append(
            _event_row(
                event_date=event_date,
                code=code,
                status_type=spec.status_type,
                status_value=spec.status_value,
                source_url=spec.source_url,
                raw_path=raw_path_text,
                confidence=spec.confidence,
                notes=notes,
            )
        )
        release_date = row.get(spec.release_date_column or "", "")
        if spec.release_status_value and _valid_date(release_date):
            events.append(
                _event_row(
                    event_date=release_date,
                    code=code,
                    status_type=spec.status_type,
                    status_value=spec.release_status_value,
                    source_url=spec.source_url,
                    raw_path=raw_path_text,
                    confidence=spec.confidence,
                    notes=f"{notes}; release_from_snapshot=true",
                )
            )
    return events


def extract_kind_status_events(
    raw_dir: Path,
    capture_date: str,
    specs: tuple[KindSnapshotSpec, ...] = DEFAULT_SPECS,
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    all_events: list[dict[str, str]] = []
    by_snapshot: dict[str, int] = {}
    missing_inputs: list[str] = []
    for spec in specs:
        raw_path = raw_dir / spec.filename
        if not raw_path.exists():
            missing_inputs.append(raw_path.as_posix())
            by_snapshot[spec.slug] = 0
            continue
        events = extract_events_from_snapshot(spec, raw_path, capture_date)
        all_events.extend(events)
        by_snapshot[spec.slug] = len(events)

    pre_dedupe_rows = len(all_events)
    all_events = _dedupe_events(all_events)
    all_events.sort(key=lambda row: (row["event_date"], row["code"], row["status_type"], row["status_value"]))
    summary = {
        "capture_date": capture_date,
        "raw_dir": raw_dir,
        "input_snapshots": len(specs),
        "missing_inputs": missing_inputs,
        "event_rows": len(all_events),
        "deduped_rows": pre_dedupe_rows - len(all_events),
        "by_snapshot": dict(sorted(by_snapshot.items())),
        "generated_at": _now_kst().isoformat(),
    }
    return all_events, summary


def _dedupe_events(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: dict[tuple[str, str, str, str, str, str], dict[str, str]] = {}
    for row in rows:
        key = (
            row["event_date"],
            row["code"],
            row["status_type"],
            row["status_value"],
            row["source"],
            row["raw_path"],
        )
        if key not in merged:
            merged[key] = dict(row)
            continue
        existing = merged[key]
        existing_notes = existing.get("notes", "")
        incoming_notes = row.get("notes", "")
        if incoming_notes and incoming_notes not in existing_notes:
            existing["notes"] = f"{existing_notes} | duplicate_source_row={incoming_notes}"
    return list(merged.values())


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EVENT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _wikilink(path: Path | str) -> str:
    rendered = Path(path).as_posix() if isinstance(path, Path) else str(path).replace("\\", "/")
    return f"[[{rendered}|{rendered}]]"


def render_report(summary: dict[str, Any], output: Path) -> str:
    lines = [
        "# KIND Status Events Extract",
        "",
        f"- Capture date: `{summary['capture_date']}`",
        f"- Raw directory: {_wikilink(summary['raw_dir'])}",
        f"- Events output: {_wikilink(output)}",
        f"- Event rows: `{summary['event_rows']}`",
        f"- Deduped rows: `{summary['deduped_rows']}`",
        "- Source: `kind`",
        "- Interpretation: normalized current/status snapshot events; not complete historical Point-in-Time coverage",
        "- Backtest readiness: `hold`",
        "",
        "## Rows By Snapshot",
        "",
        "| Snapshot | Event rows |",
        "| --- | ---: |",
    ]
    for slug, count in summary["by_snapshot"].items():
        lines.append(f"| `{slug}` | {count} |")

    if summary["missing_inputs"]:
        lines.extend(["", "## Missing Inputs", ""])
        for path in summary["missing_inputs"]:
            lines.append(f"- {_wikilink(path)}")

    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- `trading_halt` rows use the capture date because the KIND current halt snapshot does not expose halt start dates.",
            "- `market` is `UNKNOWN` until joined to an official listed-issue or market classification source.",
            "- Use [[scripts/quant_point_in_time_status_events_validate.py|scripts/quant_point_in_time_status_events_validate.py]] before replay.",
            "- This advances source normalization, but it does not make `Backtest` ready without historical coverage.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    today = _now_kst().date().isoformat()
    parser = argparse.ArgumentParser(description="Extract KIND status snapshots into Point-in-Time status events.")
    parser.add_argument("--capture-date", default=today, type=_validate_capture_date)
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args()

    raw_dir = args.raw_dir or Path("_report/raw") / args.capture_date[:4] / args.capture_date / "kind" / "status-source-probe"
    rows, summary = extract_kind_status_events(raw_dir, args.capture_date)
    _write_csv(args.output, rows)
    if args.report_output:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(render_report(summary, args.output), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
