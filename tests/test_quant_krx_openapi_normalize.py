from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NORMALIZE = REPO_ROOT / "scripts" / "quant_krx_openapi_normalize.py"


def _write_raw(path: Path, rows: list[dict[str, str]]) -> None:
    path.write_text(json.dumps({"OutBlock_1": rows}, ensure_ascii=False), encoding="utf-8")


class QuantKrxOpenapiNormalizeTest(unittest.TestCase):
    def test_normalizes_core_raw_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw"
            out_dir = root / "normalized"
            raw_dir.mkdir()
            _write_raw(
                raw_dir / "kospi_stock_daily_20250102.raw.json",
                [
                    {
                        "BAS_DD": "20250102",
                        "ISU_CD": "005930",
                        "ISU_NM": "Samsung Electronics",
                        "MKT_NM": "KOSPI",
                        "SECT_TP_NM": "",
                        "TDD_CLSPRC": "53,400",
                        "CMPPREVDD_PRC": "100",
                        "FLUC_RT": "0.19",
                        "TDD_OPNPRC": "53,000",
                        "TDD_HGPRC": "54,000",
                        "TDD_LWPRC": "52,900",
                        "ACC_TRDVOL": "12,345",
                        "ACC_TRDVAL": "659,223,000",
                        "MKTCAP": "318,000,000,000,000",
                        "LIST_SHRS": "5,969,782,550",
                    }
                ],
            )
            _write_raw(
                raw_dir / "kospi_issue_base_20250102.raw.json",
                [
                    {
                        "ISU_CD": "KR7005930003",
                        "ISU_SRT_CD": "005930",
                        "ISU_NM": "Samsung Electronics Common",
                        "ISU_ABBRV": "Samsung Electronics",
                        "ISU_ENG_NM": "Samsung Electronics Co., Ltd.",
                        "LIST_DD": "19750611",
                        "MKT_TP_NM": "KOSPI",
                        "SECUGRP_NM": "Stock",
                        "SECT_TP_NM": "",
                        "KIND_STKCERT_TP_NM": "Common",
                        "PARVAL": "100",
                        "LIST_SHRS": "5,969,782,550",
                    }
                ],
            )
            _write_raw(
                raw_dir / "kospi_index_daily_20250102.raw.json",
                [
                    {
                        "BAS_DD": "20250102",
                        "IDX_CLSS": "KOSPI",
                        "IDX_NM": "KOSPI",
                        "CLSPRC_IDX": "2,398.94",
                        "CMPPREVDD_IDX": "0.50",
                        "FLUC_RT": "0.02",
                        "OPNPRC_IDX": "2,400.00",
                        "HGPRC_IDX": "2,410.00",
                        "LWPRC_IDX": "2,390.00",
                        "ACC_TRDVOL": "123,456",
                        "ACC_TRDVAL": "1,000,000,000",
                        "MKTCAP": "2,000,000,000,000,000",
                    }
                ],
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(NORMALIZE),
                    "--raw-dir",
                    str(raw_dir),
                    "--bas-dd",
                    "20250102",
                    "--output-dir",
                    str(out_dir),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("| `stock_daily` | 1 |", result.stdout)
            with (out_dir / "stock_daily.csv").open("r", encoding="utf-8-sig", newline="") as handle:
                stock_rows = list(csv.DictReader(handle))
            with (out_dir / "issue_base.csv").open("r", encoding="utf-8-sig", newline="") as handle:
                issue_rows = list(csv.DictReader(handle))
            with (out_dir / "index_daily.csv").open("r", encoding="utf-8-sig", newline="") as handle:
                index_rows = list(csv.DictReader(handle))

            self.assertEqual(stock_rows[0]["date"], "2025-01-02")
            self.assertEqual(stock_rows[0]["code"], "005930")
            self.assertEqual(stock_rows[0]["close"], "53400")
            self.assertEqual(stock_rows[0]["trading_value_krw"], "659223000")
            self.assertEqual(issue_rows[0]["standard_code"], "KR7005930003")
            self.assertEqual(issue_rows[0]["code"], "005930")
            self.assertEqual(issue_rows[0]["listing_date"], "1975-06-11")
            self.assertEqual(index_rows[0]["index_class"], "KOSPI")
            self.assertEqual(index_rows[0]["close"], "2398.94")

    def test_rejects_unknown_service_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            raw_dir = Path(tmp)
            _write_raw(raw_dir / "unknown_service_20250102.raw.json", [])

            result = subprocess.run(
                [sys.executable, str(NORMALIZE), "--raw-dir", str(raw_dir)],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsupported service id", result.stderr)

    def test_invalid_bas_dd_filter_fails(self) -> None:
        result = subprocess.run(
            [sys.executable, str(NORMALIZE), "--raw-dir", ".", "--bas-dd", "2025-01-02"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--bas-dd must be YYYYMMDD", result.stderr)


if __name__ == "__main__":
    unittest.main()
