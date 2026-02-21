# Chat Mode Prompts (Developer Mode, Read-Only)

Use these once ChatGPT Developer Mode is enabled and connected to this MCP server.

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
