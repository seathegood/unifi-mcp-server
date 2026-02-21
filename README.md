# UniFi MCP Server (seathegood fork)

This repository is a fork of `enuno/unifi-mcp-server` focused on ChatGPT integration and container-first deployment. It provides a FastMCP server for UniFi workflows with practical defaults for remote connector use. This README is the primary source of truth for this fork.

## Key Capabilities

- FastMCP server for UniFi API operations and automation workflows.
- ChatGPT integration modes:
  - Deep Research style deployments with `search` and `fetch` exposure.
  - Developer Mode deployments with full tool access.
- Redaction enabled by default for sensitive fields in tool output and logs.

## Quickstart

### Local STDIO

```bash
docker run -i --rm \
  -e UNIFI_API_KEY=your-api-key \
  -e UNIFI_API_TYPE=local \
  -e UNIFI_LOCAL_HOST=192.168.1.1 \
  ghcr.io/seathegood/unifi-mcp-server:latest
```

### Remote HTTP (Streamable HTTP)

```bash
docker run --rm -p 8080:8080 \
  -e UNIFI_API_KEY=your-api-key \
  -e MCP_TRANSPORT=http \
  -e MCP_HOST=0.0.0.0 \
  -e MCP_PORT=8080 \
  -e MCP_PATH=/mcp \
  ghcr.io/seathegood/unifi-mcp-server:latest
```

## ChatGPT Integration

- Setup and transport guidance: [`docs/chatgpt.md`](docs/chatgpt.md)
- Prompt packs: [`docs/prompts/`](docs/prompts/)

## Deployment

- Compose example: [`deploy/compose.example.yml`](deploy/compose.example.yml)
- Traefik hardening and reverse proxy setup: [`docs/deploy-traefik.md`](docs/deploy-traefik.md)

## Security

- Redaction is enabled by default to reduce accidental exposure of sensitive data.
- For internet-facing deployments, place the MCP endpoint behind an authentication proxy.

## Upstream Attribution

This fork is based on [`enuno/unifi-mcp-server`](https://github.com/enuno/unifi-mcp-server) and keeps Apache-2.0 licensing.

For upstream-specific notes and archived references, see [`docs/upstream-notes.md`](docs/upstream-notes.md).
