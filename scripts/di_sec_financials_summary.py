"""Render DI financials.md from SEC companyfacts raw JSON."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo


try:
    KST = ZoneInfo("Asia/Seoul")
except Exception:
    KST = timezone(timedelta(hours=9), "KST")

DEFAULT_RAW_ROOT = Path("_report/raw")
DEFAULT_RESEARCH_ROOT = Path("_report/di/research")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SYMBOL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9.\-]{0,14}$")

FLOW_METRICS = {
    "revenue": ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"),
    "operating_income": ("OperatingIncomeLoss",),
    "net_income": ("NetIncomeLoss", "ProfitLoss"),
    "operating_cash_flow": ("NetCashProvidedByUsedInOperatingActivities",),
    "capex": ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"),
}

INSTANT_METRICS = {
    "cash_and_investments": ("CashCashEquivalentsAndShortTermInvestments", "CashAndCashEquivalentsAtCarryingValue"),
    "assets": ("Assets",),
    "liabilities": ("Liabilities",),
    "debt_proxy": ("DebtLongtermAndShorttermCombinedAmount", "LongTermDebt", "LongTermDebtNoncurrent"),
    "equity": ("StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"),
}


@dataclass(frozen=True)
class Fact:
    concept: str
    unit: str
    value: int | float
    start: str
    end: str
    filed: str
    fy: str
    fp: str
    form: str
    accn: str


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


def _read_json(path: Path) -> Any:
    if not path.exists():
        raise ValueError(f"{path}: file not found")
    return json.loads(path.read_text(encoding="utf-8"))


def _raw_dir(raw_root: Path, run_date: str, symbol: str) -> Path:
    return raw_root / run_date[:4] / run_date / "sec" / symbol.upper()


def _output_path(research_root: Path, symbol: str) -> Path:
    return research_root / symbol.upper() / "financials.md"


def _parse_date(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _duration_days(fact: Fact) -> int | None:
    if not fact.start or not fact.end:
        return None
    start = _parse_date(fact.start)
    end = _parse_date(fact.end)
    if start is None or end is None:
        return None
    return (end - start).days + 1


def _facts_for_concept(us_gaap: dict[str, Any], concept: str, preferred_unit: str = "USD") -> list[Fact]:
    payload = us_gaap.get(concept)
    if not isinstance(payload, dict):
        return []
    units = payload.get("units")
    if not isinstance(units, dict):
        return []
    unit_name = preferred_unit if isinstance(units.get(preferred_unit), list) else next((key for key, value in units.items() if isinstance(value, list)), "")
    raw_facts = units.get(unit_name) if unit_name else []
    if not isinstance(raw_facts, list):
        return []

    facts: list[Fact] = []
    for row in raw_facts:
        if not isinstance(row, dict) or row.get("val") is None:
            continue
        value = row.get("val")
        if not isinstance(value, (int, float)):
            continue
        facts.append(
            Fact(
                concept=concept,
                unit=unit_name,
                value=value,
                start=str(row.get("start") or ""),
                end=str(row.get("end") or ""),
                filed=str(row.get("filed") or ""),
                fy=str(row.get("fy") or ""),
                fp=str(row.get("fp") or ""),
                form=str(row.get("form") or ""),
                accn=str(row.get("accn") or ""),
            )
        )
    return facts


def _dedupe_latest_by_end(facts: Iterable[Fact]) -> list[Fact]:
    latest: dict[str, Fact] = {}
    for fact in facts:
        existing = latest.get(fact.end)
        if existing is None or (fact.filed, fact.accn) > (existing.filed, existing.accn):
            latest[fact.end] = fact
    return sorted(latest.values(), key=lambda item: (item.end, item.filed))


def _select_metric_facts(
    us_gaap: dict[str, Any],
    concepts: tuple[str, ...],
    selector: str,
    limit: int,
) -> tuple[str, list[Fact]]:
    selected_concept = ""
    selected_facts: list[Fact] = []
    for concept in concepts:
        facts = _facts_for_concept(us_gaap, concept)
        if selector == "annual":
            candidates = [
                fact
                for fact in facts
                if fact.form == "10-K" and fact.fp == "FY" and (_duration_days(fact) or 0) >= 300
            ]
        elif selector == "quarter":
            candidates = [
                fact
                for fact in facts
                if fact.form in {"10-Q", "10-K"} and fact.start and 60 <= (_duration_days(fact) or 0) <= 120
            ]
        elif selector == "instant":
            candidates = [fact for fact in facts if not fact.start and fact.form in {"10-Q", "10-K"}]
        else:
            raise ValueError(f"unknown selector: {selector}")
        candidates = _dedupe_latest_by_end(candidates)
        if not candidates:
            continue
        if not selected_facts or (candidates[-1].end, candidates[-1].filed) > (selected_facts[-1].end, selected_facts[-1].filed):
            selected_concept = concept
            selected_facts = candidates
    return selected_concept, selected_facts[-limit:]


def _format_usd(value: int | float | None) -> str:
    if value is None:
        return "-"
    sign = "-" if value < 0 else ""
    value = abs(float(value))
    if value >= 1_000_000_000:
        return f"{sign}${value / 1_000_000_000:,.1f}B"
    if value >= 1_000_000:
        return f"{sign}${value / 1_000_000:,.1f}M"
    return f"{sign}${value:,.0f}"


def _format_pct(numerator: int | float | None, denominator: int | float | None) -> str:
    if numerator is None or denominator in (None, 0):
        return "-"
    return f"{float(numerator) / float(denominator) * 100:,.1f}%"


def _values_by_end(facts: list[Fact]) -> dict[str, Fact]:
    return {fact.end: fact for fact in facts}


def _metric_bundle(us_gaap: dict[str, Any], selector: str, limit: int) -> dict[str, tuple[str, list[Fact]]]:
    source = FLOW_METRICS if selector in {"annual", "quarter"} else INSTANT_METRICS
    return {
        metric: _select_metric_facts(us_gaap, concepts, selector, limit)
        for metric, concepts in source.items()
    }


def _metric_notes(bundle: dict[str, tuple[str, list[Fact]]]) -> list[str]:
    notes: list[str] = []
    for metric, (concept, facts) in bundle.items():
        if not facts:
            notes.append(f"- `{metric}`: no usable SEC companyfacts concept found in the configured alternatives.")
        else:
            notes.append(f"- `{metric}`: `{concept}`; latest end `{facts[-1].end}`, filed `{facts[-1].filed}`.")
    return notes


def render_financials(*, raw_dir: Path, symbol: str, run_date: str, annual_limit: int, quarter_limit: int) -> str:
    companyfacts = _read_json(raw_dir / "companyfacts.raw.json")
    submissions = _read_json(raw_dir / "submissions.raw.json")
    if not isinstance(companyfacts, dict):
        raise ValueError(f"{raw_dir / 'companyfacts.raw.json'}: expected JSON object")
    if not isinstance(submissions, dict):
        submissions = {}
    us_gaap = ((companyfacts.get("facts") or {}).get("us-gaap") or {})
    if not isinstance(us_gaap, dict):
        raise ValueError(f"{raw_dir / 'companyfacts.raw.json'}: expected facts.us-gaap object")

    annual = _metric_bundle(us_gaap, "annual", annual_limit)
    quarterly = _metric_bundle(us_gaap, "quarter", quarter_limit)
    instant = _metric_bundle(us_gaap, "instant", quarter_limit)

    revenue = _values_by_end(annual["revenue"][1])
    operating_income = _values_by_end(annual["operating_income"][1])
    net_income = _values_by_end(annual["net_income"][1])
    ocf = _values_by_end(annual["operating_cash_flow"][1])
    capex = _values_by_end(annual["capex"][1])
    annual_periods = sorted(set(revenue) | set(operating_income) | set(net_income) | set(ocf) | set(capex))[-annual_limit:]

    q_revenue = _values_by_end(quarterly["revenue"][1])
    q_operating_income = _values_by_end(quarterly["operating_income"][1])
    q_net_income = _values_by_end(quarterly["net_income"][1])
    q_ocf = _values_by_end(quarterly["operating_cash_flow"][1])
    q_capex = _values_by_end(quarterly["capex"][1])
    quarter_periods = sorted(set(q_revenue) | set(q_operating_income) | set(q_net_income) | set(q_ocf) | set(q_capex))[-quarter_limit:]

    cash = _values_by_end(instant["cash_and_investments"][1])
    assets = _values_by_end(instant["assets"][1])
    liabilities = _values_by_end(instant["liabilities"][1])
    debt = _values_by_end(instant["debt_proxy"][1])
    equity = _values_by_end(instant["equity"][1])
    balance_periods = sorted(set(cash) | set(assets) | set(liabilities) | set(debt) | set(equity))[-quarter_limit:]

    lines = [
        f"# {symbol.upper()} Financials",
        "",
        "## 메타",
        "",
        f"- Symbol: `{symbol.upper()}`",
        f"- Company: {submissions.get('name') or companyfacts.get('entityName') or '-'}",
        f"- 작성일: `{_now_kst().date().isoformat()}`",
        f"- 기준 원천일: `{run_date}`",
        f"- 원천: `{(raw_dir / 'companyfacts.raw.json').as_posix()}`",
        "- 해석: SEC XBRL companyfacts 기반 재무 요약이며, 투자 추천 또는 주문 의도가 아니다.",
        "- Order intent generated: `false`",
        "",
        "## 연간 실적 요약",
        "",
        "| 기간 종료 | 매출 | 영업이익 | 순이익 | 영업현금흐름 | Capex | Free Cash Flow | 영업이익률 | 순이익률 | FCF margin |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    if annual_periods:
        for period in annual_periods:
            rev = revenue.get(period)
            op = operating_income.get(period)
            ni = net_income.get(period)
            cash_flow = ocf.get(period)
            cap = capex.get(period)
            fcf = cash_flow.value - cap.value if cash_flow and cap else None
            lines.append(
                "| "
                + " | ".join(
                    [
                        period,
                        _format_usd(rev.value if rev else None),
                        _format_usd(op.value if op else None),
                        _format_usd(ni.value if ni else None),
                        _format_usd(cash_flow.value if cash_flow else None),
                        _format_usd(cap.value if cap else None),
                        _format_usd(fcf),
                        _format_pct(op.value if op else None, rev.value if rev else None),
                        _format_pct(ni.value if ni else None, rev.value if rev else None),
                        _format_pct(fcf, rev.value if rev else None),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| - | - | - | - | - | - | - | - | - | - |")

    lines.extend(
        [
            "",
            "## 최근 분기 실적 요약",
            "",
            "| 기간 종료 | 매출 | 영업이익 | 순이익 | 영업현금흐름 | Capex | Free Cash Flow | 영업이익률 | 순이익률 | FCF margin |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    if quarter_periods:
        for period in quarter_periods:
            rev = q_revenue.get(period)
            op = q_operating_income.get(period)
            ni = q_net_income.get(period)
            cash_flow = q_ocf.get(period)
            cap = q_capex.get(period)
            fcf = cash_flow.value - cap.value if cash_flow and cap else None
            lines.append(
                "| "
                + " | ".join(
                    [
                        period,
                        _format_usd(rev.value if rev else None),
                        _format_usd(op.value if op else None),
                        _format_usd(ni.value if ni else None),
                        _format_usd(cash_flow.value if cash_flow else None),
                        _format_usd(cap.value if cap else None),
                        _format_usd(fcf),
                        _format_pct(op.value if op else None, rev.value if rev else None),
                        _format_pct(ni.value if ni else None, rev.value if rev else None),
                        _format_pct(fcf, rev.value if rev else None),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| - | - | - | - | - | - | - | - | - | - |")

    lines.extend(
        [
            "",
            "## 재무상태",
            "",
            "| 기간 종료 | 현금/단기투자 | Debt proxy | 순현금/(순부채 proxy) | 총자산 | 총부채 | 자본 |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    if balance_periods:
        for period in balance_periods:
            cash_fact = cash.get(period)
            debt_fact = debt.get(period)
            net_cash = cash_fact.value - debt_fact.value if cash_fact and debt_fact else None
            lines.append(
                "| "
                + " | ".join(
                    [
                        period,
                        _format_usd(cash_fact.value if cash_fact else None),
                        _format_usd(debt_fact.value if debt_fact else None),
                        _format_usd(net_cash),
                        _format_usd(assets[period].value if period in assets else None),
                        _format_usd(liabilities[period].value if period in liabilities else None),
                        _format_usd(equity[period].value if period in equity else None),
                    ]
                )
                + " |"
            )
    else:
        lines.append("| - | - | - | - | - | - | - |")

    lines.extend(
        [
            "",
            "## XBRL Concept 선택 메모",
            "",
            "### Flow metrics",
            "",
            *_metric_notes(annual),
            "",
            "### Quarterly flow metrics",
            "",
            *_metric_notes(quarterly),
            "",
            "### Balance sheet metrics",
            "",
            *_metric_notes(instant),
            "",
            "## 확인 필요",
            "",
            "- SEC companyfacts는 표준화된 XBRL 숫자만 요약한다. 세그먼트, 가이던스, 리스크 문장은 `sec-filing-sections.md`와 원문 섹션을 같이 읽어야 한다.",
            "- `Debt proxy`는 회사별 부채 태그 차이가 있어 순현금/순부채의 완전한 정의가 아니다. 10-K 주석에서 debt, lease, cash equivalents 정의를 확인해야 한다.",
            "- Capex는 SEC 태그상 현금 유출액을 양수로 기록하는 경우를 기준으로 FCF = 영업현금흐름 - Capex로 계산했다.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    default_run_date = _now_kst().date().isoformat()
    parser = argparse.ArgumentParser(description="Render DI financials.md from SEC companyfacts raw JSON.")
    parser.add_argument("--symbol", required=True, type=_validate_symbol)
    parser.add_argument("--run-date", type=_validate_ymd, default=default_run_date)
    parser.add_argument("--raw-root", type=Path, default=DEFAULT_RAW_ROOT)
    parser.add_argument("--raw-dir", type=Path)
    parser.add_argument("--research-root", type=Path, default=DEFAULT_RESEARCH_ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--annual-limit", type=int, default=5)
    parser.add_argument("--quarter-limit", type=int, default=6)
    args = parser.parse_args()

    raw_dir = args.raw_dir or _raw_dir(args.raw_root, args.run_date, args.symbol)
    output = args.output or _output_path(args.research_root, args.symbol)
    try:
        report = render_financials(raw_dir=raw_dir, symbol=args.symbol, run_date=args.run_date, annual_limit=args.annual_limit, quarter_limit=args.quarter_limit)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
