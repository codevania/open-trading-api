from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.quant_kis_demo_order_preflight import validate_order_intents


FIELDS = (
    "env_dv",
    "dry_run",
    "order_side",
    "code",
    "quantity",
    "limit_price_krw",
    "order_type",
    "source_strategy",
)


def _write_csv(path: Path, rows: list[dict[str, str]], fields: tuple[str, ...] = FIELDS) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _intent(**overrides: str) -> dict[str, str]:
    row = {
        "env_dv": "demo",
        "dry_run": "true",
        "order_side": "buy",
        "code": "005930",
        "quantity": "1",
        "limit_price_krw": "70000",
        "order_type": "limit",
        "source_strategy": "unit-test",
    }
    row.update(overrides)
    return row


class QuantKisDemoOrderPreflightTest(unittest.TestCase):
    def test_accepts_one_share_demo_limit_buy_intent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "intents.csv"
            _write_csv(path, [_intent()])

            results, summary = validate_order_intents(path)

        self.assertTrue(results[0].valid)
        self.assertEqual(results[0].order_value_krw, 70000)
        self.assertEqual(summary["valid_rows"], 1)
        self.assertEqual(summary["invalid_rows"], 0)

    def test_rejects_real_or_non_dry_run_or_large_orders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "intents.csv"
            _write_csv(
                path,
                [
                    _intent(env_dv="real"),
                    _intent(dry_run="false"),
                    _intent(quantity="2"),
                    _intent(limit_price_krw="200000"),
                ],
            )

            results, summary = validate_order_intents(path)

        self.assertEqual(summary["valid_rows"], 0)
        self.assertIn("env_dv must be demo", results[0].errors)
        self.assertIn("dry_run must be true", results[1].errors)
        self.assertIn("quantity must be <= 1", results[2].errors)
        self.assertIn("order_value_krw must be <= 100000", results[3].errors)

    def test_rejects_sell_until_position_check_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "intents.csv"
            _write_csv(path, [_intent(order_side="sell")])

            results, _summary = validate_order_intents(path)

        self.assertFalse(results[0].valid)
        self.assertIn("sell intents require a separate demo position check", results[0].errors)

    def test_rejects_missing_required_columns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            _write_csv(path, [{"env_dv": "demo"}], fields=("env_dv",))

            with self.assertRaisesRegex(ValueError, "missing required columns"):
                validate_order_intents(path)


if __name__ == "__main__":
    unittest.main()
