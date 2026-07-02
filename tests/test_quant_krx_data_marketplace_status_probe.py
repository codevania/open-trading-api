from __future__ import annotations

import unittest

from scripts.quant_krx_data_marketplace_status_probe import (
    classify_json_response,
    extract_screen_definition,
    parse_menu_results,
)


class QuantKrxDataMarketplaceStatusProbeTest(unittest.TestCase):
    def test_parse_menu_results_preserves_screen_metadata(self) -> None:
        payload = {
            "result": [
                {
                    "org_menu_nm": ["전종목 지정내역"],
                    "menu_nm": ["통계 > 기본 통계 > 주식 > 종목정보 > 전종목 지정내역"],
                    "scren_no": ["12006"],
                    "scren_url": ["/contents/MDC/STAT/standard/MDCSTAT020.jsp"],
                    "menu_id": ["MDC0201020202"],
                    "scren_id": ["MDCSTAT020"],
                }
            ]
        }

        results = parse_menu_results("전종목 지정내역", payload)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].screen_id, "MDCSTAT020")
        self.assertEqual(results[0].screen_url, "/contents/MDC/STAT/standard/MDCSTAT020.jsp")

    def test_extract_screen_definition_reads_defaults_and_blds(self) -> None:
        html = """
        <form name="MDCSTAT020_FORM" id="MDCSTAT020_FORM">
          <input type="hidden" name="locale" value="ko_KR"/>
          <input type="radio" name="mktId" value="ALL" checked>
          <input type="radio" name="mktId" value="STK">
          <script>
            grid: [{ bld: 'dbms/MDC/STAT/standard/MDCSTAT02001', bldDataKey: 'OutBlock_1' }]
          </script>
        </form>
        """

        definition = extract_screen_definition("/contents/MDC/STAT/standard/MDCSTAT020.jsp", html)

        self.assertEqual(definition.form_id, "MDCSTAT020_FORM")
        self.assertEqual(definition.defaults, {"locale": "ko_KR", "mktId": "ALL"})
        self.assertEqual(definition.blds, ["dbms/MDC/STAT/standard/MDCSTAT02001"])
        self.assertEqual(definition.bld_data_keys, ["OutBlock_1"])

    def test_classify_logout_as_auth_required(self) -> None:
        result = classify_json_response(400, "text/plain", "LOGOUT", None)

        self.assertEqual(result["status"], "auth_required")
        self.assertIsNone(result["row_count"])

    def test_classify_outblock_rows(self) -> None:
        result = classify_json_response(200, "application/json", "{}", {"OutBlock_1": [{"A": "1"}, {"A": "2"}]})

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["row_count"], 2)

    def test_classify_screen_specific_output_rows(self) -> None:
        result = classify_json_response(200, "application/json", "{}", {"output": [{"A": "1"}]}, ["output"])

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["row_count"], 1)


if __name__ == "__main__":
    unittest.main()
