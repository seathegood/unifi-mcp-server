# AI Agent Command Guide

This guide replaces legacy client-specific command docs with a client-neutral reference for ChatGPT, Codex, Cursor, and other MCP-capable assistants.

## Common Workflow Commands

- `setup`: Initialize local environment and dependencies
- `format`: Run formatting tools
- `lint`: Run static checks and fixers
- `test`: Run unit and integration tests
- `security`: Run security and dependency scans
- `docs`: Update README/API docs and generated references
- `pr`: Prepare pull request metadata and checklist
- `build-docker`: Build container image for local validation
- `unifi-mcp-inspect`: Start MCP Inspector for tool validation
- `unifi-mcp-live-test`: Run live UniFi API validation checks
- `unifi-api-docs-update`: Refresh API-derived documentation
- `unifi-mcp-test-coverage`: Run coverage workflow and summarize gaps
- `unifi-mcp-release-prep`: Execute release preparation checklist

## Usage Pattern

1. Confirm environment variables from `.env.example`.
2. Run read-only validation steps first (`lint`, `test`, `docs`).
3. Run mutating or release workflows only after review.
4. Record outputs in PR notes for reviewer traceability.

## Scope

These commands are workflow references only. The canonical implementation remains the repository scripts, Make targets, and CI workflows.
