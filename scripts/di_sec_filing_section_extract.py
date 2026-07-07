"""Extract SEC filing narrative sections into ignored raw text files."""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo


try:
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = timezone(timedelta(hours=9), "KST")

DEFAULT_RAW_ROOT = Path("_report/raw")
DEFAULT_RESEARCH_ROOT = Path("_report/di/research")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SYMBOL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9.\-]{0,14}$")
FILING_NAME_RE = re.compile(
    r"^(?P<form>10-[KQ])_(?P<filing_date>\d{4}-\d{2}-\d{2})_(?P<accession>[A-Za-z0-9]+)_(?P<document>.+)\.raw\.html$"
)
SPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class SectionSpec:
    key: str
    title: str
    forms: tuple[str, ...]
    start_patterns: tuple[re.Pattern[str], ...]
    end_patterns: tuple[re.Pattern[str], ...]


@dataclass(frozen=True)
class FilingDocument:
    form: str
    filing_date: str
    accession: str
    document: str
    path: Path


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag.lower() in {"script", "style", "noscript"}:
            self._skip_depth += 1
            return
        if tag.lower() in {"br", "p", "div", "tr", "table", "h1", "h2", "h3", "h4", "li"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1
            return
        if tag.lower() in {"p", "div", "tr", "table", "h1", "h2", "h3", "h4", "li"}:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        raw = html.unescape(" ".join(self.parts))
        lines = [SPACE_RE.sub(" ", line).strip() for line in raw.splitlines()]
        return "\n".join(line for line in lines if line)


def _now_kst() -> datetime:
    return datetime.now(KST).replace(microsecond=0)


def _validate_ymd(value: str) -> str:
    if not DATE_RE.match(value):
        raise argparse.ArgumentTypeError("date must be YYYY-MM-DD")
    return value


def _validate_symbol(value: str) -> str:
    if not SYMBOL_RE.match(value):
        raise argparse.ArgumentTypeError("symbol must start with a letter and contain only letters, digits, dot, or hyphen")
    return value.upper()


def _raw_dir(raw_root: Path, run_date: str, symbol: str) -> Path:
    return raw_root / run_date[:4] / run_date / "sec" / symbol.upper()


def _output_path(research_root: Path, symbol: str) -> Path:
    return research_root / symbol.upper() / "sec-filing-sections.md"


def _section_raw_path(raw_dir: Path, filing: FilingDocument, section_key: str) -> Path:
    return raw_dir / "sections" / f"{filing.form}_{filing.filing_date}_{filing.accession}_{section_key}.raw.txt"


def _section_specs() -> tuple[SectionSpec, ...]:
    flags = re.IGNORECASE | re.MULTILINE
    return (
        SectionSpec(
            key="business",
            title="Business",
            forms=("10-K",),
            start_patterns=(re.compile(r"(?:^|\n)item\s+1\.?\s+b\s*usiness\b", flags),),
            end_patterns=(re.compile(r"(?:^|\n)item\s+1a\.?\s+ris\s*k\s+factors\b", flags),),
        ),
        SectionSpec(
            key="risk_factors",
            title="Risk Factors",
            forms=("10-K", "10-Q"),
            start_patterns=(re.compile(r"(?:^|\n)item\s+1a\.?\s+ris\s*k\s+factors\b", flags),),
            end_patterns=(
                re.compile(r"(?:^|\n)item\s+1b\.?", flags),
                re.compile(r"(?:^|\n)item\s+2\.?", flags),
            ),
        ),
        SectionSpec(
            key="mda",
            title="MD&A",
            forms=("10-K",),
            start_patterns=(re.compile(r"(?:^|\n)item\s+7\.?\s+management", flags),),
            end_patterns=(
                re.compile(r"(?:^|\n)item\s+7a\.?", flags),
                re.compile(r"(?:^|\n)item\s+8\.?", flags),
            ),
        ),
        SectionSpec(
            key="quarterly_mda",
            title="Quarterly MD&A",
            forms=("10-Q",),
            start_patterns=(re.compile(r"(?:^|\n)item\s+2\.?\s+management", flags),),
            end_patterns=(
                re.compile(r"(?:^|\n)item\s+3\.?", flags),
                re.compile(r"(?:^|\n)item\s+4\.?", flags),
            ),
        ),
    )


def _filing_documents(raw_dir: Path) -> list[FilingDocument]:
    filings_dir = raw_dir / "filings"
    rows: list[FilingDocument] = []
    for path in sorted(filings_dir.glob("*.raw.html")):
        match = FILING_NAME_RE.match(path.name)
        if not match:
            continue
        rows.append(
            FilingDocument(
                form=match.group("form"),
                filing_date=match.group("filing_date"),
                accession=match.group("accession"),
                document=match.group("document"),
                path=path,
            )
        )
    return rows


def _html_to_text(path: Path) -> str:
    parser = TextExtractor()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return parser.text()


def _first_end_after(text: str, start: int, patterns: Iterable[re.Pattern[str]]) -> int:
    positions = [match.start() for pattern in patterns for match in [pattern.search(text, start)] if match]
    return min(positions) if positions else len(text)


def _extract_section(text: str, spec: SectionSpec, min_chars: int) -> tuple[str, str]:
    candidates: list[str] = []
    for pattern in spec.start_patterns:
        for match in pattern.finditer(text):
            end = _first_end_after(text, match.end(), spec.end_patterns)
            snippet = text[match.start() : end].strip()
            if len(snippet) >= min_chars:
                candidates.append(snippet)
    if not candidates:
        return "missing", ""
    candidates.sort(key=len, reverse=True)
    return "ok", candidates[0]


def _render_report(symbol: str, run_date: str, raw_dir: Path, rows: list[dict[str, str | int]]) -> str:
    lines = [
        f"# {symbol.upper()} SEC Filing Section Map",
        "",
        f"- Run date: `{run_date}`",
        f"- Generated at: `{_now_kst().isoformat()}`",
        f"- Raw dir: `{raw_dir.as_posix()}`",
        "- Source: SEC filing HTML converted to ignored raw text snippets",
        "- Interpretation: section source map only; no buy or order intent is generated",
        "- Order intent generated: `false`",
        "",
        "## Sections",
        "",
        "| Form | Filing date | Section | Status | Characters | Local raw path |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['form']}`",
                    str(row["filing_date"]),
                    str(row["section"]),
                    f"`{row['status']}`",
                    str(row["characters"]),
                    f"`{row['raw_output']}`" if row["raw_output"] else "-",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Reading Order",
            "",
            "1. Start with `business` to understand the operating model and segment language.",
            "2. Read `risk_factors` before writing the bear case or invalidation rule.",
            "3. Use `mda` and `quarterly_mda` to connect revenue, margin, capex, and cash-flow changes to management wording.",
            "4. Keep copied source text in `_report/raw/`; write conclusions in `thesis.md` and `decision.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def extract(args: argparse.Namespace) -> Path:
    raw_dir = args.raw_dir or _raw_dir(args.raw_root, args.run_date, args.symbol)
    output = args.output or _output_path(args.research_root, args.symbol)
    filings = _filing_documents(raw_dir)
    if not filings:
        raise ValueError(f"{raw_dir / 'filings'}: no filing HTML documents found")

    rows: list[dict[str, str | int]] = []
    specs = _section_specs()
    for filing in filings:
        text = _html_to_text(filing.path)
        for spec in specs:
            if filing.form not in spec.forms:
                continue
            status, snippet = _extract_section(text, spec, args.min_chars)
            raw_output = ""
            if snippet:
                section_path = _section_raw_path(raw_dir, filing, spec.key)
                section_path.parent.mkdir(parents=True, exist_ok=True)
                section_path.write_text(snippet + "\n", encoding="utf-8")
                raw_output = section_path.as_posix()
            rows.append(
                {
                    "form": filing.form,
                    "filing_date": filing.filing_date,
                    "section": spec.key,
                    "status": status,
                    "characters": len(snippet),
                    "raw_output": raw_output,
                }
            )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(_render_report(args.symbol, args.run_date, raw_dir, rows), encoding="utf-8")
    return output


def main() -> int:
    default_run_date = _now_kst().date().isoformat()
    parser = argparse.ArgumentParser(description="Extract SEC filing narrative sections into ignored raw text files.")
    parser.add_argument("--symbol", required=True, type=_validate_symbol)
    parser.add_argument("--run-date", type=_validate_ymd, default=default_run_date)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--research-root", type=Path, default=DEFAULT_RESEARCH_ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--min-chars", type=int, default=500)
    args = parser.parse_args()

    try:
        output = extract(args)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    print(output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
