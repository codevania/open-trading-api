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
