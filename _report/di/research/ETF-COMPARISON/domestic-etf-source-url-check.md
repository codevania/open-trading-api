# Domestic ETF Source URL Check

- Run date: `2026-07-08`
- Scope: Korea-listed S&P 500 ETF candidates in `_report/di/candidates/core-satellite-candidates.yaml`
- Interpretation: source URL verification only; no buy or order intent is generated
- Order intent generated: `false`

## Results

| Symbol | Candidate | Issuer/source check | Result | Source URL |
| --- | --- | --- | --- | --- |
| `360750` | TIGER US S&P500 | Mirae Asset TIGER official page returned HTTP 200 and included `360750`, `TIGER`, and Korean/US product clues. | verified_source_url | https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 |
| `360200` | ACE US S&P500 | ACE ETF official page returned HTTP 200 and included `360200` and `ACE`. | verified_source_url | https://www.aceetf.co.kr/fund/360200 |
| `379800` | KODEX US S&P500TR | Legacy KODEX URL candidate redirected to the KODEX product list, and the official search page did not confirm a product-specific detail page in this check. | unresolved | TODO |

## Next Actions

1. Run ETF source collection for `360750` and `360200` to preserve issuer raw pages under `_report/raw/`.
2. Re-check `379800` through KODEX issuer pages, KRX ETF data, or brokerage product search before filling `source_url`.
3. Keep all three domestic ETF candidates on `hold` until fee, distribution, currency hedge, NAV/liquidity, and tax/account evidence are filled.
