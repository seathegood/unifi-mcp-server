# Integration Validation Harness

This repo includes a small integration harness to verify ChatGPT-facing MCP behavior in Deep Research style deployments.

## What it validates

- `search` and `fetch` calls complete over MCP HTTP.
- `search(query)` returns the expected list shape:
  - `id`, `title`, `snippet`, `updated_at`, `site_scope`
- `fetch(id)` returns expected object shape:
  - `id`, `title`, `updated_at`, `site_scope`, `text`
- fetched `text` is non-empty
- fetched payload does not contain basic forbidden secret/password patterns

The script exits non-zero on any failure.

## Script location

- `scripts/integration_check.py`

## Local run (server already running)

1. Start server in HTTP deep-research mode (example):

```bash
MCP_TRANSPORT=http \
MCP_PROFILE=deep-research \
MCP_HOST=127.0.0.1 \
MCP_PORT=8080 \
MCP_PATH=/mcp \
python -m src
```

2. In a second shell, run:

```bash
python scripts/integration_check.py --url http://127.0.0.1:8080/mcp
```

## Local run (harness starts server)

If your env already contains required UniFi variables (for example `UNIFI_API_KEY`), you can let the harness start the server:

```bash
python scripts/integration_check.py --start-local --url http://127.0.0.1:8080/mcp
```

## Remote run behind Traefik

Run against your external MCP URL:

```bash
python scripts/integration_check.py --url https://<your-domain>/mcp
```

Notes:
- Keep `MCP_PROFILE=deep-research` on the deployment you validate.
- Ensure Traefik routing preserves `/mcp` and forwards to the app service on port `8080`.
- Ensure your auth proxy/middleware allows this test client to call MCP methods.

## Minimal prompts for the other chat

- `Search for VLANs and subnets, then fetch the most relevant document.`
- `Fetch inventory snapshot and list AP firmware.`

## Why this supports ChatGPT integration

It verifies the exact retrieval workflow ChatGPT relies on in Deep Research mode: `search` to discover document ids, `fetch` to retrieve a document body, and baseline redaction hygiene in returned content.
