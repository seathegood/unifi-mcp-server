#!/usr/bin/env python3
"""Small MCP integration harness for ChatGPT Deep Research workflows."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_URL = "http://127.0.0.1:8080/mcp"
DEFAULT_QUERY = "vlans"
REQUEST_TIMEOUT = 20

FORBIDDEN_PHRASES = (
    "wpa password",
    "wifi password",
)

FORBIDDEN_PATTERNS = (
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{50,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(
        r"(?i)(api[_-]?key|token|secret|passphrase|password)\s*[:=]\s*(?!\*+redacted\*+|redacted)[A-Za-z0-9_./+=-]{16,}"
    ),
)


class IntegrationCheckError(RuntimeError):
    """Raised when a validation check fails."""


@dataclass
class MCPClient:
    """Minimal JSON-RPC client for MCP streamable HTTP endpoints."""

    url: str
    timeout: int = REQUEST_TIMEOUT
    session_id: str | None = None

    def request(self, payload: dict[str, Any], expect_response: bool = True) -> dict[str, Any] | None:
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "content-type": "application/json",
            "accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["mcp-session-id"] = self.session_id

        req = urllib.request.Request(self.url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                self.session_id = resp.headers.get("mcp-session-id", self.session_id)
                if not expect_response:
                    return None
                raw = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise IntegrationCheckError(
                f"HTTP {exc.code} for payload method={payload.get('method')}: {error_body}"
            ) from exc
        except urllib.error.URLError as exc:
            raise IntegrationCheckError(f"Failed to reach MCP endpoint at {self.url}: {exc}") from exc

        return _parse_json_or_sse(raw)


def _parse_json_or_sse(raw: str) -> dict[str, Any]:
    text = raw.strip()
    if not text:
        raise IntegrationCheckError("Empty HTTP response body")
    if text.startswith("{"):
        decoded = json.loads(text)
        if not isinstance(decoded, dict):
            raise IntegrationCheckError("Expected JSON object response")
        return decoded

    # Basic SSE fallback: parse last `data:` event that looks like JSON.
    last_data = ""
    for line in text.splitlines():
        if line.startswith("data:"):
            last_data = line[5:].strip()
    if not last_data:
        raise IntegrationCheckError(f"Could not parse response as JSON or SSE data: {text[:200]!r}")
    decoded = json.loads(last_data)
    if not isinstance(decoded, dict):
        raise IntegrationCheckError("Expected JSON object in SSE data")
    return decoded


def _extract_result_payload(response: dict[str, Any]) -> Any:
    if "error" in response:
        raise IntegrationCheckError(f"MCP returned error: {response['error']}")
    if "result" not in response:
        raise IntegrationCheckError(f"Missing JSON-RPC result: {response}")

    result = response["result"]
    if isinstance(result, (list, dict)) and "content" not in result:
        return result
    if isinstance(result, dict):
        if "structuredContent" in result:
            return result["structuredContent"]
        content = result.get("content")
        if isinstance(content, list):
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "text" and isinstance(item.get("text"), str):
                    text = item["text"].strip()
                    if not text:
                        return ""
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return text
        if "text" in result and isinstance(result["text"], str):
            text = result["text"].strip()
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text

    raise IntegrationCheckError(f"Unable to decode tool payload from response: {response}")


def _validate_search_payload(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise IntegrationCheckError(f"search result is not a list: {type(payload).__name__}")
    if not payload:
        raise IntegrationCheckError("search returned zero results")

    required_keys = {"id", "title", "snippet", "updated_at", "site_scope"}
    for idx, item in enumerate(payload):
        if not isinstance(item, dict):
            raise IntegrationCheckError(f"search item #{idx} is not an object")
        missing = required_keys.difference(item.keys())
        if missing:
            raise IntegrationCheckError(f"search item #{idx} missing keys: {sorted(missing)}")
    return payload


def _validate_fetch_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise IntegrationCheckError(f"fetch result is not an object: {type(payload).__name__}")
    required_keys = {"id", "title", "updated_at", "site_scope", "text"}
    missing = required_keys.difference(payload.keys())
    if missing:
        raise IntegrationCheckError(f"fetch payload missing keys: {sorted(missing)}")

    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        raise IntegrationCheckError("fetch text is empty")
    return payload


def _validate_redaction(payload: dict[str, Any]) -> None:
    body = json.dumps(payload, ensure_ascii=False)
    body_lower = body.lower()

    for phrase in FORBIDDEN_PHRASES:
        if phrase in body_lower:
            raise IntegrationCheckError(f"Forbidden phrase found in payload: {phrase!r}")

    for pattern in FORBIDDEN_PATTERNS:
        if pattern.search(body):
            raise IntegrationCheckError(f"Forbidden secret-like pattern found: {pattern.pattern}")


def _wait_for_server(client: MCPClient, max_wait_seconds: int) -> None:
    start = time.time()
    while True:
        try:
            _initialize(client)
            return
        except IntegrationCheckError:
            if time.time() - start > max_wait_seconds:
                raise IntegrationCheckError("MCP server did not become ready before timeout")
            time.sleep(1)


def _initialize(client: MCPClient) -> None:
    init_response = client.request(
        {
            "jsonrpc": "2.0",
            "id": "init-1",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "integration-check", "version": "1.0"},
            },
        }
    )
    if init_response is None:
        raise IntegrationCheckError("initialize returned no response")
    if "error" in init_response:
        raise IntegrationCheckError(f"initialize failed: {init_response['error']}")

    # Best-effort notify initialized; ignore failures for compatibility.
    try:
        client.request(
            {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {},
            },
            expect_response=False,
        )
    except IntegrationCheckError:
        pass


def _run_check(client: MCPClient, query: str) -> None:
    _initialize(client)

    search_response = client.request(
        {
            "jsonrpc": "2.0",
            "id": "search-1",
            "method": "tools/call",
            "params": {"name": "search", "arguments": {"query": query}},
        }
    )
    if search_response is None:
        raise IntegrationCheckError("search returned no response")
    search_payload = _extract_result_payload(search_response)
    search_results = _validate_search_payload(search_payload)

    first_doc_id = str(search_results[0]["id"])
    fetch_response = client.request(
        {
            "jsonrpc": "2.0",
            "id": "fetch-1",
            "method": "tools/call",
            "params": {"name": "fetch", "arguments": {"id": first_doc_id}},
        }
    )
    if fetch_response is None:
        raise IntegrationCheckError("fetch returned no response")
    fetch_payload = _extract_result_payload(fetch_response)
    fetch_doc = _validate_fetch_payload(fetch_payload)
    _validate_redaction(fetch_doc)

    print("PASS: integration check succeeded")
    print(f"- endpoint: {client.url}")
    print(f"- query: {query}")
    print(f"- matched documents: {len(search_results)}")
    print(f"- fetched id: {first_doc_id}")


def _start_local_server(url: str) -> subprocess.Popen[str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise IntegrationCheckError(f"Unsupported URL scheme for local start: {url}")
    if not parsed.hostname:
        raise IntegrationCheckError(f"URL must include a host: {url}")
    if not parsed.path:
        raise IntegrationCheckError(f"URL must include MCP path: {url}")

    env = os.environ.copy()
    env["MCP_TRANSPORT"] = "http"
    env["MCP_PROFILE"] = "deep-research"
    env["MCP_HOST"] = parsed.hostname
    env["MCP_PORT"] = str(parsed.port or 80)
    env["MCP_PATH"] = parsed.path

    cmd = [sys.executable, "-m", "src"]
    return subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate MCP search/fetch integration contract.")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"MCP endpoint URL (default: {DEFAULT_URL})")
    parser.add_argument(
        "--query",
        default=DEFAULT_QUERY,
        help=f"Search query used for validation (default: {DEFAULT_QUERY!r})",
    )
    parser.add_argument(
        "--start-local",
        action="store_true",
        help="Start a local server process in deep-research profile before running checks.",
    )
    parser.add_argument(
        "--startup-timeout",
        type=int,
        default=35,
        help="Seconds to wait for local startup readiness (default: 35).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    client = MCPClient(args.url)
    proc: subprocess.Popen[str] | None = None

    try:
        if args.start_local:
            proc = _start_local_server(args.url)
            _wait_for_server(client, args.startup_timeout)
        _run_check(client, args.query)
        return 0
    except IntegrationCheckError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    finally:
        if proc is not None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    raise SystemExit(main())
