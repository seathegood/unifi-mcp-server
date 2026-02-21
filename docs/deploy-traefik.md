# Traefik Deployment (Docker Compose / TrueNAS-friendly)

This guide provides example-only deployment artifacts for running the UniFi MCP server behind Traefik with a safer default posture.

## What to use

- Compose example: `deploy/compose.example.yml`
- Env template: `deploy/env.example`

## Safe quickstart (copy/paste)

```bash
cd deploy
cp env.example env
# Edit deploy/env: set UNIFI_API_KEY and deployment-specific values only.
# Keep MCP_PROFILE=deep-research for first exposure.
docker compose -f compose.example.yml up -d
```

The example keeps secrets out of Git by using `env_file` and an untracked `deploy/env` file.

## Transport and TLS model

- The app serves MCP over streamable HTTP (`MCP_TRANSPORT=http`) on internal port `8080`.
- Traefik should terminate TLS on `websecure` and forward plain HTTP to the container.
- Expose `/mcp` through Traefik only; do not publish container port `8080` directly to the internet.

## Authentication and access controls

Minimum recommended control stack:

1. Forward-auth with Authentik (preferred).
   - Use Traefik `forwardAuth` middleware to enforce identity and policy before requests reach MCP.
2. Basic auth (minimum baseline if forward-auth is not available).
   - Use Traefik basic auth middleware with strong credentials and short rotation windows.
3. Optional IP allowlist.
   - Restrict endpoint reachability to trusted egress CIDRs (VPN, office NAT, controlled runners).

Keep middleware names generic in compose labels and define their real values in your Traefik dynamic config.

## Why `MCP_PROFILE=deep-research` is safer

- It limits exposed tools to `health_check`, `search`, and `fetch`.
- It prevents accidental mutating operations during first rollout.
- It aligns with retrieval-oriented connector workflows and tighter blast radius.

Move to broader exposure only after auth, observability, and policy controls are validated.

## Logging guidance

- Keep `UNIFI_AUDIT_LOG_ENABLED=true` for mutating operation traceability.
- Run with `LOG_LEVEL=INFO` in production and use `DEBUG` only for short troubleshooting windows.
- Configure reverse-proxy and app logs to avoid request header/token capture.
- Do not log `Authorization`, API keys, cookies, or forwarded identity tokens.
- Rotate logs and define retention windows suitable for incident response.

## Notes on variable naming

Some external examples use `UNIFI_BASE_URL` / `UNIFI_API_TOKEN`. This project uses:

- `UNIFI_API_KEY` for token auth
- `UNIFI_API_TYPE` + (`UNIFI_CLOUD_API_URL` or `UNIFI_LOCAL_HOST`/`UNIFI_LOCAL_PORT`) for base URL selection
- `UNIFI_DEFAULT_SITE` for site selection (legacy alias `UNIFI_SITE` also works)
