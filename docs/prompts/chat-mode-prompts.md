# Chat Mode Prompts (Developer Mode, Read-Only)

Use these once ChatGPT Developer Mode is enabled and connected to this MCP server.

## Mutating safety pattern

```text
Mutating request. Always use plan/apply flow:
1) Call plan_mutation(tool_name="<MUTATING_TOOL>", params={...}, dry_run=true)
2) Show the returned diff and warnings to the user
3) Ask for explicit confirmation
4) Only then call apply_mutation(plan_id="<PLAN_ID>", confirmation_token="<TOKEN>")

Rules:
- Never call mutating tools directly.
- Never infer confirmation; require explicit user approval first.
- Plans are process-local and short-lived (TTL). If expired or after restart, re-plan.
- Confirmation token can be either the per-plan token returned by `plan_mutation` or `MCP_CONFIRM_TOKEN` from server env.
```

## Quick site context

```text
Read-only request. For UniFi site "<SITE_SCOPE>", provide a concise environment summary.
Requirements:
- Include: document_id, timestamp_utc, site_scope.
- Mark output: "redacted by default".
- Include only configuration and status context; do not change anything.
```

## Safe network config pull

```text
Read-only request. Pull current network configuration for site "<SITE_SCOPE>" and summarize VLANs, subnets, and DHCP settings.
Requirements:
- Include: document_id, timestamp_utc, site_scope.
- Mark output: "redacted by default".
- If fields are missing, report "unknown" rather than guessing.
```

## Safe Wi-Fi mapping pull

```text
Read-only request. Pull SSID configuration for site "<SITE_SCOPE>" and map each SSID to its VLAN/network.
Requirements:
- Include: document_id, timestamp_utc, site_scope.
- Mark output: "redacted by default".
- Note any SSID with no clear VLAN mapping.
```

## Safe firewall review

```text
Read-only request. Summarize firewall posture for site "<SITE_SCOPE>" including policy defaults and top rule intents.
Requirements:
- Include: document_id, timestamp_utc, site_scope.
- Mark output: "redacted by default".
- Keep findings defensive; no attack or bypass instructions.
```
