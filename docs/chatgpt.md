# ChatGPT Integration

This project uses FastMCP and can be connected to ChatGPT in two distinct ways.

## Deep Research vs Developer Mode

### Use Deep Research when

- You want read-only research workflows
- You expose only `health_check`, `search`, and `fetch` MCP tools
- You want safer retrieval-focused analysis of UniFi data

Set `MCP_PROFILE=deep-research` for this deployment mode.

### Use Developer Mode when

- You need interactive operations, analysis, and iteration
- You need access to the full UniFi MCP tool surface
- You can run a remote MCP transport endpoint for ChatGPT

Set `MCP_PROFILE=full` (default) for this mode.

## Transport Requirements

- Streaming HTTP is preferred for ChatGPT Developer Mode MCP connections
- SSE is acceptable when your deployment documents and supports it
- Local stdio-only MCP setups are not sufficient for ChatGPT remote connector workflows

## Security Notes

- Never expose UniFi API keys or session tokens in prompts, logs, or screenshots
- Place MCP behind an authenticated proxy or gateway before exposing it remotely
- Start with read-only tools and add mutating tools only after policy review
- Restrict network access and IP ranges for remote MCP endpoints

## Tool Safety Conventions

- Tool classification source of truth is `src/tools/registry.py`.
- Human-readable inventory is `docs/tool-classification.md`.
- `read_only` tools are safe to expose by default.
- `risky_read` tools are still read-only, but may return sensitive payloads.
- `mutating` tools must follow plan/apply semantics and require explicit caller confirmation.
- Future write workflow scaffolding is in `src/tools/change_control.py`:
  - `plan_change(change_request) -> { plan_id, diff, warnings, confirmation_token, expires_at }`
  - `apply_change(plan_id, confirmation_token) -> result`
- `apply_change` rejects requests without a valid confirmation token.

## Minimal Smoke Test Prompts

Use these prompts after connecting ChatGPT to your MCP endpoint.

1. `List available MCP tools and identify which ones are read-only.`
2. `Run a safe read-only query to list UniFi sites.`
3. `For the default site, summarize connected devices and flag offline devices.`
4. `Explain which tool calls were made and why each call was needed.`

If these pass, move to role-based access, narrower scopes, and production hardening.
