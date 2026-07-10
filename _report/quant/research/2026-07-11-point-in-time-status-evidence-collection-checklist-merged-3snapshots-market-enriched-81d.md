# Point-in-Time Status Evidence Collection Checklist

- Evidence queue rows: [[_report/quant/research/2026-07-10-point-in-time-status-evidence-collection-queue-merged-3snapshots-market-enriched-81d.rows.csv|_report/quant/research/2026-07-10-point-in-time-status-evidence-collection-queue-merged-3snapshots-market-enriched-81d.rows.csv]]
- KIS/KRX API call: `false`
- Order intent generated: `false`
- Backtest readiness impact: `hold`
- Interpretation: operator checklist only, not source coverage evidence

## Summary

| Metric | Value |
| --- | ---: |
| Checklist batches | 33 |
| Pending batches | 33 |
| Queued source rows | 385 |
| Queued code references | 347 |

## Priority Counts

| Priority | Batches |
| --- | ---: |
| `1` | 10 |
| `2` | 18 |
| `3` | 5 |

## Blocker Counts

| Blocker | Batches |
| --- | ---: |
| `market_label_resolution` | 5 |
| `release_resume_evidence` | 18 |
| `source_manifest_evidence` | 10 |

## Status Type Counts

| Status type | Batches |
| --- | ---: |
| `delisting` | 4 |
| `managed_issue` | 10 |
| `market_alert` | 8 |
| `trading_halt` | 11 |

## Collection Status Counts

| Collection status | Batches |
| --- | ---: |
| `pending_market_label_evidence` | 5 |
| `pending_raw_evidence` | 10 |
| `pending_release_resume_evidence` | 18 |

## Market Scope Counts

| Market scope | Batches |
| --- | ---: |
| `KOSDAQ` | 11 |
| `KOSDAQ;KOSPI` | 7 |
| `KOSPI` | 4 |
| `UNKNOWN` | 8 |
| `required_manifest_scope` | 3 |

## Execution Order

1. Complete `P1-*` source manifest evidence first.
2. Complete `P2-*` release/resume evidence after the matching official source coverage is available.
3. Complete `P3-*` market-label evidence only where official evidence or deterministic joins support the label.

## Checklist Batches

## P1 Source Manifest Evidence

### P1-001 `source_manifest_evidence` / `delisting`

- Collection status: `pending_raw_evidence`
- Market scope: `required_manifest_scope`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `kind:Managed issue event;Trading halt or resumption disclosure;Delisting disclosure`
- Manifest source: `kind`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `1`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-001/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

### P1-002 `source_manifest_evidence` / `delisting`

- Collection status: `pending_raw_evidence`
- Market scope: `required_manifest_scope`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `krx_data_marketplace:Designated details of all issues;Market alert issue;Delisting`
- Manifest source: `krx_data_marketplace`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `2`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-002/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

### P1-003 `source_manifest_evidence` / `delisting`

- Collection status: `pending_raw_evidence`
- Market scope: `required_manifest_scope`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `manual_snapshot:Manual download captured from an official KRX or KIND page`
- Manifest source: `manual_snapshot`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `3`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-003/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

### P1-004 `source_manifest_evidence` / `managed_issue`

- Collection status: `pending_raw_evidence`
- Market scope: `KOSDAQ;KOSPI`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `kind:Managed issue event;Trading halt or resumption disclosure;Delisting disclosure`
- Manifest source: `kind`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `4`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-004/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

### P1-005 `source_manifest_evidence` / `managed_issue`

- Collection status: `pending_raw_evidence`
- Market scope: `KOSDAQ;KOSPI`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `krx_data_marketplace:Designated details of all issues;Market alert issue;Delisting`
- Manifest source: `krx_data_marketplace`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `5`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-005/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

### P1-006 `source_manifest_evidence` / `managed_issue`

- Collection status: `pending_raw_evidence`
- Market scope: `KOSDAQ;KOSPI`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `manual_snapshot:Manual download captured from an official KRX or KIND page`
- Manifest source: `manual_snapshot`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `6`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-006/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

### P1-007 `source_manifest_evidence` / `market_alert`

