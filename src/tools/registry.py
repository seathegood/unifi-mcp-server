"""MCP tool metadata and safety classification.

This registry is used as a source of truth for tool safety semantics:
- read_only: no side effects, safe by default
- mutating: creates/updates/deletes state or triggers actions
- risky_read: read-only, but may return sensitive information
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ToolClass = Literal["read_only", "mutating", "risky_read"]


@dataclass(frozen=True)
class ToolMetadata:
    """Metadata for a single MCP tool."""

    name: str
    classification: ToolClass
    summary: str


# NOTE:
# FastMCP read-only annotations are not used here because this repository
# supports a broad FastMCP version range. We keep tool semantics in this
# registry and surface them in docs.
READ_ONLY_HINTS_SUPPORTED = False


TOOL_NAMES: tuple[str, ...] = (
    "health_check",
    "search",
    "fetch",
    "debug_api_request",
    "get_device_details",
    "get_device_statistics",
    "list_devices_by_type",
    "search_devices",
    "get_client_details",
    "get_client_statistics",
    "list_active_clients",
    "search_clients",
    "get_network_details",
    "list_vlans",
    "get_subnet_info",
    "get_network_statistics",
    "get_site_details",
    "list_all_sites",
    "get_site_statistics",
    "list_firewall_rules",
    "create_firewall_rule",
    "update_firewall_rule",
    "delete_firewall_rule",
    "trigger_backup",
    "list_backups",
    "get_backup_details",
    "download_backup",
    "delete_backup",
    "restore_backup",
    "validate_backup",
    "get_backup_status",
    "get_restore_status",
    "schedule_backups",
    "get_backup_schedule",
    "create_network",
    "update_network",
    "delete_network",
    "restart_device",
    "locate_device",
    "upgrade_device",
    "block_client",
    "unblock_client",
    "reconnect_client",
    "list_wlans",
    "create_wlan",
    "update_wlan",
    "delete_wlan",
    "get_wlan_statistics",
    "list_port_forwards",
    "create_port_forward",
    "delete_port_forward",
    "get_dpi_statistics",
    "list_top_applications",
    "get_client_dpi",
    "get_application_info",
    "list_pending_devices",
    "adopt_device",
    "execute_port_action",
    "authorize_guest",
    "limit_bandwidth",
    "list_vouchers",
    "get_voucher",
    "create_vouchers",
    "delete_voucher",
    "bulk_delete_vouchers",
    "list_radius_profiles",
    "get_radius_profile",
    "create_radius_profile",
    "update_radius_profile",
    "delete_radius_profile",
    "list_radius_accounts",
    "create_radius_account",
    "delete_radius_account",
    "get_guest_portal_config",
    "configure_guest_portal",
    "list_hotspot_packages",
    "create_hotspot_package",
    "delete_hotspot_package",
    "list_firewall_zones",
    "create_firewall_zone",
    "update_firewall_zone",
    "list_qos_profiles",
    "get_qos_profile",
    "create_qos_profile",
    "update_qos_profile",
    "delete_qos_profile",
    "list_proav_templates",
    "create_proav_profile",
    "validate_proav_profile",
    "get_smart_queue_config",
    "configure_smart_queue",
    "disable_smart_queue",
    "list_traffic_routes",
    "create_traffic_route",
    "update_traffic_route",
    "delete_traffic_route",
    "list_acl_rules",
    "get_acl_rule",
    "create_acl_rule",
    "update_acl_rule",
    "delete_acl_rule",
    "list_wan_connections",
    "list_dpi_categories",
    "list_dpi_applications",
    "list_countries",
    "assign_network_to_zone",
    "get_zone_networks",
    "delete_firewall_zone",
    "unassign_network_from_zone",
    "get_traffic_flows",
    "get_flow_statistics",
    "get_traffic_flow_details",
    "get_top_flows",
    "get_flow_risks",
    "get_flow_trends",
    "filter_traffic_flows",
    "list_traffic_matching_lists",
    "get_traffic_matching_list",
    "create_traffic_matching_list",
    "update_traffic_matching_list",
    "delete_traffic_matching_list",
    "get_network_topology",
    "get_device_connections",
    "get_port_mappings",
    "export_topology",
    "get_topology_statistics",
    "list_vpn_tunnels",
    "list_vpn_servers",
    "list_site_to_site_vpns",
    "get_site_to_site_vpn",
    "update_site_to_site_vpn",
    "list_device_tags",
    "list_all_sites_aggregated",
    "get_internet_health",
    "get_site_health_summary",
    "get_cross_site_statistics",
    "list_vantage_points",
    "get_site_inventory",
    "compare_site_performance",
    "search_across_sites",
)


RISKY_READ_TOOLS: set[str] = {
    "debug_api_request",
    "get_device_details",
    "get_device_statistics",
    "list_devices_by_type",
    "search_devices",
    "get_client_details",
    "get_client_statistics",
    "list_active_clients",
    "search_clients",
    "get_client_dpi",
    "list_pending_devices",
    "get_backup_details",
    "download_backup",
    "get_backup_status",
    "get_restore_status",
    "get_network_topology",
    "get_device_connections",
    "get_port_mappings",
    "get_site_inventory",
    "search_across_sites",
}


MUTATING_PREFIXES: tuple[str, ...] = (
    "create_",
    "update_",
    "delete_",
    "trigger_",
    "restore_",
    "schedule_",
    "restart_",
    "locate_",
    "upgrade_",
    "block_",
    "unblock_",
    "reconnect_",
    "adopt_",
    "authorize_",
    "limit_",
    "configure_",
    "disable_",
    "assign_",
    "unassign_",
    "bulk_delete_",
)


MUTATING_TOOL_OVERRIDES: set[str] = {
    "execute_port_action",
}


def classify_tool(tool_name: str) -> ToolClass:
    """Classify a tool by side-effect and sensitivity level."""
    if tool_name in MUTATING_TOOL_OVERRIDES or tool_name.startswith(MUTATING_PREFIXES):
        return "mutating"
    if tool_name in RISKY_READ_TOOLS:
        return "risky_read"
    return "read_only"


def get_tool_registry() -> dict[str, ToolMetadata]:
    """Return metadata for all registered MCP tools."""
    return {
        tool_name: ToolMetadata(
            name=tool_name,
            classification=classify_tool(tool_name),
            summary=tool_name.replace("_", " "),
        )
        for tool_name in TOOL_NAMES
    }


TOOL_REGISTRY = get_tool_registry()
