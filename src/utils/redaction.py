"""Central redaction helpers for MCP tool responses."""

from __future__ import annotations

from typing import Any

SENSITIVE_RESPONSE_FIELDS = {
    "mac",
    "client_mac",
    "device_mac",
    "ip",
    "ip_address",
    "fixed_ip",
    "hostname",
    "serial",
    "serial_number",
    "email",
    "latitude",
    "longitude",
    "location",
}


FULL_REDACTION_FIELDS = {
    "password",
    "passphrase",
    "psk",
    "secret",
    "token",
    "api_key",
}


def _redact_mac(value: str) -> str:
    parts = value.split(":")
    if len(parts) == 6 and all(len(p) == 2 for p in parts):
        return "**:**:**:**:**:" + parts[-1]
    return "***"


def _redact_ip(value: str) -> str:
    parts = value.split(".")
    if len(parts) == 4 and all(part.isdigit() for part in parts):
        return "***.***.***." + parts[-1]
    return "***"


def _redact_value(key: str, value: Any) -> str:
    if value is None:
        return "None"
    value_str = str(value)

    if key in FULL_REDACTION_FIELDS:
        return "***"
    if key in {"mac", "client_mac", "device_mac"}:
        return _redact_mac(value_str)
    if key in {"ip", "ip_address", "fixed_ip"}:
        return _redact_ip(value_str)
    if len(value_str) <= 4:
        return "***"
    return "***" + value_str[-2:]


def redact_client_device_data(payload: Any) -> Any:
    """Redact sensitive client/device fields from tool output payloads."""
    if isinstance(payload, dict):
        redacted: dict[str, Any] = {}
        for key, value in payload.items():
            key_lower = key.lower()
            if key_lower in SENSITIVE_RESPONSE_FIELDS or key_lower in FULL_REDACTION_FIELDS:
                redacted[key] = _redact_value(key_lower, value)
                continue

            if isinstance(value, (dict, list)):
                redacted[key] = redact_client_device_data(value)
            else:
                redacted[key] = value
        return redacted

    if isinstance(payload, list):
        return [redact_client_device_data(item) for item in payload]

    return payload
