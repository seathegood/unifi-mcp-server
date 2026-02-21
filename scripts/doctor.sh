#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR" || exit 1

PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

pass() {
  PASS_COUNT=$((PASS_COUNT + 1))
  echo "PASS: $1"
}

warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  echo "WARN: $1"
}

fail() {
  FAIL_COUNT=$((FAIL_COUNT + 1))
  echo "FAIL: $1"
}

section() {
  echo
  echo "== $1 =="
}

has_rg() {
  command -v rg >/dev/null 2>&1
}

scan_pattern() {
  local pattern="$1"
  shift

  if has_rg; then
    rg -n -H -I --hidden --glob '!.git' --glob '!node_modules' --glob '!*.svg' --glob '!*.png' --glob '!*.jpg' --glob '!*.jpeg' --glob '!*.gif' -e "$pattern" "$@" 2>/dev/null || true
  else
    grep -R -n -E "$pattern" "$@" 2>/dev/null || true
  fi
}

check_file_exists() {
  local path="$1"
  if [[ -f "$path" ]]; then
    pass "Found $path"
  else
    fail "Missing required file: $path"
  fi
}

section "Required docs and scripts"
check_file_exists "docs/chatgpt.md"
check_file_exists "docs/connector-readiness.md"
check_file_exists "scripts/doctor.sh"

section "Connector capability checks"

if scan_pattern 'async def search\(' src/main.py >/dev/null && \
   scan_pattern 'async def fetch\(' src/main.py >/dev/null && \
   scan_pattern '"search"' src/tools/registry.py >/dev/null && \
   scan_pattern '"fetch"' src/tools/registry.py >/dev/null; then
  pass "search/fetch MCP tools are implemented and registered"
else
  fail "search/fetch MCP tools were not fully verified"
fi

if scan_pattern 'if settings\.mcp_transport == "http"' src/main.py >/dev/null && \
   scan_pattern 'MCP_TRANSPORT=http' deploy/env.example >/dev/null; then
  pass "Remote HTTP transport path is present"
else
  fail "Remote HTTP transport checks failed"
fi

if scan_pattern 'MCP_PATH=/mcp' .env.example deploy/env.example >/dev/null && \
   scan_pattern 'Path prefix: `/mcp`' docs/deploy-traefik.md >/dev/null; then
  pass "Repository documents /mcp endpoint routing"
else
  fail "Could not confirm /mcp endpoint documentation"
fi

if scan_pattern 'INCLUDE_MACS=false' .env.example deploy/env.example >/dev/null && \
   scan_pattern 'INCLUDE_SERIALS=false' .env.example deploy/env.example >/dev/null && \
   scan_pattern 'INCLUDE_PUBLIC_IP=false' .env.example deploy/env.example >/dev/null && \
   scan_pattern 'include_macs: bool = Field\([[:space:]]*default=False' src/config/config.py >/dev/null && \
   scan_pattern 'include_serials: bool = Field\([[:space:]]*default=False' src/config/config.py >/dev/null && \
   scan_pattern 'include_public_ip: bool = Field\([[:space:]]*default=False' src/config/config.py >/dev/null; then
  pass "Redaction defaults are set to safe values"
else
  fail "Redaction default checks failed"
fi

if scan_pattern 'Minimal Smoke Test Prompts' docs/chatgpt.md >/dev/null; then
  pass "Sample prompts are present in docs/chatgpt.md"
else
  fail "Sample prompts section missing in docs/chatgpt.md"
fi

section "Policy lint: forbidden terms"
if has_rg; then
  FORBIDDEN_MATCHES="$(rg -n -H -I --hidden --glob '!.git' --glob '!node_modules' --glob '!scripts/doctor.sh' --glob '!docs/connector-readiness.md' '(?i)\b(claude|anthropic)\b' . 2>/dev/null || true)"
else
  FORBIDDEN_MATCHES="$(grep -R -n -E -i '\b(claude|anthropic)\b' . 2>/dev/null | grep -Ev 'scripts/doctor\.sh|docs/connector-readiness\.md' || true)"
fi
if [[ -n "$FORBIDDEN_MATCHES" ]]; then
  fail "Found forbidden terms (Claude/Anthropic references still present)"
  echo "$FORBIDDEN_MATCHES" | sed -n '1,20p'
