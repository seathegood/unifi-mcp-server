"""Configuration document registry and Deep Research search/fetch tools."""

from __future__ import annotations

import ipaddress
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from urllib.parse import urlparse

from ..api import UniFiClient
from ..config import Settings
from ..utils import get_logger

logger = get_logger(__name__)

_DOC_SPECS: tuple[tuple[str, str], ...] = (
    ("inventory_snapshot", "Inventory Snapshot"),
    ("networks_vlans_subnets", "Networks, VLANs, and Subnets"),
    ("wifi_ssids_security", "Wi-Fi SSIDs and Security"),
    ("firewall_posture_summary", "Firewall Posture Summary"),
    ("port_profiles_summary", "Port Profiles Summary"),
)

SENSITIVE_ALWAYS_REDACT = {
    "api_key",
    "x_api_key",
    "token",
    "access_token",
    "authorization",
    "password",
    "passphrase",
    "x_passphrase",
    "psk",
    "x_psk",
    "pre_shared_key",
    "x_ipsec_pre_shared_key",
    "owner",
    "owner_name",
    "ownername",
}

MAC_KEY_MARKERS = ("mac", "bssid", "oui")
SERIAL_KEY_MARKERS = ("serial",)
PUBLIC_IP_KEY_MARKERS = ("wan", "public", "external", "uplink")


@dataclass
class ConfigurationDocument:
    """Generated configuration document for Deep Research."""

    id: str
    title: str
    updated_at: str
    text: str
    url: str | None = None


def list_document_ids() -> list[str]:
    """Return stable document identifiers."""
    return [doc_id for doc_id, _ in _DOC_SPECS]


