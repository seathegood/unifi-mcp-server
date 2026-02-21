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

## Deep Research Document Contract

The Deep Research tools return stable document metadata to make retrieval deterministic.

- `search(query)` returns a ranked list (default top 5):
  - `id` (string)
  - `title` (string)
  - `snippet` (string)
  - `updated_at` (ISO8601 UTC string)
  - `site_scope` (site label or `all sites: ...` for aggregated docs)
- `fetch(id)` returns:
  - `id` (string)
  - `title` (string)
  - `updated_at` (ISO8601 UTC string)
  - `site_scope` (string)
  - `text` (string)
  - `source` (optional string; controller source, redacted by default when needed)

The current document ids are:

- `inventory_snapshot`
- `networks_vlans_subnets`
- `wifi_ssids_security`
- `firewall_posture_summary`
- `port_profiles_summary`

### Example `fetch("networks_vlans_subnets")`

```json
{
  "id": "networks_vlans_subnets",
  "title": "Networks, VLANs, and Subnets",
  "updated_at": "2026-02-21T01:23:45.123456+00:00",
  "site_scope": "all sites: HQ (site-1)",
  "source": "https://api.ui.com",
  "text": "# Networks, VLANs, and Subnets\\n- Generated (UTC): 2026-02-21T01:23:45.123456+00:00\\n- Controller: https://api.ui.com\\n- Site context: all sites: HQ (site-1)\\n\\n## Networks\\n### Site: HQ (site-1)\\n- LAN | purpose=corporate | vlan=1 | subnet=10.0.1.0/24 | dhcp=True\\n\\n## Raw (redacted) JSON\\n{...}"
}
```

### Example `fetch("inventory_snapshot")`

```json
{
  "id": "inventory_snapshot",
  "title": "Inventory Snapshot",
  "updated_at": "2026-02-21T01:23:45.123456+00:00",
  "site_scope": "all sites: HQ (site-1)",
  "source": "https://api.ui.com",
  "text": "# Inventory Snapshot\\n- Generated (UTC): 2026-02-21T01:23:45.123456+00:00\\n- Controller: https://api.ui.com\\n- Site context: all sites: HQ (site-1)\\n\\n## Summary\\n- Site: HQ (site-1)\\n  - Devices: 1 (1 online)\\n  - Clients (known): 1\\n  - Networks: 1\\n  - SSIDs: 1\\n\\n## Raw (redacted) JSON\\n{...}"
}
```