else
  pass "No forbidden terms found (Claude/Anthropic)"
fi

section "Best-effort secret scan"
SECRET_MATCHES=""
SECRET_SCAN_PATHS=(src deploy .env.example docker-compose.yml README.md)

# High-confidence token formats.
SECRET_MATCHES+="$(scan_pattern 'AKIA[0-9A-Z]{16}' "${SECRET_SCAN_PATHS[@]}")"$'\n'
SECRET_MATCHES+="$(scan_pattern 'ghp_[A-Za-z0-9]{36}' "${SECRET_SCAN_PATHS[@]}")"$'\n'
SECRET_MATCHES+="$(scan_pattern 'github_pat_[A-Za-z0-9_]{50,}' "${SECRET_SCAN_PATHS[@]}")"$'\n'
SECRET_MATCHES+="$(scan_pattern 'xox[baprs]-[A-Za-z0-9-]{10,}' "${SECRET_SCAN_PATHS[@]}")"$'\n'

# Generic long assignments to secret-like keys.
SECRET_MATCHES+="$(scan_pattern '(?i)(api[_-]?key|token|secret|password|passphrase)[[:space:]]*[:=][[:space:]]*[A-Za-z0-9_./+=-]{24,}' "${SECRET_SCAN_PATHS[@]}")"$'\n'

# Trim obvious placeholders to reduce noise.
FILTERED_SECRET_MATCHES="$(printf '%s\n' "$SECRET_MATCHES" | sed '/^$/d' | grep -Evi '(changeme|your-api-key|your-token|example|sample|placeholder|dummy|test|<.*>|-here)' || true)"

if [[ -n "$FILTERED_SECRET_MATCHES" ]]; then
  fail "Possible hard-coded secrets detected"
  echo "$FILTERED_SECRET_MATCHES" | sed -n '1,20p'
else
  pass "No obvious committed secrets detected"
fi

section "No-secrets-in-logs heuristics"
if scan_pattern 'from \.sanitize import' src/api/client.py src/utils/__init__.py >/dev/null && \
   scan_pattern 'log_api_request\(' src/api/client.py >/dev/null; then
  pass "Logging/sanitization utilities are present"
else
  warn "Could not fully verify logging sanitization integration"
fi

section "Optional local MCP probe"
DOCTOR_PING_LOCAL="${DOCTOR_PING_LOCAL:-0}"
DOCTOR_MCP_URL="${DOCTOR_MCP_URL:-http://127.0.0.1:8080/mcp}"

if [[ "$DOCTOR_PING_LOCAL" == "1" ]]; then
  if ! command -v curl >/dev/null 2>&1; then
    warn "curl not available; skipping local MCP probe"
  else
    HTTP_CODE="$(curl -sS -k -m 5 -o /tmp/unifi-doctor-get.out -w '%{http_code}' "$DOCTOR_MCP_URL" || true)"
    if [[ "$HTTP_CODE" == "000" ]]; then
      fail "Local endpoint not reachable at $DOCTOR_MCP_URL"
    else
      pass "Local endpoint reachable at $DOCTOR_MCP_URL (GET status $HTTP_CODE)"

      INIT_PAYLOAD='{"jsonrpc":"2.0","id":"doctor-init","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"doctor","version":"1.0"}}}'
      INIT_CODE="$(curl -sS -k -m 8 -o /tmp/unifi-doctor-init.out -w '%{http_code}' -H 'content-type: application/json' -d "$INIT_PAYLOAD" "$DOCTOR_MCP_URL" || true)"
      if [[ "$INIT_CODE" == "000" ]]; then
        warn "Initialize probe failed to reach endpoint"
      else
        if [[ "$INIT_CODE" =~ ^2 ]]; then
          pass "Initialize handshake request succeeded (HTTP $INIT_CODE)"
        else
          warn "Initialize handshake returned HTTP $INIT_CODE (endpoint responded; verify runtime MCP behavior)"
        fi
      fi
    fi
  fi
else
  echo "INFO: Skipping local probe (set DOCTOR_PING_LOCAL=1 to enable)."
fi

echo
printf 'Summary: %d passed, %d warnings, %d failed\n' "$PASS_COUNT" "$WARN_COUNT" "$FAIL_COUNT"

if (( FAIL_COUNT > 0 )); then
  exit 1
fi

exit 0
