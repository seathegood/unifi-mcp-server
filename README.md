# UniFi MCP Server (seathegood fork)

This repository is a fork of `enuno/unifi-mcp-server` focused on ChatGPT integration and container-first deployment. It provides a FastMCP server for UniFi workflows with safe defaults for remote connector use.

## Local Work Contract

Use `make` as the shared command contract for humans, CI, and coding agents.

```bash
make bootstrap
cp .env.example .env
make doctor
make check
```

Primary targets:

- `make bootstrap` - create `.venv` and install dev dependencies
- `make doctor` - static readiness and safety checks (`scripts/doctor.sh`)
- `make check` - doctor checks, format checks, lint, and unit tests
- `make build` - build the Python package
- `make format` - apply formatting
- `make clean-local` - remove local caches and `_tmp/`

Windows equivalents:

- `.venv\Scripts\python -m pytest tests\unit`
- `.venv\Scripts\python -m black src tests`

## Environment Files

- `.env` is local-only and must stay untracked.
- `.env.example` is the template with placeholders only.
- `deploy/env.example` is the deployment-oriented template.

Required environment variable:

- `UNIFI_API_KEY`

Common transport variables:

- `MCP_TRANSPORT` (`stdio` or `http`)
- `MCP_HOST`, `MCP_PORT`, `MCP_PATH`
- `MCP_PROFILE` (`full` or `deep-research`)

## Artifact Conventions

- `_tmp/` for transient local artifacts (untracked).
- `_reports/` for generated reports you want to keep locally.
- `reports/` is legacy; prefer `_reports/` for new outputs.
- `.venv/` is the repo-root virtual environment (untracked).

## ChatGPT Integration

- Setup and transport guidance: [`docs/chatgpt.md`](docs/chatgpt.md)
- Prompt packs: [`docs/prompts/`](docs/prompts/)
- Connector readiness checklist: [`docs/connector-readiness.md`](docs/connector-readiness.md)

## Deployment

- Compose example: [`deploy/compose.example.yml`](deploy/compose.example.yml)
- Traefik hardening and reverse proxy setup: [`docs/deploy-traefik.md`](docs/deploy-traefik.md)
- Runtime image build instructions: [`Dockerfile`](Dockerfile)

## Security

- Redaction is enabled by default to reduce accidental exposure of sensitive data.
- For internet-facing deployments, place the MCP endpoint behind an authentication proxy.
- Keep secrets in environment variables, never in committed docs or scripts.

## Agent Guidance

Primary agent instructions live in [`docs/AGENTS.md`](docs/AGENTS.md). A root `AGENTS.md` pointer is included for tooling that discovers guidance at repository root.

## Upstream Attribution

This fork is based on [`enuno/unifi-mcp-server`](https://github.com/enuno/unifi-mcp-server) and keeps Apache-2.0 licensing. For upstream-specific notes and archived references, see [`docs/upstream-notes.md`](docs/upstream-notes.md).
