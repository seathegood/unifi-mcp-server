# Deep Research Prompts (UniFi MCP)

Use these in ChatGPT Deep Research with a read-only MCP deployment that exposes `search` and `fetch`.

## VLANs and subnets

```text
Use MCP search/fetch to build a VLAN and subnet inventory for UniFi site "<SITE_SCOPE>".
Requirements:
- Read-only only.
- Return: VLAN name, VLAN ID, subnet/CIDR, gateway, DHCP status.
- Include metadata on every section: document_id, timestamp_utc, site_scope.
- Mark output: "redacted by default" (mask sensitive fields unless explicitly requested).
- If multiple sources conflict, show both and label confidence.
```

## SSIDs and VLAN mappings

```text
Use MCP search/fetch to list SSIDs and their VLAN mappings for UniFi site "<SITE_SCOPE>".
Requirements:
- Read-only only.
- Return: SSID name, network/VLAN binding, security mode, enabled/disabled state.
- Include metadata on every section: document_id, timestamp_utc, site_scope.
- Mark output: "redacted by default".
- Flag missing or ambiguous mappings explicitly.
```

## Inventory snapshot

```text
Use MCP search/fetch to create a current inventory snapshot for UniFi site "<SITE_SCOPE>".
Requirements:
- Read-only only.
- Return counts and tables for gateways, switches, APs, and clients (online/offline where available).
- Include metadata on every section: document_id, timestamp_utc, site_scope.
- Mark output: "redacted by default".
- If data is partial, state gaps and the exact endpoints searched.
```

## Firewall posture

```text
Use MCP search/fetch to summarize firewall posture for UniFi site "<SITE_SCOPE>".
Requirements:
- Read-only only.
- Return: default policy stance, major rule groups, notable allow/deny patterns, and exposed services summary.
- Include metadata on every section: document_id, timestamp_utc, site_scope.
- Mark output: "redacted by default".
- Do not provide exploit guidance; provide defensive observations only.
```
