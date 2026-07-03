from __future__ import annotations

import unittest

from scripts.quant_kind_status_source_probe import (
    KindStatusSpec,
    build_download_payload,
    classify_download_response,
    extract_download_definition,
    extract_form_defaults,
)


class QuantKindStatusSourceProbeTest(unittest.TestCase):
    def test_extract_form_defaults_uses_search_form_only(self) -> None:
        html = """
        <form id="AKCFrm">
          <input type="hidden" name="method" value="topSearch"/>
        </form>
        <form id="searchForm">
          <input type="hidden" name="method" value=""/>
          <input type="hidden" name="searchFromDate" value="2026-07-02"/>
          <input type="text" name="startDate" value=""/>
          <input type="text" name="endDate" value=""/>
          <input type="radio" name="marketType" value=""/>
          <input type="radio" name="marketType" value="2" checked="checked"/>
          <select name="currentPageSize">
            <option value="15">15</option>
            <option value="30" selected="selected">30</option>
          </select>
        </form>
        """

        defaults = extract_form_defaults(html, capture_date="2026-07-03")

        self.assertEqual(defaults["method"], "")
        self.assertEqual(defaults["startDate"], "2026-07-03")
        self.assertEqual(defaults["endDate"], "2026-07-03")
        self.assertEqual(defaults["marketType"], "2")
        self.assertEqual(defaults["currentPageSize"], "30")

    def test_extract_download_definition_reads_action_method_and_forwards(self) -> None:
        html = """
        <script>
        function fnDownload(){
          $("#searchForm > #forward").val("one_down");
          $("#searchForm > #forward").val("two_down");
          $("#searchForm > #method").val("searchSub");
          $("#searchForm").attr('action', '/investwarn/sample.do').submit();
        }
        </script>
        """

        definition = extract_download_definition(html)

        self.assertEqual(definition.action, "/investwarn/sample.do")
        self.assertEqual(definition.methods, ["searchSub"])
        self.assertEqual(definition.forwards, ["one_down", "two_down"])

    def test_build_download_payload_overrides_runtime_fields(self) -> None:
        spec = KindStatusSpec(
            slug="market_alert_warning",
            label="Market alert warning",
            status_type_hint="market_alert",
            page_path="/page",
            post_path="/post",
            download_method="investattentwarnriskySub",
            download_forward="invstwarnisu_down",
            extra_fields={"menuIndex": "2"},
        )
        html = """
        <form id="searchForm">
          <input type="hidden" name="method" value=""/>
          <input type="hidden" name="forward" value=""/>
          <input type="hidden" name="menuIndex" value="1"/>
          <input type="text" name="startDate" value=""/>
          <input type="text" name="endDate" value=""/>
        </form>
        """

        payload = build_download_payload(spec, html, "2026-07-03")

        self.assertEqual(payload["method"], "investattentwarnriskySub")
        self.assertEqual(payload["forward"], "invstwarnisu_down")
        self.assertEqual(payload["menuIndex"], "2")
        self.assertEqual(payload["currentPageSize"], "3000")
        self.assertEqual(payload["startDate"], "2026-07-03")

    def test_classify_excel_html_table_download(self) -> None:
        content = b"<html><table><tr><th>A</th></tr><tr><td>1</td></tr></table></html>"

        result = classify_download_response(
            200,
            "application/vnd.ms-excel; charset=EUC-KR",
            "attachment; filename=test.xls",
            content,
        )

        self.assertEqual(result["classification"], "ok_table_download")
        self.assertEqual(result["filename"], "test.xls")
        self.assertEqual(result["table_count"], 1)
        self.assertEqual(result["table_tr_count"], 2)

    def test_classify_html_without_table(self) -> None:
        result = classify_download_response(200, "text/html", "", b"<html><body>No table</body></html>")

        self.assertEqual(result["classification"], "html_without_table")
        self.assertEqual(result["table_count"], 0)


if __name__ == "__main__":
    unittest.main()