- Collection status: `pending_raw_evidence`
- Market scope: `KOSDAQ;KOSPI`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `krx_data_marketplace:Designated details of all issues;Market alert issue;Delisting`
- Manifest source: `krx_data_marketplace`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `7`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-007/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

### P1-008 `source_manifest_evidence` / `market_alert`

- Collection status: `pending_raw_evidence`
- Market scope: `KOSDAQ;KOSPI`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `manual_snapshot:Manual download captured from an official KRX or KIND page`
- Manifest source: `manual_snapshot`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `8`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-008/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

### P1-009 `source_manifest_evidence` / `trading_halt`

- Collection status: `pending_raw_evidence`
- Market scope: `KOSDAQ;KOSPI`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `kind:Managed issue event;Trading halt or resumption disclosure;Delisting disclosure`
- Manifest source: `kind`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `9`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-009/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

### P1-010 `source_manifest_evidence` / `trading_halt`

- Collection status: `pending_raw_evidence`
- Market scope: `KOSDAQ;KOSPI`
- Source rows: `1`
- Code references: `0`
- Code sample: `not_applicable`
- Suggested source: `manual_snapshot:Manual download captured from an official KRX or KIND page`
- Manifest source: `manual_snapshot`
- Required evidence: `fill source_url, raw_path, and confidence with official raw evidence covering the market-data window`
- Source plan rows: `10`
- Raw path suggestion: `_report/raw/quant/status-evidence/p1-010/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Fill the P1 source-manifest packet, then run fill-progress, materialize, validate, and coverage audit.

## P2 Release/Resume Evidence

### P2-001 `release_resume_evidence` / `managed_issue`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `25`
- Code references: `25`
- Code sample: `001840;008290;016790;023440;024830`
- Suggested source: `krx_data_marketplace;kind;manual_snapshot`
- Manifest source: `krx_data_marketplace;kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `14;19;25;28;29;30;31;32;33;34;36;37;38;39;40;41;42;43;44;45;46;47;48;49;50`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-001/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-002 `release_resume_evidence` / `managed_issue`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `25`
- Code references: `25`
- Code sample: `066790;066900;068240;068940;069920`
- Suggested source: `krx_data_marketplace;kind;manual_snapshot`
- Manifest source: `krx_data_marketplace;kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `51;52;53;54;56;57;58;59;60;61;62;63;64;65;66;67;68;69;71;72;73;74;75;76;77`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-002/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-003 `release_resume_evidence` / `managed_issue`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `25`
- Code references: `25`
- Code sample: `203690;214610;217480;219550;222160`
- Suggested source: `krx_data_marketplace;kind;manual_snapshot`
- Manifest source: `krx_data_marketplace;kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `78;79;80;81;82;83;84;85;86;87;88;89;90;91;92;93;94;95;96;97;98;100;101;103;105`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-003/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-004 `release_resume_evidence` / `managed_issue`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `7`
- Code references: `7`
- Code sample: `377460;380540;393970;412540;418250`
- Suggested source: `krx_data_marketplace;kind;manual_snapshot`
- Manifest source: `krx_data_marketplace;kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `106;107;108;110;111;114;115`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-004/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-005 `release_resume_evidence` / `managed_issue`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSPI`
- Source rows: `18`
- Code references: `18`
- Code sample: `001470;001570;001770;002410;005030`
- Suggested source: `krx_data_marketplace;kind;manual_snapshot`
- Manifest source: `krx_data_marketplace;kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `11;12;13;15;16;17;18;20;21;22;23;24;26;27;35;55;70;102`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-005/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-006 `release_resume_evidence` / `managed_issue`

- Collection status: `pending_release_resume_evidence`
- Market scope: `UNKNOWN`
- Source rows: `6`
- Code references: `6`
- Code sample: `309710;373790;397420;424460;454180`
- Suggested source: `krx_data_marketplace;kind;manual_snapshot`
- Manifest source: `krx_data_marketplace;kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `99;104;109;112;113;116`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-006/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-007 `release_resume_evidence` / `market_alert`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `25`
- Code references: `25`
- Code sample: `001000;008290;026910;032860;033540`
- Suggested source: `krx_data_marketplace;manual_snapshot`
- Manifest source: `krx_data_marketplace;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `118;125;133;134;135;137;138;139;140;141;142;143;144;145;146;147;148;149;150;152;153;154;156;157;158`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-007/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-008 `release_resume_evidence` / `market_alert`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `25`
- Code references: `25`
- Code sample: `121440;122350;123750;127120;142760`
- Suggested source: `krx_data_marketplace;manual_snapshot`
- Manifest source: `krx_data_marketplace;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `159;160;161;162;163;164;165;166;167;168;169;170;172;173;174;175;176;177;178;179;180;182;183;184;185`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-008/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-009 `release_resume_evidence` / `market_alert`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `7`
- Code references: `7`
- Code sample: `368970;372800;377030;419080;424980`
- Suggested source: `krx_data_marketplace;manual_snapshot`
- Manifest source: `krx_data_marketplace;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `186;187;188;189;190;191;192`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-009/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-010 `release_resume_evidence` / `market_alert`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSPI`
- Source rows: `18`
- Code references: `18`
- Code sample: `000890;001210;001420;002870;002990`
- Suggested source: `krx_data_marketplace;manual_snapshot`
- Manifest source: `krx_data_marketplace;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `117;119;120;121;122;123;124;126;127;128;129;130;131;132;136;151;181;194`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-010/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-011 `release_resume_evidence` / `market_alert`

- Collection status: `pending_release_resume_evidence`
- Market scope: `UNKNOWN`
- Source rows: `3`
- Code references: `3`
- Code sample: `092590;217880;463020`
- Suggested source: `krx_data_marketplace;manual_snapshot`
- Manifest source: `krx_data_marketplace;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `155;171;193`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-011/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-012 `release_resume_evidence` / `trading_halt`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `25`
- Code references: `25`
- Code sample: `001840;002680;007720;009730;016790`
- Suggested source: `kind;manual_snapshot`
- Manifest source: `kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `202;205;211;215;221;224;226;227;228;230;231;232;233;234;235;236;237;238;239;240;241;242;243;244;246`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-012/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-013 `release_resume_evidence` / `trading_halt`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `25`
- Code references: `25`
- Code sample: `060230;060240;064090;065150;065420`
- Suggested source: `kind;manual_snapshot`
- Manifest source: `kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `247;248;249;250;251;252;253;254;255;256;258;260;261;262;263;264;265;266;267;269;270;273;274;275;276`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-013/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-014 `release_resume_evidence` / `trading_halt`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `25`
- Code references: `25`
- Code sample: `210120;214610;217480;234920;241820`
- Suggested source: `kind;manual_snapshot`
- Manifest source: `kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `277;280;281;284;286;287;288;289;290;291;293;294;299;300;301;303;304;305;307;309;311;313;314;315;316`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-014/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-015 `release_resume_evidence` / `trading_halt`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSDAQ`
- Source rows: `8`
- Code references: `8`
- Code sample: `393970;412540;418250;446840;465320`
- Suggested source: `kind;manual_snapshot`
- Manifest source: `kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `317;318;319;320;321;322;323;324`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-015/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-016 `release_resume_evidence` / `trading_halt`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSPI`
- Source rows: `25`
- Code references: `25`
- Code sample: `000040;000300;001470;001520;001525`
- Suggested source: `kind;manual_snapshot`
- Manifest source: `kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `195;196;197;198;199;200;201;203;204;206;207;208;209;210;212;213;214;217;218;219;220;222;223;225;229`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-016/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-017 `release_resume_evidence` / `trading_halt`

- Collection status: `pending_release_resume_evidence`
- Market scope: `KOSPI`
- Source rows: `8`
- Code references: `8`
- Code sample: `057050;069460;074610;119650;143210`
- Suggested source: `kind;manual_snapshot`
- Manifest source: `kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `245;257;259;268;271;272;279;312`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-017/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

