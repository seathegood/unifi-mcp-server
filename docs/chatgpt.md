# ChatGPT Integration

This project uses FastMCP and can be connected to ChatGPT in two distinct ways.

## Deep Research vs Developer Mode

### Use Deep Research when

- You want read-only research workflows
- You expose only `search` and `fetch` MCP tools
- You want safer retrieval-focused analysis of UniFi data

### Use Developer Mode when

- You need interactive operations, analysis, and iteration
- You need access to a broader toolset than `search` and `fetch`
- You can run a remote MCP transport endpoint for ChatGPT

## Transport Requirements

- Streaming HTTP is preferred for ChatGPT Developer Mode MCP connections
- SSE is acceptable when your deployment documents and supports it
- Local stdio-only MCP setups are not sufficient for ChatGPT remote connector workflows

## Security Notes

- Never expose UniFi API keys or session tokens in prompts, logs, or screenshots
- Place MCP behind an authenticated proxy or gateway before exposing it remotely
- Start with read-only tools and add mutating tools only after policy review
- Restrict network access and IP ranges for remote MCP endpoints

## Minimal Smoke Test Prompts

Use these prompts after connecting ChatGPT to your MCP endpoint.

1. `List available MCP tools and identify which ones are read-only.`
2. `Run a safe read-only query to list UniFi sites.`
3. `For the default site, summarize connected devices and flag offline devices.`
4. `Explain which tool calls were made and why each call was needed.`

If these pass, move to role-based access, narrower scopes, and production hardening.
