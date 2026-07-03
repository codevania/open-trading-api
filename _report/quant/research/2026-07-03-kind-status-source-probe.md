# KIND Status Source Probe

- Capture date: `2026-07-03`
- Source: `KIND` public status pages
- Raw manifest: [[_report/raw/2026/2026-07-03/kind/status-source-probe.raw.json|_report/raw/2026/2026-07-03/kind/status-source-probe.raw.json]]
- OK table downloads: `6/7`
- Interpretation: official current/status download evidence; not historical Point-in-Time coverage by itself
- Backtest readiness: `hold`

## Results

| Status source | Hint | Method | Forward | Classification | Filename | Bytes | Tables | TR tags | Raw |
| --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| Managed issue | `managed_issue` | `searchAdminIssueSub` | `adminissue_down` | `ok_table_download` | `관리종목.xls` | 27512 | 1 | 105 | [[_report/raw/2026/2026-07-03/kind/status-source-probe/managed_issue.xls|_report/raw/2026/2026-07-03/kind/status-source-probe/managed_issue.xls]] |
| KOSDAQ watchlist issue | `managed_issue` | `searchHwangiIssueSub` | `hwangiissue_down` | `html_without_table` | `` | 5707 | 0 | 0 | [[_report/raw/2026/2026-07-03/kind/status-source-probe/watchlist_issue.html|_report/raw/2026/2026-07-03/kind/status-source-probe/watchlist_issue.html]] |
| Trading halt | `trading_halt` | `searchTradingHaltIssueSub` | `tradinghaltissue_down` | `ok_table_download` | `매매거래정지종목.xls` | 29885 | 1 | 127 | [[_report/raw/2026/2026-07-03/kind/status-source-probe/trading_halt.xls|_report/raw/2026/2026-07-03/kind/status-source-probe/trading_halt.xls]] |
| Delisted company | `delisting` | `searchDelCompanySub` | `delcompany_down` | `ok_table_download` | `상장폐지현황.xls` | 19711 | 1 | 63 | [[_report/raw/2026/2026-07-03/kind/status-source-probe/delisted_company.xls|_report/raw/2026/2026-07-03/kind/status-source-probe/delisted_company.xls]] |
| Market alert caution | `market_alert` | `investattentwarnriskySub` | `invstcautnisu_down` | `ok_table_download` | `투자주의종목.xls` | 12232 | 1 | 41 | [[_report/raw/2026/2026-07-03/kind/status-source-probe/market_alert_caution.xls|_report/raw/2026/2026-07-03/kind/status-source-probe/market_alert_caution.xls]] |
| Market alert warning | `market_alert` | `investattentwarnriskySub` | `invstwarnisu_down` | `ok_table_download` | `투자경고종목.xls` | 5552 | 1 | 17 | [[_report/raw/2026/2026-07-03/kind/status-source-probe/market_alert_warning.xls|_report/raw/2026/2026-07-03/kind/status-source-probe/market_alert_warning.xls]] |
| Market alert risk | `market_alert` | `investattentwarnriskySub` | `invstriskisu_down` | `ok_table_download` | `투자위험종목.xls` | 988 | 1 | 2 | [[_report/raw/2026/2026-07-03/kind/status-source-probe/market_alert_risk.xls|_report/raw/2026/2026-07-03/kind/status-source-probe/market_alert_risk.xls]] |

## Guardrails

- Treat these as source-availability probes until normalized event rows pass validation.
- `TR tags` are raw HTML table row tags, not confirmed investable-code event rows.
- Historical `Backtest` remains blocked until the selected date range has reproducible status coverage.
- If a source returns `html_without_table`, inspect the raw file before using it for normalization.