### P2-018 `release_resume_evidence` / `trading_halt`

- Collection status: `pending_release_resume_evidence`
- Market scope: `UNKNOWN`
- Source rows: `14`
- Code references: `14`
- Code sample: `0099X0;212310;222670;232530;238500`
- Suggested source: `kind;manual_snapshot`
- Manifest source: `kind;manual_snapshot`
- Required evidence: `official release/resume, cleared, delisting withdrawal, or other dated inactive-state evidence for this code/status group`
- Source plan rows: `216;278;282;283;285;292;295;296;297;298;302;306;308;310`
- Raw path suggestion: `_report/raw/quant/status-evidence/p2-018/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Extract dated release/resume or cleared-state events, then validate and replay the expanded status events.

## P3 Market Label Evidence

### P3-001 `market_label_resolution` / `delisting`

- Collection status: `pending_market_label_evidence`
- Market scope: `UNKNOWN`
- Source rows: `9`
- Code references: `9`
- Code sample: `149300;238170;257990;288490;308700`
- Suggested source: `kind`
- Manifest source: `krx_data_marketplace;kind;manual_snapshot`
- Required evidence: `official market label, listing status, or deterministic local market-data join evidence for this code`
- Source plan rows: `325;326;327;328;329;330;331;332;333`
- Raw path suggestion: `_report/raw/quant/status-evidence/p3-001/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Resolve market labels only with official evidence or deterministic local joins, then rerun market enrichment.

