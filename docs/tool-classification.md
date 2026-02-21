# MCP Tool Classification

This table is generated from `src/tools/registry.py` and defines server-side safety semantics.

## Handling Conventions

- `read_only`: safe for standard retrieval workflows.
- `risky_read`: still read-only, but responses require redaction-aware handling.
- `mutating`: must use plan/apply workflow and explicit caller confirmation.
- Plan/apply scaffolding is implemented in `src/tools/change_control.py`.

## Summary

- `read_only`: 63 tools
- `mutating`: 57 tools
- `risky_read`: 20 tools

## Classification Table

| Tool | Classification | Notes |
| --- | --- | --- |
| `adopt_device` | `mutating` | Creates/updates/deletes/triggers actions |
| `assign_network_to_zone` | `mutating` | Creates/updates/deletes/triggers actions |
| `authorize_guest` | `mutating` | Creates/updates/deletes/triggers actions |
| `block_client` | `mutating` | Creates/updates/deletes/triggers actions |
| `bulk_delete_vouchers` | `mutating` | Creates/updates/deletes/triggers actions |
| `compare_site_performance` | `read_only` | No side effects |
| `configure_guest_portal` | `mutating` | Creates/updates/deletes/triggers actions |
| `configure_smart_queue` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_acl_rule` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_firewall_rule` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_firewall_zone` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_hotspot_package` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_network` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_port_forward` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_proav_profile` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_qos_profile` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_radius_account` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_radius_profile` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_traffic_matching_list` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_traffic_route` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_vouchers` | `mutating` | Creates/updates/deletes/triggers actions |
| `create_wlan` | `mutating` | Creates/updates/deletes/triggers actions |
| `debug_api_request` | `risky_read` | Read-only but may expose sensitive details |
| `delete_acl_rule` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_backup` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_firewall_rule` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_firewall_zone` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_hotspot_package` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_network` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_port_forward` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_qos_profile` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_radius_account` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_radius_profile` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_traffic_matching_list` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_traffic_route` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_voucher` | `mutating` | Creates/updates/deletes/triggers actions |
| `delete_wlan` | `mutating` | Creates/updates/deletes/triggers actions |
| `disable_smart_queue` | `mutating` | Creates/updates/deletes/triggers actions |
| `download_backup` | `risky_read` | Read-only but may expose sensitive details |
| `execute_port_action` | `mutating` | Creates/updates/deletes/triggers actions |
| `export_topology` | `read_only` | No side effects |
| `fetch` | `read_only` | No side effects |
| `filter_traffic_flows` | `read_only` | No side effects |
| `get_acl_rule` | `read_only` | No side effects |
| `get_application_info` | `read_only` | No side effects |
| `get_backup_details` | `risky_read` | Read-only but may expose sensitive details |
| `get_backup_schedule` | `read_only` | No side effects |
| `get_backup_status` | `risky_read` | Read-only but may expose sensitive details |
| `get_client_details` | `risky_read` | Read-only but may expose sensitive details |
| `get_client_dpi` | `risky_read` | Read-only but may expose sensitive details |
| `get_client_statistics` | `risky_read` | Read-only but may expose sensitive details |
| `get_cross_site_statistics` | `read_only` | No side effects |
| `get_device_connections` | `risky_read` | Read-only but may expose sensitive details |
| `get_device_details` | `risky_read` | Read-only but may expose sensitive details |
| `get_device_statistics` | `risky_read` | Read-only but may expose sensitive details |
| `get_dpi_statistics` | `read_only` | No side effects |
| `get_flow_risks` | `read_only` | No side effects |
| `get_flow_statistics` | `read_only` | No side effects |
| `get_flow_trends` | `read_only` | No side effects |
| `get_guest_portal_config` | `read_only` | No side effects |
| `get_internet_health` | `read_only` | No side effects |
| `get_network_details` | `read_only` | No side effects |
| `get_network_statistics` | `read_only` | No side effects |
| `get_network_topology` | `risky_read` | Read-only but may expose sensitive details |
| `get_port_mappings` | `risky_read` | Read-only but may expose sensitive details |
| `get_qos_profile` | `read_only` | No side effects |
| `get_radius_profile` | `read_only` | No side effects |
| `get_restore_status` | `risky_read` | Read-only but may expose sensitive details |
| `get_site_details` | `read_only` | No side effects |
| `get_site_health_summary` | `read_only` | No side effects |
| `get_site_inventory` | `risky_read` | Read-only but may expose sensitive details |
| `get_site_statistics` | `read_only` | No side effects |
| `get_site_to_site_vpn` | `read_only` | No side effects |
| `get_smart_queue_config` | `read_only` | No side effects |
| `get_subnet_info` | `read_only` | No side effects |
| `get_top_flows` | `read_only` | No side effects |
| `get_topology_statistics` | `read_only` | No side effects |
| `get_traffic_flow_details` | `read_only` | No side effects |
| `get_traffic_flows` | `read_only` | No side effects |
| `get_traffic_matching_list` | `read_only` | No side effects |
| `get_voucher` | `read_only` | No side effects |
| `get_wlan_statistics` | `read_only` | No side effects |
| `get_zone_networks` | `read_only` | No side effects |
| `health_check` | `read_only` | No side effects |
| `limit_bandwidth` | `mutating` | Creates/updates/deletes/triggers actions |
| `list_acl_rules` | `read_only` | No side effects |
| `list_active_clients` | `risky_read` | Read-only but may expose sensitive details |
| `list_all_sites` | `read_only` | No side effects |
| `list_all_sites_aggregated` | `read_only` | No side effects |
| `list_backups` | `read_only` | No side effects |
| `list_countries` | `read_only` | No side effects |
| `list_device_tags` | `read_only` | No side effects |
| `list_devices_by_type` | `risky_read` | Read-only but may expose sensitive details |
| `list_dpi_applications` | `read_only` | No side effects |
| `list_dpi_categories` | `read_only` | No side effects |
| `list_firewall_rules` | `read_only` | No side effects |
| `list_firewall_zones` | `read_only` | No side effects |
| `list_hotspot_packages` | `read_only` | No side effects |
| `list_pending_devices` | `risky_read` | Read-only but may expose sensitive details |
| `list_port_forwards` | `read_only` | No side effects |
| `list_proav_templates` | `read_only` | No side effects |
| `list_qos_profiles` | `read_only` | No side effects |
| `list_radius_accounts` | `read_only` | No side effects |
| `list_radius_profiles` | `read_only` | No side effects |
| `list_site_to_site_vpns` | `read_only` | No side effects |
| `list_top_applications` | `read_only` | No side effects |
| `list_traffic_matching_lists` | `read_only` | No side effects |
| `list_traffic_routes` | `read_only` | No side effects |
| `list_vantage_points` | `read_only` | No side effects |
| `list_vlans` | `read_only` | No side effects |
| `list_vouchers` | `read_only` | No side effects |
| `list_vpn_servers` | `read_only` | No side effects |
| `list_vpn_tunnels` | `read_only` | No side effects |
| `list_wan_connections` | `read_only` | No side effects |
| `list_wlans` | `read_only` | No side effects |
| `locate_device` | `mutating` | Creates/updates/deletes/triggers actions |
| `reconnect_client` | `mutating` | Creates/updates/deletes/triggers actions |
| `restart_device` | `mutating` | Creates/updates/deletes/triggers actions |
| `restore_backup` | `mutating` | Creates/updates/deletes/triggers actions |
| `schedule_backups` | `mutating` | Creates/updates/deletes/triggers actions |
| `search` | `read_only` | No side effects |
| `search_across_sites` | `risky_read` | Read-only but may expose sensitive details |
| `search_clients` | `risky_read` | Read-only but may expose sensitive details |
| `search_devices` | `risky_read` | Read-only but may expose sensitive details |
| `trigger_backup` | `mutating` | Creates/updates/deletes/triggers actions |
| `unassign_network_from_zone` | `mutating` | Creates/updates/deletes/triggers actions |
| `unblock_client` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_acl_rule` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_firewall_rule` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_firewall_zone` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_network` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_qos_profile` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_radius_profile` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_site_to_site_vpn` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_traffic_matching_list` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_traffic_route` | `mutating` | Creates/updates/deletes/triggers actions |
| `update_wlan` | `mutating` | Creates/updates/deletes/triggers actions |
| `upgrade_device` | `mutating` | Creates/updates/deletes/triggers actions |
| `validate_backup` | `read_only` | No side effects |
| `validate_proav_profile` | `read_only` | No side effects |
