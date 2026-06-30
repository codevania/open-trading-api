from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples_llm"
MCP_CONFIGS = ROOT / "MCP" / "Kis Trading MCP" / "configs"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def dataframe_records(value: Any) -> Any:
    if isinstance(value, pd.DataFrame):
        return value.to_dict("records")
    if isinstance(value, tuple):
        return {f"output{i + 1}": dataframe_records(item) for i, item in enumerate(value)}
    return value


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def api_detail(tool_name: str, api_type: str) -> dict[str, Any]:
    config = json.loads((MCP_CONFIGS / f"{tool_name}.json").read_text(encoding="utf-8"))
    apis = config.get("apis", {})
    if api_type not in apis:
        return {
            "ok": False,
            "error": f"지원하지 않는 API 타입: {api_type}",
            "available_apis": sorted(apis),
        }
    api_info = apis[api_type]
    params = {}
    for param_name, param_info in api_info.get("params", {}).items():
        params[param_name] = {
            "name": param_info.get("name", param_name),
            "type": param_info.get("type", "str"),
            "required": param_info.get("required", False),
            "default_value": param_info.get("default_value"),
            "description": param_info.get("description", ""),
        }
    return {
        "ok": True,
        "data": {
            "tool_name": tool_name,
            "api_type": api_type,
            "name": api_info.get("name", ""),
            "category_detail": api_info.get("category", ""),
            "method": api_info.get("method", ""),
            "api_path": api_info.get("api_path", ""),
            "github_url": api_info.get("github_url", ""),
            "params": params,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-date", required=True)
    parser.add_argument("--raw-dir", required=True)
    args = parser.parse_args()

    run_date = datetime.strptime(args.run_date, "%Y-%m-%d").date()
    date_ymd = run_date.strftime("%Y%m%d")
    start_ymd = (run_date - timedelta(days=75)).strftime("%Y%m%d")
    raw_dir = (ROOT / args.raw_dir).resolve()
    raw_dir.mkdir(parents=True, exist_ok=True)

    preflight = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": "repo-local MCP config equivalent of find_api_detail",
        "domestic_stock": {
            api: api_detail("domestic_stock", api)
            for api in [
                "find_stock_code",
                "inquire_price",
                "inquire_daily_itemchartprice",
                "investor_trade_by_stock_daily",
                "news_title",
            ]
        },
        "overseas_stock": {
            api: api_detail("overseas_stock", api)
            for api in ["price", "dailyprice"]
        },
    }
    save_json(raw_dir / "preflight_find_api_detail.json", preflight)

    sys.path.insert(0, str(EXAMPLES))
    ka = load_module("kis_auth", EXAMPLES / "kis_auth.py")
    ka.auth()

    inquire_price = load_module(
        "daily_inquire_price",
        EXAMPLES / "domestic_stock" / "inquire_price" / "inquire_price.py",
    ).inquire_price
    inquire_daily = load_module(
        "daily_inquire_daily_itemchartprice",
        EXAMPLES / "domestic_stock" / "inquire_daily_itemchartprice" / "inquire_daily_itemchartprice.py",
    ).inquire_daily_itemchartprice
    investor_flow = load_module(
        "daily_investor_trade_by_stock_daily",
        EXAMPLES / "domestic_stock" / "investor_trade_by_stock_daily" / "investor_trade_by_stock_daily.py",
    ).investor_trade_by_stock_daily
    overseas_price = load_module(
        "daily_overseas_price",
        EXAMPLES / "overseas_stock" / "price" / "price.py",
    ).price
    overseas_dailyprice = load_module(
        "daily_overseas_dailyprice",
        EXAMPLES / "overseas_stock" / "dailyprice" / "dailyprice.py",
    ).dailyprice

    domestic_symbols = {
        "005930": {"market": "KRX", "name": "삼성전자"},
        "000660": {"market": "KRX", "name": "SK하이닉스"},
        "402340": {"market": "KRX", "name": "SK스퀘어"},
        "011790": {"market": "KRX", "name": "SKC"},
        "011070": {"market": "KRX", "name": "LG이노텍"},
        "009150": {"market": "KRX", "name": "삼성전기"},
        "454910": {"market": "KRX", "name": "두산로보틱스"},
    }
    overseas_symbols = {
        "NAS_NVDA": {"market": "NASDAQ", "name": "NVIDIA", "exchange_code": "NAS", "code": "NVDA"},
    }
    summary: dict[str, Any] = {
        "run_date": args.run_date,
        "raw_dir": str(raw_dir),
        "preflight": "preflight_find_api_detail.json saved before live calls",
        "symbols": {},
    }

    for code, meta in domestic_symbols.items():
        symbol_dir = raw_dir / code
        calls: dict[str, Any] = {}
        try:
            result = inquire_price("real", "J", code)
            records = dataframe_records(result)
            save_json(symbol_dir / "inquire_price.json", records)
            calls["inquire_price"] = {"ok": True, "rows": len(records)}
        except Exception as exc:
            save_json(symbol_dir / "inquire_price.json", {"ok": False, "error": str(exc)})
            calls["inquire_price"] = {"ok": False, "error": str(exc)}

        try:
            result = inquire_daily("real", "J", code, start_ymd, date_ymd, "D", "0")
            records = dataframe_records(result)
            save_json(symbol_dir / "inquire_daily_itemchartprice.json", records)
            calls["inquire_daily_itemchartprice"] = {
                "ok": True,
                "rows1": len(records.get("output1", [])),
                "rows2": len(records.get("output2", [])),
            }
        except Exception as exc:
            save_json(symbol_dir / "inquire_daily_itemchartprice.json", {"ok": False, "error": str(exc)})
            calls["inquire_daily_itemchartprice"] = {"ok": False, "error": str(exc)}

        try:
            result = investor_flow("J", code, date_ymd, "", "", max_depth=3)
            records = dataframe_records(result)
            save_json(symbol_dir / "investor_trade_by_stock_daily.json", records)
            calls["investor_trade_by_stock_daily"] = {
                "ok": True,
                "rows1": len(records.get("output1", [])),
                "rows2": len(records.get("output2", [])),
            }
        except Exception as exc:
            save_json(symbol_dir / "investor_trade_by_stock_daily.json", {"ok": False, "error": str(exc)})
            calls["investor_trade_by_stock_daily"] = {"ok": False, "error": str(exc)}

        summary["symbols"][code] = {**meta, "calls": calls}

    for symbol_key, meta in overseas_symbols.items():
        symbol_dir = raw_dir / symbol_key
        calls = {}
        try:
            result = overseas_price("", meta["exchange_code"], meta["code"], "real")
            records = dataframe_records(result)
            save_json(symbol_dir / "price.json", records)
            calls["price"] = {"ok": True, "rows": len(records)}
        except Exception as exc:
            save_json(symbol_dir / "price.json", {"ok": False, "error": str(exc)})
            calls["price"] = {"ok": False, "error": str(exc)}

        try:
            result = overseas_dailyprice("", meta["exchange_code"], meta["code"], "0", date_ymd, "0", "real", max_depth=2)
            records = dataframe_records(result)
            save_json(symbol_dir / "dailyprice.json", records)
            calls["dailyprice"] = {
                "ok": True,
                "rows1": len(records.get("output1", [])),
                "rows2": len(records.get("output2", [])),
            }
        except Exception as exc:
            save_json(symbol_dir / "dailyprice.json", {"ok": False, "error": str(exc)})
            calls["dailyprice"] = {"ok": False, "error": str(exc)}

        summary["symbols"]["NAS:NVDA"] = {**meta, "calls": calls}

    save_json(raw_dir / "collection_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