### P3-002 `market_label_resolution` / `managed_issue`

- Collection status: `pending_market_label_evidence`
- Market scope: `UNKNOWN`
- Source rows: `6`
- Code references: `6`
- Code sample: `309710;373790;397420;424460;454180`
- Suggested source: `kind`
- Manifest source: `krx_data_marketplace;kind;manual_snapshot`
- Required evidence: `official market label, listing status, or deterministic local market-data join evidence for this code`
- Source plan rows: `334;335;336;337;338;339`
- Raw path suggestion: `_report/raw/quant/status-evidence/p3-002/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Resolve market labels only with official evidence or deterministic local joins, then rerun market enrichment.

### P3-003 `market_label_resolution` / `market_alert`

- Collection status: `pending_market_label_evidence`
- Market scope: `UNKNOWN`
- Source rows: `4`
- Code references: `3`
- Code sample: `092590;217880;463020`
- Suggested source: `kind`
- Manifest source: `krx_data_marketplace;manual_snapshot`
- Required evidence: `official market label, listing status, or deterministic local market-data join evidence for this code`
- Source plan rows: `340;341;342;343`
- Raw path suggestion: `_report/raw/quant/status-evidence/p3-003/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Resolve market labels only with official evidence or deterministic local joins, then rerun market enrichment.

### P3-004 `market_label_resolution` / `trading_halt`

- Collection status: `pending_market_label_evidence`
- Market scope: `UNKNOWN`
- Source rows: `25`
- Code references: `9`
- Code sample: `0099X0;212310`
- Suggested source: `kind`
- Manifest source: `kind;manual_snapshot`
- Required evidence: `official market label, listing status, or deterministic local market-data join evidence for this code`
- Source plan rows: `344;345;346;347;348;349;350;351;352;353;354;355;356;357;358;359;360;361;362;363;364;365;366;367;368`
- Raw path suggestion: `_report/raw/quant/status-evidence/p3-004/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Resolve market labels only with official evidence or deterministic local joins, then rerun market enrichment.

### P3-005 `market_label_resolution` / `trading_halt`

- Collection status: `pending_market_label_evidence`
- Market scope: `UNKNOWN`
- Source rows: `17`
- Code references: `6`
- Code sample: `266350;267080`
- Suggested source: `kind`
- Manifest source: `kind;manual_snapshot`
- Required evidence: `official market label, listing status, or deterministic local market-data join evidence for this code`
- Source plan rows: `369;370;371;372;373;374;375;376;377;378;379;380;381;382;383;384;385`
- Raw path suggestion: `_report/raw/quant/status-evidence/p3-005/`
- [ ] Open the suggested official source or deterministic local evidence path.
- [ ] Capture the raw response, downloaded file, screenshot metadata, or deterministic join evidence under the suggested raw directory.
- [ ] Record source URL, raw path, confidence, capture date, and extraction notes in the follow-up evidence artifact before promotion.
- [ ] Next validation: Resolve market labels only with official evidence or deterministic local joins, then rerun market enrichment.

## Guardrails

- This checklist is not a source coverage manifest.
- Do not pass checklist or queue rows to the coverage audit as evidence.
- Keep `Backtest readiness` at `hold` until official raw capture, manifest validation, coverage audit, lifecycle coverage, costs, OOS, and Bias Control pass.
