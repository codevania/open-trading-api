# Local KIS Trading MCP run files

1. Open `.env.kis` and fill in your KIS API/account values.
2. Start Docker Desktop.
3. Run `run-kis-trade-mcp.bat`.
4. Check `http://localhost:3000/sse`.

Useful scripts:

- `build-kis-trade-mcp.bat`: rebuilds the Docker image.
- `run-kis-trade-mcp.bat`: starts the MCP container on port 3000.
- `logs-kis-trade-mcp.bat`: follows container logs.
- `status-kis-trade-mcp.bat`: shows container status.
- `stop-kis-trade-mcp.bat`: stops the container.

Claude Desktop MCP config:

```json
{
  "mcpServers": {
    "kis-trade-mcp": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "http://localhost:3000/sse"]
    }
  }
}
```

Codex MCP config:

This repo is registered globally in Codex as `kis_trade_mcp` with:

```powershell
codex mcp add kis_trade_mcp -- `
  "C:\Users\codevania\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe" `
  run -i --rm `
  --env-file "F:\Github\open-trading-api\MCP\Kis Trading MCP\.env.kis" `
  -e MCP_TYPE=stdio `
  -e MCP_HOST=localhost `
  -e MCP_PORT=3000 `
  -e MCP_PATH=/sse `
  --entrypoint uv `
  kis-trade-mcp:latest `
  run python server.py
```

Confirm it with:

```powershell
codex mcp list
codex mcp get kis_trade_mcp
```

## Codex App troubleshooting notes

- If `codex mcp list` shows `kis_trade_mcp` as `enabled` but the current Codex App thread does not expose `mcp__kis_trade_mcp__...` tools, treat it as a session tool-surface issue, not missing registration. Start a fresh Codex App thread or restart the app so MCP metadata is loaded into the tool surface.
- The KIS Trading MCP registers category tools such as `domestic_stock` and `overseas_stock`. `find_api_detail` is an `api_type` passed to that category tool, not a separate top-level tool name.
- For daily-report automation while direct MCP tools are not exposed, keep using `scripts/daily_report_collect.py`. It writes `preflight_find_api_detail.json` from the repo-local MCP configs before live data calls, then stores the raw KIS responses under `_report/raw/YYYY/YYYY-MM-DD/`.
- If `uv run` fails with a Windows cache permission error under `C:\Users\...\AppData\Local\uv\cache`, run uv through the repo-local cache wrapper:

```powershell
.\scripts\uv-workspace.ps1 run python scripts\daily_report_collect.py --run-date 2026-07-03 --raw-dir _report\raw\2026\2026-07-03
```