async def search_documents(query: str, settings: Settings) -> list[dict[str, Any]]:
    """Search generated configuration documents by keyword matching."""
    query_text = query.strip()
    if not query_text:
        return []

    documents = await _build_documents(settings)
    tokens = [token for token in re.split(r"\s+", query_text.lower()) if token]
    query_lower = query_text.lower()

    results: list[dict[str, Any]] = []
    for doc in documents:
        title_lower = doc.title.lower()
        body_lower = doc.text.lower()

        score = 0
        if query_lower in title_lower:
            score += 8
        if query_lower in body_lower:
            score += 4

        for token in tokens:
            if token in title_lower:
                score += 4
            if token in body_lower:
                score += 1

        if score <= 0:
            continue

        results.append(
            {
                "id": doc.id,
                "title": doc.title,
                "snippet": _build_snippet(doc.text, query_lower),
                "score": score,
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results


async def fetch_document(doc_id: str, settings: Settings) -> dict[str, Any]:
    """Fetch full document text by stable id."""
    documents = await _build_documents(settings)
    by_id = {doc.id: doc for doc in documents}

    if doc_id not in by_id:
        known = ", ".join(sorted(by_id.keys()))
        raise ValueError(f"Unknown document id '{doc_id}'. Known ids: {known}")

    doc = by_id[doc_id]
    payload: dict[str, Any] = {
        "id": doc.id,
        "title": doc.title,
        "url": doc.url,
        "text": doc.text,
    }
    return payload


async def _build_documents(settings: Settings) -> list[ConfigurationDocument]:
    """Generate all configuration documents from current controller state."""
    now = datetime.now(UTC)
    updated_at = now.isoformat()

    include_macs = bool(getattr(settings, "include_macs", False))
    include_serials = bool(getattr(settings, "include_serials", False))
    include_public_ip = bool(getattr(settings, "include_public_ip", False))

    async with UniFiClient(settings) as client:
        await client.authenticate()

        sites = await _get_sites(client, settings)
        site_records = [
            {
                "site_id": _site_id(site),
                "site_name": site.get("name") or site.get("desc") or _site_id(site),
                "devices": await _safe_get(client, f"/ea/sites/{_site_id(site)}/devices"),
                "clients": await _safe_get(client, f"/ea/sites/{_site_id(site)}/stat/alluser"),
                "networks": await _safe_get(client, f"/ea/sites/{_site_id(site)}/rest/networkconf"),
                "wlans": await _safe_get(client, f"/ea/sites/{_site_id(site)}/rest/wlanconf"),
                "firewall_rules": await _safe_get(client, f"/ea/sites/{_site_id(site)}/rest/firewallrule"),
                "port_profiles": await _safe_get(client, f"/ea/sites/{_site_id(site)}/rest/portconf"),
                "wans": await _safe_get(client, f"/integration/v1/sites/{_site_id(site)}/wans"),
            }
            for site in sites
            if _site_id(site)
        ]

    context = _site_context(site_records)
    controller = _controller_label(settings, include_public_ip)

    return [
        ConfigurationDocument(
            id="inventory_snapshot",
            title="Inventory Snapshot",
            updated_at=updated_at,
            text=_render_inventory_doc(
                updated_at,
                controller,
                context,
                site_records,
                include_macs,
                include_serials,
                include_public_ip,
            ),
        ),
        ConfigurationDocument(
            id="networks_vlans_subnets",
            title="Networks, VLANs, and Subnets",
            updated_at=updated_at,
            text=_render_networks_doc(
                updated_at,
                controller,
                context,
                site_records,
                include_macs,
                include_serials,
                include_public_ip,
            ),
        ),
        ConfigurationDocument(
            id="wifi_ssids_security",
            title="Wi-Fi SSIDs and Security",
            updated_at=updated_at,
            text=_render_wifi_doc(
                updated_at,
                controller,
                context,
                site_records,
                include_macs,
                include_serials,
                include_public_ip,
            ),
        ),
        ConfigurationDocument(
            id="firewall_posture_summary",
            title="Firewall Posture Summary",
            updated_at=updated_at,
            text=_render_firewall_doc(
                updated_at,
                controller,
                context,
                site_records,
                include_macs,
                include_serials,
                include_public_ip,
            ),
        ),
        ConfigurationDocument(
            id="port_profiles_summary",
            title="Port Profiles Summary",
            updated_at=updated_at,
            text=_render_port_profiles_doc(
                updated_at,
                controller,
                context,
                site_records,
                include_macs,
                include_serials,
                include_public_ip,
            ),
        ),
    ]


def _base_header(title: str, updated_at: str, controller: str, site_context: str) -> list[str]:
    return [
        f"# {title}",
        f"- Generated (UTC): {updated_at}",
        f"- Controller: {controller}",
        f"- Site context: {site_context}",
        "",
    ]


def _render_inventory_doc(
    updated_at: str,
    controller: str,
    site_context: str,
    site_records: list[dict[str, Any]],
    include_macs: bool,
    include_serials: bool,
    include_public_ip: bool,
) -> str:
    lines = _base_header("Inventory Snapshot", updated_at, controller, site_context)
    lines.append("## Summary")

    for record in site_records:
        devices = record["devices"]
        clients = record["clients"]
        networks = record["networks"]
        wlans = record["wlans"]
        online = sum(1 for device in devices if device.get("state") == 1)
        lines.extend(
            [
                f"- Site: {record['site_name']} ({record['site_id']})",
                f"  - Devices: {len(devices)} ({online} online)",
                f"  - Clients (known): {len(clients)}",
                f"  - Networks: {len(networks)}",
                f"  - SSIDs: {len(wlans)}",
            ]
        )

    raw_payload = {
        "sites": [
            {
                "site_id": rec["site_id"],
                "site_name": rec["site_name"],
                "sample_device": rec["devices"][0] if rec["devices"] else {},
                "sample_wan": rec["wans"][0] if rec["wans"] else {},
            }
            for rec in site_records
        ]
    }

    return _append_raw_json(
        lines,
        raw_payload,
        include_macs=include_macs,
        include_serials=include_serials,
        include_public_ip=include_public_ip,
    )


def _render_networks_doc(
    updated_at: str,
    controller: str,
    site_context: str,
    site_records: list[dict[str, Any]],
    include_macs: bool,
    include_serials: bool,
    include_public_ip: bool,
) -> str:
    lines = _base_header("Networks, VLANs, and Subnets", updated_at, controller, site_context)
    lines.append("## Networks")

    raw_payload: dict[str, Any] = {"sites": []}
    for record in site_records:
        lines.append(f"### Site: {record['site_name']} ({record['site_id']})")
        networks = record["networks"]
        if not networks:
            lines.append("- No networks returned")
            continue

        for network in networks:
            vlan = network.get("vlan_id") or network.get("vlan") or "none"
            subnet = network.get("ip_subnet") or "n/a"
            dhcp_enabled = bool(network.get("dhcpd_enabled", False))
            lines.append(
                f"- {network.get('name', 'Unnamed')} | purpose={network.get('purpose', 'unknown')} | vlan={vlan} | subnet={subnet} | dhcp={dhcp_enabled}"
            )

        raw_payload["sites"].append(
            {
                "site_id": record["site_id"],
                "networks": networks[:8],
            }
        )

    return _append_raw_json(
        lines,
        raw_payload,
        include_macs=include_macs,
        include_serials=include_serials,
        include_public_ip=include_public_ip,
    )


def _render_wifi_doc(
    updated_at: str,
    controller: str,
    site_context: str,
    site_records: list[dict[str, Any]],
    include_macs: bool,
    include_serials: bool,
    include_public_ip: bool,
) -> str:
    lines = _base_header("Wi-Fi SSIDs and Security", updated_at, controller, site_context)
    lines.append("## SSID Posture")

    raw_payload: dict[str, Any] = {"sites": []}
    for record in site_records:
        lines.append(f"### Site: {record['site_name']} ({record['site_id']})")
        wlans = record["wlans"]
        if not wlans:
            lines.append("- No SSIDs returned")
            continue

        for wlan in wlans:
            lines.append(
                "- "
                f"{wlan.get('name', 'Unnamed')} | "
                f"enabled={bool(wlan.get('enabled', False))} | "
                f"security={wlan.get('security', 'unknown')} | "
                f"guest={bool(wlan.get('is_guest', False))} | "
                f"vlan={wlan.get('vlan') if wlan.get('vlan') is not None else 'none'}"
            )

        raw_payload["sites"].append(
            {
                "site_id": record["site_id"],
                "wlans": wlans[:12],
            }
        )

    return _append_raw_json(
        lines,
        raw_payload,
        include_macs=include_macs,
        include_serials=include_serials,
        include_public_ip=include_public_ip,
    )


def _render_firewall_doc(
    updated_at: str,
    controller: str,
    site_context: str,
    site_records: list[dict[str, Any]],
    include_macs: bool,
    include_serials: bool,
    include_public_ip: bool,
) -> str:
    lines = _base_header("Firewall Posture Summary", updated_at, controller, site_context)
    lines.append("## Rule Summary")

    raw_payload: dict[str, Any] = {"sites": []}
    for record in site_records:
        rules = record["firewall_rules"]
        enabled_count = sum(1 for rule in rules if rule.get("enabled", True))
        action_counts: dict[str, int] = {}

        for rule in rules:
            action = str(rule.get("action", "unknown")).lower()
            action_counts[action] = action_counts.get(action, 0) + 1

        lines.append(f"### Site: {record['site_name']} ({record['site_id']})")
        lines.append(f"- Total rules: {len(rules)}")
        lines.append(f"- Enabled rules: {enabled_count}")
        if action_counts:
            lines.append(
                "- Action mix: "
                + ", ".join(f"{action}={count}" for action, count in sorted(action_counts.items()))
            )
        else:
            lines.append("- Action mix: none")

        raw_payload["sites"].append(
            {
                "site_id": record["site_id"],
                "firewall_rules": rules[:20],
            }
        )

    return _append_raw_json(
        lines,
        raw_payload,
        include_macs=include_macs,
        include_serials=include_serials,
        include_public_ip=include_public_ip,
    )


def _render_port_profiles_doc(
    updated_at: str,
    controller: str,
    site_context: str,
    site_records: list[dict[str, Any]],
    include_macs: bool,
    include_serials: bool,
    include_public_ip: bool,
) -> str:
    lines = _base_header("Port Profiles Summary", updated_at, controller, site_context)
    lines.append("## Profiles")

    raw_payload: dict[str, Any] = {"sites": []}
    for record in site_records:
        profiles = record["port_profiles"]
        lines.append(f"### Site: {record['site_name']} ({record['site_id']})")

        if not profiles:
            lines.append("- No port profiles returned (endpoint unavailable or none configured)")
        else:
            for profile in profiles:
                profile_name = profile.get("name", "Unnamed")
                native_network = (
                    profile.get("native_networkconf_id")
                    or profile.get("native_network")
                    or "default"
                )
                poe_mode = profile.get("poe_mode") or profile.get("poe") or "unknown"
                lines.append(
                    f"- {profile_name} | native_network={native_network} | poe={poe_mode}"
                )

        raw_payload["sites"].append(
            {
                "site_id": record["site_id"],
                "port_profiles": profiles[:20],
            }
        )

    return _append_raw_json(
        lines,
        raw_payload,
        include_macs=include_macs,
        include_serials=include_serials,
        include_public_ip=include_public_ip,
    )


def _append_raw_json(
    lines: list[str],
    payload: dict[str, Any],
    include_macs: bool,
    include_serials: bool,
    include_public_ip: bool,
) -> str:
    redacted = _redact_payload(
        payload,
        include_macs=include_macs,
        include_serials=include_serials,
        include_public_ip=include_public_ip,
    )

    lines.extend(
        [
            "",
            "## Raw (redacted) JSON",
            "```json",
            json.dumps(redacted, indent=2, sort_keys=True),
            "```",
        ]
    )
    return "\n".join(lines)


def _site_context(site_records: list[dict[str, Any]]) -> str:
    if not site_records:
        return "No sites returned"
    return ", ".join(f"{site['site_name']} ({site['site_id']})" for site in site_records)


def _controller_label(settings: Settings, include_public_ip: bool) -> str:
    parsed = urlparse(settings.base_url)
    host = parsed.hostname or settings.base_url
    port = parsed.port

    safe_host = host
    if _is_public_ip(host) and not include_public_ip:
        safe_host = "REDACTED_PUBLIC_IP"

    scheme = parsed.scheme or "https"
    if port:
        return f"{scheme}://{safe_host}:{port}"
    return f"{scheme}://{safe_host}"


async def _get_sites(client: UniFiClient, settings: Settings) -> list[dict[str, Any]]:
    endpoint = "/ea/sites"
    if settings.api_type.value == "local":
        endpoint = settings.get_integration_path("sites")

    response = await _safe_get(client, endpoint)
    if isinstance(response, list):
        return response
    return []


async def _safe_get(client: UniFiClient, endpoint: str) -> list[dict[str, Any]]:
    try:
        response = await client.get(endpoint)
        if isinstance(response, list):
            return [item for item in response if isinstance(item, dict)]
        if isinstance(response, dict):
            data = response.get("data", [])
            if isinstance(data, list):
                return [item for item in data if isinstance(item, dict)]
        return []
    except Exception as exc:
        logger.warning("Failed to fetch endpoint %s: %s", endpoint, exc)
        return []


def _site_id(site: dict[str, Any]) -> str:
    value = site.get("id") or site.get("_id") or site.get("site_id") or site.get("name") or ""
    return str(value)


def _build_snippet(text: str, query_lower: str, length: int = 320) -> str:
    normalized = " ".join(text.split())
    idx = normalized.lower().find(query_lower)
    if idx < 0:
        return normalized[:length]

    start = max(idx - 100, 0)
    end = min(start + length, len(normalized))
    return normalized[start:end]


def _redact_payload(
    value: Any,
    include_macs: bool,
    include_serials: bool,
    include_public_ip: bool,
    key: str | None = None,
) -> Any:
    if isinstance(value, dict):
        return {
            dict_key: _redact_payload(
                dict_value,
                include_macs=include_macs,
                include_serials=include_serials,
                include_public_ip=include_public_ip,
                key=dict_key,
            )
            for dict_key, dict_value in value.items()
        }

    if isinstance(value, list):
        return [
            _redact_payload(
                item,
                include_macs=include_macs,
                include_serials=include_serials,
                include_public_ip=include_public_ip,
                key=key,
            )
            for item in value
        ]

    if not isinstance(value, str):
        return value

    normalized_key = (key or "").lower()

    if normalized_key in SENSITIVE_ALWAYS_REDACT:
        return "REDACTED"

    if any(marker in normalized_key for marker in MAC_KEY_MARKERS) and not include_macs:
        return "REDACTED"

    if any(marker in normalized_key for marker in SERIAL_KEY_MARKERS) and not include_serials:
        return "REDACTED"

    if _looks_like_mac(value) and not include_macs:
        return "REDACTED"

    if _looks_like_serial(value) and any(marker in normalized_key for marker in SERIAL_KEY_MARKERS):
        if not include_serials:
            return "REDACTED"

    is_public_ip_context = any(marker in normalized_key for marker in PUBLIC_IP_KEY_MARKERS)
    if is_public_ip_context and _looks_like_ip(value) and not include_public_ip:
        return "REDACTED_PUBLIC_IP"

    return value


def _looks_like_mac(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}", value))


def _looks_like_serial(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9\-]{6,}", value))


def _looks_like_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
    except ValueError:
        return False
    return True


def _is_public_ip(value: str) -> bool:
    try:
        ip_value = ipaddress.ip_address(value)
    except ValueError:
        return False

    return not (
        ip_value.is_private
        or ip_value.is_loopback
        or ip_value.is_link_local
        or ip_value.is_multicast
        or ip_value.is_reserved
    )
