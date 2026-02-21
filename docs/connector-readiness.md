# Connector Readiness Checklist

Use this checklist before exposing the MCP endpoint to ChatGPT connector workflows.

## Core checklist

- [ ] Remote HTTP transport runs.
  - Evidence: `MCP_TRANSPORT=http` in deployment env (`deploy/env.example`) and HTTP branch in `src/main.py`.
- [ ] `/mcp` is reachable over HTTPS.
  - Evidence: reverse proxy/TLS config and successful external probe to `https://<host>/mcp`.
- [ ] `search` and `fetch` are implemented.
  - Evidence: tool definitions in `src/main.py` and metadata in `src/tools/registry.py`.
- [ ] Redaction defaults are enabled.
  - Evidence: `INCLUDE_MACS=false`, `INCLUDE_SERIALS=false`, `INCLUDE_PUBLIC_IP=false` in env templates and config defaults.
- [ ] No secrets in logs.
  - Evidence: redaction/sanitize utilities in use and clean `scripts/doctor.sh` secret scan.
- [ ] Claude/Anthropic references are removed.
  - Evidence: `scripts/doctor.sh` forbidden-term scan passes.
- [ ] Sample prompts are included.
  - Evidence: `docs/chatgpt.md` includes the `Minimal Smoke Test Prompts` section.

## Automated checks

Run:

```bash
scripts/doctor.sh
```

Optional local runtime probe (if the server is running locally):

```bash
DOCTOR_PING_LOCAL=1 DOCTOR_MCP_URL=http://127.0.0.1:8080/mcp scripts/doctor.sh
```

## Notes

- The script is best-effort and intentionally conservative on secret detection to keep false positives manageable.
- HTTPS reachability is environment-specific and cannot be fully proven by static repository checks alone.
