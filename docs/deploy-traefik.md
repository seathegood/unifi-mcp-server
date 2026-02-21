# Traefik Deployment (Docker Compose / TrueNAS-friendly)

This guide provides **example-only** deployment artifacts for running the UniFi MCP server behind Traefik. It does not assume Kubernetes and avoids hard-coding network topology.

## What to use

- Compose example: `deploy/compose.example.yml`
- Env template: `deploy/env.example`

## Copy/paste quickstart (safe)

```bash
cd deploy
cp env.example env
# Edit deploy/env and add your real UNIFI_API_KEY (and local settings if using local mode)
docker compose -f compose.example.yml up -d
```

The example keeps secrets out of Git by using `env_file` and a separate untracked `deploy/env` file.

## Traefik label examples

The compose example includes labels for:

- Host rule: `unifi-mcp.<your-domain>`
- Path prefix: `/mcp`
- TLS enabled on `websecure`

If you do not want path-based routing, remove the `PathPrefix(`/mcp`)` part and keep only the host rule.

## Recommended access controls

Use one or both:

1. Forward-auth middleware (recommended):
   - Put Authentik in front of the MCP endpoint with Traefik `forwardAuth`.
   - Enforce user/group policy before traffic reaches the app.
2. IP allowlist middleware:
   - Restrict access to trusted LAN/VPN CIDRs for machine-to-machine clients.

Keep middleware references generic in compose labels and define the actual middlewares in your Traefik dynamic config.

## Why start read-only first

Even with auth in place, start by exposing read-only operations to validate:

- auth flow correctness,
- audit visibility,
- endpoint behavior for your client tooling.

Then enable mutating workflows in a controlled change window.

## Logging and retention guidance

- Keep `UNIFI_AUDIT_LOG_ENABLED=true` for mutating operation traceability.
- Run with `LOG_LEVEL=INFO` in production (use `DEBUG` only temporarily).
- Rotate application and reverse-proxy logs; avoid unbounded retention.
- Keep logs long enough for incident review, and scrub exports before sharing.

## Notes on variable naming

Some platforms/docs use `UNIFI_BASE_URL` and `UNIFI_API_TOKEN`. This project uses:

- `UNIFI_API_KEY` for token auth
- `UNIFI_API_TYPE` + (`UNIFI_CLOUD_API_URL` or `UNIFI_LOCAL_HOST`/`UNIFI_LOCAL_PORT`) for base URL selection
- Optional site selector via `UNIFI_DEFAULT_SITE` (legacy alias `UNIFI_SITE` also works)
